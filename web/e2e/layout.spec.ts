import { expect, test } from '@playwright/test'

// The desktop layout from its first width up to past the one where the 14-day time bar (792px)
// fits its column whole, at about 1416px.
const WIDTHS = [900, 1024, 1280, 1440]

test.use({ viewport: { width: 1280, height: 800 }, isMobile: false, hasTouch: false })

test('the time bar stays in the map and nothing scrolls the app sideways', async ({
  page,
}) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Ho capito' }).click()

  const main = page.getByRole('main')
  const app = main.locator('xpath=..')
  const strip = page.getByRole('radiogroup', { name: 'Giorno' })
  const center = page.getByRole('button', { name: 'Centra sulla mia posizione' })
  await expect(strip).toBeVisible()

  for (const width of WIDTHS) {
    await page.setViewportSize({ width, height: 800 })
    const box = async (locator: typeof strip) => (await locator.boundingBox())!
    const [mapBox, stripBox, centerBox] = [
      await box(main),
      await box(strip),
      await box(center),
    ]

    // The date strip ends inside the map instead of poking past its right edge...
    expect(stripBox.x, `strip left at ${width}px`).toBeGreaterThanOrEqual(mapBox.x)
    expect(stripBox.x + stripBox.width, `strip right at ${width}px`).toBeLessThanOrEqual(
      mapBox.x + mapBox.width,
    )
    // ...the app itself is never pushed sideways, so the wordmark and the panel stay in view...
    expect(await app.evaluate((el) => el.scrollLeft), `scrollLeft at ${width}px`).toBe(0)
    // ...and the center button sits above the time bar, not on it.
    expect(
      centerBox.y + centerBox.height,
      `center button at ${width}px`,
    ).toBeLessThanOrEqual(stripBox.y)
    expect(centerBox.x + centerBox.width).toBeLessThanOrEqual(mapBox.x + mapBox.width)
  }
})

test.describe('a 360 px phone in analysis mode', () => {
  test.use({ viewport: { width: 360, height: 740 }, isMobile: true, hasTouch: true })

  test('the factor panel sits between the species bar and the date strip', async ({
    page,
  }) => {
    await page.goto('/?mode=analysis&f=rain_trigger')
    await page.getByRole('button', { name: 'Ho capito' }).click()

    const panel = page.getByRole('region', { name: "Fattori dell'indice" })
    const toggle = page.getByRole('button', { name: 'Analisi' })
    const strip = page.getByRole('radiogroup', { name: 'Giorno' })
    const species = page.getByRole('radiogroup', { name: 'Specie' })
    await expect(panel.getByRole('button', { name: 'Pioggia di innesco' })).toBeVisible()
    await expect(strip).toBeVisible()

    const box = async (locator: typeof panel) => (await locator.boundingBox())!
    const [panelBox, toggleBox, stripBox, speciesBox] = [
      await box(panel),
      await box(toggle),
      await box(strip),
      await box(species),
    ]
    // Nothing covers the date strip, and the toggle stays under the species bar.
    expect(panelBox.y + panelBox.height).toBeLessThanOrEqual(stripBox.y)
    expect(toggleBox.y).toBeGreaterThanOrEqual(speciesBox.y + speciesBox.height)
    expect(panelBox.x).toBeGreaterThanOrEqual(0)
    expect(panelBox.x + panelBox.width).toBeLessThanOrEqual(360)
    const app = page.getByRole('main').locator('xpath=..')
    expect(await app.evaluate((el) => el.scrollLeft)).toBe(0)
  })
})
