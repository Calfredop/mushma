import { useId, useState } from 'react'
import { useTranslation } from 'react-i18next'
import type { DayScore, HabitatShare } from '../api/queries'
import { ChevronIcon } from '../components/icons'
import { ScoreChip } from '../components/ScoreChip'
import { usePersistentFlag } from '../hooks/usePersistentFlag'
import { intlLocale, type Language } from '../i18n'
import { usesRain, usesTerrain } from '../score/detail'
import { explainScore, type FactorBreakdown } from '../score/impact'
import type { Species } from '../state/urlState'
import { formatDayLong } from '../time/days'
import { FactorDetail } from './FactorDetail'
import panel from './panel.module.css'
import styles from './WhyBreakdown.module.css'

interface Props {
  species: Species
  day: DayScore
  isForecast: boolean
  /** The cell's forest types, for the habitat factor's detail. */
  habitats?: readonly HabitatShare[]
}

export function WhyBreakdown({ species, day, isForecast, habitats }: Props) {
  const { t, i18n } = useTranslation()
  const detailIds = useId()
  const [showAll, setShowAll] = usePersistentFlag('mushma.whyDetails')
  // A row the visitor opened or closed on its own; the switch resets them all.
  const [overrides, setOverrides] = useState<Record<string, boolean>>({})
  // The factors at full credit, folded into one row until it is opened.
  const [foldOpen, setFoldOpen] = useState(false)
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

  const isOpen = (key: string) => overrides[key] ?? showAll
  const toggleRow = (key: string) =>
    setOverrides((current) => ({ ...current, [key]: !(current[key] ?? showAll) }))
  const toggleAll = () => {
    setShowAll(!showAll)
    setOverrides({})
  }
  const rainDetailOpen = explanation.factors.some(
    (f) => isOpen(f.key) && usesRain(f.rule),
  )
  const terrainDetailOpen = explanation.factors.some(
    (f) => isOpen(f.key) && usesTerrain(f.rule),
  )

  // Fold the factors holding nothing back, when some others do. Not when the score is blocked
  // (every other factor then has no share, whatever its value), nor when nothing holds it back
  // (there would be nothing left beside the fold), nor with every detail on.
  const idle = explanation.factors.filter((f) => f.impact === 0)
  const folding =
    explanation.blockedBy.length === 0 &&
    !explanation.nothingHolding &&
    idle.length > 0 &&
    !showAll
  const shown = folding
    ? explanation.factors.filter((f) => f.impact > 0)
    : explanation.factors

  const row = (factor: (typeof explanation.factors)[number], hidden = false) => (
    <li
      key={factor.key}
      id={`${detailIds}-row-${factor.key}`}
      className={styles.factor}
      data-blocking={explanation.blockedBy.includes(factor.key)}
      hidden={hidden}
    >
      <button
        type="button"
        className={styles.name}
        aria-expanded={isOpen(factor.key)}
        aria-controls={isOpen(factor.key) ? `${detailIds}-${factor.key}` : undefined}
        onClick={() => toggleRow(factor.key)}
      >
        {label(factor)}
        <ChevronIcon direction={isOpen(factor.key) ? 'up' : 'down'} />
      </button>
      <span
        className={styles.track}
        role="meter"
        aria-label={label(factor)}
        aria-valuemin={0}
        aria-valuemax={1}
        aria-valuenow={Number(factor.value.toFixed(2))}
      >
        <span className={styles.valueFill} style={{ width: `${factor.value * 100}%` }} />
      </span>
      <span className={styles.value}>{number.format(factor.value)}</span>
      <span className={styles.brake}>
        {factor.impact > 0 &&
          t('why.holdsBackValue', { percent: percent(factor.impact) })}
      </span>
      {isOpen(factor.key) && (
        <FactorDetail
          factor={factor}
          date={day.date}
          id={`${detailIds}-${factor.key}`}
          habitats={habitats}
        />
      )}
    </li>
  )

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

      <div className={styles.tools}>
        <button
          type="button"
          role="switch"
          aria-checked={showAll}
          className={styles.switch}
          onClick={toggleAll}
        >
          <span className={styles.switchTrack} aria-hidden="true">
            <span className={styles.switchThumb} />
          </span>
          {t('why.detail.showAll')}
        </button>
      </div>

      {/* One grid for every row, so the bars, values and brakes line up down the list. */}
      <ul className={styles.factors}>
        <li role="presentation" className={styles.columns} aria-hidden="true">
          <span>{t('why.favourable')}</span>
          <span>{t('why.holdsBack')}</span>
        </li>
        {shown.map((factor) => row(factor))}
        {folding && (
          <li role="presentation" className={styles.foldRow}>
            <button
              type="button"
              className={styles.fold}
              aria-expanded={foldOpen}
              aria-controls={idle.map((f) => `${detailIds}-row-${f.key}`).join(' ')}
              onClick={() => setFoldOpen((open) => !open)}
            >
              {t('why.fold', { count: idle.length, value: number.format(1) })}
              <ChevronIcon direction={foldOpen ? 'up' : 'down'} />
            </button>
          </li>
        )}
        {folding && idle.map((factor) => row(factor, !foldOpen))}
      </ul>

      {rainDetailOpen && <p className={panel.note}>{t('why.detail.rainNote')}</p>}
      {terrainDetailOpen && <p className={panel.note}>{t('why.detail.terrainNote')}</p>}
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
