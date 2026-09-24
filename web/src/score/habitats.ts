import type { HabitatShare } from '../api/queries'

/** A forest type covering less of the cell's woods than this is folded into "other types". */
export const MIN_FOREST_SHARE = 0.1

export interface ForestMix {
  /** The types worth naming, largest first: those covering a tenth of the woods, and always the largest. */
  main: HabitatShare[]
  /** The share left to the smaller types; 0 when there are none. */
  rest: number
}

/**
 * A cell's forest types as the UI names them. The API sends them largest first. A cached or
 * older response may lack them, and then there is nothing to name.
 */
export function forestMix(habitats: readonly HabitatShare[] | undefined): ForestMix {
  const shares = habitats ?? []
  const main = shares.filter((h, i) => i === 0 || h.fraction >= MIN_FOREST_SHARE)
  const rest = shares.slice(main.length).reduce((sum, h) => sum + h.fraction, 0)
  return { main, rest }
}
