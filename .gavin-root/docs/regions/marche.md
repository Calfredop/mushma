# marche

Region #5 of the full-Italy rollout (card `region-marche.md`). API id `marche`, web slug
`/marche`, ISTAT COD_REG 11, Wikidata Q1279. Config: `api/src/api/config/regions/marche.yaml`.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Marche, **Rete Ecologica Marche (REM), Vegetazione naturale 1:50.000**, edition of March 2019 (`rm_rem_vegetazione`) | open by default (CAD art. 52 c. 2), reused as CC BY 4.0 | zip shapefile on `static.regione.marche.it` (REM "Cartografia .shapefile" page) |
| forest-area cross-check | Regione Marche, Carta dell'uso del suolo 1:10.000, 2007 (CUS 2007) | CC BY 4.0 (open-data portal) | Corine level 2 only; not used by the build |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 7029 "Marche, IT" | per record | counts per cell only |

**What was checked, and why REM.**

- **Inventario e Carta Forestale della Regione Marche** (IPLA, 2000–2001, the card's candidate):
  published only as PDF sheets at 1:25,000 and 1:100,000 (`regione.marche.it/Portals/0/Agricoltura/
  foreste/cartografia/`, `LEGGIMI.TXT` lists them). No vector download, WMS or WFS: the region's
  GeoServer (`wms.cartografia.marche.it`) serves orthophotos, CTR, geology, boundaries and
  landslides, nothing forestal.
- **Carta Forestale d'Italia CFI2020** (CREA / MASAF, 1:10,000, INFC categories): shapefiles only
  on request by e-mail, two regions at a time, after registration. Not scriptable.
- **Carta dell'uso del suolo 2007** (Regione Marche open data, CC BY 4.0, direct shapefile): the
  published layer is dissolved to Corine **level 2** (`LIV_2`): 31 forest, 32 shrub and herbaceous,
  with no broadleaf/conifer/mixed split and no macchia/regrowth split. It cannot feed
  `forest.groups`; it serves below as the forest-area cross-check.
- **CLC 2018 IV level alone** (Umbria's path): built and measured, **201,233 ha of forest, −31.0 %
  against INFC 2015**, 1,964 woodland cells. Marche's woods are many small patches in the hills
  that CLC's 25 ha unit leaves out, so CLC alone is not usable here.
- **REM Vegetazione naturale 50k**: 17,949 polygons of natural and semi-natural vegetation, each
  with its physiognomy and dominant species (`TipoFisio`, e.g. "Bosco deciduo di Ostrya carpinifolia
  Scop.", "Rimboschimento sempreverde a pino nero"; `SpeciePrev`, the species alone). One layer gives
  both the broad groups and the forest types, read once, like Liguria's forest-type map.

**Licence (to check).** The REM download page states no licence. Italian public-administration
data published without an express licence are open data by default (CAD, D.Lgs. 82/2005, art. 52
c. 2), and CC BY 4.0 is the reference licence of AgID's open-data guidelines; the Region's own
open-data portal uses CC BY 4.0 for its maps. So the app credits "Vegetazione naturale REM ©
Regione Marche, CC BY 4.0". If Regione Marche states other terms, CLC IV alone is the fallback
(and would need the −31 % explained).

**Download.** `static.regione.marche.it` sends its leaf certificate without the GlobalSign RSA OV
SSL CA 2018 intermediate, which curl and browsers fetch themselves and Python does not. The grid's
`fetch` now adds the intermediates in `api/src/api/config/certs/` to the default trust (the public
certificate from GlobalSign's repository, valid to 2028); verification stays on.

Class mapping (`marche.yaml`), whole-map areas (the map also covers Alta Valmarecchia, see below):

| `TipoFisio` | group | ha | | `SpeciePrev` | habitat |
|---|---|---|---|---|---|
| Bosco deciduo di … (16 species) | broadleaf | 250,755 | | Ostrya carpinifolia, Carpinus betulus, Fraxinus excelsior, Acer obtusatum / pseudoplatanus, Alnus cordata | mixed_broadleaf |
| Rimboschimento sempreverde a leccio (holm-oak woods) | broadleaf | 4,399 | | Quercus pubescens, Q. cerris, Q. robur | deciduous_oak |
| Rimboschimento deciduo | broadleaf | 393 | | Fagus sylvatica | beech |
| Bosco misto di Quercus pubescens, Rimboschimento misto | mixed | 3,218 | | Castanea sativa | chestnut |
| Rimboschimento sempreverde a pino nero | conifer | 16,418 | | Quercus ilex | evergreen_oak |
| Rimboschimento sempreverde, Bosco sempreverde di Pinus halepensis | conifer | 632 | | Populus nigra, Salix alba, Alnus glutinosa, Fraxinus oxycarpa, Ulmus minor | riparian |
| Arbusteto di Erica arborea, Juniperus oxycedrus, Ampelodesmos | macchia | 4,360 | | Robinia, Ailanthus | exotic_broadleaf |
| Arbusteto deciduo (Spartium, Prunus, Crataegus, Cornus, Rubus, willows), Arbusteto misto (Cercis, Cotinus), Prebosco di Ulmus minor | transitional | 14,799 | | Pinus halepensis, P. pinea | mediterranean_pine |
| | | | | Pinus nigra | mountain_pine |
| | | | | Abies alba, A. cephalonica | fir_spruce |
| | | | | Cupressus arizonica | other_conifer |

Left out, as UCS and CLC leave 321/322 out in Tuscany: montane heath and shrub (Juniperus communis
and nana, Calluna, Vaccinium, Salix retusa, Rhamnus alpinus: 1,352 ha), Arundo pliniana reed beds
on the clays (996 ha), garighe, grassland and wetlands. **Black pine goes to `mountain_pine`**, as
CLC IV files it (3122, pini montani e oromediterranei) in Tuscany; Liguria sent its mixed
plantations (`RI`) to `other_conifer`. The holm-oak woods carry the "Rimboschimento … a leccio"
label even where they are natural (Conero, Furlo, Frasassi); they are broadleaf either way.

## Woodland grid

Built 2026-09-25 (`uv run python -m api.grid.build --region marche`, 55 s with a warm cache).

- Cells 9,690; inside area 9,327 km² (the generalised ISTAT 2025 boundary).
- **Woodland cells 2,370** (a quarter of the cells: the Marche hills are farmland with small woods;
  the woodland is the Apennine and pre-Apennine ridges). 93 of the 225 comuni have woodland cells.
- **Forest area 259,734 ha vs INFC 2015 bosco 291,767 ha: −11.0 %**, just outside ±10 %. Explained:
  - REM also maps the Alta Valmarecchia comuni that moved to Emilia-Romagna in 2009 (Casteldelci,
    Maiolo, Novafeltria, Pennabilli, San Leo, Sant'Agata Feltria, Talamello) and 2021
    (Montecopiolo, Sassofeltrio): 15,917 ha of its forest lie there, outside ISTAT 2025's Marche.
    Inside it, REM holds 258,980 ha, which the 20 m rasterization reproduces (259,734 ha).
  - The rest is scale: at 1:50,000 REM drops small woods. The 1:10,000 CUS 2007, clipped to the
    same boundary, holds 284,143 ha of forest (−2.6 %). But it would add only **159 woodland
    cells** (2,529 against 2,370; 2,244 in both), and the per-cell forest share of the two maps
    correlates at 0.97: the woods REM misses are scattered patches in cells that are mostly fields.
  - INFC 2015 counts Marche as it was then (with Montecopiolo and Sassofeltrio, about 1,400 ha of
    forest), which leaves the comparison at about −10.7 %.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 72 % of a cell's wooded area.
- Terrain: woodland elevation median 669 m (5th–95th percentile 337–1,207 m), max 1,724 m; slope
  median 22.2° (Tuscany 16.6°), 32 % of woodland cells above 25°; 75 cells have no aspect.
- Soil pH (SoilGrids, not scored): woodland median 6.73 (6.21–7.26, 5th–95th percentile), less
  acid than Tuscany's and Liguria's: limestone and marl.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| mixed_broadleaf (hop-hornbeam) | 44.0 % | 1,187 | 666 m |
| deciduous_oak (downy and Turkey oak) | 29.2 % | 729 | 603 m |
| beech | 9.3 % | 219 | 1,193 m |
| mountain_pine (black-pine reforestation) | 7.0 % | 126 | 571 m |
| transitional_woodland_shrub | 2.5 % | 2 | |
| chestnut | 2.4 % | 45 | 889 m |
| evergreen_oak | 2.3 % | 38 | 591 m |
| riparian | 1.6 % | 9 | 288 m |
| macchia | 1.3 % | 6 | 925 m |
| mixed_broadleaf_conifer, mediterranean_pine, exotic_broadleaf, fir_spruce | 0.1 % each | 1–3 | |

Woodland cells by province: Pesaro e Urbino 808, Macerata 727, Ascoli Piceno 470, Ancona 295,
Fermo 70.

Threshold sensitivity (recomputed from stored fractions, a few cells off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 3,376 | 2,825 | **2,361** | 1,894 | 1,470 |

## Weather

- Points: 56 candidates on the 0.2° lattice, **47 on land**; all 2,370 woodland cells weighted.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region marche`,
  118 land nodes at 0.1°, three 14-day windows of 2024). Cooling per km of height across nodes,
  median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 4.67 | 6.08 | 4.10 | 4.79 | 4.5 | +0.29 |
  | temperature_2m_mean | 4.13 | 5.94 | 4.63 | 4.78 | 4.5 | +0.28 |
  | temperature_2m_min | 3.77 | 6.31 | 4.86 | 4.90 | 4.2 | +0.70 |
  | soil_temperature_0_to_7cm_mean | 3.73 | 5.71 | 3.98 | 4.13 | 3.7 | +0.43 |

  Every fitted rate is within 1 °C/km of the national one, so **the national lapse rates are kept**
  (no weather override). Leave-out test on the 0.2° lattice (stride 2), RMSE with the national
  rates vs none vs 6.5 °C/km: mean air temperature 0.28 / 0.51 / 0.29 °C, minimum
  0.51 / 0.68 / 0.50 °C, maximum 0.37 / 0.53 / 0.40 °C, soil 0.30 / 0.50 / 0.30 °C; daily rain RMSE
  0.97 mm either way.
- **History** comes from the CDS ERA5-Land time-series product, one request per node for
  2016-01-01 to 2026-09-14 (the nodes shared with Umbria and Emilia-Romagna came from the shared
  cache). Snowfall, which that product lacks, comes from Open-Meteo's archive (`era5_seamless`,
  ERA5 snowfall, as Tuscany's whole history has it): CDS's gridded queue was still stuck on
  2026-09-25 (another lane's gridded ERA5-Land job sat "accepted" for over an hour), so
  `backfill --source cds --skip-snowfall`, then `backfill --source open_meteo --variables
  snowfall_sum`. Open-Meteo's archive and the ECMWF IFS forecast fill the days after 2026-09-14.

### Rain scale: borrowed, no Marche gauge check

Marche publishes no open daily rain that a script can read:

- the Region's rain gauges (Centro Funzionale's SIRMIP network, the old Servizio Idrografico's
  successor) give daily data through an online extractor after registration;
- the AMAP agrometeo network (ex ASSAM, 88 stations) has an open-data API
  (`apimeteo.regione.marche.it`, "possono essere utilizzati liberamente") that serves stations
  and sensors but not yet the daily measures ("saranno resi disponibili"); its free daily data
  come one station and variable at a time through a web form (1,000 records per request).

So there is no gauge check, and the scale is borrowed. It cannot be the national one: that scales
`era5_seamless` only, while `api.model.inputs` scales the rain normals whatever their source
(Liguria's finding), so CDS history rain would stay raw while `percent_of_normal` divided it by
scaled normals. And both bordering regions' gauge checks on the same CDS rain found the national
scale 25–30 % too wet. **`marche.yaml` sets the mean of the two bordering regions' woodland-gauge
fits, 0.76 + 0.57 per km**, over `era5_land_cds` and `era5_seamless`:

| fit (CDS rain, woodland gauges, 2019–2025) | a | b per km | factor at 200 / 500 / 800 / 1,200 m |
|---|---|---|---|
| Umbria (8 Servizio Idrografico gauges, 402–1,053 m; raw pooled 0.88, all 82 gauges 1.01) | 0.89 | 0.33 | 0.96 / 1.06 / 1.15 / 1.29 |
| Emilia-Romagna (66 ARPAE gauges, 183–1,535 m; raw 1.06 below 400 m, 0.94 at 400–800 m, 0.69 above) | 0.62 | 0.80 | 0.78 / 1.02 / 1.26 / 1.58 |
| **Marche (mean, used)** | **0.76** | **0.57** | **0.87 / 1.04 / 1.22 / 1.44** |
| national (Tuscan gauges, `era5_seamless`) | 1.28 | 0.29 | 1.34 / 1.43 / 1.51 / 1.63 |

Both neighbours find the raw reanalysis about right in the lowlands and dry in the mountains,
which is the shape used; Marche's Apennine side faces the Adriatic like Emilia-Romagna's, its
ridge is shared with Umbria. The Emilia-Romagna fit is its lane's as of 2026-09-25 (not yet
merged). A national or per-zone rain calibration (card `fix-rain-calibration-region-borders.md`)
should replace it; AMAP's daily measures, once the API serves them, would allow a Marche check.

## Sightings

`uv run python -m api.sightings.ingest fetch --region marche` (2026-09-25): **39 GBIF records** for
the three groups over the bbox and **none from iNaturalist** in the last two weeks. After the
quality filters (28 too imprecise, 7 with unknown uncertainty, 4 undated, 4 of an excluded basis)
7 are kept, and **2 land on Marche's woodland cells** (5 are outside the region inside the bbox,
or on non-woodland cells). GBIF holds no *B. edulis* and no *C. cibarius* in the whole bbox. Most
Marche iNaturalist records (23 porcini, 7 ovoli, 15 *Cantharellus*) have obscured locations and
never reach GBIF at a usable precision (`species-ecology/marche.md`, Occurrence cross-check).

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/marche.md`; rules in
`api/src/api/config/species/marche/` (23 new references, all opened).

- **All three groups and six keys kept.** The Marche porcino is mostly the summer one (*B.
  aestivalis* = *reticulatus*, 300–1,300 m, mid-May to October, per the regional mycological
  societies' bulletin); *B. edulis* and *B. pinophilus* are present but uncommon. The commonest
  Marche chanterelle is *C. ferruginascens*, which grows on calcareous soil. The regional law is
  L.R. 18/2022 (L.R. 17/2001 is repealed): 3 kg a day for all species, no closed ovoli.
- **Changed from Tuscany: what the habitat classes hold here.** 18 affinities move. Black-pine
  reforestation (`mountain_pine`, 7 %) goes down for *edulis* (0.1), *pinophilus* and
  *reticulatus* (0.3) and gallinacci (0.1): no Marche source reports them there (the Sibillini
  lists name Suillus, Lactarius and Craterellus). Hop-hornbeam (`mixed_broadleaf`, 44 %) goes up
  for *aereus* (0.6) and down for *edulis* and *pinophilus* (0.1). Broom scrub (`transitional`)
  and montane heath (`macchia`) go down for most keys. Gallinacci go up in beech (1.0) and
  deciduous oak (0.6). *B. reticulatus* stays at full credit up to 1,300 m (Tuscany 1,100 m).
- **Unchanged: season windows, weather rules, stoppers, growth clocks.** No Marche or
  central-Apennine study gives numbers, and the Marche records and pages agree with the Tuscan
  windows.
- **Effect on the grid** (habitat × altitude gates, woodland mean): *edulis* 0.78 → 0.54,
  *pinophilus* 0.66 → 0.49, the other keys within ±0.02 of Tuscany's rules on the same cells.
- **Open questions:** black pine and hop-hornbeam (51 % of the woods) rest on absences and
  forager magazines; substrate (the woods are mostly on limestone, which the rules cannot see);
  *B. aereus*'s 1,250 m ceiling may be low here; the slope stopper was left alone (woodland mean
  0.984, Tuscany 0.994).
- **Press contrasts** (`marche/sanity.yaml`): 12, written before any Marche score existed, 8 for
  porcini, 2 for ovoli (ids `ovoli_…`) and 2 for gallinacci (ids `gallinacci_…`). Marche local
  press on mushroom seasons is thin: seven rest on one forager blog about the Teramo side of the
  Monti della Laga, read onto Acquasanta Terme and Arquata del Tronto (it matches Cronache Picene
  in September 2019).

## Validation

Scored 2016-03-18 to 2026-10-03 on 2026-09-26 (rules version `6d7ac926cd60`, the borrowed rain
scale, snowfall from `era5_seamless`): 2,370 woodland cells × 3,852 days per key, no cell-day
without a score. `onboard` ran the hold-out backtest and the sanity check; the train-season
backtest (`--seasons train --label onboard-train`) and the ovoli and gallinacci sanity runs
(`--group`) were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **0**, against the 50 the parent plan asks for.
Hold-out 2024–2025: **2** (porcini, 10 and 15 September 2024, two neighbouring cells).

**Backtest** (hold-out, porcini, n = 2): model `auc_local` 0.82 (0.67–0.98), `auc_region` 0.80,
`auc_time_effort` 0.13; the calendar baseline 0.50 / 0.82 / 0.60, habitat 0.50. Two sightings in
one place and one week say nothing either way. Validating Marche needs records with locations: the
regional mycological societies' exhibition records or the AST mycological inspectorates, or central
Italy's records pooled.

**Sanity check** (`marche/sanity.yaml`, 12 contrasts written before any Marche score existed), each
contrast read against its own group:

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Laga–Montegallo 2019 > 2017, 2–9 Sep | porcini | 0.920 | 0.019 | yes |
| Laga 2016 > 2017, 25 Sep–10 Oct | porcini | 0.788 | 0.913 | no |
| Laga July 2016 > July 2017 | porcini | 0.716 | 0.270 | yes |
| Laga late August 2018 > 2017 | porcini | 0.773 | 0.203 | yes |
| Laga 2024 > 2020, 28 Aug–6 Sep | porcini | 0.851 | 0.496 | yes |
| Laga 2025: 8–20 Sep > 1–12 Oct | porcini | 0.522 | 0.736 | no |
| Catria–Nerone > southern Marche, 1–12 Sep 2021 | porcini | 0.670 | 0.734 | no |
| Marche October 2022 > normal | porcini | 0.545 | 0.504 | yes |
| Laga ovoli 2024 > normal, 25 Aug–6 Sep | ovoli | 0.436 | 0.327 | yes |
| Laga ovoli 2020: 7–15 Sep > 5–24 Aug | ovoli | 0.439 | 0.289 | yes |
| Laga gallinacci June 2016 > June 2025 | gallinacci | 0.494 | 0.280 | yes |
| Marche gallinacci June 2022 > June 2024 | gallinacci | 0.131 | 0.465 | no |

**8 of 12 hold** (porcini 5/8, ovoli 2/2, gallinacci 1/2). The `Data` section's "9/12" is the
default run, which scores all 12 on the porcini group. Of the four misses, two rest on the weakest
sources (a national magazine's regional bulletin for Catria 2021 and June 2022); the 2016/2017
turn of October and the 2025 timing are misses on the Laga forager blog, where the model puts the
better window the other way round. None has been investigated further. See `.gavin-root/docs/species-ecology/
marche.md` for each contrast's evidence.

**The served window.** On 26 September 2026 porcini score almost 0 across Marche (mean 0.003):
the reanalysis puts the last 30 days at about 35 % of the cells' normal rain, and porcini's 30-day
rain factor is 0 below 50 %; season, habitat and temperature are all near full credit. Umbria,
scored independently on the same reanalysis, reads 0.015 that day, so this is the weather, not the
Marche rules (the percentage of normal does not depend on the rain scale). Ovoli mean 0.20 and
gallinacci 0.34, with 7 % of cells at 0.6 or more on the combined score.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-26 (`deploy/rsync-region-data.sh marche`, 213
files, 189 MB, no redeploy); the post-sync read of the live API was not run from this session.
The server serves a region only when its YAML is in the deployed code and its stores are on disk,
so they stay inert until `main` with `config/regions/marche.yaml` is deployed by the rail's "Deploy
pulled main" step (with the daily job, which brings the weather and scores up to that day). Then
check:

- [ ] `https://mappafunghi.app/marche` and `/marche/porcini`, `/marche/ovoli`, `/marche/gallinacci`
  show real scores for today (not fixtures), and a tapped cell's "why this score" names Marche
  habitats (hop-hornbeam as mixed broadleaf, black pine as mountain pine).
- [ ] `https://api.mappafunghi.app/regions` lists `marche`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Marche URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/marche` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci nelle Marche", description, canonical, og image `og/marche.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1279).
- [ ] `/credits` shows "Regione Marche — Rete Ecologica Marche, Vegetazione naturale 1:50.000".
- [ ] The next morning's daily job has a `region_done` line for `marche`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Region lookup by bbox.** `findRegionAt` picks the first region whose bbox holds a point, the
  current region first. Marche's bbox shares its whole western half with Umbria's (Fabriano,
  Camerino, Cagli, Apecchio, the Sibillini: most Marche woodland), and its north-west corner with
  Tuscany's. Inside `/marche` a point there opens Marche's forecast; from the hub or `/toscana` the
  switch offer names Umbria (or Tuscany) first, and inside `/umbria` a tap near Fabriano opens
  Umbria's forecast for a point outside Umbria's grid. Card `fix-region-lookup-by-boundary.md`.
- **Rain scale borrowed** from the neighbours (Weather above); card
  `fix-rain-calibration-region-borders.md`.
- **REM licence** stated by law, not by the download page (Sources above).
- **Woodland is a quarter of the cells.** Marche's hill woods are small patches in farmland; the
  1:50,000 map and the 50 % rule keep the Apennine and pre-Apennine woods and drop the hedgerow
  woods of the hills (Woodland grid above).

## Data

- cells: 9690
- woodland cells: 2370
- INFC deviation: -11.0% (grid 259,734 ha vs 291,767 ha) — outside ±10%
- weather nodes: 47
- years stored: 2016–2026 (11 years)
- sightings kept: 2
- backtest AUC (auc_local, model, all): porcini 0.824
- sanity contrasts: 9/12 passed

