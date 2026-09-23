import { describe, expect, it } from 'vitest'
import {
  canPickSpecies,
  keepIndicators,
  parseUrlState,
  rollToday,
  serializeUrlState,
  speciesForMode,
  toggleIndicator,
  type UrlState,
  withMode,
} from './urlState'

const today = '2026-09-17'
const window = { pastDays: 6, forecastDays: 7 }

describe('parseUrlState', () => {
  it('defaults to today and no spot', () => {
    expect(parseUrlState('', today, window)).toEqual({
      date: today,
      spot: null,
      view: 'now',
      comune: null,
      season: null,
      mode: 'map',
      indicators: [],
    })
  })

  it('reads a date inside the window and a cell', () => {
    expect(
      parseUrlState('?date=2026-09-20&cell=1kmN2438E4372', today, window),
    ).toMatchObject({
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

  it('falls back to defaults for dates outside the window and bad points', () => {
    expect(parseUrlState('?date=2026-10-30&at=abc,1', today, window)).toMatchObject({
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
      serializeUrlState(
        {
          date: today,
          spot: null,
          view: 'now',
          comune: null,
          season: null,
          mode: 'map',
          indicators: [],
        },
        today,
      ),
    ).toBe('')
  })

  it('round-trips a full state', () => {
    const state: UrlState = {
      date: '2026-09-12',
      spot: { kind: 'point', lat: 43.123456789, lon: 11.5 },
      view: 'now',
      comune: null,
      season: null,
      mode: 'map',
      indicators: [],
    }
    const search = serializeUrlState(state, today)
    expect(search).toBe('?date=2026-09-12&at=43.12346%2C11.5')
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

describe('time views in the URL', () => {
  const historyStart = '2016-01-01'

  it('defaults to the "now" view with no comune and no season', () => {
    const state = parseUrlState('', today, window, undefined, historyStart)
    expect(state.view).toBe('now')
    expect(state.comune).toBeNull()
    expect(state.season).toBeNull()
  })

  it('replays any past day back to the start of the history', () => {
    expect(
      parseUrlState('?date=2024-10-12', today, window, undefined, historyStart).date,
    ).toBe('2024-10-12')
    expect(
      parseUrlState('?date=2015-12-31', today, window, undefined, historyStart).date,
    ).toBe(today)
    // The future still stops at the end of the forecast.
    expect(
      parseUrlState('?date=2026-09-25', today, window, undefined, historyStart).date,
    ).toBe(today)
  })

  it('reads the seasons view with a comune and a season on the map', () => {
    const state = parseUrlState(
      '?view=seasons&comune=046007&season=2024',
      today,
      window,
      undefined,
      historyStart,
    )
    expect(state).toMatchObject({ view: 'seasons', comune: '046007', season: 2024 })
  })

  it('keeps a season on the map only in the seasons view, and only a stored year', () => {
    expect(
      parseUrlState('?view=outlook&season=2024', today, window, undefined, historyStart)
        .season,
    ).toBeNull()
    expect(
      parseUrlState('?view=seasons&season=2015', today, window, undefined, historyStart)
        .season,
    ).toBeNull()
    expect(
      parseUrlState('?view=seasons&season=twenty', today, window, undefined, historyStart)
        .season,
    ).toBeNull()
    expect(
      parseUrlState('?view=almanac', today, window, undefined, historyStart).view,
    ).toBe('now')
    expect(
      parseUrlState('?comune=<script>', today, window, undefined, historyStart).comune,
    ).toBeNull()
  })

  it('round-trips the time views and omits their defaults', () => {
    const state: UrlState = {
      date: '2024-10-12',
      spot: null,
      view: 'seasons',
      comune: '046007',
      season: 2024,
      mode: 'map',
      indicators: [],
    }
    const search = serializeUrlState(state, today)
    expect(search).toBe('?date=2024-10-12&view=seasons&comune=046007&season=2024')
    expect(parseUrlState(search, today, window, undefined, historyStart)).toEqual(state)
    expect(
      serializeUrlState(
        {
          date: today,
          spot: null,
          view: 'now',
          comune: null,
          season: null,
          mode: 'map',
          indicators: [],
        },
        today,
      ),
    ).toBe('')
  })

  it('keeps a replayed day at midnight instead of pulling it back to today', () => {
    expect(
      rollToday('2024-10-12', '2026-09-17', '2026-09-18', window, historyStart),
    ).toBe('2024-10-12')
    expect(
      rollToday('2026-09-11', '2026-09-17', '2026-09-18', window, historyStart),
    ).toBe('2026-09-11')
  })
})

describe('analysis mode in the URL', () => {
  const parse = (search: string) => parseUrlState(search, today, window)

  it('reads the mode and its indicators in the order they were turned on', () => {
    expect(parse('?mode=analysis&f=drying,rain_trigger')).toMatchObject({
      mode: 'analysis',
      indicators: ['drying', 'rain_trigger'],
    })
  })

  it('drops unknown and repeated ids', () => {
    expect(
      parse('?mode=analysis&f=rain_trigger,tartufi,,drying,rain_trigger').indicators,
    ).toEqual(['rain_trigger', 'drying'])
  })

  it('turns on rain_trigger when it opens with no f', () => {
    expect(parse('?mode=analysis').indicators).toEqual(['rain_trigger'])
  })

  it('keeps an empty f: every indicator turned off', () => {
    expect(parse('?mode=analysis&f=').indicators).toEqual([])
  })

  it('has no combined score: Tutti opens as porcini', () => {
    expect(speciesForMode('combined', 'analysis')).toBe('porcini')
    expect(speciesForMode('ovoli', 'analysis')).toBe('ovoli')
    expect(speciesForMode('combined', 'map')).toBe('combined')
  })

  it('ignores indicators outside the mode, and an unknown mode', () => {
    expect(parse('?f=drying')).toMatchObject({ mode: 'map', indicators: [] })
    expect(parse('?mode=xray&f=drying')).toMatchObject({ mode: 'map', indicators: [] })
  })

  it('round-trips, writing f only in the mode', () => {
    const state: UrlState = {
      ...parse(''),
      mode: 'analysis',
      indicators: ['rain_trigger', 'evaporative_demand'],
    }
    const search = serializeUrlState(state, today)
    expect(search).toBe('?mode=analysis&f=rain_trigger%2Cevaporative_demand')
    expect(parse(search)).toEqual(state)
    expect(serializeUrlState({ ...state, indicators: [] }, today)).toBe(
      '?mode=analysis&f=',
    )
    expect(serializeUrlState({ ...state, mode: 'map' }, today)).toBe('')
  })
})

describe('analysis mode transitions', () => {
  const base = parseUrlState('', today, window)

  it('entering turns on rain_trigger when nothing is on', () => {
    expect(withMode(base, 'analysis')).toMatchObject({
      mode: 'analysis',
      indicators: ['rain_trigger'],
    })
  })

  it('entering again brings back the indicators it had', () => {
    const left = withMode({ ...base, mode: 'analysis', indicators: ['drying'] }, 'map')
    expect(left.mode).toBe('map')
    expect(withMode(left, 'analysis').indicators).toEqual(['drying'])
  })

  it('Tutti cannot be picked in it', () => {
    expect(canPickSpecies('ovoli', 'analysis')).toBe(true)
    expect(canPickSpecies('combined', 'analysis')).toBe(false)
    expect(canPickSpecies('combined', 'map')).toBe(true)
  })

  it('keeps only the indicators the species has, or rain_trigger when none is left', () => {
    const inMode = {
      ...base,
      mode: 'analysis' as const,
      indicators: ['drying', 'rain_30d', 'heat_spike'],
    }
    const ovoli = ['rain_trigger', 'rain_30d', 'evaporative_demand']
    expect(keepIndicators(inMode, ovoli).indicators).toEqual(['rain_30d'])
    expect(
      keepIndicators({ ...inMode, indicators: ['drying', 'heat_spike'] }, ovoli)
        .indicators,
    ).toEqual(['rain_trigger'])
    expect(keepIndicators({ ...inMode, indicators: [] }, ovoli).indicators).toEqual([])
    // Nothing to drop: the same state, so no re-render.
    const kept = { ...inMode, indicators: ['rain_30d'] }
    expect(keepIndicators(kept, ovoli)).toBe(kept)
  })

  it('turns an indicator on at the top of the stack, or off', () => {
    const inMode = { ...base, mode: 'analysis' as const, indicators: ['rain_trigger'] }
    const on = toggleIndicator(inMode, 'drying')
    expect(on.indicators).toEqual(['rain_trigger', 'drying'])
    expect(toggleIndicator(on, 'rain_trigger').indicators).toEqual(['drying'])
  })
})
