# Trentino-Alto Adige

Region card: `region-trentino-alto-adige.md` (region #9 of `feat-full-italy-coverage.md`). API id
`trentino_alto_adige`, web slug `/trentino-alto-adige`, ISTAT COD_REG 4, names "Trentino-Alto Adige"
/ en "Trentino-South Tyrol". Two autonomous provinces, Trento (6,208 km², 166 comuni) and Bolzano /
South Tyrol (7,399 km², 116 comuni, bilingual Italian and German names). The most Alpine region so
far: more than half the woodland lies between 1,000 and 2,000 m, mostly spruce, with larch and
stone pine up to the tree line, silver fir and beech in southern Trentino, Scots pine on the dry
slopes of the inner valleys (Val Venosta, Valle Isarco), and oak, hop-hornbeam, chestnut and holm
oak only low down on the Adige, Sarca and Valsugana slopes and around Lake Garda.

## Sources

**Decision: each province's own forest-type map, one layer per province for both the groups and
the types.** Checked 2026-09-26:

| candidate | what it is | verdict |
|---|---|---|
| **Tipi forestali PAT integrati, elaborazione statica 2021** (Provincia autonoma di Trento, Servizio Foreste) | The real forest type (*tipo forestale reale*) of every forest unit in the management plans of the public and large private forests (SIGFAT), harmonised and filled in from other surveys where there is no plan, so it covers all of Trentino's forest. 56,531 polygons, 15 categories and 54 types of the Trentino typology (Odasso), valid from 2022-01-01. GeoNetwork record `p_TN:920383ad-…`: CC BY 4.0, "nessuna limitazione", zip with a GeoPackage and a shapefile (136 MB) | **used** (`pat_tipi_forestali`) |
| Tipi forestali — SIGFAT (same office) | The latest management-plan units only (public and large private forests), updated continuously | not complete: the integrated map fills its gaps |
| **Tipologie forestali dell'Alto Adige** (Provincia autonoma di Bolzano, Ufficio Pianificazione forestale; *Waldtypisierung Südtirol*) | The forest area typed by site: 94,671 polygons, 86 types in 14 groups, derived from the geological map, the DTM and the technical map and calibrated on field plots (2010, published 2011). Open-data portal "Foreste: tipi forestali": CC0 1.0; WFS `p_bz-Forestry:ForestTypes` on the provincial GeoServer | **used** (`pbz_tipologie_forestali`) |
| ISPRA CLC 2018 IV level | National fallback, 25 ha minimum unit | not needed: both provinces have open, finer, typed maps |

Both maps cover forest only, so each gives both the broad groups (how much of each cell is
woodland) and the habitats (which kind), from its own class. The two classifications differ, so
`forest.types` became a list of layers, one per source, like `forest.groups` already was
(`api.grid.build.read_layered_cover`; the card's "follow-up for the foundation's forest card" is
this change, made here with its tests). A group layer and a types layer on the same source are read
once.

- **Trento** is mapped by type (`label`), 54 codes. Its map says what grows there: *peccete
  secondarie* (spruce that replaced beech or fir) and *lariceti secondari* are their own types.
- **Bolzano** is mapped by group (`WGRU_BEZ_I`), 14 names. Its map types a stand by its site and
  names the trees that site carries (e.g. *Piceo-abieti-faggeta*, spruce-fir-beech); in South
  Tyrol's largely near-natural forests that is close to what grows there, but a site typed as beech
  forest may in fact carry planted spruce. The riparian woods and the green-alder and
  mountain-pine scrub have a group name but no group code, hence the name.
- **Mountain-pine krummholz (*mughete*) and green-alder scrub are not forest.** INFC counts them as
  *arbusteti subalpini* (other wooded land), and a prostrate mugo pine does not reach the 5 m a
  forest needs. They go to the transitional group, which does not count toward the woodland mask
  (Trento MU 13,866 ha and OA 8,590 ha; Bolzano 13,194 ha).
- **Mixed.** The Bolzano spruce-fir-beech group and the oak-Scots pine group (*Querco-pinete*), and
  Trento's *faggeta mesalpica con conifere*, go to `mixed` (`mixed_broadleaf_conifer`).

Map areas by group (from the polygons; the grid's rasterized totals are in Grid):

| group | Trento | Bolzano |
|---|---|---|
| conifer | 254,314 ha | 278,642 ha |
| broadleaf | 99,691 ha | 33,585 ha |
| mixed | 15,284 ha | 30,767 ha |
| transitional (not forest) | 22,455 ha | 13,194 ha |
| **forest (conifer + broadleaf + mixed)** | **369,289 ha** | **342,994 ha** |
| INFC 2015 bosco | 373,259 ha | 339,270 ha |

The Trento total, 391,745 ha with the scrub, matches the Province's own 390,463 ha of forest.

| Trento type (`label`) | ha | group | habitat |
|---|---|---|---|
| PE, PEX, PE_* peccete | 119,522 | conifer | fir_spruce |
| FA_* faggete (not FA_con) | 46,982 | broadleaf | beech |
| LA, LAX, LA_* lariceti | 48,066 | conifer | other_conifer |
| AB, AB_* abieteti | 37,557 | conifer | fir_spruce |
| PS_* pinete (silvestre, nero) | 34,714 | conifer | mountain_pine |
| OO, OO_pri orno-ostrieti | 23,490 | broadleaf | mixed_broadleaf |
| FA_con faggeta mesalpica con conifere | 15,284 | mixed | mixed_broadleaf_conifer |
| MU_* mughete | 13,866 | transitional | transitional_woodland_shrub |
| LC_*, CB_* larici-cembrete, cembrete | 14,455 | conifer | other_conifer |
| OQ ostrio-querceto, QC querco-carpineto, QR querceto | 12,644 | broadleaf | deciduous_oak |
| OA ontaneta di ontano verde | 8,590 | transitional | transitional_woodland_shrub |
| TR formazioni transitorie (corileti, betuleti) | 5,895 | broadleaf | mixed_broadleaf |
| RO robinieto | 4,965 | broadleaf | exotic_broadleaf |
| AF, AF_ob, AT aceri-frassineti, aceri-tiglieti | 1,881 | broadleaf | mixed_broadleaf |
| LE_* leccete (Alto Garda) | 1,739 | broadleaf | evergreen_oak |
| OB, ON ontanete di ontano bianco e nero | 1,342 | broadleaf | riparian |
| CS, CS_ro castagneti | 754 | broadleaf | chestnut |

| Bolzano group (`WGRU_BEZ_I`) | ha | group | habitat |
|---|---|---|---|
| Peccete subalpine | 91,929 | conifer | fir_spruce |
| Peccete montane | 67,563 | conifer | fir_spruce |
| Piceo-abieteti | 54,808 | conifer | fir_spruce |
| Larici-cembrete | 46,735 | conifer | other_conifer |
| Piceo-abieti-faggete | 20,453 | mixed | mixed_broadleaf_conifer |
| Mughete e bassofusti di ontano verde | 13,194 | transitional | transitional_woodland_shrub |
| Faggete | 11,512 | broadleaf | beech |
| Querceti | 11,292 | broadleaf | deciduous_oak |
| Querco-pinete | 10,314 | mixed | mixed_broadleaf_conifer |
| Lariceti | 9,003 | conifer | other_conifer |
| Pinete | 8,604 | conifer | mountain_pine |
| Orno-ostrieti | 7,651 | broadleaf | mixed_broadleaf |
| Boschi ripariali | 2,319 | broadleaf | riparian |
| Boschi di latifoglie (frassino-tiglieti) | 811 | broadleaf | mixed_broadleaf |

**Chestnut is nearly absent from both maps** (754 ha in Trento; no chestnut group in Bolzano, whose
site typology puts chestnut inside two oak types, Ei2 *querceto di rovere silicatico a castagno*
and Ei5 *bosco misto di querce e castagno*, 7,661 ha together, mapped here as `deciduous_oak`). Chestnut dominates
only 7 woodland cells (Storo, Borgo Chiese, Arco). Ovoli and *B. aereus* lean on chestnut, so their
habitat credit here comes from the oak and hop-hornbeam woods (species research).

A YAML trap found on the way: PyYAML reads a bare `ON` (Trento's *ontaneta di ontano nero*) as the
boolean `true`, so the code matched nothing. It is quoted now, and the loader rejects a class code
read as a boolean (`api.grid.build.class_codes`).

Credits: both maps are added to the app's credits list (`web/src/credits.ts`). The South Tyrolean
rain gauges feed a check only, never the app.

## Config

`api/src/api/config/regions/trentino_alto_adige.yaml`:

- **Boundary.** ISTAT COD_REG 4; bbox `[10.38, 45.67, 12.48, 47.1]`, the ISTAT 2025 boundary's
  extent (10.3858, 45.6745, 12.4777, 47.0916) rounded outward to 0.01°. Region area 13,606 km².
- **Forest.** Two layers in both `forest.groups` and `forest.types`: `pat_tipi_forestali` by
  `label` and `pbz_tipologie_forestali` by `WGRU_BEZ_I`, mapping above. The Bolzano WFS is read in
  pages of 2,000 sorted by `ID`: the GeoServer cut responses of 5,000 features short at about
  4.2 MB after a few requests.
- **iNaturalist place** 10874, "Trentino-Alto Adige, IT" (admin level 10), resolved by name on
  2026-09-26 (`api.inaturalist.org/v1/places/autocomplete?q=Trentino`).
- **Gauges.** `api.weather.checks gauges --region trentino_alto_adige` reads the Provincia di
  Bolzano's open daily rain (`api.weather.bolzano_meteo`, Validation). Trento's history is not
  openly downloadable (Validation).
- **`model:` overrides:** the rain scale, ×0.75 over `era5_land_cds` and `era5_seamless`
  (Validation, rain gauges). The gauge check asked for it: the reanalysis is wetter than the South
  Tyrolean gauges, as in Piemonte, and the national scale covers `era5_seamless` only, so without
  an override the CDS history would go unscaled while the recent days got ×1.7 at these heights.
- **Weather points.** 81 land nodes on the 0.2° lattice (81 candidates), all woodland cells within
  reach.

### Lapse rates (`api.weather.checks lattice --region trentino_alto_adige`)

230 ERA5-Land land nodes at 0.1° (532–2,836 m), three 14-day windows of 2024 (Jan, Jul, Oct), run
2026-09-26. Cooling per km of height, median of the daily fits:

| variable | Jan | Jul | Oct | all | national config | difference |
|---|---|---|---|---|---|---|
| Tmin | 6.93 | 5.42 | 4.59 | **5.26** | 4.2 | **+1.06** |
| Tmax | 6.03 | 5.72 | 4.69 | **5.38** | 4.5 | +0.88 |
| Tmean | 6.30 | 5.86 | 4.80 | **5.56** | 4.5 | **+1.06** |
| soil 0–7 cm | 0.17 | 4.76 | 3.60 | **3.60** | 3.7 | −0.10 |

Tmax and soil are within 1 °C/km; **Tmin and Tmean sit just over the line (+1.06)**, the same case as
Piemonte's Tmin (+1.04). January cools fastest (a stable, snow-covered valley atmosphere; the soil
under snow barely cools with height at all, 0.17). **The national rates are kept**, because the
leave-out test shows no gain from the region's own rates on the lattice the app serves:

| leave-out RMSE | Tmin | Tmax | Tmean | soil |
|---|---|---|---|---|
| served lattice (0.2°, stride 2), national | 0.547 °C | 0.394 °C | 0.395 °C | 0.721 °C |
| served lattice, fitted (5.26 / 5.38 / 5.56 / 3.60) | 0.538 °C | 0.401 °C | 0.401 °C | 0.721 °C |
| stride 3 (0.3°), national | 0.927 °C | 0.555 °C | 0.659 °C | 1.033 °C |
| stride 3, fitted | 0.898 °C | 0.536 °C | 0.642 °C | 1.036 °C |

A 0.009 °C gain for Tmin and a 0.006 °C loss for Tmean on the served lattice do not justify a
per-region rate. Leave-out at the 0.2° lattice with no lapse correction: 0.86 / 0.75 / 0.77 /
0.88 °C (Tmin, Tmax, Tmean, soil), with 6.5 °C/km 0.58 / 0.46 / 0.45 / 0.81 °C: the national
rates are the best of the three. Errors are about 20 % larger than Piemonte's (0.45 °C Tmin): the
relief between nodes is steeper still.

## Grid

`uv run python -m api.grid.build --region trentino_alto_adige` (3.6 min the first time, with the
Bolzano WFS pages, the Trento zip, the DEM tiles and SoilGrids fetched; 1 min cached):

- **Cells 14,088; woodland 7,698** (54.6 %, the highest share so far). Threshold sensitivity
  (forest share of the cell, before the 0.25 km² floor): 0.3 → 9,156, 0.4 → 8,502, **0.5 → 7,772**,
  0.6 → 6,922, 0.7 → 5,898. Trento 4,002 woodland cells, Bolzano 3,696.
- **INFC 2015: −0.1 %** (grid 712,120 ha vs 712,529 ha bosco), well inside ±10 %. The provinces
  agree on their own (the maps' forest 369,289 ha vs INFC 373,259 ha in Trento, 342,994 ha vs
  339,270 ha in Bolzano), because the subalpine scrub is left out of the forest as INFC leaves it.
- **Habitats on woodland cells** (share of wooded area; cells where dominant; their mean height):

| habitat | share | dominant cells | mean elevation |
|---|---|---|---|
| fir_spruce (spruce, silver fir) | 53.1 % | 4,532 | 1,493 m |
| other_conifer (larch, stone pine) | 14.2 % | 953 | 1,819 m |
| beech | 8.4 % | 665 | 1,033 m |
| mixed_broadleaf_conifer (spruce-fir-beech, oak-Scots pine) | 6.7 % | 483 | 1,111 m |
| mountain_pine (Scots pine, black pine) | 5.9 % | 382 | 907 m |
| mixed_broadleaf (hop-hornbeam, ash-maple, hazel-birch) | 5.4 % | 358 | 679 m |
| deciduous_oak | 3.2 % | 228 | 665 m |
| transitional_woodland_shrub (mugo, green alder) | 1.6 % | 26 | 1,561 m |
| exotic_broadleaf (robinia) | 0.6 % | 46 | 682 m |
| riparian | 0.4 % | 1 | 899 m |
| evergreen_oak (holm oak, Alto Garda) | 0.2 % | 17 | 445 m |
| chestnut | 0.1 % | 7 | 720 m |

  The belts are in the right order: holm oak by Lake Garda at 450 m, oaks, hop-hornbeam and robinia
  at 650–700 m, Scots and black pine at 900 m, beech and the mixed woods at 1,000–1,100 m, spruce
  and fir at 1,500 m, larch and stone pine at 1,800 m. The dominant habitat covers a median 75 % of
  the wooded area (Piemonte 71 %, Tuscany 89 %). `borrowed_type_fraction` is 0 everywhere (groups
  and types come from the same maps).
- **Terrain.** Woodland cells: median elevation 1,407 m (Piemonte 838 m), 95th percentile 1,992 m,
  max 2,427 m, min 231 m; 196 cells below 500 m, 1,414 at 500–1,000 m, 2,852 at 1,000–1,500 m,
  2,885 at 1,500–2,000 m and 351 above. Median slope 26.9°. All have terrain; 71 have no aspect.
- **Soil pH.** Median 6.28 (5th–95th percentile 5.31–6.66); lowest under spruce and fir (5.90),
  highest under holm oak (6.67).
- **Places.** 282 comuni get cells; 2 cells fall outside every comune polygon. Nearest locality
  median 2.2 km, max 12.8 km (Piemonte 1.0 and 8.8 km: fewer villages up high). Comune names are
  ISTAT's bilingual forms (`Renon/Ritten`).
- **Spot checks:**

| place | cell | woodland | forest | top habitats | elev. m | comune |
|---|---|---|---|---|---|---|
| Foresta di Paneveggio | `1kmE4455N2578` | yes | 0.79 | fir_spruce 1.00 | 1538 | Primiero San Martino di Castrozza (TN) |
| Latemar above Obereggen | `1kmE4438N2585` | yes | 0.86 | fir_spruce 1.00 | 1741 | Nova Ponente/Deutschnofen (BZ) |
| Val di Funes | `1kmE4454N2613` | yes | 0.97 | fir_spruce 0.85, other_conifer 0.14 | 1777 | Funes/Villnöß (BZ) |
| Bosco di Dobbiaco | `1kmE4490N2625` | yes | 0.80 | fir_spruce 0.89, riparian 0.11 | 1275 | Dobbiaco/Toblach (BZ) |
| Sonnenberg above Naturno (Val Venosta) | `1kmE4397N2616` | yes | 0.68 | deciduous_oak 0.98 | 748 | Naturno/Naturns (BZ) |
| Scots pine above Sluderno (Val Venosta) | `1kmE4367N2617` | yes | 0.73 | fir_spruce 0.60, mountain_pine 0.23 | 1394 | Sluderno/Schluderns (BZ) |
| Lavarone plateau | `1kmE4417N2538` | yes | 0.93 | fir_spruce 0.69, beech 0.28 | 1148 | Lavarone (TN) |
| Monte Bondone | `1kmE4403N2544` | yes | 0.96 | fir_spruce 0.38, beech 0.30 | 1173 | Garniga Terme (TN) |
| Robinia and chestnut above Roncegno | `1kmE4430N2547` | yes | 0.99 | exotic_broadleaf 0.69, fir_spruce 0.23 | 797 | Roncegno Terme (TN) |
| Chestnut woods of Storo | `1kmE4362N2524` | yes | 0.68 | chestnut 0.57, exotic_broadleaf 0.34 | 551 | Storo (TN) |
| Holm oak above Torbole | `1kmE4388N2526` | yes | 0.82 | evergreen_oak 1.00 | 264 | Nago-Torbole (TN) |
| Bolzano (city) | `1kmE4425N2599` | no | 0.07 | — | 284 | Bolzano/Bozen (BZ) |
| Trento (city) | `1kmE4407N2551` | no | 0.09 | — | 204 | Trento (TN) |

## Weather history

From the Copernicus CDS, 2016-01-01 to 2026-09-14, through the ERA5-Land time-series product
(`cds.method: timeseries`): 81 node requests, 16 of them already cached by Lombardia's lane (the
nodes the two regions share), 65 fetched at about 37 s each (40 min). The days after 2026-09-14 come from the Open-Meteo update
step, as for every region.

**Snowfall** comes from the shared Italy-wide gridded files (`sf_*_35.40_6.60_47.10_18.60`), cached
by the Lombardia lane earlier the same day. That area stops at 47.1° N, the basemap's extent, and
five of the region's nodes sit at 47.2° N (the 0.2° lattice around the Ahrntal, the upper Val
Pusteria and the Val di Vizze, whose cells reach 47.09° N): the snowfall read failed on them. A
node at most one ERA5-Land step (0.1°) past the file now takes the file's edge row
(`api.weather.cds.read_snowfall_zip`), which is nearer the cells those nodes serve than the nodes
themselves; further out is still an error. No new gridded request was needed.

**Open-Meteo.** The update stored `era5_seamless` for 2026-09-12 to 09-20; the forecast call then
hit Open-Meteo's daily limit (HTTP 429, "Daily API request limit exceeded"): the free quota is per
IP, shared by every lane on this machine, and it was spent by mid-afternoon on 2026-09-26 (the
species research found the elevation API at its limit too and used the DEM tiles instead). The served window
(today −6 to +7, with factors) and the seasonal tendencies wait for the next day's quota; the
server's daily job fetches them anyway once the region is deployed.

## Data

- cells: 14088
- woodland cells: 7698
- INFC deviation: -0.1% (grid 712,120 ha vs 712,529 ha) — within ±10 %
- weather nodes: 81
- years stored: 2016–2026 (11 years)
- sightings kept: 255
- backtest AUC (auc_local, model, all): gallinacci 0.538, ovoli 0.746, porcini 0.602
- sanity contrasts: 11/16 passed

## Validation

### Rain gauges (`api.weather.checks gauges --region trentino_alto_adige`)

**South Tyrol only.** The Provincia di Bolzano publishes one workbook of daily rain per station
("Tageswerte Temperaturen und Niederschläge", data.civis.bz.it, CC0 1.0), 1981–2024, a day being
the rain from 09:00 CET of the day before to 09:00 CET of the labelled day (the SIR Toscana cut,
`sir.gauge_day_totals`). `api.weather.bolzano_meteo` reads them with the standard library. Of the
portal's 58 station links, 8 land on the weather site's 404 page and one is mangled in the portal's
own metadata (`M%C2%81hlen`, HTTP 400): 49 stations read, 43 with 80 % of 2019–2024, **17 in
woodland cells** (214–1,883 m; one below 400 m, one at 400–800 m, 15 above).

**Trento's gauges are not in the check.** Meteotrentino's history is open (CC BY 4.0, "Dati
storici stazioni meteorologiche" on dati.trentino.it) but served only through an interactive
Hydstra WEB app (storico.meteotrentino.it) whose JSON web service answers 404; its `service.asmx`
gives only the last week; and the Open Data Hub (NOI), which carries Meteotrentino's stations,
limits anonymous requests to 5-day ranges (about 440 requests per station for 2019–2024) and
labels its daily series with an undocumented cut. So the scale is fitted on South Tyrol and
applied to Trentino too; the Prealps south of Trento are wetter, and whether ERA5-Land's excess
holds there is not checked.

- **ERA5-Land (CDS) holds 1.34 of the gauge rain** (pooled 2019–2024; median per gauge 1.31, daily
  correlation 0.68, 3-day wet-window hit rate 0.89, false alarms 0.24). By height band: 1.17
  (the one gauge below 400 m), 1.16 (400–800 m), 1.35 (800–1,200 m), 1.37 above; by year 1.20 (wet
  2024) to 1.53 (dry 2022). The same excess as Piemonte (1.33).
- **It rains too often, and too little when it pours.** The reanalysis has 1 mm or more on 59 % of
  days against the gauges' 28 %, and 5 mm or more on 1.7 times as many days. On gauge days under
  5 mm it gives 5.7 times the gauge rain; on gauge days of 20 mm or more, 0.52 of it.
- **The fit.** Least squares of gauge totals on model totals × (a + b × km, capped at 1.7 km as
  the national scale is) over 2019–2024 gives **a = 0.843, b = −0.077 per km**; a factor alone
  gives **0.746**. So `trentino_alto_adige.yaml` sets `model.precipitation_scale` to **0.75, no
  height term**, over both `era5_land_cds` and `era5_seamless`. Pooled ratio 1.34 → 1.00, bands
  0.87 (the two gauges below 800 m) and 1.01–1.02 above. Fitted on 2019–2023 alone it gives 0.73
  and 0.87 on the wet 2024 (Piemonte's held at 1.02): with 17 gauges the year-to-year spread is
  most of the uncertainty.
- **What a factor cannot fix.** Share of windows at or above each rule threshold:

| | gauges | raw | × 0.75 (shipped) | × 0.85 |
|---|---|---|---|---|
| 3-day ≥ 10 mm | 25.6 % | 40.6 % | 30.9 % | 35.5 % |
| 3-day ≥ 30 mm | 7.9 % | 8.2 % | 3.7 % | 5.5 % |
| 30-day ≥ 25 mm | 82.4 % | 95.1 % | 91.8 % | 93.6 % |
| 30-day ≥ 75 mm | 47.4 % | 69.3 % | 52.6 % | 60.8 % |

  The raw reanalysis already meets the 30 mm trigger as often as the gauges; ×0.75 halves it, while
  the 10 mm step and the 30-day thresholds stay too often met. ×0.85 is no better overall. The
  totals fit ships, the method every region so far used; porcini's 30-day rain is scored against
  each cell's own normal and is unaffected. Correcting the drizzle itself (a wet-day threshold or
  quantile mapping per region) is the cross-region follow-up Piemonte named.

### Backtest (priors: rules version `2e812362221d`)

Run 2026-09-26 on the stores above: the onboard's hold-out run (`backtest/trentino_alto_adige/onboard/`)
and the train seasons (`--seasons train --label onboard-train`). Scores cover 7,698 cells × 3,839
days (2016-03-18 to 2026-09-20), none without weather.

**Usable presences (unique, unobscured group-cell-day sightings on woodland cells) in the train
seasons 2016–2023: 122** (porcini 69, gallinacci 49, ovoli 4; by year 4, 5, 6, 22, 27, 22, 11, 25),
over the 50 the card asks before tuning, so the pre-registered tuning ran (Tuning, below). The
hold-out 2024–2025 holds 65 (porcini 38, gallinacci 26, ovoli 1). The most of any region so far
(Tuscany 55, Piemonte 53, Emilia-Romagna 13).

| group | split | n | `auc_local` model | habitat | `auc_time_effort` model | calendar | `auc_region` model | habitat |
|---|---|---|---|---|---|---|---|---|
| porcini | train | 69 | 0.530 (0.48–0.58) | 0.504 | 0.617 (0.56–0.67) | 0.516 | 0.857 | 0.501 |
| ovoli | train | 4 | 0.771 (0.67–0.87) | 0.676 | 0.505 (0.30–0.73) | 0.532 | 0.964 | 0.798 |
| gallinacci | train | 49 | 0.612 (0.57–0.65) | 0.534 | 0.530 (0.47–0.59) | 0.520 | 0.879 | 0.532 |
| porcini | hold-out | 38 | 0.602 (0.55–0.65) | 0.536 | 0.536 (0.46–0.61) | 0.516 | 0.794 | 0.529 |
| ovoli | hold-out | 1 | 0.746 | 0.512 | 0.928 | 0.598 | 0.970 | 0.762 |
| gallinacci | hold-out | 26 | 0.538 (0.48–0.60) | 0.521 | 0.528 (0.43–0.62) | 0.525 | 0.797 | 0.514 |

- **Where, region-wide:** the model ranks the finders' cells well against the whole region
  (`auc_region` 0.79–0.97), far above habitat alone (0.50–0.80): the altitude bands and the
  spruce-heavy host lists put the sightings in the right belts.
- **When:** porcini's timing at the finder's cell beats the calendar on the train seasons
  (`auc_time_effort` 0.617 against 0.516, interval above 0.5), the first region where it clearly
  does; on the hold-out it is 0.536, still above the calendar's 0.516 but with an interval that
  crosses 0.5.
- **Where, locally:** within 20 km on the day (`auc_local`) the model beats habitat for porcini on
  the hold-out (0.602 against 0.536) and for gallinacci on the train seasons (0.612 against 0.534),
  and sits near habitat otherwise, as in Tuscany and Piemonte.
- Ovoli: 4 train presences and 1 hold-out; no conclusion.

### Tuning (pre-registered rain search, 2026-09-26)

With 122 usable train presences the card's protocol applies, as Model v1 ran it for Tuscany (55)
and Piemonte (53): `api.model.tuning --region trentino_alto_adige --search rain`, one pass of
coordinate descent on the train seasons 2016–2023, an alternative kept only if it raises the
group's objective (mean of pooled `auc_local` and `auc_time_effort`) by at least 0.02, season
windows, altitude bands and habitat affinities frozen; run once with the rain scale as configured
(`tuned-rain`, ×0.75) and once without (`tuned-rain-scale-off`); a winner judged once on the
hold-out. Porcini's 30-day rain was already relative to the cell's normal, so its `relative`
alternative equals the prior.

| trial (train objective) | scale on (×0.75) | scale off |
|---|---|---|
| start | porcini 0.574, ovoli 0.638, gallinacci 0.571 | 0.558, 0.614, 0.552 |
| porcini trigger higher / much higher | 0.571 / 0.556 | 0.570 / 0.571 |
| porcini `rain_30d` higher / much higher | 0.567 / 0.570 | 0.559 / 0.557 |
| porcini clock cooler / warmer | 0.551 / 0.562 | 0.542 / 0.562 |
| ovoli trigger higher / much higher | 0.568 / 0.590 | 0.608 / 0.545 |
| ovoli `rain_30d` higher / much higher / relative | 0.630 / 0.645 / 0.630 | **0.635** (kept) / 0.601 / 0.591 |
| ovoli clock cooler / warmer | 0.611 / 0.639 | 0.610 / 0.637 |
| gallinacci trigger higher / much higher | 0.566 / 0.569 | 0.559 / 0.552 |
| gallinacci `rain_30d` higher / much higher / relative | 0.569 / 0.567 / 0.584 | 0.560 / 0.554 / 0.568 |
| gallinacci clock cooler / warmer | 0.565 / 0.575 | 0.551 / 0.556 |
| gallinacci sun line off | 0.571 | 0.552 |

- **The rain scale stays on.** With it every group starts higher (porcini +0.015, ovoli +0.024,
  gallinacci +0.018), and the runs end at a mean of 0.594 (scale on) against 0.582 (scale off). The
  scale is fitted to gauges, not sightings; the sightings agree with it here.
- **Nothing clears the margin with the scale on**, the configuration that ships. The best gains are
  gallinacci's 30-day rain relative to the cell's normal (+0.013, also the Piemonte candidate) and
  ovoli's much higher 30-day rain (+0.007), both under 0.02.
- **The one change kept, ovoli's higher 30-day rain, exists only without the scale** (+0.021 on 4
  presences), where it undoes the scale's cut to the ovoli rain; with the scale on the same change
  loses 0.008. There is no candidate in the shipped configuration, and 1 hold-out ovoli presence
  could not judge one. **Nothing is tuned: the researched priors ship** (rules version
  `2e812362221d`, the one the stores were scored with).

### Press contrasts (`sanity.yaml`, `backtest/trentino_alto_adige/onboard/sanity_porcini.csv`)

**11 of 16 hold.**

| contrast | higher | lower | holds |
|---|---|---|---|
| `fiemme_2019_2021` | 0.740 | 0.385 | yes |
| `alta_valsugana_2020_2021` | 0.701 | 0.340 | yes |
| `trentino_july_2023_2022` | 0.705 | 0.518 | yes |
| `vallagarina_low_2024` | 0.702 | 0.708 | no (a tie) |
| `region_early_august_2025` | 0.752 | 0.574 | yes |
| `west_vs_dolomites_2023` | 0.518 | 0.424 | yes |
| `valsugana_vs_southern_trentino_2023` | 0.627 | 0.929 | no |
| `south_tyrol_september_vs_august_2023` | 0.763 | 0.724 | yes |
| `isarco_2025_2023` | 0.411 | 0.761 | no |
| `south_tyrol_2021_poor` | 0.559 | 0.638 | no |
| `south_tyrol_2019_late` | 0.530 | 0.294 | yes |
| `trentino_vs_south_tyrol_august_2019` | 0.608 | 0.571 | yes |
| `trentino_vs_south_tyrol_july_2024` | 0.617 | 0.465 | yes |
| `south_tyrol_vs_trentino_july_2025` | 0.217 | 0.196 | yes |
| `gallinacci_pusteria_2023_2022` | 0.813 | 0.384 | yes |
| `gallinacci_trentino_2024_2025` | 0.640 | 0.691 | no |

- The good and bad years hold, most by wide margins (Fiemme 2019/2021, Alta Valsugana 2020/2021,
  the late 2019 season in South Tyrol, the Val Pusteria chanterelles of 2023 against 2022), and so
  do both cross-province contrasts that run in opposite directions (Trentino ahead in July 2024,
  South Tyrol ahead in July 2025), so no constant bias between the provinces is carrying them.
- **Four misses are weather the reanalysis does not show** (area means of the history tables' rain
  and temperature, weighted by woodland cells):
  - `isarco_2025_2023`: the press calls early August 2025 "molto piovosa" in the Valle Isarco and
    2023 scarce; the reanalysis has the reverse, 2023 at 127 % of the normal 30-day rain with 66 mm
    in the window and 1.1 °C cooler than normal, 2025 at 99 % with 32 mm and 1.1 °C warmer.
  - `valsugana_vs_southern_trentino_2023`: the reanalysis gives southern Trentino (Garda, Vallarsa,
    Ala) 123 % of its normal 30-day rain against the Valsugana's 93 %, the reverse of the Funghi
    Magazine report the contrast rests on.
  - `south_tyrol_2021_poor` ("zu trocken, zu windig, zu heiß"): August to mid-September 2021 comes
    out at 111 % of the normal rain and 1.0 °C cooler than normal over South Tyrol's woods. The
    drought, if it was one, is not in the reanalysis for that window; wind is not in the rules.
  - `gallinacci_trentino_2024_2025`: July 2025 was the wetter and cooler (89 mm and −1.0 °C against
    54 mm and +1.4 °C in 2024) and the rules favour it; the press found fewer chanterelles.
- **One is a tie:** `vallagarina_low_2024` (0.702 against 0.708). The low Vallagarina got 117 % of
  its normal rain and ran 1.7 °C warm in late July 2024; "gran caldo alternato a forti temporali"
  is there, but the storms outweigh the heat in the score.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-26 (`deploy/rsync-region-data.sh
trentino_alto_adige`, 480 files, 436 MB, no redeploy). Checked right after the sync: `/regions`
lists the six live regions without this one, and `/status?region=trentino_alto_adige` answers 404.
The server serves a region only when its YAML is
in the deployed code and its stores are on disk, so they stay inert until `main` with
`config/regions/trentino_alto_adige.yaml` is deployed by the rail's "Deploy pulled main" step, with
the daily job. **The stores stop at 2026-09-20**: Open-Meteo's daily limit was spent on 2026-09-26
before the forecast and the seasonal tendencies could be fetched, so the served window (today −6 to
+7, with factors) and the outlook come from the server's first daily job for the region. The merged
`main` must carry this branch's fix to `/overview` (`api/src/api/registry.py`): without it the hub's
overview answers 404 for every region until that job has scored Trentino-Alto Adige through today.
Then check:

- [ ] The daily job after the deploy has a `region_done` line for `trentino_alto_adige`
  (`journalctl -u mushma-daily`), with the weather update filling 2026-09-21 onward, the served
  window scored with factors, the seasonal fetch and the outlook built; its Open-Meteo call count
  stays inside the budget.
- [ ] `https://mappafunghi.app/trentino-alto-adige` and `/trentino-alto-adige/porcini`, `/ovoli`,
  `/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this score"
  names the region's habitats (spruce and fir, larch and stone pine, Scots pine, beech).
- [ ] `https://api.mappafunghi.app/regions` lists `trentino_alto_adige` with all three species; the
  hub `/` lists it and colours it from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Trentino-Alto Adige URLs (built from the
  registry).
- [ ] Lighthouse SEO is 100 on `/trentino-alto-adige` (prerendered title, description, canonical,
  og image `og/trentino-alto-adige.png`, JSON-LD Dataset with `sameAs` Wikidata Q1237).
- [ ] `/credits` shows "Provincia autonoma di Trento — Tipi forestali PAT integrati 2021" and
  "Provincia autonoma di Bolzano — Tipologie forestali dell'Alto Adige".
- [ ] The next morning's daily job has a `region_done` line for `trentino_alto_adige` again, and no
  `region_failed`.

## Known limitations

- **Rain scale from South Tyrol alone.** 17 woodland gauges, all in the province of Bolzano; the
  scale is applied to Trentino too, whose Prealps are wetter (Validation, rain gauges). Fitted on
  2019–2023 it held the wet 2024 at 0.87.
- **Drizzle.** The reanalysis rains on 59 % of days against the gauges' 28 % and gives half the rain
  of the heavy days; at ×0.75 a 3-day total of 30 mm comes half as often as at the gauges.
- **Bolzano's forest types are site types.** The map names the trees a site carries, not a survey of
  what grows there; spruce planted on beech or fir sites is typed by the site. Trento's map is a
  survey of the real types.
- **Chestnut is barely mapped** (7 cells where dominant): Trento's map holds 754 ha of castagneti,
  Bolzano's has no chestnut group (chestnut sits inside two oak types). Ovoli and *B. aereus* lean on
  oak here instead.
- **Region finder by bbox.** The web registry finds a region by bbox (`findRegionAt`). This bbox
  (10.38–12.48° E, 45.67–47.10° N) takes in Belluno, Cortina and the Asiago plateau (Veneto), the
  Garda shore of Lombardy and Val Müstair (Switzerland); and Lombardia's bbox, on its own branch,
  takes in most of Trentino, Trento city included, so once both are served a fix in Trento from the
  hub goes to whichever comes first in the registry. Added to `fix-region-lookup-by-boundary.md`.
- **Lapse rates.** Minimum and mean temperature cool 1.06 °C/km faster with height than the
  national rates, without a measurable downscaling gain from the region's own (Config, Lapse
  rates).
- **Snowfall at the northern edge.** The five nodes at 47.2° N take the Italy-wide snowfall file's
  47.1° N row (Weather history).
