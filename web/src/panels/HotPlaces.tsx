import { useTranslation } from 'react-i18next'
import type { Hotspot } from '../api/queries'
import { ScoreChip } from '../components/ScoreChip'
import { SIGHTINGS_WINDOW_DAYS } from '../config'
import { intlLocale, type Language } from '../i18n'
import type { SpeciesOrCombined } from '../state/urlState'
import { formatDayLong, type IsoDate } from '../time/days'
import styles from './HotPlaces.module.css'
import panel from './panel.module.css'

interface Props {
  species: SpeciesOrCombined
  date: IsoDate
  hotspots: Hotspot[] | undefined
  isLoading: boolean
  isError: boolean
  onRetry: () => void
  onSelect: (hotspot: Hotspot) => void
  sightingsVisible: boolean
  onSightingsVisibleChange: (visible: boolean) => void
  sightingsError: boolean
}

export function HotPlaces({
  species,
  date,
  hotspots,
  isLoading,
  isError,
  onRetry,
  onSelect,
  sightingsVisible,
  onSightingsVisibleChange,
  sightingsError,
}: Props) {
  const { t, i18n } = useTranslation()
  const locale = intlLocale(i18n.resolvedLanguage as Language)

  return (
    <section className={panel.section} aria-labelledby="hot-places-title">
      <header className={panel.header}>
        <h2 id="hot-places-title" className={panel.title}>
          {t('hotspots.title')}
        </h2>
        <p className={panel.subtitle}>
          {t('hotspots.subtitle', {
            species: t(`species.${species}.name`),
            date: formatDayLong(date, locale),
          })}
        </p>
      </header>

      {isLoading && <p className={panel.status}>{t('hotspots.loading')}</p>}
      {isError && (
        <p className={panel.status} role="alert">
          {t('hotspots.loadError')}{' '}
          <button type="button" className={panel.linkButton} onClick={onRetry}>
            {t('map.retry')}
          </button>
        </p>
      )}
      {hotspots?.length === 0 && <p className={panel.status}>{t('hotspots.empty')}</p>}

      {hotspots && hotspots.length > 0 && (
        <ol className={styles.list}>
          {hotspots.map((hotspot, index) => (
            <li key={hotspot.id}>
              <button
                type="button"
                className={styles.item}
                onClick={() => onSelect(hotspot)}
              >
                <span className={styles.rank} aria-hidden="true">
                  {index + 1}
                </span>
                <span className={styles.place}>
                  <span className={styles.name}>{hotspot.place.nearest_place}</span>
                  <span className={styles.meta}>
                    {t('spot.comune', { comune: hotspot.place.comune })} ·{' '}
                    {t('hotspots.cells', { count: hotspot.cell_ids.length })}
                    {hotspot.recent_sightings > 0 && (
                      <>
                        {' · '}
                        {t('hotspots.sightings', { count: hotspot.recent_sightings })}
                      </>
                    )}
                  </span>
                </span>
                <ScoreChip score={hotspot.score} />
              </button>
            </li>
          ))}
        </ol>
      )}

      <div className={styles.sightings}>
        <label className={styles.toggle}>
          <input
            type="checkbox"
            role="switch"
            checked={sightingsVisible}
            onChange={(event) => onSightingsVisibleChange(event.target.checked)}
          />
          <span className={styles.toggleText}>
            <span className={styles.toggleLabel}>{t('sightings.toggle')}</span>
            <span className={styles.meta}>
              {t('sightings.window', { days: SIGHTINGS_WINDOW_DAYS })}
            </span>
          </span>
        </label>
        <p className={styles.note}>{t('sightings.note')}</p>
        {sightingsError && (
          <p className={panel.status} role="alert">
            {t('sightings.loadError')}
          </p>
        )}
      </div>
    </section>
  )
}
