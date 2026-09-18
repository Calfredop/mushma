import type {
  CellDetailResponse,
  Hotspot,
  OutlookResponse,
  SeasonMapResponse,
  SeasonsResponse,
} from '../api/queries'

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

// --- Time views (M6) ----------------------------------------------------------------------------

const month = (m: number, goodDays: number) => ({
  month: m,
  good_days: goodDays,
  rain: { total_mm: 100, normal_mm: 80 },
  temperature: { mean_c: 15, normal_c: 14.5 },
  sightings: m === 10 ? 2 : 0,
})

export const SEASONS: SeasonsResponse = {
  species: 'porcini',
  area: { code: null, name: 'Toscana', kind: 'region' },
  good_score: 0.6,
  baseline: {
    weather_years: [2022, 2023, 2024, 2025],
    score_years: [2022, 2023, 2024, 2025],
  },
  seasons: [
    {
      year: 2025,
      complete: true,
      through: '2025-12-31',
      good_days: 62,
      good_days_typical: 50,
      peak_date: '2025-09-24',
      peak_share: 0.87,
      window: { start: '2025-05-01', end: '2025-12-20' },
      rain: { total_mm: 1150, normal_mm: 1000 },
      temperature: { mean_c: 16.8, normal_c: 17.2 },
      weather_through: '2025-12-20',
      sightings: 15,
      months: [month(9, 16), month(10, 22)],
    },
    {
      year: 2026,
      complete: false,
      through: '2026-09-17',
      good_days: 4,
      good_days_typical: 19,
      peak_date: '2026-06-02',
      peak_share: 0.2,
      window: { start: '2026-05-01', end: '2026-12-20' },
      rain: { total_mm: 364, normal_mm: 420 },
      temperature: { mean_c: 22.6, normal_c: 20.9 },
      weather_through: '2026-09-11',
      sightings: 1,
      months: [month(6, 3)],
    },
  ],
}

export const SEASON_MAP: SeasonMapResponse = {
  year: 2025,
  species: 'porcini',
  complete: true,
  through: '2025-12-31',
  good_score: 0.6,
  cells: [{ cell_id: '1kmE4365N2248', lon: 10.4, lat: 44.1, good_days: 115 }],
  comuni: [
    {
      code: '046009',
      name: 'Careggine',
      good_days: 115,
      good_days_typical: 105,
      rain: null,
      temperature: null,
      sightings: 0,
    },
  ],
}

export const OUTLOOK: OutlookResponse = {
  species: 'porcini',
  area: { code: '051030', name: 'Pieve Santo Stefano', kind: 'comune' },
  issued: '2026-09-18',
  good_share: 0.25,
  rain_lead: { min_days: 10, max_days: 16 },
  rain_tilt: { wetter_pct: 125, drier_pct: 75 },
  baseline: {
    weather_years: [2022, 2023, 2024, 2025],
    score_years: [2022, 2023, 2024, 2025],
  },
  window: { start: '2026-05-01', end: '2026-12-20' },
  season_to_date: {
    through: '2026-09-17',
    good_days: 1,
    good_days_typical: 26,
    rain: { total_mm: 361, normal_mm: 495 },
    temperature: { mean_c: 22.4, normal_c: 20.6 },
    weather_through: '2026-09-11',
    sightings: 0,
  },
  periods: [
    {
      start: '2026-09-28',
      end: '2026-10-04',
      kind: 'week',
      past_good_years: 4,
      past_years: 4,
      rain: { total_mm: 20, normal_mm: 27 },
      temperature_anomaly_c: 2.8,
      lead_rain_pct: 26,
      outlook: 'worse',
    },
    {
      start: '2026-11-02',
      end: '2026-11-30',
      kind: 'month',
      past_good_years: 3,
      past_years: 4,
      rain: { total_mm: 121, normal_mm: 107 },
      temperature_anomaly_c: 1,
      lead_rain_pct: 130,
      outlook: 'better',
    },
  ],
}
