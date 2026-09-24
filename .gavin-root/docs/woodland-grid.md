# Woodland grid: 1 km cells with habitat, terrain and place labels

Build date: 2026-09-17. Card: M2 · Woodland grid. Traces to PRD → Architecture (Grid, Areas),
Candidate data sources, Model (Known gaps) and Milestone 2.

The static layer every score sits on. For each 1 km cell of the EEA reference grid over Tuscany it
records whether the cell is mostly woodland, which habitats make up its wooded area, its terrain and
topsoil pH, and which comune and locality it belongs to.

## At a glance

| | |
|---|---|
| Cells intersecting Tuscany | **23,803** (their inside area sums to 22,991 km², the ISTAT region area) |
| Woodland cells (≥ 50 % forest, ≥ 25 ha of it) | **10,778** |
| Forest in the grid | 1,058,107 ha = 46.0 % of the land; INFC 2015 "bosco" 1,035,448 ha (**+2.2 %**) |
| Forest + macchia + regrowth | 1,159,893 ha; RaF 2019 1,163,057 ha (**−0.3 %**), INFC total wooded land 1,189,722 ha (−2.5 %) |
| Forest inside woodland cells | 847,470 ha, 80 % of all forest |
| Map export (woodland cells, WGS84 GeoJSON) | 2.7 MB raw, **274 KB gzipped** (budget: 1 MB compressed) |
| Build | `cd api && uv run python -m api.grid.build --region tuscany`; ~11 min cold (SoilGrids is slow), ~1.5 min warm |

## Outputs

Everything lands in `$DATA_DIR/grid/<region>/` (`api/data/grid/tuscany/` locally, gitignored):

| file | contents |
|---|---|
| `cells.parquet` | one row per cell (GeoParquet, EPSG:3035 squares). Columns below. |
| `cell_habitats.parquet` | long table `(cell_id, habitat, fraction)` for every cell with wooded area; fractions sum to 1 per cell |
| `cells_wgs84.geojson` | woodland cells only, `[lon, lat]` counter-clockwise rings (5 decimals), `id` = cell id, properties `dominant_habitat`, `elevation_m` |
| `meta.json` | build time, CRS, woodland rule, search radii, sources with licence and attribution, counts |

`cells.parquet` columns:

| column | meaning |
|---|---|
| `cell_id` | EEA reference grid code, e.g. `1kmE4453N2199` = lower-left corner at E 4 453 000, N 2 199 000 m (EPSG:3035). Stable across rebuilds. |
| `x_min`, `y_min`, `lon`, `lat` | lower-left corner (EPSG:3035) and WGS84 centre |
| `region_fraction` | share of the cell inside the region boundary |
| `woodland` | the mask (see below) |
| `forest_fraction`, `wooded_fraction` | forest share, and forest + macchia + regrowth share, of the cell's area inside the region (capped at 1) |
| `dominant_habitat`, `dominant_fraction` | largest habitat and its share of the wooded area |
| `borrowed_type_fraction` | share of the wooded area whose forest type came from neighbouring cells or a group fallback (see below) |
| `elevation_m`, `elevation_min_m`, `elevation_max_m` | mean and range of DEM heights |
| `slope_deg` | mean pixel slope |
| `aspect_deg` | compass bearing the cell mostly faces (0 = N); null when flat or slopes cancel out |
| `northness` | mean cos(aspect), flat pixels = 0: +1 all north-facing, −1 all south-facing |
| `soil_ph` | topsoil (0–30 cm) pH in water, SoilGrids |
| `comune_code`, `comune_name`, `province` | ISTAT comune covering most of the cell, and its province abbreviation |
| `place_name`, `place_distance_km` | nearest ISTAT inhabited locality to the cell centre |

Querying with DuckDB (no spatial extension needed):

```sql
SELECT c.cell_id, c.comune_name, h.fraction
FROM 'cells.parquet' c JOIN 'cell_habitats.parquet' h USING (cell_id)
WHERE c.woodland AND h.habitat = 'beech' AND h.fraction > 0.5;
```

## Grid

- **CRS and naming.** EPSG:3035 (ETRS89-LAEA, the EEA reference grid), 1 km cells aligned to
  multiples of 1000 m. Ids follow the EEA `CELLCODE` form (`1km` + `E` easting/1000 + `N`
  northing/1000 of the lower-left corner), so they match other EEA-grid datasets.
- **Clipping.** Every cell whose area overlaps the ISTAT 2025 region boundary (generalised version)
  is kept, including coastal and island slivers. `region_fraction` records how much is inside.
  Cells touching the boundary only along an edge are dropped.
- **Region config.** `api/src/api/config/regions/tuscany.yaml` holds the boundary (ISTAT region
  code), bbox, grid spec, and the source class mappings. Another region is a new YAML file plus, if
  its forest sources differ, new class mappings (see "Adding a region").

## Forest source

| | Regione Toscana UCS 2019 | ISPRA CLC 2018 IV livello | Copernicus HRL Forest Type 2018 | RT Vegetazione forestale | RT Inventario Forestale (IFT) |
|---|---|---|---|---|---|
| Detail | 1:10,000; woods mapped down to 2,000 m² | 1:100,000; 25 ha minimum unit | 10 m raster, 0.5 ha | 250 m field squares, published at 1:250,000 | 400 m sample points |
| Reference year | 2019 (also 2007–2016) | 2018 | 2018 | surveyed 1990s, published 1999 | 1985–1993 |
| Forest classes | 311 broadleaf, 312 conifer, 313 mixed, 323 sclerophyll, 324 regrowth. **No forest types.** | 3111–3117 broadleaf types, 3121–3125 conifer types, 3131/3132 mixed, 3231/3232 macchia, 324. **Maps 1:1 to the rule vocabulary.** | broadleaf / coniferous only | 18 dominant-species groups | forest category + 3 species with cover |
| Licence | CC BY 4.0 | CC BY 4.0 | Copernicus open access (attribution) | CC BY-SA 4.0 | CC BY-SA 4.0 |
| Access | 273 MB zip (7z inside), no login | ArcGIS REST query, no login (12 pages of 2,000 features for Tuscany) | EU Login for downloads; anonymous ImageServer export | 12 MB zip | 10 MB zip |
| Tuscany forest area | 1,058,414 ha (+2.2 % vs INFC) | 994,235 ha (−4.0 %) | not measured | 954,567 ha | ~1,080,000 ha of forest and shrub categories |

**Decision: combine UCS 2019 (how much) with CLC 2018 IV level (which kind).**

- UCS is the most detailed and most recent map, its forest total matches the national inventory
  within 2.2 %, and its 92 % thematic accuracy is documented. It separates broadleaf, conifer and
  mixed forest, macchia and regrowth, but not tree species.
- CLC IV level is the only current, openly licensed, scriptable map with forest types
  (castagneti, faggete, cerrete, leccete, abetine, pinete…). Its 25 ha minimum unit misses small
  woods: 203 cells that UCS calls woodland have under 10 % CLC forest.
- On woodland cells the two agree only moderately on the broadleaf/conifer split (correlation 0.57
  and 0.61), which is why the broad split comes from the finer map.
- HRL Forest Type has no species. The two regional forest-type layers are 25–40 years old and
  share-alike licensed. Their typology (with acidophilous sub-types) will return as the regional
  "Carta delle Categorie Forestali" that LaMMA is producing from UCS 2019; it is not published yet.

## Woodland mask

A cell is **woodland** when forest (UCS 311 + 312 + 313) covers **at least 50 %** of its area inside
the region **and** at least **0.25 km²** in absolute terms. Macchia (323) and regrowth (324) do not
count towards the mask, but they are kept as habitat fractions because ovoli and *B. aereus* rules
use them. The absolute floor stops border and island slivers from qualifying on a few hectares
(228 cells would otherwise).

Threshold sensitivity. 0.5 is the built count; the other columns are recomputed from the stored
fractions and may be off by a few cells:

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 13,849 | 12,284 | **10,778** | 9,213 | 7,588 |

50 % matches the PRD's "mostly forest" and its ~12k estimate. All cells keep `forest_fraction`, so
M3 can change the threshold without rebuilding: only `woodland` and the map export depend on it.

Implementation: land-cover polygons are rasterized at 20 m onto the grid (2,500 pixels per cell)
and counted per cell. Rasterized totals match the vector areas to within 41 ha for all of Tuscany.

## Habitat per cell

The vocabulary is the one the species rules were drafted with, now owned by
`api/src/api/config/habitats.yaml` (a test checks that every species rule in
`api/src/api/config/species/` scores exactly this vocabulary). Each habitat belongs to a broad group:

| group (UCS 2019) | habitats (CLC 2018 IV level) |
|---|---|
| broadleaf (311) | `evergreen_oak` 3111, `deciduous_oak` 3112, `mixed_broadleaf` 3113, `chestnut` 3114, `beech` 3115, `riparian` 3116, `exotic_broadleaf` 3117 |
| conifer (312) | `mediterranean_pine` 3121, `mountain_pine` 3122, `fir_spruce` 3123, `other_conifer` 3124, 3125 |
| mixed (313) | `mixed_broadleaf_conifer` |
| macchia (323) | `macchia` |
| transitional (324) | `transitional_woodland_shrub` |

For each cell:

1. UCS gives each group's share of the cell.
2. Broadleaf and conifer shares are split among their habitats in proportion to the CLC types of
   that group **in the cell**. If the cell has none, the types in the surrounding 5 × 5 cells are
   used, then 11 × 11. If there are still none, the group falls back to its generic habitat
   (`mixed_broadleaf`, `other_conifer`). Single-habitat groups map directly.
3. Fractions are normalised over the cell's wooded area (forest + macchia + regrowth), so they sum
   to 1. A rule's habitat factor is Σ fraction × affinity; the cell's forest share is a separate
   column.

Results on the 10,778 woodland cells:

| habitat | share of wooded area | cells where dominant | mean elevation of those cells |
|---|---|---|---|
| deciduous_oak | 36.1 % | 4,368 | 457 m |
| chestnut | 18.7 % | 2,062 | 651 m |
| evergreen_oak | 12.9 % | 1,450 | 248 m |
| beech | 8.5 % | 949 | 1,106 m |
| mixed_broadleaf_conifer | 7.8 % | 761 | 390 m |
| mixed_broadleaf | 4.9 % | 543 | 615 m |
| transitional_woodland_shrub | 3.4 % | 10 | 748 m |
| mediterranean_pine | 3.0 % | 300 | 226 m |
| mountain_pine | 1.8 % | 127 | 814 m |
| exotic_broadleaf | 1.0 % | 118 | 395 m |
| fir_spruce | 0.6 % | 39 | 1,088 m |
| other_conifer | 0.6 % | 25 | 507 m |
| macchia | 0.4 % | 4 | 345 m |
| riparian | 0.2 % | 22 | 294 m |

- The elevation order (evergreen oak and pines low, chestnut in the hills, beech and fir at
  1,100 m) is what the Tuscan forest belts should look like.
- The dominant habitat covers a median 89 % of the wooded area.
- `borrowed_type_fraction` is 0 for most woodland cells (mean 4.7 %). 357 cells take more than half
  their type from neighbours or the fallback. These are small woods that CLC's 25 ha unit does not
  map.

## Terrain

- **Source.** Copernicus DEM GLO-30 (1 arcsecond COGs on AWS open data), warped bilinearly to 25 m
  on the grid. Slope and aspect are computed per pixel in metres, then reduced per cell. Pixels
  outside the region are dropped.
- **Surface model caveat.** GLO-30 includes part of the canopy, so woodland heights read maybe
  10–20 m high. That is negligible against altitude bands hundreds of metres wide. TINITALY 1.1
  (INGV, 10 m bare ground, CC BY 4.0, scriptable tile zips and WCS) is a drop-in swap if a rule ever
  needs it.
- **Flat pixels.** Slopes under 2° have no aspect. `aspect_deg` is null when the mean aspect vector
  is shorter than 0.1 (flat, or ridges facing both ways): 383 woodland cells.
- **Woodland cell summary.** Elevation median 469 m (max 1,652 m), slope median 16.6°, northness
  centred on 0.
- **Coverage.** 20 cells, all slivers smaller than a DEM pixel, have no terrain.

## Soil pH (optional item: done, because it was cheap)

- **Source.** SoilGrids 2.0 pH in water (ISRIC, 250 m, CC BY 4.0), fetched with three WCS requests
  (0–5, 5–15, 15–30 cm) over the region's bbox.
- **Method.** Each layer's cell mean (nearest resampling to 125 m, SoilGrids' 0 = no data) is
  weighted by layer thickness.
- **Result.** Woodland cells: median pH 6.64 (5.44–7.66). The lowest medians sit under fir (5.94)
  and beech (6.04), the highest under deciduous oak (6.84) and riparian woods (7.11). The ordering
  is plausible, but SoilGrids is modelled with wide uncertainty, so treat it as a hint.
- **Status.** Not used by the v1 rules (`soil_ph` is still a `missing` attribute in the rule
  schema). M3 can enable a gallinacci acidity rule and let the backtest decide.
- **Alternatives if SoilGrids proves too coarse.** The Regione Toscana pedological map, or a
  lithology layer (calcareous share per cell from the regional geological database). Either one is
  a new reader plus a `class_fractions` call.

## Place labels

- **Comune.** From ISTAT 2025 generalised boundaries: the comune covering the largest share of the
  cell. All 273 Tuscan comuni get cells; 5 coastal slivers fall outside every comune polygon.
- **Nearest locality.** From ISTAT Basi territoriali 2021 locality points, types 1 (centro abitato)
  and 2 (nucleo abitato), measured from the cell centre. Places up to 0.1° outside the region
  count, so border cells can take a neighbouring village.
  - Median distance 1.3 km; max 35 km (uninhabited islands).
  - ISTAT was chosen over GeoNames because GeoNames gives English exonyms for big towns
    ("Florence") and is untyped. ISTAT names are official Italian, typed, and share the comuni's
    licence.

## Sanity check

`api/tests/grid/test_tuscany_grid_data.py` re-runs these checks against the built grid. It is
skipped when the grid is not built, e.g. in CI. All 15 pass.

- Cell count 23,803; inside area = region area within 0.1 %.
- Woodland cells 10,778, within the expected 10,000–12,500.
- Forest area within 5 % of INFC 2015 (+2.2 %).
- Habitat fractions sum to 1 in every cell.
- Monte Amiata summit cell tops out at 1,730 m (summit 1,738 m).
- Spot checks:

| place | cell | woodland | forest | top habitats | elev. m | slope ° | pH | comune | nearest locality |
|---|---|---|---|---|---|---|---|---|---|
| Casentino, Camaldoli | `1kmE4467N2301` | yes | 0.92 | mixed_broadleaf_conifer 0.49, fir_spruce 0.39, beech 0.10 | 1061 | 20 | 5.9 | Poppi (AR) | Convento Camaldoli, 1.5 km |
| Casentino, Badia Prataglia | `1kmE4471N2300` | yes | 0.93 | fir_spruce 0.46, beech 0.33, mixed_broadleaf_conifer 0.22 | 1054 | 18 | 6.1 | Poppi (AR) | Fiume d'Isola, 0.7 km |
| Amiata, summit | `1kmE4453N2199` | yes | 0.93 | beech 1.00 | 1549 | 18 | 6.1 | Castel del Piano (GR) | Rifugio Cantore, 1.3 km |
| Amiata, chestnut belt above Castel del Piano | `1kmE4450N2199` | yes | 0.99 | chestnut 1.00 | 1052 | 15 | 6.3 | Castel del Piano (GR) | Collevergari, 2.0 km |
| Garfagnana, Orecchiella | `1kmE4350N2343` | yes | 0.51 | beech 0.34, transitional_woodland_shrub 0.23, mountain_pine 0.18 | 1175 | 17 | 5.9 | Villa Collemandina (LU) | Sulcina, 1.0 km |
| Garfagnana, chestnut slopes near Castelnuovo | `1kmE4356N2334` | yes | 0.71 | chestnut 0.97, transitional_woodland_shrub 0.03 | 320 | 25 | 6.7 | Pieve Fosciana (LU) | Volcascio, 0.6 km |
| Vallombrosa | `1kmE4446N2292` | yes | 0.82 | fir_spruce 0.95, beech 0.02, deciduous_oak 0.02 | 1057 | 17 | 5.9 | Reggello (FI) | Vallombrosa, 0.3 km |
| San Rossore pine woods | `1kmE4345N2290` | yes | 0.97 | mediterranean_pine 0.95, mixed_broadleaf_conifer 0.05 | 8 | 5 | 6.8 | Pisa (PI) | Cascine Nuove, 4.7 km |
| Maremma, Monti dell'Uccellina | `1kmE4412N2169` | yes | 1.00 | evergreen_oak 1.00 | 221 | 17 | 6.5 | Magliano in Toscana (GR) | Stazione di Alberese, 2.3 km |
| Pisa (city) | `1kmE4353N2289` | no | 0.00 | transitional_woodland_shrub 1.00 (a scrap of scrub) | 9 | 5 | — | Pisa (PI) | Pisa, 0.5 km |
| Firenze (city) | `1kmE4422N2296` | no | 0.00 | — | 60 | 7 | — | Firenze (FI) | Firenze, 1.4 km |

- The comuni with the most beech-dominated woodland cells are Sambuca Pistoiese, Firenzuola,
  Pontremoli, San Godenzo and Abetone Cutigliano, all on the Apennine ridge.
- Correction during the check: my first "Amiata chestnut" coordinate landed on farmland at 505 m
  below Castel del Piano. It was moved to the chestnut slopes at ~1,000 m, where the grid has 67
  chestnut-dominated woodland cells around the mountain.

## Known gaps and hand-offs

- **Acidophilous forest sub-types** (castagneto acidofilo, cerreta acidofila) are not in any current
  open map. Swap in the regional Carta delle Categorie Forestali when LaMMA publishes it: map its
  categories to habitats in the region config, with new habitat keys if the rules want the
  sub-types.
- **Chestnut orchards vs coppice** (the ovoli appendix suggests 1.0 vs 0.7 affinity) are not
  separated by CLC or UCS.
- **Porcini 100 m wood-edge rule** is not computed. The cell table has `wooded_fraction`, and the
  land-cover rasterization could add an edge-length or edge-buffer share per cell if M3 wants it.
- **M3 · Model v1.** Habitat fractions are shares of the wooded area, not of the cell. If sparse
  woodland should score lower, multiply by `forest_fraction` in the rule, not in the grid.
  `soil_ph`, `aspect_deg` and `northness` are ready for rules that are currently disabled.
- **M2 · Weather ingest.** Downscale to cell centres (`lon`, `lat`) and adjust temperature by
  `elevation_m`. Only woodland cells need scores.
- **M4/M5 · Map delivery.** GeoJSON of woodland cells is 274 KB gzipped. Scores can ship as a
  separate `{cell_id: score}` payload joined on `id`, so the geometry is cached once.
- **Data refresh.** Delete a file under `api/data/raw/` to re-download it. UCS is updated roughly
  every three years; point `class_column` at the new year.

### Adding a region

1. Write `api/src/api/config/regions/<region>.yaml` with the ISTAT region code, bbox, and
   (optionally) a regional forest source.
2. **Forest groups.** Point `forest.groups` at a vector source declared in `sources.yaml`
   (`source`, `class_column`, `classes` mapping land-cover codes → broadleaf / conifer /
   mixed / macchia / transitional). Supported downloads: zip shapefile, GeoPackage, a named
   layer inside a zip, ArcGIS REST, WFS. Legacy `year_column` is still accepted as an alias
   for `class_column`. **Omit `forest.groups`** to derive groups from CLC IV alone (311x →
   broadleaf, 312x → conifer, 313x → mixed, 3231/3232 → macchia, 324x → transitional).
3. **Forest types.** `forest.types` names the CLC (or equivalent) source and, when needed,
   `classes` mapping type codes → habitats. If `classes` is omitted, the shared CLC IV
   defaults are used (`api.grid.forest.CLC_IV_DEFAULT_TYPES`).
4. The build prints the region's forest area against the INFC 2015 "bosco" figure in
   `api/src/api/config/infc2015.yaml` and warns when the difference exceeds ±10 %.
5. National raw files (ISTAT boundaries and localities, DEM tiles, CLC pages by bbox) are
   cached once under `$DATA_DIR/raw/` and reused across regions.
6. Run the build with `--region <region>`.

Example CLC-only neighbour (Umbria):

```yaml
forest:
  types:
    source: ispra_clc18_iv
```

Example with a regional land-cover map (Tuscany):

```yaml
forest:
  groups:
    source: rt_ucs
    class_column: ucs19
    classes: {"311": broadleaf, "312": conifer, "313": mixed, "323": macchia, "324": transitional}
  types:
    source: ispra_clc18_iv
    classes: { ... CLC IV → habitat ... }
```

## Sources and licences

| source | licence | attribution |
|---|---|---|
| ISTAT, Confini delle unità amministrative 2025 | CC BY 4.0 | Confini amministrativi © ISTAT |
| ISTAT, Basi territoriali 2021, località | CC BY 4.0 | Località © ISTAT |
| Regione Toscana, Uso e copertura del suolo 2007–2019 | CC BY 4.0 | Uso e copertura del suolo © Regione Toscana |
| ISPRA, Corine Land Cover 2018 IV livello | CC BY 4.0 | Corine Land Cover 2018 IV livello © ISPRA |
| Copernicus DEM GLO-30 | Copernicus DEM licence | Produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved |
| SoilGrids 2.0 (ISRIC) | CC BY 4.0 | SoilGrids © ISRIC — World Soil Information |

The same list, with homepages and download details, is in `api/src/api/config/sources.yaml` and is
copied into each build's `meta.json` for the app's credits page.

Reference figures: INFC 2015 tables (2022 release), inventarioforestale.org; Regione Toscana,
Rapporto sullo stato delle foreste in Toscana 2019; UCS metadata and specifications, Regione Toscana
GeoNetwork; CLC IV level, ISPRA SINAnet; LaMMA, Carta delle Categorie Forestali technical
specifications.
