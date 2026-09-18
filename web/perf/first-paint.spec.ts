/**
 * PRD → Constraints → Mobile performance: first map paint under ~3 s on 4G.
 *
 * A mid-range phone: 4× CPU slowdown, as in Lighthouse's mobile profile. The
 * network follows Chrome DevTools' presets:
 * - `fast4g` (default, the budget): 9 Mbps down, 1.5 Mbps up, 165 ms latency
 * - `slow4g` (stress, Lighthouse's mobile network): 1.6 Mbps, 750 kbps, 562 ms
 *
 * "First map paint" is the app's `mushma:first-map-paint` mark: the first time
 * the map goes idle with the basemap and the score cells drawn. Cold = empty
 * HTTP cache; warm = a reload.
 *
 *   pnpm run perf                        # fast4g
 *   PERF_NETWORK=slow4g pnpm run perf    # report only; the budget applies to 4G
 */
import { expect, test } from '@playwright/test'

const BUDGET_MS = 3000
const CPU_SLOWDOWN = Number(process.env.PERF_CPU_SLOWDOWN ?? 4)
const NETWORKS = {
  // Chrome DevTools NetworkManager presets (throughput × 0.9, latency × 2.75 / 3.75).
  fast4g: { latency: 60 * 2.75, download: (9e6 / 8) * 0.9, upload: (1.5e6 / 8) * 0.9 },
  slow4g: {
    latency: 150 * 3.75,
    download: (1.6e6 / 8) * 0.9,
    upload: (0.75e6 / 8) * 0.9,
  },
}
const NETWORK = (process.env.PERF_NETWORK ?? 'fast4g') as keyof typeof NETWORKS

async function measure(page: import('@playwright/test').Page) {
  const cdp = await page.context().newCDPSession(page)
  await cdp.send('Network.enable')
  const network = NETWORKS[NETWORK]
  await cdp.send('Network.emulateNetworkConditions', {
    offline: false,
    latency: network.latency,
    downloadThroughput: network.download,
    uploadThroughput: network.upload,
  })
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: CPU_SLOWDOWN })

  await page.goto('/', { waitUntil: 'commit' })
  const handle = await page.waitForFunction(
    () => {
      const [mark] = performance.getEntriesByName('mushma:first-map-paint')
      const [fcp] = performance.getEntriesByName('first-contentful-paint')
      const [appStart] = performance.getEntriesByName('mushma:app-start')
      const [mapCreated] = performance.getEntriesByName('mushma:map-created')
      const [mapLoaded] = performance.getEntriesByName('mushma:map-loaded')
      return (
        mark && {
          firstMapPaint: mark.startTime,
          fcp: fcp?.startTime ?? null,
          appStart: appStart?.startTime ?? null,
          mapCreated: mapCreated?.startTime ?? null,
          mapLoaded: mapLoaded?.startTime ?? null,
        }
      )
    },
    null,
    { timeout: 60_000, polling: 100 },
  )
  const timings = (await handle.jsonValue()) as {
    firstMapPaint: number
    fcp: number | null
  }
  const transfer = await page.evaluate(() =>
    Math.round(
      performance
        .getEntriesByType('resource')
        .reduce((sum, e) => sum + (e as PerformanceResourceTiming).transferSize, 0) /
        1024,
    ),
  )
  const heaviest = await page.evaluate(() =>
    (performance.getEntriesByType('resource') as PerformanceResourceTiming[])
      .map((e) => ({
        name: e.name.replace(location.origin, '').replace(/\?.*/, ''),
        kb: Math.round(e.transferSize / 1024),
        start: Math.round(e.startTime),
        end: Math.round(e.responseEnd),
      }))
      .sort((a, b) => b.kb - a.kb)
      .slice(0, 25),
  )
  if (process.env.PERF_DETAIL) console.log(JSON.stringify(heaviest))
  return { ...timings, transferKb: transfer }
}

test(`first map paint on a mid-range phone over throttled ${NETWORK}`, async ({
  browser,
  page,
}) => {
  // Start the browser's GPU process in a throwaway context first: a real phone
  // doesn't pay for spinning up software WebGL, and this context shares no cache.
  const warmup = await browser.newContext()
  const warmupPage = await warmup.newPage()
  await warmupPage.setContent('<canvas></canvas>')
  await warmupPage.evaluate(() => {
    const gl = document.querySelector('canvas')!.getContext('webgl2')
    gl?.clear(gl.COLOR_BUFFER_BIT)
    return new Promise((resolve) => requestAnimationFrame(resolve))
  })
  await warmup.close()

  const cold = await measure(page)
  const warm = await measure(page)
  const report = {
    network: NETWORK,
    cpuSlowdown: CPU_SLOWDOWN,
    cold: { ...cold, firstMapPaint: Math.round(cold.firstMapPaint) },
    warm: { ...warm, firstMapPaint: Math.round(warm.firstMapPaint) },
  }
  console.log(JSON.stringify(report, null, 2))
  await test.info().attach('first-paint.json', {
    body: JSON.stringify(report, null, 2),
    contentType: 'application/json',
  })
  if (NETWORK === 'fast4g') expect(cold.firstMapPaint).toBeLessThan(BUDGET_MS)
})
