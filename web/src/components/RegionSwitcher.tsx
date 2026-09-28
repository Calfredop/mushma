import { useId, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { listRegions, type RegionDefinition } from '../regions'
import { currentLanguage, type Language } from '../i18n'
import { ChevronIcon } from './icons'
import styles from './RegionSwitcher.module.css'

interface Props {
  value: RegionDefinition
  onChange: (slug: string) => void
  /** Leave the region map for the national hub. */
  onShowAll: () => void
}

function matches(name: string, query: string): boolean {
  const norm = (s: string) => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase()
  return norm(name).includes(norm(query.trim()))
}

export function RegionSwitcher({ value, onChange, onShowAll }: Props) {
  const { t } = useTranslation()
  const language = currentLanguage() as Language
  const id = useId()
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('')
  const rootRef = useRef<HTMLDivElement>(null)
  const searchRef = useRef<HTMLInputElement>(null)
  const regions = listRegions()
  const filtered = regions.filter((region) => matches(region.name[language], query))

  const close = () => {
    setOpen(false)
    setQuery('')
  }

  return (
    <div
      ref={rootRef}
      className={styles.switcher}
      onBlur={(event) => {
        if (!rootRef.current?.contains(event.relatedTarget as Node)) close()
      }}
    >
      <button
        type="button"
        className={styles.trigger}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={`${id}-list`}
        aria-label={t('regions.label')}
        onClick={() => {
          if (open) {
            close()
            return
          }
          setOpen(true)
          // Focus the search once the menu is in the DOM.
          queueMicrotask(() => searchRef.current?.focus())
        }}
      >
        <span>{value.name[language]}</span>
        <ChevronIcon direction={open ? 'up' : 'down'} />
      </button>
      {open && (
        <div className={styles.menu}>
          <div className={styles.header}>
            <button
              type="button"
              className={styles.showAll}
              onClick={() => {
                onShowAll()
                close()
              }}
            >
              {t('regions.showAll')}
            </button>
            <input
              ref={searchRef}
              type="search"
              className={styles.search}
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder={t('regions.searchPlaceholder')}
              aria-label={t('regions.search')}
              autoComplete="off"
              enterKeyHint="search"
            />
          </div>
          <ul
            id={`${id}-list`}
            role="listbox"
            aria-label={t('regions.label')}
            className={styles.list}
          >
            {filtered.length === 0 ? (
              <li className={styles.empty} role="presentation">
                {t('regions.noResults')}
              </li>
            ) : (
              filtered.map((region) => (
                <li key={region.slug} role="presentation">
                  <button
                    type="button"
                    role="option"
                    aria-selected={region.slug === value.slug}
                    className={styles.option}
                    onClick={() => {
                      onChange(region.slug)
                      close()
                    }}
                  >
                    {region.name[language]}
                  </button>
                </li>
              ))
            )}
          </ul>
        </div>
      )}
    </div>
  )
}
