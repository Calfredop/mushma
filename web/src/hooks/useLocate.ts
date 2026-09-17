import { useCallback, useState } from 'react'
import { REGION } from '../config'
import { inBounds } from '../geo/distance'

export type LocateError = 'denied' | 'unavailable' | 'outside'

interface Options {
  onLocated: (lat: number, lon: number) => void
  onError: (error: LocateError) => void
}

/** One-shot GPS fix, restricted to the region. */
export function useLocate({ onLocated, onError }: Options) {
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
        if (inBounds(coords.latitude, coords.longitude, REGION.bounds)) {
          onLocated(coords.latitude, coords.longitude)
        } else {
          onError('outside')
        }
      },
      (error) => {
        setLocating(false)
        onError(error.code === error.PERMISSION_DENIED ? 'denied' : 'unavailable')
      },
      { enableHighAccuracy: false, timeout: 15_000, maximumAge: 5 * 60_000 },
    )
  }, [onLocated, onError])

  return { locate, locating }
}
