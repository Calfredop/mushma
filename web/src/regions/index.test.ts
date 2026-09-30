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

  it("finds Basilicata for Matera and the Val d'Agri, and leaves Campania and Calabria their towns in its bbox", () => {
    expect(findRegionAt(40.666, 16.604)?.slug).toBe('basilicata') // Matera
    expect(findRegionAt(40.345, 15.9)?.slug).toBe('basilicata') // Viggiano
    expect(findRegionAt(40.212, 16.676)?.slug).toBe('basilicata') // Policoro
    expect(findRegionAt(40.39, 15.59)?.slug).toBe('campania') // Sala Consilina
    expect(findRegionAt(40.107, 16.581)?.slug).toBe('calabria') // Rocca Imperiale
  })
})
