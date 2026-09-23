import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { TimeBar } from './TimeBar'

const props = {
  today: '2026-09-18',
  date: '2026-09-18',
  window: { pastDays: 6, forecastDays: 7 },
  historyStart: '2016-01-01',
  season: null,
  seasons: [2022, 2023, 2024, 2025, 2026],
  onDate: () => {},
  onSeason: () => {},
}

describe('TimeBar', () => {
  it('opens a calendar next to the date strip to replay a past day', async () => {
    const onDate = vi.fn()
    render(<TimeBar {...props} onDate={onDate} />)
    expect(screen.getByRole('radiogroup', { name: 'Giorno' })).toBeInTheDocument()

    await userEvent.click(
      screen.getByRole('button', { name: 'Rivedi un giorno passato' }),
    )
    fireEvent.change(screen.getByLabelText('Giorno da rivedere'), {
      target: { value: '2024-10-12' },
    })
    // Typing a date doesn't jump to it on every keystroke: the Replay button does.
    expect(onDate).not.toHaveBeenCalled()
    await userEvent.click(screen.getByRole('button', { name: 'Rivedi' }))
    expect(onDate).toHaveBeenCalledWith('2024-10-12')
    expect(screen.queryByLabelText('Giorno da rivedere')).not.toBeInTheDocument()

    await userEvent.click(
      screen.getByRole('button', { name: 'Rivedi un giorno passato' }),
    )
    await userEvent.click(
      screen.getByRole('button', { name: 'Stesso giorno, un anno prima' }),
    )
    expect(onDate).toHaveBeenLastCalledWith('2025-09-18')
  })

  it('steps through a replayed day and goes back to today', async () => {
    const onDate = vi.fn()
    render(<TimeBar {...props} date="2024-10-12" onDate={onDate} />)
    expect(screen.getByText('sabato 12 ottobre 2024')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Giorno prima' }))
    expect(onDate).toHaveBeenLastCalledWith('2024-10-11')
    await userEvent.click(screen.getByRole('button', { name: 'Oggi' }))
    expect(onDate).toHaveBeenLastCalledWith('2026-09-18')
  })

  it('shows a season on the map and moves between seasons', async () => {
    const onSeason = vi.fn()
    render(<TimeBar {...props} season={2022} onSeason={onSeason} />)
    expect(screen.getByText('Stagione 2022')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Stagione precedente' })).toBeDisabled()

    await userEvent.click(screen.getByRole('button', { name: 'Stagione successiva' }))
    expect(onSeason).toHaveBeenLastCalledWith(2023)
    await userEvent.click(
      screen.getByRole('button', { name: 'Togli la stagione dalla mappa' }),
    )
    expect(onSeason).toHaveBeenLastCalledWith(null)
  })
})

describe('TimeBar in analysis mode', () => {
  it('has a play button beside the strip, and touching the strip pauses', async () => {
    const onToggle = vi.fn()
    const onTouch = vi.fn()
    const { rerender } = render(
      <TimeBar {...props} playback={{ playing: false, onToggle, onTouch }} />,
    )
    await userEvent.click(screen.getByRole('button', { name: 'Riproduci i giorni' }))
    expect(onToggle).toHaveBeenCalledTimes(1)
    expect(onTouch).not.toHaveBeenCalled()

    rerender(<TimeBar {...props} playback={{ playing: true, onToggle, onTouch }} />)
    expect(screen.getByRole('button', { name: 'Metti in pausa' })).toHaveAttribute(
      'aria-pressed',
      'true',
    )
    await userEvent.click(screen.getAllByRole('radio', { name: /previsione$/ })[0])
    expect(onTouch).toHaveBeenCalled()
  })

  it('keeps the forecast hatch on the strip', () => {
    render(
      <TimeBar
        {...props}
        playback={{ playing: false, onToggle: () => {}, onTouch: () => {} }}
      />,
    )
    const forecast = screen
      .getAllByRole('radio')
      .filter((day) => day.getAttribute('data-kind') === 'forecast')
    expect(forecast).toHaveLength(7)
  })

  it('has no play button on a replayed day or a season', () => {
    const playback = { playing: false, onToggle: () => {}, onTouch: () => {} }
    const { rerender } = render(
      <TimeBar {...props} date="2024-10-12" playback={playback} />,
    )
    expect(screen.queryByRole('button', { name: 'Riproduci i giorni' })).toBeNull()
    rerender(<TimeBar {...props} season={2024} playback={playback} />)
    expect(screen.queryByRole('button', { name: 'Riproduci i giorni' })).toBeNull()
  })
})
