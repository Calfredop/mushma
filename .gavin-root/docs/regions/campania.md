# campania

Region #14 of the full-Italy rollout (card `region-campania.md`). API id `campania`, web slug
`/campania`, ISTAT COD_REG 15, Wikidata Q1438. Config: `api/src/api/config/regions/campania.yaml`.
The first southern region.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | ISPRA and ARPA Campania, **Carta della Natura della Regione Campania, carta degli habitat 1:25.000** (Bagnaia, Viglietti et al. 2017, published 2018) (`ispra_cnat_campania`) | CC BY 4.0 | GeoPackage on ISPRA's SDI (`sdi.isprambiente.it/download_ogc/cnat/`), no login |
| forest-area cross-check | Regione Campania, Carta dell'utilizzazione agricola dei suoli (CUAS) 2009 | no licence stated (open by default) | ArcGIS REST on the SIT's server; not used by the build |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | two open-sea DEM tiles do not exist (below) |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 9703 "Campania, IT" | per record | counts per cell only |

**What was checked, and why the Carta della Natura.**

- **CUAS, Carta dell'utilizzazione agricola dei suoli** (the card's candidate): the Region's
  land-use map, updated in 2009 from the 2001 edition, served as layer 5 of
  `geomaps.regione.campania.it/server/rest/services/SIT/Cartografia_Tematica/MapServer` (30,669
  polygons, queryable). It is an agricultural map: its forest classes are only 5.1 boschi di
  latifoglie (366,721 ha), 5.2 conifere (5,615 ha) and 5.3 misti (3,658 ha), with 2.5 castagneti da
  frutto (8,891 ha) filed among the tree crops, 6.2 cespuglieti and 6.3 vegetazione sclerofilla.
  No forest types, so it could only give `forest.groups`, with CLC IV for the types (Tuscany's
  pattern). No licence is stated on the SIT, the ArcGIS item, or the GeoNetwork records; L.R.
  Campania 14/2013 (art. 2 m, art. 3) makes the Region's data freely reusable with attribution,
  but names no licence.
- **Carta Forestale d'Italia CFI2020** (CREA): shapefiles on request only, as for Marche and
  Umbria. Not scriptable.
- **Piani di gestione forestale** (agricoltura.regione.campania.it): map sheets of the state forests
  only, not a regional layer.
- **Carta della Natura, Campania** (ISPRA with ARPA Campania, the Region's environment agency):
  habitat map of the whole region, photo-interpreted at 1:5,000 and returned at 1:25,000
  (convention 2015–2017), 42,792 polygons, each with its CORINE Biotopes habitat (`codice_corine`):
  41.18 southern beech woods, 41.9 chestnut woods, 83.12 chestnut orchards, 41.7511 Turkey-oak woods,
  41.732 downy-oak woods, 41.8 hop-hornbeam and mixed thermophilous woods, 41.C1 *Alnus cordata*,
  45.31/45.32 holm oak, 42.83 stone pine, 83.31 conifer plantations, 42.15 southern Apennine silver
  fir… One layer gives both the broad groups and the forest types, read once (Marche's pattern), at
  a finer scale and later date than CUAS or CLC IV (1:100,000, 2018).

**Licence.** The RNDT record (`ispra_rm:0005CNATHB_DT`) declares "Dato concesso con licenza
CC-BY-4.0 — gli Enti proprietari dei dati sono ARPA Campania e ISPRA", with a link to the CC BY 4.0
deed, and then asks that reproduction "a mezzo stampa e internet … ai fini di ricerca, didattici, di
divulgazione, di studio, di tempo libero" be requested and the source cited. The app credits
"Carta della Natura della Regione Campania © ISPRA, ARPA Campania, CC BY 4.0", and its use (a free
map for dissemination and leisure) is one the record names. A courtesy notice to
`cartanatura@isprambiente.it` would satisfy the "previa richiesta" clause; it has not been sent
(Known limitations).

**Download.** `https://sdi.isprambiente.it/download_ogc/cnat/CNAT_Habitat_Campania.gpkg` (174 MB,
layer `CNAT_Habitat_Campania`, EPSG:25832). The GeoPackage's metadata has a non-UTF-8 byte that
makes `pyogrio.read_info` fail; `read_dataframe`, which the build uses, reads it fine.

Class mapping (`campania.yaml`), whole-map areas:

| CORINE Biotopes | group | habitat | ha |
|---|---|---|---|
| 41.7511, 41.7512 Turkey oak (and Hungarian oak); 41.732 downy oak | broadleaf | deciduous_oak | 102,973; 59,669 |
| 41.18 faggete dell'Italia meridionale | broadleaf | beech | 65,276 |
| 41.9 chestnut woods; 83.12 chestnut orchards | broadleaf | chestnut | 51,140; 24,340 |
| 41.8 hop-hornbeam, hornbeam, ash, maple; 41.C1 *Alnus cordata*; 41.4 ravine woods; 41.B birch; 41.D aspen | broadleaf | mixed_broadleaf | 38,680; 11,386; 574 |
| 45.31, 45.32 holm oak; 45.21 cork oak | broadleaf | evergreen_oak | 35,929; 728 |
| 44.61 poplar, 44.14 willow, 44.513 black alder, 44.71 plane, 44.9 alder-willow swamp woods | broadleaf | riparian | 11,584 |
| 41.Lcn exotic broadleaf; 44.D2cn allochthonous riparian woods | broadleaf | exotic_broadleaf | 2,397 |
| 83.31 conifer plantations | conifer | mountain_pine | 12,619 |
| 42.83 stone pine, 42.84 Aleppo pine, 16.29 wooded dunes | conifer | mediterranean_pine | 3,253 |
| 42.15 silver fir | conifer | fir_spruce | 90 |
| 42.A1 cypress | conifer | other_conifer | 85 |
| 32.3, 32.4 garighe e macchie mesomediterranee; 32.214 lentisk, 32.215 *Cytisus*, 32.22 *Euphorbia dendroides* macchia; 32.13, 16.27, 16.28 juniper and dune macchia | macchia | macchia | 23,090 |
| 31.8A bramble, 31.81 deciduous scrub, 32.A *Spartium*, 31.844, 31.845, 32.26 broom, 31.8C hazel scrub, 44.12 shrub willows | transitional | transitional_woodland_shrub | 29,877 |

Forest (broadleaf + conifer) 420,723 ha on the whole map. **Chestnut orchards count as forest**:
INFC files them under its chestnut category, and they are prime ground for porcini and ovoli in
Irpinia, Roccamonfina and the Cilento (the map holds 24,340 ha of them; CUAS 8,891 ha). **Conifer plantations go to `mountain_pine`**: they are the black-pine reforestation of
inland Irpinia and the Sannio (two thirds of their area at 400–1,000 m: Ariano Irpino, Bisaccia,
Greci, Vallata, Zungoli), as Marche files its black pine; about a fifth lies below 200 m (the
plain around Nola, Paestum), where they are stone pine. Left out, as UCS and CLC leave 321/322 out
in Tuscany: 32.23 *Ampelodesmos* steppe and garrigue (13,146 ha), 31.863 bracken (4,527 ha),
grassland, rock and wetlands; hazel orchards (83.19cn, 29,796 ha), poplar and other broadleaf
plantations (83.321, 83.325) and parks stay farmland or town.

## Woodland grid

Built 2026-09-27 (`uv run python -m api.grid.build --region campania`, 38 s with the DEM tiles
fetched for the first time).

- Cells 14,151; inside area 13,603 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 3,733** (26 % of the cells), in 375 of the 549 comuni. By province: Salerno
  1,895, Avellino 749, Caserta 621, Benevento 351, Napoli 117.
- **Forest area 420,450 ha vs INFC 2015 bosco 403,927 ha: +4.1 %**, inside ±10 %. The 20 m
  rasterization reproduces the map's 420,723 ha within 0.1 %. Without the chestnut orchards it
  would be −1.9 %. CUAS 2009 holds 375,994 ha of forest (−6.9 %), 384,885 ha with its chestnut
  orchards (−4.7 %).
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 85 % of a cell's wooded area.
- Terrain: woodland elevation median 700 m (5th–95th percentile 235–1,321 m), highest cell mean
  1,718 m (Monte Cervati), highest point in a woodland cell 1,889 m; slope median 19.9°
  (Tuscany 16.6°), 24 % of woodland cells above 25°; 54 cells have no aspect. 15 slivers (no
  woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.58 (6.17–7.11, 5th–95th percentile), between
  Tuscany's and Marche's: volcanic ash and flysch over much of the chestnut belt, limestone on the
  Matese, Picentini, Alburni and Lattari.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (Turkey and downy oak) | 30.8 % | 1,249 | 568 m |
| chestnut (woods and orchards) | 20.1 % | 799 | 660 m |
| beech | 19.2 % | 747 | 1,209 m |
| mixed_broadleaf (hop-hornbeam, *Alnus cordata*) | 14.0 % | 509 | 783 m |
| evergreen_oak (holm oak) | 8.4 % | 334 | 420 m |
| transitional_woodland_shrub | 2.6 % | 6 | |
| mountain_pine (conifer plantations) | 2.2 % | 46 | 632 m |
| macchia | 1.0 % | 6 | |
| riparian | 0.9 % | 11 | 238 m |
| mediterranean_pine | 0.5 % | 17 | 396 m |
| exotic_broadleaf | 0.4 % | 9 | 559 m |
| fir_spruce, other_conifer | < 0.1 % | 0 | |

- The comuni with the most beech-dominated woodland cells are Bagnoli Irpino (47), Acerno, Sanza,
  Calabritto, Campagna and San Gregorio Matese; with the most chestnut-dominated, Acerno (31),
  Giffoni Valle Piana, Montella, Serino, Roccamonfina, Monteforte Irpino, Giffoni Sei Casali and
  Tramonti. The comuni with the most woodland cells: Sanza (107), Campagna, Acerno, Montella,
  Casaletto Spartano, Bagnoli Irpino, Giffoni Valle Piana.

Spot checks:

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Laceno woods | `1kmE4750N1981` | yes | 1.00 | beech 0.95, mixed_broadleaf 0.05 | 1187 | 27 | 6.2 | Bagnoli Irpino (AV) | Contrada Agnolivieri, 3.1 km |
| Acerno, Picentini | `1kmE4747N1974` | yes | 0.88 | chestnut 0.56, deciduous_oak 0.31, transitional 0.11 | 707 | 16 | 6.3 | Acerno (SA) | Acerno, 2.3 km |
| Monte Terminio | `1kmE4739N1983` | yes | 0.88 | beech 1.00 | 1430 | 23 | 6.2 | Volturara Irpina (AV) | Volturara Irpina, 6.4 km |
| Monte Cervati | `1kmE4788N1927` | yes | 0.69 | beech 1.00 | 1718 | 26 | 6.4 | Piaggine (SA) | Posto della Madonna-Verlingieri, 7.7 km |
| Roccamonfina | `1kmE4656N2029` | yes | 0.53 | chestnut 0.80, riparian 0.20 | 570 | 9 | 6.6 | Roccamonfina (CE) | Garofali, 0.6 km |
| Monte Faito (Lattari) | `1kmE4701N1963` | yes | 0.79 | chestnut 0.42, mountain_pine 0.29, beech 0.29 | 1018 | 26 | 6.4 | Castellammare di Stabia (NA) | Villaggio Monte Faito, 0.1 km |
| Ischia, Epomeo | `1kmE4651N1967` | yes | 0.64 | chestnut 0.65, transitional 0.22, evergreen_oak 0.12 | 633 | 22 | 6.4 | Serrara Fontana (NA) | Migliaccia, 0.6 km |
| Taburno | `1kmE4708N2011` | yes | 0.89 | beech 0.82, fir_spruce 0.18 (the planted silver fir) | 1160 | 22 | 6.3 | Tocco Caudio (BN) | Madonna Immacolata, 2.6 km |
| Alburni, Petina | `1kmE4776N1954` | yes | 0.61 | deciduous_oak 0.95, transitional 0.05 | 690 | 10 | 6.7 | Petina (SA) | Petina, 1.8 km |
| Vesuvius, upper cone | `1kmE4696N1980` | no | 0.00 | transitional 1.00 (regrowth on lava) | 1029 | 22 | 6.8 | Ottaviano (NA) | Somma Vesuviana, 5.3 km |
| Napoli (city) | `1kmE4680N1982` | no | 0.01 | a scrap of exotic broadleaf | 78 | 10 | — | Napoli (NA) | Napoli, 0.6 km |

Threshold sensitivity (recomputed from stored fractions, a few cells off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 5,519 | 4,526 | **3,731** | 3,042 | 2,415 |

**DEM tiles over open sea.** Campania's bbox reaches 39.99° N, so it asks for the 1° tiles N39 E013
and N39 E014, which lie wholly in the Tyrrhenian: the Copernicus bucket has no such tiles and
answers 404. `api.grid.sources.fetch_dem_tiles` now skips a tile the bucket lacks (and fails only
when a region has none); Sicily, Sardinia, Calabria and Puglia will need the same.

## Weather

- Points: 75 candidates on the 0.2° lattice, **60 on land**; 3,726 of the 3,733 woodland cells
  weighted, 7 out of reach (island and coastal slivers more than 30 km from a land node).
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region campania`,
  180 land nodes at 0.1°, −22 to 1,047 m of model height, three 14-day windows of 2024). Cooling per
  km of height across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference | all, nodes above 300 m |
  |---|---|---|---|---|---|---|---|
  | temperature_2m_max | 5.62 | 4.42 | 4.83 | 4.85 | 4.5 | +0.35 | 5.31 |
  | temperature_2m_mean | 5.96 | 4.81 | 5.25 | 5.24 | 4.5 | +0.74 | 5.19 |
  | temperature_2m_min | 6.54 | 5.01 | 5.55 | **5.67** | 4.2 | **+1.47** | 4.84 (+0.64) |
  | soil_temperature_0_to_7cm_mean | 5.27 | 6.89 | 4.84 | **5.29** | 3.7 | **+1.59** | 4.77 (+1.07) |

  Tmin and soil cool more than 1 °C/km faster than the national rates across all nodes. **The
  national rates are kept** anyway, as Piemonte kept its Tmin (+1.04):
  - the steep fits come from the coast: the lowland nodes by the sea stay warm at night and in
    winter (January Tmin 6.54 °C/km). Above 300 m, where 91 % of the woodland cells are, Tmin cools at
    4.84 °C/km, inside the line, and soil at 4.77 (+1.07), on it;
  - Campania's own rates barely downscale better. Leave-out RMSE, national rates vs Campania's
    fitted rates (Tmin and soil only / all four):

    | leave-out RMSE | national | Tmin and soil fitted | all four fitted | 6.5 °C/km | none |
    |---|---|---|---|---|---|
    | Tmin, served lattice (0.2°, stride 2) | 0.540 | 0.522 | 0.522 | 0.528 | 0.748 |
    | Tmin, stride 3 (0.3°) | 0.702 | 0.688 | 0.688 | 0.709 | 1.033 |
    | soil, stride 2 | 0.504 | 0.503 | 0.503 | 0.532 | 0.659 |
    | soil, stride 3 | 0.578 | 0.606 | 0.606 | 0.682 | 0.825 |
    | Tmean, stride 2 | 0.349 | 0.349 | 0.341 | 0.360 | 0.607 |

    A 0.02 °C gain on Tmin and a loss on soil at the coarser lattice do not justify a per-region
    lapse rate, which the weather config does not support (lapse rates are national, in
    `weather.yaml`).
  - Daily rain RMSE on the leave-out is 1.23 mm at stride 2 and 1.44 mm at stride 3 whatever the
    rates.
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-16 (60 nodes fetched, 44 min on 2026-09-27), with snowfall from CDS's
  gridded ERA5-Land, whose national half-year files an earlier lane had already cached. Open-Meteo's
  archive and the ECMWF IFS forecast fill the days after 2026-09-16 (`onboard --only update`).
- `uv sync --group cds` was missing in this checkout; the first CDS run stopped at once on it.

### Rain scale: a lowland gauge check, no woodland gauges

Campania has no open daily rain from gauges in its woods:

- The Centro Funzionale Multirischi (Protezione Civile) runs about 200 rain gauges, many in the
  mountains. Its portal's REST API is public for the station list (with heights) and the last two
  days of each sensor (`CentroFunzionalePortaleRest/rest/recuperodati/…`), but the archive is
  delivered only after registration (signed `.p7m` files). Not used.
- The Region's **agrometeo network** (Assessorato Agricoltura, 38 stations) publishes daily data for
  every station as monthly Excel archives, no login
  (`agricoltura.regione.campania.it/meteo/dati_<year>/<mese>_<year>.zip`; 2019–2021 in one layout,
  2022– in another). All 38 are farm stations at 11–769 m: **none lies in a woodland cell** (the
  most wooded, Montella's, is 24 % forest), so `api.weather.checks gauges`, which compares woodland
  cells only, has nothing to compare, and no network was wired into `GAUGE_NETWORKS`.

So a one-off lowland check read the stored CDS rain bilinearly at each agrometeo gauge's own
position (sea nodes left out, as the model does) and compared totals over each gauge's days,
2019–2025 (calendar days; the 34 gauges with 1,000 or more days after merging spellings that
changed between years; Barano d'Ischia is out of the lattice's reach):

| band | gauges | raw CDS / gauge rain (pooled) |
|---|---|---|
| below 200 m | 19 | 1.21 |
| 200–400 m | 5 | 1.10 |
| 400–800 m | 9 | 0.96 |
| all | 33 | 1.12 (median gauge 1.17) |

Capaccio-Gromola (11 m, on the Paestum plain) reads 2,550 mm a year against 670–1,040 mm at
the other plain gauges and a daily correlation of 0.26 (the others 0.54–0.80), so it is left out as
faulty; with it the fit below is 0.86 + 0.30 per km. The reanalysis rains too often (1 mm or more
on 30–37 % of days, the gauges 17–30 %): the same drizzle excess Piemonte found.

**`campania.yaml` sets 0.77 + 0.52 per km** over `era5_land_cds` and `era5_seamless`: the least-squares
fit through the origin of gauge totals on model totals × (a + b × elevation), a = 0.765, b = 0.520.
Above 800 m, where most of the beech and half the chestnut grow, the slope is an extrapolation;
it has the shape every Apennine woodland fit on the same CDS rain has found (about right or wet in
the lowlands, dry in the mountains):

| fit (CDS rain) | a | b per km | factor at 200 / 500 / 800 / 1,200 m |
|---|---|---|---|
| **Campania (33 agrometeo gauges, 11–769 m, used)** | **0.77** | **0.52** | **0.87 / 1.03 / 1.19 / 1.39** |
| Umbria (8 woodland gauges, 402–1,053 m) | 0.89 | 0.33 | 0.96 / 1.06 / 1.15 / 1.29 |
| Emilia-Romagna (66 woodland gauges, 183–1,535 m) | 0.62 | 0.80 | 0.78 / 1.02 / 1.26 / 1.58 |
| Marche (borrowed: mean of the two above) | 0.76 | 0.57 | 0.87 / 1.04 / 1.22 / 1.44 |
| national (Tuscan gauges, `era5_seamless`) | 1.28 | 0.29 | 1.34 / 1.43 / 1.51 / 1.63 |

West of the Apennine chain orographic rain reaches 1,700–2,000 mm a year and the high reliefs up to
2,200 mm, against under 1,000 mm on the coast (`species-ecology/campania.md`, Climate, citing
Allocca et al. 2014 and the regional forest plan), so a mountain factor above 1 is expected. A national
or per-zone calibration (card `fix-rain-calibration-region-borders.md`) should replace this; the
Centro Funzionale's archive would allow a woodland check if the human registers for it.

## Sightings

`uv run python -m api.sightings.ingest fetch --region campania` (2026-09-27): **24 GBIF records**
for the three groups over the bbox (4 *B. edulis*, 6 *B. reticulatus*, none of *B. aereus* or
*B. pinophilus*, 4 *A. caesarea*, 10 *Cantharellus*) and **none from iNaturalist** in the last two
weeks. After the quality filters (4 too imprecise, 4 with unknown uncertainty) 20 are kept, and
**12 land on Campania's woodland cells** (8 are outside the region inside the bbox, or on
non-woodland cells). All 12 are on woodland, none obscured:

| group | train seasons 2016–2023 | hold-out 2024–2025 | where |
|---|---|---|---|
| porcini | 3 cell-days (4 records) | 0 | Laceno beech (Bagnoli Irpino, June 2020); Matese beech (San Gregorio Matese, 13 September 2022, two cells) |
| gallinacci | 2 | 5 | Taburno beech (Moiano, Tocco Caudio, 8 October 2024, three cells); holm oak at Capua and Caserta; Vesuvius chestnut (Ottaviano); Campi Flegrei oak (Pozzuoli) |
| ovoli | 0 | 1 | Matese hop-hornbeam (Piedimonte Matese, September 2025) |

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/campania.md`; rules in
`api/src/api/config/species/campania/` (31 new references, all opened; child card
`region-campania-species.md`).

- **All three groups and six keys kept.** The regional checklist (25 years in 16 areas) has *C.
  cibarius* and *B. edulis* in its second-highest frequency class and *B. aereus* in the 70–80 %
  class; the ovolo is in 11 of its 16 areas. *B. pinophilus* is the rare one but the checklist, the
  regional atlas and the picking rules all name it. The regional law is L.R. 8/2007: ovoli capped at
  1 kg a day, the closed ovolo banned.
- **The Campania porcino is the black one low down and the summer one high up.** *B. aereus* is the
  main porcino of the lower chestnut and oak ("assente sotto faggio"); *B. aestivalis* (=
  *reticulatus*) prefers the beech from 1,100 to 1,600–1,700 m; *B. edulis* is uncommon, in the
  highest beech in late autumn. *B. reticulatus* takes beech as a full host and its altitude band
  reaches the beech tree line (full to 1,600 m, 0 at 1,900 m): its located records sit at a median
  1,118 m (Tuscany 649 m).
- **Seasons:** *B. aereus*'s summer/autumn handover moves up to 600–800 m and its lowland window
  stays full to 30 November (0 on 10 January); the gallinacci mountain window opens from mid-May.
  Other windows stay Tuscany's.
- **13 affinities move** for what the Carta della Natura classes hold here: bramble, broom and
  *Spartium* (`transitional_woodland_shrub`) go down for every key; hop-hornbeam and *Alnus cordata*
  (`mixed_broadleaf`) go down for *B. edulis* and up for *B. aereus*; beech goes up for *B.
  reticulatus* and gallinacci, deciduous oak up for gallinacci.
- **Weather rules, stoppers and growth clocks unchanged**: no Campania or southern-Apennine study
  gives numbers, and the regional lore (rain, then sultry heat and no wind) agrees with them.
- **Press contrasts** (`campania/sanity.yaml`): 13, written before any Campania score existed, 11 for
  porcini and 2 for gallinacci (none for ovoli: no Campania source judges an ovolo year). Most rest on
  Funghi Magazine's national bulletins, read through Wayback captures.

## Validation

Scored 2016 to 2026-10-04 on 2026-09-27 (rules version `4046ecb26310`, rain scale 0.77 + 0.52 per
km): 3,733 woodland cells × every day per key, history without factors, the served window
2026-09-21 to 2026-10-04 with them. `onboard` ran the hold-out backtest and the sanity check; the
train-season backtest (`--seasons train --label onboard-train`) and the gallinacci sanity run
(`--group gallinacci`) were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **5** (porcini 3, gallinacci 2), against the 50 the
parent plan asks for. Hold-out 2024–2025: **6** (gallinacci 5, ovoli 1).

**Backtest** (model vs the calendar baseline; `auc_local` / `auc_region` / `auc_time_effort`):

| seasons | group | n | model | calendar | habitat `auc_local` |
|---|---|---|---|---|---|
| hold-out 2024–2025 | gallinacci | 5 | 0.60 (0.47–0.73) / 0.97 / 0.77 | 0.53 / 0.79 / 0.60 | 0.51 |
| hold-out 2024–2025 | ovoli | 1 | 0.87 / 0.99 / 0.77 | 0.76 / 0.95 / 0.61 | 0.71 |
| train 2016–2023 | porcini | 3 | 0.62 (0.54–0.70) / 0.85 / 0.32 | 0.50 / 0.77 / 0.50 | 0.50 |
| train 2016–2023 | gallinacci | 2 | 0.40 / 0.81 / 0.67 | 0.34 / 0.59 / 0.47 | 0.53 |

The model ranks the sighting cells well against the whole region (`auc_region` 0.81–0.99: they are
beech, holm oak and chestnut cells in season) and better than the calendar and habitat baselines
locally, but eleven sightings in a handful of weeks say little. The two Matese porcini of 13
September 2022 score 0.73–0.74, on a day the model rates below most other days of that season
in those cells (`auc_time_effort` 0.19). Validating Campania needs records with locations: the mycological
groups' exhibition records (the Matese and Laceno societies), the ASL mycological inspectorates, or
southern Italy's records pooled.

**Sanity check** (`campania/sanity.yaml`), each contrast read against its own group:

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Laceno 2016 > normal, 15 Sep–2 Oct | porcini | 0.949 | 0.531 | yes |
| Salerno 2018 > 2017, 20 Aug–4 Sep | porcini | 0.846 | 0.000 | yes |
| Campania June 2018 > June 2024 | porcini | 0.511 | 0.060 | yes |
| Campania September: normal > 2019 | porcini | 0.434 | 0.447 | no |
| Campania 2020: October > late August–September | porcini | 0.849 | 0.129 | yes |
| Matese > Cilento, early August 2020 | porcini | 0.628 | 0.125 | yes |
| Irpinia > Matese, 8–22 Sep 2021 | porcini | 0.179 | 0.197 | no |
| Campania August 2022 > 2019 and 2021 | porcini | 0.511 | 0.143 | yes |
| Cilento > Irpinia, 15–28 Aug 2023 | porcini | 0.809 | 0.547 | yes |
| Irpinia > Matese, 1–12 Oct 2023 | porcini | 0.034 | 0.000 | yes |
| Cilento > Matese, 8–16 Aug 2024 | porcini | 0.027 | 0.623 | no |
| Salerno gallinacci 2018 > 2017 | gallinacci | 0.653 | 0.005 | yes |
| Campania gallinacci June 2023 > normal | gallinacci | 0.789 | 0.456 | yes |

**10 of 13 hold** (porcini 8/11, gallinacci 2/2); the `Data` section's "10/13" is the default run,
which scores all 13 on the porcini group and happens to give the same count. Of the three misses:
September 2019 is a near tie (0.434 against 0.447, and "normal" includes 2019); the Matese side of
2021 rests on a hedge ("potrebbe migliorare"); and August 2024 puts the Matese well above the
Cilento where the bulletin says the Matese "ha già dato" and the Cilento was better, possibly the
Molise side of the Matese. Irpinia against the Matese in October 2023 holds on scores near 0.

**The served window.** On 27 September 2026 porcini score 0 across Campania: the reanalysis puts
the last 30 days at about 26 % of the cells' normal rain (1–16 September brought 10 mm against 37–157
mm in past Septembers), and porcini's 30-day rain factor is 0 below 50 %; season, habitat and
altitude are near full credit. The 25 September storm (8 mm on average over the nodes, about 90 mm at the Centro
Funzionale's Agerola gauge) is in the trigger window but not enough to lift the month. Gallinacci
mean 0.11 and ovoli 0.02, with no cell at 0.6 or more on the combined score. Marche and Umbria read
near 0 for porcini on the same days, so this is the weather, not the Campania rules.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-27 (`deploy/rsync-region-data.sh campania`, 208
files, 310 MB, no redeploy). The server serves a region only when its YAML is in the deployed code
and its stores are on disk, so they stay inert until `main` with `config/regions/campania.yaml` is
deployed by the rail's "Deploy pulled main" step (with the daily job, which brings the weather and
scores up to that day). Then check:

- [ ] `https://mappafunghi.app/campania` and `/campania/porcini`, `/campania/ovoli`,
  `/campania/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Campania habitats (chestnut on the Roccamonfina, beech on the Laceno).
- [ ] `https://api.mappafunghi.app/regions` lists `campania`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Campania URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/campania` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Campania", description, canonical, og image `og/campania.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1438).
- [ ] `/credits` shows "ISPRA, ARPA Campania — Carta della Natura della Regione Campania 1:25.000".
- [ ] The next morning's daily job has a `region_done` line for `campania`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Rain scale above 800 m is extrapolated.** Campania's open gauges are all farm stations at 11–769
  m; the mountain factor follows the shape of the Apennine woodland fits (Weather). Card
  `fix-rain-calibration-region-borders.md`; the Centro Funzionale's archive, after registration,
  would allow a woodland gauge check.
- **Carta della Natura licence clause.** The record declares CC BY 4.0 and also asks that
  reproduction be requested (Sources). A courtesy notice to ISPRA (`cartanatura@isprambiente.it`)
  and ARPA Campania has not been sent; it is the human's call.
- **Conifer plantations are all `mountain_pine`.** About a fifth of their area lies below 200 m and is
  likely stone pine (Sources).
- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point. No
  served region's bbox overlaps Campania's today, but Lazio's, Molise's, Puglia's and Basilicata's
  will. Card `fix-region-lookup-by-boundary.md`.
- **Validation rests on eleven sightings** and one magazine's bulletins (Validation).
- **DEM sea tiles.** The grid build now skips Copernicus tiles that do not exist over open sea
  (Woodland grid); the other coastal southern regions rely on the same change.

## Data

- cells: 14151
- woodland cells: 3733
- INFC deviation: +4.1% (grid 420,450 ha vs 403,927 ha) — within ±10 %
- weather nodes: 60
- years stored: 2016–2026 (11 years)
- sightings kept: 12
- backtest AUC (auc_local, model, all): gallinacci 0.599, ovoli 0.868
- sanity contrasts: 10/13 passed

