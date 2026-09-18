# Performance check: first map paint

M5 frontend core. Traces to PRD → Constraints → Mobile performance ("first map paint under ~3 s on
4G"). Measured 2026-09-17 against fixture data.

## Result

| network (Chrome DevTools preset) | CPU | cold first map paint | cold FCP | warm first map paint | cold transfer |
|---|---|---|---|---|---|
| **Fast 4G**: 9 Mbps down, 1.5 Mbps up, 165 ms latency | 4× slower | **2.62 s, 2.68 s, 2.43 s** (3 runs) | 1.1–1.3 s | 1.3–1.4 s | 646 KB |
| Slow 4G (Lighthouse's mobile network): 1.6 Mbps, 750 kbps, 562 ms | 4× slower | 8.1 s | 3.7 s | 3.7 s | 646 KB |

**It passes the 3 s budget on 4G with ~10% headroom.** On Lighthouse's Slow 4G, which is closer to a
good 3G link, the cold cache takes 8 s. Just moving the ~650 KB a vector map needs takes over 3 s at
1.6 Mbps. After the first visit, reloads take 3.7 s on that link, and M7's offline cache is what
covers bad signal in the woods.

## How it's measured

`pnpm run perf` in `web/` (`web/perf/`, not part of CI):

1. Builds the app with the real basemap extracts (`scripts/extract-basemap.sh`).
2. Serves `dist/` the way production does: brotli, immutable caching for hashed and `/vendor/`
   files, range requests for the `.pmtiles` files. It also starts the fixture API.
3. Loads the page in Playwright's Chromium on a Moto G4 viewport. It throttles network and CPU with
   the Chrome DevTools Protocol and reads the app's `mushma:first-map-paint` mark. That mark is the
   first time the map is idle with the basemap and the score cells drawn.

On macOS, WebGL runs on the host GPU (ANGLE Metal), because a phone has a GPU too. With software
GL (SwiftShader), shader compilation alone took 4 s of CPU and hid every real cost. The first
profile flagged that as `_setupPainter`.

`PERF_NETWORK=slow4g` and `PERF_CPU_SLOWDOWN=6` change the profile. The budget is only enforced
on Fast 4G.

## What got it under budget

Cold first map paint started at 12 s on Slow 4G with software GL. On Fast 4G with the GPU it was
3–4 s, before these changes:

- **MapLibre served verbatim**, not re-bundled: `/vendor/maplibre-gl-<version>/`, preloaded with
  `modulepreload`. The main thread and the web worker share one cached copy of
  `maplibre-gl-shared.mjs`. Re-bundling also broke the worker, and the map never loaded.
- **Score layers baked into the initial style**, so the map's first complete render already
  includes the cells, with no second pass after `load`.
- **Hillshade after the first paint.** The terrain tiles, about 250 KB, were the heaviest part of
  the cold load, so relief now fades in once the scores are on screen.
- **The map is created after the app shell paints**, so the header, species switcher and hot places
  show while WebGL starts up.
- **No PMTiles metadata request** (the style already names the layers), and a `preconnect` to the
  glyph and sprite host.

## Cold-load budget today

About 380 KB of JavaScript (brotli): MapLibre ~263 KB, the app ~117 KB. Then ~80 KB of fonts,
~150 KB of basemap tiles and directories, three glyph ranges, the sprite, and the API.

## Re-run when

- **M4 changes grid delivery.** 34 fixture cells are a few KB, but ~12k real cells can reach the
  PRD's ~1 MB compressed payload budget. That payload sits on the critical path.
- **The basemap moves to the Cloudflare Worker** (one more origin and a TLS handshake), or glyphs and
  sprites are self-hosted in M7 (one fewer).
- **The API goes live on Fly.** `auto_stop_machines = "stop"` means a cold start can add seconds to
  the first `/scores` request. Keeping one machine running, or caching `/scores` at the edge, would
  remove that.
