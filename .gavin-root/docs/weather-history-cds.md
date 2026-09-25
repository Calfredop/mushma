# Weather history from the Copernicus CDS

Spike for `weather-history-cds.md` (parent: `feat-full-italy-coverage.md`).
Written 2026-09-24. Live Tuscany-2024 RMSE numbers land here once `CDSAPI_KEY` is
available and a year has been fetched (see Status).

## Decision

| Choice | Value |
|---|---|
| Dataset | Hourly `reanalysis-era5-land` (not `derived-era5-land-daily-statistics`) |
| Aggregation | Europe/Rome local days here (DST-aware), from hourly NetCDF |
| Source id | `era5_land_cds` (new), ranked **before** `era5_seamless` in `source_order` |
| Lattice | Unchanged 0.2° (same points as today) |
| ET0 / VPD | Derived from hourly 2 m T, dew point, 10 m wind and SSRD (Open-Meteo / FAO-56) |
| Rain / snow / wind | ERA5-Land's own fields (Open-Meteo `era5_seamless` fills those from ERA5) |
| Seasonal lattice | Stride 3 on the weather points → 0.6° (~1/9 of the land nodes) |
| Open-Meteo daily budget (20 regions) | Target ≤ ~5,000 weighted calls/day (see below) |

Tuscany keeps its stored `era5_seamless` history. New regions backfill only from CDS.
A day present in both sources prefers CDS.

### Why not the CDS daily-statistics product

1. **Timezone.** `derived-era5-land-daily-statistics` shifts by a fixed UTC offset
   (`utc+01:00` / `utc+02:00`). Europe/Rome needs DST. Open-Meteo and the species
   rules already use true local days.
2. **Accumulations.** ERA5-Land daily statistics omit accumulated variables
   (precipitation, snowfall, radiation). Those are required for rain, snow and ET0.
3. **ET0 and VPD** are not CDS fields. They need hourly inputs anyway.

So requests are cached under `$DATA_DIR/raw/cds/` as ~7-day hourly chunks (a full
month of all variables exceeds CDS cost limits on a regional bbox) and aggregated
once into the daily store.

### Fetching: the time-series product (2026-09-25, `region-umbria` card)

The weekly chunks were too slow to onboard 19 regions. A region needs ~630 requests
for 2016 to today, and CDS runs **one request per account at a time**, across every
dataset. Each request ran ~2.5–6 min, so a region took ~30–60 h, and every region rail
shares the account (a full queue also rejects new submissions with "Number queued
requests for this dataset is temporarily limited").

`cds.method: timeseries` in `weather.yaml` now fetches the same hourly ERA5-Land
values from the `reanalysis-era5-land-timeseries` product instead:

- **Node series.** One request per weather node (the 0.2° lattice nodes sit on the
  ERA5-Land grid) for the whole range, with the nine variables it offers. One Umbrian
  node for 2016-01-01 → 2026-09-14 took **35 s** to run (7.6 MB zip).
- **Same values.** Checked against the weekly chunk at the same node (N43.00 E12.40,
  8–14 Aug 2026, 168 hours): temperatures, dew point and soil temperature within
  0.0003 K, soil water and wind identical. Precipitation and radiation are **already
  hourly increments** in this product (weekly sums equal to 2e-8 m); the gridded
  dataset's 00 UTC carry-over step does not exist here.
- **Snowfall** is not in the product. It comes from the gridded dataset, snowfall only,
  half a year per request (cost 1 × 24 h × 31 d × 6 months × 2 = 8,928 of 12,000); a
  month the range only partly covers goes alone with its days, so no request asks for
  days CDS does not have yet. It is deaccumulated per node over the whole range at once.
- **Local days.** Node series start a day before the range, so each Europe/Rome day
  gets its evening UTC hours; days are aggregated a year at a time with the same
  `aggregate_hourly_frame` and written under the same source id `era5_land_cds`.
- **Cost for a region.** Umbria: 56 node requests + 22 snowfall requests instead of 634
  chunks. Chunks still work (`method: chunks`) and their cache is untouched.
- **Queue.** `CdsClient` waits out the "temporarily limited" rejections (2 min, up to
  an hour) instead of failing the backfill. Queued weekly chunks from any rail still
  delay everyone's requests, so rails should not warm chunk caches any more.

## Variable map

| Store variable | CDS / derived |
|---|---|
| `precipitation_sum` (mm) | `total_precipitation` (m → ×1000), local-day sum |
| `snowfall_sum` (cm) | `snowfall` (m of water equiv. → ×100 as cm), local-day sum |
| `temperature_2m_{min,max,mean}` (°C) | `2m_temperature` (K → °C), local-day min/max/mean |
| `soil_temperature_0_to_7cm_mean` (°C) | `soil_temperature_level_1` (K → °C), mean |
| `soil_moisture_0_to_7cm_mean` (m³/m³) | `volumetric_soil_water_layer_1`, mean |
| `soil_moisture_7_to_28cm_mean` (m³/m³) | `volumetric_soil_water_layer_2`, mean |
| `wind_speed_10m_max` (km/h) | `√(u²+v²)` from `10m_u/v_component_of_wind` (m/s → ×3.6), local-day max |
| `vapour_pressure_deficit_max` (kPa) | hourly `es(T) − es(Td)`, then max (Open-Meteo / FAO-56) |
| `et0_fao_evapotranspiration` (mm) | FAO-56 Penman–Monteith on hourly steps, summed (Open-Meteo method) |

ERA5-Land precipitation and wind differ from Open-Meteo's `era5_seamless` (which
takes rain/snow/wind from ERA5). Tuscany 2024 node-by-node vs stored
`era5_seamless` (`checks/cds_vs_seamless_2024.json`), after fixing deaccumulation
(full UTC series; drop leading 00 UTC carryover; ignore float32 plateau noise):

| Variable | Metric | Measured | Gate |
|---|---|---|---|
| `temperature_2m_{min,max,mean}`, soil T | RMSE | 0.07–0.16 °C | ≤ 0.3 °C |
| `vapour_pressure_deficit_max` | mean abs % | 0.7 % | ≤ 10 % |
| `precipitation_sum` wet 3-day | Pearson r | **0.957** | ≥ 0.95 |
| `et0_fao_evapotranspiration` | mean abs % | **3.6 %** | ≤ 10 % |
| `wind_speed_10m_max` | bias | −1.8 km/h | informational (ERA5-Land vs ERA5) |
| soil moisture | RMSE | ~0.0005–0.0007 | informational (near-identical) |

Decision: ship `era5_land_cds` ahead of `era5_seamless` in `source_order`. All
hard gates pass; wind remains the known ERA5-Land vs ERA5 gap.

## Volume, queue, disk (Tuscany 2024, measured)

| | Measured |
|---|---|
| Raw NetCDF zip cache | **91 MB** (60 weekly chunks, bbox ~42.3–44.8°N / 9.5–12.6°E) |
| CDS wall time | **~4.2 h** cold (60 retrieves; ~4 min/chunk average queue+download) |
| Reprocess from cache | **~30 s** |
| Normalized Parquet | **1.9 MB** / year (103 land nodes × 11 variables) |

Italy as one national bbox is larger; the ingest still requests **per region
bbox** so region rails do not block each other and caches stay reusable.

## Open-Meteo daily call budget for 20 regions

History backfill leaves Open-Meteo. The daily job still needs `update` (recent
reanalysis + forecast) and `seasonal fetch` on the free tier (~10,000 calls/day,
~300,000/month). Target: about half of the day (~5,000).

Tuscany today (103 land nodes, 0.2°): ~290 calls for `update`, ~450 for seasonal
→ ~740/region. ×20 ≈ 14,800 — too high.

| Change | Effect |
|---|---|
| Seasonal points: every 3rd weather point (0.6°) | ~1/9 of seasonal calls → ~50/region |
| `forecast.past_days`: 14 → 7 | Cuts the forecast weight (~40 %) |
| Keep `history.recent_days` at 14 | CDS covers settled history; Open-Meteo only bridges the CDS delay |

Projected per region after the change: update ≈ 200, seasonal ≈ 50 → **~250**.
×20 ≈ **5,000** weighted calls/day (~150,000/month). Measured counts from a
multi-region dry run replace these once two regions are served.

## Credentials

```sh
# api/.env (gitignored), or ~/.cdsapirc
CDSAPI_KEY=uid:api-key   # from https://cds.climate.copernicus.eu/how-to-api
```

```sh
uv run python -m api.weather.ingest backfill --source cds --region tuscany --start 2024-01-01 --end 2024-12-31
```

## Status

- [x] Dataset / aggregation / source id decided (this page)
- [x] Derived ET0/VPD module and CDS ingest implemented (see `api/src/api/weather/{derived,cds}.py`)
- [x] Chunking: ~7-day requests (month-sized all-variable requests hit CDS cost limits)
- [x] Live Tuscany 2024 fetch + node-by-node RMSE vs `era5_seamless` (numbers above)
- [x] Measured volume / queue / disk for Tuscany; daily call counts for ≥2 regions still pending a second region
