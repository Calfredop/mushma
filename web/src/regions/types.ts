/**
 * Region registry types: pure data, no `import.meta.env`. Build-time scripts import these
 * modules directly through Vite's config loader, which does not define `import.meta.env`.
 */
import type { LngLatBoundsLike } from 'maplibre-gl'
import type { Species } from '../state/urlState.js'

/** SEO title/description and the visible intro for one locale. */
export interface RegionLocaleCopy {
  seo: {
    region: { title: string; description: string }
    porcini: { title: string; description: string }
    ovoli: { title: string; description: string }
    gallinacci: { title: string; description: string }
  }
  intro: {
    region: string
    porcini: string
    ovoli: string
    gallinacci: string
  }
  /** schema.org Dataset names for the region and each species page. */
  dataset: {
    region: string
    porcini: string
    ovoli: string
    gallinacci: string
  }
}

export interface RegionDefinition {
  /** Path segment (`/toscana`) and registry key. */
  slug: string
  name: { it: string; en: string }
  /**
   * "In the region" with the region's own preposition, when `in <name>` is wrong: Italian says
   * "nelle Marche", "nel Lazio". Omitted, it is `in <name>` (see `regionLocative`).
   */
  locative?: { it: string; en: string }
  /**
   * The whole region, as the area picker offers it: "Tutta la Toscana", "Tutto il Piemonte",
   * "Tutte le Marche", "Tutta l'Umbria". Required: the article and agreement differ by region.
   */
  whole: { it: string; en: string }
  bounds: [[number, number], [number, number]]
  maxBounds: LngLatBoundsLike
  minZoom: number
  maxZoom: number
  species: Species[]
  /** The API's region id (`tuscany`, `umbria`, `emilia_romagna`). */
  apiRegionId: string
  /** Wikidata item id, e.g. `Q1273`: the region's `sameAs` in the pages' JSON-LD. */
  wikidata: string
  /**
   * The first day with scores: the weather history starts in 2016
   * (.gavin-root/docs/weather-ingest.md).
   */
  historyStart: string
  /** Per-locale SEO title/description, intro and Dataset names. */
  copy: { it: RegionLocaleCopy; en: RegionLocaleCopy }
}

export type Bounds = [[number, number], [number, number]]
