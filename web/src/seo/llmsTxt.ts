/**
 * `/llms.txt` (llmstxt.org): a Markdown briefing for LLMs and answer engines. It says what the
 * site is, the rules an answer about it must keep (conditions only, never edibility; a 0–1
 * index, not a probability; sightings only as counts per cell) and links every page and data
 * source. Built from the same route list and locale copy as the sitemap and the JSON-LD, in
 * Italian like the rest of the indexed copy (`vite.config.ts` writes it at build time).
 */
import { type Credit, DATA_CREDITS, SOFTWARE_CREDITS } from '../credits.js'
import en from '../i18n/locales/en.json' with { type: 'json' }
import it from '../i18n/locales/it.json' with { type: 'json' }
import { ROUTES, SITE_URL } from '../routes.js'
import type { JsonLdLanguage } from './structuredData.js'

interface Copy {
  seo: { credits: { description: string } }
  intro: Record<string, string>
  disclaimer: { body1: string; body2: string; body3: string }
  credits: {
    title: string
    dataTitle: string
    license: string
    use: Record<Credit['use'], string>
  }
  structuredData: {
    appDescription: string
    features: Record<string, string>
    dataset: Record<string, string>
    score: { name: string; description: string }
    method: string
  }
  llms: {
    methodTitle: string
    liveData: string
    privacy: string
    featuresIntro: string
    mapsTitle: string
  }
}

const COPY: Record<JsonLdLanguage, Copy> = { it: it as Copy, en: en as Copy }

function link(text: string, url: string, note?: string): string {
  const item = `- [${text.replace(/[[\]]/g, '\\$&')}](${url})`
  return note ? `${item}: ${note}` : item
}

function creditLink(credit: Credit, copy: Copy): string {
  const license = copy.credits.license.replace('{{license}}', credit.license)
  return link(credit.name, credit.url, `${copy.credits.use[credit.use]}. ${license}`)
}

export function buildLlmsTxt(lang: JsonLdLanguage = 'it'): string {
  const copy = COPY[lang]
  const { structuredData: sd } = copy
  const mapRoutes = ROUTES.filter((route) => route.region !== null)

  const blocks = [
    '# Mappa Funghi',
    `> ${sd.appDescription}`,
    copy.disclaimer.body1,
    copy.disclaimer.body2,
    copy.disclaimer.body3,
    `**${sd.score.name}.** ${sd.score.description}`,
    `**${copy.llms.methodTitle}.** ${sd.method}`,
    copy.llms.liveData,
    copy.llms.privacy,
    [copy.llms.featuresIntro, '', ...Object.values(sd.features).map((f) => `- ${f}`)],
    `## ${copy.llms.mapsTitle}`,
    mapRoutes.map((route) =>
      link(
        sd.dataset[route.seoKey],
        `${SITE_URL}${route.path}`,
        copy.intro[route.seoKey],
      ),
    ),
    `## ${copy.credits.dataTitle}`,
    [
      link(copy.credits.title, `${SITE_URL}/credits`, copy.seo.credits.description),
      ...DATA_CREDITS.map((credit) => creditLink(credit, copy)),
    ],
    // "Optional" is llmstxt.org's own section name (skippable when context is short), so it
    // stays in English whatever the copy's language.
    '## Optional',
    [
      ...SOFTWARE_CREDITS.map((credit) => creditLink(credit, copy)),
      link('Sitemap', `${SITE_URL}/sitemap.xml`),
    ],
  ]
  return `${blocks.map((block) => (Array.isArray(block) ? block.join('\n') : block)).join('\n\n')}\n`
}
