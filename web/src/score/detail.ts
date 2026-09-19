/**
 * Reading a factor's rule for the "why this score" details. The API sends each
 * rule's response as a trapezoid, `[zero_below, full_from, full_to, zero_above]`
 * with a null pair leaving a side open (api/src/api/config/species/README.md).
 * This turns it into the two facts a sentence needs: where the rule gives full
 * credit, and where it gives none.
 */
import type { components } from '../api/schema'

export type FactorRule = components['schemas']['FactorRule']
/** Four edges, `[zero_below, full_from, full_to, zero_above]`; the API sends them as a plain list. */
export type Trapezoid = readonly (number | null)[]

export type FullBand =
  | { kind: 'between'; from: number; to: number }
  | { kind: 'at'; value: number }
  | { kind: 'from'; from: number }
  | { kind: 'upTo'; to: number }

/** A ramp reaches zero at its edge; a zero-width ramp is a step that keeps the edge. */
export interface ZeroEdge {
  kind: 'atOrBelow' | 'below' | 'atOrAbove' | 'above'
  value: number
}

export interface Band {
  /** Null when the rule is open on both sides: full credit everywhere. */
  full: FullBand | null
  zero: ZeroEdge[]
}

export function describeBand(edges: Trapezoid): Band {
  const [a = null, b = null, c = null, d = null] = edges
  const hasLower = a !== null && b !== null
  const hasUpper = c !== null && d !== null

  let full: FullBand | null = null
  if (hasLower && hasUpper) {
    full = b === c ? { kind: 'at', value: b } : { kind: 'between', from: b, to: c }
  } else if (hasLower) {
    full = { kind: 'from', from: b }
  } else if (hasUpper) {
    full = { kind: 'upTo', to: c }
  }

  const zero: ZeroEdge[] = []
  if (hasLower) zero.push({ kind: a < b ? 'atOrBelow' : 'below', value: a })
  if (hasUpper) zero.push({ kind: c < d ? 'atOrAbove' : 'above', value: d })
  return { full, zero }
}

export const OP_SYMBOL = { lt: '<', lte: '≤', gt: '>', gte: '≥' } as const

const RAIN_VARIABLES = new Set(['precipitation_sum', 'rain_sum', 'water_balance'])

/** Whether the factor reads rain, directly or through the water balance. */
export function usesRain(rule: FactorRule | null | undefined): boolean {
  return rule?.variable != null && RAIN_VARIABLES.has(rule.variable)
}
