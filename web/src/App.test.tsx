import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'

// WebGL doesn't run in jsdom: the stub shows what the app asks of the map.
vi.mock('./map/ConditionsMap', () => ({
  ConditionsMap: (props: Record<string, unknown>) => (
    <div
      data-testid="map"
      data-camera={JSON.stringify(props.camera ?? null)}
      data-spot-point={JSON.stringify(props.spotPoint ?? null)}
      data-user-position={JSON.stringify(props.userPosition ?? null)}
      data-analysis={JSON.stringify(props.analysis ?? null)}
    />
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

const mapProp = (name: string): unknown =>
  JSON.parse(screen.getByTestId('map').getAttribute(`data-${name}`) ?? 'null')

beforeEach(() => localStorage.setItem('mushma.disclaimer.v1', 'accepted'))

afterEach(() => {
  localStorage.clear()
  Reflect.deleteProperty(navigator, 'geolocation')
  window.history.replaceState(null, '', '/')
})

describe('centre on my position', () => {
  it('moves the map to the fix and marks it, without opening a spot', async () => {
    mockGeolocation(43.85, 11.73)
    render(<App />)

    await userEvent.click(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    )

    expect(mapProp('camera')).toMatchObject({ lat: 43.85, lon: 11.73 })
    expect(mapProp('user-position')).toEqual({ lat: 43.85, lon: 11.73 })
    expect(mapProp('spot-point')).toBeNull()
  })

  it('leaves the map alone for a fix outside the region, and says why', async () => {
    mockGeolocation(45.46, 9.19) // Milan
    render(<App />)

    await userEvent.click(
      screen.getByRole('button', { name: 'Centra sulla mia posizione' }),
    )

    expect(await screen.findByText(/fuori dalla Toscana/i)).toBeInTheDocument()
    expect(mapProp('camera')).toBeNull()
    expect(mapProp('user-position')).toBeNull()
  })
})

describe('analysis mode', () => {
  it('swaps the legend for the factors, turns on rain_trigger and leaves Tutte', async () => {
    window.history.replaceState(null, '', '/?species=combined')
    render(<App />)
    expect(
      screen.getByRole('heading', { name: 'Indice delle condizioni' }),
    ).toBeInTheDocument()

    const toggle = screen.getByRole('button', { name: 'Analisi' })
    expect(toggle).toHaveAttribute('aria-pressed', 'false')
    await userEvent.click(toggle)

    expect(toggle).toHaveAttribute('aria-pressed', 'true')
    expect(window.location.search).toBe('?mode=analysis&f=rain_trigger')
    expect(screen.getByRole('radio', { name: 'Porcini' })).toBeChecked()
    expect(screen.getByRole('radio', { name: 'Tutte' })).toBeDisabled()
    expect(
      screen.getByRole('heading', { name: "Fattori dell'indice" }),
    ).toBeInTheDocument()
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
