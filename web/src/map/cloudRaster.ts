/**
 * Soft score "clouds": one raster over the region. Cell scores are stamped as
 * contiguous 1 km squares in Web Mercator (matching how MapLibre stretches an
 * image source), blurred once, then colourised — so neighbours blend without
 * the lattice/donut artefacts of heatmaps or stacked circle-blur, and land on
 * the same centres as the squircle GeoJSON cells.
 */
import { GOOD_DAYS_CLASSES, SCORE_CLASSES, type ScoreClass } from '../score/scale'

const KM_PER_DEGREE_LAT = 111.32

export type CloudCell = { lon: number; lat: number; score: number }
export type CloudScale = 'score' | 'goodDays'
export type CloudBounds = [[number, number], [number, number]]

/** Max edge length; keeps the paint cheap on phones (~11k cells). */
export const CLOUD_MAX_EDGE = 768

/** Overall opacity of the coloured field over the basemap. */
export const CLOUD_OPACITY = 0.78

/** Blur radius as a fraction of one cell's pixel size. */
export const CLOUD_BLUR_CELLS = 0.55

/**
 * Web Mercator Y in 0…1 (MapLibre / EPSG:3857). Image sources stretch rows
 * linearly in this space between the north and south corners — not in latitude —
 * so the cloud must stamp cells here or they drift ~1 km north mid-Tuscany.
 */
export function mercatorY(lat: number): number {
  const sin = Math.sin((lat * Math.PI) / 180)
  return 0.5 - (Math.log((1 + sin) / (1 - sin)) * 0.25) / Math.PI
}

function hexRgb(hex: string): [number, number, number] {
  const n = Number.parseInt(hex.slice(1), 16)
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255]
}

/** Continuous ramp through the stepped classes so blurred scores don't band. */
export function rampColor(
  value: number,
  classes: readonly ScoreClass[],
): [number, number, number] {
  if (!(value > classes[0].min)) return hexRgb(classes[0].color)
  for (let i = 1; i < classes.length; i++) {
    const prev = classes[i - 1]
    const next = classes[i]
    if (value < next.min) {
      const t = (value - prev.min) / (next.min - prev.min)
      const a = hexRgb(prev.color)
      const b = hexRgb(next.color)
      return [
        Math.round(a[0] + (b[0] - a[0]) * t),
        Math.round(a[1] + (b[1] - a[1]) * t),
        Math.round(a[2] + (b[2] - a[2]) * t),
      ]
    }
  }
  return hexRgb(classes[classes.length - 1].color)
}

export function cloudRasterSize(
  [[west, south], [east, north]]: CloudBounds,
  maxEdge = CLOUD_MAX_EDGE,
): { width: number; height: number } {
  const spanLon = Math.max(east - west, 1e-6)
  const spanLat = Math.max(north - south, 1e-6)
  const minEdge = Math.max(32, Math.round(maxEdge / 8))
  if (spanLon >= spanLat) {
    const width = maxEdge
    return {
      width,
      height: Math.max(minEdge, Math.round(maxEdge * (spanLat / spanLon))),
    }
  }
  const height = maxEdge
  return {
    width: Math.max(minEdge, Math.round(maxEdge * (spanLon / spanLat))),
    height,
  }
}

/** Expand bounds by a fraction of the span so the blur has room at the edges. */
export function paddedCloudBounds(
  [[west, south], [east, north]]: CloudBounds,
  padFraction = 0.02,
): CloudBounds {
  const padLon = (east - west) * padFraction
  const padLat = (north - south) * padFraction
  return [
    [west - padLon, south - padLat],
    [east + padLon, north + padLat],
  ]
}

/** Image world corners for a MapLibre image source: NW, NE, SE, SW. */
export function cloudImageCoordinates([[west, south], [east, north]]: CloudBounds) {
  return [
    [west, north],
    [east, north],
    [east, south],
    [west, south],
  ] as [[number, number], [number, number], [number, number], [number, number]]
}

function blurSeparable(
  input: Float32Array,
  width: number,
  height: number,
  radius: number,
  treatNan = false,
): Float32Array {
  if (radius < 1) return input
  const r = Math.max(1, Math.round(radius))
  const tmp = new Float32Array(input.length)
  const out = new Float32Array(input.length)

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let sum = 0
      let count = 0
      for (let k = -r; k <= r; k++) {
        const xx = x + k
        if (xx < 0 || xx >= width) continue
        const v = input[y * width + xx]
        if (treatNan && Number.isNaN(v)) continue
        sum += v
        count++
      }
      tmp[y * width + x] = count === 0 ? (treatNan ? NaN : 0) : sum / count
    }
  }

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      let sum = 0
      let count = 0
      for (let k = -r; k <= r; k++) {
        const yy = y + k
        if (yy < 0 || yy >= height) continue
        const v = tmp[yy * width + x]
        if (treatNan && Number.isNaN(v)) continue
        sum += v
        count++
      }
      out[y * width + x] = count === 0 ? (treatNan ? NaN : 0) : sum / count
    }
  }
  return out
}

/**
 * Paint woodland cell scores into RGBA image data covering `bounds`.
 * Empty cells stay transparent so the basemap reads underneath.
 */
export function paintCloudRaster(
  cells: readonly CloudCell[],
  bounds: CloudBounds,
  scale: CloudScale,
  sizeKm = 1,
  maxEdge = CLOUD_MAX_EDGE,
): {
  width: number
  height: number
  data: Uint8ClampedArray
  bounds: CloudBounds
  coordinates: ReturnType<typeof cloudImageCoordinates>
} {
  const padded = paddedCloudBounds(bounds)
  const [[west, south], [east, north]] = padded
  const { width, height } = cloudRasterSize(padded, maxEdge)
  const spanLon = east - west
  const myNorth = mercatorY(north)
  const mySouth = mercatorY(south)
  const spanMy = mySouth - myNorth
  const scores = new Float32Array(width * height)
  const mask = new Float32Array(width * height)
  scores.fill(NaN)

  const classes = scale === 'score' ? SCORE_CLASSES : GOOD_DAYS_CLASSES
  const halfLat = sizeKm / 2 / KM_PER_DEGREE_LAT
  const midLat = (south + north) / 2
  const cellH =
    (Math.abs(mercatorY(midLat + halfLat) - mercatorY(midLat - halfLat)) / spanMy) *
    height
  const blurPx = Math.max(1, cellH * CLOUD_BLUR_CELLS)

  for (const cell of cells) {
    // Per-cell lon half-width matches geojson.cellSquare (squircle / hit targets).
    const halfLon =
      sizeKm / 2 / (KM_PER_DEGREE_LAT * Math.cos((cell.lat * Math.PI) / 180))
    const x0 = Math.floor(((cell.lon - halfLon - west) / spanLon) * width)
    const x1 = Math.ceil(((cell.lon + halfLon - west) / spanLon) * width)
    const y0 = Math.floor(((mercatorY(cell.lat + halfLat) - myNorth) / spanMy) * height)
    const y1 = Math.ceil(((mercatorY(cell.lat - halfLat) - myNorth) / spanMy) * height)
    for (let y = Math.max(0, y0); y < Math.min(height, y1); y++) {
      for (let x = Math.max(0, x0); x < Math.min(width, x1); x++) {
        const i = y * width + x
        scores[i] = cell.score
        mask[i] = 1
      }
    }
  }

  const softScores = blurSeparable(scores, width, height, blurPx, true)
  const softMask = blurSeparable(mask, width, height, blurPx, false)
  const rgba = new Uint8ClampedArray(width * height * 4)

  for (let i = 0; i < softScores.length; i++) {
    const a = softMask[i] * CLOUD_OPACITY
    const o = i * 4
    if (a < 0.02 || Number.isNaN(softScores[i])) {
      rgba[o + 3] = 0
      continue
    }
    const [r, g, b] = rampColor(softScores[i], classes)
    rgba[o] = r
    rgba[o + 1] = g
    rgba[o + 2] = b
    rgba[o + 3] = Math.round(Math.min(1, a) * 255)
  }

  return {
    width,
    height,
    data: rgba,
    bounds: padded,
    coordinates: cloudImageCoordinates(padded),
  }
}

export type CloudRaster = ReturnType<typeof paintCloudRaster>

/** Tiny transparent PNG used as the image source placeholder before the first paint. */
export const EMPTY_CLOUD_DATA_URL =
  'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR4nGNgAAIAAAUAAXpeqz8AAAAASUVORK5CYII='

/** Encode painted cloud pixels as a PNG data URL for MapLibre's image source. */
export function cloudRasterDataUrl(raster: CloudRaster): string {
  const canvas = document.createElement('canvas')
  canvas.width = raster.width
  canvas.height = raster.height
  const ctx = canvas.getContext('2d')!
  // Copy into a fresh ImageData: TS DOM types reject a Uint8ClampedArray whose
  // buffer is ArrayBufferLike (SharedArrayBuffer), which Float32→paint paths hit.
  const image = ctx.createImageData(raster.width, raster.height)
  image.data.set(raster.data)
  ctx.putImageData(image, 0, 0)
  return canvas.toDataURL('image/png')
}
