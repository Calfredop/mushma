/**
 * The hub map's region layers: every Italian region's boundary, the served ones filled with
 * their mean conditions score and labelled, a hovered one outlined. Pure style data, so the
 * expressions are unit tested; `HubMap` adds them to the map.
 */
import type {
  DataDrivenPropertyValueSpecification,
  ExpressionSpecification,
  LayerSpecification,
  Map as MapLibreMap,
} from 'maplibre-gl'
import type { Language } from '../i18n'
import type { HubRegion } from '../pages/hubRegions'
import type { RegionBoundaries } from '../regions/boundaries'
import { scoreColor } from '../score/scale'
import { LABEL_FONT } from './basemap'

export const HUB_REGIONS_SOURCE = 'hub-regions'
export const HUB_LABELS_SOURCE = 'hub-region-labels'
export const HUB_FILL_LAYER = 'hub-regions-fill'
const HUB_LINE_LAYER = 'hub-regions-line'
const HUB_HOVER_LAYER = 'hub-regions-hover'
const HUB_LABEL_LAYER = 'hub-regions-label'

/** A served region with no score today yet: lighter than the land, so it still reads as open. */
export const NO_SCORE_COLOR = '#F8FAF6'
const CLEAR = 'rgba(0, 0, 0, 0)'
const INK = '#1C211D'
const MUTED = '#8F9A92'
const HALO = '#EDF0EA'

const slug: ExpressionSpecification = ['get', 'slug']
const hovered: ExpressionSpecification = ['boolean', ['feature-state', 'hover'], false]

/** `match` needs at least one label; with none, every region takes the fallback. */
function bySlug<T>(
  outputs: [string, T][],
  fallback: T,
): DataDrivenPropertyValueSpecification<T> {
  if (outputs.length === 0) return fallback as DataDrivenPropertyValueSpecification<T>
  return [
    'match',
    slug,
    ...outputs.flat(),
    fallback,
  ] as unknown as DataDrivenPropertyValueSpecification<T>
}

function servedOr<T>(
  regions: HubRegion[],
  served: T | ExpressionSpecification,
  other: T,
): DataDrivenPropertyValueSpecification<T> {
  if (regions.length === 0) return other as DataDrivenPropertyValueSpecification<T>
  return [
    'match',
    slug,
    regions.map((r) => r.region.slug),
    served,
    other,
  ] as unknown as DataDrivenPropertyValueSpecification<T>
}

export function regionFillColor(
  regions: HubRegion[],
): DataDrivenPropertyValueSpecification<string> {
  return bySlug(
    regions.map((r) => [
      r.region.slug,
      r.meanScore === undefined ? NO_SCORE_COLOR : scoreColor(r.meanScore),
    ]),
    CLEAR,
  )
}

/** Unserved regions stay in the layer, clear, so a tap on one can still say it isn't covered. */
export function regionFillOpacity(
  regions: HubRegion[],
): DataDrivenPropertyValueSpecification<number> {
  return servedOr(regions, ['case', hovered, 0.92, 0.72], 0)
}

function lineColor(regions: HubRegion[]) {
  return servedOr(regions, INK, MUTED)
}

function lineWidth(regions: HubRegion[]) {
  return servedOr(regions, 1.25, 0.75)
}

function lineOpacity(regions: HubRegion[]) {
  return servedOr(regions, 0.7, 0.55)
}

/** One point per served region, named in the UI language. */
export function regionLabelPoints(
  boundaries: RegionBoundaries,
  regions: HubRegion[],
  language: Language,
): GeoJSON.FeatureCollection<GeoJSON.Point, { slug: string; name: string }> {
  const bySlugName = new Map(regions.map((r) => [r.region.slug, r.region.name[language]]))
  return {
    type: 'FeatureCollection',
    features: boundaries.features.flatMap((feature) => {
      const name = bySlugName.get(feature.properties.slug)
      if (name === undefined) return []
      return [
        {
          type: 'Feature' as const,
          properties: { slug: feature.properties.slug, name },
          geometry: { type: 'Point' as const, coordinates: feature.properties.label },
        },
      ]
    }),
  }
}

/**
 * The fill goes under the basemap's roads and places (`beneath`), the borders and the hover ring
 * above them (`above`, the first label layer), and the region names on top.
 */
export function hubLayers(regions: HubRegion[]): {
  beneath: LayerSpecification[]
  above: LayerSpecification[]
  top: LayerSpecification[]
} {
  return {
    beneath: [
      {
        id: HUB_FILL_LAYER,
        type: 'fill',
        source: HUB_REGIONS_SOURCE,
        paint: {
          'fill-color': regionFillColor(regions),
          'fill-opacity': regionFillOpacity(regions),
        },
      },
    ],
    above: [
      {
        id: HUB_LINE_LAYER,
        type: 'line',
        source: HUB_REGIONS_SOURCE,
        layout: { 'line-join': 'round' },
        paint: {
          'line-color': lineColor(regions),
          'line-width': lineWidth(regions),
          'line-opacity': lineOpacity(regions),
        },
      },
      {
        id: HUB_HOVER_LAYER,
        type: 'line',
        source: HUB_REGIONS_SOURCE,
        layout: { 'line-join': 'round' },
        paint: {
          'line-color': INK,
          'line-width': 2.5,
          'line-opacity': ['case', hovered, 1, 0],
        },
      },
    ],
    top: [
      {
        id: HUB_LABEL_LAYER,
        type: 'symbol',
        source: HUB_LABELS_SOURCE,
        layout: {
          'text-field': ['get', 'name'],
          'text-font': LABEL_FONT,
          'text-size': ['interpolate', ['linear'], ['zoom'], 4, 11, 7, 15],
          'text-max-width': 8,
        },
        paint: {
          'text-color': INK,
          'text-halo-color': HALO,
          'text-halo-width': 1.5,
        },
      },
    ],
  }
}

/** Repaints the layers that depend on which regions are served and their scores. */
export function applyHubPaint(
  map: Pick<MapLibreMap, 'setPaintProperty'>,
  regions: HubRegion[],
) {
  map.setPaintProperty(HUB_FILL_LAYER, 'fill-color', regionFillColor(regions))
  map.setPaintProperty(HUB_FILL_LAYER, 'fill-opacity', regionFillOpacity(regions))
  map.setPaintProperty(HUB_LINE_LAYER, 'line-color', lineColor(regions))
  map.setPaintProperty(HUB_LINE_LAYER, 'line-width', lineWidth(regions))
  map.setPaintProperty(HUB_LINE_LAYER, 'line-opacity', lineOpacity(regions))
}
