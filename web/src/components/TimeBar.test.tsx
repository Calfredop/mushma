import { fireEvent, render, screen, within } from '@testing-library/react'
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

  it('expands the date strip into a month calendar, bounded by the history and the forecast', async () => {
    const onDate = vi.fn()
    render(<TimeBar {...props} onDate={onDate} />)
    const toggle = screen.getByRole('button', { name: 'Mostra il calendario' })
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('group', { name: 'Calendario' })).not.toBeInTheDocument()

    await userEvent.click(toggle)
    const calendar = screen.getByRole('group', { name: 'Calendario' })
    expect(within(calendar).getByText('settembre 2026')).toBeInTheDocument()
    expect(
      within(calendar).getByRole('button', {
        name: 'venerdì 18 settembre, dati osservati',
      }),
    ).toHaveAttribute('aria-pressed', 'true')
    // Daily scores reach today + 7; later days are only an outlook, so they can't be picked.
    expect(
      within(calendar).getByRole('button', { name: 'venerdì 25 settembre, previsione' }),
    ).toBeEnabled()
    expect(
      within(calendar).getByRole('button', { name: 'sabato 26 settembre, previsione' }),
    ).toBeDisabled()
    expect(within(calendar).getByText(/fino a venerdì 25 settembre/)).toBeInTheDocument()
    expect(
      within(calendar).getByRole('button', { name: 'Mese successivo' }),
    ).toBeDisabled()

    // A strip day keeps the calendar open, so days can be compared.
    await userEvent.click(
      within(calendar).getByRole('button', { name: 'martedì 22 settembre, previsione' }),
    )
    expect(onDate).toHaveBeenLastCalledWith('2026-09-22')
    expect(calendar).toBeInTheDocument()

    // An older day is a replay: it goes on the map and the calendar folds away.
    await userEvent.click(
      within(calendar).getByRole('button', { name: 'Mese precedente' }),
    )
    expect(within(calendar).getByText('agosto 2026')).toBeInTheDocument()
    await userEvent.click(
      within(calendar).getByRole('button', {
        name: 'mercoledì 12 agosto, dati osservati',
      }),
    )
    expect(onDate).toHaveBeenLastCalledWith('2026-08-12')
    expect(screen.queryByRole('group', { name: 'Calendario' })).not.toBeInTheDocument()
  })

  it('stops the calendar at the first day of the history', async () => {
    render(<TimeBar {...props} historyStart="2026-09-10" />)
    await userEvent.click(screen.getByRole('button', { name: 'Mostra il calendario' }))
    expect(screen.getByRole('button', { name: 'Mese precedente' })).toBeDisabled()
    expect(
      screen.getByRole('button', { name: 'mercoledì 9 settembre, dati osservati' }),
    ).toBeDisabled()
    await userEvent.click(screen.getByRole('button', { name: 'Nascondi il calendario' }))
    expect(screen.queryByRole('group', { name: 'Calendario' })).not.toBeInTheDocument()
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
