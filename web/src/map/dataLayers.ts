/**
 * mushma's own sources and layers, merged into the basemap style up front so
 * the map's first complete render already includes the score cells.
 *
 * Scores (and analysis factors) draw as soft "clouds": blurred overlapping
 * circles so neighbouring patches blend and woodland edges feather out,
 * instead of hard dots that morph into 1 km squares.
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

const LAGO = '#1F56A0'
const CARTA = '#F8FAF6'
const LICHENE = '#EDF0EA'
const SCORE = scoreStepExpression(['get', 'score']) as ExpressionSpecification

/** How soft the cloud edge is. MapLibre: 1 → only the centre stays full opacity. */
export const CLOUD_BLUR = 0.85

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

/** The Bosco layer's opacity when it's on. Off is 0, set directly. */
export const FOREST_CLOUD_OPACITY = 0.85

/** What the cells' `score` property holds: a day's conditions score, or a season's good days. */
export type CellScale = 'score' | 'goodDays'

export function cellColor(scale: CellScale): ExpressionSpecification {
  return scale === 'score'
    ? SCORE
    : (goodDaysStepExpression(['get', 'score']) as ExpressionSpecification)
}

export const EMPTY_COLLECTION = { type: 'FeatureCollection' as const, features: [] }

/** Invisible 1 km hit fill a tap can land on (score mode). */
export const CELL_LAYERS = ['cells-hit']

/** Score-mode layers toggled together: hit target + visible cloud. */
export const SCORE_LAYERS = ['cells-hit', 'cells-cloud']

/** Invisible 1 km hit fill in analysis mode. */
export const ANALYSIS_CELL_LAYERS = ['factors-base-hit']

/** Analysis-mode layers toggled together: hit target + Bosco/woodland cloud. */
export const ANALYSIS_LAYERS = ['factors-base-hit', 'factors-base-cloud']

/** Indicator clouds go in here: over the cells, under the basemap's roads. */
export const ANALYSIS_LAYERS_BEFORE = DATA_LAYERS_BEFORE

/**
 * Soft cloud radius in screen pixels. Sized so blobs cover roughly a 1 km cell
 * from mid-zoom up and still read as patches when the whole region is in view.
 */
const CELL_CLOUD_RADIUS: ExpressionSpecification = [
  'interpolate',
  ['linear'],
  ['zoom'],
  6,
  7,
  8,
  14,
  10,
  24,
  12,
  42,
  14,
  78,
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
  // Invisible 1 km squares: tap targets. The cloud is visual only.
  {
    id: 'cells-hit',
    type: 'fill',
    source: 'cells-squares',
    paint: { 'fill-color': '#000', 'fill-opacity': 0 },
  },
  {
    id: 'cells-cloud',
    type: 'circle',
    source: 'cells-points',
    paint: {
      'circle-color': SCORE,
      'circle-radius': CELL_CLOUD_RADIUS,
      'circle-blur': CLOUD_BLUR,
      'circle-opacity': 0.78,
    },
  },
  // Analysis mode: where the woodland is (and -- when Bosco is on -- forest type), what a
  // tap lands on, under the indicator clouds. Hidden with the scores on. Bosco off is
  // 'circle-opacity' 0 (ConditionsMap sets it).
  {
    id: 'factors-base-hit',
    type: 'fill',
    source: 'cells-squares',
    layout: { visibility: 'none' },
    paint: { 'fill-color': '#000', 'fill-opacity': 0 },
  },
  {
    id: 'factors-base-cloud',
    type: 'circle',
    source: 'cells-points',
    layout: { visibility: 'none' },
    paint: {
      'circle-color': FOREST_FILL,
      'circle-opacity': 0,
      'circle-radius': CELL_CLOUD_RADIUS,
      'circle-blur': CLOUD_BLUR,
    },
  },
]

export interface ActiveIndicator {
  id: string
  color: string
}

/**
 * Analysis mode: one soft cloud per indicator, bottom to top. A cell's opacity is the
 * factor's value times the layer's share of the cap (`layerOpacities`); a cell whose rules
 * lack the factor isn't drawn.
 */
export function analysisLayers(active: readonly ActiveIndicator[]): LayerSpecification[] {
  const shares = layerOpacities(active.length)
  return active.map(({ id, color }, i): LayerSpecification => {
    const opacity: ExpressionSpecification = ['*', ['get', id], shares[i]]
    const filter: FilterSpecification = ['has', id]
    return {
      id: `indicator-cloud-${id}`,
      type: 'circle',
      source: 'cells-points',
      filter,
      paint: {
        'circle-color': color,
        'circle-radius': CELL_CLOUD_RADIUS,
        'circle-blur': CLOUD_BLUR,
        'circle-opacity': opacity,
      },
    }
  })
}

/** Above everything in the basemap, labels included. */
const TOP_LAYER_SPECS: LayerSpecification[] = [
  // Everything outside the region is veiled; the region is a hole in it.
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
  // A searched, tapped or GPS point, tied to the woodland cell that answers for it.
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
  // Sightings ring the cell, so its score colour stays visible; the count sits beside it.
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
      sightings: empty(),
      'spot-point': empty(),
      'region-mask': { type: 'geojson', data: regionMask(region) },
    },
    layers,
  }
}
