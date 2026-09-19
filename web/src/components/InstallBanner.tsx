import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { usePwaInstall } from '../hooks/usePwaInstall'
import { CloseIcon, DownloadIcon } from './icons'
import styles from './InstallBanner.module.css'

const STORAGE_KEY = 'mushma.installBanner.dismissed'

function dismissed(): boolean {
  try {
    return localStorage.getItem(STORAGE_KEY) === '1'
  } catch {
    return false
  }
}

export function InstallBanner() {
  const { t } = useTranslation()
  const { available, install } = usePwaInstall()
  const [hidden, setHidden] = useState(dismissed)

  if (!available || hidden) return null

  const dismiss = () => {
    setHidden(true)
    try {
      localStorage.setItem(STORAGE_KEY, '1')
    } catch {
      // Shown again next visit; nothing else depends on it.
    }
  }

  return (
    <div className={styles.banner} role="status">
      <DownloadIcon />
      <p className={styles.text}>{t('pwa.installBanner')}</p>
      <button type="button" className={styles.install} onClick={install}>
        {t('pwa.install')}
      </button>
      <button
        type="button"
        className={styles.dismiss}
        aria-label={t('pwa.dismiss')}
        onClick={dismiss}
      >
        <CloseIcon />
      </button>
    </div>
  )
}
