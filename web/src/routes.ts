/**
 * The canonical route list: hub, region/species paths from the region registry, plus the static
 * pages. It drives client routing, the sitemap and the prerendered per-route heads (build
 * scripts import it directly, so — like `./regions` — it must stay free of `import.meta.env`).
 */
import {
  DEFAULT_REGION_SLUG,
  findRegion,
  listRegions,
  pwaHubRedirectSlug,
  REGIONS,
  type RegionDefinition,
} from './regions/index.js'
import {
  isSpeciesOrCombined,
  SPECIES,
  type Species,
  type SpeciesOrCombined,
} from './state/urlState.js'

export const SITE_URL = 'https://mappafunghi.app'

export const STATIC_PAGES = ['credits', 'terms', 'privacy'] as const
export type StaticPage = (typeof STATIC_PAGES)[number]

export type RouteMatch =
  | { kind: 'hub' }
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
  if (segments.length === 0) return { kind: 'hub' }
  if (segments.length > 2) return { kind: 'not-found' }

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
 * a legacy `?species=` link, or an installed PWA opening `/` with a stored last region — the
 * canonical URL to `replaceState` to. Bare `/` is the hub for ordinary visits.
 */
export function resolveLocation(pathname: string, search: string): ResolvedLocation {
  const params = new URLSearchParams(search)
  const hadSpeciesParam = params.has('species')
  const legacySpecies = params.get('species')
  params.delete('species')
  const query = params.toString()
  const suffix = query ? `?${query}` : ''

  if (pathname === '/') {
    const species: SpeciesOrCombined = isSpeciesOrCombined(legacySpecies)
      ? legacySpecies
      : 'combined'
    // Legacy `?species=` still lands on a region page (default region).
    if (hadSpeciesParam) {
      const region = REGIONS[DEFAULT_REGION_SLUG]
      const path =
        species === 'combined'
          ? regionPath(region.slug)
          : speciesPath(region.slug, species)
      return {
        match: { kind: 'region', region, species },
        redirectTo: `${path}${suffix}`,
      }
    }
    const pwaSlug = pwaHubRedirectSlug()
    if (pwaSlug) {
      const region = REGIONS[pwaSlug]
      return {
        match: { kind: 'region', region, species: 'combined' },
        redirectTo: `${regionPath(region.slug)}${suffix}`,
      }
    }
    return { match: { kind: 'hub' } }
  }

  const match = matchPath(pathname)
  if (hadSpeciesParam) return { match, redirectTo: `${pathname}${suffix}` }
  return { match }
}

export interface SiteRoute {
  path: string
  region: string | null
  species: SpeciesOrCombined | null
  /**
   * SEO copy key: `hub` for `/`; a static page name; or a region's seo/intro key
   * (`region` | species) read from that region's registry copy.
   */
  seoKey: string
}

/**
 * The route's link-preview card: `/og/hub.png` for the hub; `/og/<region>.png`, or
 * `/og/<region>-<species>.png` for a species page. A page with no region (credits) reuses the
 * default region's.
 */
export function ogImagePath(
  route: Pick<SiteRoute, 'region' | 'species' | 'path'>,
): string {
  if (route.path === '/') return '/og/hub.png'
  const region = route.region ?? DEFAULT_REGION_SLUG
  const name =
    route.species && route.species !== 'combined' ? `${region}-${route.species}` : region
  return `/og/${name}.png`
}

export const ROUTES: SiteRoute[] = [
  { path: '/', region: null, species: null, seoKey: 'hub' },
  ...listRegions().flatMap((region) => [
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

/** The canonical route a path matched, or undefined for a 404. */
export function siteRouteFor(match: RouteMatch): SiteRoute | undefined {
  if (match.kind === 'not-found') return undefined
  const path =
    match.kind === 'hub'
      ? '/'
      : match.kind === 'static'
        ? `/${match.page}`
        : match.species === 'combined'
          ? regionPath(match.region.slug)
          : speciesPath(match.region.slug, match.species)
  return ROUTES.find((route) => route.path === path)
}
