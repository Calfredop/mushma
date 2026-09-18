import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { DateStrip } from './DateStrip'

describe('DateStrip', () => {
  it('lists past days, today and forecast days, marking forecasts', () => {
    render(
      <DateStrip
        today="2026-09-17"
        value="2026-09-17"
        window={{ pastDays: 2, forecastDays: 2 }}
        onChange={() => {}}
      />,
    )
    const days = within(screen.getByRole('radiogroup', { name: 'Giorno' })).getAllByRole(
      'radio',
    )
    expect(days).toHaveLength(5)
    expect(days.map((d) => d.getAttribute('data-kind'))).toEqual([
      'past',
      'past',
      'today',
      'forecast',
      'forecast',
    ])
    expect(days[2]).toHaveAttribute('aria-checked', 'true')
    expect(days[2]).toHaveTextContent('Oggi')
    expect(days[3]).toHaveAccessibleName('venerdì 18 settembre, previsione')
    expect(days[0]).toHaveAccessibleName('martedì 15 settembre, dati osservati')
  })

  it('selects a day', async () => {
    const onChange = vi.fn()
    render(
      <DateStrip
        today="2026-09-17"
        value="2026-09-17"
        window={{ pastDays: 1, forecastDays: 1 }}
        onChange={onChange}
      />,
    )
    await userEvent.click(
      screen.getByRole('radio', { name: 'venerdì 18 settembre, previsione' }),
    )
    expect(onChange).toHaveBeenCalledWith('2026-09-18')
  })
})
