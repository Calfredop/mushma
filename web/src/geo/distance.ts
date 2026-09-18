/** A point this far from a cell centre is outside that ~1 km cell. */
export const OUTSIDE_CELL_KM = 0.75

const EARTH_RADIUS_KM = 6371

/** Great-circle distance in km between two WGS84 points. */
export function distanceKm(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
): number {
  const toRad = (deg: number) => (deg * Math.PI) / 180
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2
  return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(a))
}

export function inBounds(
  lat: number,
  lon: number,
  [[west, south], [east, north]]: [[number, number], [number, number]],
): boolean {
  return lon >= west && lon <= east && lat >= south && lat <= north
}

/**
 * The box around two [lon, lat] points as [south-west, north-east]. MapLibre
 * reads a two-point bounds that way without reordering, and a west corner east
 * of the east corner means "crosses the antimeridian".
 */
export function boundsAround(
  [lon1, lat1]: [number, number],
  [lon2, lat2]: [number, number],
): [[number, number], [number, number]] {
  return [
    [Math.min(lon1, lon2), Math.min(lat1, lat2)],
    [Math.max(lon1, lon2), Math.max(lat1, lat2)],
  ]
}
