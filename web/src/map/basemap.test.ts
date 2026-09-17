import { describe, expect, it } from 'vitest'
import { buildMapStyle, DATA_LAYERS_BEFORE, hillshade, sourceUrl } from './basemap'

describe('sourceUrl', () => {
  it('reads .pmtiles files through the pmtiles protocol with an absolute URL', () => {
    expect(sourceUrl('/basemap/tuscany.pmtiles', 'http://localhost:5173/app')).toBe(
      'pmtiles://http://localhost:5173/basemap/tuscany.pmtiles',
    )
  })

  it('passes TileJSON URLs through', () => {
    expect(sourceUrl('https://tiles.example.workers.dev/tuscany.json', 'http://x')).toBe(
      'https://tiles.example.workers.dev/tuscany.json',
    )
  })
})

describe('buildMapStyle', () => {
  it('draws a plain land fill without a basemap', () => {
    const style = buildMapStyle({ lang: 'it' })
    expect(style.layers.map((l) => l.id)).toEqual(['background'])
    expect(style.sources).toEqual({})
    expect(style.glyphs).toContain('{fontstack}/{range}.pbf')
  })

  it('adds the Protomaps layers with Italian labels and the data-layer anchor', () => {
    const style = buildMapStyle({
      basemapUrl: '/b.pmtiles',
      lang: 'it',
      origin: 'http://h',
    })
    const ids = style.layers.map((l) => l.id)
    expect(style.sources.protomaps).toMatchObject({
      type: 'vector',
      url: 'pmtiles://http://h/b.pmtiles',
    })
    expect(ids).toContain(DATA_LAYERS_BEFORE)
    expect(ids).toContain('places_locality')
    expect(
      JSON.stringify(style.layers.find((l) => l.id === 'places_locality')),
    ).toContain('name:it')
  })

  it('describes hillshade as a separate terrarium source and layer', () => {
    const { source, layer } = hillshade('/t.pmtiles', 'http://h')
    expect(source).toMatchObject({
      type: 'raster-dem',
      encoding: 'terrarium',
      url: 'pmtiles://http://h/t.pmtiles',
    })
    expect(layer).toMatchObject({ id: 'hillshade', type: 'hillshade', source: 'terrain' })
  })
})
