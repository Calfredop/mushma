---
kind: task
title: [foundation] Weather history from the Copernicus CDS
parent: feat-full-italy-coverage.md
complexity: intricate
---
Replace the Open-Meteo archive as the source of weather history with a bulk ERA5-Land
download from the Copernicus Climate Data Store (CDS), so a new region's 2016→today
history costs no API quota. The forecast (`ecmwf_ifs`) and the seasonal fetch stay on
Open-Meteo. Context: `.gavin-root/docs/weather-ingest.md`, `api/src/api/config/weather.yaml`,
`api/src/api/weather/`. Decisions in the parent plan `feat-full-italy-coverage.md`.

Spike first, written to `.gavin-root/docs/weather-history-cds.md`:
1. Which CDS dataset yields the 11 daily variables of `weather.yaml` as Europe/Rome
   local days: `derived-era5-land-daily-statistics` (daily stats, fixed UTC offset,
   no DST) or hourly `reanalysis-era5-land` aggregated here. ET0 FAO-56 and daily
   maximum VPD are not CDS variables: compute them from hourly 2 m temperature, dew
   point, wind and radiation the way Open-Meteo documents, or show which alternative
   the rules can take. Rain, snow and wind come from ERA5-Land's own fields (Open-Meteo
   takes them from ERA5): measure the difference.
2. Validate on Tuscany's 103 nodes for 2024, node by node against the stored
   `era5_seamless` values: RMSE and bias per variable, judged against the rule ramps
   as the lattice test was (temperatures within ~0.3 °C, wet 3-day rain totals
   r ≥ 0.95, ET0 and VPD within ~10 %). Record volume, queue time and disk per
   region-year.
3. Decide and record: dataset, aggregation, tolerances, and whether the result is a
   new source id (`era5_land_cds`, ranked with `era5_seamless` in the source order)
   or replaces it.

Then the ingest, tests first:
- `api.weather.ingest backfill --source cds` (or a `cds` subcommand) fetches by region
  bbox and year into the same daily Parquet table and point set (0.2° lattice
  unchanged), resumable, cached under `$DATA_DIR/raw/cds/`, with the key from
  `CDSAPI_KEY` or `~/.cdsapirc` (the human registers; the README says how).
- Derived variables live in one tested module; units are checked as the Open-Meteo
  parser checks them.
- Daily budget: Open-Meteo `update` plus `seasonal fetch` for 20 regions must stay
  under ~5,000 weighted calls a day and 150,000 a month. Thin the seasonal lattice
  (36 km data: stride 3 or a 0.6° lattice) and, if needed, `recent_days`; record the
  measured calls per region.
- `weather.yaml` gains the CDS source and the seasonal stride; `sources.yaml` and the
  credits gain the CDS citation (ERA5-Land is already CC BY 4.0); `meta.json` and the
  downscaled `source` column name the new source.

Done when: the spike doc has the numbers and the decision; `uv run pytest`, `ruff
check` and `ruff format --check` pass; Tuscany 2024 from CDS matches the stored
history within the tolerances; the projected daily call count for 20 regions is in
the doc.

Blocked (2026-09-24): spike decision + ingest/tests/README done (`era5_land_cds`,
hourly CDS → Europe/Rome days, seasonal stride 3, forecast past_days 7). Live 2024
RMSE vs stored `era5_seamless` still needs `CDSAPI_KEY` in `api/.env` (rail gate was
marked done but no key was on disk). Parent checklist stays open until that lands.

Done 2026-09-25. Tuscany 2024 CDS backfill (60 weekly chunks, ~4.2 h cold / ~30 s from
cache, 91 MB raw, 1.9 MB parquet). Deaccumulation fixed (full UTC series; drop leading
00 UTC carryover; ignore float32 SSRD plateau noise). All RMSE gates pass (temps
≤0.3 °C, VPD ≤10 %, rain wet-3d r 0.957, ET0 MAPE 3.6 %) — see
`.gavin-root/docs/weather-history-cds.md` and `checks/cds_vs_seamless_2024.json`.
