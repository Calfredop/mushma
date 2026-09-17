<!-- gavin:start -->
## Gavin workspace

This repo is a gavin workspace. Read `.gavin-root/PRD.md` first — it leads all
development. Follow the gavin workflow skill in `.opencode/skills/gavin/SKILL.md`
(plan before coding, keep plan statuses current, use the gavin_* MCP tools).
<!-- gavin:end -->

## Project

mushma estimates where and when wild edible mushrooms (porcini, ovoli,
gallinacci) are likely to fruit in **Tuscany**. It does this with transparent
per-species rules over weather, habitat and terrain, validated against public
sightings. It is for a group of friends and a portfolio. The PRD
(`.gavin-root/PRD.md`) has the details.

This file is the single source of project instructions: `CLAUDE.md` and
`GEMINI.md` import it. Edit here.

## Layout

- `web/` — Vite + React + TypeScript (strict) SPA, MapLibre GL, i18n (it/en;
  library chosen in M5), PWA. Deployed to Vercel.
  - `cd web && pnpm install` then `pnpm dev` (dev server), `pnpm test`
    (Vitest), `pnpm run lint` (ESLint), `pnpm run format:check` (Prettier),
    `pnpm run build` (type-check + production build).
- `api/` — Python + FastAPI service and the scheduled data pipeline
  (ingest → grid scoring → store). Storage is DuckDB reading Parquet files on
  a Fly Volume (not Postgres/PostGIS — see PRD → Architecture). Deployed to
  Fly.io.
  - `cd api && uv sync` then `uv run fastapi dev src/api/main.py` (dev
    server), `uv run pytest`, `uv run ruff check .`,
    `uv run ruff format --check .`.
- `.gavin-root/docs/` — research and reports (species ecology, sightings
  profile, validation). Cards write their findings there.

See the root `README.md` for the full dev and deploy commands.

## Tooling

- JS/TS: **pnpm** (never npm/yarn). TypeScript strict. ESLint + Prettier. Tests with Vitest.
- Python: **uv** for envs and deps (never bare pip). Ruff for lint + format. Tests with pytest.
- Git + GitHub. Never commit secrets; use `.env` files (gitignored) and host env vars.

## Conventions

- **TDD for the model and data code.** Write the failing test first for scoring
  rules, downscaling and data parsers/ingest. Keep UI tests light
  (key flows and components with logic).
- **Rules are data.** Species rules (thresholds, windows, habitats) live in
  config with a cited `source` and a `confidence` per rule, not scattered
  through code. Every score must return its factor breakdown; the "why this
  score" UI depends on it.
- **The model runs server-side.** The frontend only displays precomputed scores
  from the API.
- **Score wording.** Scores are a 0–1 index, not a probability. UI and copy say
  "conditions score", never "probability" or "% chance".
- **No hardcoded UI strings.** Everything goes through i18n; Italian is the
  default locale and English must be kept complete.
- **Geo.** Grid math uses a projected CRS (EPSG:3035). API output and the map
  use WGS84, and MapLibre/GeoJSON coordinates are `[lon, lat]`. Metric units.
- **Time.** Dates are in `Europe/Rome`. Open-Meteo returns UTC unless asked:
  always pass `timezone=Europe/Rome` so daily totals are local days.
- **Data files.** Downloads, rasters and caches live under gitignored folders
  (`api/data/`) and are produced by reproducible scripts. Never commit them.
- **External APIs.** Cache responses, batch coordinates where the API allows
  (Open-Meteo does), respect rate limits, and credit every data source in the app.
- **Safety.** Never produce edibility or identification claims in the UI or
  copy. The app forecasts conditions only.
- **Sightings privacy.** Public sightings are only ever exposed as counts per
  cell: never coordinates, and never re-sharpen records the source obscured.
