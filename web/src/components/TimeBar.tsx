import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import type { DateWindowSize } from '../state/urlState'
import {
  addDays,
  daysBetween,
  formatDateFull,
  type IsoDate,
  sameDayLastYear,
} from '../time/days'
import { DateStrip } from './DateStrip'
import { CalendarIcon, ChevronIcon, CloseIcon } from './icons'
import styles from './TimeBar.module.css'

interface Props {
  today: IsoDate
  date: IsoDate
  window: DateWindowSize
  /** The first day a past date can be replayed from. */
  historyStart: IsoDate
  /** A past season on the map, or null for a day. */
  season: number | null
  /** Seasons that can be put on the map, oldest first. */
  seasons: number[]
  onDate: (date: IsoDate) => void
  onSeason: (season: number | null) => void
}

/** Which day (or season) the map shows: the date strip, a replayed past day, or a season. */
export function TimeBar({
  today,
  date,
  window,
  historyStart,
  season,
  seasons,
  onDate,
  onSeason,
}: Props) {
  const { t, i18n } = useTranslation()
  const locale = intlLocale(i18n.resolvedLanguage as Language)
  const [picking, setPicking] = useState(false)
  const [draft, setDraft] = useState('')
  const yesterday = addDays(today, -1)

  const pick = (value: IsoDate) => {
    if (!value || value < historyStart || value > yesterday) return
    onDate(value)
    setPicking(false)
  }

  const openPicker = () => {
    setDraft(date < today ? date : '')
    setPicking((open) => !open)
  }

  // A typed date is only a draft: each keystroke can already make a valid date (day first, in
  // Italian), so the Replay button, or Enter, is what jumps to it.
  const picker = picking && (
    <form
      className={styles.picker}
      onSubmit={(event) => {
        event.preventDefault()
        pick(draft)
      }}
    >
      <label className={styles.pickerLabel}>
        <span>{t('replay.pickLabel')}</span>
        <input
          type="date"
          className={styles.input}
          min={historyStart}
          max={yesterday}
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
        />
      </label>
      <button type="submit" className={styles.go} disabled={!draft}>
        {t('replay.go')}
      </button>
      <button
        type="button"
        className={styles.textButton}
        onClick={() => pick(sameDayLastYear(date))}
      >
        {t('replay.lastYear')}
      </button>
      <button
        type="button"
        className={styles.iconButton}
        aria-label={t('replay.close')}
        onClick={() => setPicking(false)}
      >
        <CloseIcon />
      </button>
    </form>
  )

  if (season !== null) {
    const index = seasons.indexOf(season)
    const previous = index > 0 ? seasons[index - 1] : null
    const next = index >= 0 && index < seasons.length - 1 ? seasons[index + 1] : null
    return (
      <div className={styles.stack}>
        <div className={styles.bar} data-mode="season">
          <button
            type="button"
            className={styles.iconButton}
            aria-label={t('season.previous')}
            disabled={previous === null}
            onClick={() => previous !== null && onSeason(previous)}
          >
            <ChevronIcon direction="left" />
          </button>
          <p className={styles.label}>
            <span className={styles.eyebrow}>{t('season.eyebrow')}</span>
            <span className={styles.value}>{t('season.label', { year: season })}</span>
          </p>
          <button
            type="button"
            className={styles.iconButton}
            aria-label={t('season.next')}
            disabled={next === null}
            onClick={() => next !== null && onSeason(next)}
          >
            <ChevronIcon direction="right" />
          </button>
          <button
            type="button"
            className={styles.back}
            aria-label={t('season.close')}
            onClick={() => onSeason(null)}
          >
            <CloseIcon />
          </button>
        </div>
      </div>
    )
  }

  if (daysBetween(today, date) < -window.pastDays) {
    const previous = addDays(date, -1)
    return (
      <div className={styles.stack}>
        {picker}
        <div className={styles.bar} data-mode="replay">
          <button
            type="button"
            className={styles.iconButton}
            aria-label={t('replay.previous')}
            disabled={previous < historyStart}
            onClick={() => onDate(previous)}
          >
            <ChevronIcon direction="left" />
          </button>
          <button
            type="button"
            className={styles.label}
            aria-expanded={picking}
            aria-label={t('replay.change', { date: formatDateFull(date, locale) })}
            onClick={openPicker}
          >
            <span className={styles.eyebrow}>{t('replay.eyebrow')}</span>
            <span className={styles.value}>{formatDateFull(date, locale)}</span>
          </button>
          <button
            type="button"
            className={styles.iconButton}
            aria-label={t('replay.next')}
            onClick={() => onDate(addDays(date, 1))}
          >
            <ChevronIcon direction="right" />
          </button>
          <button type="button" className={styles.back} onClick={() => onDate(today)}>
            {t('replay.back')}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.stack}>
      {picker}
      <div className={styles.row}>
        <button
          type="button"
          className={styles.calendar}
          aria-label={t('replay.open')}
          aria-expanded={picking}
          onClick={openPicker}
        >
          <CalendarIcon />
        </button>
        <DateStrip today={today} value={date} window={window} onChange={onDate} />
      </div>
    </div>
  )
}
