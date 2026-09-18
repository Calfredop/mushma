import type { CellDetailResponse, Hotspot } from '../api/queries'

const factors = (scale: number) => [
  { key: 'season', i18n_key: 'factor.season', value: 1, contribution: 1 },
  { key: 'habitat', i18n_key: 'factor.habitat', value: 0.9, contribution: 0.9 },
  {
    key: 'rain_trigger',
    i18n_key: 'factor.rain_trigger',
    value: 0.5 * scale,
    contribution: 0.7 * scale,
  },
  { key: 'frost', i18n_key: 'factor.frost', value: 1, contribution: 1 },
]

const days = (species: string, base: number) =>
  [
    '2026-09-17',
    '2026-09-18',
    '2026-09-19',
    '2026-09-20',
    '2026-09-21',
    '2026-09-22',
    '2026-09-23',
    '2026-09-24',
  ].map((date, i) => {
    const scale = species === 'ovoli' ? 0 : 1 - i * 0.05
    const f = factors(scale)
    return { date, score: base * scale, factors: f }
  })

export const CELL_DETAIL: CellDetailResponse = {
  cell_id: '1kmN2438E4372',
  lon: 11.7333,
  lat: 43.85,
  place: { comune: 'Poppi', nearest_place: 'Camaldoli' },
  species: [
    { species: 'porcini', days: days('porcini', 0.63) },
    { species: 'ovoli', days: days('ovoli', 0.4) },
    { species: 'gallinacci', days: days('gallinacci', 0.81) },
  ],
}

export const HOTSPOTS: Hotspot[] = [
  {
    id: 'hotspot-1',
    place: { comune: 'Arcidosso', nearest_place: 'Bagnolo' },
    lon: 10.93,
    lat: 42.91,
    score: 0.72,
    cell_ids: ['a', 'b'],
    recent_sightings: 3,
  },
  {
    id: 'hotspot-2',
    place: { comune: 'Poppi', nearest_place: 'Camaldoli' },
    lon: 11.73,
    lat: 43.85,
    score: 0.41,
    cell_ids: ['c'],
    recent_sightings: 0,
  },
]
