import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { WhyBreakdown } from './WhyBreakdown'

const day = (
  factors: { key: string; value: number; contribution: number }[],
  score: number,
) => ({
  date: '2026-09-18',
  score,
  factors: factors.map((f) => ({ ...f, i18n_key: `factor.${f.key}` })),
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
