import { useTranslation } from 'react-i18next'
import type { SpeciesProfile, TaxonProfile } from '../api/queries'
import styles from './SpeciesBreakdown.module.css'

interface Props {
  /** Names the list for assistive technology. */
  label: string
  profiles: SpeciesProfile[]
  /** A species' or taxon's figure: its habitat fit, one season's good days. */
  value: (entry: SpeciesProfile | TaxonProfile) => number
  /** The figure a full bar stands for. */
  scale: number
  format: (value: number) => string
  /** Bar colour: the map's "good" colour for good days, ink for the woodland itself. */
  tone: 'good' | 'habitat'
}

function ranked<T>(entries: T[], value: (entry: T) => number): T[] {
  return [...entries].sort((a, b) => value(b) - value(a))
}

/**
 * The three species ranked by a figure, each broken down by taxon (the porcini keys). A species
 * with a single taxon keeps it on its own line, under its Latin name.
 */
export function SpeciesBreakdown({ label, profiles, value, scale, format, tone }: Props) {
  const { t } = useTranslation()

  const bar = (figure: number) => (
    <span className={styles.track} aria-hidden="true">
      <span
        className={styles.bar}
        style={{ width: `${Math.min(1, scale > 0 ? figure / scale : 0) * 100}%` }}
      />
    </span>
  )

  return (
    <ul className={styles.list} aria-label={label} data-tone={tone}>
      {ranked(profiles, value).map((profile) => {
        const name = t(`species.${profile.species}.name`)
        const only = profile.taxa.length === 1 ? profile.taxa[0] : null
        return (
          <li key={profile.species}>
            <div className={styles.row}>
              <span className={styles.name}>
                <span className={styles.common}>{name}</span>
                <span className={styles.latin}>
                  {only ? only.taxon : t(`species.${profile.species}.latin`)}
                </span>
              </span>
              {bar(value(profile))}
              <span className={styles.value}>{format(value(profile))}</span>
            </div>
            {!only && profile.taxa.length > 0 && (
              <ul className={styles.taxa} aria-label={name}>
                {ranked(profile.taxa, value).map((taxon) => (
                  <li key={taxon.key}>
                    <div className={styles.row} data-taxon>
                      <span className={styles.name}>
                        <span className={styles.latin}>{taxon.taxon}</span>
                      </span>
                      {bar(value(taxon))}
                      <span className={styles.value}>{format(value(taxon))}</span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </li>
        )
      })}
    </ul>
  )
}
