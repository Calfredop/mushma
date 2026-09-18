import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { HOTSPOTS } from '../test/fixtures'
import { HotPlaces } from './HotPlaces'

const props = {
  species: 'porcini' as const,
  date: '2026-09-17',
  isLoading: false,
  isError: false,
  onRetry: () => {},
  onSelect: () => {},
  sightingsVisible: false,
  onSightingsVisibleChange: () => {},
  sightingsError: false,
}

describe('HotPlaces', () => {
  it('ranks places and opens one on the map', async () => {
    const onSelect = vi.fn()
    render(<HotPlaces {...props} hotspots={HOTSPOTS} onSelect={onSelect} />)
    const items = screen.getAllByRole('listitem')
    expect(items[0]).toHaveTextContent('Bagnolo')
    expect(items[0]).toHaveTextContent('2 celle · 3 avvistamenti recenti')
    expect(items[1]).toHaveTextContent('1 cella')
    expect(items[1]).not.toHaveTextContent('avvistament')

    await userEvent.click(screen.getByRole('button', { name: /Camaldoli/ }))
    expect(onSelect).toHaveBeenCalledWith(HOTSPOTS[1])
  })

  it('says when nothing is favourable', () => {
    render(<HotPlaces {...props} hotspots={[]} />)
    expect(screen.getByText(/Nessuna zona con condizioni favorevoli/)).toBeInTheDocument()
  })

  it('toggles the sightings overlay, which only ever shows counts per cell', async () => {
    const onChange = vi.fn()
    render(
      <HotPlaces {...props} hotspots={HOTSPOTS} onSightingsVisibleChange={onChange} />,
    )
    expect(screen.getByText(/mai posizioni esatte/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('switch', { name: /Avvistamenti pubblici/ }))
    expect(onChange).toHaveBeenCalledWith(true)
  })
})
