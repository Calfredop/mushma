import {
  onlineManager,
  QueryClient,
  QueryClientProvider,
  useQueryClient,
} from '@tanstack/react-query'
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from 'react'
import { LazyMotion } from 'motion/react'
import { useTranslation } from 'react-i18next'
import { track } from './analytics'
import {
  ApiError,
  type DateRange,
  factorsQuery,
  type Hotspot,
  isClientError,
  type RegionOverview,
  useComuni,
  useFactors,
  useForestTypeCells,
  useHotspots,
  useOutlook,
  usePlausibleSpecies,
  useScores,
  useSeasonMap,
  useSeasons,
  useSightingTotals,
  useSpotForecast,
  useStatus,
  useOverview,
} from './api/queries'
import styles from './App.module.css'
import { CookieBanner } from './components/CookieBanner'
import { DataStatus } from './components/DataStatus'
import { DisclaimerDialog, disclaimerAccepted } from './components/DisclaimerDialog'
import { ChevronIcon, GitHubIcon, LayersIcon, LocateIcon } from './components/icons'
import { IndicatorPanel } from './components/IndicatorPanel'
import { InfoMenu } from './components/InfoMenu'
import { InstallBanner } from './components/InstallBanner'
import { PanelBoundary } from './components/PanelBoundary'
import { Legend } from './components/Legend'
import { PlaceSearch } from './components/PlaceSearch'
import { RegionSwitcher } from './components/RegionSwitcher'
import { Sheet, type SheetLayout } from './components/Sheet'
import { SpeciesSwitcher } from './components/SpeciesSwitcher'
import { TimeBar } from './components/TimeBar'
import { ViewTabs } from './components/ViewTabs'
import {
  DATE_WINDOW,
  HOTSPOT_LIMIT,
  REPLAY_SIGHTINGS_DAYS,
  REPO_URL,
  SIGHTINGS_WINDOW_DAYS,
  findRegionAt,
  listRegions,
  rememberRegion,
  servedBounds,
} from './config'
import { getConsent } from './consent'
import { distanceKm, inBounds, OUTSIDE_CELL_KM } from './geo/distance'
import type { Place } from './geo/photon'
import { type LocateError, useLocate } from './hooks/useLocate'
import { useMediaQuery } from './hooks/useMediaQuery'
import { usePersistentFlag } from './hooks/usePersistentFlag'
import { usePlayback } from './hooks/usePlayback'
import { currentLanguage, intlLocale, type Language } from './i18n'
import './i18n'
import { type AnalysisView, ConditionsMap } from './map/ConditionsMap'
import type { MapPadding } from './map/padding'
import { CreditsPage } from './pages/CreditsPage'
import { HubPage } from './pages/HubPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { PrivacyPage } from './pages/PrivacyPage'
import { TermsPage } from './pages/TermsPage'
import { HotPlaces } from './panels/HotPlaces'
import { OutlookPanel } from './panels/OutlookPanel'
import { SeasonsPanel } from './panels/SeasonsPanel'
import { SpotPanel } from './panels/SpotPanel'
import { regionPath, SITE_URL, siteRouteFor } from './routes'
import { indicatorOf } from './score/indicators'
import {
  seoKeyForRoute,
  setDocumentCanonical,
  setDocumentDescription,
  setDocumentJsonLd,
  setDocumentRobots,
} from './seo/head'
import { structuredData } from './seo/structuredData'
import { type Snap, visibleAt } from './sheet/snaps'
import { AppStateProvider, type CameraRequest } from './state/AppState'
import { useAppState } from './state/useAppState'
import type { Spot, SpeciesOrCombined } from './state/urlState'
import {
  addDays,
  dateWindow,
  daysBetween,
  formatDayMonth,
  type IsoDate,
} from './time/days'

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

/** Motion's animation features come after first paint (PRD → Mobile performance). */
const loadMotionFeatures = () =>
  import('./motionFeatures').then((module) => module.default)

// What covers a phone's map besides the sheet: the species pill and cluster on top (under the
// clear top: the safe-area inset and any system blur), the cluster down the right, the time
// bar riding on the sheet.
const PHONE_CHROME = { top: 72, right: 68, left: 16, bottom: 96 }
// On a desktop: the species pill on top, the cluster and zoom on the right, the time bar below,
// and the floating panel (--panel-width, inset --space-4) on the left while it is open.
const DESKTOP_CHROME = { top: 82, right: 76, bottom: 100, left: 16 }
const PANEL_INSET = 16 + 400 + 16

/** The footer's pages, by short name: one row of links, even on a 360px phone. */
const FOOTER_PAGES = [
  { path: '/credits', label: 'footer.credits' },
  { path: '/terms', label: 'footer.terms' },
  { path: '/privacy', label: 'footer.privacy' },
] as const

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
  const { navigate } = app
  const desktop = useMediaQuery('(min-width: 900px)')

  // The phone sheet: a chosen spot opens at half.
  const [snap, setSnap] = useState<Snap>(app.spot ? 'half' : 'peek')
  const [sheetLayout, setSheetLayout] = useState<SheetLayout | null>(null)
  const [introOpen, setIntroOpen] = useState(false)
  // The desktop panel folded to its header; the browser remembers it.
  const [panelCollapsed, setPanelCollapsed] = usePersistentFlag('mushma.panel.collapsed')
  const mapAreaRef = useRef<HTMLElement>(null)
  const [disclaimerOpen, setDisclaimerOpen] = useState(() => !disclaimerAccepted())
  const [cookieBannerOpen, setCookieBannerOpen] = useState(() => getConsent() === null)
  // A key, not a translated string, so it follows a language switch.
  const [locateError, setLocateError] = useState<LocateError | null>(null)
  /** Another served region where a GPS/search landed — offer one-tap switch. */
  const [switchOffer, setSwitchOffer] = useState<{
    slug: string
    lat: number
    lon: number
  } | null>(null)
  // The last GPS fix, for the dot on the map. Never in the URL: a shared link doesn't carry it.
  const [userPosition, setUserPosition] = useState<{ lat: number; lon: number } | null>(
    null,
  )
  const online = useOnline()
  const apiRegionId = app.region.apiRegionId

  // What the map shows: a day (the date strip or a replayed past day), or a whole season.
  const seasonMode = app.season !== null
  const inStrip = daysBetween(app.today, app.date) >= -DATE_WINDOW.pastDays
  // Analysis mode: the factors behind a species' score. They are only kept for the strip's days.
  const analysis = app.mode === 'analysis'
  const factorDay = !seasonMode && inStrip
  const factorSpecies = app.species === 'combined' ? 'porcini' : app.species
  const scores = useScores(
    apiRegionId,
    app.species,
    app.date,
    app.today,
    !seasonMode && !analysis,
  )
  const factors = useFactors(
    apiRegionId,
    factorSpecies,
    app.date,
    app.today,
    analysis && factorDay,
  )
  // The Bosco layer's forest types: static grid data, fetched once regardless of the toggle's
  // own state, so switching it on never waits on a request.
  const forestTypes = useForestTypeCells(apiRegionId, analysis)
  const seasonMap = useSeasonMap(apiRegionId, app.season, app.species)
  const hotspots = useHotspots(
    apiRegionId,
    app.species,
    app.date,
    app.today,
    HOTSPOT_LIMIT,
    !seasonMode && app.view === 'now',
  )
  const spotForecast = useSpotForecast(apiRegionId, app.spot, app.today)
  const dataStatus = useStatus(apiRegionId)
  const comuni = useComuni(apiRegionId, app.view !== 'now')
  const seasons = useSeasons(
    apiRegionId,
    app.species,
    app.comune,
    app.view === 'seasons' || seasonMode,
  )
  const outlook = useOutlook(
    apiRegionId,
    app.view === 'outlook' && app.species !== 'combined' ? app.species : null,
    app.comune,
  )
  // A chosen zone's plausible species, in the seasons and outlook views.
  const plausibleQuery = usePlausibleSpecies(
    apiRegionId,
    app.comune,
    app.view !== 'now' && app.comune !== null,
  )
  const plausible = {
    data: plausibleQuery.data,
    isLoading: plausibleQuery.isPending,
    isError: plausibleQuery.isError,
    onRetry: () => void plausibleQuery.refetch(),
  }

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
  const sightings = useSightingTotals(
    apiRegionId,
    app.species,
    sightingsRange,
    app.sightingsVisible,
  )
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

  // Once a species' factors are known, the indicators it doesn't have come off.
  const { keepIndicators } = app
  const servedFactors = factorDay ? factors.data?.factors : undefined
  useEffect(() => {
    if (analysis && servedFactors) keepIndicators(servedFactors.map((f) => f.id))
  }, [analysis, servedFactors, keepIndicators])
  const activeIndicators = useMemo(
    () => app.indicators.map((id) => ({ id, color: indicatorOf(id).color })),
    [app.indicators],
  )
  const factorIds = useMemo(() => servedFactors?.map((f) => f.id) ?? [], [servedFactors])
  const factorCells = factorDay ? factors.data?.cells : undefined
  const forestByCellId = useMemo(
    () =>
      forestTypes.data &&
      new Map(forestTypes.data.cells.map((c) => [c.cell_id, c.habitat])),
    [forestTypes.data],
  )
  const analysisView = useMemo<AnalysisView | null>(
    () =>
      analysis
        ? {
            cells: factorCells,
            ids: factorIds,
            active: activeIndicators,
            forestTypes: { byCellId: forestByCellId, on: app.forest },
          }
        : null,
    [analysis, factorCells, factorIds, activeIndicators, forestByCellId, app.forest],
  )

  // Play: a day a second through the strip, the next days fetched ahead.
  const queryClient = useQueryClient()
  const stripDays = useMemo(
    () => dateWindow(app.today, DATE_WINDOW).map(({ date }) => date),
    [app.today],
  )
  const { today } = app
  const prefetchFactors = useCallback(
    (date: IsoDate) =>
      void queryClient.prefetchQuery(
        factorsQuery(apiRegionId, factorSpecies, date, today),
      ),
    [queryClient, apiRegionId, factorSpecies, today],
  )
  const playback = usePlayback({
    days: stripDays,
    date: app.date,
    onDate: app.setDate,
    prefetch: prefetchFactors,
    enabled: analysis && factorDay,
  })

  const { selectSpot, flyTo, setComune, setDate, setSpecies, setRegion } = app
  const handleSpeciesChange = useCallback(
    (species: SpeciesOrCombined) => {
      track({ name: 'species-switch', data: { species } })
      setSpecies(species)
    },
    [setSpecies],
  )
  const handleDateChange = useCallback(
    (date: IsoDate) => {
      const offset = daysBetween(app.today, date)
      track({
        name: 'date-move',
        data: { offset: offset < -DATE_WINDOW.pastDays ? 'replay' : offset },
      })
      setDate(date)
    },
    [app.today, setDate],
  )
  const chooseComune = useCallback(
    (code: string | null) => {
      setComune(code)
      const comune = code ? comuni.data?.comuni.find((c) => c.code === code) : undefined
      if (comune) flyTo({ lat: comune.lat, lon: comune.lon, zoom: COMUNE_ZOOM })
    },
    [setComune, flyTo, comuni.data],
  )
  const openSpot = useCallback(
    (
      spot: Spot,
      method: 'map' | 'search' | 'gps' | 'hotspot',
      camera?: Omit<CameraRequest, 'id'>,
    ) => {
      track({ name: 'spot-open', data: { method } })
      selectSpot(spot, camera)
      setSnap('half')
      setPanelCollapsed(false)
      setLocateError(null)
      setSwitchOffer(null)
    },
    [selectSpot, setPanelCollapsed],
  )

  const offerOrOpen = useCallback(
    (lat: number, lon: number, method: 'map' | 'search' | 'gps' | 'hotspot') => {
      if (inBounds(lat, lon, app.region.bounds)) {
        openSpot({ kind: 'point', lat, lon }, method, { lat, lon, zoom: SPOT_ZOOM })
        return
      }
      const other = findRegionAt(lat, lon)
      if (other && other.slug !== app.region.slug) {
        setUserPosition({ lat, lon })
        setSwitchOffer({ slug: other.slug, lat, lon })
        setLocateError(null)
        return
      }
      setLocateError('outside')
    },
    [app.region.bounds, app.region.slug, openSpot],
  )

  const acceptSwitch = useCallback(() => {
    if (!switchOffer) return
    const { slug, lat, lon } = switchOffer
    setSwitchOffer(null)
    setLocateError(null)
    setRegion(slug)
    window.setTimeout(() => {
      openSpot({ kind: 'point', lat, lon }, 'gps', { lat, lon, zoom: SPOT_ZOOM })
    }, 0)
  }, [switchOffer, setRegion, openSpot])

  // "La mia posizione" in the search opens the forecast where you stand; the button on the map
  // only goes there.
  const onOtherRegion = useCallback((slug: string, lat: number, lon: number) => {
    setUserPosition({ lat, lon })
    setSwitchOffer({ slug, lat, lon })
    setLocateError(null)
  }, [])
  const spotLocate = useLocate({
    onLocated: useCallback(
      (lat: number, lon: number) => {
        setUserPosition({ lat, lon })
        openSpot({ kind: 'point', lat, lon }, 'gps', { lat, lon, zoom: SPOT_ZOOM })
      },
      [openSpot],
    ),
    onError: setLocateError,
    bounds: app.region.bounds,
    onOtherRegion,
  })
  const centerLocate = useLocate({
    onLocated: useCallback(
      (lat: number, lon: number) => {
        setUserPosition({ lat, lon })
        setLocateError(null)
        setSwitchOffer(null)
        flyTo({ lat, lon, zoom: SPOT_ZOOM })
      },
      [flyTo],
    ),
    onError: setLocateError,
    bounds: app.region.bounds,
    onOtherRegion,
  })
  const locating = spotLocate.locating || centerLocate.locating

  // A shared link (?cell= or ?at=) opens on its spot: move the map there once
  // the forecast says where the cell is. A distant cell is framed by the map itself.
  const linkedSpot = useRef(app.spot)
  useEffect(() => {
    const initial = linkedSpot.current
    const detail = spotForecast.data
    if (!initial || !detail) return
    linkedSpot.current = null
    if (JSON.stringify(initial) !== JSON.stringify(app.spot)) return
    // A link to a spot is a spot chosen: a folded desktop panel opens for it.
    setPanelCollapsed(false)
    if (initial.kind === 'point') {
      if (distanceKm(initial.lat, initial.lon, detail.lat, detail.lon) > OUTSIDE_CELL_KM)
        return
      selectSpot(initial, { lat: initial.lat, lon: initial.lon, zoom: SPOT_ZOOM })
    } else {
      selectSpot(initial, { lat: detail.lat, lon: detail.lon, zoom: SPOT_ZOOM })
    }
  }, [spotForecast.data, app.spot, selectSpot, setPanelCollapsed])

  const selectedCellId =
    app.spot?.kind === 'cell' ? app.spot.cellId : (spotForecast.data?.cell_id ?? null)

  const onHotspot = (hotspot: Hotspot) =>
    openSpot({ kind: 'cell', cellId: hotspot.cell_ids[0] }, 'hotspot', {
      lat: hotspot.lat,
      lon: hotspot.lon,
      zoom: HOTSPOT_ZOOM,
    })
  const onPlace = (place: Place) => offerOrOpen(place.lat, place.lon, 'search')

  // On a phone the map runs under the sheet: camera moves keep a place clear of it, as it is
  // or at half, where a chosen spot opens (full leaves too little map to aim at).
  const mapPadding = useMemo<MapPadding | undefined>(() => {
    if (desktop) {
      return {
        ...DESKTOP_CHROME,
        left: panelCollapsed ? DESKTOP_CHROME.left : PANEL_INSET,
      }
    }
    if (!sheetLayout) return undefined
    return {
      top: sheetLayout.clearTop + PHONE_CHROME.top,
      right: PHONE_CHROME.right,
      left: PHONE_CHROME.left,
      bottom:
        visibleAt(snap === 'full' ? 'half' : snap, sheetLayout) + PHONE_CHROME.bottom,
    }
  }, [desktop, panelCollapsed, sheetLayout, snap])

  const introKey = app.species === 'combined' ? 'region' : app.species
  const introCopy = app.region.copy[language].intro[introKey]
  const offeredRegion = switchOffer
    ? (listRegions().find((r) => r.slug === switchOffer.slug) ?? null)
    : null

  const infoMenuActions = {
    onDisclaimer: () => setDisclaimerOpen(true),
    onCookies: () => setCookieBannerOpen(true),
    onNavigate: navigate,
  }

  const layer = analysis ? factors : seasonMode ? seasonMap : scores
  const scoresUnavailable = layer.isError && isClientError(layer.error)
  // In analysis mode: why nothing is drawn, if nothing is.
  const analysisNote = !factorDay
    ? t('analysis.unavailable')
    : factors.isError
      ? t(scoresUnavailable ? 'analysis.unavailable' : 'analysis.loadError')
      : factors.isPending
        ? t('analysis.loading')
        : app.indicators.length === 0
          ? t('analysis.noneOn')
          : undefined
  const status = locating
    ? t('locate.locating')
    : offeredRegion
      ? undefined
      : !online
        ? t('errors.offline')
        : analysis
          ? (analysisNote ?? (locateError && t(`locate.${locateError}`)))
          : layer.isError
            ? seasonMode
              ? t(scoresUnavailable ? 'season.noData' : 'map.loadError')
              : t(scoresUnavailable ? 'map.noData' : 'map.loadError')
            : layer.isPending || layer.isPlaceholderData
              ? t(seasonMode ? 'season.loading' : 'map.loading')
              : locateError && t(`locate.${locateError}`)

  return (
    <LazyMotion features={loadMotionFeatures} strict>
      <div
        className={styles.app}
        data-sheet={desktop ? undefined : snap}
        data-panel={desktop ? (panelCollapsed ? 'collapsed' : 'open') : undefined}
      >
        <main ref={mapAreaRef} className={styles.mapArea}>
          <ConditionsMap
            cells={analysis ? undefined : mapCells}
            scale={seasonMode ? 'goodDays' : 'score'}
            analysis={analysisView}
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
            userPosition={userPosition}
            lang={language}
            region={app.region}
            padding={mapPadding}
            // No zoom: the map only moves if the sheet opening over it would hide the tap.
            onCellClick={(cellId, lat, lon) =>
              openSpot({ kind: 'cell', cellId }, 'map', { lat, lon })
            }
            onPointClick={(lat, lon) => {
              if (!inBounds(lat, lon, app.region.bounds)) return
              openSpot({ kind: 'point', lat, lon }, 'map', { lat, lon })
            }}
            onHotspotClick={onHotspot}
          />
          <div className={styles.species}>
            <RegionSwitcher value={app.region} onChange={setRegion} />
            <SpeciesSwitcher
              value={app.species}
              onChange={handleSpeciesChange}
              species={app.region.species}
              noCombined={analysis}
            />
          </div>
          <div className={styles.cluster}>
            <button
              type="button"
              className={styles.fab}
              aria-label={t('analysis.toggle')}
              title={t('analysis.toggle')}
              aria-pressed={analysis}
              onClick={() => app.setMode(analysis ? 'map' : 'analysis')}
            >
              <LayersIcon />
            </button>
            <button
              type="button"
              className={styles.fab}
              aria-label={t('locate.center')}
              title={t('locate.center')}
              aria-busy={centerLocate.locating}
              onClick={centerLocate.locate}
            >
              <LocateIcon />
            </button>
            {!desktop && (
              <InfoMenu placement="left" className={styles.fab} {...infoMenuActions} />
            )}
          </div>
          {offeredRegion && (
            <p className={styles.status} role="status">
              {t('locate.switchOffer', { region: offeredRegion.name[language] })}
              <button type="button" onClick={acceptSwitch}>
                {t('locate.switch', { region: offeredRegion.name[language] })}
              </button>
              <button type="button" onClick={() => setSwitchOffer(null)}>
                {t('locate.dismissSwitch')}
              </button>
            </p>
          )}
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
              {analysis ? (
                <IndicatorPanel
                  layout={desktop ? 'panel' : 'row'}
                  chips={servedFactors}
                  active={app.indicators}
                  onToggle={app.toggleIndicator}
                  note={servedFactors ? undefined : analysisNote}
                  showSightings={app.sightingsVisible}
                  forestOn={app.forest}
                  onToggleForest={app.toggleForestLayer}
                />
              ) : (
                <Legend
                  showSightings={app.sightingsVisible}
                  season={app.season}
                  collapsible={!desktop}
                />
              )}
            </div>
            <div className={styles.dates}>
              <TimeBar
                today={app.today}
                date={app.date}
                window={DATE_WINDOW}
                historyStart={app.region.historyStart}
                season={app.season}
                seasons={seasonYears}
                onDate={handleDateChange}
                onSeason={app.setSeason}
                playback={
                  analysis
                    ? {
                        playing: playback.playing,
                        onToggle: playback.toggle,
                        onTouch: playback.pause,
                      }
                    : undefined
                }
              />
            </div>
          </div>
        </main>

        <Sheet
          mode={desktop ? 'panel' : 'sheet'}
          snap={snap}
          onSnap={setSnap}
          onGeometry={setSheetLayout}
          stage={mapAreaRef}
          collapsed={desktop && panelCollapsed}
          label={t(app.spot ? 'spot.title' : `views.${app.view}`)}
          header={
            <>
              <div className={styles.brand}>
                <h1 className={styles.wordmark}>{t('app.name')}</h1>
                {desktop && (
                  <div className={styles.headerActions}>
                    <InfoMenu
                      placement="below"
                      className={styles.headerButton}
                      {...infoMenuActions}
                    />
                    <button
                      type="button"
                      className={styles.headerButton}
                      aria-expanded={!panelCollapsed}
                      aria-controls="panel-body"
                      aria-label={t(panelCollapsed ? 'sheet.expand' : 'sheet.collapse')}
                      title={t(panelCollapsed ? 'sheet.expand' : 'sheet.collapse')}
                      onClick={() => setPanelCollapsed(!panelCollapsed)}
                    >
                      <ChevronIcon direction={panelCollapsed ? 'down' : 'up'} />
                    </button>
                  </div>
                )}
              </div>
              <PlaceSearch
                onSelect={onPlace}
                // Down to half, so the map shows the search for a fix and any error.
                onLocate={() => {
                  setSnap('half')
                  spotLocate.locate()
                }}
                locating={spotLocate.locating}
                // A phone: the sheet comes up full, so the list has room above the keyboard.
                onFocus={() => setSnap('full')}
                bounds={servedBounds()}
              />
            </>
          }
        >
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
              {app.route.kind === 'region' && (
                <div className={styles.intro}>
                  <p>{t(`lede.${introKey}`)}</p>
                  <button
                    type="button"
                    className={styles.more}
                    aria-expanded={introOpen}
                    aria-controls="intro-more"
                    onClick={() => setIntroOpen((open) => !open)}
                  >
                    {t('lede.more')}
                    <ChevronIcon direction={introOpen ? 'up' : 'down'} />
                  </button>
                  {/* Folded, not left out: it is what the page says to search engines too. */}
                  <p id="intro-more" hidden={!introOpen}>
                    {introCopy}
                  </p>
                </div>
              )}
              <ViewTabs
                value={app.view}
                panelId="sheet-view"
                onChange={(view) => {
                  track({ name: 'view-switch', data: { view } })
                  app.setView(view)
                  setSnap((current) => (current === 'peek' ? 'half' : current))
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
                      onReplayDay={handleDateChange}
                      sightingsVisible={app.sightingsVisible}
                      onSightingsVisibleChange={app.setSightingsVisible}
                      plausible={plausible}
                    />
                  )}
                  {app.view === 'outlook' && (
                    <OutlookPanel
                      species={app.species}
                      onSpecies={handleSpeciesChange}
                      comuni={comuni.data?.comuni}
                      comune={app.comune}
                      onComune={chooseComune}
                      outlook={outlook.data}
                      isLoading={outlook.isPending && outlook.fetchStatus !== 'idle'}
                      isError={outlook.isError}
                      onRetry={() => void outlook.refetch()}
                      plausible={plausible}
                    />
                  )}
                </PanelBoundary>
              </div>
            </>
          )}
          <InstallBanner />
          <footer className={styles.footer}>
            <DataStatus
              online={online}
              updatedAt={dataStatus.data?.updated_at ?? undefined}
            />
            <p>{t('disclaimer.short')}</p>
            <nav className={styles.links} aria-label={t('footer.links')}>
              {FOOTER_PAGES.map(({ path, label }) => (
                <a
                  key={path}
                  href={path}
                  onClick={(event) => {
                    event.preventDefault()
                    navigate(path)
                  }}
                >
                  {t(label)}
                </a>
              ))}
              <button type="button" onClick={() => setDisclaimerOpen(true)}>
                {t('footer.disclaimer')}
              </button>
              <button type="button" onClick={() => setCookieBannerOpen(true)}>
                {t('footer.cookies')}
              </button>
              <a
                className={styles.github}
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={t('nav.github')}
                title={t('nav.github')}
              >
                <GitHubIcon />
              </a>
            </nav>
          </footer>
        </Sheet>

        {app.route.kind === 'static' && app.route.page === 'credits' && (
          <CreditsPage
            backHref={regionPath(app.region.slug)}
            onBack={() => navigate(regionPath(app.region.slug))}
          />
        )}
        {app.route.kind === 'static' && app.route.page === 'terms' && (
          <TermsPage
            backHref={regionPath(app.region.slug)}
            onBack={() => navigate(regionPath(app.region.slug))}
            onDisclaimerClick={() => setDisclaimerOpen(true)}
            onPrivacyClick={() => navigate('/privacy')}
          />
        )}
        {app.route.kind === 'static' && app.route.page === 'privacy' && (
          <PrivacyPage
            backHref={regionPath(app.region.slug)}
            onBack={() => navigate(regionPath(app.region.slug))}
            onDisclaimerClick={() => setDisclaimerOpen(true)}
          />
        )}
        <DisclaimerDialog
          open={disclaimerOpen}
          onClose={() => setDisclaimerOpen(false)}
        />
        <CookieBanner
          open={cookieBannerOpen}
          onClose={() => setCookieBannerOpen(false)}
          onPrivacyClick={() => {
            setCookieBannerOpen(false)
            navigate('/privacy')
          }}
        />
      </div>
    </LazyMotion>
  )
}

function Root() {
  const app = useAppState()
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const overview = useOverview(app.species, app.date, app.today, app.route.kind === 'hub')

  useEffect(() => {
    if (app.route.kind === 'hub') {
      document.title = t('seo.hub.title')
      setDocumentDescription(t('seo.hub.description'))
      setDocumentCanonical(`${SITE_URL}/`)
      setDocumentRobots(false)
      const siteRoute = siteRouteFor(app.route)
      setDocumentJsonLd(siteRoute && structuredData(siteRoute, currentLanguage()))
      return
    }
    if (app.route.kind === 'region') {
      const seoKey = app.route.species === 'combined' ? 'region' : app.route.species
      const seo = app.route.region.copy[language].seo[seoKey]
      document.title = seo.title
      setDocumentDescription(seo.description)
      setDocumentCanonical(`${SITE_URL}${app.path}`)
      setDocumentRobots(false)
      const siteRoute = siteRouteFor(app.route)
      setDocumentJsonLd(siteRoute && structuredData(siteRoute, currentLanguage()))
      return
    }
    const key = seoKeyForRoute(app.route)
    document.title = t(key ? `seo.${key}.title` : 'notFound.title')
    setDocumentDescription(key ? t(`seo.${key}.description`) : undefined)
    setDocumentCanonical(key ? `${SITE_URL}${app.path}` : undefined)
    setDocumentRobots(key === null)
    const siteRoute = siteRouteFor(app.route)
    setDocumentJsonLd(siteRoute && structuredData(siteRoute, currentLanguage()))
  }, [app.route, app.path, t, language, i18n.resolvedLanguage])

  if (app.route.kind === 'not-found') return <NotFoundPage />
  if (app.route.kind === 'hub') {
    return (
      <HubShell
        overview={overview.data?.regions}
        overviewPending={overview.isPending}
        onSelectRegion={(slug) => {
          rememberRegion(slug)
          app.navigate(regionPath(slug))
        }}
      />
    )
  }
  return <MapScreen />
}

/** Hub with the same first-visit disclaimer and cookie banner as the map. */
function HubShell({
  overview,
  overviewPending,
  onSelectRegion,
}: {
  overview: RegionOverview[] | undefined
  overviewPending: boolean
  onSelectRegion: (slug: string) => void
}) {
  const { navigate } = useAppState()
  const [disclaimerOpen, setDisclaimerOpen] = useState(() => !disclaimerAccepted())
  const [cookieBannerOpen, setCookieBannerOpen] = useState(() => getConsent() === null)

  return (
    <>
      <HubPage
        overview={overview}
        overviewPending={overviewPending}
        onSelectRegion={onSelectRegion}
        onNavigate={navigate}
        onDisclaimer={() => setDisclaimerOpen(true)}
        onCookies={() => setCookieBannerOpen(true)}
      />
      <DisclaimerDialog open={disclaimerOpen} onClose={() => setDisclaimerOpen(false)} />
      <CookieBanner
        open={cookieBannerOpen}
        onClose={() => setCookieBannerOpen(false)}
        onPrivacyClick={() => {
          setCookieBannerOpen(false)
          navigate('/privacy')
        }}
      />
    </>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppStateProvider>
        <Root />
      </AppStateProvider>
    </QueryClientProvider>
  )
}
