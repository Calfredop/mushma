/// <reference types="vitest/config" />
import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs'
import { isAbsolute, relative, resolve } from 'node:path'
import react from '@vitejs/plugin-react'
import { type Connect, defineConfig, loadEnv, type Plugin, type UserConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

const BASEMAP_DIR = resolve(import.meta.dirname, 'data/basemap')

/**
 * Serves the gitignored basemap extracts (scripts/extract-basemap.sh) at
 * /basemap/ in dev and preview, with the HTTP range requests PMTiles needs.
 * Production reads them from object storage instead (PRD → Basemap).
 */
function serveBasemap(): Plugin {
  const middleware: Connect.NextHandleFunction = (req, res, next) => {
    if (!req.url?.startsWith('/basemap/')) return next()
    let file: string
    try {
      file = resolve(BASEMAP_DIR, decodeURIComponent(req.url.split('?')[0].slice(9)))
    } catch {
      return next()
    }
    // Only files inside BASEMAP_DIR: no `..`, no absolute paths, no directories.
    const inside = relative(BASEMAP_DIR, file)
    if (!inside || inside.startsWith('..') || isAbsolute(inside)) return next()
    const stat = existsSync(file) ? statSync(file) : undefined
    if (!stat?.isFile()) return next()

    const size = stat.size
    let start = 0
    let end = size - 1
    res.setHeader('Accept-Ranges', 'bytes')
    res.setHeader('Content-Type', 'application/octet-stream')
    if (req.headers.range) {
      const range = /^bytes=(\d+)-(\d*)$/.exec(req.headers.range)
      start = range ? Number(range[1]) : size
      end = range?.[2] ? Math.min(Number(range[2]), size - 1) : size - 1
      if (start > end) {
        res.statusCode = 416
        res.setHeader('Content-Range', `bytes */${size}`)
        res.end()
        return
      }
      res.statusCode = 206
      res.setHeader('Content-Range', `bytes ${start}-${end}/${size}`)
    }
    res.setHeader('Content-Length', end - start + 1)
    createReadStream(file, { start, end })
      .on('error', () => res.destroy())
      .pipe(res)
  }
  return {
    name: 'mushma-serve-basemap',
    configureServer: (server) => void server.middlewares.use(middleware),
    configurePreviewServer: (server) => void server.middlewares.use(middleware),
  }
}

/**
 * MapLibre 6 starts its web worker from `maplibre-gl-worker.mjs` next to its
 * own module, and the worker imports `maplibre-gl-shared.mjs`. Re-bundling it
 * breaks that (the map never loads), so it's served verbatim: excluded from
 * dev pre-bundling, and in builds kept external and copied to a versioned
 * /vendor/ path. The main thread and the worker then share one cached copy of
 * the shared chunk.
 */
const MAPLIBRE_DIST = resolve(import.meta.dirname, 'node_modules/maplibre-gl/dist')
const MAPLIBRE_VERSION: string = JSON.parse(
  readFileSync(resolve(MAPLIBRE_DIST, '../package.json'), 'utf8'),
).version
const MAPLIBRE_VENDOR = `vendor/maplibre-gl-${MAPLIBRE_VERSION}`
const MAPLIBRE_FILES = [
  'maplibre-gl.mjs',
  'maplibre-gl-shared.mjs',
  'maplibre-gl-worker.mjs',
]

function vendorMaplibre(): Plugin {
  return {
    name: 'mushma-vendor-maplibre',
    apply: 'build',
    config: () => ({
      build: {
        rollupOptions: {
          external: ['maplibre-gl'],
          output: { paths: { 'maplibre-gl': `/${MAPLIBRE_VENDOR}/maplibre-gl.mjs` } },
        },
      },
    }),
    generateBundle() {
      for (const file of MAPLIBRE_FILES) {
        this.emitFile({
          type: 'asset',
          fileName: `${MAPLIBRE_VENDOR}/${file}`,
          source: readFileSync(resolve(MAPLIBRE_DIST, file)),
        })
      }
    },
    transformIndexHtml: () =>
      ['maplibre-gl.mjs', 'maplibre-gl-shared.mjs'].map((file) => ({
        tag: 'link',
        attrs: { rel: 'modulepreload', href: `/${MAPLIBRE_VENDOR}/${file}` },
        injectTo: 'head' as const,
      })),
  }
}

/**
 * Offline caching (PRD → PWA, M7): the app shell and fonts are precached (generateSW's own
 * build manifest, below); everything else is cached as it's used, never speculatively:
 * - API responses (scores, spot forecasts, hotspots, comuni, history, outlook, status): the
 *   read-only GET routes the API serves, matched by path regardless of `VITE_API_BASE_URL`
 *   being a same-origin proxy/rewrite or an absolute cross-origin URL. NetworkFirst, so a
 *   forager with signal always gets today's numbers; a short timeout falls back to whatever
 *   was last cached for that place once the signal drops.
 * - Basemap/terrain tiles and Protomaps' glyphs/sprite (self-hosted extracts, PRD → Basemap):
 *   CacheFirst, since a build-pinned tile never changes. `cacheableResponse: [0, 200]` is the
 *   safety net PRD → Basemap warns about: the pmtiles protocol reads `.pmtiles` files with
 *   byte-range requests (206), which the Cache API can't store — Workbox silently skips
 *   caching those and the map still works, just without that tile offline.
 */
const API_ROUTE_RE =
  /\/(scores|spot|cells\/[^/?]+|hotspots|sightings|comuni|history\/[^/?]+|outlook|status)(\?|$)/

function tileOrigin(url: string | undefined): string | undefined {
  if (!url) return undefined
  try {
    return new URL(url).origin
  } catch {
    return undefined // relative (local dev, served from this same origin under /basemap/)
  }
}

function pwaPlugin(env: Record<string, string>): Plugin[] {
  const tileOrigins = new Set(
    [tileOrigin(env.VITE_BASEMAP_URL), tileOrigin(env.VITE_TERRAIN_URL)].filter(
      (v) => !!v,
    ),
  )
  return VitePWA({
    registerType: 'autoUpdate',
    includeAssets: ['favicon.svg', 'icons/apple-touch-icon.png'],
    manifest: {
      name: 'Mappa Funghi',
      short_name: 'Mappa Funghi',
      description:
        'Fruiting-conditions scores for porcini, ovoli and gallinacci in Tuscany.',
      lang: 'it',
      start_url: '/',
      scope: '/',
      display: 'standalone',
      background_color: '#edf0ea',
      theme_color: '#edf0ea',
      icons: [
        {
          src: '/icons/icon-192.png',
          sizes: '192x192',
          type: 'image/png',
          purpose: 'any',
        },
        {
          src: '/icons/icon-512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any',
        },
        {
          src: '/icons/icon-maskable-512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'maskable',
        },
      ],
    },
    workbox: {
      navigateFallback: '/index.html',
      // The basemap/terrain extracts are 100+ MB and never part of the build; only the app
      // shell (JS/CSS/fonts) is precached here.
      globPatterns: ['**/*.{js,css,html,woff2}'],
      runtimeCaching: [
        {
          urlPattern: ({ url, request }) =>
            request.method === 'GET' && API_ROUTE_RE.test(url.pathname),
          handler: 'NetworkFirst',
          options: {
            cacheName: 'mushma-api',
            networkTimeoutSeconds: 4,
            cacheableResponse: { statuses: [0, 200] },
            expiration: { maxEntries: 300, maxAgeSeconds: 2 * 24 * 60 * 60 },
          },
        },
        {
          urlPattern: ({ url, request }) =>
            request.method === 'GET' &&
            (url.origin === 'https://protomaps.github.io' ||
              tileOrigins.has(url.origin) ||
              url.pathname.startsWith('/basemap/')),
          handler: 'CacheFirst',
          options: {
            cacheName: 'mushma-basemap',
            cacheableResponse: { statuses: [0, 200] },
            expiration: { maxEntries: 4000, maxAgeSeconds: 30 * 24 * 60 * 60 },
          },
        },
      ],
    },
  })
}

/**
 * Tunnel mode (`scripts/tunnel.sh`, `pnpm run tunnel`): serve this dev server through a
 * cloudflared quick tunnel so a phone or a friend can reach the local stack.
 *
 * - `allowedHosts`: Vite refuses a request whose `Host` header it doesn't know. The quick
 *   tunnel's hostname is random per run, so the whole domain is allowed (a leading dot is
 *   Vite's subdomain wildcard) rather than passed back in from cloudflared.
 * - `host`: bind every interface, which also makes the server reachable over the LAN.
 * - `hmr`: the tunnel terminates TLS on 443, so the HMR socket has to be told to dial
 *   `wss://<host>:443`. Without this the app loads and live reload silently stops.
 *
 * The API needs nothing: it rides the `/api` proxy below on the same origin, so there is no
 * second hostname and no CORS. `tunnel.sh` exports `VITE_API_BASE_URL=/api` to make sure of
 * it (a real env var outranks `.env`, where a local override may point at localhost:8000).
 */
const TUNNEL_SERVER: UserConfig['server'] = {
  allowedHosts: ['.trycloudflare.com'],
  host: true,
  hmr: { protocol: 'wss', clientPort: 443 },
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, import.meta.dirname, '')
  const apiProxy = {
    '/api': {
      target: env.API_PROXY_TARGET || 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path: string) => path.replace(/^\/api/, ''),
    },
  }
  return {
    plugins: [react(), serveBasemap(), vendorMaplibre(), ...pwaPlugin(env)],
    optimizeDeps: { exclude: ['maplibre-gl'] },
    server: { proxy: apiProxy, ...(env.TUNNEL ? TUNNEL_SERVER : {}) },
    preview: { proxy: apiProxy },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './src/test/setup.ts',
      include: ['src/**/*.test.{ts,tsx}'],
    },
  }
})
