import { describe, expect, it } from 'vitest'
import {
  addDays,
  dateWindow,
  daysBetween,
  formatDay,
  formatDayLong,
  todayInRome,
} from './days'

describe('todayInRome', () => {
  it('uses the Europe/Rome calendar day, not UTC', () => {
    // 22:30 UTC on the 16th is 00:30 on the 17th in Rome (CEST, UTC+2).
    expect(todayInRome(new Date('2026-09-16T22:30:00Z'))).toBe('2026-09-17')
    // 23:30 UTC on 31 Dec is already New Year in Rome (CET, UTC+1).
    expect(todayInRome(new Date('2026-12-31T23:30:00Z'))).toBe('2027-01-01')
    expect(todayInRome(new Date('2026-09-17T10:00:00Z'))).toBe('2026-09-17')
  })
})

describe('addDays and daysBetween', () => {
  it('moves across month, year and DST boundaries by whole days', () => {
    expect(addDays('2026-09-30', 1)).toBe('2026-10-01')
    expect(addDays('2027-01-01', -1)).toBe('2026-12-31')
    expect(addDays('2026-10-24', 2)).toBe('2026-10-26') // DST ends 25 Oct
    expect(daysBetween('2026-09-17', '2026-09-24')).toBe(7)
    expect(daysBetween('2026-09-17', '2026-09-11')).toBe(-6)
  })
})

describe('dateWindow', () => {
  it('lists past days, today and forecast days in order', () => {
    const days = dateWindow('2026-09-17', { pastDays: 2, forecastDays: 3 })
    expect(days).toEqual([
      { date: '2026-09-15', offset: -2, kind: 'past' },
      { date: '2026-09-16', offset: -1, kind: 'past' },
      { date: '2026-09-17', offset: 0, kind: 'today' },
      { date: '2026-09-18', offset: 1, kind: 'forecast' },
      { date: '2026-09-19', offset: 2, kind: 'forecast' },
      { date: '2026-09-20', offset: 3, kind: 'forecast' },
    ])
  })
})

describe('formatDay', () => {
  it('formats a calendar day in the UI language without shifting it', () => {
    expect(formatDay('2026-09-17', 'it-IT')).toEqual({ weekday: 'gio', day: '17' })
    expect(formatDay('2026-09-17', 'en-GB')).toEqual({ weekday: 'Thu', day: '17' })
    expect(formatDayLong('2026-09-17', 'it-IT')).toBe('giovedì 17 settembre')
    expect(formatDayLong('2026-09-17', 'en-GB')).toBe('Thursday 17 September')
  })
})
