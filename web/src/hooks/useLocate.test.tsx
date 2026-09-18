import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { useLocate } from './useLocate'

function mockGeolocation(result: { lat: number; lon: number } | { code: number }) {
  const getCurrentPosition = vi.fn(
    (success: PositionCallback, failure: PositionErrorCallback) => {
      if ('code' in result) {
        failure({ code: result.code, PERMISSION_DENIED: 1 } as GeolocationPositionError)
      } else {
        success({
          coords: { latitude: result.lat, longitude: result.lon },
        } as GeolocationPosition)
      }
    },
  )
  vi.stubGlobal('navigator', { ...navigator, geolocation: { getCurrentPosition } })
}

afterEach(() => vi.unstubAllGlobals())

describe('useLocate', () => {
  it('reports a fix inside Tuscany', () => {
    mockGeolocation({ lat: 43.85, lon: 11.73 })
    const onLocated = vi.fn()
    const onError = vi.fn()
    const { result } = renderHook(() => useLocate({ onLocated, onError }))
    act(() => result.current.locate())
    expect(onLocated).toHaveBeenCalledWith(43.85, 11.73)
    expect(onError).not.toHaveBeenCalled()
  })

  it('refuses a fix outside the region', () => {
    mockGeolocation({ lat: 45.46, lon: 9.19 }) // Milan
    const onError = vi.fn()
    const { result } = renderHook(() => useLocate({ onLocated: vi.fn(), onError }))
    act(() => result.current.locate())
    expect(onError).toHaveBeenCalledWith('outside')
  })

  it('tells denied permission apart from other failures', () => {
    const onError = vi.fn()
    mockGeolocation({ code: 1 })
    const denied = renderHook(() => useLocate({ onLocated: vi.fn(), onError }))
    act(() => denied.result.current.locate())
    mockGeolocation({ code: 3 })
    const timeout = renderHook(() => useLocate({ onLocated: vi.fn(), onError }))
    act(() => timeout.result.current.locate())
    expect(onError.mock.calls).toEqual([['denied'], ['unavailable']])
  })
})
