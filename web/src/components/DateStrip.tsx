import { useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import type { DateWindowSize } from '../state/urlState'
import { dateWindow, formatDay, formatDayLong, type IsoDate } from '../time/days'
import styles from './DateStrip.module.css'

interface Props {
  today: IsoDate
  value: IsoDate
  window: DateWindowSize
  onChange: (date: IsoDate) => void
  /** Any touch, scroll or key on the strip (analysis mode pauses its playback on it). */
  onTouch?: () => void
}

export function DateStrip({ today, value, window, onChange, onTouch }: Props) {
  const { t, i18n } = useTranslation()
  const locale = intlLocale(i18n.resolvedLanguage as Language)
  const selectedRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    selectedRef.current?.scrollIntoView?.({ block: 'nearest', inline: 'center' })
  }, [value])

  return (
    <div
      role="radiogroup"
      aria-label={t('date.label')}
      className={styles.strip}
      onPointerDown={onTouch}
      onWheel={onTouch}
      onKeyDown={onTouch}
    >
      {dateWindow(today, window).map(({ date, kind }) => {
        const { weekday, day } = formatDay(date, locale)
        const long = formatDayLong(date, locale)
        const selected = date === value
        return (
          <button
            key={date}
            ref={selected ? selectedRef : undefined}
            type="button"
            role="radio"
            aria-checked={selected}
            aria-label={
              kind === 'forecast'
                ? t('date.forecastDay', { date: long })
                : t('date.observedDay', { date: long })
            }
            data-kind={kind}
            className={styles.day}
            onClick={() => onChange(date)}
          >
            <span className={styles.weekday}>
              {kind === 'today' ? t('date.today') : weekday}
            </span>
            <span className={styles.number}>{day}</span>
          </button>
        )
      })}
    </div>
  )
}
