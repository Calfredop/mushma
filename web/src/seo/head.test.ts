import { afterEach, describe, expect, it } from 'vitest'
import {
  seoKeyForRoute,
  setDocumentCanonical,
  setDocumentDescription,
  setDocumentJsonLd,
  setDocumentRobots,
} from './head'

afterEach(() => {
  document.head.querySelectorAll('meta[name="description"]').forEach((el) => el.remove())
  document.head.querySelectorAll('meta[name="robots"]').forEach((el) => el.remove())
  document.head.querySelectorAll('link[rel="canonical"]').forEach((el) => el.remove())
  document.head
    .querySelectorAll('script[type="application/ld+json"]')
    .forEach((el) => el.remove())
})

describe('seoKeyForRoute', () => {
  it('keys the combined region view as "region" and a species page as the species', () => {
    const region = { slug: 'toscana' } as never
    expect(seoKeyForRoute({ kind: 'region', region, species: 'combined' })).toBe('region')
    expect(seoKeyForRoute({ kind: 'region', region, species: 'porcini' })).toBe('porcini')
  })

  it('keys a static page as itself, and a not-found match as null', () => {
    expect(seoKeyForRoute({ kind: 'static', page: 'credits' })).toBe('credits')
    expect(seoKeyForRoute({ kind: 'not-found' })).toBeNull()
  })
})

describe('setDocumentDescription', () => {
  it('creates the tag, then updates it in place, then removes it', () => {
    setDocumentDescription('first')
    expect(
      document.head.querySelector('meta[name="description"]')?.getAttribute('content'),
    ).toBe('first')

    setDocumentDescription('second')
    expect(document.head.querySelectorAll('meta[name="description"]')).toHaveLength(1)
    expect(
      document.head.querySelector('meta[name="description"]')?.getAttribute('content'),
    ).toBe('second')

    setDocumentDescription(undefined)
    expect(document.head.querySelector('meta[name="description"]')).toBeNull()
  })
})

describe('setDocumentCanonical', () => {
  it('creates, updates and removes the canonical link', () => {
    setDocumentCanonical('https://mappafunghi.app/toscana')
    expect(
      document.head.querySelector('link[rel="canonical"]')?.getAttribute('href'),
    ).toBe('https://mappafunghi.app/toscana')

    setDocumentCanonical('https://mappafunghi.app/toscana/porcini')
    expect(document.head.querySelectorAll('link[rel="canonical"]')).toHaveLength(1)
    expect(
      document.head.querySelector('link[rel="canonical"]')?.getAttribute('href'),
    ).toBe('https://mappafunghi.app/toscana/porcini')

    setDocumentCanonical(undefined)
    expect(document.head.querySelector('link[rel="canonical"]')).toBeNull()
  })
})

describe('setDocumentRobots', () => {
  it('sets noindex only when asked, and clears it again', () => {
    setDocumentRobots(true)
    expect(
      document.head.querySelector('meta[name="robots"]')?.getAttribute('content'),
    ).toBe('noindex')

    setDocumentRobots(false)
    expect(document.head.querySelector('meta[name="robots"]')).toBeNull()
  })
})

describe('setDocumentJsonLd', () => {
  const scripts = () =>
    document.head.querySelectorAll<HTMLScriptElement>(
      'script[type="application/ld+json"]',
    )

  it('updates the prerendered JSON-LD in place, then removes it', () => {
    const prerendered = document.createElement('script')
    prerendered.type = 'application/ld+json'
    prerendered.textContent = '{"@context":"https://schema.org","name":"prerendered"}'
    document.head.appendChild(prerendered)

    setDocumentJsonLd({ '@context': 'https://schema.org', name: 'client' })
    expect(scripts()).toHaveLength(1)
    expect(JSON.parse(scripts()[0].textContent!)).toEqual({
      '@context': 'https://schema.org',
      name: 'client',
    })

    setDocumentJsonLd(undefined)
    expect(scripts()).toHaveLength(0)
  })

  it('creates the script when the page has none', () => {
    setDocumentJsonLd({ '@context': 'https://schema.org', name: 'fresh' })
    expect(scripts()).toHaveLength(1)
    expect(JSON.parse(scripts()[0].textContent!).name).toBe('fresh')
  })
})
