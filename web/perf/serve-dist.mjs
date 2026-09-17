// A production-like static server for the performance check: serves dist/
// brotli-compressed with long-lived caching for hashed files (as Vercel does),
// the basemap extracts with range requests, and proxies /api to the fixture API.
//
//   node perf/serve-dist.mjs <port> <api-origin>
import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs'
import { request as httpRequest, createServer } from 'node:http'
import { extname, isAbsolute, join, relative, resolve } from 'node:path'
import { brotliCompressSync, constants } from 'node:zlib'

const [port = '5182', api = 'http://localhost:8011'] = process.argv.slice(2)
const root = resolve(import.meta.dirname, '..')
const dist = join(root, 'dist')
const basemap = join(root, 'data/basemap')
const types = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.css': 'text/css',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
}
const compressible = new Set(['.html', '.js', '.mjs', '.css', '.svg', '.json'])
const cache = new Map()

function serveFile(req, res, file) {
  const ext = extname(file)
  const immutable = file.includes('/assets/') || file.includes('/vendor/')
  res.setHeader('Content-Type', types[ext] ?? 'application/octet-stream')
  res.setHeader(
    'Cache-Control',
    immutable ? 'public, max-age=31536000, immutable' : 'no-cache',
  )
  if (compressible.has(ext) && /\bbr\b/.test(req.headers['accept-encoding'] ?? '')) {
    if (!cache.has(file)) {
      cache.set(
        file,
        brotliCompressSync(readFileSync(file), {
          params: { [constants.BROTLI_PARAM_QUALITY]: 9 },
        }),
      )
    }
    const body = cache.get(file)
    res.setHeader('Content-Encoding', 'br')
    res.setHeader('Content-Length', body.length)
    res.end(body)
    return
  }
  res.setHeader('Content-Length', statSync(file).size)
  createReadStream(file).pipe(res)
}

function serveRange(req, res, file) {
  const size = statSync(file).size
  let start = 0
  let end = size - 1
  res.setHeader('Accept-Ranges', 'bytes')
  res.setHeader('Content-Type', 'application/octet-stream')
  if (req.headers.range) {
    const range = /^bytes=(\d+)-(\d*)$/.exec(req.headers.range)
    start = range ? Number(range[1]) : size
    end = range?.[2] ? Math.min(Number(range[2]), size - 1) : size - 1
    if (start > end) {
      res.writeHead(416, { 'Content-Range': `bytes */${size}` }).end()
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

/** A regular file inside `root`, or undefined. */
function fileWithin(root, path) {
  const file = resolve(root, `.${path}`)
  const inside = relative(root, file)
  if (inside.startsWith('..') || isAbsolute(inside)) return undefined
  return existsSync(file) && statSync(file).isFile() ? file : undefined
}

createServer((req, res) => {
  let path
  try {
    path = decodeURIComponent(new URL(req.url, 'http://x').pathname)
  } catch {
    return res.writeHead(400).end()
  }
  if (path.startsWith('/api/')) {
    const target = new URL(req.url.replace(/^\/api/, ''), api)
    const upstream = httpRequest(
      target,
      { method: req.method, headers: req.headers },
      (up) => {
        res.writeHead(up.statusCode ?? 502, up.headers)
        up.pipe(res)
      },
    )
    upstream.on('error', () => res.writeHead(502).end())
    req.pipe(upstream)
    return
  }
  if (path.startsWith('/basemap/')) {
    const file = fileWithin(basemap, path.slice('/basemap'.length))
    return file ? serveRange(req, res, file) : res.writeHead(404).end()
  }
  const file = fileWithin(dist, path)
  serveFile(req, res, file ?? join(dist, 'index.html')) // SPA fallback
}).listen(Number(port), () =>
  console.log(`dist on http://localhost:${port}, api → ${api}`),
)
