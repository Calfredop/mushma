import { describe, expect, it } from 'vitest'
import { ROUTES } from '../routes'
import { routeHeads } from './prerender'
import { buildRobotsTxt, buildSitemapXml } from './sitemap'

describe('buildSitemapXml', () => {
  const xml = buildSitemapXml(routeHeads())

  it('is well-formed sitemap XML', () => {
    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>')).toBe(true)
    expect(xml).toContain('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    expect(xml).toContain('</urlset>')
  })

  it('lists every route, including the credits page, as an absolute mappafunghi.app URL', () => {
    for (const route of ROUTES) {
      expect(xml).toContain(`<loc>https://mappafunghi.app${route.path}</loc>`)
    }
    expect(xml).toContain('<loc>https://mappafunghi.app/credits</loc>')
  })

  it('lists each URL exactly once', () => {
    const matches = xml.match(/<loc>/g) ?? []
    expect(matches).toHaveLength(ROUTES.length)
  })
})

describe('buildRobotsTxt', () => {
  const robots = buildRobotsTxt()

  it('allows crawling and points at the sitemap', () => {
    expect(robots).toContain('User-agent: *')
    expect(robots).toContain('Allow: /')
    expect(robots).toContain('Sitemap: https://mappafunghi.app/sitemap.xml')
  })
})
