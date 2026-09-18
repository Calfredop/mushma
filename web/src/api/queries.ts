/** TanStack Query hooks over the typed API client. The frontend only reads. */
import { type UseQueryResult, useQueries, useQuery } from '@tanstack/react-query'
import { useCallback } from 'react'
import { SIGHTINGS_WINDOW_DAYS } from '../config'
import { sightingsByCell } from '../map/geojson'
import {
  SPECIES,
  type Species,
  type SpeciesOrCombined,
  type Spot,
} from '../state/urlState'
import { addDays, type IsoDate } from '../time/days'
import { apiClient } from './client'
import type { components } from './schema'

export type ScoresResponse = components['schemas']['ScoresResponse']
export type CellDetailResponse = components['schemas']['CellDetailResponse']
export type HotspotsResponse = components['schemas']['HotspotsResponse']
export type Hotspot = components['schemas']['Hotspot']
export type SpeciesForecast = components['schemas']['SpeciesForecast']
export type DayScore = components['schemas']['DayScore']

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

/** Past days never change once scored; today and the forecast refresh. */
function staleTimeFor(date: IsoDate, today: IsoDate): number {
  return date < today ? Infinity : 10 * MINUTE
}

export function useScores(species: SpeciesOrCombined, date: IsoDate, today: IsoDate) {
  return useQuery({
    queryKey: ['scores', species, date],
    queryFn: ({ signal }) =>
      apiClient
        .GET('/scores', { params: { query: { species, date } }, signal })
        .then(unwrap<ScoresResponse>('/scores')),
    staleTime: staleTimeFor(date, today),
    placeholderData: (previous) => previous,
  })
}

export function useHotspots(
  species: SpeciesOrCombined,
  date: IsoDate,
  today: IsoDate,
  limit: number,
) {
  return useQuery({
    queryKey: ['hotspots', species, date, limit],
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

/** Sighting totals per cell for one species, or summed over all of them. */
export function useSightingTotals(
  species: SpeciesOrCombined,
  today: IsoDate,
  enabled: boolean,
) {
  const since = addDays(today, -SIGHTINGS_WINDOW_DAYS)
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
  return useQueries({
    queries: speciesList.map((sp) => ({
      queryKey: ['sightings', sp, since],
      enabled,
      queryFn: ({ signal }: { signal: AbortSignal }) =>
        apiClient
          .GET('/sightings', { params: { query: { species: sp, since } }, signal })
          .then(unwrap<components['schemas']['SightingsResponse']>('/sightings')),
      staleTime: 60 * MINUTE,
    })),
    // Stable, so totals (a Map) are only rebuilt when the results change.
    combine,
  })
}
