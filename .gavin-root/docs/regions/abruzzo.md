# abruzzo

Region #12 of the full-Italy rollout (card `region-abruzzo.md`). API id `abruzzo`, web slug
`/abruzzo`, ISTAT COD_REG 13. Config: `api/src/api/config/regions/abruzzo.yaml`. The highest
Apennine woodland: beech from about 900 m to the tree line at 1,800–1,900 m on the Gran Sasso, the
Majella, the Sirente-Velino and in the Parco Nazionale d'Abruzzo, over downy oak, Turkey oak and
hop-hornbeam hills; the Monti della Laga are the siliceous exception in a limestone region.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | Regione Abruzzo, **Carta Tipologico-Forestale**, Tipologie forestali, published 2009 (`ra_carta_tipologico_forestale`) | **CC BY-NC 3.0** | ArcGIS REST layer on `catasto.regione.abruzzo.it` (MapServer 1, 70,095 polygons); the open-data portal has the same map as one RAR per IGM sheet |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 10867 "Abruzzo, IT" | per record | counts per cell only |

**What was checked (2026-09-26).**

- **Carta Tipologico-Forestale della Regione Abruzzo** (Regione Abruzzo, Servizio Foreste; first
  typology 2001, map published at the end of 2009 on the IGM 1:25,000 base; 0.5 ha minimum unit,
  10 % cover, the FAO/INFC definition): 33 forest and shrub types (`DES_TCF`, e.g. "Faggeta montana
  (eutrofica-mesoneutrofila-acidofila)", "Querceto di roverella mesoxerofilo", "Rimboschimento di
  conifere nella fascia montana") and 13 categories. The open-data portal
  (`opendata.regione.abruzzo.it`, "Categorie e Tipologie forestali") states **CC BY-NC 3.0**; the
  geoportale's catalogue says "Licenza Regione Abruzzo", "nessun download". The type sheets and a
  descriptive article are on the geoportale's download area.
- **Carta dell'Uso del Suolo, edizione 2000** (1:25,000, Corine legend to level 4) and its
  **2018–2019 rapid update**: the 2000 edition is on the same open-data portal under the same
  CC BY-NC 3.0; the 2018–2019 update is only a WMS layer on the geoportale.
- **ISPRA Carta della Natura** Abruzzo (1:50,000, 2011, CORINE Biotopes): CC BY 4.0, but only
  on request through ISPRA's form, as for Umbria. Not scriptable.
- **CREA Carta Forestale d'Italia CFI2020**: on emailed request to MASAF, two regions at a time
  (Umbria and Marche docs). Not scriptable.
- **CLC 2018 IV level alone** (Umbria's path): built and measured, **308,633 ha of forest, −25.0 %
  against INFC 2015**, 3,041 woodland cells. Too far off to use when a better map exists.

**Decision: the Carta Tipologico-Forestale for both layers, under CC BY-NC 3.0.** No regional
source is openly licensed, so the card's rule pointed at CLC IV alone. The human chose the regional
map on 2026-09-28: it finds **402,905 ha, −2.1 %** against INFC and 3,782 woodland cells, with
real forest types. mappafunghi is non-commercial (friends and a portfolio; Open-Meteo's free tier
already requires it), which CC BY-NC permits with attribution. **If the app ever becomes
commercial, Abruzzo must go back to CLC IV** (drop `forest.groups` and point `forest.types` at
`ispra_clc18_iv`, as `umbria.yaml` does) or obtain the Region's permission. The credit reads
"Carta Tipologico-Forestale © Regione Abruzzo, CC BY-NC 3.0".

**Download.** The ArcGIS server caps a query at 1,000 features (`maxRecordCount`) while the grid
asked for pages of 2,000 and stepped its offset by 2,000, so it would have skipped every other
thousand polygons. `fetch_arcgis_features` now steps by the number of features the server returned
(test `test_fetch_arcgis_features_follows_a_server_capped_page`); CLC's server returns full pages,
so the other regions' builds are unchanged. The 71 pages hold all 70,095 polygons.

Class mapping (`abruzzo.yaml`, one layer gives both), whole-map areas:

| `DES_TCF` | group | habitat | ha |
|---|---|---|---|
| Faggeta montana, termofila e basso montana, altomontana rupestre | broadleaf | beech | 135,278 |
| Querceto di roverella (pioniero, tipico, mesoxerofilo), Cerreta (mesoxerofila, mesofila) | broadleaf | deciduous_oak | 123,341 |
| Orno-ostrieto pioniero, Ostrieto mesoxerofilo and mesofilo | broadleaf | mixed_broadleaf | 41,488 |
| Latifoglie di invasione miste e varie (maples, ash, cherry on old fields), Boschi di forra, Pioppeto di pioppo tremulo | broadleaf | mixed_broadleaf | 29,906 |
| Pioppo-saliceto ripariale | broadleaf | riparian | 27,968 |
| Castagneto da frutto, Castagneto (neutrofilo-acidofilo) | broadleaf | chestnut | 6,017 |
| Lecceta rupicola, costiera termofila, mesoxerofila | broadleaf | evergreen_oak | 5,304 |
| Robinieto-ailanteto | broadleaf | exotic_broadleaf | 2,759 |
| Rimboschimento di conifere nella fascia altocollinare e submontana, nella fascia montana; Pineta naturale di pino nero di Villetta Barrea | conifer | mountain_pine | 29,063 |
| Rimboschimento di conifere mediterranee (Aleppo pine) | conifer | mediterranean_pine | 1,846 |
| Variante abete bianco (beech with silver fir) | mixed | mixed_broadleaf_conifer | 50 |
| Arbusteto a prevalenza di ginepri mesoxerofili, di specie della macchia | macchia | macchia | 8,730 |
| Arbusteto a prevalenza di rose, rovi e prugnolo, di ginestre; Boscaglia pioniera calanchiva | transitional | transitional_woodland_shrub | 20,067 |
| **left out:** Arbusteto a prevalenza di ginepri nella fascia montana e subalpina, Mugheta appenninica | — | — | 22,202 |

- **Black pine goes to `mountain_pine`**, as CLC IV files it (3122) in Tuscany and as Marche does.
  Both reforestation types are "principalmente pino nero"; the montane one (9,708 ha, above 900 m
  in the beech belt) also holds silver and Greek fir, spruce, larch and Douglas fir, which the map
  does not separate.
- **The native silver fir** (Martese in the Laga, Rosello and Castiglione Messer Marino in the Alto
  Vastese) is mapped inside the beech types, so `fir_spruce` is empty in Abruzzo.
- **Left out**, as Marche leaves its montane heath out and INFC files both as other wooded land:
  the montane and subalpine juniper scrub (*Juniperus communis* and *nana*, 20,785 ha, up to
  2,200 m) and the Majella's mugo-pine krummholz (1,417 ha, above 1,850 m). The juniper scrub of the
  oak belt (*J. oxycedrus*, 8,724 ha) goes to `macchia`, as in Marche.
- The label "Rimboschimento di conifere nella fascia altocollinare e subm" is cut at 60 characters
  in the source; the config matches it as stored.

Credits: the new source is the forest map, added to the app's credits (`web/src/credits.ts`,
"Regione Abruzzo — Carta Tipologico-Forestale", CC BY-NC 3.0) and to `sources.yaml`, which the
grid build copies into the region's `meta.json`. Everything else Abruzzo uses is already credited
nationally.

## Config

- **Boundary.** ISTAT COD_REG 13; bbox `[13.01, 41.68, 14.79, 42.9]`, the ISTAT 2025 boundary's
  extent (13.0189, 41.6821, 14.7830, 42.8948) rounded outward to 0.01°. Inside area 10,796 km².
- **Forest.** The Carta Tipologico-Forestale for groups and types (Sources above).
- **Sightings.** iNaturalist place 10867, resolved by name ("Abruzzo, IT", admin level 10) on
  2026-09-26.
- **Model.** A borrowed rain scale, 0.83 + 0.43 per km (Weather below). No other override.

## Woodland grid

Built 2026-09-28 (`uv run python -m api.grid.build --region abruzzo`, 34 s with the map cached;
the first download took 10 minutes).

- Cells 11,189; inside area 10,796 km².
- **Woodland cells 3,782** (a third of the cells). 208 of the 305 comuni have woodland cells.
  By province: L'Aquila 2,443, Teramo 585, Chieti 550, Pescara 204.
- **Forest area 402,905 ha vs INFC 2015 bosco 411,588 ha: −2.1 %**, within ±10 %.
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 76 % of a cell's wooded area.
- Terrain: woodland elevation median **1,061 m** (5th–95th percentile 449–1,661 m), max 1,940 m;
  551 woodland cells above 1,500 m and 126 above 1,700 m (Marche: median 669 m, max 1,724 m).
  Slope median 19.9°, 21 % of woodland cells above 25°; 59 cells have no aspect.
- Soil pH (SoilGrids, not scored): woodland median 6.65 (6.16–7.33, 5th–95th percentile):
  limestone, with the Laga flysch at the acid end.

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| beech | 39.4 % | 1,538 | 1,416 m |
| deciduous_oak (downy and Turkey oak) | 28.3 % | 1,308 | 804 m |
| mixed_broadleaf (hop-hornbeam, old-field broadleaf) | 16.4 % | 551 | 924 m |
| mountain_pine (black-pine reforestation) | 6.7 % | 232 | 969 m |
| riparian | 2.0 % | 20 | 395 m |
| transitional_woodland_shrub | 2.0 % | 3 | |
| chestnut | 1.9 % | 55 | 913 m |
| evergreen_oak | 1.5 % | 56 | 762 m |
| macchia (oak-belt juniper scrub) | 1.4 % | 10 | 903 m |
| mediterranean_pine, exotic_broadleaf, mixed_broadleaf_conifer | 0.3 % or less each | 0–8 | |

CLC IV alone, for comparison (built 2026-09-26): 3,041 woodland cells, median 1,126 m; beech
46.4 %, deciduous oak 28.4 %, mixed broadleaf 8.4 %, transitional 6.4 %, mixed broadleaf–conifer
3.4 %, mountain pine 3.3 %, chestnut 2.1 %. CLC's 25 ha unit drops the hill woods (deciduous oak
cells 964 against 1,308, hop-hornbeam 267 against 551), which is most of the −25 %.

Threshold sensitivity (recomputed from stored fractions, a few cells off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 5,268 | 4,461 | **3,778** | 3,113 | 2,481 |

## Weather

- Points: 59 candidates on the 0.2° lattice, **55 on land**; all 3,782 woodland cells weighted,
  none out of reach.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region abruzzo`,
  148 land nodes at 0.1°, three 14-day windows of 2024, run 2026-09-28). Cooling per km of height
  across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.17 | 5.19 | 4.18 | 4.98 | 4.5 | +0.48 |
  | temperature_2m_mean | 4.65 | 4.98 | 4.50 | 4.74 | 4.5 | +0.24 |
  | temperature_2m_min | 4.18 | 4.26 | 4.11 | 4.18 | 4.2 | −0.02 |
  | soil_temperature_0_to_7cm_mean | 3.81 | 4.42 | 3.90 | 3.98 | 3.7 | +0.28 |

  Every fitted rate is within 1 °C/km of the national one, so **the national lapse rates are kept**
  (no weather override). Leave-out test on the 0.2° lattice (stride 2), RMSE with the national
  rates vs none vs 6.5 °C/km: mean air temperature 0.31 / 0.84 / 0.40 °C, minimum
  0.51 / 0.90 / 0.59 °C, maximum 0.33 / 0.85 / 0.42 °C, soil 0.33 / 0.74 / 0.50 °C; daily rain RMSE
  1.31 mm either way. The height correction matters more here than in Marche (without it the mean
  temperature's error doubles, 0.84 against 0.51 °C there): the lattice spans the Adriatic hills
  and the Gran Sasso.

### Rain scale: borrowed, no Abruzzo gauge check

Abruzzo publishes no open daily rain that a script can read:

- the regional Ufficio Idrografico e Mareografico (now under the Agenzia di Protezione Civile)
  gives station data through the POLARIS WEB portal (`idrodataabruzzo.siapmicros.com`), free but
  behind SPID or CIE login, or on request through the same identity;
- the Annali Idrologici are published as PDF tables.

So there is no gauge check, and the scale is borrowed, as Marche's is. It cannot be the national
one: that scales `era5_seamless` only, while the rain normals are scaled whatever their source, and
every CDS woodland-gauge fit so far finds the national scale 25–30 % too wet. **`abruzzo.yaml` sets
the mean of the two nearest measured fits on the same CDS rain, 0.83 + 0.43 per km**, over
`era5_land_cds` and `era5_seamless`:

| fit (CDS rain, gauges, 2019–2025) | a | b per km | factor at 200 / 500 / 800 / 1,200 / 1,600 m |
|---|---|---|---|
| Umbria (8 Servizio Idrografico woodland gauges, 402–1,053 m) | 0.89 | 0.33 | 0.96 / 1.06 / 1.15 / 1.29 / 1.42 |
| Campania (33 agrometeo gauges, 11–769 m; its lane, not yet merged) | 0.77 | 0.52 | 0.87 / 1.03 / 1.19 / 1.39 / 1.60 |
| **Abruzzo (mean, used)** | **0.83** | **0.43** | **0.92 / 1.05 / 1.17 / 1.35 / 1.52** |
| Marche (borrowed: mean of Umbria and Emilia-Romagna) | 0.76 | 0.57 | 0.87 / 1.04 / 1.22 / 1.44 / 1.67 |
| national (Tuscan gauges, `era5_seamless`) | 1.28 | 0.29 | 1.34 / 1.43 / 1.51 / 1.63 / 1.74 |

Umbria borders Abruzzo's Apennine ridge to the north-west, Campania's measured gauges lie south of
Molise; Abruzzo's own neighbours Lazio and Molise have no fit yet. Every fit agrees on the shape
(about right at mid elevation, dry in the mountains). Abruzzo's woodland reaches 1,900 m and its
median is 1,061 m, so half of it lies above every gauge used: the upper factors are extrapolated. A
national or per-zone rain calibration (card `fix-rain-calibration-region-borders.md`) should
replace it; POLARIS data, if the Region opens them without login, would allow an Abruzzo check.

## Sightings

`uv run python -m api.sightings.ingest fetch --region abruzzo` (2026-09-28): **30 GBIF records**
for the three groups over the bbox and **none from iNaturalist** in the last two weeks. After the
quality filters (2 too imprecise, 6 with unknown uncertainty) 28 are kept, and **8 land on Abruzzo's
woodland cells**: porcini 4 (October 2020, September 2022, and two of one cell and day in July 2025),
gallinacci 4 (October 2012, obscured; October 2020; May and July 2025); no ovoli. The other 20 are
outside the region inside the bbox, or on cells that are not woodland: 16 of the 18 coastal records
(black porcini and Mediterranean chanterelles around the Torino di Sangro holm-oak reserve, one
observer, October to December) fall on farmland cells of the coast, where a 100 ha wood is well
under half a cell (`species-ecology/abruzzo.md`, Occurrence cross-check).

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/abruzzo.md`; rules in
`api/src/api/config/species/abruzzo/` (9 new references, all opened, with the rain prior).

- **All three groups and six keys kept.** Every key has an Abruzzo record or source: the Abruzzo
  mycologists' book cards, the regional law (L.R. 34/2006 as amended to L.R. 14/2020: minimum size
  for porcini, no closed ovoli), a forager's ten years of dated posts on the Teramo side of the
  Laga, and iNaturalist.
- **Altitude bands move up** (only *B. aereus* keeps Tuscany's): *B. edulis* and *B. pinophilus*
  full to 1,800 m, zero at 2,000 m; *B. reticulatus* full to 1,500 m, zero at 1,800 m; gallinacci
  full to 1,400 m, zero at 1,900 m; the ovolo full to 900 m, zero at 1,200 m. Beech runs to the
  tree line here (forest-map median 1,385 m, p99 1,824 m).
- **Two season windows move, on the Laga sequence:** the ovolo is in full season from 1 August
  (Tuscany 1 September) and the gallinacci mountain window ramps 15 May → 15 June (Tuscany 1 June →
  1 July). The porcini windows are Tuscany's.
- **17 habitat affinities follow what the classes hold here.** Black-pine reforestation
  (`mountain_pine`) goes down to 0.3 for the four porcini; hop-hornbeam and old-field broadleaf
  (`mixed_broadleaf`, 16.5 % of the woods) to 0.1 for *B. edulis* and *B. pinophilus*; broom,
  bramble and badland scrub down for most keys. Beech becomes a full chanterelle host (1.0) and a
  marginal black-porcino host (0.3); deciduous oak a secondary chanterelle host (0.6). `macchia`
  (oak-belt *J. oxycedrus* scrub) is 0.3 for *B. aereus* and the ovolo, 0.1 for gallinacci.
- **Unchanged:** weather rules, stoppers, growth clocks. No Abruzzo study gives numbers; the Laga
  blog's lore agrees with the Tuscan rules. The slope stopper was checked on the grid (mean 0.989)
  and left alone.
- **Effect on the grid** (habitat × altitude gates, woodland mean, Tuscan rules → Abruzzo rules):
  *B. edulis* 0.89 → 0.83, *B. reticulatus* 0.70 → 0.93, *B. aereus* 0.44 → 0.45, *B. pinophilus*
  0.85 → 0.80, ovoli 0.35 → 0.45, gallinacci 0.72 → 0.90.
- **Press contrasts** (`abruzzo/sanity.yaml`): 16, written before any Abruzzo score existed, 12 for
  porcini, 2 for ovoli and 2 for gallinacci. Eleven rest on the Laga forager blog; Marche's Laga
  contrasts, read onto Marche comuni there, sit on their own Abruzzo comuni here.
- **Open questions:** high beech in midsummer (the porcini windows leave a 20 July–15 August gap
  above 1,500 m that the blog fills with *B. pinophilus*); thin, concentrated evidence (31 records,
  18 from one coastal wood); two compromise affinities (`mountain_pine` 0.3 for *B. edulis*, beech
  0.3 for *B. aereus*).

## Validation

Scored 2016-03-18 to 2026-10-05 on 2026-09-28 (rules version `48e18c023a4f`, the borrowed rain
scale, CDS history with CDS snowfall, then Open-Meteo's archive and the ECMWF IFS forecast from 14
September): 3,782 woodland cells × 3,854 days per key, no cell-day without weather. `onboard` ran
the hold-out backtest and the sanity check; the train-season backtest (`--seasons train --label
onboard-train`) and the ovoli and gallinacci sanity runs (`--group`) were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **3** (porcini 2: October 2020, September 2022;
gallinacci 1: October 2020), against the 50 the parent plan asks for. Hold-out 2024–2025: **3**
(porcini 1, July 2025; gallinacci 2, May and July 2025). No ovoli at all.

**Backtest** (model; calendar and habitat baselines in brackets):

| group | split | n | `auc_local` | `auc_region` | `auc_time_effort` |
|---|---|---|---|---|---|
| porcini | train | 2 | 0.63 (0.42–0.84) [0.61, 0.50] | 0.97 [0.80, 0.50] | 0.76 [0.51, 0.50] |
| gallinacci | train | 1 | — (no cells around it on the day) | 0.87 [0.87, 0.54] | 0.31 [0.50, 0.50] |
| porcini | hold-out | 1 | 0.70 [0.04, 0.50] | 0.62 [0.53, 0.50] | 0.23 [0.35, 0.50] |
| gallinacci | hold-out | 2 | 0.92 (0.89–0.95) [0.43, 0.51] | 0.89 [0.79, 0.54] | 0.56 (0.19–0.93) [0.56, 0.50] |

Six sightings in ten years say nothing either way; the region-wide ranking (`auc_region`) is the
only figure with a pattern (the altitude bands and windows put the few finds in the right belts).
Validating Abruzzo needs records with locations: the regional mycological societies' exhibition
records, the ASL mycological inspectorates, or central Italy's records pooled.

**Sanity check** (`abruzzo/sanity.yaml`, 16 contrasts written before any Abruzzo score existed),
each contrast read against its own group (`backtest/abruzzo/onboard/sanity_<group>.csv`):

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Laga July 2024 > July 2018 | porcini | 0.456 | 0.774 | no |
| Laga late August 2018 > 2017 | porcini | 0.794 | 0.188 | yes |
| Marsica early September 2018 > normal | porcini | 0.893 | 0.461 | yes |
| Abruzzo summer 2019 (drought) < normal | porcini | 0.332 | 0.377 | no |
| Laga early September 2019 > 2016 | porcini | 0.782 | 0.543 | yes |
| Valle Castellana > Ceppo, 2020 | porcini | 0.852 | 0.844 | yes (barely) |
| Chieti hills > Gran Sasso–Majella beech, turn of Aug–Sep 2021 | porcini | 0.254 | 0.276 | no |
| Abruzzo October 2022 > normal | porcini | 0.612 | 0.569 | yes |
| Laga > south-west, October 2023 | porcini | 0.703 | 0.099 | yes |
| Laga late August 2024 > 2020 | porcini | 0.841 | 0.361 | yes |
| Laga turn of Sep–Oct 2016 > 2017 | porcini | 0.819 | 0.903 | no |
| Laga 2025: mid-September > October | porcini | 0.558 | 0.712 | no |
| Laga ovoli 2024 > normal | ovoli | 0.507 | 0.363 | yes |
| Valle Castellana ovoli 2020 timing | ovoli | 0.494 | 0.399 | yes |
| Laga gallinacci June 2016 > June 2025 | gallinacci | 0.833 | 0.441 | yes |
| Laga gallinacci July 2024 > July 2025 | gallinacci | 0.613 | 0.501 | yes |

**11 of 16 hold** (porcini 7/12, ovoli 2/2, gallinacci 2/2). The `Data` section's "11/16" is the
default run, which scores all 16 on the porcini group and happens to give the same total. Two of
the five misses are the same Laga blog contrasts Marche missed on its own comuni (the 2016/2017
turn of October and the 2025 timing): the model puts the better window the other way round on
both sides of the Tronto, so it is the weather or the rules, not the Abruzzo mapping. The July
2024 flush of summer porcini is the largest miss; two (2019 drought, 2021 Chieti) miss by less than
0.05. None has been investigated further; see `species-ecology/abruzzo.md`, Sanity contrasts, for
each contrast's evidence and weaknesses.

**The served window.** On 28 September 2026 porcini score almost 0 across Abruzzo (mean 0.039): the
reanalysis puts the last 30 days at a median 27 % of the cells' normal rain, and porcini's 30-day
rain factor is 0 below 50 %; season, habitat and altitude are at or near full credit. Marche read
the same on 26 September (35 % of normal, mean 0.003): a dry September across central Italy, not the
Abruzzo rules. Ovoli mean 0.08, gallinacci 0.23, with 3.8 % of cells at 0.6 or more on the combined
score.

## After the deploy: what to verify

The stores were rsync'd to the server on 2026-09-28 (`deploy/rsync-region-data.sh abruzzo`, 208
files, 283 MB, no redeploy). The server serves a region only when its YAML is in the deployed code
and its stores are on disk, so they stay inert until `main` with `config/regions/abruzzo.yaml` is
deployed by the rail's "Deploy pulled main" step (with the daily job, which brings the weather and
scores up to that day). Then check:

- [ ] `https://mappafunghi.app/abruzzo` and `/abruzzo/porcini`, `/abruzzo/ovoli`,
  `/abruzzo/gallinacci` show real scores for today (not fixtures), and a tapped cell's "why this
  score" names Abruzzo habitats (beech; hop-hornbeam as mixed broadleaf; black pine as mountain
  pine).
- [ ] `https://api.mappafunghi.app/regions` lists `abruzzo`; the hub `/` lists it and colours it
  from `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Abruzzo URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/abruzzo` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Abruzzo", description, canonical, og image `og/abruzzo.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1284).
- [ ] `/credits` shows "Regione Abruzzo — Carta Tipologico-Forestale", CC BY-NC 3.0.
- [ ] The next morning's daily job has a `region_done` line for `abruzzo`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **Non-commercial forest map.** The Carta Tipologico-Forestale is CC BY-NC 3.0 (Sources above). A
  commercial use of the app would need CLC IV instead (−25 % forest) or the Region's permission.
- **The forest map is from 2009.** Seventeen years of abandonment have turned fields into
  woodland ("Latifoglie di invasione" were already "in continuo aumento"), so the map is if
  anything short of today's woods; INFC 2015 agrees within 2 %.
- **Rain scale borrowed** from Umbria and Campania (Weather above), and extrapolated above about
  1,000 m, where half of Abruzzo's woodland lies; card `fix-rain-calibration-region-borders.md`.
- **Region lookup by bbox.** Abruzzo's bbox overlaps Marche's southern edge (Ascoli Piceno, the
  Laga's Marche side), Lazio's eastern edge (Amatrice, Sora) and the north of Molise.
  `findRegionAt` picks the first registered bbox that holds a point, so a GPS fix or search there
  may be offered the wrong region. Card `fix-region-lookup-by-boundary.md`.
- **No validation to speak of:** 6 usable sightings in ten years (Validation above).

## Data

- cells: 11189
- woodland cells: 3782
- INFC deviation: -2.1% (grid 402,905 ha vs 411,588 ha) — within ±10 %
- weather nodes: 55
- years stored: 2016–2026 (11 years)
- sightings kept: 8
- backtest AUC (auc_local, model, all): gallinacci 0.922, porcini 0.704
- sanity contrasts: 11/16 passed

