import { act, renderHook, waitFor } from '@testing-library/react'
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
  it('reports a fix inside Tuscany', async () => {
    mockGeolocation({ lat: 43.85, lon: 11.73 })
    const onLocated = vi.fn()
    const onError = vi.fn()
    const { result } = renderHook(() => useLocate({ onLocated, onError }))
    act(() => result.current.locate())
    await waitFor(() => expect(onLocated).toHaveBeenCalledWith(43.85, 11.73))
    expect(onError).not.toHaveBeenCalled()
  })

  it('refuses a fix in another region when it has no switch to offer', async () => {
    mockGeolocation({ lat: 45.46, lon: 9.19 }) // Milan
    const onError = vi.fn()
    const { result } = renderHook(() => useLocate({ onLocated: vi.fn(), onError }))
    act(() => result.current.locate())
    await waitFor(() => expect(onError).toHaveBeenCalledWith('outside'))
  })

  it('refuses a fix outside every served region', async () => {
    mockGeolocation({ lat: 48.14, lon: 11.58 }) // Munich
    const onError = vi.fn()
    const onOtherRegion = vi.fn()
    const { result } = renderHook(() =>
      useLocate({ onLocated: vi.fn(), onError, onOtherRegion }),
    )
    act(() => result.current.locate())
    await waitFor(() => expect(onError).toHaveBeenCalledWith('outside'))
    expect(onOtherRegion).not.toHaveBeenCalled()
  })

  it('offers another served region when the fix lands there', async () => {
    mockGeolocation({ lat: 42.9, lon: 12.5 }) // Umbria
    const onOtherRegion = vi.fn()
    const onError = vi.fn()
    const { result } = renderHook(() =>
      useLocate({
        onLocated: vi.fn(),
        onError,
        region: 'toscana',
        onOtherRegion,
      }),
    )
    act(() => result.current.locate())
    await waitFor(() => expect(onOtherRegion).toHaveBeenCalledWith('umbria', 42.9, 12.5))
    expect(onError).not.toHaveBeenCalled()
  })

  it('offers Marche for a fix in Fabriano from Umbria, whose bbox holds it', async () => {
    mockGeolocation({ lat: 43.33, lon: 12.9 })
    const onLocated = vi.fn()
    const onOtherRegion = vi.fn()
    const { result } = renderHook(() =>
      useLocate({ onLocated, onError: vi.fn(), region: 'umbria', onOtherRegion }),
    )
    act(() => result.current.locate())
    await waitFor(() => expect(onOtherRegion).toHaveBeenCalledWith('marche', 43.33, 12.9))
    expect(onLocated).not.toHaveBeenCalled()
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
