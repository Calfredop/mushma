import { type GeoJSONSource, Map as MapLibreMap, type MapMouseEvent } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useEffect, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { BASEMAP_URL } from '../config'
import type { Language } from '../i18n'
import type { HubRegion } from '../pages/hubRegions'
import { ITALY_BOUNDS, REGIONS } from '../regions'
import { loadRegionBoundaries, type RegionBoundaries } from '../regions/boundaries'
import { basemapLayers, buildMapStyle, DATA_LAYERS_BEFORE } from './basemap'
import styles from './HubMap.module.css'
import {
  HUB_FILL_LAYER,
  HUB_LABELS_SOURCE,
  HUB_REGIONS_SOURCE,
  applyHubPaint,
  hubLayers,
  regionLabelPoints,
} from './hubLayers'
import { type MapPadding, mergePadding } from './padding'
import { mapLocale, registerPmtiles } from './setup'

const EDGE = { top: 16, right: 16, bottom: 16, left: 16 }

const prefersReducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false

interface Props {
  regions: HubRegion[]
  /** The region whose outline is drawn hovered: under the pointer here or in the list. */
  highlighted: string | null
  /** What covers the map's edges (the panel, the sheet): Italy is framed in what's left. */
  padding: MapPadding | undefined
  lang: Language
  onHover: (slug: string | null) => void
  onSelect: (slug: string) => void
  /** A tap on a region the app doesn't serve (its slug), or off every region (null). */
  onUnserved: (slug: string | null) => void
}

/** The national map on the hub: every region's real boundary, the served ones to tap. */
export function HubMap({
  regions,
  highlighted,
  padding,
  lang,
  onHover,
  onSelect,
  onUnserved,
}: Props) {
  const { t } = useTranslation()
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<MapLibreMap | null>(null)
  const [ready, setReady] = useState(false)
  const [boundaries, setBoundaries] = useState<RegionBoundaries | null>(null)
  const [drawn, setDrawn] = useState(false)
  const callbacks = useRef({ onHover, onSelect, onUnserved })
  const initial = useRef({ lang, locale: mapLocale(t), padding, regions })
  const paddingRef = useRef(padding)
  // Once someone pans or zooms, the map stays where they put it.
  const moved = useRef(false)

  useEffect(() => {
    callbacks.current = { onHover, onSelect, onUnserved }
  })

  useEffect(() => {
    let live = true
    void loadRegionBoundaries().then((data) => {
      if (live) setBoundaries(data)
    })
    return () => {
      live = false
    }
  }, [])

  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    registerPmtiles()
    const map = new MapLibreMap({
      container,
      style: buildMapStyle({ lang: initial.current.lang, basemapUrl: BASEMAP_URL }),
      bounds: ITALY_BOUNDS,
      fitBoundsOptions: { padding: mergePadding(EDGE, initial.current.padding) },
      minZoom: 3,
      maxZoom: 9,
      dragRotate: false,
      pitchWithRotate: false,
      touchPitch: false,
      attributionControl: { compact: true },
      locale: initial.current.locale,
    })
    map.touchZoomRotate.disableRotation()
    map.keyboard.disableRotation()
    mapRef.current = map
    if (import.meta.env.DEV) window.__mushmaMap = map
    map.once('style.load', () => setReady(true))
    map.on('movestart', (event) => {
      if ('originalEvent' in event && event.originalEvent) moved.current = true
    })

    const regionAt = (event: MapMouseEvent) => {
      const feature = map.queryRenderedFeatures(event.point, {
        layers: [HUB_FILL_LAYER],
      })[0]
      const slug = feature?.properties?.slug
      return typeof slug === 'string' ? slug : null
    }
    map.on('mousemove', (event) => {
      if (!map.getLayer(HUB_FILL_LAYER)) return
      const slug = regionAt(event)
      const served = slug !== null && REGIONS[slug] !== undefined
      map.getCanvas().style.cursor = served ? 'pointer' : ''
      callbacks.current.onHover(served ? slug : null)
    })
    map.on('mouseout', () => callbacks.current.onHover(null))
    map.on('click', (event) => {
      if (!map.getLayer(HUB_FILL_LAYER)) return
      const slug = regionAt(event)
      if (slug !== null && REGIONS[slug]) callbacks.current.onSelect(slug)
      else callbacks.current.onUnserved(slug)
    })

    return () => {
      map.remove()
      mapRef.current = null
      if (window.__mushmaMap === map) delete window.__mushmaMap
      setReady(false)
      setDrawn(false)
    }
  }, [])

  // The regions go on once both the style and the boundaries are in, whichever comes last.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !ready || !boundaries || map.getSource(HUB_REGIONS_SOURCE)) return
    const { regions: first, lang: firstLang } = initial.current
    map.addSource(HUB_REGIONS_SOURCE, {
      type: 'geojson',
      data: boundaries,
      promoteId: 'slug',
    })
    map.addSource(HUB_LABELS_SOURCE, {
      type: 'geojson',
      data: regionLabelPoints(boundaries, first, firstLang),
    })
    const layers = hubLayers(first)
    const beneath = map.getLayer(DATA_LAYERS_BEFORE) ? DATA_LAYERS_BEFORE : undefined
    const firstLabel = map.getStyle().layers.find((layer) => layer.type === 'symbol')?.id
    for (const layer of layers.beneath) map.addLayer(layer, beneath)
    for (const layer of layers.above) map.addLayer(layer, firstLabel)
    for (const layer of layers.top) map.addLayer(layer)
    setDrawn(true)
  }, [ready, boundaries])

  // Scores and names: repainted as the overview and the language change.
  useEffect(() => {
    const map = mapRef.current
    if (!map || !drawn || !boundaries) return
    applyHubPaint(map, regions)
    map
      .getSource<GeoJSONSource>(HUB_LABELS_SOURCE)
      ?.setData(regionLabelPoints(boundaries, regions, lang))
  }, [drawn, boundaries, regions, lang])

  useEffect(() => {
    const map = mapRef.current
    if (!map || !drawn || !highlighted) return
    const feature = { source: HUB_REGIONS_SOURCE, id: highlighted }
    map.setFeatureState(feature, { hover: true })
    return () => {
      if (map.getSource(HUB_REGIONS_SOURCE))
        map.setFeatureState(feature, { hover: false })
    }
  }, [drawn, highlighted])

  // Italy stays framed in the part of the map the panel or the sheet leaves clear.
  useEffect(() => {
    const map = mapRef.current
    const previous = paddingRef.current
    paddingRef.current = padding
    if (!map || moved.current || JSON.stringify(previous) === JSON.stringify(padding)) {
      return
    }
    map.fitBounds(ITALY_BOUNDS, {
      padding: mergePadding(EDGE, padding),
      duration: prefersReducedMotion() ? 0 : 300,
    })
  }, [padding])

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
    <div
      ref={containerRef}
      className={styles.map}
      role="region"
      aria-label={t('hub.mapLabel')}
    />
  )
}
