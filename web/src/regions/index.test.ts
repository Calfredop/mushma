import { describe, expect, it } from 'vitest'
import { listRegions } from '.'
import type { RegionBoundaries } from './boundaries'
import { findRegionAt, regionAt } from './lookup'

describe('the region registry', () => {
  it.each(listRegions().map((region) => [region.slug, region] as const))(
    '%s names the whole region in its own words, in both languages',
    (_, region) => {
      expect(region.whole.it).toContain(region.name.it)
      expect(region.whole.en).toContain(region.name.en)
    },
  )

  it("finds Valle d'Aosta for a fix in Aosta, although Piemonte's bbox holds it too", async () => {
    expect((await findRegionAt(45.737, 7.32))?.slug).toBe('valle-d-aosta')
    expect((await findRegionAt(45.07, 7.69))?.slug).toBe('piemonte') // Torino
  })

  it("finds Molise for Campobasso and Isernia, and leaves its neighbours' towns in its bbox to them", async () => {
    expect((await findRegionAt(41.56, 14.66))?.slug).toBe('molise') // Campobasso
    expect((await findRegionAt(41.59, 14.23))?.slug).toBe('molise') // Isernia
    expect((await findRegionAt(41.78, 14.11))?.slug).toBe('abruzzo') // Castel di Sangro
    expect((await findRegionAt(41.41, 14.37))?.slug).toBe('campania') // Piedimonte Matese
  })

  it('finds Sardinia for Cagliari, Nuoro and La Maddalena, and not for Corsica', async () => {
    expect((await findRegionAt(39.22, 9.11))?.slug).toBe('sardegna') // Cagliari
    expect((await findRegionAt(40.32, 9.33))?.slug).toBe('sardegna') // Nuoro
    expect((await findRegionAt(41.21, 9.41))?.slug).toBe('sardegna') // La Maddalena
    expect(await findRegionAt(41.39, 9.16)).toBeUndefined() // Bonifacio
  })

  it("keeps Trento and Pordenone in their regions, although Veneto's bbox holds them", async () => {
    expect((await findRegionAt(46.07, 11.12))?.slug).toBe('trentino-alto-adige') // Trento
    expect((await findRegionAt(45.96, 12.66))?.slug).toBe('friuli-venezia-giulia') // Pordenone
    expect((await findRegionAt(45.41, 11.88))?.slug).toBe('veneto') // Padova
  })

  it("finds Basilicata for Matera and the Val d'Agri, and leaves Campania and Calabria their towns in its bbox", async () => {
    expect((await findRegionAt(40.666, 16.604))?.slug).toBe('basilicata') // Matera
    expect((await findRegionAt(40.345, 15.9))?.slug).toBe('basilicata') // Viggiano
    expect((await findRegionAt(40.212, 16.676))?.slug).toBe('basilicata') // Policoro
    expect((await findRegionAt(40.39, 15.59))?.slug).toBe('campania') // Sala Consilina
    expect((await findRegionAt(40.107, 16.581))?.slug).toBe('calabria') // Rocca Imperiale
  })

  it("finds Marche for Fabriano, from anywhere, although Umbria's bbox holds it", async () => {
    expect((await findRegionAt(43.33, 12.9))?.slug).toBe('marche')
    expect((await findRegionAt(43.33, 12.9, 'toscana'))?.slug).toBe('marche')
    expect((await findRegionAt(43.33, 12.9, 'umbria'))?.slug).toBe('marche')
  })

  it('finds Liguria for La Spezia and Umbria for Perugia', async () => {
    expect((await findRegionAt(44.1, 9.82))?.slug).toBe('liguria') // La Spezia
    expect((await findRegionAt(44.1, 9.82, 'toscana'))?.slug).toBe('liguria')
    expect((await findRegionAt(43.11, 12.39))?.slug).toBe('umbria') // Perugia
    expect((await findRegionAt(43.11, 12.39, 'marche'))?.slug).toBe('umbria')
  })

  it('gives each side of the Strait of Messina its own region', async () => {
    expect((await findRegionAt(38.11, 15.65))?.slug).toBe('calabria') // Reggio Calabria
    expect((await findRegionAt(38.19, 15.55))?.slug).toBe('sicilia') // Messina
  })

  it('keeps a fix on the beach, just off the simplified coast, in its region', async () => {
    // Viareggio's shore, a few hundred metres west of the ~500 m coastline.
    expect((await findRegionAt(43.87, 10.235))?.slug).toBe('toscana')
    // Out at sea, well clear of any coast.
    expect(await findRegionAt(43.5, 9.9)).toBeUndefined()
  })
})

describe('regionAt', () => {
  const square = (slug: string, west: number): RegionBoundaries['features'][number] => ({
    type: 'Feature',
    properties: { slug, code: 0, name: slug, label: [west + 0.5, 43.5] },
    geometry: {
      type: 'Polygon',
      coordinates: [
        [
          [west, 43],
          [west + 1, 43],
          [west + 1, 44],
          [west, 44],
          [west, 43],
        ],
      ],
    },
  })
  // Two served regions sharing the border at 11° E.
  const boundaries: RegionBoundaries = {
    type: 'FeatureCollection',
    features: [square('toscana', 10), square('umbria', 11)],
  }

  it('takes the region whose boundary holds the point, whatever the preferred one', () => {
    expect(regionAt(43.5, 10.9, boundaries)?.slug).toBe('toscana')
    expect(regionAt(43.5, 10.9, boundaries, 'umbria')?.slug).toBe('toscana')
    expect(regionAt(43.5, 11.1, boundaries, 'toscana')?.slug).toBe('umbria')
  })

  it('keeps the current region within a kilometre of its boundary', () => {
    expect(regionAt(43.5, 11, boundaries, 'umbria')?.slug).toBe('umbria') // on the border
    expect(regionAt(43.5, 11, boundaries, 'toscana')?.slug).toBe('toscana')
    expect(regionAt(43.5, 11.005, boundaries, 'toscana')?.slug).toBe('toscana') // ~0.4 km in
    expect(regionAt(43.5, 11.05, boundaries, 'toscana')?.slug).toBe('umbria') // ~4 km in
  })

  it('takes the nearest region within a kilometre of its boundary, else none', () => {
    expect(regionAt(42.995, 10.5, boundaries)?.slug).toBe('toscana') // ~0.6 km south
    expect(regionAt(42.995, 11.8, boundaries)?.slug).toBe('umbria')
    expect(regionAt(42.98, 10.5, boundaries)).toBeUndefined() // ~2.2 km south
  })
})
