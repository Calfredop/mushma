/**
 * Place search with Photon (komoot), OpenStreetMap data. Its public instance
 * allows search-as-you-type within fair use, unlike Nominatim; callers
 * debounce and cache. Credited in the app.
 */
import type { Language } from '../i18n'

const PHOTON = 'https://photon.komoot.io/api/'
const LIMIT = 6

export interface Place {
  id: string
  name: string
  /** Comune and province, when they differ from the name. */
  detail: string
  lat: number
  lon: number
}

interface PhotonFeature {
  geometry: { type: string; coordinates: number[] }
  properties: {
    osm_type?: string
    osm_id?: number
    name?: string
    city?: string
    county?: string
  }
}

export function photonUrl(
  query: string,
  language: Language,
  [[west, south], [east, north]]: [[number, number], [number, number]],
): string {
  const params = new URLSearchParams({
    q: query,
    limit: String(LIMIT),
    bbox: [west, south, east, north].join(','),
  })
  // Photon supports default/en/de/fr; "default" gives local (Italian) names.
  if (language === 'en') params.set('lang', 'en')
  return `${PHOTON}?${params}`
}

export function parsePhoton(body: { features: PhotonFeature[] }): Place[] {
  const seen = new Set<string>()
  const places: Place[] = []
  for (const { geometry, properties } of body.features) {
    if (!properties.name || geometry.type !== 'Point') continue
    const id = `${properties.osm_type ?? ''}${properties.osm_id ?? ''}`
    if (seen.has(id)) continue
    seen.add(id)
    const detail = [properties.city, properties.county]
      .filter(
        (part, index, parts) =>
          part && part !== properties.name && parts.indexOf(part) === index,
      )
      .join(', ')
    const [lon, lat] = geometry.coordinates
    places.push({ id, name: properties.name, detail, lat, lon })
  }
  return places
}

export async function searchPlaces(
  query: string,
  language: Language,
  bounds: [[number, number], [number, number]],
  signal?: AbortSignal,
): Promise<Place[]> {
  const response = await fetch(photonUrl(query, language, bounds), { signal })
  if (!response.ok) throw new Error(`Photon answered ${response.status}`)
  return parsePhoton(await response.json())
}
