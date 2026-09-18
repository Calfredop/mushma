import { useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import styles from './DisclaimerDialog.module.css'

const STORAGE_KEY = 'mushma.disclaimer.v1'

// eslint-disable-next-line react-refresh/only-export-components
export function disclaimerAccepted(): boolean {
  try {
    return localStorage.getItem(STORAGE_KEY) === 'accepted'
  } catch {
    return false
  }
}

interface Props {
  open: boolean
  onClose: () => void
}

/** Conditions only, never edibility or identification (PRD → Principles). */
export function DisclaimerDialog({ open, onClose }: Props) {
  const { t } = useTranslation()
  const ref = useRef<HTMLDialogElement>(null)

  useEffect(() => {
    const dialog = ref.current
    if (!dialog) return
    if (open && !dialog.open) {
      if (typeof dialog.showModal === 'function') dialog.showModal()
      else dialog.setAttribute('open', '')
    }
    if (!open && dialog.open) {
      if (typeof dialog.close === 'function') dialog.close()
      else dialog.removeAttribute('open')
    }
  }, [open])

  const accept = () => {
    try {
      localStorage.setItem(STORAGE_KEY, 'accepted')
    } catch {
      // Shown again next visit; nothing else depends on it.
    }
    onClose()
  }

  return (
    <dialog
      ref={ref}
      className={styles.dialog}
      aria-labelledby="disclaimer-title"
      onCancel={(event) => {
        event.preventDefault()
        accept()
      }}
    >
      <h2 id="disclaimer-title" className={styles.title}>
        {t('disclaimer.title')}
      </h2>
      <p>{t('disclaimer.body1')}</p>
      <p>{t('disclaimer.body2')}</p>
      <p className={styles.strong}>{t('disclaimer.body3')}</p>
      <button type="button" className={styles.accept} onClick={accept}>
        {t('disclaimer.accept')}
      </button>
    </dialog>
  )
}
