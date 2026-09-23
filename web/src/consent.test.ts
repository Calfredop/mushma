import { afterEach, describe, expect, it, vi } from 'vitest'
import { getConsent, onConsentChange, setConsent } from './consent'

afterEach(() => localStorage.clear())

describe('getConsent', () => {
  it('is null until a choice is made', () => {
    expect(getConsent()).toBeNull()
  })

  it('reads back what was set', () => {
    setConsent('accepted')
    expect(getConsent()).toBe('accepted')
    setConsent('declined')
    expect(getConsent()).toBe('declined')
  })

  it('ignores an unrelated or corrupt stored value', () => {
    localStorage.setItem('mushma.cookieConsent.v1', 'yes please')
    expect(getConsent()).toBeNull()
  })
})

describe('onConsentChange', () => {
  it('fires in the same tab the moment the choice is set', () => {
    const listener = vi.fn()
    const unsubscribe = onConsentChange(listener)
    setConsent('accepted')
    expect(listener).toHaveBeenCalledOnce()
    expect(listener).toHaveBeenCalledWith('accepted')
    unsubscribe()
  })

  it('stops firing once unsubscribed', () => {
    const listener = vi.fn()
    const unsubscribe = onConsentChange(listener)
    unsubscribe()
    setConsent('declined')
    expect(listener).not.toHaveBeenCalled()
  })
})
