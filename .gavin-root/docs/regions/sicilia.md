# sicilia

Region #18 of the full-Italy rollout (card `region-sicilia.md`). API id `sicilia`, web slug
`/sicilia`, ISTAT COD_REG 19, Wikidata Q1460. Config: `api/src/api/config/regions/sicilia.yaml`.
The third southern region, after Campania and Calabria, and the first island.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Siciliana, Comando del Corpo Forestale, **Carta forestale regionale** (Sistema Informativo Forestale, 1:10,000, published with the Piano Forestale Regionale, metadata of 10 February 2012) (`sif_carta_forestale`) | open by default (CAD art. 52 c. 2), reused as CC BY 4.0 | ArcGIS REST MapServer of the SIF, query enabled, no login |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | open-sea DEM tiles skipped (Woodland grid) |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 96908 "Sicily, IT" | per record | counts per cell only |

**What was checked, and why the SIF forest map.**

- **Sistema Informativo Forestale (SIF)** of the Comando del Corpo Forestale
  (`sif.regione.sicilia.it`): the forest maps of the regional forest inventory (IFRS), drawn on the
  1:10,000 Carta Tecnica Regionale to the FAO FRA 2000 definitions INFC uses, with a hierarchical
  forest-type legend (category, type, subtype, variant) after the University of Palermo's
  typology (La Mantia et al. 2000, 2001) (Piano Forestale Regionale 2021–2025, draft of May 2020,
  §3.1.1). Its ArcGIS server (`sifweb.regione.sicilia.it/arcgis/rest/services`) publishes the
  "Carta forestale regionale siciliana" as two layers of the same 110,716 polygons in
  `SIF_CART_TEMATICA`: layer 37, "Categorie Forestali" (the type code, `CODCAMPO`), and layer 38,
  "Classi inventariali", which carries the inventory class (`DESCRIPTION`) **and** the type code.
  The build reads layer 38 only (Download below). Query is enabled (1,000 features a page), in
  RDN2008 / UTM 33N (EPSG:7792), so the `GEOMETRY.STArea()` column is a true area.
- **ISPRA Carta della Natura, Sicilia** (1:50,000, 2008, with the Eolie updated in 2011):
  CORINE Biotopes habitats, a 477 MB GeoPackage on ISPRA's SDI, CC BY 4.0 but "previa richiesta"
  (the Campania precedent). Coarser and older than the SIF map, and its biotopes lump the Sicilian
  forest types (no split of *Q. gussonei* Turkey oak, of the reforestation by species, of Etna's
  laricio from its beech). Not used.
- **Carta Forestale d'Italia CFI2020** (CREA): on request only, as for Marche, Umbria and Calabria.
- **CLC 2018 IV level** (1:100,000): the national fallback, not needed.
- The SIF also serves the two legal forest maps (L.R. 16/1996 art. 4 and D.Lgs. 227/2001; layers
  39 and 40), which say what the law treats as forest but carry no forest type.

**Licence.** The RNDT record of the service (`r_sicili:ae06fe5c-a920-4b9c-bdee-ee972d93afa2`,
also shown as record 256 on the regional SITR geoportale) names no licence: its use limitation is
"nessuna condizione applicabile", its constraints "proprietà intellettuale dei dati" (the INSPIRE
code for intellectual property rights, which says who owns the data, not how it may be reused). The
SITR portal's own footer carries CC BY 4.0, and the SIF portal states no terms. Public data an
administration publishes without adopting a licence are open by default (CAD, D.Lgs. 82/2005, art.
52 c. 2), the reading this project took for Marche's REM map; so the map is reused as CC BY 4.0 and
credited "Carta forestale regionale © Regione Siciliana, Comando del Corpo Forestale (SIF)" with a
link to the SIF's forest-map page.

**Download.** `http://sifweb.regione.sicilia.it/arcgis/rest/services/SIF_CART_TEMATICA/MapServer/38`,
paged over the region's bbox by the build (111 pages of 1,000 features, about 20 s a page) and
cached under `raw/sif_carta_forestale/sicilia/`. Two loader fixes came with it (`fix(grid): an
ArcGIS forest layer honours where, and is paged once per region`): the ArcGIS reader now applies a
group layer's `where` (it ignored it), and the group layers read the same per-region page cache as
the forest types. The Abruzzo lane's paging fix is cherry-picked too (`fix(grid): page an ArcGIS
layer by what the server returned`): the SIF server answers 1,000 features to a request for 2,000.

**Classes.** The map's inventory classes, whole map (`GEOMETRY.STArea()`):

| class (`DESCRIPTION`) | polygons | ha | in the grid |
|---|---|---|---|
| 31a boschi | 32,004 | 321,618 | broadleaf or conifer, by type |
| 31b formazioni forestali rade (tree cover 5–10 %, INFC's "boschi radi") | 4,917 | 12,752 | transitional |
| 31c aree boscate temporaneamente prive di copertura | 1,065 | 8,896 | transitional |
| 21 arboricoltura da legno | 1,076 | 6,823 | left out |
| 32x arbusteti | 28,499 | 173,836 | macchia (MM) or transitional (AS, FR) |
| 32 praterie, pascoli, incolti e frutteti abbandonati | 43,153 | 388,383 | left out |

Class mapping of the woods (31a) by type (`CODCAMPO`), `sicilia.yaml`:

| type | group | habitat | ha (31a) |
|---|---|---|---|
| QU2 thermophilous downy oak, QU5 downy oak on siliceous soils, QU4 xerophilous downy oak on limestone, QU3 mesoxerophilous downy oak, QU1 sessile oak | broadleaf | deciduous_oak | 33,473; 42,523; 7,545; 4,064; 529 |
| CE2 montane Turkey oak, CE1 thermophilous Turkey oak of *Quercus gussonei* | broadleaf | deciduous_oak | 16,413; 8,850 |
| RI3 Mediterranean conifer reforestation (Aleppo, stone and maritime pine, cypress) | conifer | mediterranean_pine | 53,315 |
| RI1 eucalyptus reforestation (*E. globulus*, *E. camaldulensis*, *E. gomphocephala*) | broadleaf | exotic_broadleaf | 38,818 |
| LE1–LE4 holm oak (pioneer on rock, thermo-Mediterranean of the coast and the Iblean *cave*, xerophilous meso-Mediterranean, mesoxerophilous) | broadleaf | evergreen_oak | 24,239 |
| SU2 inland cork oak, SU1 coastal cork oak, SU3 cork oak on the Iblean volcanites | broadleaf | evergreen_oak | 11,297; 7,731; 2,436 |
| FA1 mesophilous beech on siliceous soils, FA4 and FA3 calcicolous beech, FA2 beech on Etna's lavas | broadleaf | beech | 13,785; 1,841; 1,168 |
| FR1 oriental plane, FR2 poplar and willow, FR3 shrub willows, FR4 tamarisk and oleander, FR5 narrow-leaved ash | broadleaf | riparian | 14,059 |
| CA1 thermophilous chestnut, CA2 montane mesophilous chestnut | broadleaf | chestnut | 7,361; 4,518 |
| RI2 broadleaf reforestation, BA1 other native broadleaves, BS1 Etna birch, BS2 aspen, BS3 manna ash, BS4 field elm, OS1–OS2 hop-hornbeam | broadleaf | mixed_broadleaf | 8,158; 4,256; 1,295 |
| RI4 montane conifer reforestation (black and laricio pine, cedar) | conifer | mountain_pine | 7,197 |
| PL1–PL3 laricio pine (*Pinus nigra* subsp. *calabrica*, Etna) | conifer | mountain_pine | 3,681 |
| BS5 robinia, BS6 ailanthus, BS7 other aliens | broadleaf | exotic_broadleaf | 1,390 |
| PM1 Aleppo pine of the south-east, PM2 maritime pine of Pantelleria, PM3 stone pine, PM4 naturalised Mediterranean pines | conifer | mediterranean_pine | 1,679 |

Shrubland (32x): MM0–MM9 Mediterranean macchia and garrigue (126,665 ha) → macchia; AS1–AS5 montane
and supra-Mediterranean scrub (39,257 ha: *Genista aetnensis* on Etna, broom, the Peloritani's
*Erica arborea*, holly, rosaceous scrub) and the shrub stands of FR3/FR4 (7,915 ha) →
transitional.

Forest (31a) is 255,746 ha broadleaf and 65,872 ha conifer on the whole map. **Reforestation is a
third of it** (RI1–RI4, 107,488 ha), as the regional plan says of the high forest ("oltre il 36
%"): it is filed by what was planted. **Eucalyptus stays forest** (38,818 ha): the map calls it
woods, INFC counts plantations for forestry purposes as "bosco", and the habitat vocabulary has a
place for it (`exotic_broadleaf`, eucalitteti), where no rule gives it host credit. Wood
plantations (21: walnut, cherry, young broadleaf plantings) stay out, as Calabria's broadleaf
plantations did.

**Forest area and INFC.** The grid holds 321,812 ha of forest against INFC 2015's "bosco" of 285,489
ha: **+12.7 %**, outside the ±10 % line. The map's legend has no class for INFC's low woods
(trees that stay under 5 m) or boscaglie: its "31a boschi" is FAO FRA forest by tree cover, which
takes them in, as it takes in the woods INFC could not reach:

| figure (INFC 2015, tables 1.1–1.3) | ha | grid vs it |
|---|---|---|
| bosco (boschi alti 284,731, of which 4,839 temporarily unstocked; plantations 758) | 285,489 | +12.7 % |
| bosco + boschi bassi 14,697 + boscaglie 4,460 + "aree boscate inaccessibili o non classificate" 8,170 | 312,816 | **+2.9 %** |
| total wooded area (bosco + altre terre boscate 101,745) | 387,234 | −16.9 % |

The rest of INFC's "altre terre boscate" is sparse woods (8,665 ha; the map's 31b holds 12,752) and
shrubland (65,753 ha; the map's 32x, which takes in garrigue, 173,836). The map was drawn on the
2008–2010 orthophotos (its polygons are stamped November 2011), INFC 2015 is five years later, and
Sicily burns: the 2012–2015 fire seasons alone would account for a few thousand hectares either
way. The regional inventory, on the same FRA definitions and a denser sample, counts 258,502 ha of
boschi alti and 515,580 ha of "superficie forestale" in all (Piano Forestale Regionale 2021–2025,
draft of May 2020, §3.1.2).

## Woodland grid

Built 2026-09-28 (`uv run python -m api.grid.build --region sicilia`, 12 minutes, 11 of them paging
the forest map).

- Cells 26,567; inside area 25,717 km² (the generalised ISTAT 2025 boundary, small islands included).
- **Woodland cells 2,278** (8.6 % of the cells, the lowest share so far: Sicily's woods are small
  and scattered through farmland and pasture), in 212 of the 391 comuni. By province: Messina 928,
  Palermo 417, Catania 363, Enna 164, Agrigento 127, Caltanissetta 117, Siracusa 67, Ragusa 48,
  Trapani 47.
- **Forest area 321,812 ha vs INFC 2015 bosco 285,489 ha: +12.7 %** (above: +2.9 % on bosco plus
  INFC's low woods, boscaglie and inaccessible woods). The 20 m rasterization reproduces the map's
  321,618 ha of 31a within 0.1 %.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 75 % of a cell's wooded area.
- Terrain: woodland elevation median 785 m (5th–95th percentile 254–1,492 m), highest cell mean
  1,912 m, highest point in a woodland cell 2,144 m (Etna); slope median 16.7°, 11.5 % of woodland
  cells above 25°; 36 have no aspect. 22 slivers (no woodland) have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.69 (6.25–7.42, 5th–95th percentile): acid on
  the Nebrodi's flysch and quartzarenite and the Peloritani's schist, alkaline on the Iblean and
  Sicani limestone. The WCS answered for the whole bbox this time (9 s).

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (downy oak s.l., Turkey oak, *Q. gussonei*) | 31.5 % | 860 | 803 m |
| mediterranean_pine (Mediterranean conifer reforestation, Aleppo, stone and maritime pine) | 14.4 % | 356 | 663 m |
| evergreen_oak (holm and cork oak) | 12.4 % | 324 | 555 m |
| exotic_broadleaf (eucalyptus, robinia, ailanthus) | 9.9 % | 260 | 431 m |
| beech | 7.9 % | 167 | 1,461 m |
| transitional_woodland_shrub | 5.4 % | 18 | |
| mixed_broadleaf (broadleaf reforestation, Etna birch, other natives) | 4.8 % | 96 | 1,178 m |
| macchia | 4.5 % | 17 | |
| mountain_pine (Etna's laricio, montane conifer reforestation) | 4.2 % | 97 | 1,334 m |
| chestnut | 3.9 % | 81 | 934 m |
| riparian | 1.2 % | 2 | |

- Beech dominates most cells in Cesarò (49, Monte Soro), Caronia, Alcara li Fusi, Bronte, Petralia
  Sottana, Longi, Isnello and San Fratello; the deciduous oaks in Caronia (101), Cesarò (66),
  Francavilla di Sicilia, Geraci Siculo, Mistretta, Monreale (Ficuzza), San Mauro Castelverde and
  Castiglione di Sicilia; the evergreen oaks in Caronia, San Mauro Castelverde, Pollina and Isnello;
  chestnut on Etna's east flank (Zafferana Etnea, Linguaglossa, Pedara, Trecastagni) and on the
  Nebrodi and Peloritani (Floresta, Montalbano Elicona, Messina); laricio and montane reforestation
  on Etna (Linguaglossa, Castiglione di Sicilia, Adrano, Maletto, Biancavilla) and in the Madonie
  and Nebrodi (Nicosia, Petralia Sottana, Floresta); the Mediterranean reforestation in the Sicani
  and the Iblei (Castronovo di Sicilia, Monterosso Almo, Sambuca, Caltabellotta, Chiaramonte Gulfi,
  Ragusa) and on Palermo's hills; eucalyptus in the interior (Mazzarino 46, Enna, Aidone, San
  Cataldo, Caltanissetta, Caltagirone, Piazza Armerina). The comuni with the most woodland cells:
  Caronia (168), Cesarò (119), Bronte, Mazzarino, Randazzo, Francavilla di Sicilia, San Mauro
  Castelverde, Geraci Siculo, Messina, Enna.
- **Small islands.** Pantelleria has 7 woodland cells (holm oak and maritime pine on Montagna
  Grande) and Salina 1 (Leni, macchia-dominated): all 8 lie more than 30 km from a land weather
  node, so they are not weighted and never scored (Weather). Lipari, Ustica, Favignana, Lampedusa
  and Linosa have none.

Spot checks:

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Monte Soro, Nebrodi | `1kmE4736N1663` | yes | 1.00 | beech 1.00 | 1717 | 15 | 6.1 | Cesarò (ME) | Pado, 9.5 km |
| Bosco di Caronia, Nebrodi | `1kmE4716N1666` | yes | 0.61 | deciduous_oak 0.50, evergreen_oak 0.36, transitional 0.14 | 735 | 14 | 6.7 | Caronia (ME) | Ricchiò, 4.9 km |
| Floresta, Nebrodi | `1kmE4755N1670` | no | 0.10 | mountain_pine 0.33, macchia 0.29, chestnut 0.15 (village, pasture) | 1277 | 12 | 6.8 | Floresta (ME) | Floresta, 0.3 km |
| Piano Battaglia, Madonie | `1kmE4677N1653` | yes | 0.53 | beech 1.00 | 1626 | 16 | 6.7 | Petralia Sottana (PA) | Castelbuono, 7.3 km |
| Piano Zucchi, Madonie | `1kmE4673N1655` | yes | 1.00 | evergreen_oak 0.98 | 1083 | 27 | 6.5 | Isnello (PA) | Collesano, 4.8 km |
| above Castelbuono, Madonie | `1kmE4681N1656` | yes | 1.00 | evergreen_oak 0.61, deciduous_oak 0.38 | 1238 | 21 | 6.4 | Castelbuono (PA) | Castelbuono, 2.4 km |
| Linguaglossa's laricio, Etna | `1kmE4768N1649` | yes | 0.92 | mountain_pine 1.00 | 1731 | 9 | 6.3 | Linguaglossa (CT) | Vena, 8.0 km |
| north-east Etna above Rovittello | `1kmE4770N1652` | yes | 0.96 | deciduous_oak 0.64, chestnut 0.17, mountain_pine 0.15 | 1359 | 11 | 6.4 | Castiglione di Sicilia (CT) | Rovittello, 4.7 km |
| Zafferana Etnea, Etna | `1kmE4771N1640` | yes | 0.86 | chestnut 0.95 | 1196 | 25 | 6.5 | Zafferana Etnea (CT) | Albergo Belvedere, 2.3 km |
| Monte Spagnolo, Etna | `1kmE4763N1654` | no | 0.10 | transitional 0.58 (*Genista aetnensis*), macchia 0.31 | 1256 | 12 | 6.5 | Randazzo (CT) | Montelaguardia, 4.0 km |
| Bosco della Ficuzza | `1kmE4622N1651` | yes | 0.80 | deciduous_oak 0.65, riparian 0.20 | 775 | 13 | 6.6 | Godrano (PA) | Ficuzza, 2.3 km |
| Bosco della Quisquina | `1kmE4634N1623` | no | 0.47 | deciduous_oak 0.41, mediterranean_pine 0.32, evergreen_oak 0.25 | 923 | 18 | 6.9 | Santo Stefano Quisquina (AG) | Santo Stefano Quisquina, 3.2 km |
| Bosco di Rossomanno, Erei | `1kmE4715N1606` | no | 0.48 | exotic_broadleaf 0.77, deciduous_oak 0.23 | 578 | 18 | 7.2 | Aidone (EN) | Aidone, 2.5 km |
| Montagna Grande, Pantelleria | `1kmE4500N1525` | yes | 0.96 | evergreen_oak 0.54, mediterranean_pine 0.42 | 602 | 20 | 6.6 | Pantelleria (TP) | Siba-Roncone, 1.5 km |
| Palermo (city) | `1kmE4617N1676` | no | 0.00 | — | 31 | 5 | — | Palermo (PA) | Palermo, 3.0 km |

Threshold sensitivity (recomputed from stored fractions, with the 0.25 km² floor):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 4,003 | 3,053 | **2,278** | 1,697 | 1,212 |

The mask is more sensitive here than anywhere so far (0.4 would add a third): many Sicilian woods
fill part of a cell, the Bosco della Quisquina and Rossomanno cells above among them. The shared
0.5 rule is kept.

**DEM tiles over open sea.** Sicily's bbox asks for twenty 1° GLO-30 tiles; the build uses the fix
cherry-picked from `region/calabria` (`fix(grid): skip DEM tiles the bucket lacks over open sea`, the
same content as on `region/campania`), so the tiles the bucket lacks are skipped.

## Weather

- Points: 104 candidates on the 0.2° lattice, **66 on land**; 2,270 of the 2,278 woodland cells
  weighted, 8 out of reach (Pantelleria's 7 and Salina's 1, more than 30 km from a land node: the
  0.2° lattice has no land node on either island).
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region sicilia`,
  2026-09-28, 221 land nodes at 0.1° of 265, three 14-day windows of 2024). Cooling per km of height
  across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.20 | 1.59 | 4.06 | 3.91 | 4.5 | −0.59 |
  | temperature_2m_mean | 6.04 | 3.01 | 4.92 | 4.92 | 4.5 | +0.42 |
  | temperature_2m_min | 6.42 | 4.01 | 4.97 | 4.97 | 4.2 | +0.77 |
  | soil_temperature_0_to_7cm_mean | 4.94 | 1.19 | 3.54 | 3.54 | 3.7 | −0.16 |

  Every rate is within 1 °C/km of the national config, so **the national rates are kept**. July's
  weak rates for the maximum and the soil are the island's summer: the interior plateau and the
  plain of Catania bake as hot as the coast, so height explains little. The national rates also
  downscale best at the served lattice. Leave-out RMSE against the full 0.1° field:

  | leave-out RMSE | none | 6.5 °C/km | national config |
  |---|---|---|---|
  | Tmin, served lattice (0.2°, stride 2) | 0.823 | 0.563 | **0.519** |
  | Tmin, stride 3 (0.3°) | 1.712 | **0.913** | 1.004 |
  | Tmax, stride 2 | 0.701 | 0.605 | **0.492** |
  | Tmean, stride 2 | 0.687 | 0.446 | **0.346** |
  | soil, stride 2 | 0.785 | 0.805 | **0.668** |
  | soil, stride 3 | 1.362 | 1.206 | **1.009** |

  Only the minimum at the coarser, unserved stride prefers a steeper rate. Daily rain RMSE on the
  leave-out is 1.21 mm at stride 2 and 1.81 mm at stride 3 whatever the rates, close to Campania's
  (1.23 and 1.44 mm) and below Calabria's.

- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-17 (66 nodes, 55 min on 2026-09-28, one CDS 502 retried), with snowfall
  from CDS's gridded ERA5-Land, whose national half-year files (35.4–47.1° N, so Sicily's nodes lie
  inside) earlier lanes had already cached. Open-Meteo's archive and the ECMWF IFS forecast fill the days after 2026-09-17
  (`api.weather.ingest update --region sicilia`, history complete to 2026-09-22; 5,697 Open-Meteo
  calls counted that day across the lanes when it ran).

### Rain scale: the SIAS gauges

The Regione Siciliana's open-data portal publishes the hourly rain of the **SIAS** (Servizio
Informativo Agrometeorologico Siciliano) network: 96 stations at 10–1,875 m, from the coast to
Monte Soro and Etna's north flank, CC BY 4.0, "dati non validati" (`dati.regione.sicilia.it`, "SIAS -
Precipitazioni", monthly zips of semicolon CSV, June 2019 to July 2022, with the station list and
heights in "Elenco sensori meteo"). **Only June 2019 to May 2020 are whole**: from mid-2020 each
monthly file holds only the first hours of every day (3–5 of 24 rows a station-day, all from
midnight), so a day counts only with all 24 hours. The hours are solar time (24 rows on the
daylight-saving days). The network is wired into `GAUGE_NETWORKS` (`api.weather.sias`, commit
`feat(checks): SIAS rain gauges for Sicily's rain check`).

Two checks over June 2019 to May 2020 (366 days):

- **Every station** (a one-off script): the stored raw CDS rain read bilinearly at each station's
  position from the land nodes (weights renormalised), against its whole days; 94 stations with 80 %
  of the days. Median daily correlation 0.73–0.75 in every band, the best of any network so far.
- **Woodland gauges** (`uv run python -m api.weather.checks gauges --region sicilia --start
  2019-06-01 --end 2020-05-31`): the 7 SIAS stations inside woodland cells (Fiumedinisi 440 m,
  Monreale Bifarera 730, Antillo 796, Pedara 810, San Fratello 1,040, Caronia Pomiere 1,470, Cesarò
  Monte Soro 1,840), downscaled as the model does: pooled ratio 0.94 (1.05 at 400–800 m, 0.86 above
  800 m), median daily correlation 0.75, wet 3-day windows caught 79 % of the time with 10 % false
  alarms.

| band | stations | raw CDS / gauge rain (pooled) | scaled / gauge | median daily correlation |
|---|---|---|---|---|
| below 200 m | 32 | 1.10 | 0.98 | 0.75 |
| 200–400 m | 22 | 1.05 | 0.96 | 0.74 |
| 400–800 m | 30 | 1.06 | 0.99 | 0.72 |
| 800 m and above | 10 | 0.99 | 0.99 | 0.75 |
| all | 94 | 1.06 (median station 1.08) | 0.98 | |
| woodland gauges (downscaled) | 7 | 0.94 | 0.92 | 0.75 |

Unlike the Apennine regions, the reanalysis is not much drier in Sicily's mountains: its bias is
spatial more than altitudinal, wet on the Tyrrhenian coast (Patti 2.03, Lascari 1.57, Caronia Buzza
1.49, Palermo 1.43) and dry on the Iblei (Modica 0.63, Palazzolo Acreide 0.66, Ragusa 0.68), whose
relief the 0.1° model smooths away. Like everywhere, it rains too often: 1 mm or more on 25 % of days
against the gauges' 16 %.

**`sicilia.yaml` sets 0.88 + 0.10 per km** over `era5_land_cds` and `era5_seamless` (the national
clamp at 1,700 m kept): the least-squares fit through the origin of gauge totals on model totals × (a
+ b × elevation) over the 94 stations, a = 0.880, b = 0.101. It is robust: leave-one-out slopes
0.08–0.13, the 40 stations at 400 m and above give 0.87 + 0.11, those at 200 m and above 0.90 +
0.08. The 7 woodland gauges alone would give 0.85 + 0.22; they stay 8 % dry after scaling (Known
limitations).

| scale | factor at 200 / 500 / 800 / 1,200 m |
|---|---|
| **Sicily (94 SIAS gauges, used)** | **0.90 / 0.93 / 0.96 / 1.00** |
| Sicily's 7 woodland gauges | 0.89 / 0.96 / 1.02 / 1.11 |
| Calabria (15 station normals) 0.85 + 0.82 | 1.01 / 1.26 / 1.50 / 1.83 |
| Campania (agrometeo, 11–769 m) 0.77 + 0.52 | 0.87 / 1.03 / 1.19 / 1.39 |
| national (Tuscan gauges) 1.28 + 0.29 | 1.34 / 1.43 / 1.51 / 1.63 |

The national scale would make Sicily's rain 49 % too wet on these gauges. The fit rests on one year,
with a wet autumn (November 2019's median station 181 mm) and a dry winter (January–February 2020
3–4 mm); it scales totals, not timing. Since the porcini's 30-day rain is a share of each cell's own
(scaled) normal, the choice matters most for the absolute rain ramps of the ovolo and the
chanterelles.

## Sightings

`uv run python -m api.sightings.ingest fetch --region sicilia` (2026-09-28; the first try lost its
connection to GBIF and was rerun): **53 GBIF records** for the three groups over the bbox (2 *B.
edulis*, 13 *B. aereus*, 3 *B. reticulatus*, no *B. pinophilus*, 7 *A. caesarea*, 28
*Cantharellus*) and **none from iNaturalist** in the last two weeks. After the quality filters (25
material samples, 10 too imprecise, 3 undated, overlapping; 36 give no uncertainty and pass) 18 are
kept, and **11 land on Sicily's woodland cells**, one of them obscured:

| group | train seasons 2016–2023 | hold-out 2024–2025 | where |
|---|---|---|---|
| porcini | 3 cell-days (plus 1 obscured) | 0 | Nebrodi beech above San Fratello (3 September 2022) and on Monte Soro (Cesarò, 26 October 2023); oak at Caronia (15 October 2023); the obscured one in Etna's oaks at Milo (September 2018) |
| gallinacci | 4 cell-days (5 records) | 0 | the Peloritani above Messina: reforestation pine and eucalyptus (31 October and 3 November 2018; Messina and Saponara, 2 October 2020) |
| ovoli | 0 | 0 | none of the 7 records passes the filters inside the woodland |

Two more predate the history: porcini in the chestnut above Linguaglossa (Etna, October 2014) and
chanterelles on Pantelleria (November 2013, a cell the weather cannot reach).

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/sicilia.md`; rules in
`api/src/api/config/species/sicilia/` (34 new references; child card `region-sicilia-species.md`).

- **All three groups and six keys kept.** The regional law (L.R. 3/2006) bans picking the closed
  ovolo and its implementing lists set a minimum cap for the porcini; the Sicilian checklist
  (Ferraro et al. 2022) has all six keys.
- **One quantitative source drives the changes**: Vasquez's census of the Sicilian Boletales
  (University of Catania, 2010–2013), 236 dated porcini records with place, height, wood and number
  of fruit bodies, mostly on Etna and the Nebrodi. The porcini split by belt: *B. reticulatus* (116
  records) in chestnut and the spring flush, *B. aereus* (82) in the downy, Turkey, holm and cork
  oak, *B. edulis* (30) in the high beech and Etna birch, *B. pinophilus* (8) the one porcino of
  the pine.
- **Etna's laricio is weak porcini ground**: `mountain_pine` is a full host for *B. pinophilus*
  only and 0.1 for *B. edulis* and *B. reticulatus*; mixed pine-beech and pine-chestnut cells keep
  their broadleaves' credit.
- **Seasons:** *B. reticulatus* opens on 15 April and is full from 15 May to 31 October (the May–June
  flush on the Nebrodi and Etna); *B. aereus*'s lower window runs from 15 April to 10 January
  (records to 8 December in the evergreen oaks), its upper one from 15 May to 30 November with the
  handover at 1,000–1,200 m; the ovolo from 15 May to 10 December, full from 1 September to 15
  November. The summer gap is left to the heat, drought and drying rules.
- **Altitude bands move up** 250–600 m with the hosts: the census's porcini medians are 1,000 m
  (*B. aereus*), 1,240 m (*B. reticulatus*) and 1,500 m (*B. edulis*). *B. edulis* is full from
  800 to 2,000 m.
- **Plantations are poor porcini ground**: `mediterranean_pine` (the Aleppo, stone pine and cypress
  reforestation) 0.1 for every porcino and the ovolo; eucalyptus 0.1 for *B. aereus* and *B.
  reticulatus* (folklore, the Erei reports) and 0 or 0.05 for the rest. The chanterelles keep the
  pines at 0.3: every Sicilian specimen with a habitat grew in stone-pine or cedar plantations over
  holm oak (the Peloritani).
- **Weather rules, stoppers and growth clocks unchanged**: no Sicilian study gives numbers, and the
  lore (a week or more after heavy rain; the tramontana "fatale per la crescita dei carpofori") fits
  the Tuscan rules.
- **Press contrasts** (`sicilia/sanity.yaml`): 14, all porcini, written before any Sicily score
  existed; 11 rest on Funghi Magazine's national bulletins (Wayback captures), three on La Sicilia
  and a trekking guide's page. No outlet gave an ovoli or chanterelle verdict on two windows.
- **Hand-offs from the research, answered here.** Habitat medians: beech-dominated cells sit at a
  median 1,461 m and chestnut at 934 m, inside the bands the research set before the grid existed.
  Forest area: explained above (INFC's low woods, boscaglie and inaccessible woods). Rain scale: the
  SIAS fit. Slope and sun stoppers: Sicily's woodland slopes (median 16.7°, 11.5 % above 25°) are
  gentler than Calabria's and Campania's, where the Tuscan anchors were kept, so they are kept here.
  The plantation cells: Validation.

## Validation

Scored 2016-03-18 to 2026-10-05 on 2026-09-28 (rules version `9dedbe811f51`, rain scale 0.88 + 0.10
per km): 2,270 woodland cells × every day per key, history without factors (3 min), the served
window 2026-09-22 to 2026-10-05 with them. `onboard --from score` ran the hold-out backtest and the
sanity check; the train-season backtest (`--seasons train --label onboard-train`) was run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **7** (gallinacci 4, porcini 3, ovoli 0), against
the 50 the parent plan asks for. Hold-out 2024–2025: **0**, so the onboarding backtest had nothing
to score.

**Backtest** (train seasons; model vs the calendar and habitat baselines, `auc_local` / `auc_region`
/ `auc_time_effort`):

| group | n | model | calendar | habitat `auc_local` |
|---|---|---|---|---|
| porcini | 3 | 0.47 (0.44–0.50) / 0.49 / 0.50 | 0.52 / 0.81 / 0.52 | 0.52 |
| gallinacci | 4 | 0.43 (0.29–0.56) / 0.87 / 0.53 | 0.52 / 0.81 / 0.61 | 0.45 |

Seven sightings say nothing either way. The Peloritani chanterelles of 31 October and 3 November
2018 score 0.95 and 0.69 on their day, those of 2 October 2020 0.39 and 0.36. Of the porcini, the
Nebrodi beech above San Fratello (3 September 2022) scores 0.32 and the two October 2023 records, oak
at Caronia on the 15th and Monte Soro's beech on the 26th, score 0: the reanalysis gives Monte Soro
38 % of its normal 30-day rain before the 26th, the late-September rain (23–30 September, 20–50 mm
at the Nebrodi nodes) spread over several light days and next to nothing in October until the 21st.
The woodland gauges above 800 m hold 0.86 of their rain in the reanalysis, 0.87 once scaled
(Weather), so the Nebrodi may have been wetter than the model thinks; the sanity check's own October
2023 timing contrast still holds. Validating Sicily needs located records: Vasquez's census (236
dated porcini records with place and height, 2011–2013) predates the history but is the lead for any
future check.

**Sanity check** (`sicilia/sanity.yaml`, all porcini):

| contrast | higher window | lower window | holds |
|---|---|---|---|
| Etna 2018 > 2017, late summer | 0.735 | 0.071 | yes |
| Etna 2018 > 2025, August | 0.547 | 0.082 | yes |
| Etna, Nebrodi, Peloritani June 2018 and 2021 > 2022 and 2024 | 0.133 | 0.063 | yes |
| Etna and Peloritani > Sicani and Ficuzza, late June 2020 | 0.246 | 0.117 | yes |
| Etna, Nebrodi, Peloritani > Sicani and Ficuzza, 1–25 October 2020 | 0.468 | 0.510 | no |
| Etna, Nebrodi, Peloritani early October 2020 > 2022 | 0.497 | 0.171 | yes |
| Etna > Sicani and Erei, September 2021 | 0.760 | 0.239 | yes |
| Sicani, Erei, Iblei September 2024 > 2021 | 0.400 | 0.243 | yes |
| Sicani and Ficuzza > Etna, 25 October–20 November 2022 | 0.009 | 0.056 | no |
| Etna and Nebrodi > Madonie, October 2023 | 0.385 | 0.002 | yes |
| Etna and Nebrodi 2023: October > the weeks before | 0.385 | 0.031 | yes |
| Etna, Nebrodi, Peloritani 2024: late summer > the weeks before | 0.578 | 0.004 | yes |
| Etna and Nebrodi September 2024 > 2025 | 0.679 | 0.083 | yes |
| Etna and Nebrodi 2025: autumn > the weeks before | 0.598 | 0.058 | yes |

**12 of 14 hold.** The two misses both set the island's west against its east, from Funghi
Magazine's sectors: in October 2020 the Sicani and Ficuzza score a shade above the east and north
(0.510 against 0.468), where the bulletins had the south and west "sferzati dal vento" with sporadic
births (the model has no wind); in November 2022 both sides score near 0 (0.009 against 0.056)
where the bulletins report "ottime nascite sui settori occidentali". The contrasts between years
and the timing contrasts, the ones the rain decides, all hold, most by wide margins.

**Which group wins the combined map.** On high combined days (0.5 or more, September 2016 to
December 2025) the chanterelles win 77 % of the cell-days in the Mediterranean pine plantations and
40 % in the eucalyptus, as in the oaks (42–54 %): their habitat gate is full from an affinity of 0.3,
which the pines keep on the Peloritani evidence (every Sicilian chanterelle specimen with a habitat
grew in stone-pine or cedar plantations over holm oak). The porcini win the beech (*B. edulis* and
*B. reticulatus*) and the laricio (*B. pinophilus*, 44 %).

**The served window.** On 28 September 2026 porcini average 0.22 across Sicily's woodland cells,
with 166 cells at 0.6 or more: the oaks and chestnut of Etna's south and west flanks (Ragalna,
Biancavilla, Zafferana Etnea, Pedara), the Bosco della Ficuzza (Monreale, Godrano), the Sicani
(Contessa Entellina, Chiusa Sclafani), Caccamo and Castellammare del Golfo, at a median 854 m. The
reanalysis gives the woodland nodes about 32 mm from 29 August to 22 September (the last reanalysis
day), against 31–82 mm (median 47) over 29 August–27 September in 2016–2025. Ovoli average 0.19 and
gallinacci 0.22.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-28 (`deploy/rsync-region-data.sh sicilia`, 210
files, 195 MB, no redeploy). The server serves a region only when its YAML is in the deployed code
and its stores are on disk, so they stay inert until `main` with `config/regions/sicilia.yaml` is
deployed by the rail's "Deploy pulled main" step (with the daily job, which brings the weather and
scores up to that day). Then check:

- [ ] `https://mappafunghi.app/sicilia` and `/sicilia/porcini`, `/sicilia/ovoli`,
  `/sicilia/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Sicilian habitats (beech on Monte Soro, laricio pine above Linguaglossa, chestnut at
  Zafferana Etnea, cork and holm oak at Caronia).
- [ ] `https://api.mappafunghi.app/regions` lists `sicilia`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Sicilia URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/sicilia` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Sicilia", description, canonical, og image `og/sicilia.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1460).
- [ ] `/credits` shows "Regione Siciliana, Comando del Corpo Forestale — Carta forestale regionale
  (SIF)".
- [ ] The next morning's daily job has a `region_done` line for `sicilia`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Validation rests on seven sightings** and one magazine's sector-level bulletins; the hold-out
  seasons have none. The two October 2023 Nebrodi porcini score 0 on a dry reanalysis month.
- **Rain scale from one year.** The SIAS portal is whole only from June 2019 to May 2020; the fit is
  robust across stations but not across years. The woodland gauges stay 8 % dry after scaling (13 %
  above 800 m), and the reanalysis's error is spatial (wet on the Tyrrhenian coast, dry on the
  Iblei), which a scale by height cannot fix. The later SIAS months could be recovered if the portal
  republishes them whole.
- **The forest map is 2008–2010 imagery** (published 2012): the great fires since (2021, 2023) are
  not in it, and it lumps INFC's low woods and boscaglie into its woods (+12.7 % on INFC bosco,
  +2.9 % with them).
- **A third of the woods are plantations**, filed by what was planted: the pine plantations score
  low for porcini but full for chanterelles, which then colour the combined map there (Validation).
- **Small islands unscored.** Pantelleria's 7 woodland cells and Salina's 1 lie more than 30 km from
  a land weather node on the 0.2° lattice.
- **Mask sensitivity.** Sicily's woods are small and scattered; lowering the 0.5 forest-share rule to
  0.4 would add a third more woodland cells (Woodland grid).
- **Region lookup by bbox.** Sicily's bbox reaches 15.66° E and takes in Reggio Calabria and Villa
  San Giovanni, while Calabria's takes in Messina's Capo Peloro; card
  `fix-region-lookup-by-boundary.md` (noted there).
- **Shared fixes cherry-picked.** `fix(grid): skip DEM tiles the bucket lacks over open sea` (same
  content as on `region/calabria` and `region/campania`) and `fix(grid): page an ArcGIS layer by what
  the server returned` (same content as on `region/abruzzo`; `region/lombardia` fixes the same lines
  differently, so whichever merges second resolves one small conflict). This branch's own
  `fix(grid): an ArcGIS forest layer honours where, and is paged once per region` touches the same
  function's last lines.

## Data

- cells: 26567
- woodland cells: 2278
- INFC deviation: +12.7% (grid 321,812 ha vs 285,489 ha) — outside ±10%
- weather nodes: 66
- years stored: 2016–2026 (11 years)
- sightings kept: 11
- sanity contrasts: 12/14 passed

