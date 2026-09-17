import { useTranslation } from 'react-i18next'
import { intlLocale, type Language } from '../i18n'
import { SCORE_CLASSES } from '../score/scale'
import styles from './Legend.module.css'

interface Props {
  showSightings: boolean
}

export function Legend({ showSightings }: Props) {
  const { t, i18n } = useTranslation()
  const number = new Intl.NumberFormat(intlLocale(i18n.resolvedLanguage as Language), {
    maximumFractionDigits: 1,
  })

  return (
    <section className={styles.legend} aria-labelledby="legend-title">
      <h2 id="legend-title" className={styles.title}>
        {t('legend.title')}
      </h2>
      <div className={styles.scale}>
        {SCORE_CLASSES.map((c) => (
          <span key={c.min} className={styles.swatch} style={{ background: c.color }} />
        ))}
      </div>
      <div className={styles.ticks} aria-hidden="true">
        {[...SCORE_CLASSES.map((c) => c.min), 1].map((tick) => (
          <span key={tick}>{number.format(tick)}</span>
        ))}
      </div>
      <div className={styles.ends}>
        <span>{t('score.low')}</span>
        <span>{t('score.high')}</span>
      </div>
      <ul className={styles.keys}>
        <li>
          <span className={styles.hatch} aria-hidden="true" />
          {t('legend.forecast')}
        </li>
        {showSightings && (
          <li>
            <span className={styles.sighting} aria-hidden="true" />
            {t('legend.sightings')}
          </li>
        )}
      </ul>
    </section>
  )
}
