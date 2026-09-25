import { expect, type Locator, type Page, test } from '@playwright/test'
import type { Map as MapLibreMap } from 'maplibre-gl'

declare global {
  interface Window {
    __mushmaMap?: MapLibreMap
  }
}

// The phone sheet: an overlay on the map with peek, half and full snaps (the default project is
// a Pixel 7, with touch).

async function open(page: Page, path = '/toscana') {
  await page.goto(path)
  await page.getByRole('button', { name: 'Ho capito' }).click()
  await page.getByRole('button', { name: 'Rifiuta' }).click()
  const sheet = page.getByRole('complementary')
  await expect(sheet).toHaveAttribute('data-snap', 'peek')
  return sheet
}

const box = async (locator: Locator) => (await locator.boundingBox())!

/** A finger on the screen, through the browser's own touch input, so it scrolls like one. */
async function swipe(page: Page, x: number, from: number, to: number, steps = 10) {
  const cdp = await page.context().newCDPSession(page)
  const point = (y: number) => [{ x, y }]
  await cdp.send('Input.dispatchTouchEvent', {
    type: 'touchStart',
    touchPoints: point(from),
  })
  for (let i = 1; i <= steps; i++) {
    await cdp.send('Input.dispatchTouchEvent', {
      type: 'touchMove',
      touchPoints: point(from + ((to - from) * i) / steps),
    })
    await page.waitForTimeout(16)
  }
  // Hold still before lifting, so the release is a placement, not a flick.
  await page.waitForTimeout(120)
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
}

test('the handle drags the sheet up to full and back down to peek', async ({ page }) => {
  const sheet = await open(page)
  const handle = await box(page.getByRole('button', { name: 'Espandi il pannello' }))
  const x = handle.x + handle.width / 2
  const y = handle.y + handle.height / 2

  await page.mouse.move(x, y)
  await page.mouse.down()
  await page.mouse.move(x, 60, { steps: 20 })
  await page.waitForTimeout(120)
  await page.mouse.up()
  await expect(sheet).toHaveAttribute('data-snap', 'full')

  // The top controls are under it now, faded out.
  await expect(page.getByRole('radiogroup', { name: 'Specie' })).toBeHidden()

  const top = await box(page.getByRole('button', { name: 'Riduci il pannello' }))
  await page.mouse.move(x, top.y + top.height / 2)
  await page.mouse.down()
  await page.mouse.move(x, page.viewportSize()!.height - 10, { steps: 20 })
  await page.waitForTimeout(120)
  await page.mouse.up()
  await expect(sheet).toHaveAttribute('data-snap', 'peek')
  await expect(page.getByRole('radiogroup', { name: 'Specie' })).toBeVisible()
})

test('at full the body scrolls; only a pull down from its top brings the sheet down', async ({
  page,
}) => {
  const sheet = await open(page)
  await page.getByRole('button', { name: 'Espandi il pannello' }).click()
  await page.getByRole('button', { name: 'Espandi il pannello' }).click()
  await expect(sheet).toHaveAttribute('data-snap', 'full')
  const body = sheet.locator('[data-part="body"]')
  const bodyBox = await box(body)
  const x = bodyBox.x + bodyBox.width / 2

  // Scrolled down a way: a pull down scrolls it back, the sheet stays.
  await body.evaluate((element) => (element.scrollTop = 300))
  await swipe(page, x, bodyBox.y + 150, bodyBox.y + 300)
  await expect(sheet).toHaveAttribute('data-snap', 'full')
  expect(await body.evaluate((element) => element.scrollTop)).toBeLessThan(300)

  // From the very top: the pull takes the sheet with it.
  await body.evaluate((element) => (element.scrollTop = 0))
  await swipe(page, x, bodyBox.y + 100, bodyBox.y + 450)
  await expect(sheet).not.toHaveAttribute('data-snap', 'full')
})

test('a tapped place stays in view above the sheet', async ({ page }) => {
  const sheet = await open(page)
  await page.waitForFunction(
    () => (window.__mushmaMap?.querySourceFeatures('cells-points').length ?? 0) > 0,
  )
  // A cell low on the map, where the half-open sheet would cover it.
  const target = await page.evaluate(() => {
    const map = window.__mushmaMap!
    const canvas = map.getCanvas().getBoundingClientRect()
    const cells = map
      .querySourceFeatures('cells-points')
      .map((feature) => {
        const [lon, lat] = (feature.geometry as { coordinates: [number, number] })
          .coordinates
        const point = map.project([lon, lat])
        return { lon, lat, x: canvas.left + point.x, y: canvas.top + point.y }
      })
      .filter((cell) => cell.x > 40 && cell.x < canvas.width - 80)
    return cells.reduce((low, cell) =>
      cell.y > low.y && cell.y < canvas.height * 0.62 ? cell : low,
    )
  })
  await page.mouse.click(target.x, target.y)
  await expect(sheet).toHaveAttribute('data-snap', 'half')
  await page.waitForFunction(() => !window.__mushmaMap!.isMoving())

  const sheetTop = (await box(sheet)).y
  const onScreen = await page.evaluate(
    ([lon, lat]) => window.__mushmaMap!.project([lon, lat]).y,
    [target.lon, target.lat],
  )
  expect(onScreen).toBeLessThan(sheetTop)
  expect(onScreen).toBeGreaterThan(0)
})

test('the handle is a whole tap target: a tap just below its grip still steps the sheet', async ({
  page,
}) => {
  const sheet = await open(page)
  const handle = await box(page.getByRole('button', { name: 'Espandi il pannello' }))
  expect(handle.height).toBeLessThan(44)
  // 8px under the handle's own box, over the wordmark.
  await page.mouse.click(handle.x + 40, handle.y + handle.height + 8)
  await expect(sheet).toHaveAttribute('data-snap', 'half')
})

test('with reduced motion the sheet jumps to its snap, without a spring', async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: 'reduce' })
  const sheet = await open(page)
  await page.getByRole('button', { name: 'Espandi il pannello' }).click()
  const soon = await sheet.evaluate((element) => element.style.transform)
  await page.waitForTimeout(800)
  const settled = await sheet.evaluate((element) => element.style.transform)
  expect(soon).toBe(settled)
  await expect(sheet).toHaveAttribute('data-snap', 'half')
})
