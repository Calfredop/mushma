/**
 * Schema.org JSON-LD for every indexed page, as one `@graph`: the site, its publisher and the
 * app on every page, then the page itself and, on a map page, the conditions-score Dataset, the
 * region and the taxa it covers, linked to GBIF, iNaturalist and Wikidata. Search engines read
 * it for rich results. LLM crawlers and answer engines read it to learn what a page covers and
 * what the score means (a 0–1 conditions index, never a probability) without running the map.
 *
 * Pure data like `./prerender`, which bakes the Italian graph into each prerendered page; the
 * client rebuilds it in the UI language as the route changes (`App.tsx` → `./head`).
 */
import { DATA_CREDITS } from '../credits.js'
import en from '../i18n/locales/en.json' with { type: 'json' }
import it from '../i18n/locales/it.json' with { type: 'json' }
import { DEFAULT_REGION_SLUG, REGIONS, type RegionDefinition } from '../regions.js'
import {
  ogImagePath,
  regionPath,
  SITE_URL,
  speciesPath,
  type SiteRoute,
} from '../routes.js'
import type { Species } from '../state/urlState.js'
import { TAXA, type Taxon } from '../taxa.js'

export type JsonLdLanguage = 'it' | 'en'
export type JsonLdNode = Record<string, unknown>

export interface JsonLdDocument {
  '@context': 'https://schema.org'
  '@graph': JsonLdNode[]
}

interface Copy {
  seo: Record<string, { title: string; description: string }>
  intro: Record<string, string>
  species: Record<Species, { name: string }>
  structuredData: {
    appDescription: string
    browserRequirements: string
    features: Record<string, string>
    dataset: Record<string, string>
    score: { name: string; description: string }
    method: string
    country: string
  }
}

const COPY: Record<JsonLdLanguage, Copy> = { it: it as Copy, en: en as Copy }

const SITE_NAME = 'Mappa Funghi'
const HOME_URL = `${SITE_URL}/`
const ORGANIZATION_ID = `${SITE_URL}/#organization`
const WEBSITE_ID = `${SITE_URL}/#website`
const APP_ID = `${SITE_URL}/#app`
/** The committed og:image cards (`scripts/generate-og-images.mjs`). */
const OG_IMAGE_SIZE = { width: 1200, height: 630 }
const ITALY_WIKIDATA = 'Q38'

function ref(id: string): JsonLdNode {
  return { '@id': id }
}

function wikidataUrl(id: string): string {
  return `https://www.wikidata.org/wiki/${id}`
}

function taxonId(taxon: Taxon): string {
  return `${SITE_URL}/#taxon-${taxon.scientificName.toLowerCase().replace(/\s+/g, '-')}`
}

function datasetId(path: string): string {
  return `${SITE_URL}${path}#dataset`
}

function placeId(region: RegionDefinition): string {
  return `${SITE_URL}${regionPath(region.slug)}#place`
}

function sources(): JsonLdNode[] {
  return DATA_CREDITS.map((credit) => ({
    '@type': 'CreativeWork',
    name: credit.name,
    url: credit.url,
  }))
}

/** The nodes every page shares: who publishes the site, the site, and the app. */
function siteNodes(copy: Copy, lang: JsonLdLanguage): JsonLdNode[] {
  return [
    {
      '@type': 'Organization',
      '@id': ORGANIZATION_ID,
      name: SITE_NAME,
      url: HOME_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/icons/icon-512.png`,
        width: 512,
        height: 512,
      },
    },
    {
      '@type': 'WebSite',
      '@id': WEBSITE_ID,
      name: SITE_NAME,
      url: HOME_URL,
      description: copy.structuredData.appDescription,
      inLanguage: lang,
      publisher: ref(ORGANIZATION_ID),
    },
    {
      '@type': 'WebApplication',
      '@id': APP_ID,
      name: SITE_NAME,
      url: `${SITE_URL}${regionPath(DEFAULT_REGION_SLUG)}`,
      description: copy.structuredData.appDescription,
      applicationCategory: 'UtilitiesApplication',
      operatingSystem: 'Any',
      browserRequirements: copy.structuredData.browserRequirements,
      inLanguage: ['it', 'en'],
      isAccessibleForFree: true,
      offers: { '@type': 'Offer', price: '0', priceCurrency: 'EUR' },
      featureList: Object.values(copy.structuredData.features),
      image: `${SITE_URL}${ogImagePath({ region: DEFAULT_REGION_SLUG, species: 'combined' })}`,
      publisher: ref(ORGANIZATION_ID),
    },
  ]
}

function placeNode(
  region: RegionDefinition,
  copy: Copy,
  lang: JsonLdLanguage,
): JsonLdNode {
  const [[west, south], [east, north]] = region.bounds
  return {
    '@type': 'AdministrativeArea',
    '@id': placeId(region),
    name: region.name[lang],
    alternateName: region.name[lang === 'it' ? 'en' : 'it'],
    sameAs: [wikidataUrl(region.wikidata)],
    // schema.org boxes are "south west north east", latitude first.
    geo: { '@type': 'GeoShape', box: `${south} ${west} ${north} ${east}` },
    containedInPlace: {
      '@type': 'Country',
      name: copy.structuredData.country,
      sameAs: [wikidataUrl(ITALY_WIKIDATA)],
    },
  }
}

function taxonNode(taxon: Taxon, species: Species, copy: Copy): JsonLdNode {
  return {
    '@type': 'Taxon',
    '@id': taxonId(taxon),
    name: taxon.scientificName,
    taxonRank: taxon.rank,
    alternateName: copy.species[species].name,
    sameAs: [
      `https://www.gbif.org/species/${taxon.gbifTaxonKey}`,
      `https://www.inaturalist.org/taxa/${taxon.inaturalistTaxonId}`,
      wikidataUrl(taxon.wikidata),
    ],
  }
}

/** A species Dataset as named from its region's Dataset, and the other way round. */
function datasetStub(path: string, name: string): JsonLdNode {
  return { '@type': 'Dataset', '@id': datasetId(path), name, url: `${SITE_URL}${path}` }
}

/** What a map page adds: its Dataset, the region, the taxa, and a breadcrumb for a species. */
function mapNodes(
  route: SiteRoute,
  region: RegionDefinition,
  copy: Copy,
  lang: JsonLdLanguage,
): { nodes: JsonLdNode[]; page: JsonLdNode } {
  const url = `${SITE_URL}${route.path}`
  const species = route.species === 'combined' || !route.species ? null : route.species
  const covered: Species[] = species ? [species] : region.species
  const taxa = covered.flatMap((s) => TAXA[s].map((taxon) => taxonNode(taxon, s, copy)))
  const taxonRefs = taxa.map((taxon) => ref(taxon['@id'] as string))
  const regionUrlPath = regionPath(region.slug)

  const dataset: JsonLdNode = {
    '@type': 'Dataset',
    '@id': datasetId(route.path),
    name: copy.structuredData.dataset[route.seoKey],
    description: copy.intro[route.seoKey],
    url,
    inLanguage: lang,
    creator: ref(ORGANIZATION_ID),
    isAccessibleForFree: true,
    spatialCoverage: ref(placeId(region)),
    temporalCoverage: `${region.historyStart}/..`,
    variableMeasured: {
      '@type': 'PropertyValue',
      name: copy.structuredData.score.name,
      description: copy.structuredData.score.description,
      minValue: 0,
      maxValue: 1,
    },
    measurementTechnique: copy.structuredData.method,
    about: taxonRefs,
    isBasedOn: sources(),
    ...(species
      ? {
          isPartOf: datasetStub(regionUrlPath, copy.structuredData.dataset.region),
        }
      : {
          hasPart: region.species.map((s) =>
            datasetStub(speciesPath(region.slug, s), copy.structuredData.dataset[s]),
          ),
        }),
  }

  const breadcrumb: JsonLdNode | null = species
    ? {
        '@type': 'BreadcrumbList',
        '@id': `${url}#breadcrumb`,
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: region.name[lang],
            item: `${SITE_URL}${regionUrlPath}`,
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: copy.species[species].name,
            item: url,
          },
        ],
      }
    : null

  return {
    nodes: [
      ...(breadcrumb ? [breadcrumb] : []),
      dataset,
      placeNode(region, copy, lang),
      ...taxa,
    ],
    page: {
      about: [ref(placeId(region)), ...taxonRefs],
      mainEntity: ref(dataset['@id'] as string),
      ...(breadcrumb ? { breadcrumb: ref(breadcrumb['@id'] as string) } : {}),
    },
  }
}

/** The page's JSON-LD graph, in `lang` (the prerendered pages are Italian). */
export function structuredData(
  route: SiteRoute,
  lang: JsonLdLanguage = 'it',
): JsonLdDocument {
  const copy = COPY[lang]
  const seo = copy.seo[route.seoKey]
  if (!seo) throw new Error(`No seo.${route.seoKey} copy for route ${route.path}`)
  const url = `${SITE_URL}${route.path}`
  const region = route.region ? REGIONS[route.region] : undefined
  const map = region ? mapNodes(route, region, copy, lang) : undefined

  const page: JsonLdNode = {
    '@type': 'WebPage',
    '@id': `${url}#webpage`,
    url,
    name: seo.title,
    description: seo.description,
    inLanguage: lang,
    isPartOf: ref(WEBSITE_ID),
    primaryImageOfPage: {
      '@type': 'ImageObject',
      url: `${SITE_URL}${ogImagePath(route)}`,
      ...OG_IMAGE_SIZE,
    },
    // A page with no map is one of the app's own (credits): it's about the app.
    ...(map ? map.page : { about: ref(APP_ID), citation: sources() }),
  }

  return {
    '@context': 'https://schema.org',
    '@graph': [...siteNodes(copy, lang), page, ...(map?.nodes ?? [])],
  }
}

/**
 * JSON for a `<script type="application/ld+json">`. Every `<` is escaped (`<`, still the
 * same JSON), so no string in the copy can close the script or open a comment.
 */
export function serializeJsonLd(doc: object): string {
  return JSON.stringify(doc).replace(/</g, '\\u003c')
}
