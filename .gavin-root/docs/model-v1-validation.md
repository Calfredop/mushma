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

## What the "why this score" panel showed for the mid-September high scores

The panel now states the measurement behind each factor (card `verbose-score-explanation`). Read on
the 2026-09-19 run (rules version `1171b4eb48d2`), because many cells scored high with only one
modest rain event a few days back. All rain below is the model's, after the rain scale above.

- **How many are high.** Of the 10,777 woodland cells, 9,002 (84 %) score at least 0.5 and 6,090
  (57 %) at least 0.7; the median is 0.74. Of the 6,090, ovoli wins 3,778, *P. reticulatus* 1,147,
  *P. edulis* 506, gallinacci 370 and *P. aereus* 289.
- **`rain_trigger`.** One 3-day total of a median 40 mm (10th to 90th percentile 28 to 81 mm), which is
  27 mm (20 to 53) of reanalysis rain before the scale. It ended 8 to 10 days before the scored day
  for 94 % of the cells, 9 days for 74 %; the other 6 % are gallinacci, whose lag window is longer
  (29 to 30 days). Half the cells sit under 40 mm, close to the 30 mm where the rule already gives
  full credit, so the value is 1.00 almost everywhere.
- **`rain_30d`.** A median 104 mm (72 to 205) in the last 30 days, against full credit from 70 to
  80 mm. Region-wide the median is 102 mm.
- **`soil_moisture`.** Not measured: every rule file has it off (it needs the per-cell climatology
  v1 does not compute), so no key scores it.
- **Is it a wet month?** Not unusually. The region-mean reanalysis rain for 21 August to 19 September
  was 82 mm in 2026, against 30, 52, 70, 88, 50, 141 and 112 mm in 2019 to 2025 (the store holds
  2019 onward until the backfill reaches earlier years), so 2026 ranks fourth of eight.
- **Example.** Cell `1kmE4400N2259`, porcini group, score 0.86: 36.7 mm in 3 days up to 9 September
  (10 days before), 153 mm in 30 days, mean air temperature 22.5 °C over 20 days.

**Reading.** The scores follow the rules as written: nothing here is a bug. The scores are high
because both rain drivers reach full credit in an ordinary September: one event of about 30 mm ten
days earlier fills the trigger, and about 80 mm a month fills the 30-day driver, which so cannot tell
a good year from an average one. Whether that is too generous is a tuning question, and no threshold
changed with this card. The candidates to test on the train seasons are the trigger ramp (10 to
30 mm), the 30-day ramp (to 70 to 80 mm) and how they interact with the rain scale, which raises
the rain by 28 % at sea level to 77 % at 1.7 km. Filed as `tune-rain-drivers-saturate.md`.

<!-- RESULTS, TUNING, HOLD-OUT, TARGETS AND SANITY CHECK FOLLOW -->
