import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { InstallBanner } from './InstallBanner'

function beforeInstallPrompt() {
  const event = new Event('beforeinstallprompt', { cancelable: true }) as Event & {
    prompt: () => Promise<void>
    userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
  }
  event.prompt = vi.fn(() => Promise.resolve())
  event.userChoice = Promise.resolve({ outcome: 'accepted' })
  return event
}

afterEach(() => localStorage.clear())

describe('InstallBanner', () => {
  it('stays hidden until the browser offers to install', () => {
    render(<InstallBanner />)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('offers to install, then prompts on click', async () => {
    render(<InstallBanner />)
    const event = beforeInstallPrompt()
    act(() => window.dispatchEvent(event))

    await userEvent.click(screen.getByRole('button', { name: 'Installa' }))
    expect(event.prompt).toHaveBeenCalled()
  })

  it('stays dismissed for this visitor once closed', async () => {
    const { unmount } = render(<InstallBanner />)
    act(() => window.dispatchEvent(beforeInstallPrompt()))
    await userEvent.click(screen.getByRole('button', { name: 'Non ora' }))
    expect(screen.queryByRole('status')).not.toBeInTheDocument()

    unmount()
    render(<InstallBanner />)
    act(() => window.dispatchEvent(beforeInstallPrompt()))
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })
})
