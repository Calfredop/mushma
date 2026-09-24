import {
  createContext,
  type ReactNode,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { DATE_WINDOW, DEFAULT_REGION_SLUG, HISTORY_START, REGIONS } from '../config'
import { type Navigate, usePath } from '../hooks/usePath'
import {
  matchPath,
  regionPath,
  resolveLocation,
  speciesPath,
  type RouteMatch,
} from '../routes'
import { type IsoDate, todayInRome } from '../time/days'
import {
  canPickSpecies,
  keepIndicators,
  type Mode,
  parseUrlState,
  rollToday,
  serializeUrlState,
  speciesForMode,
  type SpeciesOrCombined,
  type Spot,
  toggleForestLayer,
  toggleIndicator,
  type UrlState,
  type View,
  withMode,
} from './urlState'
import type { RegionDefinition } from '../regions'

/**
 * Fixes a legacy `/` or `?species=` link to its canonical region/species path, once,
 * synchronously, before the first paint. Idempotent: safe to run twice (StrictMode).
 */
function normalizeLegacyLocation(): null {
  const { redirectTo } = resolveLocation(window.location.pathname, window.location.search)
  const current = `${window.location.pathname}${window.location.search}`
  if (redirectTo && redirectTo !== current) {
    window.history.replaceState(window.history.state, '', redirectTo)
  }
  return null
}

/** A one-shot request for the map camera, e.g. after a search or GPS fix. */
export interface CameraRequest {
  lon: number
  lat: number
  /** Omitted to keep the current zoom. */
  zoom?: number
  /** Changes on every request so repeating the same place still moves the map. */
  id: number
}

export interface AppStateValue extends UrlState {
  today: IsoDate
  /** What the path resolved to: the map (a region), a static page, or nothing known. */
  route: RouteMatch
  /** The active region: the path's region, or the default region on a static/not-found page. */
  region: RegionDefinition
  species: SpeciesOrCombined
  setSpecies: (species: SpeciesOrCombined) => void
  path: string
  navigate: Navigate
  /** A day on the map; takes a season off the map. */
  setDate: (date: IsoDate) => void
  setView: (view: View) => void
  setComune: (comune: string | null) => void
  /** A past season on the map (opens the seasons view), or null for back to the day. */
  setSeason: (season: number | null) => void
  selectSpot: (spot: Spot, camera?: Omit<CameraRequest, 'id'>) => void
  clearSpot: () => void
  /** Move the map without choosing a spot, e.g. to a comune. */
  flyTo: (camera: Omit<CameraRequest, 'id'>) => void
  camera: CameraRequest | null
  sightingsVisible: boolean
  setSightingsVisible: (visible: boolean) => void
  setMode: (mode: Mode) => void
  toggleIndicator: (id: string) => void
  /** Once the species' indicators are known: drop any it doesn't have. */
  keepIndicators: (available: readonly string[]) => void
  /** Analysis mode's Bosco toggle, independent of the indicators. */
  toggleForestLayer: () => void
}

// eslint-disable-next-line react-refresh/only-export-components
export const AppStateContext = createContext<AppStateValue | null>(null)

export function AppStateProvider({ children }: { children: ReactNode }) {
  useState(normalizeLegacyLocation)
  const [path, navigate] = usePath()
  const route = useMemo(() => matchPath(path), [path])
  const region = route.kind === 'region' ? route.region : REGIONS[DEFAULT_REGION_SLUG]
  const routeSpecies: SpeciesOrCombined =
    route.kind === 'region' ? route.species : 'combined'

  const [today, setToday] = useState(() => todayInRome())
  const [state, setState] = useState<UrlState>(() =>
    parseUrlState(
      window.location.search,
      today,
      DATE_WINDOW,
      region.bounds,
      HISTORY_START,
    ),
  )
  const species = speciesForMode(routeSpecies, state.mode)
  const [camera, setCamera] = useState<CameraRequest | null>(null)
  const [sightingsVisible, setSightingsVisible] = useState(false)
  const cameraId = useRef(0)

  // An open tab (or a phone woken in the morning) crosses midnight in Rome:
  // move "today", and the selected date with it when it meant today.
  const todayRef = useRef(today)
  useEffect(() => {
    const check = () => {
      const previous = todayRef.current
      const now = todayInRome()
      if (now === previous) return
      todayRef.current = now
      setToday(now)
      setState((s) => ({
        ...s,
        date: rollToday(s.date, previous, now, DATE_WINDOW, HISTORY_START),
      }))
    }
    const interval = setInterval(check, 60_000)
    document.addEventListener('visibilitychange', check)
    return () => {
      clearInterval(interval)
      document.removeEventListener('visibilitychange', check)
    }
  }, [])

  useEffect(() => {
    const search = serializeUrlState(state, today)
    if (search !== window.location.search) {
      window.history.replaceState(
        window.history.state,
        '',
        `${window.location.pathname}${search}`,
      )
    }
  }, [state, today])

  // Analysis mode on a "Tutti" path shows porcini: the path follows, without a back-button stop.
  useEffect(() => {
    if (route.kind === 'region' && species !== routeSpecies && species !== 'combined') {
      navigate(speciesPath(region.slug, species), { replace: true })
    }
  }, [route.kind, species, routeSpecies, region.slug, navigate])

  const setSpecies = useCallback(
    (next: SpeciesOrCombined) => {
      if (!canPickSpecies(next, state.mode)) return
      navigate(
        next === 'combined' ? regionPath(region.slug) : speciesPath(region.slug, next),
      )
    },
    [navigate, region.slug, state.mode],
  )
  const setMode = useCallback((mode: Mode) => setState((s) => withMode(s, mode)), [])
  const toggle = useCallback((id: string) => setState((s) => toggleIndicator(s, id)), [])
  const keep = useCallback(
    (available: readonly string[]) => setState((s) => keepIndicators(s, available)),
    [],
  )
  const toggleForest = useCallback(() => setState((s) => toggleForestLayer(s)), [])
  const setDate = useCallback(
    (date: IsoDate) => setState((s) => ({ ...s, date, season: null })),
    [],
  )
  // Only the seasons view puts a season on the map; leaving it goes back to the day.
  const setView = useCallback(
    (view: View) =>
      setState((s) => ({ ...s, view, season: view === 'seasons' ? s.season : null })),
    [],
  )
  const setComune = useCallback(
    (comune: string | null) => setState((s) => ({ ...s, comune })),
    [],
  )
  const setSeason = useCallback(
    (season: number | null) =>
      setState((s) => ({ ...s, season, view: season === null ? s.view : 'seasons' })),
    [],
  )
  const selectSpot = useCallback((spot: Spot, request?: Omit<CameraRequest, 'id'>) => {
    setState((s) => ({ ...s, spot }))
    if (request) setCamera({ ...request, id: ++cameraId.current })
  }, [])
  const clearSpot = useCallback(() => setState((s) => ({ ...s, spot: null })), [])
  const flyTo = useCallback((request: Omit<CameraRequest, 'id'>) => {
    setCamera({ ...request, id: ++cameraId.current })
  }, [])

  const value = useMemo<AppStateValue>(
    () => ({
      ...state,
      today,
      route,
      region,
      species,
      setSpecies,
      path,
      navigate,
      setDate,
      setView,
      setComune,
      setSeason,
      selectSpot,
      clearSpot,
      flyTo,
      camera,
      sightingsVisible,
      setSightingsVisible,
      setMode,
      toggleIndicator: toggle,
      keepIndicators: keep,
      toggleForestLayer: toggleForest,
    }),
    [
      state,
      today,
      route,
      region,
      species,
      setSpecies,
      path,
      navigate,
      setDate,
      setView,
      setComune,
      setSeason,
      selectSpot,
      clearSpot,
      flyTo,
      camera,
      sightingsVisible,
      setMode,
      toggle,
      keep,
      toggleForest,
    ],
  )

  return <AppStateContext.Provider value={value}>{children}</AppStateContext.Provider>
}
