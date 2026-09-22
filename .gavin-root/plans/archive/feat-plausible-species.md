---
order: 3072
kind: task
title: [feat] plausible species
status: Done
---
When selecting a zone, add a plausible species breakdown in the sidebar’s stats

## Plan

Agreed with the human (2026-09-19): show **both** measures, and break each species group down
per taxon (the four porcini keys, not only "porcini").

- **Habitat fit**: per taxon and group, the share of the zone's woodland whose forest type ×
  altitude (the rules' static gates, weather aside: the backtest's `static` baseline) reach a
  plausible level. Standing profile of the zone, shown under the Zona picker (Seasons, Outlook).
- **Good days per species**: for the chosen season, each group's and taxon's good days in the
  zone, inside the season's stats.

- [x] history config: the plausible-fit threshold, with its rationale
- [x] `api.history.plausible`: static fit per cell and taxon, share per area (TDD)
- [x] per-area season good days for the taxon keys (TDD)
- [x] history build writes `area_fit.parquet` and `taxon_seasons/`; store readers
- [x] `GET /species` (models, repository protocol, live + fixture, tests, openapi.json)
- [x] web: schema, query hook, plausible-species block under the Zona picker, per-species good days in the season stats, it/en strings, tests
- [x] docs: time-views.md and README endpoint list
- [x] rebuild local history, check real numbers and the UI in the browser
- [x] lint, format, tests; commit

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
