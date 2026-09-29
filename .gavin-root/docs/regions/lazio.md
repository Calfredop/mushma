# lazio

Region #4 of the full-Italy rollout (card `region-lazio.md`). API id `lazio`, web slug `/lazio`,
ISTAT COD_REG 12, Wikidata Q1282. Config: `api/src/api/config/regions/lazio.yaml`. Tuscany's
neighbour to the south: volcanic lake districts (Volsini, Cimini, Sabatini, Colli Albani) in the
west, the limestone Apennines (Reatini, Simbruini, Ernici, Lepini, Ausoni, Aurunci) in the east.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Lazio, **Carta forestale su base tipologica** (1:10,000; E-GEOS and Forest Lab for the Agenzia Regionale Parchi, final test February 2011; Chirici et al. 2014, Forest@ 11: 65–71) (`lazio_carta_forestale`) | CC BY 4.0 | WFS SHAPE-ZIP from the regional geoportal, the download the open-data portal publishes; no login |
| forest-area cross-check | Regione Lazio, Carta di Uso del Suolo 1:25,000 (CUS 2000; the 2016 update revises urban and farm classes only) | CC BY 4.0 | WFS on the same geoportal; not used by the build |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | one open-sea DEM tile does not exist (below) |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| rain check | Regione Lazio, ARSIAL SIARL agrometeo network (station list and "Serie Storica Agrometeo") | CC BY 4.0 | validation only (Weather) |
| sightings | GBIF (bbox), iNaturalist place 8670 "Lazio, IT" | per record | counts per cell only |

**What was checked, and why the Carta forestale.**

- **Carta forestale su base tipologica** (the card's second candidate, "the regional forest
  typology map"): the Region's forest-type map, photo-interpreted at 1:10,000 (0.5 ha minimum unit)
  from the 2005–2007 ADS40 flight and SPOT5 images, derived from the Region's Carta delle formazioni
  naturali e seminaturali. 39,095 polygons, each with its forest category (`categoria`: Faggeta,
  Cerreta, Castagneto, Lecceta, Ostrieto…) and type (`tipologia`: "Faggeta montana eutrofica",
  "Castagneto (eutrofico) su depositi vulcanici", "Cerreta acidofila e subacidofila collinare"…,
  35 types), plus cover class (`copertura`: 2 = forest 10–50 %, 3 = forest over 50 %, 4 =
  shrubland) and structure (coppice, high forest, composite). One layer gives both the broad
  groups and the forest types, read once (Marche's pattern), at ten times the scale of CLC IV.
  The open-data portal (dati.lazio.it, dataset "carta-forestale-su-base-tipologica-della-regione-lazio",
  holder Regione Lazio, Direzione Capitale Naturale, Parchi e Aree Protette) lists it with
  `license_id: cc-by4` in its catalogue record (`/api/3/action/package_show`), though its English
  dataset page shows no licence. The geoportal layer is `geonode:tipi_forestali2`.
- **Carta di Uso del Suolo** (CUS, the card's first candidate): the Region's land-use map at
  1:25,000 (2000 edition, 77,395 polygons; CC BY 4.0), CLC to the fourth and fifth level. Its forest
  classes are only 311 broadleaf (473,913 ha), 312 conifer (10,912 ha) and 313 mixed (7,975 ha),
  with 2242 chestnut orchards (9,852 ha) among the tree crops: no forest types, so it could only
  give `forest.groups`, with CLC IV for the types. The 2016 update (16,511 polygons) re-maps
  urban and farm land only. It serves as the cross-check below. No 1:10,000 land-use map is
  published on the geoportal; the Carta forestale is the Region's 1:10,000 map of its woods.
- **ISPRA Carta della Natura, Lazio**: the habitat map at 1:50,000 (2009), coarser and older than
  the Carta forestale; a GeoPackage exists on ISPRA's SDI (`CNAT_Habitat_Lazio.gpkg`, 341 MB).
  Not needed.
- **Carta Forestale d'Italia CFI2020** (CREA): shapefiles on request only, as for Marche and Umbria.

**Download.** `https://geoportale.regione.lazio.it/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typename=geonode%3Atipi_forestali2&outputFormat=SHAPE-ZIP&srs=EPSG%3A25833&format_options=charset%3AUTF-8`
(87 MB zip, one shapefile, EPSG:25833; 19 s on 2026-09-28). GeoServer returns all 39,095
features in one response, so no paging. Several other resources on dati.lazio.it answer HTTP
500 (the Protezione Civile station list, some SIARL years); this one did not.

Class mapping (`lazio.yaml`, by `tipologia`), whole-map areas:

| Carta forestale type (category) | group | habitat | ha |
|---|---|---|---|
| Cerreta acidofila / neutro-basifila, collinare / submontana; Querceto a cerro e farnetto (Cerreta) | broadleaf | deciduous_oak | 130,943; 14,387 |
| Querceto a roverella mesoxerofilo, con cerro (Querceto a roverella); Querceto a farnia; Querceto a caducifoglie mediterranee xerofile | broadleaf | deciduous_oak | 71,972; 64; 794 |
| Faggeta montana eutrofica, termofila e basso montana, altomontana e rupestre | broadleaf | beech | 86,079 |
| Ostrieto mesofilo; Orno-ostrieto e boscaglie a carpinella (Ostrieto); Bosco di forra | broadleaf | mixed_broadleaf | 83,887; 3,329 |
| Castagneto su depositi vulcanici, dei substrati arenacei e marnosi, dei rilievi calcarei, su lave acide | broadleaf | chestnut | 56,443 |
| Lecceta mesoxerofila, costiera termofila, rupicola, con faggio; Sughereta con caducifoglie, costiera tipica | broadleaf | evergreen_oak | 44,152; 2,707 |
| Altri boschi igrofili; Saliceto ripariale | broadleaf | riparian | 16,770 |
| Robinieto/ailanteto | broadleaf | exotic_broadleaf | 1,201 |
| Rimboschimento di pini e/o altre conifere montane | conifer | mountain_pine | 11,536 |
| Pineta di pino domestico; Pineta di altre specie termofile | conifer | mediterranean_pine | 4,134; 2,546 |
| Arbusteti a specie della macchia mediterranea | macchia | macchia | 13,234 |
| Arbusteti temperati; Boschi di neoformazione; Boscaglie a paliuro e terebinto | transitional | transitional_woodland_shrub | 64,026; 9,859; 796 |

Forest (broadleaf + conifer) 530,943 ha on the whole map. There is no mixed class and no fir or
spruce class (INFC 2015 gives Lazio no silver-fir wood; `species-ecology/lazio.md`). **Chestnut
orchards are already in**: 9,268 of CUS 2000's 9,852 ha of *castagneti da frutto* (94 %) lie inside
Carta forestale polygons, 7,556 ha of them as Castagneto (Pescorocchiano, Sutri, Caprarola,
Capranica, Collalto Sabino, Vallerano, Ronciglione), so no second layer is needed. **Querceto a
caducifoglie mediterranee xerofile** is filed under Pseudo-macchia but is a deciduous-oak wood with
10 % or more tree cover, so it counts as forest; the rest of Pseudo-macchia (regrowth on abandoned
land, *Paliurus* and *Pistacia terebinthus* scrub) is transitional, as CLC 324 is. **Conifer
reforestation goes to `mountain_pine`**: black pine on the limestone mountains (median 929 m of the
cells it dominates). Left out: timber plantations (*arboricoltura da legno*, 818 ha), as UCS and
CLC leave plantations to farmland in Tuscany.

## Woodland grid

Built 2026-09-28 (`uv run python -m api.grid.build --region lazio`, 82 s with the DEM tiles
fetched for the first time).

- Cells 17,868; inside area 17,209 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 4,799** (27 % of the cells), in 318 of the 378 comuni. By province: Rieti
  1,636, Frosinone 1,158, Roma 1,125, Viterbo 546, Latina 334.
- **Forest area 530,501 ha vs INFC 2015 bosco 560,236 ha: −5.3 %**, inside ±10 %. The 20 m
  rasterization reproduces the map's 530,943 ha within 0.1 %. CUS 2000 holds 492,800 ha of forest
  (−12.0 %), 502,652 ha with its chestnut orchards (−10.3 %): the Carta forestale's 0.5 ha unit
  finds more of the small woods.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 81 % of a cell's wooded area.
- Terrain: woodland elevation median 726 m (5th–95th percentile 145–1,479 m), highest cell mean
  1,853 m (Accumoli, the Laga), highest point in a woodland cell 2,121 m (Filettino, the
  Simbruini); slope median 19.3° (Tuscany 16.6°), 18 % of woodland cells above 25°; 176 cells
  have no aspect. 20 slivers (no woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.76 (6.31–7.15, 5th–95th percentile).

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (Turkey, downy and Hungarian oak) | 32.3 % | 1,772 | 503 m |
| beech | 19.9 % | 989 | 1,309 m |
| mixed_broadleaf (hop-hornbeam, ravine woods) | 18.9 % | 972 | 769 m |
| chestnut (woods and orchards) | 11.0 % | 535 | 651 m |
| evergreen_oak (holm and cork oak) | 7.9 % | 392 | 579 m |
| transitional_woodland_shrub | 5.7 % | 23 | 879 m |
| mountain_pine (conifer reforestation) | 2.4 % | 74 | 929 m |
| mediterranean_pine | 0.8 % | 32 | 34 m |
| riparian | 0.7 % | 5 | 296 m |
| macchia | 0.6 % | 5 | 226 m |
| exotic_broadleaf | < 0.1 % | 0 | |

- The comuni with the most beech-dominated woodland cells are Leonessa (108), Filettino,
  Fiamignano, Borgorose, Veroli, Vico nel Lazio and Petrella Salto; with the most chestnut-dominated,
  Pescorocchiano (44), Amatrice, Viterbo, Rocca di Papa, Bracciano, Petrella Salto and Canepina; with
  the most holm-oak-dominated, Carpineto Romano (34), Amaseno, Colle San Magno and Monte San Biagio.
  The comuni with the most woodland cells: Leonessa (136), Rieti, Amatrice, Pescorocchiano,
  Borgorose, Tolfa, Petrella Salto, Filettino.
- **The low beech is in the grid.** The Cimini and Sabatini beech woods that grow far below the
  Apennine beech belt keep their own cells: Monte Venere above Lake Vico (94 % beech at 603 m)
  and Monte Raschio at Oriolo Romano (83 % at 469 m); 12 woodland cells below 700 m are at least
  30 % beech.

Spot checks (the nearest woodland cell to each named place):

| place | cell | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|
| Monte Cimino | `1kmE4502N2147` | 1.00 | chestnut 0.63, beech 0.36, deciduous_oak 0.02 | 930 | 20 | 6.4 | Soriano nel Cimino (VT) | Strada Romana, 2.4 km |
| Monte Venere (Lago di Vico) | `1kmE4500N2140` | 0.61 | beech 0.94, deciduous_oak 0.06 | 603 | 12 | 6.4 | Caprarola (VT) | San Rocco, 4.3 km |
| Monte Raschio (Oriolo Romano) | `1kmE4500N2121` | 0.70 | beech 0.83, deciduous_oak 0.13, chestnut 0.03 | 469 | 10 | 6.7 | Oriolo Romano (VT) | Oriolo Romano, 2.7 km |
| Macchia Grande di Manziana | `1kmE4497N2114` | 0.61 | deciduous_oak 0.80, chestnut 0.17 | 357 | 8 | 6.8 | Manziana (RM) | Scopetoni, 0.8 km |
| Monti della Tolfa | `1kmE4482N2121` | 0.72 | deciduous_oak 0.79, transitional 0.16, macchia 0.03 | 428 | 13 | 6.6 | Tolfa (RM) | Tolfa, 3.2 km |
| Monte Rufeno | `1kmE4477N2188` | 1.00 | deciduous_oak 0.93, mountain_pine 0.07 | 555 | 12 | 6.6 | Acquapendente (VT) | Torre Alfina, 4.6 km |
| Castelli, Maschio delle Faete | `1kmE4548N2075` | 0.90 | chestnut 1.00 | 841 | 18 | 6.4 | Rocca di Papa (RM) | Valle Pantano-Vicinale delle Faete, 0.4 km |
| Terminillo, Vallonina | `1kmE4565N2157` | 0.83 | beech 1.00 | 1319 | 32 | 6.3 | Cantalice (RI) | Pian de' Valli, 2.7 km |
| Monte Livata (Simbruini) | `1kmE4581N2099` | 0.98 | mixed_broadleaf 0.46, mountain_pine 0.32, beech 0.23 | 1305 | 28 | 6.5 | Subiaco (RM) | Livata, 2.4 km |
| Campo Staffi (Simbruini) | `1kmE4598N2090` | 0.93 | beech 0.91, mountain_pine 0.06 | 1445 | 26 | 6.3 | Filettino (FR) | Campocatino, 3.2 km |
| Forca d'Acero (Val di Comino) | `1kmE4640N2077` | 0.70 | beech 0.81, mountain_pine 0.19 | 1383 | 31 | 6.5 | San Donato Val di Comino (FR) | San Donato Val di Comino, 2.6 km |
| Castel Fusano pinewood | `1kmE4514N2072` | 0.99 | mediterranean_pine 0.74, evergreen_oak 0.26 | 15 | 4 | 6.8 | Roma (RM) | Lido di Ostia, 2.1 km |
| Selva del Circeo | `1kmE4576N2034` | 0.75 | deciduous_oak 0.55, mediterranean_pine 0.34, macchia 0.12 | 28 | 3 | 6.8 | Sabaudia (LT) | Sacramento, 3.7 km |
| Ponza (not woodland) | `1kmE4571N1982` | 0.00 | macchia 0.89, transitional 0.11 | 27 | 14 | — | Ponza (LT) | Ponza, 0.5 km |
| Roma, city centre (not woodland) | `1kmE4528N2091` | 0.00 | — | 47 | 7 | — | Roma (RM) | Roma, 1.7 km |

Threshold sensitivity (recomputed from stored fractions, a few cells off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 6,841 | 5,708 | **4,796** | 3,955 | 3,111 |

**DEM tiles over open sea.** Lazio's bbox reaches 40.78° N and 11.44° E to take in the Pontine
islands, so it asks for the 1° tile N40 E011, which lies wholly in the Tyrrhenian: the Copernicus
bucket has no such tile and answers 404. The branch carries Campania's
`fix(grid): skip DEM tiles the bucket lacks over open sea` (the same patch as the Campania,
Calabria and Puglia branches, so the merges agree).

## Weather

- Points: 94 candidates on the 0.2° lattice, **81 on land**; all 4,799 woodland cells weighted,
  none out of reach.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region lazio`,
  250 land nodes at 0.1°, −56 to 1,588 m of model height, three 14-day windows of 2024). Cooling
  per km of height across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference | all, nodes above 300 m (155) |
  |---|---|---|---|---|---|---|---|
  | temperature_2m_max | 5.18 | 6.24 | 4.67 | 5.36 | 4.5 | +0.86 | 5.33 |
  | temperature_2m_mean | 4.41 | 5.10 | 4.23 | 4.52 | 4.5 | +0.02 | 4.64 |
  | temperature_2m_min | 3.83 | 3.33 | 3.19 | 3.37 | 4.2 | −0.83 | 3.51 |
  | soil_temperature_0_to_7cm_mean | 3.66 | 4.16 | 3.31 | 3.70 | 3.7 | 0.00 | 3.82 |

  Every fit is within 1 °C/km of the national rates, so **the national rates are kept**. 86 % of
  the woodland cells lie above 300 m, where the fits are the same. Leave-out RMSE (°C) of the
  skipped nodes, with the national rates, 6.5 °C/km and none:

  | leave-out RMSE | national | 6.5 °C/km | none |
  |---|---|---|---|
  | Tmin, served lattice (0.2°, stride 2) | 0.470 | 0.456 | 0.621 |
  | Tmin, stride 3 (0.3°) | 0.721 | 0.776 | 1.045 |
  | Tmean, stride 2 | 0.279 | 0.280 | 0.477 |
  | soil, stride 2 | 0.461 | 0.468 | 0.573 |

  Daily rain RMSE on the leave-out is 1.08 mm at stride 2 and 1.49 mm at stride 3 whatever the
  rates.
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-17 (81 nodes; the ingest's summary: 53 fetched, 51 from the shared cache;
  46 min on 2026-09-28, with the Sicilia lane queueing on the same
  account), with snowfall from CDS's gridded ERA5-Land, whose national half-year files earlier
  lanes had cached. Open-Meteo's archive and the ECMWF IFS forecast fill
  the days after 2026-09-17 (`api.weather.ingest update --region lazio`: history to 2026-09-22).
- `uv sync --group cds` was run first in this checkout (the memory card on the CDS group).

### Rain scale: the SIARL agrometeo gauges

Lazio publishes two open daily rain series (CC BY 4.0, dati.lazio.it):

- The **Protezione Civile** network ("Serie storica dato pluviometrico", about 220 gauges, monthly
  CSVs from September 2018, many in the mountains): the CSVs give only the station's name, and the
  station list with positions ("Rete di Stazioni di monitoraggio idro-termo-pluviometriche", 2014)
  answers HTTP 500 on the portal. The real-time portal (temporeale.regione.lazio.it, AEGIS) was not
  used. Without positions the gauges cannot be placed on the grid, so this network is not used.
- The **SIARL** agrometeo network (ARSIAL, 95 stations at 1–1,176 m): a station list with
  positions and heights and one CSV of daily values per year since 2004. The 2017, 2019 and 2022
  files answer HTTP 500; 2016, 2018, 2020 and 2021 (to 30 July) and 2023 (to 29 June) download.
  Wired as `GAUGE_NETWORKS["lazio"]` (`api.weather.siarl`, calendar days), run one year at a time
  since the years are not contiguous.

**Woodland gauges.** Five SIARL gauges lie in woodland cells: Canino diga (165 m), Borgovelino
(468 m), Agosta (476 m), Castel di Tora (550 m) and Accumoli (1,176 m). `uv run python -m
api.weather.checks gauges --region lazio --start … --end …` over the five published windows:

| window | pooled raw CDS / gauge | median daily correlation |
|---|---|---|
| 2016 | 0.86 | 0.71 |
| 2018 | 1.04 | 0.66 |
| 2020 | 1.03 | 0.74 |
| 2021, Jan–Jul | 0.93 | 0.70 |
| 2023, Jan–Jun | 1.09 | 0.79 |
| all (1,481 days per gauge) | **0.98** | |

Per gauge over all windows: Canino 1.03, Borgovelino 0.84, Agosta 0.93, Castel di Tora 1.06,
Accumoli 1.12. In the woods the raw reanalysis is about right.

**All gauges, at their own positions.** As for Campania, a one-off read the stored CDS rain
bilinearly at each gauge (sea nodes left out, as the model does) and compared totals over each
gauge's days in the published years (92 gauges with 1,000 or more days):

| band | gauges | raw CDS / gauge rain (pooled) | after the scale |
|---|---|---|---|
| below 200 m | 40 | 1.19 | 1.00 |
| 200–400 m | 37 | 1.17 | 1.03 |
| 400–800 m | 14 | 1.01 | 0.94 |
| 800–1,300 m | 1 | 1.12 | 1.22 |
| all | 92 | 1.15 (median gauge 1.18) | |

The reanalysis rains too often (1 mm or more on a median 37 % of days, the gauges 26 %), the same
drizzle excess Piemonte and Campania found; median daily correlation 0.70, lowest on the coast
(Montalto di Castro, Cerveteri, Maccarese, 0.51–0.61). Four lowland gauges read far less than the
reanalysis (Viterbo 581 mm a year, ratio 1.73; Ronciglione 1.61; Cerveteri 1.59; Soriano Pantane
1.46); leaving out every gauge above 1.45 changes the fit to 0.84 + 0.21 per km, so they stay in.

**`lazio.yaml` sets 0.82 + 0.23 per km** over `era5_land_cds` and `era5_seamless`: the least-squares
fit through the origin of gauge totals on model totals × (a + b × elevation), a = 0.819,
b = 0.229. Over Lazio's woodland cells it averages 0.99, so it mostly takes the lowland excess
out and leaves the woods about where they were (the five woodland gauges: 0.98 raw, 0.94
scaled). Above 800 m, where 43 % of the woodland cells lie, it rests on Accumoli alone and is an
extrapolation; Accumoli itself would read 1.22 scaled.

| fit (CDS rain) | a | b per km | factor at 200 / 500 / 800 / 1,200 m |
|---|---|---|---|
| **Lazio (92 SIARL gauges, 1–1,176 m, used)** | **0.82** | **0.23** | **0.86 / 0.93 / 1.00 / 1.09** |
| Lazio, gauges at 200 m and above (52) | 0.80 | 0.26 | 0.86 / 0.93 / 1.01 / 1.12 |
| Campania (33 agrometeo gauges, 11–769 m) | 0.77 | 0.52 | 0.87 / 1.03 / 1.19 / 1.39 |
| Umbria (8 woodland gauges, 402–1,053 m) | 0.89 | 0.33 | 0.96 / 1.06 / 1.15 / 1.29 |
| national (Tuscan gauges, `era5_seamless`) | 1.28 | 0.29 | 1.34 / 1.43 / 1.51 / 1.63 |

Lazio's factor sits below its neighbours' at every height, so rain steps at the Umbria and
Campania borders (card `fix-rain-calibration-region-borders.md`). The Protezione Civile's mountain
gauges would allow a proper woodland fit once the Region republishes their station list.

## Sightings

`uv run python -m api.sightings.ingest fetch --region lazio` (2026-09-28): **73 GBIF records** for
the three groups over the bbox (queried as *B. edulis* 3, *B. aereus* 9, *B. reticulatus* 7,
*B. pinophilus* 1, *A. caesarea* 22, *Cantharellus* 36) and **none from iNaturalist** in the last
two weeks. The quality filters drop 4 too imprecise, 18 with unknown uncertainty and 8 of an
excluded basis; 61 are kept and **30 land on Lazio's woodland cells** (31 are outside the region
inside the bbox, or on non-woodland cells). All 30 are on woodland, none obscured, all GBIF:

| group | train seasons 2016–2023 | hold-out 2024–2025 | 2026 | where |
|---|---|---|---|---|
| porcini | 2 cell-days | 3 | 1 | Turkey oak at Manziana and Canale Monterano (Sabatini), Farnese; hop-hornbeam at Trevi nel Lazio (Simbruini); beech at Subiaco, 13 July 2026 |
| gallinacci | 5 | 4 | 0 | chestnut at Soriano nel Cimino and Collalto Sabino; beech at Arcinazzo Romano; Turkey oak at Trevignano, Tolfa, Acquapendente, Farnese, Sabaudia (Circeo), Nespolo |
| ovoli | 5 | 6 | 0 | Turkey oak at Trevignano, Bassano Romano, Canale Monterano, Colleferro, Farnese, Sabaudia, Nespolo; holm oak at San Felice Circeo; stone pine at Sabaudia; hop-hornbeam at Supino (Lepini); chestnut at Pescorocchiano |

(cell-days: unique group-cell-day sightings; ovoli's hold-out holds 8 records on 6 cell-days. Train seasons 12 in all, hold-out 13.)

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/lazio.md`; rules in
`api/src/api/config/species/lazio/` (24 new references and 3 copied from the Abruzzo and Campania
branches, all opened; child card `region-lazio-species.md`).

- **All three groups and six keys kept.** The regional law (L.R. 32/1998, as amended to L.R.
  20/2024) regulates the porcini group, the ovolo (banning the closed one) and every *Cantharellus*.
  *B. pinophilus* has no Lazio record or source and stays, as in Umbria and the Marche.
- **The Lazio porcino is the summer and the black one in the low volcanic woods**: *B. aestivalis*
  (= *reticulatus*) under beech and Turkey oak at Monte Venere and in the Mola di Oriolo, *B. aereus*
  under Turkey oak (Monte Rufeno's porcino); *B. edulis* in the Apennine beech and on the Cimini's
  acid soils.
- **Seasons, weather rules, growth clocks and stoppers are Tuscany's**: the Lazio records fit the
  Tuscan windows (September–October for porcini and ovoli, October to January on the coast for
  chanterelles), and the coast's summer drought comes from the weather itself.
- **Altitude bands rise with the Lazio beech** (to 1,800–1,900 m): *B. edulis* and *B. pinophilus*
  full to 1,800 m, *B. reticulatus* to 1,400 m, gallinacci to 1,400 m, the ovolo to 900 m; *B.
  aereus* keeps Tuscany's band. The low volcanic beech (788 ha below 700 m) needed no change.
- **14 affinities move** for what the Carta forestale's classes hold here: hop-hornbeam on
  limestone (`mixed_broadleaf`) down for *B. edulis* and *B. pinophilus*, up for *B. aereus*;
  black-pine reforestation (`mountain_pine`) down for four keys; broom and bramble scrub down for
  five; deciduous oak up for gallinacci; beech from 0 to 0.1 for the ovolo.
- **Press contrasts** (`lazio/sanity.yaml`): 15, written before any Lazio score existed, 13 for
  porcini, 1 for ovoli and 1 for gallinacci, mostly on Funghi Magazine's bulletins with local press
  (Tusciaweb, Viterbonews24, RietiLife, Castelli Notizie, Terzo Binario) and A.M.E.R.'s outing
  reports.

## Validation

Scored 2016-03-18 to 2026-10-05 on 2026-09-28 (rules version `5caa31640299`, rain scale 0.82 + 0.23
per km): 4,799 woodland cells × every day per key, history without factors, the served window
2026-09-22 to 2026-10-05 with them. `onboard` ran the hold-out backtest and the sanity check; the
train-season backtest (`--seasons train --label onboard-train`) and the ovoli and gallinacci sanity
runs (`--group ovoli`, `--group gallinacci`) were run after it. The first train run stopped on a
connection iNaturalist dropped while serving the observer-effort histogram; `JsonClient` now
retries a dropped connection (`fix(sightings): retry a server that hangs up without answering`).

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **12** (porcini 2, gallinacci 5, ovoli 5), against
the 50 the parent plan asks for. Hold-out 2024–2025: **13** (porcini 3, gallinacci 4, ovoli 6).

**Backtest** (model vs the calendar baseline; `auc_local` with its interval / `auc_region` /
`auc_time_effort`):

| seasons | group | n | model | calendar | habitat `auc_local` |
|---|---|---|---|---|---|
| hold-out 2024–2025 | porcini | 3 | 0.65 (0.63–0.67) / 0.95 / 0.62 | 0.55 / 0.81 / 0.51 | 0.50 |
| hold-out 2024–2025 | ovoli | 6 | 0.56 (0.46–0.66) / 0.96 / 0.52 | 0.54 / 0.93 / 0.52 | 0.55 |
| hold-out 2024–2025 | gallinacci | 4 | 0.42 (0.28–0.57) / 0.91 / 0.71 | 0.39 / 0.74 / 0.50 | 0.51 |
| train 2016–2023 | porcini | 2 | 0.84 (0.74–0.95) / 0.87 / 0.75 | 0.59 / 0.81 / 0.66 | 0.50 |
| train 2016–2023 | ovoli | 5 | 0.57 (0.37–0.76) / 0.93 / 0.34 | 0.53 / 0.93 / 0.51 | 0.53 |
| train 2016–2023 | gallinacci | 5 | 0.58 (0.35–0.79) / 0.87 / 0.55 | 0.53 / 0.76 / 0.56 | 0.51 |

The model ranks the sighting cells well against the whole region (`auc_region` 0.87–0.96: they are
Turkey-oak, chestnut and beech cells in season), above the calendar locally in every row, and above
the habitat baseline except for gallinacci in the hold-out (0.42 against 0.51); but 25 sightings over
ten years say little, and the intervals cross 0.5 for every group but porcini. Validating Lazio needs records with locations: the
mycological groups' outing records (A.M.E.R.'s are dated and placed), or the ASL mycological
inspectorates.

**Sanity check** (`lazio/sanity.yaml`), each contrast read against its own group:

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Rieti and Frosinone > Viterbo, Roma, Latina, 10–24 Sep 2023 | porcini | 0.644 | 0.710 | no |
| Simbruini and Ernici > Cimini, Sabatini, Tolfa, 30 Sep–14 Oct 2023 | porcini | 0.000 | 0.000 | no |
| Sabatini and Tolfa 2023: timing | porcini | 0.654 | 0.000 | yes |
| Roma, Latina, Frosinone > Viterbo, 20 Sep–10 Oct 2020 | porcini | 0.517 | 0.761 | no |
| Reatino 2020: timing | porcini | 0.785 | 0.700 | yes |
| Viterbo, Frosinone, Latina: a normal September > 2019 | porcini | 0.424 | 0.417 | yes |
| Basso Lazio 2021: late August > September | porcini | 0.176 | 0.218 | no |
| Castelli Romani 2022: timing | porcini | 0.328 | 0.000 | yes |
| Reatino and Velino 2022 > 2021 | porcini | 0.376 | 0.203 | yes |
| Cimini, September 2022 > 2024 | porcini | 0.746 | 0.759 | no |
| Terminillo and Reatini > Cimini, 12–29 Sep 2024 | porcini | 0.830 | 0.843 | no |
| Lazio, early September 2025 > normal | porcini | 0.657 | 0.440 | yes |
| Viterbo, early October 2016 > 2020 | porcini | 0.798 | 0.935 | no |
| Sabatini and Tolfa ovoli, October 2016 and 2024 > 2023 | ovoli | 0.959 | 0.310 | yes |
| Alta Sabina gallinacci, June 2023 > 2018 | gallinacci | 0.589 | 0.596 | no |

**7 of 15 hold** (porcini 6/13, ovoli 1/1, gallinacci 0/1); the `Data` section's "7/15" is the
default run, which scores all 15 on the porcini group and happens to give the same count. Of the
eight misses:
- three are near ties (Cimini 2022 against 2024, 0.746 against 0.759; Terminillo against the
  Cimini in 2024, 0.830 against 0.843; Alta Sabina, 0.589 against 0.596), and one holds on a near
  tie (September 2019, 0.424 against 0.417);
- two rest on bulletins that say the rain came and the porcini did not: "Il Viterbese … è rimasto a
  secco non in termini di pioggia, quanto di nascite" (2020, both Viterbo contrasts). A
  weather-and-woods score cannot see that, and the model rates the Viterbese high on its rain;
- in early October 2023 both sides score 0 (the dry autumn of 2023: porcini's 30-day rain factor
  is 0 below half the normal), where the bulletin still reports "qualche porcino" in the Simbruini;
- mid-September 2023 by province and the Basso Lazio timing of 2021 are plain misses, both on
  province-wide areas that mix mountain and coast.

With too few presences to tune, the priors stand; the contrasts, most of them from one national
magazine at province level, are recorded as they are and not adjusted to the scores.

**The served window.** On 28 September 2026 porcini score 0.04 on average across Lazio, and 123
cells reach 0.6, all in the province of Rome (Roma's coastal pinewoods and oaks, Bracciano,
Cerveteri, Manziana, Tolfa): the reanalysis puts 32 mm on the nodes in the last 30 days, most of it
on 10 and 18 September, and porcini's 30-day rain factor is 0 below half the normal almost
everywhere else. Ovoli average 0.17 with 573 cells at 0.6 or more (the Turkey oak and chestnut of
the Tolfa, the Sabatini, the Cimini and the Castelli), gallinacci 0.19 with none at 0.6.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-28 (`deploy/rsync-region-data.sh lazio`, 220
files, 373 MB, no redeploy). The server serves a region only when its YAML is in the deployed code
and its stores are on disk, so they stay inert until `main` with `config/regions/lazio.yaml` is
deployed by the rail's "Deploy pulled main" step (with the daily job, which brings the weather and
scores up to that day). Then check:

- [ ] `https://mappafunghi.app/lazio` and `/lazio/porcini`, `/lazio/ovoli`, `/lazio/gallinacci`
  show real scores for today (not fixtures), and a tapped cell's "why this score" names Lazio
  habitats (chestnut on the Cimini, beech on the Terminillo and the Simbruini).
- [ ] `https://api.mappafunghi.app/regions` lists `lazio`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Lazio URLs (built from the registry; the
  local build has them).
- [ ] Lighthouse SEO is 100 on `/lazio` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci nel Lazio", description, canonical, og image `og/lazio.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1282).
- [ ] `/credits` shows "Regione Lazio — Carta forestale su base tipologica".
- [ ] The next morning's daily job has a `region_done` line for `lazio`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Rain scale above 800 m is extrapolated.** Only one SIARL gauge (Accumoli, 1,176 m) lies above
  800 m, where 43 % of the woodland cells are: there the raw reanalysis is 12 % wet, while the fit
  scales it up 9 % (Weather). The Protezione Civile's mountain gauges publish open daily rain but not, for
  now, their positions; once the Region republishes the station list, a woodland fit replaces this
  one. Rain also steps at the Umbria and Campania borders (card
  `fix-rain-calibration-region-borders.md`).
- **SIARL years.** 2017, 2019 and 2022 answer HTTP 500 on dati.lazio.it, and 2021 and 2023 stop in
  mid-year; the check uses the 4.1 years that download.
- **The forest map shows the woods of 2005–2007.** Fires, clearings and regrowth since then are not
  in it. CLC IV is newer (2018) but maps 25 ha units where this map maps 0.5 ha, and has no
  forest types beyond its fourth level; the forest area lands at −5.3 % on INFC 2015.
- **Conifer reforestation is all `mountain_pine`.** The map has one class for pine and other
  montane conifer plantations; 5 % of that area lies below 400 m, where it may not be black pine.
- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point: from
  the hub, a fix in Viterbo or on the Cimini is offered Tuscany, and one in Rieti or on the
  Terminillo Umbria. Inside `/lazio` the current region comes first, so it is right there. Card
  `fix-region-lookup-by-boundary.md` (Lazio's cases added).
- **Validation rests on 25 sightings** and mostly one magazine's province-level bulletins; 7 of 15
  press contrasts hold, three misses being near ties (Validation).

## Data

- cells: 17868
- woodland cells: 4799
- INFC deviation: -5.3% (grid 530,501 ha vs 560,236 ha) — within ±10 %
- weather nodes: 81
- years stored: 2016–2026 (11 years)
- sightings kept: 30
- backtest AUC (auc_local, model, all): gallinacci 0.425, ovoli 0.557, porcini 0.652
- sanity contrasts: 7/15 passed

