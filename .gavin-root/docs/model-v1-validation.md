# Model v1 validation: do sightings fall on high-scoring cell-days?

Card: M3 · Model v1. Traces to PRD → Model (Validation, Score semantics, Known data traps), Principles
(Explainable, Honest uncertainty) and Milestone 3.

<!-- RESULTS: filled in once the train seasons are backfilled -->

## What was tested

The rules in `api/src/api/config/species/` score every woodland cell and day from 0 to 1. The backtest
asks one question: **is a public sighting's cell-day scored higher than the cell-days it could have
been instead?** Sightings are presence-only: they say where and when someone found the species, never
where it was absent. Every sighting is therefore ranked against a **background** of alternatives, and
the result is an AUC: the chance the sighting outscores a background cell-day (ties count half).
0.5 is chance; 1 means the sighting beat every alternative.

Code: `api.model.backtest` (scoring, backgrounds, summaries), `api.model.metrics`, `api.model.effort`,
`api.model.tuning`. Commands:

```sh
cd api
uv run python -m api.model.backtest run --seasons train --label priors
uv run python -m api.model.tuning --label tuned
uv run python -m api.model.backtest run --seasons holdout --label tuned-holdout --allow-holdout
```

## Data

- **Scores.** Every woodland cell (10,778) and day of each season, from the downscaled Open-Meteo
  `era5_seamless` reanalysis (`weather-ingest.md`), with rain scaled by cell height (below).
- **Sightings.** The GBIF + iNaturalist store (`sightings-profile.md`) after two fixes made for this
  card: 28 soil-DNA `MATERIAL_SAMPLE` records removed, and gallinacci widened to the *Cantharellus*
  genus. A presence is a unique (species, cell, day) record that is not flagged obscured (a
  village-square pin): several photos from one outing count once.
- **Observer effort.** Fungi of any kind recorded on iNaturalist in Tuscany each day
  (`observations/histogram`, verifiable, place 13073), used to weight background days.

## Train and hold-out seasons

Fixed in `config/model.yaml` and the PRD **before any score was compared with a sighting**, looking
only at how many sightings each year holds:

| role | seasons | why |
|---|---|---|
| train | 2016–2023 | tune on the past; 2019–2023 hold nearly all the older sightings |
| hold-out | 2024, 2025 | the two most recent complete seasons: the way the app is used, past seasons teach and the next one tests |
| live | 2026 | still in season; reported once it ends, never used for tuning |

Season windows, altitude bands and habitat affinities are **frozen**: the species research derived them
partly from sightings of every year, hold-out included, so tuning them would leak. For the same reason
the season and altitude gates are not independent of the hold-out sightings; the same-cell timing
metrics below are the ones they cannot flatter.

## Backgrounds: correcting for how sightings are collected

Sightings cluster where people live and walk, on weekends, and in October, whatever the conditions.
Each background removes part of that:

| metric | a sighting is ranked against | removes |
|---|---|---|
| `auc_region` | every woodland cell-day of the season | nothing: season and habitat alone win it. Reported only for contrast. |
| `auc_day` | every other woodland cell on the same day | when people went out |
| `auc_local` | other woodland cells within 20 km on the same day | when, and where people live and walk: only places the finder could as easily have visited |
| `auc_time` | the same cell on the other days within ±30 days | where: tests timing alone |
| `auc_time_effort` | the same, each day weighted by that day's fungi observations + 1 | where, and the weekly and seasonal rhythm of outings |

**Lift** (from the same-day and local percentiles): how over-represented sightings are among the top
10 % or 20 % of their day's cells; 1 is chance.

Per-sighting AUCs are averaged over sightings (an AUC stratified by sighting), with 90 % bootstrap
intervals over sightings.

## Baselines

Built from the same rule files, per species group, max over its keys like the model:

| baseline | what it keeps |
|---|---|
| `habitat` | habitat affinity alone (the PRD's baseline) |
| `static` | habitat × altitude |
| `calendar` | every gate: season × habitat × altitude. The rules with the weather taken out. |

`habitat` and `static` do not change from day to day, so their `auc_time` is 0.5 by construction.
**The weather rules earn their place only if the model beats `calendar`** on the local and time
backgrounds.

## Null check

Before any real sighting was scored, the harness was run with random sightings:

- **Unit test.** 400 random cell-days on random scores give 0.50 ± 0.04 on every background.
- **Real 2025 scores, 300 random autumn cell-days** (uniform over woodland cells, 1 September to
  29 November). The random points know nothing, yet `auc_region` gives the model 0.77 and the calendar
  baseline 0.72, because autumn is in season. `auc_time` gives 0.57 and 0.55, because the ±30-day
  window reaches into late summer. The corrected backgrounds sit at chance: `auc_day` 0.49,
  `auc_local` 0.48, `auc_time_effort` 0.51.

That is why the results below lead with `auc_local` and `auc_time_effort`, and why the tuning
objective is their mean.

## Rain scale

The reanalysis rain is too dry in the hills against the SIR Toscana gauges (`weather-ingest.md`). The
rules' rain thresholds come from gauge-based studies, so before scoring, reanalysis rain is multiplied
by `1.28 + 0.29 × elevation (km)`: a least-squares fit of gauge totals on model totals over the 133
woodland gauges of 2025. On the 145 gauges of 2026 it moves the pooled model/gauge ratio from 0.68 to
0.99 (0.96–1.03 in each elevation band). It corrects totals, not timing. Tuning tests scoring with and
without it.

<!-- RESULTS, TUNING, HOLD-OUT, TARGETS AND SANITY CHECK FOLLOW -->
