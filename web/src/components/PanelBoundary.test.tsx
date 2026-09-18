import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { PanelBoundary } from './PanelBoundary'

function Broken(): never {
  throw new Error('bad response')
}

describe('PanelBoundary', () => {
  it('keeps a failing panel from blanking the app, and says what to do', () => {
    const quiet = vi.spyOn(console, 'error').mockImplementation(() => {})
    render(
      <PanelBoundary resetKey="a">
        <Broken />
      </PanelBoundary>,
    )
    expect(screen.getByRole('alert')).toHaveTextContent(/Ricarica la pagina/)
    quiet.mockRestore()
  })

  it('renders its panel when nothing fails', () => {
    render(
      <PanelBoundary resetKey="a">
        <p>ok</p>
      </PanelBoundary>,
    )
    expect(screen.getByText('ok')).toBeInTheDocument()
  })
})
