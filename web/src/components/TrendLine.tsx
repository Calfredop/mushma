import { type PointerEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import { formatScore } from '../score/format'
import { scoreColor } from '../score/scale'
import {
  fittedChange,
  TREND_DAYS,
  type TrendDirection,
  trendDirection,
  trendDomain,
  type TrendPoint,
  trendStart,
} from '../score/trend'
import {
  daysBetween,
  formatDay,
  formatDayLong,
  formatDayMonth,
  type IsoDate,
} from '../time/days'
import styles from './TrendLine.module.css'

/** Drawing units: `small` sits in a list row, `large` spans a panel and scales with it. */
const GEOMETRY = {
  small: { width: 56, height: 20, pad: 3.5 },
  large: { width: 320, height: 64, pad: 7 },
} as const

interface Props {
  /** Scores per day, oldest first; days outside the window ending `today` are not drawn. */
  points: readonly TrendPoint[]
  today: IsoDate
  /** What the line follows, first in its accessible name: a species, a region, an area. */
  subject: string
  size?: 'small' | 'large'
}

/** Which way a score line is heading. The angle carries the direction; the colour repeats it. */
export function TrendArrow({
  direction,
  labelled = false,
}: {
  direction: TrendDirection
  /** Say it in words too, where there is room. */
  labelled?: boolean
}) {
  const { t } = useTranslation()
  return (
    <span className={styles.arrow} data-direction={direction}>
      <svg
        viewBox="0 0 16 16"
        width="16"
        height="16"
        aria-hidden="true"
        focusable="false"
      >
        <path d="M2.5 8h10M9 4.5 12.5 8 9 11.5" />
      </svg>
      {labelled && <span className={styles.word}>{t(`trend.${direction}`)}</span>}
    </span>
  )
}

/** The legend for small trend lines: what the little line next to a score is. */
export function TrendKey() {
  const { t } = useTranslation()
  return (
    <span className={styles.key}>
      <svg
        viewBox="0 0 20 10"
        width="20"
        height="10"
        aria-hidden="true"
        focusable="false"
      >
        <path className={styles.line} d="M1.5 7.5 5.5 4l3.5 2.5 4.5-4.5 5 2.5" />
      </svg>
      {t('trend.key')}
    </span>
  )
}

/**
 * A score over the 15 days ending today: a sparkline in the quiet ink, today's dot in its score
 * colour, and an arrow for the fitted direction (score/trend.ts). The y-range follows the data
 * (widened to a minimum span), so read the numbers, not the height.
 */
export function TrendLine({ points, today, subject, size = 'small' }: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const locale = intlLocale(language)
  const [active, setActive] = useState<number | null>(null)

  const start = trendStart(today)
  const shown = points.filter((p) => p.date >= start && p.date <= today)
  if (shown.length === 0) return null

  const direction = trendDirection(fittedChange(shown))
  const [lo, hi] = trendDomain(shown)
  const { width, height, pad } = GEOMETRY[size]
  const x = (date: IsoDate) =>
    pad + (daysBetween(start, date) / (TREND_DAYS - 1)) * (width - 2 * pad)
  const y = (score: number) => pad + (1 - (score - lo) / (hi - lo)) * (height - 2 * pad)
  const line = shown
    .map(
      (p, i) => `${i === 0 ? 'M' : 'L'}${x(p.date).toFixed(1)} ${y(p.score).toFixed(1)}`,
    )
    .join('')
  const last = shown[shown.length - 1]
  const label = t('trend.summary', {
    subject,
    direction: t(`trend.${direction}`),
    from: formatScore(shown[0].score, language),
    to: formatScore(last.score, language),
  })

  if (size === 'small') {
    return (
      <span className={styles.small} role="img" aria-label={label} title={label}>
        <svg
          className={styles.chart}
          viewBox={`0 0 ${width} ${height}`}
          aria-hidden="true"
          focusable="false"
        >
          <path className={styles.line} d={line} />
          <circle
            className={styles.dot}
            cx={x(last.date)}
            cy={y(last.score)}
            r={3}
            fill={scoreColor(last.score)}
          />
        </svg>
        <TrendArrow direction={direction} />
      </span>
    )
  }

  const focus = active === null ? last : shown[active]
  const dayName = (date: IsoDate) =>
    date === today
      ? t('trend.today')
      : `${formatDay(date, locale).weekday} ${formatDayMonth(date, locale)}`
  // The day nearest the pointer, so a finger dragged along the line reads each day in turn.
  const point = (event: PointerEvent<SVGSVGElement>) => {
    const box = event.currentTarget.getBoundingClientRect()
    const at = ((event.clientX - box.left) / box.width) * width
    let nearest = 0
    shown.forEach((p, i) => {
      if (Math.abs(x(p.date) - at) < Math.abs(x(shown[nearest].date) - at)) nearest = i
    })
    setActive(nearest)
  }

  return (
    <figure className={styles.large}>
      <div className={styles.status}>
        <TrendArrow direction={direction} labelled />
        <span className={styles.readout}>
          {dayName(focus.date)} · <strong>{formatScore(focus.score, language)}</strong>
        </span>
      </div>
      <svg
        className={styles.chart}
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={label}
        onPointerDown={point}
        onPointerMove={point}
        // A finger lifted keeps its day; a mouse leaving hands back to today.
        onPointerLeave={(event) => {
          if (event.pointerType === 'mouse') setActive(null)
        }}
      >
        {focus !== last && (
          <line
            className={styles.hairline}
            x1={x(focus.date)}
            x2={x(focus.date)}
            y1={0}
            y2={height}
          />
        )}
        <path className={styles.line} d={line} />
        <circle
          className={styles.dot}
          cx={x(last.date)}
          cy={y(last.score)}
          r={4.5}
          fill={scoreColor(last.score)}
        />
        {focus !== last && (
          <circle
            className={styles.dot}
            cx={x(focus.date)}
            cy={y(focus.score)}
            r={4}
            fill={scoreColor(focus.score)}
          />
        )}
      </svg>
      <figcaption className={styles.axis} aria-hidden="true">
        <span>{formatDayMonth(start, locale)}</span>
        <span>{t('trend.today')}</span>
      </figcaption>
      <table className="visually-hidden">
        <caption>{label}</caption>
        <thead>
          <tr>
            <th scope="col">{t('trend.dayColumn')}</th>
            <th scope="col">{t('trend.scoreColumn')}</th>
          </tr>
        </thead>
        <tbody>
          {shown.map((p) => (
            <tr key={p.date}>
              <td>{formatDayLong(p.date, locale)}</td>
              <td>{formatScore(p.score, language)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </figure>
  )
}
