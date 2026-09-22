---
order: 3072
title: Tune the rain drivers: both reach full credit in an ordinary September
status: Done
priority: medium
complexity: complex
---
## Why

The "why this score" panel (card `verbose-score-explanation`) shows that on 2026-09-19, 57 % of the
woodland cells score at least 0.7. Both rain drivers are at full credit there: `rain_trigger` from
one ~30 mm, 3-day event about 10 days earlier, and `rain_30d` from ~70 to 80 mm a month. The month
was not unusually wet (region-mean raw rain 82 mm for 21 Aug to 19 Sep, fourth of eight seasons from
2019), so the drivers saturate in an ordinary September and cannot tell a good year from an average
one. The evidence and numbers are in `.gavin-root/docs/model-v1-validation.md`, section "What the
'why this score' panel showed for the mid-September high scores".

This card is the **tuning** that card deliberately did not do. It follows the backtest protocol in
`model-v1-validation.md`: tune on the train seasons only, judge on the hold-out, and keep season
windows, altitude bands and habitat affinities frozen.

## Checklist

- [x] Read the backtest and tuning harness (`api/src/api/model/backtest.py`, `tuning.py`) and the
      current train-season baseline before changing anything
- [x] Test the trigger ramp (`amount_mm` 10 to 30 mm) and the 30-day ramp (to 70 to 80 mm) with
      higher plateaus, on the train seasons, per species key
- [x] Test them with and without `precipitation_scale` (x1.28 + 0.29/km), because the scale lowers
      the raw rain a threshold needs by 22 % at sea level to 43 % at 1.7 km
- [x] Consider a relative 30-day driver (`percent_of_normal`, already written and disabled) once
      the per-cell climatology exists, so an ordinary month stops scoring as a good one
- [x] Test the growth clock's temperatures and the gallinacci shade rule (GAL-07, applied all year
      though its source limits it to June–September), which cost gallinacci some `auc_local` in the
      comparison of card `algo-more-factor` (`model-v1-validation.md`)
- [x] Judge any change on the hold-out seasons (2024, 2025), and write the result into
      `model-v1-validation.md`
- [x] If `precipitation_scale.enabled` changes, remove or reword `why.detail.rainNote` in
      `web/src/i18n/locales/{it,en}.json`, which states that the rain is adjusted upward

## Result (2026-09-22)

Full write-up: `model-v1-validation.md`, section "Rain drivers: tuning on the train seasons, judged
on the hold-out".

- New engine aggregate `percent_of_normal` (rain only): the window's rain as a share of the cell's
  daily normals, downscaled and rain-scaled like the rain. Tuning search `--search rain` in
  `api.model.tuning`, run with the rain scale on and off.
- **Adopted:** porcini `rain_30d` (all four keys) is now relative to the cell's normal, 0 at 50 %
  and full from 125 %. Train +0.03 under both scalings, hold-out 0.526 → 0.539. On 2026-09-19 the
  porcini `rain_30d` is at full credit in 18 % of cells instead of 77 %.
- **Not adopted:** ovoli trigger 20→60 mm (train +0.03, but hold-out 0.507 → 0.463 on 6
  sightings). Gallinacci, the growth clock and the GAL-07 shade line: nothing cleared the margin.
- The rain scale stays on (0.012 short of the margin), so `why.detail.rainNote` is unchanged. The
  "why" panel and the API contract learned the new aggregate (`%`, it/en copy).
- Scoring now needs `climatology/<region>/normals.parquet` and refuses to start without it
  (`api.history.build normals`). The daily job relies on it already being on the Fly volume.

