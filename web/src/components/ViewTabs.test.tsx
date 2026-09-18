import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useState } from 'react'
import { describe, expect, it } from 'vitest'
import type { View } from '../state/urlState'
import { ViewTabs } from './ViewTabs'

function Tabs() {
  const [view, setView] = useState<View>('now')
  return <ViewTabs value={view} onChange={setView} panelId="panel" />
}

describe('ViewTabs', () => {
  it('is one tab stop, and the arrow keys move between views like any tab list', async () => {
    render(<Tabs />)
    const tab = (name: string) => screen.getByRole('tab', { name })
    expect(tab('Oggi')).toHaveAttribute('tabindex', '0')
    expect(tab('Stagioni')).toHaveAttribute('tabindex', '-1')

    tab('Oggi').focus()
    await userEvent.keyboard('{ArrowRight}')
    expect(tab('Stagioni')).toHaveFocus()
    expect(tab('Stagioni')).toHaveAttribute('aria-selected', 'true')

    await userEvent.keyboard('{End}')
    expect(tab('Prospettive')).toHaveAttribute('aria-selected', 'true')
    await userEvent.keyboard('{ArrowRight}')
    expect(tab('Oggi')).toHaveFocus()
    await userEvent.keyboard('{ArrowLeft}')
    expect(tab('Prospettive')).toHaveFocus()
  })
})
