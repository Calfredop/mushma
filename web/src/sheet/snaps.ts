/**
 * The phone sheet's snap points and the arithmetic of dragging it. Positions are the sheet's
 * downward push in px (a CSS translateY): 0 shows all of it (full), larger shows less.
 */

export type Snap = 'peek' | 'half' | 'full'

/** Smallest to largest. */
export const SNAPS: readonly Snap[] = ['peek', 'half', 'full']

export interface SheetGeometry {
  /** The sheet's own height: all of it shows at full. */
  height: number
  /** How far the sheet is pushed down at each snap. */
  y: Record<Snap, number>
}

/** Half open is about this much of the screen. */
const HALF = 0.5
/** Half stays at least this far from peek and from full, so each snap is its own place. */
const MIN_GAP = 48
/** How far ahead a release is projected: a flick carries past the nearest snap. */
const PROJECTION_MS = 200
/** Past either end the sheet moves this much per px of drag. */
const RESISTANCE = 0.3

const clamp = (value: number, min: number, max: number) =>
  Math.min(Math.max(value, min), max)

/**
 * @param height the sheet's height, which is what shows at full
 * @param peek what shows at peek: the header and the home-indicator inset
 * @param viewport the screen's height
 */
export function sheetGeometry({
  height,
  peek,
  viewport,
}: {
  height: number
  peek: number
  viewport: number
}): SheetGeometry {
  const peekY = Math.max(0, height - peek)
  const half = clamp(Math.round(viewport * HALF), peek + MIN_GAP, height - MIN_GAP)
  const halfY = clamp(height - half, 0, peekY)
  return { height, y: { full: 0, half: halfY, peek: peekY } }
}

export const visibleAt = (snap: Snap, geometry: SheetGeometry) =>
  geometry.height - geometry.y[snap]

/** Where a release lands: the snap nearest to where the gesture was heading. */
export function snapAfterRelease(
  y: number,
  /** px per ms, positive downwards. */
  velocity: number,
  geometry: SheetGeometry,
): Snap {
  const projected = y + velocity * PROJECTION_MS
  return SNAPS.reduce((best, snap) =>
    Math.abs(geometry.y[snap] - projected) < Math.abs(geometry.y[best] - projected)
      ? snap
      : best,
  )
}

/** The finger's position, with resistance past either end. */
export function rubberBand(y: number, min: number, max: number): number {
  if (y < min) return min - (min - y) * RESISTANCE
  if (y > max) return max + (y - max) * RESISTANCE
  return y
}

/** The handle button cycles through the snaps; the arrow keys step and stop at the ends. */
export function stepSnap(snap: Snap, direction: 'up' | 'down' | 'cycle'): Snap {
  const index = SNAPS.indexOf(snap)
  if (direction === 'cycle') return SNAPS[(index + 1) % SNAPS.length]
  const next = clamp(index + (direction === 'up' ? 1 : -1), 0, SNAPS.length - 1)
  return SNAPS[next]
}

/** How far the map's bottom controls ride up: with the sheet, as far as half. */
export const liftFor = (y: number, geometry: SheetGeometry) =>
  Math.max(0, geometry.height - Math.max(y, geometry.y.half))

/** 0 at half or lower, 1 at full: the top of the map fades as the sheet covers it. */
export function coverFor(y: number, geometry: SheetGeometry): number {
  const span = geometry.y.half - geometry.y.full
  if (span <= 0) return y <= geometry.y.full ? 1 : 0
  return clamp((geometry.y.half - y) / span, 0, 1)
}
