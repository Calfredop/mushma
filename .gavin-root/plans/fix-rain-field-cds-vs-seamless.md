---
title: [model] Rain field: fit against the source each region scores (CDS vs era5_seamless)
status: To Do
priority: medium
complexity: moderate
---
Found by `fix-rain-calibration-region-borders.md` (`.gavin-root/docs/rain-scale-field.md` → Known limits).

The national rain field (`config/rain_scale_field.csv`) is fitted on gauge/reanalysis ratios where the reanalysis is Open-Meteo `era5_seamless`, because Open-Meteo serves no `era5_land` rain. Most regions score CDS ERA5-Land (`era5_land_cds`). April–November rain from `era5_seamless` is lower than CDS at the same nodes: Sicily 2019 0.893, Lazio 2020 0.952, Sardinia 2021 0.954, South Tyrol 2023 0.964, Lombardia 2024 0.979, Campania 2024 0.983, Calabria 2024 0.987, Abruzzo 2024 0.987, Molise 2024 0.986, Puglia 2024 0.968, Basilicata 2024 0.993, Veneto 2024 0.995, Valle d'Aosta 2024 1.004, Friuli 2024 1.031. So CDS regions' scaled rain runs up to 11 % wet (Sicily), 1–5 % in most, and about 3 % dry in Friuli. The measurement pooled April–November `era5_seamless` / CDS rain at a region's stored nodes; `api.weather.rain_field._reanalysis` fetches the `era5_seamless` side.

- [ ] Choose the approach:
  - fit the gauge ratios against CDS rain where a CDS node series exists (the cached `raw/cds/ts_*` files, or the server's stores); or
  - fit a second smooth field of `era5_seamless`/CDS ratios at every CDS node, and divide by it for CDS rows (`PrecipitationScale.factor` per source).
- [ ] Measure seamless/CDS for Tuscany, Umbria, Liguria, Emilia-Romagna, Piemonte and Marche, whose CDS stores are only on the server.
- [ ] Refit, re-run `rain_field borders`, then re-score and backtest Sicily first (the largest gap).
