/**
 * The trend line: a conditions score per day over the 15 days ending today, and which way it
 * is heading. The API serves the scores; this only reads their shape for the arrow and the chart.
 */
import { addDays, daysBetween, type IsoDate } from '../time/days'

/** The window: the 15 days ending today, today included (the API's `TREND_DAYS`). */
export const TREND_DAYS = 15

/** A fitted change smaller than this across the window reads as steady: a quarter of a score
 * class. In season a region's mean moves about 0.1 over 15 days (median, 2025–2026), so about a
 * quarter of windows come out steady. */
export const STEADY_BAND = 0.05

/** The sparkline's smallest y-span, so a small wiggle doesn't fill the whole height. */
const MIN_SPAN = 0.2

export interface TrendPoint {
  date: IsoDate
  score: number
}

export type TrendDirection = 'up' | 'down' | 'steady'

export function trendStart(today: IsoDate): IsoDate {
  return addDays(today, -(TREND_DAYS - 1))
}

/**
 * The least-squares line through the days, as its change across a whole window. Days are placed
 * by date, so a missing day keeps its gap. A straight fit rather than the last day minus the
 * first, so one odd day at either end doesn't flip the arrow.
 */
export function fittedChange(points: readonly TrendPoint[]): number | null {
  if (points.length < 2) return null
  const xs = points.map((p) => daysBetween(points[0].date, p.date))
  const meanX = xs.reduce((a, b) => a + b, 0) / xs.length
  const meanY = points.reduce((a, p) => a + p.score, 0) / points.length
  let num = 0
  let den = 0
  points.forEach((p, i) => {
    num += (xs[i] - meanX) * (p.score - meanY)
    den += (xs[i] - meanX) ** 2
  })
  if (den === 0) return null
  return (num / den) * (TREND_DAYS - 1)
}

export function trendDirection(change: number | null): TrendDirection {
  if (change === null || Math.abs(change) < STEADY_BAND) return 'steady'
  return change > 0 ? 'up' : 'down'
}

/** The y-range to draw: the data's own, widened to at least MIN_SPAN around its middle and kept
 * inside 0–1, so a steady line looks steady and a real move still shows. */
export function trendDomain(points: readonly TrendPoint[]): [number, number] {
  if (points.length === 0) return [0, 1]
  const scores = points.map((p) => p.score)
  let lo = Math.min(...scores)
  let hi = Math.max(...scores)
  if (hi - lo < MIN_SPAN) {
    const mid = (lo + hi) / 2
    lo = mid - MIN_SPAN / 2
    hi = mid + MIN_SPAN / 2
  }
  if (lo < 0) [lo, hi] = [0, hi - lo]
  if (hi > 1) [lo, hi] = [lo - (hi - 1), 1]
  return [Math.max(lo, 0), Math.min(hi, 1)]
}
