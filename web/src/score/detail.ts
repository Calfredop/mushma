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

/**
 * What the slope microclimate (api `config/model.yaml`) moves: the day's temperatures and drying
 * (so the water balance), and the sun ratio itself.
 */
const TERRAIN_VARIABLES = new Set([
  'temperature_2m_mean',
  'temperature_2m_max',
  'soil_temperature_0_to_7cm_mean',
  'et0_fao_evapotranspiration',
  'water_balance',
  'sun_exposure_pct',
])

/** Whether the factor reads rain, directly or through the water balance. */
export function usesRain(rule: FactorRule | null | undefined): boolean {
  return rule?.variable != null && RAIN_VARIABLES.has(rule.variable)
}

/**
 * Whether a factor reads weather adjusted to the cell's slope, or counts its lag on the growth
 * clock, whose pace reads the adjusted soil temperature.
 */
export function usesTerrain(rule: FactorRule | null | undefined): boolean {
  if (rule?.lag_unit === 'growth_days') return true
  return rule?.variable != null && TERRAIN_VARIABLES.has(rule.variable)
}
