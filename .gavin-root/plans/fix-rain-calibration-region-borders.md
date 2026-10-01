---
order: 3072
title: [model] Rain calibration without steps at region borders
status: In Progress
priority: medium
complexity: moderate
---
Found by the Umbria card (`.gavin-root/docs/regions/umbria.md` → Validation → "Known issue: a step at the Tuscan border").

Each region scales the reanalysis rain with its own region-wide gauge fit (`model.precipitation_scale`): Tuscany 1.28 + 0.29/km (SIR gauges, `era5_seamless`), Umbria 0.89 + 0.33/km (Servizio Idrografico gauges, CDS), Liguria 1.04 + 0.20/km (ARPAL, CDS). The reanalysis products agree (CDS vs `era5_seamless` rain pooled 0.995, Tuscany 2024); the gauge networks don't (Tuscany reads the reanalysis at 0.63–0.79 of gauge rain, Umbria about 0.9–1.1). The same raw rain is therefore scaled ×1.41 on the Tuscan side of the border and ×0.99 on the Umbrian side 12 km away. On 2026-09-25 the border band scored 0.86 vs 0.47 (combined) and 0.47 vs 0.07 (porcini), a visible step on the hub map.

- [x] Decide the shape: one national fit, per climate zone, or a smooth per-node factor from every region's open gauges (SIR Toscana, ARPAL, Umbria's Servizio Idrografico, …)
  - **Decided 2026-09-30 (human): a smooth field fitted on every gauge at once.** By 2026-09-30 all 20 regions carry their own fit (Tuscany 1.28, Emilia-Romagna 0.62, Valle d'Aosta 0.58, …). Seven region docs report a step at their borders: lazio, molise, lombardia, friuli_venezia_giulia, abruzzo, marche and campania, plus umbria.
  - Shape: at every node of a 0.25° lattice over Italy, a local `a + b × elevation_km`, clamped at `z_max`. The fit is weighted least squares of gauge/reanalysis ratios, with a Gaussian distance kernel and a ridge pull toward the national fit. The kernel width is chosen by spatial-block cross-validation: a national fit and per-region fits are its two extremes. The field is committed as a small CSV under `config/`, with a `source` and `confidence`. Cells read `a`, `b` and `z_max` bilinearly at their lon/lat.
  - Reanalysis at the gauges: Open-Meteo `era5_land` at each gauge's nearest 0.1° node (`elevation=nan`), the same ERA5-Land as CDS and `era5_seamless`, from one source for every network. No region grid or weather store is needed.
  - Networks whose gauges have no committed parser (Basilicata, Calabria, Puglia, Valle d'Aosta and Veneto yearbooks, Campania agrometeo) join as pseudo-gauges drawn from their published fit, at their own woodland cells within their gauge height range. Borrowed fits (Abruzzo, Marche, Molise) and FVG (none) are left out and take the field's value.
- [x] Fit it with the gauge networks in `api.weather.checks` (`GAUGE_NETWORKS`), all gauges rather than woodland-only where a region has few (Umbria has 8 in woodland, 82 overall)
  - Done 2026-10-01. Write-up: `.gavin-root/docs/rain-scale-field.md`.
    - Code: `api/src/api/weather/rain_field.py` (collect, fit, borders), `api/src/api/model/rain_field.py` (lookup), `config/rain_field.yaml` (inputs) and `config/rain_scale_field.csv` (the field). `model.yaml` points at the field; the 19 region rain blocks are removed.
    - Data: 1,980 gauges in 10 networks, all stations, April–November, plus 278 pseudo-gauges for the six regions fitted on yearbooks or farm networks.
    - Fit: a 25 km Gaussian kernel won 50 km block cross-validation, log error 0.186 against 0.252 for one national fit.
  - Over all 361 SIR gauges in 2023–2025 the Tuscan reanalysis is about right (pooled 1.05), so Tuscan rain drops about 27 % against the old 1.28 + 0.29/km. The old fit leaned on the wet 2025.
  - Limit, filed as `fix-rain-field-cds-vs-seamless.md`: the field is fitted on `era5_seamless`, but most regions score CDS, which is up to 11 % wetter (Sicily) and 3 % drier in Friuli.
- [x] Also: Tuscany's local store holds CDS rows for 2024 that outrank `era5_seamless` and are not in the national `precipitation_scale.sources`, so they go unscaled (check whether the server has them)
  - Resolved by config, not by checking the server: the national scale now lists `sources: [era5_land_cds, era5_seamless]`, so CDS rows are scaled in every region's store, whether the server has any or not. Reading the server was not permitted from this session.
- [ ] [Re-score the affected regions; record before/after at the Tuscany–Umbria and Tuscany–Liguria borders](./re-score-the-affected-regions-record-before-after-at-the-tuscany-umbria-and-tuscany-liguria-borders.md)
  - Factors before/after, at points every 5 km along every border (`rain_field borders`; `rain-scale-field.md` → Before and after):
    - Tuscany–Umbria: ×1.37 vs ×1.00 before, ×0.92–1.03 with the field.
    - Liguria–Tuscany: ×1.09 vs ×1.35 before, ×0.89–1.23 with the field.
  - Scores re-scored locally in the 10 km border band (in memory; the stores are untouched):
    - Lazio–Abruzzo, 20 Oct 2025: combined 0.71 vs 0.78 before, 0.70 vs 0.73 after.
    - Basilicata–Calabria, 20 Oct 2025: 0.68 vs 0.82 before, 0.68 vs 0.66 after.
  - Still to do, on the server (Tuscany, Umbria and Liguria have no stores on the laptop):
    1. Re-run the Tuscan backtest first (rain −27 %, and the rain-driver tuning was done on the old scale).
    2. Rebuild the normals and history and re-score every region (rain moves −27 % to +21 % per region).
    3. Re-score the Tuscany–Umbria and Tuscany–Liguria border bands, then deploy.
- [x] Regions without open daily gauges get their factor from the fit too: Marche (`marche.yaml`) borrows the mean of Umbria's and Emilia-Romagna's CDS fits, 0.76 + 0.57/km, until then (`.gavin-root/docs/regions/marche.md` → Weather); Campania (`campania.yaml`) fits 0.77 + 0.52/km on its 33 open agrometeo farm gauges (11–769 m, none in woodland), so its mountain factor is extrapolated (`.gavin-root/docs/regions/campania.md` → Weather)
  - Done: Marche, Abruzzo, Molise and Friuli add no gauges and read the field fitted on their neighbours'. Campania (with Basilicata, Calabria, Puglia, Valle d'Aosta and Veneto) joins as pseudo-gauges carrying its own fit, at its woodland cells within its gauge heights (11–769 m), so above them it follows the field, not an extrapolation.
