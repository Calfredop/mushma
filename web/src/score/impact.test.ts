import { describe, expect, it } from 'vitest'
import { explainScore } from './impact'

const factor = (key: string, value: number, contribution = value) => ({
  key,
  i18n_key: `factor.${key}`,
  value,
  contribution,
})

describe('explainScore', () => {
  it('splits the shortfall by each factor’s share of −ln(score), keeping API order', () => {
    // score = 0.5 * 0.25 = 0.125; −ln shares are ln2 : 2·ln2 → 1/3 : 2/3
    const result = explainScore([
      factor('season', 1),
      factor('rain_30d', 0.5),
      factor('frost', 0.25),
    ])
    expect(result.factors.map((f) => f.key)).toEqual(['season', 'rain_30d', 'frost'])
    expect(result.factors[0].impact).toBe(0)
    expect(result.factors[1].impact).toBeCloseTo(1 / 3)
    expect(result.factors[2].impact).toBeCloseTo(2 / 3)
    expect(result.blockedBy).toEqual([])
    expect(result.nothingHolding).toBe(false)
  })

  it('uses the contribution, not the raw value, so driver weights count', () => {
    // A driver at value 0.25 with weight share ½ contributes 0.5.
    const result = explainScore([factor('rain_trigger', 0.25, 0.5), factor('frost', 0.5)])
    expect(result.factors[0].impact).toBeCloseTo(0.5)
    expect(result.factors[1].impact).toBeCloseTo(0.5)
  })

  it('gives all the impact to factors at zero and names them as blockers', () => {
    const result = explainScore([
      factor('season', 0),
      factor('habitat', 0.4),
      factor('frost', 0),
    ])
    expect(result.factors.map((f) => f.impact)).toEqual([0.5, 0, 0.5])
    expect(result.blockedBy).toEqual(['season', 'frost'])
  })

  it('reports that nothing holds the score back when every factor is ideal', () => {
    const result = explainScore([factor('season', 1), factor('frost', 1)])
    expect(result.factors.map((f) => f.impact)).toEqual([0, 0])
    expect(result.nothingHolding).toBe(true)
  })

  it('handles an empty factor list', () => {
    expect(explainScore([])).toEqual({ factors: [], blockedBy: [], nothingHolding: true })
  })
})
