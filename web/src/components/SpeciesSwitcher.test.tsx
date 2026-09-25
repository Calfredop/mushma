import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { SPECIES } from '../state/urlState'
import { SpeciesSwitcher } from './SpeciesSwitcher'

describe('SpeciesSwitcher', () => {
  it('offers every species and Tutte', async () => {
    const onChange = vi.fn()
    render(<SpeciesSwitcher value="porcini" onChange={onChange} species={SPECIES} />)
    await userEvent.click(screen.getByRole('radio', { name: 'Tutte' }))
    expect(onChange).toHaveBeenCalledWith('combined')
  })

  it('disables Tutte in analysis mode, which has no combined score', async () => {
    const onChange = vi.fn()
    render(
      <SpeciesSwitcher
        value="porcini"
        onChange={onChange}
        species={SPECIES}
        noCombined
      />,
    )
    const tutti = screen.getByRole('radio', { name: 'Tutte' })
    expect(tutti).toBeDisabled()
    await userEvent.click(tutti)
    expect(onChange).not.toHaveBeenCalled()
    await userEvent.click(screen.getByRole('radio', { name: 'Ovoli' }))
    expect(onChange).toHaveBeenCalledWith('ovoli')
  })

  it('only lists the species the region offers', () => {
    render(
      <SpeciesSwitcher
        value="porcini"
        onChange={vi.fn()}
        species={['porcini', 'ovoli']}
      />,
    )
    expect(screen.getByRole('radio', { name: 'Porcini' })).toBeInTheDocument()
    expect(screen.getByRole('radio', { name: 'Ovoli' })).toBeInTheDocument()
    expect(screen.queryByRole('radio', { name: 'Gallinacci' })).not.toBeInTheDocument()
  })
})
