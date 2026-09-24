---
title: [fix] Season gate halves at the altitude where two windows hand over
status: In Progress
priority: high
complexity: simple
---
Traces to PRD → Model (Factors, Score semantics). Related: `model-habitat-tiers.md` (same principle: good conditions are ×1, only poor ones lower the score).

## Bug

Two species have a lowland and a mountain season window, with `elevation_weight` trapezoids that hand over from one to the other: gallinacci (600→1000 m) and porcini *aereus* (400→600 m). `_season` in `api/src/api/model/factors.py` multiplies each window by its weight and takes the **max**. In the middle of the handover each weight is 0.5, so even when both windows say "in season" the gate is 0.5.

Measured on the Tuscan grid (2026-09-24), the best value over the whole year:

| species | band | peak season gate | cells |
|---|---|---|---|
| gallinacci | 600–700 m | 0.88 (min 0.75) | 946 |
| gallinacci | 700–900 m | 0.50–0.63 | 1,465 |
| gallinacci | 900–1000 m | 0.87 | 499 |
| aereus | 400–600 m | 0.74–0.76 (min 0.50) | 2,779 |

24 % of woodland cells never reach 0.95 for gallinacci, and 23 % for aereus. The gallinacci note says "the appendix blends the two windows linearly across 600–1000 m; this schema takes the max of the weighted windows, which is close". It is not close: the linear blend gives 1 wherever both windows are in season.

## Fix

Blend the elevation-weighted windows: **Σ weight × window** over the windows that have an `elevation_weight`, then the max with any unweighted windows. This is the design the ecology appendices describe, so it is a fix, not a retune of a frozen rule (`season_window` is in `backtest.frozen_factor_kinds`).

- The loader (`api/src/api/model/rules.py`) should reject a season factor whose elevation weights do not sum to 1 at every elevation, since a blend only makes sense then. Check with the shipped files: gallinacci `[null,null,600,1000]` + `[600,1000,null,null]` and aereus `[null,null,400,600]` + `[400,600,null,null]` both sum to 1.

## Steps

- [x] Failing test first: `tests/model/test_factors.py::test_elevation_weights_hand_over_between_windows` pins the bug (`value[:, august] == [1, 0.5, 1]`). Change it to expect `[1, 1, 1]` (both windows in season at 500 m). Add a case where only one window is in season at the midpoint (→ 0.5). Add a loader test rejecting weights that do not sum to 1.
- [x] Implement the blend in `_season`, plus the loader check
- [x] Update the `season_window` row in `api/src/api/config/species/README.md` ("max over windows of date membership × elevation…") and the gallinacci `season` note ("which is close")
- [x] `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`
- [x] Re-run the grid check (peak season by elevation band for gallinacci and aereus → 1.00 everywhere in season)
- [ ] Backtest before/after for gallinacci and the porcini group; note the result in `.gavin-root/docs/model-v1-validation.md`
  - Blocked in this session: `api/data/grid`, `api/data/weather` and `api/data/sightings` are all
    empty in this checkout (that store lives on the machine that seeds the Hetzner server, per the
    root README's deploy section). `uv run python -m api.model.backtest` needs all three. In place
    of it, re-ran the elevation-band grid check with the real gallinacci/aereus rules over a full
    year at every elevation from 300–1100 m (synthetic cells, since no real grid was available):
    every band now peaks at 1.0000 (see the commit). Run the real backtest on a machine with the
    data stores and log train/holdout `auc_local`/`auc_time_effort` before vs. after for gallinacci
    and porcini in `model-v1-validation.md`, then tick this box.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
