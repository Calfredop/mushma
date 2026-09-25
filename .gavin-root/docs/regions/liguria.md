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
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-14, with snowfall from Italy-wide half-year files of the gridded dataset
  shared by every region (`cds.snowfall_area`); Open-Meteo's archive and ECMWF IFS forecast fill
  the days after.
- **Rain scale: Liguria's own** (`model:` in `liguria.yaml`), from the gauge check below.

### Gauge check (ARPA Liguria)

ARPAL publishes the OMIRL network's daily rain free for "consultazione o elaborazioni automatiche"
(citing ARPAL), through Regione Liguria's Ambiente in Liguria extraction service: one CSV per year
with every station. Station positions come from OMIRL's REST station list, joined by code and name
(`api.weather.arpal`, wired into `api.weather.checks gauges` as the Liguria gauge network). A daily
value is a UTC day (checked against the hourly values of one station), so the model's local days
are re-cut by the Rome offset. 172 gauges get a position; 84 sit on woodland cells.

Downscaled **raw** CDS rain against the woodland gauges (pooled model/gauge ratio):

| period | gauges | all | below 400 m | 400–800 m | above 800 m | median daily r | 3-day ≥ 10 mm hit / false alarm |
|---|---|---|---|---|---|---|---|
| 2025 | 84 | 0.785 | 0.833 | 0.810 | 0.681 | 0.77 | 0.83 / 0.14 |
| 2019–2025 | 79 | 0.879 | 0.918 | 0.906 | 0.767 | 0.76 | 0.84 / 0.12 |

The reanalysis is too dry in the hills, as in Tuscany, but less so. The national scale
(1.28 + 0.29 per km, fitted on Tuscan `era5_seamless` rain in 2025) would make Liguria's rain
**26 % too wet** over 2019–2025 (13 % in 2025), so the gauge check asks for an override.
Least squares through the origin of gauge totals on model totals × (a + b × km), the Tuscan
method:

| fit | a | b per km | pooled on 2019–2025 | by band (< 400 / 400–800 / > 800 m) |
|---|---|---|---|---|
| 2019–2025 (**used**) | 1.04 | 0.20 | 1.005 | 0.99 / 1.04 / 0.96 |
| 2019–2024, checked on 2025 | 1.01 | 0.20 | 0.88 on 2025 | 0.88 / 0.91 / 0.83 |
| national | 1.28 | 0.29 | 1.26 (2025: 1.13) | 1.23 / 1.30 / 1.21 |

The ratio moves about 10 % from year to year (2025 was a dry year for the model), so the seven-year
fit is used. It scales totals: timing errors and missed convective cells stay (median daily
correlation 0.76).

**Foundation issue found here.** The national scale lists `sources: [era5_seamless]`, and
`api.model.inputs` scales rain only from those sources but scales the rain normals whatever their
source. For a CDS region, history rain would stay unscaled while `percent_of_normal` divides by
scaled normals (reading ~30–40 % low). Liguria's override names `era5_land_cds` too. Other CDS
regions, and Tuscany's 2024 CDS rows, need the same thought (Emilia-Romagna and Umbria lanes told).

## Sightings

`uv run python -m api.sightings.ingest fetch --region liguria` (2026-09-25): 148 GBIF records and
1 recent iNaturalist record for the three groups over the bbox; 112 pass the quality filters (37
too imprecise, 18 with unknown uncertainty, 1 undated); **46 land on Liguria's woodland cells**
(66 are off the woodland grid: outside the region inside the bbox, or on non-woodland cells).

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/liguria.md`; rules in
`api/src/api/config/species/liguria/` (14 new references, all verified).

- **All three groups kept.** Ovoli are the least common but clearly present: the Beigua park names
  "porcini ed ovoli" as its hinterland's mushrooms, the regional law (L.R. 17/2014) sets a separate
  1 kg limit for them, and iNaturalist holds 24 Ligurian ovoli against 31 porcini.
- **Changed from Tuscany: where the hosts are.** *B. edulis* altitude band starts at 150→450 m
  (Tuscany 200→700 m) and *B. pinophilus* at 250→600 m (300→800 m): Ligurian beech grows from about
  500 m and chestnut from 300 m. Eight habitat affinities follow what Liguria's classes hold:
  `other_conifer` (black pine, Douglas fir plantations) up for *edulis*, *reticulatus* and
  *pinophilus*; `mediterranean_pine` (maritime pine) up for *edulis*, *pinophilus* and gallinacci;
  `mountain_pine` (Scots pine) to 1.0 for *pinophilus*; `mixed_broadleaf_conifer` (here chestnut or
  oak with pine, not beech with fir) up for *aereus* and ovoli.
- **Unchanged: season windows, weather rules, stoppers, growth clocks.** No Ligurian or NW-Apennine
  source gives weather numbers; the one Ligurian plot study (Sassello 2012–2014) found no climate
  effect at plot scale.
- **Open questions.** The `slope` and `sun_exposure` stoppers were anchored on Tuscan grid
  percentiles, and Liguria's woods are steeper (median slope 22.7° against 16.6°). The slope stopper
  (×1 to 25°, ×0.8 from 40°) touches 34 % of Ligurian woodland cells against 13 % in Tuscany, but its
  mean factor is only 0.985 (Tuscany 0.994; 10th percentile 0.94), so it was left alone. Intense
  autumn storms saturate the 30 mm rain trigger, and no source gives a "too much rain" threshold.
- **Press contrasts** (`liguria/sanity.yaml`): 11, written before any Liguria score existed, 9 for
  porcini, 1 for ovoli (id `ovoli_…`) and 1 for gallinacci (id `gallinacci_…`). The sanity check
  scores one group per run (`--group`), so each contrast is read against its own group below.

## After the deploy: what to verify

The stores are rsync'd to the server before the PR; the API serves Liguria once main (with
`config/regions/liguria.yaml`) is redeployed by the rail's "Deploy pulled main" step. Then check:

- [ ] `https://mappafunghi.app/liguria` and `/liguria/porcini`, `/liguria/ovoli`,
  `/liguria/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Ligurian habitats.
- [ ] `https://api.mappafunghi.app/regions` lists `liguria`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Liguria URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/liguria` (prerendered title, description, canonical, og image
  `og/liguria.png`, JSON-LD Dataset with `sameAs` Wikidata Q1256).
- [ ] `/credits` shows "Regione Liguria — Tipi forestali e uso del suolo 2025".
- [ ] The next morning's daily job has a `region_done` line for `liguria`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- The web registry finds a region by bbox (`findRegionAt`), and Liguria's bbox overlaps Tuscany's
  around La Spezia and the Lunigiana border. The current region is checked first, so inside
  `/liguria` a point near La Spezia opens Liguria's forecast; from the hub or another region the
  switch offer names the first match in registry order (Tuscany). A boundary-polygon lookup would
  fix it for every pair of neighbours.
