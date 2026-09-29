import { useId } from 'react'
import { useTranslation } from 'react-i18next'
import type { TrendResponse } from '../api/queries'
import { TrendLine } from '../components/TrendLine'
import type { SpeciesOrCombined } from '../state/urlState'
import type { IsoDate } from '../time/days'
import styles from './AreaTrend.module.css'
import panel from './panel.module.css'

export interface TrendState {
  data: TrendResponse | undefined
  isLoading: boolean
  isError: boolean
  onRetry: () => void
  /** The window's last day. */
  today: IsoDate
}

interface Props {
  trend: TrendState
  species: SpeciesOrCombined
  /** The zone picked (null: the whole region). A trend for another zone is not this one's. */
  comune: string | null
  /** The region's name in the UI language, for the whole-region line's accessible name. */
  regionName: string
}

/** How the chosen zone's (or the whole region's) mean score moved over the last 15 days. */
export function AreaTrend({ trend, species, comune, regionName }: Props) {
  const { t } = useTranslation()
  const titleId = useId()
  const { isLoading, isError, onRetry, today } = trend
  const data =
    trend.data?.species === species && trend.data.area.code === comune
      ? trend.data
      : undefined

  return (
    <section className={styles.block} aria-labelledby={titleId}>
      <h3 id={titleId} className={styles.title}>
        {t('trend.title')}
      </h3>
      {isLoading && !data && <p className={panel.status}>{t('trend.loading')}</p>}
      {isError && !data && (
        <p className={panel.status} role="alert">
          {t('trend.loadError')}{' '}
          <button type="button" className={panel.linkButton} onClick={onRetry}>
            {t('map.retry')}
          </button>
        </p>
      )}
      {data && data.days.length === 0 && (
        <p className={panel.status}>{t('trend.empty')}</p>
      )}
      {data && data.days.length > 0 && (
        <>
          <TrendLine
            size="large"
            points={data.days}
            today={today}
            subject={data.area.kind === 'comune' ? data.area.name : regionName}
          />
          <p className={panel.note}>{t('trend.note')}</p>
        </>
      )}
    </section>
  )
}
