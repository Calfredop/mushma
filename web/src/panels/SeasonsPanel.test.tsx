import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { REGIONS } from '../regions'
import { PLAUSIBLE, SEASON_MAP, SEASONS } from '../test/fixtures'
import { SeasonsPanel } from './SeasonsPanel'

const props = {
  species: 'porcini' as const,
  region: REGIONS.toscana,
  comuni: [
    {
      code: '046009',
      name: 'Careggine',
      province: 'LU',
      lon: 10.3,
      lat: 44.1,
      cells: 20,
    },
  ],
  comune: null,
  onComune: () => {},
  seasons: SEASONS,
  isLoading: false,
  isError: false,
  onRetry: () => {},
  selected: null,
  onSelect: () => {},
  seasonMap: undefined,
  onReplayDay: () => {},
  sightingsVisible: false,
  onSightingsVisibleChange: () => {},
}

describe('SeasonsPanel', () => {
  it("calls the whole region by the region's name, and offers it in its own words", () => {
    render(<SeasonsPanel {...props} region={REGIONS.piemonte} />)
    expect(screen.getByText('Porcini · Piemonte')).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Tutto il Piemonte' })).toBeInTheDocument()
  })

  it('lists the seasons newest first, the one under way marked "so far"', () => {
    render(<SeasonsPanel {...props} />)
    const rows = screen.getAllByRole('button', { pressed: false })
    expect(rows[0]).toHaveAccessibleName(
      '2026: 4 giorni favorevoli finora, tipico 19, pioggia al 87% del normale, temperatura +1,7 °C rispetto al normale',
    )
    expect(rows[1]).toHaveAccessibleName(/^2025: 62 giorni favorevoli, tipico 50/)
    expect(
      screen.getByText(
        'Tipico: il valore di mezzo delle stagioni 2022–2025 (metà sopra, metà sotto)',
      ),
    ).toBeInTheDocument()
  })

  it('puts a season on the map, and takes it off again', async () => {
    const onSelect = vi.fn()
    const { rerender } = render(<SeasonsPanel {...props} onSelect={onSelect} />)
    await userEvent.click(screen.getByRole('button', { name: /^2025:/ }))
    expect(onSelect).toHaveBeenLastCalledWith(2025)

    rerender(<SeasonsPanel {...props} onSelect={onSelect} selected={2025} />)
    await userEvent.click(screen.getByRole('button', { name: /^2025:/, pressed: true }))
    expect(onSelect).toHaveBeenLastCalledWith(null)
  })

  it('explains a chosen season and replays its best day', async () => {
    const onReplayDay = vi.fn()
    const onComune = vi.fn()
    render(
      <SeasonsPanel
        {...props}
        selected={2025}
        seasonMap={SEASON_MAP}
        onReplayDay={onReplayDay}
        onComune={onComune}
      />,
    )
    expect(screen.getByText('Meglio del solito')).toBeInTheDocument()
    expect(screen.getByText(/24 set, favorevole il 87% del bosco/)).toBeInTheDocument()
    expect(screen.getByText('1150 mm, il 115% del normale')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Rivedilo sulla mappa' }))
    expect(onReplayDay).toHaveBeenCalledWith('2025-09-24')

    await userEvent.click(
      screen.getByRole('button', { name: 'Guarda le stagioni di Careggine' }),
    )
    expect(onComune).toHaveBeenCalledWith('046009')
  })

  it('says so when an area has no seasons yet', () => {
    render(<SeasonsPanel {...props} seasons={{ ...SEASONS, seasons: [] }} />)
    expect(screen.getByText(/nessuna stagione calcolata/)).toBeInTheDocument()
  })

  it('switches the area', async () => {
    const onComune = vi.fn()
    render(<SeasonsPanel {...props} onComune={onComune} />)
    await userEvent.selectOptions(
      screen.getByRole('combobox', { name: 'Zona' }),
      '046009',
    )
    expect(onComune).toHaveBeenCalledWith('046009')
  })

  it("breaks a zone's chosen season down by species and taxon", () => {
    render(
      <SeasonsPanel
        {...props}
        comune="046009"
        seasons={{ ...SEASONS, area: PLAUSIBLE.area }}
        selected={2025}
        plausible={{
          data: PLAUSIBLE,
          isLoading: false,
          isError: false,
          onRetry: () => {},
        }}
      />,
    )
    expect(
      screen.getByRole('list', { name: 'Specie adatte alla zona' }),
    ).toBeInTheDocument()
    const byDays = screen.getByRole('list', { name: 'Giorni favorevoli per specie' })
    const lines = within(byDays)
      .getAllByRole('listitem')
      .map((item) => item.firstElementChild?.textContent)
    expect(lines).toEqual([
      'GallinacciCantharellus cibarius s.l.71',
      'PorciniBoletus edulis e affini62',
      'Boletus edulis40',
      'Boletus reticulatus21',
      'Boletus pinophilus12',
      'Boletus aereus3',
      'OvoliAmanita caesarea0',
    ])
  })

  it('shows no species breakdown for the whole region', () => {
    render(
      <SeasonsPanel
        {...props}
        selected={2025}
        plausible={{
          data: undefined,
          isLoading: false,
          isError: false,
          onRetry: () => {},
        }}
      />,
    )
    expect(screen.queryByText('Specie adatte alla zona')).not.toBeInTheDocument()
    expect(screen.queryByText('Giorni favorevoli per specie')).not.toBeInTheDocument()
  })
})
