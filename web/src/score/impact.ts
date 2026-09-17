/**
 * Presentation of the API's factor breakdown for "why this score". The model
 * runs server-side; this only splits the score's shortfall between the
 * factors the API already returned.
 *
 * The API guarantees Π contribution = score, so in log space the shortfall is
 * additive: −ln score = Σ −ln contribution. Each factor's impact is its share
 * of that sum (see .gavin-root/docs/species-rules/README.md → Proposed
 * breakdown weighting). Impacts sum to 1 unless nothing holds the score back.
 */
import type { components } from '../api/schema'

export type FactorBreakdown = components['schemas']['FactorBreakdown']

export interface ExplainedFactor extends FactorBreakdown {
  /** Share of the score's shortfall caused by this factor, 0–1. */
  impact: number
}

export interface ScoreExplanation {
  /** In the API's order (gates, drivers, stoppers); never re-sorted. */
  factors: ExplainedFactor[]
  /** Keys of factors at zero, which alone zero the score. */
  blockedBy: string[]
  nothingHolding: boolean
}

const EPSILON = 1e-9

export function explainScore(factors: FactorBreakdown[]): ScoreExplanation {
  const blockedBy = factors.filter((f) => f.contribution < EPSILON).map((f) => f.key)

  if (blockedBy.length > 0) {
    return {
      factors: factors.map((f) => ({
        ...f,
        impact: blockedBy.includes(f.key) ? 1 / blockedBy.length : 0,
      })),
      blockedBy,
      nothingHolding: false,
    }
  }

  const shortfalls = factors.map((f) => Math.max(0, -Math.log(f.contribution)))
  const total = shortfalls.reduce((sum, s) => sum + s, 0)
  const nothingHolding = total < EPSILON

  return {
    factors: factors.map((f, i) => ({
      ...f,
      impact: nothingHolding ? 0 : shortfalls[i] / total,
    })),
    blockedBy: [],
    nothingHolding,
  }
}
