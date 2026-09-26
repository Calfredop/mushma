import { expect, type Page, test } from '@playwright/test'
import type { Map as MapLibreMap } from 'maplibre-gl'

declare global {
  interface Window {
    __mushmaMap?: MapLibreMap
  }
}

/** Screen position of the best-scoring cell, read from the live map. */
async function bestCellOnScreen(page: Page) {
  await page.waitForFunction(() => {
    const map = window.__mushmaMap
    return (
      !!map?.getSource('cells-points') &&
      map.querySourceFeatures('cells-points').length > 0
    )
  })
  return page.evaluate(() => {
    const map = window.__mushmaMap!
    const features = map.querySourceFeatures('cells-points')
    const best = features.reduce((a, b) =>
      Number(b.properties.score) > Number(a.properties.score) ? b : a,
    )
    const [lon, lat] = (best.geometry as { coordinates: [number, number] }).coordinates
    const point = map.project([lon, lat])
    const box = map.getCanvas().getBoundingClientRect()
    return {
      x: box.left + point.x,
      y: box.top + point.y,
      id: String(best.properties.cell_id),
    }
  })
}

test('map → spot forecast → why this score', async ({ page }) => {
  await page.goto('/toscana')

  // First visit: the disclaimer.
  const disclaimer = page.getByRole('dialog', { name: 'Prima di usare la mappa' })
  await expect(disclaimer).toBeVisible()
  await disclaimer.getByRole('button', { name: 'Ho capito' }).click()
  await expect(disclaimer).toBeHidden()

  // Combined view on the region path; switch to porcini.
  await expect(page).toHaveURL(/\/toscana$/)
  await expect(page.getByRole('radio', { name: 'Tutte' })).toBeChecked()
  await page.getByRole('radio', { name: 'Porcini' }).click()
  await expect(page).toHaveURL(/\/toscana\/porcini$/)

  // The map: species switcher, hatched forecast days, hot places.
  await expect(page.getByRole('radio', { name: /previsione$/ }).first()).toHaveAttribute(
    'data-kind',
    'forecast',
  )
  await expect(page.getByRole('heading', { name: 'Zone migliori' })).toBeVisible()

  // Tap the best cell.
  const cell = await bestCellOnScreen(page)
  await page.mouse.click(cell.x, cell.y)
  await expect(page).toHaveURL(new RegExp(`cell=${cell.id}`))

  // Spot forecast: every species with an 8-day outlook.
  await expect(page.getByText('Previsione del punto')).toBeVisible()
  await expect(page.getByRole('button', { name: /^Porcini, / })).toHaveCount(8)
  await expect(page.getByRole('button', { name: /^Gallinacci, / })).toHaveCount(8)

  // Why this score: the factor list, then a forecast day.
  // The spot opens at half; the why list is further down, so the sheet comes up full.
  await page.getByRole('button', { name: 'Espandi il pannello' }).click()
  await expect(page.getByRole('complementary')).toHaveAttribute('data-snap', 'full')
  const why = page.getByRole('region', { name: 'Perché questo indice' })
  await expect(why).toBeVisible()
  // The factors holding nothing back fold into one row when any sit at 1.00.
  const folded = why.getByRole('button', {
    name: /^(Altri \d+ fattori già ideali|Un altro fattore già ideale) \(1,00\)$/,
  })
  if (await folded.count()) await folded.click()
  await expect(why.getByRole('meter', { name: 'Stagione' })).toBeVisible()
  await expect(why.getByRole('listitem')).not.toHaveCount(0)

  const forecastBar = page.getByRole('button', { name: /^Porcini, / }).nth(3)
  await forecastBar.click()
  await expect(forecastBar).toHaveAttribute('aria-pressed', 'true')
  await expect(why.getByText(/Questo giorno deve ancora arrivare/)).toBeVisible()
})

test('seasons on the map, a replayed day, and the outlook', async ({ page }) => {
  await page.goto('/toscana')
  await page.getByRole('button', { name: 'Ho capito' }).click()
  // The cookie banner covers the sheet's buttons on a phone.
  await page.getByRole('button', { name: 'Rifiuta' }).click()

  // The outlook needs a single species: the combined default has none.
  await page.getByRole('radio', { name: 'Porcini' }).click()
  await expect(page).toHaveURL(/\/toscana\/porcini$/)

  // Past seasons: pick one and it goes on the map as good days per cell. The view tabs are
  // under the sheet's peek (wordmark and search): open it first.
  await page.getByRole('button', { name: 'Espandi il pannello' }).click()
  await page.getByRole('tab', { name: 'Stagioni' }).click()
  await expect(page.getByRole('heading', { name: 'Stagioni', level: 2 })).toBeVisible()
  const lastYear = String(new Date().getFullYear() - 1)
  await page.getByRole('button', { name: new RegExp(`^${lastYear}:`) }).click()
  await expect(page).toHaveURL(new RegExp(`season=${lastYear}`))
  await expect(page.getByRole('main').getByText(`Stagione ${lastYear}`)).toBeVisible()
  await expect(
    page.getByRole('main').getByText(`Giorni favorevoli nel ${lastYear}`),
  ).toBeAttached()

  // Replay its best day: the date bar turns into a past day.
  await page.getByRole('button', { name: 'Rivedilo sulla mappa' }).click()
  await expect(page.getByText('Giorno passato')).toBeVisible()
  await expect(page).toHaveURL(/date=\d{4}-\d{2}-\d{2}/)
  await page.getByRole('button', { name: 'Oggi', exact: true }).click()
  await expect(page.getByRole('radiogroup', { name: 'Giorno' })).toBeVisible()

  // The outlook: an outlook, never a forecast.
  await page.getByRole('tab', { name: 'Prospettive' }).click()
  await expect(
    page.getByText("Un'indicazione di massima, non una previsione"),
  ).toBeVisible()
  await expect(page.getByText('La stagione finora')).toBeVisible()
})

test('analysis mode: two factors on the map, played through the days', async ({
  page,
}) => {
  await page.goto('/toscana')
  await page.getByRole('button', { name: 'Ho capito' }).click()
  // The cookie banner covers the play button on a phone.
  await page.getByRole('button', { name: 'Rifiuta' }).click()

  // The ◈ button in the map's cluster: rain_trigger comes on, and Tutte can't be picked, so
  // the path moves from the region ("Tutti") to porcini.
  await page.getByRole('button', { name: 'Analisi' }).click()
  await expect(page).toHaveURL(/\/toscana\/porcini\?mode=analysis&f=rain_trigger$/)
  await expect(page.getByRole('radio', { name: 'Tutte' })).toBeDisabled()

  // A second chip: both are drawn, each as its own layer.
  const panel = page.getByRole('region', { name: "Fattori dell'indice" })
  await panel.getByRole('button', { name: 'Vento e aria secca' }).click()
  await expect(panel.getByRole('button', { name: 'Vento e aria secca' })).toHaveAttribute(
    'aria-pressed',
    'true',
  )
  await expect(page).toHaveURL(/f=rain_trigger%2Cdrying/)
  await page.waitForFunction(() => {
    const map = window.__mushmaMap
    return (
      !!map?.getLayer('indicator-fill-rain_trigger') &&
      !!map.getLayer('indicator-fill-drying') &&
      map.getLayoutProperty('cells-dot', 'visibility') === 'none' &&
      map.querySourceFeatures('cells-points').some((f) => 'drying' in f.properties)
    )
  })

  // Play: the date moves on by itself, then pauses.
  const selected = page
    .getByRole('radiogroup', { name: 'Giorno' })
    .getByRole('radio', { checked: true })
  const today = await selected.getAttribute('aria-label')
  await page.getByRole('button', { name: 'Riproduci i giorni' }).click()
  await expect(selected).not.toHaveAttribute('aria-label', today!)
  await expect(page).toHaveURL(/date=\d{4}-\d{2}-\d{2}/)
  await page.getByRole('button', { name: 'Metti in pausa' }).click()
  await expect(page.getByRole('button', { name: 'Riproduci i giorni' })).toBeVisible()
})

test('hub at / lists regions and enters one', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Ho capito' }).click()
  await page.getByRole('button', { name: 'Rifiuta' }).click()
  await expect(page).toHaveURL(/\/$/)
  await expect(page.getByRole('heading', { name: 'Regioni coperte' })).toBeVisible()
  await page.getByRole('link', { name: /^Toscana/ }).click()
  await expect(page).toHaveURL(/\/toscana$/)
  await expect(page.getByRole('radio', { name: 'Tutte' })).toBeVisible()
})

test('a region on the hub map is drawn to its border and opens on a tap', async ({
  page,
}) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Ho capito' }).click()
  await page.getByRole('button', { name: 'Rifiuta' }).click()
  await page.waitForFunction(() => {
    const map = window.__mushmaMap
    return !!map?.getLayer('hub-regions-fill') && map.loaded()
  })
  // Every Italian region's real boundary is there, not a box: served or not.
  const regions = await page.evaluate(() => {
    const features = window.__mushmaMap!.querySourceFeatures('hub-regions')
    return new Set(features.map((f) => String(f.properties.slug))).size
  })
  expect(regions).toBe(20)

  // Tuscany's label point is inside it, above the half-open sheet.
  const tuscany = await page.evaluate(() => {
    const map = window.__mushmaMap!
    const point = map.project([11.25, 43.42])
    const box = map.getCanvas().getBoundingClientRect()
    return { x: box.left + point.x, y: box.top + point.y }
  })
  await page.mouse.click(tuscany.x, tuscany.y)
  await expect(page).toHaveURL(/\/toscana$/)
})
