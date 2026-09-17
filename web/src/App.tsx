import { onlineManager, QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from 'react'
import { useTranslation } from 'react-i18next'
import {
  ApiError,
  type Hotspot,
  isClientError,
  useHotspots,
  useScores,
  useSightingTotals,
  useSpotForecast,
} from './api/queries'
import styles from './App.module.css'
import { DateStrip } from './components/DateStrip'
import { DisclaimerDialog, disclaimerAccepted } from './components/DisclaimerDialog'
import { ChevronIcon, InfoIcon, LocateIcon, SearchIcon } from './components/icons'
import { LanguageSwitcher } from './components/LanguageSwitcher'
import { Legend } from './components/Legend'
import { PlaceSearch } from './components/PlaceSearch'
import { SpeciesSwitcher } from './components/SpeciesSwitcher'
import { DATE_WINDOW, HOTSPOT_LIMIT, REGION } from './config'
import { distanceKm, inBounds, OUTSIDE_CELL_KM } from './geo/distance'
import type { Place } from './geo/photon'
import { type LocateError, useLocate } from './hooks/useLocate'
import { useMediaQuery } from './hooks/useMediaQuery'
import { usePath } from './hooks/usePath'
import type { Language } from './i18n'
import './i18n'
import { ConditionsMap } from './map/ConditionsMap'
import { CreditsPage } from './pages/CreditsPage'
import { HotPlaces } from './panels/HotPlaces'
import { SpotPanel } from './panels/SpotPanel'
import { AppStateProvider } from './state/AppState'
import { useAppState } from './state/useAppState'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // A 4xx (e.g. a date outside the served window) won't fix itself.
      retry: (failures, error) =>
        !(error instanceof ApiError && error.status < 500) && failures < 2,
      refetchOnWindowFocus: false,
    },
  },
})

const SPOT_ZOOM = 12
const HOTSPOT_ZOOM = 9.5

function useOnline(): boolean {
  return useSyncExternalStore(
    (onChange) => onlineManager.subscribe(onChange),
    () => onlineManager.isOnline(),
  )
}

function MapScreen() {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const app = useAppState()
  const [path, navigate] = usePath()
  const desktop = useMediaQuery('(min-width: 900px)')

  const [sheetOpen, setSheetOpen] = useState(app.spot !== null)
  const [searchOpen, setSearchOpen] = useState(false)
  const [disclaimerOpen, setDisclaimerOpen] = useState(() => !disclaimerAccepted())
  // A key, not a translated string, so it follows a language switch.
  const [locateError, setLocateError] = useState<LocateError | null>(null)
  const online = useOnline()

  const scores = useScores(app.species, app.date, app.today)
  const hotspots = useHotspots(app.species, app.date, app.today, HOTSPOT_LIMIT)
  const spotForecast = useSpotForecast(app.spot, app.today)
  const sightings = useSightingTotals(app.species, app.today, app.sightingsVisible)

  const { selectSpot } = app
  const openSpot = useCallback(
    (...args: Parameters<typeof selectSpot>) => {
      selectSpot(...args)
      setSheetOpen(true)
      setSearchOpen(false)
      setLocateError(null)
    },
    [selectSpot],
  )

  const { locate, locating } = useLocate({
    onLocated: useCallback(
      (lat: number, lon: number) =>
        openSpot({ kind: 'point', lat, lon }, { lat, lon, zoom: SPOT_ZOOM }),
      [openSpot],
    ),
    onError: setLocateError,
  })

  // A shared link (?cell= or ?at=) opens on its spot: move the map there once
  // the forecast says where the cell is. A distant cell is framed by the map itself.
  const linkedSpot = useRef(app.spot)
  useEffect(() => {
    const initial = linkedSpot.current
    const detail = spotForecast.data
    if (!initial || !detail) return
    linkedSpot.current = null
    if (JSON.stringify(initial) !== JSON.stringify(app.spot)) return
    if (initial.kind === 'point') {
      if (distanceKm(initial.lat, initial.lon, detail.lat, detail.lon) > OUTSIDE_CELL_KM)
        return
      selectSpot(initial, { lat: initial.lat, lon: initial.lon, zoom: SPOT_ZOOM })
    } else {
      selectSpot(initial, { lat: detail.lat, lon: detail.lon, zoom: SPOT_ZOOM })
    }
  }, [spotForecast.data, app.spot, selectSpot])

  const selectedCellId =
    app.spot?.kind === 'cell' ? app.spot.cellId : (spotForecast.data?.cell_id ?? null)

  const onHotspot = (hotspot: Hotspot) =>
    openSpot(
      { kind: 'cell', cellId: hotspot.cell_ids[0] },
      { lat: hotspot.lat, lon: hotspot.lon, zoom: HOTSPOT_ZOOM },
    )
  const onPlace = (place: Place) =>
    openSpot(
      { kind: 'point', lat: place.lat, lon: place.lon },
      { lat: place.lat, lon: place.lon, zoom: SPOT_ZOOM },
    )

  const search = (
    <PlaceSearch
      onSelect={onPlace}
      autoFocus={!desktop}
      onDismiss={desktop ? undefined : () => setSearchOpen(false)}
    />
  )

  const scoresUnavailable = scores.isError && isClientError(scores.error)
  const status = locating
    ? t('locate.locating')
    : !online
      ? t('errors.offline')
      : scores.isError
        ? t(scoresUnavailable ? 'map.noData' : 'map.loadError')
        : scores.isPending || scores.isPlaceholderData
          ? t('map.loading')
          : locateError && t(`locate.${locateError}`)

  return (
    <div className={styles.app} data-sheet={sheetOpen ? 'open' : 'closed'}>
      <header className={styles.topbar}>
        <h1 className={styles.wordmark}>{t('app.name')}</h1>
        <div className={styles.actions}>
          {!desktop && (
            <button
              type="button"
              className={styles.iconButton}
              aria-label={t('search.open')}
              aria-expanded={searchOpen}
              onClick={() => setSearchOpen((open) => !open)}
            >
              <SearchIcon />
            </button>
          )}
          <button
            type="button"
            className={styles.iconButton}
            aria-label={t('locate.button')}
            aria-busy={locating}
            onClick={locate}
          >
            <LocateIcon />
          </button>
          <LanguageSwitcher />
          <button
            type="button"
            className={styles.iconButton}
            aria-label={t('nav.disclaimer')}
            onClick={() => setDisclaimerOpen(true)}
          >
            <InfoIcon />
          </button>
        </div>
        {!desktop && searchOpen && <div className={styles.searchOverlay}>{search}</div>}
      </header>

      <main className={styles.mapArea}>
        <ConditionsMap
          cells={scores.data?.cells}
          selectedCellId={selectedCellId}
          sightings={app.sightingsVisible ? sightings.totals : undefined}
          hotspots={hotspots.data?.hotspots}
          camera={app.camera}
          spotPoint={
            app.spot?.kind === 'point'
              ? {
                  point: [app.spot.lon, app.spot.lat],
                  cell: spotForecast.data
                    ? [spotForecast.data.lon, spotForecast.data.lat]
                    : undefined,
                }
              : null
          }
          lang={language}
          // On a phone the sheet opens and the map shrinks around its centre:
          // centre on the tap so the chosen spot stays in view.
          onCellClick={(cellId, lat, lon) =>
            openSpot({ kind: 'cell', cellId }, desktop ? undefined : { lat, lon })
          }
          onPointClick={(lat, lon) => {
            if (!inBounds(lat, lon, REGION.bounds)) return
            openSpot({ kind: 'point', lat, lon }, desktop ? undefined : { lat, lon })
          }}
          onHotspotClick={onHotspot}
        />
        <div className={styles.species}>
          <SpeciesSwitcher value={app.species} onChange={app.setSpecies} />
        </div>
        {status && (
          <p className={styles.status} role="status">
            {status}
            {scores.isError && !scoresUnavailable && online && (
              <button type="button" onClick={() => void scores.refetch()}>
                {t('map.retry')}
              </button>
            )}
          </p>
        )}
        <div className={styles.bottom}>
          <div className={styles.legend}>
            <Legend showSightings={app.sightingsVisible} />
          </div>
          <div className={styles.dates}>
            <DateStrip
              today={app.today}
              value={app.date}
              window={DATE_WINDOW}
              onChange={app.setDate}
            />
          </div>
        </div>
      </main>

      <aside
        className={styles.sheet}
        aria-label={t(app.spot ? 'spot.title' : 'hotspots.title')}
      >
        {!desktop && (
          <button
            type="button"
            className={styles.handle}
            aria-expanded={sheetOpen}
            aria-label={t(sheetOpen ? 'sheet.collapse' : 'sheet.expand')}
            onClick={() => setSheetOpen((open) => !open)}
          >
            <span className={styles.grip} />
            <ChevronIcon direction={sheetOpen ? 'down' : 'up'} />
          </button>
        )}
        <div className={styles.sheetBody}>
          {desktop && <div className={styles.desktopSearch}>{search}</div>}
          {app.spot ? (
            <SpotPanel
              key={JSON.stringify(app.spot)}
              spot={app.spot}
              detail={spotForecast.data}
              isLoading={spotForecast.isPending}
              isError={spotForecast.isError}
              notFound={isClientError(spotForecast.error)}
              onRetry={() => void spotForecast.refetch()}
              onClose={app.clearSpot}
              species={app.species}
              date={app.date}
              today={app.today}
            />
          ) : (
            <HotPlaces
              species={app.species}
              date={app.date}
              hotspots={hotspots.data?.hotspots}
              isLoading={hotspots.isPending}
              isError={hotspots.isError}
              onRetry={() => void hotspots.refetch()}
              onSelect={onHotspot}
              sightingsVisible={app.sightingsVisible}
              onSightingsVisibleChange={app.setSightingsVisible}
              sightingsError={sightings.isError}
            />
          )}
          <footer className={styles.footer}>
            <p>{t('disclaimer.short')}</p>
            <p className={styles.links}>
              <a
                href="/credits"
                onClick={(event) => {
                  event.preventDefault()
                  navigate('/credits')
                }}
              >
                {t('nav.credits')}
              </a>
              <button type="button" onClick={() => setDisclaimerOpen(true)}>
                {t('nav.disclaimer')}
              </button>
            </p>
          </footer>
        </div>
      </aside>

      {path === '/credits' && <CreditsPage onBack={() => navigate('/')} />}
      <DisclaimerDialog open={disclaimerOpen} onClose={() => setDisclaimerOpen(false)} />
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppStateProvider>
        <MapScreen />
      </AppStateProvider>
    </QueryClientProvider>
  )
}
