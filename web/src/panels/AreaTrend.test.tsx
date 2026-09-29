import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { TrendResponse } from '../api/queries'
import { AreaTrend } from './AreaTrend'

const TODAY = '2026-09-29'

const TREND: TrendResponse = {
  species: 'porcini',
  area: { code: '048001', name: 'Poppi', kind: 'comune' },
  days: [
    { date: '2026-09-27', score: 0.3 },
    { date: '2026-09-28', score: 0.4 },
    { date: '2026-09-29', score: 0.5 },
  ],
}

const state = {
  data: TREND,
  isLoading: false,
  isError: false,
  onRetry: () => {},
  today: TODAY,
}

describe('AreaTrend', () => {
  it("draws the zone's line under its heading", () => {
    render(
      <AreaTrend trend={state} species="porcini" comune="048001" regionName="Toscana" />,
    )
    expect(
      screen.getByRole('region', { name: 'Andamento degli ultimi 15 giorni' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('img', { name: /^Poppi, ultimi 15 giorni/ }),
    ).toBeInTheDocument()
  })

  it("waits rather than showing another zone's line", () => {
    render(
      <AreaTrend
        trend={{ ...state, isLoading: true }}
        species="porcini"
        comune={null}
        regionName="Toscana"
      />,
    )
    expect(screen.queryByRole('img')).not.toBeInTheDocument()
    expect(screen.getByText("Carico l'andamento…")).toBeInTheDocument()
  })

  it('says so when no day was scored', () => {
    render(
      <AreaTrend
        trend={{ ...state, data: { ...TREND, days: [] } }}
        species="porcini"
        comune="048001"
        regionName="Toscana"
      />,
    )
    expect(
      screen.getByText('Nessun indice calcolato negli ultimi 15 giorni.'),
    ).toBeInTheDocument()
  })

  it('offers a retry when it cannot load', async () => {
    const onRetry = vi.fn()
    render(
      <AreaTrend
        trend={{ ...state, data: undefined, isError: true, onRetry }}
        species="porcini"
        comune={null}
        regionName="Toscana"
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Riprova' }))
    expect(onRetry).toHaveBeenCalled()
  })
})
