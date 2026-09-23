import { describe, expect, it } from 'vitest'
import { ROUTES } from '../routes'
import { renderNotFoundHtml, renderRouteHtml, routeHeads } from './prerender'

const TEMPLATE = `<!doctype html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <title>Mappa Funghi</title>
    <script type="module" crossorigin src="/assets/index-abc123.js"></script>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
`

describe('routeHeads', () => {
  it('has a head for every route in the canonical list', () => {
    const heads = routeHeads()
    expect(heads.map((h) => h.path)).toEqual(ROUTES.map((r) => r.path))
  })

  it('gives the region page and each species page their own title and description', () => {
    const heads = routeHeads()
    const byPath = Object.fromEntries(heads.map((h) => [h.path, h]))
    expect(byPath['/toscana'].title).toContain('Toscana')
    expect(byPath['/toscana/porcini'].title).toContain('Porcini')
    expect(byPath['/toscana/ovoli'].title).toContain('Ovoli')
    expect(byPath['/toscana/gallinacci'].title).toContain('Gallinacci')
    expect(byPath['/credits'].title).toContain('crediti')
    // Every title and description is distinct: no two pages compete for the same query.
    expect(new Set(heads.map((h) => h.title)).size).toBe(heads.length)
    expect(new Set(heads.map((h) => h.description)).size).toBe(heads.length)
  })

  it('builds an absolute, https, mappafunghi.app URL and image for every route', () => {
    for (const head of routeHeads()) {
      expect(head.url).toBe(`https://mappafunghi.app${head.path}`)
      expect(head.image).toMatch(/^https:\/\/mappafunghi\.app\/og\/.+\.png$/)
    }
  })

  it('points the credits page at the region page image', () => {
    const heads = routeHeads()
    const region = heads.find((h) => h.path === '/toscana')!
    const credits = heads.find((h) => h.path === '/credits')!
    expect(credits.image).toBe(region.image)
  })
})

describe('renderRouteHtml', () => {
  const head = routeHeads().find((h) => h.path === '/toscana/porcini')!

  it('replaces the title', () => {
    const html = renderRouteHtml(TEMPLATE, head)
    expect(html).toContain(`<title>${head.title}</title>`)
    expect(html).not.toContain('<title>Mappa Funghi</title>')
  })

  it('sets the meta description and canonical link', () => {
    const html = renderRouteHtml(TEMPLATE, head)
    expect(html).toContain(`<meta name="description" content="${head.description}">`)
    expect(html).toContain(`<link rel="canonical" href="${head.url}">`)
  })

  it('sets Open Graph and Twitter card tags', () => {
    const html = renderRouteHtml(TEMPLATE, head)
    expect(html).toContain(`<meta property="og:title" content="${head.title}">`)
    expect(html).toContain(`<meta property="og:url" content="${head.url}">`)
    expect(html).toContain(`<meta property="og:image" content="${head.image}">`)
    expect(html).toContain('<meta name="twitter:card" content="summary_large_image">')
    expect(html).toContain(`<meta name="twitter:image" content="${head.image}">`)
  })

  it("embeds the page's JSON-LD graph, in Italian", () => {
    const html = renderRouteHtml(TEMPLATE, head)
    const scripts = [
      ...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs),
    ]
    expect(scripts).toHaveLength(1)
    const jsonLd = JSON.parse(scripts[0][1])
    expect(jsonLd).toEqual(head.jsonLd)
    expect(jsonLd['@context']).toBe('https://schema.org')
    expect(jsonLd['@graph']).toContainEqual(
      expect.objectContaining({ '@type': 'WebPage', url: head.url, inLanguage: 'it' }),
    )
    expect(jsonLd['@graph']).toContainEqual(
      expect.objectContaining({ '@type': 'WebApplication' }),
    )
  })

  it('gives every route a JSON-LD graph that describes that same page', () => {
    for (const routeHead of routeHeads()) {
      expect(routeHead.jsonLd['@graph']).toContainEqual(
        expect.objectContaining({ '@type': 'WebPage', url: routeHead.url }),
      )
    }
  })

  it('keeps the rest of the built document intact', () => {
    const html = renderRouteHtml(TEMPLATE, head)
    expect(html).toContain('<html lang="it">')
    expect(html).toContain('src="/assets/index-abc123.js"')
  })

  it('escapes HTML-sensitive characters in the copy', () => {
    const html = renderRouteHtml(TEMPLATE, {
      path: '/x',
      url: 'https://mappafunghi.app/x',
      title: 'Fun & Games "quoted"',
      description: '<script>alert(1)</script>',
      image: 'https://mappafunghi.app/og/x.png',
      intro: undefined,
      jsonLd: { '@context': 'https://schema.org', '@graph': [] },
    })
    expect(html).not.toContain('<script>alert(1)</script>')
    expect(html).toContain('Fun &amp; Games &quot;quoted&quot;')
  })
})

function escapeForAssertion(value: string): string {
  return value.replace(
    /[&<>"']/g,
    (ch) =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]!,
  )
}

describe('renderRouteHtml intro copy', () => {
  it('seeds the region and species pages with their intro paragraph inside #root', () => {
    for (const path of [
      '/toscana',
      '/toscana/porcini',
      '/toscana/ovoli',
      '/toscana/gallinacci',
    ]) {
      const head = routeHeads().find((h) => h.path === path)!
      expect(head.intro).toBeTruthy()
      const html = renderRouteHtml(TEMPLATE, head)
      expect(html).toContain(
        `<div id="root"><p>${escapeForAssertion(head.intro!)}</p></div>`,
      )
    }
  })

  it('leaves #root empty for a page with no intro copy', () => {
    const head = routeHeads().find((h) => h.path === '/credits')!
    expect(head.intro).toBeUndefined()
    const html = renderRouteHtml(TEMPLATE, head)
    expect(html).toContain('<div id="root"></div>')
  })

  it('escapes the intro text', () => {
    const html = renderRouteHtml(TEMPLATE, {
      path: '/x',
      url: 'https://mappafunghi.app/x',
      title: 'x',
      description: 'x',
      image: 'https://mappafunghi.app/og/x.png',
      intro: '<b>bold</b> & "quoted"',
      jsonLd: { '@context': 'https://schema.org', '@graph': [] },
    })
    expect(html).toContain('<p>&lt;b&gt;bold&lt;/b&gt; &amp; &quot;quoted&quot;</p>')
  })
})

describe('renderNotFoundHtml', () => {
  const html = renderNotFoundHtml(TEMPLATE)

  it('sets a title and description, and marks the page noindex', () => {
    expect(html).toMatch(/<title>.+<\/title>/)
    expect(html).not.toContain('<title>Mappa Funghi</title>')
    expect(html).toContain('<meta name="robots" content="noindex">')
    expect(html).toMatch(/<meta name="description" content=".+">/)
  })

  it('has no canonical, Open Graph or JSON-LD: there is nothing to index', () => {
    expect(html).not.toContain('rel="canonical"')
    expect(html).not.toContain('og:')
    expect(html).not.toContain('application/ld+json')
  })

  it('shows a visible link back to the default region', () => {
    expect(html).toContain('<a href="/toscana">')
  })

  it('keeps the rest of the built document intact', () => {
    expect(html).toContain('<html lang="it">')
    expect(html).toContain('src="/assets/index-abc123.js"')
  })
})
