/** Build-time settings (Vite env) and region constants. */
import type { DateWindowSize } from './state/urlState'
import { REGIONS, DEFAULT_REGION_SLUG } from './regions'

export * from './regions'

/** `/api` goes through the Vite dev proxy (vite.config.ts) or a host rewrite. */
export const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * Self-hosted basemap and terrain (PRD → Architecture → Basemap): a `.pmtiles`
 * URL or a TileJSON URL. Without a basemap the map draws a plain land fill.
 */
export const BASEMAP_URL: string | undefined =
  import.meta.env.VITE_BASEMAP_URL || undefined
export const TERRAIN_URL: string | undefined =
  import.meta.env.VITE_TERRAIN_URL || undefined

/** The active region, until path routing (`/:region`) picks one per request. */
export const REGION = REGIONS[DEFAULT_REGION_SLUG]

/** Past days → today → +7 on the date strip: the scored window with its factor breakdown. */
export const DATE_WINDOW: DateWindowSize = { pastDays: 6, forecastDays: 7 }

/**
 * The first day a past date can be replayed from: the weather history starts in 2016
 * (.gavin-root/docs/weather-ingest.md). A day the API has no scores for says so on the map.
 */
export const HISTORY_START = '2016-01-01'

/** "Recent" sightings on the map overlay. */
export const SIGHTINGS_WINDOW_DAYS = 90

/** A replayed day shows the sightings of this many days either side of it. */
export const REPLAY_SIGHTINGS_DAYS = 14

export const HOTSPOT_LIMIT = 10

export const CELL_SIZE_KM = 1

/**
 * How old `/status`'s `updated_at` can be before the UI calls it stale (M7). The daily job must
 * finish before 07:00 Europe/Rome (PRD → Constraints → Freshness); this gives it room to run late
 * without a false warning, while still catching a genuinely missed run by the next morning.
 */
export const STALE_DATA_HOURS = 30
