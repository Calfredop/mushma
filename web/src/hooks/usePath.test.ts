import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { usePath } from './usePath'

afterEach(() => {
  window.history.replaceState(null, '', '/')
})

describe('usePath', () => {
  it('reads the current pathname', () => {
    window.history.replaceState(null, '', '/toscana/porcini?date=2026-09-20')
    const { result } = renderHook(() => usePath())
    expect(result.current[0]).toBe('/toscana/porcini')
  })

  it('pushes a new path, keeping the current query string by default', () => {
    window.history.replaceState(null, '', '/toscana/porcini?date=2026-09-20')
    const { result } = renderHook(() => usePath())
    act(() => result.current[1]('/toscana/ovoli'))
    expect(window.location.pathname).toBe('/toscana/ovoli')
    expect(window.location.search).toBe('?date=2026-09-20')
  })

  it('accepts an explicit search string', () => {
    window.history.replaceState(null, '', '/?species=ovoli&date=2026-09-20')
    const { result } = renderHook(() => usePath())
    act(() => result.current[1]('/toscana/ovoli', { search: '?date=2026-09-20' }))
    expect(window.location.pathname + window.location.search).toBe(
      '/toscana/ovoli?date=2026-09-20',
    )
  })

  it('replaces instead of pushing when asked to', () => {
    window.history.replaceState(null, '', '/')
    const before = window.history.length
    const { result } = renderHook(() => usePath())
    act(() => result.current[1]('/toscana', { replace: true }))
    expect(window.location.pathname).toBe('/toscana')
    expect(window.history.length).toBe(before)
  })

  it('is a no-op when the target already matches the current URL', () => {
    window.history.replaceState(null, '', '/toscana?date=2026-09-20')
    const before = window.history.length
    const { result } = renderHook(() => usePath())
    act(() => result.current[1]('/toscana'))
    expect(window.history.length).toBe(before)
  })

  it('re-renders on popstate', () => {
    window.history.replaceState(null, '', '/toscana')
    const { result } = renderHook(() => usePath())
    act(() => {
      window.history.pushState(null, '', '/toscana/porcini')
      window.dispatchEvent(new PopStateEvent('popstate'))
    })
    expect(result.current[0]).toBe('/toscana/porcini')
  })
})
