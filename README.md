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
pnpm run lint        # ESLint (also rejects hardcoded UI strings)
pnpm run format:check
pnpm run build       # type-check + production build
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
fill.

`.gavin-root/docs/visual-direction.md` has the palette, the score colour scale
and the type choices.

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

There's no data layer yet (M2/M3), so the API only runs in fixture mode:
set `MUSHMA_FIXTURES=1` (see `api/.env.example`) to serve the real routes
(`/scores`, `/spot`, `/cells/{id}`, `/hotspots`, `/sightings`) from a
hand-shaped fixture dataset. Without it those routes return 503.

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
  `web`, and set these environment variables:
  - `VITE_API_BASE_URL`: the deployed `api/` URL (the API needs CORS for the
    Vercel domain; M4).
  - `VITE_BASEMAP_URL` and `VITE_TERRAIN_URL`: the basemap files uploaded to
    object storage (a `.pmtiles` URL served with range requests, or a TileJSON
    URL from the Protomaps Cloudflare Worker).
- **api/** → Fly.io. From `api/`: `fly launch --no-deploy` to attach an app
  (the included `fly.toml` is a starting point), `fly volumes create
  mushma_data --size 1` for the DuckDB/Parquet data directory, then
  `fly deploy`.
