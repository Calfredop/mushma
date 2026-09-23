/**
 * Analysis mode's indicators: one colour per factor of the species rules, in families of related
 * hues, drawn on the map with the factor's 0–1 value as opacity. Derivation and checks (Lago, the
 * Machado CVD simulation, stacking): `.gavin-root/docs/visual-direction.md` → Analysis mode.
 */

/** In the order the chip panel groups them. */
export const FAMILIES = [
  'water',
  'warmth',
  'drying',
  'cold',
  'terrain',
  'season',
  'other',
] as const
export type Family = (typeof FAMILIES)[number]

export interface Indicator {
  family: Family
  color: string
}

const water = (color: string): Indicator => ({ family: 'water', color })
const warmth = (color: string): Indicator => ({ family: 'warmth', color })
const drying = (color: string): Indicator => ({ family: 'drying', color })
const cold = (color: string): Indicator => ({ family: 'cold', color })
const terrain = (color: string): Indicator => ({ family: 'terrain', color })

/**
 * Keyed by factor id, which is also the `factor.*` label key for most factors. A rule id with a
 * window in its name shares the colour of the concept it names (`water_balance_60d` is the water
 * balance), since a species never has both.
 */
const INDICATORS: Readonly<Record<string, Indicator>> = {
  rain_trigger: water('#268C9F'),
  rain_30d: water('#2FA8A3'),
  rain_frequency: water('#60BCD4'),
  water_balance: water('#92C8B2'),
  water_balance_60d: water('#92C8B2'),
  drought: water('#537B6D'),
  drought_14d: water('#537B6D'),
  soil_moisture: water('#599576'),
  early_season_wetness: water('#72ADB6'),
  waterlogging: water('#55866C'),

  air_temperature: warmth('#EF8332'),
  soil_temperature: warmth('#DA6210'),
  heat: warmth('#F8A650'),
  heat_spike: warmth('#CA3707'),

  drying: drying('#F4D03D'),
  evaporative_demand: drying('#E3B409'),

  frost: cold('#A476E6'),
  hard_frost: cold('#764DD6'),
  cold_nights: cold('#C593DF'),
  snow: cold('#C0BCFD'),

  habitat: terrain('#49553B'),
  altitude: terrain('#473C25'),
  slope: terrain('#756A3F'),
  sun_exposure: terrain('#9DA06C'),
  lithology: terrain('#645850'),
  soil_ph: terrain('#6C8970'),

  season: { family: 'season', color: '#5C0E59' },
}

/** A factor the palette doesn't know yet still draws, in a neutral grey. */
export const NEUTRAL_INDICATOR: Indicator = { family: 'other', color: '#7A827C' }

/** The indicator analysis mode turns on first. Every species has it. */
export const DEFAULT_INDICATOR = 'rain_trigger'

export function isIndicator(id: string): boolean {
  return Object.hasOwn(INDICATORS, id)
}

export function indicatorOf(id: string): Indicator {
  return isIndicator(id) ? INDICATORS[id] : NEUTRAL_INDICATOR
}

/** The most a fully favourable cell covers the map, however many indicators are on. */
export const OPACITY_CAP = 0.75

/**
 * Each layer's opacity at a value of 1, bottom to top, so every indicator weighs the same in the
 * blend (cap / n) and all of them together cover at most the cap. With one indicator on it is the
 * cap itself; a plain `value × cap` per layer would let the top one hide the rest.
 */
export function layerOpacities(count: number, cap = OPACITY_CAP): number[] {
  const share = cap / count
  return Array.from({ length: count }, (_, i) => share / (1 - (count - 1 - i) * share))
}
