import { useTranslation } from 'react-i18next'
import { regionPath } from '../routes'
import { useAppState } from '../state/useAppState'
import styles from './NotFoundPage.module.css'

export function NotFoundPage() {
  const { t } = useTranslation()
  const { region, navigate } = useAppState()
  const backHref = regionPath(region.slug)
  return (
    <div className={styles.page}>
      <div className={styles.inner}>
        <p className={styles.eyebrow}>{t('notFound.eyebrow')}</p>
        <h1 className={styles.title}>{t('notFound.title')}</h1>
        <p className={styles.body}>{t('notFound.body')}</p>
        <a
          href={backHref}
          className={styles.back}
          onClick={(event) => {
            event.preventDefault()
            navigate(backHref)
          }}
        >
          {t('nav.backToMap')}
        </a>
      </div>
    </div>
  )
}
