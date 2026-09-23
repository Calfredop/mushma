import { describe, expect, it } from 'vitest'
import type { FilterSpecification, LayerSpecification } from 'maplibre-gl'
import { layerOpacities, OPACITY_CAP } from '../score/indicators'
import { buildMapStyle, DATA_LAYERS_BEFORE } from './basemap'
import {
  ANALYSIS_CELL_LAYERS,
  ANALYSIS_LAYERS_BEFORE,
  analysisLayers,
  CELL_LAYERS,
  regionMask,
  withDataLayers,
} from './dataLayers'

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
    expect(base.layers).toHaveLength(ids.length - 12) // the input style is not mutated
  })

  it('has hidden analysis base layers among the cells, where indicators go in', () => {
    const style = withDataLayers(buildMapStyle({ lang: 'it' }), region)
    const ids = style.layers.map((l) => l.id)
    expect(ids.slice(0, 6)).toEqual([
      'background',
      'cells-dot',
      'cells-fill',
      'factors-base-dot',
      'factors-base-fill',
      'cells-outline',
    ])
    // Indicators go in under the outline, so selection, spot and sightings stay on top.
    expect(ANALYSIS_LAYERS_BEFORE).toBe('cells-outline')
    for (const id of ANALYSIS_CELL_LAYERS) {
      const layer = style.layers.find((l) => l.id === id)!
      expect(layer.layout?.visibility).toBe('none')
    }
    // Taps land on the square first, then the dot, in either mode.
    expect(CELL_LAYERS[0]).toBe('cells-fill')
    expect(ANALYSIS_CELL_LAYERS[0]).toBe('factors-base-fill')
  })

  it('still works over the plain land fill', () => {
    const style = withDataLayers(buildMapStyle({ lang: 'it' }), region)
    expect(style.layers.map((l) => l.id).slice(0, 3)).toEqual([
      'background',
      'cells-dot',
      'cells-fill',
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

describe('analysisLayers', () => {
  const active = [
    { id: 'rain_trigger', color: '#268C9F' },
    { id: 'drying', color: '#F4D03D' },
  ]
  const byId = (layers: LayerSpecification[], id: string) =>
    layers.find((layer) => layer.id === id)!

  it('draws a dot layer and a square layer per indicator, bottom to top', () => {
    expect(analysisLayers(active).map((layer) => layer.id)).toEqual([
      'indicator-dot-rain_trigger',
      'indicator-fill-rain_trigger',
      'indicator-dot-drying',
      'indicator-fill-drying',
    ])
    expect(analysisLayers([])).toEqual([])
  })

  it('dots below zoom 11 and squares from 9, like the score, on the shared cell sources', () => {
    const layers = analysisLayers(active)
    const dot = byId(layers, 'indicator-dot-drying')
    const fill = byId(layers, 'indicator-fill-drying')
    expect(dot).toMatchObject({ type: 'circle', source: 'cells-points', maxzoom: 11 })
    expect(fill).toMatchObject({ type: 'fill', source: 'cells-squares', minzoom: 9 })
    expect(dot.paint).toMatchObject({ 'circle-color': '#F4D03D' })
    expect(fill.paint).toMatchObject({ 'fill-color': '#F4D03D' })
  })

  it('never draws a cell whose winning rules lack the factor', () => {
    const layers = analysisLayers(active)
    const filter: FilterSpecification = ['has', 'rain_trigger']
    for (const id of ['indicator-dot-rain_trigger', 'indicator-fill-rain_trigger']) {
      expect(byId(layers, id)).toMatchObject({ filter })
    }
  })

  it("sets opacity to the value times each layer's share of the cap", () => {
    const [bottom, top] = layerOpacities(2)
    const layers = analysisLayers(active)
    const fill = (id: string) => byId(layers, `indicator-fill-${id}`)
    const dot = (id: string) => byId(layers, `indicator-dot-${id}`)
    // Squares fade in from zoom 9 to 10.5, dots fade out from 9.5 to 10.5.
    expect(fill('rain_trigger').paint).toMatchObject({
      'fill-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        9,
        0,
        10.5,
        ['*', ['get', 'rain_trigger'], bottom],
      ],
    })
    expect(dot('drying').paint).toMatchObject({
      'circle-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        9.5,
        ['*', ['get', 'drying'], top],
        10.5,
        0,
      ],
    })
    expect(
      analysisLayers([active[0]]).find((l) => l.type === 'fill')!.paint,
    ).toMatchObject({
      'fill-opacity': [
        'interpolate',
        ['linear'],
        ['zoom'],
        9,
        0,
        10.5,
        ['*', ['get', 'rain_trigger'], OPACITY_CAP],
      ],
    })
  })
})
