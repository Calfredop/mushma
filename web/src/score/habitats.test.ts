import { describe, expect, it } from 'vitest'
import { forestMix } from './habitats'

describe('forestMix', () => {
  it('keeps the types covering a tenth of the woods and sums up the rest', () => {
    const mix = forestMix([
      { habitat: 'beech', fraction: 0.6 },
      { habitat: 'chestnut', fraction: 0.3 },
      { habitat: 'fir_spruce', fraction: 0.06 },
      { habitat: 'macchia', fraction: 0.04 },
    ])
    expect(mix.main.map((h) => h.habitat)).toEqual(['beech', 'chestnut'])
    expect(mix.rest).toBeCloseTo(0.1)
  })

  it('always names the largest type, however mixed the woods', () => {
    const mix = forestMix([
      { habitat: 'beech', fraction: 0.09 },
      { habitat: 'chestnut', fraction: 0.08 },
    ])
    expect(mix.main.map((h) => h.habitat)).toEqual(['beech'])
    expect(mix.rest).toBeCloseTo(0.08)
  })

  it('has nothing to name when the API sent no forest types', () => {
    expect(forestMix(undefined)).toEqual({ main: [], rest: 0 })
    expect(forestMix([])).toEqual({ main: [], rest: 0 })
  })
})
