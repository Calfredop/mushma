---
order: 5120
kind: task
title: [algo] more factor
status: Done
---
Let’s take in account in growth ratio for:
[ ] deceleration/aceleration factors: ideal temperatures, ideal relative humidity…
[ ] land slopeness
[ ] sun expsure and shadow

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->

## Design (agreed 2026-09-19)

- **Growth clock.** A per-species `growth` block gives each cell-day a pace = temperature pace
  (Yan & Hunt 1999 cardinal curve on 0–7 cm soil temperature, 1 at a reference) × humidity pace
  (daily max VPD; 1 in humid air, down to a floor in dry air). `rain_event` counts its lag in growth
  days (Σ pace since the rain ended): warm and humid brings the flush sooner, cold or dry later.
  Pace ≡ 1 reproduces today's model. Humidity uses VPD, already ingested (no re-download).
- **Terrain microclimate** (`model.yaml`, every species). A daily sun ratio per cell (clear-sky
  sun on the cell's mean surface vs flat ground, with a monthly diffuse-sky share) shifts air and
  soil temperature and scales ET0 before the rules read them.
- **Per-species lines.** `sun_exposure` (the research's aspect preferences, on the sun ratio, with
  a generic `where` altitude condition) and `slope` (a soft penalty on steep cells). Slope acts only
  through its line, never also on the rain, so the same water is not counted twice.
- **Enable, and backtest the train seasons** before and after; no tuning, no hold-out.
- Not in: ridge cast shadows (DEM horizon pass), relative humidity ingest, canopy shade.

## Checklist

- [x] References for every new rule in `references.yaml` (literature check of 2026-09-19)
- [x] Sun ratio maths (`api.model.terrain`), test first
- [x] Microclimate config in `model.yaml` and applied in `load_weather`; `sun_exposure_pct` series
- [x] Rule schema: species `growth` block, `where` condition, terrain series; loader checks, test first
- [x] Engine: growth-day lags in `rain_event`, `where` in factors, lookback; `growth_days` in the breakdown
- [x] Store `<factor>__growth_days`; API breakdown, `openapi.json`, web `schema.ts`
- [x] Rule files: growth, sun_exposure and slope for the six keys; retire the known gaps they fill
- [x] Web "why" panel copy (it + en): growth days, sun exposure, slope, `where`, microclimate note
- [x] Docs: species README, `species-ecology.md`, PRD Model factors
- [x] Train-season backtest before and after, written into `model-v1-validation.md`
- [x] Full checks (pytest, ruff, vitest, eslint, prettier, build), then commit
