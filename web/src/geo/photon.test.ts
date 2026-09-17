import { describe, expect, it } from 'vitest'
import { parsePhoton, photonUrl } from './photon'

describe('photonUrl', () => {
  it('limits the search to the region and only sends supported languages', () => {
    const it = new URL(
      photonUrl('Camaldoli', 'it', [
        [9.68, 42.23],
        [12.38, 44.48],
      ]),
    )
    expect(it.origin + it.pathname).toBe('https://photon.komoot.io/api/')
    expect(it.searchParams.get('q')).toBe('Camaldoli')
    expect(it.searchParams.get('bbox')).toBe('9.68,42.23,12.38,44.48')
    expect(it.searchParams.has('lang')).toBe(false) // Photon has no Italian; default is local names
    expect(
      new URL(
        photonUrl('x', 'en', [
          [0, 0],
          [1, 1],
        ]),
      ).searchParams.get('lang'),
    ).toBe('en')
  })
})

describe('parsePhoton', () => {
  it('turns features into places with a readable detail line, dropping duplicates', () => {
    const places = parsePhoton({
      features: [
        {
          geometry: { type: 'Point', coordinates: [11.82, 43.79] },
          properties: {
            osm_type: 'N',
            osm_id: 1,
            name: 'Camaldoli',
            city: 'Poppi',
            county: 'Arezzo',
          },
        },
        {
          geometry: { type: 'Point', coordinates: [11.82, 43.79] },
          properties: { osm_type: 'N', osm_id: 1, name: 'Camaldoli', city: 'Poppi' },
        },
        {
          geometry: { type: 'Point', coordinates: [11.25, 43.77] },
          properties: { osm_type: 'R', osm_id: 2, name: 'Firenze', county: 'Firenze' },
        },
        { geometry: { type: 'Point', coordinates: [1, 2] }, properties: { osm_id: 3 } },
      ],
    })
    expect(places).toEqual([
      { id: 'N1', name: 'Camaldoli', detail: 'Poppi, Arezzo', lat: 43.79, lon: 11.82 },
      { id: 'R2', name: 'Firenze', detail: '', lat: 43.77, lon: 11.25 },
    ])
  })
})
