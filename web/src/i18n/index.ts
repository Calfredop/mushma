import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
import it from './locales/it.json'

export const LANGUAGES = ['it', 'en'] as const
export type Language = (typeof LANGUAGES)[number]
export const DEFAULT_LANGUAGE: Language = 'it'

const STORAGE_KEY = 'mushma.language'

function isLanguage(value: unknown): value is Language {
  return LANGUAGES.includes(value as Language)
}

/** The visitor's saved choice, else Italian (AGENTS.md: Italian is the default). */
export function initialLanguage(): Language {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (isLanguage(saved)) return saved
  } catch {
    // Storage can be blocked (private mode); the default still works.
  }
  return DEFAULT_LANGUAGE
}

export function currentLanguage(): Language {
  return isLanguage(i18n.resolvedLanguage) ? i18n.resolvedLanguage : DEFAULT_LANGUAGE
}

export async function changeLanguage(language: Language): Promise<void> {
  try {
    localStorage.setItem(STORAGE_KEY, language)
  } catch {
    // Not persisted, but the switch still applies to this visit.
  }
  await i18n.changeLanguage(language)
}

/** BCP 47 locale for Intl formatting. */
export function intlLocale(language: Language = currentLanguage()): string {
  return language === 'it' ? 'it-IT' : 'en-GB'
}

function syncDocument(language: string) {
  if (typeof document === 'undefined') return
  document.documentElement.lang = language
  document.title = i18n.t('app.documentTitle')
}

void i18n.use(initReactI18next).init({
  resources: { it: { translation: it }, en: { translation: en } },
  lng: initialLanguage(),
  supportedLngs: LANGUAGES,
  fallbackLng: DEFAULT_LANGUAGE,
  initAsync: false,
  returnNull: false,
  interpolation: { escapeValue: false },
})

i18n.on('languageChanged', syncDocument)
syncDocument(i18n.language)

export default i18n
