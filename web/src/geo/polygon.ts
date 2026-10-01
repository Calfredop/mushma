/** Point-in-polygon and distance to a boundary, for WGS84 GeoJSON polygons (`[lon, lat]`). */

type Areal = GeoJSON.Polygon | GeoJSON.MultiPolygon
type Ring = GeoJSON.Position[]

const KM_PER_DEGREE = 111.195

function polygons(geometry: Areal): Ring[][] {
  return geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates
}

/** Even-odd ray casting: a point on an edge may fall either side. */
function inRing(lat: number, lon: number, ring: Ring): boolean {
  let inside = false
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i]
    const [xj, yj] = ring[j]
    if (yi > lat !== yj > lat && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) {
      inside = !inside
    }
  }
  return inside
}

/** Whether the point lies in the geometry: inside an outer ring and outside its holes. */
export function inPolygon(lat: number, lon: number, geometry: Areal): boolean {
  return polygons(geometry).some(
    ([outer, ...holes]) =>
      inRing(lat, lon, outer) && !holes.some((hole) => inRing(lat, lon, hole)),
  )
}

/**
 * Km from the point to the geometry's nearest edge, 0 inside it. Flat-earth over each edge, on a
 * plane scaled for the point's latitude: good to a few metres over the kilometres it is used for.
 */
export function distanceToPolygonKm(lat: number, lon: number, geometry: Areal): number {
  if (inPolygon(lat, lon, geometry)) return 0
  const kx = KM_PER_DEGREE * Math.cos((lat * Math.PI) / 180)
  const ky = KM_PER_DEGREE
  let nearest = Infinity
  for (const rings of polygons(geometry)) {
    for (const ring of rings) {
      for (let i = 1; i < ring.length; i++) {
        const ax = (ring[i - 1][0] - lon) * kx
        const ay = (ring[i - 1][1] - lat) * ky
        const bx = (ring[i][0] - lon) * kx
        const by = (ring[i][1] - lat) * ky
        const dx = bx - ax
        const dy = by - ay
        const length2 = dx * dx + dy * dy
        const t =
          length2 === 0 ? 0 : Math.max(0, Math.min(1, -(ax * dx + ay * dy) / length2))
        nearest = Math.min(nearest, Math.hypot(ax + t * dx, ay + t * dy))
      }
    }
  }
  return nearest
}
