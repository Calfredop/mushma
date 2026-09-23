import { useTranslation } from 'react-i18next'
import { track } from '../analytics'
import { changeLanguage, LANGUAGES } from '../i18n'
import styles from './LanguageSwitcher.module.css'

export function LanguageSwitcher() {
  const { t, i18n } = useTranslation()

  return (
    <div role="group" aria-label={t('language.label')} className={styles.switcher}>
      {LANGUAGES.map((language) => (
        <button
          key={language}
          type="button"
          lang={language}
          aria-label={t(`language.${language}`)}
          aria-pressed={i18n.resolvedLanguage === language}
          className={styles.option}
          onClick={() => {
            track({ name: 'language-switch', data: { lang: language } })
            void changeLanguage(language)
          }}
        >
          {language.toUpperCase()}
        </button>
      ))}
    </div>
  )
}
