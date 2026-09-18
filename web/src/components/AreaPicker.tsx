import { useTranslation } from 'react-i18next'
import type { Comune } from '../api/queries'
import styles from './AreaPicker.module.css'

interface Props {
  comuni: Comune[] | undefined
  value: string | null
  onChange: (comune: string | null) => void
}

const REGION = ''

/** All of Tuscany, or one comune with woodland. */
export function AreaPicker({ comuni, value, onChange }: Props) {
  const { t } = useTranslation()
  return (
    <label className={styles.picker}>
      <span className={styles.label}>{t('area.label')}</span>
      <select
        className={styles.select}
        value={value ?? REGION}
        disabled={!comuni}
        onChange={(event) => onChange(event.target.value || null)}
      >
        <option value={REGION}>{t('area.region')}</option>
        {value && !comuni?.some((c) => c.code === value) && (
          <option value={value}>{value}</option>
        )}
        {comuni?.map((comune) => (
          <option key={comune.code} value={comune.code}>
            {comune.province
              ? t('area.comune', { name: comune.name, province: comune.province })
              : comune.name}
          </option>
        ))}
      </select>
    </label>
  )
}
