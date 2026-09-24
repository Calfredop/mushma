/** The shareable part of the app state, kept in the URL query string. */
import { inBounds } from '../geo/distance.js'
import { DEFAULT_INDICATOR, isIndicator } from '../score/indicators.js'
import { type IsoDate, daysBetween } from '../time/days.js'

type Bounds = [[number, number], [number, number]]

export const SPECIES = ['porcini', 'ovoli', 'gallinacci'] as const
export const SPECIES_OR_COMBINED = [...SPECIES, 'combined'] as const
export type Species = (typeof SPECIES)[number]
export type SpeciesOrCombined = (typeof SPECIES_OR_COMBINED)[number]

export function isSpeciesOrCombined(value: string | null): value is SpeciesOrCombined {
  return SPECIES_OR_COMBINED.includes(value as SpeciesOrCombined)
}

export type Spot =
  { kind: 'cell'; cellId: string } | { kind: 'point'; lat: number; lon: number }

/** What the sheet shows: hot places now, past seasons, or the seasonal outlook. */
export const VIEWS = ['now', 'seasons', 'outlook'] as const
export type View = (typeof VIEWS)[number]

/** The map's scores, or analysis mode: the factors behind them, one coloured layer each. */
export const MODES = ['map', 'analysis'] as const
export type Mode = (typeof MODES)[number]

/** The species and region live in the path (`routes.ts`); this is everything else. */
export interface UrlState {
  /** Any day from the start of the history to the end of the forecast. */
  date: IsoDate
  spot: Spot | null
  view: View
  /** ISTAT code of the comune the seasons and outlook views look at; null is all of Tuscany. */
  comune: string | null
  /** A past season shown on the map (seasons view only). */
  season: number | null
  mode: Mode
  /**
   * Analysis mode: the factor ids drawn on the map, in the order they were turned on (the last on
   * top). Kept while the mode is off, so turning it back on restores them.
   */
  indicators: string[]
  /**
   * Analysis mode's Bosco toggle: each cell's dominant forest type instead of, or alongside, the
   * factor layers. Its own flag, not one more indicator -- it doesn't depend on species or day,
   * so it isn't cleared or restored by `keepIndicators`. Kept while the mode is off, like the
   * indicators, and defaults to off.
   */
  forest: boolean
}

export interface DateWindowSize {
  pastDays: number
  forecastDays: number
}

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/
const COMUNE_CODE = /^[\w-]{1,32}$/
const POINT_DECIMALS = 5 // ~1 m, far finer than a 1 km cell

/** A real calendar day: 2026-09-31 must not become 1 October. */
function isCalendarDate(value: string): boolean {
  if (!ISO_DATE.test(value)) return false
  const parsed = new Date(`${value}T00:00:00Z`)
  return !Number.isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value
}

/**
 * A servable day: inside the date strip's window, or, with a history, any day from its first
 * day on (a replay) up to the end of the forecast.
 */
function inWindow(
  date: IsoDate,
  today: IsoDate,
  window: DateWindowSize,
  historyStart?: IsoDate,
): boolean {
  const offset = daysBetween(today, date)
  if (offset > window.forecastDays) return false
  if (historyStart !== undefined) return date >= historyStart
  return offset >= -window.pastDays
}

function parseDate(
  value: string | null,
  today: IsoDate,
  window: DateWindowSize,
  historyStart?: IsoDate,
): IsoDate {
  if (!value || !isCalendarDate(value)) return today
  return inWindow(value, today, window, historyStart) ? value : today
}

/**
 * After midnight in Rome: a date that meant "today" follows the new today, and
 * one that is no longer servable returns to it. A replayed past day stays put.
 */
export function rollToday(
  date: IsoDate,
  previousToday: IsoDate,
  today: IsoDate,
  window?: DateWindowSize,
  historyStart?: IsoDate,
): IsoDate {
  if (date === previousToday) return today
  if (window && !inWindow(date, today, window, historyStart)) return today
  return date
}

function parseView(value: string | null): View {
  return VIEWS.includes(value as View) ? (value as View) : 'now'
}

function parseSeason(
  value: string | null,
  view: View,
  today: IsoDate,
  historyStart?: IsoDate,
): number | null {
  if (view !== 'seasons' || !value || !/^\d{4}$/.test(value)) return null
  const year = Number(value)
  const first = historyStart
    ? Number(historyStart.slice(0, 4))
    : Number(today.slice(0, 4))
  return year >= first && year <= Number(today.slice(0, 4)) ? year : null
}

function parseSpot(params: URLSearchParams, region?: Bounds): Spot | null {
  const cellId = params.get('cell')
  if (cellId) return { kind: 'cell', cellId }

  const at = params.get('at')?.split(',')
  if (at?.length !== 2 || at.some((part) => part.trim() === '')) return null
  const [lat, lon] = at.map(Number)
  if (
    !Number.isFinite(lat) ||
    !Number.isFinite(lon) ||
    Math.abs(lat) > 90 ||
    Math.abs(lon) > 180
  ) {
    return null
  }
  if (region && !inBounds(lat, lon, region)) return null
  return { kind: 'point', lat, lon }
}

/** No `f` opens on the default indicator; an empty one means every indicator was turned off. */
function parseIndicators(value: string | null): string[] {
  if (value === null) return [DEFAULT_INDICATOR]
  const ids = value.split(',').filter(isIndicator)
  return [...new Set(ids)]
}

export function parseUrlState(
  search: string,
  today: IsoDate,
  window: DateWindowSize,
  region?: Bounds,
  historyStart?: IsoDate,
): UrlState {
  const params = new URLSearchParams(search)
  const view = parseView(params.get('view'))
  const comune = params.get('comune')
  const mode: Mode = params.get('mode') === 'analysis' ? 'analysis' : 'map'
  return {
    date: parseDate(params.get('date'), today, window, historyStart),
    spot: parseSpot(params, region),
    view,
    comune: comune && COMUNE_CODE.test(comune) ? comune : null,
    season: parseSeason(params.get('season'), view, today, historyStart),
    mode,
    indicators: mode === 'analysis' ? parseIndicators(params.get('f')) : [],
    forest: mode === 'analysis' && params.get('bosco') === '1',
  }
}

// --- Analysis mode -------------------------------------------------------------------------------

/** The species analysis mode opens on in place of "Tutti". */
export const ANALYSIS_SPECIES: Species = 'porcini'

/**
 * Analysis mode has no combined score (a cell's factors come from one species' rules), so "Tutti"
 * becomes porcini. The species lives in the path, so the app state moves the path to match.
 */
export function speciesForMode(
  species: SpeciesOrCombined,
  mode: Mode,
): SpeciesOrCombined {
  return mode === 'analysis' && species === 'combined' ? ANALYSIS_SPECIES : species
}

/** A species switch keeps the mode; in analysis mode "Tutti" can't be picked. */
export function canPickSpecies(species: SpeciesOrCombined, mode: Mode): boolean {
  return !(mode === 'analysis' && species === 'combined')
}

/** Into or out of analysis mode; with nothing on, it opens on the default indicator. */
export function withMode<S extends UrlState>(state: S, mode: Mode): S {
  if (mode === 'map') return state.mode === 'map' ? state : { ...state, mode }
  const indicators =
    state.mode === 'map' && state.indicators.length === 0
      ? [DEFAULT_INDICATOR]
      : state.indicators
  if (state.mode === mode && indicators === state.indicators) return state
  return { ...state, mode, indicators }
}

/**
 * Once a species' indicators are known: keep only the ones it has, in order. If none of them is
 * left, the default indicator (which every species has) comes on instead of a blank map.
 */
export function keepIndicators<S extends UrlState>(
  state: S,
  available: readonly string[],
): S {
  const kept = state.indicators.filter((id) => available.includes(id))
  if (kept.length === state.indicators.length) return state
  const fallback = available.includes(DEFAULT_INDICATOR) ? [DEFAULT_INDICATOR] : []
  return { ...state, indicators: kept.length > 0 ? kept : fallback }
}

/** On goes on top of the stack; off comes out of it. */
export function toggleIndicator<S extends UrlState>(state: S, id: string): S {
  const indicators = state.indicators.includes(id)
    ? state.indicators.filter((other) => other !== id)
    : [...state.indicators, id]
  return { ...state, indicators }
}

/** The Bosco toggle: independent of the indicators, so it can be on with any of them, or alone. */
export function toggleForestLayer<S extends UrlState>(state: S): S {
  return { ...state, forest: !state.forest }
}

function round(value: number): number {
  return Number(value.toFixed(POINT_DECIMALS))
}

export function serializeUrlState(state: UrlState, today: IsoDate): string {
  const params = new URLSearchParams()
  if (state.date !== today) params.set('date', state.date)
  if (state.spot?.kind === 'cell') params.set('cell', state.spot.cellId)
  if (state.spot?.kind === 'point') {
    params.set('at', `${round(state.spot.lat)},${round(state.spot.lon)}`)
  }
  if (state.view !== 'now') params.set('view', state.view)
  if (state.comune) params.set('comune', state.comune)
  if (state.season !== null) params.set('season', String(state.season))
  if (state.mode === 'analysis') {
    params.set('mode', 'analysis')
    params.set('f', state.indicators.join(','))
    if (state.forest) params.set('bosco', '1')
  }
  const search = params.toString()
  return search ? `?${search}` : ''
}
