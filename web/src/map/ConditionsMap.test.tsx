import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { REGIONS } from '../regions'
import { ConditionsMap } from './ConditionsMap'

const noop = () => {}

/** Renders the map shell only: the MapLibre map itself waits a frame, and we unmount first. */
function renderMap(region: (typeof REGIONS)[string]) {
  return render(
    <ConditionsMap
      cells={undefined}
      selectedCellId={null}
      sightings={undefined}
      hotspots={undefined}
      camera={null}
      spotPoint={null}
      userPosition={null}
      lang="it"
      region={region}
      onCellClick={noop}
      onPointClick={noop}
      onHotspotClick={noop}
    />,
  )
}

describe('ConditionsMap', () => {
  it('names the map after its region, with the region’s own preposition', () => {
    const { unmount } = renderMap(REGIONS.marche)
    expect(
      screen.getByRole('region', {
        name: "Mappa dell'indice delle condizioni nelle Marche",
      }),
    ).toBeInTheDocument()
    unmount()
  })

  it('names another region’s map after it, not after Tuscany', () => {
    const { unmount } = renderMap(REGIONS.piemonte)
    expect(
      screen.getByRole('region', {
        name: "Mappa dell'indice delle condizioni in Piemonte",
      }),
    ).toBeInTheDocument()
    unmount()
  })
})
