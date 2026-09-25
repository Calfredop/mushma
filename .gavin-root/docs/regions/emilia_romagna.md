# emilia_romagna

Emilia-Romagna (slug `emilia-romagna`, API id `emilia_romagna`, ISTAT COD_REG 8). Region card:
`region-emilia-romagna.md`; species evidence: `.gavin-root/docs/species-ecology/emilia_romagna.md`.

## Forest source

**Decision: the regional Carta forestale 2025 alone, for both how much forest and which kind.** No
CLC.

| | Regione Emilia-Romagna, Carta forestale regionale 2025 |
|---|---|
| Detail | photo-interpreted at 1:10,000 (checked at 1:5,000) from the AGEA 2023 flight; minimum unit 0.16 ha |
| Approved | Determinazione n. 6273 of 31/03/2026, which also fixes the method |
| Classes | land use `STC_RER` (bosco, arbusteti in evoluzione, arboricoltura…) and the INFC forest category `COD_CAT` (faggete, cerrete, boschi di roverella, castagneti, ostrieti, pinete…) |
| Licence | CC BY 4.0: the Regione's environment site, which publishes the shapefiles, releases its contents under CC BY 4.0 unless stated otherwise (Note legali); the shapefiles state no other licence |
| Access | nine provincial zips (RDN2008 / UTM 32N, 181 MB), no login; the loader reads them as one source (`download.parts`) |
| Forest area | 596,026 ha of bosco, 603,201 ha with chestnut orchards and temporarily bare woods |

Why it beats the CLC fallback here: it is 2023 imagery at 1:10,000 against CLC's 2018 at 25 ha,
and its forest categories map straight onto the rule habitats. Types come from the same polygons as
the forest mask, so no cell borrows its forest types from its neighbours (Tuscany: 4.7 % on
average).

Checked and not used: the Regione's CKAN portal (dati.emilia-romagna.it) lists only the 1986 and
2003 Bologna provincial forest maps (CC BY 3.0); the DBTR "Bosco" layer (CC BY 4.0) has no forest
types; the forest map's WMS has no WFS or ArcGIS feature service behind it.

Mapping (region config `api/src/api/config/regions/emilia_romagna.yaml`):

- **Forest** = land uses 11 bosco, 12b/12c/12d/12f (woods temporarily bare, owed or compensatory
  replanting, woods along infrastructure), 26 chestnut orchards, 99 boschetto. Split into broadleaf
  or conifer by forest category, then into habitats by the same category (faggete → beech; cerrete,
  roverella, rovere, farnia → deciduous_oak; castagneti → chestnut; ostrieti, carpineti,
  acero-frassineti, other deciduous → mixed_broadleaf; riparian poplar, willow, alder, ash-elm →
  riparian; robinieti and plantations → exotic_broadleaf; leccete → evergreen_oak; black, Scots and
  mountain pine → mountain_pine; maritime and stone pine, cypress → mediterranean_pine; fir and
  spruce (incl. abieti-faggeti) → fir_spruce; larch and exotic conifers → other_conifer).
- **Transitional** = land use 210 "Area a vegetazione boschiva ed arbustiva in evoluzione", which
  is CLC 324's own name. Kept as a habitat fraction, not counted as woodland (same rule as
  Tuscany).
- **Left out**, like the national inventory's "bosco": tree farming and poplar plantations (21, 22a,
  22p, 23), hazel orchards (25), grassland (27), heath and scrub (28), parks (44).

## Grid

Built with `uv run python -m api.grid.build --region emilia_romagna` (about 3 minutes).

- 23,231 cells; inside area 22,501.8 km², the ISTAT region area.
- **INFC 2015 bosco: grid 602,901 ha vs 584,901 ha (+3.1 %)**, within ±10 %. The raster count
  matches the vector total (603,201 ha) to 0.05 %.
- **5,900 woodland cells** (forest ≥ 50 % of the cell's inside area and ≥ 0.25 km²). Parma 1,577,
  Forlì-Cesena 1,072, Bologna 927, Piacenza 886, Reggio Emilia 570, Modena 534, Ravenna 171,
  Rimini 152, Ferrara 11.

  | minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
  |---|---|---|---|---|---|
  | woodland cells | 8,239 | 7,069 | **5,893** | 4,748 | 3,648 |

  (Recomputed from the stored fractions; the built count is 5,900.)
- Habitats on woodland cells:

  | habitat | share of wooded area | cells where dominant | mean elevation of those cells |
  |---|---|---|---|
  | deciduous_oak | 36.7 % | 2,585 | 607 m |
  | beech | 21.8 % | 1,299 | 1,176 m |
  | mixed_broadleaf | 20.1 % | 1,317 | 590 m |
  | chestnut | 8.1 % | 405 | 750 m |
  | mountain_pine | 4.6 % | 160 | 606 m |
  | transitional_woodland_shrub | 2.9 % | 7 | 788 m |
  | exotic_broadleaf | 1.8 % | 55 | 353 m |
  | riparian | 1.6 % | 24 | 305 m |
  | fir_spruce | 1.4 % | 16 | 1,139 m |
  | mediterranean_pine | 0.4 % | 23 | 34 m |
  | other_conifer | 0.3 % | 6 | 767 m |
  | evergreen_oak | 0.1 % | 3 | 3 m |

  The belts read as the northern Apennines should: oaks and hop-hornbeam in the hills, chestnut
  around 750 m, beech and fir above 1,100 m, and the coastal pinewoods and holm oak of Ravenna and
  Mesola at sea level. Beech holds a larger share than in Tuscany (8.5 %), evergreen oak and macchia
  almost none. The dominant habitat covers a median 70 % of a cell's wooded area.
- Terrain: elevation median 701 m (max 1,706 m), slope median 18.4°; 163 cells have no aspect
  (flat or two-faced). Soil pH median 6.60 (5th–95th percentile 5.99–7.03). 161 comuni have
  woodland cells; 8 coastal slivers fall outside every comune; nearest locality median 1.1 km.

## Weather

- **Lattice.** 92 candidate nodes at 0.2°, 86 on land; every woodland cell within reach.
- **Lapse rates: national rates kept** (`uv run python -m api.weather.checks lattice --region
  emilia_romagna`, 236 land nodes at 0.1°, three 14-day windows of 2024). Median of the daily
  fits of cooling with height, against the national config:

  | variable | January | July | October | all | national | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 3.25 | 5.47 | 4.16 | 4.55 | 4.5 | +0.05 |
  | temperature_2m_mean | 2.08 | 4.79 | 3.96 | 4.10 | 4.5 | −0.40 |
  | temperature_2m_min | 1.82 | 3.12 | 3.54 | 3.14 | 4.2 | **−1.06** |
  | soil_temperature_0_to_7cm_mean | 2.08 | 3.86 | 3.27 | 3.32 | 3.7 | −0.38 |

  Minimum temperature's fit is just past the card's 1 °C/km line, and it was **kept anyway**:
  - The low figure comes from January, when inversions over the Po plain nodes flatten or reverse
    the gradient (daily fits range −0.15 to 5.6, SD 2.1). In the seasons the rules score, July and
    October, the fits are 3.1 and 3.5.
  - Using 3.1 °C/km makes the leave-out test **worse**: minimum temperature RMSE 0.445 vs 0.435 °C
    at the 0.2° lattice, 0.594 vs 0.587 °C at 0.3°. Using every fitted rate changes no other
    variable by more than 0.004 °C.
  - A regional rate would also need a per-region lapse override, which the weather config does not
    have. Not worth adding for a rate that predicts worse.

  With the national rates, the 0.2° lattice's leave-out RMSE is 0.29–0.44 °C for air temperature
  (0.49–0.57 °C with no height correction), 0.32 °C for soil temperature and 1.9 mm for daily rain.

- **History.** Copernicus ERA5-Land from the CDS time-series product, one request per node for
  2016-01-01 to 2026-09-14 (86 nodes, 3.36 M daily values). Snowfall, which that product lacks, comes
  from the Open-Meteo ERA5 archive (`era5_seamless`, 2,402 weighted calls) while the CDS gridded
  queue was jammed; the store takes each variable from its best source, so CDS snowfall wins if
  it is fetched later. A spot check at four nodes over 23 Aug to 13 Sep 2026 against the weekly
  gridded chunks matched every instantaneous variable to float32 precision. The chunk path was the
  wrong one where they differed: it misses the previous evening on each chunk's first day, and its
  deaccumulation dropped a wet 00-01 UTC hour (4.4 mm on 10 Sep; fixed in `cds.py`).
- **Rain gauges: a regional rain scale** (`uv run python -m api.weather.checks gauges --region
  emilia_romagna`). ARPAE-SIMC publishes every station's observations as open data (CC BY 4.0,
  dati.arpae.it "Meteo - dati osservati"). Its daily totals ending at 08:00 UTC are 09:00-09:00 CET
  days, the same cut as SIR Toscana's. 66 gauges sit in woodland cells with at least 80 % of days
  (median 716 m).

  | | below 400 m | 400-800 m | above 800 m | all |
  |---|---|---|---|---|
  | gauges | 7-8 | 33-34 | 25 | 66 |
  | raw ERA5-Land / gauge, 2025 | 1.06 | 0.94 | 0.69 | 0.82 |
  | raw ERA5-Land / gauge, 2026 (Jan-Aug) | 1.06 | 0.89 | 0.66 | 0.79 |
  | Tuscan scale (1.28 + 0.29/km), 2025 / 2026 | 1.45 / 1.44 | 1.36 / 1.29 | 1.09 / 1.05 | **1.23 / 1.18** |
  | **Emilia-Romagna scale (0.62 + 0.80/km)**, 2025 / 2026 | 0.91 / 0.91 | 1.04 / 0.99 | 1.00 / 0.96 | **1.01 / 0.97** |

  ERA5-Land is about right in the low hills and increasingly dry with height, far more steeply
  than in Tuscany. The Tuscan scale would make the region's woodland rain about a fifth too wet,
  so `emilia_romagna.yaml` overrides `model.precipitation_scale`: fitted on 2025, checked on
  2026. The fit weights every gauge equally (OLS of each gauge's ratio on elevation). Tuscany's
  totals fit gives the same pooled result, a = 0.534, b = 0.881, but leaves the lowland gauges 16 %
  dry. It scales the CDS history and the Open-Meteo reanalysis days that bridge its lag; forecast
  rain stays unscaled, as nationally. Over woodland cells the factor runs 0.85-1.68 (5th-95th
  percentile, median 1.18). The 1.3 % of woodland below the lowest gauge (183 m, mostly the
  Ravenna and Mesola coastal woods) is extrapolated. Daily correlation with the gauges is 0.63-0.66
  and 3-day wet windows are caught 71-83 % of the time: the scale fixes totals, not timing.

## Data

- cells: 23231
- woodland cells: 5900
- INFC deviation: +3.1% (grid 602,901 ha vs 584,901 ha) — within ±10 %
- weather nodes: 86
- years stored: 2016–2026 (11 years)
- sightings kept: 28
- backtest AUC (auc_local, model, all): gallinacci 0.813, ovoli 0.554, porcini 0.372
- sanity contrasts: 10/12 passed

## Sightings

`uv run python -m api.sightings.ingest fetch --region emilia_romagna` (GBIF over the region's bbox,
iNaturalist place 96905 "Emilia-Romagna, IT", resolved by name on 2026-09-25):

- GBIF 152 records, iNaturalist 4 not already in GBIF; 131 pass the quality filters (3 undated, 24
  too imprecise, 23 of unknown precision dropped).
- **28 stored on woodland cells.** The bbox reaches into Tuscany, Liguria and Lombardy: of GBIF's
  kept records, 90 fall outside the region and 13 inside it but off woodland (mostly mountain
  villages such as Pievepelago and Albareto).
- Usable presences (unique, unobscured group-cell-days) by season:

  | season | porcini | ovoli | gallinacci |
  |---|---|---|---|
  | 2018 | 1 | 0 | 0 |
  | 2019 | 1 | 0 | 0 |
  | 2020 | 1 | 0 | 3 |
  | 2021 | 2 | 0 | 0 |
  | 2022 | 2 | 0 | 1 |
  | 2023 | 1 | 0 | 1 |
  | 2024 | 3 | 1 | 1 |
  | 2025 | 3 | 1 | 0 |
  | 2026 | 1 | 0 | 3 |

  **Train seasons 2016–2023: 13 presences** (porcini 8, gallinacci 5, ovoli 0); hold-out 2024–2025:
  9. The card tunes only at 50 or more, so the researched priors ship untuned.

## Validation

**No tuning: the priors ship.** The train seasons (2016-2023) hold 13 usable presences (porcini 8,
gallinacci 5, ovoli 0), against the card's floor of 50. The species files stay `draft`, with the
researched windows, bands and affinities (`.gavin-root/docs/species-ecology/emilia_romagna.md`).

Backtest (`api.model.backtest run --region emilia_romagna`; stores under
`backtest/emilia_romagna/{priors,onboard}`): the model against the calendar baseline (every gate,
weather taken out) and habitat alone, AUC with the model's 95 % bootstrap interval.

| group | seasons | presences | metric | model (95 % CI) | calendar | habitat |
|---|---|---|---|---|---|---|
| porcini | train 2016-23 | 8 | auc_region | 0.84 (0.78-0.89) | 0.80 | 0.50 |
| | | | auc_local | 0.62 (0.43-0.79) | 0.53 | 0.50 |
| | | | auc_time_effort | 0.60 (0.51-0.69) | 0.52 | 0.50 |
| porcini | hold-out 2024-25 | 6 | auc_region | 0.81 (0.74-0.88) | 0.68 | 0.50 |
| | | | auc_local | 0.37 (0.20-0.57) | 0.42 | 0.50 |
| | | | auc_time_effort | 0.43 (0.32-0.53) | 0.53 | 0.50 |
| gallinacci | train | 5 | auc_region | 0.81 (0.73-0.89) | 0.68 | 0.62 |
| | | | auc_local | 0.31 (0.14-0.46) | 0.28 | 0.54 |
| | | | auc_time_effort | 0.58 (0.51-0.65) | 0.54 | 0.50 |
| gallinacci | hold-out | 1 | auc_region / local / time | 0.84 / 0.81 / 0.55 | 0.67 / 0.82 / 0.47 | |
| ovoli | hold-out | 2 | auc_region / local / time | 0.93 / 0.55 / 0.60 | 0.89 / 0.59 / 0.64 | |

What this supports:
- **Where and in which season: yes.** `auc_region` is 0.81-0.93 in every group and period, above
  both habitat alone and the calendar baseline in all five rows.
- **When, within the season: a hint on train only.** On the train seasons the weather lifts timing
  a little above the calendar baseline (porcini 0.60, gallinacci 0.58, both intervals above 0.5). On
  the six hold-out porcini it does not (0.43). One or two sightings move these numbers by 0.1.
- **Which of the nearby woods: no signal.** `auc_local` straddles 0.5 with intervals 0.3-0.4 wide.
  Gallinacci sit below it on train. All five records are in beech at 1,200-1,520 m (Ferriere,
  Sestola, Albareto), on the ramp of the altitude band (full to 1,300 m, zero at 1,800 m), so the
  lower woods around them outscore them. A hint that the band's top is low for the Emilian
  beech belt. The card and the PRD keep altitude bands frozen, and five records are no basis to
  move it: recheck when more records exist.

**Sanity check: 10 of 12 press contrasts hold** (porcini group, `api.model.sanity`, contrasts and
sources in `api/src/api/config/species/emilia_romagna/sanity.yaml`):

| contrast | higher | lower | holds |
|---|---|---|---|
| Cerreto Laghi, early October: 2017 (200 kg) over 2016 (30 kg) | 0.96 | 0.73 | yes |
| Reggio-Parma crinale, mid-September 2019 against normal years | 0.96 | 0.80 | yes |
| Mid-September 2019: Reggio side ahead of the Taro and Ceno valleys | 0.96 | 0.77 | yes |
| First half of August 2018: Val Ceno and Berceto ahead of Albareto | 0.50 | 0.58 | **no** |
| Taro valley, first half of August 2017: drought, no summer flush (normal over 2017) | 0.60 | 0.20 | yes |
| Alta Val Nure, late August to mid-September 2022: best in twenty years | 0.95 | 0.63 | yes |
| Modena Apennines, same window 2022: a record year | 0.93 | 0.61 | yes |
| Early October 2023: Ligurian border ahead of Modena to San Marino | 0.32 | 0.23 | yes |
| Pievepelago 2024: mid-July flush over the early-August drought pause | 0.61 | 0.54 | yes |
| Val Trebbia 2025: early September over the short mid-August flush | 0.98 | 0.64 | yes |
| Parma Apennines 2020: a rich September over an October stopped by storms and tramontana | 0.66 | 0.87 | **no** |
| Alto Savio 2024: among the most copious seasons in decades | 0.86 | 0.61 | yes |

The two misses:
- **Val Ceno vs Albareto, August 2018.** Neighbouring valleys, which the model ranks the other
  way round (0.50 vs 0.58). One contrast; not investigated further.
- **October 2020.** No rule reads wind. The drying stopper counts days with ET0 of 4 mm or more
  in the past week, which a cold October tramontana rarely reaches, so the storms-then-wind spell
  that stopped the flush still scores well.

Mean September-October porcini score by year follows the press: lowest in 2023 (0.31), when the
October reports say "quasi assenti", and highest in 2024 (0.87), the Alto Savio's record year.
The 2017 drought sits low too (0.48), and 2019 and 2022 high (0.73, 0.66).

## After the deploy

The rail pushes the branch, opens the PR and, after the merge, deploys main with the daily job.
Then check:

- [ ] `https://mappafunghi.app/emilia-romagna` and its species pages (`/porcini`, `/ovoli`,
      `/gallinacci`) show real scores, not the empty state; `/status?region=emilia_romagna` has
      today's date.
- [ ] The hub (`/`) lists Emilia-Romagna and colours it from `/overview`; `/regions` includes
      `emilia_romagna`.
- [ ] `https://mappafunghi.app/sitemap.xml` lists `/emilia-romagna` and its three species pages.
- [ ] Lighthouse SEO is 100 on `/emilia-romagna`.
- [ ] The next morning's daily job has a `region_done` line for `emilia_romagna`
      (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.
- [ ] The credits page lists "Regione Emilia-Romagna — Carta forestale regionale".
