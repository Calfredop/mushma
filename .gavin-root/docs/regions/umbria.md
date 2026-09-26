# Umbria

Region card: `region-umbria.md` (region #3 of `feat-full-italy-coverage.md`). API id `umbria`,
web slug `/umbria`, ISTAT COD_REG 10. A landlocked region of oak and hop-hornbeam hills with a
beech belt on the Apennine ridge, east of Tuscany.

## Sources

**Decision: CLC IV level alone** (ISPRA Corine Land Cover 2018 IV livello, CC BY 4.0), as for the
foundation's dry run. No Umbrian forest or land-use map was usable, because none has an open
licence (checked 2026-09-25):

| candidate | what it is | why not |
|---|---|---|
| Regione Umbria, *Carta geobotanica con principali classi di utilizzazione del suolo* (PUT 2000) | 1:50,000, 1999 edition, 1,047 polygons with 19 physiognomic units (e.g. "Boschi di caducifoglie collinari e submontane", "Rimboschimenti a conifere"). Queryable on the SIAT ArcGIS server (`siat.regione.umbria.it/arcgis/rest/services/public/WEBGIS4_WGS84_UTM33/MapServer/0`) | UmbriaGeo's terms: free for study and research only; "per la pubblicazione e/o altri usi dei dati" needs written authorization from Regione Umbria SIAT; no commercial use. It is not an open licence. It is also 27 years old and coarser in type than CLC: no separate chestnut or beech class. |
| Regione Umbria DBGT 1:10,000, `Bosco` layer (`DBT_06_Vegetazione`) | Forest polygons with a TUFF-style definition (≥ 2,000 m², ≥ 20 % cover) and a species attribute | Covers only the western Tevere–Trasimeno strip (x 255–297 km UTM33), not the region; same UmbriaGeo terms |
| "Carta forestale regionale" (the card's candidate) | The regional forest map behind *Lo stato delle foreste in Umbria* (Regione Umbria, 2009): photo-interpreted, forest types (cerrete ~40 %, orno-ostrieti ~26 % of the woods) | Not published as data: no dataset on `dati.regione.umbria.it` (CC BY portal; searched "forestale", "bosco", "uso del suolo", "vegetazione") or UmbriaGeo; the related PUT/PPR maps are PDFs |
| CREA, *Carta Forestale d'Italia* CFI2020 | National 1:10,000 forest map with INFC categories; Umbria 383,349 ha (FAO definition) | Distributed only on an emailed request approved by MASAF, for at most two regions, with a 7-day download window. That is not an open, scriptable source. |
| ISPRA, *Carta della Natura* Umbria | 1:25,000 habitat map, CORINE Biotopes, completed 2025 | "Disponibili su richiesta" (request form); no open download |

What CLC alone costs:

- **Forest area: −20.2 % vs INFC 2015** (311,303 ha in the grid vs 390,305 ha bosco). CLC's
  25 ha minimum unit drops the small woods, hedgerow woods and young regrowth of the Umbrian
  hill farmland; adding CLC's transitional woodland-shrub (324) and sclerophyll (323) brings the
  grid's wooded area to 346,880 ha (−11 %). INFC's own 2005 figure was 371,574 ha bosco, and
  the regional forest inventory of 1993 counted 300,500 ha under the stricter D.Lgs 227/2001
  definition. CLC IV is therefore within the spread of the regional sources' own definitions, but
  well short of the current inventory. The ±10 % target is missed and explained here.
- **Woodland cells: 3,253 of 8,826** (37 %). A cell counts only when CLC forest covers at least
  half of it, so mosaic hill cells with many small woods drop out. The share of cells counted is
  below the ~46 % of land the inventory calls wooded.
- **Types come from CLC directly** (`borrowed_type_fraction` is 0 everywhere, because groups and
  types are the same map). On the woodland cells, the share of wooded area is: deciduous oak 58.8 %,
  mixed broadleaf 11.1 %, holm oak 9.6 %, beech 6.5 % (dominant cells at a mean 1,197 m), mixed
  broadleaf–conifer 5.8 %, transitional 4.9 %, chestnut 1.5 %, mountain pine 1.2 %,
  Mediterranean pine 0.5 %, no fir or spruce. INFC 2005's categories show the same picture:
  cerrete ~120,000 ha, roverella >96,500 ha, ostrieti ~60,000 ha, leccete ~40,000 ha; conifers
  are ~2 % pure and ~8 % mixed (*Lo stato delle foreste in Umbria*, 2009).
- **Chestnut is under-mapped.** Chestnut stands are small and scattered (Orvietano, Monte
  Peglia, Monti Amerini, Alta Valle del Tevere), so CLC folds most of them into deciduous oak or
  mixed broadleaf. The species rules keep chestnut as a host; the gap mostly lowers ovoli and
  gallinacci habitat scores where chestnut is hidden in oak cells.

Swap-in path: if Regione Umbria publishes its forest map (or UmbriaGeo data) under CC BY or
IODL 2.0, add it to `api/src/api/config/sources.yaml` and point `forest.groups` (and possibly
`forest.types`) at it in `api/src/api/config/regions/umbria.yaml`
(`.gavin-root/docs/woodland-grid.md` → "Adding a region").

Credits: every source Umbria's data uses (Copernicus ERA5-Land, Open-Meteo, ECMWF, ISPRA CLC,
Copernicus DEM, SoilGrids, ISTAT, GBIF, iNaturalist) is already on the app's credits list, which is
national, so nothing is added. The Umbrian rain gauges feed a check only, never the app.

## Config

`api/src/api/config/regions/umbria.yaml`:

- **Boundary.** ISTAT COD_REG 10; bbox `[11.89, 42.36, 13.27, 43.62]`, the ISTAT 2025 boundary's
  extent (11.8919, 42.3641, 13.2637, 43.6173) rounded outward to 0.01°.
- **Forest.** CLC IV level alone (no `forest.groups`), shared CLC IV type defaults (Sources above).
- **iNaturalist place** 10875, "Umbria, IT" (admin level 10), resolved by name on 2026-09-25
  (`api.inaturalist.org/v1/places/autocomplete?q=Umbria`). The foundation read one global place
  (Toscana) and cached GBIF pages by taxon only, so a second region would have fetched Tuscany's
  records; this card made the place and both raw caches per region.
- **Gauges.** `api.weather.checks gauges --region umbria` reads the Regione Umbria Servizio
  Idrografico's daily rain (open data, CC BY; `GAUGE_NETWORKS["umbria"]`, Validation).
- **`model:` overrides:** none (Validation, gauge check).
- **Weather points.** 56 land nodes on the 0.2° lattice, all 3,253 woodland cells within reach.

### Lapse rates (`api.weather.checks lattice --region umbria`)

153 ERA5-Land land nodes at 0.1°, three 14-day windows of 2024 (Jan, Jul, Oct). Cooling per km of
height, median of the daily fits:

| variable | Jan | Jul | Oct | all | national config | difference |
|---|---|---|---|---|---|---|
| Tmin | 3.90 | 4.30 | 2.35 | **3.24** | 4.2 | −0.96 |
| Tmax | 4.91 | 7.30 | 4.32 | **5.25** | 4.5 | +0.75 |
| Tmean | 4.34 | 6.23 | 3.77 | **4.34** | 4.5 | −0.16 |
| soil 0–7 cm | 3.60 | 6.59 | 2.95 | **3.60** | 3.7 | −0.10 |

Every fit is within 1 °C/km of the national rates (Tmin the closest call, like Tuscany's October
valley inversions), so **the national rates are kept**. Leave-out test at the 0.2° lattice with
them: RMSE 0.25 °C (Tmean), 0.39 °C (Tmin), 0.29 °C (Tmax), 0.34 °C (soil), 1.05 mm daily rain,
against 0.23 / 0.38 / 0.27 / 0.35 °C with 6.5 °C/km and 0.41 / 0.50 / 0.45 / 0.43 °C with no lapse
correction.

## Weather history

From the Copernicus CDS, 2016-01-01 to 2026-09-14, through the ERA5-Land time-series product
(`cds.method: timeseries`, added by this card; `.gavin-root/docs/weather-history-cds.md`): 56 node
requests of about 40 s each, plus 23 Italy-wide half-yearly snowfall requests that every region
shares, instead of 634 weekly bbox chunks that CDS would have run one at a time for about 30–60 h. The days after 2026-09-14 come from the Open-Meteo update
step, as for every region.

## Data

- cells: 8826
- woodland cells: 3253
- INFC deviation: -20.2% (grid 311,303 ha vs 390,305 ha) — outside ±10%
- weather nodes: 56
- years stored: 2016–2026 (11 years)
- sightings kept: 3
- backtest AUC (auc_local, model, all): gallinacci 0.281, ovoli 0.196
- sanity contrasts: 9/12 passed

## Validation

Run 2026-09-25 on the stores above (rules version `cd4c9095dbba`).

### Rain gauges (`api.weather.checks gauges --region umbria`)

Regione Umbria Servizio Idrografico, open daily rain (CC BY). 91 stations report since 2016, but
only those inside woodland cells count, and only **8** do with 80 % of days over 2019–2025 (9 in
2025), at 402–1,053 m; the stations carry no height, so each takes its cell's DEM mean.

- **Gauge days are calendar days**: median daily correlation 0.65 against 0.42 when the model is
  re-cut to 09:00–09:00 days (2025).
- **ERA5-Land (CDS) holds 0.88 of the gauge rain** over 2019–2025 (median 0.85, daily correlation
  0.71, 3-day wet-window hit rate 0.78), 0.81 in 2025.
- **The national rain scale does not fit.** 1.28 + 0.29 per km (fitted on Tuscan gauges, and
  applied to `era5_seamless` only) would make Umbrian rain 32 % too wet; a least-squares fit of
  gauge totals on model totals × (a + b × km) over 2019–2025 gives **a = 0.89, b = 0.33 per km**
  (pooled ratio 0.88 → 1.00; 2025 alone 0.92 + 0.41 per km). So `umbria.yaml` sets
  `model.precipitation_scale` to it, over both `era5_land_cds` and `era5_seamless`: Umbria's
  history is CDS, which the national block would have left unscaled while the normals were scaled.
- With 8 gauges the elevation slope is loosely held; the intercept agrees between the two windows.
- **Corroborated on every Umbrian gauge.** A one-off check (not the committed tool) interpolated the
  CDS rain bilinearly from the nodes to all **82** gauges with 80 % of days in 2019–2025 (67–1,538 m,
  heights from their grid cell): raw pooled ratio 1.01 (1.12 below 400 m, 0.88 at 400–800 m, 0.90
  above), own fit 0.85 + 0.31 per km, and the woodland fit above lands at 1.04 on them. The national
  scale would be 1.42 there.

**Known issue: a step at the Tuscan border.** CDS and `era5_seamless` rain agree in amount (pooled
0.995 over Tuscany's 103 nodes in 2024), but Tuscany's SIR gauges read the reanalysis at 0.63–0.79
of gauge rain and Umbria's at about 0.9–1.1, so each region's own region-wide fit scales the same
reanalysis rain differently: at the border near Cortona (Tuscany, 437 m, ×1.41) and Lisciano Niccone
(Umbria, 295 m, ×0.99), 12 km apart, the raw 3-day rain was 18.6 and 17.8 mm on 25 Sep 2026, scaled
to 26.2 and 17.6 mm. That day the combined score's mean along the border band was 0.86 on the Tuscan
side and 0.47 on the Umbrian side, porcini 0.47 and 0.07. Tuscany's scale was fitted on gauges where
the reanalysis misses the Apennine and Apuan orographic rain; one region-wide number cannot be right
at both ends of Tuscany. A national or spatially smooth rain calibration (per zone or node, from
every region's open gauges) is the fix, and is a cross-region follow-up, not this card's.

### Backtest (hold-out seasons 2024–2025, `backtest/umbria/onboard/`)

**Usable presences: 0 in the train seasons (2016–2023)**, far below the 50 the card asks before
tuning, so **nothing is tuned: the researched priors ship**. The hold-out has 3 (gallinacci 2, ovoli
1, porcini 0), all 2024–2025 GBIF records; the AUCs (auc_local gallinacci 0.28, ovoli 0.20; auc_region
0.73 and 0.94) rest on one or two points and say nothing either way. Umbria has almost no public
records (`species-ecology/umbria.md`, Sightings): validating it needs central-Italy records pooled
with it.

Combined-score winners over the 2024 and 2025 cell-days that have one: gallinacci 55 %, porcini 32 %,
ovoli 13 %; 40 % of cell-days have no group in season. Gallinacci wins most because its season is
the longest.

### Press contrasts (`sanity.yaml`, porcini, `backtest/umbria/onboard/sanity_porcini.csv`)

**9 of 12 hold.**

| contrast | higher | lower | holds |
|---|---|---|---|
| `valnerina_2023` | 0.340 | 0.410 | no |
| `alta_valnerina_october_2023` | 0.012 | 0.073 | no |
| `orvietano_2023` | 0.508 | 0.439 | yes |
| `umbria_2022_summer` | 0.222 | 0.174 | yes |
| `umbria_2022_autumn` | 0.736 | 0.585 | yes |
| `marche_border_2021` | 0.513 | 0.182 | yes |
| `umbria_2021_early_september` | 0.442 | 0.328 | yes |
| `apennine_august_2019` | 0.326 | 0.274 | yes |
| `umbria_2024_autumn` | 0.957 | 0.615 | yes |
| `alta_valle_tevere_2024` | 0.943 | 0.506 | yes |
| `umbria_2025_early` | 0.725 | 0.496 | yes |
| `acquasparta_sellano_2025` | 0.554 | 0.752 | no |

- The good and bad years (2022 drought then boom, 2021, 2024, 2025) and the Apennine-border
  contrasts all hold.
- **Both Valnerina misses come from the rain, not the rules.** In the upper Valnerina (416 woodland
  cells, median 1,006 m) in early October 2023, the 30-day rain factor (percentage of the cell's
  normal) is 0 on 96 % of cell-days: ERA5-Land saw a dry September there. The late-August 2023 claim
  credits Valnerina "dove le piogge sono state più copiose": local storms a ~9 km reanalysis
  misses, the known convective-rain trap (`weather-ingest.md`). Season, habitat, altitude and
  temperature gates are open in those cells.
- `acquasparta_sellano_2025` names its areas "ad esempio", so it was the weakest claim.

### Cells without weather

7 woodland cells never get weather or a score: border slivers with under 0.25 ha inside Umbria and
no DEM pixel of their own (so no height to move temperatures to), which pass the woodland test
because CLC forest across the border counts toward the cell. Tuscany has the same kind (its daily
runs report a few cell-days without weather). They show as unscored on the map.

## After the deploy

**Ship order (decided with the human, 2026-09-25): the stores go to the server only after this card
is merged and deployed.** `main` already carries `umbria.yaml` (the foundation's fixture), and a
region is served as soon as its grid and score meta are on the server's disk, so rsyncing before the
deploy would serve Umbria on the old code (no species list; a failing morning job for Umbria, with
an alert and no heartbeat). So, after the PR is merged and the rail's "Deploy pulled main" has run:

- [ ] Run the gavin tool **Rsync region data** standalone (it runs in the root checkout, whose
      `api/data` is the shared data root): region `umbria`, redeploy `yes`, tests `no`, run_job
      `yes`. Umbria goes live on the new code and the daily job scores it at once.

Then check:

- [ ] `https://mappafunghi.app/umbria` and `/umbria/porcini`, `/umbria/ovoli`, `/umbria/gallinacci`
      show real scores: cells coloured, a tapped cell has a breakdown, the date control reaches
      +7 days.
- [ ] The hub `/` lists Umbria and colours it on the national map (`GET /overview` has an
      `umbria` row); `GET https://api.mappafunghi.app/regions` includes `umbria` with all three
      species.
- [ ] `https://mappafunghi.app/sitemap.xml` has `/umbria` and its three species pages (it already
      does from the foundation's fixture entry).
- [ ] Lighthouse SEO 100 on `/umbria` (mobile).
- [ ] The next morning's daily job has a `region_done` line for `umbria`
      (`journalctl -u mushma-daily`), and its `open_meteo_calls` total stays inside the budget.
