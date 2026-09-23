import { readdirSync, readFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import it_ from '../i18n/locales/it.json'
import {
  DEFAULT_INDICATOR,
  FAMILIES,
  indicatorOf,
  isIndicator,
  layerOpacities,
  NEUTRAL_INDICATOR,
  OPACITY_CAP,
} from './indicators'

// Tests run from web/.
const SPECIES_RULES_DIR = resolve(process.cwd(), '../api/src/api/config/species')

/** Every enabled factor id in the species rule files: the chips the API can send. */
function enabledRuleFactorIds(): string[] {
  return readdirSync(SPECIES_RULES_DIR)
    .filter((file) => file.endsWith('.yaml'))
    .flatMap((file) =>
      // The `factors:` list only, up to the next top-level key (known_gaps have ids too).
      `\n${readFileSync(join(SPECIES_RULES_DIR, file), 'utf8').split('\nfactors:\n')[1] ?? ''}`
        .split(/\n[a-z_]+:/)[0]
        .split(/\n {2}- id: /)
        .slice(1)
        .filter((block) => !/\n {4}enabled: false/.test(block))
        .map((block) => block.split('\n')[0].trim()),
    )
}

describe('indicator colours', () => {
  it('has a colour for every factor label in the locales', () => {
    const missing = Object.keys(it_.factor).filter((id) => !isIndicator(id))
    expect(missing).toEqual([])
  })

  it('has a colour for every enabled factor in the species rules', () => {
    const ids = enabledRuleFactorIds()
    expect(ids).toEqual(expect.arrayContaining(['season', 'rain_trigger', 'hard_frost']))
    expect(ids.filter((id) => !isIndicator(id))).toEqual([])
  })

  it('gives every factor of a family its own colour, except a windowed alias', () => {
    const ids = Object.keys(it_.factor)
    for (const family of FAMILIES) {
      const colours = ids
        .filter((id) => indicatorOf(id).family === family)
        .map((id) => indicatorOf(id).color)
      expect(new Set(colours).size, family).toBe(colours.length)
    }
    expect(indicatorOf('water_balance_60d')).toEqual(indicatorOf('water_balance'))
    expect(indicatorOf('drought_14d')).toEqual(indicatorOf('drought'))
  })

  it('never uses Lago, which means selection', () => {
    const colours = Object.keys(it_.factor).map((id) =>
      indicatorOf(id).color.toUpperCase(),
    )
    expect(colours).not.toContain('#1F56A0')
  })

  it('falls back to a neutral colour for an unknown factor', () => {
    expect(isIndicator('tartufi')).toBe(false)
    expect(indicatorOf('tartufi')).toBe(NEUTRAL_INDICATOR)
    expect(indicatorOf('toString')).toBe(NEUTRAL_INDICATOR)
    expect(NEUTRAL_INDICATOR.family).toBe('other')
  })

  it('opens on an indicator the palette knows', () => {
    expect(isIndicator(DEFAULT_INDICATOR)).toBe(true)
  })
})

describe('layerOpacities', () => {
  const coverage = (opacities: number[]) =>
    1 - opacities.reduce((clear, a) => clear * (1 - a), 1)

  it('is the cap itself for one indicator', () => {
    expect(layerOpacities(1)).toEqual([OPACITY_CAP])
  })

  it('weighs every stacked indicator the same and covers at most the cap', () => {
    for (const count of [2, 3, 5]) {
      const opacities = layerOpacities(count)
      expect(coverage(opacities)).toBeCloseTo(OPACITY_CAP)
      // The weight a layer keeps after everything above it: all equal.
      const weights = opacities.map(
        (a, i) => a * opacities.slice(i + 1).reduce((clear, b) => clear * (1 - b), 1),
      )
      for (const weight of weights) expect(weight).toBeCloseTo(OPACITY_CAP / count)
    }
  })
})
