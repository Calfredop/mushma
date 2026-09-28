import { useCallback, useState } from 'react'
import { type CellStyle, isCellStyle } from '../map/dataLayers'

const STORAGE_KEY = 'mushma.cellStyle'

function read(fallback: CellStyle): CellStyle {
  try {
    const value = localStorage.getItem(STORAGE_KEY)
    return isCellStyle(value) ? value : fallback
  } catch {
    return fallback
  }
}

/** Soft cloud field vs discrete squircle cells; remembered across visits. */
export function useCellStyle(
  fallback: CellStyle = 'cloud',
): [CellStyle, (style: CellStyle) => void, () => void] {
  const [style, setStyle] = useState(() => read(fallback))
  const update = useCallback((value: CellStyle) => {
    setStyle(value)
    try {
      localStorage.setItem(STORAGE_KEY, value)
    } catch {
      // Not persisted; the choice still applies until the page closes.
    }
  }, [])
  const toggle = useCallback(() => {
    update(style === 'cloud' ? 'squircle' : 'cloud')
  }, [style, update])
  return [style, update, toggle]
}
