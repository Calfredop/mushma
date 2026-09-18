import { defineConfig, devices } from '@playwright/test'

/**
 * End-to-end smoke test against the real FastAPI app in fixture mode and the
 * Vite dev server. The basemap is left out (a plain land fill) so the test
 * needs neither the tile extracts nor the network.
 */
const API_PORT = 8011
const WEB_PORT = 5181

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL: `http://localhost:${WEB_PORT}`,
    locale: 'it-IT',
    timezoneId: 'Europe/Rome',
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'mobile',
      use: {
        ...devices['Pixel 7'],
        // WebGL for MapLibre in headless Chromium.
        launchOptions: {
          args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'],
        },
      },
    },
  ],
  webServer: [
    {
      command: `uv run fastapi run src/api/main.py --port ${API_PORT}`,
      cwd: '../api',
      env: { MUSHMA_FIXTURES: '1' },
      url: `http://localhost:${API_PORT}/health`,
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
    {
      command: `pnpm exec vite --port ${WEB_PORT} --strictPort`,
      env: {
        API_PROXY_TARGET: `http://localhost:${API_PORT}`,
        VITE_API_BASE_URL: '/api',
        VITE_BASEMAP_URL: '',
        VITE_TERRAIN_URL: '',
      },
      url: `http://localhost:${WEB_PORT}`,
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
    },
  ],
})
