import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { HubPage } from './HubPage'

// WebGL doesn't run in jsdom: the stub shows what the hub asks of the map, and lets a test tap it.
vi.mock('../map/HubMap', () => ({
  HubMap: (props: {
    highlighted: string | null
    onSelect: (slug: string) => void
    onUnserved: (slug: string | null) => void
  }) => (
    <div data-testid="map" data-highlighted={props.highlighted ?? ''}>
      <button type="button" onClick={() => props.onSelect('umbria')}>
        tap Umbria
      </button>
      <button type="button" onClick={() => props.onUnserved('lazio')}>
        tap Lazio
      </button>
    </div>
  ),
}))

function renderHub(overviewPending = false) {
  const handlers = {
    onSelectRegion: vi.fn(),
    onNavigate: vi.fn(),
    onDisclaimer: vi.fn(),
    onCookies: vi.fn(),
  }
  render(
    <HubPage
      overview={[
        { region: 'tuscany', mean_score: 0.855, good_share: 0.89, updated_at: null },
      ]}
      overviewPending={overviewPending}
      {...handlers}
    />,
  )
  return handlers
}

describe('HubPage', () => {
  it('lists every served region as a link, with its share of favourable woods and mean score', () => {
    renderHub()
    const list = screen.getByRole('list')
    const toscana = within(list).getByRole('link', { name: /^Toscana/ })
    const umbria = within(list).getByRole('link', { name: /^Umbria/ })
    expect(toscana).toHaveAttribute('href', '/toscana')
    expect(toscana).toHaveTextContent('89% dei boschi in condizioni favorevoli')
    expect(
      within(toscana).getByRole('img', { name: 'Indice delle condizioni 0,86 su 1' }),
    ).toBeInTheDocument()
    // Served, but missing from today's overview.
    expect(umbria).toHaveAttribute('href', '/umbria')
    expect(umbria).toHaveTextContent('Indice di oggi non ancora disponibile')
  })

  it('opens a region from its row or from the map', async () => {
    const { onSelectRegion } = renderHub()
    await userEvent.click(screen.getByRole('link', { name: /^Toscana/ }))
    expect(onSelectRegion).toHaveBeenLastCalledWith('toscana')
    await userEvent.click(screen.getByRole('button', { name: 'tap Umbria' }))
    expect(onSelectRegion).toHaveBeenLastCalledWith('umbria')
  })

  it('lights up a region on the map while its row is hovered', async () => {
    renderHub()
    await userEvent.hover(screen.getByRole('link', { name: /^Umbria/ }))
    expect(screen.getByTestId('map')).toHaveAttribute('data-highlighted', 'umbria')
    await userEvent.unhover(screen.getByRole('link', { name: /^Umbria/ }))
    expect(screen.getByTestId('map')).toHaveAttribute('data-highlighted', '')
  })

  it("says a tapped region isn't covered yet, until dismissed", async () => {
    renderHub()
    await userEvent.click(screen.getByRole('button', { name: 'tap Lazio' }))
    expect(screen.getByRole('status')).toHaveTextContent('Lazio non è ancora coperta.')
    await userEvent.click(screen.getByRole('button', { name: 'Chiudi' }))
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })
})
