import { type KeyboardEvent, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import { type View, VIEWS } from '../state/urlState'
import styles from './ViewTabs.module.css'

interface Props {
  value: View
  onChange: (view: View) => void
  /** Id of the element each tab controls (the sheet's panel). */
  panelId: string
}

const KEYS: Record<string, (index: number) => number> = {
  ArrowRight: (i) => (i + 1) % VIEWS.length,
  ArrowLeft: (i) => (i - 1 + VIEWS.length) % VIEWS.length,
  Home: () => 0,
  End: () => VIEWS.length - 1,
}

/** Now · Seasons · Outlook: what the sheet shows. A WAI-ARIA tab list: one tab stop, arrows
 * move between the tabs. */
export function ViewTabs({ value, onChange, panelId }: Props) {
  const { t } = useTranslation()
  const tabs = useRef<(HTMLButtonElement | null)[]>([])

  const onKeyDown = (event: KeyboardEvent) => {
    const move = KEYS[event.key]
    if (!move) return
    event.preventDefault()
    const next = move(VIEWS.indexOf(value))
    onChange(VIEWS[next])
    tabs.current[next]?.focus()
  }

  return (
    <div
      role="tablist"
      aria-label={t('views.label')}
      className={styles.tabs}
      onKeyDown={onKeyDown}
    >
      {VIEWS.map((view, index) => (
        <button
          key={view}
          ref={(element) => {
            tabs.current[index] = element
          }}
          id={`view-tab-${view}`}
          type="button"
          role="tab"
          aria-selected={value === view}
          aria-controls={panelId}
          tabIndex={value === view ? 0 : -1}
          data-view={view}
          className={styles.tab}
          onClick={() => onChange(view)}
        >
          {t(`views.${view}`)}
        </button>
      ))}
    </div>
  )
}
