---
order: 3072
title: Tune the rain drivers: both reach full credit in an ordinary September
status: To Do
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

- [ ] Read the backtest and tuning harness (`api/src/api/model/backtest.py`, `tuning.py`) and the
      current train-season baseline before changing anything
- [ ] Test the trigger ramp (`amount_mm` 10 to 30 mm) and the 30-day ramp (to 70 to 80 mm) with
      higher plateaus, on the train seasons, per species key
- [ ] Test them with and without `precipitation_scale` (x1.28 + 0.29/km), because the scale lowers
      the raw rain a threshold needs by 22 % at sea level to 43 % at 1.7 km
- [ ] Consider a relative 30-day driver (`percent_of_normal`, already written and disabled) once
      the per-cell climatology exists, so an ordinary month stops scoring as a good one
- [ ] Judge any change on the hold-out seasons (2024, 2025), and write the result into
      `model-v1-validation.md`
- [ ] If `precipitation_scale.enabled` changes, remove or reword `why.detail.rainNote` in
      `web/src/i18n/locales/{it,en}.json`, which states that the rain is adjusted upward
