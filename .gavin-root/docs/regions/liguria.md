# liguria

Region #2 of the full-Italy rollout (card `region-liguria.md`). API id `liguria`, web slug
`/liguria`, ISTAT COD_REG 7, Wikidata Q1256. Config: `api/src/api/config/regions/liguria.yaml`.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Liguria, **Tipi forestali della Regione Liguria sc. 1:10.000, ed. 2025** (`rl_tipi_forestali`) | CC BY 4.0 (metadata `r_liguri:D.2661`) | WFS `geoservizi.regione.liguria.it/geoserver/M2661/wfs`, layer `M2661:L10450` |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 96906 "Liguria, IT" | per record | counts per cell only |

Why the regional map and not CLC IV alone: Liguria publishes an open, current forest-type map at
1:10,000 (0.5 ha minimum unit), photo-interpreted from AGEA 2019 and 2022 orthophotos and
Sentinel-2 with the IPLA forest-type legend. Its 52,044 polygons carry, on one layer:

- `cod_uso`: the 2025 land-use code (the national Corine-style legend to level III, with Liguria's
  own level IV: **3114 is beech and 3115 chestnut here**, unlike CLC IV);
- `cod_catfor` / `cod_tipofo`: the IPLA forest category and type on wooded land.

So one source gives both the broad groups (`cod_uso`) and the forest types (`cod_catfor`), read
once. GeoServer caps a GetFeature at 5,000 features, so the WFS reader pages it (`page_size` +
`sort_by`). The older editions (Tipi forestali 1:25,000 ed. 2013, Uso del suolo 2019 and 2024) are
superseded by the 2025 pair (Uso del suolo 2025 is the same polygons, WFS `M2660`).

Class mapping (`liguria.yaml`):

| `cod_uso` | group | | `cod_catfor` (IPLA) | habitat |
|---|---|---|---|---|
| 3111–3117 | broadleaf | | CA castagneti | chestnut |
| 312 | conifer | | FA faggete | beech |
| 313 | mixed | | QU querceti, CE cerrete | deciduous_oak |
| 323 | macchia | | LE leccete (and sugherete) | evergreen_oak |
| 324 | transitional | | OS orno-ostrieti, LM carpineti / acero-frassineti | mixed_broadleaf |
| | | | FR formazioni riparie | riparian |
| | | | PC pinete di pino marittimo e d'Aleppo | mediterranean_pine |
| | | | PM pinete di pino silvestre (and a little uncinato) | mountain_pine |
| | | | AB abetine | fir_spruce |
| | | | LC lariceti, RI rimboschimenti | other_conifer |

Unmapped categories sit outside forest land use: AM (montane shrub), BS (robinieti and invasion
scrub, all on 324 regrowth), MM (macchia, on 323), CP, NA. RI (plantations, mostly black pine) goes
to `other_conifer` as CLC's 3124/3125 do; a type-level split (`cod_tipofo`) would send RI20A to
`mountain_pine`, 2,151 ha, not worth the extra mapping.

## Woodland grid

Built 2026-09-25 (`uv run python -m api.grid.build --region liguria`, 104 s with a warm cache).

- Cells 5,883; inside area 5,422 km² (ISTAT 5,416 km²).
- **Woodland cells 3,952**; all 234 comuni get cells; 4 coastal slivers fall outside every comune.
- **Forest area 352,119 ha vs INFC 2015 bosco 343,160 ha: +2.6 %** (within ±10 %). Forest is
  land use 311x + 312 + 313; adding 324 regrowth (22,800 ha) would overshoot to about +9 %, which is
  why regrowth stays a habitat and not woodland, as in Tuscany.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0):
  the 1:10,000 map leaves no gaps, unlike CLC's 25 ha unit in Tuscany. The dominant habitat covers a
  median 61 % of a cell's wooded area (Tuscany 89 %): Ligurian woods are finer-grained mixes.
- Terrain: woodland elevation median 575 m, max 1,845 m; slope median 22.7° (Tuscany 16.6°);
  108 cells have no aspect (flat or two-way ridges); 13 slivers have no terrain.
- Soil pH (SoilGrids, not scored): woodland median 6.35 (5.81–7.00, 5th–95th percentile).

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| chestnut | 28.3 % | 1,265 | 564 m |
| mixed_broadleaf (mostly hop-hornbeam) | 15.9 % | 646 | 571 m |
| mixed_broadleaf_conifer | 14.4 % | 589 | 444 m |
| beech | 11.5 % | 524 | 1,035 m |
| deciduous_oak | 11.2 % | 413 | 526 m |
| mediterranean_pine | 4.6 % | 180 | 339 m |
| evergreen_oak | 4.5 % | 181 | 344 m |
| transitional_woodland_shrub | 4.0 % | 10 | 770 m |
| other_conifer | 2.2 % | 64 | 985 m |
| mountain_pine | 1.7 % | 57 | 1,075 m |
| macchia | 1.2 % | 18 | 350 m |
| riparian | 0.2 % | 0 | |
| fir_spruce | 0.1 % | 5 | 1,207 m |

Woodland cells by province: Genova 1,361, Savona 1,241, Imperia 719, La Spezia 631.

Threshold sensitivity (recomputed from stored fractions, a few cells off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 4,576 | 4,307 | **3,940** | 3,458 | 2,887 |

## Weather

- Points: 57 candidates on the 0.2° lattice, **38 on land**; all 3,952 woodland cells weighted.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region liguria`,
  106 land nodes at 0.1°, three 14-day windows of 2024). Cooling per km of height across nodes,
  median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 4.06 | 3.32 | 4.07 | 3.71 | 4.5 | −0.79 |
  | temperature_2m_mean | 5.20 | 3.99 | 4.68 | 4.53 | 4.5 | +0.03 |
  | temperature_2m_min | 5.81 | 4.52 | 4.90 | 4.92 | 4.2 | +0.72 |
  | soil_temperature_0_to_7cm_mean | 3.76 | 3.57 | 3.85 | 3.72 | 3.7 | +0.02 |

  Every fitted rate is within 1 °C/km of the national one, so **the national lapse rates are kept**
  (no `model:` or weather override). Leave-out test on the 0.2° lattice (stride 2), RMSE with the
  national rates vs none vs 6.5 °C/km: mean air temperature 0.40 / 0.97 / 0.46 °C, minimum
  0.58 / 1.10 / 0.55 °C, soil 0.41 / 0.87 / 0.52 °C; wet-day rain RMSE 2.1 mm either way.
- **Rain scale.** The national `precipitation_scale` (1.28 + 0.29 per km, fitted on SIR Toscana
  gauges) applies; see Validation for the gauge check.

## Sightings

`uv run python -m api.sightings.ingest fetch --region liguria` (2026-09-25): 148 GBIF records and
1 recent iNaturalist record for the three groups over the bbox; 112 pass the quality filters (37
too imprecise, 18 with unknown uncertainty, 1 undated); **46 land on Liguria's woodland cells**
(66 are off the woodland grid: outside the region inside the bbox, or on non-woodland cells).

## Known limitations

- The web registry finds a region by bbox (`findRegionAt`), and Liguria's bbox overlaps Tuscany's
  around La Spezia and the Lunigiana border. The current region is checked first, so inside
  `/liguria` a point near La Spezia opens Liguria's forecast; from the hub or another region the
  switch offer names the first match in registry order (Tuscany). A boundary-polygon lookup would
  fix it for every pair of neighbours.
