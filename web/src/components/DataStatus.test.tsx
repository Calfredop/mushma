import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { DataStatus } from './DataStatus'

afterEach(() => vi.useRealTimers())

describe('DataStatus', () => {
  it('shows the offline indicator and ignores updatedAt while offline', () => {
    render(<DataStatus online={false} updatedAt="2026-09-18T05:02:00Z" />)
    expect(screen.getByRole('status')).toHaveTextContent('Offline')
  })

  it('renders nothing while online with no status yet', () => {
    render(<DataStatus online={true} updatedAt={undefined} />)
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('shows a plain "updated" line for a recent run', () => {
    vi.useFakeTimers().setSystemTime(new Date('2026-09-18T06:00:00Z'))
    render(<DataStatus online={true} updatedAt="2026-09-18T05:02:00Z" />)
    const status = screen.getByRole('status')
    expect(status).toHaveTextContent('Aggiornato 18 set, 07:02')
    expect(status).not.toHaveAttribute('data-stale')
  })

  it('warns when the last run is older than the stale threshold', () => {
    vi.useFakeTimers().setSystemTime(new Date('2026-09-19T12:00:00Z')) // 31h later
    render(<DataStatus online={true} updatedAt="2026-09-18T05:02:00Z" />)
    const status = screen.getByRole('status')
    expect(status).toHaveTextContent("L'ultimo aggiornamento")
    expect(status).toHaveAttribute('data-stale', 'true')
  })
})
