import { describe, expect, it } from 'vitest'
import {
  CLOUD_OPACITY,
  cloudImageCoordinates,
  cloudRasterSize,
  mercatorY,
  paintCloudRaster,
  paddedCloudBounds,
  rampColor,
} from './cloudRaster'
import { SCORE_CLASSES } from '../score/scale'

/** Latitude at a pixel row as MapLibre maps an image between north and south (Mercator-linear). */
function latAtPixelRow(
  y: number,
  height: number,
  north: number,
  south: number,
): number {
  const myNorth = mercatorY(north)
  const mySouth = mercatorY(south)
  const my = myNorth + ((y + 0.5) / height) * (mySouth - myNorth)
  const n = Math.exp((0.5 - my) * 4 * Math.PI)
  return (Math.asin((n - 1) / (n + 1)) * 180) / Math.PI
}

describe('rampColor', () => {
  it('returns class colours at the breaks and blends between them', () => {
    expect(rampColor(0, SCORE_CLASSES)).toEqual([0xf7, 0xf0, 0xc6])
    expect(rampColor(0.2, SCORE_CLASSES)).toEqual([0xf0, 0xc9, 0x67])
    const mid = rampColor(0.3, SCORE_CLASSES)
    expect(mid[0]).toBeGreaterThan(0xe6)
    expect(mid[0]).toBeLessThan(0xf0)
  })
})

describe('cloudRasterSize', () => {
  it('fits the longer side to the max edge', () => {
    expect(cloudRasterSize([[0, 0], [2, 1]], 100)).toEqual({ width: 100, height: 50 })
    expect(cloudRasterSize([[0, 0], [1, 2]], 100)).toEqual({ width: 50, height: 100 })
  })
})

describe('paintCloudRaster', () => {
  const bounds: [[number, number], [number, number]] = [
    [10, 43],
    [11, 44],
  ]

  it('leaves empty space transparent so the basemap shows through', () => {
    const { data } = paintCloudRaster([], bounds, 'score', 1, 64)
    expect(data.every((v, i) => i % 4 !== 3 || v === 0)).toBe(true)
  })

  it('colours a cell and feathers its edge instead of a hard square', () => {
    // Bounds only a few km across so a 1 km cell spans many pixels.
    const tight: [[number, number], [number, number]] = [
      [10.48, 43.48],
      [10.52, 43.52],
    ]
    const { data, width, height, coordinates } = paintCloudRaster(
      [{ lon: 10.5, lat: 43.5, score: 0.9 }],
      tight,
      'score',
      1,
      128,
    )
    expect(coordinates[0][0]).toBeLessThan(10.48)
    expect(coordinates[1][0]).toBeGreaterThan(10.52)

    let opaque = 0
    let soft = 0
    for (let i = 3; i < data.length; i += 4) {
      const a = data[i]
      if (a > CLOUD_OPACITY * 255 * 0.7) opaque++
      else if (a > 8 && a < CLOUD_OPACITY * 255 * 0.5) soft++
    }
    expect(opaque).toBeGreaterThan(0)
    expect(soft).toBeGreaterThan(0)
    expect(width).toBeGreaterThan(32)
    expect(height).toBeGreaterThan(32)
  })

  it('places a cell where MapLibre will show it (Mercator Y, not equirectangular)', () => {
    // Region-sized bounds: equirectangular paint drifts ~1 km north mid-Tuscany.
    const region: [[number, number], [number, number]] = [
      [9.68, 42.23],
      [12.38, 44.48],
    ]
    const cell = { lon: 11.0, lat: 43.4, score: 0.9 }
    const { data, width, height, bounds: painted } = paintCloudRaster(
      [cell],
      region,
      'score',
      1,
      768,
    )
    const [[, south], [, north]] = painted

    let sumA = 0
    let sumY = 0
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const a = data[(y * width + x) * 4 + 3]
        if (a <= 0) continue
        sumA += a
        sumY += y * a
      }
    }
    expect(sumA).toBeGreaterThan(0)
    const shownLat = latAtPixelRow(sumY / sumA, height, north, south)
    const deltaKm = (shownLat - cell.lat) * 111.32
    // Squircle GeoJSON is the truth; cloud must land within a few hundred metres.
    expect(Math.abs(deltaKm)).toBeLessThan(0.25)
  })

  it('blends neighbouring cells so the midpoint is between their colours', () => {
    // Two adjacent 1 km cells on a fine raster: centres 1 km apart in lon at ~43.5°.
    const lat = 43.5
    const dLon = 1 / (111.32 * Math.cos((lat * Math.PI) / 180))
    const { data, width, height, bounds: painted } = paintCloudRaster(
      [
        { lon: 10.5, lat, score: 0.1 },
        { lon: 10.5 + dLon, lat, score: 0.9 },
      ],
      [
        [10.3, 43.3],
        [10.7 + dLon, 43.7],
      ],
      'score',
      1,
      256,
    )
    const [[west], [east]] = [painted[0], painted[1]]
    const midLon = 10.5 + dLon / 2
    const x = Math.round(((midLon - west) / (east - west)) * (width - 1))
    const y = Math.round(height / 2)
    const o = (y * width + x) * 4
    // Pale straw → porcino brown; midpoint should be neither extreme.
    expect(data[o + 3]).toBeGreaterThan(20)
    expect(data[o]).toBeGreaterThan(0x65)
    expect(data[o]).toBeLessThan(0xf7)
  })
})

describe('paddedCloudBounds', () => {
  it('expands the region a little for blur bleed', () => {
    const padded = paddedCloudBounds([
      [10, 40],
      [12, 42],
    ])
    expect(padded[0][0]).toBeLessThan(10)
    expect(padded[1][1]).toBeGreaterThan(42)
    expect(cloudImageCoordinates(padded)).toHaveLength(4)
  })
})
