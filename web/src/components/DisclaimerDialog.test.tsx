import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { DISCLAIMER_SECTIONS } from '../disclaimer'
import itLocale from '../i18n/locales/it.json'
import { DisclaimerDialog, disclaimerAccepted } from './DisclaimerDialog'

afterEach(() => localStorage.clear())

describe('DisclaimerDialog', () => {
  it('shows every section of the copy, then the ASL check', () => {
    // A section added to the copy but not to the list would never be shown.
    expect(Object.keys(itLocale.disclaimer.sections)).toEqual([...DISCLAIMER_SECTIONS])

    render(<DisclaimerDialog open onClose={() => {}} />)
    const dialog = screen.getByRole('dialog', { name: itLocale.disclaimer.title })
    for (const key of DISCLAIMER_SECTIONS) {
      const { title, body } = itLocale.disclaimer.sections[key]
      expect(within(dialog).getByRole('heading', { level: 3, name: title })).toBeVisible()
      expect(within(dialog).getByText(body)).toBeVisible()
    }
    expect(within(dialog).getByText(itLocale.disclaimer.inspection)).toBeVisible()
  })

  it('opens with focus on its title, so reading starts at the top', () => {
    render(<DisclaimerDialog open onClose={() => {}} />)
    expect(
      screen.getByRole('heading', { level: 2, name: itLocale.disclaimer.title }),
    ).toHaveFocus()
  })

  it('remembers the acceptance, but not one given to the shorter v1 text', async () => {
    localStorage.setItem('mushma.disclaimer.v1', 'accepted')
    expect(disclaimerAccepted()).toBe(false)

    const onClose = vi.fn()
    render(<DisclaimerDialog open onClose={onClose} />)
    await userEvent.click(
      screen.getByRole('button', { name: itLocale.disclaimer.accept }),
    )

    expect(onClose).toHaveBeenCalledOnce()
    expect(disclaimerAccepted()).toBe(true)
  })
})
