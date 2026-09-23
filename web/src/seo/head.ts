/**
 * Keeps the live document's `<title>`, meta description, canonical link and robots tag in
 * step with client-side navigation. The prerendered files (`./prerender.ts`) carry the
 * Italian-only indexed copy; this mirrors it for the current UI language and route.
 */
import type { RouteMatch, StaticPage } from '../routes'
import type { Species } from '../state/urlState'

export type SeoKey = 'region' | Species | StaticPage

/** The `seo.<key>` entry that matches a route, or null for a 404 (no page to index). */
export function seoKeyForRoute(route: RouteMatch): SeoKey | null {
  if (route.kind === 'region')
    return route.species === 'combined' ? 'region' : route.species
  if (route.kind === 'static') return route.page
  return null
}

function upsertMeta(attr: 'name' | 'property', key: string, content: string | undefined) {
  const selector = `meta[${attr}="${key}"]`
  const existing = document.head.querySelector<HTMLMetaElement>(selector)
  if (content === undefined) {
    existing?.remove()
    return
  }
  const el = existing ?? document.head.appendChild(document.createElement('meta'))
  el.setAttribute(attr, key)
  el.setAttribute('content', content)
}

export function setDocumentDescription(description: string | undefined): void {
  upsertMeta('name', 'description', description)
}

export function setDocumentRobots(noindex: boolean): void {
  upsertMeta('name', 'robots', noindex ? 'noindex' : undefined)
}

export function setDocumentCanonical(url: string | undefined): void {
  const existing = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]')
  if (!url) {
    existing?.remove()
    return
  }
  const el = existing ?? document.head.appendChild(document.createElement('link'))
  el.setAttribute('rel', 'canonical')
  el.setAttribute('href', url)
}
