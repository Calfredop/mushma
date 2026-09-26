import { describe, expect, it } from 'vitest'
import type { RegionOverview } from '../api/queries'
import { REGIONS } from '../regions'
import { hubRegions } from './hubRegions'

const row = (region: string, mean_score: number, good_share: number): RegionOverview => ({
  region,
  mean_score,
  good_share,
  updated_at: null,
})

describe('hubRegions', () => {
  it('lists every served region, named in the UI language, in alphabetical order', () => {
    const regions = [REGIONS.umbria, REGIONS.toscana]
    expect(hubRegions(undefined, 'it', regions).map((r) => r.region.slug)).toEqual([
      'toscana',
      'umbria',
    ])
  })

  it("adds a region's mean score and good share from the overview, by its API id", () => {
    const [toscana, umbria] = hubRegions([row('tuscany', 0.855, 0.89)], 'en', [
      REGIONS.toscana,
      REGIONS.umbria,
    ])
    expect(toscana).toMatchObject({ meanScore: 0.855, goodShare: 0.89 })
    // Served by the app, but not in today's overview (yet): no score, still listed.
    expect(umbria).toMatchObject({ meanScore: undefined, goodShare: undefined })
  })
})
