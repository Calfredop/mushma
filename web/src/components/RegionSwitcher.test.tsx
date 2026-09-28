import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { RegionSwitcher } from './RegionSwitcher'
import { REGIONS } from '../regions'

describe('RegionSwitcher', () => {
  it('lists every served region and navigates on pick', async () => {
    const onChange = vi.fn()
    const onShowAll = vi.fn()
    render(
      <RegionSwitcher
        value={REGIONS.toscana}
        onChange={onChange}
        onShowAll={onShowAll}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Regione' }))
    // Search is focused on open; picking must still work (mousedown keeps focus).
    expect(screen.getByRole('searchbox', { name: 'Cerca una regione' })).toHaveFocus()
    await userEvent.click(screen.getByRole('option', { name: 'Umbria' }))
    expect(onChange).toHaveBeenCalledWith('umbria')
  })

  it('filters the list by the search query', async () => {
    render(
      <RegionSwitcher value={REGIONS.toscana} onChange={vi.fn()} onShowAll={vi.fn()} />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Regione' }))
    await userEvent.type(
      screen.getByRole('searchbox', { name: 'Cerca una regione' }),
      'umb',
    )
    expect(screen.getByRole('option', { name: 'Umbria' })).toBeInTheDocument()
    expect(screen.queryByRole('option', { name: 'Toscana' })).not.toBeInTheDocument()
  })

  it('calls onShowAll from Mostra tutte', async () => {
    const onShowAll = vi.fn()
    render(
      <RegionSwitcher value={REGIONS.toscana} onChange={vi.fn()} onShowAll={onShowAll} />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Regione' }))
    await userEvent.click(screen.getByRole('button', { name: 'Mostra tutte' }))
    expect(onShowAll).toHaveBeenCalledOnce()
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })
})
