import { describe, expect, it } from 'vitest'
import { distanceToPolygonKm, inPolygon } from './polygon'

// A 1° square with a 0.5° hole, and a separate island east of it.
const square: GeoJSON.Polygon = {
  type: 'Polygon',
  coordinates: [
    [
      [10, 43],
      [11, 43],
      [11, 44],
      [10, 44],
      [10, 43],
    ],
    [
      [10.25, 43.25],
      [10.75, 43.25],
      [10.75, 43.75],
      [10.25, 43.75],
      [10.25, 43.25],
    ],
  ],
}
const withIsland: GeoJSON.MultiPolygon = {
  type: 'MultiPolygon',
  coordinates: [
    square.coordinates,
    [
      [
        [12, 43],
        [12.1, 43],
        [12.1, 43.1],
        [12, 43.1],
        [12, 43],
      ],
    ],
  ],
}

describe('inPolygon', () => {
  it('holds a point inside the outer ring and outside its holes', () => {
    expect(inPolygon(43.1, 10.1, square)).toBe(true)
    expect(inPolygon(43.5, 10.5, square)).toBe(false) // in the hole
    expect(inPolygon(43.5, 11.5, square)).toBe(false)
  })

  it('holds a point in any part of a multipolygon', () => {
    expect(inPolygon(43.05, 12.05, withIsland)).toBe(true)
    expect(inPolygon(43.1, 10.1, withIsland)).toBe(true)
    expect(inPolygon(43.05, 11.5, withIsland)).toBe(false)
  })
})

describe('distanceToPolygonKm', () => {
  it('is zero inside and the distance to the nearest edge outside', () => {
    expect(distanceToPolygonKm(43.1, 10.1, square)).toBe(0)
    // 0.01° of latitude south of the square: ~1.1 km.
    expect(distanceToPolygonKm(42.99, 10.5, square)).toBeCloseTo(1.11, 1)
    // In the hole, 0.05° of longitude at 43.5° N from its west edge: ~4.0 km.
    expect(distanceToPolygonKm(43.5, 10.3, square)).toBeCloseTo(4.03, 1)
  })

  it('measures to the nearest part of a multipolygon', () => {
    // 0.1° of longitude west of the island, 0.9° east of the square.
    expect(distanceToPolygonKm(43.05, 11.9, withIsland)).toBeCloseTo(8.1, 0)
  })
})
