import { describe, expect, it } from 'vitest'
import {
  GOOD_DAYS_CLASSES,
  goodDaysClass,
  goodDaysStepExpression,
  SCORE_CLASSES,
  scoreClass,
  scoreColor,
  scoreInk,
  scoreStepExpression,
} from './scale'

describe('score scale', () => {
  it('has five classes from pale straw to porcino brown', () => {
    expect(SCORE_CLASSES.map((c) => c.color)).toEqual([
      '#F7F0C6',
      '#F0C967',
      '#E68C2C',
      '#B34F2A',
      '#652D1F',
    ])
  })

  it.each([
    [0, 0],
    [0.19, 0],
    [0.2, 1],
    [0.39, 1],
    [0.4, 2],
    [0.6, 3],
    [0.79, 3],
    [0.8, 4],
    [1, 4],
  ])('puts score %s in class index %s', (score, index) => {
    expect(scoreClass(score)).toBe(index)
  })

  it('clamps scores outside 0–1 instead of throwing', () => {
    expect(scoreClass(-0.1)).toBe(0)
    expect(scoreClass(1.3)).toBe(4)
    expect(scoreClass(Number.NaN)).toBe(0)
  })

  it('maps a score to its class colour', () => {
    expect(scoreColor(0.05)).toBe('#F7F0C6')
    expect(scoreColor(0.85)).toBe('#652D1F')
  })

  it('uses dark ink on light classes and white ink on dark classes', () => {
    expect(scoreInk(0.1)).toBe('#1C211D')
    expect(scoreInk(0.5)).toBe('#1C211D')
    expect(scoreInk(0.65)).toBe('#FFFFFF')
    expect(scoreInk(0.95)).toBe('#FFFFFF')
  })

  it('builds a MapLibre step expression with the same class breaks', () => {
    expect(scoreStepExpression(['get', 'score'])).toEqual([
      'step',
      ['get', 'score'],
      '#F7F0C6',
      0.2,
      '#F0C967',
      0.4,
      '#E68C2C',
      0.6,
      '#B34F2A',
      0.8,
      '#652D1F',
    ])
  })
})

describe('good-days scale (a season on the map)', () => {
  it('uses the same five colours with day breaks', () => {
    expect(GOOD_DAYS_CLASSES.map((c) => c.color)).toEqual(
      SCORE_CLASSES.map((c) => c.color),
    )
    expect(GOOD_DAYS_CLASSES.map((c) => c.min)).toEqual([0, 10, 30, 60, 90])
  })

  it.each([
    [0, 0],
    [9, 0],
    [10, 1],
    [59, 2],
    [60, 3],
    [120, 4],
  ])('%d good days is class %d', (days, expected) => {
    expect(goodDaysClass(days)).toBe(expected)
  })

  it('builds a MapLibre step expression with the same breaks', () => {
    expect(goodDaysStepExpression(['get', 'score'])).toEqual([
      'step',
      ['get', 'score'],
      '#F7F0C6',
      10,
      '#F0C967',
      30,
      '#E68C2C',
      60,
      '#B34F2A',
      90,
      '#652D1F',
    ])
  })
})
