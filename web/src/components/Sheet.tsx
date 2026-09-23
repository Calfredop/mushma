import {
  animate,
  type AnimationPlaybackControls,
  m,
  useMotionValue,
  useMotionValueEvent,
} from 'motion/react'
import {
  type PointerEvent,
  type ReactNode,
  type RefObject,
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from 'react'
import { useTranslation } from 'react-i18next'
import {
  coverFor,
  liftFor,
  rubberBand,
  type SheetGeometry,
  type Snap,
  sheetGeometry,
  snapAfterRelease,
  stepSnap,
} from '../sheet/snaps'
import { ChevronIcon } from './icons'
import styles from './Sheet.module.css'

export interface SheetLayout extends SheetGeometry {
  /** The top safe-area inset, for the map padding under the species pill. */
  safeTop: number
}

interface Props {
  /** A phone's draggable sheet over the map, or a desktop's side panel. */
  mode: 'sheet' | 'panel'
  snap: Snap
  onSnap: (snap: Snap) => void
  label: string
  /** The wordmark and the search: always in view, and what the sheet is dragged by. */
  header: ReactNode
  children: ReactNode
  /** The sheet's size at each snap, once measured and whenever it changes. */
  onGeometry?: (layout: SheetLayout) => void
  /** Gets `--sheet-lift` (px) and `--sheet-cover` (0–1) as the sheet moves, for what rides on
   * the map. */
  stage?: RefObject<HTMLElement | null>
  /** A desktop panel folded to its header (`panel-body` is what a toggle controls). */
  collapsed?: boolean
  className?: string
}

export function Sheet(props: Props) {
  return props.mode === 'panel' ? <Panel {...props} /> : <PhoneSheet {...props} />
}

function Panel({ label, header, children, collapsed = false, className }: Props) {
  return (
    <aside
      className={`${styles.panel} ${className ?? ''}`}
      aria-label={label}
      data-collapsed={collapsed || undefined}
    >
      <div className={styles.panelHead}>{header}</div>
      <div id="panel-body" className={styles.panelBody} hidden={collapsed}>
        {children}
      </div>
    </aside>
  )
}

/** Movement before a press becomes a drag, so taps still reach buttons and the search. */
const DRAG_THRESHOLD = 6
/** Velocity is read over the last stretch of the gesture. */
const VELOCITY_WINDOW_MS = 100
/** A tap's focus follows its pointerdown this closely; keyboard focus comes on its own. */
const POINTER_FOCUS_MS = 800
const SPRING = { type: 'spring', stiffness: 420, damping: 42 } as const

const reducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false

/** Tells what rides on the map where the sheet is. */
function publish(
  stage: HTMLElement | null | undefined,
  value: number,
  geometry: SheetGeometry | null,
) {
  if (!stage || !geometry) return
  stage.style.setProperty('--sheet-lift', `${liftFor(value, geometry)}px`)
  stage.style.setProperty('--sheet-cover', String(coverFor(value, geometry)))
}

interface Drag {
  startY: number
  /** The sheet's position when the finger went down. */
  startSheet: number
  active: boolean
  samples: { t: number; y: number }[]
}

function PhoneSheet({
  snap,
  onSnap,
  label,
  header,
  children,
  onGeometry,
  stage,
  className,
}: Props) {
  const { t } = useTranslation()
  const rootRef = useRef<HTMLElement>(null)
  const headRef = useRef<HTMLDivElement>(null)
  const bodyRef = useRef<HTMLDivElement>(null)
  const safeTopRef = useRef<HTMLDivElement>(null)
  const safeBottomRef = useRef<HTMLDivElement>(null)
  const [layout, setLayout] = useState<SheetLayout | null>(null)
  const y = useMotionValue(0)
  const animation = useRef<AnimationPlaybackControls | null>(null)
  // The snap the sheet last went to, and the speed a drag let go at (px/s).
  const shown = useRef<Snap | null>(null)
  const releaseVelocity = useRef(0)
  const drag = useRef<Drag | null>(null)
  const dragged = useRef(false)
  const pointerAt = useRef(0)
  // For the gesture handlers, which outlive a render.
  const latest = useRef({ snap, layout, onSnap })
  useLayoutEffect(() => {
    latest.current = { snap, layout, onSnap }
  })

  // Measure: its height is what shows at full; its header and the home indicator are its peek.
  useLayoutEffect(() => {
    const root = rootRef.current
    const head = headRef.current
    if (!root || !head) return
    const measure = () => {
      const next: SheetLayout = {
        ...sheetGeometry({
          height: root.offsetHeight,
          peek: head.offsetHeight + (safeBottomRef.current?.offsetHeight ?? 0),
          viewport: window.innerHeight,
        }),
        safeTop: safeTopRef.current?.offsetHeight ?? 0,
      }
      setLayout((previous) =>
        previous && JSON.stringify(previous) === JSON.stringify(next) ? previous : next,
      )
    }
    measure()
    const observer =
      typeof ResizeObserver === 'undefined' ? undefined : new ResizeObserver(measure)
    observer?.observe(root)
    observer?.observe(head)
    window.addEventListener('resize', measure)
    return () => {
      observer?.disconnect()
      window.removeEventListener('resize', measure)
    }
  }, [])

  useEffect(() => {
    if (layout) onGeometry?.(layout)
  }, [layout, onGeometry])

  useMotionValueEvent(y, 'change', (value) =>
    publish(stage?.current, value, latest.current.layout),
  )

  const springTo = useCallback(
    (target: number, velocity = 0) => {
      animation.current?.stop()
      animation.current = animate(y, target, { ...SPRING, velocity })
    },
    [y],
  )

  // To the snap: a new snap springs there, a new size (or the first) puts it there at once.
  useLayoutEffect(() => {
    if (!layout) return
    const target = layout.y[snap]
    if (shown.current === null || shown.current === snap || reducedMotion()) {
      animation.current?.stop()
      y.set(target)
      // Now, not on motion's next frame: the first paint must not show a full sheet.
      if (rootRef.current) {
        rootRef.current.style.transform = target ? `translateY(${target}px)` : 'none'
      }
      publish(stage?.current, target, layout)
    } else {
      springTo(target, releaseVelocity.current)
    }
    releaseVelocity.current = 0
    shown.current = snap
  }, [snap, layout, y, stage, springTo])

  useEffect(() => () => animation.current?.stop(), [])

  const begin = (clientY: number) => {
    drag.current = {
      startY: clientY,
      startSheet: y.get(),
      active: false,
      samples: [{ t: performance.now(), y: clientY }],
    }
  }

  /** Follows the finger once past the threshold; says whether the sheet is being dragged. */
  const move = (clientY: number): boolean => {
    const current = drag.current
    const geometry = latest.current.layout
    if (!current || !geometry) return false
    const dy = clientY - current.startY
    if (!current.active) {
      if (Math.abs(dy) < DRAG_THRESHOLD) return false
      // Caught mid-spring: carry on from where it is.
      animation.current?.stop()
      current.active = true
      current.startSheet = y.get() - dy
    }
    y.set(rubberBand(current.startSheet + dy, geometry.y.full, geometry.y.peek))
    const now = performance.now()
    current.samples.push({ t: now, y: clientY })
    while (
      current.samples.length > 2 &&
      now - current.samples[0].t > VELOCITY_WINDOW_MS
    ) {
      current.samples.shift()
    }
    return true
  }

  const end = () => {
    const current = drag.current
    drag.current = null
    const { layout: geometry, snap: from, onSnap: settle } = latest.current
    if (!current?.active || !geometry) return
    // The click a drag's release may fire is not a press of the handle.
    dragged.current = true
    setTimeout(() => {
      dragged.current = false
    })
    const first = current.samples[0]
    const last = current.samples[current.samples.length - 1]
    const velocity = last.t > first.t ? (last.y - first.y) / (last.t - first.t) : 0
    const target = snapAfterRelease(y.get(), velocity, geometry)
    const speed = reducedMotion() ? 0 : velocity * 1000
    if (target === from) {
      if (reducedMotion()) y.set(geometry.y[target])
      else springTo(geometry.y[target], speed)
    } else {
      releaseVelocity.current = speed
      settle(target)
    }
  }

  // The handle and header drag the sheet, whatever the input. The window follows the pointer
  // from there: a mouse soon leaves the header, and capturing it would take the click from a
  // button or the search that was only tapped.
  const onHeadPointerDown = (event: PointerEvent<HTMLDivElement>) => {
    if (event.button !== 0) return
    dragged.current = false
    begin(event.clientY)
    const onMove = (moved: globalThis.PointerEvent) => {
      if (moved.pointerId === event.pointerId) move(moved.clientY)
    }
    const onUp = (up: globalThis.PointerEvent) => {
      if (up.pointerId !== event.pointerId) return
      window.removeEventListener('pointermove', onMove)
      window.removeEventListener('pointerup', onUp)
      window.removeEventListener('pointercancel', onUp)
      end()
    }
    window.addEventListener('pointermove', onMove)
    window.addEventListener('pointerup', onUp)
    window.addEventListener('pointercancel', onUp)
  }

  // The body scrolls; a vertical touch drags the sheet instead unless the sheet is full, and
  // at full only a pull down from the very top does. Touch events, since only a non-passive
  // touchmove can stop the page from scrolling once the sheet has the gesture.
  useEffect(() => {
    const body = bodyRef.current
    if (!body) return
    let mode: 'undecided' | 'sheet' | 'native' = 'native'
    let x0 = 0
    let y0 = 0
    const onStart = (event: TouchEvent) => {
      if (event.touches.length !== 1) {
        mode = 'native'
        drag.current = null
        return
      }
      const touch = event.touches[0]
      x0 = touch.clientX
      y0 = touch.clientY
      mode = 'undecided'
      begin(touch.clientY)
    }
    const onMove = (event: TouchEvent) => {
      const touch = event.touches[0]
      if (mode === 'undecided') {
        const dx = touch.clientX - x0
        const dy = touch.clientY - y0
        if (Math.abs(dx) < 4 && Math.abs(dy) < 4) return
        const vertical = Math.abs(dy) > Math.abs(dx)
        const full = latest.current.snap === 'full'
        mode = vertical && (!full || (body.scrollTop <= 0 && dy > 0)) ? 'sheet' : 'native'
        if (mode === 'native') drag.current = null
      }
      if (mode !== 'sheet') return
      if (event.cancelable) event.preventDefault()
      move(touch.clientY)
    }
    const onEnd = () => {
      if (mode === 'sheet') end()
      else drag.current = null
      mode = 'native'
    }
    body.addEventListener('touchstart', onStart, { passive: true })
    body.addEventListener('touchmove', onMove, { passive: false })
    body.addEventListener('touchend', onEnd)
    body.addEventListener('touchcancel', onEnd)
    return () => {
      body.removeEventListener('touchstart', onStart)
      body.removeEventListener('touchmove', onMove)
      body.removeEventListener('touchend', onEnd)
      body.removeEventListener('touchcancel', onEnd)
    }
    // begin, move and end only touch refs.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <m.aside
      ref={rootRef}
      className={`${styles.sheet} ${className ?? ''}`}
      data-part="sheet"
      data-snap={snap}
      aria-label={label}
      // Bound only once measured: motion seeds a style value from the first render it sees,
      // and a first-render 0 would put the sheet at full when its features load.
      style={layout ? { y } : undefined}
    >
      <div
        ref={headRef}
        className={styles.head}
        data-part="head"
        onPointerDown={onHeadPointerDown}
      >
        <button
          type="button"
          className={styles.handle}
          aria-expanded={snap !== 'peek'}
          aria-label={t(snap === 'full' ? 'sheet.collapse' : 'sheet.expand')}
          onClick={() => {
            if (dragged.current) {
              dragged.current = false
              return
            }
            onSnap(stepSnap(snap, 'cycle'))
          }}
          onKeyDown={(event) => {
            if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return
            event.preventDefault()
            onSnap(stepSnap(snap, event.key === 'ArrowUp' ? 'up' : 'down'))
          }}
        >
          <span className={styles.grip} />
          <ChevronIcon direction={snap === 'full' ? 'down' : 'up'} />
        </button>
        <div className={styles.header}>{header}</div>
      </div>
      <div
        ref={bodyRef}
        className={styles.body}
        data-part="body"
        onPointerDown={() => {
          pointerAt.current = Date.now()
        }}
        onFocus={() => {
          // Keyboard focus below the fold: bring the whole sheet up so it can be seen.
          if (snap === 'full' || Date.now() - pointerAt.current < POINTER_FOCUS_MS) return
          onSnap('full')
        }}
      >
        {children}
      </div>
      <div ref={safeTopRef} className={styles.safeTop} data-part="safe-top" />
      <div ref={safeBottomRef} className={styles.safeBottom} data-part="safe-bottom" />
    </m.aside>
  )
}
