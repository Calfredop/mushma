import type { RegionOverview } from '../api/queries'
import { intlLocale, type Language } from '../i18n'
import { listRegions, type RegionDefinition } from '../regions'

/** A served region as the hub shows it: on the map and in the picker. */
export interface HubRegion {
  region: RegionDefinition
  /** Mean conditions score over the region's woodland cells; undefined until the overview has it. */
  meanScore: number | undefined
  /** Share of the region's woodland cells at or above the overview's good score. */
  goodShare: number | undefined
}

/** Every served region with the overview's numbers, by name in the UI language. */
export function hubRegions(
  overview: RegionOverview[] | undefined,
  language: Language,
  regions: RegionDefinition[] = listRegions(),
): HubRegion[] {
  const byId = new Map((overview ?? []).map((row) => [row.region, row]))
  const collator = new Intl.Collator(intlLocale(language))
  return regions
    .map((region) => {
      const row = byId.get(region.apiRegionId)
      return { region, meanScore: row?.mean_score, goodShare: row?.good_share }
    })
    .sort((a, b) => collator.compare(a.region.name[language], b.region.name[language]))
}
