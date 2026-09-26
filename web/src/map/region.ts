import type { GeoJSONSource, Map as MapLibreMap } from 'maplibre-gl'
import type { RegionDefinition } from '../regions'
import { regionMask } from './dataLayers'
import { type MapPadding, mergePadding } from './padding'

/** What the map takes from a region: its name, where it opens and how far it lets you go. */
export type MapRegion = Pick<
  RegionDefinition,
  'name' | 'locative' | 'bounds' | 'maxBounds' | 'minZoom' | 'maxZoom'
>

/** A region is framed with a margin, and clear of `padding` when there is one. */
export function regionPadding(padding: MapPadding | undefined): MapPadding {
  return mergePadding({ top: 24, bottom: 24, left: 24, right: 24 }, padding)
}

/**
 * Moves a live map to another region, as if it had opened there: the region framed, its own
 * pan and zoom limits, and the mask around it.
 */
export function showRegion(
  map: MapLibreMap,
  region: MapRegion,
  padding: MapPadding | undefined,
): void {
  map.getSource<GeoJSONSource>('region-mask')?.setData(regionMask(region.bounds))
  // The old region's pan limit would hold the camera back from the new one.
  map.setMaxBounds(null)
  map.setMinZoom(region.minZoom)
  map.setMaxZoom(region.maxZoom)
  map.fitBounds(region.bounds, { padding: regionPadding(padding), animate: false })
  map.setMaxBounds(region.maxBounds)
}
