/**
 * mushma's own sources and layers, merged into the basemap style up front so
 * the map's first complete render already includes the score cells.
 */
import type {
  ExpressionSpecification,
  LayerSpecification,
  SourceSpecification,
  StyleSpecification,
} from 'maplibre-gl'
import { goodDaysStepExpression, scoreStepExpression } from '../score/scale'
import { DATA_LAYERS_BEFORE, LABEL_FONT } from './basemap'

const LAGO = '#1F56A0'
const HUMUS = '#1C211D'
const CARTA = '#F8FAF6'
const LICHENE = '#EDF0EA'
const SCORE = scoreStepExpression(['get', 'score']) as ExpressionSpecification

/** What the cells' `score` property holds: a day's conditions score, or a season's good days. */
export type CellScale = 'score' | 'goodDays'

export function cellColor(scale: CellScale): ExpressionSpecification {
  return scale === 'score'
    ? SCORE
    : (goodDaysStepExpression(['get', 'score']) as ExpressionSpecification)
}

export const EMPTY_COLLECTION = { type: 'FeatureCollection' as const, features: [] }

/** Layers a tap can land on, nearest first. */
export const CELL_LAYERS = ['cells-fill', 'cells-dot']

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
  // Region view: a dot per cell, fading out as the true 1 km squares appear.
  {
    id: 'cells-dot',
    type: 'circle',
    source: 'cells-points',
    maxzoom: 11,
    paint: {
      'circle-color': SCORE,
      'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 3.5, 8, 5, 10.5, 7],
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
    paint: { 'line-color': HUMUS, 'line-opacity': 0.18, 'line-width': 0.6 },
  },
]

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
