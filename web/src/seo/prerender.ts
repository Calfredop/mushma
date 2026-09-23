/**
 * Turns the built `dist/index.html` into one prerendered file per route: its own title, meta
 * description, canonical, Open Graph + Twitter card tags and `WebApplication` JSON-LD.
 *
 * Pure string transforms, so they're cheap to unit test directly; the prerender plugin in
 * `vite.config.ts` does the file I/O and imports only this module (not the rest of the app),
 * so it stays free of `import.meta.env` like `./routes` and `./regions`.
 */
import it from '../i18n/locales/it.json' with { type: 'json' }
import { DEFAULT_REGION_SLUG } from '../regions.js'
import { regionPath, ROUTES, SITE_URL, type SiteRoute } from '../routes.js'

interface SeoCopy {
  title: string
  description: string
}

const SEO_COPY = (it as { seo: Record<string, SeoCopy> }).seo
const INTRO_COPY = (it as { intro: Record<string, string> }).intro

export interface RouteHead {
  path: string
  url: string
  title: string
  description: string
  image: string
  /** Visible lede paragraph (item: "Visible intro copy"); undefined for pages with none. */
  intro: string | undefined
}

/** `/og/<region>.png`, or `/og/<region>-<species>.png` for a species page (item 9). */
function ogImagePath(route: SiteRoute): string {
  const region = route.region ?? DEFAULT_REGION_SLUG
  const name =
    route.species && route.species !== 'combined' ? `${region}-${route.species}` : region
  return `/og/${name}.png`
}

export function routeHeads(routes: SiteRoute[] = ROUTES): RouteHead[] {
  return routes.map((route) => {
    const copy = SEO_COPY[route.seoKey]
    if (!copy) throw new Error(`No seo.${route.seoKey} copy for route ${route.path}`)
    return {
      path: route.path,
      url: `${SITE_URL}${route.path}`,
      title: copy.title,
      description: copy.description,
      image: `${SITE_URL}${ogImagePath(route)}`,
      intro: INTRO_COPY[route.seoKey],
    }
  })
}

const HTML_ESCAPES: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (ch) => HTML_ESCAPES[ch])
}

function webApplicationJsonLd(head: RouteHead): string {
  const json = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: 'Mappa Funghi',
    description: head.description,
    url: head.url,
    image: head.image,
    inLanguage: 'it',
    applicationCategory: 'UtilitiesApplication',
    operatingSystem: 'Any',
  })
  // The copy is ours, so this can't happen today; kept so it stays true if that changes.
  return json.replace(/<\/script/gi, '<\\/script')
}

const TITLE_TAG = /<title>[\s\S]*?<\/title>/
const ROOT_DIV = '<div id="root"></div>'

/**
 * Renders one route's prerendered HTML from the built `dist/index.html` template. The intro
 * paragraph, when the route has one, goes inside `#root`: real, visible text for crawlers and
 * pre-JS visitors — the client replaces it (`createRoot`, not hydration) the moment it mounts.
 */
export function renderRouteHtml(template: string, head: RouteHead): string {
  if (!TITLE_TAG.test(template)) throw new Error('template has no <title> tag')
  if (!template.includes('</head>')) throw new Error('template has no </head>')
  if (head.intro && !template.includes(ROOT_DIV)) {
    throw new Error('template has no empty #root to seed the intro copy into')
  }

  const tags = [
    `<meta name="description" content="${escapeHtml(head.description)}">`,
    `<link rel="canonical" href="${head.url}">`,
    `<meta property="og:type" content="website">`,
    `<meta property="og:site_name" content="Mappa Funghi">`,
    `<meta property="og:locale" content="it_IT">`,
    `<meta property="og:title" content="${escapeHtml(head.title)}">`,
    `<meta property="og:description" content="${escapeHtml(head.description)}">`,
    `<meta property="og:url" content="${head.url}">`,
    `<meta property="og:image" content="${head.image}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<meta name="twitter:title" content="${escapeHtml(head.title)}">`,
    `<meta name="twitter:description" content="${escapeHtml(head.description)}">`,
    `<meta name="twitter:image" content="${head.image}">`,
    `<script type="application/ld+json">${webApplicationJsonLd(head)}</script>`,
  ].join('\n    ')

  let html = template
    .replace(TITLE_TAG, `<title>${escapeHtml(head.title)}</title>`)
    .replace('</head>', `    ${tags}\n</head>`)
  if (head.intro) {
    html = html.replace(ROOT_DIV, `<div id="root"><p>${escapeHtml(head.intro)}</p></div>`)
  }
  return html
}

interface NotFoundCopy {
  eyebrow: string
  title: string
  body: string
}

const NOT_FOUND_COPY = (it as { notFound: NotFoundCopy }).notFound
const BACK_TO_MAP = (it as { nav: { backToMap: string } }).nav.backToMap

/**
 * Renders the static `404.html` Vercel serves for any path outside the route list: its own
 * title, `noindex` (nothing here to index), and a real link back to the default region — no
 * canonical, Open Graph or JSON-LD, since there's no page to describe.
 */
export function renderNotFoundHtml(template: string): string {
  if (!TITLE_TAG.test(template)) throw new Error('template has no <title> tag')
  if (!template.includes('</head>')) throw new Error('template has no </head>')
  if (!template.includes(ROOT_DIV)) throw new Error('template has no empty #root')

  const backHref = regionPath(DEFAULT_REGION_SLUG)
  const tags = [
    `<meta name="robots" content="noindex">`,
    `<meta name="description" content="${escapeHtml(NOT_FOUND_COPY.body)}">`,
  ].join('\n    ')
  const body = [
    `<div id="root">`,
    `<p>${escapeHtml(NOT_FOUND_COPY.eyebrow)}</p>`,
    `<h1>${escapeHtml(NOT_FOUND_COPY.title)}</h1>`,
    `<p>${escapeHtml(NOT_FOUND_COPY.body)}</p>`,
    `<p><a href="${backHref}">${escapeHtml(BACK_TO_MAP)}</a></p>`,
    `</div>`,
  ].join('')

  return template
    .replace(TITLE_TAG, `<title>${escapeHtml(NOT_FOUND_COPY.title)}</title>`)
    .replace('</head>', `    ${tags}\n</head>`)
    .replace(ROOT_DIV, body)
}
