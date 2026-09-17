import { defineConfig, devices } from '@playwright/test'

/**
 * Performance check (not part of CI): `pnpm run perf`. Builds with the real
 * basemap extracts if web/data/basemap/ has them (scripts/extract-basemap.sh).
 */
const API_PORT = 8012
const WEB_PORT = 5182

export default defineConfig({
  testDir: '.',
  testMatch: 'first-paint.spec.ts',
  reporter: 'list',
  timeout: 180_000,
  use: {
    baseURL: `http://localhost:${WEB_PORT}`,
    locale: 'it-IT',
    timezoneId: 'Europe/Rome',
  },
  projects: [
    {
      name: 'mid-range phone',
      use: {
        ...devices['Moto G4'],
        // A phone renders WebGL on its GPU, so use the host GPU where there is one;
        // software GL (SwiftShader) spends seconds compiling shaders on the CPU.
        launchOptions: {
          args:
            process.platform === 'darwin'
              ? ['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist']
              : ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'],
        },
      },
    },
  ],
  webServer: [
    {
      command: `uv run fastapi run src/api/main.py --port ${API_PORT}`,
      cwd: '../../api',
      env: { MUSHMA_FIXTURES: '1' },
      url: `http://localhost:${API_PORT}/health`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: `pnpm run build && node perf/serve-dist.mjs ${WEB_PORT} http://localhost:${API_PORT}`,
      cwd: '..',
      env: {
        VITE_API_BASE_URL: '/api',
        VITE_BASEMAP_URL: '/basemap/tuscany.pmtiles',
        VITE_TERRAIN_URL: '/basemap/tuscany-terrain.pmtiles',
      },
      url: `http://localhost:${WEB_PORT}`,
      reuseExistingServer: false,
      timeout: 180_000,
    },
  ],
})
