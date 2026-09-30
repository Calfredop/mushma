# sardegna

Region #19 of the full-Italy rollout (card `region-sardegna.md`). API id `sardegna`, web slug
`/sardegna`, ISTAT COD_REG 20, Wikidata Q1462. Config: `api/src/api/config/regions/sardegna.yaml`.
The second island, after Sicily, and the most wooded region of Italy by INFC's total: holm-oak
and cork-oak woods over most of it, from the Gallura's granite and the Alà plateau to the
Supramonte's limestone and the Sulcis-Iglesiente; downy oak on the Barbagia, the Marghine and the
Gennargentu's flanks; post-war pine plantations on every massif; wild-olive woods on the hills.
There is **no beech, no silver fir and no spruce** on the island.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | ISPRA and Regione Sardegna, **Carta della Natura della Regione Sardegna**, carta degli habitat 1:50,000, 2011 (`ispra_cnat_sardegna`) | CC BY 4.0 | one GeoPackage on ISPRA's SDI, 27,261 polygons, 93 CORINE Biotopes habitats |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| rain check | ARPAS daily station data 2016–2022 | CC BY-NC-ND | used for the gauge check only, never served (Weather) |
| sightings | GBIF (bbox), iNaturalist place 13071 "Sardegna, IT" | per record | counts per cell only |

**What was checked (2026-09-30).**

- **Regione Sardegna, Carta dell'uso del suolo 2008** (1:25,000, CLC legend to the 5th level,
  photo-interpreted by Agristudio on the 2003–2006 imagery; RNDT record `R_SARDEG:TVWIX`), the
  candidate the card named. It is open: the record gives **CC BY 4.0** and "no limitations to
  public access", and the geoportale serves the polygons as one zip
  (`webgis.regione.sardegna.it/scaricocartografiaETL/usoSuolo/usoSuolo2008/usoSuolo2008Areali.zip`,
  158,023 polygons, Monte Mario / Gauss-Boaga West). But its forest has **no types** beyond two
  plantation classes: 3111 "bosco di latifoglie" (353,141 ha) lumps the holm oak, the mixed cork
  oak and the downy oak; only pure, tended cork stands (31122, 80,487 ha) and chestnut orchards
  (31123, 772 ha) are split out; 3121 "bosco di conifere" (36,915 ha) and 313 mixed (12,411 ha).
  Its woods need **20 % tree cover** (the legend's change to CLC, with three density classes), so
  the sparser holm-oak and cork woods fall into macchia (3231, 336,398 ha) or are cork pasture
  (2413, "pascoli e seminativi arborati con copertura della sughera dal 5 al 25 %"). Its forest
  classes hold **504,919 ha, −19.4 % against INFC 2015** (bosco 626,140 ha).
- **Regione Sardegna, DBGT 10k 2022, strato BOSCO** (the geotopographic database, 367,021
  polygons, RDN2008 / UTM 32N): the same legend carried into the 1:10,000 database (its `UDS`
  column is the 2008 code), with an `Essenze` column that says only "essenze latifoglie", "leccio
  e sughera", "castagno" or "non conosciuto" (59 % of the area). No forest types.
- **Carta forestale del Distretto Arci-Grighine** (1:10,000, 2010, Del Favero's typology): the
  pilot of the 25 forest districts, 55,000 ha around Monte Arci only. No regional forest-type map
  exists; the district plans that followed are not published as data.
- **CLC 2018 IV level** (ISPRA's ArcGIS layer, clipped to the ISTAT boundary): 402,860 ha of
  forest, **−35.7 %** (3111 holm and cork oak 293,358 ha, 3121 Mediterranean pines 59,203 ha,
  3112 deciduous oak 31,182 ha, 3131–3132 mixed 13,618 ha, 3114 chestnut 1,451 ha; no 3122).
- **ISPRA Carta della Natura, Regione Sardegna, 1:50,000** (Camarda I., Carta L., Laureti L.,
  Angelini P., Brunu A., Brundu G. 2011; report Camarda et al., ISPRA Rapporti 222/2015): drawn by
  the University of Sassari for ISPRA and the Region, finished in 2010, photo-interpreted on the
  IT2000 orthophotos (1998–99) and Landsat IMAGE2000 with field checks. The GeoPackage
  (`sdi.isprambiente.it/download_ogc/cnat/CNAT_Habitat_Sardegna.gpkg`, dated 2022-08-01,
  EPSG:25832; it also holds a Valle d'Aosta layer, so the source names its layer) carries the
  Sardinian forest habitats the national legend adds: 45.317 **Leccete sarde**, 45.323 supra-
  Mediterranean holm oak of Sardinia, 45.21 cork oak, 41.72 **Querceti a roverella della
  Sardegna**, 45.1 wild olive and carob, 83.31 conifer plantations, 83.322 eucalyptus, and 84.6
  **Pascolo alberato in Sardegna (dehesa)**. ISPRA's data sheet (RNDT `ispra_rm:0017CNATHB_DT`)
  gives **CC BY 4.0**, with the "previa richiesta" wording Campania's and Molise's records carry.
  Its forest classes hold **573,146 ha, −8.5 %** against INFC.

**Decision: the Carta della Natura for both layers**, as Campania, Calabria and Molise use theirs.
It is the only open map of Sardinia's woodland with forest types, and it lands within ±10 % of
INFC where the Region's own open land-use map does not (−19.4 %). The two maps disagree more than
their totals say: rasterized at 50 m, 327,000 ha are forest on both, 247,000 ha only on the
Carta della Natura (105,000 of them macchia on the land-use map, 34,000 its 3242 reforestation
sites, 15,000 pasture) and 178,000 ha only on the land-use map (64,000 of them holm-oak or cork
"matorral" and macchia on the Carta della Natura, 31,000 dehesa). They were drawn ten years and
two scales apart, and Sardinia's holm oak runs from high forest to tall macchia without a break.
The price is the older imagery (1998–99) and the coarser scale: the chestnut orchards of the
Barbagia (Aritzo, Desulo, Tonara, Belvì) are mostly lumped into the downy oak around them (Woodland
grid). The credit reads "Carta della Natura della Regione Sardegna © ISPRA, Regione Sardegna, CC BY
4.0" (`sources.yaml`, and `web/src/credits.ts`).

Class mapping (`sardegna.yaml`, one layer gives both), whole-map areas:

| `codice_corine` | group | habitat | ha |
|---|---|---|---|
| 45.317 Sardinian holm oak, 45.323 supra-Mediterranean holm oak of Sardinia | broadleaf | evergreen_oak | 195,034; 22,574 |
| 45.21 cork oak | broadleaf | evergreen_oak | 103,597 |
| 41.732 Mediterranean downy oak, 41.72 downy oak of Sardinia (*Quercus pubescens* s.l.: *Q. ichnusae*, *Q. congesta*, *Q. virgiliana*) | broadleaf | deciduous_oak | 32,986; 31,205 |
| 45.1 wild olive and carob woods | broadleaf | mixed_broadleaf | 57,038 |
| 41.81 hop-hornbeam, 45.8 holly, 41.D1 aspen and birch | broadleaf | mixed_broadleaf | 208; 53; 4 |
| 83.322 eucalyptus plantations | broadleaf | exotic_broadleaf | 21,991 |
| 44.63 narrow-leaved ash, 44.61 poplar, 44.13 willow, 44.91 alder and willow carr | broadleaf | riparian | 6,759 |
| 41.9 chestnut | broadleaf | chestnut | 971 |
| 83.31 conifer plantations | conifer | mediterranean_pine | 94,522 |
| 16.29 wooded dunes, 42.84 Aleppo pine, 42.83 stone pine, 42.82 maritime pine | conifer | mediterranean_pine | 3,489; 1,183; 883; 103 |
| 42.A7 yew woods | conifer | other_conifer | 100 |
| 32.3 and 32.4 meso-Mediterranean macchia and garrigue, 32.211 low wild-olive and lentisk macchia, 32.11–32.14 and 32.18 matorral (evergreen oak, wild olive, juniper, pine, laurel), 32.212–32.24 other macchia, 16.27 and 16.28 dune scrub | macchia | macchia | 636,519 in all |
| 44.81 tamarisk and oleander, 44.12 willow scrub, 32.26 thermo-Mediterranean broom, 31.81 deciduous scrub, 31.844 and 31.845 broom, 31.8A bramble | transitional | transitional_woodland_shrub | 11,345 in all |
| **left out:** 84.6 dehesa (112,668), 31.75 the Gennargentu's spiny oro-Mediterranean heath (13,682), 83.325 broadleaf plantations (857), 32.217 coastal *Helichrysum* garrigue (1,765), 32.23 Ampelodesmos steppe (1,544), 33.2 and 33.9 phrygana, 31.43 prostrate juniper, 31.863 bracken, grassland and rock | — | — | |

- **The conifer plantations are Mediterranean pine.** 83.31 (94,522 ha) is the post-war
  reforestation of every massif (the Limbara, the Gennargentu, Monte Lerno, Marganai, the Sette
  Fratelli, Monte Arci) and the coast: maritime, Aleppo and stone pine for the most part, with black
  pine and cypress on the mountains. Where the Carta della Natura has 83.31 and CLC IV has conifer
  forest, CLC files 37,781 ha as 3121 Mediterranean pines and 1,455 ha as 3125 exotic conifers, and
  **has no 3122 (black pine) anywhere in Sardinia**; the grid gives a code one habitat, so all of it
  is `mediterranean_pine`, as CLC files it.
- **The wild-olive and carob woods (45.1) are forest**, as INFC counts them ("altri boschi di
  latifoglie sempreverdi"), under `mixed_broadleaf`: they are not oak, and no rule should read
  them as holm oak. They sit low (median cell 273 m: Paulilatino, Carbonia, Muravera).
- **The dehesa (84.6, 112,668 ha) is left out**, as CLC's agroforestry areas (244) are everywhere:
  wooded pasture of cork and downy oak, 5–25 % cover on the land-use map, grazed. Counting it would
  take the forest to +9.5 % of INFC but make open pasture "woodland". It is the Sardinian ground
  closest to the Spanish dehesas where *B. aereus* is picked (species doc); it stays a known
  limitation.
- The holm-oak and cork "matorral" (32.11, 117,958 ha) is macchia, as Calabria files it: tall
  evergreen-oak scrub, not counted towards the mask but kept as a habitat fraction the rules read.

## Config

- **Boundary.** ISTAT COD_REG 20; bbox `[8.13, 38.85, 9.83, 41.32]`, the ISTAT 2025 boundary's
  extent (8.1331, 38.8592, 9.8284, 41.3133) rounded outward to 0.01°: Sant'Antioco and San Pietro
  to the south-west, the Asinara to the north-west, La Maddalena to the north-east. It stops short
  of Corsica (Bonifacio, 41.39° N) and touches no other served region's bbox. Inside area 24,127
  km².
- **Forest.** The Carta della Natura for groups and types (Sources above).
- **Sightings.** iNaturalist place 13071, resolved by name ("Sardegna, IT", admin level 10) on
  2026-09-30.
- **Weather.** Fitted lapse rates for the minimum and the topsoil (Weather below).
- **Model.** A rain scale from the ARPAS gauges, 1.00 + 0.34 per km (Weather below): the gauge
  check asks for it, since the national scale would make Sardinia's rain 20–25 % too wet. No other
  override.

## Woodland grid

Built 2026-09-30 (`uv run python -m api.grid.build --region sardegna`, 2 min 15 s, most of it
the DEM).

- Cells 25,026; inside area 24,127 km² (the generalised ISTAT 2025 boundary, small islands
  included).
- **Woodland cells 5,141** (20.5 % of the cells, the highest share so far), in 262 of the 377
  comuni. By province: Nuoro 1,948, Sassari 1,310, Sud Sardegna 1,082, Oristano 403, Cagliari
  398. Most wooded comuni: Baunei (119 cells), Bitti (111), Orgosolo (109), Buddusò (103), Alà dei
  Sardi (95), Sinnai (85), Pula (77), Villagrande Strisaili (71), Urzulei (69), Ulassai (66),
  Aritzo (59), Nuoro (58).
- **Forest area 573,104 ha vs INFC 2015 bosco 626,140 ha: −8.5 %**, within ±10 %. INFC's own
  categories (as SardegnaForeste reports them, 2025): holm oak 255,463 ha (the map 217,608),
  cork oak 152,755 (103,597, plus cork in the dehesa left out), deciduous oaks 87,780 (64,191),
  Mediterranean pines 34,633 (the map's pines and plantations 100,258: INFC files many plantations
  under other conifer categories or arboriculture, 25,885 ha).
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 86 % of a cell's wooded area.
- Terrain: woodland elevation median **517 m** (5th–95th percentile 136–967 m), highest cell mean
  1,384 m, highest point in a woodland cell 1,557 m: Sardinia's woods stop low, the Gennargentu's
  top is heath and pasture. Slope median 16.9°, 9.5 % of woodland cells above 25°; 169 have no
  aspect. 18 slivers (no woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.56 (6.14–7.06, 5th–95th percentile).

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| evergreen_oak (holm and cork oak) | 53.7 % | 3,097 | 511 m |
| mediterranean_pine (plantations, coastal pine) | 15.5 % | 857 | 567 m |
| macchia | 11.5 % | 56 | 522 m |
| deciduous_oak (downy oak s.l.) | 9.9 % | 585 | 726 m |
| mixed_broadleaf (wild olive and carob) | 7.2 % | 463 | 273 m |
| exotic_broadleaf (eucalyptus) | 1.3 % | 76 | 138 m |
| riparian | 0.4 % | — | |
| transitional_woodland_shrub | 0.3 % | — | |
| chestnut | 0.2 % | 7 | 1,005 m |
| other_conifer (yew) | < 0.1 % | — | |

- The evergreen oaks dominate most cells in Baunei (112), Bitti, Pula, Orgosolo, Urzulei, Sinnai,
  Alà dei Sardi, Buddusò, Santadi and Dorgali; the downy oaks in Fonni (44), Bonorva, Desulo,
  Macomer, Bono, Aritzo, Bolotana, Tonara and Mamoiada; the pine plantations in Alà dei Sardi,
  Buddusò, Bitti, Alghero, Seui, Aritzo, Pattada, Orgosolo, Oschiri and Arzana; the wild olive in
  Paulilatino (52), Carbonia, Muravera, Orotelli and Lodè; eucalyptus in Teulada, Siliqua and on
  the Arborea reclamation.
- **Chestnut is almost missing**: 971 ha on the map, 7 cells where it dominates (Desulo 5, Tonara,
  Santu Lussurgiu). The Barbagia's chestnut orchards are small and at 1:50,000 fall inside the
  downy oak: the cell above Aritzo reads downy oak 0.94, chestnut 0.02. CLC IV has 1,451 ha, the
  land-use map 772 ha of orchards.

Spot checks:

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Monte Ortobene | `1kmE4266N1914` | yes | 1.00 | evergreen_oak 1.00 | 765 | 14 | 6.4 | Nuoro (NU) | Nostra Signora de Su Monte, 0.9 km |
| Aritzo | `1kmE4251N1873` | yes | 0.83 | deciduous_oak 0.94, mediterranean_pine 0.04, chestnut 0.02 | 812 | 16 | 6.5 | Aritzo (NU) | Aritzo, 0.5 km |
| Alà dei Sardi | `1kmE4264N1950` | yes | 0.61 | deciduous_oak 0.99, evergreen_oak 0.01 | 640 | 9 | 6.5 | Alà dei Sardi (SS) | Alà dei Sardi, 0.6 km |
| Foresta di Burgos | `1kmE4233N1923` | yes | 0.67 | evergreen_oak 0.79, mediterranean_pine 0.13, deciduous_oak 0.09 | 888 | 11 | 6.3 | Burgos (SS) | Burgos, 2.2 km |
| Monte Limbara | `1kmE4249N1973` | yes | 0.64 | mediterranean_pine 1.00 | 1061 | 12 | 6.2 | Tempio Pausania (SS) | Tempio Pausania, 6.5 km |
| Calangianus | `1kmE4252N1980` | no | 0.11 | evergreen_oak 1.00 (cork, around the town) | 512 | 8 | 6.5 | Calangianus (SS) | Calangianus, 0.3 km |
| Monte Arci | `1kmE4211N1855` | yes | 1.00 | evergreen_oak 1.00 | 560 | 22 | 6.2 | Marrubiu (OR) | Alle Sorgenti, 3.4 km |
| Sette Fratelli | `1kmE4269N1799` | yes | 1.00 | mediterranean_pine 0.64, evergreen_oak 0.36 | 637 | 17 | 6.5 | Sinnai (CA) | Monte Cresia, 1.6 km |
| Monte Linas | `1kmE4202N1817` | no | 0.35 | evergreen_oak 0.99 | 982 | 29 | 6.3 | Gonnosfanadiga (SU) | Gonnosfanadiga, 6.7 km |
| Supramonte di Orgosolo | `1kmE4272N1893` | no | 0.37 | macchia 0.62, evergreen_oak 0.32 | 935 | 16 | 6.4 | Orgosolo (NU) | Urzulei, 7.9 km |
| Montiferru above Santu Lussurgiu | `1kmE4202N1893` | no | 0.21 | mediterranean_pine 0.87, macchia 0.13 | 809 | 15 | 6.1 | Santu Lussurgiu (OR) | Santu Lussurgiu, 3.7 km |
| Is Arenas, Narbolia | `1kmE4190N1887` | no | 0.32 | macchia 0.51, mediterranean_pine 0.49 | 5 | 2 | — | Narbolia (OR) | Torre del Pozzo, 2.0 km |
| Punta La Marmora, Gennargentu | `1kmE4263N1877` | no | 0.01 | macchia 0.82, deciduous_oak 0.18 | 1479 | 35 | 6.5 | Arzana (NU) | Desulo, 9.2 km |
| Cagliari (city) | `1kmE4243N1792` | no | 0.00 | — | 15 | 5 | — | Cagliari (CA) | Villaggio Pescatori, 1.6 km |

Threshold sensitivity (recomputed from stored fractions, with the 0.25 km² floor):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 7,426 | 6,197 | **5,140** | 4,176 | 3,251 |

The shared 0.5 rule is kept.

## Weather

- Points: 106 candidates on the 0.2° lattice, **61 on land**; all 5,141 woodland cells weighted,
  none out of reach (La Maddalena, San Pietro and Sant'Antioco hold no woodland cells).
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region sardegna`,
  2026-09-30, 242 land nodes at 0.1° of 314, three 14-day windows of 2024). Cooling per km of
  height across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.32 | −1.41 | 3.81 | 3.77 | 4.5 | −0.73 |
  | temperature_2m_mean | 5.86 | 1.52 | 4.94 | 4.75 | 4.5 | +0.25 |
  | temperature_2m_min | 6.36 | 4.35 | 5.30 | 5.26 | 4.2 | **+1.06** |
  | soil_temperature_0_to_7cm_mean | 4.86 | 4.43 | 4.95 | 4.72 | 3.7 | **+1.02** |

  The minimum and the topsoil cool more than 1 °C/km faster with height than the national rates,
  in every month, so **`sardegna.yaml` sets 5.3 (min) and 4.7 (soil)**; the maximum and the mean
  are within 1 °C/km and keep 4.5. July's maximum warms with height: the Campidano and the
  interior plains bake hotter than the breezy uplands at noon. The fitted rates downscale a little
  better than the national ones. Leave-out RMSE against the full 0.1° field:

  | leave-out RMSE | none | 6.5 °C/km | national config | **Sardinia (5.3 min, 4.7 soil)** |
  |---|---|---|---|---|
  | Tmin, served lattice (0.2°, stride 2) | 0.627 | 0.357 | 0.374 | **0.351** |
  | Tmin, stride 3 (0.3°) | 0.755 | 0.493 | 0.456 | **0.452** |
  | soil, stride 2 | 0.741 | 0.643 | 0.620 | **0.616** |
  | soil, stride 3 | 0.976 | 0.744 | 0.751 | **0.730** |
  | Tmax, stride 2 | 0.525 | 0.610 | **0.516** | (national) |
  | Tmean, stride 2 | 0.485 | 0.348 | **0.284** | (national) |

  Daily rain RMSE on the leave-out is 1.04 mm at stride 2 and 1.11 mm at stride 3 whatever the
  rates, the lowest of the southern regions (Sicily 1.21 and 1.81).

- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-19 (61 nodes, 57 min on 2026-09-30), with snowfall from CDS's gridded
  ERA5-Land, whose national half-year files earlier lanes had already cached. Open-Meteo's archive
  and the ECMWF IFS forecast fill the days after (`api.weather.ingest update --region sardegna`,
  history complete to 2026-09-24; 2,241 Open-Meteo calls counted that day across the lanes when it
  ran).

### Rain scale: the ARPAS gauges

ARPAS publishes its stations' daily data as **one table a year on its ArcGIS Online organisation**
("Rete meteo ARPAS 2016-2023"): 2016–2022, about 300 stations of the ReteUnica and the
ReteFiduciaria at 0–1,372 m, each row with the station's code, name, height and position and the
day's rain (`PCG`, mm), unvalidated. The 2021 item states **CC BY-NC-ND 3.0 IT**, as does the SIRA
portal that serves the same network in real time, and gives its times in UTC. The data are used
here only to fit and check the rain scale, never served or redistributed, which the non-commercial,
no-derivatives licence allows. Coverage grows through the years (119 rain stations in 2016, 300
from 2019). One day at La Maddalena reads −8,920.4 mm and is dropped; the other extremes are real
storms (10 October 2018 on the south-east, 469 mm at Uta; 28 November 2020 on the Nuorese, 501 mm
at Oliena and the Bitti flood). The network is wired into `GAUGE_NETWORKS` (`api.weather.arpas`,
commit `feat(checks): ARPAS rain gauges for Sardinia's rain check`).

Two checks over 2018–2022 (1,826 days):

- **Every station** (a one-off script): the stored raw CDS rain read bilinearly at each station's
  position from the land nodes (weights renormalised), re-cut into UTC days, against its days; 272
  stations with 80 % of the days. Median daily correlation 0.71–0.73 in every band.
- **Woodland gauges** (`uv run python -m api.weather.checks gauges --region sardegna --start
  2018-01-01 --end 2022-12-31`): the 35 ARPAS stations inside woodland cells (9–1,261 m: Alà dei
  Sardi, Desulo, Aritzo, Fonni, Orgosolo Montes, Monte Rasu above Bono, Pula Is Cannoneris,
  Castiadas Minni Minni…), downscaled as the model does: pooled ratio 0.79 raw (1.02 below 400 m,
  0.76 at 400–800 m, 0.75 above 800 m) and **0.97 scaled**, median daily correlation 0.71, wet
  3-day windows caught 69 % of the time with 6 % false alarms.

| band | stations | raw CDS / gauge rain (pooled) | scaled / gauge | median daily correlation |
|---|---|---|---|---|
| below 200 m | 125 | 0.95 | 0.97 | 0.71 |
| 200–400 m | 56 | 0.93 | 1.03 | 0.73 |
| 400–800 m | 65 | 0.81 | 0.97 | 0.72 |
| 800 m and above | 26 | 0.74 | 1.00 | 0.71 |
| all | 272 | 0.88 (median station 0.90) | | |
| woodland gauges (downscaled) | 35 | 0.79 | 0.97 | 0.71 |

Unlike Sicily, and like the Apennine regions, the reanalysis is **drier the higher the gauge**, and
its bias is spatial too: dry on the south-east's granite mountains, whose relief the 0.1° model
smooths away (Pula Is Cannoneris 0.48, Sinnai Serpeddì 0.51, Maracalagonis 0.55, Castiadas Minni
Minni 0.57, Burcei 0.58), wet on the north-west coast (Sorso 1.45, Bosa 1.37, Castelsardo 1.33).
Like everywhere, it rains too often: 1 mm or more on 28 % of days against the gauges' 21 %.

**`sardegna.yaml` sets 1.00 + 0.34 per km** over `era5_land_cds` and `era5_seamless` (the
national clamp at 1,700 m kept; the highest woodland point is 1,557 m): the least-squares fit
through the origin of gauge totals on model totals × (a + b × elevation) over the 272 stations,
a = 1.002, b = 0.342. It is robust: leave-one-out slopes 0.33–0.35; the 141 stations whole over
2016–2022 give 1.00 + 0.32; those at 200 m and above 0.97 + 0.38, at 400 m and above 1.07 + 0.26;
the 35 woodland gauges alone 1.00 + 0.37.

| scale | factor at 200 / 500 / 800 / 1,200 m |
|---|---|
| **Sardinia (272 ARPAS gauges, used)** | **1.07 / 1.17 / 1.27 / 1.41** |
| Sicily (94 SIAS gauges) 0.88 + 0.10 | 0.90 / 0.93 / 0.96 / 1.00 |
| Campania (agrometeo) 0.77 + 0.52 | 0.87 / 1.03 / 1.19 / 1.39 |
| national (Tuscan gauges) 1.28 + 0.29 | 1.34 / 1.43 / 1.51 / 1.63 |

The national scale would make Sardinia's rain 20–25 % too wet on these gauges. The fit scales
totals, not timing; since the porcini's 30-day rain is a share of each cell's own (scaled) normal,
the choice matters most for the absolute rain ramps of the ovolo and the chanterelles.

## Sightings

`uv run python -m api.sightings.ingest fetch --region sardegna` (2026-09-30): **62 GBIF records**
for the three groups over the bbox (3 *B. edulis*, 25 *B. aereus*, 4 *B. reticulatus*, no *B.
pinophilus*, 18 *A. caesarea*, 16 *Cantharellus*) and **none from iNaturalist** in the last two
weeks. After the quality filters (6 excluded by basis of record, 20 too imprecise; 18 give no
uncertainty and pass) 36 are kept, and **19 land on Sardinia's woodland cells**, none obscured,
all but one in evergreen-oak cells:

| group | before 2016 | train seasons 2016–2023 | hold-out 2024–2025 | where |
|---|---|---|---|---|
| porcini | 2 | 3 cell-days | 2 | the Gallura's cork oak (Calangianus, 24 September 2016; Sant'Antonio di Gallura, 14 November 2019; Tempio Pausania, 13 September 2024), Monte Arci (Santa Giusta, 12 November 2023), the Iglesiente (Iglesias, 24 November 2025) |
| ovoli | 2 | 4 | 1 | the Gallura (Sant'Antonio di Gallura, 25 May 2020; Calangianus, 4 November 2022), Alà dei Sardi (15 October 2018), the Sette Fratelli (Sinnai, 30 September 2020), Uta (19 November 2025) |
| gallinacci | 1 | 1 | 2 (3 records) | the Montiferru (Scano di Montiferro, 11 May 2016), the Marganai (Domusnovas, 24 November 2025), the Sarcidano (Nurallao, 27 November 2025) |

The records before 2016 (porcini at Sinnai in September 1997 and Calangianus in October 1999, ovoli
at Tempio in November 2000 and Sinnai in October 2006, chanterelles at Tempio in November 2011)
predate the history. Most come from a handful of recorders on the Gallura's granite and the Sette
Fratelli: the few Sardinian records are a map of where they walk, not of where the woods are.

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/sardegna.md`; rules in
`api/src/api/config/species/sardegna/` (97 new references; child card `region-sardegna-species.md`).

- **All three groups and five keys kept; *B. pinophilus* dropped**: no Sardinian record on
  iNaturalist or GBIF, no page in the forestry agency's catalogue, and none of its hosts (beech,
  fir, natural mountain pine) on the island; only readers' reports in Funghi Magazine, one of whose
  own bulletins says the climate keeps it off. Puglia is the precedent. **No regional picking law**:
  the national L. 352/1993 and municipal ordinances apply (the 2020 bill, PL 170, lapsed).
- **No porcini census exists.** The evidence is the forestry agency's pages, a review of Sardinian
  mycology, the cork-oak and plantation surveys, 57 iNaturalist records, about 140 Funghi Magazine
  bulletins and about 75 local-press articles: the season evidence is mostly folklore, the hosts
  plausible.
- ***B. aereus* leads** ("abbondante nei boschi della Sardegna"; 18 of the 25 porcini records),
  *B. reticulatus* second, *B. edulis* rare.
- **Seasons:** *B. aereus*'s lower window opens on 1 April and is full from 1 May to 10 January (a
  spring flush of "porcini neri" in every year Funghi Magazine covers, 2018–2025), its upper one
  from 15 May to 30 November with the handover at 800–1,000 m; *B. reticulatus* 15 April to 20
  December; *B. edulis* from 1 July, full from 1 September to 10 January; the ovolo 15 May to 10
  December, as in Sicily; the chanterelles into February in the lowlands. The summer gap is left to
  the heat, drought and drying rules.
- **Hosts:** holm and cork oak full for *B. aereus*, *B. reticulatus* and the ovolo; *B. edulis*
  0.3 there. The macchia (three fifths of it evergreen-oak matorral and *Erica*-*Arbutus* macchia)
  is secondary for *B. aereus* and the ovolo (0.6), marginal for *B. reticulatus* (0.3) and *B.
  edulis* (0.1). The pine plantations 0.1 for every porcino but *B. edulis* (0.3, the Limbara's
  montane plantations); the wild-olive woods and the tamarisk thickets 0.1 for every key; the
  eucalyptus 0. The chestnut, hidden in the map's downy oak, is carried by `deciduous_oak`.
- **Altitude bands follow the oak belt**: *B. aereus* full to 1,100 m, the ovolo to 1,000 m, *B.
  reticulatus* to 1,200 m; *B. edulis* and the chanterelles keep Tuscany's bands. 96 % of the
  woodland cells lie below 1,000 m.
- **Weather rules, stoppers and growth clocks unchanged**: no Sardinian study gives numbers, and
  the lore (a flush about ten days after a good rain; repeated light rain better than storms; the
  maestrale "wasting" the rain) fits the Tuscan rules. The wind is recorded as a known gap.
- **Press contrasts** (`sardegna/sanity.yaml`): 16 (13 porcini, 1 ovoli, 2 gallinacci) over 11
  areas, written before any Sardinia score existed; 10 rest mainly on Funghi Magazine's bulletins,
  the rest on L'Unione Sarda, Cagliaripad, Olbia.it, Gallura Oggi, the ASL Gallura and a hiking
  blog.
- **Hand-offs from the research, answered here.** Forest area: −8.5 % (Woodland grid); the dehesa
  is the first class to reconsider if porcini sightings land in it. Rain scale: the ARPAS fit.
  Slope stopper: Sardinia's woodland slopes (median 16.9°, p90 24.9°) match Tuscany's and Sicily's,
  so the band is kept. **Sun stopper:** on the Sardinian woodland cells the day's sun ratio is below
  80 % of flat ground's (where the soft *B. aereus* stopper reaches its ×0.9 floor) on 1.7 % of
  cells on 15 October and 4.6 % on 15 November (Sicily 2.2 % and 6.1 %; median 99 %), so the
  Tuscan anchors are kept. The montane plantations (fir, cedar and black pine on the Limbara)
  cannot be split from the lowland pines on the 1:50,000 map (Known limitations).

## Validation

Scored 2016-03-18 to 2026-10-07 on 2026-09-30 (rules version `12b948c9a856`, rain scale 1.00 + 0.34
per km, lapse rates 5.3 min and 4.7 soil): 5,141 woodland cells × every day per key, history
without factors (4 min), the served window 2026-09-24 to 2026-10-07 with them. `onboard --from
score` ran the hold-out backtest and the sanity check; the train-season backtest (`--seasons train
--label onboard-train`) and the per-group sanity reruns (`--group ovoli`, `--group gallinacci`)
were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **8** (ovoli 4, porcini 3, gallinacci 1), against
the 50 the parent plan asks for. Hold-out 2024–2025: **5** (porcini 2, gallinacci 2, ovoli 1).

**Backtest** (model vs the calendar and habitat baselines, `auc_local` / `auc_region` /
`auc_time_effort`):

| seasons | group | n | model | calendar | habitat `auc_local` |
|---|---|---|---|---|---|
| train 2016–2023 | porcini | 3 | 0.73 (0.62–0.85) / 0.95 / 0.78 | 0.58 / 0.77 / 0.57 | 0.58 |
| train | ovoli | 4 | 0.70 (0.57–0.82) / 0.89 / 0.66 | 0.61 / 0.81 / 0.56 | 0.61 |
| train | gallinacci | 1 | 0.68 / 0.66 / 0.51 | 0.62 / 0.47 / 0.65 | 0.68 |
| hold-out 2024–2025 | porcini | 2 | 0.48 (0.46–0.50) / 0.88 / 0.54 | 0.60 / 0.77 / 0.61 | 0.60 |
| hold-out | ovoli | 1 | 0.78 / 0.94 / 0.67 | 0.58 / 0.79 / 0.60 | 0.58 |
| hold-out | gallinacci | 2 | 0.92 (0.89–0.95) / 0.98 / 0.93 | 0.74 / 0.79 / 0.50 | 0.55 |

Thirteen sightings say little, but they lean the right way: the model beats the calendar on
`auc_region` for every group and on `auc_local` for all but the hold-out porcini. On their own days
the Gallura's porcini score 0.82 (Calangianus, 24 September 2016) and 0.94 (Sant'Antonio di
Gallura, 14 November 2019), Monte Arci's 0.64 (12 November 2023), Tempio's 0.49 (13 September 2024)
and Iglesias's 0.58 (24 November 2025); the ovoli 0.95 (Alà dei Sardi, October 2018), 0.99
(Calangianus, November 2022), 0.45 (Sinnai, 30 September 2020), 0.60 (Uta, November 2025) and 0.02
for the one in May (Sant'Antonio di Gallura, 25 May 2020, where the ovolo's window only opens); the
chanterelles of November 2025 at Domusnovas and Nurallao 1.00 and 0.89, Scano di Montiferro's in
May 2016 0.33. The hold-out porcini's `auc_local` of 0.48 is two sightings that score well on their
day (0.49 and 0.58) in cells whose neighbours score as well.

**Sanity check** (`sardegna/sanity.yaml`; each contrast scored on its own group):

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Gennargentu early September 2018 > 2020 | porcini | 0.799 | 0.320 | yes |
| Sardinia June 2018 > 2019 | porcini | 0.464 | 0.249 | yes |
| Sardinia late spring 2023 > 2021 | porcini | 0.802 | 0.211 | yes |
| Sardinia 2023: spring > October | porcini | 0.802 | 0.000 | yes |
| Sardinia 2023: November > the weeks before | porcini | 0.353 | 0.000 | yes |
| Sardinia October 2020 > 2021 | porcini | 0.673 | 0.209 | yes |
| Gallura > Montiferru and Marghine, early October 2020 | porcini | 0.876 | 0.912 | no |
| Linas and Arburese October 2020 > 2019 and 2025 | porcini | 0.814 | 0.106 | yes |
| Gallura > Sette Fratelli, November 2021 | porcini | 0.857 | 0.855 | yes (by 0.002) |
| the west > the east, autumn 2022 | porcini | 0.497 | 0.410 | yes |
| Sardinia late September 2024 > 2025 | porcini | 0.559 | 0.486 | yes |
| Gallura > the south, November 2024 | porcini | 0.321 | 0.506 | no |
| Monte Arci November 2023 > 2024 | porcini | 0.693 | 0.008 | yes |
| Gennargentu and the south September 2019 > 2022 | ovoli | 0.453 | 0.007 | yes |
| 2021: November > the weeks before | gallinacci | 0.759 | 0.262 | yes |
| 2022: December > the weeks before | gallinacci | 0.709 | 0.467 | yes |

**14 of 16 hold** (porcini 11 of 13, ovoli 1 of 1, gallinacci 2 of 2). The onboard summary's
"13/16" scores every contrast on porcini; the chanterelles' December 2022 contrast fails there
(0.289 against 0.498) and holds on its own group. The two misses both set one area against another
in the same weeks, as Sicily's did: in early October 2020 the Montiferru and Marghine score a shade
above the Gallura (0.912 against 0.876), both high, where the bulletins had the north and east
ahead because passing storms hit them more often while the centre-west had strong winds (the model
has no wind); in late October to November 2024 the south scores above the Gallura (0.506 against
0.321), where the bulletins had "al Sud non ci sono state grandi nascite causa della siccità" and
the north giving "molte nascite". The contrasts between years and the timing
contrasts, the ones the rain decides, all hold, most by wide margins; the Gallura-Sette Fratelli
one holds by 0.002 and says nothing.

**The served window.** On 30 September 2026 porcini average 0.08 across Sardinia's woodland cells,
with 270 cells at 0.6 or more, all on the east: the holm oak of the Ogliastra and the Sarrabus
(Baunei 68, Tertenia 34, Villaputzu 32, San Vito 19, Villasalto 17, Armungia 15, Ulassai, Jerzu,
Arzana, Talana), at a median 416 m. The island had a dry September: the woodland nodes' rain from
31 August to 29 September averages 12 mm in 2026 against 9–95 mm (median 48) in 2016–2025, and only
the eastern nodes caught the storms of 19–20 September (30–47 mm, a median woodland node 5 mm).
Ovoli average 0.09 and gallinacci 0.06; the forecast lifts porcini to 0.12 and 488 cells by 7
October.

## After the deploy: what to verify

The stores are rsync'd to the server with `deploy/rsync-region-data.sh sardegna` (no redeploy;
below). The server serves a region only when its YAML is in the deployed code and its stores are
on disk, so they stay inert until `main` with `config/regions/sardegna.yaml` is deployed by the
rail's "Deploy pulled main" step (with the daily job, which brings the weather and scores up to
that day). Then check:

- [ ] `https://mappafunghi.app/sardegna` and `/sardegna/porcini`, `/sardegna/ovoli`,
  `/sardegna/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Sardinian habitats (holm oak on Monte Ortobene above Nuoro, cork oak around
  Calangianus and Tempio, downy oak at Fonni and Aritzo, pine plantations on the Limbara).
- [ ] `https://api.mappafunghi.app/regions` lists `sardegna`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Sardegna URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/sardegna` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Sardegna", description, canonical, og image `og/sardegna.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1462).
- [ ] `/credits` shows "ISPRA, Regione Sardegna — Carta della Natura della Regione Sardegna
  1:50.000".
- [ ] The next morning's daily job has a `region_done` line for `sardegna`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Validation rests on thirteen sightings** (8 train, 5 hold-out), almost all in the Gallura's
  and the south-east's evergreen oak, and on one magazine's sector-level bulletins for most of the
  contrasts.
- **The forest map is 1998–99 imagery** at 1:50,000 (published 2011). The fires since (Montiferru,
  July 2021: some 13,000 ha around Cuglieri, Santu Lussurgiu and Scano di Montiferro) are not in
  it, and small woods and orchards are lumped with their surroundings: the Barbagia's chestnut is
  almost invisible (971 ha) and scored as downy oak.
- **The conifer plantations are one habitat.** 83.31 files the Limbara's and the Gennargentu's
  montane black pine, fir and cedar with the coastal Aleppo and stone pine as
  `mediterranean_pine`; *B. edulis* gets 0.3 there where Tuscany's montane pine would give 0.6.
- **The dehesa is left out** (112,668 ha of wooded cork and downy-oak pasture), as CLC's
  agroforestry areas are; it is the Sardinian ground closest to the Spanish dehesas where *B.
  aereus* is picked. If sightings land there, it is the first class to reconsider.
- **The reanalysis's rain error is spatial** as well as by height: dry on the south-east's granite
  mountains (Sette Fratelli, Pula), wet on the north-west coast. A scale by height cannot fix it;
  the reanalysis also rains too often (28 % of days against 21 %).
- **The rain gauges are CC BY-NC-ND** and unvalidated: fine for a check, not for redistribution;
  the fit and the per-station ratios are ours, the station series are not republished.
- **Wind is not scored**: the maestrale that dries the west after a rain is the bulletins' most
  common complaint.

## Data

- cells: 25026
- woodland cells: 5141
- INFC deviation: -8.5% (grid 573,104 ha vs 626,140 ha) — within ±10 %
- weather nodes: 61
- years stored: 2016–2026 (11 years)
- sightings kept: 19
- backtest AUC (auc_local, model, all): gallinacci 0.919, ovoli 0.777, porcini 0.481
- sanity contrasts: 13/16 passed (the onboard's count, every contrast on porcini; 14/16 each on its
  own group, Validation)

