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

## Growth clock and terrain factors: train-season comparison (2026-09-19)

Card `algo-more-factor` added three things to every species key. Every number in them is a derived
prior; no threshold was tuned against a sighting:

- **Growth clock.** Each cell-day gets a growth pace: Yan & Hunt's cardinal-temperature curve on
  0–7 cm soil temperature, 1 at the weather the lag windows were drawn from (15 °C for the autumn
  taxa, 17–18 °C for the summer ones), times a humidity pace that halves at high daily maximum VPD
  (2.0 kPa for the autumn taxa, 3.0 kPa for the summer ones). `rain_trigger` counts its lag in growth
  days, the sum of the paces since the rain ended, instead of calendar days.
- **Terrain microclimate** (`config/model.yaml`). Each cell's temperatures and ET0 are shifted by its
  sun ratio, the clear-sky sun on its mean surface over flat ground's (`api.model.terrain`). In
  mid-October 90 % of woodland cells get 84–114 % of flat ground's sun, so ±0.6 °C of mean air
  temperature.
- **`sun_exposure` and `slope` stoppers.** Sun exposure carries the research's aspect preferences
  (POR-A5, POR-A6, OVO-04, GAL-07), with floors of 0.8–0.9. Slope is ×1 up to 15° and ×0.8 from 35°.

**How it was compared.** The train seasons that hold stored sightings (2019–2023; 2016–2018 hold
none) were scored before (rules version `1171b4eb48d2`) and after (`9db6ca599f80`) on the backend
worktree's weather of 2026-09-19. 2018 was still being backfilled, which leaves only the lookback of
early 2019 incomplete. That gives 55 presences: porcini 23, ovoli 16, gallinacci 16. Three ablations
separate the parts. The hold-out seasons were not scored.

**Objective** (mean of the pooled `auc_local` and `auc_time_effort`, the tuning objective):

| rules | porcini | ovoli | gallinacci |
|---|---|---|---|
| before | 0.535 | 0.504 | 0.614 |
| growth clock only | 0.545 | 0.514 | 0.613 |
| sun-exposure and slope lines only | 0.540 | 0.504 | 0.596 |
| terrain (microclimate and lines, no clock) | 0.542 | 0.495 | 0.602 |
| all three (shipped) | **0.558** | 0.509 | 0.600 |

**The two metrics, before → after, with 90 % bootstrap intervals:**

| group | `auc_local` | `auc_time_effort` |
|---|---|---|
| porcini | 0.509 (0.43–0.59) → 0.498 (0.41–0.59) | 0.561 (0.46–0.66) → 0.617 (0.53–0.70) |
| ovoli | 0.439 (0.36–0.53) → 0.428 (0.36–0.51) | 0.569 (0.50–0.63) → 0.589 (0.52–0.66) |
| gallinacci | 0.707 (0.61–0.79) → 0.684 (0.58–0.78) | 0.520 (0.45–0.59) → 0.517 (0.42–0.62) |

The calendar baseline (the gates alone, unchanged by this card) scores `auc_time_effort` 0.522
(porcini), 0.537 (ovoli) and 0.479 (gallinacci).

**Reading.**

- **The growth clock helps timing.** On its own it moves porcini's effort-weighted timing AUC from
  0.561 to 0.595, and ovoli's from 0.569 to 0.589. With the microclimate and the new lines on as
  well, porcini reaches 0.617, the first porcini interval that clears 0.5. Gallinacci's
  timing does not move: its lag window is already 4 to 50 days wide.
- **The terrain lines do not help same-day ranking yet.** Sunny and shady slopes sit side by side
  within 20 km, so `auc_local` is where they should show. Porcini and ovoli stay at chance there, as
  before. Gallinacci loses 0.02–0.03 of `auc_local` (0.707 → 0.677 with the lines alone). The first
  suspect is its shade preference below 600 m (GAL-07), which the source limits to June–September
  and the engine applies all year.
- **None of the differences is outside the bootstrap intervals.** At 16–23 presences per group this
  is a direction to follow, not a result. The changes stay on as priors. The tuning card
  (`tune-rain-drivers-saturate.md`) should test the gallinacci sun line and the clock's
  temperatures on the train seasons, like every other threshold.
- **Cost.** Scoring a season takes about three times as long: 40–75 calendar lags per rain event
  instead of about 18. The daily run scores 14 days, so it adds seconds.

## Rain drivers: tuning on the train seasons, judged on the hold-out (2026-09-22)

Card `tune-rain-drivers-saturate`. The panel reading above showed both rain drivers at full credit in
an ordinary September. This is the tuning that reading left open, done by the protocol: tuned on the
train seasons only, judged once on the hold-out, with season windows, altitude bands and habitat
affinities frozen.

**Search** (`api.model.tuning --search rain`, written into the code before any train season was
scored with these rules). One pass of coordinate descent per group, each alternative kept only if it
raises the group's train objective by at least 0.02 (`MARGIN`):

| choice | prior | alternatives |
|---|---|---|
| `rain_trigger` amount | porcini, ovoli 10→30 mm; gallinacci 10→20 mm | ×1.5 (`higher`), ×2 (`much_higher`) |
| `rain_30d` | porcini 20→80, ovoli 25→75, gallinacci 15→70 mm | ×1.5, ×2, and `relative`: the 30 days as a percentage of the cell's own normal, 0 at 50 %, full from 125 % |
| growth-clock temperatures | the rule files | cardinal curve and reference 3 °C cooler, or warmer |
| gallinacci `sun_exposure` (GAL-07) | on all year | off |

The whole search ran twice, with the rain scale on (as configured) and off, because the scale lowers
the raw rain a millimetre threshold needs by 22 % at sea level to 43 % at 1.7 km.

**The relative driver** is new engine code: `percent_of_normal` reads the daily rain normals per
weather point (`api.history.build normals`: the mean of each calendar day over the complete
reanalysis years 2016–2025, smoothed over 31 days), downscaled to the cell with the rain's own
weights and multiplied by the same rain scale, so the percentage does not depend on the scale. The
normals use every baseline year's weather, hold-out included. That is weather, not sightings, so it
leaks nothing about where the fungi were found.

**Train objective per trial** (mean of the pooled `auc_local` and `auc_time_effort`; 55 presences:
porcini 23, ovoli 16, gallinacci 16):

| trial | scale on | scale off |
|---|---|---|
| start (prior rules) | porcini 0.558, ovoli 0.509, gallinacci 0.600 | 0.563, 0.507, 0.627 |
| porcini trigger ×1.5 / ×2 | 0.574 / 0.555 | 0.554 / 0.549 |
| porcini `rain_30d` ×1.5 / ×2 / **relative** | 0.561 / 0.571 / **0.587** (kept) | 0.571 / 0.591 / **0.594** (kept) |
| porcini clock cooler / warmer | 0.550 / 0.585 | 0.566 / 0.599 |
| ovoli trigger ×1.5 / **×2** | 0.531 / **0.540** (kept) | 0.530 / **0.543** (kept) |
| ovoli `rain_30d` ×1.5 / ×2 / relative | 0.533 / 0.538 / 0.525 | 0.544 / 0.526 / 0.535 |
| ovoli clock cooler / warmer | 0.511 / 0.544 | 0.491 / 0.543 |
| gallinacci trigger ×1.5 / ×2 | 0.608 / 0.608 | 0.627 / 0.636 |
| gallinacci `rain_30d` ×1.5 / ×2 / relative | 0.593 / 0.604 / 0.610 | 0.621 / 0.620 / 0.612 |
| gallinacci clock cooler / warmer | 0.604 / 0.596 | 0.625 / 0.618 |
| gallinacci sun line off | 0.604 | 0.625 |

Both runs kept the same two changes and nothing else. With them, the scale-off run ends at a mean of
0.588 over the three groups and the scale-on run at 0.576: 0.012 apart, under the margin, so **the
rain scale stays on**. It is fitted to gauges, not to sightings, and the tuning gives no reason to
drop it; `why.detail.rainNote` stays as written.

**Hold-out** (2024, 2025: porcini 19, ovoli 6, gallinacci 10 presences), scored once with the prior
rules and once with the two train winners:

| group | objective prior → tuned | `auc_local` | `auc_time_effort` |
|---|---|---|---|
| porcini (relative `rain_30d`) | 0.526 → **0.539** | 0.476 → 0.477 | 0.576 (0.49–0.66) → 0.601 (0.51–0.69) |
| ovoli (trigger 20→60 mm) | 0.507 → **0.463** | 0.523 → 0.531 | 0.490 (0.33–0.65) → 0.394 (0.24–0.57) |
| gallinacci (unchanged) | 0.578 → 0.578 | 0.550 | 0.605 |

**Decision.**

- **Porcini: adopted.** The 30-day rain of all four porcini keys is now scored against the cell's
  own normal (the factor notes record the tuning, and cite `mushma_rain_tuning_2026`). It won under both rain scalings, and
  it held its direction on the hold-out (+0.013), mostly in timing (`auc_time_effort` +0.025, on top
  of the growth clock's gain).
- **Ovoli: not adopted.** The doubled trigger ramp cleared the train margin under both scalings but
  lost 0.044 on the hold-out, all of it in timing. Six presences is too few to call that a
  reversal, but a change the hold-out does not confirm is not shipped. The ramp stays at 10→30 mm.
  Choosing between the two with the hold-out uses it once more than the protocol intends; reverting
  to the prior is the conservative side of that choice.
- **Gallinacci and the growth clock: nothing changes.** No alternative cleared the margin, the
  shade line (GAL-07) included: turning it off gave −0.002 to +0.004, so its all-year application
  is not what cost gallinacci its `auc_local`.

**What it does to the saturated day.** Re-scoring 2026-09-19 (the weather stored on 2026-09-22) with
the prior and the adopted rules: the porcini `rain_30d` input has a median of 97 % of normal, an
ordinary month, and the share of woodland cells where it gives full credit falls from 77 % to 18 %
(median value 1.00 → 0.62). Porcini cells scoring at least 0.7 fall from 34 % to 18 % (median
0.63 → 0.54). The combined score moves less (at least 0.7: 48 % → 43 %), because ovoli wins most of
the high cells and its rain lines are unchanged; its trigger and 30-day ramps still fill in an
ordinary September, and whether that is too generous has to wait for more ovoli sightings.

**Still open.** With the prior rules, the habitat baseline beats the model on `auc_local` in every
group on the train seasons (porcini 0.561 vs 0.498, ovoli 0.470 vs 0.428, gallinacci 0.759 vs 0.684): within 20 km on a
given day, the weather and terrain lines rank the finder's cell below where habitat alone would.
The rain drivers were not the cause; that is for a later card.

## Slope and sun exposure at full credit for normal terrain (2026-09-24)

Card `model-terrain-full-credit`. `slope` (all 6 keys) moved from `[null, null, 15, 35]` to
`[null, null, 25, 40]`, floor 0.8; `sun_exposure` for *B. edulis*/*B. pinophilus* (POR-A5) from
`[null, null, 95, 120]` to `[null, null, 105, 125]`, floor 0.8; gallinacci (GAL-07) from
`[null, null, 90, 110]` to `[null, null, 105, 120]`, floor 0.85. Both stoppers previously stopped
full credit below what is typical Tuscan woodland terrain (median slope 16.6°, median sun ratio
100 % of flat ground's on 15 Oct), which in practice penalised ordinary flat and north-facing
cells relative to steep or shaded ones. The new trapezoids give full credit to about the woodland
p90 and only reduce clearly steep or clearly sunny cells. Neither factor was tuned: `slope` is a
`static_band`, frozen by `backtest.frozen_factor_kinds`; `sun_exposure` is folklore, set from the
grid distribution and the cited sources, not by search.

**Grid check** (`data/grid/tuscany/cells.parquet`, 10,778 woodland cells, production
`series.trapezoid` + `with_floor`): slope held back (score < 1) 59.2 % → 13.2 % of cells, mean
×0.962 → ×0.994. Sun ratio on 15 Oct, with the `where` elevation fade applied: edulis/pinophilus
held back 69.8 % → 23.8 % (mean ×0.955 → ×0.989); gallinacci 66.5 % → 16.2 % (mean ×0.953 →
×0.995).

**How it was compared.** A second session was live-editing the same 6 species YAMLs in this
checkout at the same time (a separate habitat-tiers card), so scoring the working tree directly
would have mixed the two changes. Instead the rules were built in isolation: the species YAMLs at
the last commit (`2b340f0`, before either session's edits) with only this card's `slope` and
`sun_exposure` trapezoids reapplied on top, loaded via `load_rules(species_dir=...)`, scored
against the same real cells/weather/sightings stores. Train (2016–2023, 55 presences: porcini 23,
ovoli 16, gallinacci 16) and hold-out (2024–2025: porcini 19, ovoli 6, gallinacci 10), both scored
once, before and after.

**Objective** (mean of the pooled `auc_local` and `auc_time_effort`):

| | porcini train | ovoli train | gallinacci train | porcini holdout | ovoli holdout | gallinacci holdout |
|---|---|---|---|---|---|---|
| before | 0.583 | 0.509 | 0.599 | 0.542 | 0.507 | 0.568 |
| after | 0.581 | 0.515 | 0.602 | 0.532 | 0.497 | 0.575 |

**The two metrics, before → after, with 90 % bootstrap intervals:**

| group | role | `auc_local` | `auc_time_effort` |
|---|---|---|---|
| porcini | train | 0.499 (0.41–0.59) → 0.500 (0.41–0.59) | 0.668 (0.57–0.75) → 0.662 (0.57–0.75) |
| ovoli | train | 0.428 (0.36–0.51) → 0.441 (0.36–0.53) | 0.589 (0.52–0.66) → 0.589 (0.52–0.66) |
| gallinacci | train | 0.680 (0.57–0.78) → 0.701 (0.60–0.79) | 0.517 (0.42–0.62) → 0.504 (0.43–0.58) |
| porcini | holdout | 0.480 (0.38–0.57) → 0.461 (0.36–0.56) | 0.604 (0.51–0.69) → 0.604 (0.51–0.69) |
| ovoli | holdout | 0.523 (0.37–0.68) → 0.504 (0.34–0.67) | 0.490 (0.33–0.65) → 0.490 (0.33–0.65) |
| gallinacci | holdout | 0.546 (0.40–0.70) → 0.597 (0.45–0.74) | 0.591 (0.51–0.69) → 0.554 (0.49–0.62) |

**Reading.** No metric moves outside its own bootstrap interval, at 6–23 presences per group and
role; this is a direction check, not a result, the same caveat as the growth-clock/terrain-lines
card above. Gallinacci's `auc_local` moves the most (+0.021 train, +0.051 holdout), consistent
with GAL-07 no longer discounting the many ordinary (flat/E/W, below-threshold) cells it used to.
The grid check is the stronger evidence here: the prior trapezoids held back the large majority of
woodland cells (59–88 % depending on the factor) for being merely typical, not steep or sunny,
which is what the card set out to fix. The change stays as a prior, same as slope and sun exposure
did after the growth-clock card.

<!-- RESULTS, TARGETS AND SANITY CHECK FOLLOW -->
