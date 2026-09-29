import { describe, expect, it } from 'vitest'
import { addDays } from '../time/days'
import {
  fittedChange,
  STEADY_BAND,
  TREND_DAYS,
  trendDirection,
  trendDomain,
  trendStart,
  type TrendPoint,
} from './trend'

const TODAY = '2026-09-29'

/** One point per day of the window, oldest first, ending today. */
function series(scores: number[]): TrendPoint[] {
  return scores.map((score, i) => ({
    date: addDays(TODAY, i - (scores.length - 1)),
    score,
  }))
}

describe('trendStart', () => {
  it('opens the window 14 days before today, so it holds 15 days', () => {
    expect(TREND_DAYS).toBe(15)
    expect(trendStart(TODAY)).toBe('2026-09-15')
  })
})

describe('fittedChange', () => {
  it('is the straight line through the days, measured across the whole window', () => {
    // +0.01 a day: 14 steps between the first day and today.
    const points = series(Array.from({ length: 15 }, (_, i) => 0.2 + 0.01 * i))
    expect(fittedChange(points)).toBeCloseTo(0.14)
  })

  it('reads a falling line as negative', () => {
    const points = series(Array.from({ length: 15 }, (_, i) => 0.8 - 0.02 * i))
    expect(fittedChange(points)).toBeCloseTo(-0.28)
  })

  it('keeps a missing day in its place rather than closing the gap', () => {
    const points = series(Array.from({ length: 15 }, (_, i) => 0.1 + 0.01 * i)).filter(
      (_, i) => i !== 3 && i !== 4,
    )
    expect(fittedChange(points)).toBeCloseTo(0.14)
  })

  it('is scaled to the full window even when only a few days are stored', () => {
    // Three days, +0.01 a day: a window's worth of that pace is +0.14.
    expect(fittedChange(series([0.3, 0.31, 0.32]))).toBeCloseTo(0.14)
  })

  it('has nothing to say about fewer than two days', () => {
    expect(fittedChange([])).toBeNull()
    expect(fittedChange(series([0.4]))).toBeNull()
  })

  it('is not pulled around by one spike as much as the last-minus-first difference is', () => {
    const scores = Array.from({ length: 15 }, () => 0.3)
    scores[0] = 0.9
    // The last day minus the first says -0.6; the fitted line only dips a little.
    expect(Math.abs(fittedChange(series(scores))!)).toBeLessThan(0.3)
  })
})

describe('trendDirection', () => {
  it.each([
    [0.2, 'up'],
    [STEADY_BAND, 'up'],
    [STEADY_BAND - 0.001, 'steady'],
    [0, 'steady'],
    [-(STEADY_BAND - 0.001), 'steady'],
    [-STEADY_BAND, 'down'],
    [-0.3, 'down'],
    [null, 'steady'],
  ] as const)('reads a change of %s as %s', (change, direction) => {
    expect(trendDirection(change)).toBe(direction)
  })

  it('treats a quarter of a score class as the smallest move worth an arrow', () => {
    expect(STEADY_BAND).toBe(0.05)
  })
})

describe('trendDomain', () => {
  it('pads a narrow range to the minimum span, centred on the data', () => {
    const [lo, hi] = trendDomain(series([0.4, 0.42, 0.44]))
    expect(hi - lo).toBeCloseTo(0.2)
    expect((lo + hi) / 2).toBeCloseTo(0.42)
  })

  it('keeps a wide range as it is', () => {
    expect(trendDomain(series([0.1, 0.7, 0.3]))).toEqual([0.1, 0.7])
  })

  it('never leaves 0-1, sliding the span inside instead', () => {
    const [lo, hi] = trendDomain(series([0, 0.01, 0.02]))
    expect(lo).toBe(0)
    expect(hi).toBeCloseTo(0.2)
    const [top0, top1] = trendDomain(series([1, 0.99]))
    expect(top1).toBe(1)
    expect(top0).toBeCloseTo(0.8)
  })

  it('gives an empty series the whole scale', () => {
    expect(trendDomain([])).toEqual([0, 1])
  })
})
