/**
 * The "Porcino" conditions-score scale: five stepped classes whose lightness
 * drops strictly from low to high, so the order survives colour-vision
 * deficiencies and bright sun. Derivation and checks:
 * `.gavin-root/docs/visual-direction.md`.
 */

const INK_DARK = '#1C211D'
const INK_LIGHT = '#FFFFFF'

export interface ScoreClass {
  /** Inclusive lower bound of the class. */
  min: number
  color: string
  /** Text colour that stays legible on `color`. */
  ink: string
}

export const SCORE_CLASSES: readonly ScoreClass[] = [
  { min: 0, color: '#F7F0C6', ink: INK_DARK },
  { min: 0.2, color: '#F0C967', ink: INK_DARK },
  { min: 0.4, color: '#E68C2C', ink: INK_DARK },
  { min: 0.6, color: '#B34F2A', ink: INK_LIGHT },
  { min: 0.8, color: '#652D1F', ink: INK_LIGHT },
]

export function scoreClass(score: number): number {
  if (!(score > 0)) return 0
  for (let i = SCORE_CLASSES.length - 1; i > 0; i--) {
    if (score >= SCORE_CLASSES[i].min) return i
  }
  return 0
}

export function scoreColor(score: number): string {
  return SCORE_CLASSES[scoreClass(score)].color
}

export function scoreInk(score: number): string {
  return SCORE_CLASSES[scoreClass(score)].ink
}

/** A MapLibre `step` expression colouring `input` with the same class breaks. */
export function scoreStepExpression(input: unknown[]): unknown[] {
  const [first, ...rest] = SCORE_CLASSES
  return ['step', input, first.color, ...rest.flatMap((c) => [c.min, c.color])]
}

/**
 * A season on the map: a woodland cell's good days (score ≥ the history's good-day threshold),
 * on the same five colours so darker still means better. Breaks from the scored seasons: in 2025
 * a porcini cell had a median of 59 good days (quartiles 41 and 72).
 */
export const GOOD_DAYS_CLASSES: readonly ScoreClass[] = SCORE_CLASSES.map((c, i) => ({
  ...c,
  min: [0, 10, 30, 60, 90][i],
}))

export function goodDaysClass(days: number): number {
  for (let i = GOOD_DAYS_CLASSES.length - 1; i > 0; i--) {
    if (days >= GOOD_DAYS_CLASSES[i].min) return i
  }
  return 0
}

export function goodDaysStepExpression(input: unknown[]): unknown[] {
  const [first, ...rest] = GOOD_DAYS_CLASSES
  return ['step', input, first.color, ...rest.flatMap((c) => [c.min, c.color])]
}
