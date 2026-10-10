import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import type { DateWindowSize } from '../state/urlState'
import {
  addDays,
  dayKind,
  daysBetween,
  formatDayLong,
  formatMonthYear,
  type IsoDate,
  monthGrid,
  monthOf,
  shiftMonth,
  weekdayInitials,
} from '../time/days'
import { ChevronIcon } from './icons'
import styles from './DateCalendar.module.css'

interface Props {
  today: IsoDate
  value: IsoDate
  window: DateWindowSize
  /** The first day a past date can be replayed from. */
  historyStart: IsoDate
  onChange: (date: IsoDate) => void
  /** Any touch or key on the calendar (analysis mode pauses its playback on it). */
  onTouch?: () => void
}

/**
 * The date strip opened up into months: any day from the history's first day to the end of the
 * daily forecast. Later days are drawn but can't be picked — beyond ~7 days is an outlook, not a
 * forecast (PRD → Principles), and the footnote says where it lives.
 */
export function DateCalendar({
  today,
  value,
  window,
  historyStart,
  onChange,
  onTouch,
}: Props) {
  const { t, i18n } = useTranslation()
  const locale = intlLocale(i18n.resolvedLanguage as Language)
  const lastDay = addDays(today, window.forecastDays)
  const [month, setMonth] = useState(() => monthOf(value))
  const previous = shiftMonth(month, -1)
  const next = shiftMonth(month, 1)

  return (
    <div
      role="group"
      aria-label={t('date.calendar')}
      className={styles.calendar}
      onPointerDown={onTouch}
      onKeyDown={onTouch}
    >
      <div className={styles.header}>
        <button
          type="button"
          className={styles.nav}
          aria-label={t('date.previousMonth')}
          disabled={previous < monthOf(historyStart)}
          onClick={() => setMonth(previous)}
        >
          <ChevronIcon direction="left" />
        </button>
        <h2 className={styles.title} aria-live="polite">
          {formatMonthYear(month, locale)}
        </h2>
        <button
          type="button"
          className={styles.nav}
          aria-label={t('date.nextMonth')}
          disabled={next > monthOf(lastDay)}
          onClick={() => setMonth(next)}
        >
          <ChevronIcon direction="right" />
        </button>
      </div>
      <div className={styles.grid}>
        {weekdayInitials(locale).map((initial, index) => (
          <span key={index} className={styles.weekday} aria-hidden="true">
            {initial}
          </span>
        ))}
        {monthGrid(month).map((date, index) => {
          if (date === null) return <span key={`pad-${index}`} />
          const kind = dayKind(daysBetween(today, date))
          const long = formatDayLong(date, locale)
          return (
            <button
              key={date}
              type="button"
              className={styles.day}
              data-kind={kind}
              aria-pressed={date === value}
              aria-current={kind === 'today' ? 'date' : undefined}
              aria-label={
                kind === 'forecast'
                  ? t('date.forecastDay', { date: long })
                  : t('date.observedDay', { date: long })
              }
              disabled={date < historyStart || date > lastDay}
              onClick={() => onChange(date)}
            >
              {Number(date.slice(8))}
            </button>
          )
        })}
      </div>
      <p className={styles.horizon}>
        {t('date.horizon', { date: formatDayLong(lastDay, locale) })}
      </p>
    </div>
  )
}
