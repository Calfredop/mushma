---
order: 5
title: M2 · Weather ingest: history, forecast, downscaling
status: Done
priority: high
complexity: complex
---
Traces to PRD → Architecture (Weather downscaling), Candidate data sources, Milestone 2, Open questions (backfill depth).
Depends on: M1 Foundations. The cell → weather-point mapping needs M2 Woodland grid; everything else can start from the region config alone.

Write tests first for parsers and downscaling (AGENTS.md). Cache every response, batch coordinates and respect Open-Meteo rate limits. Always request daily data with `timezone=Europe/Rome`, so a day's rain is a local day.

- [x] Weather point set: a coarse grid over Tuscany matched to the source model resolution, plus each point's elevation
- [x] Open-Meteo history client (ERA5 / ERA5-Land): daily precipitation, air temp min/max, soil temperature, soil moisture, max wind, ET0 and vapour-pressure deficit (the drying factors); cached, batched, retry and backoff
- [x] Open-Meteo forecast client (today +7 days) for the same variables, using matching variable names and units
- [x] Normalized daily weather table (point × date × variable) in the chosen storage; re-runs for the same date are idempotent
- [x] Downscaling to cells: elevation lapse-rate temperature correction; precipitation by nearest or interpolated point
- [x] Decide history backfill depth (archive range vs rate limits vs backtest needs) and record it in the PRD
- [ ] [Run the backfill](./run-the-backfill.md)
- [x] Optional ground-truth check: compare ERA5-Land rain with a few SIR Toscana gauges and note any bias
- [x] Record Open-Meteo attribution (CC BY 4.0) for the credits page
