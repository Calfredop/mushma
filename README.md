# mushma

Estimates where and when wild edible mushrooms (porcini, ovoli, gallinacci)
are likely to be fruiting in **Tuscany**, from transparent per-species rules
over weather, habitat and terrain, validated against public sightings. See
`.gavin-root/PRD.md` for the full product requirements.

## Layout

- `web/` — Vite + React + TypeScript SPA, MapLibre GL, i18n (it/en), PWA.
  Deployed to Vercel.
- `api/` — Python + FastAPI service and the scheduled data pipeline
  (ingest → grid scoring → store). Deployed to Fly.io.
- `.gavin-root/docs/` — research and reports (species ecology, sightings
  profile, validation).

## Prerequisites

- [pnpm](https://pnpm.io) (Node version pinned in `.nvmrc`; use
  [nvm](https://github.com/nvm-sh/nvm) or [fnm](https://github.com/Schniz/fnm) to install it)
- [uv](https://docs.astral.sh/uv/) (installs the pinned Python itself)
- [Docker](https://www.docker.com/) if you want to build the `api/` image locally
- [flyctl](https://fly.io/docs/flyctl/install/) to deploy `api/`

## web/

```sh
cd web
pnpm install
cp .env.example .env
pnpm dev             # dev server, http://localhost:5173
pnpm test            # Vitest (unit + components, includes the i18n missing-key check)
pnpm run test:e2e    # Playwright smoke test: map → spot → why (starts the fixture API itself)
pnpm run lint        # ESLint (also rejects hardcoded UI strings)
pnpm run format:check
pnpm run build       # type-check + production build
pnpm run perf        # first-map-paint check on a throttled phone profile (local only)
```

`.env` points `VITE_API_BASE_URL` at `/api`, which the dev server proxies to
`API_PROXY_TARGET` (default `http://localhost:8000`). Run the API in fixture
mode alongside it (see api/ below).

**Basemap.** The map uses a self-hosted Protomaps extract plus Mapterhorn
hillshade (PRD → Architecture → Basemap). Fetch them once with the
[pmtiles CLI](https://docs.protomaps.com/pmtiles/cli) (`brew install pmtiles`):

```sh
cd web && scripts/extract-basemap.sh   # ~210 MB into the gitignored web/data/basemap/
```

The dev server serves them at `/basemap/`. Without them, leave
`VITE_BASEMAP_URL` and `VITE_TERRAIN_URL` empty and the map draws a plain land
fill. `pnpm run test:e2e` always runs that way.

`.gavin-root/docs/visual-direction.md` has the palette, the score colour scale
and the type choices. `.gavin-root/docs/perf-first-map-paint.md` has the
performance method and results.

`web/src/api/schema.ts` is a TypeScript client generated from `api/openapi.json`
(the API's contract). After changing any `api/` route or response model, run
`uv run python scripts/export_openapi.py` in `api/`, then
`pnpm run generate:api` in `web/`, and commit both. CI fails if either drifts.

## api/

```sh
cd api
uv sync
uv run fastapi dev src/api/main.py   # dev server, http://localhost:8000
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

`GET /health` returns `{"status": "ok"}`.

The routes don't read the data pipeline's stores (below) yet (M4), so the API only runs in
fixture mode: set `MUSHMA_FIXTURES=1` (see `api/.env.example`) to serve the real routes
(`/scores`, `/spot`, `/cells/{id}`, `/hotspots`, `/sightings`) from a hand-shaped fixture
dataset. Without it those routes return 503.

### Woodland grid

The static 1 km grid (woodland mask, habitat, terrain, soil pH, place labels) is built by a
reproducible script. It downloads every source into `api/data/raw/` once (about 2 GB unpacked,
gitignored) and writes `api/data/grid/tuscany/`: about 10 minutes the first time (SoilGrids is
slow), under 2 minutes after that.

```sh
cd api
uv run python -m api.grid.build --region tuscany
```

Set `DATA_DIR` to build somewhere else (it is `/data` on Fly). Outputs, sources and the woodland
rule are described in `.gavin-root/docs/woodland-grid.md`.

### Weather

Daily weather comes from Open-Meteo: ERA5-Land history and the ECMWF IFS forecast, fetched on a
0.2° lattice of model nodes and downscaled to the woodland cells. Build the point set once the grid
exists, then backfill and update:

```sh
cd api
uv run python -m api.weather.ingest points            # land nodes and cell weights (~130 API calls)
uv run python -m api.weather.ingest backfill --wait   # history from 2016, newest first; ~4 days
uv run python -m api.weather.ingest update            # daily: new reanalysis days + 7-day forecast
uv run python -m api.weather.ingest downscale --start 2026-09-10 --end 2026-09-24
```

The backfill stays under the free API limits (it keeps a shared tally in
`api/data/raw/open_meteo/usage.json`), resumes where it stopped, and skips anything already stored.
Sources, method, checks and the backfill-depth decision are in `.gavin-root/docs/weather-ingest.md`.

### Sightings

Public porcini, ovoli and gallinacci sightings come from GBIF (which already carries research-grade
iNaturalist records) and, for the last two weeks GBIF hasn't caught up with, iNaturalist directly.
They validate the model and back the hotspots list's "recent sightings" signal:

```sh
cd api
uv run python -m api.sightings.ingest resolve-taxa   # check config against each API's taxonomy
uv run python -m api.sightings.ingest fetch          # GBIF history + recent iNaturalist -> store
uv run python -m api.sightings.ingest profile        # counts, licenses, town-proximity bias
```

Only a cell id and species ever land in the store: no sighting's coordinates are kept, so nothing
finer than a 1 km cell can leave it. Method, quality filters and the first pull's profile are in
`.gavin-root/docs/sightings-profile.md`.

### Model

Per-species rules (`api/src/api/config/species/`, one file per species key, every rule with a cited
source) score each woodland cell and day from 0 to 1: a conditions index, not a probability. Groups
(porcini, ovoli, gallinacci) take the max over their keys and `combined` the max over the groups in
season. Every score keeps its factor breakdown.

```sh
cd api
uv run python -m api.model.pipeline rules                                          # validate and summarise
uv run python -m api.model.pipeline score --start 2026-09-03 --end 2026-09-24      # recent days + forecast
uv run python -m api.model.pipeline score --start 2025-01-01 --end 2025-12-31 --no-factors  # history
```

Scores land in `api/data/scores/tuscany/` (`daily/` for every key, `factors/` for the breakdowns).
A year of every cell takes about 25 seconds. How a score is computed is in
`api/src/api/config/species/README.md`; the evidence is in `.gavin-root/docs/species-ecology.md`.

To build and run the production container locally:

```sh
cd api
docker build -t mushma-api .
docker run -p 8000:8000 mushma-api
```

### Scheduled job

`api/src/api/jobs/daily.py` is the one command the Fly-scheduled machine runs: weather update →
sightings fetch → score today -6 to +7 (the served window, with factors) → store. (No separate
"downscale to cells" step: scoring downscales on the fly from the point-level weather store, so
running the ingest CLI's `downscale` export here would just be unused disk churn.) It runs each
step as its own process in that order and stops at the first failure rather than risk scoring on
top of a half-updated weather store; every step logs one JSON line on start and finish.
Set `ALERT_WEBHOOK_URL` (a Slack/Discord/etc. incoming webhook) to get a one-line POST on failure;
unset, it's a no-op and only Fly's own machine-exit alerting fires.

```sh
cd api
uv run python -m api.jobs.daily
```

Must finish well before 07:00 Europe/Rome (PRD → Constraints → Freshness) — see Deploying below for
how it's scheduled, and check the actual run time after the first few days land.

## CI

GitHub Actions (`.github/workflows/ci.yml`) lints and tests both `web/` and
`api/` on every push and pull request against `main`.

## Deploying

- **web/** → Vercel. Import the repo, set the project's Root Directory to
  `web`, and set these environment variables:
  - `VITE_API_BASE_URL`: the deployed `api/` URL (the API needs CORS for the
    Vercel domain; M4).
  - `VITE_BASEMAP_URL` and `VITE_TERRAIN_URL`: the basemap files uploaded to
    object storage (a `.pmtiles` URL served with range requests, or a TileJSON
    URL from the Protomaps Cloudflare Worker).
- **api/** → Fly.io. From `api/`: `fly launch --no-deploy` to attach an app
  (the included `fly.toml` is a starting point), `fly volumes create
  mushma_data --size 1` for the DuckDB/Parquet data directory, then
  `fly deploy`. That starts the `web` process group behind `http_service`;
  the scheduled job is a separate machine you create once from the `job`
  process group in `fly.toml`:

  ```sh
  fly machine run . --app mushma-api --process-group job --schedule daily \
    --vm-memory 1024
  ```

  (check `fly machine run --help` for the exact flags on your flyctl version —
  they've moved before). After the first couple of runs, check `fly machine
  status`/`fly logs` for the actual trigger time and nudge the schedule if
  needed so it lands before 07:00 Europe/Rome. Set `ALERT_WEBHOOK_URL` with
  `fly secrets set` if you want failure notifications.
