/** How the time views put history numbers into words and figures. Display only: every number
 * comes precomputed from the API. */
import type { RainStat, TemperatureStat } from '../api/queries'
import { intlLocale, type Language } from '../i18n'

/**
 * A season within ±15 % of its typical good days reads as usual. A wording judgement, not a
 * model rule: it only picks the label next to the numbers, which are always shown.
 */
export const VERDICT_BAND = 0.15

export type Verdict = 'better' | 'usual' | 'worse'

export function seasonVerdict(
  goodDays: number,
  typical: number | null | undefined,
): Verdict | null {
  if (typical === null || typical === undefined || typical <= 0) return null
  const ratio = goodDays / typical
  if (ratio >= 1 + VERDICT_BAND) return 'better'
  if (ratio <= 1 - VERDICT_BAND) return 'worse'
  return 'usual'
}

/** Rain as a percentage of its normal, or null without one. */
export function rainPercent(rain: RainStat | null | undefined): number | null {
  if (!rain || rain.normal_mm <= 0) return null
  return (rain.total_mm / rain.normal_mm) * 100
}

/** Degrees above (positive) or below normal. */
export function temperatureDelta(
  temperature: TemperatureStat | null | undefined,
): number | null {
  return temperature ? temperature.mean_c - temperature.normal_c : null
}

export function formatPercent(percent: number, language: Language): string {
  return new Intl.NumberFormat(intlLocale(language), {
    style: 'percent',
    maximumFractionDigits: 0,
  }).format(percent / 100)
}

export function formatDelta(value: number, language: Language): string {
  const rounded = Math.round(value * 10) / 10
  return new Intl.NumberFormat(intlLocale(language), {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
    signDisplay: rounded === 0 ? 'never' : 'always',
  }).format(rounded)
}

export function formatDays(value: number, language: Language): string {
  return new Intl.NumberFormat(intlLocale(language), { maximumFractionDigits: 0 }).format(
    value,
  )
}

export function formatMm(value: number, language: Language): string {
  return new Intl.NumberFormat(intlLocale(language), { maximumFractionDigits: 0 }).format(
    value,
  )
}
