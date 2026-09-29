# Valle d'Aosta

Region card: `region-valle-d-aosta.md` (region #7 of `feat-full-italy-coverage.md`). API id
`valle_d_aosta`, web slug `/valle-d-aosta`, ISTAT COD_REG 2, names "Valle d'Aosta" / en "Aosta
Valley". The smallest region (3,261 km²) and wholly Alpine: the Dora Baltea valley from Courmayeur
to Pont-Saint-Martin and its side valleys, officially bilingual (Italian and French place names).
Larch is its commonest forest, then spruce and Scots pine; beech, chestnut and oaks only low in the
Bassa Valle and on warm slopes. The central valley is one of the driest in the Alps (Aosta about
550 mm a year).

The only region so far with **two groups**: porcini and gallinacci. Ovoli (and *B. aereus*) have
no record in the region from any source, so its rules have no ovoli group and the web registry
offers two species (`species-ecology/valle_d_aosta.md`, Keys and groups dropped).

## Sources

**Decision: the Region's Carta forestale, Tipi forestali 2020 (IPLA), for both layers, saved by
hand** (`rvda_tipi_forestali` in `api/src/api/config/sources.yaml`; CC BY 4.0, "Dati estratti dal
Repertorio cartografico SCT della Regione Autonoma Valle d'Aosta"). Checked 2026-09-29:

| candidate | what it is | verdict |
|---|---|---|
| **Tipi forestali 2020** (Regione Autonoma Valle d'Aosta, Struttura forestazione; IPLA) | The regional forest map on the IPLA typology shared with Piemonte, made in 2021 from the 2012 orthophotos checked against 2018–2020 imagery, at 1:5,000 for a 1:10,000 map (1 ha mapping unit, isolated polygons to 0.2 ha): forest only, each polygon with its category (`ca`, 17 categories) and type. Geoportale SCT record `r_vda:04259-META:20211029:091000`. In the SCT **Repertorio cartografico**, whose data the Region licenses CC BY 4.0 (DGR 899/2014, DGR 1620/2016; `CC_BY_Repertorio_SCT_Outil_v3.pdf`), but the vector file is served only to registered users signed in with SPID (SCT-Outil), and the `Forestazione` WFS lists no feature type (WMS only; GetFeatureInfo returns attributes without geometry) | **used**, downloaded once by the human |
| Tipi forestali 2011 (Renerfor) | The first map on the same typology | superseded by 2020 |
| Carta di copertura del suolo VDA 2020/2022/2024 (Sentinel-2, EAGLE, 10 m) | Land cover to the IV level, CC BY 4.0, same SPID-gated Repertorio | no forest types |
| ISPRA / ARPA VdA, Carta della Natura, carta degli habitat 1:50,000 (2007) | CORINE Biotopes habitats (42.331 larch, 42.21 subalpine spruce, 42.53/42.55 Scots pine…), CC BY 4.0, readable by bbox from ISPRA's national GeoPackage without a login | the open fallback: coarser and 13 years older |
| ISPRA CLC 2018 IV level | National fallback, 25 ha minimum unit | **−25.5 % against INFC** (provisional grid, 73,946 ha against 99,243 ha): not enough |

The human chose the IPLA map (question asked in the session on 2026-09-29, since gavin's MCP could
not reach the daemon), and it was downloaded through their signed-in SCT-Outil session in Chrome
(Repertorio cartografico, search "Tipi forestali", tick the row, "Download dati selezionati", then
"Scarica il file"). The download, `u<user>_<date>.zip`, wraps `forestale_tipi_forestali_2020.zip`,
which holds the shapefile twice: ED50 / UTM 32N (23032) and RDN2008 / UTM 32N (7791, converted with
the IGM grids; the one read), with `licenza.pdf` (CC BY 4.0) and `istruzioni.pdf`. The loader gained a `manual` download shape for it
(`api.grid.sources.read_vector`): the config names the page to get the file from and the name it is
saved under in `$DATA_DIR/raw/rvda_tipi_forestali/`; a build without the file stops and says both.
**To rebuild the grid on another machine, download "Tipi forestali 2020" from SCT-Outil
(Repertorio cartografico → Forestazione) and save the inner `forestale_tipi_forestali_2020.zip`
unchanged as `raw/rvda_tipi_forestali/tipi_forestali_2020.zip`.**

Credits: the map is added to the app's national credits list (`web/src/credits.ts`). The rain
figures of the Region's statistical yearbook feed a check only, never the app.

## Config

`api/src/api/config/regions/valle_d_aosta.yaml`:

- **Boundary.** ISTAT COD_REG 2; bbox `[6.80, 45.46, 7.94, 45.99]`, the ISTAT 2025 boundary's
  extent (6.8016, 45.4670, 7.9395, 45.9878) rounded outward to 0.01°. Region area 3,261 km², 74
  comuni.
- **Forest.** `forest.groups` and `forest.types` both on `rvda_tipi_forestali`, class column and
  type field `ca`, read once (the one-map path Piemonte uses), mapping in Grid below.
- **iNaturalist place** 10882, "Valle d'Aosta, IT" (admin level 10), resolved by name on
  2026-09-29 (`api.inaturalist.org/v1/places/autocomplete?q=Valle d'Aosta`).
- **`weather.lapse_rates`** for the three air temperatures (below) and **`model:` the rain scale**,
  0.58 + 0.04 per km over `era5_land_cds` and `era5_seamless` (Weather, rain scale).
- **Weather points.** 27 land nodes on the 0.2° lattice (27 candidates), all 971 woodland cells
  within reach.

### Lapse rates: the region's own for air temperature

`uv run python -m api.weather.checks lattice --region valle_d_aosta` (59 ERA5-Land land nodes at
0.1° around the woodland cells, three 14-day windows of 2024), run 2026-09-29 on the final grid.
Cooling per km of height across nodes, median of the daily fits:

| variable | Jan | Jul | Oct | all | national | difference |
|---|---|---|---|---|---|---|
| temperature_2m_min | 4.69 | 5.66 | 4.66 | 5.33 | 4.2 | **+1.13** |
| temperature_2m_mean | 4.96 | 6.06 | 5.22 | 5.54 | 4.5 | **+1.04** |
| temperature_2m_max | 5.31 | 6.28 | 5.72 | 5.88 | 4.5 | **+1.38** |
| soil_temperature_0_to_7cm_mean | 1.11 | 5.50 | 4.02 | 4.02 | 3.7 | +0.32 |

The three air temperatures are past the card's 1 °C/km line, and as in Lombardia the fitted rates
**predict better** (leave-out RMSE, °C, when the lattice skips nodes and predicts them from the
rest):

| variable | 0.2° national | 0.2° regional | 0.2° 6.5 | 0.3° national | 0.3° regional | 0.3° 6.5 |
|---|---|---|---|---|---|---|
| temperature_2m_min | 0.973 | 0.768 | **0.743** | 0.952 | **0.764** | 0.797 |
| temperature_2m_mean | 0.737 | **0.542** | 0.563 | 0.789 | **0.615** | 0.665 |
| temperature_2m_max | 0.786 | **0.569** | 0.591 | 0.881 | **0.663** | 0.686 |
| soil_temperature_0_to_7cm_mean (3.7 kept) | **1.948** | — | 2.034 | **1.823** | — | 2.111 |

So **`valle_d_aosta.yaml` sets `weather.lapse_rates`** to 5.3 (min), 5.6 (mean), 5.9 (max). Soil
keeps the national 3.7: its fit is within the line (and January's is snow-bound, 1.11). The steep
rates are not a winter inversion artefact: July and October fit as steeply as January or more. The
errors are the largest of any region so far (Lombardia's 0.2° Tmean RMSE was 0.371 °C with its own
rates): the relief between nodes is the steepest of any region. The same check on the provisional CLC-only
grid (61 nodes) gave the same rates within 0.06 °C/km.

## Grid

`uv run python -m api.grid.build --region valle_d_aosta` (8 s; the DEM tiles and SoilGrids were
fetched for the provisional build the same morning):

- **The map's categories** (17,374 polygons, 98,868 ha, areas from the polygons in RDN2008 / UTM 32N;
  the species research quotes the Region's own 98,869 ha):

| category | ha | group | habitat |
|---|---|---|---|
| LC lariceti e cembrete | 43,088 | conifer | other_conifer |
| PE peccete | 13,545 | conifer | fir_spruce |
| PS pinete di pino silvestre | 9,614 | conifer | mountain_pine |
| BS boscaglie pioniere e d'invasione | 6,171 | broadleaf | mixed_broadleaf |
| AF acero-tiglio-frassineti | 5,954 | broadleaf | mixed_broadleaf |
| CA castagneti | 4,720 | broadleaf | chestnut |
| QR querceti di **roverella** | 3,846 | broadleaf | deciduous_oak |
| PN pinete di pino uncinato | 3,247 | conifer | mountain_pine |
| OV arbusteti subalpini | 2,774 | transitional | transitional_woodland_shrub |
| AB abetine | 1,762 | conifer | fir_spruce |
| RI rimboschimenti | 1,310 | conifer | other_conifer |
| FA faggete | 1,154 | broadleaf | beech |
| AN alneti planiziali e montani | 674 | broadleaf | riparian |
| AS arbusteti planiziali, collinari e montani | 648 | transitional | transitional_woodland_shrub |
| SP formazioni legnose riparie | 167 | broadleaf | riparian |
| RB robinieti | 126 | broadleaf | exotic_broadleaf |
| QV querceti di **rovere** | 68 | broadleaf | deciduous_oak |

  The codes are Piemonte's IPLA codes with one swap: here **QR is downy oak and QV sessile oak**
  (the map's own QGIS legend, and the areas: downy oak is the region's oak), the reverse of
  Piemonte. Both are `deciduous_oak`, so the habitat does not change. RI (plantations) follows
  Piemonte and Liguria as `other_conifer`. The shrublands (OV green alder and rhododendron, AS) are
  not forest and go to the transitional group, outside the woodland mask. The map also carries a
  type (`tipo`, 52 types) and a variant letter (`tipifore`, e.g. LC52B); the variants' meaning is in
  the IPLA typology book, not in the file, so no variant is used (see Known limitations on larch).
- **Cells 3,457; woodland 971** (28.1 %). Threshold sensitivity (forest share of the cell, before
  the 0.25 km² floor): 0.3 → 1,340, 0.4 → 1,169, **0.5 → 974**, 0.6 → 773, 0.7 → 605.
- **INFC 2015: −3.8 %** (grid 95,484 ha vs 99,243 ha bosco), inside ±10 %. CLC IV alone gave
  73,946 ha (−25.5 %) on the provisional build.
- **Habitats on woodland cells** (share of wooded area; cells where dominant; their mean height):

| habitat | share | dominant cells | mean elevation |
|---|---|---|---|
| other_conifer (larch, stone pine, plantations) | 40.2 % | 424 | 1,766 m |
| fir_spruce | 19.0 % | 179 | 1,593 m |
| mountain_pine (Scots pine, *P. uncinata*) | 15.3 % | 165 | 1,395 m |
| mixed_broadleaf | 12.2 % | 90 | 1,156 m |
| chestnut | 5.8 % | 64 | 839 m |
| deciduous_oak | 3.7 % | 35 | 907 m |
| beech | 1.6 % | 14 | 1,201 m |
| transitional_woodland_shrub | 1.5 % | — | — |
| riparian | 0.6 % | — | — |
| exotic_broadleaf (robinia) | 0.1 % | — | — |

  The belts are in the right order: chestnut at 840 m, oaks at 910 m, beech at 1,200 m, Scots and
  mountain pine at 1,400 m, spruce and fir at 1,600 m, larch at 1,770 m. The dominant habitat covers
  a median 69 % of the wooded area (Piemonte 71 %). `borrowed_type_fraction` is 0 everywhere (groups
  and types are one map).
- **Terrain.** Woodland cells: median elevation 1,582 m (p10 930 m, p90 1,985 m, max 2,217 m, min
  433 m), the highest of any region; 32 cells below 700 m, 182 at 1,900–2,200 m. Median slope 29.3°
  (p90 36.8°, max 44.4°; the species research's slope band, x1 to 36°, x0.8 from 45°, was set from
  an approximation and fits). All have terrain; 4 have no aspect.
- **Soil pH.** Median 6.26 (5th–95th percentile 5.89–6.59); lowest under fir/spruce (6.13) and larch
  (6.16), highest under oaks (6.53).
- **Places.** All 74 comuni get cells; 2 cells fall outside every comune polygon. Nearest locality
  median 2.5 km, max 11.7 km.
- **Spot checks** (the most wooded cell of each comune):

| comune (woodland cells) | cell | forest | top habitats | elev. m |
|---|---|---|---|---|
| Champdepraz, Mont Avic (27) | `1kmE4137N2512` | 1.00 | mountain_pine 0.43, mixed_broadleaf 0.27, deciduous_oak 0.12 | 1165 |
| Nus, Saint-Barthélemy (20) | `1kmE4126N2522` | 0.96 | other_conifer 0.60, fir_spruce 0.29, mountain_pine 0.11 | 1868 |
| Saint-Pierre (6) | `1kmE4103N2518` | 0.79 | mountain_pine 0.71, other_conifer 0.19, fir_spruce 0.09 | 1909 |
| Perloz (14) | `1kmE4149N2503` | 0.95 | chestnut 0.63, other_conifer 0.17, mixed_broadleaf 0.15 | 1083 |
| Courmayeur (20) | `1kmE4086N2524` | 0.93 | fir_spruce 0.78, other_conifer 0.22 | 1703 |
| Brusson (26) | `1kmE4147N2517` | 0.95 | other_conifer 0.72, fir_spruce 0.17, mountain_pine 0.10 | 1765 |
| Valtournenche (14) | `1kmE4136N2530` | 0.94 | other_conifer 0.89, fir_spruce 0.11 | 1901 |
| Cogne (25) | `1kmE4113N2505` | 0.90 | other_conifer 0.72, mountain_pine 0.25, fir_spruce 0.03 | 1884 |
| Gressoney-Saint-Jean (19) | `1kmE4154N2516` | 0.88 | other_conifer 0.71, fir_spruce 0.29 | 1776 |
| La Thuile (14) | `1kmE4083N2514` | 0.82 | fir_spruce 0.85, other_conifer 0.15 | 1687 |
| Morgex (21) | `1kmE4086N2520` | 0.94 | fir_spruce 0.74, mountain_pine 0.22, mixed_broadleaf 0.04 | 1486 |
| Aosta (city; 6 of 21 cells woodland, on the slopes) | — | — | — | — |

## Weather

### History

Copernicus ERA5-Land from the CDS time-series product, one request per node for 2016-01-01 to
2026-09-18: 27 nodes on the 0.2° lattice (every candidate around the woodland cells is on land),
1.16 M daily values, fetched in 33 min on 2026-09-29 (none of the node series was in the shared
cache: the other lanes' requests end on other days). Snowfall from the shared Italy-wide gridded
file. The days after 2026-09-18 come from the Open-Meteo update step, as for every region.

### Rain scale: the Region's yearbook totals

The Region's rain gauges belong to the Centro funzionale (CF) and ARPA Valle d'Aosta. The CF's
daily data are CC BY 4.0, but served only through a request form that asks for a name and an email
and prepares a zip later (`presidi2.regione.vda.it/str_dataview_download`), so no script can fetch
them and the human chose not to. The Region's **statistical yearbook** (Annuario statistico
regionale, Osservatorio economico e sociale) publishes, every year, the monthly rain of 15 of those
stations as an open PDF table ("Precipitazioni cumulate (mm) in alcune località della Valle
d'Aosta": annuari 2017–2025 hold 2016–2024). So the check compares totals, not days, as Puglia's
did with its Annali: raw CDS rain summed per month, read bilinearly from the land nodes at each
gauge, against the gauges' months, keeping gauge-years with all twelve months (a month the yearbook
marks `..`, under 90 % coverage, or `(c)`, "presumibilmente sottostimato", drops its year). The
tables were parsed by column position and each year's months summed back to the table's own annual
total or mean to the tenth of a millimetre. Positions and heights from the CF's station map
(`cf.regione.vda.it`, rain stations); the yearbook's "Gressoney-Saint-Jean" is taken to be the CF
station Bieltschocke (1,370 m), the one near the village (the fit barely moves without it: 0.589 +
0.037 per km).

| station | m | years | gauge mm/yr | raw CDS mm/yr | raw / gauge |
|---|---|---|---|---|---|
| Donnas (ARPA) | 318 | 9 | 1,040 | 1,348 | 1.30 |
| Verrès | 375 | 8 | 740 | 1,356 | 1.83 |
| Aosta Mont Fleury (ARPA) | 577 | 9 | 588 | 1,357 | **2.31** |
| Saint-Vincent | 626 | 8 | 652 | 1,402 | 2.15 |
| Courmayeur Dolonne | 1,200 | 9 | 1,061 | 1,517 | 1.43 |
| Etroubles (ARPA) | 1,339 | 9 | 643 | 1,363 | 2.12 |
| Gressoney-Saint-Jean | 1,370 | 7 | 970 | 1,545 | 1.59 |
| La Thuile Les Granges (ARPA) | 1,637 | 9 | 926 | 1,500 | 1.62 |
| Champorcher Petit-Mont-Blanc | 1,640 | 8 | 1,087 | 1,305 | **1.20** |
| Nus Saint-Barthélemy | 1,675 | 8 | 699 | 1,321 | 1.89 |
| Cogne Gimillan (ARPA) | 1,785 | 9 | 687 | 1,409 | 2.05 |
| Rhêmes-Notre-Dame Chaudanne | 1,794 | 8 | 899 | 1,474 | 1.64 |
| Valtournenche Breuil-Cervinia | 1,998 | 8 | 964 | 1,448 | 1.50 |
| Ollomont By | 2,017 | 8 | 831 | 1,368 | 1.65 |
| Ayas Alpe Aventine | 2,045 | 6 | 977 | 1,522 | 1.56 |

- **ERA5-Land holds 1.67 of the gauges' rain**, the wettest excess of any region so far (Piemonte
  1.33). It gives every station 1,300–1,550 mm a year, while the gauges run from 590 mm at Aosta to
  1,090 at Champorcher: the reanalysis spreads the rain of the border ridges over the whole region and
  misses the central valley's rain shadow. The excess is worst at the dry inner stations (Aosta 2.31,
  Saint-Vincent 2.15, Etroubles 2.12, Cogne 2.05) and least in the wetter Bassa Valle and toward
  Monte Rosa (Champorcher 1.20, Donnas 1.30). By year it runs from 1.28 (wet 2024) to 1.75.
- **The fit.** Least squares through the origin of gauge totals on model totals × (a + b × km) over
  the May–October totals (the months the rules score; Lombardia fitted the same months), 15 gauges,
  gauge-years with all six months: **a = 0.584, b = 0.036 per km** (a factor alone 0.633; the same
  fit on annual totals 0.573 + 0.024). Leaving one gauge out moves a within 0.58–0.63 and b within
  0.01–0.05, except without Donnas (0.46 + 0.11), the one low wet gauge. **`valle_d_aosta.yaml` sets
  0.58 + 0.04 per km, clamped at 2,000 m** (the highest gauges), over `era5_land_cds` and
  `era5_seamless`: 0.60 at 500 m, 0.64 at 1,500 m, 0.66 from 2,000 m.

| May–October | gauges | raw / gauge | scaled (0.58 + 0.04 × km) | a factor alone (0.633) |
|---|---|---|---|---|
| below 1,000 m | 4 | 1.73 | 1.04 | 1.10 |
| 1,000–1,600 m | 3 | 1.65 | 1.04 | 1.04 |
| 1,600–2,100 m | 8 | 1.51 | 0.98 | 0.95 |
| all | 15 | 1.59 | 1.00 | 1.00 |

- **Out of sample.** A factor fitted on 2016–2021 (0.603) leaves 2022–2024 at 0.89 of the gauges: in
  wet 2024 the reanalysis held only 1.28 of the gauge rain. The scale is right on average, not in
  every year.
- **What a factor cannot fix.** It scales totals. The rain shadow stays: scaled, Aosta still gets
  about 1.4 of its gauge rain and Champorcher 0.78. Porcini's 30-day rain is read as a share of the
  cell's own normal, which no scale changes; the 3-day trigger (10 → 30 mm) and gallinacci's 30-day
  totals are read in millimetres, and there the dry central valley reads wetter than it is. Monthly
  totals say nothing about the drizzle Piemonte's daily check found (the reanalysis raining on twice
  as many days as the gauges), which is likely here too. A daily check from the CF's form data is the
  follow-up that would show it.
- The yearbook figures feed this check only; they are not republished or shown in the app.

## Sightings

`api.sightings.ingest fetch --region valle_d_aosta`: GBIF over the bbox gave 132 records (*B. edulis*
49, *B. reticulatus* 6, *B. pinophilus* 1, *Cantharellus* 76; no *B. aereus*, no *A. caesarea*);
iNaturalist's recent fetch added none. The quality filters drop 86 as too imprecise and 34 without
a stated uncertainty; of the 46 kept, 40 fall off the woodland grid (outside the region, or in open
cells), so **6 sightings are stored, all porcini**: 2017-08-07, 2017-08-23, 2020-06-02 (two
records, one cell-day), 2022-07-16, 2025-09-10 (obscured by the source, so the backtest leaves it
out). No gallinacci sighting passes. The region is the
least recorded so far, as the species research found (17 *B. edulis* on iNaturalist in all).

## Data

- cells: 3457
- woodland cells: 971
- INFC deviation: -3.8% (grid 95,484 ha vs 99,243 ha) — within ±10 %
- weather nodes: 27
- years stored: 2016–2026 (11 years)
- sightings kept: 6
- sanity contrasts: 10/12 passed

## Validation

### Backtest (priors: rules version `a242d2c4a703`)

Run 2026-09-29 on the stores above: the onboard's hold-out run (`backtest/valle_d_aosta/onboard/`,
2024–2025) and the train seasons (`--seasons train --label onboard-train`). Scores cover 971 cells ×
3,848 days of history (2016-03-18 to 2026-09-29) plus the served window to 2026-10-06, none without
weather.

**Usable presences (unique, unobscured group-cell-day sightings on woodland cells) in the train
seasons 2016–2023: 4** (porcini 4, gallinacci 0), far under the 50 the card asks before tuning, so
**nothing is tuned: the researched priors ship.** The hold-out 2024–2025 holds none (its one record,
2025-09-10, is obscured by the source), so the hold-out run is empty.

On the 4 train presences (porcini; intervals from 4 points are wide and the numbers are anecdotes,
not a validation):

| metric | model | calendar | habitat | static |
|---|---|---|---|---|
| `auc_region` | 0.901 (0.83–0.97) | 0.822 | 0.541 | 0.573 |
| `auc_local` | 0.478 (0.21–0.71) | 0.557 | 0.532 | 0.557 |
| `auc_time_effort` | 0.690 (0.55–0.83) | 0.562 | 0.500 | 0.500 |

The finders' cells rank high region-wide (the bands and windows put them in the right belts), and
across the season at their cell the model beats the calendar; within 20 km on the day it does not.
Four sightings can say no more than that. The press contrasts are the real check here.

### Press contrasts (`sanity.yaml`, porcini, `backtest/valle_d_aosta/onboard/sanity_porcini.csv`)

**10 of 12 hold.**

| contrast | higher | lower | holds |
|---|---|---|---|
| `region_2023_2022_mid_august` | 0.115 | 0.293 | **no** |
| `region_2021_2022_august` | 0.697 | 0.221 | yes |
| `region_2021_august_normal` | 0.596 | 0.279 | yes |
| `gran_paradiso_2019_2020_august` | 0.428 | 0.027 | yes |
| `lys_vs_gran_paradiso_august_2020` | 0.190 | 0.021 | yes |
| `lys_vs_cervino_august_2020` | 0.193 | 0.089 | yes |
| `rosa_cervino_vs_gran_paradiso_september_2019` | 0.417 | 0.292 | yes |
| `south_vs_north_dora_late_august_2021` | 0.274 | 0.318 | **no** |
| `east_vs_west_autumn_2023` | 0.440 | 0.421 | yes (barely) |
| `south_vs_north_dora_september_2024` | 0.383 | 0.362 | yes (barely) |
| `region_june_july_2024_normal` | 0.380 | 0.302 | yes |
| `region_late_july_vs_early_august_2025` | 0.337 | 0.314 | yes |

- The good and bad years hold, often widely (2021 against the 2022 drought, the Gran Paradiso's 2019
  against 2020), and so do the east-west contrasts between the Monte Rosa valleys and the Gran
  Paradiso.
- **`region_2023_2022_mid_august` is the reanalysis and the heat.** In the reanalysis the two summers
  had the same rain (137 and 138 mm over the region's nodes from 20 July to 26 August), so the 2022
  drought the press describes ("piogge sempre troppo brevi, irrisorie e spesso seguite da vento
  secco") is not in it, and the 2022 rain fell in the first half of August, before the window. Mid
  to late August 2023 was the record heatwave (the window's mean Tmax over the nodes 21.3 °C against
  17.8 °C in 2022), which the temperature rules score down; the 2023 flush the press reports came
  from the early-August rains, and the storms that ended the heat came after the window.
- **`south_vs_north_dora_late_august_2021` is the foehn.** The press blames the "vento favonico" for
  drying the woods north of the Dora in days; no rule reads wind, and the reanalysis gives the two
  sides the same rain. The species research found the foehn blamed for failed flushes almost every
  year: a drying-wind factor is a candidate for the model, not for this region's config.
- The rain scale does not change these: porcini read their 30-day rain as a share of each cell's
  normal, and both failures turn on rain the reanalysis spreads evenly.

## After the deploy: what to verify

The stores were rsync'd to the server with `deploy/rsync-region-data.sh valle_d_aosta` (no
redeploy); see the ship note below. The server serves a region only when its YAML is in the deployed
code and its stores are on disk, so they stay inert until `main` with
`config/regions/valle_d_aosta.yaml` is deployed by the rail's "Deploy pulled main" step, with the
daily job. The stores are scored through 2026-10-06 (the served window from the update of
2026-09-29); the daily job catches them up. The merged `main` must carry this branch's fix to the
cell detail (`api/src/api/live/repository.py`): without it every tapped cell in Valle d'Aosta answers
500, since the region has no ovoli store. Then check:

- [ ] The daily job after the deploy has a `region_done` line for `valle_d_aosta`
  (`journalctl -u mushma-daily`), no `region_failed`, and its Open-Meteo call count stays inside the
  budget.
- [ ] `https://mappafunghi.app/valle-d-aosta` and `/valle-d-aosta/porcini`, `/valle-d-aosta/gallinacci`
  show real scores for today (not fixtures); `/valle-d-aosta/ovoli` is a not-found page; a tapped
  cell opens (no 500), lists porcini and gallinacci only, and its "why this score" names the
  region's habitats (larch and stone pine, spruce and fir, Scots pine).
- [ ] `https://api.mappafunghi.app/regions` lists `valle_d_aosta` with `["porcini", "gallinacci"]`;
  the hub `/` lists it and colours it from `/overview` for porcini, gallinacci and all species, and
  leaves it uncoloured for ovoli without breaking the other regions.
- [ ] A GPS fix or a search in Aosta, from the hub, offers Valle d'Aosta, not Piemonte.
- [ ] `https://mappafunghi.app/sitemap.xml` has the three Valle d'Aosta URLs (built from the
  registry).
- [ ] Lighthouse SEO is 100 on `/valle-d-aosta` (prerendered title, description, canonical, og image
  `og/valle-d-aosta.png`, JSON-LD Dataset with `sameAs` Wikidata Q1222).
- [ ] `/credits` shows "Regione Autonoma Valle d'Aosta — Carta forestale, Tipi forestali 2020
  (Repertorio cartografico SCT)".
- [ ] The next morning's daily job has a `region_done` line for `valle_d_aosta` again.

## Known limitations

- **Larch.** Larch and stone pine are 40 % of the woods and score as a non-host (0.1) for *B.
  edulis*, *B. pinophilus* and gallinacci, so a pure larch cell gets a third of full habitat credit
  (the species research's biggest choice; Piemonte keeps 0.3 on the same typology). The map's IPLA
  variants (e.g. LC52B) probably mark larch stands with spruce or stone pine; mapping the spruce
  variants to `fir_spruce` needs the variant legend from the typology book, which the file does not
  carry. If the larch valleys (Valdigne, Valpelline, upper Ayas, Valtournenche) score too low once
  the season can be watched, that, or larch at 0.3, is the first knob.
- **Rain.** The reanalysis gives the whole region 1,300–1,550 mm a year and misses the central
  valley's rain shadow; the scale fixes totals on average (Weather), not the shadow, the year to
  year swing or the drizzle. A daily gauge check would need the Centro funzionale's form data.
- **Foehn.** No rule reads the drying wind the press blames for most failed flushes here.
- **Four sightings.** The backtest cannot validate the region; the press contrasts are the check.
- **Ovoli.** None in the region's rules or pages; the hub's ovoli map leaves the region uncoloured.
  If a documented Bassa Valle find turns up, the species appendix says how to bring the group back.
- **Region lookup by bbox.** Valle d'Aosta is registered before Piemonte so that a fix in the region
  finds it (Piemonte's bbox holds all of it), but its own bbox takes in the Canavese strip of
  Piemonte (Ivrea, Valchiusella, Carema), Chamonix and the Valais border valleys: from the hub, a fix
  there is offered Valle d'Aosta. `fix-region-lookup-by-boundary.md` would fix every pair.
