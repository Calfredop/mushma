import { useQuery } from '@tanstack/react-query'
import { useId, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { REGION } from '../config'
import { type Place, searchPlaces } from '../geo/photon'
import { useDebouncedValue } from '../hooks/useDebouncedValue'
import type { Language } from '../i18n'
import { CloseIcon, SearchIcon } from './icons'
import styles from './PlaceSearch.module.css'

const MIN_QUERY = 3

interface Props {
  onSelect: (place: Place) => void
  autoFocus?: boolean
  onDismiss?: () => void
}

export function PlaceSearch({ onSelect, autoFocus, onDismiss }: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const id = useId()
  const [text, setText] = useState('')
  const [activeIndex, setActive] = useState(0)
  const query = useDebouncedValue(text.trim(), 350)
  const enabled = query.length >= MIN_QUERY

  const results = useQuery({
    queryKey: ['places', language, query],
    queryFn: ({ signal }) => searchPlaces(query, language, REGION.bounds, signal),
    enabled,
    staleTime: Infinity,
    retry: 1,
  })

  const places = enabled ? (results.data ?? []) : []
  const open = enabled && (places.length > 0 || results.isSuccess || results.isError)
  // Clamped on read: results can arrive, shrink or change after an arrow key.
  const active = Math.max(0, Math.min(activeIndex, places.length - 1))

  const choose = (place: Place) => {
    setText('')
    onSelect(place)
  }

  return (
    <div className={styles.search}>
      <div className={styles.field}>
        <SearchIcon />
        <label htmlFor={`${id}-input`} className="visually-hidden">
          {t('search.label')}
        </label>
        <input
          id={`${id}-input`}
          type="search"
          role="combobox"
          aria-expanded={open}
          aria-controls={`${id}-results`}
          aria-autocomplete="list"
          aria-activedescendant={open && places[active] ? `${id}-${active}` : undefined}
          autoComplete="off"
          enterKeyHint="search"
          placeholder={t('search.placeholder')}
          value={text}
          autoFocus={autoFocus}
          onChange={(event) => {
            setText(event.target.value)
            setActive(0)
          }}
          onKeyDown={(event) => {
            if (event.key === 'ArrowDown') {
              event.preventDefault()
              setActive(Math.min(active + 1, places.length - 1))
            } else if (event.key === 'ArrowUp') {
              event.preventDefault()
              setActive(Math.max(active - 1, 0))
            } else if (event.key === 'Enter' && places[active]) {
              event.preventDefault()
              choose(places[active])
            } else if (event.key === 'Escape') {
              if (text) setText('')
              else onDismiss?.()
            }
          }}
        />
        {(text || onDismiss) && (
          <button
            type="button"
            className={styles.clear}
            aria-label={t('search.clear')}
            onClick={() => (text ? setText('') : onDismiss?.())}
          >
            <CloseIcon />
          </button>
        )}
      </div>

      {open && (
        <div className={styles.popover}>
          <ul
            id={`${id}-results`}
            role="listbox"
            aria-label={t('search.label')}
            className={styles.results}
          >
            {places.map((place, index) => (
              <li
                key={place.id}
                id={`${id}-${index}`}
                role="option"
                aria-selected={index === active}
                className={styles.result}
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => choose(place)}
              >
                <span className={styles.name}>{place.name}</span>
                {place.detail && <span className={styles.detail}>{place.detail}</span>}
              </li>
            ))}
          </ul>
          {results.isSuccess && places.length === 0 && (
            <p className={styles.message}>{t('search.noResults')}</p>
          )}
          {results.isError && (
            <p className={styles.message} role="alert">
              {t('search.error')}
            </p>
          )}
          <p className={styles.attribution}>{t('search.attribution')}</p>
        </div>
      )}
    </div>
  )
}
