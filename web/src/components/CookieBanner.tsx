import { useTranslation } from 'react-i18next'
import { setConsent } from '../consent'
import styles from './CookieBanner.module.css'

interface Props {
  open: boolean
  onClose: () => void
  onPrivacyClick: () => void
}

/** Real Accept/Decline for the self-hosted analytics `feat-umami-integration.md` gates on this. */
export function CookieBanner({ open, onClose, onPrivacyClick }: Props) {
  const { t } = useTranslation()
  if (!open) return null

  const choose = (accepted: boolean) => {
    setConsent(accepted ? 'accepted' : 'declined')
    onClose()
  }

  return (
    <div className={styles.banner} role="dialog" aria-label={t('cookies.title')}>
      <p className={styles.intro}>{t('cookies.intro')}</p>
      <a
        href="/privacy"
        className={styles.privacyLink}
        onClick={(event) => {
          event.preventDefault()
          onPrivacyClick()
        }}
      >
        {t('cookies.privacyLink')}
      </a>
      <div className={styles.actions}>
        <button type="button" className={styles.decline} onClick={() => choose(false)}>
          {t('cookies.decline')}
        </button>
        <button type="button" className={styles.accept} onClick={() => choose(true)}>
          {t('cookies.accept')}
        </button>
      </div>
    </div>
  )
}
