import { onlineManager, QueryClient, QueryClientProvider } from '@tanstack/react-query'
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from 'react'
import { useTranslation } from 'react-i18next'
import {
  ApiError,
  type DateRange,
  type Hotspot,
  isClientError,
  useComuni,
  useHotspots,
  useOutlook,
  useScores,
  useSeasonMap,
  useSeasons,
  useSightingTotals,
  useSpotForecast,
} from './api/queries'
import styles from './App.module.css'
import { DisclaimerDialog, disclaimerAccepted } from './components/DisclaimerDialog'
import { ChevronIcon, InfoIcon, LocateIcon, SearchIcon } from './components/icons'
import { InstallBanner } from './components/InstallBanner'
import { LanguageSwitcher } from './components/LanguageSwitcher'
import { PanelBoundary } from './components/PanelBoundary'
import { Legend } from './components/Legend'
import { PlaceSearch } from './components/PlaceSearch'
import { SpeciesSwitcher } from './components/SpeciesSwitcher'
import { TimeBar } from './components/TimeBar'
import { ViewTabs } from './components/ViewTabs'
import {
  DATE_WINDOW,
  HISTORY_START,
  HOTSPOT_LIMIT,
  REGION,
  REPLAY_SIGHTINGS_DAYS,
  SIGHTINGS_WINDOW_DAYS,
} from './config'
import { distanceKm, inBounds, OUTSIDE_CELL_KM } from './geo/distance'
import type { Place } from './geo/photon'
import { type LocateError, useLocate } from './hooks/useLocate'
import { useMediaQuery } from './hooks/useMediaQuery'
import { usePath } from './hooks/usePath'
import { intlLocale, type Language } from './i18n'
import './i18n'
import { ConditionsMap } from './map/ConditionsMap'
import { CreditsPage } from './pages/CreditsPage'
import { HotPlaces } from './panels/HotPlaces'
import { OutlookPanel } from './panels/OutlookPanel'
import { SeasonsPanel } from './panels/SeasonsPanel'
import { SpotPanel } from './panels/SpotPanel'
import { AppStateProvider } from './state/AppState'
import { useAppState } from './state/useAppState'
import { addDays, daysBetween, formatDayMonth } from './time/days'

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
const COMUNE_ZOOM = 10.5

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

  // What the map shows: a day (the date strip or a replayed past day), or a whole season.
  const seasonMode = app.season !== null
  const inStrip = daysBetween(app.today, app.date) >= -DATE_WINDOW.pastDays
  const scores = useScores(app.species, app.date, app.today, !seasonMode)
  const seasonMap = useSeasonMap(app.season, app.species)
  const hotspots = useHotspots(
    app.species,
    app.date,
    app.today,
    HOTSPOT_LIMIT,
    !seasonMode && app.view === 'now',
  )
  const spotForecast = useSpotForecast(app.spot, app.today)
  const comuni = useComuni(app.view !== 'now')
  const seasons = useSeasons(
    app.species,
    app.comune,
    app.view === 'seasons' || seasonMode,
  )
  const outlook = useOutlook(
    app.view === 'outlook' && app.species !== 'combined' ? app.species : null,
    app.comune,
  )

  // Sightings from the time on the map: the last months, the weeks around a replayed day, or
  // the whole of a season.
  const sightingsRange: DateRange = seasonMode
    ? { since: `${app.season}-01-01`, until: `${app.season}-12-31` }
    : inStrip
      ? { since: addDays(app.today, -SIGHTINGS_WINDOW_DAYS) }
      : {
          since: addDays(app.date, -REPLAY_SIGHTINGS_DAYS),
          until: addDays(app.date, REPLAY_SIGHTINGS_DAYS),
        }
  const sightings = useSightingTotals(app.species, sightingsRange, app.sightingsVisible)
  const replayWindow =
    !seasonMode && !inStrip && sightingsRange.until
      ? t('sightings.replayWindow', {
          start: formatDayMonth(sightingsRange.since, intlLocale(language)),
          end: formatDayMonth(sightingsRange.until, intlLocale(language)),
        })
      : undefined
  // Once per response: the map rebuilds ~11k features whenever this array changes.
  const seasonCells = useMemo(
    () => seasonMap.data?.cells.map((c) => ({ ...c, score: c.good_days })),
    [seasonMap.data],
  )
  const mapCells = seasonMode ? seasonCells : scores.data?.cells
  const seasonYears = seasons.data?.seasons.map((s) => s.year) ?? []

  const { selectSpot, flyTo, setComune } = app
  const chooseComune = useCallback(
    (code: string | null) => {
      setComune(code)
      const comune = code ? comuni.data?.comuni.find((c) => c.code === code) : undefined
      if (comune) flyTo({ lat: comune.lat, lon: comune.lon, zoom: COMUNE_ZOOM })
    },
    [setComune, flyTo, comuni.data],
  )
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

  const layer = seasonMode ? seasonMap : scores
  const scoresUnavailable = layer.isError && isClientError(layer.error)
  const status = locating
    ? t('locate.locating')
    : !online
      ? t('errors.offline')
      : layer.isError
        ? seasonMode
          ? t(scoresUnavailable ? 'season.noData' : 'map.loadError')
          : t(scoresUnavailable ? 'map.noData' : 'map.loadError')
        : layer.isPending || layer.isPlaceholderData
          ? t(seasonMode ? 'season.loading' : 'map.loading')
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
          cells={mapCells}
          scale={seasonMode ? 'goodDays' : 'score'}
          selectedCellId={selectedCellId}
          sightings={app.sightingsVisible ? sightings.totals : undefined}
          hotspots={
            !seasonMode && app.view === 'now' ? hotspots.data?.hotspots : undefined
          }
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
            {layer.isError && !scoresUnavailable && online && (
              <button type="button" onClick={() => void layer.refetch()}>
                {t('map.retry')}
              </button>
            )}
          </p>
        )}
        <div className={styles.bottom}>
          <div className={styles.legend}>
            <Legend showSightings={app.sightingsVisible} season={app.season} />
          </div>
          <div className={styles.dates}>
            <TimeBar
              today={app.today}
              date={app.date}
              window={DATE_WINDOW}
              historyStart={HISTORY_START}
              season={app.season}
              seasons={seasonYears}
              onDate={app.setDate}
              onSeason={app.setSeason}
            />
          </div>
        </div>
      </main>

      <aside
        className={styles.sheet}
        aria-label={t(app.spot ? 'spot.title' : `views.${app.view}`)}
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
            <>
              <ViewTabs
                value={app.view}
                panelId="sheet-view"
                onChange={(view) => {
                  app.setView(view)
                  setSheetOpen(true)
                }}
              />
              <div
                id="sheet-view"
                role="tabpanel"
                aria-labelledby={`view-tab-${app.view}`}
              >
                <PanelBoundary resetKey={`${app.view}|${app.species}|${app.comune}`}>
                  {app.view === 'now' && (
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
                      sightingsWindow={replayWindow}
                    />
                  )}
                  {app.view === 'seasons' && (
                    <SeasonsPanel
                      species={app.species}
                      comuni={comuni.data?.comuni}
                      comune={app.comune}
                      onComune={chooseComune}
                      seasons={seasons.data}
                      isLoading={seasons.isPending}
                      isError={seasons.isError}
                      onRetry={() => void seasons.refetch()}
                      selected={app.season}
                      onSelect={app.setSeason}
                      seasonMap={seasonMap.data}
                      onReplayDay={app.setDate}
                      sightingsVisible={app.sightingsVisible}
                      onSightingsVisibleChange={app.setSightingsVisible}
                    />
                  )}
                  {app.view === 'outlook' && (
                    <OutlookPanel
                      species={app.species}
                      onSpecies={app.setSpecies}
                      comuni={comuni.data?.comuni}
                      comune={app.comune}
                      onComune={chooseComune}
                      outlook={outlook.data}
                      isLoading={outlook.isPending && outlook.fetchStatus !== 'idle'}
                      isError={outlook.isError}
                      onRetry={() => void outlook.refetch()}
                    />
                  )}
                </PanelBoundary>
              </div>
            </>
          )}
          <InstallBanner />
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
