import { useId, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { listRegions, type RegionDefinition } from '../regions'
import { currentLanguage, type Language } from '../i18n'
import { ChevronIcon } from './icons'
import styles from './RegionSwitcher.module.css'

interface Props {
  value: RegionDefinition
  onChange: (slug: string) => void
}

export function RegionSwitcher({ value, onChange }: Props) {
  const { t } = useTranslation()
  const language = currentLanguage() as Language
  const id = useId()
  const [open, setOpen] = useState(false)
  const rootRef = useRef<HTMLDivElement>(null)
  const regions = listRegions()

  return (
    <div
      ref={rootRef}
      className={styles.switcher}
      onBlur={(event) => {
        if (!rootRef.current?.contains(event.relatedTarget as Node)) setOpen(false)
      }}
    >
      <button
        type="button"
        className={styles.trigger}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={`${id}-list`}
        aria-label={t('regions.label')}
        onClick={() => setOpen((v) => !v)}
      >
        <span>{value.name[language]}</span>
        <ChevronIcon direction={open ? 'up' : 'down'} />
      </button>
      {open && (
        <ul
          id={`${id}-list`}
          role="listbox"
          aria-label={t('regions.label')}
          className={styles.list}
        >
          {regions.map((region) => (
            <li key={region.slug} role="presentation">
              <button
                type="button"
                role="option"
                aria-selected={region.slug === value.slug}
                className={styles.option}
                onClick={() => {
                  onChange(region.slug)
                  setOpen(false)
                }}
              >
                {region.name[language]}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
