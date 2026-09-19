import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { usePwaInstall } from './usePwaInstall'

afterEach(() => vi.unstubAllGlobals())

function beforeInstallPrompt() {
  const event = new Event('beforeinstallprompt', { cancelable: true }) as Event & {
    prompt: () => Promise<void>
    userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
  }
  event.prompt = vi.fn(() => Promise.resolve())
  event.userChoice = Promise.resolve({ outcome: 'accepted' })
  return event
}

describe('usePwaInstall', () => {
  it('is unavailable until the browser offers to install', () => {
    const { result } = renderHook(() => usePwaInstall())
    expect(result.current.available).toBe(false)
  })

  it('becomes available once the browser fires beforeinstallprompt', () => {
    const { result } = renderHook(() => usePwaInstall())
    act(() => window.dispatchEvent(beforeInstallPrompt()))
    expect(result.current.available).toBe(true)
  })

  it('prompts the deferred event and hides again once the choice resolves', async () => {
    const { result } = renderHook(() => usePwaInstall())
    const event = beforeInstallPrompt()
    act(() => window.dispatchEvent(event))
    await act(async () => result.current.install())
    expect(event.prompt).toHaveBeenCalled()
    expect(result.current.available).toBe(false)
  })

  it('hides once the app reports it was installed', () => {
    const { result } = renderHook(() => usePwaInstall())
    act(() => window.dispatchEvent(beforeInstallPrompt()))
    act(() => window.dispatchEvent(new Event('appinstalled')))
    expect(result.current.available).toBe(false)
  })

  it('never offers to install when already running standalone', () => {
    vi.stubGlobal('matchMedia', (query: string) => ({
      matches: query === '(display-mode: standalone)',
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }))
    const { result } = renderHook(() => usePwaInstall())
    act(() => window.dispatchEvent(beforeInstallPrompt()))
    expect(result.current.available).toBe(false)
  })
})
