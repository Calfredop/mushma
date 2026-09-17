# Species rules

The rule config the model scores with: one file per species key, a shared bibliography, and the
roll-up into the app's species in `../model.yaml`. The rules come from
`.gavin-root/docs/species-ecology.md` and its evidence appendices in `.gavin-root/docs/species-ecology/`.
Every number is a **prior for the backtest** unless the file's `status` is `tuned`
(see `.gavin-root/docs/model-v1-validation.md`).

`api.model.rules.load_rules()` loads and validates everything here, and refuses to load on the first
problem, naming the file and the rule. `tests/model/test_rules.py` runs it against the shipped files and
against 21 deliberately broken copies.

## Files

| file | what it is |
|---|---|
| `porcini_edulis.yaml`, `porcini_reticulatus.yaml`, `porcini_aereus.yaml`, `porcini_pinophilus.yaml` | the four porcini taxa, all in group `porcini` |
| `ovoli_caesarea.yaml` | *Amanita caesarea*, group `ovoli` |
| `gallinacci_cibarius.yaml` | *Cantharellus cibarius* s.l., group `gallinacci` |
| `references.yaml` | shared bibliography; every factor `source` id resolves here |
| `../model.yaml` | which keys make up each group, in tie-break order |

## How a score is computed

For one cell, species key and day (`api.model.engine`):

```
score = Π gates  ×  Π stoppers  ×  exp( Σ_d w_d · ln f_d  /  Σ_d w_d )
```

- **gate** (`season`, `habitat`, `altitude`): suitability that barely changes day to day.
  Multiplicative, so out of season or outside the altitude band means 0.
- **driver** (rain, temperature, moisture): the weather conditions, combined as a **weighted geometric
  mean**. Any driver at 0 zeroes the score, so heat cannot make up for missing rain. Partial values
  still trade off against each other.
- **stopper** (frost, snow, heat spike, drying): a penalty that multiplies the score, where 1 means no
  effect.
- Factors with `enabled: false` are recorded but not scored. They are alternatives to compare in the
  backtest (air vs soil temperature, rain vs water balance), rules that need a per-cell climatology v1
  does not compute (`percent_of_normal`, `percentile_of_normal`), or rules on data v1 does not have
  (`data: missing`).

Every factor value is in [0, 1] and comes from a **trapezoid** `[zero_below, full_from, full_to,
zero_above]`: 0 outside, linear ramps, 1 on the plateau. A `null` pair makes one side open-ended, e.g.
`[10, 30, null, null]` means "0 at 10 mm, full from 30 mm up". A zero-width ramp is a step that
includes its edge: `[null, null, 1, 1]` is 1 up to 1 and 0 above.

A **`floor`** lifts the response linearly so a weakly sourced rule cannot zero a score on its own:
`value = floor + (1 − floor) × trapezoid`.

Weather windows include the day being scored. A window that reaches before the weather's first day, or
holds a day with no data, makes the factor, and so the score, missing: the engine never scores on
partial weather.

### Factor kinds

| kind | input | value |
|---|---|---|
| `season_window` | one or more `DD-MM` trapezoids, optional `elevation_weight` and `altitude_shift` per window | max over windows of date membership × elevation weight; windows may wrap the year end; 29 February counts as the 28th |
| `habitat` | affinity 0–1 per habitat key | Σ over the cell's habitat fractions of fraction × affinity (`default` for unlisted habitats) |
| `static_band` | a cell attribute (`elevation_m`, `soil_ph`, …) | trapezoid of the attribute |
| `rain_event` | daily rain, `accumulation_days` | max over whole-day lags d of amount(rain summed over the days ending d days ago) × lag(d); a tie goes to the longest lag, so "30 mm, 12 days ago" names when the rain ended |
| `window_aggregate` | a daily variable, `sum`/`mean`/`min`/`max` over `window_days` ending `offset_days` ago | trapezoid of the aggregate |
| `count_days` | a daily variable, comparison and threshold | trapezoid of the number of matching days in the window |
| `days_since` | a daily variable, comparison and threshold | trapezoid of the days since the last matching day, capped at `max_lookback_days` |

Derived daily series: `water_balance` = `precipitation_sum − et0_fao_evapotranspiration`;
`temperature_2m_max_anomaly_30d` = the day's Tmax minus the mean Tmax of the 30 days before.

## The breakdown

Every score comes with its factors, in a fixed order (gates, drivers, stoppers, each in file order),
never re-sorted by size. Each line has:

| field | meaning |
|---|---|
| `key`, `i18n_key`, `role`, `weight` | the factor as configured |
| `value` | the factor's 0–1 response |
| `contribution` | its multiplicative share of the score: `value` for gates and stoppers, `value ** (w / Σ w)` for drivers. **The product of the contributions is the score.** |
| `input` | what the factor measured, in its own unit (mm of rain, °C, days, metres), when it measures something |
| `days_ago` | rain events only: when the rain it scored ended |

`i18n_key` values are shared across species (`factor.rain_trigger`, `factor.frost`, …) so the UI
translates each factor once. The UI splits the score's shortfall between factors in log space:
`impact_i = −ln contribution_i / Σ_j −ln contribution_j`, and a factor at 0 takes all of it ("blocked
by frost").

## Groups and the combined score

`../model.yaml` lists the keys behind each app species:

- **Group score** (`porcini`, `ovoli`, `gallinacci`) = the max over the group's keys, with the winning
  key's breakdown, so the UI can also say which porcino. On a tie the key listed first wins. Max, not
  sum, because the four porcini share the same rain logic; a sum would count it four times.
- **Combined score** (`combined`) = the max over the groups **in season** (every season gate of at
  least one of the group's keys is open for that cell and day), with the winning group's breakdown. On a
  tie the group listed first wins. When no group is in season the combined score is 0, with no winner
  and no breakdown ("out of season"). It keeps the 0–1 index meaning: the best conditions of the three,
  here, today.

## Rules for rules

The loader enforces all of these:

- Every factor has `source` (≥ 1 id from `references.yaml`) and `confidence`
  (`strong` / `plausible` / `folklore`, defined in `species-ecology.md`). Every reference has a DOI or
  a URL.
- Trapezoid edges are in order, and a `null` edge comes as a (zero, full) pair.
- Drivers have a `weight`; gates and stoppers do not. Each species has at least one enabled driver.
- `derived: true` means the numbers were turned from qualitative or out-of-region evidence into
  parameters, and `notes` must then say how. A disabled factor's `notes` must say why.
- `data`: `available` = inputs exist in v1; `derived` = computed from available inputs; `missing` =
  needs data v1 lacks, and must be `enabled: false`.
- An enabled factor may only read weather variables the ingest fetches (`../weather.yaml`) and cell
  attributes the woodland grid has. Habitat keys must be in `../habitats.yaml`.
- Factor ids are unique per file; the file name is the species key; the key's `group` matches
  `../model.yaml`, which must list every file.
- `known_gaps` records effects the sources support but the engine cannot encode (aspect conditional on
  elevation, change detection, compound conditions, calendar-anchored windows, growing degree-days) or
  that need missing data, so they stay visible.
