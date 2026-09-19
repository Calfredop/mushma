import { act, cleanup, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { changeLanguage } from '../i18n'
import type { FactorBreakdown } from '../score/impact'
import { WhyBreakdown } from './WhyBreakdown'

type FactorInput = Pick<FactorBreakdown, 'key' | 'value' | 'contribution'> &
  Partial<FactorBreakdown>

const day = (factors: FactorInput[], score: number) => ({
  date: '2026-09-18',
  score,
  factors: factors.map((f) => ({ i18n_key: `factor.${f.key}`, ...f })),
})

describe('WhyBreakdown', () => {
  it('lists factors in API order with how favourable each is and how much it holds back', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { key: 'season', value: 1, contribution: 1 },
            { key: 'rain_30d', value: 0.5, contribution: 0.5 },
            { key: 'frost', value: 0.25, contribution: 0.25 },
          ],
          0.125,
        )}
      />,
    )
    const section = screen.getByRole('region', { name: 'Perché questo indice' })
    expect(
      within(section).getByText('Porcini · venerdì 18 settembre'),
    ).toBeInTheDocument()
    expect(
      within(section).getByRole('img', { name: 'Indice delle condizioni 0,13 su 1' }),
    ).toBeInTheDocument()

    const rows = within(section).getAllByRole('listitem')
    expect(rows.map((row) => row.firstChild?.textContent)).toEqual([
      'Stagione',
      'Pioggia degli ultimi 30 giorni',
      'Gelate',
    ])
    expect(rows[0]).not.toHaveTextContent('frena')
    expect(rows[1]).toHaveTextContent('frena del 33%')
    expect(rows[2]).toHaveTextContent('frena del 67%')
    expect(within(rows[2]).getByRole('meter', { name: 'Gelate' })).toHaveAttribute(
      'aria-valuenow',
      '0.25',
    )
    expect(screen.queryByText(/previsione/)).not.toBeInTheDocument()
  })

  it('names the blocking factors and explains forecast days', () => {
    render(
      <WhyBreakdown
        species="ovoli"
        isForecast
        day={day(
          [
            { key: 'season', value: 0, contribution: 0 },
            { key: 'altitude', value: 0, contribution: 0 },
            { key: 'frost', value: 0.9, contribution: 0.9 },
          ],
          0,
        )}
      />,
    )
    expect(screen.getByText('Bloccato da: Stagione e Quota')).toBeInTheDocument()
    expect(screen.getByText(/Questo giorno è una previsione/)).toBeInTheDocument()
  })

  it('falls back to a readable label for a factor it has no translation for', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([{ key: 'moon_phase', value: 1, contribution: 1 }], 1)}
      />,
    )
    expect(screen.getByText('Altro fattore (moon_phase)')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Nessun fattore frena l’indice in questo giorno.'.replace('’', "'"),
      ),
    ).toBeInTheDocument()
  })
})

describe('WhyBreakdown emphasis', () => {
  it('emphasises only factors that are at zero', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { key: 'season', value: 0, contribution: 0 },
            { key: 'altitude', value: 0, contribution: 0 },
            { key: 'frost', value: 0.6, contribution: 0.6 },
          ],
          0,
        )}
      />,
    )
    const rows = screen.getAllByRole('listitem')
    expect(rows.map((row) => row.dataset.blocking)).toEqual(['true', 'true', 'false'])
  })

  it('does not emphasise a lone factor that holds back everything but is not zero', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { key: 'season', value: 1, contribution: 1 },
            { key: 'frost', value: 0.6, contribution: 0.6 },
          ],
          0.6,
        )}
      />,
    )
    expect(screen.getAllByRole('listitem').map((row) => row.dataset.blocking)).toEqual([
      'false',
      'false',
    ])
  })
})

const rainTrigger: FactorInput = {
  key: 'rain_trigger',
  value: 0.7,
  contribution: 0.85,
  role: 'driver',
  weight: 2,
  input: 42,
  unit: 'mm',
  days_ago: 6,
  rule: {
    kind: 'rain_event',
    variable: 'precipitation_sum',
    variable_unit: 'mm',
    window_days: 3,
    trapezoid: [10, 30, null, null],
    lag_days: [6, 10, 16, 24],
  },
}
const altitude: FactorInput = {
  key: 'altitude',
  value: 0.6,
  contribution: 0.6,
  role: 'gate',
  input: 640,
  unit: 'm',
  rule: {
    kind: 'static_band',
    variable: 'elevation_m',
    variable_unit: 'm',
    trapezoid: [200, 700, 1600, 1900],
  },
}
const frost: FactorInput = {
  key: 'frost',
  value: 0.6,
  contribution: 0.6,
  role: 'stopper',
  input: 2,
  unit: 'days',
  rule: {
    kind: 'count_days',
    variable: 'temperature_2m_min',
    variable_unit: '°C',
    window_days: 7,
    offset_days: 0,
    op: 'lte',
    threshold: 0,
    trapezoid: [null, null, 1, 2],
  },
}
const airTemperature: FactorInput = {
  key: 'air_temperature',
  value: 0.8,
  contribution: 0.8,
  role: 'driver',
  weight: 1,
  input: 14.2,
  unit: '°C',
  rule: {
    kind: 'window_aggregate',
    variable: 'temperature_2m_mean',
    variable_unit: '°C',
    aggregate: 'mean',
    window_days: 20,
    offset_days: 0,
    trapezoid: [6, 10, 17, 22],
  },
}
const season: FactorInput = {
  key: 'season',
  value: 1,
  contribution: 1,
  role: 'gate',
  rule: { kind: 'season_window' },
}
const habitat: FactorInput = {
  key: 'habitat',
  value: 0.8,
  contribution: 0.8,
  role: 'gate',
  rule: { kind: 'habitat' },
}

const rowOf = (name: string) =>
  screen.getByRole('button', { name }).closest('li') as HTMLElement

describe('WhyBreakdown details', () => {
  const user = userEvent.setup()

  beforeEach(() => localStorage.clear())
  afterEach(async () => {
    cleanup()
    await act(() => changeLanguage('it'))
  })

  it('keeps every row compact until asked, and opens one row on its own', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([season, rainTrigger], 0.6)}
      />,
    )
    const button = screen.getByRole('button', { name: 'Pioggia di innesco' })
    expect(button).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByText(/di pioggia in 3 giorni/)).not.toBeInTheDocument()

    await user.click(button)

    expect(button).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('button', { name: 'Stagione' })).toHaveAttribute(
      'aria-expanded',
      'false',
    )
    expect(screen.getByText(/di pioggia in 3 giorni/)).toBeInTheDocument()
  })

  it('says how much rain fell, over how long, when it ended, and what the rule wanted', async () => {
    render(
      <WhyBreakdown species="porcini" isForecast={false} day={day([rainTrigger], 0.7)} />,
    )
    await user.click(screen.getByRole('button', { name: 'Pioggia di innesco' }))
    const row = rowOf('Pioggia di innesco')
    expect(row).toHaveTextContent(
      '42 mm di pioggia in 3 giorni fino a sabato 12 settembre (6 giorni prima).',
    )
    expect(row).toHaveTextContent(
      'La regola dà credito pieno da 30 mm in su; nullo fino a 10 mm.',
    )
    expect(row).toHaveTextContent(
      'Distanza dal giorno valutato: credito pieno da 10 a 16 giorni; nullo fino a 6 giorni e da 24 giorni in su.',
    )
  })

  it("shows a gate's attribute and its band", async () => {
    render(
      <WhyBreakdown species="porcini" isForecast={false} day={day([altitude], 0.6)} />,
    )
    await user.click(screen.getByRole('button', { name: 'Quota' }))
    const row = rowOf('Quota')
    expect(row).toHaveTextContent('Per questa cella: 640 m.')
    expect(row).toHaveTextContent(
      'La regola dà credito pieno da 700 a 1600 m; nullo fino a 200 m e da 1900 m in su.',
    )
  })

  it('counts matching days against the window and the threshold', async () => {
    render(<WhyBreakdown species="porcini" isForecast={false} day={day([frost], 0.6)} />)
    await user.click(screen.getByRole('button', { name: 'Gelate' }))
    const row = rowOf('Gelate')
    expect(row).toHaveTextContent('2 giorni su 7 con temperatura minima ≤ 0 °C.')
    expect(row).toHaveTextContent(
      'La regola dà credito pieno fino a 1 giorno; nullo da 2 giorni in su.',
    )
  })

  it('names the aggregate and its window for a weather average', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([airTemperature], 0.8)}
      />,
    )
    await user.click(screen.getByRole('button', { name: "Temperatura dell'aria" }))
    const row = rowOf("Temperatura dell'aria")
    expect(row).toHaveTextContent("Temperatura dell'aria, media su 20 giorni: 14,2 °C.")
    expect(row).toHaveTextContent(
      'La regola dà credito pieno da 10 a 17 °C; nullo fino a 6 °C e da 22 °C in su.',
    )
  })

  it('gives season and habitat a plain line with no numbers', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([season, habitat], 0.8)}
      />,
    )
    await user.click(screen.getByRole('button', { name: 'Stagione' }))
    await user.click(screen.getByRole('button', { name: 'Tipo di bosco' }))
    expect(rowOf('Stagione')).toHaveTextContent(
      "Il periodo dell'anno in cui questa specie di solito fruttifica",
    )
    expect(rowOf('Tipo di bosco')).toHaveTextContent(
      'Quanto il tipo di bosco di questa cella si adatta alla specie',
    )
    for (const name of ['Stagione', 'Tipo di bosco']) {
      const detail = within(rowOf(name)).getByTestId('factor-detail')
      expect(detail).not.toHaveTextContent(/\d/)
    }
  })

  it('still renders when the day has no measurement or no rule', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { ...rainTrigger, input: null, days_ago: null },
            { key: 'frost', value: 1, contribution: 1 },
          ],
          1,
        )}
      />,
    )
    await user.click(screen.getByRole('button', { name: 'Pioggia di innesco' }))
    await user.click(screen.getByRole('button', { name: 'Gelate' }))
    expect(rowOf('Pioggia di innesco')).toHaveTextContent(
      'Misura non disponibile per questo giorno.',
    )
    expect(rowOf('Pioggia di innesco')).toHaveTextContent(
      'La regola dà credito pieno da 30 mm in su',
    )
    expect(rowOf('Gelate')).toHaveTextContent(
      'Nessun dettaglio disponibile per questo fattore.',
    )
  })

  it('opens every row with one switch, remembers it, and lets a row close on its own', async () => {
    const { unmount } = render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([season, altitude, rainTrigger], 0.5)}
      />,
    )
    const toggle = screen.getByRole('switch', { name: 'Mostra tutti i dettagli' })
    expect(toggle).toHaveAttribute('aria-checked', 'false')

    await user.click(toggle)
    expect(toggle).toHaveAttribute('aria-checked', 'true')
    for (const name of ['Stagione', 'Quota', 'Pioggia di innesco']) {
      expect(screen.getByRole('button', { name })).toHaveAttribute(
        'aria-expanded',
        'true',
      )
    }
    expect(localStorage.getItem('mushma.whyDetails')).toBe('1')

    unmount()
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([season, altitude, rainTrigger], 0.5)}
      />,
    )
    expect(screen.getByRole('switch', { name: 'Mostra tutti i dettagli' })).toBeChecked()
    await user.click(screen.getByRole('button', { name: 'Quota' }))
    expect(screen.getByRole('button', { name: 'Quota' })).toHaveAttribute(
      'aria-expanded',
      'false',
    )
    expect(screen.getByRole('button', { name: 'Stagione' })).toHaveAttribute(
      'aria-expanded',
      'true',
    )

    await user.click(screen.getByRole('switch', { name: 'Mostra tutti i dettagli' }))
    for (const name of ['Stagione', 'Quota', 'Pioggia di innesco']) {
      expect(screen.getByRole('button', { name })).toHaveAttribute(
        'aria-expanded',
        'false',
      )
    }
    expect(localStorage.getItem('mushma.whyDetails')).toBe('0')
  })

  it('works when storage is blocked', async () => {
    const blocked = () => {
      throw new Error('blocked')
    }
    const getItem = Storage.prototype.getItem
    const setItem = Storage.prototype.setItem
    Storage.prototype.getItem = blocked
    Storage.prototype.setItem = blocked
    try {
      render(
        <WhyBreakdown species="porcini" isForecast={false} day={day([altitude], 0.6)} />,
      )
      await user.click(screen.getByRole('switch', { name: 'Mostra tutti i dettagli' }))
      expect(screen.getByRole('button', { name: 'Quota' })).toHaveAttribute(
        'aria-expanded',
        'true',
      )
    } finally {
      Storage.prototype.getItem = getItem
      Storage.prototype.setItem = setItem
    }
  })

  it('says what the rain figure is, only while a rain detail is open', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([altitude, rainTrigger], 0.5)}
      />,
    )
    const note = /stima del modello meteo/
    expect(screen.queryByText(note)).not.toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Quota' }))
    expect(screen.queryByText(note)).not.toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Pioggia di innesco' }))
    expect(screen.getByText(note)).toBeInTheDocument()
  })

  it('reads in English too', async () => {
    await act(() => changeLanguage('en'))
    render(
      <WhyBreakdown species="porcini" isForecast={false} day={day([rainTrigger], 0.7)} />,
    )
    await user.click(screen.getByRole('button', { name: 'Trigger rain' }))
    const row = rowOf('Trigger rain')
    expect(row).toHaveTextContent(
      '42 mm of rain in 3 days up to Saturday 12 September (6 days before).',
    )
    expect(row).toHaveTextContent(
      'The rule gives full credit from 30 mm up; none up to 10 mm.',
    )
  })
})
