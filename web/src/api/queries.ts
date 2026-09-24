/** TanStack Query hooks over the typed API client. The frontend only reads. */
import {
  queryOptions,
  type UseQueryResult,
  useQueries,
  useQuery,
} from '@tanstack/react-query'
import { useCallback } from 'react'
import { sightingsByCell } from '../map/geojson'
import {
  SPECIES,
  type Species,
  type SpeciesOrCombined,
  type Spot,
} from '../state/urlState'
import { DATE_WINDOW } from '../config'
import { daysBetween, type IsoDate } from '../time/days'
import { apiClient } from './client'
import type { components } from './schema'

export type ScoresResponse = components['schemas']['ScoresResponse']
export type FactorsResponse = components['schemas']['FactorsResponse']
export type FactorChip = components['schemas']['FactorChip']
export type CellFactors = components['schemas']['CellFactors']
export type CellDetailResponse = components['schemas']['CellDetailResponse']
export type HabitatShare = components['schemas']['HabitatShare']
export type HotspotsResponse = components['schemas']['HotspotsResponse']
export type Hotspot = components['schemas']['Hotspot']
export type SpeciesForecast = components['schemas']['SpeciesForecast']
export type DayScore = components['schemas']['DayScore']
export type Comune = components['schemas']['Comune']
export type SeasonsResponse = components['schemas']['SeasonsResponse']
export type SeasonSummary = components['schemas']['SeasonSummary']
export type MonthStat = components['schemas']['MonthStat']
export type SeasonMapResponse = components['schemas']['SeasonMapResponse']
export type ComuneSeason = components['schemas']['ComuneSeason']
export type OutlookResponse = components['schemas']['OutlookResponse']
export type OutlookPeriod = components['schemas']['OutlookPeriod']
export type RainStat = components['schemas']['RainStat']
export type TemperatureStat = components['schemas']['TemperatureStat']
export type StatusResponse = components['schemas']['StatusResponse']
export type PlausibleSpeciesResponse = components['schemas']['PlausibleSpeciesResponse']
export type SpeciesProfile = components['schemas']['SpeciesProfile']
export type TaxonProfile = components['schemas']['TaxonProfile']
export type ForestTypesResponse = components['schemas']['ForestTypesResponse']
export type CellForestType = components['schemas']['CellForestType']

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, path: string) {
    super(`API ${path} answered ${status}`)
    this.status = status
  }
}

type Result<T> = { data?: T; response: Response }

function unwrap<T>(path: string) {
  return ({ data, response }: Result<T>): T => {
    if (data === undefined) throw new ApiError(response.status, path)
    return data
  }
}

const MINUTE = 60_000
const DAY = 24 * 60 * MINUTE

/**
 * The daily job re-scores the date strip's days (today -6 to +7) every morning, so they refresh;
 * an older, replayed day only changes when history is re-scored, so it keeps for a day.
 */
function staleTimeFor(date: IsoDate, today: IsoDate): number {
  return daysBetween(today, date) < -DATE_WINDOW.pastDays ? DAY : 10 * MINUTE
}

export function useScores(
  species: SpeciesOrCombined,
  date: IsoDate,
  today: IsoDate,
  enabled = true,
) {
  return useQuery({
    queryKey: ['scores', species, date],
    enabled,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/scores', { params: { query: { species, date } }, signal })
        .then(unwrap<ScoresResponse>('/scores')),
    staleTime: staleTimeFor(date, today),
    placeholderData: (previous) => previous,
  })
}

/** Analysis mode: every factor behind one species' score, per cell, for one day. Shared by
 * `useFactors` and the play button's prefetch, so both fill the same cache entry. */
export function factorsQuery(species: Species, date: IsoDate, today: IsoDate) {
  return queryOptions({
    queryKey: ['factors', species, date],
    queryFn: ({ signal }) =>
      apiClient
        .GET('/factors', { params: { query: { species, date } }, signal })
        .then(unwrap<FactorsResponse>('/factors')),
    staleTime: staleTimeFor(date, today),
  })
}

export function useFactors(
  species: Species,
  date: IsoDate,
  today: IsoDate,
  enabled = true,
) {
  return useQuery({
    ...factorsQuery(species, date, today),
    enabled,
    // The last day stays drawn while the next loads, but never another species' factors.
    placeholderData: (previous) => (previous?.species === species ? previous : undefined),
  })
}

export function useHotspots(
  species: SpeciesOrCombined,
  date: IsoDate,
  today: IsoDate,
  limit: number,
  enabled = true,
) {
  return useQuery({
    queryKey: ['hotspots', species, date, limit],
    enabled,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/hotspots', { params: { query: { species, date, limit } }, signal })
        .then(unwrap<HotspotsResponse>('/hotspots')),
    staleTime: staleTimeFor(date, today),
  })
}

/** 4xx: the request itself can't be served (unknown cell, date outside the window). */
export function isClientError(error: unknown): boolean {
  return error instanceof ApiError && error.status >= 400 && error.status < 500
}

export function useSpotForecast(spot: Spot | null, today: IsoDate) {
  return useQuery({
    // Keyed on today too: the outlook starts from today, so it moves at midnight.
    queryKey: ['spot', spot, today],
    enabled: spot !== null,
    queryFn: ({ signal }) => {
      if (spot?.kind === 'cell') {
        return apiClient
          .GET('/cells/{cell_id}', { params: { path: { cell_id: spot.cellId } }, signal })
          .then(unwrap<CellDetailResponse>('/cells'))
      }
      if (spot?.kind === 'point') {
        return apiClient
          .GET('/spot', { params: { query: { lat: spot.lat, lon: spot.lon } }, signal })
          .then(unwrap<CellDetailResponse>('/spot'))
      }
      throw new Error('no spot selected')
    },
    staleTime: 10 * MINUTE,
  })
}

/** A span of days for the sightings overlay; `until` omitted means up to now. */
export interface DateRange {
  since: IsoDate
  until?: IsoDate
}

/** Sighting totals per cell for one species, or summed over all of them. */
export function useSightingTotals(
  species: SpeciesOrCombined,
  range: DateRange,
  enabled: boolean,
) {
  const speciesList: readonly Species[] = species === 'combined' ? SPECIES : [species]
  const combine = useCallback(
    (results: UseQueryResult<components['schemas']['SightingsResponse']>[]) => ({
      totals: results.every((r) => r.data)
        ? sightingsByCell(results.map((r) => r.data!))
        : undefined,
      isError: enabled && results.some((r) => r.isError),
    }),
    [enabled],
  )
  const { since, until } = range
  return useQueries({
    queries: speciesList.map((sp) => ({
      queryKey: ['sightings', sp, since, until ?? null],
      enabled,
      queryFn: ({ signal }: { signal: AbortSignal }) =>
        apiClient
          .GET('/sightings', {
            params: { query: { species: sp, since, ...(until ? { until } : {}) } },
            signal,
          })
          .then(unwrap<components['schemas']['SightingsResponse']>('/sightings')),
      staleTime: 60 * MINUTE,
    })),
    // Stable, so totals (a Map) are only rebuilt when the results change.
    combine,
  })
}

// --- Time views (M6) ----------------------------------------------------------------------------

/** Comuni with woodland, for the area picker. Changes only when the grid is rebuilt. */
/** Data freshness (M7): when the pipeline last ran and through which day. Polled, not just
 * fetched once, so a long-open tab picks up tomorrow's run without a reload. */
export function useStatus() {
  return useQuery({
    queryKey: ['status'],
    queryFn: ({ signal }) =>
      apiClient
        .GET('/status', { signal })
        .then(unwrap<components['schemas']['StatusResponse']>('/status')),
    staleTime: 10 * MINUTE,
    refetchInterval: 10 * MINUTE,
  })
}

export function useComuni(enabled: boolean) {
  return useQuery({
    queryKey: ['comuni'],
    enabled,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/comuni', { signal })
        .then(unwrap<components['schemas']['ComuniResponse']>('/comuni')),
    staleTime: 24 * 60 * MINUTE,
  })
}

/** Analysis mode's Bosco layer: every woodland cell's dominant forest type. Static grid data --
 * doesn't vary by species or day, so it's fetched once and kept, like `useComuni`. */
export function useForestTypeCells(enabled: boolean) {
  return useQuery({
    queryKey: ['forest-types'],
    enabled,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/forest-types', { signal })
        .then(unwrap<ForestTypesResponse>('/forest-types')),
    staleTime: 24 * 60 * MINUTE,
  })
}

/** Every stored season for Tuscany (`comune` null) or one comune. */
export function useSeasons(
  species: SpeciesOrCombined,
  comune: string | null,
  enabled: boolean,
) {
  return useQuery({
    queryKey: ['seasons', species, comune],
    enabled,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/history/seasons', {
          params: { query: { species, ...(comune ? { comune } : {}) } },
          signal,
        })
        .then(unwrap<SeasonsResponse>('/history/seasons')),
    staleTime: 60 * MINUTE,
    placeholderData: (previous) => previous,
  })
}

/** One season on the map: good days per woodland cell, and the comuni ranked by them. */
export function useSeasonMap(year: number | null, species: SpeciesOrCombined) {
  return useQuery({
    queryKey: ['season-map', year, species],
    enabled: year !== null,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/history/season/{year}', {
          params: { path: { year: year! }, query: { species } },
          signal,
        })
        .then(unwrap<SeasonMapResponse>('/history/season')),
    staleTime: 60 * MINUTE,
    placeholderData: (previous) => previous,
  })
}

/** The season so far and the outlook after the 7-day forecast, for one species. */
export function useOutlook(species: Species | null, comune: string | null) {
  return useQuery({
    queryKey: ['outlook', species, comune],
    enabled: species !== null,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/outlook', {
          params: { query: { species: species!, ...(comune ? { comune } : {}) } },
          signal,
        })
        .then(unwrap<OutlookResponse>('/outlook')),
    staleTime: 60 * MINUTE,
  })
}

/** Which species the woodland of a comune (or Tuscany) plausibly holds, per species and taxon,
 * and each one's good days per season. */
export function usePlausibleSpecies(comune: string | null, enabled: boolean) {
  return useQuery({
    queryKey: ['species', comune],
    enabled,
    queryFn: ({ signal }) =>
      apiClient
        .GET('/species', {
          params: { query: comune ? { comune } : {} },
          signal,
        })
        .then(unwrap<PlausibleSpeciesResponse>('/species')),
    staleTime: 60 * MINUTE,
  })
}
