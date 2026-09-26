import { describe, expect, it } from 'vitest'
import type { RegionBoundaries } from '../regions/boundaries'
import { REGIONS } from '../regions'
import { scoreColor } from '../score/scale'
import type { HubRegion } from '../pages/hubRegions'
import {
  NO_SCORE_COLOR,
  regionFillColor,
  regionFillOpacity,
  regionLabelPoints,
} from './hubLayers'

const regions: HubRegion[] = [
  { region: REGIONS.toscana, meanScore: 0.855, goodShare: 0.89 },
  { region: REGIONS.umbria, meanScore: undefined, goodShare: undefined },
]

const square = (x: number, y: number): GeoJSON.Polygon => ({
  type: 'Polygon',
  coordinates: [
    [
      [x, y],
      [x + 1, y],
      [x + 1, y + 1],
      [x, y + 1],
      [x, y],
    ],
  ],
})

const boundaries: RegionBoundaries = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: { slug: 'liguria', code: 7, name: 'Liguria', label: [8.5, 44.3] },
      geometry: square(8, 44),
    },
    {
      type: 'Feature',
      properties: { slug: 'toscana', code: 9, name: 'Toscana', label: [11.25, 43.42] },
      geometry: square(11, 43),
    },
    {
      type: 'Feature',
      properties: { slug: 'umbria', code: 10, name: 'Umbria', label: [12.43, 42.96] },
      geometry: square(12, 42),
    },
  ],
}

describe('regionFillColor', () => {
  it("colours a region by its mean score's class, a served region without one in a neutral tint, and leaves the rest clear", () => {
    expect(regionFillColor(regions)).toEqual([
      'match',
      ['get', 'slug'],
      'toscana',
      scoreColor(0.855),
      'umbria',
      NO_SCORE_COLOR,
      'rgba(0, 0, 0, 0)',
    ])
  })
})

describe('regionFillOpacity', () => {
  it('fills only served regions, a hovered one more strongly', () => {
    expect(regionFillOpacity(regions)).toEqual([
      'match',
      ['get', 'slug'],
      ['toscana', 'umbria'],
      ['case', ['boolean', ['feature-state', 'hover'], false], 0.92, 0.72],
      0,
    ])
  })

  it('is a plain 0 when no region is served, which a match expression cannot say', () => {
    expect(regionFillOpacity([])).toBe(0)
  })
})

describe('regionLabelPoints', () => {
  it("puts a served region's name, in the UI language, at its label point", () => {
    const points = regionLabelPoints(boundaries, regions, 'en')
    expect(points.features).toEqual([
      {
        type: 'Feature',
        properties: { slug: 'toscana', name: 'Tuscany' },
        geometry: { type: 'Point', coordinates: [11.25, 43.42] },
      },
      {
        type: 'Feature',
        properties: { slug: 'umbria', name: 'Umbria' },
        geometry: { type: 'Point', coordinates: [12.43, 42.96] },
      },
    ])
  })
})
