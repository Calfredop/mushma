import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it } from 'vitest'
import i18n, { changeLanguage } from '../i18n'
import { LanguageSwitcher } from './LanguageSwitcher'

afterEach(async () => {
  await act(() => changeLanguage('it'))
  localStorage.clear()
})

describe('LanguageSwitcher', () => {
  it('starts in Italian and switches the UI to English', async () => {
    render(<LanguageSwitcher />)
    expect(screen.getByRole('group', { name: 'Lingua' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Italiano' })).toHaveAttribute(
      'aria-pressed',
      'true',
    )

    await userEvent.click(screen.getByRole('button', { name: 'English' }))

    expect(screen.getByRole('group', { name: 'Language' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'English' })).toHaveAttribute(
      'aria-pressed',
      'true',
    )
    expect(i18n.language).toBe('en')
    expect(document.documentElement.lang).toBe('en')
    expect(localStorage.getItem('mushma.language')).toBe('en')
  })
})
