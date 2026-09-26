import { describe, expect, it } from 'vitest'
import type { LngLatBoundsLike, Map as MapLibreMap } from 'maplibre-gl'
import { REGIONS } from '../regions'
import { regionMask } from './dataLayers'
import { showRegion } from './region'

/** Just enough of a MapLibre map to see where it ends up, and under which limits. */
function fakeMap(opening: (typeof REGIONS)[string]) {
  const state = {
    maxBounds: opening.maxBounds as LngLatBoundsLike | null,
    minZoom: opening.minZoom,
    maxZoom: opening.maxZoom,
    mask: regionMask(opening.bounds) as unknown,
    fitted: null as null | {
      bounds: LngLatBoundsLike
      options: { padding?: unknown; animate?: boolean }
      /** The pan limit in force while the camera moved. */
      maxBounds: LngLatBoundsLike | null
    },
  }
  const map = {
    getSource: (id: string) =>
      id === 'region-mask'
        ? { setData: (data: unknown) => (state.mask = data) }
        : undefined,
    setMaxBounds: (bounds: LngLatBoundsLike | null) => (state.maxBounds = bounds),
    setMinZoom: (zoom: number) => (state.minZoom = zoom),
    setMaxZoom: (zoom: number) => (state.maxZoom = zoom),
    fitBounds: (bounds: LngLatBoundsLike, options: { animate?: boolean }) => {
      state.fitted = { bounds, options, maxBounds: state.maxBounds }
    },
  }
  return { map: map as unknown as MapLibreMap, state }
}

describe('showRegion', () => {
  const from = REGIONS.toscana
  const to = REGIONS.piemonte

  it('frames the new region, free of the old region’s pan limit', () => {
    const { map, state } = fakeMap(from)
    showRegion(map, to, undefined)
    expect(state.fitted?.bounds).toEqual(to.bounds)
    expect(state.fitted?.maxBounds).toBeNull()
  })

  it('leaves the new region’s own limits on', () => {
    const { map, state } = fakeMap(from)
    showRegion(map, to, undefined)
    expect(state.maxBounds).toEqual(to.maxBounds)
    expect(state.minZoom).toBe(to.minZoom)
    expect(state.maxZoom).toBe(to.maxZoom)
  })

  it('masks everything outside the new region', () => {
    const { map, state } = fakeMap(from)
    showRegion(map, to, undefined)
    expect(state.mask).toEqual(regionMask(to.bounds))
  })

  it('keeps the region clear of what covers the map', () => {
    const { map, state } = fakeMap(from)
    showRegion(map, to, { top: 10, bottom: 300, left: 0, right: 0 })
    expect(state.fitted?.options.padding).toEqual({
      top: 24,
      bottom: 300,
      left: 24,
      right: 24,
    })
  })
})
