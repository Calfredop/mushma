# Piemonte

Region card: `region-piemonte.md` (region #6 of `feat-full-italy-coverage.md`). API id `piemonte`,
web slug `/piemonte`, ISTAT COD_REG 1, names "Piemonte" / en "Piedmont". Alps on three sides
(Marittime, Cozie, Graie, Pennine, Lepontine) and a strip of Ligurian Apennine in the south-east;
wide chestnut belts in the hills and lower valleys, beech above them, larch and spruce up to the
tree line, robinia along the plain.

Branch note: `region/piemonte` was cut from `main` and fast-forwarded onto `region/umbria` (the lane's
previous rail, PR still open when this card ran), because Umbria carries the shared weather,
sightings and onboarding fixes every new region needs (CDS time-series history, per-region
iNaturalist place, Open-Meteo snowfall fallback). Three shared commits from `region/liguria` were
taken as well: the WFS paging and one-map forest read (`2440b40`), the og-image registry script
(`4df3925`) and the openrsync fix to `deploy/rsync-region-data.sh` (from `4670306`). Once Umbria and
Liguria are merged, this branch's own diff is Piemonte's.

## Sources

**Decision: Regione Piemonte's Carta forestale regionale, edizione 2025, for both layers**
(`rp_carta_forestale` in `api/src/api/config/sources.yaml`; CC BY 4.0, "Carta forestale regionale
2025 © Regione Piemonte (IPLA)"). Checked 2026-09-25:

| candidate | what it is | verdict |
|---|---|---|
| **Carta forestale regionale 2025** (Regione Piemonte, IPLA) | The 2016 Carta forestale (1:10,000, photo-interpretation and forest management plans) updated with the forest limit of the Carta Forestale d'Italia (CFI 2020). 74,021 polygons of forest only, each with its IPLA forest category (`ca_1`, 21 categories) and type (`tf_1`, 109 types with variants). Geoportale Piemonte record `r_piemon:130b499f-…`: licence CC BY 4.0, "no limitations to public access", GeoPackage by direct download (`datigeo-piem-download.it/…/SIFOR/CF_2025.gpkg`, 194 MB) | **used** |
| Carta forestale regionale 2024 | Same method plus the "Land Cover Piemonte" layer; WMS only in its record, no download link | superseded by 2025 |
| Carta forestale 2016 | The IPLA map the later editions start from | older; 2025 carries it forward |
| ISPRA CLC 2018 IV level | National fallback, 25 ha minimum unit | not needed: the regional map is open, finer and typed |

The map covers forest only, so one map gives both the broad groups (how much of each cell is
woodland) and the habitats (which kind), from the category. There is no land-use code and no mixed
category: IPLA types a stand by its dominant species. The shrubland categories (OV arbusteti
subalpini: green alder and rhododendron; AS arbusteti planiziali, collinari e montani) are not forest
(INFC counts them as *altre terre boscate*), so they go to the transitional group, which does not
count toward the woodland mask.

| category | ha | group | habitat |
|---|---|---|---|
| CA castagneti | 212,245 | broadleaf | chestnut |
| FA faggete | 145,080 | broadleaf | beech |
| RB robinieti | 130,276 | broadleaf | exotic_broadleaf |
| LC lariceti e cembrete | 97,044 | conifer | other_conifer |
| BS boscaglie pioniere e d'invasione | 78,991 | broadleaf | mixed_broadleaf |
| AF acero-tiglio-frassineti | 49,091 | broadleaf | mixed_broadleaf |
| QR querceti di rovere | 48,046 | broadleaf | deciduous_oak |
| QV querceti di roverella | 42,843 | broadleaf | deciduous_oak |
| QC querco-carpineti | 38,769 | broadleaf | deciduous_oak |
| OV arbusteti subalpini | 33,574 | transitional | transitional_woodland_shrub |
| RI rimboschimenti | 21,549 | conifer | other_conifer |
| SP saliceti e pioppeti ripari | 17,375 | broadleaf | riparian |
| PS pinete di pino silvestre | 15,436 | conifer | mountain_pine |
| AB abetine | 15,305 | conifer | fir_spruce |
| OS orno-ostrieti | 14,563 | broadleaf | mixed_broadleaf |
| PE peccete | 9,621 | conifer | fir_spruce |
| AN alneti planiziali e montani | 5,188 | broadleaf | riparian |
| CE cerrete | 4,587 | broadleaf | deciduous_oak |
| AS arbusteti planiziali, collinari e montani | 4,164 | transitional | transitional_woodland_shrub |
| PN pinete di pino montano (uncinato) | 2,743 | conifer | mountain_pine |
| PM pinete di pino marittimo | 685 | conifer | mediterranean_pine |

Areas are from the polygons (the `ettari` column is empty). The total, 987,175 ha, matches the
region's own 986,132 ha for the 2025 edition (38 % of the region; castagneti 22 %, faggete 15 %,
robinieti 13 %, larici-cembrete 10 %, boscaglie 8 %). Checks on the less obvious codes: PM polygons
all sit at 8.48–8.84° E, 44.51–44.65° N, the Appennino alessandrino above Ovada and Voltaggio,
where maritime pine grows, so PM is *pino marittimo* and PN (western Alps) is *pino montano*. RI
types are conifer plantations (RI20A pino nero, B peccio, C larice, D douglasia, E pino silvestre;
only RI20G is red oak), so RI is `other_conifer` as in Liguria.

Credits: the map is added to the app's national credits list (`web/src/credits.ts`). The ARPA
Piemonte rain gauges feed a check only, never the app.

## Config

`api/src/api/config/regions/piemonte.yaml`:

- **Boundary.** ISTAT COD_REG 1; bbox `[6.62, 44.06, 9.22, 46.47]`, the ISTAT 2025 boundary's
  extent (6.6266, 44.0606, 9.2140, 46.4643) rounded outward to 0.01°. Region area 25,389 km².
- **Forest.** `forest.groups` and `forest.types` both on `rp_carta_forestale`, class column and
  type field `ca_1` (read once: the one-map path from `region/liguria`), mapping above.
- **iNaturalist place** 10872, "Piemonte, IT" (admin level 10), resolved by name on 2026-09-25
  (`api.inaturalist.org/v1/places/autocomplete?q=Piemonte`).
- **Gauges.** `api.weather.checks gauges --region piemonte` reads ARPA Piemonte's open daily rain
  (`api.weather.arpa_piemonte`, Validation).
- **`model:` overrides:** see Validation.

## Grid

`uv run python -m api.grid.build --region piemonte` (4.3 min, the DEM tiles and SoilGrids fetched
for the first time):

- **Cells 26,148; woodland 9,537** (36.5 %). Threshold sensitivity (forest share of the cell, before
  the 0.25 km² floor): 0.3 → 12,339, 0.4 → 11,018, **0.5 → 9,673**, 0.6 → 8,322, 0.7 → 6,949.
- **INFC 2015: +6.7 %** (grid 949,734 ha vs 890,433 ha bosco), inside ±10 %. The map's forest
  categories hold 949,437 ha; the gap to INFC is the regional forest definition (L.R. 4/2009 and the
  CFI 2020 limit: ≥ 2,000 m², ≥ 20 % cover) and ten years of regrowth on abandoned land, mostly
  boscaglie and robinia.
- **Habitats on woodland cells** (share of wooded area; cells where dominant; their mean height):

| habitat | share | dominant cells | mean elevation |
|---|---|---|---|
| chestnut | 25.6 % | 2,647 | 672 m |
| beech | 17.9 % | 1,712 | 1,207 m |
| mixed_broadleaf | 15.8 % | 1,254 | 1,041 m |
| deciduous_oak | 13.7 % | 1,373 | 498 m |
| other_conifer (larch, stone pine, plantations) | 12.0 % | 1,134 | 1,647 m |
| exotic_broadleaf (robinia) | 7.7 % | 928 | 281 m |
| fir_spruce | 3.0 % | 268 | 1,407 m |
| mountain_pine | 2.1 % | 169 | 1,293 m |
| transitional_woodland_shrub | 1.2 % | 9 | 1,324 m |
| riparian | 1.0 % | 39 | 347 m |
| mediterranean_pine | 0.1 % | 4 | 411 m |

  The belts are in the right order: robinia and riparian woods on the plain, oaks in the hills,
  chestnut at 670 m, beech at 1,200 m, fir and spruce at 1,400 m, larch at 1,650 m. The dominant
  habitat covers a median 71 % of the wooded area (Tuscany 89 %): Alpine cells mix belts.
  `borrowed_type_fraction` is 0 everywhere (groups and types are one map).
- **Terrain.** Woodland cells: median elevation 838 m, 95th percentile 1,774 m, max 2,307 m; median
  slope 22.8°. All have terrain; 410 have no aspect (flat or two-sided).
- **Soil pH.** Median 6.27 (5th–95th percentile 5.73–7.02); lowest under fir/spruce (6.03), beech
  and larch (6.14), highest under robinia (6.72).
- **Places.** 1,180 comuni get cells; 6 cells fall outside every comune polygon. Nearest locality
  median 1.0 km, max 8.8 km.
- **Spot checks:**

| place | cell | woodland | forest | top habitats | elev. m | comune |
|---|---|---|---|---|---|---|
| Gran Bosco di Salbertrand | `1kmE4076N2443` | yes | 0.90 | fir_spruce 0.75, other_conifer 0.21 | 1507 | Salbertrand (TO) |
| Scots pine above Oulx | `1kmE4070N2439` | yes | 0.81 | mountain_pine 0.89, other_conifer 0.08 | 1282 | Oulx (TO) |
| Chestnut slopes of Garessio | `1kmE4163N2346` | yes | 0.79 | chestnut 0.93, deciduous_oak 0.07 | 704 | Garessio (CN) |
| Val Casotto | `1kmE4154N2352` | yes | 1.00 | chestnut 0.91, beech 0.09 | 1046 | Pamparato (CN) |
| Bosco della Partecipanza, Trino | `1kmE4185N2458` | yes | 0.54 | deciduous_oak 1.00 | 151 | Trino (VC) |
| Capanne di Marcarolo | `1kmE4223N2382` | yes | 0.89 | other_conifer 0.78 (plantations), deciduous_oak 0.19 | 832 | Bosio (AL) |
| Oasi Zegna | `1kmE4175N2509` | yes | 1.00 | beech 0.45, mixed_broadleaf 0.39, other_conifer 0.16 | 1098 | Valdilana (BI) |
| Bobbio Pellice | `1kmE4091N2414` | yes | 0.86 | other_conifer 0.39, chestnut 0.30 | 947 | Bobbio Pellice (TO) |
| Santa Maria Maggiore (village) | `1kmE4201N2559` | no | 0.18 | — | 837 | Santa Maria Maggiore (VB) |
| Torino (city) | `1kmE4138N2442` | no | 0.00 | — | 246 | Torino (TO) |

## Data

(written by `api.regions.onboard piemonte`)
