# calabria

Region #17 of the full-Italy rollout (card `region-calabria.md`). API id `calabria`, web slug
`/calabria`, ISTAT COD_REG 18, Wikidata Q1458. Config: `api/src/api/config/regions/calabria.yaml`.
The second southern region, after Campania.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | ISPRA and Regione Calabria, **Carta della Natura della Regione Calabria, carta degli habitat 1:25.000** (Paone, Caridi, Caruso et al. 2023, published November 2024) (`ispra_cnat_calabria`) | CC BY 4.0 | GeoPackage on ISPRA's SDI (`sdi.isprambiente.it/download_ogc/cnat/`), no login |
| forest-area cross-check | Regione Calabria, Carta dell'Uso del Territorio (CUT), 1:5,000 | no licence stated (open by default) | ArcGIS REST on the Region's cartographic server; not used by the build |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | open-sea DEM tiles skipped (Woodland grid) |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 9323 "Calabria, IT" | per record | counts per cell only |

**What was checked, and why the Carta della Natura.**

- **Geoportale della Regione Calabria** (`geoportale.regione.calabria.it`, catalogue at
  `cartografico.regione.calabria.it/geoportal`): no forest-type map. Its only forest dataset,
  "Paesaggio forestale", is a landscape unit of the regional landscape plan (QTRP), not a
  vegetation map. The Region's land-use map, the **Carta dell'Uso del Territorio (CUT)**, is
  published one class per layer (`GeoHub/boschi_di_latifoglie`, `boschi_di_conifere`,
  `boschi_misti_di_conifere_e_latifoglie`, … on the ArcGIS server, 1:5,000, CORINE structure with
  a IV-level code, metadata created 2020). Its forest layers hold 311 broadleaf 378,016 ha (3111
  87,098; 3112 216,289; 3115 72,251; 3116 8,027; 3113 1,932; 3114 chestnut only 100 ha), 312 conifer
  107,836 ha (3122 90,759; 3121 15,032) and 313 mixed 27,257 ha: **513,109 ha**. Its IV level
  does not separate chestnut from the oaks, and its metadata states no licence ("non identificati
  (cfr. art. 1 Codice Amministrazione Digitale)"; under CAD art. 52 that makes it open by default,
  with no named licence). So it serves as the cross-check below.
- **Carta Forestale d'Italia CFI2020** (CREA): shapefiles on request only, as for Marche, Umbria and
  Campania. Not scriptable.
- **Carta della Natura, Calabria** (ISPRA with the Region, which ran it with the Università
  Mediterranea di Reggio Calabria and the Università della Calabria under a 2020 agreement):
  habitat map of the whole region at 1:25,000, completed 2023 and published in November 2024,
  85,365 polygons in 123 habitats, each with its CORINE Biotopes code (`codice`): 41.18 southern
  beech woods, 42.65 laricio pine, 42.G_n conifers outside their range, 41.9 chestnut woods, 41.C1
  *Alnus cordata*, 41.7511/41.7512 Turkey oak, 41.732 downy oak, 45.31/45.32 holm oak, 45.21 cork
  oak, 42.15 southern Apennine silver fir, 42.711 *pino loricato*… One layer gives both the broad
  groups and the forest types, read once (Campania's pattern), with the tree species the
  regional CUT and CLC IV (1:100,000, 2018) lack or lump.

**Licence.** Calabria's dataset has no record in the RNDT yet (the other regions' Carta della Natura
datasets do, each declaring CC BY 4.0). The series it belongs to, "Carta della Natura Carta degli
Habitat d'Italia – Serie" (`ispra_rm:CNAT01_SDT`), declares "Open Data" and the CC BY 4.0 deed, and
ISPRA's legal notes release "i dati pubblicati sul presente sito … con licenza CC-BY 4.0", asking
that the source be cited with a link. The ISPRA page for Calabria offers the map as a free
shapefile on request; the GeoPackage is on the same public download path as every other region's.
The app credits "Carta della Natura della Regione Calabria © ISPRA, Regione Calabria, CC BY 4.0"
and links the ISPRA page. The Campania record's extra "previa richiesta" clause is not in
anything published for Calabria.

**Download.** `https://sdi.isprambiente.it/download_ogc/cnat/CNAT_Habitat_Calabria.gpkg` (720 MB,
layer `cartadeglihabi_calabria`, EPSG:25832). Its `Shape_Area` column is in Web Mercator units,
about 1.66 times the true area at Calabria's latitude: every area here is measured from the
geometry (whole map 1,507,903 ha, against the 1,522,000 ha of the region).

Class mapping (`calabria.yaml`), whole-map areas:

| CORINE Biotopes | group | habitat | ha |
|---|---|---|---|
| 41.732 downy oak; 41.7512 Turkey oak with Hungarian oak (farnetto); 41.7511 Turkey oak; 41.7513 sessile oak; 44.4 floodplain pedunculate oak | broadleaf | deciduous_oak | 72,496; 45,324; 29,010; 103 |
| 45.31, 45.32 holm oak; 45.21 cork oak; 45.8 holly | broadleaf | evergreen_oak | 95,500; 10,787 |
| 41.18 faggete dell'Italia meridionale | broadleaf | beech | 100,254 |
| 42.G_n conifers planted outside their range; 83.31 conifer plantations; 42.65 laricio pine; 42.612 Apennine black pine; 42.711 *pino loricato* | conifer | mountain_pine | 70,157; 19,401; 8,439; 540; 387 |
| 41.9 chestnut woods; 83.12 chestnut orchards | broadleaf | chestnut | 83,645; 1,683 |
| 41.C1 *Alnus cordata*; 41.81 hop-hornbeam; 41.4 ravine woods; 41.D aspen | broadleaf | mixed_broadleaf | 13,923; 1,421; 780 |
| 42.84 Aleppo pine, 42.83 stone pine, 16.29 wooded dunes | conifer | mediterranean_pine | 14,579 |
| 44.61 poplar, 44.513 black alder, 44.14 willow, 44.71 plane | broadleaf | riparian | 10,504 |
| 41.L_n exotic broadleaf (robinia, ailanthus); 44.D2_n allochthonous riparian woods | broadleaf | exotic_broadleaf | 4,232 |
| 42.15 southern Apennine silver fir | conifer | fir_spruce | 3,423 |
| 32.214 lentisk, 32.215 *Cytisus*, 32.11 evergreen-oak matorral, 32.3 macchia, 32.22 *Euphorbia dendroides*, 32.12, 32.13, 32.212, 32.24, 32.4; 16.27, 16.28 dune macchia | macchia | macchia | 70,244 |
| 32.A *Spartium*, 31.844 broom, 31.81 deciduous scrub, 31.8A bramble, 31.87 recently burnt or felled woods, 44.81 tamarisk and oleander, 44.12 shrub willows, 31.88 juniper, 31.A_n, 32.26 | transitional | transitional_woodland_shrub | 57,954 |

Forest (broadleaf + conifer) 586,590 ha on the whole map. **The out-of-range conifers are laricio
pine**: 42.G_n covers 70,157 ha at a median 1,279 m (10th–90th percentile of polygon area 932–1,426
m, none below 400 m), in San Giovanni in Fiore, Longobucco, Casali del Manco, Taverna and the rest of
the Sila and Presila, where the laricio was replanted after the war cuts; Villaggio Mancuso's
forest is one. With the native laricio (42.65, 8,439 ha), black pine and *loricato* it makes 79,523
ha, against INFC 2015's 73,443 ha of "pinete di pino nero, laricio e loricato" (15 % of Calabria's
high forest, 32 % of Italy's; the laricio subcategory alone is 10 % of Calabria's forest and 89 % of
Italy's). Douglas fir, the other planted conifer, covers 746 ha in INFC. So
all of it is `mountain_pine`, as CLC IV 3122 files the laricio, together with the conifer
plantations (83.31, median 855 m, 15 % below 400 m, where some will be Aleppo or maritime pine).
**Chestnut orchards count as forest**, as in Campania. Left out: **broadleaf plantations** (83.325,
22,723 ha, median 163 m: mostly the eucalyptus planted on the Ionian hills), poplar plantations,
*Ampelodesmos* steppe (32.23, 34,455 ha), bracken (31.863, 16,035 ha), garighe (32.9, 32.217),
grassland, rock and wetlands.

**Forest area and INFC.** The grid holds 586,561 ha of forest against INFC 2015's "bosco" of 495,177
ha: **+18.5 %**, outside the ±10 % line. The gap is INFC's, not the map's:

| figure | ha | grid vs it |
|---|---|---|
| INFC 2015 bosco | 495,177 | +18.5 % |
| INFC 2015 bosco + "aree boscate inaccessibili o non classificate" | 579,945 | **+1.1 %** |
| INFC 2015 total forest (bosco + altre terre boscate) | 650,620 | −9.8 % |
| Regione Calabria CUT, 311 + 312 + 313 (1:5,000) | 513,109 | +14.3 % |

INFC files 84,768 ha of Calabria's wooded land as "aree boscate inaccessibili o non classificate",
outside "bosco": 21 % of Italy's whole figure for that class, from a region with 5.9 % of its forest
(regional forest programme 2024, tables 1.7.1–1.7.2, citing INFC 2015). Those are wooded points the
inventory could not reach or classify on the ground; a map drawn from orthophotos counts them as
woods, whatever their type. The rest of INFC's "altre terre boscate" (low and sparse woods,
boscaglie, 36,814 ha of shrubland) is what the grid calls macchia and transitional. Against
INFC's categories (high forest only, so every INFC figure is short by its share of the
unclassified woods), the map's excess is in the evergreen and deciduous oaks and chestnut: holm
oak 95,500 ha (INFC leccete 48,692), cork oak 10,787 (5,224), deciduous oaks 146,933 (rovere and
roverella 53,790, cerro and farnetto 43,593), chestnut 85,328 (68,966). Its beech (100,254 ha,
INFC 79,413), pines (79,523 and 14,579 ha, INFC 73,443 and 17,474) and silver fir (3,423 ha, INFC
3,731) are close. The CUT lands between the two (+3.6 % on bosco) but cannot be
checked for types (it files only 100 ha as chestnut).

## Woodland grid

Built 2026-09-28 (`uv run python -m api.grid.build --region calabria`, 47 s once the DEM tiles and
the soil layers were cached).

- Cells 15,602; inside area 15,079 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 5,679** (36 % of the cells, the highest share of any region so far), in 312 of
  the 404 comuni. By province: Cosenza 3,008, Reggio Calabria 1,102, Catanzaro 943, Vibo Valentia
  338, Crotone 288.
- **Forest area 586,561 ha vs INFC 2015 bosco 495,177 ha: +18.5 %** (above: +1.1 % on bosco plus
  INFC's inaccessible woods). The 20 m rasterization reproduces the map's 586,590 ha within 0.01 %.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 83 % of a cell's wooded area.
- Terrain: woodland elevation median 856 m (5th–95th percentile 321–1,528 m), highest cell mean
  1,976 m (Serra Dolcedorme, Pollino, *pino loricato*), highest point in a woodland cell 2,260 m;
  slope median 19.8°, 20 % of woodland cells above 25°; 125 cells have no aspect. 16 slivers (no
  woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.30 (5.99–6.81, 5th–95th percentile), the most
  acid so far: granite, gneiss and schist under the Sila, the Serre and the Aspromonte.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (downy, Turkey and Hungarian oak) | 20.0 % | 1,274 | 678 m |
| beech | 19.7 % | 1,115 | 1,268 m |
| mountain_pine (laricio, *loricato*, black pine, plantations) | 17.6 % | 935 | 1,215 m |
| evergreen_oak (holm and cork oak) | 16.6 % | 1,079 | 590 m |
| chestnut (woods and orchards) | 15.5 % | 957 | 817 m |
| transitional_woodland_shrub | 3.0 % | 12 | |
| mixed_broadleaf (*Alnus cordata*, hop-hornbeam) | 2.8 % | 162 | 788 m |
| macchia | 2.0 % | 19 | |
| mediterranean_pine | 1.4 % | 96 | 433 m |
| fir_spruce (silver fir) | 0.7 % | 22 | 1,040 m |
| riparian | 0.5 % | 3 | |
| exotic_broadleaf | 0.2 % | 5 | |

- The comuni with the most beech-dominated woodland cells are Taverna (61), Casali del Manco (60),
  San Donato di Ninea (55), Saracena (51), Aprigliano, San Giovanni in Fiore, Grisolia and Stilo;
  with the most pine-dominated, San Giovanni in Fiore (166), Longobucco (117), Casali del Manco,
  Taverna, Bocchigliero, Celico, Aprigliano and Spezzano della Sila; with the most
  chestnut-dominated, Acri and Decollatura (34 each), Reggio di Calabria, Aprigliano, Fuscaldo,
  Gimigliano, Casali del Manco and Luzzi; silver fir dominates 13 cells of Serra San Bruno. The
  comuni with the most woodland cells: San Giovanni in Fiore (236), Longobucco (192), Casali del
  Manco (135), Acri, Taverna, Bocchigliero, Aprigliano.

Spot checks:

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Villaggio Mancuso, Sila Piccola | `1kmE4888N1801` | yes | 0.95 | mountain_pine 0.97 | 1100 | 15 | 6.3 | Sorbo San Basile (CZ) | Villaggio Racise, 1.7 km |
| Sila Greca above Longobucco | `1kmE4896N1839` | yes | 0.93 | mountain_pine 0.93, transitional 0.07 | 1198 | 24 | 6.5 | Longobucco (CS) | Longobucco, 4.9 km |
| Camigliatello Silano | `1kmE4879N1829` | no | 0.47 | riparian 0.64, mountain_pine 0.35 (village, pasture) | 1253 | 12 | 6.5 | Spezzano della Sila (CS) | Camigliatello Silano, 0.7 km |
| Monte Botte Donato, Sila | `1kmE4879N1822` | yes | 0.97 | beech 1.00 | 1805 | 16 | 6.2 | Casali del Manco (CS) | Baracchella II, 5.4 km |
| Serra Dolcedorme, Pollino | `1kmE4854N1888` | yes | 0.64 | mountain_pine 1.00 (*pino loricato*) | 1976 | 35 | 6.3 | Castrovillari (CS) | Contrada Piana 2, 6.1 km |
| Monte Cocuzzo, Catena Costiera | `1kmE4853N1814` | yes | 0.60 | beech 0.48, mountain_pine 0.32, chestnut 0.10 | 1272 | 23 | 6.3 | Mendicino (CS) | Piro, 3.7 km |
| Monte Reventino | `1kmE4873N1794` | yes | 1.00 | chestnut 1.00 | 942 | 15 | 6.3 | Decollatura (CZ) | Villa Rosa, 1.6 km |
| Bosco di Santa Maria, Serre | `1kmE4877N1742` | yes | 1.00 | fir_spruce 0.95, beech 0.05 | 1127 | 16 | 6.0 | Serra San Bruno (VV) | Ombrellino, 1.7 km |
| Mongiana, Serre | `1kmE4875N1736` | yes | 0.84 | chestnut 0.88 | 871 | 21 | 6.2 | Mongiana (VV) | Mongiana, 1.0 km |
| Gambarie, Aspromonte | `1kmE4835N1695` | yes | 0.50 | chestnut 0.44, beech 0.41, mountain_pine 0.15 | 1334 | 13 | 6.4 | Santo Stefano in Aspromonte (RC) | Gambarie, 0.2 km |
| Montalto, Aspromonte | `1kmE4842N1695` | yes | 1.00 | beech 0.96 | 1855 | 17 | 6.2 | Samo (RC) | Gambarie, 7.0 km |
| Cittanova, Aspromonte | `1kmE4857N1717` | yes | 0.98 | evergreen_oak 0.90, chestnut 0.10 | 687 | 28 | 6.1 | Cittanova (RC) | Cittanova, 2.2 km |
| Orsomarso, Valle dell'Argentino | `1kmE4832N1875` | yes | 1.00 | evergreen_oak 0.97 | 355 | 30 | 6.3 | Orsomarso (CS) | Orsomarso, 3.5 km |
| Reggio Calabria (city) | `1kmE4819N1688` | no | 0.00 | — | 42 | 7 | — | Reggio di Calabria (RC) | Reggio di Calabria, 1.0 km |

Threshold sensitivity (recomputed from stored fractions):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 7,257 | 6,399 | **5,678** | 4,956 | 4,184 |

**Soil layers from ISRIC's static files.** SoilGrids' WCS answered 503 for the whole-region request
all morning (a gateway timeout; small requests passed in about 30 s). The three pH layers were
warped instead from ISRIC's static VRT (`files.isric.org/soilgrids/latest/data/phh2o/`, the same
Homolosine COGs behind the WCS) to the EPSG:4326 GeoTIFFs the build caches (int16, 0 = no data,
about 250 m pixels): 7 s a layer. Against two WCS tiles fetched before the switch, 70–87 % of pixels
are identical and the mean difference is 0.02–0.04 pH (nearest-pixel alignment). A one-off here;
if the WCS keeps failing for other regions, `fetch` could read the VRT the same way.

**DEM tiles over open sea.** Calabria's bbox asks for twelve 1° GLO-30 tiles; the build uses the
fix cherry-picked from `region/campania` (`fix(grid): skip DEM tiles the bucket lacks over open
sea`), so the Tyrrhenian and Ionian tiles the bucket lacks are skipped.

## Weather

- Points: 77 candidates on the 0.2° lattice, **48 on land**; all 5,679 woodland cells weighted,
  none out of reach.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region calabria`,
  2026-09-28, 165 land nodes at 0.1° of 210, three 14-day windows of 2024). Cooling per km of height
  across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.16 | 3.53 | 3.77 | 4.02 | 4.5 | −0.48 |
  | temperature_2m_mean | 5.40 | 4.43 | 4.53 | 4.70 | 4.5 | +0.20 |
  | temperature_2m_min | 5.38 | 5.14 | 4.76 | 4.97 | 4.2 | +0.77 |
  | soil_temperature_0_to_7cm_mean | 4.39 | 4.98 | 3.85 | 4.32 | 3.7 | +0.62 |

  Every rate is within 1 °C/km of the national config, so **the national rates are kept**. They
  also downscale best. Leave-out RMSE against the full 0.1° field:

  | leave-out RMSE | none | 6.5 °C/km | national config |
  |---|---|---|---|
  | Tmin, served lattice (0.2°, stride 2) | 0.974 | 0.578 | **0.525** |
  | Tmin, stride 3 (0.3°) | 1.700 | 0.841 | **0.736** |
  | Tmax, stride 2 | 0.866 | 0.592 | **0.465** |
  | Tmean, stride 2 | 0.887 | 0.468 | **0.369** |
  | soil, stride 2 | 0.988 | 0.696 | **0.632** |
  | soil, stride 3 | 1.643 | 1.176 | **0.972** |

  Daily rain RMSE on the leave-out is 1.80 mm at stride 2 and 2.53 mm at stride 3 whatever the
  rates: Calabria's rain varies over shorter distances than Campania's (1.23 and 1.44 mm), the
  Tyrrhenian slopes and the Ionian coast a few kilometres apart.
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-17 (48 nodes fetched, 45 min on 2026-09-28), with snowfall from CDS's
  gridded ERA5-Land, whose national half-year files an earlier lane had already cached. Open-Meteo's
  archive and the ECMWF IFS forecast fill the days after 2026-09-17 (`onboard --only update`,
  history complete to 2026-09-22; 1,871 Open-Meteo calls counted that morning across the lanes).

### Rain scale: a station-normals check, no open daily gauges

Calabria publishes no open daily rain a script can read:

- **ARPACAL's Centro Funzionale Multirischi** (`cfd.calabria.it`, about 200 rain gauges, many in
  the mountains) calls its data public, but the "Dati storici" archive sits behind a login
  (`Login/login.php`); registration asks for an identity document, and the data may not be passed on
  (`species-ecology/calabria.md`, Weather rules). Its scanned yearbooks stop in 2000.
- **ARSAC's agrometeo network** (`arsacagrometeo.it`, farm stations) gives daily data after
  registration too.
- **ISPRA's SCIA**, which republishes regional networks' daily series with a CSV download, links
  a time-series server that answered 404 and 500 on 2026-09-28.

So no `GAUGE_NETWORKS` entry and no woodland gauge check. Instead, a one-off check read the raw CDS
rain of 2016–2025 bilinearly at 15 stations (land nodes only, weights renormalised, the stations at
their towns' coordinates) and compared it with the **long-term station normals the regional forest
programme quotes** (Programma Forestale Regionale 2024, section 1.2.1, pp. 10–11; long-term means,
dated only for Laghitello, 1939–2001, which is left out for want of its position):

| station | m | normal mm/yr | raw CDS 2016–2025 | ratio |
|---|---|---|---|---|
| Villa San Giovanni | 10 | 676 | 803 | 1.19 |
| Briatico | 25 | 815 | 911 | 1.12 |
| Tropea | 51 | 719 | 920 | 1.28 |
| Reggio Calabria | 51 | 594 | 783 | 1.32 |
| Melito di Porto Salvo | 52 | 526 | 632 | 1.20 |
| Capo dell'Armi | 103 | 494 | 632 | 1.28 |
| Joppolo | 185 | 879 | 928 | 1.06 |
| Arena | 450 | 1,114 | 872 | 0.78 |
| Serra San Bruno | 790 | 1,772 | 834 | 0.47 |
| San Lorenzo Bellizzi | 851 | 1,023 | 803 | 0.79 |
| Mongiana | 921 | 1,765 | 832 | 0.47 |
| Fabrizia | 948 | 1,720 | 837 | 0.49 |
| Villaggio Mancuso | 1,041 | 1,616 | 1,079 | 0.67 |
| Camigliatello | 1,253 | 1,634 | 1,058 | 0.65 |
| Gambarie | 1,300 | 1,608 | 889 | 0.55 |

Heights without a quoted station height (Villa San Giovanni, Reggio, Melito, Capo dell'Armi,
Camigliatello, Villaggio Mancuso) are the DEM's at the town. The pattern is the Apennine one,
stronger: the reanalysis is wet on the coast (1.19 pooled below 200 m) and far too dry in the
mountains (0.59 at 800 m and above), where the Serre catch 1,700–1,800 mm a year that its 0.1°
relief cannot raise.

**`calabria.yaml` sets 0.85 + 0.82 per km, clamped at 1,300 m**, over `era5_land_cds` and
`era5_seamless`: the least-squares fit through the origin of the normals on model totals × (a + b ×
elevation), a = 0.848, b = 0.819. It is robust to any one station (leave-one-out slopes 0.77–0.95;
0.66 without the three Serre stations, 0.76 without the four Strait-coast ones). The clamp stops it
at the highest station instead of the national 1,700 m, so the Sila and Pollino tops get 1.92, not
2.24.

| scale | factor at 200 / 500 / 800 / 1,200 m | stations below 200 m / at 800 m and above, scaled over normal |
|---|---|---|
| **Calabria (15 station normals, used)** | **1.01 / 1.26 / 1.50 / 1.83** | **1.01 / 1.00** (by construction) |
| Apennine prior (mean of Umbria, Emilia-Romagna, Campania) 0.76 + 0.55 | 0.87 / 1.04 / 1.20 / 1.42 | 0.95 / 0.79 |
| Campania (agrometeo, 11–769 m) 0.77 + 0.52 | 0.87 / 1.03 / 1.19 / 1.39 | 0.96 / 0.78 |
| Emilia-Romagna (66 woodland gauges) 0.62 + 0.80 | 0.78 / 1.02 / 1.26 / 1.58 | |
| national (Tuscan gauges) 1.28 + 0.29 | 1.34 / 1.43 / 1.51 / 1.63 | 1.55 / 0.93 |
| none | 1 | 1.19 / 0.59 |

The fit's slope matches Emilia-Romagna's woodland-gauge fit, the one dense gauge set so far. Its
weakness is the period: the normals are older long-term means (the one dated runs 1939–2001), the
model years are 2016–2025, and Calabrian rainfall has not been stationary. If the recent decade was 10 % drier than the normals' years, the
fit would be 0.76 + 0.74 (5 %: 0.81 + 0.78), so the scale may be up to about 10 % wet. It scales
totals, not timing, and the porcini's 30-day rain is a share of each cell's own (scaled) normal, so
the choice matters most for the absolute rain ramps of the ovolo and the chanterelles.

## Sightings

`uv run python -m api.sightings.ingest fetch --region calabria` (2026-09-28): **30 GBIF records** for
the three groups over the bbox (6 *B. edulis*, 5 *B. aereus*, 4 *B. reticulatus*, 4 *B.
pinophilus*, 7 *A. caesarea*, 4 *Cantharellus*) and **none from iNaturalist** in the last two
weeks. After the quality filters (11 too imprecise, 4 with unknown
uncertainty) 19 are kept, and **16 land on Calabria's woodland cells**. None is obscured:

| group | train seasons 2016–2023 | hold-out 2024–2025 | where |
|---|---|---|---|
| porcini | 7 cell-days (8 records) | 1 | Aspromonte beech (Sant'Eufemia d'Aspromonte, Reggio di Calabria, 2022; 2024 in the hold-out); Aspromonte pine (Roccaforte del Greco, 4 November 2022); Pollino beech (Saracena, September 2019); *Alnus cordata* on the Reventino side (Martirano Lombardo, 2021, 2022); oak at Mottafollone (October 2020) |
| gallinacci | 4 | 0 | Aspromonte beech and chestnut (Sant'Eufemia d'Aspromonte 2020, Reggio di Calabria 2023); Martirano Lombardo 2021; holm oak at Acquaro (Serre, 2022) |
| ovoli | 2 | 0 | chestnut at Martirano Lombardo (August 2022); holm oak at Molochio (Aspromonte, September 2023) |

One more porcini record (Longobucco, laricio, July 2011) predates the history. The Sila, the
region's best-known porcini ground, has no kept record in the grid's years.

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/calabria.md`; rules in
`api/src/api/config/species/calabria/` (46 new references; child card `region-calabria-species.md`).

- **All three groups and six keys kept.** ISPRA's two Calabria manuals file about 45,000 records of
  the regional mycological groups under their habitats; all six keys are there, in the Acri
  museum's cards, the regional monographs and the regional law (L.R. 30/2001).
- **The Sila's laricio is *B. pinophilus* ground.** Of 5,464 laricio records, *B. pinophilus* is
  0.9 % (8th of 933 species), *B. edulis* 0.3 %, *B. reticulatus* 0.1 %; the dialect keeps "sillu 'e
  pinu" apart from "sillu 'e fagu". So `mountain_pine` is a full host for *B. pinophilus* and a
  non-host (0.1) for *B. edulis*, *B. reticulatus* and the chanterelles; mixed pine and beech cells
  keep full credit through their beech.
- **Seasons:** *B. pinophilus* has a spring window (full 20 May–30 June) and an autumn one (15
  September–15 November); *B. reticulatus* is full from 1 June to 31 October; *B. aereus*'s lowland
  window runs to 10 January; the chanterelles' lowland window to 25 January; the ovolo is full from
  1 August to 5 November. The summer gap is left to the rain, heat and drying rules, not written
  into the calendar: July and August bring 3–4 % of the year's rain even in the Sila.
- **Altitude bands move up** 150–250 m with the hosts (chestnut median 816 m, beech 1,270 m on the
  map).
- **Affinities** follow what Calabria's classes hold: `macchia` (lentisk and *Cytisus*),
  `mediterranean_pine` (Aleppo pine), `mixed_broadleaf` (*Alnus cordata*) and
  `transitional_woodland_shrub` (*Spartium* and broom) move down; the evergreen oaks move up for
  the ovolo (cork oak has the highest ovolo, *B. aereus* and chanterelle shares of any habitat).
- **Weather rules, stoppers and growth clocks unchanged**: no Calabrian study gives numbers, and the
  Monte Cocuzzo field notes (ovoli 10–12 days after the last useful rain, porcini about 15) fall
  inside the Tuscan plateaus.
- **Press contrasts** (`calabria/sanity.yaml`): 15, written before any Calabria score existed, 14 for
  porcini and 1 for ovoli; 14 rest on Funghi Magazine's national bulletins (read through Wayback
  captures), one on three local outlets.
- **Hand-offs from the research, answered here.** Forest area: explained above (INFC's
  inaccessible woods). Rain scale: the station-normals fit. The 83.31 conifer plantations may hold
  some silver-fir plantations, which would belong in `fir_spruce`; the map gives them one code, so
  they stay `mountain_pine` (median 855 m, most too low for fir). The slope and aspect stoppers are
  anchored on Tuscan percentiles; Calabria's woodland slopes (median 19.8°) match Campania's, where
  they were kept.

## Validation

Scored 2016 to 2026-10-05 on 2026-09-28 (rules version `9a2df6bd6885`, rain scale 0.85 + 0.82 per
km to 1,300 m): 5,679 woodland cells × every day per key, history without factors (7 min), the
served window 2026-09-22 to 2026-10-05 with them. `onboard` ran the hold-out backtest and the sanity
check; the train-season backtest (`--seasons train --label onboard-train`) and the ovoli sanity run
(`--group ovoli --label onboard-ovoli`) were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **13** (porcini 7, gallinacci 4, ovoli 2), against
the 50 the parent plan asks for. Hold-out 2024–2025: **1** (porcini).

**Backtest** (model vs the calendar and habitat baselines; `auc_local` / `auc_region` /
`auc_time_effort`):

| seasons | group | n | model | calendar | habitat `auc_local` |
|---|---|---|---|---|---|
| hold-out 2024–2025 | porcini | 1 | 0.76 / 0.88 / 0.25 | 0.51 / 0.78 / 0.50 | 0.50 |
| train 2016–2023 | porcini | 7 | 0.59 (0.43–0.75) / 0.73 / 0.56 | 0.53 / 0.78 / 0.52 | 0.50 |
| train 2016–2023 | gallinacci | 4 | 0.57 (0.46–0.69) / 0.62 / 0.26 | 0.50 / 0.78 / 0.49 | 0.53 |
| train 2016–2023 | ovoli | 2 | 0.36 (0.32–0.39) / 0.65 / 0.55 | 0.65 / 0.93 / 0.51 | 0.60 |

Fourteen sightings say little. The porcini hold-out record (Aspromonte beech above Reggio, 6 October
2024) scores 0.70; of the seven train porcini, four score 0.77–1.00 on their day (Aspromonte beech,
Sant'Eufemia and Reggio, September and October 2022; oak at Mottafollone, October 2020; Martirano
Lombardo, 8 September 2022), the Pollino beech of 21 September 2019 0.37, and two score 0: the
Aspromonte pine of 4 November 2022 at 1,407 m and Martirano Lombardo's *Alnus cordata* on 10
September 2021. The ovoli pair splits, 0.96 in Martirano Lombardo's chestnut
(25 August 2022) and 0 in Molochio's holm oak (6 September 2023). Validating Calabria needs
located records: the Sila's porcini are the region's best known and have none kept here; the
regional mycological groups' records (ISPRA's tables count some 45,000) or the ASP mycological
inspectorates are the leads.

**Sanity check** (`calabria/sanity.yaml`), each contrast read against its own group:

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Sila 2016 > normal, 6–24 Sep | porcini | 0.923 | 0.475 | yes |
| Sila 2021 > 2019, 30 Aug–10 Sep | porcini | 0.268 | 0.453 | no |
| Sila 2020 and 2022 > 2019 and 2024, 8–22 Aug | porcini | 0.363 | 0.135 | yes |
| Sila Grande 2020 > 2025, 20 Jul–5 Aug | porcini | 0.396 | 0.000 | yes |
| Sila 2018, 2020, 2021 > 2024, 2025, 18–30 Jun | porcini | 0.551 | 0.094 | yes |
| Sila 2023: 22 Sep–12 Oct > 1–15 Sep | porcini | 0.737 | 0.154 | yes |
| Sila > Serre and Aspromonte, 3–20 Oct 2023 | porcini | 0.781 | 0.382 | yes |
| Sila > Pollino, Orsomarso, Catena Costiera, 3–20 Oct 2023 | porcini | 0.781 | 0.213 | yes |
| Sila and Catena Costiera > inner Pollino, 15 Sep–15 Oct 2021 | porcini | 0.796 | 0.817 | no |
| Pollino and Catena Costiera > Serre and Aspromonte, 20 Oct–5 Nov 2022 | porcini | 0.730 | 0.350 | yes |
| Catena Costiera and Orsomarso > Serre and Aspromonte, 14–26 Aug 2023 | porcini | 0.361 | 0.229 | yes |
| Tyrrhenian Aspromonte and Serre 2020 > 2024, 8–20 Aug | porcini | 0.216 | 0.000 | yes |
| Sila 2020: 28 Sep–20 Oct > 1–20 Sep | porcini | 0.764 | 0.078 | yes |
| Sila spring 2023 > 2020 and 2022, 10–20 May | porcini | 0.657 | 0.251 | yes |
| Sila Piccola and Greca 2019: 10–20 Sep > 22 Aug–8 Sep | ovoli | 0.438 | 0.128 | yes |

**13 of 15 hold** (porcini 12/14, ovoli 1/1); the `Data` section's "13/15" is the default run, which
scores all 15 on the porcini group (the ovoli contrast holds there too, 0.775 against 0.196). The
two misses: early September 2021 against 2019 in the Sila, where the 2019 side rests on "in modo
sporadico" and the model puts 2019 higher; and autumn 2021, where
the inner Pollino, "poor throughout" in the bulletins, scores a shade above the Sila and the Catena
Costiera (0.817 against 0.796), both high. The contrasts that separate the Sila from the Serre and
Aspromonte in October 2023, and the timing contrasts of 2020 and 2023, hold by wide margins.

**The served window.** On 28 September 2026 porcini average 0.41 across Calabria's woodland cells,
with 1,769 cells at 0.6 or more: the beech, chestnut and pine of the Sila Piccola and the Presila
(San Giovanni in Fiore, Taverna, Aprigliano, Cotronei, Sorbo San Basile, Petilia Policastro,
Decollatura) and the Serre (Stilo), at a median 969 m. The reanalysis gives the nodes about 43 mm
over the last 30 days (29 August–27 September, raw), against 27–139 mm in the same window of past
years (median about 58), with the storms of 20–25 September; so Calabria scores where Campania and
the central regions read near 0 the day before. Ovoli average 0.39 and gallinacci 0.44.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-28 (`deploy/rsync-region-data.sh calabria`, 214
files, 435 MB, no redeploy). The server serves a region only when its YAML is in the deployed code and its stores are
on disk, so they stay inert until `main` with `config/regions/calabria.yaml` is deployed by the
rail's "Deploy pulled main" step (with the daily job, which brings the weather and scores up to that
day). Then check:

- [ ] `https://mappafunghi.app/calabria` and `/calabria/porcini`, `/calabria/ovoli`,
  `/calabria/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Calabrian habitats (laricio pine in the Sila, beech on the Aspromonte, silver fir at
  Serra San Bruno).
- [ ] `https://api.mappafunghi.app/regions` lists `calabria`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Calabria URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/calabria` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Calabria", description, canonical, og image `og/calabria.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1458).
- [ ] `/credits` shows "ISPRA, Regione Calabria — Carta della Natura della Regione Calabria
  1:25.000".
- [ ] The next morning's daily job has a `region_done` line for `calabria`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Rain scale from normals, not daily gauges.** The scale is fitted on older long-term station
  means (Weather); if 2016–2025 was drier, it is up to about 10 % wet. ARPACAL's Centro Funzionale
  archive, after registration, would allow a woodland gauge check, but its terms forbid passing the
  data on: the human's call.
- **Forest area +18.5 % on INFC bosco**, explained by INFC's 84,768 ha of inaccessible and
  unclassified woods (+1.1 % with them), but the map's evergreen and deciduous oak areas are well
  above INFC's categories; some of what it maps as holm or downy oak wood INFC would call low or
  sparse woods (altre terre boscate).
- **Laricio plantations and native laricio share one key.** 42.G_n (70,157 ha, the post-war
  reforestation) and 42.65 (8,439 ha) are both `mountain_pine`; the ISPRA records suggest the
  porcini favour the older stands. The 83.31 plantations may include some silver fir.
- **Validation rests on fourteen sightings** and mostly one magazine's bulletins; the Sila has no
  located record (Validation).
- **SoilGrids from the static files** (Woodland grid): a one-off workaround for the WCS's 503s.
- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point.
  Calabria's bbox overlaps Campania's in a sliver of sea and Basilicata's coast near Maratea, and
  will overlap Basilicata's and Sicily's (the Strait of Messina). Card `fix-region-lookup-by-boundary.md`.
- **The DEM sea-tile fix** is cherry-picked from `region/campania`; the two branches carry the same
  commit content and merge cleanly in either order.

## Data

- cells: 15602
- woodland cells: 5679
- INFC deviation: +18.4% (grid 586,561 ha vs 495,177 ha) — outside ±10%
- weather nodes: 48
- years stored: 2016–2026 (11 years)
- sightings kept: 16
- backtest AUC (auc_local, model, all): porcini 0.756
- sanity contrasts: 13/15 passed

