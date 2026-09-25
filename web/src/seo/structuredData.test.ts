import { describe, expect, it } from 'vitest'
import { DATA_CREDITS } from '../credits'
import itLocale from '../i18n/locales/it.json'
import { REGIONS } from '../regions'
import { ROUTES, type SiteRoute } from '../routes'
import { TAXA } from '../taxa'
import { type JsonLdNode, serializeJsonLd, structuredData } from './structuredData'

function route(path: string): SiteRoute {
  const found = ROUTES.find((r) => r.path === path)
  if (!found) throw new Error(`no route ${path}`)
  return found
}

function graph(path: string, lang: 'it' | 'en' = 'it'): JsonLdNode[] {
  return structuredData(route(path), lang)['@graph']
}

function nodesOfType(nodes: JsonLdNode[], type: string): JsonLdNode[] {
  return nodes.filter((node) => node['@type'] === type)
}

function onlyNode(nodes: JsonLdNode[], type: string): JsonLdNode {
  const found = nodesOfType(nodes, type)
  expect(found, `exactly one ${type}`).toHaveLength(1)
  return found[0]
}

/** Every `{ "@id": … }` object anywhere under `value`: a reference to another node. */
function references(value: unknown): string[] {
  if (Array.isArray(value)) return value.flatMap(references)
  if (value === null || typeof value !== 'object') return []
  const entries = Object.entries(value)
  if (entries.length === 1 && entries[0][0] === '@id') return [entries[0][1] as string]
  return entries.flatMap(([, v]) => references(v))
}

const MAP_PAGES = [
  '/toscana',
  '/toscana/porcini',
  '/toscana/ovoli',
  '/toscana/gallinacci',
]

describe('structuredData', () => {
  it('is one schema.org @graph per route, with unique ids and no dangling references', () => {
    for (const { path } of ROUTES) {
      const doc = structuredData(route(path))
      expect(doc['@context']).toBe('https://schema.org')
      const ids = doc['@graph'].map((node) => node['@id'])
      expect(ids.every((id) => typeof id === 'string' && id.startsWith('https://'))).toBe(
        true,
      )
      expect(new Set(ids).size).toBe(ids.length)
      for (const ref of references(doc['@graph'])) expect(ids).toContain(ref)
    }
  })

  it('names the site, its publisher and the app on every page', () => {
    for (const { path } of ROUTES) {
      const nodes = graph(path)
      expect(onlyNode(nodes, 'Organization')).toMatchObject({
        name: 'Mappa Funghi',
        url: 'https://mappafunghi.app/',
      })
      expect(onlyNode(nodes, 'WebSite')).toMatchObject({
        name: 'Mappa Funghi',
        url: 'https://mappafunghi.app/',
        inLanguage: 'it',
      })
      const app = onlyNode(nodes, 'WebApplication')
      expect(app).toMatchObject({
        name: 'Mappa Funghi',
        url: 'https://mappafunghi.app/',
        isAccessibleForFree: true,
        offers: { '@type': 'Offer', price: '0', priceCurrency: 'EUR' },
      })
      expect(app.featureList).toEqual(Object.values(itLocale.structuredData.features))
      expect(app.image).toBe('https://mappafunghi.app/og/hub.png')
    }
  })

  it('describes each page with its own URL, title and description', () => {
    for (const siteRoute of ROUTES) {
      const { path, seoKey, region: regionSlug } = siteRoute
      const page = onlyNode(graph(path), 'WebPage')
      const url =
        path === '/' ? 'https://mappafunghi.app/' : `https://mappafunghi.app${path}`
      if (regionSlug) {
        const region = REGIONS[regionSlug]
        const key = seoKey as 'region' | 'porcini' | 'ovoli' | 'gallinacci'
        const seo = region.copy.it.seo[key]
        expect(page).toMatchObject({
          url,
          name: seo.title,
          description: seo.description,
          inLanguage: 'it',
        })
      } else {
        const copy = itLocale.seo[seoKey as keyof typeof itLocale.seo]
        expect(page).toMatchObject({
          url,
          name: copy.title,
          description: copy.description,
          inLanguage: 'it',
        })
      }
    }
  })

  it('gives each map page a Dataset: the 0–1 conditions score, over the region, since 2016', () => {
    for (const path of MAP_PAGES) {
      const nodes = graph(path)
      const page = onlyNode(nodes, 'WebPage')
      const dataset = onlyNode(nodes, 'Dataset')
      expect(page.mainEntity).toEqual({ '@id': dataset['@id'] })
      expect(dataset).toMatchObject({
        url: `https://mappafunghi.app${path}`,
        temporalCoverage: '2016-01-01/..',
        isAccessibleForFree: true,
        variableMeasured: {
          '@type': 'PropertyValue',
          name: itLocale.structuredData.score.name,
          minValue: 0,
          maxValue: 1,
        },
      })
      // Google Dataset Search wants a description of 50–5,000 characters.
      expect((dataset.description as string).length).toBeGreaterThanOrEqual(50)
      expect(dataset.spatialCoverage).toEqual({
        '@id': onlyNode(nodes, 'AdministrativeArea')['@id'],
      })
      const sources = (dataset.isBasedOn as JsonLdNode[]).map((source) => source.url)
      expect(sources).toEqual(DATA_CREDITS.map((credit) => credit.url))
    }
  })

  it('says the score is an index, not a probability', () => {
    const score = onlyNode(graph('/toscana'), 'Dataset').variableMeasured as JsonLdNode
    expect(score.description).toContain('non è una probabilità')
    const scoreEn = onlyNode(graph('/toscana', 'en'), 'Dataset')
      .variableMeasured as JsonLdNode
    expect(scoreEn.description).toContain('not a probability')
  })

  it('places the region with a lat-lon GeoShape box and its Wikidata item', () => {
    expect(onlyNode(graph('/toscana/porcini'), 'AdministrativeArea')).toMatchObject({
      name: 'Toscana',
      alternateName: 'Tuscany',
      sameAs: ['https://www.wikidata.org/wiki/Q1273'],
      // schema.org boxes are "south west north east", latitude first.
      geo: { '@type': 'GeoShape', box: '42.23 9.68 44.48 12.38' },
      containedInPlace: {
        '@type': 'Country',
        name: 'Italia',
        sameAs: ['https://www.wikidata.org/wiki/Q38'],
      },
    })
  })

  it('links a species page to its taxa on GBIF, iNaturalist and Wikidata', () => {
    for (const species of ['porcini', 'ovoli', 'gallinacci'] as const) {
      const nodes = graph(`/toscana/${species}`)
      const taxa = nodesOfType(nodes, 'Taxon')
      expect(taxa.map((taxon) => taxon.name)).toEqual(
        TAXA[species].map((taxon) => taxon.scientificName),
      )
      for (const [i, taxon] of TAXA[species].entries()) {
        expect(taxa[i]).toMatchObject({
          taxonRank: taxon.rank,
          alternateName: itLocale.species[species].name,
          sameAs: [
            `https://www.gbif.org/species/${taxon.gbifTaxonKey}`,
            `https://www.inaturalist.org/taxa/${taxon.inaturalistTaxonId}`,
            `https://www.wikidata.org/wiki/${taxon.wikidata}`,
          ],
        })
      }
      const about = [onlyNode(nodes, 'AdministrativeArea'), ...taxa].map((node) => ({
        '@id': node['@id'],
      }))
      expect(onlyNode(nodes, 'WebPage').about).toEqual(about)
      expect(onlyNode(nodes, 'Dataset').about).toEqual(about.slice(1))
    }
  })

  it('covers every species of the region on the region page', () => {
    const names = nodesOfType(graph('/toscana'), 'Taxon').map((taxon) => taxon.name)
    expect(names).toEqual(
      [...TAXA.porcini, ...TAXA.ovoli, ...TAXA.gallinacci].map((t) => t.scientificName),
    )
  })

  it('ties each species Dataset into the region Dataset', () => {
    const regionDataset = onlyNode(graph('/toscana'), 'Dataset')
    const parts = regionDataset.hasPart as JsonLdNode[]
    expect(parts.map((part) => part.url)).toEqual([
      'https://mappafunghi.app/toscana/porcini',
      'https://mappafunghi.app/toscana/ovoli',
      'https://mappafunghi.app/toscana/gallinacci',
    ])
    const porcini = onlyNode(graph('/toscana/porcini'), 'Dataset')
    expect(porcini.isPartOf).toMatchObject({
      '@type': 'Dataset',
      '@id': regionDataset['@id'],
      url: 'https://mappafunghi.app/toscana',
    })
    expect(parts[0]['@id']).toBe(porcini['@id'])
  })

  it('gives species pages a two-step breadcrumb, and no other page one', () => {
    const crumbs = onlyNode(graph('/toscana/ovoli'), 'BreadcrumbList')
    expect(crumbs.itemListElement).toEqual([
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Toscana',
        item: 'https://mappafunghi.app/toscana',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Ovoli',
        item: 'https://mappafunghi.app/toscana/ovoli',
      },
    ])
    expect(onlyNode(graph('/toscana/ovoli'), 'WebPage').breadcrumb).toEqual({
      '@id': crumbs['@id'],
    })
    expect(nodesOfType(graph('/toscana'), 'BreadcrumbList')).toEqual([])
    expect(nodesOfType(graph('/credits'), 'BreadcrumbList')).toEqual([])
  })

  it('has the credits page cite the data sources, with no Dataset, place or taxa', () => {
    const nodes = graph('/credits')
    const page = onlyNode(nodes, 'WebPage')
    expect((page.citation as JsonLdNode[]).map((c) => c.url)).toEqual(
      DATA_CREDITS.map((credit) => credit.url),
    )
    expect(page.about).toEqual({ '@id': onlyNode(nodes, 'WebApplication')['@id'] })
    for (const type of ['Dataset', 'AdministrativeArea', 'Taxon']) {
      expect(nodesOfType(nodes, type)).toEqual([])
    }
  })

  it('follows the UI language', () => {
    const nodes = graph('/toscana/porcini', 'en')
    expect(onlyNode(nodes, 'WebPage')).toMatchObject({
      name: 'Porcini in Tuscany: conditions index | Mappa Funghi',
      inLanguage: 'en',
    })
    expect(onlyNode(nodes, 'Dataset').name).toBe(
      'Conditions index for porcini in Tuscany',
    )
    expect(onlyNode(nodes, 'AdministrativeArea')).toMatchObject({
      name: 'Tuscany',
      alternateName: 'Toscana',
    })
    // The ids name the thing, not the language: they stay the same.
    expect(graph('/toscana/porcini', 'en').map((n) => n['@id'])).toEqual(
      graph('/toscana/porcini').map((n) => n['@id']),
    )
  })
})

describe('serializeJsonLd', () => {
  it('round-trips through JSON.parse', () => {
    const doc = structuredData(route('/toscana'))
    expect(JSON.parse(serializeJsonLd(doc))).toEqual(doc)
  })

  it('never lets the copy close the <script> it sits in', () => {
    const doc = { '@context': 'https://schema.org', name: '</script><script>alert(1)' }
    const out = serializeJsonLd(doc)
    expect(out).not.toContain('<')
    expect(JSON.parse(out)).toEqual(doc)
  })
})
