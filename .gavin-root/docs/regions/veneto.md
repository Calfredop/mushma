# Veneto

Region card: `region-veneto.md` (region #10 of `feat-full-italy-coverage.md`). API id `veneto`, web
slug `/veneto`, ISTAT COD_REG 5, names "Veneto" / en "Veneto". 18,345 km² (ISTAT 2025), 560 comuni
in seven provinces (Belluno, Treviso, Vicenza, Verona, Padova, Venezia, Rovigo). From the Dolomites to
the sea: spruce, fir, larch and beech in the Dolomites of Belluno (Cadore, Comelico, the Agordino,
the Val di Zoldo, Cortina) and on the Prealps (the Asiago plateau, the Grappa, the Cansiglio, the
Lessinia, the Monte Baldo), hop-hornbeam and downy oak on the Prealps' lower slopes, chestnut and oak
on the Colli Euganei, the Colli Berici and the Montello, and almost no forest on the plain, which
covers half the region. The Vaia storm of 29 October 2018 flattened about 12,000 ha of forest here,
most of it spruce in the Agordino, Comelico and on the Asiago plateau.

## Sources

**Decision: the Region's Carta della copertura del suolo 2021, one map for both the groups and the
types** (`rv_ccs2021` in `api/src/api/config/sources.yaml`; IODL 2.0, "Regione del Veneto – L.R. n.
28/76 – Formazione della Carta Tecnica Regionale"). Checked 2026-09-29:

| candidate | what it is | verdict |
|---|---|---|
| **Carta della copertura del suolo 2021** (Regione del Veneto, Direzione Pianificazione Territoriale; GeoServer `rv:c0506171_ccs2021`) | The regional land-cover database redone in full from the AGEA 2021 orthophoto: 1:10,000, 0.25 ha minimum unit, a five-level Corine legend whose forest classes (level 4 and 5) are the categories and types of the regional forest typology (Del Favero et al. 2000), 73 forest and scrub classes. A `specific` flag marks forest hit by the Vaia storm (01), bark beetle (02) or fire (03). RNDT record `r_veneto:c0506171_CCS2021`, published 2025-07-03: IODL 2.0, no limits on public access; WFS and shapefile | **used** |
| Carta regionale delle categorie forestali (Regione del Veneto, Direzione Foreste; `rv:c0605011_categforestali_c` and `_ci`) | The forest map of 2006 (IT2000 orthophotos, about 2000), same typology, two layers by canopy cover (over 30 %, 10–30 %); IODL 2.0 ("tutti i dati cartografici presenti in questa sezione", Ricerca forestale e cartografia) | the same typology 20 years older, before Vaia: used only to check the plantations below |
| ISPRA CLC 2018 IV level | National fallback, 25 ha minimum unit | not needed: the regional map is open, finer, newer and typed |

Forest by the older map: 378,272 ha with cover over 30 % (−9.2 % against INFC 2015's 416,704 ha of
*bosco*), 392,139 ha with the 10–30 % layer (−5.9 %), leaving out, as below, the mugo pine, the
shrubland, the green alder and the broadleaf plantations for timber.

The 2021 map covers the whole region, so it needs a filter: the GeoServer layer holds 407,081
polygons, and the source asks for the forest and scrub classes (Corine level 3 in 311, 312, 313, 322,
323; 48,912 polygons, 441 MB of GeoJSON) with a CQL filter in place of the bbox (the loader gained a
WFS `cql_filter`; GeoServer answers HTTP 500 to any CQL `OR`, so the filter is one `IN` list). The
level-5 code (`clc_lv_all`, the level-4 code and a 0 where a polygon has no type) says which broad
group a polygon is and which habitat; the YAML maps every code.

- **Not forest.** Mugo-pine krummholz (32231–32233, 31,197 ha), shrubland (32211, 7,208 ha),
  green-alder scrub (31122, 2,651 ha) and woods in evolution (32300) go to the transitional group,
  which does not count toward the woodland mask: INFC counts them as *arbusteti* and *altre terre
  boscate*, as in Trentino-Alto Adige and Friuli-Venezia Giulia. The Euganean *pseudomacchia* (32221,
  124 ha) goes to macchia. **Broadleaf plantations for timber** (31151, *impianto di latifoglie*,
  1,359 ha: walnut, cherry and poplar on the plain) are left out, as INFC leaves *arboricoltura da
  legno* out and as the older map marks them "non bosco".
- **Vaia, bark beetle and fire.** The map flags 10,227 ha of forest: 9,731 ha hit by Vaia (8,100 ha
  of it conifer), 466 ha of bark-beetle kill, 31 ha of burnt wood. Their polygons keep a forest code,
  but the stands were flattened or killed, so a second group layer (`specific <> '-99994'`) sends them
  to transitional, as not woodland, and they give no type. With them counted as forest the grid would
  be 2.0 % below INFC instead of 4.4 %.
- **Mixed.** The *piceo-faggeti* (31311, 31312) are the map's only mixed forest; the fir woods with
  beech (31213) stay conifer.
- **Oak.** The *ostrio-querceti* (31184, 31185) are downy-oak woods with hop-hornbeam on the Prealps'
  and hills' warm slopes; they go to `deciduous_oak` with the *rovereti* (31135, 31136), the
  *querco-carpineti* (31195, 31196) and the Euganean oak wood with Mediterranean elements (31171).
  The *orno-ostrieti* (31181–31183) and the *carpineti* (31191–31194) go to `mixed_broadleaf`.
- **Conifer plantations** (31220, *formazione antropogena di conifere*, 27,894 ha unflagged) carry no species
  in the 2021 map. In the 2006 map the same class names what was planted: spruce on 21,900 of its
  28,600 ha (on beech and hop-hornbeam sites, 77 %), black and Scots pine on 3,200, larch on 3,000,
  stone and maritime pine on the coast on 900. So they go to `fir_spruce`.
- **Larch and stone pine** (31231–31235) go to `other_conifer`, the Scots pine woods (31251–31257) to
  `mountain_pine`, holm oak (31162) to `evergreen_oak`, robinia (31152) to `exotic_broadleaf`, and the
  willow, alder and coastal wet woods (31121, 31161, 31163) to `riparian`.

Areas of the forest the map does not flag (the flagged forest is its own row):

| code family | ha | group | habitat |
|---|---|---|---|
| 3124 peccete | 44,194 | conifer | fir_spruce |
| 3114 faggete | 79,768 | broadleaf | beech |
| 3118 orno-ostrieti (31181–31183) | 60,004 | broadleaf | mixed_broadleaf |
| 3123 lariceti e larici-cembreti | 37,893 | conifer | other_conifer |
| 3122 formazione antropogena di conifere | 27,894 | conifer | fir_spruce |
| 3118 ostrio-querceti (31184, 31185) | 26,481 | broadleaf | deciduous_oak |
| 3121 abieteti | 21,716 | conifer | fir_spruce |
| 3113 castagneti | 20,123 | broadleaf | chestnut |
| 3115 robinieti | 19,510 | broadleaf | exotic_broadleaf |
| 3125 pinete di pino silvestre | 13,167 | conifer | mountain_pine |
| 3116 saliceti, bosco costiero; 31121 ontano nero e bianco | 10,976 | broadleaf | riparian |
| 3131 piceo-faggeti | 10,148 | mixed | mixed_broadleaf_conifer |
| 3111 aceri-frassineti; 31123 betuleti; 3119 carpineti | 15,204 | broadleaf | mixed_broadleaf |
| 31100 latifoglie without a category | 8,600 | broadleaf | from the cell's other types |
| 3119 querco-carpineti; 3113 rovereti; 3117 Euganean oak | 2,825 | broadleaf | deciduous_oak |
| 31162 lecceta | 173 | broadleaf | evergreen_oak |
| 3223 mughete; 3221 arbusteti; 31122 ontano verde; 323 | 41,086 | transitional | transitional_woodland_shrub |
| forest flagged Vaia, bark beetle, fire | 10,227 | transitional | — |
| 32221 pseudomacchia | 124 | macchia | macchia |
| 31151 impianto di latifoglie | 1,359 | left out | — |

Map areas by group: broadleaf 243,665 ha, conifer 144,863 ha, mixed 10,148 ha; **forest 398,676 ha**
against INFC 2015's 416,704 ha (−4.3 %); transitional 51,313 ha with the flagged forest.

Credits: the map is added to the app's credits list (`web/src/credits.ts`).

## Config

`api/src/api/config/regions/veneto.yaml`:

- **Boundary.** ISTAT COD_REG 5; bbox `[10.62, 44.79, 13.11, 46.68]`, the ISTAT 2025 boundary's
  extent (10.6229, 44.7928, 13.1022, 46.6798) rounded outward to 0.01°. Region area 18,345 km², 560
  comuni.
- **Forest.** Two `forest.groups` layers on `rv_ccs2021` (the forest the map does not flag, by
  `clc_lv_all`; the flagged forest, by `clc_lvl_3`, to transitional) and `forest.types` on the same
  source and filter, mapping above.
- **iNaturalist place** 13074, "Veneto, IT" (admin level 10), resolved by name on 2026-09-29
  (`api.inaturalist.org/v1/places/autocomplete?q=Veneto`).
- **Weather points.** 69 land nodes on the 0.2° lattice (73 candidates), all 4,025 woodland cells
  within reach.
- **No `weather.lapse_rates`** (below).

### Lapse rates (`api.weather.checks lattice --region veneto`)

178 ERA5-Land land nodes at 0.1° (184 candidates, −51 to 2,069 m), three 14-day windows of 2024 (Jan,
Jul, Oct), run 2026-09-29. Cooling per km of height, median of the daily fits:

| variable | Jan | Jul | Oct | all | national config | difference |
|---|---|---|---|---|---|---|
| Tmin | 3.87 | 4.26 | 3.82 | **3.94** | 4.2 | −0.26 |
| Tmax | 3.69 | 5.48 | 3.36 | **4.47** | 4.5 | −0.03 |
| Tmean | 4.14 | 5.33 | 3.85 | **4.44** | 4.5 | −0.06 |
| soil 0–7 cm | 0.21 | 4.73 | 3.49 | **3.49** | 3.7 | −0.21 |

All four are within 1 °C/km of the national rates, the closest of any Alpine region so far (the
plain's winter inversions pull January's air rates down), so **the national rates are kept**. They
are the best of the three on the leave-out test:

| leave-out RMSE | Tmin | Tmax | Tmean | soil |
|---|---|---|---|---|
| served lattice (0.2°, stride 2), no lapse | 0.670 °C | 0.643 °C | 0.621 °C | 0.537 °C |
| served lattice, 6.5 °C/km | 0.558 °C | 0.367 °C | 0.381 °C | 0.551 °C |
| **served lattice, national** | **0.488 °C** | **0.327 °C** | **0.325 °C** | **0.408 °C** |
| stride 3 (0.3°), national | 0.815 °C | 0.591 °C | 0.597 °C | 0.787 °C |

## Grid

`uv run python -m api.grid.build --region veneto` (4 min, most of it the 441 MB GetFeature):

- **Cells 18,981; woodland 4,025** (21.2 %, the plain has none). Threshold sensitivity (forest share
  of the cell, before the 0.25 km² floor): 0.3 → 5,380, 0.4 → 4,731, **0.5 → 4,094**, 0.6 → 3,451,
  0.7 → 2,752. By province: Belluno 2,159 woodland cells, Vicenza 1,041, Verona 416, Treviso 363,
  Padova 43, Venezia 2, Rovigo 1.
- **INFC 2015: −4.4 %** (grid 398,369 ha vs 416,704 ha bosco), inside ±10 %. INFC 2015 predates Vaia;
  with the 10,227 ha of flagged forest counted the gap would be −2.0 %.
- **Habitats on woodland cells** (share of wooded area; cells where dominant; their mean height):

| habitat | share | dominant cells | mean elevation |
|---|---|---|---|
| fir_spruce (spruce, silver fir, spruce plantations) | 25.5 % | 1,024 | 1,323 m |
| beech | 21.8 % | 915 | 1,043 m |
| mixed_broadleaf (hop-hornbeam, ash-maple, hornbeam) | 19.6 % | 929 | 617 m |
| other_conifer (larch, stone pine) | 8.7 % | 353 | 1,659 m |
| transitional_woodland_shrub (mugo, green alder, Vaia) | 5.4 % | 38 | 1,386 m |
| deciduous_oak (downy oak with hop-hornbeam, sessile oak) | 5.0 % | 246 | 350 m |
| chestnut | 4.3 % | 181 | 481 m |
| mountain_pine (Scots pine) | 3.6 % | 132 | 1,064 m |
| mixed_broadleaf_conifer (spruce-beech) | 2.9 % | 100 | 1,199 m |
| exotic_broadleaf (robinia) | 2.4 % | 83 | 282 m |
| riparian | 0.8 % | 23 | 215 m |
| evergreen_oak (holm oak, Bosco Nordio, Colli Euganei) | 0.0 % | 1 | 5 m |

  The belts are in order: robinia and the riparian woods on the plain's edge and the Montello at
  200–300 m, oaks at 350 m, chestnut at 480 m, hop-hornbeam at 620 m, beech and Scots pine at
  1,050 m, spruce-beech at 1,200 m, spruce and fir at 1,320 m, larch and stone pine at 1,660 m. The
  dominant habitat covers a median 71 % of the wooded area (Friuli-Venezia Giulia 77 %, Trentino-Alto
  Adige 75 %). `borrowed_type_fraction` is 0 almost everywhere (mean 0.07 %; one cell over half): the
  8,600 ha of broadleaf without a category share cells with typed woods.
- **Terrain.** Woodland cells: median elevation 994 m, 5th percentile 262 m, 95th 1,755 m, max
  2,154 m, min 3 m; 709 cells up to 500 m, 1,317 at 500–1,000 m, 1,367 at 1,000–1,500 m, 612 at
  1,500–2,000 m, 20 above. Median slope 23.8°. All have terrain; 81 have no aspect.
- **Soil pH.** Median 5.97 (5th–95th percentile 5.35–6.59); lowest under larch, spruce and
  spruce-beech (5.52–5.61), highest under the oaks and holm oak (6.48–6.93).
- **Places.** All 560 comuni get cells (206 with woodland); 7 cells fall outside every comune
  polygon. Nearest locality median 1.3 km, max 8.6 km.
- **Spot checks:**

| place | cell | woodland | forest | top habitats | elev. m | comune |
|---|---|---|---|---|---|---|
| Asiago plateau, Bosco di Gallio | `1kmE4443N2533` | yes | 0.74 | beech 0.51, fir_spruce 0.40, transitional 0.09 | 1429 | Gallio (VI) |
| Val Galmarara, Asiago plateau | `1kmE4432N2536` | yes | 0.98 | fir_spruce 0.89, other_conifer 0.09 | 1405 | Roana (VI) |
| Cansiglio forest | `1kmE4506N2552` | yes | 0.58 | beech 0.88, fir_spruce 0.12 | 1090 | Fregona (TV) |
| Val Visdende | `1kmE4523N2614` | yes | 0.96 | fir_spruce 0.92, other_conifer 0.05 | 1435 | Santo Stefano di Cadore (BL) |
| Rocca Pietore (Vaia) | `1kmE4472N2592` | yes | 0.64 | fir_spruce 0.75, transitional 0.18 | 1246 | Rocca Pietore (BL) |
| Monte Grappa, north slope | `1kmE4460N2532` | yes | 0.99 | fir_spruce 0.95, beech 0.05 | 1471 | Seren del Grappa (BL) |
| Val di Zoldo | `1kmE4488N2584` | yes | 0.56 | mixed_broadleaf 0.65, mixed_broadleaf_conifer 0.34 | 990 | Val di Zoldo (BL) |
| Cortina, Pocol | `1kmE4482N2604` | no | 0.47 | other_conifer 0.87, transitional 0.11 | 1569 | Cortina d'Ampezzo (BL) |
| Lessinia, Bosco Chiesanuova | `1kmE4402N2501` | yes | 0.52 | beech 0.82, fir_spruce 0.17 | 1004 | Bosco Chiesanuova (VR) |
| Monte Baldo, upper slopes | `1kmE4386N2510` | no | 0.03 | transitional 0.96 (mugo) | 1812 | Ferrara di Monte Baldo (VR) |
| Colli Euganei, Monte Venda | `1kmE4453N2468` | yes | 0.92 | chestnut 0.69, deciduous_oak 0.26 | 478 | Vo' (PD) |
| Colli Berici | `1kmE4443N2483` | yes | 0.71 | deciduous_oak 0.83, chestnut 0.14 | 356 | Castegnero (VI) |
| Montello | `1kmE4485N2524` | yes | 0.83 | exotic_broadleaf 0.98, chestnut 0.02 | 326 | Volpago del Montello (TV) |
| Bosco Nordio | `1kmE4499N2449` | no | 0.44 | evergreen_oak 0.93 | 4 | Chioggia (VE) |
| Venezia (city) | `1kmE4503N2483` | no | 0.00 | — | 9 | Venezia (VE) |
| Padova (city) | `1kmE4468N2479` | no | 0.00 | — | 19 | Padova (PD) |
