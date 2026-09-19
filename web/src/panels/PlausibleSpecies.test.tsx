import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { PLAUSIBLE } from '../test/fixtures'
import { PlausibleSpecies } from './PlausibleSpecies'

const state = { data: PLAUSIBLE, isLoading: false, isError: false, onRetry: () => {} }

const rows = (list: HTMLElement) =>
  within(list)
    .getAllByRole('listitem')
    .map((item) => item.firstElementChild?.textContent)

describe('PlausibleSpecies', () => {
  it('ranks the species by how much of the zone suits them', () => {
    render(<PlausibleSpecies plausible={state} />)
    const list = screen.getByRole('list', { name: 'Specie plausibili' })
    expect(rows(list)).toEqual([
      'PorciniBoletus edulis e affini92%',
      'Boletus reticulatus85%',
      'Boletus edulis61%',
      'Boletus pinophilus30%',
      'Boletus aereus7%',
      'GallinacciCantharellus cibarius s.l.70%',
      'OvoliAmanita caesarea4%',
    ])
  })

  it('breaks porcini down by taxon, a one-taxon group on its own line', () => {
    render(<PlausibleSpecies plausible={state} />)
    const porcini = screen.getByRole('list', { name: 'Porcini' })
    expect(within(porcini).getAllByRole('listitem')).toHaveLength(4)
    expect(screen.queryByRole('list', { name: 'Ovoli' })).not.toBeInTheDocument()
  })

  it('says so when no species suits the zone', () => {
    const none = {
      ...PLAUSIBLE,
      species: PLAUSIBLE.species.map((s) => ({
        ...s,
        fit_share: 0,
        taxa: s.taxa.map((t) => ({ ...t, fit_share: 0 })),
      })),
    }
    render(<PlausibleSpecies plausible={{ ...state, data: none }} />)
    expect(
      screen.getByText('In questa zona nessuna delle tre specie trova bosco adatto.'),
    ).toBeInTheDocument()
  })

  it('offers a retry when it cannot load', async () => {
    const onRetry = vi.fn()
    render(
      <PlausibleSpecies
        plausible={{ data: undefined, isLoading: false, isError: true, onRetry }}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Riprova' }))
    expect(onRetry).toHaveBeenCalled()
  })
})
