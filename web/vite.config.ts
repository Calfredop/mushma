/// <reference types="vitest/config" />
import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs'
import { isAbsolute, relative, resolve } from 'node:path'
import react from '@vitejs/plugin-react'
import { type Connect, defineConfig, loadEnv, type Plugin } from 'vite'

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
    plugins: [react(), serveBasemap(), vendorMaplibre()],
    optimizeDeps: { exclude: ['maplibre-gl'] },
    server: { proxy: apiProxy },
    preview: { proxy: apiProxy },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './src/test/setup.ts',
      include: ['src/**/*.test.{ts,tsx}'],
    },
  }
})
