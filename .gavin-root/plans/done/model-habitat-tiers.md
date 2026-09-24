---
title: [model] Tipo di bosco: good woods at full credit, poor woods penalised
status: Done
priority: medium
complexity: moderate
---
Traces to PRD → Model (Factors, Score semantics, Principles: explainable).

## Why

The habitat factor is a gate: it multiplies the score and is capped at 1, so the best wood is ×1 and every other wood pulls the score down (`api/src/api/model/factors.py` `_habitat`, the woodland-weighted mean affinity). Each species' table is a smooth ranking with only one type at 1.0. For *B. edulis* that is beech 1.0, chestnut 0.9, fir 0.9, mixed broadleaf+conifer 0.8. A chestnut or fir cell therefore scores 10 % under an otherwise identical beech cell because beech tops the list, which in practice is a bonus for the top host.

The tables are "scaled from host rankings in Italian sources". A ranking says which trees are hosts. It gives no yield ratio between them, and it also reflects how common each forest is and where people pick. Decision (2026-09-24): **a good host is the baseline (×1). Only poor or unsuitable woods lower the score**, the same flat-top shape every other rule uses.

## Design

Four levels per species instead of a smooth scale, each with its cited source:

| level | value | meaning |
|---|---|---|
| host | 1.0 | a main host in the sources |
| secondary | ~0.6 | a documented host, clearly less typical |
| marginal | ~0.3 | occasional, or a mixed class where only some trees are hosts |
| non-host | 0–0.1 | not a host / not recorded |

- Mixed and transitional classes (`mixed_broadleaf`, `mixed_broadleaf_conifer`, `transitional_woodland_shrub`) stay below 1 **only** for dilution: only some of their trees are hosts. Say so in each note.
- Species groups take the max over their keys (porcini = 4 keys). Check the porcini group result per forest type, not only each key's.
- Rules are data: the levels change only the species YAMLs and the ecology docs. The engine is untouched unless the open question below is decided for a change.
- Habitat is in `backtest.frozen_factor_kinds` (derived partly from hold-out sightings). Set the levels from the literature, **not** by tuning on sightings. The backtest is only a before/after check.

## Open question: how a cell's forest types combine

Today the factor is the area-weighted mean affinity over the cell's woods, so non-host woods dilute a cell that has plenty of host wood. Measured on the Tuscan grid (2026-09-24): 25 % of woodland cells have no type covering 70 % of the woods. Among cells where ≥30 % of the woods (≈30 ha) is a top host, 28 % of *B. edulis* cells (955 of 3,419) still score habitat < 0.8. Ovoli: 1,661 of 6,913. Gallinacci: 680 of 2,371. A forager goes to the good part of the cell.

Option: score the host share with a saturation instead, e.g. full credit once about a third of the woods are hosts (the host-weighted share through a trapezoid). This needs an engine change (`_habitat` in `api/src/api/model/factors.py`), a schema field for the saturation, and TDD. Keep it apart from the level change, so the backtest before/after can tell the two effects apart.

## Steps

- [x] Decide the open question with the human: keep the area-weighted mean, or saturate on host share (and at what share) — **decided 2026-09-24: saturate.** `_habitat`'s existing `Σ fraction × affinity` *is* the host-weighted share; apply a `[0, 0.30, null, null]` trapezoid to it (full credit once ~30% of the woods are worth a host), same threshold for all 6 keys.
- [x] Draft the four-level table for each of the 6 keys (porcini_edulis, porcini_pinophilus, porcini_reticulatus, porcini_aereus, ovoli_caesarea, gallinacci_cibarius), with the source per level, from `.gavin-root/docs/species-ecology/*.md`. **Show it to the human and wait for approval before editing.** — approved 2026-09-24 as drafted (host/secondary/marginal/non-host per key; porcini-group max checked, no regressions).
- [x] Update `habitat.input.affinity` + `notes` in the 6 files under `api/src/api/config/species/`
- [x] Update the matching ecology rows: POR-H1..H4 (`porcini.md`), OVO-02 and the affinity table (`ovoli.md`), GAL-05 and the affinity section (`gallinacci.md`), plus the summary in `species-ecology.md`
- [x] Saturation: failing tests first in `tests/model`, then `_habitat` + the rule schema + `species/README.md`. Backtest it as a separate step from the levels.
- [x] `uv run pytest`: fix any test or fixture that pins the old affinities (`tests/model`, `tests/live`, `api/src/api/fixtures`) — all 770 tests pass with no changes needed; ruff check/format clean too
- [x] Backtest before/after on train + hold-out; add a short section to `.gavin-root/docs/model-v1-validation.md` (lift/AUC per species, habitat-only baseline too) — train only (hold-out is `--allow-holdout`-gated and this is a literature-derived prior, not a tuning decision to confirm on hold-out). Ovoli improved, gallinacci regressed on `auc_local` (traced to evergreen_oak → host), porcini eased slightly; adopted anyway since levels trace to sources, not sightings. Section: "Habitat tiers and saturation (2026-09-24)".
- [x] Web: the why panel's per-type fit ("faggeta 1,00, castagneto 0,90") still reads well with levels — four clean values (1.00/0.60/0.30/~0) read *more* cleanly than the old smooth scale, so numbers are kept rather than adding level-name i18n keys. The "why" fold is generic (`impact === 0` in `WhyBreakdown.tsx`, no habitat-specific code), so it already hides `habitat` whenever it's at full credit; confirmed live below.
- [x] Re-score and spot-check a chestnut and a fir cell for porcini on the map — re-ran the pipeline for 2026-09-20..27 and hit `/cells/{cell_id}` directly. Fir cell `1kmE4375N2338` (99.5% fir_spruce, Bar Alpino, 1453 m): porcini habitat 0.9 → **1.0**, and it's the winning key's affinity table (edulis) coming through end-to-end from the YAML. Chestnut cell `1kmE4305N2356` (100% chestnut, Castoglio): habitat 1.0 as before. Both now fold in the why panel; today's porcini score is weather-limited (`rain_30d` = 0), unrelated to this change.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
