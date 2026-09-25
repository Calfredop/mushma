/**
 * Region registry: one import line per region. Pure data — no `import.meta.env`.
 * Adding a region means adding its file and one line here.
 */
import { inBounds } from '../geo/distance.js'
import { liguria } from './liguria.js'
import { marche } from './marche.js'
import { toscana } from './toscana.js'
import type { Bounds, RegionDefinition } from './types.js'
import { umbria } from './umbria.js'

export type { Bounds, RegionDefinition, RegionLocaleCopy } from './types.js'

export const REGIONS: Record<string, RegionDefinition> = {
  [toscana.slug]: toscana,
  [umbria.slug]: umbria,
  [liguria.slug]: liguria,
  [marche.slug]: marche,
}

export const DEFAULT_REGION_SLUG = toscana.slug

/** A known slug's region, or the default region for an unknown or missing one. */
export function getRegion(slug: string | undefined): RegionDefinition {
  return (slug !== undefined && REGIONS[slug]) || REGIONS[DEFAULT_REGION_SLUG]
}

/** A known slug's region, or undefined — for callers that must tell "unknown" from "default". */
export function findRegion(slug: string): RegionDefinition | undefined {
  return REGIONS[slug]
}

/** "In the region" in `lang`: the region's `locative`, or `in <name>`. */
export function regionLocative(region: RegionDefinition, lang: 'it' | 'en'): string {
  return region.locative?.[lang] ?? `in ${region.name[lang]}`
}

/** Every served region, in registry order. */
export function listRegions(): RegionDefinition[] {
  return Object.values(REGIONS)
}

/** The first served region whose bbox contains the point, or undefined. */
export function findRegionAt(lat: number, lon: number): RegionDefinition | undefined {
  return listRegions().find((region) => inBounds(lat, lon, region.bounds))
}

/** Union of every served region's bounds, for place search across regions. */
export function servedBounds(): Bounds {
  const regions = listRegions()
  let west = Infinity
  let south = Infinity
  let east = -Infinity
  let north = -Infinity
  for (const region of regions) {
    const [[w, s], [e, n]] = region.bounds
    west = Math.min(west, w)
    south = Math.min(south, s)
    east = Math.max(east, e)
    north = Math.max(north, n)
  }
  return [
    [west, south],
    [east, north],
  ]
}

/** Italy overview frame for the hub map (same bbox as the national basemap extract). */
export const ITALY_BOUNDS: Bounds = [
  [6.6, 35.4],
  [18.6, 47.1],
]

export const LAST_REGION_KEY = 'mushma.lastRegion'

export function readLastRegionSlug(): string | undefined {
  try {
    const slug = localStorage.getItem(LAST_REGION_KEY)
    return slug && REGIONS[slug] ? slug : undefined
  } catch {
    return undefined
  }
}

export function rememberRegion(slug: string): void {
  try {
    if (REGIONS[slug]) localStorage.setItem(LAST_REGION_KEY, slug)
  } catch {
    // private mode / quota: ignore
  }
}

function isStandalone(): boolean {
  return (
    typeof window !== 'undefined' &&
    (window.matchMedia?.('(display-mode: standalone)').matches === true ||
      (window.navigator as { standalone?: boolean }).standalone === true)
  )
}

/**
 * When an installed PWA opens at `/`, send it to the last region if one is stored.
 * Browser visits to `/` stay on the hub.
 */
export function pwaHubRedirectSlug(): string | undefined {
  return isStandalone() ? readLastRegionSlug() : undefined
}
