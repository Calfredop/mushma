import { useTranslation } from 'react-i18next'
import { ChevronIcon } from '../components/icons'
import { PRIVACY_SECTIONS } from '../legal'
import styles from './CreditsPage.module.css'

interface Props {
  backHref: string
  onBack: () => void
  onDisclaimerClick: () => void
}

export function PrivacyPage({ backHref, onBack, onDisclaimerClick }: Props) {
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
        <h1 className={styles.title}>{t('privacy.title')}</h1>
        <p className={styles.intro}>{t('privacy.intro')}</p>

        <section>
          <h2 className={styles.heading}>{t('privacy.controller.title')}</h2>
          <p>{t('privacy.controller.body')}</p>
        </section>

        {PRIVACY_SECTIONS.map((key) => (
          <section key={key}>
            <h2 className={styles.heading}>{t(`privacy.sections.${key}.title`)}</h2>
            <p>{t(`privacy.sections.${key}.body`)}</p>
            {key === 'sightingsPrivacy' && (
              <p>
                {t('privacy.disclaimerNote')}{' '}
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
      </div>
    </div>
  )
}
