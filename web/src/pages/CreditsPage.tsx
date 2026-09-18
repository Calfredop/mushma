import { useTranslation } from 'react-i18next'
import { ChevronIcon } from '../components/icons'
import { type Credit, DATA_CREDITS, SOFTWARE_CREDITS } from '../credits'
import styles from './CreditsPage.module.css'

interface Props {
  onBack: () => void
}

function CreditList({ credits }: { credits: Credit[] }) {
  const { t } = useTranslation()
  return (
    <ul className={styles.list}>
      {credits.map((credit) => (
        <li key={credit.name} className={styles.item}>
          <a href={credit.url} target="_blank" rel="noreferrer" className={styles.name}>
            {credit.name}
          </a>
          <span>{t(`credits.use.${credit.use}`)}</span>
          <span className={styles.license}>
            {t('credits.license', { license: credit.license })}
          </span>
        </li>
      ))}
    </ul>
  )
}

export function CreditsPage({ onBack }: Props) {
  const { t } = useTranslation()
  return (
    <div className={styles.page}>
      <div className={styles.inner}>
        <a
          href="/"
          className={styles.back}
          onClick={(event) => {
            event.preventDefault()
            onBack()
          }}
        >
          <ChevronIcon direction="left" />
          {t('nav.backToMap')}
        </a>
        <h1 className={styles.title}>{t('credits.title')}</h1>
        <p className={styles.intro}>{t('credits.intro')}</p>
        <p className={styles.note}>{t('credits.fixtureNote')}</p>

        <h2 className={styles.heading}>{t('credits.dataTitle')}</h2>
        <CreditList credits={DATA_CREDITS} />

        <h2 className={styles.heading}>{t('credits.softwareTitle')}</h2>
        <CreditList credits={SOFTWARE_CREDITS} />

        <h2 className={styles.heading}>{t('disclaimer.title')}</h2>
        <p>{t('disclaimer.body1')}</p>
        <p>{t('disclaimer.body2')}</p>
        <p>{t('disclaimer.body3')}</p>
      </div>
    </div>
  )
}
