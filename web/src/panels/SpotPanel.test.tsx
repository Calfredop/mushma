import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { CELL_DETAIL } from '../test/fixtures'
import { SpotPanel } from './SpotPanel'

const base = {
  isLoading: false,
  isError: false,
  onRetry: () => {},
  onClose: () => {},
  today: '2026-09-17',
}

describe('SpotPanel', () => {
  it('shows every species with today’s score and an 8-day outlook, forecast days marked', () => {
    render(
      <SpotPanel
        {...base}
        spot={{ kind: 'cell', cellId: CELL_DETAIL.cell_id }}
        detail={CELL_DETAIL}
        species="porcini"
        date="2026-09-17"
      />,
    )
    expect(screen.getByRole('heading', { name: 'Camaldoli' })).toBeInTheDocument()
    expect(screen.getByText('Comune di Poppi')).toBeInTheDocument()

    const porciniBars = screen.getAllByRole('button', { name: /^Porcini, / })
    expect(porciniBars).toHaveLength(8)
    expect(porciniBars[0]).toHaveAttribute('data-forecast', 'false')
    expect(porciniBars.slice(1).every((bar) => bar.dataset.forecast === 'true')).toBe(
      true,
    )
    expect(screen.getAllByRole('button', { name: /^(Ovoli|Gallinacci), / })).toHaveLength(
      16,
    )

    // The why breakdown starts on the selected species and map day.
    const why = screen.getByRole('region', { name: 'Perché questo indice' })
    expect(within(why).getByText('Porcini · giovedì 17 settembre')).toBeInTheDocument()
  })

  it('switches the why breakdown when a day bar is picked', async () => {
    render(
      <SpotPanel
        {...base}
        spot={{ kind: 'cell', cellId: CELL_DETAIL.cell_id }}
        detail={CELL_DETAIL}
        species="porcini"
        date="2026-09-17"
      />,
    )
    await userEvent.click(
      screen.getByRole('button', {
        name: 'Gallinacci, sabato 19 settembre: indice 0,73',
      }),
    )
    const why = screen.getByRole('region', { name: 'Perché questo indice' })
    expect(within(why).getByText('Gallinacci · sabato 19 settembre')).toBeInTheDocument()
    expect(
      within(why).getByText(/Questo giorno deve ancora arrivare/),
    ).toBeInTheDocument()
  })

  it('explains the best species when "All" is selected, and notes a distant nearest cell', () => {
    render(
      <SpotPanel
        {...base}
        spot={{ kind: 'point', lat: 43.95, lon: 11.7333 }}
        detail={CELL_DETAIL}
        species="combined"
        date="2026-09-10"
      />,
    )
    expect(screen.getByText(/Cella boschiva più vicina a 11,1 km/)).toBeInTheDocument()
    expect(screen.getByText(/per i giorni passati guarda la mappa/)).toBeInTheDocument()
    const why = screen.getByRole('region', { name: 'Perché questo indice' })
    expect(within(why).getByText('Gallinacci · giovedì 17 settembre')).toBeInTheDocument()
  })

  it('offers a retry when the forecast fails, and closes', async () => {
    const onRetry = vi.fn()
    const onClose = vi.fn()
    render(
      <SpotPanel
        {...base}
        isError
        onRetry={onRetry}
        onClose={onClose}
        spot={{ kind: 'cell', cellId: 'x' }}
        detail={undefined}
        species="porcini"
        date="2026-09-17"
      />,
    )
    expect(screen.getByRole('alert')).toHaveTextContent(
      'Non riesco a caricare la previsione',
    )
    await userEvent.click(screen.getByRole('button', { name: 'Riprova' }))
    await userEvent.click(screen.getByRole('button', { name: 'Chiudi la previsione' }))
    expect(onRetry).toHaveBeenCalledOnce()
    expect(onClose).toHaveBeenCalledOnce()
  })
})
