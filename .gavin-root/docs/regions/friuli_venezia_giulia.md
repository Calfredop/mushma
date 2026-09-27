# Friuli-Venezia Giulia

Region card: `region-friuli-venezia-giulia.md` (region #11 of `feat-full-italy-coverage.md`). API id
`friuli_venezia_giulia`, web slug `/friuli-venezia-giulia`, ISTAT COD_REG 6, names "Friuli-Venezia
Giulia" / en "Friuli-Venezia Giulia". 7,920 km² (ISTAT 2025, Sappada included since 2017), 215
comuni in four former provinces (Udine, Pordenone, Gorizia, Trieste). From the sea to the Austrian and
Slovenian borders in about 100 km: the Karst above Trieste with downy oak, hop-hornbeam and the
black-pine plantations of the late 1800s; lowland oak-hornbeam relicts and the coastal woods of
Lignano; chestnut, sessile oak and robinia on the Collio and the moraine hills; the Carnic and Julian
Prealps, where beech is the most extensive forest, with native black and Scots pine on the dolomite
of the Val Cellina, Val Tramontina and Carnia; and spruce, silver fir, larch and spruce-fir-beech in
Carnia and the Val Canale around Tarvisio.

## Sources

**Decision: the Region's Tipologie forestali 2013, one map for both the groups and the types**
(`fvg_tipologie_forestali` in `api/src/api/config/sources.yaml`; IODL 2.0, "Tipologie forestali ©
Regione Autonoma Friuli Venezia Giulia"). Checked 2026-09-27:

| candidate | what it is | verdict |
|---|---|---|
| **Tipologie forestali 2013** (Regione FVG, Direzione centrale risorse agroalimentari, forestali e ittiche; IRDAT catalogue, WFS `IRDAT:TIPOLOGIE_FORESTALI_2013`) | The forest area typed with the regional typology (Del Favero et al., *La vegetazione forestale e la selvicoltura nella regione Friuli-Venezia Giulia*, 1998: 20 categories, 105 types and subtypes, 70 variants). It joins the "Tipi forestali 1998" survey (mountain area, hills and Karst, 1997–1999, updated 2010: 312,825 ha), the 2011 "Completamento del GIS dei Tipi forestali" (the lowland and hill woods it lacked, validated 2013: 11,009 ha) and the Sappada forest plan of 2017 (1,631 ha). 20,556 polygons, 325,467 ha. RNDT record `r_friuve:m2182-cc-i10191` (revised 2013-11-11): IODL 2.0 under DGR 2626/2014 (the Region's open-data rules, L.R. 7/2014), no limits on public access; WFS, shapefile and KML from IRDAT | **used** |
| Tipologie forestali (the 1998 layer, `IRDAT:TIPOLOGIE_FORESTALI`) | The 1997–1999 survey alone, "oltre 255 mila ettari" in its abstract, 19,388 polygons | superseded by the 2013 layer |
| PPR — Territori coperti da foreste e boschi (`PPR:v_territori_coperti_da_foreste_e_boschi`) | The landscape plan's forest limit, no forest type | no types; the 2013 map gives both |
| ISPRA CLC 2018 IV level | National fallback, 25 ha minimum unit | not needed: the regional map is open, finer and typed |

The map covers forest only, so one map gives both the broad groups (how much of each cell is
woodland) and the habitats (which kind), from the type code `CODICE_TIPO`. A code is the category
letter, the type and an optional lower-case variant (GH1a: *faggeta montana tipica esalpica*, variant
with silver fir). Plantations and new woodland carry what grows there over the site they sit on
(SN/GB0: spruce planted on a beech site; XE/DB0: *neocolonizzazione esalpica* heading for
hop-hornbeam) and are mapped by what grows there. The YAML lists all 412 codes in the map (typos
included: `Gl0`, `Hc1`, the lower-case categories `c`, `p`, `r`), each to a group and a habitat,
generated from per-category rules and checked against the downloaded polygons; a code the map adds
later would be dropped with its area, and the build's INFC check would show it. Three codes filed
under another category follow their category and name: `XD/CC0` (in I, a Scots pine wood),
`XD/CE0` (in Q, *Salix waldsteiniana* scrub) and `ST/GH2` (in L, a spruce-beech wood).

- **Not forest.** Mugo-pine krummholz (H *mughete*, 12,880 ha), green-alder scrub (PA0, 3,789 ha)
  and subalpine *Salix waldsteiniana* scrub (QA5, 288 ha) go to the transitional group, which does
  not count toward the woodland mask: INFC counts them as *arbusteti subalpini*, as in Trentino-Alto
  Adige and Piemonte.
- **Mixed.** Spruce-beech (L *piceo-faggeti*) and fir-spruce-beech (MB, MC, MD *abieti-piceo-faggeti*)
  go to `mixed` (`mixed_broadleaf_conifer`); fir and spruce-fir without beech (MA, ME–MI, ML) stay
  conifer.
- **Oak.** The *ostrio-querceti* (DC) are downy-oak woods with hop-hornbeam, the Karst's and the
  Prealps' warm slopes; they go to `deciduous_oak` with the *rovereti* (CA, CB) and the
  *querco-carpineti* (BA, BB). The *orno-ostrieti* (DB, DD) and the *carpineti* (BC–BF) go to
  `mixed_broadleaf`.
- **Black pine is native here** (I *pinete di pino nero*, 35,000 ha on the dolomite of the Carnic Prealps and Carnia) as well
  as planted on the Karst (SI *rimboschimenti di pino*); both go to `mountain_pine` with Scots pine.

| code family | ha | group | habitat |
|---|---|---|---|
| G faggete | 79,339 | broadleaf | beech |
| I pinete di pino nero e pino silvestre | 43,460 | conifer | mountain_pine |
| N peccete | 28,858 | conifer | fir_spruce |
| L piceo-faggeti | 27,306 | mixed | mixed_broadleaf_conifer |
| DC ostrio-querceti | 18,324 | broadleaf | deciduous_oak |
| DB, DD orno-ostrieti | 18,249 | broadleaf | mixed_broadleaf |
| CC–CF castagneti | 17,852 | broadleaf | chestnut |
| E aceri-frassineti, aceri-tiglieti | 14,401 | broadleaf | mixed_broadleaf |
| H mughete | 12,880 | transitional | transitional_woodland_shrub |
| MB, MC, MD abieti-piceo-faggeti | 11,534 | mixed | mixed_broadleaf_conifer |
| R robinieti, platano | 10,370 | broadleaf | exotic_broadleaf |
| MA, ME–MI, ML abieteti, piceo-abieteti | 7,840 | conifer | fir_spruce |
| X neocolonizzazioni (broadleaf) | 5,338 | broadleaf | mixed_broadleaf |
| O lariceti | 4,674 | conifer | other_conifer |
| PA0 alneta di ontano verde | 3,789 | transitional | transitional_woodland_shrub |
| SI rimboschimenti di pino | 3,659 | conifer | mountain_pine |
| J, T1–T4, U, PB, PC, QA2, QZ, XQ, AC riparian, terrace and marsh woods | 5,226 | broadleaf | riparian |
| CA, CB rovereti; BA, BB querco-carpineti | 2,793 | broadleaf | deciduous_oak |
| BC–BF carpineti; F betuleti, corileti; QA1, QD, T8, SU | 5,310 | broadleaf | mixed_broadleaf |
| SN rimboschimenti di abete rosso; XN | 1,895 | conifer | fir_spruce |
| ST, SO, S/ other conifer plantations; XO | 1,800 | conifer | other_conifer |
| A ostrio-lecceta, lecceta con pino nero | 250 | broadleaf | evergreen_oak |

Map areas by group, from the polygons: broadleaf 177,451 ha, conifer 92,210 ha, mixed 38,848 ha,
transitional (not forest) 16,957 ha; **forest (broadleaf + conifer + mixed) 308,510 ha** against
INFC 2015's 332,556 ha of *bosco* (−7.2 %). INFC 2015 predates Sappada's move from Veneto (2017), so
its figure leaves out Sappada's woods, which the map and the grid include; the gap would be a little
wider without them.

Credits: the map is added to the app's credits list (`web/src/credits.ts`).

## Config

`api/src/api/config/regions/friuli_venezia_giulia.yaml`:

- **Boundary.** ISTAT COD_REG 6; bbox `[12.32, 45.58, 13.92, 46.65]`, the ISTAT 2025 boundary's
  extent (12.3209, 45.5812, 13.9189, 46.6478) rounded outward to 0.01°. Region area 7,920 km².
- **Forest.** `forest.groups` and `forest.types` both on `fvg_tipologie_forestali`, class column and
  type field `CODICE_TIPO` (read once, one-map path), mapping above. The GeoServer answers the whole
  layer (79 MB of GeoJSON in EPSG:25833) in one GetFeature, so there is no paging.
- **iNaturalist place** 10869, "Friuli-Venezia Giulia, IT" (admin level 10), resolved by name on
  2026-09-27 (`api.inaturalist.org/v1/places/autocomplete?q=Friuli`).
- **Weather points.** 50 land nodes on the 0.2° lattice (54 candidates), every woodland cell within
  reach.

### Lapse rates (`api.weather.checks lattice --region friuli_venezia_giulia`)

122 ERA5-Land land nodes at 0.1° (−26 to 1,706 m), three 14-day windows of 2024 (Jan, Jul, Oct), run
2026-09-27. Cooling per km of height, median of the daily fits:

| variable | Jan | Jul | Oct | all | national config | difference |
|---|---|---|---|---|---|---|
| Tmin | 6.00 | 5.14 | 4.11 | **5.24** | 4.2 | **+1.04** |
| Tmax | 5.01 | 5.94 | 3.48 | **5.13** | 4.5 | +0.63 |
| Tmean | 5.57 | 5.74 | 3.84 | **5.25** | 4.5 | +0.75 |
| soil 0–7 cm | 0.22 | 5.35 | 3.58 | **3.58** | 3.7 | −0.12 |

Tmax, Tmean and soil are within 1 °C/km; **Tmin sits just over the line (+1.04)**, the same case as
Piemonte's Tmin (+1.04) and Trentino-Alto Adige's (+1.06). Above 500 m alone the fit is 5.22 / 5.35 /
5.50 / 3.80. **The national rates are kept**, because the leave-out test finds no gain from the
region's own rates on the lattice the app serves:

| leave-out RMSE | Tmin | Tmax | Tmean | soil |
|---|---|---|---|---|
| served lattice (0.2°, stride 2), national | 0.561 °C | 0.347 °C | 0.378 °C | 0.416 °C |
| served lattice, fitted (5.24 / 5.13 / 5.25 / 3.58) | 0.567 °C | 0.345 °C | 0.379 °C | 0.417 °C |
| stride 3 (0.3°), national | 0.813 °C | 0.570 °C | 0.581 °C | 0.667 °C |
| stride 3, fitted | 0.800 °C | 0.565 °C | 0.569 °C | 0.667 °C |

The fitted rates lose 0.006 °C for Tmin on the served lattice and gain at most 0.002 °C elsewhere.
Leave-out at the 0.2° lattice with no lapse correction: 0.73 / 0.62 / 0.63 / 0.59 °C (Tmin, Tmax,
Tmean, soil); with 6.5 °C/km 0.60 / 0.38 / 0.41 / 0.49 °C: the national rates are the best of the
three.

## Grid

`uv run python -m api.grid.build --region friuli_venezia_giulia` (55 s, the WFS layer, DEM tiles and
SoilGrids fetched):

- **Cells 8,297; woodland 3,304** (39.8 %). Threshold sensitivity (forest share of the cell, before
  the 0.25 km² floor): 0.3 → 3,909, 0.4 → 3,656, **0.5 → 3,388**, 0.6 → 3,077, 0.7 → 2,689. By
  former province: Udine 2,288 woodland cells, Pordenone 809, Trieste 135, Gorizia 72.
- **INFC 2015: −7.3 %** (grid 308,339 ha vs 332,556 ha bosco), inside ±10 %. The grid keeps the map's
  forest (308,510 ha); the gap is the map's, with the subalpine scrub left out as INFC leaves it (it
  would be −2.3 % with the mughete and green alder counted).
- **Habitats on woodland cells** (share of wooded area; cells where dominant; their mean height):

| habitat | share | dominant cells | mean elevation |
|---|---|---|---|
| beech | 26.9 % | 876 | 1,021 m |
| mountain_pine (black pine, Scots pine) | 15.8 % | 518 | 769 m |
| mixed_broadleaf (hop-hornbeam, ash-maple, hornbeam, new woodland) | 14.4 % | 472 | 621 m |
| mixed_broadleaf_conifer (spruce-beech, fir-spruce-beech) | 13.2 % | 468 | 1,175 m |
| fir_spruce (spruce, silver fir) | 12.3 % | 404 | 1,237 m |
| deciduous_oak (downy oak with hop-hornbeam, sessile oak, oak-hornbeam) | 6.1 % | 240 | 271 m |
| chestnut | 6.0 % | 209 | 396 m |
| exotic_broadleaf (robinia) | 1.9 % | 65 | 211 m |
| other_conifer (larch, conifer plantations) | 1.7 % | 40 | 1,388 m |
| transitional_woodland_shrub (mugo, green alder) | 1.5 % | 7 | 1,375 m |
| riparian | 0.2 % | 3 | 410 m |
| evergreen_oak (holm oak, Karst coast and Lignano) | 0.0 % | 2 | 63 m |

  The belts are in the right order: oaks on the Karst and in the lowland relicts at 270 m, robinia
  at 210 m, chestnut at 400 m, hop-hornbeam and the new woodland at 600 m, black and Scots pine at
  770 m, beech at 1,000 m, the spruce-beech and fir-spruce-beech woods at 1,200 m, spruce and fir at
  1,240 m, larch at 1,390 m. The dominant habitat covers a median 77 % of the wooded area (Trentino-Alto
  Adige 75 %, Piemonte 71 %). `borrowed_type_fraction` is 0 everywhere (groups and types come from
  the same map). Chestnut is well mapped here (17,852 ha, 209 cells where dominant), unlike
  Trentino-Alto Adige.
- **Terrain.** Woodland cells: median elevation 874 m, 95th percentile 1,524 m, max 1,898 m, min 6 m;
  699 cells up to 500 m, 1,317 at 500–1,000 m, 1,097 at 1,000–1,500 m, 191 at 1,500–2,000 m. Median
  slope 27.0°. All have terrain; 79 have no aspect.
- **Soil pH.** Median 5.56 (5th–95th percentile 5.12–6.19); lowest under the spruce-beech and
  spruce-fir woods (5.34–5.40), highest under the oaks and holm oak (6.15–6.37).
- **Places.** 215 comuni get cells (110 with woodland); 7 cells fall outside every comune polygon.
  Nearest locality median 1.6 km, max 9.3 km. Comune names are ISTAT's, bilingual on the Karst and
  the Collio (`Monrupino-Repentabor`, `San Floriano del Collio-Števerjan`).
- **Spot checks:**

| place | cell | woodland | forest | top habitats | elev. m | comune |
|---|---|---|---|---|---|---|
| Bosco di Fusine, Tarvisio | `1kmE4602N2603` | yes | 0.97 | mixed_broadleaf_conifer 0.87, fir_spruce 0.11 | 1020 | Tarvisio (UD) |
| Val Saisera slope | `1kmE4585N2600` | yes | 0.75 | beech 0.47, mixed_broadleaf_conifer 0.33 | 1443 | Dogna (UD) |
| Forni di Sopra | `1kmE4521N2594` | yes | 0.93 | fir_spruce 0.86, mixed_broadleaf_conifer 0.13 | 1534 | Forni di Sopra (UD) |
| Sauris | `1kmE4529N2597` | yes | 0.87 | mixed_broadleaf_conifer 0.69, beech 0.28 | 1207 | Sauris (UD) |
| Bosco di Ramaz above Paluzza | `1kmE4550N2607` | yes | 0.94 | fir_spruce 0.60, mixed_broadleaf 0.38 | 1122 | Cercivento (UD) |
| Piancavallo | `1kmE4516N2557` | yes | 0.86 | beech 1.00 | 1241 | Aviano (PN) |
| Val Cellina at Claut | `1kmE4513N2577` | yes | 0.72 | mountain_pine 1.00 | 789 | Claut (PN) |
| Val Tramontina | `1kmE4536N2580` | yes | 0.54 | mountain_pine 0.77, fir_spruce 0.23 | 380 | Tramonti di Sotto (PN) |
| Monte Matajur | `1kmE4592N2571` | yes | 0.79 | mixed_broadleaf 0.78, beech 0.22 | 1084 | Pulfero (UD) |
| Collio above San Floriano | `1kmE4599N2548` | yes | 0.50 | exotic_broadleaf 0.98, chestnut 0.02 | 190 | San Floriano del Collio-Števerjan (GO) |
| Black pine at Basovizza (Karst) | `1kmE4623N2510` | yes | 0.63 | mountain_pine 0.73, deciduous_oak 0.27 | 424 | Trieste (TS) |
| Monrupino (Karst) | `1kmE4617N2518` | yes | 0.88 | deciduous_oak 1.00 | 327 | Monrupino-Repentabor (TS) |
| Bosco Baredi (lowland oak) | `1kmE4563N2525` | yes | 0.52 | deciduous_oak 0.99 | 7 | Muzzana del Turgnano (UD) |
| Lignano coastal wood | `1kmE4562N2510` | yes | 0.59 | evergreen_oak 0.89, exotic_broadleaf 0.11 | 6 | Lignano Sabbiadoro (UD) |
| Udine (city) | `1kmE4571N2555` | no | 0.00 | — | 116 | Udine (UD) |
| Trieste (city) | `1kmE4615N2511` | no | 0.00 | — | 32 | Trieste (TS) |

## Weather history

From the Copernicus CDS, 2016-01-01 to 2026-09-16, through the ERA5-Land time-series product
(`cds.method: timeseries`): 50 node requests, none shared with an earlier region, fetched at about
40 s each (36 min on 2026-09-27, one 502 retried). **Snowfall** comes from the shared Italy-wide
gridded files (`sf_*_35.40_6.60_47.10_18.60`, 23 half-year files, all cached by earlier lanes); the
region's northernmost cells reach 46.65° N, well inside the files' 47.1° N edge.

**Open-Meteo.** The update step stored `era5_seamless` for 2026-09-13 to 09-21 and the forecast on
the morning of 2026-09-27, with 1,220 of the day's 10,000 shared calls spent by then.

## Data

- cells: 8297
- woodland cells: 3304
- INFC deviation: -7.3% (grid 308,339 ha vs 332,556 ha) — within ±10 %
- weather nodes: 50
- years stored: 2016–2026 (11 years)
- sightings kept: 7
- sanity contrasts: 12/16 passed (the onboard reads all 16 for porcini; with the ovoli and gallinacci
  contrasts read for their own groups, 11/16: Validation)


## Validation

### Rain gauges: not run, rain scale off

ARPA FVG publishes daily rain for about 60 priority stations through the OSMER archive
(`meteo.fvg.it/archivio.php`, "dati giornalieri"; the site's content is CC BY-SA 3.0 IT, credit
"ARPA FVG - OSMER e GRN"), and daily rain maps interpolated from 160+ stations (`raster.php`). Both
are served by the site's `ajax/*.php` endpoints, which on 2026-09-27 answered HTTP 400 to every
request: from a script, and from the site's own pages in a browser alike, all morning. The station
list (code, name, position, height, first year) is in the archive page itself; the data were not.
No other open daily rain covers the region's woods: GHCN-Daily has Rivolto and Trieste only, both
outside woodland, and the Slovene and Carinthian networks lie outside the grid. So there is **no FVG
gauge check**, and the follow-up card `fix-fvg-rain-gauge-check.md` holds the steps for when the
archive answers.

**The rain scale is off** (`model.precipitation_scale.enabled: false` in the region YAML, reference
`mushma_fvg_rain_unscaled_2026`): the CDS history, the Open-Meteo days and the rain normals all stay
as the reanalysis gives them. The national scale cannot stay as it is: it multiplies `era5_seamless`
only, while the normals are scaled whatever their source, so with this region's history from the
CDS it would scale the recent days and the normals and not the history. No bordering region has a
fit to borrow (Veneto is not done), and the Alpine fits on the same CDS rain disagree: ×0.74 in
Piemonte (97 gauges), ×0.75 in South Tyrol (17), ×0.96 in Lombardy (60, May–October). The Friulian
Prealps are the wettest part of Italy (over 3,300 mm a year at Musi), where a 0.1° reanalysis may
as well be too dry as too wet. Porcini's 30-day rain is scored against each cell's own normal and
does not depend on the scale; the 3-day triggers and the ovoli and gallinacci 30-day ramps do.

### Backtest (priors: rules version `8fbc20c567f2`)

Run 2026-09-27 on the stores above: the onboard's hold-out run (`backtest/friuli_venezia_giulia/onboard/`)
and the train seasons (`--seasons train --label onboard-train`). Scores cover 3,304 cells × 3,846
days of history (2016-03-18 to 2026-09-27) and the served window to 2026-10-04 (from the forecast
after 2026-09-21), none without weather.

**Usable presences (unique, unobscured group-cell-day sightings on woodland cells) in the train
seasons 2016–2023: 7** (porcini 4, gallinacci 3, ovoli 0; by year 2016: 2, 2018: 1, 2019: 1, 2021: 1,
2023: 2), far below the 50 the card asks before tuning. **Nothing is tuned: the researched priors
ship.** The hold-out 2024–2025 holds none. The fetch found 168 GBIF records of the six taxa in the
bbox (none from iNaturalist's recent window), 140 of them Austrian or Slovene (the bbox takes in a
strip of Carinthia and western Slovenia) and 28 Italian; 84 passed the quality filters (a date and a
precise enough position), and 77 of those fall outside the region's woodland cells. FVG has 3,172 iNaturalist fungi records in all, 14 of *B.
edulis* (species research, Sightings); the MUSE north-east census that places the species here is
undated.

| group | n | `auc_region` model | calendar | habitat | `auc_time_effort` model | calendar | `auc_local` model | habitat |
|---|---|---|---|---|---|---|---|---|
| porcini | 4 | 0.898 (0.83–0.97) | 0.780 | 0.507 | 0.799 (0.72–0.88) | 0.507 | 0.496 (0.39–0.59) | 0.503 |
| gallinacci | 3 | 0.863 (0.80–0.93) | 0.847 | 0.517 | 0.547 (0.31–0.78) | 0.602 | 0.462 (0.30–0.62) | 0.507 |

With 4 and 3 presences these are anecdotes, not measures. The four porcini finds sit in the
mountains in August and early October, where the model ranks them high against the whole region
(`auc_region` 0.90) and against the same cells' other days (`auc_time_effort` 0.80); within 20 km on
the day it does no better than habitat.

### Press contrasts (`sanity.yaml`, `backtest/friuli_venezia_giulia/onboard/sanity_*.csv`)

**11 of 16 hold**, each contrast read for its own group (the onboard's summary, 12/16, reads the
ovoli and gallinacci contrasts as porcini too). Weather columns: area means of the history tables'
unscaled rain and temperature over the contrast's window, weighted by woodland cells, with the 30
days before the window, against the 2016–2025 normals.

| contrast | group | higher | lower | holds |
|---|---|---|---|---|
| `carnia_vs_hills_2017` | porcini | 0.891 | 0.838 | yes |
| `carnia_vs_tarvisiano_2017` | porcini | 0.816 | 0.868 | no |
| `carso_2017_2016_autumn` | porcini | 0.983 | 0.580 | yes |
| `alps_2016_late_summer` | porcini | 0.671 | 0.790 | no |
| `alps_2020_2021_september` | porcini | 0.884 | 0.581 | yes |
| `alps_2021_august_vs_september` | porcini | 0.961 | 0.384 | yes |
| `alps_2023_2024_late_july` | porcini | 0.881 | 0.754 | yes |
| `alps_vs_hills_carso_october_2023` | porcini | 0.569 | 0.570 | no (a tie) |
| `carso_2023_2024_august` | porcini | 0.863 | 0.000 | yes |
| `carso_2023_august_vs_autumn` | porcini | 0.863 | 0.536 | yes |
| `region_2025_2024_early_august` | porcini | 0.846 | 0.520 | yes |
| `dolomiti_friulane_vs_giulie_july_2024` | porcini | 0.755 | 0.768 | no |
| `pordenone_vs_trieste_september_2023` | porcini | 0.712 | 0.708 | yes (narrowly) |
| `hills_2023_2017_early_august` | porcini | 0.721 | 0.490 | yes |
| `gallinacci_alps_2016_2021` | gallinacci | 0.920 | 0.930 | no |
| `ovoli_carso_2017_2016` | ovoli | 0.964 | 0.798 | yes |

- The Karst holds everywhere it is tested (the 2017 autumn against the 2016 drought, for porcini and
  ovoli; August 2023 against the heat of August 2024, 0.86 against 0.00; August 2023 against the dry
  foehn autumn), and so do the year contrasts in the Alps (2020 against 2021, August against
  September 2021, 2023 against 2024, 2025 against 2024), most by wide margins.
- **The misses, with the weather:**
  - `alps_2016_late_summer`: the press found no porcini below 1,500 m until about 1 September 2016.
    The reanalysis has the 30 days before the window (late May to 19 June) at 164 % of the normal
    rain, the window at 90 % and 0.3 °C cool; the rules reward the wet start, and nothing in them holds a
    flush back after it.
  - `carnia_vs_tarvisiano_2017`: the two areas had the same season in the reanalysis (window rain
    115 % and 113 % of normal, 1.4 °C and 1.3 °C cool); the ranking is the paper's subtitle, and its
    text names the Tarvisiano only for fly agarics.
  - `dolomiti_friulane_vs_giulie_july_2024`: the Julian Prealps failed from "too much" storm rain;
    the reanalysis gives them 130 % of normal in the 30 days before, which a rain rule reads as
    favourable, as Trentino-Alto Adige's `vallagarina_low_2024` found.
  - `alps_vs_hills_carso_october_2023`: a tie. The window was almost rainless everywhere (7 % and 1 %
    of normal) and 3–4 °C warm; the press's difference (flushes continuing in the high Alps, the
    Karst dried by the foehn) is not in the rain, and the Alpine season window, closing by 25
    October, costs the Alps what the drought costs the hills.
  - `gallinacci_alps_2016_2021`: nearly a tie (0.920 against 0.930). July-August 2021 was wet in the
    reanalysis (126 % of normal) after a dry June (51 %); the press's 2021 shortage is a
    whole-season verdict blamed on cold rain, wind and drought.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-27 (`deploy/rsync-region-data.sh
friuli_venezia_giulia`, 437 files, 211 MB, no redeploy). Checked right after the sync: `/regions`
lists the six live regions without this one, and `/status?region=friuli_venezia_giulia` answers 404.
The server serves a region only when its YAML is in the deployed code and its stores are on disk,
so they stay inert until `main` with `config/regions/friuli_venezia_giulia.yaml` is deployed by the
rail's "Deploy pulled main" step, with the daily job. The stores are scored through 2026-10-04 (the
served window of 2026-09-27, forecast from 2026-09-22), and the seasonal tendencies and outlook
were built the same morning. If the deploy comes after 2026-10-04 and before the daily job has run,
the hub's `/overview` needs the fix on `region/trentino-alto-adige` (`api/src/api/registry.py`: a
region not scored through the date is left out instead of failing the whole hub). Then check:

- [ ] The daily job after the deploy has a `region_done` line for `friuli_venezia_giulia`
  (`journalctl -u mushma-daily`), with the weather update filling from 2026-09-22 onward, the served
  window scored with factors, the seasonal fetch and the outlook built; its Open-Meteo call count
  stays inside the budget (this region adds 50 nodes).
- [ ] `https://mappafunghi.app/friuli-venezia-giulia` and `/friuli-venezia-giulia/porcini`,
  `/ovoli`, `/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names the region's habitats (beech, black and Scots pine, spruce-beech, spruce and fir,
  the Karst's downy oak).
- [ ] `https://api.mappafunghi.app/regions` lists `friuli_venezia_giulia` with all three species;
  the hub `/` lists it and colours it from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Friuli-Venezia Giulia URLs (built from the
  registry; the local build has them).
- [ ] Lighthouse SEO is 100 on `/friuli-venezia-giulia` (prerendered title, description, canonical,
  og image `og/friuli-venezia-giulia.png`, JSON-LD Dataset with `sameAs` Wikidata Q1250).
- [ ] `/credits` shows "Regione Autonoma Friuli Venezia Giulia — Tipologie forestali 2013" (IODL 2.0).
- [ ] The next morning's daily job has a `region_done` line for `friuli_venezia_giulia` again, and no
  `region_failed`.

## Known limitations

- **No rain gauge check; rain scale off.** ARPA FVG's archive answered HTTP 400 on the day
  (Validation). Whether the reanalysis is too wet or too dry here is unknown, and the Friulian
  Prealps are where it matters most. Follow-up: `fix-fvg-rain-gauge-check.md`.
- **Almost no dated sightings.** 7 usable presences in 2016–2023 and none in 2024–2025; the backtest
  cannot measure anything, and the validation rests on 16 press contrasts, 10 of them from one
  magazine's bulletins. The MUSE census that places the species here is undated; the Federazione
  dei Gruppi Micologici del FVG keeps the records behind it (species research, Open questions).
- **An older forest map.** The Tipologie forestali join a 1997–1999 survey (updated 2010) and a
  2011–2013 completion of the lowland woods: older than Piemonte's and Liguria's 2025 maps. Woods
  grown since, on abandoned meadows above all, are missing; the grid's forest is 7.3 % below INFC
  2015 (2.3 % with the mugo and green-alder scrub counted).
- **Black pine.** 15 % of the woods, three quarters of it black pine, which the species research
  made marginal for *B. edulis* on Karst evidence; the native pinewoods of the Prealps are not
  studied (species research, Open questions). The Dolomiti Friulane contrast missed narrowly.
- **The Karst's drainage and wind.** Thin limestone soil, the bora and the foehn dry the Karst
  faster than the rain rules assume; the drying-wind gap named by earlier regions fits the Karst
  best.
- **Region finder by bbox.** The web registry finds a region by bbox (`findRegionAt`). This bbox
  (12.32–13.92° E, 45.58–46.65° N) takes in western Slovenia (Nova Gorica, Tolmin, Kobarid, Bovec),
  a strip of Carinthia, Veneto's eastern plain and the Alpago; and Trentino-Alto Adige's bbox, on its
  own branch, reaches 12.48° E, so Erto e Casso and Cimolais fall inside both. Added to
  `fix-region-lookup-by-boundary.md`.
- **Lapse rates.** Minimum temperature cools 1.04 °C/km faster with height than the national rate,
  without a measurable downscaling gain from the region's own (Config, Lapse rates).
