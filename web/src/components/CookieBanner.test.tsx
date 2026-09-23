import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { getConsent } from '../consent'
import itLocale from '../i18n/locales/it.json'
import { CookieBanner } from './CookieBanner'

afterEach(() => localStorage.clear())

describe('CookieBanner', () => {
  it('remembers Accept, and closes', async () => {
    const onClose = vi.fn()
    render(<CookieBanner open onClose={onClose} onPrivacyClick={() => {}} />)

    await userEvent.click(screen.getByRole('button', { name: itLocale.cookies.accept }))

    expect(getConsent()).toBe('accepted')
    expect(onClose).toHaveBeenCalledOnce()
  })

  it('remembers Decline, and closes', async () => {
    const onClose = vi.fn()
    render(<CookieBanner open onClose={onClose} onPrivacyClick={() => {}} />)

    await userEvent.click(screen.getByRole('button', { name: itLocale.cookies.decline }))

    expect(getConsent()).toBe('declined')
    expect(onClose).toHaveBeenCalledOnce()
  })

  it('links to the Privacy Policy', async () => {
    const onPrivacyClick = vi.fn()
    render(<CookieBanner open onClose={() => {}} onPrivacyClick={onPrivacyClick} />)
    const link = screen.getByRole('link', { name: itLocale.cookies.privacyLink })
    expect(link).toHaveAttribute('href', '/privacy')

    await userEvent.click(link)
    expect(onPrivacyClick).toHaveBeenCalledOnce()
  })

  it('shows no controls while closed', () => {
    render(<CookieBanner open={false} onClose={() => {}} onPrivacyClick={() => {}} />)
    expect(
      screen.queryByRole('button', { name: itLocale.cookies.accept }),
    ).not.toBeInTheDocument()
  })
})
