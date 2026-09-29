import { fireEvent, render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { addDays } from '../time/days'
import { TrendLine } from './TrendLine'

const TODAY = '2026-09-29'

/** One score per day, oldest first, ending today. */
const series = (scores: number[]) =>
  scores.map((score, i) => ({ date: addDays(TODAY, i - (scores.length - 1)), score }))

const RISING = series(Array.from({ length: 15 }, (_, i) => 0.2 + 0.02 * i))
const FALLING = series(Array.from({ length: 15 }, (_, i) => 0.6 - 0.02 * i))
const FLAT = series(Array.from({ length: 15 }, (_, i) => 0.3 + (i % 2) * 0.01))

/** The line above the chart that reads one day's score. */
const readout = () => screen.getByText('·', { exact: false, selector: 'span' })

describe('TrendLine', () => {
  it('names what it follows, which way it went, and from and to what', () => {
    render(<TrendLine points={RISING} today={TODAY} subject="Porcini" />)
    expect(
      screen.getByRole('img', {
        name: 'Porcini, ultimi 15 giorni. In crescita: da 0,20 a 0,48',
      }),
    ).toBeInTheDocument()
  })

  it.each([
    [RISING, 'up'],
    [FALLING, 'down'],
    [FLAT, 'steady'],
  ])('points its arrow the way the line goes', (points, direction) => {
    const { container } = render(
      <TrendLine points={points} today={TODAY} subject="Toscana" />,
    )
    expect(container.querySelector('[data-direction]')).toHaveAttribute(
      'data-direction',
      direction,
    )
  })

  it('leaves out days before the window', () => {
    const older = [{ date: addDays(TODAY, -20), score: 0.9 }, ...RISING]
    render(<TrendLine points={older} today={TODAY} subject="Porcini" />)
    expect(screen.getByRole('img')).toHaveAccessibleName(/da 0,20 a 0,48/)
  })

  it('draws nothing without a day in the window', () => {
    const { container } = render(
      <TrendLine points={[]} today={TODAY} subject="Porcini" />,
    )
    expect(container).toBeEmptyDOMElement()
  })

  describe('large', () => {
    it("reads today's score and says the direction in words", () => {
      render(<TrendLine points={FALLING} today={TODAY} subject="Toscana" size="large" />)
      expect(screen.getByText('In calo')).toBeInTheDocument()
      expect(readout()).toHaveTextContent('Oggi · 0,32')
    })

    it('lists every day in a table for screen readers', () => {
      render(<TrendLine points={RISING} today={TODAY} subject="Toscana" size="large" />)
      const table = screen.getByRole('table')
      expect(within(table).getAllByRole('row')).toHaveLength(16) // a header and 15 days
    })

    it('reads the day under the pointer', () => {
      render(<TrendLine points={RISING} today={TODAY} subject="Toscana" size="large" />)
      const chart = screen.getByRole('img')
      chart.getBoundingClientRect = () => ({ left: 0, width: 320 }) as DOMRect
      fireEvent.pointerDown(chart, { clientX: 0 })
      // The first day of the window: Tuesday 15 September.
      expect(readout()).toHaveTextContent('mar 15 set · 0,20')
    })
  })
})
