import { useTranslation } from 'react-i18next'
import { STALE_DATA_HOURS } from '../config'
import { intlLocale } from '../i18n'
import { formatUpdatedAt } from '../time/days'
import styles from './DataStatus.module.css'
import { OfflineIcon } from './icons'

function isStale(updatedAt: string): boolean {
  return Date.now() - new Date(updatedAt).getTime() > STALE_DATA_HOURS * 60 * 60 * 1000
}

interface Props {
  online: boolean
  /** `/status`'s `updated_at`; undefined while loading, before the first pipeline run, or on
   * a load error -- any of which just leaves this silent rather than guessing. */
  updatedAt: string | undefined
  /** `/status`'s `rules_version`: the hash the scoring pipeline stamped on the last run. */
  rulesVersion?: string | null
}

/** "Last updated" + the rules version the pipeline stamped, with a stale-data warning when the
 * pipeline hasn't run (M7). A persistent offline indicator takes over instead when there's no
 * connection at all to ask `/status`. */
export function DataStatus({ online, updatedAt, rulesVersion }: Props) {
  const { t } = useTranslation()

  if (!online) {
    return (
      <p className={styles.status} role="status">
        <OfflineIcon />
        {t('freshness.offline')}
      </p>
    )
  }

  if (!updatedAt) return null
  const date = formatUpdatedAt(updatedAt, intlLocale())
  const version = rulesVersion?.trim() || undefined

  return (
    <p
      className={styles.status}
      data-stale={isStale(updatedAt) || undefined}
      role="status"
    >
      <span>
        {t(isStale(updatedAt) ? 'freshness.stale' : 'freshness.updated', { date })}
      </span>
      {version && (
        <>
          <span className={styles.sep} aria-hidden="true">
            ·
          </span>
          <span className={styles.version} title={t('freshness.versionHint')}>
            <span className={styles.versionLabel}>{t('freshness.version')}</span>
            <span className={styles.versionHash}>{version}</span>
          </span>
        </>
      )}
    </p>
  )
}
