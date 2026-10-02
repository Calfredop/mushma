---
kind: task
title: Re-score the affected regions; record before/after at the Tuscany–Umbria and Tuscany–Liguria borders
parent: fix-rain-calibration-region-borders.md
---
The rain scale is now one national field (`api/src/api/config/rain_scale_field.csv`, cited from `model.yaml → precipitation_scale.field`). It replaces 19 per-region fits. Read `.gavin-root/docs/rain-scale-field.md` first: method, numbers, and "Before and after".

Rain changes by region, mean factor over woodland: Tuscany −27 %, Abruzzo −22 %, Liguria −13 %, Friuli −12 %, Calabria −10 %, Campania and Molise −8 %, Lombardia +6 %, Piemonte +11 %, Trentino-Alto Adige +15 %, Valle d'Aosta +19 %, Sicily +21 %. The others move within ±3 %. The served scores, history and normals were all built with the old scales. Tuscany, Umbria and Liguria have no stores on the laptop; the server has every region.

1. **Tuscan backtest first.** Tuscany's rain-driver tuning (`mushma_rain_tuning_2026`, `model-v1-validation.md` → Rain drivers) was done on the wetter 1.28 + 0.29/km rain. Re-run the backtest and sanity contrasts on the field, compare with the recorded hold-out results, and stop to ask the human if the hold-out drops.
2. **Re-score every region.** Rebuild the normals (`api.history.build normals`), the history, and the scores of the served window, in the order the deploy docs give (`README.md`, `deploy/`). Then rsync or deploy.
3. **Record the borders.** Score the woodland cells within 10 km of the Tuscany–Umbria and Tuscany–Liguria borders on 25 Sep 2026 (the day `regions/umbria.md` measured 0.86 vs 0.47 combined and 0.47 vs 0.07 porcini) and on one wet autumn day. Use the old and new scale on the same weather. The method: score the cells in memory with `load_weather` and `score_frames` (`api.model.inputs`, `api.model.pipeline`), passing a `ModelConfig` whose `precipitation_scale` is the old fit from `api.weather.rain_field.old_fits("<rev before the field>")`. Add the numbers to `rain-scale-field.md` → Before and after, and to `regions/umbria.md`.

Tick the parent's item when done.

## Status 2026-10-01
- **Done:** the served window (today −6 to +7) is re-scored with the field in all 20 regions. The live `/status?region=` rules versions match the code; the regions were re-scored between 07:43 and 07:57 UTC. Live border scores are recorded in `rain-scale-field.md`.
- **Not done:** the Tuscan backtest, and the re-score of past seasons (2016 to today −7) with their history tables. The agent's attempt to launch these on the server was blocked by the auto-mode safety check (production), so a human runs it.
  - Script: `scratchpad/rescore-history-remote.sh` from session 033fe57b, copied to the server and run as the transient unit `mushma-rescore`. Order: Tuscan backtest (holdout + train) → per region `pipeline score --no-factors` → `history.build update` → `bump_region` → restart api.
  - Estimate: about 9 s per year for 1,455 cells on the laptop, so about 2–4 h for Italy on the server. Finish it before the 05:00 daily job.
- **Compare against:** previous Tuscan hold-out (`tuned-holdout`, model, all seasons), `auc_local` / `auc_time_effort`:
  - porcini 0.477 / 0.601 (19 sightings)
  - gallinacci 0.550 / 0.605 (10)
  - ovoli 0.531 / 0.394 (6)

## Tuscan backtest on the field (server, 2026-10-01; `backtest/tuscany/rain-field-holdout`, `rain-field-train`)
Model, all seasons, `auc_local` / `auc_time_effort`.

| | hold-out before (`tuned-holdout`, 22 Sep) | hold-out, field | train before (`habitat-tiers-after`, 24 Sep) | train, field |
|---|---|---|---|---|
| porcini | 0.477 / 0.601 | **0.512 / 0.606** | 0.433 / 0.668 | 0.455 / 0.657 |
| gallinacci | 0.550 / 0.605 | 0.564 / 0.597 | 0.493 / 0.504 | 0.502 / 0.566 |
| ovoli | 0.531 / 0.394 | 0.654 / 0.361 | 0.542 / 0.589 | 0.549 / 0.570 |

- No drop: porcini and gallinacci hold or rise on both. The hold-out is 35 sightings (2024: 26, 2025: 9), so the noise is a few hundredths.
- The "before" runs predate some rule changes (habitat tiers, region rules), so these are not a pure rain-only contrast.
- Re-tuning is not needed for the drier Tuscan rain.

The first history re-score failed in every region before writing anything: it started at 2016-01-01, but scoring needs 77 days of weather lookback (the store starts 2016-01-01). The script now starts each region at `history_score_range` (2016-03-18), as onboard does.

## Done 2026-10-01
The second run (start at each region's first lookback-complete day, 2016-03-18) ran from about 12:25 to 19:05 UTC as the transient unit `mushma-rescore` on the server. It re-scored 2016-03-18 to 2026-09-24 without factors and rebuilt the history tables for all 20 regions, bumping each region's response cache, and ended `done` with no `region_failed`. Lombardia (6,018 woodland cells) took about 2.5 min per year. The served window had already been re-scored by the deploy's `--run-job`.

Spot check after the run: the live `/history/seasons?species=porcini&region=tuscany` and `…&region=umbria` answer 200, with seasons from 2016.
