import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import { GOOD_DAYS_CLASSES, SCORE_CLASSES } from '../score/scale'
import { ChevronIcon } from './icons'
import styles from './Legend.module.css'

interface Props {
  showSightings: boolean
  /** A season on the map: the cells show its good days instead of a day's score. */
  season?: number | null
  /** A phone: one chip with the scale, that opens to the whole key. */
  collapsible?: boolean
}

export function Legend({ showSightings, season = null, collapsible = false }: Props) {
  const { t, i18n } = useTranslation()
  const [open, setOpen] = useState(false)
  const number = new Intl.NumberFormat(intlLocale(i18n.resolvedLanguage as Language), {
    maximumFractionDigits: 1,
  })
  const seasonMode = season !== null
  const classes = seasonMode ? GOOD_DAYS_CLASSES : SCORE_CLASSES
  const ticks = seasonMode
    ? classes.map((c, i) => (i === classes.length - 1 ? `${c.min}+` : String(c.min)))
    : [...classes.map((c) => c.min), 1].map((tick) => number.format(tick))

  return (
    <section
      className={styles.legend}
      data-collapsible={collapsible || undefined}
      aria-labelledby="legend-title"
    >
      <div id="legend-key" className={styles.key} hidden={collapsible && !open}>
        <h2 id="legend-title" className={styles.title}>
          {seasonMode ? t('season.legendTitle', { year: season }) : t('legend.title')}
        </h2>
        <div className={styles.scale}>
          {classes.map((c) => (
            <span key={c.min} className={styles.swatch} style={{ background: c.color }} />
          ))}
        </div>
        <div
          className={styles.ticks}
          data-mode={seasonMode ? 'season' : 'score'}
          aria-hidden="true"
        >
          {ticks.map((tick) => (
            <span key={tick}>{tick}</span>
          ))}
        </div>
        <div className={styles.ends}>
          <span>{seasonMode ? t('season.few') : t('score.low')}</span>
          <span>{seasonMode ? t('season.many') : t('score.high')}</span>
        </div>
        {(!seasonMode || showSightings) && (
          <ul className={styles.keys}>
            {!seasonMode && (
              <li>
                <span className={styles.hatch} aria-hidden="true" />
                {t('legend.forecast')}
              </li>
            )}
            {showSightings && (
              <li>
                <span className={styles.sighting} aria-hidden="true" />
                {t('legend.sightings')}
              </li>
            )}
          </ul>
        )}
      </div>
      {collapsible && (
        <button
          type="button"
          className={styles.chip}
          aria-expanded={open}
          aria-controls="legend-key"
          onClick={() => setOpen((value) => !value)}
        >
          <span className={styles.chipScale} aria-hidden="true">
            {classes.map((c) => (
              <span key={c.min} style={{ background: c.color }} />
            ))}
          </span>
          {t('legend.toggle')}
          <ChevronIcon direction={open ? 'down' : 'up'} />
        </button>
      )}
    </section>
  )
}
