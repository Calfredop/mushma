import { useTranslation } from 'react-i18next'
import type { Comune, OutlookPeriod, OutlookResponse } from '../api/queries'
import { AreaPicker } from '../components/AreaPicker'
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
import { SPECIES, type Species, type SpeciesOrCombined } from '../state/urlState'
import { addDays, formatDayMonth, formatMonth } from '../time/days'
import styles from './OutlookPanel.module.css'
import panel from './panel.module.css'

interface Props {
  species: SpeciesOrCombined
  onSpecies: (species: Species) => void
  comuni: Comune[] | undefined
  comune: string | null
  onComune: (comune: string | null) => void
  outlook: OutlookResponse | undefined
  isLoading: boolean
  isError: boolean
  onRetry: () => void
}

const TILT_MARK = { better: '▲', usual: '●', worse: '▼', unknown: '?' } as const

function yearsLabel(years: number[]): string {
  if (years.length === 0) return ''
  const sorted = [...years].sort()
  return sorted.length === 1
    ? String(sorted[0])
    : `${sorted[0]}–${sorted[sorted.length - 1]}`
}

/** The season so far and the weeks and months ahead: an outlook, never a forecast. */
export function OutlookPanel({
  species,
  onSpecies,
  comuni,
  comune,
  onComune,
  outlook,
  isLoading,
  isError,
  onRetry,
}: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const locale = intlLocale(language)

  return (
    <section className={panel.section} aria-labelledby="outlook-title">
      <header className={panel.header}>
        <div className={styles.titleRow}>
          <h2 id="outlook-title" className={panel.title}>
            {t('outlook.title')}
          </h2>
          <span className={styles.badge}>{t('outlook.badge')}</span>
        </div>
        {species !== 'combined' && (
          <p className={panel.subtitle}>
            {t('outlook.subtitle', {
              species: t(`species.${species}.name`),
              area:
                !outlook || outlook.area.kind === 'region'
                  ? t('app.region')
                  : outlook.area.name,
            })}
          </p>
        )}
      </header>

      {species === 'combined' ? (
        <div className={styles.pick}>
          <p className={panel.note}>{t('outlook.pickSpecies')}</p>
          <div className={styles.pickButtons}>
            {SPECIES.map((sp) => (
              <button
                key={sp}
                type="button"
                className={styles.pickButton}
                onClick={() => onSpecies(sp)}
              >
                {t(`species.${sp}.name`)}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <>
          <AreaPicker comuni={comuni} value={comune} onChange={onComune} />
          {isLoading && <p className={panel.status}>{t('outlook.loading')}</p>}
          {isError && (
            <p className={panel.status} role="alert">
              {t('outlook.loadError')}{' '}
              <button type="button" className={panel.linkButton} onClick={onRetry}>
                {t('map.retry')}
              </button>
            </p>
          )}
          {outlook && (
            <OutlookBody outlook={outlook} language={language} locale={locale} />
          )}
        </>
      )}
    </section>
  )
}

function OutlookBody({
  outlook,
  language,
  locale,
}: {
  outlook: OutlookResponse
  language: Language
  locale: string
}) {
  const { t } = useTranslation()
  const speciesName = t(`species.${outlook.species}.name`)
  const soFar = outlook.season_to_date
  const verdict = soFar ? seasonVerdict(soFar.good_days, soFar.good_days_typical) : null
  const rain = soFar ? rainPercent(soFar.rain) : null
  const delta = soFar ? temperatureDelta(soFar.temperature) : null
  const pastYears = yearsLabel(outlook.baseline.score_years)
  const windowText = t('outlook.window', {
    start: formatDayMonth(outlook.window.start, locale),
    end: formatDayMonth(outlook.window.end, locale),
  })

  return (
    <>
      {soFar && soFar.through >= outlook.window.start && (
        <article className={styles.card} aria-labelledby="so-far-title">
          <header className={styles.cardHeader}>
            <h3 id="so-far-title" className={styles.cardTitle}>
              {t('outlook.soFarTitle')}
            </h3>
            {verdict && (
              <span className={styles.verdict} data-verdict={verdict}>
                {t(`verdict.${verdict}`)}
              </span>
            )}
          </header>
          <dl className={styles.facts}>
            <div>
              <dt>{t('outlook.goodDays')}</dt>
              <dd>
                {formatDays(soFar.good_days, language)}
                {soFar.good_days_typical !== null &&
                  soFar.good_days_typical !== undefined && (
                    <span className={styles.aside}>
                      {' '}
                      {t('outlook.typicalToDate', {
                        typical: formatDays(soFar.good_days_typical, language),
                      })}
                    </span>
                  )}
              </dd>
            </div>
            {soFar.rain && rain !== null && (
              <div>
                <dt>{t('outlook.rain')}</dt>
                <dd>
                  {t('outlook.rainValue', {
                    mm: formatMm(soFar.rain.total_mm, language),
                    percent: formatPercent(rain, language),
                  })}
                </dd>
              </div>
            )}
            {delta !== null && (
              <div>
                <dt>{t('outlook.temperature')}</dt>
                <dd>
                  {t('outlook.temperatureValue', { delta: formatDelta(delta, language) })}
                </dd>
              </div>
            )}
          </dl>
          <p className={panel.note}>
            {soFar.weather_through
              ? t('outlook.soFarNote', {
                  start: formatDayMonth(outlook.window.start, locale),
                  end: formatDayMonth(soFar.through, locale),
                  weather: formatDayMonth(soFar.weather_through, locale),
                })
              : t('outlook.soFarNoteScores', {
                  start: formatDayMonth(outlook.window.start, locale),
                  end: formatDayMonth(soFar.through, locale),
                })}
          </p>
        </article>
      )}

      <h3 className={styles.sectionTitle}>{t('outlook.periodsTitle')}</h3>
      {outlook.periods.length === 0 ? (
        <p className={panel.status}>
          {t('outlook.outOfSeason', { species: speciesName, window: windowText })}
        </p>
      ) : (
        <ol className={styles.periods}>
          {outlook.periods.map((period) => (
            <PeriodRow
              key={period.start}
              period={period}
              language={language}
              locale={locale}
            />
          ))}
        </ol>
      )}

      <details className={styles.how}>
        <summary>{t('outlook.howTitle')}</summary>
        <p>
          {t('outlook.how1', {
            years: pastYears,
            share: formatPercent(outlook.good_share * 100, language),
          })}
        </p>
        <p>
          {t('outlook.how2', {
            species: speciesName,
            min: outlook.rain_lead.min_days,
            max: outlook.rain_lead.max_days,
            wetter: formatPercent(outlook.rain_tilt.wetter_pct, language),
            drier: formatPercent(outlook.rain_tilt.drier_pct, language),
          })}
        </p>
        <p>{t('outlook.how3')}</p>
        {outlook.issued && (
          <p className={panel.note}>
            {t('outlook.issued', { date: formatDayMonth(outlook.issued, locale) })}
          </p>
        )}
      </details>
    </>
  )
}

function PeriodRow({
  period,
  language,
  locale,
}: {
  period: OutlookPeriod
  language: Language
  locale: string
}) {
  const { t } = useTranslation()
  // A month the season window clips (1–20 December) gives its dates, not the month's name.
  const wholeMonth =
    period.kind === 'month' &&
    period.start.endsWith('-01') &&
    addDays(period.end, 1).endsWith('-01')
  const label = wholeMonth
    ? t('outlook.monthPeriod', {
        month: formatMonth(Number(period.start.slice(5, 7)), locale, 'long'),
      })
    : t('outlook.weekPeriod', {
        start: formatDayMonth(period.start, locale),
        end: formatDayMonth(period.end, locale),
      })
  const tally =
    period.past_years > 0
      ? t('outlook.pastSeasons', {
          good: period.past_good_years,
          years: period.past_years,
        })
      : t('outlook.noPast')

  return (
    <li className={styles.period} data-outlook={period.outlook}>
      <div className={styles.periodHead}>
        <span className={styles.periodLabel}>{label}</span>
        <span className={styles.tilt} data-outlook={period.outlook}>
          <span aria-hidden="true">{TILT_MARK[period.outlook]}</span>
          {t(`outlook.tilt.${period.outlook}`)}
        </span>
      </div>
      <div className={styles.periodBody}>
        {period.past_years > 0 && (
          <span className={styles.tally} aria-hidden="true">
            {Array.from({ length: period.past_years }, (_, i) => (
              <span
                key={i}
                className={styles.dot}
                data-good={i < period.past_good_years}
              />
            ))}
          </span>
        )}
        <span className={styles.tallyText}>{tally}</span>
      </div>
      {period.lead_rain_pct !== null && period.lead_rain_pct !== undefined && (
        <p className={styles.lead}>
          {t('outlook.leadRain', {
            percent: formatPercent(period.lead_rain_pct, language),
          })}
        </p>
      )}
    </li>
  )
}
