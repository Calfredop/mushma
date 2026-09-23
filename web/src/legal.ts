/**
 * Section order for the Terms and Privacy pages, each a `terms.sections.<key>` or
 * `privacy.sections.<key>` title and body in the locale copy — same shape and purpose as
 * `disclaimer.ts`'s `DISCLAIMER_SECTIONS`, so the pages and the locale files never drift apart.
 */
export const TERMS_SECTIONS = [
  'service',
  'scoreNature',
  'userResponsibility',
  'liability',
  'governingLaw',
  'changes',
] as const

export type TermsSection = (typeof TERMS_SECTIONS)[number]

export const PRIVACY_SECTIONS = [
  'dataCollected',
  'legalBasis',
  'analytics',
  'sightingsPrivacy',
  'subprocessors',
  'retention',
  'internationalTransfer',
  'rights',
  'complaint',
] as const

export type PrivacySection = (typeof PRIVACY_SECTIONS)[number]
