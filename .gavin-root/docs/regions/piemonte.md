# Piemonte

Region card: `region-piemonte.md` (region #6 of `feat-full-italy-coverage.md`). API id `piemonte`,
web slug `/piemonte`, ISTAT COD_REG 1, names "Piemonte" / en "Piedmont". Alps on three sides
(Marittime, Cozie, Graie, Pennine, Lepontine) and a strip of Ligurian Apennine in the south-east;
wide chestnut belts in the hills and lower valleys, beech above them, larch and spruce up to the
tree line, robinia along the plain.

Branch note: `region/piemonte` was cut from `main` and fast-forwarded onto `region/umbria` (the lane's
previous rail, PR still open when this card ran), because Umbria carries the shared weather,
sightings and onboarding fixes every new region needs (CDS time-series history, per-region
iNaturalist place, Open-Meteo snowfall fallback). Three shared commits from `region/liguria` were
taken as well: the WFS paging and one-map forest read (`2440b40`), the og-image registry script
(`4df3925`) and the openrsync fix to `deploy/rsync-region-data.sh` (from `4670306`). Once Umbria and
Liguria are merged, this branch's own diff is Piemonte's.

## Sources

**Decision: Regione Piemonte's Carta forestale regionale, edizione 2025, for both layers**
(`rp_carta_forestale` in `api/src/api/config/sources.yaml`; CC BY 4.0, "Carta forestale regionale
2025 © Regione Piemonte (IPLA)"). Checked 2026-09-25:

| candidate | what it is | verdict |
|---|---|---|
| **Carta forestale regionale 2025** (Regione Piemonte, IPLA) | The 2016 Carta forestale (1:10,000, photo-interpretation and forest management plans) updated with the forest limit of the Carta Forestale d'Italia (CFI 2020). 74,021 polygons of forest only, each with its IPLA forest category (`ca_1`, 21 categories) and type (`tf_1`, 109 types with variants). Geoportale Piemonte record `r_piemon:130b499f-…`: licence CC BY 4.0, "no limitations to public access", GeoPackage by direct download (`datigeo-piem-download.it/…/SIFOR/CF_2025.gpkg`, 194 MB) | **used** |
| Carta forestale regionale 2024 | Same method plus the "Land Cover Piemonte" layer; WMS only in its record, no download link | superseded by 2025 |
| Carta forestale 2016 | The IPLA map the later editions start from | older; 2025 carries it forward |
| ISPRA CLC 2018 IV level | National fallback, 25 ha minimum unit | not needed: the regional map is open, finer and typed |

The map covers forest only, so one map gives both the broad groups (how much of each cell is
woodland) and the habitats (which kind), from the category. There is no land-use code and no mixed
category: IPLA types a stand by its dominant species. The shrubland categories (OV arbusteti
subalpini: green alder and rhododendron; AS arbusteti planiziali, collinari e montani) are not forest
(INFC counts them as *altre terre boscate*), so they go to the transitional group, which does not
count toward the woodland mask.

| category | ha | group | habitat |
|---|---|---|---|
| CA castagneti | 212,245 | broadleaf | chestnut |
| FA faggete | 145,080 | broadleaf | beech |
| RB robinieti | 130,276 | broadleaf | exotic_broadleaf |
| LC lariceti e cembrete | 97,044 | conifer | other_conifer |
| BS boscaglie pioniere e d'invasione | 78,991 | broadleaf | mixed_broadleaf |
| AF acero-tiglio-frassineti | 49,091 | broadleaf | mixed_broadleaf |
| QR querceti di rovere | 48,046 | broadleaf | deciduous_oak |
| QV querceti di roverella | 42,843 | broadleaf | deciduous_oak |
| QC querco-carpineti | 38,769 | broadleaf | deciduous_oak |
| OV arbusteti subalpini | 33,574 | transitional | transitional_woodland_shrub |
| RI rimboschimenti | 21,549 | conifer | other_conifer |
| SP saliceti e pioppeti ripari | 17,375 | broadleaf | riparian |
| PS pinete di pino silvestre | 15,436 | conifer | mountain_pine |
| AB abetine | 15,305 | conifer | fir_spruce |
| OS orno-ostrieti | 14,563 | broadleaf | mixed_broadleaf |
| PE peccete | 9,621 | conifer | fir_spruce |
| AN alneti planiziali e montani | 5,188 | broadleaf | riparian |
| CE cerrete | 4,587 | broadleaf | deciduous_oak |
| AS arbusteti planiziali, collinari e montani | 4,164 | transitional | transitional_woodland_shrub |
| PN pinete di pino montano (uncinato) | 2,743 | conifer | mountain_pine |
| PM pinete di pino marittimo | 685 | conifer | mediterranean_pine |

Areas are from the polygons (the `ettari` column is empty). The total, 987,175 ha, matches the
region's own 986,132 ha for the 2025 edition (38 % of the region; castagneti 22 %, faggete 15 %,
robinieti 13 %, larici-cembrete 10 %, boscaglie 8 %). Checks on the less obvious codes: PM polygons
all sit at 8.48–8.84° E, 44.51–44.65° N, the Appennino alessandrino above Ovada and Voltaggio,
where maritime pine grows, so PM is *pino marittimo* and PN (western Alps) is *pino montano*. RI
types are conifer plantations (RI20A pino nero, B peccio, C larice, D douglasia, E pino silvestre;
only RI20G is red oak), so RI is `other_conifer` as in Liguria.

Credits: the map is added to the app's national credits list (`web/src/credits.ts`). The ARPA
Piemonte rain gauges feed a check only, never the app.

## Config

`api/src/api/config/regions/piemonte.yaml`:

- **Boundary.** ISTAT COD_REG 1; bbox `[6.62, 44.06, 9.22, 46.47]`, the ISTAT 2025 boundary's
  extent (6.6266, 44.0606, 9.2140, 46.4643) rounded outward to 0.01°. Region area 25,389 km².
- **Forest.** `forest.groups` and `forest.types` both on `rp_carta_forestale`, class column and
  type field `ca_1` (read once: the one-map path from `region/liguria`), mapping above.
- **iNaturalist place** 10872, "Piemonte, IT" (admin level 10), resolved by name on 2026-09-25
  (`api.inaturalist.org/v1/places/autocomplete?q=Piemonte`).
- **Gauges.** `api.weather.checks gauges --region piemonte` reads ARPA Piemonte's open daily rain
  (`api.weather.arpa_piemonte`, Validation).
- **`model:` overrides:** the rain scale, ×0.74 over `era5_land_cds` and `era5_seamless` (Validation,
  rain gauges). The gauge check asked for it: the reanalysis is wetter than the Piedmontese gauges,
  the reverse of Tuscany.
- **Weather points.** 125 land nodes on the 0.2° lattice (128 candidates), all 9,537 woodland cells
  within reach.

### Lapse rates (`api.weather.checks lattice --region piemonte`)

377 ERA5-Land land nodes at 0.1° (76–2,787 m), three 14-day windows of 2024 (Jan, Jul, Oct), run
2026-09-26. Cooling per km of height, median of the daily fits:

| variable | Jan | Jul | Oct | all | national config | difference |
|---|---|---|---|---|---|---|
| Tmin | 4.63 | 5.56 | 4.91 | **5.24** | 4.2 | **+1.04** |
| Tmax | 4.69 | 5.24 | 4.25 | **4.86** | 4.5 | +0.36 |
| Tmean | 4.53 | 5.53 | 4.77 | **5.03** | 4.5 | +0.53 |
| soil 0–7 cm | 0.38 | 4.82 | 4.09 | **4.09** | 3.7 | +0.39 |

Tmax, Tmean and soil are within 1 °C/km. **Tmin sits just over the line (+1.04)**; the same fit on the
125 stored 0.2° CDS nodes gives 5.19 (+0.99). January soil barely cools with height (0.38): snow
cover holds the topsoil near 0 °C in the Alps. **The national rates are kept, Tmin included,**
because the leave-out test shows no gain from Piemonte's own rate:

| Tmin leave-out RMSE | national 4.2 | 5.2 | fitted (all four) |
|---|---|---|---|
| served lattice (0.2°, stride 2) | 0.447 °C | 0.438 °C | 0.439 °C |
| stride 3 (0.3°) | 0.602 °C | 0.616 °C | 0.619 °C |

A 0.01 °C gain on the served lattice and a loss on the coarser one do not justify a per-region lapse
rate, which the weather config does not support yet (lapse rates are national, in `weather.yaml`).
Leave-out at the 0.2° lattice with the national rates: RMSE 0.33 °C (Tmean), 0.45 °C (Tmin), 0.36 °C
(Tmax), 0.77 °C (soil), against 0.37 / 0.48 / 0.40 / 0.77 °C with 6.5 °C/km and 0.68 / 0.74 / 0.69 /
0.97 °C with no lapse correction. Errors are about 40 % larger than Umbria's (0.25 °C Tmean): the
Alpine relief between nodes.

## Grid

`uv run python -m api.grid.build --region piemonte` (4.3 min, the DEM tiles and SoilGrids fetched
for the first time):

- **Cells 26,148; woodland 9,537** (36.5 %). Threshold sensitivity (forest share of the cell, before
  the 0.25 km² floor): 0.3 → 12,339, 0.4 → 11,018, **0.5 → 9,673**, 0.6 → 8,322, 0.7 → 6,949.
- **INFC 2015: +6.7 %** (grid 949,734 ha vs 890,433 ha bosco), inside ±10 %. The map's forest
  categories hold 949,437 ha; the gap to INFC is the regional forest definition (L.R. 4/2009 and the
  CFI 2020 limit: ≥ 2,000 m², ≥ 20 % cover) and ten years of regrowth on abandoned land, mostly
  boscaglie and robinia.
- **Habitats on woodland cells** (share of wooded area; cells where dominant; their mean height):

| habitat | share | dominant cells | mean elevation |
|---|---|---|---|
| chestnut | 25.6 % | 2,647 | 672 m |
| beech | 17.9 % | 1,712 | 1,207 m |
| mixed_broadleaf | 15.8 % | 1,254 | 1,041 m |
| deciduous_oak | 13.7 % | 1,373 | 498 m |
| other_conifer (larch, stone pine, plantations) | 12.0 % | 1,134 | 1,647 m |
| exotic_broadleaf (robinia) | 7.7 % | 928 | 281 m |
| fir_spruce | 3.0 % | 268 | 1,407 m |
| mountain_pine | 2.1 % | 169 | 1,293 m |
| transitional_woodland_shrub | 1.2 % | 9 | 1,324 m |
| riparian | 1.0 % | 39 | 347 m |
| mediterranean_pine | 0.1 % | 4 | 411 m |

  The belts are in the right order: robinia and riparian woods on the plain, oaks in the hills,
  chestnut at 670 m, beech at 1,200 m, fir and spruce at 1,400 m, larch at 1,650 m. The dominant
  habitat covers a median 71 % of the wooded area (Tuscany 89 %): Alpine cells mix belts.
  `borrowed_type_fraction` is 0 everywhere (groups and types are one map).
- **Terrain.** Woodland cells: median elevation 838 m, 95th percentile 1,774 m, max 2,307 m; median
  slope 22.8°. All have terrain; 410 have no aspect (flat or two-sided).
- **Soil pH.** Median 6.27 (5th–95th percentile 5.73–7.02); lowest under fir/spruce (6.03), beech
  and larch (6.14), highest under robinia (6.72).
- **Places.** 1,180 comuni get cells; 6 cells fall outside every comune polygon. Nearest locality
  median 1.0 km, max 8.8 km.
- **Spot checks:**

| place | cell | woodland | forest | top habitats | elev. m | comune |
|---|---|---|---|---|---|---|
| Gran Bosco di Salbertrand | `1kmE4076N2443` | yes | 0.90 | fir_spruce 0.75, other_conifer 0.21 | 1507 | Salbertrand (TO) |
| Scots pine above Oulx | `1kmE4070N2439` | yes | 0.81 | mountain_pine 0.89, other_conifer 0.08 | 1282 | Oulx (TO) |
| Chestnut slopes of Garessio | `1kmE4163N2346` | yes | 0.79 | chestnut 0.93, deciduous_oak 0.07 | 704 | Garessio (CN) |
| Val Casotto | `1kmE4154N2352` | yes | 1.00 | chestnut 0.91, beech 0.09 | 1046 | Pamparato (CN) |
| Bosco della Partecipanza, Trino | `1kmE4185N2458` | yes | 0.54 | deciduous_oak 1.00 | 151 | Trino (VC) |
| Capanne di Marcarolo | `1kmE4223N2382` | yes | 0.89 | other_conifer 0.78 (plantations), deciduous_oak 0.19 | 832 | Bosio (AL) |
| Oasi Zegna | `1kmE4175N2509` | yes | 1.00 | beech 0.45, mixed_broadleaf 0.39, other_conifer 0.16 | 1098 | Valdilana (BI) |
| Bobbio Pellice | `1kmE4091N2414` | yes | 0.86 | other_conifer 0.39, chestnut 0.30 | 947 | Bobbio Pellice (TO) |
| Santa Maria Maggiore (village) | `1kmE4201N2559` | no | 0.18 | — | 837 | Santa Maria Maggiore (VB) |
| Torino (city) | `1kmE4138N2442` | no | 0.00 | — | 246 | Torino (TO) |

## Weather history

From the Copernicus CDS, 2016-01-01 to 2026-09-14, through the ERA5-Land time-series product
(`cds.method: timeseries`): 125 node requests, 27 of them already cached by Liguria's lane (the
nodes the two regions share), 98 fetched at 20–80 s each, 89 min in all. The days after 2026-09-14
come from the Open-Meteo update step, as for every region.

**Snowfall.** The time-series product has none, and the gridded dataset's queue was stuck on
2026-09-25 as it was for Umbria and Liguria (a one-request probe for 1–14 Sep 2026, Italy-wide, sat
in "accepted" for over an hour while the node series ran). So the node backfill ran with
`--skip-snowfall`, and snowfall is filled from the Open-Meteo archive once the daily call budget
allows (see Data); CDS snowfall, if the queued Italy-wide requests ever finish, outranks it.

## Data

- cells: 26148
- woodland cells: 9537
- INFC deviation: +6.7% (grid 949,734 ha vs 890,433 ha) — within ±10 %
- weather nodes: 125
- years stored: 2016–2026 (11 years)
- sightings kept: 104
- backtest AUC (auc_local, model, all): gallinacci 0.519, ovoli 0.558, porcini 0.558
- sanity contrasts: 9/14 passed

## Validation

### Rain gauges (`api.weather.checks gauges --region piemonte`)

ARPA Piemonte's open daily rain (CC BY 4.0, "Fonte: Arpa Piemonte"), read from its Meteoweb REST API
(`api.weather.arpa_piemonte`): 323 measuring points with a rain gauge, 153 of them in woodland cells,
**97** with valid rain on 80 % of the days of 2019–2025, at 270–2,280 m (8 below 400 m, 38 at
400–800 m, 51 above). The stations carry their height. Per ARPA's data guide (*Banca Dati Storica —
Guida alla lettura dei dati*, v1.7) a daily total is the rain of 00–24 **UTC**, so the model's
calendar days are re-cut as for ARPA Liguria (median daily correlation 0.797 against 0.794 on
calendar days: the cut barely matters at this scale). Only rain marked OK (class `0` or `Z`) counts;
snowfall (`5`), snow melted in the gauge (`3`), uncertain and unusable days are left out of both
sides.

- **ERA5-Land (CDS) holds 1.33 of the gauge rain** (pooled 2019–2025; median per gauge 1.36, daily
  correlation 0.80, 3-day wet-window hit rate 0.92, false alarms 0.19). The same in every height
  band (1.28 below 400 m, 1.34 at 400–800 m, 1.33 above), so height has no part in it; by year it
  runs from 1.14 (wet 2024) to 1.67 (dry 2022).
- **It rains too often, and too little when it pours.** The reanalysis has 1 mm or more on 51 % of
  days against the gauges' 25 %, and 5 mm or more on 1.6 times as many days. On gauge days under
  5 mm it gives six times the gauge rain; on gauge days of 20 mm or more, 0.70 of it. The totals are
  high because of the drizzle, which is also why the ratio is highest in dry years.
- **The national rain scale does not fit.** 1.28 + 0.29 per km (fitted on Tuscan gauges, applied to
  `era5_seamless` only) would make Piedmontese rain **2.05** times the gauges'. A least-squares fit of
  gauge totals on model totals × (a + b × km, capped at 1.7 km as the national scale is) over
  2019–2025 gives **a = 0.733, b = 0.007 per km**; a factor alone gives 0.740. So `piemonte.yaml` sets
  `model.precipitation_scale` to **0.74, no height term**, over both `era5_land_cds` and
  `era5_seamless` (Piemonte's history is CDS). Pooled ratio 1.33 → 0.98, every band 0.94–1.03.
  Fitted on 2019–2024 alone it gives 0.76 and holds 2025 at 1.02.
- **What a factor cannot fix.** The rules read rain as 3-day totals (the rain trigger ramps from 10
  to 30 mm), 30-day totals (ovoli 25 → 75 mm, gallinacci 15 → 70 mm), a count of 5 mm days
  (gallinacci) and, for porcini, the 30-day total as a percentage of the cell's normal, which no
  scale changes. Share of windows at or above each threshold:

| | gauges | raw | × 0.74 (shipped) | × 0.85 |
|---|---|---|---|---|
| 3-day ≥ 10 mm | 21.9 % | 34.6 % | 27.7 % | 30.8 % |
| 3-day ≥ 30 mm | 8.6 % | 11.1 % | 6.7 % | 8.5 % |
| 30-day ≥ 25 mm | 64.5 % | 87.3 % | 81.0 % | 84.3 % |
| 30-day ≥ 75 mm | 31.3 % | 49.2 % | 35.3 % | 41.8 % |

  ×0.85 would match the frequency of the 30 mm trigger but leave every 30-day threshold a third too
  often met; ×0.74 (the totals fit, the method Tuscany, Liguria and Umbria used) is closer
  everywhere but makes 30 mm events a fifth too rare. The totals fit ships. Correcting the drizzle
  itself (a wet-day threshold or quantile mapping per region, from every region's open gauges) is a
  cross-region follow-up, like the calibration step at the Tuscan–Umbrian border.

### Backtest (priors: rules version `4c220f432f29`)

Run 2026-09-26 on the stores above: the onboard's hold-out run (`backtest/piemonte/onboard/`) and
the train seasons (`--seasons train --label onboard-train`). Scores cover 9,537 cells × 3,845 days
(2016-03-18 to 2026-09-26), none without weather.

**Usable presences (unique, unobscured group-cell-day sightings on woodland cells) in the train
seasons 2016–2023: 53** (porcini 37, gallinacci 9, ovoli 7; none in 2016–2017), just over the 50 the
card asks before tuning, so the pre-registered tuning ran (Tuning, below); nothing it found held on
the hold-out, so the priors ship. The hold-out 2024–2025
holds 27 (porcini 15, gallinacci 9, ovoli 3).

| group | split | n | `auc_local` model | habitat | `auc_time_effort` model | calendar | `auc_region` model | habitat |
|---|---|---|---|---|---|---|---|---|
| porcini | train | 37 | 0.523 (0.46–0.59) | 0.529 | 0.459 (0.39–0.53) | 0.481 | 0.695 | 0.533 |
| ovoli | train | 7 | 0.753 (0.63–0.86) | 0.633 | 0.769 (0.67–0.86) | 0.605 | 0.950 | 0.720 |
| gallinacci | train | 9 | 0.564 (0.42–0.70) | 0.567 | 0.551 (0.44–0.66) | 0.514 | 0.836 | 0.542 |
| porcini | hold-out | 15 | 0.558 (0.48–0.64) | 0.561 | 0.543 (0.45–0.64) | 0.514 | 0.795 | 0.533 |
| ovoli | hold-out | 3 | 0.558 (0.34–0.77) | 0.645 | 0.272 (0.20–0.34) | 0.442 | 0.888 | 0.720 |
| gallinacci | hold-out | 9 | 0.519 (0.37–0.66) | 0.540 | 0.498 (0.36–0.63) | 0.564 | 0.801 | 0.542 |

- **Where, region-wide:** the model ranks the finders' cells well against the whole region
  (`auc_region` 0.70–0.95), well above habitat alone (0.53–0.72): the altitude bands and season
  windows put the Piedmontese sightings in the right belts.
- **Where, locally, and when:** within 20 km on the day (`auc_local`) and across the season at the
  finder's cell (`auc_time_effort`) the model is at habitat or calendar level for porcini and
  gallinacci, as in Tuscany and Liguria. Ovoli's train figures are the best of any group so far but
  rest on 7 presences, and its 3 hold-out presences go the other way on timing.
- Combined-score winners over the hold-out cell-days that have one: gallinacci 51 %, porcini 39 %,
  ovoli 10 %; 46 % of cell-days have no group in season (the Alpine winter is long).

### Tuning (pre-registered rain search, 2026-09-26)

With 53 usable train presences the card's protocol applies, as Model v1 ran it for Tuscany (55):
`api.model.tuning --region piemonte --search rain`, one pass of coordinate descent on the train
seasons 2016–2023, an alternative kept only if it raises the group's objective (mean of pooled
`auc_local` and `auc_time_effort`) by at least 0.02, season windows, altitude bands and habitat
affinities frozen; run once with the rain scale as configured (`tuned-rain`) and once without
(`tuned-rain-scale-off`); a winner judged once on the hold-out. Porcini's 30-day rain was already
relative to the cell's normal (Tuscany's tuning), so its `higher` alternatives move a
percentage-of-normal ramp and `relative` equals the prior.

| trial (train objective) | scale on (×0.74) | scale off |
|---|---|---|
| start | porcini 0.491, ovoli 0.761, gallinacci 0.557 | 0.482, 0.724, 0.562 |
| porcini trigger ×1.5 / ×2 | 0.502 / 0.475 | 0.491 / 0.502 |
| porcini `rain_30d` higher / much higher | 0.486 / 0.490 | 0.483 / 0.487 |
| porcini clock cooler / warmer | 0.482 / 0.481 | 0.480 / 0.494 |
| ovoli trigger ×1.5 / ×2 | 0.774 / 0.726 | 0.767 / **0.773** (kept) |
| ovoli `rain_30d` ×1.5 / ×2 / relative | 0.705 / 0.623 / 0.724 | 0.762 / 0.737 / 0.758 |
| ovoli clock cooler / warmer | 0.760 / 0.747 | 0.775 / 0.686 |
| gallinacci trigger ×1.5 / ×2 | 0.507 / 0.501 | 0.543 / 0.491 |
| gallinacci `rain_30d` ×1.5 / ×2 / **relative** | 0.570 / 0.587 / **0.595** (kept) | 0.565 / 0.586 / **0.612** (kept) |
| gallinacci clock cooler / warmer | 0.609 / 0.580 | 0.613 / 0.608 |
| gallinacci sun line off | 0.595 | 0.611 |

- **The rain scale stays on.** The runs end at a mean of 0.616 (scale on) and 0.622 (scale off), 0.006
  apart, under the margin; the scale is fitted to gauges, not sightings. Without it, ovoli ask for
  a doubled trigger ramp (+0.049), which is what the ×0.74 scale already does to the rain (with it,
  the same change gains only +0.013).
- **The one candidate, gallinacci's 30-day rain relative to the cell's normal** (0 at 50 %, full from
  125 %), won under both scalings, on 9 presences. **On the hold-out it lost**: objective 0.508 →
  0.483 (`auc_local` 0.519 → 0.454, `auc_time_effort` 0.498 → 0.512; 9 presences,
  `backtest/piemonte/tuned-holdout/`). A change the hold-out does not confirm is not shipped (as
  Tuscany's ovoli trigger), so **nothing is tuned: the researched priors ship** (rules version
  `4c220f432f29`, the one the stores were scored with).

### Press contrasts (`sanity.yaml`, porcini, `backtest/piemonte/onboard/sanity_porcini.csv`)

**9 of 14 hold.**

| contrast | higher | lower | holds |
|---|---|---|---|
| `biellese_2025_2024` | 0.703 | 0.107 | yes |
| `valsesia_2022_2021` | 0.553 | 0.467 | yes |
| `valsesia_ossola_2023_late` | 0.585 | 0.580 | yes (barely) |
| `alto_piemonte_vs_valsusa_2023` | 0.756 | 0.671 | yes |
| `torinese_vs_valsesia_ossola_june_2024` | 0.727 | 0.788 | no |
| `cuneo_valleys_2023_2024_vs_2021` | 0.762 | 0.216 | yes |
| `cuneo_valleys_spring_2022_2021` | 0.345 | 0.535 | no |
| `valle_po_2025` | 0.933 | 0.635 | yes |
| `cuneo_border_july_2024_2025` | 0.520 | 0.203 | yes |
| `alto_tanaro_vs_marittime_2020` | 0.439 | 0.491 | no |
| `marittime_vs_langhe_roero_2023` | 0.026 | 0.178 | no |
| `alessandria_valleys_vs_acquese_2020` | 0.473 | 0.539 | no |
| `acquese_ovadese_2021` | 0.415 | 0.153 | yes |
| `marcarolo_vs_cuneese_october_2021` | 0.732 | 0.204 | yes |

- The good and bad years hold, often by wide margins (Biellese 2025/2024, Cuneo valleys 2023–24/2021,
  the 2021 drought in the Acquese and the Cuneese against the October flood near Marcarolo).
- **Three misses are rain the reanalysis does not resolve** (factor breakdown re-scored in memory):
  - `marittime_vs_langhe_roero_2023`: on the Alpi Marittime cells (440, median 1,355 m) the 3-day
    rain trigger is 0 on 78–87 % of cell-days (median 3-day total about 7 mm) and the 30-day rain is
    41 % of normal; season, habitat, altitude and temperature are open. The "unica doccia utile" was
    local storms a ~9 km reanalysis misses.
  - `alessandria_valleys_vs_acquese_2020`: the 241 mm at Fraconalto on 29 August, with 2 mm "a
    pochissima distanza", is not in the reanalysis: the south-eastern valleys get 76 % of their
    normal 30-day rain against the upper Acquese's 87 %.
  - `alto_tanaro_vs_marittime_2020`: both sides get about their normal rain (104 % and 106 %), so the
    local drought "verso le Alpi Marittime" is not there to score.
- **One is a gap in the rules:** `torinese_vs_valsesia_ossola_june_2024` claims too much rain held
  red porcini back in Valsesia and the Ossola (30-day rain 132 % of normal, 3-day totals of about
  40 mm); no rule lowers a score for excess rain, so the wetter side scores higher.
- **One the weather cannot show:** `cuneo_valleys_spring_2022_2021` credits the spring 2022 flush to
  the woods recovering after more than a year of drought; the reanalysis rain of the two springs is
  alike (81 % and 77 % of normal), and the rules keep no memory of a long drought.

## Known limitations

- **Region finder by bbox.** The web registry finds a region by bbox (`findRegionAt`), and
  Piemonte's bbox (6.62–9.22° E, 44.06–46.47° N) takes in western Lombardy (Milan, Varese, Pavia),
  Genoa, the Aosta Valley and parts of Switzerland and France. Until those regions are served, a GPS
  fix or a search there is offered Piemonte (Genoa goes to Liguria once it is registered before
  Piemonte). The web test for "a fix outside every region" moved from Milan to Munich for this
  reason. A boundary-polygon lookup would fix it for every pair of neighbours.
- **Drizzle.** The reanalysis rains too often and too little when it pours (Validation, rain
  gauges); a factor cannot fix both.
- **Convective rain.** Local summer storms that a ~9 km reanalysis misses cost three press contrasts.
- **Larch.** A pure larch cell gets full *B. edulis* habitat credit, because the habitat factor
  saturates at a 0.3 affinity share and larch (`other_conifer`) sits at 0.3
  (`species-ecology/piemonte.md`). If Alpine cells score too high once the season can be watched,
  larch at 0.1 is the first knob.
- **Lapse rates.** Minimum temperature cools 1.04 °C/km faster with height than the national rate
  (Config, Lapse rates), without a measurable downscaling gain from the regional rate.
