import { type CSSProperties, type ReactNode, useState } from 'react'
import { useTranslation } from 'react-i18next'
import type { FactorChip } from '../api/queries'
import { type Family, FAMILIES, indicatorOf } from '../score/indicators'
import { ChevronIcon } from './icons'
import styles from './IndicatorPanel.module.css'

interface Props {
  /** The species' factors, in breakdown order; undefined while they load or on a day without. */
  chips: FactorChip[] | undefined
  /** The ids that are on. */
  active: readonly string[]
  onToggle: (id: string) => void
  /** Said instead of the chips when there are none to show (loading, a day without factors). */
  note?: string
  showSightings?: boolean
}

/** Analysis mode's legend: every factor as a chip, grouped by family, and the opacity key. */
export function IndicatorPanel({
  chips,
  active,
  onToggle,
  note,
  showSightings = false,
}: Props) {
  const { t, i18n } = useTranslation()
  const [open, setOpen] = useState(true)

  // A chip is named like its row in "why"; a few factors share a label there and get their own.
  const label = (chip: FactorChip) => {
    const own = `analysis.name.${chip.id}`
    if (i18n.exists(own)) return t(own as 'analysis.name.hard_frost')
    return i18n.exists(chip.i18n_key) ? t(chip.i18n_key as 'factor.season') : chip.id
  }

  const groups = FAMILIES.map((family) => ({
    family,
    chips: (chips ?? []).filter((chip) => indicatorOf(chip.id).family === family),
  })).filter((group) => group.chips.length > 0)

  return (
    <section className={styles.panel} aria-labelledby="indicators-title">
      <div className={styles.header}>
        <h2 id="indicators-title" className={styles.title}>
          {t('analysis.title')}
        </h2>
        <button
          type="button"
          className={styles.fold}
          aria-expanded={open}
          aria-controls="indicators-body"
          aria-label={t(open ? 'analysis.collapse' : 'analysis.expand')}
          onClick={() => setOpen((value) => !value)}
        >
          <ChevronIcon direction={open ? 'down' : 'up'} />
        </button>
      </div>
      <div id="indicators-body" className={styles.body} hidden={!open}>
        {groups.length === 0 ? (
          note && <p className={styles.note}>{note}</p>
        ) : (
          <div className={styles.groups}>
            {groups.map((group) => (
              <FamilyGroup key={group.family} family={group.family}>
                {group.chips.map((chip) => (
                  <button
                    key={chip.id}
                    type="button"
                    className={styles.chip}
                    aria-pressed={active.includes(chip.id)}
                    style={{ '--chip': indicatorOf(chip.id).color } as CSSProperties}
                    onClick={() => onToggle(chip.id)}
                  >
                    <span className={styles.swatch} aria-hidden="true" />
                    {label(chip)}
                  </button>
                ))}
              </FamilyGroup>
            ))}
          </div>
        )}
        <div className={styles.key}>
          <span className={styles.ramp} aria-hidden="true" />
          <div className={styles.ends}>
            <span>{t('analysis.keyLow')}</span>
            <span>{t('analysis.keyHigh')} →</span>
          </div>
        </div>
        {showSightings && (
          <p className={styles.sightings}>
            <span className={styles.ring} aria-hidden="true" />
            {t('legend.sightings')}
          </p>
        )}
      </div>
    </section>
  )
}

function FamilyGroup({ family, children }: { family: Family; children: ReactNode }) {
  const { t } = useTranslation()
  const id = `indicator-family-${family}`
  return (
    <div role="group" aria-labelledby={id} className={styles.group}>
      <h3 id={id} className={styles.family}>
        {t(`analysis.family.${family}`)}
      </h3>
      <div className={styles.chips}>{children}</div>
    </div>
  )
}
