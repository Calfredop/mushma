import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { Place } from '../geo/photon'
import { PlaceSearch } from './PlaceSearch'

const PISA: Place = { id: 'n1', name: 'Pisa', detail: 'PI', lat: 43.72, lon: 10.4 }
const searchPlaces = vi.fn(() => Promise.resolve([PISA]))
vi.mock('../geo/photon', () => ({ searchPlaces: () => searchPlaces() }))

afterEach(() => searchPlaces.mockClear())

function setup(props: Partial<Parameters<typeof PlaceSearch>[0]> = {}) {
  const onSelect = vi.fn()
  const onLocate = vi.fn()
  render(
    <QueryClientProvider client={new QueryClient()}>
      <PlaceSearch onSelect={onSelect} onLocate={onLocate} {...props} />
    </QueryClientProvider>,
  )
  return { onSelect, onLocate, input: screen.getByRole('combobox') }
}

const options = () => screen.getAllByRole('option').map((option) => option.textContent)

describe('PlaceSearch', () => {
  it('lists "La mia posizione" first as soon as the field has focus', async () => {
    const { input } = setup()
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
    expect(input).toHaveAttribute('aria-expanded', 'false')

    await userEvent.click(input)

    expect(input).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getAllByRole('option')).toHaveLength(1)
    expect(screen.getByRole('option', { name: /^La mia posizione/ })).toHaveAttribute(
      'aria-selected',
      'true',
    )
  })

  it('opens the forecast where you are from it, by tap or by Enter', async () => {
    const { input, onLocate } = setup()
    await userEvent.click(input)
    await userEvent.click(screen.getByRole('option', { name: /^La mia posizione/ }))
    expect(onLocate).toHaveBeenCalledOnce()
    // Chosen: the field lets go, so the list and a phone's keyboard close.
    expect(input).not.toHaveFocus()

    await userEvent.click(input)
    await userEvent.keyboard('{Enter}')
    expect(onLocate).toHaveBeenCalledTimes(2)
  })

  it('keeps it first, above the places found', async () => {
    const { input, onSelect, onLocate } = setup()
    await userEvent.type(input, 'Pis')
    await screen.findByRole('option', { name: /^Pisa/ })
    expect(options()).toEqual([expect.stringMatching(/^La mia posizione/), 'PisaPI'])

    await userEvent.keyboard('{ArrowDown}{Enter}')
    expect(onSelect).toHaveBeenCalledWith(PISA)
    expect(onLocate).not.toHaveBeenCalled()
  })

  it('closes its list on Escape and when the field loses focus', async () => {
    const { input } = setup()
    await userEvent.click(input)
    await userEvent.keyboard('{Escape}')
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()

    await userEvent.click(input)
    expect(screen.getByRole('listbox')).toBeInTheDocument()
    await userEvent.click(document.body)
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })

  it('without a locate action, focus alone opens nothing', async () => {
    const { input } = setup({ onLocate: undefined })
    await userEvent.click(input)
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })

  it('tells its parent when it takes focus', async () => {
    const onFocus = vi.fn()
    const { input } = setup({ onFocus })
    await userEvent.click(input)
    expect(onFocus).toHaveBeenCalledOnce()
  })
})
