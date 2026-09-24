import { type CSSProperties, type ReactNode, useState } from 'react'
import { useTranslation } from 'react-i18next'
import type { FactorChip } from '../api/queries'
import { useForestTypes } from '../hooks/useForestTypes'
import {
  forestColorOf,
  FOREST_GROUPS,
  forestHabitatsByGroup,
} from '../score/forestColors'
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
  /** A floating panel grouped by family (default), or a phone's one scrolling row of chips. */
  layout?: 'panel' | 'row'
  /** The Bosco toggle: each cell's forest type instead of, or alongside, the factor chips.
   * Doesn't depend on species or day, so it isn't one of `chips`. */
  forestOn?: boolean
  onToggleForest?: () => void
}

const FOREST_HABITATS_BY_GROUP = forestHabitatsByGroup()
/** One representative colour per group, for the toggle chip's swatch. */
const FOREST_GROUP_SWATCH = FOREST_GROUPS.map((group) =>
  forestColorOf(FOREST_HABITATS_BY_GROUP[group][0]),
)

/** Analysis mode's legend: every factor as a chip, grouped by family, and the opacity key. */
export function IndicatorPanel({
  chips,
  active,
  onToggle,
  note,
  showSightings = false,
  layout = 'panel',
  forestOn = false,
  onToggleForest = () => {},
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

  const chipButton = (chip: FactorChip) => (
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
  )

  const forestToggle = (
    <button
      type="button"
      className={styles.chip}
      aria-pressed={forestOn}
      onClick={onToggleForest}
    >
      <span className={styles.forestSwatch} aria-hidden="true">
        {FOREST_GROUP_SWATCH.map((color, i) => (
          <span key={i} style={{ background: color }} />
        ))}
      </span>
      {t('analysis.forest.toggle')}
    </button>
  )

  if (layout === 'row') {
    const ordered = groups.flatMap((group) => group.chips)
    return (
      <section className={styles.rowPanel} aria-labelledby="indicators-title">
        <h2 id="indicators-title" className="visually-hidden">
          {t('analysis.title')}
        </h2>
        <div className={styles.row} data-part="row">
          <p className={styles.keyChip}>
            {t('analysis.keyLowShort')}
            <span className={styles.ramp} aria-hidden="true" />
            {t('analysis.keyHighShort')}
          </p>
          {forestToggle}
          {ordered.length === 0
            ? note && <p className={styles.keyChip}>{note}</p>
            : ordered.map(chipButton)}
          {showSightings && (
            <p className={styles.keyChip}>
              <span className={styles.ring} aria-hidden="true" />
              {t('legend.sightings')}
            </p>
          )}
        </div>
      </section>
    )
  }

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
        <div className={styles.forestRow}>{forestToggle}</div>
        {forestOn && <ForestLegend />}
        {groups.length === 0 ? (
          note && <p className={styles.note}>{note}</p>
        ) : (
          <div className={styles.groups}>
            {groups.map((group) => (
              <FamilyGroup key={group.family} family={group.family}>
                {group.chips.map(chipButton)}
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

/** The Bosco toggle's legend: every forest type, by broad group. Reference swatches, not
 * buttons -- the layer is one on/off, not 14 toggles. */
function ForestLegend() {
  const { t } = useTranslation()
  const { name } = useForestTypes()
  return (
    <div className={styles.groups}>
      {FOREST_GROUPS.map((group) => (
        <div
          key={group}
          role="group"
          aria-labelledby={`forest-group-${group}`}
          className={styles.group}
        >
          <h3 id={`forest-group-${group}`} className={styles.family}>
            {t(`forest.group.${group}`)}
          </h3>
          <div className={styles.chips}>
            {FOREST_HABITATS_BY_GROUP[group].map((habitat) => (
              <span
                key={habitat}
                className={styles.chip}
                style={{ '--chip': forestColorOf(habitat) } as CSSProperties}
              >
                <span
                  className={`${styles.swatch} ${styles.filled}`}
                  aria-hidden="true"
                />
                {name(habitat)}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
