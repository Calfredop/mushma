import { useTranslation } from 'react-i18next'
import type { DayScore } from '../api/queries'
import { ScoreChip } from '../components/ScoreChip'
import { intlLocale, type Language } from '../i18n'
import { explainScore, type FactorBreakdown } from '../score/impact'
import type { Species } from '../state/urlState'
import { formatDayLong } from '../time/days'
import panel from './panel.module.css'
import styles from './WhyBreakdown.module.css'

interface Props {
  species: Species
  day: DayScore
  isForecast: boolean
}

export function WhyBreakdown({ species, day, isForecast }: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const locale = intlLocale(language)
  const explanation = explainScore(day.factors)
  const number = new Intl.NumberFormat(locale, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })

  const label = (factor: FactorBreakdown) =>
    i18n.exists(factor.i18n_key)
      ? t(factor.i18n_key as 'factor.season')
      : t('why.unknownFactor', { key: factor.key })

  const percent = (impact: number) =>
    impact > 0 && impact < 0.005 ? '<1' : String(Math.round(impact * 100))

  const blockedLabels = new Intl.ListFormat(locale, { type: 'conjunction' }).format(
    day.factors.filter((f) => explanation.blockedBy.includes(f.key)).map(label),
  )

  return (
    <section className={styles.why} aria-labelledby="why-title">
      <header className={styles.header}>
        <div>
          <h3 id="why-title" className={styles.title}>
            {t('why.title')}
          </h3>
          <p className={panel.subtitle}>
            {t('why.subtitle', {
              species: t(`species.${species}.name`),
              date: formatDayLong(day.date, locale),
            })}
          </p>
        </div>
        <ScoreChip score={day.score} size="large" />
      </header>

      {explanation.blockedBy.length > 0 && (
        <p className={styles.summary}>{t('why.blocked', { factors: blockedLabels })}</p>
      )}
      {explanation.nothingHolding && (
        <p className={styles.summary}>{t('why.nothingHolding')}</p>
      )}

      <div className={styles.columns} aria-hidden="true">
        <span>{t('why.favourable')}</span>
        <span>{t('why.holdsBack')}</span>
      </div>
      <ul className={styles.factors}>
        {explanation.factors.map((factor) => (
          <li
            key={factor.key}
            className={styles.factor}
            data-blocking={explanation.blockedBy.includes(factor.key)}
          >
            <span className={styles.name}>{label(factor)}</span>
            <span className={styles.impactText}>
              {factor.impact > 0 &&
                t('why.holdsBackValue', { percent: percent(factor.impact) })}
            </span>
            <span className={styles.valueCell}>
              <span
                className={styles.track}
                role="meter"
                aria-label={label(factor)}
                aria-valuemin={0}
                aria-valuemax={1}
                aria-valuenow={Number(factor.value.toFixed(2))}
              >
                <span
                  className={styles.valueFill}
                  style={{ width: `${factor.value * 100}%` }}
                />
              </span>
              <span className={styles.value}>{number.format(factor.value)}</span>
            </span>
            <span className={styles.track} aria-hidden="true">
              <span
                className={styles.impactFill}
                style={{ width: `${factor.impact * 100}%` }}
              />
            </span>
          </li>
        ))}
      </ul>

      <p className={panel.note}>{t('why.explain')}</p>
      {isForecast && (
        <p className={styles.forecast}>
          <span className={styles.hatch} aria-hidden="true" />
          {t('why.forecastNote')}
        </p>
      )}
    </section>
  )
}
