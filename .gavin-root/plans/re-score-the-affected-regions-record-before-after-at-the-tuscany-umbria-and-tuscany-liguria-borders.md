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
