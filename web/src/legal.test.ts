import { describe, expect, it } from 'vitest'
import itLocale from './i18n/locales/it.json'
import { PRIVACY_SECTIONS, TERMS_SECTIONS } from './legal'

describe('legal section lists', () => {
  it('matches every terms.sections key in the locale copy', () => {
    // A section added to the copy but not to the list would never be shown, or the other way.
    expect(Object.keys(itLocale.terms.sections)).toEqual([...TERMS_SECTIONS])
  })

  it('matches every privacy.sections key in the locale copy', () => {
    expect(Object.keys(itLocale.privacy.sections)).toEqual([...PRIVACY_SECTIONS])
  })
})
