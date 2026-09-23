import { useTranslation } from 'react-i18next'
import { ChevronIcon } from '../components/icons'
import { TERMS_SECTIONS } from '../legal'
import styles from './CreditsPage.module.css'

interface Props {
  backHref: string
  onBack: () => void
  onDisclaimerClick: () => void
  onPrivacyClick: () => void
}

export function TermsPage({
  backHref,
  onBack,
  onDisclaimerClick,
  onPrivacyClick,
}: Props) {
  const { t } = useTranslation()
  return (
    <div className={styles.page}>
      <div className={styles.inner}>
        <a
          href={backHref}
          className={styles.back}
          onClick={(event) => {
            event.preventDefault()
            onBack()
          }}
        >
          <ChevronIcon direction="left" />
          {t('nav.backToMap')}
        </a>
        <h1 className={styles.title}>{t('terms.title')}</h1>
        <p className={styles.intro}>{t('terms.intro')}</p>

        {TERMS_SECTIONS.map((key) => (
          <section key={key}>
            <h2 className={styles.heading}>{t(`terms.sections.${key}.title`)}</h2>
            <p>{t(`terms.sections.${key}.body`)}</p>
            {key === 'userResponsibility' && (
              <p>
                {t('terms.disclaimerNote')}{' '}
                <button
                  type="button"
                  className={styles.inlineLink}
                  onClick={onDisclaimerClick}
                >
                  {t('nav.disclaimer')}
                </button>
              </p>
            )}
          </section>
        ))}

        <p>
          {t('terms.privacyNote')}{' '}
          <a
            href="/privacy"
            className={styles.inlineLink}
            onClick={(event) => {
              event.preventDefault()
              onPrivacyClick()
            }}
          >
            {t('nav.privacy')}
          </a>
        </p>
      </div>
    </div>
  )
}
