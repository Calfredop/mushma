/** Build-time settings (Vite env) and region constants. */
import type { LngLatBoundsLike } from 'maplibre-gl'
import type { DateWindowSize } from './state/urlState'

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

/**
 * Tuscany, kept in config so another region can be added later (PRD → Current
 * focus). Bounds include the Tuscan Archipelago.
 */
export const REGION = {
  bounds: [
    [9.68, 42.23],
    [12.38, 44.48],
  ] as [[number, number], [number, number]],
  maxBounds: [
    [8.4, 41.5],
    [13.6, 45.2],
  ] as LngLatBoundsLike,
  minZoom: 6,
  maxZoom: 15,
}

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
