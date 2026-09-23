import { useQuery } from '@tanstack/react-query'
import { useId, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { REGION } from '../config'
import { type Place, searchPlaces } from '../geo/photon'
import { useDebouncedValue } from '../hooks/useDebouncedValue'
import type { Language } from '../i18n'
import { CloseIcon, LocateIcon, SearchIcon } from './icons'
import styles from './PlaceSearch.module.css'

const MIN_QUERY = 3

interface Props {
  onSelect: (place: Place) => void
  autoFocus?: boolean
  onDismiss?: () => void
  /** Defaults to the default region's bounds. */
  bounds?: [[number, number], [number, number]]
  /** "La mia posizione": first in the list whenever the field has focus. */
  onLocate?: () => void
  /** A GPS fix is on its way. */
  locating?: boolean
  onFocus?: () => void
}

type Option = { kind: 'locate' } | { kind: 'place'; place: Place }

export function PlaceSearch({
  onSelect,
  autoFocus,
  onDismiss,
  bounds = REGION.bounds,
  onLocate,
  locating = false,
  onFocus,
}: Props) {
  const { t, i18n } = useTranslation()
  const language = i18n.resolvedLanguage as Language
  const id = useId()
  const inputRef = useRef<HTMLInputElement>(null)
  const [text, setText] = useState('')
  const [focused, setFocused] = useState(false)
  const [activeIndex, setActive] = useState(0)
  const query = useDebouncedValue(text.trim(), 350)
  const enabled = query.length >= MIN_QUERY

  const results = useQuery({
    queryKey: ['places', language, query],
    queryFn: ({ signal }) => searchPlaces(query, language, bounds, signal),
    enabled,
    staleTime: Infinity,
    retry: 1,
  })

  const places = enabled ? (results.data ?? []) : []
  const options: Option[] = [
    ...(onLocate ? [{ kind: 'locate' as const }] : []),
    ...places.map((place) => ({ kind: 'place' as const, place })),
  ]
  const open =
    focused &&
    (onLocate !== undefined ||
      (enabled && (places.length > 0 || results.isSuccess || results.isError)))
  // Clamped on read: results can arrive, shrink or change after an arrow key.
  const active = Math.max(0, Math.min(activeIndex, options.length - 1))

  // Chosen: the field lets go, so the list and a phone's keyboard close.
  const choose = (option: Option) => {
    setText('')
    inputRef.current?.blur()
    if (option.kind === 'locate') onLocate?.()
    else onSelect(option.place)
  }

  return (
    <div className={styles.search}>
      <div className={styles.field}>
        <SearchIcon />
        <label htmlFor={`${id}-input`} className="visually-hidden">
          {t('search.label')}
        </label>
        <input
          ref={inputRef}
          id={`${id}-input`}
          type="search"
          role="combobox"
          aria-expanded={open}
          aria-controls={`${id}-results`}
          aria-autocomplete="list"
          aria-activedescendant={open && options[active] ? `${id}-${active}` : undefined}
          autoComplete="off"
          enterKeyHint="search"
          placeholder={t('search.placeholder')}
          value={text}
          autoFocus={autoFocus}
          onFocus={() => {
            setFocused(true)
            setActive(0)
            onFocus?.()
          }}
          onBlur={() => setFocused(false)}
          onChange={(event) => {
            setText(event.target.value)
            setActive(0)
          }}
          onKeyDown={(event) => {
            if (event.key === 'ArrowDown') {
              event.preventDefault()
              setActive(Math.min(active + 1, options.length - 1))
            } else if (event.key === 'ArrowUp') {
              event.preventDefault()
              setActive(Math.max(active - 1, 0))
            } else if (event.key === 'Enter' && open && options[active]) {
              event.preventDefault()
              choose(options[active])
            } else if (event.key === 'Escape') {
              if (text) setText('')
              else {
                event.currentTarget.blur()
                onDismiss?.()
              }
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
            {options.map((option, index) => (
              <li
                key={option.kind === 'locate' ? 'locate' : option.place.id}
                id={`${id}-${index}`}
                role="option"
                aria-selected={index === active}
                aria-busy={option.kind === 'locate' ? locating : undefined}
                className={styles.result}
                data-kind={option.kind}
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => choose(option)}
              >
                {option.kind === 'locate' ? (
                  <>
                    <LocateIcon />
                    <span className={styles.name}>{t('search.myLocation')}</span>
                    <span className={styles.detail}>
                      {t(locating ? 'locate.locating' : 'search.myLocationHint')}
                    </span>
                  </>
                ) : (
                  <>
                    <span className={styles.name}>{option.place.name}</span>
                    {option.place.detail && (
                      <span className={styles.detail}>{option.place.detail}</span>
                    )}
                  </>
                )}
              </li>
            ))}
          </ul>
          {enabled && results.isSuccess && places.length === 0 && (
            <p className={styles.message}>{t('search.noResults')}</p>
          )}
          {enabled && results.isError && (
            <p className={styles.message} role="alert">
              {t('search.error')}
            </p>
          )}
          {enabled && <p className={styles.attribution}>{t('search.attribution')}</p>}
        </div>
      )}
    </div>
  )
}
