import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { DataStatus } from './DataStatus'

afterEach(() => vi.useRealTimers())

describe('DataStatus', () => {
  it('shows the offline indicator and ignores updatedAt while offline', () => {
    render(
      <DataStatus
        online={false}
        updatedAt="2026-09-18T05:02:00Z"
        rulesVersion="abc123def456"
      />,
    )
    expect(screen.getByRole('status')).toHaveTextContent('Offline')
    expect(screen.getByRole('status')).not.toHaveTextContent('abc123')
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
    expect(status).not.toHaveTextContent('regole')
  })

  it('appends the rules version the pipeline stamped, with a tooltip', () => {
    vi.useFakeTimers().setSystemTime(new Date('2026-09-18T06:00:00Z'))
    render(
      <DataStatus
        online={true}
        updatedAt="2026-09-18T05:02:00Z"
        rulesVersion="a3f2c1b9d4e5"
      />,
    )
    const status = screen.getByRole('status')
    expect(status).toHaveTextContent('Aggiornato 18 set, 07:02')
    expect(status).toHaveTextContent('regole')
    expect(status).toHaveTextContent('a3f2c1b9d4e5')
    expect(status.querySelector('[title]')).toHaveAttribute(
      'title',
      "Versione delle regole stampata dall'ultimo calcolo della pipeline",
    )
  })

  it('warns when the last run is older than the stale threshold', () => {
    vi.useFakeTimers().setSystemTime(new Date('2026-09-19T12:00:00Z')) // 31h later
    render(
      <DataStatus
        online={true}
        updatedAt="2026-09-18T05:02:00Z"
        rulesVersion="fixtures"
      />,
    )
    const status = screen.getByRole('status')
    expect(status).toHaveTextContent("L'ultimo aggiornamento")
    expect(status).toHaveTextContent('fixtures')
    expect(status).toHaveAttribute('data-stale', 'true')
  })
})
