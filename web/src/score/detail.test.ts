import { describe, expect, it } from 'vitest'
import { describeBand, usesRain, usesTerrain } from './detail'

describe('describeBand', () => {
  it('reads a full trapezoid as a plateau with a zero edge on each side', () => {
    expect(describeBand([200, 700, 1600, 1900])).toEqual({
      full: { kind: 'between', from: 700, to: 1600 },
      zero: [
        { kind: 'atOrBelow', value: 200 },
        { kind: 'atOrAbove', value: 1900 },
      ],
    })
  })

  it('reads a rule open above as "from" its plateau, zero at and below its lower edge', () => {
    expect(describeBand([10, 30, null, null])).toEqual({
      full: { kind: 'from', from: 30 },
      zero: [{ kind: 'atOrBelow', value: 10 }],
    })
  })

  it('reads a rule open below as "up to" its plateau, zero at and above its upper edge', () => {
    expect(describeBand([null, null, 1, 3])).toEqual({
      full: { kind: 'upTo', to: 1 },
      zero: [{ kind: 'atOrAbove', value: 3 }],
    })
  })

  it('reads a zero-width ramp as a step that keeps its edge: zero strictly beyond it', () => {
    expect(describeBand([null, null, 1, 1])).toEqual({
      full: { kind: 'upTo', to: 1 },
      zero: [{ kind: 'above', value: 1 }],
    })
    expect(describeBand([5, 5, null, null])).toEqual({
      full: { kind: 'from', from: 5 },
      zero: [{ kind: 'below', value: 5 }],
    })
  })

  it('reads a plateau of one point as that point', () => {
    expect(describeBand([3, 4, 4, 6]).full).toEqual({ kind: 'at', value: 4 })
  })

  it('has nothing to say about a rule that is always fully open', () => {
    expect(describeBand([null, null, null, null])).toEqual({ full: null, zero: [] })
  })
})

describe('usesRain', () => {
  it('is true for the rain variables and the water balance, which counts rain', () => {
    for (const variable of ['precipitation_sum', 'rain_sum', 'water_balance']) {
      expect(usesRain({ kind: 'window_aggregate', variable })).toBe(true)
    }
  })

  it('is false for other variables, and for a factor without a rule', () => {
    expect(usesRain({ kind: 'window_aggregate', variable: 'temperature_2m_mean' })).toBe(
      false,
    )
    expect(usesRain({ kind: 'season_window' })).toBe(false)
    expect(usesRain(null)).toBe(false)
    expect(usesRain(undefined)).toBe(false)
  })
})

describe('usesTerrain', () => {
  it('is true for what the slope microclimate adjusts, and for a lag on the growth clock', () => {
    for (const variable of [
      'temperature_2m_mean',
      'temperature_2m_max',
      'soil_temperature_0_to_7cm_mean',
      'et0_fao_evapotranspiration',
      'water_balance',
      'sun_exposure_pct',
    ]) {
      expect(usesTerrain({ kind: 'window_aggregate', variable })).toBe(true)
    }
    expect(
      usesTerrain({
        kind: 'rain_event',
        variable: 'precipitation_sum',
        lag_unit: 'growth_days',
      }),
    ).toBe(true)
  })

  it('is false for what it leaves alone', () => {
    expect(
      usesTerrain({ kind: 'window_aggregate', variable: 'temperature_2m_min' }),
    ).toBe(false)
    expect(
      usesTerrain({
        kind: 'rain_event',
        variable: 'precipitation_sum',
        lag_unit: 'days',
      }),
    ).toBe(false)
    expect(usesTerrain({ kind: 'static_band', variable: 'elevation_m' })).toBe(false)
    expect(usesTerrain(null)).toBe(false)
  })
})
