import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'
import { SPECIES } from './state/urlState'
import { TAXA } from './taxa'

// Tests run from web/.
const SIGHTINGS_YAML = resolve(process.cwd(), '../api/src/api/config/sightings.yaml')

interface PinnedTaxon {
  scientificName: string
  rank: string
  gbifTaxonKey: number
  inaturalistTaxonId: number
}

/** The `species:` block of sightings.yaml, read line by line (no YAML dependency in web/). */
function pinnedTaxa(): Record<string, PinnedTaxon[]> {
  const taxa: Record<string, PinnedTaxon[]> = {}
  let inSpecies = false
  let current: PinnedTaxon[] | undefined
  for (const line of readFileSync(SIGHTINGS_YAML, 'utf8').split('\n')) {
    if (/^\S/.test(line) && !line.startsWith('#')) {
      inSpecies = line.startsWith('species:')
      continue
    }
    if (!inSpecies) continue
    const species = /^ {2}(\w+):\s*$/.exec(line)
    if (species) {
      current = taxa[species[1]] = []
      continue
    }
    const name = /^\s+- scientific_name:\s*([^#]+?)\s*(?:#.*)?$/.exec(line)
    if (name) {
      current!.push({
        scientificName: name[1],
        rank: 'species',
        gbifTaxonKey: 0,
        inaturalistTaxonId: 0,
      })
      continue
    }
    const taxon = current?.at(-1)
    const field = /^\s+(rank|gbif_taxon_key|inaturalist_taxon_id):\s*(\w+)/.exec(line)
    if (!taxon || !field) continue
    if (field[1] === 'rank') taxon.rank = field[2].toLowerCase()
    if (field[1] === 'gbif_taxon_key') taxon.gbifTaxonKey = Number(field[2])
    if (field[1] === 'inaturalist_taxon_id') taxon.inaturalistTaxonId = Number(field[2])
  }
  return taxa
}

describe('TAXA', () => {
  it('matches the taxa and ids pinned in the sightings ingest config', () => {
    const pinned = pinnedTaxa()
    expect(Object.keys(pinned).sort()).toEqual([...SPECIES].sort())
    for (const species of SPECIES) {
      expect(
        TAXA[species].map(
          ({ scientificName, rank, gbifTaxonKey, inaturalistTaxonId }) => ({
            scientificName,
            rank,
            gbifTaxonKey,
            inaturalistTaxonId,
          }),
        ),
      ).toEqual(pinned[species])
    }
  })

  it('gives every taxon a Wikidata item id', () => {
    for (const taxon of Object.values(TAXA).flat()) {
      expect(taxon.wikidata).toMatch(/^Q\d+$/)
    }
  })
})
