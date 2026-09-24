---
kind: task
title: [foundation] API and daily job serve many regions
parent: feat-full-italy-coverage.md
complexity: complex
---
The API and the daily job serve every region that has stores on disk. Context:
`api/src/api/{routes,repository,models,main,cache}.py`, `api/src/api/live/repository.py`
(REGION hardcoded), `api/src/api/jobs/daily.py`, `api/src/api/history/build.py`
(REGION_NAMES), `api/src/api/fixtures/`, `api/openapi.json`. Decisions in the parent
plan `feat-full-italy-coverage.md`.

Contract first (schema and fixtures, so the web card can start against them):
- `region` query parameter on every data route (`/scores`, `/grid`, `/factors`,
  `/spot`, `/cells/{id}`, `/hotspots`, `/sightings`, `/comuni`, `/seasons`,
  `/season-map`, `/outlook`, `/species`, `/status`), default `tuscany`; an unknown or
  unserved region is a 404 with a problem body.
- `GET /regions`: the served regions (id, names, bbox, history start, species
  offered, `updated_at`), read from `config/regions/*.yaml` filtered by stores present.
- `GET /overview?species=&date=`: per served region, the share of woodland cells at
  or above `good_score` (history.yaml) and the mean score, plus `updated_at`; cached
  like `/scores`.
- `openapi.json` regenerated; fixtures gain a second fake region so tests route
  between two.

Then:
- A repository registry keyed by region id (one `LiveRepository` per region, lazily
  loaded); caches keyed by region; region names from the region YAML, not
  `REGION_NAMES`.
- `jobs/daily.py` runs each step for every served region in turn; one region's
  failure is logged and alerted but does not stop the others; the job logs the
  weighted Open-Meteo calls it used; one heartbeat as today.
- `/status` answers per region; rate limits and gzip unchanged.

Done when: pytest and ruff green; a local run with Tuscany plus the fixture region
answers every route for both; `uv run python -m api.jobs.daily` loops both; the
OpenAPI diff is summarised in the commit message.

## Done (2026-09-24)

Multi-region API shipped: `region` on every data route (default `tuscany`, unknown →
`application/problem+json` 404), `GET /regions` and `GET /overview`, fixture Umbria
alongside Tuscany, lazy per-region `LiveRepository` registry, daily job loops served
regions (one failure does not stop the others; logs weighted Open-Meteo calls; one
heartbeat). Region display names come from `config/regions/*.yaml`. pytest 833 and
ruff green; OpenAPI regenerated (`/regions`, `/overview`, `region` query on data routes).
