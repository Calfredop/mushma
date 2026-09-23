import { useTranslation } from 'react-i18next'
import { DISCLAIMER_SECTIONS } from '../disclaimer'
import styles from './DisclaimerText.module.css'

/** The disclaimer's sections under an h2 of the caller's, closing on the ASL check. */
export function DisclaimerText() {
  const { t } = useTranslation()
  return (
    <>
      {DISCLAIMER_SECTIONS.map((key) => (
        <section key={key} className={styles.section}>
          <h3 className={styles.heading}>{t(`disclaimer.sections.${key}.title`)}</h3>
          <p className={styles.body}>{t(`disclaimer.sections.${key}.body`)}</p>
        </section>
      ))}
      <p className={styles.callout}>{t('disclaimer.inspection')}</p>
    </>
  )
}
