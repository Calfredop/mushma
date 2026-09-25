import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { RegionSwitcher } from './RegionSwitcher'
import { REGIONS } from '../regions'

describe('RegionSwitcher', () => {
  it('lists every served region and navigates on pick', async () => {
    const onChange = vi.fn()
    render(<RegionSwitcher value={REGIONS.toscana} onChange={onChange} />)
    await userEvent.click(screen.getByRole('button', { name: 'Regione' }))
    await userEvent.click(screen.getByRole('option', { name: 'Umbria' }))
    expect(onChange).toHaveBeenCalledWith('umbria')
  })
})
