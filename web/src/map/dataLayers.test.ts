import { describe, expect, it } from 'vitest'
import type { FilterSpecification, LayerSpecification } from 'maplibre-gl'
import { layerOpacities, OPACITY_CAP } from '../score/indicators'
import { buildMapStyle, DATA_LAYERS_BEFORE } from './basemap'
import {
  ANALYSIS_CELL_LAYERS,
  ANALYSIS_LAYERS,
  ANALYSIS_LAYERS_BEFORE,
  analysisLayers,
  CELL_CLOUD_RADIUS,
  CELL_LAYERS,
  SCORE_LAYERS,
  regionMask,
  withDataLayers,
} from './dataLayers'

const region: [[number, number], [number, number]] = [
  [9.68, 42.23],
  [12.38, 44.48],
]

describe('withDataLayers', () => {
  it('puts soft score clouds under the basemap roads and labels, and overlays on top', () => {
    const base = buildMapStyle({
      basemapUrl: '/b.pmtiles',
      lang: 'it',
      origin: 'http://h',
    })
    const style = withDataLayers(base, region)
    const ids = style.layers.map((l) => l.id)
    const roads = ids.indexOf(DATA_LAYERS_BEFORE)
    expect(ids.indexOf('cells-cloud')).toBeLessThan(roads)
    expect(ids.indexOf('cells-hit')).toBeLessThan(roads)
    expect(ids.indexOf('region-mask')).toBeGreaterThan(ids.indexOf('places_locality'))
    expect(ids.slice(-3)).toEqual(['spot-point', 'sightings-circle', 'sightings-count'])
    expect(Object.keys(style.sources)).toEqual(
      expect.arrayContaining(['protomaps', 'cells-points', 'cells-squares', 'sightings']),
    )
    expect(base.layers).toHaveLength(ids.length - 11) // the input style is not mutated
  })

  it('draws scores as a blurred cloud, with an invisible hit fill for taps', () => {
    const style = withDataLayers(buildMapStyle({ lang: 'it' }), region)
    const cloud = style.layers.find((l) => l.id === 'cells-cloud')!
    const hit = style.layers.find((l) => l.id === 'cells-hit')!
    expect(cloud).toMatchObject({ type: 'circle', source: 'cells-points' })
    expect(cloud).not.toHaveProperty('maxzoom')
    expect(cloud).not.toHaveProperty('minzoom')
    expect(cloud.paint).toMatchObject({
      'circle-blur': expect.any(Number),
      'circle-opacity': expect.any(Number),
    })
    expect((cloud.paint as { 'circle-blur': number })['circle-blur']).toBeGreaterThan(0.4)
    expect(hit).toMatchObject({
      type: 'fill',
      source: 'cells-squares',
      paint: { 'fill-opacity': 0 },
    })
    expect(style.layers.some((l) => l.id === 'cells-dot')).toBe(false)
    expect(style.layers.some((l) => l.id === 'cells-fill')).toBe(false)
    expect(style.layers.some((l) => l.id === 'cells-outline')).toBe(false)
  })

  it('keeps cloud radius geographic so adjacent 1 km cells stay linked when zooming in', () => {
    // Screen pixels for a fixed ground size double each zoom step — linear zoom
    // stops left huge gaps between neighbours at high zoom.
    expect(CELL_CLOUD_RADIUS[1]).toEqual(['exponential', 2])
    const px = (z: number) => {
      for (let i = 3; i < CELL_CLOUD_RADIUS.length; i += 2) {
        if (CELL_CLOUD_RADIUS[i] === z) return CELL_CLOUD_RADIUS[i + 1] as number
      }
      return undefined
    }
    // From z10 → z14 (4 steps) radius should grow ~16×, not stall.
    expect(px(14)! / px(10)!).toBeGreaterThan(12)
    // At mid-zoom the blob is wider than half a cell (500 m) so neighbours overlap
    // even after blur; ~18 px ≈ 2 km at z10 over Tuscany.
    expect(px(10)!).toBeGreaterThanOrEqual(18)
  })

  it('has hidden analysis base layers among the cells, where indicators go in', () => {
    const style = withDataLayers(buildMapStyle({ lang: 'it' }), region)
    const ids = style.layers.map((l) => l.id)
    expect(ids.slice(0, 5)).toEqual([
      'background',
      'cells-hit',
      'cells-cloud',
      'factors-base-hit',
      'factors-base-cloud',
    ])
    expect(ANALYSIS_LAYERS_BEFORE).toBe(DATA_LAYERS_BEFORE)
    for (const id of ANALYSIS_CELL_LAYERS) {
      const layer = style.layers.find((l) => l.id === id)!
      expect(layer.layout?.visibility).toBe('none')
    }
    // Taps land on the invisible hit fill; visibility toggles hit + cloud together.
    expect(CELL_LAYERS).toEqual(['cells-hit'])
    expect(ANALYSIS_CELL_LAYERS).toEqual(['factors-base-hit'])
    expect(SCORE_LAYERS).toEqual(['cells-hit', 'cells-cloud'])
    expect(ANALYSIS_LAYERS).toEqual(['factors-base-hit', 'factors-base-cloud'])
  })

  it('still works over the plain land fill', () => {
    const style = withDataLayers(buildMapStyle({ lang: 'it' }), region)
    expect(style.layers.map((l) => l.id).slice(0, 3)).toEqual([
      'background',
      'cells-hit',
      'cells-cloud',
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

  it('draws one soft cloud layer per indicator, bottom to top', () => {
    expect(analysisLayers(active).map((layer) => layer.id)).toEqual([
      'indicator-cloud-rain_trigger',
      'indicator-cloud-drying',
    ])
    expect(analysisLayers([])).toEqual([])
  })

  it('uses blurred circles on the shared points source at every zoom', () => {
    const layers = analysisLayers(active)
    const cloud = byId(layers, 'indicator-cloud-drying')
    expect(cloud).toMatchObject({ type: 'circle', source: 'cells-points' })
    expect(cloud).not.toHaveProperty('maxzoom')
    expect(cloud).not.toHaveProperty('minzoom')
    expect(cloud.paint).toMatchObject({
      'circle-color': '#F4D03D',
      'circle-blur': expect.any(Number),
    })
    expect((cloud.paint as { 'circle-blur': number })['circle-blur']).toBeGreaterThan(0.5)
  })

  it('never draws a cell whose winning rules lack the factor', () => {
    const layers = analysisLayers(active)
    const filter: FilterSpecification = ['has', 'rain_trigger']
    expect(byId(layers, 'indicator-cloud-rain_trigger')).toMatchObject({ filter })
  })

  it("sets opacity to the value times each layer's share of the cap", () => {
    const [bottom, top] = layerOpacities(2)
    const layers = analysisLayers(active)
    const cloud = (id: string) => byId(layers, `indicator-cloud-${id}`)
    expect(cloud('rain_trigger').paint).toMatchObject({
      'circle-opacity': ['*', ['get', 'rain_trigger'], bottom],
    })
    expect(cloud('drying').paint).toMatchObject({
      'circle-opacity': ['*', ['get', 'drying'], top],
    })
    expect(analysisLayers([active[0]])[0].paint).toMatchObject({
      'circle-opacity': ['*', ['get', 'rain_trigger'], OPACITY_CAP],
    })
  })
})
