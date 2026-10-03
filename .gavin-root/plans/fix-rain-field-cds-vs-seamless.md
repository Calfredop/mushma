---
title: [model] Rain field: fit against the source each region scores (CDS vs era5_seamless)
status: In Progress
priority: medium
complexity: moderate
---
Found by `fix-rain-calibration-region-borders.md` (`.gavin-root/docs/rain-scale-field.md` → Known limits).

The national rain field (`config/rain_scale_field.csv`) is fitted on gauge/reanalysis ratios where the reanalysis is Open-Meteo `era5_seamless`, because Open-Meteo serves no `era5_land` rain. Most regions score CDS ERA5-Land (`era5_land_cds`). April–November rain from `era5_seamless` is lower than CDS at the same nodes: Sicily 2019 0.893, Lazio 2020 0.952, Sardinia 2021 0.954, South Tyrol 2023 0.964, Lombardia 2024 0.979, Campania 2024 0.983, Calabria 2024 0.987, Abruzzo 2024 0.987, Molise 2024 0.986, Puglia 2024 0.968, Basilicata 2024 0.993, Veneto 2024 0.995, Valle d'Aosta 2024 1.004, Friuli 2024 1.031. So CDS regions' scaled rain runs up to 11 % wet (Sicily), 1–5 % in most, and about 3 % dry in Friuli. The measurement pooled April–November `era5_seamless` / CDS rain at a region's stored nodes; `api.weather.rain_field._reanalysis` fetches the `era5_seamless` side.

- [x] Choose the approach:
  - fit the gauge ratios against CDS rain where a CDS node series exists (the cached `raw/cds/ts_*` files, or the server's stores); or
  - fit a second smooth field of `era5_seamless`/CDS ratios at every CDS node, and divide by it for CDS rows (`PrecipitationScale.factor` per source).
  - **Chosen: the second (a per-source ratio), on the 0.2° weather lattice.** Every region still scores `era5_seamless` for its last few reanalysis days (CDS runs about 5 days behind), so one gauge field in CDS terms would mis-scale those days. The ratio has to be per node, not smooth: Sicily's nodes run 0.6–1.2 (log sd 0.12), and a node keeps its level between years (2019–21 against 2023–25: r 0.90, rms 0.06). The six pseudo-gauge fits were made against CDS, so they convert to seamless terms by dividing by the same ratio.
- [x] Build it (TDD; the ratio direction and the pseudo-gauge conversion were superseded by the flip below): `rain_field cds` measures both rains per node over April–November 2019–2025; `fit` also writes `config/rain_seamless_per_cds.csv` and moves the CDS-fitted pseudo-gauges to the seamless level; `PrecipitationScale.source_ratios` multiplies each source's factor in `load_weather` and in the history area rollup; rain normals record their source (Tuscany's are `era5_seamless`); `rules_version` hashes the ratio file; `borders` reads the field as it stood at `--before`, with CDS columns.
- [x] Measure the 14 local CDS stores. 13 done (Sicily 0.905 … Friuli 1.027, table in `docs/rain-scale-field.md` → CDS rain and the field). Veneto was cut off by Open-Meteo's daily cap (9,000 calls). The overnight script finishes it.
- [x] Measure seamless/CDS for Tuscany, Umbria, Liguria, Emilia-Romagna, Piemonte and Marche, whose CDS stores are only on the server.
  - Done overnight 2026-10-03 (and Veneto): Tuscany 0.975, Umbria 0.983, Liguria 0.982, Emilia-Romagna 0.989, Piemonte 0.994, Marche 0.971, Veneto 0.990. 892 nodes in all, pooled 0.974. Refit and `borders` ran at 04:03.
  - **Finding that reopens the approach:** Open-Meteo's `era5_seamless` rain is coarse ERA5. 60 % of nodes share their season total with a neighbour (CDS 8 %), in 2×2 blocks on the 0.2° lattice. So the per-node ratio is mostly 0.25° ERA5 blocks against ERA5-Land's 0.1° rain: Valle d'Aosta has 1.59 at one node and 0.98 one node away. Multiplying CDS by it puts those blocks into every region's history. Proposed flip: fit the gauges against CDS instead (daily CDS from the stores, no Open-Meteo quota needed), so the pseudo-gauges need no conversion, and give `era5_seamless` rows (Tuscany's history, everyone's last days) a CDS/seamless ratio, which smooths the blocks out instead of adding them. The machinery (`source_ratios`, per-source rollup, normals source) stays.
  - Reading the server was refused from this session, so `rain_field cds` fetches their nodes from CDS itself (`config/rain_field.yaml → cds_fetch`; Tuscany 91 land nodes, the rest unknown until probed). Started 2026-10-02 16:00; needs the next day's Open-Meteo budget.
  - Unattended: `scratchpad/overnight.sh` (this session's) waits for 02:00 Rome, runs `cds --region veneto`, the six regions, then `fit`. To redo it by hand: `uv run --group cds python -m api.weather.rain_field cds --region veneto --region tuscany --region umbria --region liguria --region emilia_romagna --region piemonte --region marche`, then `fit`. Downloads are cached, so a rerun only fetches what is missing.
  - Then add the seven regions to the table in `docs/rain-scale-field.md`, and remove the "CDS correction stops 30 km from the measured nodes" limit.
- [x] Flip to CDS (decided 2026-10-03):
  - [x] `collect` compares gauges with CDS rain read from the weather stores (local region stores + `rain_field/cds_store/`), not Open-Meteo `era5_seamless`; a gauge corner node no store holds is fetched (2 in Lombardia; the rest were at sea).
  - [x] Ratio file is `rain_cds_per_seamless.csv` (CDS / seamless) under `source_ratios: {era5_seamless: ...}`; the pseudo-gauge conversion is gone.
  - [x] Re-collected all ten networks (same gauge counts but Sicily 93 of 95), refit: CV log error 0.184 at 25 km, against 0.186 on seamless; national 0.93 + 0.05/km. Sicily gauge/CDS 1.03 (gauge/seamless was 1.15).
  - [x] Tests, config comments, references entry, `docs/rain-scale-field.md` (Method, The field, CDS rain and the field).
- [x] Refit, re-run `rain_field borders`, then re-score and backtest Sicily first (the largest gap).
  - [x] `borders --before HEAD`: CDS rows move −11 % (Lombardia–Trentino, 2,600 m) to +4 %, most within ±5 %; no steps.
  - [x] Sicily on the CDS fit (`cds-field`): sanity 12/14 (the October 2020 near-tie flips, 0.500 vs 0.529), window means −3 to −36 % (median −7 %), backtest of 3–4 presences says nothing. In the doc.
- [ ] Commit (code, config, both fitted CSVs, doc, card).
- [ ] Deploy and re-score every region on the server. Each region's normals must be rebuilt first (`history update` does it), so they record their source; until then they count as `era5_seamless` and a CDS region's percent-of-normal would be off by its ratio.
- [ ] Re-run the Tuscan backtest (the field card's open item; Tuscan rain moves again here).
- [x] Decision: era5_seamless rain turned out to be coarse ERA5 (2x2 blocks), so the per-node CDS ratio adds those blocks to CDS history. Flip the fit to CDS and give era5_seamless rows a CDS/seamless ratio, or ship the current version?
  Options: A) Flip: fit gauges against CDS (recommended) B) Ship the current seamless-based version
  Answer (2026-10-03): Flip: fit gauges against CDS (recommended)
