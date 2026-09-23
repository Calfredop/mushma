import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { setConsent } from './consent'
import { beforeSendGuard, initAnalytics, track } from './analytics'

const SRC = 'https://m.mappafunghi.app/js/widget.js'
const WEBSITE_ID = 'site-123'
const DOMAINS = 'mappafunghi.app'

function configure() {
  vi.stubEnv('PROD', true)
  vi.stubEnv('VITE_UMAMI_SRC', SRC)
  vi.stubEnv('VITE_UMAMI_WEBSITE_ID', WEBSITE_ID)
  vi.stubEnv('VITE_UMAMI_DOMAINS', DOMAINS)
}

function injectedScript(): HTMLScriptElement | null {
  return document.querySelector('script[data-website-id]')
}

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  vi.unstubAllEnvs()
  document.querySelectorAll('script[data-website-id]').forEach((el) => el.remove())
  localStorage.clear()
})

describe('initAnalytics', () => {
  it('injects no script when unconfigured', () => {
    vi.stubEnv('PROD', true)
    setConsent('accepted')
    initAnalytics()
    expect(injectedScript()).toBeNull()
  })

  it('injects no script outside a production build, even fully configured', () => {
    configure()
    vi.stubEnv('PROD', false)
    setConsent('accepted')
    initAnalytics()
    expect(injectedScript()).toBeNull()
  })

  it('injects no script without consent', () => {
    configure()
    initAnalytics()
    expect(injectedScript()).toBeNull()
  })

  it('injects no script when consent was declined', () => {
    configure()
    setConsent('declined')
    initAnalytics()
    expect(injectedScript()).toBeNull()
  })

  it('loads once consent is accepted, live', () => {
    configure()
    initAnalytics()
    expect(injectedScript()).toBeNull()
    setConsent('accepted')
    expect(injectedScript()).not.toBeNull()
  })

  it('sets the tracker attributes', () => {
    configure()
    setConsent('accepted')
    initAnalytics()
    const script = injectedScript()
    expect(script?.src).toBe(SRC)
    expect(script?.dataset.websiteId).toBe(WEBSITE_ID)
    expect(script?.dataset.excludeSearch).toBe('true')
    expect(script?.dataset.autoTrack).toBe('false')
    expect(script?.dataset.domains).toBe(DOMAINS)
    expect(script?.dataset.beforeSend).toBeTruthy()
    expect(
      (window as unknown as Record<string, unknown>)[script!.dataset.beforeSend!],
    ).toBe(beforeSendGuard)
  })
})

describe('beforeSendGuard', () => {
  it('drops everything unless consent is accepted', () => {
    expect(beforeSendGuard('pageview', { url: '/toscana' })).toBe(false)
    setConsent('declined')
    expect(beforeSendGuard('pageview', { url: '/toscana' })).toBe(false)
  })

  it('collapses any app path to /, keeps /credits, and drops the query', () => {
    setConsent('accepted')
    expect(
      beforeSendGuard('pageview', { url: '/toscana/porcini?at=43.5,11.2' }),
    ).toMatchObject({ url: '/' })
    expect(beforeSendGuard('pageview', { url: '/credits?x=1' })).toMatchObject({
      url: '/credits',
    })
    expect(beforeSendGuard('pageview', { url: '/' })).toMatchObject({ url: '/' })
  })

  it('strips the query string from the referrer', () => {
    setConsent('accepted')
    const result = beforeSendGuard('pageview', {
      url: '/',
      referrer: 'https://example.com/foo?bar=baz',
    })
    expect(result).toMatchObject({ referrer: 'https://example.com/foo' })
  })

  it('drops event data properties that are not on the allowlist', () => {
    setConsent('accepted')
    const result = beforeSendGuard('event', {
      url: '/toscana',
      name: 'species-switch',
      data: { species: 'porcini', at: '43.5,11.2', cell: 'abc123' },
    })
    expect(result).toMatchObject({ data: { species: 'porcini' } })
  })
})

describe('track', () => {
  it('does nothing when the tracker is not loaded', () => {
    delete (window as { umami?: unknown }).umami
    expect(() => track({ name: 'pwa-install' })).not.toThrow()
  })

  it('forwards the event name and data to the loaded tracker', () => {
    const trackFn = vi.fn()
    ;(window as unknown as { umami: { track: typeof trackFn } }).umami = {
      track: trackFn,
    }
    track({ name: 'species-switch', data: { species: 'ovoli' } })
    expect(trackFn).toHaveBeenCalledWith('species-switch', { species: 'ovoli' })
    delete (window as { umami?: unknown }).umami
  })
})
