import { describe, expect, it } from 'vitest'
import {
  coverFor,
  liftFor,
  rubberBand,
  sheetGeometry,
  snapAfterRelease,
  stepSnap,
  visibleAt,
} from './snaps'

// A 390×844 phone: the sheet is 796px tall at full (a 48px sliver of map above it), its peek is
// the 106px header and 34px of home indicator.
const phone = sheetGeometry({ height: 796, peek: 140, viewport: 844 })

describe('sheetGeometry', () => {
  it('pushes the sheet down to each snap: full shows all of it, peek only its header', () => {
    expect(phone.y.full).toBe(0)
    expect(visibleAt('full', phone)).toBe(796)
    expect(visibleAt('peek', phone)).toBe(140)
    expect(phone.y.peek).toBe(656)
  })

  it('opens half about half the screen', () => {
    expect(visibleAt('half', phone)).toBe(422)
  })

  it('keeps half clear of peek and full on a short screen', () => {
    // A phone on its side: 360px tall.
    const flat = sheetGeometry({ height: 320, peek: 140, viewport: 360 })
    expect(visibleAt('half', flat)).toBeGreaterThanOrEqual(140 + 48)
    expect(visibleAt('half', flat)).toBeLessThanOrEqual(320 - 48)
    expect(flat.y.peek).toBeGreaterThan(flat.y.half)
    expect(flat.y.half).toBeGreaterThan(flat.y.full)
  })

  it('never pushes the sheet below its own peek', () => {
    const tiny = sheetGeometry({ height: 100, peek: 140, viewport: 150 })
    expect(tiny.y.peek).toBe(0)
    expect(tiny.y.half).toBe(0)
  })
})

describe('snapAfterRelease', () => {
  const halfY = phone.y.half // 374

  it('settles on the nearest snap when let go slowly', () => {
    expect(snapAfterRelease(halfY + 30, 0, phone)).toBe('half')
    expect(snapAfterRelease(20, 0.05, phone)).toBe('full')
    expect(snapAfterRelease(phone.y.peek - 10, 0, phone)).toBe('peek')
  })

  it('follows a flick past the nearest snap', () => {
    // Just above half, flicked up hard: full, not back to half.
    expect(snapAfterRelease(halfY - 40, -1.5, phone)).toBe('full')
    // Just below full, flicked down: half.
    expect(snapAfterRelease(30, 1.2, phone)).toBe('half')
    // Near half, flicked down hard: peek.
    expect(snapAfterRelease(halfY + 20, 2, phone)).toBe('peek')
  })

  it('lands on the end snap when dragged past it', () => {
    expect(snapAfterRelease(-60, 0, phone)).toBe('full')
    expect(snapAfterRelease(phone.y.peek + 60, 0, phone)).toBe('peek')
  })
})

describe('rubberBand', () => {
  it('follows the finger between the ends', () => {
    expect(rubberBand(200, 0, 656)).toBe(200)
  })

  it('resists past either end', () => {
    expect(rubberBand(-100, 0, 656)).toBeGreaterThan(-100)
    expect(rubberBand(-100, 0, 656)).toBeLessThan(0)
    expect(rubberBand(756, 0, 656)).toBeLessThan(756)
    expect(rubberBand(756, 0, 656)).toBeGreaterThan(656)
  })
})

describe('stepSnap', () => {
  it('cycles peek → half → full → peek, for the handle button', () => {
    expect(stepSnap('peek', 'cycle')).toBe('half')
    expect(stepSnap('half', 'cycle')).toBe('full')
    expect(stepSnap('full', 'cycle')).toBe('peek')
  })

  it('steps up and down, stopping at the ends, for the arrow keys', () => {
    expect(stepSnap('peek', 'up')).toBe('half')
    expect(stepSnap('full', 'up')).toBe('full')
    expect(stepSnap('full', 'down')).toBe('half')
    expect(stepSnap('peek', 'down')).toBe('peek')
  })
})

describe('what rides on the map', () => {
  it('lifts the bottom controls with the sheet, up to half', () => {
    expect(liftFor(phone.y.peek, phone)).toBe(140)
    expect(liftFor(phone.y.half, phone)).toBe(422)
    // Past half the sheet covers them instead of pushing them off the top.
    expect(liftFor(phone.y.full, phone)).toBe(422)
  })

  it('covers the top of the map between half and full', () => {
    expect(coverFor(phone.y.peek, phone)).toBe(0)
    expect(coverFor(phone.y.half, phone)).toBe(0)
    expect(coverFor(phone.y.half / 2, phone)).toBeCloseTo(0.5)
    expect(coverFor(phone.y.full, phone)).toBe(1)
    expect(coverFor(-40, phone)).toBe(1)
  })
})
