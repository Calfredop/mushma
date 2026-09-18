import { describe, expect, it } from 'vitest'
import { boundsAround, distanceKm, inBounds } from './distance'

describe('boundsAround', () => {
  it('orders the corners south-west then north-east whatever order the points come in', () => {
    // A point east of its cell: MapLibre would read [point, cell] as crossing the antimeridian.
    expect(boundsAround([11.9, 43.4], [11.85, 43.42])).toEqual([
      [11.85, 43.4],
      [11.9, 43.42],
    ])
    expect(boundsAround([10, 44], [11, 43])).toEqual([
      [10, 43],
      [11, 44],
    ])
  })
})

describe('distanceKm and inBounds', () => {
  it('measures great-circle distance and checks a box', () => {
    expect(distanceKm(43.85, 11.7333, 43.95, 11.7333)).toBeCloseTo(11.12, 1)
    const box: [[number, number], [number, number]] = [
      [9.68, 42.23],
      [12.38, 44.48],
    ]
    expect(inBounds(43.77, 11.25, box)).toBe(true)
    expect(inBounds(45.46, 9.19, box)).toBe(false)
  })
})
