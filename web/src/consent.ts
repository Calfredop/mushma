/**
 * The cookie/analytics consent choice: `null` until answered. `feat-umami-integration.md`'s
 * analytics loader gates on this, so the contract (storage key, value shape, the change event)
 * is fixed here rather than duplicated there.
 */
const STORAGE_KEY = 'mushma.cookieConsent.v1'
const CHANGE_EVENT = 'mushma:cookie-consent-change'

export type Consent = 'accepted' | 'declined'

function isConsent(value: string | null): value is Consent {
  return value === 'accepted' || value === 'declined'
}

export function getConsent(): Consent | null {
  try {
    const value = localStorage.getItem(STORAGE_KEY)
    return isConsent(value) ? value : null
  } catch {
    return null
  }
}

export function setConsent(consent: Consent): void {
  try {
    localStorage.setItem(STORAGE_KEY, consent)
  } catch {
    // Not persisted, but the choice still applies to this visit.
  }
  // `storage` only fires in other tabs; this tab's own listeners (the banner, the
  // analytics loader) need to hear about the choice too.
  window.dispatchEvent(new CustomEvent<Consent>(CHANGE_EVENT, { detail: consent }))
}

/** Calls `listener` whenever the choice changes in this tab. Returns the unsubscribe. */
export function onConsentChange(listener: (consent: Consent) => void): () => void {
  const handler = (event: Event) => listener((event as CustomEvent<Consent>).detail)
  window.addEventListener(CHANGE_EVENT, handler)
  return () => window.removeEventListener(CHANGE_EVENT, handler)
}
