# puglia

Region #15 of the full-Italy rollout (card `region-puglia.md`). API id `puglia`, web slug `/puglia`,
ISTAT COD_REG 16, Wikidata Q1447. Config: `api/src/api/config/regions/puglia.yaml`. The third
southern region, after Campania and Calabria, and the least wooded so far.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Puglia, **Carta dei Tipi Forestali della Regione Puglia** (ARIF and DiSAAT, Università di Bari; DGR 806/2020, approved by DGR 1279/2022) (`puglia_tipi_forestali`) | open by default (CAD art. 52 c. 2), credited as CC BY 4.0 | ArcGIS REST on the SIT Puglia's federated server, no login |
| forest-area cross-checks | Regione Puglia, Uso del Suolo 2011 (UDS, 1:5,000); ISPRA and ARPA Puglia, Carta della Natura della Regione Puglia 1:50,000 (2013) | IODL 2.0; CC BY 4.0 | not used by the build |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | open-sea DEM tiles skipped (Woodland grid) |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 13069 "Apulia, IT" | per record | counts per cell only |

**What was checked, and why the Carta dei Tipi Forestali.**

- **Uso del Suolo 2011** (the card's candidate; SIT Puglia, published on `dati.puglia.it` under
  IODL 2.0): the Region's land-use map at 1:5,000 (0.25 ha minimum unit), CORINE classes to the
  IV level, photo-interpreted on the 2011 orthophotos. Its forest layer ("Superfici boscate",
  62,287 polygons) holds 311 boschi di latifoglie 97,788 ha, 312 conifere 15,229 ha and 313 misti
  12,946 ha, **125,963 ha**, plus 314 prati e pascoli alberati 17,024 ha, 323 sclerophyll
  vegetation 35,183 ha and 322 scrub 28,425 ha. Its IV level splits no forest type (only 3241/3242
  natural and artificial recolonisation), so it could only give `forest.groups`, with a second map
  for the types. A 2023 update (UDS 2023, CC BY 4.0 in the RNDT, record
  `r_puglia:7cefa029-daa7-45d6-a505-cc9b40d7a179`) is catalogued but not yet published as a
  download or a service.
- **Carta della Natura, Puglia** (ISPRA with ARPA Puglia): the SDI's GeoPackage
  (`sdi.isprambiente.it/download_ogc/cnat/CNAT_Habitat_Puglia.gpkg`, 143 MB, 41,530 polygons) is the
  1:50,000 edition of 2010–2013 (RNDT `ispra_rm:0016CNATHB_DT`, "Dato concesso con licenza
  CC-BY-4.0", with the same "previa richiesta" clause as Campania's record). Its CORINE Biotopes
  classes give the types (41.7511 Turkey oak 50,832 ha, 41.782 *Quercus trojana* 26,583, 45.31A
  holm oak 18,457, 41.737B downy oak 12,411, 42.84 Aleppo pine 10,416, 83.31 conifer plantations
  26,351, 41.18 beech 4,683, 41.9 chestnut 3,110), at a coarser scale and an older date than the
  Region's map. ISPRA's new 1:25,000 edition (Augello et al. 2025, 112 habitats, CC BY 4.0) is
  given out on request only, not scriptable.
- **Carta dei Tipi Forestali** (the Region's forest map, made with ARIF and the Università di
  Bari's DiSAAT, approved in 2022 and served on the SIT; its types are described in the
  Region's manual "I tipi forestali della Puglia: classificazioni e selvicoltura", 2025): 29,522
  polygons, 247,418 ha measured from the geometry (the manual's table gives 245,774 ha), minimum
  polygon 0.5 ha, the FRA 2000 forest definition that INFC also uses. Every polygon carries its
  INFC-style category (`cod_categ`: 3110 roverella, 3111 cerro, farnetto, fragno and vallonea,
  3114 faggete, 3117 leccete, 3120 Mediterranean pines…, plus 3140 wooded pastures, 321 grassland,
  322 temperate scrub and 323 macchia) and its type (`cod_tipo`: CE7 fragno of mesic soils, FA3
  the Gargano's "faggete abissali", PA6 Aleppo-pine reforestation of the inland Murge…). One layer
  gives both the broad groups and the forest types, read once (Liguria's and Abruzzo's pattern),
  with the Macedonian oak (fragno), found in Italy only here and in Basilicata, as its own type.
- **Carta Forestale d'Italia CFI2020** (CREA): shapefiles on request only, as for Marche, Umbria,
  Campania and Calabria. Not scriptable.

**Licence.** No licence is stated for the Carta dei Tipi Forestali: not on the SIT's viewer
(`webapps.sit.puglia.it/freewebapps/CartaTipiForestali`), its ArcGIS service (empty
`copyrightText`), the Region's forestry pages, the RNDT or `dati.puglia.it`. Italian public data
published without a licence are open by default (CAD, D.Lgs. 82/2005, art. 52 c. 2), with CC BY 4.0
as the reference licence of AgID's guidelines: the treatment Marche's REM vegetation map had. The
Region's other SIT datasets are IODL 2.0 (UDS 2011) and CC BY 4.0 (UDS 2023). The app credits
"Carta dei Tipi Forestali © Regione Puglia (ARIF, DiSAAT Università di Bari), CC BY 4.0". The
manual that describes the types is "tutti i diritti riservati"; only its facts (type names, areas)
are used here.

**Download.** `https://arcgisfed-sit.regione.puglia.it/hosted/rest/services/Operationals2/CartaTipiForestali/MapServer/0`,
paged as GeoJSON 2,000 features at a time (15 pages, about 40 s each). The viewer's own server
(`webapps.sit.puglia.it/arcgis/rest/services/Operationals2/CartaTipiForestali/MapServer/0`) serves
the same layer but caps a query at 1,000 features and has no GeoJSON output.

Class mapping (`puglia.yaml`, by `cod_tipo`), whole-map areas:

| types | group | habitat | ha |
|---|---|---|---|
| CE1–CE5, CE9 Turkey oak (with downy oak, holm oak, hop-hornbeam, hornbeam, farnetto, *Carpinus orientalis*); CE6, CE7 Macedonian oak (fragno); CE8 *Q. macrolepis*; QU1–QU5 downy oak | broadleaf | deciduous_oak | 31,913; 21,808; 6; 20,741 |
| LE1–LE8 holm oak; SU1 cork oak | broadleaf | evergreen_oak | 17,793; 78 |
| PA1–PA7 Aleppo pine (PA6 inland reforestation 12,575, PA1 coastal reforestation 3,499, natural stands on the coast and the gravine); BC1 other Mediterranean conifers | conifer | mediterranean_pine | 30,980; 1,124 |
| OS1–OS5 hop-hornbeam and hornbeam; BN1, BN2, BN4 maple, invasion woods, aspen | broadleaf | mixed_broadleaf | 5,611; 6,834 |
| FA1–FA4 beech | broadleaf | beech | 4,009 |
| BI1, BI2, BI5 willow, poplar, elm and ash galleries | broadleaf | riparian | 3,830 |
| PM1 black and laricio pine reforestation | conifer | mountain_pine | 1,400 |
| CA1 chestnut | broadleaf | chestnut | 698 |
| BC2 montane reforestation with other conifers | conifer | other_conifer | 283 |
| MM1–MM10 macchia and garighe; AB1, AB2 wild-olive formations (3119) | macchia | macchia | 32,520; 3,625 |
| AR1 blackthorn, AR2 broom, AR4 *Paliurus* pseudo-macchia; 3140 wooded pastures; BI3 tamarisk and shrub willows | transitional | transitional_woodland_shrub | 18,042; 3,714; 267 |

Left out: 321 grassland (39,486 ha), AR3 bracken (1,280 ha) and the tree plantations 2240–2242
(poplar, other broadleaves, conifers: 1,290 ha, arboricoltura da legno, outside INFC's bosco), as
Calabria leaves bracken and plantations out. **The wild-olive woods** (3119 "altri boschi di
latifoglie sempreverdi", 3,628 ha) are INFC forest but go to macchia: wild olive, lentisk and
*Paliurus* host none of the mapped species, and the map's largest macchia type (MM1, 28,563 ha) is
the same wild olive and lentisk. **The Aleppo-pine reforestation** (PA1, PA6: the Murge's
Mercadante and Alta Murgia plantings, the Gargano coast) stays `mediterranean_pine` with the
natural stands, where Campania filed its conifer plantations (black pine) as `mountain_pine`: the
map names the species. There is no mixed class.

**Forest area and INFC.**

| figure | ha | vs INFC 2015 bosco (142,349 ha) |
|---|---|---|
| Carta dei Tipi Forestali, 3110–3122 without 3119 | 147,441 | +3.6 % |
| **the grid** (the same, without BI3's 267 ha of shrub willow and tamarisk) | **147,110** | **+3.3 %** |
| Carta dei Tipi Forestali with 3119 wild-olive woods | 151,069 | +6.1 % |
| Uso del Suolo 2011, 311 + 312 + 313 | 125,963 | −11.5 % |
| Uso del Suolo 2011 with 314 wooded pastures | 142,987 | +0.4 % |
| Carta della Natura 2013, forest habitats (41.x, 45.x without 45.1, 44.61, 44.14, 42.84, 83.31, 16.29) | 162,116 | +13.9 % |

The Region's map comes within 4 % of INFC, and its forest classes follow INFC's categories. The
Uso del Suolo 2011 falls 11.5 % short, and lands on INFC's figure only if its wooded pastures (314)
are counted too. The Carta della Natura runs 14 % over: at 1:50,000 its polygons take in clearings
and scrub, and its conifer plantations (83.31, 26,351 ha) are half as large again as the Region's
reforestation (PA1, PA6, PM1, BC2 and 2242 together, 17,950 ha). **Its olive and carob woods**
(45.1, 13,284 ha, 11,160 of them in one Cagnano Varano complex) show how coarse it is: under them
the Region's map has scrub (3,582 ha), wild-olive woods (2,252), macchia (1,569) and grassland
(767), and only about 3,300 ha of hop-hornbeam, holm-oak, Turkey-oak and downy-oak wood.

## Woodland grid

Built 2026-09-28 (`uv run python -m api.grid.build --region puglia`, 4 min with the DEM tiles to
fetch).

- Cells 20,079; inside area 19,353 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 1,105** (5.5 % of the cells, the fewest of any region so far), in 68 of the 257
  comuni. By province: Foggia 813 (the Gargano and the Monti Dauni), Taranto 167, Bari 96,
  Barletta-Andria-Trani 14, Lecce 9, Brindisi 6. Puglia's forest is scattered: of its 147,110 ha,
  only 81,013 (55 %) lie in woodland cells; the rest is in cells less than half wooded (at a 0.3
  threshold 1,812 cells would qualify; below).
- **Forest area 147,110 ha vs INFC 2015 bosco 142,349 ha: +3.3 %** (Sources).
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 79 % of a cell's wooded area.
- Terrain: woodland elevation median 490 m (5th–95th percentile 111–859 m), highest cell mean
  1,050 m (Monti Dauni, Faeto and Biccari below Monte Cornacchia, black-pine reforestation),
  highest point in a woodland cell 1,146 m; slope median 11.9° (95th percentile 20.3°), the
  gentlest so far: the Murge are a plateau and the Gargano a karst upland. 66 woodland cells have
  no aspect; 21 slivers (no woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.76 (6.50–7.29, 5th–95th percentile), the
  least acid so far: limestone throughout. SoilGrids' WCS answered at once this time.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (Turkey oak, downy oak, fragno) | 47.3 % | 622 | 556 m |
| mediterranean_pine (Aleppo pine) | 17.4 % | 217 | 246 m |
| evergreen_oak (holm oak) | 11.4 % | 132 | 429 m |
| mixed_broadleaf (hop-hornbeam, hornbeam, invasion woods) | 8.2 % | 75 | 592 m |
| transitional_woodland_shrub | 6.0 % | 7 | |
| beech | 4.5 % | 39 | 749 m |
| macchia | 2.7 % | 1 | |
| mountain_pine (black-pine reforestation) | 1.1 % | 8 | 902 m |
| chestnut | 0.6 % | 0 | |
| riparian | 0.5 % | 3 | |
| other_conifer | 0.2 % | 1 | |

- The comuni with the most woodland cells: Monte Sant'Angelo (132), Vieste (110), San Marco in Lamis
  (101), Vico del Gargano (76), Martina Franca (65), San Nicandro Garganico (46), Mottola (39),
  Cagnano Varano (38), Peschici (37), Mattinata (30). Beech dominates 39 cells in the Foresta Umbra
  (Monte Sant'Angelo 19, Vieste 12, Vico del Gargano 7, Ischitella 1); the deciduous oaks lead in
  San Marco in Lamis (91), Monte Sant'Angelo (70), Vico del Gargano (50), Mottola (38) and Martina
  Franca (36, the fragno woods); Aleppo pine in Vieste (65), Peschici (27), Castellaneta (15), Vico
  del Gargano, Gravina in Puglia and Cassano delle Murge (the Mercadante reforestation); holm oak
  in Martina Franca (29), Monte Sant'Angelo (24), Mattinata and Vieste. Chestnut dominates no cell.
- The provinces of Lecce and Brindisi have 15 woodland cells (9 and 6): the Salento's woods
  (Rauccio, Santa Teresa, the coastal pinewoods) are mostly smaller than half a cell.

Spot checks (for a named wood, the comune's most wooded cell of that habitat):

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Foresta Umbra, beech | `1kmE4823N2098` | yes | 1.00 | beech 1.00 | 744 | 14 | 6.5 | Monte Sant'Angelo (FG) | Mattinata, 11.1 km |
| Foresta Umbra, centre | `1kmE4820N2099` | yes | 0.95 | beech 0.93, mountain_pine 0.06 | 805 | 9 | 6.4 | Monte Sant'Angelo (FG) | Vico del Gargano, 9.0 km |
| Gargano, Turkey and downy oak | `1kmE4793N2088` | yes | 1.00 | deciduous_oak 0.93, mixed_broadleaf 0.07 | 919 | 5 | 6.5 | San Marco in Lamis (FG) | Convento San Matteo, 3.4 km |
| Cagnano Varano | `1kmE4793N2100` | yes | 1.00 | deciduous_oak 0.71, mixed_broadleaf 0.18, evergreen_oak 0.11 | 551 | 14 | 6.6 | Cagnano Varano (FG) | Capoiale-Isola Varano, 7.0 km |
| Gargano coast, Aleppo pine | `1kmE4837N2101` | no (coastal sliver) | 1.00 | mediterranean_pine 1.00 | 18 | 14 | — | Vieste (FG) | Lama Le Canne, 2.5 km |
| Monti Dauni, Faeto | `1kmE4755N2039` | yes | 0.89 | deciduous_oak 0.78, mixed_broadleaf 0.17 | 748 | 15 | 6.6 | Faeto (FG) | Celle di San Vito, 0.8 km |
| Monte Cornacchia | `1kmE4753N2043` | yes | 0.72 | mountain_pine 0.43, deciduous_oak 0.40, mixed_broadleaf 0.14 | 1050 | 16 | 6.6 | Faeto (FG) | Faeto, 4.0 km |
| Murgia dei Trulli, fragno | `1kmE4931N1979` | yes | 0.96 | deciduous_oak 0.54, evergreen_oak 0.41 | 411 | 10 | 6.9 | Martina Franca (TA) | Crispiano, 5.8 km |
| Murgia dei Trulli, holm oak | `1kmE4932N1979` | yes | 1.00 | evergreen_oak 0.95, deciduous_oak 0.05 | 438 | 7 | 6.8 | Martina Franca (TA) | Casa di riposo San Raffaele, 5.2 km |
| Alta Murgia, Mercadante | `1kmE4887N2001` | yes | 0.99 | mediterranean_pine 1.00 | 427 | 5 | 6.9 | Cassano delle Murge (BA) | Borgo Incoronata-Lagogemolo, 1.3 km |
| Gioia del Colle | `1kmE4914N1995` | yes | 0.79 | deciduous_oak 0.99 | 359 | 4 | 7.3 | Gioia del Colle (BA) | Convento Madonna della Scala, 4.1 km |
| Arco ionico, Aleppo pine | `1kmE4909N1956` | yes | 0.98 | mediterranean_pine 1.00 | 6 | 2 | 7.1 | Castellaneta (TA) | Città del Catalano, 0.6 km |
| Salento, Lecce | `1kmE5027N1958` | yes | 0.67 | mediterranean_pine 0.85, macchia 0.15 | 10 | 2 | 7.1 | Lecce (LE) | Campo Verde, 0.8 km |
| San Domino, Tremiti | `1kmE4776N2129` | no | 0.26 | mediterranean_pine 1.00 | 30 | 9 | 7.2 | Isole Tremiti (FG) | Villaggio San Domino, 0.1 km |
| Bari (city) | `1kmE4899N2028` | no | 0.00 | — | 15 | 5 | — | Bari (BA) | Bari, 1.4 km |

Threshold sensitivity (recomputed from stored fractions):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 1,812 | 1,417 | **1,105** | 841 | 622 |

**DEM tiles over open sea.** Puglia's bbox asks for 1° GLO-30 tiles over the Adriatic and the
Ionian; the branch carries the fix cherry-picked from `region/campania` (`fix(grid): skip DEM tiles
the bucket lacks over open sea`), so the tiles the bucket lacks are skipped.

## Weather

- Points: 85 candidates on the 0.2° lattice, **63 on land**; 1,104 of the 1,105 woodland cells
  weighted. The one out of reach is the Tremiti's Aleppo-pine cell (`1kmE4775N2128`, San Domino):
  no land node lies within reach of the islands, so it is not scored (Known limitations).
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region puglia`,
  2026-09-28, 137 land nodes at 0.1° of 163, three 14-day windows of 2024). Cooling per km of
  height across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.63 | 6.01 | 4.45 | 5.39 | 4.5 | +0.89 |
  | temperature_2m_mean | 5.45 | 5.67 | 4.63 | 5.39 | 4.5 | +0.89 |
  | temperature_2m_min | 5.38 | 4.66 | 4.46 | 4.73 | 4.2 | +0.53 |
  | soil_temperature_0_to_7cm_mean | 4.71 | 5.31 | 3.69 | 4.53 | 3.7 | +0.83 |

  Every rate is within 1 °C/km of the national config, so **the national rates are kept**. The
  maxima and means cool faster with height than in Calabria (4.02 and 4.70), but the config's rates
  still downscale best, except Tmin at the coarser stride. Leave-out RMSE against the full 0.1°
  field:

  | leave-out RMSE | none | 6.5 °C/km | national config |
  |---|---|---|---|
  | Tmin, served lattice (0.2°, stride 2) | 0.656 | 0.479 | **0.446** |
  | Tmin, stride 3 (0.3°) | 0.953 | **0.646** | 0.686 |
  | Tmax, stride 2 | 0.631 | 0.627 | **0.548** |
  | Tmean, stride 2 | 0.540 | 0.397 | **0.323** |
  | soil, stride 2 | 0.626 | 0.602 | **0.516** |
  | soil, stride 3 | 0.765 | 0.668 | **0.614** |

  Daily rain RMSE on the leave-out is 0.87 mm at stride 2 and 0.94 mm at stride 3 whatever the
  rates, a smoother field than Calabria's (1.80 and 2.53) or Campania's (1.23 and 1.44).
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-17 (63 land nodes, 52 min on 2026-09-28), with snowfall
  from CDS's gridded ERA5-Land, whose national half-year files earlier lanes had cached. Open-Meteo's
  archive and the ECMWF IFS forecast fill the days after 2026-09-17 (`ingest update`, history
  complete to 2026-09-22; 2,804 Open-Meteo calls counted that day across the lanes by then).

### Rain scale: the Protezione Civile's gauge totals

Puglia's rain gauges belong to the Region's Protezione Civile (Centro Funzionale Decentrato, 163
rain gauges). Its daily data are not open: data not yet in the Annali are given on request, for a
fee to private users. But it publishes the **Annali idrologici, Parte I, dati storici**: for every
gauge, a workbook of monthly and annual totals from 1921 to 2020, with the gauge's coordinates and no
height (`protezionecivile.regione.puglia.it/annali-idrologici-parte-i-dati-storici`, 162 workbooks
in one zip). ARPA Puglia's open meteo data (CC BY 4.0 on `dati.puglia.it`) cover 24 urban and
air-quality stations for 2023–2024 only. So the check compares totals, not days: raw CDS rain
summed per month, read bilinearly from the land nodes at each gauge (weights renormalised; gauges
whose surrounding nodes are sea or were not fetched drop out), against the gauges' months,
keeping gauge-years with all twelve months and gauges with at least three such years in 2016–2020;
heights from the DEM at each gauge. 139 gauges pass; 42 of them lie within 5 km of a woodland cell.
The Region's site reserves its contents; the figures are used for this check only and not
republished.

| gauges | band | gauges | gauge mm/yr (median) | raw CDS / gauge (pooled) | scaled |
|---|---|---|---|---|---|
| all 139 | below 200 m | 66 | 607 | 1.07 | 1.02 |
| | 200–400 m | 27 | 628 | 1.04 | 1.07 |
| | 400–600 m | 22 | 740 | 0.92 | 1.01 |
| | 600–800 m | 15 | 805 | 0.90 | 1.05 |
| | 800 m and above | 9 | 896 | 0.93 | 1.14 |
| 42 near woodland | pooled | | | 0.91 | 1.00 |
| | below 200 m / 200–400 / 400–600 / 600–800 / 800+ | | | 1.06 / 0.99 / 0.87 / 0.86 / 0.80 | 1.01 / 1.04 / 0.97 / 1.00 / 0.98 |

The reanalysis is close to the gauges in Puglia: 1.00 pooled over all 139 gauges, a little wet on
the plains and the coast (1.07 below 200 m), a little dry in the hills. **`puglia.yaml` sets 0.93 +
0.34 per km, clamped at 900 m**, over `era5_land_cds` and `era5_seamless`: the least-squares fit
through the origin of gauge totals on model totals × (a + b × elevation) over the 42 near-woodland
gauges (a = 0.933, b = 0.340; leave-one-out 0.91–0.95 and 0.28–0.39). All 139 gauges give 0.93 +
0.23. The clamp stops it at the fit's highest gauge (Orto di Zolfo, 914 m, Monti Dauni).

| scale | factor at 200 / 500 / 800 m | near-woodland gauges scaled over gauge |
|---|---|---|
| **Puglia (42 near-woodland gauges, used)** | **1.00 / 1.10 / 1.20** | **1.00** |
| Puglia, all 139 gauges | 0.97 / 1.04 / 1.11 | 0.95 |
| Umbria (Servizio Idrografico) 0.89 + 0.33 | 0.96 / 1.06 / 1.15 | |
| Campania (agrometeo) 0.77 + 0.52 | 0.87 / 1.03 / 1.19 | |
| Calabria (station normals) 0.85 + 0.82 | 1.01 / 1.26 / 1.50 | |
| national (Tuscan gauges) 1.28 + 0.29 | 1.34 / 1.43 / 1.51 | 1.29 |
| none | 1 | 0.91 |

The scale fits totals, not single gauges: the wettest woodland gauges stay short. Bosco Umbra (779
m, in the Foresta Umbra) catches 1,129 mm a year against 720 raw and about 860 scaled; San Giovanni
Rotondo (610 m) 982 against 679 raw and 772 scaled; Faeto 1,010 against 734 and 883. The Gargano's
and the Monti Dauni's orographic rain is likely sharper than the 0.2° lattice can hold, as in
Calabria's Serre. Monte Sant'Angelo (792 m) and Sant'Agata di Puglia go the other way (raw 1.14).
The years are 2016–2020, the only overlap between the Annali and the CDS history.

## Sightings

`uv run python -m api.sightings.ingest fetch --region puglia` (2026-09-28): **10 GBIF records** for
the three groups over the bbox (5 *B. edulis*, 1 *B. aereus*, 2 *A. caesarea*, 2 *Cantharellus*),
all iNaturalist research-grade observations, and **none from iNaturalist** in the last two weeks.
After the quality filters (2 too imprecise: an ovolo at Monte Sant'Angelo with a 7.8 km radius, a
*B. edulis* in Campania with a 1,029 m radius) 8 are kept, and **none lands on a woodland cell**:

- one *B. edulis* of 28 June 2020 lies inside the bbox but in Campania (Bagnoli Irpino), off the
  grid;
- the others sit in cells that are not woodland: *B. edulis* at Gravina in Puglia (December 2023,
  farmland) and Ginosa (September 2019, near the coast), Roseto Valfortore (August 2022, a cell with
  29 % black-pine reforestation), *B. aereus* at Gravina in Puglia (May 2024, macchia), a
  chanterelle at Castellana Grotte (October 2018, a cell with 12 % downy oak) and at Monteleone di
  Puglia (December 2023), an ovolo at Rocchetta Sant'Antonio (November 2020, scrub).

So the store holds **0 usable presences**: the backtest has nothing to score, and validation rests
on the press contrasts (Validation).

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/puglia.md`; rules in
`api/src/api/config/species/puglia/` (31 new references; child card `region-puglia-species.md`).

- **Five keys kept, *B. pinophilus* dropped.** No Puglia source or record names it, and its hosts
  are missing: no fir, 1,401 ha of black-pine plantations on limestone, 699 ha of chestnut. *B.
  edulis* is kept for the Gargano beech on national evidence only.
- **The fragno is a deciduous oak**, and a full host for *B. aereus*, *B. reticulatus* and the
  ovolo (an ectomycorrhizal oak; the black porcino, the chanterelle and the ovolo are among the
  commonest species of the national downy-oak records). No Puglia source names a key under it.
- **Aleppo pine hosts none of the keys** (none of 822 Aleppo-pine records in ISPRA's Calabrian
  tables): `mediterranean_pine` drops to 0.1 for *B. aereus* and the chanterelles. The Gargano's
  beech becomes a full chanterelle host.
- **Seasons:** *B. reticulatus* opens on 15 April, full from 15 May; *B. aereus*'s lowland window
  runs from 15 May (full 15 June) to 10 January; the chanterelles' lowland window opens on 15 March
  (full 15 April) and their mountain window on 15 May. No altitude band moves up: Puglia's hosts are
  low (beech median 742 m, down to about 250 m in the karst hollows).
- **Weather rules, stoppers and growth clocks unchanged**: no Puglia study gives numbers. Three
  bulletins name dry north-easterly winds as what ends a flush; no rule reads wind (Validation).
- **Press contrasts** (`puglia/sanity.yaml`): 13, written before any Puglia score existed (10
  porcini, 1 ovoli, 2 gallinacci, 2018–2025), all on Funghi Magazine's national bulletins read
  through Wayback captures: Puglia's local press reports cardoncelli, not porcini seasons.
- The regional law on picking (L.R. Puglia 12/2003, in force) is in the ecology doc.
- **Hand-offs from the research, answered here.** Rain and gauges: the Weather section's gauge
  check. Fog on the Gargano: a known gap on *B. edulis*. Fragmentation: the grid keeps the national
  half-wooded mask (Woodland grid). Slope and sun-exposure stoppers are anchored on Tuscan
  percentiles; Puglia's woodland is gentler (median 11.9°, only 3 cells steeper than 25°).

## Validation

Scored 2016-03-18 to 2026-10-05 on 2026-09-28 (`onboard puglia --from score`; rules as committed,
rain scale 0.93 + 0.34 per km to 900 m): 1,105 woodland cells × every day per key, history without
factors (2 min), the served window 2026-09-22 to 2026-10-05 with them. The Tremiti cell has no
weather (3,847 cell-days without weather in the history). `onboard` ran the hold-out backtest and
the sanity check; the train-season backtest (`--seasons train --label onboard-train`) and the
group sanity runs (`--group ovoli --label onboard-ovoli`, `--group gallinacci --label
onboard-gallinacci`) were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **0**, against the 50 the parent plan asks for.
Hold-out 2024–2025: **0**. The backtest skips every season ("no sightings"); there is no AUC to
report.

**Sanity check** (`puglia/sanity.yaml`), each contrast read against its own group:

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Puglia early June 2020 > 2018 and 2021 | porcini | 0.386 | 0.277 | yes |
| Gargano and Monti Dauni early August 2020 > 2021, 2023, 2025 | porcini | 0.105 | 0.085 | yes |
| Gargano and Monti Dauni late August 2022 > 2023 | porcini | 0.392 | 0.205 | yes |
| Arco ionico early September 2021 > 2019 | porcini | 0.251 | 0.066 | yes |
| Gargano > Monti Dauni, September 2021 | porcini | 0.396 | 0.313 | yes |
| Gargano > Monti Dauni, 10–23 October 2020 | porcini | 0.602 | 0.753 | no |
| Murge > Salento, 10–23 October 2020 | porcini | 0.214 | 0.461 | no |
| Puglia autumn 2018 > 2021 and 2023 | porcini | 0.681 | 0.375 | yes |
| Murge, Taranto and Salento late October 2022 > 2021 and 2023 | porcini | 0.829 | 0.373 | yes |
| Puglia 2025: 14–26 August > 10 July–8 August | porcini | 0.136 | 0.014 | yes |
| Puglia 2025: 14–26 August > 10 July–8 August | ovoli | 0.094 | 0.006 | yes |
| Puglia 20 May–16 June 2023 > the same days in other years | gallinacci | 0.660 | 0.296 | yes |
| Puglia 8–22 December 2023 > the same days in other years | gallinacci | 0.681 | 0.649 | yes |

**11 of 13 hold** (porcini 8/10, ovoli 1/1, gallinacci 2/2); the `Data` section's "10/13" is the
default run, which scores all 13 on the porcini group. Both misses come from one bulletin of 23
October 2020: "maggior presenza di funghi autunnali in Gargano, rispetto al Sub-Appennino Dauno",
with no reason given, and the Salento "spesso sferzato dal vento, con nascite ridotte al lumicino"
while the Murge's porcini grew "là dove si mantiene l'umidità al riparo dal vento". The model reads
rain, temperature and drying, not wind, and scores the Monti Dauni and the Salento higher.
The December 2023 chanterelle contrast holds by a narrow margin (0.681 against 0.649) on the lowland
window's down-ramp, and the two August 2025 contrasts set 14–26 August against 10 July–8 August,
while the ovolo's and the porcini's seasons are ramping up, which favours them.

**The served window.** On 28 September 2026 porcini average 0.03 across Puglia's woodland cells,
ovoli 0.03 and gallinacci 0.12. Fifteen cells reach 0.6 for porcini, all in the Fortore corner of the
Monti Dauni (Celenza Valfortore 10, Pietramontecorvino 3, Carlantino 2), 12 of them deciduous oak,
at a median 456 m. The reanalysis gives the nodes about 21 mm of rain from 29 August to 22 September,
against 15–141 mm in the same days of past years (median about 45): Puglia is dry.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-28 (`deploy/rsync-region-data.sh puglia`, 190
files, 97 MB, no redeploy). The server serves a region only when its YAML is in the deployed code
and its stores are on disk, so they stay inert until `main` with `config/regions/puglia.yaml` is
deployed by the rail's "Deploy pulled main" step (with the daily job, which brings the weather and
scores up to that day). Then check:

- [ ] `https://mappafunghi.app/puglia` and `/puglia/porcini`, `/puglia/ovoli`, `/puglia/gallinacci`
  show real scores for today (not fixtures), and a tapped cell's "why this score" names Apulian
  habitats (beech in the Foresta Umbra, Turkey oak at San Marco in Lamis, the fragno woods at
  Martina Franca as deciduous oak, Aleppo pine at Castellaneta).
- [ ] `https://api.mappafunghi.app/regions` lists `puglia`; the hub `/` lists it and colours it from
  `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Puglia URLs (built from the registry; the
  local build has them).
- [ ] Lighthouse SEO is 100 on `/puglia` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Puglia", description, canonical, og image `og/puglia.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1447).
- [ ] `/credits` shows "Regione Puglia — Carta dei Tipi Forestali (ARIF, Università di Bari)".
- [ ] The next morning's daily job has a `region_done` line for `puglia`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **The forest map's licence is unstated** (Sources): used as open by default, as Marche's REM
  map was; a decision on the card asks the human whether to keep it or switch to the Uso del Suolo
  2011 with the Carta della Natura's types.
- **Few woodland cells.** Puglia's forest is scattered: 1,105 cells pass the national half-wooded
  mask, and the provinces of Lecce and Brindisi keep 15 of them. Many fragno woods and the Salento's
  relict woods (Rauccio, Santa Teresa) are smaller than half a cell and are not scored. A lower
  threshold would be a national change (Woodland grid, threshold sensitivity).
- **The Tremiti are not scored.** Their one woodland cell (San Domino's Aleppo pine) has no land
  weather node within reach.
- **Rain scale from monthly totals of 2016–2020**, not daily gauges, and the wettest woodland
  gauges stay short after scaling: Bosco Umbra by 24 %, San Giovanni Rotondo by 21 %, Faeto by 13 %
  (Weather). The
  Centro Funzionale's daily data would allow a proper daily check; they are given on request.
- **No usable sightings** (Sightings): the backtest scores nothing, and validation rests on the press
  contrasts, all on one magazine's bulletins.
- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point.
  Puglia's bbox takes in Irpinia (Bagnoli Irpino, Bisaccia, Andretta), the Vulture and the Materano
  (Matera, Montescaglioso) and Molise's coast at Termoli, which belong to Campania, Basilicata and
  Molise. Card `fix-region-lookup-by-boundary.md`.
- **The DEM sea-tile fix** is cherry-picked from `region/campania`; the branches carry the same
  commit content and merge cleanly in either order.

## Data

- cells: 20079
- woodland cells: 1105
- INFC deviation: +3.3% (grid 147,110 ha vs 142,349 ha) — within ±10 %
- weather nodes: 63
- years stored: 2016–2026 (11 years)
- sightings kept: 0 (8 pass the filters, none on a woodland cell)
- sanity contrasts: 10/13 passed

