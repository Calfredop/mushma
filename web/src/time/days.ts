/**
 * Calendar days as ISO `YYYY-MM-DD` strings in Europe/Rome (AGENTS.md → Time).
 * Arithmetic runs on UTC midnights so DST never shifts a day.
 */

export type IsoDate = string

export type DayKind = 'past' | 'today' | 'forecast'

export interface WindowDay {
  date: IsoDate
  /** Days from today: negative in the past, positive in the forecast. */
  offset: number
  kind: DayKind
}

const ROME_DAY = new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Europe/Rome',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
})

const MS_PER_DAY = 86_400_000

export function todayInRome(now: Date = new Date()): IsoDate {
  return ROME_DAY.format(now)
}

function toUtc(date: IsoDate): Date {
  return new Date(`${date}T00:00:00Z`)
}

export function addDays(date: IsoDate, days: number): IsoDate {
  return new Date(toUtc(date).getTime() + days * MS_PER_DAY).toISOString().slice(0, 10)
}

export function daysBetween(from: IsoDate, to: IsoDate): number {
  return Math.round((toUtc(to).getTime() - toUtc(from).getTime()) / MS_PER_DAY)
}

export function dateWindow(
  today: IsoDate,
  { pastDays, forecastDays }: { pastDays: number; forecastDays: number },
): WindowDay[] {
  const days: WindowDay[] = []
  for (let offset = -pastDays; offset <= forecastDays; offset++) {
    const kind: DayKind = offset < 0 ? 'past' : offset === 0 ? 'today' : 'forecast'
    days.push({ date: addDays(today, offset), offset, kind })
  }
  return days
}

export function formatDay(
  date: IsoDate,
  locale: string,
): { weekday: string; day: string } {
  const utc = toUtc(date)
  return {
    weekday: new Intl.DateTimeFormat(locale, { weekday: 'short', timeZone: 'UTC' })
      .format(utc)
      .replace('.', ''),
    day: new Intl.DateTimeFormat(locale, { day: 'numeric', timeZone: 'UTC' }).format(utc),
  }
}

export function formatDayLong(date: IsoDate, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    timeZone: 'UTC',
  }).format(toUtc(date))
}
