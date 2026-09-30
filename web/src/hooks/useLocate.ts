import { useCallback, useState } from 'react'
import { DEFAULT_REGION_SLUG } from '../config'
import { findRegionAt } from '../regions/lookup'

export type LocateError = 'denied' | 'unavailable' | 'outside'

interface Options {
  onLocated: (lat: number, lon: number) => void
  onError: (error: LocateError) => void
  /** The region the user is in (its slug); defaults to the default region. */
  region?: string
  /**
   * Called when the fix is outside `region` but inside another served region (the caller offers
   * a switch). Without it, such a fix is outside.
   */
  onOtherRegion?: (slug: string, lat: number, lon: number) => void
}

/** One-shot GPS fix. In `region` → onLocated; other served region → onOtherRegion; else outside. */
export function useLocate({
  onLocated,
  onError,
  region = DEFAULT_REGION_SLUG,
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
        const { latitude: lat, longitude: lon } = coords
        void findRegionAt(lat, lon, region).then((found) => {
          setLocating(false)
          if (found?.slug === region) onLocated(lat, lon)
          else if (found && onOtherRegion) onOtherRegion(found.slug, lat, lon)
          else onError('outside')
        })
      },
      (error) => {
        setLocating(false)
        onError(error.code === error.PERMISSION_DENIED ? 'denied' : 'unavailable')
      },
      { enableHighAccuracy: false, timeout: 15_000, maximumAge: 5 * 60_000 },
    )
  }, [onLocated, onError, region, onOtherRegion])

  return { locate, locating }
}
