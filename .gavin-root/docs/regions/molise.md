# molise

Region #13 of the full-Italy rollout (card `region-molise.md`). API id `molise`, web slug
`/molise`, ISTAT COD_REG 14. Config: `api/src/api/config/regions/molise.yaml`. A small region of
hills and mid mountains: Turkey-oak and downy-oak woods over most of it, from the Fortore and the
Frentani hills to the Alto Molise; beech on the Matese, the Montagnola di Frosolone, the Mainarde
and the Alto Molise, where the relict silver fir of Pescopennataro, Capracotta and Collemeluccio
grows; a few pine woods on the Adriatic dunes.

## Sources

| need | source | licence | notes |
|---|---|---|---|
| boundary, comuni, localities | ISTAT 2025 generalised boundaries, Basi territoriali 2021 | CC BY 4.0 | national files, shared cache |
| woodland (how much and which kind) | ISPRA, **Carta della Natura della Regione Molise**, carta degli habitat 1:25,000, 2021 (`ispra_cnat_molise`) | CC BY 4.0 | one GeoPackage on ISPRA's SDI, 27,661 polygons, 103 CORINE Biotopes habitats |
| terrain, soil pH | Copernicus DEM GLO-30, SoilGrids 2.0 | as Tuscany | |
| weather | CDS ERA5-Land (history), Open-Meteo ECMWF IFS (recent days, forecast, seasonal) | CC BY 4.0 | |
| sightings | GBIF (bbox), iNaturalist place 10871 "Molise, IT" | per record | counts per cell only |

**What was checked (2026-09-30).**

- **Regione Molise, Carta delle Tipologie Forestali** (Carta forestale su basi tipologiche,
  1:10,000, 13 categories and 34 types, approved by DGR 252 of 16 March 2009; 2011 in ISPRA's
  lineage). The Region's page (`regione.molise.it`, IDPagina 737, Servizio Tutela e Valorizzazione
  Patrimonio Forestale) offers the map and its report as **PDFs only**, under the site's "Tutti i
  diritti riservati". No vector download, no licence.
- **The regional geoportale** (`geo.regione.molise.it`, `www.geo.regione.molise.it`): the host
  names no longer resolve (DNS, 2026-09-30); a 2024 survey by the Istituto Centrale per
  l'Archeologia already found it "non consultabile causa malfunzionamento". Its download service
  was restricted when it worked. The Region's cartography page lists only the Alto Molise mountain
  community's forest types.
- **Regione Molise open data** (`opendata.regione.molise.it`): tables only, no land-use or forest
  layer. No Molise forest dataset on dati.gov.it.
- **ISPRA Carta della Natura, Regione Molise, 1:25,000, 2021** (Ceralli D. 2021; report Ceralli
  D., Laureti L., ISPRA Rapporti 348/2021): a full revision, on the AGEA 2018 orthophotos and the
  new national legend, of the 2015 edition. For the forest habitats it used the Region's 1:10,000
  Carta Forestale su Basi Tipologiche (2011) as its information layer ("si è ricorsi al
  contributo della Carta Forestale su Basi Tipologiche della Regione Molise"), and the Region's
  2012 CLC IV land-use map at 1:25,000 as its base. The GeoPackage
  (`sdi.isprambiente.it/download_ogc/cnat/CNAT_Habitat_Molise.gpkg`, dated 2022-08-01, EPSG:25832)
  is the one the RNDT record `ispra_rm:CNAT_MOL_2015_v1` links; its 631 polygons of 4D_n match the
  2021 report's habitat table, so it holds the 2021 map. The record declares **CC BY 4.0** and also
  asks that use for research, teaching, dissemination, study and leisure be requested and credited
  ("previa richiesta"), the same wording as Campania's record; ISPRA's legal notes release Carta
  della Natura data under CC BY 4.0.
- **CLC 2018 IV level alone** (Umbria's path), measured on ISPRA's layer clipped to the ISTAT
  boundary: **120,284 ha of forest, −21.5 % against INFC 2015** (3112 deciduous oak 87,769 ha, 3115
  beech 16,143 ha, 3113 mixed broadleaf 8,635 ha; 324x transitional 21,352 ha). CLC's 25 ha unit
  drops the small hill woods of a region where woodland is broken up by fields.

**Decision: the Carta della Natura for both layers**, as Campania and Calabria use theirs. It is
the only open vector map of Molise's woodland with forest types, it carries the Region's own
forest-type map into its forest habitats, and it lands within 4 % of INFC. The credit reads
"Carta della Natura della Regione Molise © ISPRA, CC BY 4.0" (`sources.yaml`, and
`web/src/credits.ts`).

Class mapping (`molise.yaml`, one layer gives both), whole-map areas:

| `codice_corine` | group | habitat | ha |
|---|---|---|---|
| 41.741 temperate Turkey oak, 41.7511 Mediterranean Turkey oak, 41.7512 Turkey oak with Hungarian oak, 41.731 temperate downy oak, 41.732 Mediterranean downy oak | broadleaf | deciduous_oak | 113,263 |
| 41.18 southern Italian beech | broadleaf | beech | 16,637 |
| 41.81 hop-hornbeam, 41.88_m ash, maple and hornbeam, 4D_n synanthropic woods, 41.F1 field elm, 41.D aspen, 41.4 ravine woods | broadleaf | mixed_broadleaf | 12,056 |
| 44.61 poplar, 44.13 and 44.14 willow, 44.63 narrow-leaved ash (riparian) | broadleaf | riparian | 8,859 |
| 45.32 supramediterranean and 45.31 thermo-mesomediterranean holm oak | broadleaf | evergreen_oak | 1,845 |
| 41.L_n robinia and ailanthus, 44.D2_n alien riparian woods | broadleaf | exotic_broadleaf | 1,296 |
| 41.9 chestnut | broadleaf | chestnut | 398 |
| 42.G_n conifers planted outside their range, 83.31_m conifer plantations | conifer | mountain_pine | 5,160 |
| 42.15 southern Apennine silver fir | conifer | fir_spruce | 398 |
| 16.29 wooded dunes (Aleppo and stone pine) | conifer | mediterranean_pine | 128 |
| 32.3_m macchia, 32.4_m thermo-mesomediterranean garrigue, 16.27 and 16.28 dune juniper and sclerophyll scrub | macchia | macchia | 804 |
| 31.81 deciduous scrub, 32.A Spartium broom, 31.88_m hill juniper scrub, 31.844 broom, 31.8A bramble, 31.87 recent clearings, 44.11/44.12 willow scrub, 44.D1_n alien riparian scrub | transitional | transitional_woodland_shrub | 21,246 |
| **left out:** 83.325_m broadleaf plantations (1,818), 83.15_m orchards (793), 83.321 poplar plantations (227), 85 parks (901), 32.23 Ampelodesmos steppe (282), 31.43 prostrate-juniper heath (148), 31.863 bracken (54), 32.6 supramediterranean garrigue (41), grassland and rock | — | — | |

- **Synanthropic woods (4D_n, 3,473 ha) are mixed broadleaf**, not exotic. ISPRA's report
  describes them as mixed deciduous woods of very variable make-up on abandoned fields, olive
  groves, orchards and pastures near villages: feral cherry, chestnut, walnut, hazel, willow,
  poplar, lime, maple, ash and hop-hornbeam, with some robinia and ailanthus (EUNIS G5.2).
- **42.G_n is two things.** ISPRA: below about 700 m, plantations of Mediterranean pines (Aleppo
  pine) and cypress, mostly round the two reservoirs (Guardialfiera on the Biferno, Occhito on the
  Fortore); above 700 m, black pine, spread over the whole region. The polygons' elevations match
  (median about 770 m; 10th percentile 280 m, 90th 1,140 m; Guardialfiera, Casacalenda, but also
  Macchiagodena, Santa Maria del Molise, Vastogirardi, Castelpetroso). The grid gives a code one
  habitat, so all of them are `mountain_pine`, as CLC IV files black pine (3122) and Calabria files
  its 42.G_n; the low half is misfiled, 2.2 % of the woods.
- **Silver fir** (42.15, 398 ha) is Pescopennataro (306 ha, the Abeti Soprani and Monte Campo),
  Agnone, Sant'Angelo del Pesco, Pescolanciano (Collemeluccio) and Belmonte del Sannio. **Chestnut**
  (398 ha) is almost all at the foot of the Matese (San Massimo, Bojano, Campochiaro, Guardiaregia,
  Roccamandolfi). **Holm oak** is the Volturno hills (Monteroduni 1,020 ha of the 1,516 ha of
  45.32) and Mafalda on the Trigno (45.31).
- Scrub follows Calabria's mapping of the same legend (31.88_m hill juniper scrub is
  transitional); the montane prostrate-juniper heath (31.43) is left out as Abruzzo leaves its
  montane juniper out. Broadleaf plantations (83.325_m, walnut and cherry arboriculture on former
  fields) stay farmland, as INFC files arboriculture outside bosco.

## Config

- **Boundary.** ISTAT COD_REG 14; bbox `[13.94, 41.36, 15.17, 42.08]`, the ISTAT 2025 boundary's
  extent (13.9410, 41.3649, 15.1616, 42.0702) rounded outward to 0.01°. Inside area 4,440 km².
- **Forest.** The Carta della Natura for groups and types (Sources above).
- **Sightings.** iNaturalist place 10871, resolved by name ("Molise, IT", admin level 10) on
  2026-09-30.
- **Model.** A borrowed rain scale (Weather below). No other override.

## Woodland grid

Built 2026-09-30 (`uv run python -m api.grid.build --region molise`, 17 s with the map cached).

- Cells 4,703; inside area 4,440 km².
- **Woodland cells 1,455** (31 % of the cells). 119 of the 136 comuni have woodland cells. By
  province: Isernia 924, Campobasso 531. Most wooded comuni: Agnone and Vastogirardi (40 cells
  each), San Pietro Avellana and Guardiaregia (36), Sepino (34), Filignano and Roccamandolfi (32),
  Pizzone (31).
- **Forest area 159,234 ha vs INFC 2015 bosco 153,248 ha: +3.9 %**, within ±10 % (the whole map,
  outside the boundary clip, holds 160,042 ha).
- Every woodland cell takes its forest types from its own polygons (`borrowed_type_fraction` 0).
  The dominant habitat covers a median 87 % of a cell's wooded area.
- Terrain: woodland elevation median **728 m** (5th–95th percentile 356–1,317 m), max 1,781 m;
  116 woodland cells above 1,200 m and 23 above 1,500 m (Abruzzo: median 1,061 m, max 1,940 m).
  Slope median 14.8°, 4 % of woodland cells above 25°; 25 cells have no aspect.
- Soil pH (SoilGrids, not scored): woodland median 6.81 (6.19–7.32, 5th–95th percentile).

| habitat | share of wooded area | cells where dominant | median elevation of those cells |
|---|---|---|---|
| deciduous_oak (Turkey oak, downy oak) | 67.3 % | 1,123 | 682 m |
| beech | 12.8 % | 182 | 1,242 m |
| mixed_broadleaf (hop-hornbeam, ash-maple, synanthropic woods) | 7.4 % | 98 | 767 m |
| transitional_woodland_shrub | 5.8 % | 5 | 1,055 m |
| mountain_pine (black pine; Aleppo pine and cypress below 700 m) | 2.2 % | 16 | 835 m |
| riparian | 2.1 % | 6 | 357 m |
| evergreen_oak | 1.4 % | 19 | 477 m |
| fir_spruce (silver fir) | 0.3 % | 4 | 1,243 m |
| chestnut | 0.3 % | 2 | 665 m |
| exotic_broadleaf, macchia | 0.2 % or less each | 0 | |

Threshold sensitivity (recomputed from stored fractions with the 0.25 km² minimum, a cell off the build):

| minimum forest share | 0.3 | 0.4 | **0.5** | 0.6 | 0.7 |
|---|---|---|---|---|---|
| woodland cells | 2,191 | 1,786 | **1,454** | 1,135 | 841 |

## Weather

- Points: 32 candidates on the 0.2° lattice, **32 on land**; all 1,455 woodland cells weighted,
  none out of reach.
- **Lattice and lapse-rate check** (`uv run python -m api.weather.checks lattice --region molise`,
  80 land nodes at 0.1°, three 14-day windows of 2024, run 2026-09-30). Cooling per km of height
  across nodes, median of daily fits:

  | variable | Jan | Jul | Oct | all | national config | difference |
  |---|---|---|---|---|---|---|
  | temperature_2m_max | 5.84 | 4.01 | 4.46 | 4.59 | 4.5 | +0.09 |
  | temperature_2m_mean | 5.50 | 4.07 | 4.52 | 4.59 | 4.5 | +0.09 |
  | temperature_2m_min | 4.48 | 3.20 | 4.06 | 4.03 | 4.2 | −0.17 |
  | soil_temperature_0_to_7cm_mean | 4.38 | 4.50 | 4.17 | 4.24 | 3.7 | +0.54 |

  Every fitted rate is within 1 °C/km of the national one, so **the national lapse rates are kept**
  (no weather override). Leave-out test on the 0.2° lattice (stride 2, 59 targets), RMSE with the
  national rates vs none vs 6.5 °C/km: mean air temperature 0.25 / 0.65 / 0.30 °C, minimum
  0.45 / 0.70 / 0.50 °C, maximum 0.35 / 0.75 / 0.33 °C, soil 0.37 / 0.63 / 0.45 °C; daily rain RMSE
  1.19 mm either way.

### Rain scale: borrowed, no Molise gauge check

Molise publishes no open daily rain:

- the regional **Centro Funzionale** (Protezione Civile, Campochiaro; heir of the Servizio
  Idrografico of Pescara) runs 22 rain gauges in its alert network and 36 more stations, and
  releases their data to third parties only on a request sent by PEC, under a regional regulation
  and **for a fee** from its price list (`protezionecivile.molise.it/la-rete/`); it publishes no
  Annali online, and ISPRA's HIS Central page for its network is gone (404);
- **ARSARP**'s agrometeorological network gives data on request (`meteo@arsarp.it`);
- the national **Meteo Hub** (Agenzia ItaliaMeteo) carries the Civil Protection network as
  `dpcn-molise` (Trivento, Campochiaro, Capracotta, Campitello Matese, Ponte Liscione…), public,
  but only the last few days are served without a login ("to access archived data the user has to
  be logged"). A free Meteo Hub account would open the archive: the one route to a Molise gauge
  check (Known limitations).

So there is no gauge check, and the scale is borrowed, as Abruzzo's and Marche's are. It cannot
be the national one: that scales `era5_seamless` only, while the rain normals are scaled whatever
their source, and every CDS gauge fit so far finds the national scale 25–50 % too wet here.
**`molise.yaml` sets the mean of the three measured fits on the same CDS rain that surround
Molise, 0.84 + 0.36 per km, clamped at 1,200 m**, over `era5_land_cds` and `era5_seamless`:

| fit (CDS rain, gauges) | a | b per km | factor at 200 / 500 / 800 / 1,200 / 1,600 m | mean over Molise's woodland |
|---|---|---|---|---|
| Lazio (92 ARSIAL agrometeo gauges, 1–1,176 m) | 0.82 | 0.23 | 0.87 / 0.93 / 1.00 / 1.10 / 1.19 | 1.00 |
| Campania (33 agrometeo gauges, 11–769 m) | 0.77 | 0.52 | 0.87 / 1.03 / 1.19 / 1.39 / 1.60 | 1.17 |
| Puglia (42 Protezione Civile gauges, 27–914 m, monthly totals; clamped at 900 m) | 0.93 | 0.34 | 1.00 / 1.10 / 1.20 / 1.24 / 1.24 | 1.17 |
| **Molise (mean, used; clamped at 1,200 m)** | **0.84** | **0.36** | **0.91 / 1.02 / 1.13 / 1.27 / 1.27** | **1.11** |
| Abruzzo (borrowed: mean of Umbria and Campania) | 0.83 | 0.43 | 0.92 / 1.04 / 1.17 / 1.35 / 1.52 | 1.16 |
| national (Tuscan gauges, `era5_seamless`) | 1.28 | 0.29 | 1.34 / 1.43 / 1.51 / 1.63 / 1.74 | 1.50 |

Lazio lies west of the Mainarde, Campania south of the Matese, Puglia east of the Fortore; Abruzzo's
scale is itself borrowed, so it is not averaged in. The three agree on the shape (the reanalysis a
little wet in the low hills, dry higher up). **The clamp at 1,200 m** is the highest gauge any of the
three fits holds (Lazio's Accumoli, 1,176 m); above it the factor stays at 1.27 rather than follow
an extrapolated slope. It touches 116 woodland cells (the Matese, Frosolone, the Alto Molise beech);
Abruzzo, unclamped, reads 1.35–1.52 across the border there. A national or per-zone rain calibration
(card `fix-rain-calibration-region-borders.md`) should replace it.

## Sightings

`uv run python -m api.sightings.ingest fetch --region molise` (2026-09-30): **12 GBIF records** for
the three groups over the bbox, all of them iNaturalist observations, and **none from iNaturalist**
in the last two weeks. After the quality filters (2 too imprecise, 2 with unknown uncertainty) 10
are kept, and **2 land on Molise's woodland cells**: gallinacci, June 2023, in Turkey oak at Busso
(690 m), west of Campobasso; porcini (*B. reticulatus*), August 2025, in pure beech at Campitello
Matese (1,595 m). No ovoli. The other 8 are outside the region inside the bbox (the Campanian
Matese in September 2022 and October 2024, the Alto Sangro and the Alto Vastese in Abruzzo, an ovolo
in September 2025 just south of the border) or on cells that are not woodland (three 2009–2010
records at Sant'Angelo del Pesco, near Capracotta, in a scrub cell). Molise is the thinnest region
so far: Abruzzo had 8 records on its woodland, Valle d'Aosta 4.

## Species rules

Full evidence: `.gavin-root/docs/species-ecology/molise.md`; rules in
`api/src/api/config/species/molise/` (15 new references, all opened, with the rain prior 16).

- **All three groups and six keys kept, on the thinnest evidence of any region.** The national
  checklist had 95 fungi on record for Molise and calls it one of "the less investigated Regions";
  iNaturalist holds 4 records of the six keys. The regional law regulates the porcini group, the
  chanterelle and the closed ovolo (L.R. 4/2008, amended to L.R. 7/2026: 3 kg a day plus one
  fruit body, dawn to dusk, porcini caps under 3 cm and chanterelle caps under 2 cm banned, closed
  ovoli banned; no season calendar). Funghi Magazine's national bulletins name Molise often, in a
  sentence or two. *B. pinophilus* has no Molise record or source of its own and stays, as in Lazio,
  Umbria and the Marche: the law covers the porcini group, the Campania checklist has it on the
  shared Matese, and its hosts are here.
- **Altitude bands move up**, as in the neighbours (only *B. aereus* keeps Tuscany's): *B. edulis*
  and *B. pinophilus* full to 1,800 m, zero at 2,000 m; *B. reticulatus* full to 1,600 m, zero at
  1,900 m (Campania's band: the one Molise record, at 1,595 m in beech, scored 0 on Tuscany's);
  gallinacci full to 1,400 m, zero at 1,900 m; the ovolo full to 900 m, zero at 1,200 m.
- **Three season windows move.** The gallinacci mountain window ramps 15 May → 15 June (Tuscany 1
  June → 1 July), as in Abruzzo and Campania; the ovolo is in full season from 1 August (Tuscany 1
  September), as in Abruzzo; *B. aereus*'s summer/autumn handover moves from 400–600 m to 600–800 m,
  as in Campania and Puglia, so the oak hills (median 654 m) keep the black porcini the bulletins
  report there in September and October.
- **13 habitat affinities follow what the classes hold here.** `mixed_broadleaf` (hop-hornbeam,
  old-field regrowth, ash-maple-hornbeam) goes to 0.1 for *B. edulis* and *B. pinophilus*;
  `mountain_pine` (black pine above 700 m, Aleppo pine and cypress below) to 0.3 for the three pine
  porcini and 0.1 for gallinacci; the thorn, broom and juniper scrub (`transitional_woodland_shrub`)
  down for all six keys; deciduous oak up to 0.6 for gallinacci (the Busso record, the neighbours).
- **Unchanged:** weather rules, stoppers, growth clocks. No Molise study gives numbers.
- **Effect on the grid** (habitat × altitude gates, woodland mean, Tuscan rules → Molise rules):
  *B. edulis* 0.82 → 0.76, *B. reticulatus* 0.94 → 1.00, *B. aereus* 0.80 → 0.80, *B. pinophilus*
  0.72 → 0.67, ovoli 0.73 → 0.82, gallinacci 0.93 → 0.99.
- **Press contrasts** (`molise/sanity.yaml`): 17, written before any Molise score existed, 14 for
  porcini, 1 for ovoli and 2 for gallinacci. Molise's local press gives almost no season verdicts:
  16 rest mainly on Funghi Magazine's bulletins, often with Molise lumped with Abruzzo, Campania or
  Puglia; one (2017) on a single sentence from a Campobasso mushroom show.
- **Open questions:** Turkey oak and downy oak are one class; the ovolo's August start and 1,200 m top
  rest on one blog and the bulletins; the bulletins blame the wind for wasted rain, which only the
  drying stopper reads; `mountain_pine` mixes Aleppo and black pine. A UniMol and AMB mycological
  survey of Pescopennataro began in October 2025 and may one day give records.

## Validation

Scored 2016-03-18 to 2026-10-07 on 2026-09-30 (rules version `70673b254ada`, the borrowed rain
scale, CDS history with CDS snowfall to 19 September, then Open-Meteo's archive and the ECMWF IFS
forecast): 1,455 woodland cells × 3,856 days per key, no cell-day without a score. `onboard` ran the
hold-out backtest and the sanity check; the train-season backtest (`--seasons train --label
onboard-train`) and the ovoli and gallinacci sanity runs (`--group`) were run after it.

**No tuning: the priors ship.** Usable presences (unique, unobscured group-cell-day sightings on
woodland cells) in the train seasons 2016–2023: **1** (gallinacci, June 2023), against the 50 the
parent plan asks for. Hold-out 2024–2025: **1** (porcini, August 2025). No ovoli.

**Backtest** (model; calendar and habitat baselines in brackets):

| group | split | n | `auc_local` | `auc_region` | `auc_time_effort` |
|---|---|---|---|---|---|
| gallinacci | train | 1 | 0.63 [0.51, 0.51] | 0.95 [0.57, 0.51] | 0.84 [0.48, 0.50] |
| porcini | hold-out | 1 | 0.21 [0.50, 0.50] | 0.61 [0.80, 0.50] | 0.41 [0.50, 0.50] |

Two sightings in ten years say nothing either way. The gallinacci record (Busso, 6 June 2023)
scored 0.93, high for the day across the region; the porcino (Campitello Matese, 10 August 2025)
scored 0.16 against a regional mean of 0.30 that day, the model putting the Matese top below the
hills after a dry July (0 until 28 July, then 0.18–0.20 until mid-August). Not investigated further.
Validating Molise needs records with locations: the Pescopennataro survey, the ASReM mycological
inspectorate, or the neighbours' records pooled.

**Sanity check** (`molise/sanity.yaml`, 17 contrasts written before any Molise score existed),
each contrast read against its own group (`backtest/molise/onboard/sanity_<group>.csv`):

| contrast | group | higher window | lower window | holds |
|---|---|---|---|---|
| Mountains, June 2018: second half > first half | porcini | 0.524 | 0.741 | no |
| Late June: mountains > hills | porcini | 0.366 | 0.316 | yes |
| Molise late June 2022 > 2024 | porcini | 0.187 | 0.142 | yes |
| Molise 2019: September > August | porcini | 0.915 | 0.382 | yes |
| Molise September 2019 > 2020 | porcini | 0.915 | 0.002 | yes |
| Molise 2017 < normal | porcini | 0.494 | 0.809 | no |
| Molise 2020: summer > September | porcini | 0.528 | 0.013 | yes |
| Campobasso August 2020 > 2023 | porcini | 0.411 | 0.047 | yes |
| Campobasso > Isernia, August 2020 | porcini | 0.357 | 0.392 | no |
| Isernia–L'Aquila border > Campobasso, August 2023 | porcini | 0.080 | 0.239 | no |
| Alto Molise August 2024 > 2023 | porcini | 0.322 | 0.001 | yes |
| Campobasso late August 2025 > 2023 | porcini | 0.395 | 0.252 | yes |
| Molise first half of October 2022 > 2023 | porcini | 0.817 | 0.021 | yes |
| Molise early October 2024 > 2020 | porcini | 0.819 | 0.665 | yes |
| Campobasso ovoli, mid-August 2025 > 2023 | ovoli | 0.331 | 0.065 | yes |
| Molise gallinacci June 2023 > 2024 | gallinacci | 0.887 | 0.467 | yes |
| Molise gallinacci late June 2022 > 2024 | gallinacci | 0.197 | 0.179 | yes (barely) |

**13 of 17 hold** (porcini 10/14, ovoli 1/1, gallinacci 2/2). The `Data` section's "13/17" is the
default run, which scores all 17 on the porcini group and happens to give the same total. Of the
four misses, the 2017 contrast rests on one sentence and the August 2023 border contrast on place
names not found in a gazetteer (species-ecology/molise.md, Sanity contrasts); the Campobasso–Isernia
one misses by 0.04; the June 2018 timing puts the two halves of June the other way round.

**The served window.** On 30 September 2026 porcini score almost 0 across Molise (mean 0.096): the
reanalysis puts the last 30 days at a median 26 % of the cells' normal rain, and porcini's 30-day
rain factor is near 0 there; season, habitat and altitude are at or near full credit. Abruzzo read
the same on 28 September (27 % of normal): a dry September across central Italy, not the Molise
rules. Ovoli mean 0.11, gallinacci 0.20, with 8.5 % of cells at 0.6 or more on the combined score.

## After the deploy: what to verify

The stores are on the server: `deploy/rsync-region-data.sh molise` ran on 2026-09-30 with
`DATA_DIR` at the shared data root and copied 204 files (129 MB) of grid, weather, scores,
sightings, climatology, history and outlook into `/srv/mushma-data`, file counts matching local.
The server serves a region only when its YAML is in the deployed code and its stores are on disk,
so the stores stay inert until `main` with `config/regions/molise.yaml` is deployed by the rail's
"Deploy pulled main" step (with the daily job, which brings the weather and scores up to that day).
Then check:

- [ ] `https://mappafunghi.app/molise` and `/molise/porcini`, `/molise/ovoli`, `/molise/gallinacci`
  show real scores for today (not fixtures), and a tapped cell's "why this score" names Molise
  habitats (Turkey oak as deciduous oak; beech; black pine as mountain pine).
- [ ] `https://api.mappafunghi.app/regions` lists `molise`; the hub `/` lists it and colours it from
  `/overview`.
- [ ] `https://mappafunghi.app/sitemap.xml` has the four Molise URLs (built from the registry).
- [ ] Lighthouse SEO is 100 on `/molise` (prerendered title "Mappa Funghi – porcini, ovoli e
  gallinacci in Molise", description, canonical, og image `og/molise.png`, JSON-LD Dataset with
  `sameAs` Wikidata Q1443).
- [ ] `/credits` shows "ISPRA — Carta della Natura della Regione Molise 1:25.000", CC BY 4.0.
- [ ] The next morning's daily job has a `region_done` line for `molise`
  (`journalctl -u mushma-daily`), and its Open-Meteo call count stays inside the budget.

## Known limitations

- **No Molise rain gauges.** The scale is borrowed from Lazio, Campania and Puglia (Weather above)
  and clamped at 1,200 m. A free Meteo Hub account (Agenzia ItaliaMeteo) would open the archive of
  the Civil Protection's `dpcn-molise` gauges for a real check; card
  `fix-rain-calibration-region-borders.md`.
- **The forest map is ISPRA's, not the Region's.** The Region's 1:10,000 forest-type map is only a
  PDF; ISPRA drew its forest habitats from it but at 1:25,000 and on its own legend, which does not
  split Turkey oak from downy oak by type and files every planted conifer in one class (42.G_n,
  Aleppo pine low, black pine high, all `mountain_pine` here).
- **Region lookup by bbox.** Molise's bbox overlaps Abruzzo's, Campania's, Lazio's and Puglia's;
  59 % of Molise's woodland cells lie inside one of theirs, and Molise's holds 1,300 of theirs.
  Molise is registered last in `web/src/regions/index.ts`, so no served region regresses, but from
  the hub a fix or a search in the Alto Molise is offered Abruzzo, on the Molise Matese Campania.
  Inside `/molise` the current-region-first rule serves it. Card `fix-region-lookup-by-boundary.md`.
- **No validation to speak of:** 2 usable sightings in ten years (Validation above).

## Data

- cells: 4703
- woodland cells: 1455
- INFC deviation: +3.9% (grid 159,234 ha vs 153,248 ha) — within ±10 %
- weather nodes: 32
- years stored: 2016–2026 (11 years)
- sightings kept: 2
- backtest AUC (auc_local, model, all): porcini 0.213
- sanity contrasts: 13/17 passed

