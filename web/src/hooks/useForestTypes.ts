import { useTranslation } from 'react-i18next'
import type { HabitatShare } from '../api/queries'
import { intlLocale, type Language } from '../i18n'
import { forestMix } from '../score/habitats'

/** A cell's forest types in the visitor's language. */
export function useForestTypes() {
  const { t, i18n } = useTranslation()
  const locale = intlLocale(i18n.resolvedLanguage as Language)
  const percent = new Intl.NumberFormat(locale, {
    style: 'percent',
    maximumFractionDigits: 0,
  })
  const list = new Intl.ListFormat(locale, { type: 'conjunction' })

  /** A forest type's name; the API's own key for a type the locales don't know yet. */
  const name = (habitat: string) => {
    const key = `forest.types.${habitat}`
    return i18n.exists(key) ? t(key as 'forest.types.beech') : habitat
  }

  /** "faggeta 60%, castagneto 30% e altri tipi 10%"; null when the API sent no types. */
  const describe = (habitats: readonly HabitatShare[] | undefined): string | null => {
    const { main, rest } = forestMix(habitats)
    if (main.length === 0) return null
    const parts = main.map((h) =>
      t('forest.share', { type: name(h.habitat), share: percent.format(h.fraction) }),
    )
    if (Math.round(rest * 100) > 0) {
      parts.push(t('forest.rest', { share: percent.format(rest) }))
    }
    return list.format(parts)
  }

  return { name, describe }
}
