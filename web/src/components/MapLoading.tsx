import styles from './MapLoading.module.css'

interface Props {
  /** What the map is waiting for: "Carico l'indice delle condizioni…". */
  label: string
  className?: string
}

/**
 * Data on its way to the map: a spinner and what it waits for, at the centre of the part of the
 * map nothing covers. A load quicker than a beat never shows it.
 */
export function MapLoading({ label, className }: Props) {
  return (
    <p className={`${styles.loading} ${className ?? ''}`} role="status">
      <span className={styles.spinner} aria-hidden="true" />
      {label}
    </p>
  )
}
