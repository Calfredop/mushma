import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import i18n, { changeLanguage } from '../i18n'
import { InfoMenu } from './InfoMenu'

const track = vi.fn()
vi.mock('../analytics', () => ({ track: (event: unknown) => track(event) }))

afterEach(async () => {
  await act(() => changeLanguage('it'))
  localStorage.clear()
  track.mockClear()
})

function setup() {
  const props = {
    onDisclaimer: vi.fn(),
    onCookies: vi.fn(),
    onNavigate: vi.fn(),
  }
  render(<InfoMenu placement="left" {...props} />)
  const button = screen.getByRole('button', { name: 'Info e impostazioni' })
  return { ...props, button }
}

describe('InfoMenu', () => {
  it('opens a menu of its seven entries from a menu button', async () => {
    const { button } = setup()
    expect(button).toHaveAttribute('aria-haspopup', 'menu')
    expect(button).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('menu')).not.toBeInTheDocument()

    await userEvent.click(button)

    expect(button).toHaveAttribute('aria-expanded', 'true')
    const menu = screen.getByRole('menu', { name: 'Info e impostazioni' })
    expect(menu).toBeInTheDocument()
    expect(screen.getAllByRole('menuitem').map((item) => item.textContent)).toEqual([
      'Avvertenze',
      'Dati e crediti',
      'Termini e condizioni',
      'Privacy',
      'Preferenze sui cookie',
      'Codice su GitHub',
    ])
    // The language switch is the seventh entry: one choice per language.
    expect(screen.getByRole('group', { name: 'Lingua' })).toBeInTheDocument()
    expect(screen.getByRole('menuitemradio', { name: 'Italiano' })).toHaveAttribute(
      'aria-checked',
      'true',
    )
    expect(screen.getByRole('menuitemradio', { name: 'English' })).toHaveAttribute(
      'aria-checked',
      'false',
    )
  })

  it('keeps real links, so the pages and the code are one click away', async () => {
    const { button } = setup()
    await userEvent.click(button)
    expect(screen.getByRole('menuitem', { name: 'Dati e crediti' })).toHaveAttribute(
      'href',
      '/credits',
    )
    expect(
      screen.getByRole('menuitem', { name: 'Termini e condizioni' }),
    ).toHaveAttribute('href', '/terms')
    expect(screen.getByRole('menuitem', { name: 'Privacy' })).toHaveAttribute(
      'href',
      '/privacy',
    )
    const github = screen.getByRole('menuitem', { name: 'Codice su GitHub' })
    expect(github).toHaveAttribute('href', 'https://github.com/Calfredop/mushma')
    expect(github).toHaveAttribute('target', '_blank')
    expect(github.getAttribute('rel')).toContain('noopener')
  })

  it('moves focus with the arrow keys, Home and End, wrapping at the ends', async () => {
    const { button } = setup()
    button.focus()
    await userEvent.keyboard('{Enter}')
    expect(screen.getByRole('menuitem', { name: 'Avvertenze' })).toHaveFocus()

    await userEvent.keyboard('{ArrowDown}')
    expect(screen.getByRole('menuitem', { name: 'Dati e crediti' })).toHaveFocus()
    await userEvent.keyboard('{End}')
    expect(screen.getByRole('menuitemradio', { name: 'English' })).toHaveFocus()
    await userEvent.keyboard('{ArrowDown}')
    expect(screen.getByRole('menuitem', { name: 'Avvertenze' })).toHaveFocus()
    await userEvent.keyboard('{ArrowUp}')
    expect(screen.getByRole('menuitemradio', { name: 'English' })).toHaveFocus()
    await userEvent.keyboard('{Home}')
    expect(screen.getByRole('menuitem', { name: 'Avvertenze' })).toHaveFocus()
  })

  it('opens on the last entry with ArrowUp', async () => {
    const { button } = setup()
    button.focus()
    await userEvent.keyboard('{ArrowUp}')
    expect(screen.getByRole('menuitemradio', { name: 'English' })).toHaveFocus()
  })

  it('closes on Escape and hands focus back to its button', async () => {
    const { button } = setup()
    await userEvent.click(button)
    await userEvent.keyboard('{ArrowDown}')
    await userEvent.keyboard('{Escape}')
    expect(screen.queryByRole('menu')).not.toBeInTheDocument()
    expect(button).toHaveAttribute('aria-expanded', 'false')
    expect(button).toHaveFocus()
  })

  it('closes on a click outside it', async () => {
    const { button } = setup()
    await userEvent.click(button)
    await userEvent.click(document.body)
    expect(screen.queryByRole('menu')).not.toBeInTheDocument()
  })

  it('runs an entry, closes, and hands focus back first', async () => {
    const { button, onDisclaimer, onCookies, onNavigate } = setup()
    // The dialog an entry opens gives focus back to whatever had it: the button, not a
    // menu item that is gone.
    onDisclaimer.mockImplementation(() => expect(button).toHaveFocus())

    await userEvent.click(button)
    await userEvent.click(screen.getByRole('menuitem', { name: 'Avvertenze' }))
    expect(onDisclaimer).toHaveBeenCalledOnce()
    expect(screen.queryByRole('menu')).not.toBeInTheDocument()

    await userEvent.click(button)
    await userEvent.click(screen.getByRole('menuitem', { name: 'Termini e condizioni' }))
    expect(onNavigate).toHaveBeenCalledWith('/terms')

    await userEvent.click(button)
    screen.getByRole('menuitem', { name: 'Preferenze sui cookie' }).focus()
    await userEvent.keyboard(' ')
    expect(onCookies).toHaveBeenCalledOnce()
  })

  it('switches the language and tracks the switch', async () => {
    const { button } = setup()
    await userEvent.click(button)
    await userEvent.click(screen.getByRole('menuitemradio', { name: 'English' }))
    expect(i18n.language).toBe('en')
    expect(track).toHaveBeenCalledWith({ name: 'language-switch', data: { lang: 'en' } })
    expect(screen.getByRole('button', { name: 'Info and settings' })).toBeInTheDocument()
  })
})
