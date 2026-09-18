import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import { GOOD_DAYS_CLASSES, SCORE_CLASSES } from '../score/scale'
import styles from './Legend.module.css'

interface Props {
  showSightings: boolean
  /** A season on the map: the cells show its good days instead of a day's score. */
  season?: number | null
}

export function Legend({ showSightings, season = null }: Props) {
  const { t, i18n } = useTranslation()
  const number = new Intl.NumberFormat(intlLocale(i18n.resolvedLanguage as Language), {
    maximumFractionDigits: 1,
  })
  const seasonMode = season !== null
  const classes = seasonMode ? GOOD_DAYS_CLASSES : SCORE_CLASSES
  const ticks = seasonMode
    ? classes.map((c, i) => (i === classes.length - 1 ? `${c.min}+` : String(c.min)))
    : [...classes.map((c) => c.min), 1].map((tick) => number.format(tick))

  return (
    <section className={styles.legend} aria-labelledby="legend-title">
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
    </section>
  )
}
