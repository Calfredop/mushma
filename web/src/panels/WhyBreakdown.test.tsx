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

    // Season holds nothing back: it folds away below the factors that do.
    const rows = within(section).getAllByRole('listitem')
    expect(rows.map((row) => row.firstChild?.textContent)).toEqual([
      'Pioggia degli ultimi 30 giorni',
      'Gelate',
    ])
    expect(rows[0]).toHaveTextContent('frena del 33%')
    expect(rows[1]).toHaveTextContent('frena del 67%')
    expect(within(rows[1]).getByRole('meter', { name: 'Gelate' })).toHaveAttribute(
      'aria-valuenow',
      '0.25',
    )
    const folded = within(section).getAllByRole('listitem', { hidden: true })[2]
    expect(folded.firstChild?.textContent).toBe('Stagione')
    expect(folded).not.toHaveTextContent('frena')
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
    expect(
      screen.getByText("L'indice è zero a causa di: Stagione e Quota"),
    ).toBeInTheDocument()
    expect(screen.getByText(/Questo giorno deve ancora arrivare/)).toBeInTheDocument()
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

describe('WhyBreakdown fold', () => {
  const user = userEvent.setup()
  beforeEach(() => localStorage.clear())

  const mixed = day(
    [
      { key: 'season', value: 1, contribution: 1 },
      { key: 'rain_30d', value: 0.5, contribution: 0.5 },
      { key: 'altitude', value: 1, contribution: 1 },
      { key: 'frost', value: 0.25, contribution: 0.25 },
      { key: 'habitat', value: 1, contribution: 1 },
    ],
    0.125,
  )

  it('folds the factors holding nothing back into one row, until it is opened', async () => {
    render(<WhyBreakdown species="porcini" isForecast={false} day={mixed} />)
    // The factors that brake, in the API's order.
    expect(screen.getAllByRole('meter').map((m) => m.getAttribute('aria-label'))).toEqual(
      ['Pioggia degli ultimi 30 giorni', 'Gelate'],
    )
    const fold = screen.getByRole('button', { name: 'Altri 3 fattori già ideali (1,00)' })
    expect(fold).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByRole('meter', { name: 'Stagione' })).toBeNull()

    await user.click(fold)
    expect(fold).toHaveAttribute('aria-expanded', 'true')
    // Opened in place, under the fold, still in the API's order.
    expect(screen.getAllByRole('meter').map((m) => m.getAttribute('aria-label'))).toEqual(
      ['Pioggia degli ultimi 30 giorni', 'Gelate', 'Stagione', 'Quota', 'Tipo di bosco'],
    )
  })

  it('counts a single one in the singular', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { key: 'season', value: 1, contribution: 1 },
            { key: 'frost', value: 0.5, contribution: 0.5 },
          ],
          0.5,
        )}
      />,
    )
    expect(
      screen.getByRole('button', { name: 'Un altro fattore già ideale (1,00)' }),
    ).toBeVisible()
  })

  it('folds nothing when the score is blocked', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { key: 'season', value: 1, contribution: 1 },
            { key: 'altitude', value: 0, contribution: 0 },
            { key: 'frost', value: 0.5, contribution: 0.5 },
          ],
          0,
        )}
      />,
    )
    expect(screen.getAllByRole('meter')).toHaveLength(3)
    expect(screen.queryByRole('button', { name: /fattor[ei] a 1,00/ })).toBeNull()
  })

  it('folds nothing when every factor brakes', () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day(
          [
            { key: 'rain_30d', value: 0.5, contribution: 0.5 },
            { key: 'frost', value: 0.5, contribution: 0.5 },
          ],
          0.25,
        )}
      />,
    )
    expect(screen.getAllByRole('meter')).toHaveLength(2)
    expect(screen.queryByRole('button', { name: /fattor[ei] a 1,00/ })).toBeNull()
  })

  it('shows every factor when all the details are on', async () => {
    render(<WhyBreakdown species="porcini" isForecast={false} day={mixed} />)
    await user.click(screen.getByRole('switch', { name: 'Mostra tutti i dettagli' }))
    expect(screen.getAllByRole('meter')).toHaveLength(5)
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
    expect(
      screen
        .getAllByRole('listitem', { hidden: true })
        .map((row) => row.dataset.blocking),
    ).toEqual(['false', 'false'])
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
const rainShare: FactorInput = {
  key: 'rain_30d',
  value: 0.62,
  contribution: 0.85,
  role: 'driver',
  weight: 1,
  input: 97,
  unit: '%',
  rule: {
    kind: 'window_aggregate',
    variable: 'precipitation_sum',
    variable_unit: 'mm',
    aggregate: 'percent_of_normal',
    window_days: 30,
    offset_days: 0,
    trapezoid: [50, 125, null, null],
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

const clockedRain: FactorInput = {
  ...rainTrigger,
  days_ago: 12,
  growth_days: 8.4,
  rule: { ...rainTrigger.rule!, lag_unit: 'growth_days' },
}
const sunExposure: FactorInput = {
  key: 'sun_exposure',
  value: 0.84,
  contribution: 0.84,
  role: 'stopper',
  input: 114,
  unit: '%',
  rule: {
    kind: 'window_aggregate',
    variable: 'sun_exposure_pct',
    variable_unit: '%',
    aggregate: 'mean',
    window_days: 1,
    offset_days: 0,
    trapezoid: [null, null, 95, 120],
    where: {
      variable: 'elevation_m',
      variable_unit: 'm',
      trapezoid: [null, null, 900, 1100],
    },
  },
}
const slope: FactorInput = {
  key: 'slope',
  value: 0.95,
  contribution: 0.95,
  role: 'stopper',
  input: 20,
  unit: '°',
  rule: {
    kind: 'static_band',
    variable: 'slope_deg',
    variable_unit: '°',
    trapezoid: [null, null, 15, 35],
  },
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
    expect(
      screen.getByRole('button', { name: 'Stagione', hidden: true }),
    ).toHaveAttribute('aria-expanded', 'false')
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
    expect(row).toHaveTextContent('Ideale da 30 mm in su; sfavorevole fino a 10 mm.')
    expect(row).toHaveTextContent(
      'Tempo dalla pioggia: ideale da 10 a 16 giorni; sfavorevole fino a 6 giorni e da 24 giorni in su.',
    )
  })

  it('counts the lag of a rain on the growth clock in growth days, and gives the pace', async () => {
    render(
      <WhyBreakdown species="porcini" isForecast={false} day={day([clockedRain], 0.7)} />,
    )
    await user.click(screen.getByRole('button', { name: 'Pioggia di innesco' }))
    const row = rowOf('Pioggia di innesco')
    expect(row).toHaveTextContent(
      '42 mm di pioggia in 3 giorni fino a domenica 6 settembre (12 giorni prima).',
    )
    expect(row).toHaveTextContent(
      "Con il caldo e l'umidità da allora, quei 12 giorni valgono 8 giorni di crescita (crescita al 70% del ritmo normale): il caldo la accelera, il freddo o l'aria secca la rallentano.",
    )
    expect(row).toHaveTextContent(
      'Crescita dalla pioggia: ideale da 10 a 16 giorni di crescita; sfavorevole fino a 6 giorni di crescita e da 24 giorni di crescita in su.',
    )
    expect(row).not.toHaveTextContent('Tempo dalla pioggia')
    expect(screen.getByText(/tengono conto del versante/)).toBeInTheDocument()
  })

  it('shows the sun on the slope on the day, and where the rule applies', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([sunExposure, slope], 0.8)}
      />,
    )
    await user.click(screen.getByRole('button', { name: 'Esposizione al sole' }))
    await user.click(screen.getByRole('button', { name: 'Pendenza' }))
    const sun = rowOf('Esposizione al sole')
    expect(sun).toHaveTextContent(
      'Sole su questo versante, rispetto al terreno piano, in questo giorno: 114%.',
    )
    expect(sun).toHaveTextContent('Ideale fino a 95%; sfavorevole da 120% in su.')
    expect(sun).toHaveTextContent(
      'Questo fattore conta in pieno a quota fino a 900 m; per niente da 1100 m in su.',
    )
    expect(rowOf('Pendenza')).toHaveTextContent('Per questa cella: 20°.')
    expect(rowOf('Pendenza')).not.toHaveTextContent('conta in pieno')
  })

  it("shows a gate's attribute and its band", async () => {
    render(
      <WhyBreakdown species="porcini" isForecast={false} day={day([altitude], 0.6)} />,
    )
    await user.click(screen.getByRole('button', { name: 'Quota' }))
    const row = rowOf('Quota')
    expect(row).toHaveTextContent('Per questa cella: 640 m.')
    expect(row).toHaveTextContent(
      'Ideale da 700 a 1600 m; sfavorevole fino a 200 m e da 1900 m in su.',
    )
  })

  it('counts matching days against the window and the threshold', async () => {
    render(<WhyBreakdown species="porcini" isForecast={false} day={day([frost], 0.6)} />)
    await user.click(screen.getByRole('button', { name: 'Gelate' }))
    const row = rowOf('Gelate')
    expect(row).toHaveTextContent('2 giorni su 7 con temperatura minima ≤ 0 °C.')
    expect(row).toHaveTextContent(
      'Ideale fino a 1 giorno; sfavorevole da 2 giorni in su.',
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
      'Ideale da 10 a 17 °C; sfavorevole fino a 6 °C e da 22 °C in su.',
    )
  })

  it("compares the month's rain with the cell's own normal", async () => {
    render(
      <WhyBreakdown species="porcini" isForecast={false} day={day([rainShare], 0.62)} />,
    )
    await user.click(
      screen.getByRole('button', { name: 'Pioggia degli ultimi 30 giorni' }),
    )
    const row = rowOf('Pioggia degli ultimi 30 giorni')
    expect(row).toHaveTextContent('Pioggia, rispetto al solito qui su 30 giorni: 97%.')
    expect(row).toHaveTextContent('Ideale da 125% in su; sfavorevole fino a 50%.')
  })

  it('gives season, and habitat without the cell’s forest types, a plain line with no numbers', async () => {
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([season, habitat], 0.8)}
      />,
    )
    await user.click(
      screen.getByRole('button', { name: 'Un altro fattore già ideale (1,00)' }),
    )
    await user.click(screen.getByRole('button', { name: 'Stagione' }))
    await user.click(screen.getByRole('button', { name: 'Tipo di bosco' }))
    expect(rowOf('Stagione')).toHaveTextContent(
      "Il periodo dell'anno in cui questa specie di solito nasce",
    )
    expect(rowOf('Tipo di bosco')).toHaveTextContent(
      'Quanto il tipo di bosco di questa cella si adatta alla specie',
    )
    for (const name of ['Stagione', 'Tipo di bosco']) {
      const detail = within(rowOf(name)).getByTestId('factor-detail')
      expect(detail).not.toHaveTextContent(/\d/)
    }
  })

  it('names the cell’s forest types and how well each suits the species', async () => {
    const fitted: FactorInput = {
      ...habitat,
      rule: { kind: 'habitat', affinity: { beech: 1, chestnut: 0.6, macchia: 0 } },
    }
    render(
      <WhyBreakdown
        species="porcini"
        isForecast={false}
        day={day([fitted], 0.8)}
        habitats={[
          { habitat: 'beech', fraction: 0.62 },
          { habitat: 'chestnut', fraction: 0.3 },
          { habitat: 'macchia', fraction: 0.08 },
        ]}
      />,
    )
    await user.click(screen.getByRole('button', { name: 'Tipo di bosco' }))
    const row = rowOf('Tipo di bosco')
    expect(row).toHaveTextContent(
      'Bosco di questa cella: faggeta 62%, castagneto 30% e altri tipi 8%.',
    )
    expect(row).toHaveTextContent(
      'Quanto ogni tipo si adatta alla specie, da 0 a 1: faggeta 1,00 e castagneto 0,60.',
    )
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
    await user.click(
      screen.getByRole('button', { name: 'Un altro fattore già ideale (1,00)' }),
    )
    await user.click(screen.getByRole('button', { name: 'Gelate' }))
    expect(rowOf('Pioggia di innesco')).toHaveTextContent(
      'Misura non disponibile per questo giorno.',
    )
    expect(rowOf('Pioggia di innesco')).toHaveTextContent('Ideale da 30 mm in su')
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
      expect(screen.getByRole('button', { name, hidden: true })).toHaveAttribute(
        'aria-expanded',
        'false',
      )
    }
    // Off again, Season folds away again.
    expect(screen.queryByRole('button', { name: 'Stagione' })).toBeNull()
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
    const note = /viene da un modello meteo/
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
    expect(row).toHaveTextContent('Ideal from 30 mm up; unfavourable up to 10 mm.')
  })
})
