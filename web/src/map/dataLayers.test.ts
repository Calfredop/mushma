import { describe, expect, it } from 'vitest'
import { buildMapStyle, DATA_LAYERS_BEFORE } from './basemap'
import { regionMask, withDataLayers } from './dataLayers'

const region: [[number, number], [number, number]] = [
  [9.68, 42.23],
  [12.38, 44.48],
]

describe('withDataLayers', () => {
  it('puts score cells under the basemap roads and labels, and overlays on top', () => {
    const base = buildMapStyle({
      basemapUrl: '/b.pmtiles',
      lang: 'it',
      origin: 'http://h',
    })
    const style = withDataLayers(base, region)
    const ids = style.layers.map((l) => l.id)
    const roads = ids.indexOf(DATA_LAYERS_BEFORE)
    expect(ids.indexOf('cells-dot')).toBeLessThan(roads)
    expect(ids.indexOf('cells-fill')).toBeLessThan(roads)
    expect(ids.indexOf('region-mask')).toBeGreaterThan(ids.indexOf('places_locality'))
    expect(ids.slice(-3)).toEqual(['spot-point', 'sightings-circle', 'sightings-count'])
    expect(Object.keys(style.sources)).toEqual(
      expect.arrayContaining(['protomaps', 'cells-points', 'cells-squares', 'sightings']),
    )
    expect(base.layers).toHaveLength(ids.length - 10) // the input style is not mutated
  })

  it('still works over the plain land fill', () => {
    const style = withDataLayers(buildMapStyle({ lang: 'it' }), region)
    expect(style.layers.map((l) => l.id).slice(0, 4)).toEqual([
      'background',
      'cells-dot',
      'cells-fill',
      'cells-outline',
    ])
  })
})

describe('regionMask', () => {
  it('is the world with the region as a hole, [lon, lat]', () => {
    const [outer, hole] = regionMask(region).geometry.coordinates
    expect(outer).toHaveLength(5)
    expect(hole[0]).toEqual([9.68, 42.23])
    expect(hole).toContainEqual([12.38, 44.48])
  })
})
