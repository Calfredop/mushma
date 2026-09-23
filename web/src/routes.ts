/**
 * The canonical route list: region/species paths from the region registry, plus the static
 * pages. It drives client routing, the sitemap and the prerendered per-route heads (build
 * scripts import it directly, so — like `./regions` — it must stay free of `import.meta.env`).
 */
import {
  DEFAULT_REGION_SLUG,
  findRegion,
  REGIONS,
  type RegionDefinition,
} from './regions.js'
import {
  isSpeciesOrCombined,
  SPECIES,
  type Species,
  type SpeciesOrCombined,
} from './state/urlState.js'

export const SITE_URL = 'https://mappafunghi.app'

export const STATIC_PAGES = ['credits'] as const
export type StaticPage = (typeof STATIC_PAGES)[number]

export type RouteMatch =
  | { kind: 'static'; page: StaticPage }
  | { kind: 'region'; region: RegionDefinition; species: SpeciesOrCombined }
  | { kind: 'not-found' }

export function regionPath(regionSlug: string): string {
  return `/${regionSlug}`
}

export function speciesPath(regionSlug: string, species: Species): string {
  return `/${regionSlug}/${species}`
}

function isStaticPage(segment: string): segment is StaticPage {
  return (STATIC_PAGES as readonly string[]).includes(segment)
}

/** Parses a pathname alone (no query string) into what it points at. */
export function matchPath(pathname: string): RouteMatch {
  const segments = pathname.split('/').filter(Boolean)
  if (segments.length === 0 || segments.length > 2) return { kind: 'not-found' }

  const [first, second] = segments
  if (segments.length === 1 && isStaticPage(first)) return { kind: 'static', page: first }

  const region = findRegion(first)
  if (!region) return { kind: 'not-found' }
  if (segments.length === 1) return { kind: 'region', region, species: 'combined' }

  if (
    !SPECIES.includes(second as Species) ||
    !region.species.includes(second as Species)
  ) {
    return { kind: 'not-found' }
  }
  return { kind: 'region', region, species: second as Species }
}

export interface ResolvedLocation {
  match: RouteMatch
  /** Set when the URL needs a client `replaceState` to reach this canonical form. */
  redirectTo?: string
}

/**
 * Reads the pathname and query string as loaded and returns what they point at, plus — for
 * the bare root or a legacy `?species=` link — the canonical URL to `replaceState` to.
 */
export function resolveLocation(pathname: string, search: string): ResolvedLocation {
  const params = new URLSearchParams(search)
  const hadSpeciesParam = params.has('species')
  const legacySpecies = params.get('species')
  params.delete('species')
  const query = params.toString()
  const suffix = query ? `?${query}` : ''

  if (pathname === '/') {
    const region = REGIONS[DEFAULT_REGION_SLUG]
    const species: SpeciesOrCombined = isSpeciesOrCombined(legacySpecies)
      ? legacySpecies
      : 'combined'
    const path =
      species === 'combined' ? regionPath(region.slug) : speciesPath(region.slug, species)
    return { match: { kind: 'region', region, species }, redirectTo: `${path}${suffix}` }
  }

  const match = matchPath(pathname)
  if (hadSpeciesParam) return { match, redirectTo: `${pathname}${suffix}` }
  return { match }
}

export interface SiteRoute {
  path: string
  region: string | null
  species: SpeciesOrCombined | null
  /** The `seo.<key>` entry in the locale files (`./seo/prerender.ts`). */
  seoKey: string
}

export const ROUTES: SiteRoute[] = [
  ...Object.values(REGIONS).flatMap((region) => [
    {
      path: regionPath(region.slug),
      region: region.slug,
      species: 'combined' as const,
      seoKey: 'region',
    },
    ...region.species.map((species) => ({
      path: speciesPath(region.slug, species),
      region: region.slug,
      species,
      seoKey: species,
    })),
  ]),
  ...STATIC_PAGES.map((page) => ({
    path: `/${page}`,
    region: null,
    species: null,
    seoKey: page,
  })),
]
