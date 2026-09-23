import { useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import styles from './DisclaimerDialog.module.css'
import { DisclaimerText } from './DisclaimerText'

// Bump the version when the text gains something every visitor must read again: v2 added
// terrain, access, no-guarantee and own-judgement to the conditions-only v1.
const STORAGE_KEY = 'mushma.disclaimer.v2'

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
  const titleRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    const dialog = ref.current
    if (!dialog) return
    if (open && !dialog.open) {
      if (typeof dialog.showModal === 'function') dialog.showModal()
      else dialog.setAttribute('open', '')
      // Start reading at the top: left alone, the browser focuses the scrolling body (a ring
      // clipped to a stray line) or the button (scrolled past the whole text).
      titleRef.current?.focus()
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
      <div className={styles.body}>
        <h2 id="disclaimer-title" ref={titleRef} tabIndex={-1} className={styles.title}>
          {t('disclaimer.title')}
        </h2>
        <DisclaimerText />
      </div>
      {/* Outside the scrolling body, so it stays in view however long the text is. */}
      <div className={styles.actions}>
        <button type="button" className={styles.accept} onClick={accept}>
          {t('disclaimer.accept')}
        </button>
      </div>
    </dialog>
  )
}
