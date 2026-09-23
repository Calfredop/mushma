/**
 * The taxa behind each species the app scores, for the pages' JSON-LD (`seo/structuredData.ts`).
 * Pure data, like `./regions`: the build imports it.
 *
 * Mirrors the sightings ingest's taxon list, api/src/api/config/sightings.yaml. That file is the
 * source of truth for the names, ranks and GBIF and iNaturalist ids, and `taxa.test.ts` fails
 * when the two drift. The Wikidata items were matched on 2026-09-23 by GBIF key (P846), or, for
 * B. aereus, whose Wikidata item carries another GBIF key, by name and iNaturalist id (P3151).
 */
import type { Species } from './state/urlState.js'

export interface Taxon {
  scientificName: string
  rank: 'species' | 'genus'
  gbifTaxonKey: number
  inaturalistTaxonId: number
  /** Wikidata item id, e.g. `Q19740`. */
  wikidata: string
}

export const TAXA: Record<Species, Taxon[]> = {
  porcini: [
    {
      scientificName: 'Boletus edulis',
      rank: 'species',
      gbifTaxonKey: 5954958,
      inaturalistTaxonId: 48701,
      wikidata: 'Q19740',
    },
    {
      scientificName: 'Boletus aereus',
      rank: 'species',
      gbifTaxonKey: 8733688,
      inaturalistTaxonId: 333772,
      wikidata: 'Q757127',
    },
    {
      scientificName: 'Boletus reticulatus',
      rank: 'species',
      gbifTaxonKey: 5954691,
      inaturalistTaxonId: 350216,
      wikidata: 'Q26203726',
    },
    {
      scientificName: 'Boletus pinophilus',
      rank: 'species',
      gbifTaxonKey: 5954949,
      inaturalistTaxonId: 335942,
      wikidata: 'Q1415435',
    },
  ],
  ovoli: [
    {
      scientificName: 'Amanita caesarea',
      rank: 'species',
      gbifTaxonKey: 5240269,
      inaturalistTaxonId: 204588,
      wikidata: 'Q220662',
    },
  ],
  // The genus, as the ingest fetches it (sightings.yaml says why).
  gallinacci: [
    {
      scientificName: 'Cantharellus',
      rank: 'genus',
      gbifTaxonKey: 9623860,
      inaturalistTaxonId: 47348,
      wikidata: 'Q922335',
    },
  ],
}
