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

/** A day in full with its year, for a replayed past day: "sabato 12 ottobre 2024". */
export function formatDateFull(date: IsoDate, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(toUtc(date))
}

/** Day and short month, for period labels: "28 set". */
export function formatDayMonth(date: IsoDate, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    month: 'short',
    timeZone: 'UTC',
  })
    .format(toUtc(date))
    .replace('.', '')
}

/**
 * A generation timestamp (`/status`'s `updated_at`, a full ISO datetime, not a calendar day) in
 * Europe/Rome (AGENTS.md → Time): "18 set, 07:02".
 */
export function formatUpdatedAt(iso: string, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Europe/Rome',
  })
    .format(new Date(iso))
    .replace('.', '')
}

/** A month (1–12) by name: "ott", or "ottobre" with `long`. */
export function formatMonth(
  month: number,
  locale: string,
  width: 'short' | 'long' = 'short',
): string {
  const date = `2001-${String(month).padStart(2, '0')}-01`
  return new Intl.DateTimeFormat(locale, { month: width, timeZone: 'UTC' })
    .format(toUtc(date))
    .replace('.', '')
}

/** The same calendar day a year earlier; 29 February becomes the 28th. */
export function sameDayLastYear(date: IsoDate): IsoDate {
  const [year, month, day] = date.split('-').map(Number)
  const candidate = `${year - 1}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  const parsed = new Date(`${candidate}T00:00:00Z`)
  return parsed.toISOString().slice(0, 10) === candidate
    ? candidate
    : `${year - 1}-${String(month).padStart(2, '0')}-28`
}
