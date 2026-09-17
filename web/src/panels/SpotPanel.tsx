import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import type { CellDetailResponse } from '../api/queries'
import { CloseIcon } from '../components/icons'
import { ScoreChip } from '../components/ScoreChip'
import { distanceKm, OUTSIDE_CELL_KM } from '../geo/distance'
import { intlLocale, type Language } from '../i18n'
import { formatScore } from '../score/format'
import { scoreColor } from '../score/scale'
import type { Species, SpeciesOrCombined, Spot } from '../state/urlState'
import { formatDay, formatDayLong, type IsoDate } from '../time/days'
import panel from './panel.module.css'
import styles from './SpotPanel.module.css'
import { WhyBreakdown } from './WhyBreakdown'

interface Props {
  spot: Spot
  detail: CellDetailResponse | undefined
  isLoading: boolean
  isError: boolean
  /** The API can't serve this spot (4xx), so retrying won't help. */
  notFound?: boolean
  onRetry: () => void
  onClose: () => void
  species: SpeciesOrCombined
  date: IsoDate
  today: IsoDate
}

interface Selection {
  species: Species
  date: IsoDate
}

function defaultSelection(
  detail: CellDetailResponse,
  species: SpeciesOrCombined,
  date: IsoDate,
): Selection {
  const firstDay = detail.species[0]?.days[0]?.date ?? date
  const inOutlook = detail.species.some((s) => s.days.some((d) => d.date === date))
  const selectedDate = inOutlook ? date : firstDay
  if (species !== 'combined') return { species, date: selectedDate }

  // "All": explain the species doing best on that day.
  const scoreOn = (s: CellDetailResponse['species'][number]) =>
    s.days.find((d) => d.date === selectedDate)?.score ?? 0
  const best = [...detail.species].sort((a, b) => scoreOn(b) - scoreOn(a))[0]
  return { species: best?.species ?? 'porcini', date: selectedDate }
}

export function SpotPanel({
  spot,
  detail,
  isLoading,
  isError,
  notFound = false,
  onRetry,
  onClose,
  species,
  date,
  today,
}: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const locale = intlLocale(language)
  const [picked, setPicked] = useState<Selection | null>(null)

  const closeButton = (
    <button
      type="button"
      className={styles.close}
      aria-label={t('spot.close')}
      onClick={onClose}
    >
      <CloseIcon />
    </button>
  )

  if (!detail) {
    return (
      <section className={panel.section} aria-labelledby="spot-title">
        <header className={styles.header}>
          <h2 id="spot-title" className={panel.title}>
            {t('spot.title')}
          </h2>
          {closeButton}
        </header>
        {isLoading && !isError && <p className={panel.status}>{t('spot.loading')}</p>}
        {isError && notFound && (
          <p className={panel.status} role="alert">
            {t('spot.notFound')}
          </p>
        )}
        {isError && !notFound && (
          <p className={panel.status} role="alert">
            {t('spot.loadError')}{' '}
            <button type="button" className={panel.linkButton} onClick={onRetry}>
              {t('map.retry')}
            </button>
          </p>
        )}
      </section>
    )
  }

  const selection = picked ?? defaultSelection(detail, species, date)
  const selectedForecast = detail.species.find((s) => s.species === selection.species)
  const selectedDay = selectedForecast?.days.find((d) => d.date === selection.date)
  const distance =
    spot.kind === 'point' ? distanceKm(spot.lat, spot.lon, detail.lat, detail.lon) : 0
  const distanceText = new Intl.NumberFormat(locale, { maximumFractionDigits: 1 }).format(
    distance,
  )

  return (
    <section className={panel.section} aria-labelledby="spot-title">
      <header className={styles.header}>
        <div>
          <p className={styles.eyebrow}>{t('spot.title')}</p>
          <h2 id="spot-title" className={panel.title}>
            {detail.place.nearest_place}
          </h2>
          <p className={panel.subtitle}>
            {t('spot.comune', { comune: detail.place.comune })}
            {distance > OUTSIDE_CELL_KM && (
              <>
                {' · '}
                {t('spot.nearestCell', { distance: distanceText })}
              </>
            )}
          </p>
        </div>
        {closeButton}
      </header>

      {date < today && <p className={panel.note}>{t('spot.pastDateNote')}</p>}

      <div className={styles.outlook}>
        <h3 className={styles.outlookTitle}>{t('spot.outlook')}</h3>
        {detail.species.map((forecast) => {
          const todayScore = forecast.days[0]?.score ?? 0
          return (
            <div
              key={forecast.species}
              className={styles.species}
              data-selected={forecast.species === selection.species}
            >
              <div className={styles.speciesName}>
                <span className={styles.common}>
                  {t(`species.${forecast.species}.name`)}
                </span>
                <span className={styles.latin}>
                  {t(`species.${forecast.species}.latin`)}
                </span>
              </div>
              <ScoreChip score={todayScore} />
              <div className={styles.bars}>
                {forecast.days.map((day) => {
                  const isForecast = day.date > today
                  const selected =
                    forecast.species === selection.species && day.date === selection.date
                  const { weekday } = formatDay(day.date, locale)
                  return (
                    <button
                      key={day.date}
                      type="button"
                      className={styles.bar}
                      data-forecast={isForecast}
                      aria-pressed={selected}
                      aria-label={t('spot.selectDay', {
                        species: t(`species.${forecast.species}.name`),
                        date: formatDayLong(day.date, locale),
                        value: formatScore(day.score, language),
                      })}
                      onClick={() =>
                        setPicked({ species: forecast.species, date: day.date })
                      }
                    >
                      <span className={styles.barTrack}>
                        <span
                          className={styles.barFill}
                          style={{
                            height: `${Math.max(day.score, 0.04) * 100}%`,
                            background: scoreColor(day.score),
                          }}
                        />
                      </span>
                      <span className={styles.barDay} aria-hidden="true">
                        {day.date === today
                          ? t('date.today').slice(0, 1)
                          : weekday.slice(0, 1)}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>

      {selectedDay && (
        <WhyBreakdown
          species={selection.species}
          day={selectedDay}
          isForecast={selectedDay.date > today}
        />
      )}
    </section>
  )
}
