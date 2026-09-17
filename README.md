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
pnpm dev            # dev server, http://localhost:5173
pnpm test           # Vitest
pnpm run lint        # ESLint
pnpm run format:check
pnpm run build       # type-check + production build
```

Copy `web/.env.example` to `web/.env` and set `VITE_API_BASE_URL` to point at
a running `api/` (defaults to `http://localhost:8000`).

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

To build and run the production container locally:

```sh
cd api
docker build -t mushma-api .
docker run -p 8000:8000 mushma-api
```

## CI

GitHub Actions (`.github/workflows/ci.yml`) lints and tests both `web/` and
`api/` on every push and pull request against `main`.

## Deploying

- **web/** → Vercel. Import the repo, set the project's Root Directory to
  `web`, and set `VITE_API_BASE_URL` to the deployed `api/` URL in the
  project's environment variables.
- **api/** → Fly.io. From `api/`: `fly launch --no-deploy` to attach an app
  (the included `fly.toml` is a starting point), `fly volumes create
  mushma_data --size 1` for the DuckDB/Parquet data directory, then
  `fly deploy`.
