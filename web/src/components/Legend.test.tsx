import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { Legend } from './Legend'

describe('Legend', () => {
  it('shows the whole key where there is room for it', () => {
    render(<Legend showSightings={false} />)
    expect(screen.getByRole('heading', { name: 'Indice delle condizioni' })).toBeVisible()
    expect(screen.getByText('Previsione')).toBeVisible()
    expect(screen.queryByRole('button', { name: 'Legenda' })).not.toBeInTheDocument()
  })

  it('folds into one chip that opens to the whole key and closes again', async () => {
    render(<Legend showSightings collapsible />)
    const chip = screen.getByRole('button', { name: 'Legenda' })
    expect(chip).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('heading', { name: 'Indice delle condizioni' })).toBeNull()

    await userEvent.click(chip)
    expect(chip).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('heading', { name: 'Indice delle condizioni' })).toBeVisible()
    expect(screen.getByText('Avvistamenti per cella')).toBeVisible()

    await userEvent.click(chip)
    expect(chip).toHaveAttribute('aria-expanded', 'false')
  })

  it("keeps a season's title in the page while folded", () => {
    render(<Legend showSightings={false} season={2025} collapsible />)
    expect(screen.getByText('Giorni favorevoli nel 2025')).toBeInTheDocument()
    expect(screen.getByText('Giorni favorevoli nel 2025')).not.toBeVisible()
  })
})
