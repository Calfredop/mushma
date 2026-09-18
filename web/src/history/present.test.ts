import { describe, expect, it } from 'vitest'
import {
  formatDays,
  formatDelta,
  formatPercent,
  rainPercent,
  seasonVerdict,
  temperatureDelta,
} from './present'

describe('seasonVerdict', () => {
  it('reads a season against the typical one, with a band either side', () => {
    expect(seasonVerdict(60, 50)).toBe('better')
    expect(seasonVerdict(55, 50)).toBe('usual')
    expect(seasonVerdict(45, 50)).toBe('usual')
    expect(seasonVerdict(40, 50)).toBe('worse')
  })

  it('has nothing to say without a typical season', () => {
    expect(seasonVerdict(40, null)).toBeNull()
    expect(seasonVerdict(0, 0)).toBeNull()
  })
})

describe('weather against normal', () => {
  it('turns rain into a share of normal and temperature into a difference', () => {
    expect(rainPercent({ total_mm: 87, normal_mm: 100 })).toBeCloseTo(87)
    expect(rainPercent({ total_mm: 5, normal_mm: 0 })).toBeNull()
    expect(rainPercent(null)).toBeNull()
    expect(temperatureDelta({ mean_c: 22.5, normal_c: 20.9 })).toBeCloseTo(1.6)
    expect(temperatureDelta(undefined)).toBeNull()
  })
})

describe('formats', () => {
  it('writes percentages, signed differences and whole days in the UI language', () => {
    expect(formatPercent(87.4, 'it')).toBe('87%')
    expect(formatPercent(115, 'en')).toBe('115%')
    expect(formatDelta(1.64, 'it')).toBe('+1,6')
    expect(formatDelta(-0.4, 'en')).toBe('-0.4')
    expect(formatDelta(0.01, 'en')).toBe('0.0')
    expect(formatDays(58.6, 'it')).toBe('59')
  })
})
