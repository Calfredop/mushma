# basilicata

Region #16 of the full-Italy rollout (card `region-basilicata.md`). API id `basilicata`, web slug
`/basilicata`, ISTAT COD_REG 17. Config: `api/src/api/config/regions/basilicata.yaml`. Southern
Apennines between Campania, Puglia and Calabria: the Lucanian side of the Pollino, the Sirino and
the Lagonegrese, the Val d'Agri, the central Apennine round Potenza, the Vulture, and the clay hills,
Murgia and Ionian coast of the Materano.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | ISPRA, **Carta della Natura della Regione Basilicata, carta degli habitat 1:50.000** (Papallo and Bianco 2012, revised 2013) (`ispra_cnat_basilicata`) | CC BY 4.0 | GeoPackage on ISPRA's SDI, no login |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 8763 "Basilicata, IT" | per record | counts per cell only |

**What was checked, and why the Carta della Natura.**

- **Carta Forestale della Basilicata** (the card's candidate): made by INEA for the Region's forestry
  office with the Università della Basilicata and published in 2006 as an atlas (Costantini,
  Bellotti, Mancino, Borghetti, Ferrara, *Carta Forestale della Basilicata. Atlante*, Regione
  Basilicata and INEA, Potenza 2006). A field survey of every forest section, 1 ha minimum unit,
  three levels (a CORINE-like category, a forest type, coppice or high forest and stage), and every
  tree species with its cover (Corona 2006, Forest@ 3: 325–326). It would be the best map for this
  job, but it is not published as data: the RSDI geoportal once showed it as a WMS layer
  (`rsdi:carta_forestale_1` on the old `/geoserver`, now only in Wayback captures of map images),
  no RNDT record or download exists, and the atlas says copies are asked for by letter. The Region
  is redrawing it (contract awarded in September 2025, due in August 2027, to be downloadable from
  the RSDI when done; Regione Basilicata, "In aggiornamento la Carta forestale regionale").
- **Carta dell'Uso del Suolo 2013** (Regione Basilicata, RNDT `r_basili:399969B4-…`): 1:5,000 from the
  2013 orthophotos, IODL 2.0, WFS on the RSDI's `rbgeoserver2016`. Its legend stops at CORINE level
  3 (311 broadleaf, 312 conifer, 313 mixed, 323 sclerophyll, 324 transitional): no forest types,
  so it could only give `forest.groups`, with a second map for the types, Tuscany's pattern. The
  RSDI (`rsdi.regione.basilicata.it`, with the Centro Funzionale and the open-data portal on the same
  hosting) closed every connection on 2026-09-30, from the shell and from a browser, while
  `www.regione.basilicata.it` answered; so the map could not be read, not even as a cross-check.
- **Piano Paesaggistico Regionale, "Foreste e boschi"** (art. 142 c. 1 lett. g, D.Lgs. 42/2004):
  the legal layer of woods and land bound to reforestation, digitised 2019–2023 (762 polygons);
  no broadleaf/conifer split and no types, and on the same unreachable RSDI.
- **Carta Forestale d'Italia CFI2020** (CREA): shapefiles on request only, as for Marche, Umbria,
  Campania and Calabria. Not scriptable.
- **Carta della Natura, Basilicata** (ISPRA with ARPA Basilicata; RNDT `ispra_rm:0003CNATHB_DT`):
  habitat map of the whole region at 1:50,000, created 2012-01-31 and revised 2013-01-31, from
  Landsat IMAGE2000, the IT2000 (1998–99) and AGEA 2008 orthophotos and field checks. 40,411
  polygons in 86 habitats, each with its CORINE Biotopes code (`codice_corine`): 41.18 southern
  beech woods, 41.7511 Turkey oak, 41.732 and 41.737B downy oak, 41.C1 *Alnus cordata*, 45.324
  supramediterranean holm oak, 42.711 *pino loricato*, 83.31 conifer plantations… One layer gives
  both the broad groups and the forest types, read once (Calabria's and Molise's pattern). It is the
  only openly licensed, downloadable map of Basilicata that names the trees. Its scale is coarser
  than the 1:25,000 editions Calabria, Campania and Molise use (ISPRA's page lists no 1:25,000
  edition for Basilicata).

**Licence.** The RNDT record declares "Dato concesso con licenza CC-BY-4.0" (use constraint: the CC
BY 4.0 deed), no access limit, and the credit "ISPRA - Sistema Informativo di Carta della Natura della
Regione Basilicata"; it also asks that reproduction for research, teaching, dissemination, study and
leisure be requested, the clause Campania's and Molise's records carry. The app credits "Carta della
Natura della Regione Basilicata © ISPRA, CC BY 4.0" and links the ISPRA page.

**Download.** `https://sdi.isprambiente.it/download_ogc/cnat/CNAT_Habitat_Baslicata.gpkg` (172 MB,
layer `CNAT_Habitat_Baslicata`, EPSG:25832). The file name misspells the region ("Baslicata"), as the
record's own link does; `CNAT_Habitat_Basilicata.gpkg` answers 404. The same polygons are served by
ISPRA's ArcGIS layer `Natura/Carta_degli_Habitat_scala_1_50_000_e_1_25_000/MapServer/0`
(`regione = 'BAS'`), with the same codes and areas. Every area here is measured from the geometry
(whole map 999,175 ha, against the 999,222 ha of the ISTAT boundary).

Class mapping (`basilicata.yaml`), whole-map areas and median height of the polygons (DEM at each
polygon's representative point, area-weighted):

| CORINE Biotopes | group | habitat | ha | median m |
|---|---|---|---|---|
| 41.7511 Turkey oak; 41.732 downy oak; 41.737B southern Italian white oak; 41.7512 Turkey oak with farnetto; 41.782 *Quercus trojana* (fragno) | broadleaf | deciduous_oak | 113,397; 36,184; 19,129; 16,614; 249 | 913; 673; 568; 847 |
| 41.18 faggete dell'Italia meridionale | broadleaf | beech | 28,494 | 1,259 |
| 45.324 supramediterranean holm oak; 45.31A southern holm oak | broadleaf | evergreen_oak | 11,975; 3,501 | 607; 277 |
| 41.C1 *Alnus cordata*; 41.81 hop-hornbeam; 41.41 ravine woods | broadleaf | mixed_broadleaf | 9,656; 5,413; 171 | 1,028; 805 |
| 44.61 poplar; 44.14, 44.13 willow; 44.513 black alder; 44.63 narrow-leaved ash | broadleaf | riparian | 10,228; 2,327; 701; 165 | 282 |
| 41.9 chestnut woods | broadleaf | chestnut | 4,253 | 867 |
| 83.324 robinia | broadleaf | exotic_broadleaf | 305 | |
| 83.31 conifer plantations | conifer | other_conifer | 18,676 | 474 |
| 42.84 Aleppo pine; 16.29 wooded dunes | conifer | mediterranean_pine | 1,407; 1,148 | 196; 7 |
| 42.711 *pino loricato* | conifer | mountain_pine | 320 | 1,211 |
| 42.15 southern Apennine silver fir | conifer | fir_spruce | 177 | 1,129 |
| 32.211 low macchia of wild olive and lentisk; 32.4, 32.3 garighe and macchia; 32.215 *Cytisus*; 32.11, 32.13 matorral; 16.27, 16.28 dune macchia; 45.1 olive and carob woods | macchia | macchia | 29,316; 3,509; 1,773; 123; 67; 146 | 269 |
| 31.8A bramble; 31.81 deciduous thickets; 44.81 tamarisk and oleander; 44.12 shrub willows; 31.844 broom; 31.88 juniper | transitional | transitional_woodland_shrub | 26,540; 24,592; 1,739; 1,186; 479; 339 | 694; 966 |

Forest (broadleaf + conifer) 284,491 ha on the whole map (broadleaf 262,763, conifer 21,728; macchia 34,934 and transitional 54,875 more). **The conifer plantations are two things
under one code**: Aleppo pine on the clay hills and the Ionian side and black pine in the mountains.
Their polygons lie at a median 474 m, but 56 % of their area is below 600 m (10th percentile 141 m)
and the 90th percentile is 1,225 m. The grid gives a code one habitat, so they go to
`other_conifer`, as Emilia-Romagna files its "piantagioni di conifere indigene" and Liguria its
"rimboschimenti", and the species rules treat `other_conifer` in Basilicata as "conifer
plantations, Aleppo pine low and black pine high", with the altitude bands separating the two.
The plantations dominate 84 woodland cells, at a median 742 m: Marsico Nuovo and Viggiano (the Val
d'Agri, black pine) and Matera, Irsina, Pomarico and Montalbano Jonico (the Materano, Aleppo pine).
**The olive and carob woods** (45.1, 146 ha) go to macchia, as Puglia files its wild-olive woods.
Left out: broadleaf plantations (83.325, 1,604 ha) and eucalyptus (83.322, 488 ha), *Ampelodesmos*
steppe (32.23), bracken (31.863), the garighe (32.217, 32.65, 33.36), the prostrate-juniper and
thorny-cushion heaths of the high Pollino (31.43, 31.77), grassland, rock and wetlands.

**Forest area and INFC.** The grid holds **284,433 ha of forest against INFC 2015's "bosco" of 288,020
ha: −1.2 %**, well inside the ±10 % line. At 1:50,000 the map's woods take in some clearings and lose
some small woods, but on the whole it matches the inventory, unlike Puglia's 1:50,000 edition (+13.9
% on INFC) and Calabria's 1:25,000 one (+18.5 %).

## Woodland grid

Built 2026-09-30 (`uv run python -m api.grid.build --region basilicata`, 18 s: the DEM tiles were
cached from the neighbours' builds and SoilGrids answered at once).

- Cells 10,359; inside area 9,992 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 2,545** (25 % of the cells), in 125 of the 131 comuni. By province: Potenza 2,230,
  Matera 315. Basilicata's woods are many and small, mostly on the Potentino's hills: forest covers
  28 % of the region but only a quarter of the cells reach the 50 % mask.
- **Forest area 284,433 ha vs INFC 2015 bosco 288,020 ha: −1.2 %**. The 20 m rasterization
  reproduces the map's 284,491 ha within 0.02 %.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 87 % of a cell's wooded area.
- Terrain: woodland elevation median 816 m (5th–95th percentile 400–1,396 m), highest cell mean 1,926
  m (Chiaromonte, the Pollino's beech), highest point in a woodland cell 2,227 m; slope median 16.3°,
  6 % of woodland cells above 25°; 64 cells have no aspect. 8 slivers (no woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.57 (6.15–7.14, 5th–95th percentile), between
  Calabria's acid granite (6.30) and Puglia's limestone.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (Turkey, downy and white oak, farnetto, fragno) | 63.4 % | 1,838 | 785 m |
| beech | 12.7 % | 308 | 1,334 m |
| transitional_woodland_shrub | 5.6 % | 11 | |
| mixed_broadleaf (*Alnus cordata*, hop-hornbeam) | 5.5 % | 116 | 973 m |
| evergreen_oak (holm oak) | 4.7 % | 128 | 550 m |
| other_conifer (conifer plantations) | 3.9 % | 84 | 742 m |
| chestnut | 1.6 % | 33 | 880 m |
| riparian | 0.9 % | 5 | |
| macchia | 0.9 % | 1 | |
| mediterranean_pine (Aleppo pine, Ionian dune pine woods) | 0.5 % | 20 | 6 m |
| mountain_pine (*pino loricato*) | 0.1 % | 1 | |
| fir_spruce (silver fir) | 0.1 % | 0 | |
| exotic_broadleaf | < 0.1 % | 0 | |

- Basilicata is **Turkey-oak country**: nearly two thirds of the wooded area is deciduous oak, the
  highest share of any region so far. The comuni with the most oak-dominated cells are Accettura (69,
  the Gallipoli Cognato forest), Lauria (62), Abriola (56), Terranova di Pollino, Bella, San
  Chirico Raparo, Forenza and Tricarico.
- Beech dominates the Pollino (Viggianello 29 cells, Terranova di Pollino 26, San Severino Lucano 18),
  the Sellata and Arioso (Abriola 19, Calvello 19), the Sirino and Lagonegrese (Lauria 18, Rivello 13)
  and the Maddalena (Marsico Nuovo 17). *Alnus cordata* and hop-hornbeam dominate the Lagonegrese and
  the Raparo (Moliterno 21, Lagonegro 19, Lauria, Castelsaraceno, Rivello). Chestnut is small and
  volcanic: the Vulture (Atella 7, Rionero in Vulture, Melfi) and Trecchina. Holm oak dominates Maratea,
  Lagonegro and the Agri and Sauro hills (Roccanova, Gallicchio, Armento). The Ionian dune pine woods
  are Policoro, Scanzano Jonico, Pisticci and Bernalda.
- Silver fir dominates no cell: its largest share is 0.42 in the Abetina di Laurenzana. *Pino
  loricato* dominates one cell, Monte La Spina above Lauria (0.71); on the Pollino's summits it shares
  cells with beech.
- The comuni with the most woodland cells: Lauria (96), Abriola and Lagonegro (76 each), Terranova di
  Pollino (74), Viggianello (71), Accettura (70), Calvello, Moliterno, Marsico Nuovo, San Chirico
  Raparo.

Spot checks (places geocoded with Photon):

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Serra del Prete, Pollino | `1kmE4849N1891` | yes | 0.84 | beech 1.00 | 1906 | 29 | 6.2 | Viggianello (PZ) | Prastio, 4.9 km |
| Piano Ruggio, Pollino | `1kmE4847N1890` | yes | 0.58 | beech 0.86, other_conifer 0.14 | 1585 | 18 | 6.5 | Viggianello (PZ) | Prastio, 4.6 km |
| Bosco Magnano, Pollino | `1kmE4846N1905` | yes | 0.77 | deciduous_oak 0.51, evergreen_oak 0.33, transitional 0.07, riparian 0.06 | 647 | 17 | 6.4 | San Severino Lucano (PZ) | Taverna Magnano, 0.3 km |
| Monte La Spina, Lauria (*pino loricato*) | `1kmE4828N1902` | yes | 0.95 | mountain_pine 0.71, beech 0.29 | 1271 | 30 | 6.1 | Lauria (PZ) | Case Corunzo, 2.4 km |
| Lago Laudemio, Monte Sirino | `1kmE4820N1913` | yes | 0.85 | beech 0.57, mixed_broadleaf 0.43 | 1594 | 19 | 6.2 | Lagonegro (PZ) | Casale Serino, 2.3 km |
| Abetina di Laurenzana | `1kmE4828N1943` | yes | 1.00 | deciduous_oak 0.49, fir_spruce 0.42, other_conifer 0.09 | 1166 | 12 | 6.3 | Laurenzana (PZ) | Laurenzana, 5.8 km |
| Bosco di Rifreddo, Pignola | `1kmE4817N1959` | yes | 0.98 | deciduous_oak 0.89, beech 0.06 | 1049 | 12 | 6.5 | Pignola (PZ) | Rifreddo, 2.2 km |
| Valico della Sellata | `1kmE4813N1955` | yes | 0.79 | deciduous_oak 0.79, transitional 0.17 | 1253 | 19 | 6.5 | Abriola (PZ) | Il Palazzo, 2.1 km |
| Foresta di Gallipoli Cognato | `1kmE4848N1948` | yes | 0.92 | deciduous_oak 1.00 | 976 | 17 | 6.5 | Accettura (MT) | Serra Verde, 4.3 km |
| Monte Vulture | `1kmE4797N2001` | yes | 1.00 | chestnut 0.65, deciduous_oak 0.24, other_conifer 0.10 | 1096 | 26 | 6.3 | Rionero in Vulture (PZ) | Barile, 3.1 km |
| Laghi di Monticchio, Vulture | `1kmE4795N1999` | yes | 0.78 | evergreen_oak 0.32, chestnut 0.31, beech 0.19, deciduous_oak 0.09 | 779 | 21 | 6.5 | Atella (PZ) | Foggianello, 3.4 km |
| Bosco Pantano, Policoro | `1kmE4892N1921` | no | 0.48 | riparian 0.59, transitional 0.41 | 5 | 2 | 6.7 | Policoro (MT) | Concio, 2.7 km |
| Murgia materana | `1kmE4883N1974` | no | 0.01 | macchia 0.86, evergreen_oak 0.14 | 356 | 8 | 7.5 | Matera (MT) | Matera, 3.4 km |
| Potenza (city) | `1kmE4813N1968` | no | 0.00 | transitional 1.00 | 747 | 10 | 7.5 | Potenza (PZ) | Potenza, 0.6 km |

The Carta della Natura's 1:50,000 shows at Piano Ruggio (a beech wood with the Pollino's pine and
fir planting) and the Rifreddo (a silver fir and beech wood inside a Turkey-oak forest, mapped as
oak): small stands of fir and pine inside larger woods are lumped with their surroundings. The Bosco
Pantano, the Ionian coast's last floodplain forest, falls just short of the mask (0.48).

Threshold sensitivity (recomputed from stored fractions):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 3,797 | 3,129 | **2,544** | 1,957 | 1,444 |

## Weather

- Points: 58 candidates on the 0.2° lattice, **51 on land**; all 2,545 woodland cells weighted,
  none out of reach.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region basilicata`,
  2026-09-30, 140 land nodes at 0.1° of 152, three 14-day windows of 2024). Cooling per km of height
  across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.36 | 4.69 | 3.86 | 4.69 | 4.5 | +0.19 |
  | temperature_2m_mean | 4.85 | 5.11 | 4.39 | 4.88 | 4.5 | +0.38 |
  | temperature_2m_min | 4.75 | 5.69 | 4.40 | 4.79 | 4.2 | +0.59 |
  | soil_temperature_0_to_7cm_mean | 3.95 | 3.99 | 3.63 | 3.84 | 3.7 | +0.14 |

  Every rate is within 1 °C/km of the national config, so **the national rates are kept**. They
  also downscale best. Leave-out RMSE against the full 0.1° field:

  | leave-out RMSE | none | 6.5 °C/km | national config |
  |---|---|---|---|
  | Tmin, served lattice (0.2°, stride 2) | 0.639 | 0.497 | **0.455** |
  | Tmin, stride 3 (0.3°) | 0.744 | 0.678 | **0.590** |
  | Tmax, stride 2 | 0.579 | 0.445 | **0.387** |
  | Tmean, stride 2 | 0.535 | 0.350 | **0.287** |
  | soil, stride 2 | 0.495 | 0.503 | **0.381** |
  | soil, stride 3 | 0.578 | 0.679 | **0.502** |

  Daily rain RMSE on the leave-out is 1.59 mm at stride 2 and 1.88 mm at stride 3 whatever the
  rates: between Campania's (1.23 and 1.44) and Calabria's (1.80 and 2.53).
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-19 (51 land nodes, about 45 min on 2026-09-30), with snowfall from CDS's
  gridded ERA5-Land, whose national half-year files earlier lanes had cached. Open-Meteo's archive
  and the ECMWF IFS forecast fill the days after 2026-09-19 (`ingest update`, history complete to
  2026-09-24; 788 Open-Meteo calls counted that day across the lanes by then).

### Rain scale: ALSIA's agrometeo station totals

Basilicata publishes no open daily rain a script could read today:

- The **Centro Funzionale Decentrato** (Protezione Civile, `centrofunzionale.regione.basilicata.it`)
  offers "dati storici" for download, free for non-commercial use with the source cited, and its
  Annali idrologici 2003–2025; its server refused every connection on 2026-09-30, like the RSDI.
- **ALSIA's Servizio Agrometeorologico Lucano** (46 farm stations, daily data since 2000) gives its
  data after registration.
- ALSIA's report *Caratterizzazione agroclimatologica della Basilicata (2000–2023)* (Scalcione,
  Dichio, Lanfredi, Coluzzi, Imbrenda, December 2024) publishes, for the 27 stations with the fewest
  gaps, each station's position and height (Table 1) and its **total rain for every year 2000–2023**
  (Table 14).

So the check compares annual totals, not days, as Puglia's did with monthly ones: raw CDS rain of
2016–2023 summed per year, read bilinearly from the land nodes at each station (weights
renormalised), against the station's year, heights from the DEM at each station. The report's
Table 1 swaps its latitude and longitude headings and gives Nova Siri Nemoli's coordinates (Table 2
has Nova Siri's, and shifts Senise, Stigliano and San Giorgio Lucano by a row); Table 14 is by name.
20 of the 27 stations lie within 5 km of a woodland cell (160 station-years, 11–919 m).

| stations | band | stations | station mm/yr (median) | raw CDS / station (pooled) | scaled |
|---|---|---|---|---|---|
| 20 near woodland | below 200 m | 8 | 605 | 0.97 | 1.01 |
| | 200–400 m | 3 | 624 | 0.98 | 1.06 |
| | 400–600 m | 6 | 871 | 0.86 | 0.96 |
| | 600–920 m | 3 | 748 | 0.94 | 1.08 |
| | pooled | | | 0.92 | 1.00 |
| all 27 | pooled | | | 0.94 | |

The reanalysis is close to the stations, as in Puglia: a little dry in the hills and mountains
(0.86–0.94 above 400 m), right on the Ionian plain. **`basilicata.yaml` sets 1.04 + 0.14 per km,
clamped at 920 m**, over `era5_land_cds` and `era5_seamless`: the least-squares fit through the
origin of station totals on model totals × (a + b × elevation) over the 20 near-woodland stations
(a = 1.038, b = 0.136; leave-one-out 1.02–1.06 and 0.06–0.18). All 27 give 1.01 + 0.17. The clamp
stops it at the highest station (Laurenzana, the Abetina, 919 m); 36 % of the woodland cells lie
above it.

| scale | factor at 200 / 500 / 800 m and above 920 m | mean over the woodland cells |
|---|---|---|
| **Basilicata (20 ALSIA stations, used)** | **1.07 / 1.11 / 1.15 / 1.16** | **1.14** |
| Puglia (42 gauges) 0.93 + 0.34 to 900 m | 1.00 / 1.10 / 1.20 / 1.24 | 1.18 |
| Campania (agrometeo) 0.77 + 0.52 | 0.87 / 1.03 / 1.19 / 1.25 at 920 m | 1.21 |
| Calabria (station normals) 0.85 + 0.82 to 1,300 m | 1.01 / 1.26 / 1.50 / 1.60 at 920 m | 1.53 |
| national (Tuscan gauges) 1.28 + 0.29 | 1.34 / 1.43 / 1.51 / 1.55 at 920 m | 1.52 |

**Its weakness is the wet south-west.** ALSIA's stations are farm stations, most of them in the dry
Materano and on the Ionian side; only three stand above 600 m, and the woods of the Sirino, the
Lagonegrese and the Pollino are the wettest part of the region. Nemoli (530 m, below the Sirino)
catches 1,657 mm a year against 1,070 raw and about 1,190 scaled (0.72); Rotonda (549 m, the
Pollino) 1,180 against 1,032 raw and 1,148 scaled. Genzano di Lucania, on the dry Bradano side, goes
the other way (raw 1.27). The same pattern as Calabria's Serre and Puglia's Gargano: the 0.2°
lattice cannot hold the Tyrrhenian orographic rain. The years are 2016–2023, the overlap between the
report and the CDS history. The report reserves no rights and ALSIA publishes it for download; its
figures are used for this check only.

## Sightings

`uv run python -m api.sightings.ingest fetch --region basilicata` (2026-09-30): **2 GBIF records** for
the three groups over the bbox, both iNaturalist research-grade observations (a *B. edulis* of 5
December 2023 near Pietrapertosa and a *B. aereus* of 18 May 2024 at Fardella), and **none from
iNaturalist** in the last two weeks. Both pass the quality filters and **neither lands on a woodland
cell**: the Pietrapertosa record's cell is 33 % forest (conifer plantation and scrub), 0.5 km from the
nearest woodland cell; Fardella's is 10 % forest, on the edge of one. So **no Basilicata sighting is
stored**, the fewest of any region so far (Molise kept 1 train presence, Calabria 16 records).

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/basilicata.md`; rules in
`api/src/api/config/species/basilicata/` (19 new references, one `bas_` block at the end of the
bibliography; child card `region-basilicata-species.md`).

- **All three groups and six keys kept.** The regional law (L.R. 48/1998, amended by L.R. 43/2001)
  names the porcini, the ovolo and the chanterelle; the Pollino's forager mycologist lists all four
  porcini; Funghi Magazine's bulletins (86 with a Basilicata line, 2018–2025) report black and summer
  porcini, *B. edulis* and chanterelles. *B. pinophilus* rests on the Pollino evidence alone (the
  Calabrian side's beech records) and the ovolo on the law and one iNaturalist record.
- **Turkey-oak country, and its Turkey oak is high** (median 913 m on the map): the black porcino's
  and the ovolo's bands climb to Calabria's (full to 1,000 m, 0 at 1,350 m); *B. edulis* and *B.
  pinophilus* go full to 1,800 m, *B. reticulatus* to 1,600 m and the chanterelles to 1,400 m, as in
  Campania and Calabria.
- **Seasons:** *B. aereus* opens on 1 May, a fortnight before Calabria ("Nascite abbondanti di
  Porcini Neri" by 16 May 2025), full from 1 June, and runs to 30 November above 800 m and 10 January
  below 600 m; the chanterelles' mountain window opens on 15 May. The other windows are Tuscany's. The
  summer gap is left to the rain, heat and drying rules, as in every region.
- **`other_conifer` is the conifer plantations** (Aleppo pine low, black pine high, Woodland grid):
  the porcini keep Tuscany's values and the altitude bands separate the two woods (*B. edulis* and
  *B. pinophilus* 0.3, *B. aereus* and the ovolo 0); the chanterelles drop to 0.1 (no chanterelle
  among 842 Calabrian plantation records). *Pino loricato* (`mountain_pine`) drops to 0.3 for *B.
  edulis* and *B. reticulatus*. Beech becomes a full host for *B. reticulatus* and the chanterelles,
  deciduous oak 0.6 for the chanterelles; *Alnus cordata* and hop-hornbeam, scrub, macchia and the
  dune pines move down.
- **Weather rules, stoppers and growth clocks unchanged**: no Lucanian study gives numbers. One known
  gap is added to *B. edulis* (fog on the holly beech, which reanalysis rain does not see).
- **Press contrasts** (`basilicata/sanity.yaml`): 14, written before any Basilicata score existed, 13
  for porcini and 1 for gallinacci, none for ovoli (no source gives a Basilicata ovolo year). 12 rest
  on Funghi Magazine's national bulletins alone; five pit the wet west against the dry east. No
  source covers 2016.

## Validation

Scored 2016 to 2026-10-07 on 2026-09-30 (rules version `072f1382926f`, rain scale 1.04 + 0.14 per km
to 920 m): 2,545 woodland cells × every day per key, history without factors, the served window
2026-09-24 to 2026-10-07 with them (`onboard --from score`, 3 min 43 s in all). `onboard` ran the
hold-out backtest and the sanity check; the gallinacci contrast was then read against its own group
(`--group gallinacci --label onboard-gallinacci`).

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **0**, against the 50 the parent plan asks for.
Hold-out 2024–2025: **0**. The backtest skips every season ("no sightings"), so there are no AUCs:
Basilicata has the fewest located records of any region so far (Sightings).

**Sanity check** (`basilicata/sanity.yaml`), each contrast read against its own group:

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| west and south 2022 > 2024, 15 Aug–10 Sep | porcini | 0.712 | 0.227 | yes |
| Potenza province > Materano, 20 Aug–8 Sep 2022 | porcini | 0.776 | 0.422 | yes |
| Tyrrhenian Lucania > the rest, 18 Aug–10 Sep 2023 | porcini | 0.506 | 0.153 | yes |
| bassa Basentana 2021 > 2022 and 2023, 30 Aug–15 Sep | porcini | 0.171 | 0.153 | yes (by a hair) |
| west and south 2020 and 2022 > 2023, 5–31 Oct | porcini | 0.819 | 0.555 | yes |
| west and south > Materano, 10 Oct–5 Nov 2022 | porcini | 0.831 | 0.628 | yes |
| whole region 2018 > 2023, 12–31 Oct | porcini | 0.874 | 0.612 | yes |
| whole region 2018 > 2017, 12–31 Oct | porcini | 0.874 | 0.130 | yes |
| whole region 2024 and 2025 > 2023, 12 May–2 Jun | porcini | 0.410 | 0.759 | no |
| 2024: 20 May–2 Jun > 8–30 Jun | porcini | 0.490 | 0.078 | yes |
| whole region 2022 > 2018 and 2024, 14–30 Jun | porcini | 0.172 | 0.319 | no |
| west and south 2021 > 2019 and 2020, 4–20 Sep | porcini | 0.462 | 0.355 | yes |
| whole region 2025 > 2024, 18 Aug–5 Sep | porcini | 0.286 | 0.170 | yes |
| whole region 2023 spring > normal, 28 May–20 Jun | gallinacci | 0.776 | 0.401 | yes |

**12 of 14 hold** (porcini 11/13, gallinacci 1/1); the `Data` section's "12/14" is the default run,
which scores all 14 on the porcini group (the gallinacci contrast holds there too, 0.897 against
0.402). Every west-against-east contrast holds, and so do the autumn ones, by wide margins. The two
misses are both early-season porcini:

- **Spring 2023.** The model puts 12 May–2 June 2023 far above 2024 and 2025 (0.759 against 0.410);
  the bulletins say the porcini were "fermi al palo" in May 2023 and came only in mid-June, while
  2024 was "una piccola apoteosi porcina" and 2025 "Nascite abbondanti di Porcini Neri". May 2023 was
  very wet in the south, and the model credits it on *B. reticulatus* and *B. pinophilus* in the
  beech; the black porcino, the one the bulletins name, wins almost no spring cell-day (a few hundred
  of some 30,000 above 0.3 in each year). The spring flush in the oak is the model's weak point here.
- **Late June 2022 against 2018 and 2024.** 2018 scores 0.585 in 14–30 June, where the bulletins
  have it "ferma al palo"; 2022 (0.172) was a "piccolo exploit". The windows are short and the
  2022 verdict is modest.

**The served window.** On 30 September 2026 porcini average 0.22 across Basilicata's woodland cells,
with 45 cells at 0.6 or more, all on the Lucanian Pollino and the upper Sinni (San Severino Lucano 18,
Viggianello 14, Chiaromonte 7, Francavilla in Sinni, San Costantino Albanese, Terranova di Pollino),
mostly Turkey oak, at a median 782 m. Ovoli average 0.22 (92 cells at 0.6 or more) and gallinacci 0.25.
The nodes had about 28 mm of rain over 31 August–29 September (raw, forecast days included), against
19–138 mm in the same window of past years (median 55): a dry September, so low scores are what the
rules should give.

## After the deploy: what to verify

The server serves a region only when its YAML is in the deployed code and its stores are on disk, so
the stores stay inert until `main` with `config/regions/basilicata.yaml` is deployed by the rail's
"Deploy pulled main" step (with the daily job, which brings the weather and scores up to that day).
Then check:

- [ ] `https://mappafunghi.app/basilicata` and `/basilicata/porcini`, `/basilicata/ovoli`,
  `/basilicata/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Lucanian habitats (Turkey oak at Gallipoli Cognato as deciduous oak, beech on the
  Pollino and the Sirino, the Val d'Agri's conifer plantations as other conifers).
- [ ] `https://api.mappafunghi.app/regions` lists `basilicata`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Basilicata URLs (built from the registry; the
  local build has them).
- [ ] Lighthouse SEO is 100 on `/basilicata` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Basilicata", description, canonical, og image `og/basilicata.png`, JSON-LD Dataset
  with `sameAs` Wikidata Q1452).
- [ ] `/credits` shows "ISPRA — Carta della Natura della Regione Basilicata 1:50.000", CC BY 4.0.
- [ ] From the hub, a GPS fix or a search in Matera or Viggiano offers Basilicata (registry order,
  Known limitations).
- [ ] The next morning's daily job has a `region_done` line for `basilicata`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **A coarse, older forest map.** The Carta della Natura is 1:50,000 on 1998–2008 imagery: small
  stands are lumped with their surroundings (the Rifreddo's silver fir as Turkey oak, Piano Ruggio's
  pine as beech), and the Bosco Pantano falls just short of the woodland mask. The Region's new Carta
  forestale (due August 2027, downloadable from the RSDI) should replace it; it may also split the
  conifer plantations into Aleppo pine (`mediterranean_pine`) and black pine (`mountain_pine`).
- **Conifer plantations share one habitat.** 83.31 is Aleppo pine low and black pine high, filed as
  `other_conifer`; the altitude bands do the separating (Species rules).
- **No located sightings.** Nothing to backtest; validation rests on 14 press contrasts, 12 of them on
  one magazine's bulletins, and the spring flush in the oak (the black porcino) is where they and the
  model disagree (Validation).
- **Rain scale from annual station totals** of mostly farm stations in the dry east: the wet
  south-west (Sirino, Lagonegrese, Pollino) stays short after scaling (Nemoli 0.72). The Centro
  Funzionale's daily historical data (free for non-commercial use, not reachable on 2026-09-30) or
  ALSIA's daily data (after registration) would allow a daily woodland gauge check.
- **The Region's servers did not answer** on 2026-09-30 (RSDI, Centro Funzionale, the open-data portal,
  the Regional Council): the Uso del suolo 2013 cross-check and the gauge check wait on them.
- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point, and
  Puglia's holds all of Basilicata. Registered after Calabria and before Puglia, the hub finds
  Basilicata for 1,134 of its 2,545 woodland cells (Matera, the Val d'Agri, Gallipoli Cognato, the
  Ionian coast); a fix in Potenza, the Vulture or the Sellata is offered Campania, one on the Lucanian
  Pollino or the Sirino Calabria, and Puglia's Altamura and Gravina go to Basilicata. Inside
  `/basilicata` the current-region-first rule serves all of it. Card
  `fix-region-lookup-by-boundary.md`.

## Data

- cells: 10359
- woodland cells: 2545
- INFC deviation: -1.2% (grid 284,433 ha vs 288,020 ha) — within ±10 %
- weather nodes: 51
- years stored: 2016–2026 (11 years)
- sightings kept: None
- sanity contrasts: 12/14 passed

