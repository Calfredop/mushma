import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LazyMotion, domAnimation } from 'motion/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { Snap } from '../sheet/snaps'
import { Sheet } from './Sheet'

// jsdom has no layout: a 390×844 phone, a 796px sheet, a 106px header, 34px of home indicator.
const HEIGHTS: Record<string, number> = { sheet: 796, head: 106, 'safe-bottom': 34 }
const offsetHeight = Object.getOwnPropertyDescriptor(
  HTMLElement.prototype,
  'offsetHeight',
)!

function reducedMotion(reduce: boolean) {
  window.matchMedia = vi.fn().mockImplementation((query: string) => ({
    matches: reduce && query.includes('prefers-reduced-motion'),
    media: query,
    addEventListener: () => {},
    removeEventListener: () => {},
  }))
}

beforeEach(() => {
  Object.defineProperty(HTMLElement.prototype, 'offsetHeight', {
    configurable: true,
    get(this: HTMLElement) {
      return HEIGHTS[this.dataset.part ?? ''] ?? 0
    },
  })
  vi.stubGlobal('innerHeight', 844)
  reducedMotion(true)
})

afterEach(() => {
  Object.defineProperty(HTMLElement.prototype, 'offsetHeight', offsetHeight)
  vi.unstubAllGlobals()
})

function setup(snap: Snap, props: Partial<Parameters<typeof Sheet>[0]> = {}) {
  const onSnap = vi.fn()
  const ui = (value: Snap) => (
    <LazyMotion features={domAnimation}>
      <Sheet
        mode="sheet"
        snap={value}
        onSnap={onSnap}
        label="Zone migliori"
        header={<p>Mappa Funghi</p>}
        {...props}
      >
        <button type="button">Stagioni</button>
      </Sheet>
    </LazyMotion>
  )
  const view = render(ui(snap))
  const sheet = () => screen.getByRole('complementary', { name: 'Zone migliori' })
  return { onSnap, sheet, rerender: (value: Snap) => view.rerender(ui(value)) }
}

describe('Sheet', () => {
  it('steps through the snaps from its handle button', async () => {
    const { onSnap, rerender } = setup('peek')
    const handle = screen.getByRole('button', { name: 'Espandi il pannello' })
    expect(handle).toHaveAttribute('aria-expanded', 'false')
    await userEvent.click(handle)
    expect(onSnap).toHaveBeenLastCalledWith('half')

    rerender('half')
    await userEvent.click(screen.getByRole('button', { name: 'Espandi il pannello' }))
    expect(onSnap).toHaveBeenLastCalledWith('full')

    rerender('full')
    const collapse = screen.getByRole('button', { name: 'Riduci il pannello' })
    expect(collapse).toHaveAttribute('aria-expanded', 'true')
    await userEvent.click(collapse)
    expect(onSnap).toHaveBeenLastCalledWith('peek')
  })

  it('moves a snap at a time with the arrow keys on its handle', async () => {
    const { onSnap } = setup('half')
    screen.getByRole('button', { name: 'Espandi il pannello' }).focus()
    await userEvent.keyboard('{ArrowUp}')
    expect(onSnap).toHaveBeenLastCalledWith('full')
    await userEvent.keyboard('{ArrowDown}')
    expect(onSnap).toHaveBeenLastCalledWith('peek')
  })

  it('sits at its snap, and under reduced motion jumps to a new one with no spring', () => {
    const { sheet, rerender } = setup('peek')
    // Peek: pushed down by all but its header and the home indicator.
    expect(sheet().style.transform).toBe('translateY(656px)')
    rerender('full')
    expect(sheet().style.transform).toBe('none')
    rerender('half')
    expect(sheet().style.transform).toBe('translateY(374px)')
  })

  it('reports its snap heights for the map padding', () => {
    const onGeometry = vi.fn()
    setup('peek', { onGeometry })
    expect(onGeometry).toHaveBeenCalledWith(
      expect.objectContaining({ height: 796, y: { full: 0, half: 374, peek: 656 } }),
    )
  })

  it('comes up to full when the keyboard moves focus into its body', () => {
    const { onSnap } = setup('peek')
    fireEvent.focusIn(screen.getByRole('button', { name: 'Stagioni' }))
    expect(onSnap).toHaveBeenLastCalledWith('full')
  })

  it('stays put when a tap focuses something in its body', () => {
    const { onSnap } = setup('half')
    const button = screen.getByRole('button', { name: 'Stagioni' })
    fireEvent.pointerDown(button)
    fireEvent.focusIn(button)
    expect(onSnap).not.toHaveBeenCalled()
  })

  it('is a plain panel on a desktop: no handle, no drag', () => {
    render(
      <Sheet
        mode="panel"
        snap="peek"
        onSnap={() => {}}
        label="Zone migliori"
        header={<p>Mappa Funghi</p>}
      >
        <p>Corpo</p>
      </Sheet>,
    )
    expect(screen.queryByRole('button', { name: 'Espandi il pannello' })).toBeNull()
    const panel = screen.getByRole('complementary', { name: 'Zone migliori' })
    expect(panel.style.transform).toBe('')
    expect(screen.getByText('Corpo')).toBeInTheDocument()
  })
})
