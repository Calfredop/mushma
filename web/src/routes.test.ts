import { describe, expect, it } from 'vitest'
import {
  matchPath,
  regionPath,
  resolveLocation,
  ROUTES,
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
  it('matches a bare region path as the combined view', () => {
    expect(matchPath('/toscana')).toMatchObject({
      kind: 'region',
      region: { slug: 'toscana' },
      species: 'combined',
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

  it('404s the bare root', () => {
    expect(matchPath('/')).toEqual({ kind: 'not-found' })
  })

  it('ignores a trailing slash', () => {
    expect(matchPath('/toscana/')).toMatchObject({ kind: 'region', species: 'combined' })
  })
})

describe('resolveLocation', () => {
  it('redirects the bare root to the default region, combined view', () => {
    const resolved = resolveLocation('/', '')
    expect(resolved.match).toMatchObject({ kind: 'region', species: 'combined' })
    expect(resolved.redirectTo).toBe('/toscana')
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
  it('lists the combined and per-species page for every region, plus the static pages', () => {
    const paths = ROUTES.map((r) => r.path)
    expect(paths).toContain('/toscana')
    expect(paths).toContain('/toscana/porcini')
    expect(paths).toContain('/toscana/ovoli')
    expect(paths).toContain('/toscana/gallinacci')
    for (const page of STATIC_PAGES) expect(paths).toContain(`/${page}`)
  })

  it('has no duplicate paths', () => {
    const paths = ROUTES.map((r) => r.path)
    expect(new Set(paths).size).toBe(paths.length)
  })
})
