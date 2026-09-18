/** The shareable part of the app state, kept in the URL query string. */
import { inBounds } from '../geo/distance'
import { type IsoDate, daysBetween } from '../time/days'

type Bounds = [[number, number], [number, number]]

export const SPECIES = ['porcini', 'ovoli', 'gallinacci'] as const
export const SPECIES_OR_COMBINED = [...SPECIES, 'combined'] as const
export type Species = (typeof SPECIES)[number]
export type SpeciesOrCombined = (typeof SPECIES_OR_COMBINED)[number]

export const DEFAULT_SPECIES: SpeciesOrCombined = 'porcini'

export type Spot =
  { kind: 'cell'; cellId: string } | { kind: 'point'; lat: number; lon: number }

export interface UrlState {
  species: SpeciesOrCombined
  date: IsoDate
  spot: Spot | null
}

export interface DateWindowSize {
  pastDays: number
  forecastDays: number
}

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/
const POINT_DECIMALS = 5 // ~1 m, far finer than a 1 km cell

function isSpeciesOrCombined(value: string | null): value is SpeciesOrCombined {
  return SPECIES_OR_COMBINED.includes(value as SpeciesOrCombined)
}

/** A real calendar day: 2026-09-31 must not become 1 October. */
function isCalendarDate(value: string): boolean {
  if (!ISO_DATE.test(value)) return false
  const parsed = new Date(`${value}T00:00:00Z`)
  return !Number.isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value
}

function inWindow(date: IsoDate, today: IsoDate, window: DateWindowSize): boolean {
  const offset = daysBetween(today, date)
  return offset >= -window.pastDays && offset <= window.forecastDays
}

function parseDate(
  value: string | null,
  today: IsoDate,
  window: DateWindowSize,
): IsoDate {
  if (!value || !isCalendarDate(value)) return today
  return inWindow(value, today, window) ? value : today
}

/**
 * After midnight in Rome: a date that meant "today" follows the new today, and
 * one that has fallen out of the served window returns to it.
 */
export function rollToday(
  date: IsoDate,
  previousToday: IsoDate,
  today: IsoDate,
  window?: DateWindowSize,
): IsoDate {
  if (date === previousToday) return today
  if (window && !inWindow(date, today, window)) return today
  return date
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
): UrlState {
  const params = new URLSearchParams(search)
  const species = params.get('species')
  return {
    species: isSpeciesOrCombined(species) ? species : DEFAULT_SPECIES,
    date: parseDate(params.get('date'), today, window),
    spot: parseSpot(params, region),
  }
}

function round(value: number): number {
  return Number(value.toFixed(POINT_DECIMALS))
}

export function serializeUrlState(state: UrlState, today: IsoDate): string {
  const params = new URLSearchParams()
  if (state.species !== DEFAULT_SPECIES) params.set('species', state.species)
  if (state.date !== today) params.set('date', state.date)
  if (state.spot?.kind === 'cell') params.set('cell', state.spot.cellId)
  if (state.spot?.kind === 'point') {
    params.set('at', `${round(state.spot.lat)},${round(state.spot.lon)}`)
  }
  const search = params.toString()
  return search ? `?${search}` : ''
}
