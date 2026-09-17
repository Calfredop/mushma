# Weather ingest: history, forecast and downscaling to cells

Build date: 2026-09-17. Card: M2 · Weather ingest. Traces to PRD → Architecture (Weather
downscaling), Candidate data sources, Milestone 2 and the backfill-depth question, now decided.

Daily weather for every woodland cell comes from Open-Meteo, fetched on a coarse lattice of model
nodes and downscaled to the 1 km grid: ERA5-Land reanalysis for the past, and ECMWF IFS for the last
few days and the next week. This page records which sources and variables the pipeline uses, how
cells get their values, the checks behind those choices, and how deep the history goes.

## At a glance

| | |
|---|---|
| History | Open-Meteo archive, model `era5_seamless` (ERA5-Land 0.1°, with rain, snow and wind from ERA5), about 6 days behind real time |
| Recent days and forecast | Open-Meteo forecast API, model `ecmwf_ifs` (IFS HRES 9 km), 14 past days + today + 7 days |
| Variables | 11 daily variables in local days (`Europe/Rome`); every weather variable the draft species rules use |
| Weather points | 0.2° lattice of ERA5-Land nodes: 129 around woodland cells, **103 on land** |
| Cells served | 10,777 of 10,778 woodland cells (one cell on Giglio has no land node within 30 km) |
| Downscaling | bilinear from the surrounding land nodes; temperatures corrected to cell height at 4.2–4.5 °C/km (air) and 3.7 °C/km (soil) |
| History depth | from **2016-01-01**, newest year first; about 2,960 weighted API calls per year |
| Daily update | about 290 weighted calls; a few seconds |
| Storage | about 0.6 MB of Parquet per year of history |

Commands (from `api/`; `DATA_DIR` moves the data as for the grid):

```sh
uv run python -m api.weather.ingest points              # once, after the grid is built
uv run python -m api.weather.ingest backfill --wait     # resumable; sleeps through daily limits
uv run python -m api.weather.ingest update              # daily: new reanalysis days + forecast
uv run python -m api.weather.ingest downscale --start 2026-09-10 --end 2026-09-24
uv run python -m api.weather.checks lattice             # lapse rates and lattice test (cached)
uv run python -m api.weather.checks gauges --start 2025-01-01 --end 2025-12-31
```

## Outputs

Everything lands in `$DATA_DIR/weather/<region>/` (`api/data/weather/tuscany/` locally, gitignored);
raw API responses are cached in `$DATA_DIR/raw/open_meteo/`.

| file | contents |
|---|---|
| `daily/source=<model>/year=<yyyy>/data.parquet` | the normalized table: `(source, point_id, date, variable, value, fetched_at)`, one row per point, local day and variable. Nulls are not stored. |
| `points.parquet` | the point set: `point_id` (e.g. `N43.80E011.80`), `lat`, `lon`, `land`, `grid_elevation_m` (ERA5-Land cell height), `dem_elevation_m` (mean DEM height of the 1 km cells nearest the node), `woodland_cells` |
| `weights.parquet` | `(method, cell_id, point_id, weight)` for `bilinear` and `nearest`; weights sum to 1 per cell and method |
| `point_cells.parquet` | per source and point: the model grid cell Open-Meteo served (`model_lat`, `model_lon`) and its mean height, the reference height for lapse-rate corrections |
| `meta.json` | sources and credits, points, variables and lapse rates |
| `cells/<start>-<end>.parquet` | downscaled exports: `(cell_id, date, variable, value, source)` |
| `checks/` | outputs of `api.weather.checks` |

The table is idempotent: the key is `(source, point_id, date, variable)`, and an upsert keeps the
newest `fetched_at`. Re-running a fetch rewrites the same rows. A newer forecast replaces the older
one for the same day. Reading a day picks the reanalysis when it exists, otherwise the forecast:

```sql
-- what WeatherStore.best_daily does
SELECT point_id, date, variable, value, source
FROM read_parquet('daily/*/*/data.parquet', hive_partitioning = false)
WHERE date BETWEEN DATE '2026-09-01' AND DATE '2026-09-24'
QUALIFY row_number() OVER (
    PARTITION BY point_id, date, variable
    ORDER BY list_position(['era5_seamless', 'ecmwf_ifs'], source)
) = 1;
```

For cells, call `api.weather.downscale.cell_weather(con, store, cells, weights, start, end,
variables, source_order)`; it returns a DuckDB relation the model can scan or write out.

## Sources

Every request pins daily values in the region's timezone, `cell_selection=nearest`, `elevation=nan`
(the raw model grid cell and its mean height, not Open-Meteo's own 90 m statistical downscaling), and
units (°C, mm, km/h). The parser rejects any response whose units differ.

- **History: `era5_seamless`.** In Open-Meteo, `era5_land` alone has no precipitation, snowfall,
  ET0 or wind; `era5_seamless` keeps the ERA5-Land grid and fills those from ERA5, which is how
  ERA5-Land itself is forced. It returns the ERA5-Land cell (e.g. 43.83 N 11.77 E → node 43.8 N 11.8
  E, 850 m) and fills sea nodes from ERA5 (sea temperatures, soil moisture 0), which is why the land
  mask comes from a separate `era5_land` probe. The archive's `best_match` was not used: since 2017
  it is ECMWF IFS, not ERA5.
- **Forecast: `ecmwf_ifs`.** The forecast API's `best_match` mixes models per variable. On
  2026-09-10 it reported 0.7 mm at Vallombrosa from a 2 km model while its soil variables came from
  IFS at a different height; IFS alone reported 39 mm and ERA5 25.5 mm. One model at every lead time
  keeps the series consistent. It shares the land model and soil layers (0–7, 7–28 cm) of ERA5-Land,
  and its 9 km grid matches ERA5-Land's resolution. `past_days=14` bridges the reanalysis delay.
- **The seam.** Where both sources have a day (2026-09-03 to 09-11, 103 nodes), IFS minus ERA5-Land
  was −0.9 °C for mean and −1.0 °C for minimum temperature, 0.0 °C for maximum, −1.3 °C for soil
  temperature, −0.01 m³/m³ for soil moisture, +1.4 mm/day for rain (r 0.80) and +1.3 km/h for wind.
  Nine days and one wet spell are too few for a correction; downscaled values carry `source`, so the
  model and the UI can tell reanalysis days from forecast days.

## Variables

| variable | unit | used by the draft rules for | downscaling | lapse rate |
|---|---|---|---|---|
| `precipitation_sum` | mm | rain trigger, 30-day rain, water balance, drought | bilinear | – |
| `snowfall_sum` | cm | snow stopper | bilinear | – |
| `temperature_2m_min` | °C | frost, cold nights | bilinear | 4.2 °C/km |
| `temperature_2m_max` | °C | heat spike (30-day anomaly) | bilinear | 4.5 °C/km |
| `temperature_2m_mean` | °C | air temperature band | bilinear | 4.5 °C/km |
| `soil_temperature_0_to_7cm_mean` | °C | soil temperature band (ovoli; porcini alternative) | bilinear | 3.7 °C/km |
| `soil_moisture_0_to_7cm_mean` | m³/m³ | post-rain moisture, waterlogging | bilinear | – |
| `soil_moisture_7_to_28cm_mean` | m³/m³ | same-month soil moisture (porcini, disabled) | bilinear | – |
| `et0_fao_evapotranspiration` | mm | drying, water balance | bilinear | – |
| `vapour_pressure_deficit_max` | kPa | drying (VPD variant) | bilinear | – |
| `wind_speed_10m_max` | km/h | drying wind (the card's "max wind"; no rule uses it yet) | bilinear | – |

`api/tests/weather/test_config.py` checks that every `variable` the species rule files use is in
this list, apart from the two derived series (`water_balance`, `temperature_2m_max_anomaly_30d`),
which M3 computes from these.

## Weather points

- **Lattice.** Nodes sit on multiples of 0.2° (every other ERA5-Land node) and are named by their
  coordinates, so ids stay stable if the stride changes. For each woodland cell centre the four
  nodes of its lattice square are candidates: 129 nodes.
- **Land.** One `era5_land` request for 2024-01-15 (temperature and topsoil moisture) marks the 103
  nodes with data as land. Sea nodes are never fetched.
- **Heights.** `grid_elevation_m` is the ERA5-Land cell height Open-Meteo reports. Across the 333
  land nodes of the full 0.1° grid it tracks the mean DEM height of the nearby 1 km cells with
  r = 0.93. The mean absolute difference is 88 m, and the grid runs lower on peaks (5th percentile
  −291 m). The IFS cells Open-Meteo serves for the same points sit on average 36 m from the ERA5-Land
  heights.

## Downscaling

For a cell, a day and a variable:

```
value = Σ wᵢ vᵢ / Σ wᵢ  +  Γ · (Σ wᵢ zᵢ / Σ wᵢ − z_cell)
```

- `wᵢ`: bilinear weights of the four corners of the cell's lattice square, by the cell centre's
  position. Sea corners are dropped and the rest renormalised: 9,597 cells use 4 corners, 720 use 3,
  336 use 2, 124 use 1. A cell with no land corner takes the nearest land node within 30 km. Corners can
  be up to 27 km away, the diagonal of a 0.2° square, but those carry near-zero weight. 29 coastal
  cells rely on a single land node more than 16 km away: 16 on Monte Argentario, 9 at Castiglione
  della Pescaia, 3 at Rosignano and 1 at Livorno. A `nearest` method is also stored, and
  each variable picks one in `weather.yaml`.
- `vᵢ`: the node's value from the most trusted source that has the day. A node missing that day
  drops out and the weights renormalise.
- `Γ`: the variable's lapse rate. `zᵢ` is the height of the model cell the value came from, per
  source, and `z_cell` is the cell's mean DEM height, so cells above their nodes come out cooler.
  Only temperatures are corrected. Rain, snow, soil moisture, ET0, VPD and wind are interpolated
  as they are.
- `source`: the least trusted source among the nodes used.

## Checks

### Lapse rates

Across Tuscany the ERA5-Land nodes carry ERA5's daily environmental lapse rate (ERA5-Land applies
it to reach 0.1°), which Dutra et al. (2020) found agrees with station observations of about
4.5 °C/km, flatter than the textbook 6.5. `checks lattice` regresses each day's node values on node
height, with latitude and longitude as covariates, over three 14-day windows of 2024 (333 land
nodes). The medians of the daily fits, in °C per km:

| variable | January | July | October | all |
|---|---|---|---|---|
| `temperature_2m_min` | 4.68 | 4.59 | 3.24 | **4.22** |
| `temperature_2m_max` | 4.56 | 4.27 | 4.64 | **4.50** |
| `temperature_2m_mean` | 4.69 | 4.61 | 4.12 | **4.45** |
| `soil_temperature_0_to_7cm_mean` | 3.36 | 3.91 | 3.41 | **3.71** |

The October Tmin rate is lower because valley inversions set in. One annual rate per variable is
kept for transparency; M3 can make it monthly if the backtest asks.

### Lattice leave-out test

Why 0.2°, and why these rates: the same windows, predicting the 248 ERA5-Land nodes a 0.2° lattice
skips (292 for 0.3°) from the nodes it keeps, with the downscaling above. RMSE against ERA5-Land's
own 0.1° values:

| variable | 0.2°, no lapse | 0.2°, 6.5 °C/km | **0.2°, config rates** | 0.3°, config rates |
|---|---|---|---|---|
| `temperature_2m_mean` (°C) | 0.40 | 0.31 | **0.26** | 0.39 |
| `temperature_2m_min` (°C) | 0.51 | 0.46 | **0.41** | 0.60 |
| `temperature_2m_max` (°C) | 0.43 | 0.35 | **0.30** | 0.50 |
| `soil_temperature_0_to_7cm_mean` (°C) | 0.47 | 0.43 | **0.37** | 0.52 |
| `soil_moisture_0_to_7cm_mean` (m³/m³) | 0.026 | 0.026 | **0.026** | 0.027 |
| `precipitation_sum` (mm/day) | 1.56 | 1.56 | **1.56** | 1.95 |
| `et0_fao_evapotranspiration` (mm) | 0.08 | 0.08 | **0.08** | 0.11 |
| `vapour_pressure_deficit_max` (kPa) | 0.09 | 0.09 | **0.09** | 0.15 |
| `wind_speed_10m_max` (km/h) | 1.83 | 1.83 | **1.83** | 2.10 |

On 3-day rain totals of at least 10 mm, the quantity the rain trigger reads, the 0.2° lattice is off
by 3.2 mm on average (r 0.99; 4.1 mm at 0.3°) in the same windows. Nearest-node without lapse correction was the worst
option everywhere (0.67 °C RMSE for mean temperature at 0.2°). The loss from the coarser lattice is
small against the rule ramps: the porcini rain trigger ramps over 20 mm and the temperature bands
over 4–5 °C. It costs a third of the calls. The one comparable error is topsoil moisture: 0.026
m³/m³ against a 0.07 ramp for ovoli, which the rules already treat as model-scaled and to be tuned.

### Ground truth: SIR Toscana gauges

`checks gauges` compares the downscaled rain in each woodland cell with the SIR Toscana rain gauges
inside it. SIR publishes every station's daily series as open JSON (CC BY-SA 4.0); only validated
and pre-validated days are kept. A gauge day runs from 09:00 to 09:00 (solar time), so calendar-day
model totals are re-cut: a gauge day ending on D takes 15/24 of D−1 and 9/24 of D. Metrics:

- the ratio of model to gauge totals over the matched days
- the daily correlation
- over 3-day windows where the gauge has at least 10 mm (the rain trigger's range): how often the
  model also reaches 10 mm, and its mean absolute error
- how often the model reaches 10 mm when the gauge does not

Woodland cells with an active SIR gauge (validated and pre-validated days, at least 80 % of days
present), 0.2° lattice and config lapse rates:

| period | band | gauges | model / gauge (pooled) | median ratio | median daily r | wet 3-day windows caught | false alarms | MAE on wet windows |
|---|---|---|---|---|---|---|---|---|
| 2025 | < 400 m | 41 | 0.79 | 0.82 | 0.64 | 82 % | 11 % | 17.7 mm |
| 2025 | 400–800 m | 55 | 0.69 | 0.70 | 0.64 | 73 % | 10 % | 18.1 mm |
| 2025 | ≥ 800 m | 37 | 0.63 | 0.69 | 0.66 | 81 % | 11 % | 18.9 mm |
| **2025** | **all** | **133** | **0.70** | **0.73** | **0.64** | **79 %** | **11 %** | **18.1 mm** |
| 2026 Jan–Sep 6 | < 400 m | 46 | 0.76 | 0.80 | 0.62 | 74 % | 7 % | 15.1 mm |
| 2026 Jan–Sep 6 | 400–800 m | 59 | 0.66 | 0.68 | 0.60 | 68 % | 7 % | 20.2 mm |
| 2026 Jan–Sep 6 | ≥ 800 m | 40 | 0.64 | 0.66 | 0.63 | 72 % | 7 % | 19.3 mm |
| **2026 Jan–Sep 6** | **all** | **145** | **0.68** | **0.70** | **0.62** | **72 %** | **7 %** | **17.8 mm** |

The seasons from 2019 go through the same check once the backfill reaches them (the backfill task
card has the command).

**Finding: the reanalysis rain is too dry in the hills, by about a third.** The model catches most
wet spells (7–8 in 10 of the gauges' 10 mm+ 3-day windows, with about 1 false alarm in 10 dry
windows), but with too little rain. The shortfall grows with height: about −20 % below 400 m, −30 %
at 400–800 m and −35 % above, in both periods. This is the known behaviour of ERA5 rain in complex
terrain: its 31 km model smooths orographic enhancement and convective cores. ERA5-Land does not add rain detail, since its rain is ERA5's interpolated. The
0.2° lattice is not the cause: against the 0.1° grid it changes wet 3-day totals by 3 mm, not
tens of mm.

No correction is applied in ingest. The rain thresholds in the draft rules come from gauge-based
studies, so on this data they would fire too rarely. **M3 should either tune the rain amounts on
the backtest (their scale is then ERA5's), or scale rain by an elevation-dependent factor fitted to
these gauges** (about ×1.25 below 400 m, ×1.45 at 400–800 m and ×1.6 above) before scoring.
`checks gauges` writes one row per gauge to `checks/gauges_<start>_<end>.csv` for that fit.

## Backfill depth and API budget

**Limits.** The free Open-Meteo API allows 600 calls per minute, 5,000 per hour, 10,000 per day and
300,000 per month per IP, for non-commercial use. The server counts in fixed UTC windows and refuses
a request only once a window is already spent. A request counts as

```
Σ over locations of max(1, variables/10 × max(1, days/14))
```

(`calculateQueryWeight` in Open-Meteo's source). A year of 11 variables at one location therefore
counts as 28.7 calls, whether it is asked in one request or many.

**Cost.** Per year of history:

| lattice | land nodes | calls per year | years per free day |
|---|---|---|---|
| 0.1° | 333 | 9,560 | 1.05 |
| **0.2°** | **103** | **2,960** | **3.4** |
| 0.3° | ≤ 63 | ≤ 1,800 | ≥ 5.5 |

**Backtest needs.** The Tuscan GBIF records for the three species, by year (2026-09-17): 185 have a
date. 166 of them (90 %) fall in 2019–2025, 2 in 2016–2018 and 17 are older (back to 1864). The
first ERA5-Land year is 1950.

**Decision (recorded in the PRD).** Backfill from 2016-01-01, newest year first:

- It covers every season with a usable number of records, the 2019 porcini flush included.
- Ten years (2016–2025) give `percent_of_normal` and `percentile_of_normal` a first climatology.
- It costs about 31,000 calls: roughly four days of background fetching within 9,000 calls a day.
  The seasons from 2019 arrive first.

The standard 1991–2020 normal would add about 75,000 calls (two weeks of free quota). It is a config
change and a re-run if M6's seasonal outlook needs cell-level normals, but area-level normals can
come cheaper from ERA5 at 0.25°.

**How the backfill runs.**

- One calendar year per request batch, each batch kept under 500 calls.
- A local budget (500/minute, 4,500/hour, 9,000/day) waits for the next UTC window before the
  server would refuse, and keeps its tally in `raw/open_meteo/usage.json` so separate runs share it.
- A chunk already complete in the store is skipped without a call, so a stopped run resumes where it
  was.
- Chunks older than 10 days are cached for good. A settled chunk that comes back with gaps is
  dropped from the cache and retried.
- `--wait` sleeps through server-side daily limits and network failures.
- By default the backfill ends 11 days ago. `update` covers the rest.

## Daily update

`update` fetches the reanalysis from the last day every point has (at least 14 days back) to
yesterday, then the forecast (14 past days to 7 ahead). At 0.2° that is about 290 calls and a few
seconds. It re-fetches when its cached responses are older than 6 hours (reanalysis) or 3 hours
(forecast). M4 schedules it before scoring, well inside the 07:00 freshness target. On Fly it runs
from Fly's IP, so it does not share the free quota with a laptop.

## Known gaps and hand-offs

- **Forecast seam.** IFS runs about 1 °C cooler than ERA5-Land for mean and minimum temperature
  and differs in rain (see Sources). It is not bias-corrected. The `source` column marks forecast
  days, and the "why" copy can say the further out, the more a score rests on the forecast (PRD).
- **One lapse rate per variable.** It is applied all year. October Tmin cools only about
  3.2 °C/km, and valley frost pockets below 1 km are not modelled.
- **No height correction** for snowfall (rain vs snow at altitude), VPD or ET0.
- **Coast and islands.** One woodland cell on Giglio has no land node within 30 km and gets no
  weather. 29 coastal cells (Monte Argentario, Castiglione della Pescaia) take it from a single land
  node 16–30 km away. Elba has land nodes.
- **Forecasts are not archived.** Each day's forecast replaces the previous one for the same
  date, so a past date can only be replayed from the reanalysis, not from the forecast issued at the
  time.
- **ERA5T.** The latest ~3 months of ERA5 are preliminary (ERA5T) and are replaced by final ERA5.
  They are normally identical, and settled chunks are not re-fetched.
- **Rain is too dry in the hills** (SIR gauges, 2025: model/gauge 0.79 below 400 m, 0.69 at
  400–800 m, 0.63 above). Not corrected in ingest; M3 decides (see Ground truth).
- **M3 · Model v1.** Read cell weather with `cell_weather()`. The derived series (`water_balance`,
  `temperature_2m_max_anomaly_30d`) and the climatology behind `percent_of_normal` /
  `percentile_of_normal` are M3's, from this table. Soil moisture is model-scaled, so prefer
  percentiles. Check `raw/open_meteo/usage.json` and `backfill.log` for backfill progress before
  backtesting seasons before 2019.
- **M4 · API + daily pipeline.** Schedule `ingest update` daily before scoring. Show
  `meta.json` → `sources` on the credits page, with a link to open-meteo.com next to the weather.
- **Scaling path.** For a denser lattice or deeper history without API limits, the same hourly
  ERA5-Land files are on Open-Meteo's AWS open-data bucket. The daily aggregation (local days, ET0,
  VPD) would then be ours, and would have to be checked against the API.

## Sources and licences

| source | licence | attribution |
|---|---|---|
| Open-Meteo Historical Weather and Forecast APIs | CC BY 4.0 | "Weather data by Open-Meteo.com", with a link to https://open-meteo.com/ next to the data |
| Copernicus Climate Change Service, ERA5-Land and ERA5 (via Open-Meteo) | CC BY 4.0 (all CDS data since 2025-07-02) | "Contains modified Copernicus Climate Change Service information" |
| ECMWF IFS HRES open data (via Open-Meteo) | CC BY 4.0 + ECMWF Terms of Use | "© European Centre for Medium-Range Weather Forecasts (ECMWF)" |
| SIR Toscana rain gauges (checks only, not in the app) | CC BY-SA 4.0 | "Servizio Idrologico Regione Toscana" |

The app credits live in `api/src/api/config/sources.yaml` (`open_meteo`, `copernicus_era5_land`,
`ecmwf_open_data`) and are copied into `meta.json`.

References: Muñoz-Sabater, J. et al. (2021), ERA5-Land: a state-of-the-art global reanalysis dataset
for land applications, ESSD 13, 4349–4383, https://doi.org/10.5194/essd-13-4349-2021; Dutra, E. et
al. (2020), Environmental lapse rate for high-resolution land surface downscaling: an application to
ERA5, Earth and Space Science 7, e2019EA000984, https://doi.org/10.1029/2019EA000984; Zippenfenig, P.
(2023), Open-Meteo.com Weather API, Zenodo, https://doi.org/10.5281/zenodo.7970649; Open-Meteo rate
limiter and call weight, github.com/open-meteo/open-meteo (`RateLimiter.swift`,
`ForecastApiResult.swift`).
