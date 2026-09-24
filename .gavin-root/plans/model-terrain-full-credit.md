---
title: [model] Slope and sun exposure: normal terrain at full credit
status: In Progress
priority: medium
complexity: simple
---
Traces to PRD → Model (Factors, Score semantics). Same principle as `model-habitat-tiers.md` (decided 2026-09-24): **terrain that is normal for the species is ×1. Only clearly unfavourable terrain lowers the score.** Today both terrain stoppers stop full credit below typical terrain, which in practice gives a bonus to flat or north-facing cells.

## Slope (all 6 species)

Every key has `slope`: `[null, null, 15, 35]`, floor 0.8 (×1 up to 15°, ×0.8 from 35°), on the cell's **mean** slope. Woodland cells on the Tuscan grid (2026-09-24):

| | p10 | p25 | median | p75 | p90 |
|---|---|---|---|---|---|
| slope (°) | 10.2 | 12.6 | 16.6 | 21.6 | 26.2 |

Above 800 m, 90–94 % of cells are steeper than 15°, so the rule trims nearly every mountain cell (53 % of all woodland cells, mean ×0.96). On 12–27 Sep 2026 it held back 73 % of the in-season cell-days for *B. edulis* and 77 % for *B. pinophilus*. The evidence is plot-scale (Mumcu Küçüker 2019: B. edulis best under ~11° on plots; Bonet 2008: falling with slope; two Spanish studies: no effect). A 1 km cell's mean slope is not the slope of the spot where the mushrooms grow.

Proposal: `[null, null, 25, 40]`, floor 0.8: full credit up to about the woodland p90, and only really steep cells lose. `slope` is a `static_band`, which is in `backtest.frozen_factor_kinds`, so set it from this reasoning and not by tuning. The backtest is only a before/after check.

Grid check after the change, run against the same `data/grid/tuscany/cells.parquet` (10,778 woodland cells) with the production `series.trapezoid` + `with_floor`: held back (score < 1) 59.2 % → 13.2 %, mean multiplier ×0.962 → ×0.994.

## Sun exposure (*B. edulis*, *B. pinophilus*, gallinacci)

The factor reads the day's sun ratio (the cell's clear-sky sun as a % of flat ground's; E and W slopes sit near 100 %). On 15 Oct: p10 89 %, p25 95 %, median 100 %, p75 105 %, p90 111 %.

| key | today | effect on flat / E / W ground |
|---|---|---|
| porcini_edulis, porcini_pinophilus (POR-A5, below ~1000 m) | `[null, null, 95, 120]`, floor 0.8 | flat 100 % → ×0.96; 65 % of cells held back on 15 Oct |
| gallinacci_cibarius (GAL-07, below ~600 m) | `[null, null, 90, 110]`, floor 0.85 | flat 100 % → ×0.925; 62 % held back |
| porcini_aereus, porcini_reticulatus, ovoli_caesarea | penalise only shady slopes | already right: flat = ×1 |

POR-A5 itself grades aspects (N ×1.0, E/W ×0.9, S ×0.8), which is a north bonus. GAL-07 penalises S/SW/W (×0.85). Proposal: flat, E and W ground at ×1, only clearly sunny slopes lose:
- edulis, pinophilus: `[null, null, 105, 125]`, floor 0.8
- gallinacci: `[null, null, 105, 120]`, floor 0.85

`sun_exposure` is a `window_aggregate` and not frozen, but it is folklore: set it from this reasoning, not by tuning.

Grid check after the change, 15 Oct 2026 sun ratio over the same 10,778 woodland cells, with the `where` elevation fade applied: edulis/pinophilus held back 69.8 % → 23.8 % (mean ×0.955 → ×0.989); gallinacci 66.5 % → 16.2 % (mean ×0.953 → ×0.995).

## Steps

- [x] Confirm the proposed trapezoids with the human (numbers above are a proposal)
- [x] Update `slope` in the 6 species YAMLs and `sun_exposure` in `porcini_edulis.yaml`, `porcini_pinophilus.yaml`, `gallinacci_cibarius.yaml`, rewriting each `notes` to state the principle (normal terrain ×1) and the grid distribution
- [x] Update the ecology docs: POR-A5 (`species-ecology/porcini.md`), GAL-07 (`species-ecology/gallinacci.md`), and the slope rows in `species-ecology.md` (lines ~105, 124, 146: "×1 to 15° → ×0.8 from 35°")
- [x] `uv run pytest`: fix any test or fixture that pins the old trapezoids (769 passed; no fixture pinned the old numbers)
- [x] Re-run the grid check: share of woodland cells held back by slope, and by sun exposure on 15 Oct, before/after
- [x] Backtest before/after on train + hold-out; note it in `.gavin-root/docs/model-v1-validation.md`

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
