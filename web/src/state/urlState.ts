/** The shareable part of the app state, kept in the URL query string. */
import { inBounds } from '../geo/distance.js'
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
  return {
    date: parseDate(params.get('date'), today, window, historyStart),
    spot: parseSpot(params, region),
    view,
    comune: comune && COMUNE_CODE.test(comune) ? comune : null,
    season: parseSeason(params.get('season'), view, today, historyStart),
  }
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
  const search = params.toString()
  return search ? `?${search}` : ''
}
