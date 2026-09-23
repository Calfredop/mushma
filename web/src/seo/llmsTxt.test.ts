import { describe, expect, it } from 'vitest'
import { DATA_CREDITS, SOFTWARE_CREDITS } from '../credits'
import { DISCLAIMER_SECTIONS } from '../disclaimer'
import en from '../i18n/locales/en.json'
import itLocale from '../i18n/locales/it.json'
import { ROUTES } from '../routes'
import { buildLlmsTxt } from './llmsTxt'

const txt = buildLlmsTxt()
const lines = txt.split('\n')

/** The H2 sections, in order, each with the lines under it. */
function sections(text: string): { title: string; lines: string[] }[] {
  const out: { title: string; lines: string[] }[] = []
  for (const line of text.split('\n')) {
    if (line.startsWith('## ')) out.push({ title: line.slice(3), lines: [] })
    else out.at(-1)?.lines.push(line)
  }
  return out
}

describe('buildLlmsTxt', () => {
  it('opens with the site name as the only H1, then a one-paragraph summary blockquote', () => {
    expect(lines[0]).toBe('# Mappa Funghi')
    expect(lines[1]).toBe('')
    expect(lines[2]).toBe(`> ${itLocale.structuredData.appDescription}`)
    expect(lines.filter((line) => line.startsWith('# '))).toHaveLength(1)
    // llmstxt.org: after the H1, only H2 sections; no deeper headings anywhere.
    expect(lines.filter((line) => /^#{3,} /.test(line))).toEqual([])
  })

  it('states the rules an answer must keep before any section: conditions only, not a probability', () => {
    const details = txt.slice(0, txt.indexOf('\n## '))
    const { sections, inspection } = itLocale.disclaimer
    for (const copy of [
      ...DISCLAIMER_SECTIONS.map(
        (key) => `**${sections[key].title}.** ${sections[key].body}`,
      ),
      inspection,
      itLocale.structuredData.score.description,
      itLocale.structuredData.method,
      itLocale.llms.liveData,
      itLocale.llms.privacy,
    ]) {
      expect(details).toContain(copy)
    }
    for (const feature of Object.values(itLocale.structuredData.features)) {
      expect(details).toContain(`- ${feature}`)
    }
  })

  it('links every map page by absolute URL, with its intro as the note', () => {
    const maps = sections(txt)[0]
    expect(maps.title).toBe(itLocale.llms.mapsTitle)
    const mapRoutes = ROUTES.filter((route) => route.region !== null)
    expect(mapRoutes).toHaveLength(4)
    for (const route of mapRoutes) {
      const name =
        itLocale.structuredData.dataset[
          route.seoKey as keyof typeof itLocale.structuredData.dataset
        ]
      const intro = itLocale.intro[route.seoKey as keyof typeof itLocale.intro]
      expect(maps.lines).toContain(
        `- [${name}](https://mappafunghi.app${route.path}): ${intro}`,
      )
    }
  })

  it('links the credits page and every data source, with what it is used for and its licence', () => {
    const data = sections(txt)[1]
    expect(data.title).toBe(itLocale.credits.dataTitle)
    expect(data.lines).toContain(
      `- [${itLocale.credits.title}](https://mappafunghi.app/credits): ${itLocale.seo.credits.description}`,
    )
    for (const credit of DATA_CREDITS) {
      expect(data.lines).toContain(
        `- [${credit.name}](${credit.url}): ${itLocale.credits.use[credit.use]}. Licenza: ${credit.license}`,
      )
    }
  })

  it('ends with the llmstxt.org "Optional" section: software credits and the sitemap', () => {
    const all = sections(txt)
    const optional = all.at(-1)!
    expect(all.map((s) => s.title)).toEqual([
      itLocale.llms.mapsTitle,
      itLocale.credits.dataTitle,
      'Optional',
    ])
    for (const credit of SOFTWARE_CREDITS) {
      expect(
        optional.lines.some((line) =>
          line.startsWith(`- [${credit.name}](${credit.url}): `),
        ),
      ).toBe(true)
    }
    expect(optional.lines).toContain('- [Sitemap](https://mappafunghi.app/sitemap.xml)')
  })

  it('links every indexed page, so a new route cannot be left out silently', () => {
    for (const route of ROUTES) {
      expect(txt).toContain(`](https://mappafunghi.app${route.path})`)
    }
  })

  it('ends with one newline and has no {{placeholders}} left over', () => {
    expect(txt.endsWith('\n')).toBe(true)
    expect(txt.endsWith('\n\n')).toBe(false)
    expect(txt).not.toContain('{{')
  })

  it('builds the same structure from the English copy', () => {
    const english = buildLlmsTxt('en')
    expect(english.split('\n')[2]).toBe(`> ${en.structuredData.appDescription}`)
    expect(sections(english).map((s) => s.title)).toEqual([
      en.llms.mapsTitle,
      en.credits.dataTitle,
      'Optional',
    ])
    expect(english).toContain(`License: ${DATA_CREDITS[0].license}`)
  })
})
