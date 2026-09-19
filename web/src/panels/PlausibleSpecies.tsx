import { useTranslation } from 'react-i18next'
import type { PlausibleSpeciesResponse } from '../api/queries'
import { SpeciesBreakdown } from '../components/SpeciesBreakdown'
import { formatPercent } from '../history/present'
import type { Language } from '../i18n'
import panel from './panel.module.css'
import styles from './PlausibleSpecies.module.css'

export interface PlausibleState {
  data: PlausibleSpeciesResponse | undefined
  isLoading: boolean
  isError: boolean
  onRetry: () => void
}

/**
 * Which species the chosen zone's woodland can plausibly hold: the share of it whose forest type
 * and altitude suit each species and taxon, weather aside. Figures come from the API.
 */
export function PlausibleSpecies({ plausible }: { plausible: PlausibleState }) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const { data, isLoading, isError, onRetry } = plausible
  const none = data?.species.every((s) => s.fit_share === 0)

  return (
    <section className={styles.block} aria-labelledby="plausible-title">
      <h3 id="plausible-title" className={styles.title}>
        {t('plausible.title')}
      </h3>
      {isLoading && !data && <p className={panel.status}>{t('plausible.loading')}</p>}
      {isError && !data && (
        <p className={panel.status} role="alert">
          {t('plausible.loadError')}{' '}
          <button type="button" className={panel.linkButton} onClick={onRetry}>
            {t('map.retry')}
          </button>
        </p>
      )}
      {data && (
        <>
          <p className={panel.note}>{t('plausible.note')}</p>
          {none ? (
            <p className={panel.status}>{t('plausible.none')}</p>
          ) : (
            <SpeciesBreakdown
              label={t('plausible.title')}
              profiles={data.species}
              value={(entry) => entry.fit_share}
              scale={1}
              format={(share) => formatPercent(share * 100, language)}
              tone="habitat"
            />
          )}
        </>
      )}
    </section>
  )
}
