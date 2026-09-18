/**
 * The basemap style (PRD → Architecture → Basemap): self-hosted Protomaps
 * vector tiles with a cool, desaturated flavor so the warm score scale is the
 * only warm thing on screen, plus Mapterhorn hillshade.
 * See .gavin-root/docs/visual-direction.md.
 */
import { type Flavor, layers, namedFlavor } from '@protomaps/basemaps'
import type {
  LayerSpecification,
  SourceSpecification,
  StyleSpecification,
} from 'maplibre-gl'

// Protomaps basemaps-assets (fonts OFL, sprites MIT). M7 self-hosts these for offline use.
const ASSETS = 'https://protomaps.github.io/basemaps-assets'
export const GLYPHS_URL = `${ASSETS}/fonts/{fontstack}/{range}.pbf`
const SPRITE_URL = `${ASSETS}/sprites/v4/light`

/** Font stack for our own symbol layers (sighting counts). */
export const LABEL_FONT = ['Noto Sans Medium']

/** Score and sightings layers go under this basemap layer, so roads and labels stay on top. */
export const DATA_LAYERS_BEFORE = 'roads_tunnels_other_casing'

const LAND = '#E4E8E2'
const WOOD = '#D6DFD4'
const WATER = '#BCCFDB'
const INK = '#4A544D'
const HALO = '#EDF0EA'
const NEUTRAL = '#DDE2DB'

const light = namedFlavor('light')

const MUSHMA_FLAVOR: Flavor = {
  ...light,
  background: LAND,
  earth: LAND,
  park_a: WOOD,
  park_b: WOOD,
  wood_a: WOOD,
  wood_b: WOOD,
  scrub_a: '#DCE3D9',
  scrub_b: '#DCE3D9',
  hospital: NEUTRAL,
  industrial: NEUTRAL,
  school: NEUTRAL,
  pedestrian: NEUTRAL,
  zoo: NEUTRAL,
  military: NEUTRAL,
  aerodrome: NEUTRAL,
  beach: '#E6E7DD',
  sand: '#E6E7DD',
  glacier: '#F4F6F3',
  water: WATER,
  buildings: '#D2D8D0',
  boundaries: '#8F9A92',
  railway: '#A9B1AB',
  city_label: INK,
  city_label_halo: HALO,
  subplace_label: '#66706A',
  subplace_label_halo: HALO,
  state_label: '#7B857E',
  state_label_halo: HALO,
  country_label: '#7B857E',
  ocean_label: '#6F8A9A',
  roads_label_minor: '#66706A',
  roads_label_minor_halo: HALO,
  roads_label_major: '#5A645D',
  roads_label_major_halo: HALO,
  address_label: '#7B857E',
  address_label_halo: HALO,
  landcover: {
    barren: '#E3E5DD',
    farmland: '#E1E6DE',
    forest: WOOD,
    glacier: '#F4F6F3',
    grassland: '#DFE5DC',
    scrub: '#DCE3D9',
    urban_area: '#DADFD8',
  },
  pois: {
    blue: '#6B7F8C',
    green: '#6B7F70',
    lapis: '#6B7F8C',
    pink: '#7B857E',
    red: '#7B857E',
    slategray: '#7B857E',
    tangerine: '#7B857E',
    turquoise: '#6B7F8C',
  },
}

const PROTOMAPS_ATTRIBUTION =
  '<a href="https://protomaps.com">Protomaps</a> © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>'
const MAPTERHORN_ATTRIBUTION =
  '<a href="https://mapterhorn.com/attribution">© Mapterhorn</a>'

/** `.pmtiles` files are read with range requests via the pmtiles protocol; anything else is TileJSON. */
export function sourceUrl(url: string, origin: string): string {
  const absolute = new URL(url, origin).href
  return /\.pmtiles(\?|$)/.test(new URL(absolute).pathname)
    ? `pmtiles://${absolute}`
    : absolute
}

export function basemapLayers(lang: string): LayerSpecification[] {
  return layers('protomaps', MUSHMA_FLAVOR, { lang }) as LayerSpecification[]
}

const HILLSHADE: LayerSpecification = {
  id: 'hillshade',
  type: 'hillshade',
  source: 'terrain',
  paint: {
    // Quiet relief: readable terrain without competing with the score colours.
    'hillshade-exaggeration': 0.18,
    'hillshade-shadow-color': '#5B675E',
    'hillshade-highlight-color': '#FFFFFF',
    'hillshade-accent-color': '#8F9A92',
  },
}

export interface MapStyleOptions {
  basemapUrl?: string
  lang: string
  origin?: string
}

export function buildMapStyle({
  basemapUrl,
  lang,
  origin = globalThis.location?.href ?? 'http://localhost',
}: MapStyleOptions): StyleSpecification {
  if (!basemapUrl) {
    return {
      version: 8,
      glyphs: GLYPHS_URL,
      sources: {},
      layers: [
        { id: 'background', type: 'background', paint: { 'background-color': LAND } },
      ],
    }
  }
  return {
    version: 8,
    glyphs: GLYPHS_URL,
    sprite: SPRITE_URL,
    sources: {
      protomaps: {
        type: 'vector',
        url: sourceUrl(basemapUrl, origin),
        attribution: PROTOMAPS_ATTRIBUTION,
      },
    },
    layers: basemapLayers(lang),
  }
}

/**
 * Hillshade is added after the first complete render, so relief never delays
 * the first look at the scores. It goes under the roads and the score cells.
 */
export function hillshade(
  terrainUrl: string,
  origin = globalThis.location?.href ?? 'http://localhost',
): { source: SourceSpecification; layer: LayerSpecification } {
  return {
    source: {
      type: 'raster-dem',
      url: sourceUrl(terrainUrl, origin),
      encoding: 'terrarium',
      tileSize: 512,
      attribution: MAPTERHORN_ATTRIBUTION,
    },
    layer: HILLSHADE,
  }
}
