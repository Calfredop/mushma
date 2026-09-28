import { act, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { useCellStyle } from './useCellStyle'

afterEach(() => localStorage.clear())

describe('useCellStyle', () => {
  it('defaults to cloud and remembers a toggle', () => {
    const { result } = renderHook(() => useCellStyle())
    expect(result.current[0]).toBe('cloud')
    act(() => result.current[2]())
    expect(result.current[0]).toBe('squircle')
    expect(localStorage.getItem('mushma.cellStyle')).toBe('squircle')
  })

  it('restores a saved style', () => {
    localStorage.setItem('mushma.cellStyle', 'squircle')
    const { result } = renderHook(() => useCellStyle())
    expect(result.current[0]).toBe('squircle')
  })
})
