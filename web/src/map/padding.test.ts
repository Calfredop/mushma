import { describe, expect, it } from 'vitest'
import { inView, mergePadding } from './padding'

const phone = { width: 390, height: 844 }
// Species pill and cluster on top, the half sheet and time bar below.
const padding = { top: 72, bottom: 518, left: 16, right: 68 }

describe('inView', () => {
  it('is true for a point in the clear part of the map', () => {
    expect(inView({ x: 200, y: 200 }, phone, padding)).toBe(true)
  })

  it('is false for a point under the sheet, the pill or the cluster', () => {
    expect(inView({ x: 200, y: 600 }, phone, padding)).toBe(false)
    expect(inView({ x: 200, y: 40 }, phone, padding)).toBe(false)
    expect(inView({ x: 370, y: 200 }, phone, padding)).toBe(false)
  })

  it('keeps a margin inside the clear part', () => {
    expect(inView({ x: 200, y: 844 - 518 - 4 }, phone, padding)).toBe(false)
  })

  it('without padding, is the whole map', () => {
    expect(inView({ x: 5, y: 830 }, phone, undefined, 0)).toBe(true)
  })
})

describe('mergePadding', () => {
  it('keeps the larger inset on each side', () => {
    expect(mergePadding({ top: 80, bottom: 150, left: 48, right: 64 }, padding)).toEqual({
      top: 80,
      bottom: 518,
      left: 48,
      right: 68,
    })
    expect(mergePadding({ top: 1, bottom: 2, left: 3, right: 4 }, undefined)).toEqual({
      top: 1,
      bottom: 2,
      left: 3,
      right: 4,
    })
  })
})
