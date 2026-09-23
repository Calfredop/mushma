/** `robots.txt` and `sitemap.xml`, generated from the same route list as the prerendered heads. */
import { SITE_URL } from '../routes.js'
import type { RouteHead } from './prerender.js'

export function buildSitemapXml(heads: RouteHead[]): string {
  const urls = heads
    .map((head) => `  <url>\n    <loc>${head.url}</loc>\n  </url>`)
    .join('\n')
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    urls,
    '</urlset>',
    '',
  ].join('\n')
}

export function buildRobotsTxt(): string {
  return ['User-agent: *', 'Allow: /', '', `Sitemap: ${SITE_URL}/sitemap.xml`, ''].join(
    '\n',
  )
}
