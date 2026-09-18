import { useTranslation } from 'react-i18next'
import type { Language } from '../i18n'
import { formatScore } from '../score/format'
import { scoreColor, scoreInk } from '../score/scale'
import styles from './ScoreChip.module.css'

interface Props {
  score: number
  size?: 'small' | 'large'
}

export function ScoreChip({ score, size = 'small' }: Props) {
  const { t, i18n } = useTranslation()
  const value = formatScore(score, i18n.resolvedLanguage as Language)
  return (
    <span
      className={styles.chip}
      data-size={size}
      style={{ background: scoreColor(score), color: scoreInk(score) }}
      role="img"
      aria-label={t('score.valueLabel', { value })}
    >
      {value}
    </span>
  )
}
