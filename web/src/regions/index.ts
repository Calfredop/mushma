/**
 * Region registry: one import line per region. Pure data — no `import.meta.env`.
 * Adding a region means adding its file and one line here.
 */
import { abruzzo } from './abruzzo.js'
import { basilicata } from './basilicata.js'
import { calabria } from './calabria.js'
import { campania } from './campania.js'
import { emiliaRomagna } from './emilia-romagna.js'
import { friuliVeneziaGiulia } from './friuli-venezia-giulia.js'
import { lazio } from './lazio.js'
import { liguria } from './liguria.js'
import { lombardia } from './lombardia.js'
import { marche } from './marche.js'
import { molise } from './molise.js'
import { piemonte } from './piemonte.js'
import { puglia } from './puglia.js'
import { sardegna } from './sardegna.js'
import { sicilia } from './sicilia.js'
import { toscana } from './toscana.js'
import { trentinoAltoAdige } from './trentino-alto-adige.js'
import type { Bounds, RegionDefinition } from './types.js'
import { umbria } from './umbria.js'
import { valleDAosta } from './valle-d-aosta.js'
import { veneto } from './veneto.js'

export type { Bounds, RegionDefinition, RegionLocaleCopy } from './types.js'

/**
 * findRegionAt (lookup.ts) tests each region's boundary, so the order below only matters when the boundaries
 * can't load and it falls back to the first bbox holding the point.
 */
export const REGIONS: Record<string, RegionDefinition> = {
  [toscana.slug]: toscana,
  [umbria.slug]: umbria,
  [liguria.slug]: liguria,
  [emiliaRomagna.slug]: emiliaRomagna,
  [marche.slug]: marche,
  // Before Piemonte, whose bbox holds all of Valle d'Aosta's.
  [valleDAosta.slug]: valleDAosta,
  [piemonte.slug]: piemonte,
  [trentinoAltoAdige.slug]: trentinoAltoAdige,
  [lombardia.slug]: lombardia,
  [friuliVeneziaGiulia.slug]: friuliVeneziaGiulia,
  [campania.slug]: campania,
  [abruzzo.slug]: abruzzo,
  [calabria.slug]: calabria,
  // After Campania and Calabria, before Puglia: Puglia's bbox holds all of Basilicata's, and
  // Basilicata's holds Campania's Vallo di Diano and Calabria's Pollino.
  [basilicata.slug]: basilicata,
  [puglia.slug]: puglia,
  [lazio.slug]: lazio,
  [sicilia.slug]: sicilia,
  [sardegna.slug]: sardegna,
  // Last: Molise's bbox and its neighbours' hold much of each other's woods.
  [molise.slug]: molise,
  // Last: Veneto's bbox and Trentino-Alto Adige's, Lombardia's and Friuli-Venezia Giulia's hold most
  // of each other's woods.
  [veneto.slug]: veneto,
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
export function regionLocative(
  region: Pick<RegionDefinition, 'name' | 'locative'>,
  lang: 'it' | 'en',
): string {
  return region.locative?.[lang] ?? `in ${region.name[lang]}`
}

/** Every served region, in registry order. */
export function listRegions(): RegionDefinition[] {
  return Object.values(REGIONS)
}

/** Whether a region's name holds the typed query, ignoring case and accents. */
export function matchesRegionName(name: string, query: string): boolean {
  const norm = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase()
  return norm(name).includes(norm(query.trim()))
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
