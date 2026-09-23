/**
 * Region registry: pure data, no `import.meta.env`. Build-time scripts (sitemap, prerendered
 * heads) import this module directly — through Vite's own config loader, which does not
 * define `import.meta.env` the way app code served by Vite does — so it must stay free of it.
 * The app imports it via `./config`, which re-exports it alongside the env-dependent settings.
 */
import type { LngLatBoundsLike } from 'maplibre-gl'
import { SPECIES, type Species } from './state/urlState.js'

export interface RegionDefinition {
  /** Path segment (`/toscana`) and registry key. */
  slug: string
  name: { it: string; en: string }
  bounds: [[number, number], [number, number]]
  maxBounds: LngLatBoundsLike
  minZoom: number
  maxZoom: number
  species: Species[]
  /** The API's region id. The API is Tuscany-only for now; unused until a second region ships. */
  apiRegionId: string
  /** Wikidata item id, e.g. `Q1273`: the region's `sameAs` in the pages' JSON-LD. */
  wikidata: string
  /**
   * The first day with scores: the weather history starts in 2016
   * (.gavin-root/docs/weather-ingest.md).
   */
  historyStart: string
}

/**
 * More regions will join Tuscany later (PRD → Current focus), so it's a registry keyed by
 * slug even with one entry. Bounds include the Tuscan Archipelago.
 */
export const REGIONS: Record<string, RegionDefinition> = {
  toscana: {
    slug: 'toscana',
    name: { it: 'Toscana', en: 'Tuscany' },
    bounds: [
      [9.68, 42.23],
      [12.38, 44.48],
    ],
    maxBounds: [
      [8.4, 41.5],
      [13.6, 45.2],
    ],
    minZoom: 6,
    maxZoom: 15,
    species: [...SPECIES],
    apiRegionId: 'tuscany',
    wikidata: 'Q1273',
    historyStart: '2016-01-01',
  },
}

export const DEFAULT_REGION_SLUG = 'toscana'

/** A known slug's region, or the default region for an unknown or missing one. */
export function getRegion(slug: string | undefined): RegionDefinition {
  return (slug !== undefined && REGIONS[slug]) || REGIONS[DEFAULT_REGION_SLUG]
}

/** A known slug's region, or undefined — for callers that must tell "unknown" from "default". */
export function findRegion(slug: string): RegionDefinition | undefined {
  return REGIONS[slug]
}
