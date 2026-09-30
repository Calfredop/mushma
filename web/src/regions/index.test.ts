import { describe, expect, it } from 'vitest'
import { findRegionAt, listRegions } from '.'

describe('the region registry', () => {
  it.each(listRegions().map((region) => [region.slug, region] as const))(
    '%s names the whole region in its own words, in both languages',
    (_, region) => {
      expect(region.whole.it).toContain(region.name.it)
      expect(region.whole.en).toContain(region.name.en)
    },
  )

  it("finds Valle d'Aosta for a fix in Aosta, although Piemonte's bbox holds it too", () => {
    expect(findRegionAt(45.737, 7.32)?.slug).toBe('valle-d-aosta')
    expect(findRegionAt(45.07, 7.69)?.slug).toBe('piemonte') // Torino
  })

  it("finds Molise for Campobasso and Isernia, and leaves its neighbours' towns in its bbox to them", () => {
    expect(findRegionAt(41.56, 14.66)?.slug).toBe('molise') // Campobasso
    expect(findRegionAt(41.59, 14.23)?.slug).toBe('molise') // Isernia
    expect(findRegionAt(41.78, 14.11)?.slug).toBe('abruzzo') // Castel di Sangro
    expect(findRegionAt(41.41, 14.37)?.slug).toBe('campania') // Piedimonte Matese
  })

  it('keeps Trento and Pordenone in their regions now that Veneto, registered last, overlaps them', () => {
    expect(findRegionAt(46.07, 11.12)?.slug).toBe('trentino-alto-adige') // Trento
    expect(findRegionAt(45.96, 12.66)?.slug).toBe('friuli-venezia-giulia') // Pordenone
    expect(findRegionAt(45.41, 11.88)?.slug).toBe('veneto') // Padova
  })
})
