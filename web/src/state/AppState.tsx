import {
  createContext,
  type ReactNode,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { DATE_WINDOW, REGION } from '../config'
import { type IsoDate, todayInRome } from '../time/days'
import {
  parseUrlState,
  rollToday,
  serializeUrlState,
  type SpeciesOrCombined,
  type Spot,
  type UrlState,
} from './urlState'

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
  setSpecies: (species: SpeciesOrCombined) => void
  setDate: (date: IsoDate) => void
  selectSpot: (spot: Spot, camera?: Omit<CameraRequest, 'id'>) => void
  clearSpot: () => void
  camera: CameraRequest | null
  sightingsVisible: boolean
  setSightingsVisible: (visible: boolean) => void
}

// eslint-disable-next-line react-refresh/only-export-components
export const AppStateContext = createContext<AppStateValue | null>(null)

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [today, setToday] = useState(() => todayInRome())
  const [state, setState] = useState<UrlState>(() =>
    parseUrlState(window.location.search, today, DATE_WINDOW, REGION.bounds),
  )
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
      setState((s) => ({ ...s, date: rollToday(s.date, previous, now, DATE_WINDOW) }))
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

  const setSpecies = useCallback(
    (species: SpeciesOrCombined) => setState((s) => ({ ...s, species })),
    [],
  )
  const setDate = useCallback((date: IsoDate) => setState((s) => ({ ...s, date })), [])
  const selectSpot = useCallback((spot: Spot, request?: Omit<CameraRequest, 'id'>) => {
    setState((s) => ({ ...s, spot }))
    if (request) setCamera({ ...request, id: ++cameraId.current })
  }, [])
  const clearSpot = useCallback(() => setState((s) => ({ ...s, spot: null })), [])

  const value = useMemo<AppStateValue>(
    () => ({
      ...state,
      today,
      setSpecies,
      setDate,
      selectSpot,
      clearSpot,
      camera,
      sightingsVisible,
      setSightingsVisible,
    }),
    [state, today, setSpecies, setDate, selectSpot, clearSpot, camera, sightingsVisible],
  )

  return <AppStateContext.Provider value={value}>{children}</AppStateContext.Provider>
}
