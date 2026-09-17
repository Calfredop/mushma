/**
 * The missing-key check: fails CI when a key exists in one locale but not the
 * other, is blank, or uses different {{variables}}, and when a factor the
 * species rules can return has no label.
 */
import { readdirSync, readFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { describe, expect, it as test } from 'vitest'
import { compareLocales, flattenKeys } from './keys'
import en from './locales/en.json'
import it from './locales/it.json'

// Tests run from web/.
const SPECIES_RULES_DIR = resolve(process.cwd(), '../.gavin-root/docs/species-rules')

describe('locales', () => {
  test('English has every Italian key, and nothing else', () => {
    expect(compareLocales(it, en)).toEqual({
      missing: [],
      extra: [],
      empty: [],
      placeholderMismatches: [],
    })
  })

  test('Italian has no blank strings', () => {
    expect(compareLocales(en, it).empty).toEqual([])
  })

  test('every factor i18n_key in the species rules has a label', () => {
    const ruleKeys = readdirSync(SPECIES_RULES_DIR)
      .filter((file) => file.endsWith('.yaml'))
      .flatMap((file) => [
        ...readFileSync(join(SPECIES_RULES_DIR, file), 'utf8').matchAll(
          /i18n_key:\s*(factor\.\w+)/g,
        ),
      ])
      .map((match) => match[1])
    expect(ruleKeys.length).toBeGreaterThan(0)

    const localeKeys = new Set(flattenKeys(it))
    expect([...new Set(ruleKeys)].filter((key) => !localeKeys.has(key)).sort()).toEqual(
      [],
    )
  })
})
