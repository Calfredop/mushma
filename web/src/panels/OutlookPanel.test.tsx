import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { OUTLOOK, PLAUSIBLE } from '../test/fixtures'
import { OutlookPanel } from './OutlookPanel'

const props = {
  species: 'porcini' as const,
  onSpecies: () => {},
  comuni: [],
  comune: '051030',
  onComune: () => {},
  outlook: OUTLOOK,
  isLoading: false,
  isError: false,
  onRetry: () => {},
}

describe('OutlookPanel', () => {
  it('is labelled an outlook, not a forecast', () => {
    render(<OutlookPanel {...props} />)
    expect(
      screen.getByText("Un'indicazione di massima, non una previsione"),
    ).toBeInTheDocument()
  })

  it('compares the season so far with past seasons and normal weather', () => {
    render(<OutlookPanel {...props} />)
    expect(screen.getByText('Peggio del solito')).toBeInTheDocument()
    expect(screen.getByText('(di solito 26 a questa data)')).toBeInTheDocument()
    expect(screen.getByText('361 mm, il 73% del normale')).toBeInTheDocument()
    expect(screen.getByText('+1,8 °C rispetto al normale')).toBeInTheDocument()
  })

  it('reads each period as a tally of past seasons and a tilt, never a chance', () => {
    const { container } = render(<OutlookPanel {...props} />)
    const periods = screen.getAllByRole('listitem')
    expect(periods[0]).toHaveTextContent('28 set – 4 ott')
    expect(periods[0]).toHaveTextContent('meno favorevole del solito')
    expect(periods[0]).toHaveTextContent('favorevole in 4 stagioni su 4')
    expect(periods[0]).toHaveTextContent('Pioggia nei giorni prima: il 26% del normale')
    expect(periods[1]).toHaveTextContent('2 nov – 30 nov') // clipped by the weeks before it
    expect(periods[1]).toHaveTextContent('più favorevole del solito')
    expect(container.textContent).not.toMatch(/possibilità|probabile|chance/i)
  })

  it('quotes the rain lead and the bands from the API', () => {
    render(<OutlookPanel {...props} />)
    expect(screen.getByText(/10–16 giorni dopo la pioggia/)).toHaveTextContent(
      'Con almeno il 125% della pioggia normale',
    )
  })

  it('asks for one species when all are selected', async () => {
    const onSpecies = vi.fn()
    render(<OutlookPanel {...props} species="combined" onSpecies={onSpecies} />)
    await userEvent.click(screen.getByRole('button', { name: 'Ovoli' }))
    expect(onSpecies).toHaveBeenCalledWith('ovoli')
  })

  it('says when the season has nothing left to look ahead to', () => {
    render(<OutlookPanel {...props} outlook={{ ...OUTLOOK, periods: [] }} />)
    expect(screen.getByText(/la stagione va dal 1 mag al 20 dic/)).toBeInTheDocument()
  })
})

describe('OutlookPanel periods', () => {
  it('names a whole month, and gives the dates of one the season clips', () => {
    const whole = { ...OUTLOOK.periods[1], start: '2026-11-01', end: '2026-11-30' }
    const clipped = { ...OUTLOOK.periods[1], start: '2026-12-01', end: '2026-12-20' }
    render(
      <OutlookPanel {...props} outlook={{ ...OUTLOOK, periods: [whole, clipped] }} />,
    )
    const periods = screen.getAllByRole('listitem')
    expect(periods[0]).toHaveTextContent(/^novembre/)
    expect(periods[1]).toHaveTextContent('1 dic – 20 dic')
  })

  it('calls the whole region by its name in the UI language', async () => {
    const { default: i18n } = await import('../i18n')
    await i18n.changeLanguage('en')
    render(
      <OutlookPanel
        {...props}
        outlook={{ ...OUTLOOK, area: { code: null, name: 'Toscana', kind: 'region' } }}
      />,
    )
    expect(screen.getByText('Porcini · Tuscany')).toBeInTheDocument()
    await i18n.changeLanguage('it')
  })

  it("shows which species the chosen zone's woodland suits", () => {
    render(
      <OutlookPanel
        {...props}
        plausible={{
          data: { ...PLAUSIBLE, area: OUTLOOK.area },
          isLoading: false,
          isError: false,
          onRetry: () => {},
        }}
      />,
    )
    expect(
      screen.getByRole('list', { name: 'Specie adatte alla zona' }),
    ).toBeInTheDocument()
  })

  it("never shows the zone picked before as this one's species", () => {
    render(
      <OutlookPanel
        {...props}
        plausible={{
          data: PLAUSIBLE,
          isLoading: true,
          isError: false,
          onRetry: () => {},
        }}
      />,
    )
    expect(
      screen.queryByRole('list', { name: 'Specie adatte alla zona' }),
    ).not.toBeInTheDocument()
    expect(screen.getByText('Carico le specie adatte alla zona…')).toBeInTheDocument()
  })
})
