/** What covers the edges of the map (the chrome, the sheet, the panel), in px per side. */
export interface MapPadding {
  top: number
  bottom: number
  left: number
  right: number
}

/** Whether a point on screen is in the clear part of the map, a margin inside its edges. */
export function inView(
  point: { x: number; y: number },
  size: { width: number; height: number },
  padding: MapPadding | undefined,
  margin = 16,
): boolean {
  const { top = 0, bottom = 0, left = 0, right = 0 } = padding ?? {}
  return (
    point.x >= left + margin &&
    point.x <= size.width - right - margin &&
    point.y >= top + margin &&
    point.y <= size.height - bottom - margin
  )
}

/** The larger inset on each side. */
export function mergePadding(
  base: MapPadding,
  extra: MapPadding | undefined,
): MapPadding {
  if (!extra) return base
  return {
    top: Math.max(base.top, extra.top),
    bottom: Math.max(base.bottom, extra.bottom),
    left: Math.max(base.left, extra.left),
    right: Math.max(base.right, extra.right),
  }
}
