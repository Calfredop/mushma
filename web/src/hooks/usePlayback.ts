import { useCallback, useEffect, useState } from 'react'
import type { IsoDate } from '../time/days'

interface Options {
  /** The days to step through, in order; it loops back to the first. */
  days: readonly IsoDate[]
  date: IsoDate
  onDate: (date: IsoDate) => void
  /** Called for the next days ahead of time, so a step never waits on the network. */
  prefetch: (date: IsoDate) => void
  /** Off (the mode left, a replayed day, a season on the map): playback stops. */
  enabled: boolean
  stepMs?: number
  ahead?: number
}

/** Analysis mode's play button: one day a second through the date strip, looping. */
export function usePlayback({
  days,
  date,
  onDate,
  prefetch,
  enabled,
  stepMs = 1000,
  ahead = 2,
}: Options) {
  const [playing, setPlaying] = useState(false)
  // Stopped for good when it can't play, rather than resuming when it can again.
  const [wasEnabled, setWasEnabled] = useState(enabled)
  if (enabled !== wasEnabled) {
    setWasEnabled(enabled)
    if (!enabled) setPlaying(false)
  }
  const active = playing && enabled

  useEffect(() => {
    if (!active || days.length === 0) return
    const at = days.indexOf(date)
    const next = (k: number) => days[(at + k) % days.length]
    for (let k = 1; k <= ahead; k++) prefetch(next(k))
    const timer = setTimeout(() => onDate(next(1)), stepMs)
    return () => clearTimeout(timer)
  }, [active, date, days, onDate, prefetch, stepMs, ahead])

  const toggle = useCallback(() => setPlaying((value) => !value), [])
  const pause = useCallback(() => setPlaying(false), [])
  return { playing: active, toggle, pause }
}
