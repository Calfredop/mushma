import {
  type ExpressionSpecification,
  type GeoJSONSource,
  Map as MapLibreMap,
  type MapMouseEvent,
  Marker,
} from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import type { Hotspot } from '../api/queries'
import type { components } from '../api/schema'
import { MinusIcon, PlusIcon } from '../components/icons'
import {
  BASEMAP_URL,
  CELL_SIZE_KM,
  DEFAULT_REGION_SLUG,
  REGIONS,
  TERRAIN_URL,
} from '../config'
import type { RegionDefinition } from '../regions'
import type { Language } from '../i18n'
import type { CameraRequest } from '../state/AppState'
import { boundsAround, distanceKm, OUTSIDE_CELL_KM } from '../geo/distance'
import { basemapLayers, buildMapStyle, DATA_LAYERS_BEFORE, hillshade } from './basemap'
import styles from './ConditionsMap.module.css'
import { inView, type MapPadding, mergePadding } from './padding'
import { mapLocale, registerPmtiles } from './setup'
import {
  type ActiveIndicator,
  ANALYSIS_CELL_LAYERS,
  ANALYSIS_LAYERS_BEFORE,
  analysisLayers,
  CELL_LAYERS,
  type CellScale,
  cellColor,
  EMPTY_COLLECTION as EMPTY,
  FOREST_DOT_OPACITY,
  FOREST_FILL_OPACITY,
  withDataLayers,
} from './dataLayers'
import {
  cellsToPoints,
  cellsToSquares,
  factorCellsToPoints,
  factorCellsToSquares,
  type ForestTypesByCell,
  sightingsToPoints,
} from './geojson'

type GridCellScore = components['schemas']['GridCellScore']
type CellFactors = components['schemas']['CellFactors']

/** Analysis mode: the factors behind the score instead of the score. */
export interface AnalysisView {
  /** The day's factor rows, or undefined while they load or on a day without factors. */
  cells: CellFactors[] | undefined
  /** The response's factor ids, in the order of each cell's `values`. */
  ids: readonly string[]
  /** The indicators to draw, bottom to top. */
  active: readonly ActiveIndicator[]
  /** The Bosco toggle: each cell's dominant forest type, and whether it's drawn. Static --
   * doesn't depend on species or day -- so it's merged onto the same cell sources regardless of
   * which factors are on. */
  forestTypes?: { byCellId: ForestTypesByCell | undefined; on: boolean }
}

declare global {
  interface Window {
    /** Dev-only handle for the end-to-end test. */
    __mushmaMap?: MapLibreMap
  }
}

const CLICK_TOLERANCE_PX = 10

/** Relief under the score cells. Added after the first paint, so it never delays it. */
function addRelief(map: MapLibreMap) {
  if (!TERRAIN_URL || map.getSource('terrain')) return
  const relief = hillshade(TERRAIN_URL)
  map.addSource('terrain', relief.source)
  map.addLayer(relief.layer, map.getLayer('cells-dot') ? 'cells-dot' : DATA_LAYERS_BEFORE)
}

/** Keeps fitted features clear of the species bar (top) and legend and dates (bottom). */
function overlayPadding(map: MapLibreMap): MapPadding {
  const height = map.getContainer().clientHeight
  return {
    top: Math.min(80, height * 0.2),
    bottom: Math.min(150, height * 0.35),
    left: 48,
    right: 64,
  }
}

const prefersReducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false

interface MapCallbacks {
  onCellClick: (cellId: string, lat: number, lon: number) => void
  onPointClick: (lat: number, lon: number) => void
  onReady: () => void
  /** What a tap can land on, the square layer first: it follows the mode. */
  cellLayers: string[]
}

type MapRegion = Pick<RegionDefinition, 'bounds' | 'maxBounds' | 'minZoom' | 'maxZoom'>

function createMap(
  container: HTMLDivElement,
  lang: Language,
  locale: Record<string, string>,
  region: MapRegion,
  padding: MapPadding | undefined,
  callbacks: { current: MapCallbacks },
): MapLibreMap {
  registerPmtiles()
  const map = new MapLibreMap({
    container,
    style: withDataLayers(
      buildMapStyle({ basemapUrl: BASEMAP_URL, lang }),
      region.bounds,
    ),
    bounds: region.bounds,
    // The region opens in the part of the map nothing covers.
    fitBoundsOptions: {
      padding: mergePadding({ top: 24, bottom: 24, left: 24, right: 24 }, padding),
    },
    maxBounds: region.maxBounds,
    minZoom: region.minZoom,
    maxZoom: region.maxZoom,
    dragRotate: false,
    pitchWithRotate: false,
    touchPitch: false,
    attributionControl: { compact: true },
    locale,
  })
  performance.mark('mushma:map-created')
  map.touchZoomRotate.disableRotation()
  map.keyboard.disableRotation()
  if (import.meta.env.DEV) window.__mushmaMap = map

  // Sources exist once the style has loaded; data can flow in from then on.
  map.once('style.load', () => callbacks.current.onReady())
  map.once('load', () => {
    performance.mark('mushma:map-loaded')
    // Relief normally follows the first paint; don't lose it if scores never arrive.
    const relief = setTimeout(() => addRelief(map), 8000)
    map.once('remove', () => clearTimeout(relief))
  })

  const pickCell = (event: MapMouseEvent) => {
    const { x, y } = event.point
    const layers = callbacks.current.cellLayers
    const features = map.queryRenderedFeatures(
      [
        [x - CLICK_TOLERANCE_PX, y - CLICK_TOLERANCE_PX],
        [x + CLICK_TOLERANCE_PX, y + CLICK_TOLERANCE_PX],
      ],
      { layers },
    )
    // Inside a square wins; otherwise the nearest dot.
    const inside = map.queryRenderedFeatures(event.point, { layers: [layers[0]] })[0]
    if (inside) return String(inside.properties.cell_id)
    let best: { id: string; distance: number } | undefined
    for (const feature of features) {
      if (feature.geometry.type !== 'Point') continue
      const [lon, lat] = feature.geometry.coordinates
      const p = map.project([lon, lat])
      const distance = Math.hypot(p.x - x, p.y - y)
      if (!best || distance < best.distance) {
        best = { id: String(feature.properties.cell_id), distance }
      }
    }
    return best?.id
  }

  map.on('click', (event) => {
    const cellId = pickCell(event)
    if (cellId) callbacks.current.onCellClick(cellId, event.lngLat.lat, event.lngLat.lng)
    else callbacks.current.onPointClick(event.lngLat.lat, event.lngLat.lng)
  })
  map.on('mousemove', (event) => {
    map.getCanvas().style.cursor = pickCell(event) ? 'pointer' : ''
  })

  return map
}

interface Props {
  cells: GridCellScore[] | undefined
  /** What `cells[].score` holds: a day's conditions score (default) or a season's good days. */
  scale?: CellScale
  /** Analysis mode, drawn instead of `cells`; null or omitted for the scores. */
  analysis?: AnalysisView | null
  selectedCellId: string | null
  /** Sighting totals per cell, or undefined to hide the overlay. */
  sightings: Map<string, number> | undefined
  hotspots: Hotspot[] | undefined
  camera: CameraRequest | null
  /** A point spot and, once resolved, the centre of the cell that answers for it. */
  spotPoint: { point: [number, number]; cell?: [number, number] } | null
  /** The visitor's last GPS fix, or null before one. */
  userPosition: { lat: number; lon: number } | null
  lang: Language
  /** Defaults to the default region. Read once, at map creation. */
  region?: MapRegion
  /** What covers the map's edges (the sheet, the controls): camera moves keep clear of it. */
  padding?: MapPadding
  onCellClick: (cellId: string, lat: number, lon: number) => void
  onPointClick: (lat: number, lon: number) => void
  onHotspotClick: (hotspot: Hotspot) => void
}

export function ConditionsMap({
  cells,
  scale = 'score',
  analysis = null,
  selectedCellId,
  sightings,
  hotspots,
  camera,
  spotPoint,
  userPosition,
  lang,
  region = REGIONS[DEFAULT_REGION_SLUG],
  padding,
  onCellClick,
  onPointClick,
  onHotspotClick,
}: Props) {
  const { t } = useTranslation()
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<MapLibreMap | null>(null)
  const [ready, setReady] = useState(false)
  const inAnalysis = analysis !== null
  const callbacks = useRef({
    onCellClick,
    onPointClick,
    onHotspotClick,
    onReady: () => setReady(true),
    cellLayers: inAnalysis ? ANALYSIS_CELL_LAYERS : CELL_LAYERS,
  })
  const initialLang = useRef(lang)
  const initialLocale = useRef(mapLocale(t))
  const initialRegion = useRef(region)
  const paddingRef = useRef(padding)

  useEffect(() => {
    paddingRef.current = padding
  }, [padding])

  useEffect(() => {
    callbacks.current = {
      onCellClick,
      onPointClick,
      onHotspotClick,
      onReady: () => setReady(true),
      cellLayers: inAnalysis ? ANALYSIS_CELL_LAYERS : CELL_LAYERS,
    }
  })

  // Create the map once, after the app shell has painted: setting up WebGL
  // is the slowest step on a phone and shouldn't hold back everything else.
  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    let map: MapLibreMap | undefined
    let timer: ReturnType<typeof setTimeout> | undefined
    const frame = requestAnimationFrame(() => {
      timer = setTimeout(() => {
        map = createMap(
          container,
          initialLang.current,
          initialLocale.current,
          initialRegion.current,
          paddingRef.current,
          callbacks,
        )
        mapRef.current = map
      })
    })
    return () => {
      cancelAnimationFrame(frame)
      clearTimeout(timer)
      if (!map) return
      map.remove()
      mapRef.current = null
      if (window.__mushmaMap === map) delete window.__mushmaMap
      setReady(false)
    }
  }, [])

  // Scores, or in analysis mode the factors: both on the same cell sources. The Bosco layer's
  // forest types ride along on the same sources too (merged in by cell_id) since they're static
  // grid data, not a species/day factor -- so toggling Bosco never needs its own setData.
  const factorCells = analysis?.cells
  const factorIds = analysis?.ids
  const forestByCellId = analysis?.forestTypes?.byCellId
  const drawn = inAnalysis ? factorCells : cells
  const firstPaintMarked = useRef(false)
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    const points = map.getSource<GeoJSONSource>('cells-points')
    const squares = map.getSource<GeoJSONSource>('cells-squares')
    if (inAnalysis) {
      const data = factorCells ?? []
      points?.setData(factorCellsToPoints(data, factorIds ?? [], forestByCellId))
      squares?.setData(
        factorCellsToSquares(data, factorIds ?? [], CELL_SIZE_KM, forestByCellId),
      )
    } else {
      const data = cells ?? []
      points?.setData(cellsToPoints(data))
      squares?.setData(cellsToSquares(data, CELL_SIZE_KM))
    }
    if (drawn && !firstPaintMarked.current) {
      firstPaintMarked.current = true
      // First map paint: basemap and score cells drawn (PRD → Mobile performance).
      map.once('idle', () => {
        performance.mark('mushma:first-map-paint')
        addRelief(map)
      })
    }
  }, [cells, inAnalysis, factorCells, factorIds, forestByCellId, drawn, ready])

  // Analysis mode hides the score colours; its base layers show where the woodland is and take
  // the taps.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    for (const id of CELL_LAYERS) {
      map.setLayoutProperty(id, 'visibility', inAnalysis ? 'none' : 'visible')
    }
    for (const id of ANALYSIS_CELL_LAYERS) {
      map.setLayoutProperty(id, 'visibility', inAnalysis ? 'visible' : 'none')
    }
  }, [inAnalysis, ready])

  // The indicators that are on, one dot and one square layer each, rebuilt when the set changes.
  const indicatorsKey = JSON.stringify(analysis?.active ?? [])
  const indicatorLayers = useRef<string[]>([])
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    for (const id of indicatorLayers.current) {
      if (map.getLayer(id)) map.removeLayer(id)
    }
    indicatorLayers.current = []
    if (!inAnalysis) return
    const active = JSON.parse(indicatorsKey) as ActiveIndicator[]
    for (const layer of analysisLayers(active)) {
      map.addLayer(layer, ANALYSIS_LAYERS_BEFORE)
      indicatorLayers.current.push(layer.id)
    }
  }, [indicatorsKey, inAnalysis, ready])

  // Bosco layer: the base fill/dot's own colour is always the forest-type expression (set once,
  // in dataLayers.ts); only the opacity toggles, so switching it on never needs a setData.
  const forestOn = inAnalysis && (analysis?.forestTypes?.on ?? false)
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    map.setPaintProperty(
      'factors-base-dot',
      'circle-opacity',
      forestOn ? FOREST_DOT_OPACITY : 0,
    )
    map.setPaintProperty(
      'factors-base-fill',
      'fill-opacity',
      forestOn ? FOREST_FILL_OPACITY : 0,
    )
  }, [forestOn, ready])

  // Colour scale: a day's score, or a season's good days.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    map.setPaintProperty('cells-dot', 'circle-color', cellColor(scale))
    map.setPaintProperty('cells-fill', 'fill-color', cellColor(scale))
  }, [scale, ready])

  // Selection.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    const filter: ExpressionSpecification = [
      '==',
      ['get', 'cell_id'],
      selectedCellId ?? '',
    ]
    map.setFilter('cells-selected', filter)
    map.setFilter('cells-selected-dot', filter)
  }, [selectedCellId, ready])

  // Sightings overlay.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    const visible = sightings !== undefined
    map
      .getSource<GeoJSONSource>('sightings')
      ?.setData(visible ? sightingsToPoints(sightings, drawn ?? []) : EMPTY)
    for (const id of ['sightings-circle', 'sightings-count']) {
      map.setLayoutProperty(id, 'visibility', visible ? 'visible' : 'none')
    }
  }, [sightings, drawn, ready])

  // Hot places, as numbered markers linked to the list.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready || !hotspots) return
    const markers = hotspots.map((hotspot, index) => {
      const element = document.createElement('button')
      element.type = 'button'
      element.className = styles.hotspot
      element.textContent = String(index + 1)
      element.setAttribute(
        'aria-label',
        t('hotspots.show', { place: hotspot.place.nearest_place }),
      )
      element.addEventListener('click', (event) => {
        event.stopPropagation()
        callbacks.current.onHotspotClick(hotspot)
      })
      return new Marker({ element, anchor: 'bottom' })
        .setLngLat([hotspot.lon, hotspot.lat])
        .addTo(map)
    })
    return () => markers.forEach((marker) => marker.remove())
  }, [hotspots, ready, t])

  // "You are here", a dot that lets taps through to the map below it.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready || !userPosition) return
    const element = document.createElement('div')
    element.className = styles.userPosition
    element.setAttribute('role', 'img')
    element.setAttribute('aria-label', t('map.userPosition'))
    const marker = new Marker({ element })
      .setLngLat([userPosition.lon, userPosition.lat])
      .addTo(map)
    return () => void marker.remove()
  }, [userPosition, ready, t])

  // Camera requests (search, GPS, hot places, a tap). Declared before the spot effect so a
  // framed spot-and-cell view wins over the fly-to. The padding keeps the place clear of what
  // covers the map, such as the phone's sheet.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready || !camera) return
    const center: [number, number] = [camera.lon, camera.lat]
    const pad = paddingRef.current
    if (camera.zoom === undefined) {
      // No zoom: only reveal it. A tapped place already in the clear stays where it is.
      const container = map.getContainer()
      const size = { width: container.clientWidth, height: container.clientHeight }
      if (inView(map.project(center), size, pad)) return
      map.easeTo({ center, padding: pad, duration: prefersReducedMotion() ? 0 : 400 })
    } else if (prefersReducedMotion()) {
      map.jumpTo({ center, zoom: camera.zoom, padding: pad })
    } else {
      map.flyTo({ center, zoom: camera.zoom, padding: pad, duration: 1400 })
    }
  }, [camera, ready])

  // Spot point, its link to a distant cell, and a view that shows both.
  const spotKey = JSON.stringify(spotPoint)
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    const spot =
      spotKey === 'null' ? null : (JSON.parse(spotKey) as NonNullable<typeof spotPoint>)
    const source = map.getSource<GeoJSONSource>('spot-point')
    if (!spot) {
      source?.setData(EMPTY)
      return
    }
    const [lon, lat] = spot.point
    const far =
      spot.cell !== undefined &&
      distanceKm(lat, lon, spot.cell[1], spot.cell[0]) > OUTSIDE_CELL_KM
    source?.setData({
      type: 'FeatureCollection',
      features: [
        ...(far && spot.cell
          ? [
              {
                type: 'Feature' as const,
                properties: {},
                geometry: {
                  type: 'LineString' as const,
                  coordinates: [spot.point, spot.cell],
                },
              },
            ]
          : []),
        {
          type: 'Feature' as const,
          properties: {},
          geometry: { type: 'Point' as const, coordinates: spot.point },
        },
      ],
    })
    if (far && spot.cell) {
      map.fitBounds(boundsAround(spot.point, spot.cell), {
        padding: mergePadding(overlayPadding(map), paddingRef.current),
        maxZoom: 12,
        animate: !prefersReducedMotion(),
      })
    }
  }, [spotKey, ready])

  // MapLibre's own UI strings follow a language switch (they're set once at creation).
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready) return
    const locale = mapLocale(t)
    map.getCanvas().setAttribute('aria-label', locale['Map.Title'])
    const button = map.getContainer().querySelector('.maplibregl-ctrl-attrib-button')
    button?.setAttribute('title', locale['AttributionControl.ToggleAttribution'])
    button?.setAttribute('aria-label', locale['AttributionControl.ToggleAttribution'])
  }, [t, ready])

  // Basemap label language.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready || !BASEMAP_URL) return
    for (const layer of basemapLayers(lang)) {
      if (
        layer.type !== 'symbol' ||
        !layer.layout?.['text-field'] ||
        !map.getLayer(layer.id)
      ) {
        continue
      }
      map.setLayoutProperty(layer.id, 'text-field', layer.layout['text-field'])
    }
  }, [lang, ready])

  return (
    <div className={styles.wrapper}>
      <div
        ref={containerRef}
        className={styles.map}
        role="region"
        aria-label={t('map.label')}
      />
      <div className={styles.zoom}>
        <button
          type="button"
          aria-label={t('map.zoomIn')}
          onClick={() => mapRef.current?.zoomIn()}
        >
          <PlusIcon />
        </button>
        <button
          type="button"
          aria-label={t('map.zoomOut')}
          onClick={() => mapRef.current?.zoomOut()}
        >
          <MinusIcon />
        </button>
      </div>
    </div>
  )
}
