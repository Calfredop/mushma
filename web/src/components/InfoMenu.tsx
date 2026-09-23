import {
  type CSSProperties,
  type KeyboardEvent,
  type MouseEvent,
  useEffect,
  useId,
  useRef,
  useState,
} from 'react'
import { createPortal } from 'react-dom'
import { useTranslation } from 'react-i18next'
import { track } from '../analytics'
import { REPO_URL } from '../config'
import { changeLanguage, LANGUAGES } from '../i18n'
import { GitHubIcon, InfoIcon } from './icons'
import styles from './InfoMenu.module.css'

const PAGES = [
  { path: '/credits', label: 'nav.credits' },
  { path: '/terms', label: 'nav.terms' },
  { path: '/privacy', label: 'nav.privacy' },
] as const

export type InfoPath = (typeof PAGES)[number]['path']

interface Props {
  /** Beside a button on the map (it opens to the button's left), or below one in a header. */
  placement: 'left' | 'below'
  onDisclaimer: () => void
  onCookies: () => void
  onNavigate: (path: InfoPath) => void
  /** The button's look where it sits. */
  className?: string
}

const GAP = 8

/** Where the menu goes, from its button's box: fixed, since it is portalled to the body. */
function position(button: HTMLElement, placement: Props['placement']): CSSProperties {
  const box = button.getBoundingClientRect()
  const right = window.innerWidth - (placement === 'left' ? box.left - GAP : box.right)
  const top = placement === 'left' ? box.top : box.bottom + GAP
  return { top, right, maxHeight: `calc(100dvh - ${top}px - ${GAP}px)` }
}

const plainClick = (event: MouseEvent) =>
  event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey

/**
 * The ⓘ menu: the disclaimer, the pages, the code and the language, behind one menu button
 * (WAI-ARIA APG menu button). It is portalled to the body so its glass blurs the map, not the
 * glass capsule its button sits in.
 */
export function InfoMenu({
  placement,
  onDisclaimer,
  onCookies,
  onNavigate,
  className,
}: Props) {
  const { t, i18n } = useTranslation()
  const id = useId()
  const buttonRef = useRef<HTMLButtonElement>(null)
  const menuRef = useRef<HTMLDivElement>(null)
  // Which item takes focus as it opens.
  const [open, setOpen] = useState<false | 'first' | 'last'>(false)
  const [style, setStyle] = useState<CSSProperties>({})

  const items = () =>
    Array.from(menuRef.current?.querySelectorAll<HTMLElement>('[role^="menuitem"]') ?? [])

  const show = (focus: 'first' | 'last') => {
    if (buttonRef.current) setStyle(position(buttonRef.current, placement))
    setOpen(focus)
  }

  const close = (refocus: boolean) => {
    setOpen(false)
    if (refocus) buttonRef.current?.focus()
  }

  // Focus goes into the menu as it opens.
  useEffect(() => {
    if (!open) return
    const all = items()
    all[open === 'first' ? 0 : all.length - 1]?.focus()
  }, [open])

  // A press anywhere else, or a new window size, closes it where it is.
  useEffect(() => {
    if (!open) return
    const onPointer = (event: PointerEvent) => {
      const target = event.target as Node
      if (menuRef.current?.contains(target) || buttonRef.current?.contains(target)) return
      setOpen(false)
    }
    const onResize = () => setOpen(false)
    document.addEventListener('pointerdown', onPointer)
    window.addEventListener('resize', onResize)
    return () => {
      document.removeEventListener('pointerdown', onPointer)
      window.removeEventListener('resize', onResize)
    }
  }, [open])

  /** Close, give focus back, then act: a dialog it opens returns focus to the button. */
  const run = (action: () => void) => {
    close(true)
    action()
  }

  const onMenuKey = (event: KeyboardEvent<HTMLDivElement>) => {
    const all = items()
    const index = all.indexOf(document.activeElement as HTMLElement)
    const focus = (next: number) => {
      event.preventDefault()
      all[(next + all.length) % all.length]?.focus()
    }
    switch (event.key) {
      case 'ArrowDown':
        return focus(index + 1)
      case 'ArrowUp':
        return focus(index - 1)
      case 'Home':
        return focus(0)
      case 'End':
        return focus(all.length - 1)
      case 'Escape':
        event.preventDefault()
        return close(true)
      case 'Tab':
        // Focus moves on from the button, as if the menu had never opened.
        return close(true)
      case ' ':
        // A link only answers Enter; a menu item answers Space too.
        if ((event.target as HTMLElement).tagName === 'A') {
          event.preventDefault()
          ;(event.target as HTMLElement).click()
        }
    }
  }

  const menu = (
    <div
      ref={menuRef}
      id={`${id}-menu`}
      role="menu"
      aria-labelledby={`${id}-button`}
      className={styles.menu}
      data-placement={placement}
      style={style}
      onKeyDown={onMenuKey}
    >
      <button
        type="button"
        role="menuitem"
        tabIndex={-1}
        className={styles.item}
        onClick={() => run(onDisclaimer)}
      >
        {t('nav.disclaimer')}
      </button>
      {PAGES.map(({ path, label }) => (
        <a
          key={path}
          role="menuitem"
          tabIndex={-1}
          className={styles.item}
          href={path}
          onClick={(event) => {
            if (!plainClick(event)) return close(false)
            event.preventDefault()
            run(() => onNavigate(path))
          }}
        >
          {t(label)}
        </a>
      ))}
      <button
        type="button"
        role="menuitem"
        tabIndex={-1}
        className={styles.item}
        onClick={() => run(onCookies)}
      >
        {t('nav.cookies')}
      </button>
      <a
        role="menuitem"
        tabIndex={-1}
        className={styles.item}
        href={REPO_URL}
        target="_blank"
        rel="noopener noreferrer"
        onClick={() => close(true)}
      >
        {t('nav.github')}
        <GitHubIcon />
      </a>
      <div role="separator" className={styles.separator} />
      <div role="group" aria-label={t('language.label')} className={styles.languages}>
        {LANGUAGES.map((language) => (
          <button
            key={language}
            type="button"
            role="menuitemradio"
            tabIndex={-1}
            lang={language}
            aria-checked={i18n.resolvedLanguage === language}
            className={styles.language}
            onClick={() =>
              run(() => {
                track({ name: 'language-switch', data: { lang: language } })
                void changeLanguage(language)
              })
            }
          >
            {t(`language.${language}`)}
          </button>
        ))}
      </div>
    </div>
  )

  return (
    <>
      <button
        ref={buttonRef}
        id={`${id}-button`}
        type="button"
        className={className}
        aria-label={t('menu.button')}
        aria-haspopup="menu"
        aria-expanded={open !== false}
        aria-controls={open ? `${id}-menu` : undefined}
        onClick={() => (open ? close(false) : show('first'))}
        onKeyDown={(event) => {
          if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return
          event.preventDefault()
          show(event.key === 'ArrowDown' ? 'first' : 'last')
        }}
      >
        <InfoIcon />
      </button>
      {open && createPortal(menu, document.body)}
    </>
  )
}
