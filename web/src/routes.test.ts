import { describe, expect, it } from 'vitest'
import {
  matchPath,
  regionPath,
  ogImagePath,
  resolveLocation,
  ROUTES,
  siteRouteFor,
  speciesPath,
  STATIC_PAGES,
} from './routes'

describe('regionPath / speciesPath', () => {
  it('builds a region path and a region+species path', () => {
    expect(regionPath('toscana')).toBe('/toscana')
    expect(speciesPath('toscana', 'porcini')).toBe('/toscana/porcini')
  })
})

describe('matchPath', () => {
  it('matches the bare root as the hub', () => {
    expect(matchPath('/')).toEqual({ kind: 'hub' })
  })

  it('matches a bare region path as the combined view', () => {
    expect(matchPath('/toscana')).toMatchObject({
      kind: 'region',
      region: { slug: 'toscana' },
      species: 'combined',
    })
  })

  it('matches a second region', () => {
    expect(matchPath('/umbria')).toMatchObject({
      kind: 'region',
      region: { slug: 'umbria', apiRegionId: 'umbria' },
      species: 'combined',
    })
    expect(matchPath('/umbria/porcini')).toMatchObject({
      kind: 'region',
      region: { slug: 'umbria' },
      species: 'porcini',
    })
  })

  it('matches a region+species path', () => {
    expect(matchPath('/toscana/porcini')).toMatchObject({
      kind: 'region',
      region: { slug: 'toscana' },
      species: 'porcini',
    })
  })

  it('matches a known static page', () => {
    expect(matchPath('/credits')).toEqual({ kind: 'static', page: 'credits' })
  })

  it('404s an unknown region', () => {
    expect(matchPath('/lombardia')).toEqual({ kind: 'not-found' })
  })

  it('404s an unknown species', () => {
    expect(matchPath('/toscana/tartufi')).toEqual({ kind: 'not-found' })
  })

  it('404s "combined" as an explicit path segment', () => {
    expect(matchPath('/toscana/combined')).toEqual({ kind: 'not-found' })
  })

  it('404s extra path segments', () => {
    expect(matchPath('/toscana/porcini/extra')).toEqual({ kind: 'not-found' })
  })

  it('ignores a trailing slash', () => {
    expect(matchPath('/toscana/')).toMatchObject({ kind: 'region', species: 'combined' })
  })
})

describe('resolveLocation', () => {
  it('keeps the bare root as the hub with no redirect', () => {
    const resolved = resolveLocation('/', '')
    expect(resolved.match).toEqual({ kind: 'hub' })
    expect(resolved.redirectTo).toBeUndefined()
  })

  it('rewrites a legacy ?species= query on the root into the species path', () => {
    const resolved = resolveLocation('/', '?species=ovoli&date=2026-09-20')
    expect(resolved.match).toMatchObject({ kind: 'region', species: 'ovoli' })
    expect(resolved.redirectTo).toBe('/toscana/ovoli?date=2026-09-20')
  })

  it('falls back to combined for an invalid legacy species value', () => {
    expect(resolveLocation('/', '?species=tartufi').redirectTo).toBe('/toscana')
  })

  it('strips a stray species query on an already-canonical path', () => {
    const resolved = resolveLocation('/toscana/porcini', '?species=ovoli&date=2026-09-20')
    expect(resolved.match).toMatchObject({ kind: 'region', species: 'porcini' })
    expect(resolved.redirectTo).toBe('/toscana/porcini?date=2026-09-20')
  })

  it('does not redirect an already-canonical URL with no legacy species param', () => {
    const resolved = resolveLocation('/toscana/porcini', '?date=2026-09-20')
    expect(resolved.match).toMatchObject({ kind: 'region', species: 'porcini' })
    expect(resolved.redirectTo).toBeUndefined()
  })

  it('does not redirect a static page', () => {
    expect(resolveLocation('/credits', '').redirectTo).toBeUndefined()
  })

  it('carries a not-found match through with no redirect', () => {
    const resolved = resolveLocation('/lombardia', '')
    expect(resolved.match).toEqual({ kind: 'not-found' })
    expect(resolved.redirectTo).toBeUndefined()
  })
})

describe('ROUTES', () => {
  it('lists the hub, every region page, and the static pages', () => {
    const paths = ROUTES.map((r) => r.path)
    expect(paths).toContain('/')
    expect(paths).toContain('/toscana')
    expect(paths).toContain('/toscana/porcini')
    expect(paths).toContain('/umbria')
    expect(paths).toContain('/umbria/gallinacci')
    for (const page of STATIC_PAGES) expect(paths).toContain(`/${page}`)
  })

  it('has no duplicate paths', () => {
    const paths = ROUTES.map((r) => r.path)
    expect(new Set(paths).size).toBe(paths.length)
  })
})

describe('siteRouteFor', () => {
  it('finds the canonical route a path matched, and none for a 404', () => {
    expect(siteRouteFor(matchPath('/'))?.path).toBe('/')
    expect(siteRouteFor(matchPath('/toscana'))?.path).toBe('/toscana')
    expect(siteRouteFor(matchPath('/toscana/porcini'))?.path).toBe('/toscana/porcini')
    expect(siteRouteFor(matchPath('/credits'))?.path).toBe('/credits')
    expect(siteRouteFor(matchPath('/lombardia'))).toBeUndefined()
  })
})

describe('ogImagePath', () => {
  it('is the hub, region, or region-species card', () => {
    expect(ogImagePath({ path: '/', region: null, species: null })).toBe('/og/hub.png')
    expect(
      ogImagePath({ path: '/toscana', region: 'toscana', species: 'combined' }),
    ).toBe('/og/toscana.png')
    expect(
      ogImagePath({ path: '/toscana/ovoli', region: 'toscana', species: 'ovoli' }),
    ).toBe('/og/toscana-ovoli.png')
    expect(ogImagePath({ path: '/credits', region: null, species: null })).toBe(
      '/og/toscana.png',
    )
  })
})
