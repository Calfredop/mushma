import { describe, expect, it } from 'vitest'
import { parseUrlState, rollToday, serializeUrlState } from './urlState'

const today = '2026-09-17'
const window = { pastDays: 6, forecastDays: 7 }

describe('parseUrlState', () => {
  it('defaults to porcini, today and no spot', () => {
    expect(parseUrlState('', today, window)).toEqual({
      species: 'porcini',
      date: today,
      spot: null,
    })
  })

  it('reads species, a date inside the window and a cell', () => {
    expect(
      parseUrlState('?species=ovoli&date=2026-09-20&cell=1kmN2438E4372', today, window),
    ).toEqual({
      species: 'ovoli',
      date: '2026-09-20',
      spot: { kind: 'cell', cellId: '1kmN2438E4372' },
    })
  })

  it('reads a point spot', () => {
    expect(parseUrlState('?at=43.85,11.73', today, window).spot).toEqual({
      kind: 'point',
      lat: 43.85,
      lon: 11.73,
    })
  })

  it('falls back to defaults for unknown species, dates outside the window and bad points', () => {
    expect(
      parseUrlState('?species=tartufi&date=2026-10-30&at=abc,1', today, window),
    ).toEqual({
      species: 'porcini',
      date: today,
      spot: null,
    })
    expect(parseUrlState('?date=2026-09-10', today, window).date).toBe(today)
    expect(parseUrlState('?date=2026-09-11', today, window).date).toBe('2026-09-11')
  })
})

describe('serializeUrlState', () => {
  it('omits defaults', () => {
    expect(
      serializeUrlState({ species: 'porcini', date: today, spot: null }, today),
    ).toBe('')
  })

  it('round-trips a full state', () => {
    const state = {
      species: 'combined' as const,
      date: '2026-09-12',
      spot: { kind: 'point' as const, lat: 43.123456789, lon: 11.5 },
    }
    const search = serializeUrlState(state, today)
    expect(search).toBe('?species=combined&date=2026-09-12&at=43.12346%2C11.5')
    expect(parseUrlState(search, today, window)).toEqual({
      ...state,
      spot: { kind: 'point', lat: 43.12346, lon: 11.5 },
    })
  })
})

describe('parseUrlState edge cases', () => {
  const region: [[number, number], [number, number]] = [
    [9.68, 42.23],
    [12.38, 44.48],
  ]

  it('rejects calendar dates that do not exist', () => {
    expect(parseUrlState('?date=2026-09-31', today, window).date).toBe(today)
    expect(parseUrlState('?date=2026-02-29', '2026-03-01', window).date).toBe(
      '2026-03-01',
    )
  })

  it('rejects empty coordinates and points outside the region', () => {
    expect(parseUrlState('?at=,', today, window, region).spot).toBeNull()
    expect(parseUrlState('?at=43.8,', today, window, region).spot).toBeNull()
    expect(parseUrlState('?at=45.46,9.19', today, window, region).spot).toBeNull()
    expect(parseUrlState('?at=43.85,11.73', today, window, region).spot).toEqual({
      kind: 'point',
      lat: 43.85,
      lon: 11.73,
    })
  })
})

describe('rollToday', () => {
  it('moves a date that was "today" to the new today, and leaves chosen dates alone', () => {
    expect(rollToday('2026-09-17', '2026-09-17', '2026-09-18')).toBe('2026-09-18')
    expect(rollToday('2026-09-20', '2026-09-17', '2026-09-18')).toBe('2026-09-20')
  })

  it('pulls a date that fell out of the window back to today', () => {
    expect(rollToday('2026-09-11', '2026-09-17', '2026-09-18', window)).toBe('2026-09-18')
  })
})
