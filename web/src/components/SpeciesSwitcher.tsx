import { useTranslation } from 'react-i18next'
import type { Species, SpeciesOrCombined } from '../state/urlState'
import styles from './SpeciesSwitcher.module.css'

interface Props {
  value: SpeciesOrCombined
  onChange: (species: SpeciesOrCombined) => void
  /** The region's offered species (combined is always available unless `noCombined`). */
  species: readonly Species[]
  /** Analysis mode has no combined score, so "Tutti" can't be picked there. */
  noCombined?: boolean
}

export function SpeciesSwitcher({ value, onChange, species, noCombined = false }: Props) {
  const { t } = useTranslation()
  const options: SpeciesOrCombined[] = ['combined', ...species]

  return (
    <div role="radiogroup" aria-label={t('species.label')} className={styles.switcher}>
      {options.map((option) => {
        const disabled = noCombined && option === 'combined'
        return (
          <button
            key={option}
            type="button"
            role="radio"
            aria-checked={value === option}
            className={styles.option}
            data-species={option}
            disabled={disabled}
            title={disabled ? t('analysis.noCombined') : undefined}
            onClick={() => onChange(option)}
          >
            {t(`species.${option}.name`)}
          </button>
        )
      })}
    </div>
  )
}
