/**
 * Self-hosted Umami analytics (`feat-umami-integration.md`). Loads only in a production build,
 * once configured and once the visitor has accepted the cookie banner (`./consent`), and follows
 * a later choice live. `data-auto-track` is off: the app fires every pageview and event itself,
 * so an in-app species/view/date change (a `pushState`/`replaceState`, per `usePath`) never
 * becomes a second, URL-carrying pageview on its own.
 *
 * `beforeSendGuard` is the actual privacy boundary, re-checked on every send: it drops the
 * payload outright unless consent is `accepted`, collapses every app path to `/` (keeping only
 * `/credits`) so the `?at=`/`?cell=` spot in the URL never reaches Umami, strips the referrer's
 * query string, and keeps only allow-listed event properties.
 */
import { type Language } from './i18n'
import { getConsent, onConsentChange, type Consent } from './consent'
import type { SpeciesOrCombined, View } from './state/urlState'

export type AnalyticsEvent =
  | { name: 'species-switch'; data: { species: SpeciesOrCombined } }
  | { name: 'view-switch'; data: { view: View } }
  | { name: 'spot-open'; data: { method: 'map' | 'search' | 'gps' | 'hotspot' } }
  | { name: 'date-move'; data: { offset: number | 'replay' } }
  | { name: 'pwa-install' }
  | { name: 'language-switch'; data: { lang: Language } }

/** Every `data` key any event above carries; the guard drops anything else. */
const ALLOWED_DATA_KEYS = new Set(['species', 'view', 'method', 'offset', 'lang'])

const GUARD_NAME = '__mushmaGuard'

interface UmamiPayload {
  url?: string
  referrer?: string
  data?: Record<string, unknown>
  [key: string]: unknown
}

declare global {
  interface Window {
    umami?: { track: (name?: string, data?: Record<string, unknown>) => void }
  }
}

function stripQuery(value: string | undefined): string | undefined {
  if (!value) return value
  const query = value.indexOf('?')
  return query === -1 ? value : value.slice(0, query)
}

/** Only `/` and `/credits` ever reach Umami as a path — the "Decided" pageview allowlist. */
function normalizedPath(url: string | undefined): string {
  return stripQuery(url) === '/credits' ? '/credits' : '/'
}

export function beforeSendGuard(
  _type: string,
  payload: UmamiPayload,
): UmamiPayload | false {
  if (getConsent() !== 'accepted') return false
  const next: UmamiPayload = {
    ...payload,
    url: normalizedPath(payload.url),
    referrer: stripQuery(payload.referrer),
  }
  if (next.data) {
    next.data = Object.fromEntries(
      Object.entries(next.data).filter(([key]) => ALLOWED_DATA_KEYS.has(key)),
    )
  }
  return next
}

interface Config {
  src: string
  websiteId: string
  domains?: string
}

function configured(): Config | null {
  if (!import.meta.env.PROD) return null
  const src = import.meta.env.VITE_UMAMI_SRC
  const websiteId = import.meta.env.VITE_UMAMI_WEBSITE_ID
  if (!src || !websiteId) return null
  return { src, websiteId, domains: import.meta.env.VITE_UMAMI_DOMAINS }
}

function loadScript(config: Config): void {
  ;(window as unknown as Record<string, unknown>)[GUARD_NAME] = beforeSendGuard
  const script = document.createElement('script')
  script.defer = true
  script.src = config.src
  script.dataset.websiteId = config.websiteId
  script.dataset.excludeSearch = 'true'
  script.dataset.autoTrack = 'false'
  script.dataset.beforeSend = GUARD_NAME
  if (config.domains) script.dataset.domains = config.domains
  // The one pageview this session sends: everything after is a typed event (`track` below).
  script.addEventListener('load', () => window.umami?.track(), { once: true })
  document.head.appendChild(script)
}

let scriptLoaded = false
let unsubscribeConsent: (() => void) | null = null

export function initAnalytics(): void {
  unsubscribeConsent?.()
  unsubscribeConsent = null
  scriptLoaded = false

  const config = configured()
  if (!config) return

  const tryLoad = (consent: Consent | null) => {
    if (scriptLoaded || consent !== 'accepted') return
    scriptLoaded = true
    loadScript(config)
  }
  tryLoad(getConsent())
  unsubscribeConsent = onConsentChange(tryLoad)
}

/** No-ops when the tracker isn't loaded (unconfigured, not yet consented, or still in dev). */
export function track(event: AnalyticsEvent): void {
  window.umami?.track(event.name, 'data' in event ? event.data : undefined)
}
