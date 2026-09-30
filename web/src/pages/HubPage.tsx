import { LazyMotion } from 'motion/react'
import { type MouseEvent, useMemo, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import type { RegionOverview, RegionTrend, TrendPoint } from '../api/queries'
import { ChevronIcon, CloseIcon, GitHubIcon, SearchIcon } from '../components/icons'
import { InfoMenu } from '../components/InfoMenu'
import { MapLoading } from '../components/MapLoading'
import { ScoreChip } from '../components/ScoreChip'
import { Sheet, type SheetLayout } from '../components/Sheet'
import { TrendKey, TrendLine } from '../components/TrendLine'
import { REPO_URL } from '../config'
import { useMediaQuery } from '../hooks/useMediaQuery'
import { intlLocale, type Language } from '../i18n'
import { HubMap } from '../map/HubMap'
import type { MapPadding } from '../map/padding'
import { matchesRegionName } from '../regions'
import { regionPath } from '../routes'
import { SCORE_CLASSES } from '../score/scale'
import { type Snap, visibleAt } from '../sheet/snaps'
import type { IsoDate } from '../time/days'
import styles from './HubPage.module.css'
import { type HubRegion, hubRegions } from './hubRegions'

/** Motion's animation features come after first paint (PRD → Mobile performance). */
const loadMotionFeatures = () =>
  import('../motionFeatures').then((module) => module.default)

/** The floating panel (--panel-width, inset --space-4) on a desktop's left. */
const PANEL_INSET = 16 + 400 + 16
const MARGIN = 16

const FOOTER_PAGES = [
  { path: '/credits', label: 'footer.credits' },
  { path: '/terms', label: 'footer.terms' },
  { path: '/privacy', label: 'footer.privacy' },
] as const

const plainClick = (event: MouseEvent) =>
  event.button === 0 &&
  !event.metaKey &&
  !event.ctrlKey &&
  !event.shiftKey &&
  !event.altKey

/** Every served region's last 15 days, for a line beside each row's score. */
export interface HubTrend {
  regions: RegionTrend[]
  today: IsoDate
}

interface HubPageProps {
  overview: RegionOverview[] | undefined
  /** Today's overview is still on its way: the rows wait for their numbers. */
  overviewPending: boolean
  trend?: HubTrend
  onSelectRegion: (slug: string) => void
  onNavigate: (path: string) => void
  onDisclaimer: () => void
  onCookies: () => void
}

/**
 * `/`: Italy on a full-bleed map, every region with its real boundary, the served ones coloured
 * by today's mean conditions score. The picker floats over it like the region's own panel: a
 * card on the left from 900px, a sheet to drag up on a phone.
 */
export function HubPage({
  overview,
  overviewPending,
  trend,
  onSelectRegion,
  onNavigate,
  onDisclaimer,
  onCookies,
}: HubPageProps) {
  const { t, i18n } = useTranslation()
  const language = (i18n.resolvedLanguage ?? 'it') as Language
  const desktop = useMediaQuery('(min-width: 900px)')
  // The list is the point of the page: a phone opens with it half up.
  const [snap, setSnap] = useState<Snap>('half')
  const [sheetLayout, setSheetLayout] = useState<SheetLayout | null>(null)
  const [highlighted, setHighlighted] = useState<string | null>(null)
  /** A region tapped on the map that the app doesn't serve yet. */
  const [uncovered, setUncovered] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  const mapAreaRef = useRef<HTMLElement>(null)

  const regions = useMemo(() => hubRegions(overview, language), [overview, language])
  // The search narrows the list only: the map keeps every region.
  const listed = regions.filter((entry) =>
    matchesRegionName(entry.region.name[language], query),
  )
  const trendRows = trend?.regions
  const trends = useMemo(
    () => new Map(trendRows?.map((row) => [row.region, row.days])),
    [trendRows],
  )

  const padding = useMemo<MapPadding | undefined>(() => {
    if (desktop) return { top: MARGIN, right: MARGIN, bottom: MARGIN, left: PANEL_INSET }
    if (!sheetLayout) return undefined
    return {
      top: sheetLayout.clearTop + MARGIN,
      right: MARGIN,
      left: MARGIN,
      // Full leaves too little map to frame Italy in: it stays framed as at half.
      bottom: visibleAt(snap === 'full' ? 'half' : snap, sheetLayout) + MARGIN,
    }
  }, [desktop, sheetLayout, snap])

  const select = (slug: string) => {
    setUncovered(null)
    onSelectRegion(slug)
  }

  const infoMenu = (
    <InfoMenu
      placement="below"
      className={styles.headerButton}
      onDisclaimer={onDisclaimer}
      onCookies={onCookies}
      onNavigate={onNavigate}
    />
  )

  return (
    <LazyMotion features={loadMotionFeatures} strict>
      <div className={styles.hub} data-sheet={desktop ? undefined : snap}>
        <main
          ref={mapAreaRef}
          className={styles.mapArea}
          aria-busy={overviewPending || undefined}
        >
          <HubMap
            regions={regions}
            highlighted={highlighted}
            padding={padding}
            lang={language}
            onHover={setHighlighted}
            onSelect={select}
            onUnserved={setUncovered}
          />
          {overviewPending && <MapLoading label={t('hub.loading')} />}
          {uncovered && (
            <p className={styles.status} role="status">
              {t('hub.notCovered', {
                region: t(`italyRegions.${uncovered}` as 'italyRegions.toscana'),
              })}
              <button type="button" onClick={() => setUncovered(null)}>
                {t('hub.dismiss')}
              </button>
            </p>
          )}
        </main>

        <Sheet
          mode={desktop ? 'panel' : 'sheet'}
          snap={snap}
          onSnap={setSnap}
          onGeometry={setSheetLayout}
          stage={mapAreaRef}
          label={t('hub.regions')}
          header={
            <>
              <div className={styles.brand}>
                <h1 className={styles.wordmark}>{t('app.name')}</h1>
                {infoMenu}
              </div>
              <p className={styles.lede}>{t('hub.lede')}</p>
            </>
          }
        >
          <section aria-labelledby="hub-regions-title">
            <div className={styles.listHead}>
              <h2 id="hub-regions-title" className={styles.listTitle}>
                {t('hub.regions')}
              </h2>
              <div className={styles.keys}>
                <ScaleKey />
                {trend && <TrendKey />}
              </div>
            </div>
            <div className={styles.search}>
              <SearchIcon />
              <input
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder={t('regions.searchPlaceholder')}
                aria-label={t('regions.search')}
                autoComplete="off"
                enterKeyHint="search"
              />
              {query && (
                <button
                  type="button"
                  className={styles.clear}
                  aria-label={t('search.clear')}
                  onClick={() => setQuery('')}
                >
                  <CloseIcon />
                </button>
              )}
            </div>
            {listed.length === 0 ? (
              <p className={styles.empty}>{t('regions.noResults')}</p>
            ) : (
              <ul className={styles.regionList}>
                {listed.map((entry) => (
                  <li key={entry.region.slug}>
                    <RegionRow
                      entry={entry}
                      trend={trends.get(entry.region.apiRegionId)}
                      today={trend?.today}
                      language={language}
                      pending={overviewPending}
                      highlighted={highlighted === entry.region.slug}
                      onHighlight={setHighlighted}
                      onSelect={select}
                    />
                  </li>
                ))}
              </ul>
            )}
            <p className={styles.more}>{t('hub.more')}</p>
          </section>
          <footer className={styles.footer}>
            <p>{t('disclaimer.short')}</p>
            <nav className={styles.links} aria-label={t('footer.links')}>
              {FOOTER_PAGES.map(({ path, label }) => (
                <a
                  key={path}
                  href={path}
                  onClick={(event) => {
                    if (!plainClick(event)) return
                    event.preventDefault()
                    onNavigate(path)
                  }}
                >
                  {t(label)}
                </a>
              ))}
              <button type="button" onClick={onDisclaimer}>
                {t('footer.disclaimer')}
              </button>
              <button type="button" onClick={onCookies}>
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
      </div>
    </LazyMotion>
  )
}

/** What the colours on the map and the chips in the list mean. */
function ScaleKey() {
  const { t } = useTranslation()
  return (
    <div className={styles.scaleKey}>
      <span>{t('hub.scaleTitle')}</span>
      <span className={styles.scale} aria-hidden="true">
        {SCORE_CLASSES.map((c) => (
          <span key={c.min} style={{ background: c.color }} />
        ))}
      </span>
    </div>
  )
}

interface RegionRowProps {
  entry: HubRegion
  /** The region's last 15 days, when the overview trend has them. */
  trend: TrendPoint[] | undefined
  today: IsoDate | undefined
  language: Language
  pending: boolean
  highlighted: boolean
  onHighlight: (slug: string | null) => void
  onSelect: (slug: string) => void
}

function RegionRow({
  entry,
  trend,
  today,
  language,
  pending,
  highlighted,
  onHighlight,
  onSelect,
}: RegionRowProps) {
  const { t } = useTranslation()
  const { region, meanScore, goodShare } = entry
  const percent = new Intl.NumberFormat(intlLocale(language), {
    style: 'percent',
    maximumFractionDigits: 0,
  })
  const summary =
    goodShare !== undefined
      ? t('hub.goodShare', { share: percent.format(goodShare) })
      : pending
        ? t('hub.loading')
        : t('hub.noScore')

  return (
    <a
      href={regionPath(region.slug)}
      className={styles.region}
      data-highlighted={highlighted || undefined}
      onClick={(event) => {
        if (!plainClick(event)) return
        event.preventDefault()
        onSelect(region.slug)
      }}
      onMouseEnter={() => onHighlight(region.slug)}
      onMouseLeave={() => onHighlight(null)}
      onFocus={() => onHighlight(region.slug)}
      onBlur={() => onHighlight(null)}
    >
      <span className={styles.regionText}>
        <span className={styles.regionName}>{region.name[language]}</span>
        <span className={styles.regionSummary}>{summary}</span>
      </span>
      {trend && today && (
        <TrendLine points={trend} today={today} subject={region.name[language]} />
      )}
      {meanScore !== undefined && <ScoreChip score={meanScore} />}
      <ChevronIcon direction="right" />
    </a>
  )
}
