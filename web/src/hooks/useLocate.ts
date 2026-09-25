import { useCallback, useState } from 'react'
import { DEFAULT_REGION_SLUG, REGIONS } from '../config'
import { inBounds } from '../geo/distance'

export type LocateError = 'denied' | 'unavailable' | 'outside'

interface Options {
  onLocated: (lat: number, lon: number) => void
  onError: (error: LocateError) => void
  /**
   * When set, a fix outside this box still succeeds if it lands in another served region
   * (the caller offers a switch). Defaults to the default region's bounds with no cross-region.
   */
  bounds?: [[number, number], [number, number]]
  /** Called when the fix is outside `bounds` but inside another served region. */
  onOtherRegion?: (slug: string, lat: number, lon: number) => void
}

/** One-shot GPS fix. Inside `bounds` → onLocated; other served region → onOtherRegion; else outside. */
export function useLocate({
  onLocated,
  onError,
  bounds = REGIONS[DEFAULT_REGION_SLUG].bounds,
  onOtherRegion,
}: Options) {
  const [locating, setLocating] = useState(false)

  const locate = useCallback(() => {
    if (!('geolocation' in navigator)) {
      onError('unavailable')
      return
    }
    setLocating(true)
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        setLocating(false)
        const { latitude: lat, longitude: lon } = coords
        if (inBounds(lat, lon, bounds)) {
          onLocated(lat, lon)
          return
        }
        if (onOtherRegion) {
          const other = Object.values(REGIONS).find(
            (region) => !inBounds(lat, lon, bounds) && inBounds(lat, lon, region.bounds),
          )
          if (other) {
            onOtherRegion(other.slug, lat, lon)
            return
          }
        }
        onError('outside')
      },
      (error) => {
        setLocating(false)
        onError(error.code === error.PERMISSION_DENIED ? 'denied' : 'unavailable')
      },
      { enableHighAccuracy: false, timeout: 15_000, maximumAge: 5 * 60_000 },
    )
  }, [onLocated, onError, bounds, onOtherRegion])

  return { locate, locating }
}
