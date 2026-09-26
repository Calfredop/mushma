# lombardia

Region #8 of the full-Italy rollout (card `region-lombardia.md`). API id `lombardia`, web slug
`/lombardia`, ISTAT COD_REG 3, Wikidata Q1210 ("Lombardia" / "Lombardy"). Config:
`api/src/api/config/regions/lombardia.yaml`; species evidence:
`.gavin-root/docs/species-ecology/lombardia.md`.

The branch was built on the lanes' unmerged work: `region/marche` (with Liguria), then
`region/umbria` and `region/emilia-romagna` were merged into `region/lombardia` on 2026-09-26, at
the human's request, before any Lombardia change. The two lanes had written the forest-source
loader twice; the merge keeps Emilia-Romagna's group layers (`forest.groups` as a list, each with
its `where`) and Liguria's one-map read (a single unfiltered group layer that is also the types
source is read once), in `api.grid.build.read_forest_cover`.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Lombardia, **Carta forestale (perimetro del bosco)** with the real forest types, revision of 2026-07-16 (`lr_carta_forestale`) | CC BY 4.0 (metadata use constraint) | ArcGIS REST MapServer, 47 sublayers |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| rain gauges (check only) | ARPA Lombardia, Idro-Nivo-Meteo network on dati.lombardia.it | CC0 1.0 | `api.weather.arpa_lombardia` |
| sightings | GBIF (bbox), iNaturalist place 10870 "Lombardia, IT" | per record | counts per cell only |

**What was checked, and why the Carta forestale.**

- **DUSAF 7.0** (the card's candidate: Regione Lombardia / ERSAF land use 2021, 1:10,000, CC BY 4.0,
  shapefile on the Geoportale): its forest classes are broadleaf, conifer and mixed woods by
  density (3111x, 3121x, 3131x) and recent plantings, with no forest type. It would give how much
  forest but not which kind.
- **Carta forestale (perimetro del bosco)**, the same Geoportale, metadata
  `r_lombar:7ceabf1c-28b2-4c0b-b4ba-4be3d17afa33`: the forest of l.r. 31/2008 art. 42 as the
  mosaic of the Piani di Indirizzo Forestale's real forest-type maps (Del Favero's Lombard
  typology: categoria, tipo, variante; "faggeta montana dei substrati carbonatici", "pecceta
  altimontana", "lariceto tipico"…), completed with DUSAF's forest classes where a PIF has no types.
  1:10,000 equivalent, 4 m positional accuracy, revised 2026-07-16, use constraint CC BY 4.0. Each
  polygon has its category (`CATEGORIA`), subcategory (`LEGENDA_1`), type (`TIP_RL`) and type code.
  **One map gives both layers**, read once, like Liguria's and the Marche's.
- **Carta dei tipi forestali reali** (`carta_reali_forestali`): a raster of the same typology; the
  vector map above supersedes it. **Carta tipi forestali potenziali**: modelled, not observed.
- **CLC IV alone** (the fallback): not needed.

**Download.** The Geoportale's shapefile package sits behind a JSF form (session cookie, view
state, auth token), which the build's `fetch` cannot script. The Region's ArcGIS REST MapServer
(`cartografia.servizirl.it/arcgis2/rest/services/agricoltura/carta_forestale`) serves the map as one
sublayer per legend class, 1,000 features a page, so the source lists its **47 polygon sublayers as
`parts`** (315,943 polygons, 342 pages, about 260 MB with `geometry_precision: 0`, i.e. whole metres
in EPSG:3035; 17 min the first time). Two loader fixes came with it:

- `fetch_arcgis_features` stepped the offset by the requested page size (2,000) while this server
  answers 1,000: it would have skipped every other thousand features. It now steps by the features
  returned.
- ArcGIS and WFS `parts` each get their own cache folder (`part_<hash>`); they shared one, so the
  second part found the first one's `.complete` marker.

Class mapping (`lombardia.yaml`, `LEGENDA_1` → group and habitat), whole-map areas from the service's
statistics:

| `LEGENDA_1` | group | habitat | ha |
|---|---|---|---|
| Orno-ostrieti; Carpineti; Aceri-frassineti ed Aceri-tiglieti; Betuleti e Corileti; Altre formazioni particolari (laburnum, white poplar, aspen, rowan) | broadleaf | mixed_broadleaf | 125,579 |
| Peccete (altimontane, montane, secondarie, di sostituzione e azonali, non classificabili); Abieteti | conifer | fir_spruce | 76,782 |
| Castagneti; Castagneti da frutto DUSAF | broadleaf | chestnut | 73,151 |
| Faggete (altimontane, montane, submontane, primitive, non classificabili) | broadleaf | beech | 67,655 |
| Lariceti; Larici-cembreti e Cembrete | conifer | other_conifer | 60,532 |
| Robinieti puri e misti; Formazioni di ciliegio tardivo; Formazioni antropogene non robinieti | broadleaf | exotic_broadleaf | 42,071 |
| Querceti di rovere, roverella, cerro, farnia, non classificabili; Querco-carpineti | broadleaf | deciduous_oak | 39,218 |
| Alneti di ontano bianco e nero; Saliceti; Formazioni ripariali DUSAF | broadleaf | riparian | 11,128 |
| Pinete di pino silvestre montane e planiziali | conifer | mountain_pine | 10,754 |
| Querceti di leccio (Garda and Lario cliffs) | broadleaf | evergreen_oak | 296 |
| Latifoglie DUSAF; Aree boscate non classificate | broadleaf | typed from neighbouring cells | 51,148 |
| Conifere DUSAF | conifer | typed from neighbouring cells | 3,029 |
| Piceo-faggeti; Misti DUSAF; Rimboschimenti recenti (and DUSAF's) | mixed | mixed_broadleaf_conifer | 30,890 |
| Cespuglieti con presenza significativa di specie arbustive alte ed arboree DUSAF (CLC 324) | transitional | transitional_woodland_shrub | 5,894 |
| Alneti di ontano verde; Mughete; Arbusteti (ginepro nano, rodoro-vaccinieti) | left out | | 25,651 |

- **Left out**: green-alder and mountain-pine scrub and the dwarf-shrub heaths, which INFC counts
  outside "bosco" (arbusteti subalpini) and CLC files under 322, left out in every region. They
  hold 25,651 ha, mostly above the treeline.
- **Rimboschimenti recenti** are 6,567 ha of conifer and 2,903 ha of broadleaf plantings (`TIP_RL`),
  hence `mixed`, the one group that says both.
- **Aree boscate non classificate** (7,629 ha, woods no PIF typed) are mostly in the plain and the
  prealps (about 750 ha north of 46.1° N), so they are broadleaf, typed from the neighbouring
  cells, as Emilia-Romagna's uncategorised woods are.
- **Larch and stone pine → `other_conifer`**, as the vocabulary defines it and as Liguria and
  Emilia-Romagna map theirs; **Scots pine → `mountain_pine`**; hornbeam with hop-hornbeam →
  `mixed_broadleaf`, oak-hornbeam of the plain and the moraines → `deciduous_oak`.

## Woodland grid

Built 2026-09-26 (`uv run python -m api.grid.build --region lombardia`; 100 s with a warm cache).

- Cells 24,715; inside area 23,876.9 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 6,018** (a quarter of the cells: the Po plain is farmland; the woods are the Alps,
  the prealps and the Oltrepò Apennine). 673 of the 1,501 comuni have woodland cells.
- **Forest area 592,446 ha vs INFC 2015 bosco 621,968 ha: −4.7 %**, within ±10 %. The mapped forest
  groups hold 592,233 ha, which the 20 m rasterization reproduces; with the left-out subalpine
  scrub the map holds 617,884 ha (−0.7 %).
- 91 % of woodland cells take all their forest types from their own polygons (mean
  `borrowed_type_fraction` 5.3 %; 337 cells borrow more than half, mostly DUSAF and unclassified
  woods in the prealps). The dominant habitat covers a median 72 % of a cell's wooded area.
- Terrain: woodland elevation median 921 m (5th–95th percentile 307–1,781 m), highest cell mean
  2,328 m (a pixel at 2,630 m); slope median 27.5° (Tuscany 16.6°, Marche 22.2°), 63 % of woodland
  cells above 25°; 188 cells have no aspect.
- Soil pH (SoilGrids, not scored): woodland median 6.00 (5.45–6.63), more acid than the Apennine
  regions: the Alpine crystalline rocks.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| mixed_broadleaf (hop-hornbeam, maple-ash, birch-hazel) | 24.4 % | 1,527 | 789 m |
| chestnut | 15.4 % | 982 | 627 m |
| fir_spruce | 14.7 % | 950 | 1,416 m |
| beech | 13.7 % | 822 | 1,091 m |
| other_conifer (larch, stone pine) | 10.2 % | 598 | 1,668 m |
| deciduous_oak | 6.6 % | 363 | 506 m |
| mixed_broadleaf_conifer (spruce-beech, recent plantings) | 5.3 % | 284 | 1,056 m |
| exotic_broadleaf (robinia) | 4.0 % | 220 | 330 m |
| riparian | 2.9 % | 160 | 435 m |
| mountain_pine (Scots pine) | 2.1 % | 111 | 732 m |
| transitional_woodland_shrub | 0.6 % | 1 | 713 m |
| evergreen_oak | 0.0 % | 0 | |

The belts read as the Lombard Alps should: robinia and oaks in the high plain and the hills,
hop-hornbeam and chestnut on the prealpine slopes (chestnut-dominated cells are most common at
Gravedona ed Uniti, Vobarno, Val di Nizza, Maccagno and Pisogne), beech around 1,100 m (Brallo di
Pregola, Tremosine, Taleggio, Valtorta), spruce at 1,400 m (Corteno Golgi, Sondalo, Valdisotto,
Ardesio, Teglio) and larch and stone pine at 1,700 m (Valfurva, San Giacomo Filippo, Chiesa in
Valmalenco).

Woodland cells by province: Brescia 1,719, Bergamo 1,205, Sondrio 1,203, Como 598, Varese 489,
Lecco 382, Pavia 361, Milano 47, Monza e Brianza 7, Cremona 6, Mantova 1.

Threshold sensitivity (recomputed from the stored fractions, one cell off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 7,597 | 6,806 | **6,017** | 5,123 | 4,139 |

Spot checks:

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Valtellina, Val Masino | `1kmE4292N2569` | yes | 0.61 | fir_spruce 0.33, other_conifer 0.30, mixed_broadleaf 0.26 | 976 | 22 | 5.7 | Val Masino (SO) | San Martino, 0.4 km |
| Valfurva near Bormio | `1kmE4354N2591` | yes | 0.98 | other_conifer 0.72, fir_spruce 0.28 | 1974 | 27 | 6.3 | Valfurva (SO) | Niblogo, 3.2 km |
| Ponte di Legno, Val Camonica | `1kmE4361N2570` | yes | 0.91 | fir_spruce 0.95, other_conifer 0.05 | 1518 | 29 | 6.5 | Ponte di Legno (BS) | Ponte di Legno, 1.8 km |
| Foppolo, Orobie (ski slopes) | `1kmE4302N2548` | no | 0.21 | other_conifer 0.86, fir_spruce 0.14 | 1767 | 20 | 6.1 | Foppolo (BG) | Foppolo, 0.9 km |
| Lario above Blevio | `1kmE4250N2524` | yes | 0.65 | mixed_broadleaf 0.73, chestnut 0.27 | 432 | 31 | 5.6 | Blevio (CO) | Blevio, 1.1 km |
| Campo dei Fiori, Varese | `1kmE4225N2529` | yes | 0.99 | beech 0.83, mixed_broadleaf_conifer 0.06, fir_spruce 0.06 | 1014 | 27 | 5.5 | Castello Cabiaglio (VA) | Brinzio, 2.3 km |
| Valsassina, Moggio | `1kmE4281N2535` | yes | 0.63 | beech 0.73, mixed_broadleaf 0.23, chestnut 0.04 | 920 | 23 | 6.0 | Moggio (LC) | Moggio, 0.4 km |
| Val Brembana, San Pellegrino | `1kmE4294N2525` | yes | 0.52 | mixed_broadleaf 0.94, mixed_broadleaf_conifer 0.05 | 523 | 24 | 6.2 | San Pellegrino Terme (BG) | Aplecchio, 0.2 km |
| Garda cliffs, Gargnano | `1kmE4372N2509` | yes | 0.73 | mixed_broadleaf 0.53, deciduous_oak 0.28, evergreen_oak 0.17 | 419 | 33 | 6.7 | Gargnano (BS) | Gargnano, 0.7 km |
| Oltrepò, Brallo di Pregola | `1kmE4263N2403` | yes | 0.78 | beech 0.99, mountain_pine 0.01 | 920 | 15 | 6.4 | Brallo di Pregola (PV) | Bralello, 0.4 km |
| Oltrepò, Menconico | `1kmE4263N2410` | yes | 0.64 | deciduous_oak 0.95, beech 0.05 | 679 | 12 | 6.8 | Menconico (PV) | Vigomarito, 0.3 km |
| Oltrepò near Varzi | `1kmE4258N2413` | no | 0.45 | deciduous_oak 0.90, chestnut 0.10 | 541 | 13 | 6.8 | Varzi (PV) | Rosara, 1.0 km |
| Milano | `1kmE4257N2483` | no | 0.00 | — | 132 | 7 | — | Milano (MI) | Milano, 1.7 km |

## Weather

- Points: 101 candidates on the 0.2° lattice, all on land; all 6,018 woodland cells weighted.

### Lapse rates: Lombardia's own for air temperature

`uv run python -m api.weather.checks lattice --region lombardia` (260 land nodes at 0.1°, −7 to
2,611 m, three 14-day windows of 2024). Cooling per km of height across nodes, median of daily
fits:

| variable | Jan | Jul | Oct | all | national | difference |
|---|---|---|---|---|---|---|
| temperature_2m_max | 5.78 | 5.77 | 4.48 | 5.47 | 4.5 | +0.97 |
| temperature_2m_mean | 6.24 | 6.37 | 5.10 | 5.74 | 4.5 | **+1.24** |
| temperature_2m_min | 6.46 | 6.53 | 5.33 | 5.94 | 4.2 | **+1.74** |
| soil_temperature_0_to_7cm_mean | 0.26 | 5.49 | 4.59 | 4.59 | 3.7 | +0.89 |

Mean and minimum temperature are past the card's 1 °C/km line, and unlike Emilia-Romagna's and
Piemonte's small excesses (−1.06 and +1.04, both kept national because the fitted rate did not
predict better), here the fitted rates **predict better**. Leave-out RMSE (°C) when the lattice
skips nodes and predicts them from the rest:

| variable | 0.2° national | 0.2° fitted | 0.3° national | 0.3° fitted |
|---|---|---|---|---|
| temperature_2m_min | 0.613 | **0.582** | 0.821 | **0.782** |
| temperature_2m_mean | 0.398 | **0.371** | 0.567 | **0.514** |
| temperature_2m_max | 0.337 | **0.315** | 0.524 | **0.463** |
| soil_temperature_0_to_7cm_mean | **0.585** | 0.587 | **0.715** | 0.744 |

The steep rates are not a winter inversion artefact: July and October fit as steeply as January
(daily fits' standard deviation 0.4–0.6 °C/km in July and October, against 1.1–1.5 in January).
So **`lombardia.yaml` sets `weather.lapse_rates`**: 5.9 (min), 5.7 (mean), 5.5 (max; just under the
line, but it predicts better at both spacings and keeps the three consistent). Soil keeps the
national 3.7, because its fitted 4.6 predicts worse (and its January fit is snow-bound). The weather
config had no per-region lapse rate: `load_weather_config(region=…)` now applies a region's
`weather.lapse_rates`, and scoring, the backtest, the history normals, the ingest, the seasonal
fetch and the checks load their region's config. Every other region is unchanged. With no
correction at all the RMSE is 0.65 °C (mean) and 0.81 °C (min) at 0.2°; 6.5 °C/km gives 0.368 and
0.579, close to the fitted rates.

### History

Copernicus ERA5-Land from the CDS time-series product, one request per node for 2016-01-01 to
2026-09-14 (101 nodes, 4.34 M daily values; 32 node series came from the shared cache, being
Piemonte's, Emilia-Romagna's and Liguria's border nodes, and 69 were fetched in 52 min on
2026-09-26). Snowfall, which that product lacks, came from the Italy-wide gridded snowfall cache
(23 half-years, 2016 to 2026-09-14), so no gridded request and no Open-Meteo archive call was
needed. The backfill stopped at 2026-09-14, where the neighbours' node series and the snowfall cache
end, so that both came from cache; Open-Meteo's archive and the ECMWF IFS forecast fill the days
after it (Data below).

### Rain gauges: ARPA Lombardia, and a rain scale fitted on May to October

`uv run python -m api.weather.checks gauges --region lombardia --start 2019-01-01 --end 2025-12-31`.
ARPA Lombardia's Idro-Nivo-Meteo network is open data on the Region's portal (CC0 1.0): the sensor
registry (`nf78-nj6b`, 326 rain sensors with height and position) and every gauge's validated
readings at up to 10-minute steps ("Precipitazioni dal 2011 al 2020" `2kar-pnuk`, "dal 2021"
`pstb-pga6`), stamped in CET at the end of their interval. `api.weather.arpa_lombardia` asks the
portal's SoQL to sum each year's valid readings (states VA, VV) into CET days with their count, one
CSV per year (about 30 s each), and keeps a day when the gauge sent at least 90 % of its usual
readings (144 for a 10-minute gauge). CET days are the model's calendar days in winter and an hour
off in summer. 268 gauges have 2019-2025 data; **60 sit in woodland cells with at least 80 % of
days** (241-2,040 m, median 994 m).

**A dozen readings flagged valid are counter spikes**: one 10-minute value of 21,164 mm (Varano
Borghi, 28 Nov 2019), 109,499 mm (Caino, 22 May 2020), 127,786 mm (Piazzatorre, 12 Feb 2020) and
nine more, from 1,625 mm up. The wettest real gauge-day of 2019-2025 is 266 mm (20 Oct 2023). Gauge-days
over 500 mm are dropped (`plausible_days`); with them in, the pooled model/gauge ratio read 0.76
and three gauges correlated at 0.0.

| elevation band | gauges | pooled model/gauge, all year | May-Oct | Nov-Apr |
|---|---|---|---|---|
| up to 800 m | 16 | 1.018 | 1.035 | 0.987 |
| 800-1,200 m | 27 | 1.058 | 1.067 | 1.042 |
| 1,200-1,600 m | 6 | 1.132 | 1.043 | 1.344 |
| above 1,600 m | 11 | 1.293 | 1.103 | 1.835 |
| **all** | **60** | **1.085** | **1.061** | **1.132** |

Median daily correlation 0.78, wet 3-day windows caught 87 % of the time (false alarms 18 %),
median 3-day error 13 mm. Unlike Tuscany (reanalysis 0.63-0.79 of the gauges) and the Apennine
neighbours, **ERA5-Land is slightly wet here**, and the excess above 1,200 m is a winter one: from
November to April the high gauges, unheated in the snow, catch little of it. In the months the
rules score the reanalysis is 1.03-1.10 of the gauges in every band.

So the rain scale is **fitted on May to October**: least squares through the origin of gauge totals
on model totals × (a + b × elevation) gives **a = 0.960, b = −0.017 per km** (config: 0.96 − 0.02
per km, elevation clamped at 2,000 m), which brings the pooled ratio to 1.00 (median gauge 1.03).
The whole year's fit, 1.06 − 0.13 per km, would dry the Alpine cells' summer rain for a winter
gauge fault. The correction is small and **within the spread between years**: 2019-2022 alone fit
0.94 − 0.04 per km, 2023-2025 alone 0.97 + 0.02, and raw rain matched the gauges in 2023-2025
(1.006); the 2019-2022 fit applied to 2023-2025 reads 0.90. It is set because a CDS region needs its
own `precipitation_scale` anyway: the national block scales `era5_seamless` only while the rain
normals are scaled whatever their source (Liguria's finding), and at Lombard heights the national
1.28 + 0.29 per km would make the rain 50-80 % too wet. Reference
`mushma_lombardia_gauge_check_2026`.

## Sightings

`uv run python -m api.sightings.ingest fetch --region lombardia` (2026-09-26): 1,472 GBIF records for
the three groups over the bbox (which also takes in Ticino, Graubünden and the neighbouring regions'
edges) and 8 iNaturalist records of the last two weeks. After the quality filters (1,130 too
imprecise, 105 with unknown uncertainty, 20 of an excluded basis, 2 undated) 328 are kept, and
**128 land on Lombardia's woodland cells** (porcini 75, gallinacci 48, ovoli 5). Unique, unobscured
group-cell-days: **65 in the train seasons 2016-2023** (porcini 42, gallinacci 20, ovoli 3; 62 of
them 2019-2023) and 26 in the hold-out 2024-2025 (porcini 12, gallinacci 13, ovoli 1). The
species research counted 403 Lombard iNaturalist records of the six taxa, most with obscured
locations, which never reach GBIF at a usable precision.

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/lombardia.md`; rules in
`api/src/api/config/species/lombardia/` (44 new references, all opened).

- **All three groups and six keys kept.** Every taxon has Lombard records and a Lombard society or
  institutional source; the ovolo is named in the regional law (l.r. 31/2008, art. 98). *B. aereus*
  is the weakest key (9 records, all but one below 600 m) and keeps a hill-only band.
- **Lombardia is conifer country above 1,000 m**, so the changes are Alpine:
  - *B. edulis* and *B. pinophilus* get an **Alpine summer window** (full 1 August or 25 July to 25
    September, closed by 25 October) blended in above 900-1,300 m, and bands reaching 2,100-2,200 m;
  - **larch and stone pine (`other_conifer`) drop to non-host (0.1)** for *B. edulis*, *B.
    pinophilus* and gallinacci: root-tip studies in the South Tyrol larch and stone-pine belt found
    no *Boletus*, and the Lombard records above 1,500 m sit in spruce;
  - Scots pine (`mountain_pine`) becomes a full *B. pinophilus* host; gallinacci take beech and
    spruce/fir as full hosts, a band to 2,100 m and no winter mode;
  - *B. reticulatus*, *B. aereus* and ovoli end earlier (31 October, 20 November, 15 November).
- **Unchanged: every weather rule and growth clock.** No Lombard or Alpine study gives better
  numbers.
- **Slope stopper moved onto the Lombard grid**: ×1 to 35°, ×0.8 from 46° (woodland median 27.5°,
  p90 35.1°).
- **Press contrasts** (`lombardia/sanity.yaml`): 14 from 2017-2025, written before any Lombard score
  existed: 10 porcini, 2 gallinacci, 2 ovoli, in Valtellina, the Orobie bergamasche, Val Camonica,
  the upper Valle Staffora, the Oltrepò and the alto Varesotto.

## After the deploy: what to verify

The server serves a region only when its YAML is in the deployed code and its stores are on disk.
The stores go to the server with `deploy/rsync-region-data.sh lombardia` (the "Rsync region data"
tool) before the deploy and stay inert until the rail's "Deploy pulled main" step deploys `main`
with `config/regions/lombardia.yaml` and runs the daily job. Then check:

- [ ] `https://mappafunghi.app/lombardia` and `/lombardia/porcini`, `/lombardia/ovoli`,
  `/lombardia/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Lombard habitats (spruce as fir/spruce, larch as other conifer, hop-hornbeam as mixed
  broadleaf).
- [ ] `https://api.mappafunghi.app/regions` lists `lombardia`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Lombardia URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/lombardia` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Lombardia", description, canonical, og image `og/lombardia.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1210).
- [ ] `/credits` shows "Regione Lombardia — Carta forestale e tipi forestali reali".
- [ ] The next morning's daily job has a `region_done` line for `lombardia`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget: Lombardia
  adds 101 nodes, the most of any region so far.
- [ ] The deployed code applies Lombardia's own lapse rates: `/srv/mushma-data/weather/lombardia/meta.json`
  (rewritten by each ingest) lists `lapse_rate_c_per_km` 5.9 / 5.7 / 5.5 for minimum, mean and
  maximum temperature, and Tuscany's still lists 4.2 / 4.5 / 4.5.

## Known limitations

- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point, the
  current region first. Lombardia's bbox [8.49, 44.67, 11.43, 46.64] takes in eastern Piemonte (the
  western shore of Lago Maggiore, Novara), the Piacenza and Parma Apennine of Emilia-Romagna, the
  Veronese shore of Garda, the Alto Garda trentino and the Adamello, and **Switzerland's Ticino and
  Graubünden valleys** (Lugano, Mesolcina, Poschiavo, part of the Engadine), which are in no served
  region. Inside `/lombardia` a tap or search there opens Lombardia's forecast for a point outside
  its grid; from the hub, Lugano offers Lombardia. Card `fix-region-lookup-by-boundary.md`.
- **Forest map read through 47 REST sublayers.** If the Region renumbers the `carta_forestale`
  MapServer's layers, a listed id may answer an error or another class. Polygons are tagged by their
  own `LEGENDA_1`, so nothing is mis-tagged, but a class whose layer moved would be left out, and the
  INFC check would show the missing area. The fix is to list the new ids (`?f=json` on the
  MapServer) or to script the Geoportale's shapefile package.
- **Rain scale inside the years' spread** (Weather above); card
  `fix-rain-calibration-region-borders.md`. Lombardia's rain meets Piemonte's, Emilia-Romagna's and
  Veneto's at long borders.
- **Lapse rates are per region now**, and only Lombardia has its own. The Alpine neighbours still to
  come (Valle d'Aosta, Trentino-Alto Adige, Veneto, Friuli-Venezia Giulia) should compare their
  lattice fits the same way; Piemonte's +1.04 did not predict better on its lattice.
- **Subalpine scrub left out.** Green alder and mountain pine (25,651 ha with the heaths) score as
  non-woodland, like CLC 322 elsewhere; if foragers report porcini or chanterelles under mountain
  pine, the mughete could come back as `mountain_pine` fractions.

## Data

- cells: 24715
- woodland cells: 6018
- INFC deviation: -4.8% (grid 592,446 ha vs 621,968 ha) — within ±10 %
- weather nodes: 101
- years stored: none
- sightings kept: None
