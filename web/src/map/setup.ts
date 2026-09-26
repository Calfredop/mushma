/** What every MapLibre map in the app sets up the same way: the basemap protocol and its UI copy. */
import type { TFunction } from 'i18next'
import { addProtocol } from 'maplibre-gl'
import { Protocol } from 'pmtiles'

let pmtilesRegistered = false
export function registerPmtiles() {
  if (pmtilesRegistered) return
  // No metadata request: the style already names the layers and the attribution.
  addProtocol('pmtiles', new Protocol({ metadata: false }).tile)
  pmtilesRegistered = true
}

/** MapLibre's own UI strings (canvas label, attribution button), from i18n. */
export function mapLocale(t: TFunction): Record<string, string> {
  return {
    'Map.Title': t('map.canvas'),
    'AttributionControl.ToggleAttribution': t('map.toggleAttribution'),
    'AttributionControl.MapFeedback': t('map.feedback'),
    'Marker.Title': t('map.marker'),
  }
}
