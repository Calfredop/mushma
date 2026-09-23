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
  const species = page.getByRole('radiogroup', { name: 'Specie' })
  const center = page.getByRole('button', { name: 'Centra sulla mia posizione' })
  await expect(strip).toBeVisible()

  for (const width of WIDTHS) {
    await page.setViewportSize({ width, height: 800 })
    const box = async (locator: typeof strip) => (await locator.boundingBox())!
    const [mapBox, stripBox, centerBox, speciesBox] = [
      await box(main),
      await box(strip),
      await box(center),
      await box(species),
    ]

    // The date strip ends inside the map instead of poking past its right edge...
    expect(stripBox.x, `strip left at ${width}px`).toBeGreaterThanOrEqual(mapBox.x)
    expect(stripBox.x + stripBox.width, `strip right at ${width}px`).toBeLessThanOrEqual(
      mapBox.x + mapBox.width,
    )
    // ...the app itself is never pushed sideways, so the wordmark and the panel stay in view...
    expect(await app.evaluate((el) => el.scrollLeft), `scrollLeft at ${width}px`).toBe(0)
    // ...and the center button, in the cluster at the top right, sits above the time bar and
    // beside the species pill, on neither.
    expect(
      centerBox.y + centerBox.height,
      `center button at ${width}px`,
    ).toBeLessThanOrEqual(stripBox.y)
    expect(centerBox.x + centerBox.width).toBeLessThanOrEqual(mapBox.x + mapBox.width)
    expect(
      speciesBox.x + speciesBox.width,
      `species pill at ${width}px`,
    ).toBeLessThanOrEqual(centerBox.x)
  }
})

// The narrowest phone the layout promises, and a common one.
for (const [width, height] of [
  [360, 640],
  [390, 844],
]) {
  test.describe(`a ${width} px phone`, () => {
    test.use({ viewport: { width, height }, isMobile: true, hasTouch: true })

    test('the map chrome: pill beside the cluster, legend chip above the strip, the rest in the sheet', async ({
      page,
    }) => {
      await page.goto('/')
      await page.getByRole('button', { name: 'Ho capito' }).click()
      await page.getByRole('button', { name: 'Rifiuta' }).click()

      const species = page.getByRole('radiogroup', { name: 'Specie' })
      const strip = page.getByRole('radiogroup', { name: 'Giorno' })
      const legend = page.getByRole('button', { name: 'Legenda' })
      const cluster = [
        page.getByRole('button', { name: 'Analisi' }),
        page.getByRole('button', { name: 'Centra sulla mia posizione' }),
        page.getByRole('button', { name: 'Info e impostazioni' }),
      ]
      await expect(strip).toBeVisible()

      const box = async (locator: typeof strip) => (await locator.boundingBox())!
      const speciesBox = await box(species)
      // Every species is whole inside the pill: none scrolled or clipped away.
      for (const radio of await species.getByRole('radio').all()) {
        const radioBox = await box(radio)
        expect(radioBox.x).toBeGreaterThanOrEqual(speciesBox.x)
        expect(radioBox.x + radioBox.width).toBeLessThanOrEqual(
          speciesBox.x + speciesBox.width + 0.5,
        )
      }
      for (const button of cluster) {
        const buttonBox = await box(button)
        // Beside the pill, not over it, inside the screen, and a whole tap target.
        expect(buttonBox.x).toBeGreaterThanOrEqual(speciesBox.x + speciesBox.width)
        expect(buttonBox.x + buttonBox.width).toBeLessThanOrEqual(width)
        expect(buttonBox.height).toBeGreaterThanOrEqual(44)
      }
      const legendBox = await box(legend)
      expect(legendBox.height).toBeGreaterThanOrEqual(44)
      expect(legendBox.y + legendBox.height).toBeLessThanOrEqual((await box(strip)).y)

      // No top bar: the wordmark and the search open the sheet.
      const sheet = page.getByRole('complementary')
      await expect(sheet.getByRole('heading', { level: 1 })).toBeVisible()
      await expect(sheet.getByRole('combobox')).toBeVisible()

      // The ⓘ menu opens whole on the screen.
      await page.getByRole('button', { name: 'Info e impostazioni' }).click()
      const menuBox = await box(page.getByRole('menu'))
      expect(menuBox.x).toBeGreaterThanOrEqual(0)
      expect(menuBox.x + menuBox.width).toBeLessThanOrEqual(width)
      expect(menuBox.y + menuBox.height).toBeLessThanOrEqual(height)
      await page.keyboard.press('Escape')
      await expect(page.getByRole('menu')).toBeHidden()

      const app = page.getByRole('main').locator('xpath=..')
      expect(await app.evaluate((el) => el.scrollLeft)).toBe(0)
      expect(await page.evaluate(() => document.scrollingElement!.scrollLeft)).toBe(0)
    })
  })
}

test.describe('a 360 px phone in analysis mode', () => {
  test.use({ viewport: { width: 360, height: 740 }, isMobile: true, hasTouch: true })

  test('the factor chips are one row just above the date strip', async ({ page }) => {
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
    // One row of chips, just above the date strip and never on it...
    expect(panelBox.y + panelBox.height).toBeLessThanOrEqual(stripBox.y)
    expect(stripBox.y - (panelBox.y + panelBox.height)).toBeLessThanOrEqual(16)
    expect(panelBox.height).toBeLessThanOrEqual(56)
    // ...opening on the opacity key, with the play button still in reach...
    await expect(panel.getByText('frena')).toBeInViewport()
    await expect(
      page.getByRole('button', { name: 'Riproduci i giorni' }),
    ).toBeInViewport()
    // ...and the ◈ toggle in the cluster beside the species bar, not on it.
    expect(toggleBox.x).toBeGreaterThanOrEqual(speciesBox.x + speciesBox.width)
    expect(panelBox.x).toBeGreaterThanOrEqual(0)
    expect(panelBox.x + panelBox.width).toBeLessThanOrEqual(360)
    const app = page.getByRole('main').locator('xpath=..')
    expect(await app.evaluate((el) => el.scrollLeft)).toBe(0)
  })
})
