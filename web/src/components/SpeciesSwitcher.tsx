import { useTranslation } from 'react-i18next'
import { SPECIES_OR_COMBINED, type SpeciesOrCombined } from '../state/urlState'
import styles from './SpeciesSwitcher.module.css'

interface Props {
  value: SpeciesOrCombined
  onChange: (species: SpeciesOrCombined) => void
}

export function SpeciesSwitcher({ value, onChange }: Props) {
  const { t } = useTranslation()

  return (
    <div role="radiogroup" aria-label={t('species.label')} className={styles.switcher}>
      {SPECIES_OR_COMBINED.map((species) => (
        <button
          key={species}
          type="button"
          role="radio"
          aria-checked={value === species}
          className={styles.option}
          data-species={species}
          onClick={() => onChange(species)}
        >
          {t(`species.${species}.name`)}
        </button>
      ))}
    </div>
  )
}
