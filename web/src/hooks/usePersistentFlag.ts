import { useCallback, useState } from 'react'

function read(key: string): boolean {
  try {
    return localStorage.getItem(key) === '1'
  } catch {
    return false
  }
}

/** A boolean the browser remembers. Storage can be blocked, so the choice always applies to this visit. */
export function usePersistentFlag(key: string): [boolean, (value: boolean) => void] {
  const [flag, setFlag] = useState(() => read(key))
  const update = useCallback(
    (value: boolean) => {
      setFlag(value)
      try {
        localStorage.setItem(key, value ? '1' : '0')
      } catch {
        // Not persisted; the choice still applies until the page closes.
      }
    },
    [key],
  )
  return [flag, update]
}
