import { describe, expect, it } from 'vitest'
import {
  cellSquare,
  cellsToPoints,
  cellsToSquares,
  sightingsByCell,
  sightingsToPoints,
} from './geojson'

const cells = [
  { cell_id: 'a', lon: 11, lat: 43.5, score: 0.4 },
  { cell_id: 'b', lon: 10.5, lat: 44, score: 0.9 },
]

describe('cellSquare', () => {
  it('draws a closed ~1 km square centred on the cell, wider in degrees of longitude', () => {
    const [ring] = cellSquare(11, 43.5, 1)
    expect(ring).toHaveLength(5)
    expect(ring[0]).toEqual(ring[4])
    const lons = ring.map(([lon]) => lon)
    const lats = ring.map(([, lat]) => lat)
    const width = Math.max(...lons) - Math.min(...lons)
    const height = Math.max(...lats) - Math.min(...lats)
    expect(height).toBeCloseTo(1 / 111.32, 5)
    expect(width).toBeCloseTo(1 / (111.32 * Math.cos((43.5 * Math.PI) / 180)), 5)
    expect((Math.max(...lons) + Math.min(...lons)) / 2).toBeCloseTo(11, 9)
  })
})

describe('cells to GeoJSON', () => {
  it('keeps cell id and score on points ([lon, lat]) and squares', () => {
    const points = cellsToPoints(cells)
    expect(points.features[1]).toEqual({
      type: 'Feature',
      id: 'b',
      geometry: { type: 'Point', coordinates: [10.5, 44] },
      properties: { cell_id: 'b', score: 0.9 },
    })
    const squares = cellsToSquares(cells)
    expect(squares.features.map((f) => f.properties)).toEqual([
      { cell_id: 'a', score: 0.4 },
      { cell_id: 'b', score: 0.9 },
    ])
    expect(squares.features[0].geometry.type).toBe('Polygon')
  })
})

describe('sightings', () => {
  it('sums counts per cell across sources and species', () => {
    const merged = sightingsByCell([
      {
        counts: [
          { cell_id: 'a', source: 'gbif', license: 'CC-BY 4.0', count: 2 },
          { cell_id: 'a', source: 'inaturalist', license: 'CC-BY-NC 4.0', count: 1 },
        ],
      },
      { counts: [{ cell_id: 'b', source: 'gbif', license: 'CC-BY 4.0', count: 4 }] },
      { counts: [{ cell_id: 'a', source: 'gbif', license: 'CC-BY 4.0', count: 5 }] },
    ])
    expect(Object.fromEntries(merged)).toEqual({ a: 8, b: 4 })
  })

  it('places each count at its cell centre, never anywhere finer, and skips unknown cells', () => {
    const points = sightingsToPoints(
      new Map([
        ['b', 3],
        ['zzz', 7],
      ]),
      cells,
    )
    expect(points.features).toEqual([
      {
        type: 'Feature',
        geometry: { type: 'Point', coordinates: [10.5, 44] },
        properties: { cell_id: 'b', count: 3 },
      },
    ])
  })
})
