import {
  addProtocol,
  Map as MapLibreMap,
  type MapMouseEvent,
  type GeoJSONSource,
} from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { Protocol } from 'pmtiles'
import { useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import type { RegionOverview } from '../api/queries'
import { BASEMAP_URL, TERRAIN_URL } from '../config'
import { currentLanguage, type Language } from '../i18n'
import { ITALY_BOUNDS, listRegions, REGIONS, type RegionDefinition } from '../regions'
import { scoreColor } from '../score/scale'
import { buildMapStyle } from '../map/basemap'
import styles from './HubPage.module.css'

let pmtilesRegistered = false
function registerPmtiles() {
  if (pmtilesRegistered) return
  addProtocol('pmtiles', new Protocol({ metadata: false }).tile)
  pmtilesRegistered = true
}

function regionPolygon(region: RegionDefinition): GeoJSON.Feature {
  const [[west, south], [east, north]] = region.bounds
  return {
    type: 'Feature',
    properties: { slug: region.slug, apiRegionId: region.apiRegionId },
    geometry: {
      type: 'Polygon',
      coordinates: [
        [
          [west, south],
          [east, south],
          [east, north],
          [west, north],
          [west, south],
        ],
      ],
    },
  }
}

function overviewCollection(
  overview: RegionOverview[] | undefined,
): GeoJSON.FeatureCollection {
  const byId = new Map((overview ?? []).map((row) => [row.region, row]))
  return {
    type: 'FeatureCollection',
    features: listRegions().map((region) => {
      const row = byId.get(region.apiRegionId)
      const feature = regionPolygon(region)
      feature.properties = {
        ...feature.properties,
        mean_score: row?.mean_score ?? 0,
        served: row !== undefined,
        color: row ? scoreColor(row.mean_score) : 'transparent',
      }
      return feature
    }),
  }
}

interface Props {
  overview: RegionOverview[] | undefined
  onSelectRegion: (slug: string) => void
}

export function HubMap({ overview, onSelectRegion }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<MapLibreMap | null>(null)
  const onSelectRef = useRef(onSelectRegion)
  const language = currentLanguage() as Language

  useEffect(() => {
    onSelectRef.current = onSelectRegion
  }, [onSelectRegion])

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return
    registerPmtiles()
    void TERRAIN_URL // reserved when the national terrain extract is pointed at
    const map = new MapLibreMap({
      container: containerRef.current,
      style: buildMapStyle({ lang: language, basemapUrl: BASEMAP_URL }),
      bounds: ITALY_BOUNDS,
      fitBoundsOptions: { padding: 24 },
      attributionControl: { compact: true },
    })
    mapRef.current = map

    map.on('load', () => {
      map.addSource('hub-regions', {
        type: 'geojson',
        data: overviewCollection(undefined),
      })
      map.addLayer({
        id: 'hub-regions-fill',
        type: 'fill',
        source: 'hub-regions',
        paint: {
          'fill-color': ['get', 'color'],
          'fill-opacity': 0.72,
        },
      })
      map.addLayer({
        id: 'hub-regions-outline',
        type: 'line',
        source: 'hub-regions',
        paint: {
          'line-color': '#1C211D',
          'line-width': 1.5,
          'line-opacity': 0.55,
        },
      })
    })

    const onClick = (event: MapMouseEvent) => {
      const hits = map.queryRenderedFeatures(event.point, {
        layers: ['hub-regions-fill'],
      })
      const slug = hits[0]?.properties?.slug
      if (typeof slug === 'string' && REGIONS[slug]) onSelectRef.current(slug)
    }
    map.on('click', onClick)
    map.on('mouseenter', 'hub-regions-fill', () => {
      map.getCanvas().style.cursor = 'pointer'
    })
    map.on('mouseleave', 'hub-regions-fill', () => {
      map.getCanvas().style.cursor = ''
    })

    return () => {
      map.remove()
      mapRef.current = null
    }
    // Mount once; language/basemap changes are rare on the hub.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const map = mapRef.current
    if (!map?.isStyleLoaded()) return
    const source = map.getSource('hub-regions') as GeoJSONSource | undefined
    source?.setData(overviewCollection(overview))
  }, [overview])

  return <div ref={containerRef} className={styles.map} role="presentation" />
}

interface HubPageProps {
  overview: RegionOverview[] | undefined
  onSelectRegion: (slug: string) => void
}

export function HubPage({ overview, onSelectRegion }: HubPageProps) {
  const { t, i18n } = useTranslation()
  const language = (i18n.resolvedLanguage ?? 'it') as Language

  return (
    <div className={styles.hub}>
      <header className={styles.header}>
        <h1 className={styles.wordmark}>{t('app.name')}</h1>
        <p className={styles.lede}>{t('hub.lede')}</p>
      </header>
      <HubMap overview={overview} onSelectRegion={onSelectRegion} />
      <section className={styles.list} aria-label={t('hub.regions')}>
        <h2 className={styles.listTitle}>{t('hub.regions')}</h2>
        <ul className={styles.regionList}>
          {listRegions().map((region) => (
            <li key={region.slug}>
              <button
                type="button"
                className={styles.regionCard}
                onClick={() => onSelectRegion(region.slug)}
              >
                <span className={styles.regionName}>{region.name[language]}</span>
                <span className={styles.regionIntro}>
                  {region.copy[language].intro.region}
                </span>
              </button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
