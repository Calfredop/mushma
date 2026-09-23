import { useTranslation } from 'react-i18next'
import { SPECIES_OR_COMBINED, type SpeciesOrCombined } from '../state/urlState'
import styles from './SpeciesSwitcher.module.css'

interface Props {
  value: SpeciesOrCombined
  onChange: (species: SpeciesOrCombined) => void
  /** Analysis mode has no combined score, so "Tutti" can't be picked there. */
  noCombined?: boolean
}

export function SpeciesSwitcher({ value, onChange, noCombined = false }: Props) {
  const { t } = useTranslation()

  return (
    <div role="radiogroup" aria-label={t('species.label')} className={styles.switcher}>
      {SPECIES_OR_COMBINED.map((species) => {
        const disabled = noCombined && species === 'combined'
        return (
          <button
            key={species}
            type="button"
            role="radio"
            aria-checked={value === species}
            className={styles.option}
            data-species={species}
            disabled={disabled}
            title={disabled ? t('analysis.noCombined') : undefined}
            onClick={() => onChange(species)}
          >
            {t(`species.${species}.name`)}
          </button>
        )
      })}
    </div>
  )
}
