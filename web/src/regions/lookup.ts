/**
 * Which served region a point is in, by the regions' simplified boundaries. Its own module: the
 * registry stays pure data for the build scripts, and the boundaries load only when first needed.
 */
import { inBounds } from '../geo/distance.js'
import { distanceToPolygonKm, inPolygon } from '../geo/polygon.js'
import { loadRegionBoundaries, type RegionBoundaries } from './boundaries.js'
import { listRegions, REGIONS } from './index.js'
import type { Bounds, RegionDefinition } from './types.js'

/**
 * A point this close to a served region's boundary counts as in it: the boundaries are simplified
 * to ~500 m, and a fix on the beach can fall just off the coast.
 */
export const NEAR_BOUNDARY_KM = 1

type BoundaryFeature = RegionBoundaries['features'][number]

const extents = new WeakMap<BoundaryFeature, Bounds>()

/** The feature's own bbox, the cheap test before its polygon. */
function extent(feature: BoundaryFeature): Bounds {
  let bounds = extents.get(feature)
  if (!bounds) {
    let west = Infinity
    let south = Infinity
    let east = -Infinity
    let north = -Infinity
    const { geometry } = feature
    const parts =
      geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates
    for (const [outer] of parts) {
      for (const [lon, lat] of outer) {
        west = Math.min(west, lon)
        south = Math.min(south, lat)
        east = Math.max(east, lon)
        north = Math.max(north, lat)
      }
    }
    bounds = [
      [west, south],
      [east, north],
    ]
    extents.set(feature, bounds)
  }
  return bounds
}

/**
 * The served region at a point, by its boundary: the `preferred` (current) region while the point
 * is within NEAR_BOUNDARY_KM of it, else the region holding the point, else the nearest within
 * NEAR_BOUNDARY_KM, else undefined.
 */
export function regionAt(
  lat: number,
  lon: number,
  boundaries: RegionBoundaries,
  preferred?: string,
): RegionDefinition | undefined {
  const padLat = NEAR_BOUNDARY_KM / 111.195
  const padLon = padLat / Math.cos((lat * Math.PI) / 180)
  const near = boundaries.features.filter((feature) => {
    const [[west, south], [east, north]] = extent(feature)
    return (
      REGIONS[feature.properties.slug] !== undefined &&
      inBounds(lat, lon, [
        [west - padLon, south - padLat],
        [east + padLon, north + padLat],
      ])
    )
  })
  const current = near.find((feature) => feature.properties.slug === preferred)
  if (current && distanceToPolygonKm(lat, lon, current.geometry) <= NEAR_BOUNDARY_KM) {
    return REGIONS[current.properties.slug]
  }
  const holding = near.find((feature) => inPolygon(lat, lon, feature.geometry))
  if (holding) return REGIONS[holding.properties.slug]
  let nearest: BoundaryFeature | undefined
  let nearestKm = NEAR_BOUNDARY_KM
  for (const feature of near) {
    const km = distanceToPolygonKm(lat, lon, feature.geometry)
    if (km <= nearestKm) {
      nearest = feature
      nearestKm = km
    }
  }
  return nearest && REGIONS[nearest.properties.slug]
}

let boundariesLoad: Promise<RegionBoundaries> | undefined

/** The boundaries chunk, fetched once; a failed fetch is retried on the next call. */
export function servedBoundaries(): Promise<RegionBoundaries> {
  boundariesLoad ??= loadRegionBoundaries().catch((error: unknown) => {
    boundariesLoad = undefined
    throw error
  })
  return boundariesLoad
}

/**
 * The served region at a point (see regionAt), `preferred` being the region the user is in. If
 * the boundaries can't load (offline, before they were ever fetched), the first bbox holding the
 * point, the preferred region's first.
 */
export async function findRegionAt(
  lat: number,
  lon: number,
  preferred?: string,
): Promise<RegionDefinition | undefined> {
  try {
    return regionAt(lat, lon, await servedBoundaries(), preferred)
  } catch {
    const current = preferred !== undefined ? REGIONS[preferred] : undefined
    if (current && inBounds(lat, lon, current.bounds)) return current
    return listRegions().find((region) => inBounds(lat, lon, region.bounds))
  }
}
