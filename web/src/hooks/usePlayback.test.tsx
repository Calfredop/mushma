import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { usePlayback } from './usePlayback'

const days = ['2026-09-17', '2026-09-18', '2026-09-19', '2026-09-20']

beforeEach(() => vi.useFakeTimers())
afterEach(() => vi.useRealTimers())

describe('usePlayback', () => {
  it('steps a day a second and loops back to the first day', () => {
    const onDate = vi.fn()
    const { result } = renderHook(() =>
      usePlayback({
        days,
        date: '2026-09-19',
        onDate,
        prefetch: () => {},
        enabled: true,
      }),
    )
    expect(result.current.playing).toBe(false)
    act(() => result.current.toggle())
    expect(result.current.playing).toBe(true)
    act(() => vi.advanceTimersByTime(999))
    expect(onDate).not.toHaveBeenCalled()
    act(() => vi.advanceTimersByTime(1))
    expect(onDate).toHaveBeenCalledWith('2026-09-20')
  })

  it('goes on from the day it lands on, round the strip', () => {
    const dates: string[] = []
    let date = '2026-09-19'
    const { result, rerender } = renderHook(() =>
      usePlayback({
        days,
        date,
        onDate: (next) => {
          dates.push(next)
          date = next
        },
        prefetch: () => {},
        enabled: true,
      }),
    )
    act(() => result.current.toggle())
    for (let i = 0; i < 3; i++) {
      act(() => vi.advanceTimersByTime(1000))
      rerender()
    }
    expect(dates).toEqual(['2026-09-20', '2026-09-17', '2026-09-18'])
  })

  it('fetches the next two days ahead', () => {
    const prefetch = vi.fn()
    const { result } = renderHook(() =>
      usePlayback({
        days,
        date: '2026-09-19',
        onDate: () => {},
        prefetch,
        enabled: true,
      }),
    )
    act(() => result.current.toggle())
    expect(prefetch.mock.calls.map(([d]) => d)).toEqual(['2026-09-20', '2026-09-17'])
  })

  it('pauses, and stops for good when it can no longer play', () => {
    const onDate = vi.fn()
    const { result, rerender } = renderHook(
      ({ enabled }) =>
        usePlayback({ days, date: '2026-09-19', onDate, prefetch: () => {}, enabled }),
      { initialProps: { enabled: true } },
    )
    act(() => result.current.toggle())
    act(() => result.current.pause())
    act(() => vi.advanceTimersByTime(3000))
    expect(onDate).not.toHaveBeenCalled()

    act(() => result.current.toggle())
    rerender({ enabled: false })
    expect(result.current.playing).toBe(false)
    rerender({ enabled: true })
    expect(result.current.playing).toBe(false)
    act(() => vi.advanceTimersByTime(3000))
    expect(onDate).not.toHaveBeenCalled()
  })
})
