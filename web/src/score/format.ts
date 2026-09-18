import { intlLocale, type Language } from '../i18n'

/** A 0–1 conditions score with two decimals in the UI language ("0,72" / "0.72"). */
export function formatScore(score: number, language: Language): string {
  return new Intl.NumberFormat(intlLocale(language), {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(score)
}
