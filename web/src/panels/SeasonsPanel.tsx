import { useTranslation } from 'react-i18next'
import type {
  Comune,
  SeasonMapResponse,
  SeasonsResponse,
  SeasonSummary,
  SpeciesProfile,
  TaxonProfile,
} from '../api/queries'
import { AreaPicker } from '../components/AreaPicker'
import { SpeciesBreakdown } from '../components/SpeciesBreakdown'
import {
  formatDays,
  formatDelta,
  formatMm,
  formatPercent,
  rainPercent,
  seasonVerdict,
  temperatureDelta,
} from '../history/present'
import { intlLocale, type Language } from '../i18n'
import type { RegionDefinition } from '../regions'
import type { SpeciesOrCombined } from '../state/urlState'
import { formatDayLong, formatDayMonth, formatMonth, type IsoDate } from '../time/days'
import panel from './panel.module.css'
import { PlausibleSpecies, type PlausibleState } from './PlausibleSpecies'
import styles from './SeasonsPanel.module.css'

interface Props {
  species: SpeciesOrCombined
  /** The region on the map: the whole-region area is called by its name. */
  region: Pick<RegionDefinition, 'name' | 'whole'>
  comuni: Comune[] | undefined
  comune: string | null
  onComune: (comune: string | null) => void
  seasons: SeasonsResponse | undefined
  isLoading: boolean
  isError: boolean
  onRetry: () => void
  /** The season on the map. */
  selected: number | null
  onSelect: (season: number | null) => void
  /** The selected season's map data: its comuni ranked by good days. */
  seasonMap: SeasonMapResponse | undefined
  onReplayDay: (date: IsoDate) => void
  sightingsVisible: boolean
  onSightingsVisibleChange: (visible: boolean) => void
  /** The chosen zone's plausible species; not shown for the whole region. */
  plausible?: PlausibleState
}

const TOP_COMUNI = 5

function yearsLabel(years: number[]): string {
  if (years.length === 0) return ''
  const sorted = [...years].sort()
  return sorted.length === 1
    ? String(sorted[0])
    : `${sorted[0]}–${sorted[sorted.length - 1]}`
}

export function SeasonsPanel({
  species,
  region,
  comuni,
  comune,
  onComune,
  seasons,
  isLoading,
  isError,
  onRetry,
  selected,
  onSelect,
  seasonMap,
  onReplayDay,
  sightingsVisible,
  onSightingsVisibleChange,
  plausible,
}: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const locale = intlLocale(language)
  const rows = seasons ? [...seasons.seasons].reverse() : []
  // The zone's own profile only: a response for the zone picked before is not this one's.
  const zone =
    comune !== null && plausible
      ? {
          ...plausible,
          data: plausible.data?.area.code === comune ? plausible.data : undefined,
        }
      : null
  const scale =
    Math.max(1, ...rows.flatMap((s) => [s.good_days, s.good_days_typical ?? 0])) * 1.04
  const chosen = rows.find((s) => s.year === selected)
  const areaName =
    !seasons || seasons.area.kind === 'region' ? region.name[language] : seasons.area.name
  const threshold = seasons
    ? new Intl.NumberFormat(locale, { minimumFractionDigits: 1 }).format(
        seasons.good_score,
      )
    : ''

  return (
    <section className={panel.section} aria-labelledby="seasons-title">
      <header className={panel.header}>
        <h2 id="seasons-title" className={panel.title}>
          {t('seasons.title')}
        </h2>
        <p className={panel.subtitle}>
          {t('seasons.subtitle', {
            species: t(`species.${species}.name`),
            area: areaName,
          })}
        </p>
      </header>

      <AreaPicker
        wholeRegion={region.whole[language]}
        comuni={comuni}
        value={comune}
        onChange={onComune}
      />
      {zone && <PlausibleSpecies plausible={zone} />}

      {isLoading && <p className={panel.status}>{t('seasons.loading')}</p>}
      {isError && (
        <p className={panel.status} role="alert">
          {t('seasons.loadError')}{' '}
          <button type="button" className={panel.linkButton} onClick={onRetry}>
            {t('map.retry')}
          </button>
        </p>
      )}
      {seasons && rows.length === 0 && (
        <p className={panel.status}>{t('seasons.empty')}</p>
      )}

      {rows.length > 0 && seasons && (
        <div className={styles.comparison}>
          <p className={panel.note}>{t('seasons.intro', { threshold })}</p>
          <div className={styles.head} aria-hidden="true">
            <span>{t('seasons.columns.year')}</span>
            <span>{t('seasons.columns.goodDays')}</span>
            <span className={styles.num}>{t('seasons.columns.rain')}</span>
            <span className={styles.num}>{t('seasons.columns.temperature')}</span>
          </div>
          <ol className={styles.rows}>
            {rows.map((season) => (
              <SeasonRow
                key={season.year}
                season={season}
                scale={scale}
                language={language}
                selected={season.year === selected}
                onSelect={() => onSelect(season.year === selected ? null : season.year)}
              />
            ))}
          </ol>
          <p className={styles.key}>
            <span className={styles.keyTick} aria-hidden="true" />
            {t('seasons.typical', { years: yearsLabel(seasons.baseline.score_years) })}
          </p>
          {selected === null && <p className={panel.note}>{t('seasons.pickHint')}</p>}
        </div>
      )}

      {chosen && seasons && (
        <SeasonDetail
          season={chosen}
          areaName={areaName}
          isRegion={seasons.area.kind === 'region'}
          seasonMap={seasonMap?.year === chosen.year ? seasonMap : undefined}
          weatherYears={yearsLabel(seasons.baseline.weather_years)}
          language={language}
          onReplayDay={onReplayDay}
          onComune={onComune}
          species={zone?.data?.species}
        />
      )}

      <label className={styles.toggle}>
        <input
          type="checkbox"
          role="switch"
          checked={sightingsVisible}
          onChange={(event) => onSightingsVisibleChange(event.target.checked)}
        />
        <span>
          <span className={styles.toggleLabel}>{t('sightings.toggle')}</span>
          <span className={panel.note}>
            {selected !== null
              ? t('sightings.seasonWindow', { year: selected })
              : t('sightings.pickSeason')}
          </span>
        </span>
      </label>
    </section>
  )
}

interface RowProps {
  season: SeasonSummary
  scale: number
  language: Language
  selected: boolean
  onSelect: () => void
}

function SeasonRow({ season, scale, language, selected, onSelect }: RowProps) {
  const { t } = useTranslation()
  const rain = rainPercent(season.rain)
  const delta = temperatureDelta(season.temperature)
  const days = formatDays(season.good_days, language)
  const typical =
    season.good_days_typical !== null && season.good_days_typical !== undefined
      ? formatDays(season.good_days_typical, language)
      : null
  const label = [
    t(season.complete ? 'seasons.rowLabel' : 'seasons.rowLabelSoFar', {
      year: season.year,
      days,
    }),
    typical && t('seasons.rowTypical', { typical }),
    rain !== null && t('seasons.rainLabel', { percent: formatPercent(rain, language) }),
    delta !== null && t('seasons.tempLabel', { delta: formatDelta(delta, language) }),
  ]
    .filter(Boolean)
    .join(', ')

  return (
    <li>
      <button
        type="button"
        className={styles.row}
        aria-pressed={selected}
        aria-label={label}
        data-complete={season.complete}
        onClick={onSelect}
      >
        <span className={styles.year} aria-hidden="true">
          {season.year}
        </span>
        <span className={styles.barCell} aria-hidden="true">
          <span className={styles.track}>
            <span
              className={styles.bar}
              style={{ width: `${(season.good_days / scale) * 100}%` }}
            />
            {season.good_days_typical !== null &&
              season.good_days_typical !== undefined && (
                <span
                  className={styles.tick}
                  style={{ left: `${(season.good_days_typical / scale) * 100}%` }}
                />
              )}
          </span>
          <span className={styles.days}>
            {days}
            {!season.complete && (
              <span className={styles.soFar}>{t('seasons.soFar')}</span>
            )}
          </span>
        </span>
        <span className={styles.num} aria-hidden="true">
          {rain !== null ? formatPercent(rain, language) : '–'}
        </span>
        <span className={styles.num} aria-hidden="true">
          {delta !== null ? `${formatDelta(delta, language)}°` : '–'}
        </span>
      </button>
    </li>
  )
}

interface DetailProps {
  season: SeasonSummary
  areaName: string
  isRegion: boolean
  seasonMap: SeasonMapResponse | undefined
  weatherYears: string
  language: Language
  onReplayDay: (date: IsoDate) => void
  onComune: (comune: string | null) => void
  /** Every species' and taxon's seasons in the zone, to break this one down. */
  species: SpeciesProfile[] | undefined
}

/** One season's good days for a species or taxon; 0 for a season it has none stored. */
function goodDaysIn(entry: SpeciesProfile | TaxonProfile, year: number): number {
  return entry.seasons.find((s) => s.year === year)?.good_days ?? 0
}

function SeasonDetail({
  season,
  areaName,
  isRegion,
  seasonMap,
  weatherYears,
  language,
  onReplayDay,
  onComune,
  species,
}: DetailProps) {
  const { t } = useTranslation()
  const locale = intlLocale(language)
  const daysIn = (entry: SpeciesProfile | TaxonProfile) => goodDaysIn(entry, season.year)
  const verdict = seasonVerdict(season.good_days, season.good_days_typical)
  const rain = rainPercent(season.rain)
  const delta = temperatureDelta(season.temperature)
  const months = season.months.filter(
    (m) =>
      m.month >= Number(season.window.start.slice(5, 7)) &&
      m.month <= Number(season.window.end.slice(5, 7)),
  )

  return (
    <article className={styles.detail} aria-labelledby="season-detail-title">
      <header className={styles.detailHeader}>
        <h3 id="season-detail-title" className={styles.detailTitle}>
          {t('seasons.detailTitle', { year: season.year, area: areaName })}
        </h3>
        {verdict && (
          <span className={styles.verdict} data-verdict={verdict}>
            {t(`verdict.${verdict}`)}
          </span>
        )}
      </header>
      {!season.complete && (
        <p className={panel.note}>
          {t('seasons.partial', { date: formatDayLong(season.through, locale) })}
        </p>
      )}

      <dl className={styles.facts}>
        <div>
          <dt>{t('seasons.goodDays')}</dt>
          <dd>
            {formatDays(season.good_days, language)}
            {season.good_days_typical !== null &&
              season.good_days_typical !== undefined && (
                <span className={styles.aside}>
                  {' '}
                  {t('seasons.typicalValue', {
                    typical: formatDays(season.good_days_typical, language),
                  })}
                </span>
              )}
          </dd>
        </div>
        <div>
          <dt>{t('seasons.bestDay')}</dt>
          <dd>
            {season.peak_date ? (
              <>
                {t('seasons.peak', {
                  date: formatDayMonth(season.peak_date, locale),
                  percent: formatPercent(season.peak_share * 100, language),
                })}{' '}
                <button
                  type="button"
                  className={panel.linkButton}
                  onClick={() => onReplayDay(season.peak_date!)}
                >
                  {t('seasons.replayPeak')}
                </button>
              </>
            ) : (
              t('seasons.noPeak')
            )}
          </dd>
        </div>
        {season.rain && rain !== null && (
          <div>
            <dt>{t('seasons.rain')}</dt>
            <dd>
              {t('seasons.rainValue', {
                mm: formatMm(season.rain.total_mm, language),
                percent: formatPercent(rain, language),
              })}
            </dd>
          </div>
        )}
        {delta !== null && (
          <div>
            <dt>{t('seasons.temperature')}</dt>
            <dd>
              {t('seasons.temperatureValue', { delta: formatDelta(delta, language) })}
            </dd>
          </div>
        )}
        <div>
          <dt>{t('seasons.sightings')}</dt>
          <dd>{t('seasons.sightingsValue', { count: season.sightings })}</dd>
        </div>
      </dl>
      {season.weather_through && (
        <p className={panel.note}>
          {t('seasons.weatherNote', {
            start: formatDayMonth(season.window.start, locale),
            end: formatDayMonth(season.weather_through, locale),
            years: weatherYears,
          })}
        </p>
      )}

      {species && (
        <>
          <h4 className={styles.subhead}>{t('plausible.seasonTitle')}</h4>
          <SpeciesBreakdown
            label={t('plausible.seasonTitle')}
            profiles={species}
            value={daysIn}
            scale={Math.max(1, ...species.map(daysIn))}
            format={(days) => formatDays(days, language)}
            tone="good"
          />
          <p className={panel.note}>{t('plausible.seasonNote')}</p>
        </>
      )}

      {months.length > 0 && (
        <>
          <h4 className={styles.subhead}>{t('seasons.months')}</h4>
          <ol className={styles.months}>
            {months.map((month) => {
              const monthRain = rainPercent(month.rain)
              const monthDelta = temperatureDelta(month.temperature)
              const daysInMonth = new Date(
                Date.UTC(season.year, month.month, 0),
              ).getUTCDate()
              return (
                <li
                  key={month.month}
                  className={styles.month}
                  aria-label={t('seasons.monthLabel', {
                    month: formatMonth(month.month, locale, 'long'),
                    days: formatDays(month.good_days, language),
                    rain: monthRain !== null ? formatPercent(monthRain, language) : '–',
                    delta: monthDelta !== null ? formatDelta(monthDelta, language) : '–',
                  })}
                >
                  <span className={styles.monthTrack} aria-hidden="true">
                    <span
                      className={styles.monthBar}
                      style={{
                        height: `${Math.max(month.good_days > 0 ? 4 : 0, (month.good_days / daysInMonth) * 100)}%`,
                      }}
                    />
                  </span>
                  <span className={styles.monthDays} aria-hidden="true">
                    {formatDays(month.good_days, language)}
                  </span>
                  <span className={styles.monthName} aria-hidden="true">
                    {formatMonth(month.month, locale)}
                  </span>
                  <span className={styles.monthWeather} aria-hidden="true">
                    {monthRain !== null ? formatPercent(monthRain, language) : '–'}
                  </span>
                  <span className={styles.monthWeather} aria-hidden="true">
                    {monthDelta !== null ? `${formatDelta(monthDelta, language)}°` : '–'}
                  </span>
                </li>
              )
            })}
          </ol>
          <p className={styles.monthKey}>{t('seasons.monthKey')}</p>
        </>
      )}

      {isRegion && seasonMap && seasonMap.comuni.length > 0 && (
        <>
          <h4 className={styles.subhead}>{t('seasons.bestComuni')}</h4>
          <ol className={styles.comuni}>
            {seasonMap.comuni.slice(0, TOP_COMUNI).map((c) => (
              <li key={c.code}>
                <button
                  type="button"
                  className={styles.comune}
                  aria-label={t('seasons.showComune', { name: c.name })}
                  onClick={() => onComune(c.code)}
                >
                  <span>{c.name}</span>
                  <span className={styles.comuneDays}>
                    {t('seasons.comuneDays', { days: formatDays(c.good_days, language) })}
                  </span>
                </button>
              </li>
            ))}
          </ol>
        </>
      )}
    </article>
  )
}
