# Draft species rule config

A draft of the rule config that M3 Model v1 loads. It has one file per scored species key, a shared
bibliography and a JSON Schema. The rules come from `../species-ecology.md` and its evidence appendices
in `../species-ecology/`. Every number is a **prior for the backtest**, not a tuned value
(`status: draft`).

M3 owns the final schema and the loader. When `api/` has a config folder, move these files there and
let the real loader and its tests replace `validate.py`.

## Files

| file | what it is |
|---|---|
| `porcini_edulis.yaml`, `porcini_reticulatus.yaml`, `porcini_aereus.yaml`, `porcini_pinophilus.yaml` | the four porcini taxa, all in group `porcini` |
| `ovoli_caesarea.yaml` | *Amanita caesarea*, group `ovoli` |
| `gallinacci_cibarius.yaml` | *Cantharellus cibarius* s.l., group `gallinacci` |
| `references.yaml` | shared bibliography; every factor `source` id resolves here |
| `species.schema.json`, `references.schema.json` | JSON Schema (draft 2020-12) for the two file types |
| `validate.py` | interim lint: schema, source ids, trapezoid order, enabled factors only use available inputs |

```sh
uv run --with pyyaml --with jsonschema python .gavin-root/docs/species-rules/validate.py
```

## How a score is computed

For one cell, species key and day:

```
score = Π gates  ×  Π stoppers  ×  exp( Σ_d w_d · ln f_d  /  Σ_d w_d )
```

- **gate** (`season`, `habitat`, `altitude`): suitability that barely changes day to day.
  Multiplicative, so out of season or outside the altitude band means 0.
- **driver** (rain, temperature, moisture): the weather conditions, combined as a **weighted geometric
  mean**. Any driver at 0 zeroes the score, so heat cannot make up for missing rain. Partial values
  still trade off against each other.
- **stopper** (frost, snow, heat spike, drying): a penalty that multiplies the score, where 1 means no
  effect. A `floor` stops a weakly sourced stopper from zeroing a score on its own.
- Factors with `enabled: false` are recorded but not scored. They are either alternatives to compare
  in the backtest (air vs soil temperature, rain vs water balance), inputs that need the history
  climatology, or rules that need data v1 does not have (`data: missing`).

Every factor value is in [0, 1] and comes from a **trapezoid** `[zero_below, full_from, full_to,
zero_above]`: 0 outside, linear ramps, 1 on the plateau. A `null` pair makes one side open-ended,
e.g. `[10, 30, null, null]` means "0 at 10 mm, full from 30 mm up".

### Factor kinds

| kind | input | value |
|---|---|---|
| `season_window` | one or more `DD-MM` trapezoids, optional `elevation_weight` per window | max over windows of date membership × elevation weight |
| `habitat` | affinity 0–1 per habitat key | Σ over the cell's habitat fractions of fraction × affinity |
| `static_band` | a cell attribute (`elevation_m`, …) | trapezoid of the attribute |
| `rain_event` | daily rain, `accumulation_days` | max over lags d of amount(rain summed over the days ending d days ago) × lag(d); the breakdown reports "N mm, d days ago" |
| `window_aggregate` | a daily variable, `sum`/`mean`/`min`/`max`/`percent_of_normal`/`percentile_of_normal` over `window_days` | trapezoid of the aggregate |
| `count_days` | a daily variable, comparison and threshold | trapezoid of the number of matching days in the window |
| `days_since` | a daily variable, comparison and threshold | trapezoid of the days since the last matching day |

Derived daily series: `water_balance` = `precipitation_sum − et0_fao_evapotranspiration`;
`temperature_2m_max_anomaly_30d` = today's Tmax minus the mean Tmax of the previous 30 days.
`percent_of_normal` and `percentile_of_normal` compare the window with the cell's own climatology for
the same calendar window, so they need the history backfill.

### Proposed breakdown weighting

The "why this score" UI needs to say how much each factor held the score back. In log space the model
is additive: `−ln score = Σ_i −w'_i ln f_i`, where `w'` is 1 for gates and stoppers and `w_d / Σ w`
for drivers. So each factor's **impact** is its share of the total shortfall:

```
impact_i = (−w'_i ln f_i) / Σ_j (−w'_j ln f_j)
```

Impacts sum to 1. A factor at 1 has impact 0, and a factor at 0 takes all the impact ("blocked by
frost"). When every factor is 1 the score is 1 and nothing is held back. The UI can order factors by
impact and show each factor's raw input (e.g. "32 mm, 12 days ago").

## Rules for rules

- Every factor has `source` (≥1 id from `references.yaml`) and `confidence`
  (`strong` / `plausible` / `folklore`, defined in `../species-ecology.md`).
- `derived: true` means the numbers were turned from qualitative or out-of-region evidence into
  parameters, and `notes` must then say how.
- `data`: `available` = inputs exist in v1; `derived` = computed from available inputs (a derived
  series or a climatology); `missing` = needs data v1 lacks, and must be `enabled: false`.
- `known_gaps` records effects the sources support but schema v1 cannot encode (aspect conditional on
  elevation, change detection, compound conditions, calendar-anchored windows, cumulative
  growing degree-days) or that need missing data. It keeps them visible for later.
- `i18n_key` values are shared across species (`factor.rain_trigger`, `factor.frost`, …) so the UI
  translates each factor once.
