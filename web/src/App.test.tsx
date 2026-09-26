import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { getConsent, setConsent } from './consent'

const track = vi.fn()
vi.mock('./analytics', () => ({ track: (event: unknown) => track(event) }))

// WebGL doesn't run in jsdom: the stub shows what the app asks of the map.
vi.mock('./map/ConditionsMap', () => ({
  ConditionsMap: (props: Record<string, unknown>) => (
    <div
      data-testid="map"
      data-camera={JSON.stringify(props.camera ?? null)}
      data-spot-point={JSON.stringify(props.spotPoint ?? null)}
      data-user-position={JSON.stringify(props.userPosition ?? null)}
      data-analysis={JSON.stringify(props.analysis ?? null)}
      data-padding={JSON.stringify(props.padding ?? null)}
    />
  ),
}))

vi.mock('./pages/HubPage', () => ({
  HubPage: (props: { onSelectRegion: (slug: string) => void }) => (
    <div data-testid="hub">
      <button type="button" onClick={() => props.onSelectRegion('umbria')}>
        Umbria
      </button>
    </div>
  ),
}))

// An empty day of scores, and nothing else: the map layer loads, the panels don't.
vi.mock('./api/client', () => ({
  apiClient: {
    GET: (path: string) =>
      Promise.resolve(
        path === '/scores'
          ? {
              data: { cells: [], date: '2026-09-19', species: 'combined' },
              response: { status: 200 },
            }
          : path === '/overview'
            ? {
                data: {
                  date: '2026-09-19',
                  species: 'combined',
                  good_score: 0.6,
                  regions: [
                    {
                      region: 'tuscany',
                      mean_score: 0.4,
                      good_share: 0.2,
                      updated_at: null,
                    },
                    {
                      region: 'umbria',
                      mean_score: 0.5,
                      good_share: 0.3,
                      updated_at: null,
                    },
                  ],
                },
                response: { status: 200 },
              }
            : { data: undefined, response: { status: 404 } },
      ),
  },
}))

function mockGeolocation(lat: number, lon: number) {
  Object.defineProperty(navigator, 'geolocation', {
    configurable: true,
    value: {
      getCurrentPosition: (success: PositionCallback) =>
        success({ coords: { latitude: lat, longitude: lon } } as GeolocationPosition),
    },
  })
}

function mockGeolocationDenied() {
  Object.defineProperty(navigator, 'geolocation', {
    configurable: true,
    value: {
      getCurrentPosition: (_: PositionCallback, error: PositionErrorCallback) =>
        error({ code: 1, PERMISSION_DENIED: 1 } as GeolocationPositionError),
    },
  })
}

const mapProp = (name: string): unknown =>
  JSON.parse(screen.getByTestId('map').getAttribute(`data-${name}`) ?? 'null')

beforeEach(() => localStorage.setItem('mushma.disclaimer.v2', 'accepted'))

afterEach(() => {
  localStorage.clear()
  Reflect.deleteProperty(navigator, 'geolocation')
  window.history.replaceState(null, '', '/toscana')
  track.mockClear()
})

describe('centre on my position', () => {
  it('moves the map to the fix and marks it, without opening a spot', async () => {
    mockGeolocation(43.85, 11.73)
    window.history.replaceState(null, '', '/toscana')
    render(<App />)

    await userEvent.click(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    )

    expect(mapProp('camera')).toMatchObject({ lat: 43.85, lon: 11.73 })
    expect(mapProp('user-position')).toEqual({ lat: 43.85, lon: 11.73 })
    expect(mapProp('spot-point')).toBeNull()
  })

  it('leaves the map alone for a fix outside the region, and says why', async () => {
    // Munich: outside every Italian region's bbox (Milan now falls inside Piemonte's).
    mockGeolocation(48.14, 11.58)
    window.history.replaceState(null, '', '/toscana')
    render(<App />)

    await userEvent.click(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    )

    expect(await screen.findByText(/fuori dalle regioni coperte/i)).toBeInTheDocument()
    expect(mapProp('camera')).toBeNull()
    expect(mapProp('user-position')).toBeNull()
  })
})

describe('the phone shell', () => {
  beforeEach(() => window.history.replaceState(null, '', '/toscana'))

  it('has no top bar: the wordmark and the search are in the sheet', async () => {
    render(<App />)
    const sheet = screen.getByRole('complementary')
    expect(
      within(sheet).getByRole('heading', { level: 1, name: 'Mappa Funghi' }),
    ).toBeInTheDocument()
    expect(
      within(sheet).getByRole('combobox', { name: 'Cerca un luogo' }),
    ).toBeInTheDocument()
    expect(screen.getAllByRole('heading', { level: 1 })).toHaveLength(1)
  })

  it('introduces the map in one line, with the rest behind "Come funziona"', async () => {
    window.history.replaceState(null, '', '/toscana/porcini')
    render(<App />)
    expect(screen.getByText('Condizioni per i porcini, cella per cella.')).toBeVisible()
    const more = screen.getByRole('button', { name: 'Come funziona' })
    expect(more).toHaveAttribute('aria-expanded', 'false')
    // Still in the page for search engines, only folded away.
    const full = screen.getByText(/non dove si trovano i funghi/)
    expect(full).not.toBeVisible()

    await userEvent.click(more)
    expect(more).toHaveAttribute('aria-expanded', 'true')
    expect(full).toBeVisible()
    expect(full).toHaveTextContent(/indice delle condizioni da 0 a 1/)
  })

  it('has one locate button, and it only centres the map', () => {
    render(<App />)
    expect(
      screen.getAllByRole('button', { name: /posizione/ }).map((b) => b.textContent),
    ).toEqual([''])
    expect(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    ).toBeInTheDocument()
  })

  it('opens the spot forecast where you are from "La mia posizione" in the search', async () => {
    mockGeolocation(43.85, 11.73)
    render(<App />)

    const sheet = screen.getByRole('complementary')
    expect(sheet).toHaveAttribute('data-snap', 'peek')
    await userEvent.click(screen.getByRole('combobox', { name: 'Cerca un luogo' }))
    // The search comes up full, so its list has room.
    expect(sheet).toHaveAttribute('data-snap', 'full')
    await userEvent.click(screen.getByRole('option', { name: /^La mia posizione/ }))
    // A chosen spot opens at half, over the map.
    expect(sheet).toHaveAttribute('data-snap', 'half')

    expect(mapProp('camera')).toMatchObject({ lat: 43.85, lon: 11.73, zoom: 12 })
    expect(mapProp('spot-point')).toMatchObject({ point: [11.73, 43.85] })
    expect(mapProp('user-position')).toEqual({ lat: 43.85, lon: 11.73 })
    expect(track).toHaveBeenCalledWith({ name: 'spot-open', data: { method: 'gps' } })
  })

  it('ends the sheet with a compact footer: status, disclaimer, one row of links and GitHub', () => {
    render(<App />)
    const footer = screen.getByRole('contentinfo')
    expect(
      within(footer).getByText(/Solo condizioni, nessuna garanzia/),
    ).toBeInTheDocument()
    const links = within(footer).getByRole('navigation', { name: 'Link utili' })
    expect(
      within(links)
        .getAllByRole('link')
        .concat(within(links).getAllByRole('button'))
        .map((item) => item.getAttribute('aria-label') ?? item.textContent),
    ).toEqual([
      'Crediti',
      'Termini',
      'Privacy',
      'Codice su GitHub',
      'Avvertenze',
      'Cookie',
    ])
    expect(within(links).getByRole('link', { name: 'Codice su GitHub' })).toHaveAttribute(
      'href',
      'https://github.com/Calfredop/mushma',
    )
  })

  it('comes down to half for "La mia posizione", so its progress and errors show on the map', async () => {
    mockGeolocationDenied()
    render(<App />)
    const sheet = screen.getByRole('complementary')
    await userEvent.click(screen.getByRole('combobox', { name: 'Cerca un luogo' }))
    expect(sheet).toHaveAttribute('data-snap', 'full')
    await userEvent.click(screen.getByRole('option', { name: /^La mia posizione/ }))
    expect(sheet).toHaveAttribute('data-snap', 'half')
    expect(await screen.findByText(/La posizione è disattivata/)).toBeInTheDocument()
  })

  it('opens the disclaimer and the pages from the ⓘ menu', async () => {
    render(<App />)
    await userEvent.click(screen.getByRole('button', { name: 'Info e impostazioni' }))
    await userEvent.click(screen.getByRole('menuitem', { name: 'Avvertenze' }))
    expect(
      screen.getByRole('dialog', { name: 'Prima di usare la mappa' }),
    ).toHaveAttribute('open')
    await userEvent.click(screen.getByRole('button', { name: 'Ho capito' }))

    await userEvent.click(screen.getByRole('button', { name: 'Info e impostazioni' }))
    await userEvent.click(screen.getByRole('menuitem', { name: 'Dati e crediti' }))
    expect(window.location.pathname).toBe('/credits')
  })
})

describe('the desktop panel', () => {
  beforeEach(() => {
    window.matchMedia = vi.fn().mockImplementation((query: string) => ({
      matches: query === '(min-width: 900px)',
      media: query,
      addEventListener: () => {},
      removeEventListener: () => {},
    }))
  })
  afterEach(() => Reflect.deleteProperty(window, 'matchMedia'))

  it('collapses to its header, is remembered, and a chosen spot opens it again', async () => {
    window.history.replaceState(null, '', '/toscana')
    const { unmount } = render(<App />)
    const toggle = screen.getByRole('button', { name: 'Riduci il pannello' })
    expect(toggle).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('tab', { name: 'Oggi' })).toBeVisible()
    // Map padding keeps camera moves clear of the open panel: 16 + 400 + 16.
    expect(mapProp('padding')).toMatchObject({ left: 432 })

    await userEvent.click(toggle)
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(toggle).toHaveAccessibleName('Espandi il pannello')
    expect(screen.queryByRole('tab', { name: 'Oggi' })).toBeNull()
    // The header row stays: wordmark and search.
    expect(screen.getByRole('heading', { level: 1 })).toBeVisible()
    expect(screen.getByRole('combobox')).toBeVisible()
    expect(mapProp('padding')).toMatchObject({ left: 16 })
    unmount()

    mockGeolocation(43.85, 11.73)
    render(<App />)
    const again = screen.getByRole('button', { name: 'Espandi il pannello' })
    expect(again).toHaveAttribute('aria-expanded', 'false')

    await userEvent.click(screen.getByRole('combobox'))
    await userEvent.click(screen.getByRole('option', { name: /^La mia posizione/ }))
    expect(again).toHaveAttribute('aria-expanded', 'true')
  })
})

describe('routing', () => {
  afterEach(() => {
    window.history.replaceState(null, '', '/')
    document.head
      .querySelectorAll(
        'meta[name="description"], meta[name="robots"], link[rel="canonical"], script[type="application/ld+json"]',
      )
      .forEach((el) => el.remove())
  })

  it('shows the hub at the bare root', async () => {
    window.history.replaceState(null, '', '/')
    render(<App />)
    expect(await screen.findByTestId('hub')).toBeInTheDocument()
    expect(window.location.pathname).toBe('/')
  })

  it('navigates from the hub into a region', async () => {
    window.history.replaceState(null, '', '/')
    render(<App />)
    await userEvent.click(await screen.findByRole('button', { name: 'Umbria' }))
    expect(window.location.pathname).toBe('/umbria')
  })

  it('switches region from the region menu, keeping the species', async () => {
    window.history.replaceState(null, '', '/toscana/porcini')
    render(<App />)
    await screen.findByTestId('map')
    await userEvent.click(screen.getByRole('button', { name: 'Regione' }))
    await userEvent.click(screen.getByRole('option', { name: 'Umbria' }))
    expect(window.location.pathname).toBe('/umbria/porcini')
  })

  it('offers to switch when GPS lands in another served region', async () => {
    mockGeolocation(42.9, 12.5) // Umbria
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await userEvent.click(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    )
    expect(await screen.findByText(/Sei in Umbria/i)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: 'Passa a Umbria' }))
    expect(window.location.pathname).toBe('/umbria')
  })

  it('names the offered region with its own preposition (nelle Marche, not in Marche)', async () => {
    mockGeolocation(43.3, 13.45) // Macerata
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await userEvent.click(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    )
    expect(await screen.findByText(/Sei nelle Marche\./)).toBeInTheDocument()
  })

  it('navigates to the species path when the switcher is used, and tracks the switch', async () => {
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await userEvent.click(screen.getByRole('radio', { name: 'Porcini' }))
    expect(window.location.pathname).toBe('/toscana/porcini')
    expect(track).toHaveBeenCalledWith({
      name: 'species-switch',
      data: { species: 'porcini' },
    })
  })

  it('keeps the title, description and canonical in step with the route', async () => {
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await screen.findByTestId('map')
    expect(document.title).toContain('Toscana')
    const canonical = () =>
      document.head.querySelector('link[rel="canonical"]')?.getAttribute('href')
    expect(canonical()).toBe('https://mappafunghi.app/toscana')

    await userEvent.click(screen.getByRole('radio', { name: 'Porcini' }))
    expect(document.title).toContain('Porcini')
    expect(canonical()).toBe('https://mappafunghi.app/toscana/porcini')
    expect(
      document.head.querySelector('meta[name="description"]')?.getAttribute('content'),
    ).toBeTruthy()
    expect(document.head.querySelector('meta[name="robots"]')).toBeNull()
  })

  it('keeps the JSON-LD graph in step with the route, and drops it on a 404', async () => {
    const webPageUrl = () => {
      const script = document.head.querySelector('script[type="application/ld+json"]')
      if (!script) return null
      const graph = JSON.parse(script.textContent!)['@graph'] as Record<string, unknown>[]
      return graph.find((node) => node['@type'] === 'WebPage')?.url
    }
    window.history.replaceState(null, '', '/toscana')
    const { unmount } = render(<App />)
    await screen.findByTestId('map')
    expect(webPageUrl()).toBe('https://mappafunghi.app/toscana')

    await userEvent.click(screen.getByRole('radio', { name: 'Porcini' }))
    expect(webPageUrl()).toBe('https://mappafunghi.app/toscana/porcini')
    expect(
      document.head.querySelectorAll('script[type="application/ld+json"]'),
    ).toHaveLength(1)
    unmount()

    window.history.replaceState(null, '', '/lombardia')
    render(<App />)
    expect(screen.getByText('Questa pagina non esiste')).toBeInTheDocument()
    expect(webPageUrl()).toBeNull()
  })

  it('shows the not-found page for an unknown region, with a link back to the map', async () => {
    window.history.replaceState(null, '', '/lombardia')
    render(<App />)
    expect(screen.getByText('Questa pagina non esiste')).toBeInTheDocument()
    expect(screen.queryByTestId('map')).not.toBeInTheDocument()
    expect(
      document.head.querySelector('meta[name="robots"]')?.getAttribute('content'),
    ).toBe('noindex')

    await userEvent.click(screen.getByRole('link', { name: 'Torna alla mappa' }))
    expect(window.location.pathname).toBe('/toscana')
  })

  it('shows the not-found page for an unknown species', () => {
    window.history.replaceState(null, '', '/toscana/tartufi')
    render(<App />)
    expect(screen.getByText('Questa pagina non esiste')).toBeInTheDocument()
  })

  it('opens the Terms and Privacy pages from the footer, with a way back to the map', async () => {
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await screen.findByTestId('map')

    const footer = within(screen.getByRole('navigation', { name: 'Link utili' }))
    await userEvent.click(footer.getByRole('link', { name: 'Termini' }))
    expect(window.location.pathname).toBe('/terms')
    expect(
      screen.getByRole('heading', { name: 'Termini e condizioni' }),
    ).toBeInTheDocument()

    await userEvent.click(screen.getByRole('link', { name: 'Torna alla mappa' }))
    expect(window.location.pathname).toBe('/toscana')

    await userEvent.click(
      within(screen.getByRole('navigation', { name: 'Link utili' })).getByRole('link', {
        name: 'Privacy',
      }),
    )
    expect(window.location.pathname).toBe('/privacy')
    expect(
      screen.getByRole('heading', { name: 'Informativa sulla privacy' }),
    ).toBeInTheDocument()
  })
})

describe('cookie banner', () => {
  afterEach(() => window.history.replaceState(null, '', '/'))

  it('shows on a first visit, and remembers Accept so it never comes back', async () => {
    window.history.replaceState(null, '', '/toscana')
    const { unmount } = render(<App />)
    await screen.findByTestId('map')

    await userEvent.click(screen.getByRole('button', { name: 'Accetta' }))
    expect(getConsent()).toBe('accepted')
    unmount()

    render(<App />)
    await screen.findByTestId('map')
    expect(screen.queryByRole('button', { name: 'Accetta' })).not.toBeInTheDocument()
  })

  it('stays away once a choice is already stored', async () => {
    setConsent('declined')
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await screen.findByTestId('map')
    expect(screen.queryByRole('button', { name: 'Rifiuta' })).not.toBeInTheDocument()
  })

  it('is reopenable from the footer to change the choice', async () => {
    setConsent('declined')
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    await screen.findByTestId('map')

    await userEvent.click(screen.getByRole('button', { name: 'Cookie' }))
    expect(screen.getByRole('button', { name: 'Accetta' })).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Accetta' }))
    expect(getConsent()).toBe('accepted')
  })
})

describe('analysis mode', () => {
  it('swaps the legend for the factors, turns on rain_trigger and leaves Tutte', async () => {
    window.history.replaceState(null, '', '/toscana')
    render(<App />)
    // A phone: the legend is one chip.
    expect(screen.getByRole('button', { name: 'Legenda' })).toBeInTheDocument()

    const toggle = screen.getByRole('button', { name: 'Analisi' })
    expect(toggle).toHaveAttribute('aria-pressed', 'false')
    await userEvent.click(toggle)

    expect(toggle).toHaveAttribute('aria-pressed', 'true')
    // No combined score in the mode: the path moves from "Tutti" to porcini.
    expect(window.location.pathname).toBe('/toscana/porcini')
    expect(window.location.search).toBe('?mode=analysis&f=rain_trigger')
    expect(screen.getByRole('radio', { name: 'Porcini' })).toBeChecked()
    expect(screen.getByRole('radio', { name: 'Tutte' })).toBeDisabled()
    expect(
      screen.getByRole('region', { name: "Fattori dell'indice" }),
    ).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Legenda' })).toBeNull()
    expect(mapProp('analysis')).toMatchObject({
      active: [{ id: 'rain_trigger', color: '#268C9F' }],
    })

    // The mocked API has no factors: the day says so instead of drawing anything.
    expect(await screen.findAllByText(/solo per gli ultimi 7 giorni/)).not.toHaveLength(0)
    expect(screen.getByRole('button', { name: 'Riproduci i giorni' })).toBeInTheDocument()

    await userEvent.click(toggle)
    expect(window.location.search).toBe('')
    expect(mapProp('analysis')).toBeNull()
    expect(screen.queryByRole('button', { name: 'Riproduci i giorni' })).toBeNull()
  })
})
