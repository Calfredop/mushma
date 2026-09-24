import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import type { FactorChip } from '../api/queries'
import { IndicatorPanel } from './IndicatorPanel'

const chip = (id: string, role: FactorChip['role'], key = id): FactorChip => ({
  id,
  role,
  i18n_key: `factor.${key}`,
})

// Gallinacci-like: two factors share the "Gelate" label, one has a windowed id.
const chips = [
  chip('season', 'gate'),
  chip('habitat', 'gate'),
  chip('rain_trigger', 'driver'),
  chip('soil_temperature', 'driver'),
  chip('water_balance_60d', 'stopper', 'water_balance'),
  chip('frost', 'stopper'),
  chip('hard_frost', 'stopper', 'frost'),
  chip('slope', 'stopper'),
  chip('mystery', 'stopper'),
]

describe('IndicatorPanel', () => {
  it('groups the chips by family, in the palette order', () => {
    render(<IndicatorPanel chips={chips} active={[]} onToggle={() => {}} />)
    const groups = screen
      .getAllByRole('group')
      .map((group) => group.getAttribute('aria-labelledby'))
    expect(groups).toEqual([
      'indicator-family-water',
      'indicator-family-warmth',
      'indicator-family-cold',
      'indicator-family-terrain',
      'indicator-family-season',
      'indicator-family-other',
    ])
    const water = screen.getByRole('group', { name: 'Pioggia e umidità' })
    expect(
      within(water)
        .getAllByRole('button')
        .map((b) => b.textContent),
    ).toEqual(['Pioggia di innesco', 'Bilancio idrico'])
  })

  it('names chips like the "why" rows, with their own name where two would share one', () => {
    render(<IndicatorPanel chips={chips} active={[]} onToggle={() => {}} />)
    const cold = screen.getByRole('group', { name: 'Freddo' })
    expect(
      within(cold)
        .getAllByRole('button')
        .map((b) => b.textContent),
    ).toEqual(['Gelate', 'Gelate forti'])
    // A factor with no label yet still gets a chip, by its id.
    expect(screen.getByRole('button', { name: 'mystery' })).toBeInTheDocument()
  })

  it('shows which chips are on and toggles one', async () => {
    const onToggle = vi.fn()
    render(<IndicatorPanel chips={chips} active={['frost']} onToggle={onToggle} />)
    expect(screen.getByRole('button', { name: 'Gelate' })).toHaveAttribute(
      'aria-pressed',
      'true',
    )
    expect(screen.getByRole('button', { name: 'Stagione' })).toHaveAttribute(
      'aria-pressed',
      'false',
    )
    await userEvent.click(screen.getByRole('button', { name: 'Stagione' }))
    expect(onToggle).toHaveBeenCalledWith('season')
  })

  it('keys opacity as favourable, never as a chance', () => {
    render(<IndicatorPanel chips={chips} active={[]} onToggle={() => {}} />)
    expect(screen.getByText("Frena l'indice")).toBeInTheDocument()
    expect(screen.getByText(/Più favorevole/)).toBeInTheDocument()
    expect(document.body.textContent).not.toMatch(/probabilit|%|possibilit/i)
  })

  it('says why there are no chips, and folds away', async () => {
    render(
      <IndicatorPanel
        chips={undefined}
        active={['rain_trigger']}
        onToggle={() => {}}
        note="Gli indicatori sono conservati solo per gli ultimi 7 giorni e per la previsione."
      />,
    )
    expect(screen.getByText(/solo per gli ultimi 7 giorni/)).toBeVisible()
    await userEvent.click(screen.getByRole('button', { name: 'Nascondi i fattori' }))
    expect(screen.queryByText(/solo per gli ultimi 7 giorni/)).not.toBeVisible()
    expect(screen.getByRole('button', { name: 'Mostra i fattori' })).toHaveAttribute(
      'aria-expanded',
      'false',
    )
  })

  describe('the Bosco toggle', () => {
    it('shows whether the forest layer is on, and toggles it', async () => {
      const onToggleForest = vi.fn()
      render(
        <IndicatorPanel
          chips={chips}
          active={[]}
          onToggle={() => {}}
          forestOn
          onToggleForest={onToggleForest}
        />,
      )
      const bosco = screen.getByRole('button', { name: 'Bosco' })
      expect(bosco).toHaveAttribute('aria-pressed', 'true')
      await userEvent.click(bosco)
      expect(onToggleForest).toHaveBeenCalledOnce()
    })

    it('is off by default, and shows no legend', () => {
      render(<IndicatorPanel chips={chips} active={[]} onToggle={() => {}} />)
      expect(screen.getByRole('button', { name: 'Bosco' })).toHaveAttribute(
        'aria-pressed',
        'false',
      )
      expect(screen.queryByText('faggeta')).toBeNull()
    })

    it('lists every forest type by broad group once turned on', () => {
      render(<IndicatorPanel chips={chips} active={[]} onToggle={() => {}} forestOn />)
      const broadleaf = screen.getByRole('group', { name: 'Latifoglie' })
      expect(within(broadleaf).getByText('faggeta')).toBeInTheDocument()
      const conifer = screen.getByRole('group', { name: 'Conifere' })
      expect(within(conifer).getByText('abetina')).toBeInTheDocument()
      // Not toggle buttons: the layer is one on/off, not 14.
      expect(within(broadleaf).queryByRole('button')).toBeNull()
    })
  })

  describe('as a row, on a phone', () => {
    it('lines the chips up with the opacity key first, and no family headings', () => {
      render(
        <IndicatorPanel
          layout="row"
          chips={chips}
          active={['frost']}
          onToggle={() => {}}
        />,
      )
      const region = screen.getByRole('region', { name: "Fattori dell'indice" })
      expect(within(region).queryAllByRole('group')).toEqual([])
      expect(within(region).queryByRole('heading', { level: 3 })).toBeNull()
      expect(
        region.querySelector('[data-part="row"]')?.firstElementChild,
      ).toHaveTextContent(/^frena.*favorevole$/)
      // Family order, as in the panel, so related colours sit together.
      expect(
        within(region)
          .getAllByRole('button')
          .map((b) => b.textContent),
      ).toEqual([
        'Bosco',
        'Pioggia di innesco',
        'Bilancio idrico',
        'Temperatura del suolo',
        'Gelate',
        'Gelate forti',
        'Tipo di bosco',
        'Pendenza',
        'Stagione',
        'mystery',
      ])
      expect(screen.getByRole('button', { name: 'Gelate' })).toHaveAttribute(
        'aria-pressed',
        'true',
      )
    })

    it('toggles a chip, and has nothing to fold', async () => {
      const onToggle = vi.fn()
      render(
        <IndicatorPanel layout="row" chips={chips} active={[]} onToggle={onToggle} />,
      )
      expect(screen.queryByRole('button', { name: 'Nascondi i fattori' })).toBeNull()
      await userEvent.click(screen.getByRole('button', { name: 'Pendenza' }))
      expect(onToggle).toHaveBeenCalledWith('slope')
    })

    it('says why there are no chips', () => {
      render(
        <IndicatorPanel
          layout="row"
          chips={undefined}
          active={[]}
          onToggle={() => {}}
          note="Caricamento dei fattori…"
        />,
      )
      expect(screen.getByText('Caricamento dei fattori…')).toBeVisible()
    })
  })
})
