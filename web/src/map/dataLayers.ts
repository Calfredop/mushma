/**
 * mushma's own sources and layers, merged into the basemap style up front so
 * the map's first complete render already includes the score cells.
 *
 * Two score styles share the same hit targets:
 * - cloud: one pre-blurred score raster (see cloudRaster.ts) so neighbours blend
 *   without heatmap/circle-blur lattice artefacts, and empty space stays clear
 * - squircle: dots that morph into 1 km squares (the discrete cell view)
 */
import type {
  ExpressionSpecification,
  FilterSpecification,
  LayerSpecification,
  SourceSpecification,
  StyleSpecification,
} from 'maplibre-gl'
import { FOREST_COLOR_BY_HABITAT, NEUTRAL_FOREST_COLOR } from '../score/forestColors'
import { layerOpacities } from '../score/indicators'
import { goodDaysStepExpression, scoreStepExpression } from '../score/scale'
import { DATA_LAYERS_BEFORE, LABEL_FONT } from './basemap'
import { EMPTY_CLOUD_DATA_URL, cloudImageCoordinates } from './cloudRaster'

const LAGO = '#1F56A0'
const HUMUS = '#1C211D'
const CARTA = '#F8FAF6'
const LICHENE = '#EDF0EA'
const SCORE = scoreStepExpression(['get', 'score']) as ExpressionSpecification

export const CELL_STYLES = ['cloud', 'squircle'] as const
export type CellStyle = (typeof CELL_STYLES)[number]

export function isCellStyle(value: string | null | undefined): value is CellStyle {
  return CELL_STYLES.includes(value as CellStyle)
}

/** Bosco layer: each habitat's colour, categorical -- a cell's forest type has no
 * favourable/unfavourable direction, so unlike the score or a factor this isn't a value×opacity
 * blend, just a fixed fill. An unknown or missing forest_type draws in the neutral grey. */
const FOREST_FILL = [
  'match',
  ['get', 'forest_type'],
  ...Object.entries(FOREST_COLOR_BY_HABITAT).flatMap(([habitat, { color }]) => [
    habitat,
    color,
  ]),
  NEUTRAL_FOREST_COLOR,
] as unknown as ExpressionSpecification

/** The Bosco layer's opacity when it's on, fading with the squircle morph. Off is 0. */
export const FOREST_DOT_OPACITY: ExpressionSpecification = [
  'interpolate',
  ['linear'],
  ['zoom'],
  9.5,
  0.85,
  10.5,
  0,
]
export const FOREST_FILL_OPACITY: ExpressionSpecification = [
  'interpolate',
  ['linear'],
  ['zoom'],
  9,
  0,
  10.5,
  0.85,
]

/** What the cells' `score` property holds: a day's conditions score, or a season's good days. */
export type CellScale = 'score' | 'goodDays'

export function cellColor(scale: CellScale): ExpressionSpecification {
  return scale === 'score'
    ? SCORE
    : (goodDaysStepExpression(['get', 'score']) as ExpressionSpecification)
}

export const EMPTY_COLLECTION = { type: 'FeatureCollection' as const, features: [] }

/** Invisible 1 km hit fill a tap can land on (either score style). */
export const CELL_LAYERS = ['cells-hit']

/** Score layers for the soft continuous field. */
export const SCORE_CLOUD_LAYERS = ['cells-hit', 'cells-cloud'] as const

/** Score layers for the discrete dot→square view. */
export const SCORE_SQUIRCLE_LAYERS = [
  'cells-hit',
  'cells-dot',
  'cells-fill',
  'cells-outline',
] as const

/** Every score-mode layer id (for hide-all when entering analysis). */
export const SCORE_LAYERS = [
  ...new Set([...SCORE_CLOUD_LAYERS, ...SCORE_SQUIRCLE_LAYERS]),
]

/** Layers a tap can land on in analysis mode. */
export const ANALYSIS_CELL_LAYERS = ['factors-base-fill', 'factors-base-dot']

/** Analysis-mode layers toggled together. */
export const ANALYSIS_LAYERS = ['factors-base-fill', 'factors-base-dot']

/** Indicator layers go in here: over the cells, under their outline and the basemap's roads. */
export const ANALYSIS_LAYERS_BEFORE = 'cells-outline'

const CELL_DOT_RADIUS: ExpressionSpecification = [
  'interpolate',
  ['linear'],
  ['zoom'],
  6,
  3.5,
  8,
  5,
  10.5,
  7,
]

type Bounds = [[number, number], [number, number]]

/** A world polygon with the region cut out of it. */
export function regionMask([[west, south], [east, north]]: Bounds) {
  return {
    type: 'Feature' as const,
    properties: {},
    geometry: {
      type: 'Polygon' as const,
      coordinates: [
        [
          [-180, -85],
          [180, -85],
          [180, 85],
          [-180, 85],
          [-180, -85],
        ],
        [
          [west, south],
          [west, north],
          [east, north],
          [east, south],
          [west, south],
        ],
      ],
    },
  }
}

const empty = (): SourceSpecification => ({ type: 'geojson', data: EMPTY_COLLECTION })

/** Under the basemap's roads and labels. */
const CELL_LAYER_SPECS: LayerSpecification[] = [
  // Invisible 1 km squares: tap targets for both styles.
  {
    id: 'cells-hit',
    type: 'fill',
    source: 'cells-squares',
    paint: { 'fill-color': '#000', 'fill-opacity': 0 },
  },
  // Cloud: one pre-blurred raster (painted in ConditionsMap). Transparent off woodland.
  {
    id: 'cells-cloud',
    type: 'raster',
    source: 'cells-cloud-raster',
    paint: {
      'raster-opacity': 1,
      'raster-fade-duration': 0,
    },
  },
  // Squircle: a dot per cell, fading into the true 1 km squares.
  {
    id: 'cells-dot',
    type: 'circle',
    source: 'cells-points',
    maxzoom: 11,
    layout: { visibility: 'none' },
    paint: {
      'circle-color': SCORE,
      'circle-radius': CELL_DOT_RADIUS,
      'circle-opacity': ['interpolate', ['linear'], ['zoom'], 9.5, 1, 10.5, 0],
      'circle-stroke-color': HUMUS,
      'circle-stroke-opacity': ['interpolate', ['linear'], ['zoom'], 9.5, 0.55, 10.5, 0],
      'circle-stroke-width': 0.8,
    },
  },
  {
    id: 'cells-fill',
    type: 'fill',
    source: 'cells-squares',
    minzoom: 9,
    layout: { visibility: 'none' },
    paint: {
      'fill-color': SCORE,
      'fill-opacity': ['interpolate', ['linear'], ['zoom'], 9, 0, 10.5, 0.82],
    },
  },
  {
    id: 'cells-outline',
    type: 'line',
    source: 'cells-squares',
    minzoom: 11,
    layout: { visibility: 'none' },
    paint: { 'line-color': HUMUS, 'line-opacity': 0.18, 'line-width': 0.6 },
  },
  // Analysis mode: woodland rings / Bosco under the indicator overlays. Hidden with the scores.
  {
    id: 'factors-base-dot',
    type: 'circle',
    source: 'cells-points',
    maxzoom: 11,
    layout: { visibility: 'none' },
    paint: {
      'circle-color': FOREST_FILL,
      'circle-opacity': 0,
      'circle-radius': CELL_DOT_RADIUS,
      'circle-stroke-color': HUMUS,
      'circle-stroke-opacity': ['interpolate', ['linear'], ['zoom'], 9.5, 0.3, 10.5, 0],
      'circle-stroke-width': 0.8,
    },
  },
  {
    id: 'factors-base-fill',
    type: 'fill',
    source: 'cells-squares',
    minzoom: 9,
    layout: { visibility: 'none' },
    paint: { 'fill-color': FOREST_FILL, 'fill-opacity': 0 },
  },
]

export interface ActiveIndicator {
  id: string
  color: string
}

/**
 * Analysis mode: a dot layer (below zoom 11) and a square layer (from 9) per indicator,
 * bottom to top. A cell's opacity is the factor's value times the layer's share of the
 * cap (`layerOpacities`); a cell whose rules lack the factor isn't drawn.
 */
export function analysisLayers(active: readonly ActiveIndicator[]): LayerSpecification[] {
  const shares = layerOpacities(active.length)
  return active.flatMap(({ id, color }, i): LayerSpecification[] => {
    const opacity: ExpressionSpecification = ['*', ['get', id], shares[i]]
    const filter: FilterSpecification = ['has', id]
    return [
      {
        id: `indicator-dot-${id}`,
        type: 'circle',
        source: 'cells-points',
        maxzoom: 11,
        filter,
        paint: {
          'circle-color': color,
          'circle-radius': CELL_DOT_RADIUS,
          'circle-opacity': ['interpolate', ['linear'], ['zoom'], 9.5, opacity, 10.5, 0],
        },
      },
      {
        id: `indicator-fill-${id}`,
        type: 'fill',
        source: 'cells-squares',
        minzoom: 9,
        filter,
        paint: {
          'fill-color': color,
          'fill-opacity': ['interpolate', ['linear'], ['zoom'], 9, 0, 10.5, opacity],
        },
      },
    ]
  })
}

/** Above everything in the basemap, labels included. */
const TOP_LAYER_SPECS: LayerSpecification[] = [
  {
    id: 'region-mask',
    type: 'fill',
    source: 'region-mask',
    paint: { 'fill-color': LICHENE, 'fill-opacity': 0.72 },
  },
  {
    id: 'cells-selected-dot',
    type: 'circle',
    source: 'cells-points',
    maxzoom: 10.5,
    filter: ['==', ['get', 'cell_id'], ''],
    paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 6, 10, 9],
      'circle-color': 'rgba(0,0,0,0)',
      'circle-stroke-color': LAGO,
      'circle-stroke-width': 3,
    },
  },
  {
    id: 'cells-selected',
    type: 'line',
    source: 'cells-squares',
    minzoom: 10.5,
    filter: ['==', ['get', 'cell_id'], ''],
    paint: { 'line-color': LAGO, 'line-width': 3 },
  },
  {
    id: 'spot-link',
    type: 'line',
    source: 'spot-point',
    filter: ['==', ['geometry-type'], 'LineString'],
    paint: { 'line-color': LAGO, 'line-width': 2, 'line-dasharray': [2, 2] },
  },
  {
    id: 'spot-point',
    type: 'circle',
    source: 'spot-point',
    filter: ['==', ['geometry-type'], 'Point'],
    paint: {
      'circle-radius': 6,
      'circle-color': CARTA,
      'circle-stroke-color': LAGO,
      'circle-stroke-width': 3,
    },
  },
  {
    id: 'sightings-circle',
    type: 'circle',
    source: 'sightings',
    layout: { visibility: 'none' },
    paint: {
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 8, 10, 11, 12, 22],
      'circle-color': 'rgba(0,0,0,0)',
      'circle-stroke-color': LAGO,
      'circle-stroke-width': 2,
    },
  },
  {
    id: 'sightings-count',
    type: 'symbol',
    source: 'sightings',
    layout: {
      visibility: 'none',
      'text-field': ['to-string', ['get', 'count']],
      'text-font': LABEL_FONT,
      'text-size': 12,
      'text-anchor': 'bottom-left',
      'text-offset': [
        'interpolate',
        ['linear'],
        ['zoom'],
        6,
        ['literal', [0.6, -0.4]],
        12,
        ['literal', [1.6, -1.4]],
      ],
      'text-allow-overlap': true,
      'text-ignore-placement': true,
    },
    paint: { 'text-color': LAGO, 'text-halo-color': CARTA, 'text-halo-width': 2 },
  },
]

export function withDataLayers(
  style: StyleSpecification,
  region: Bounds,
): StyleSpecification {
  const layers = [...style.layers]
  const at = layers.findIndex((layer) => layer.id === DATA_LAYERS_BEFORE)
  layers.splice(at === -1 ? layers.length : at, 0, ...CELL_LAYER_SPECS)
  layers.push(...TOP_LAYER_SPECS)
  return {
    ...style,
    sources: {
      ...style.sources,
      'cells-points': empty(),
      'cells-squares': empty(),
      'cells-cloud-raster': {
        type: 'image',
        url: EMPTY_CLOUD_DATA_URL,
        coordinates: cloudImageCoordinates(region),
      },
      sightings: empty(),
      'spot-point': empty(),
      'region-mask': { type: 'geojson', data: regionMask(region) },
    },
    layers,
  }
}
