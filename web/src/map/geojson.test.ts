import { describe, expect, it } from 'vitest'
import {
  cellSquare,
  cellsToPoints,
  cellsToSquares,
  factorCellsToPoints,
  factorCellsToSquares,
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

describe('factor cells to GeoJSON', () => {
  const ids = ['season', 'rain_trigger', 'cold_nights']
  const factorCells = [
    { cell_id: 'a', lon: 11, lat: 43.5, values: [1, 0.25, null] },
    { cell_id: 'b', lon: 10.5, lat: 44, values: [0, null, 0.5] },
  ]

  it('puts each factor value under its id, and leaves out the ones the winner lacks', () => {
    const points = factorCellsToPoints(factorCells, ids)
    expect(points.features[0]).toEqual({
      type: 'Feature',
      id: 'a',
      geometry: { type: 'Point', coordinates: [11, 43.5] },
      properties: { cell_id: 'a', season: 1, rain_trigger: 0.25 },
    })
    expect(points.features[1].properties).toEqual({
      cell_id: 'b',
      season: 0,
      cold_nights: 0.5,
    })
  })

  it('draws the same properties on the squares', () => {
    const squares = factorCellsToSquares(factorCells, ids)
    expect(squares.features[1].geometry.type).toBe('Polygon')
    expect(squares.features.map((f) => f.properties)).toEqual(
      factorCellsToPoints(factorCells, ids).features.map((f) => f.properties),
    )
  })

  it('merges in a cell forest type by cell_id, when given one', () => {
    const forestTypes = new Map([['a', 'beech']])
    const points = factorCellsToPoints(factorCells, ids, forestTypes)
    expect(points.features[0].properties).toEqual({
      cell_id: 'a',
      season: 1,
      rain_trigger: 0.25,
      forest_type: 'beech',
    })
    // Cell b has no entry in the map: no forest_type property, same as a factor the winner lacks.
    expect(points.features[1].properties).not.toHaveProperty('forest_type')
  })

  it('leaves forest_type out when no lookup is given', () => {
    const points = factorCellsToPoints(factorCells, ids)
    expect(points.features[0].properties).not.toHaveProperty('forest_type')
  })
})
