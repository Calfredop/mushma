import { describe, expect, it } from 'vitest'
import { compareLocales, flattenKeys, placeholders } from './keys'

describe('flattenKeys', () => {
  it('lists every leaf as a dotted key', () => {
    expect(flattenKeys({ a: 'x', b: { c: 'y', d: { e: 'z' } } })).toEqual([
      'a',
      'b.c',
      'b.d.e',
    ])
  })
})

describe('placeholders', () => {
  it('finds interpolation variables, ignoring formats and duplicates', () => {
    expect(
      placeholders('{{count}} in {{place}}, {{ count }} {{date, datetime}}'),
    ).toEqual(['count', 'date', 'place'])
  })
})

describe('compareLocales', () => {
  it('reports keys missing from or extra to the other locale', () => {
    const result = compareLocales({ a: 'A', b: { c: 'C' } }, { a: 'A', d: 'D' })
    expect(result.missing).toEqual(['b.c'])
    expect(result.extra).toEqual(['d'])
  })

  it('reports empty strings and mismatched placeholders', () => {
    const result = compareLocales(
      { a: '{{n}} cells', b: 'ok', c: 'x' },
      { a: '{{count}} cells', b: 'ok', c: '  ' },
    )
    expect(result.placeholderMismatches).toEqual(['a'])
    expect(result.empty).toEqual(['c'])
  })

  it('is clean when both locales agree', () => {
    expect(compareLocales({ a: 'Hi {{name}}' }, { a: 'Ciao {{name}}' })).toEqual({
      missing: [],
      extra: [],
      empty: [],
      placeholderMismatches: [],
    })
  })
})
