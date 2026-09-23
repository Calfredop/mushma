/**
 * The disclaimer's sections, in reading order, each a `disclaimer.sections.<key>` title and
 * body in the locale copy. The dialog, the credits page and `/llms.txt` all render this list,
 * so the three never drift apart. Plain data: the build scripts import it too.
 */
export const DISCLAIMER_SECTIONS = [
  'conditions',
  'score',
  'terrain',
  'access',
  'noGuarantee',
  'judgement',
] as const

export type DisclaimerSection = (typeof DISCLAIMER_SECTIONS)[number]
