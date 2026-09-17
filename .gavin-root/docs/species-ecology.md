# Species ecology: cited rules for porcini, ovoli and gallinacci

Research date: 2026-09-17. Card: M3 · Species ecology research. Traces to PRD → Species (v1),
Model (Factors, Score semantics, Known gaps) and Principles (explainable).

This document turns foraging lore and the literature into rules the M3 engine can encode. Each rule
has a source and a confidence. It covers **fruiting conditions only**: nothing here is about edibility
or identifying specimens.

| what | where |
|---|---|
| This synthesis: key findings, rules at a glance, season cross-check, variable mapping, habitat vocabulary, combined-score proposal, hand-offs | this file |
| Full evidence per species, rule by rule, with local reference lists (`[R1]`…) | [`species-ecology/porcini.md`](species-ecology/porcini.md), [`species-ecology/ovoli.md`](species-ecology/ovoli.md), [`species-ecology/gallinacci.md`](species-ecology/gallinacci.md) |
| Draft rule config (one file per species key), shared bibliography, JSON Schema, scoring semantics, lint | [`species-rules/`](species-rules/README.md) |

## How to read the rules

**Confidence** (every rule carries one):

- **strong**: peer-reviewed quantitative field data linking fruiting to the factor, ideally Italian or
  Mediterranean, or several consistent peer-reviewed sources.
- **plausible**: qualitative statements from reputable mycological sources (societies, universities,
  regional agencies, IGP specifications), or quantitative data from another climate or a related taxon
  that we extrapolate.
- **folklore**: forager lore, blogs and commercial pages with no traceable data. Recorded when it is
  widespread, because the backtest can test it.

**Derived numbers.** Most parameters are **derived**: turned into a trapezoid from a qualitative
statement ("about two weeks after rain"), from another climate, or from sightings. The config marks
them `derived: true` and says how in `notes`. They are **priors for the backtest**, not findings.

**References.** 91 sources in [`species-rules/references.yaml`](species-rules/references.yaml): 45
peer-reviewed, 1 preprint, 4 theses, 14 institutional, 7 mycological society, 1 monograph, 2 datasets,
2 of our own analyses and 15 web pages (the folklore). 73 were opened (`verified`) and 18 are
`snippet-only`. Every DOI cited was checked to resolve (doi.org handle API, 2026-09-17).

## Key findings

1. **Only *Boletus edulis* has quantitative weather–fruiting studies.** These are a Tuscan site on
   Monte Amiata (Salerni et al. 2023), a German beech preprint, and Spanish pine yield models. The
   other three porcini, ovoli and gallinacci borrow the rain logic and shift temperature bands using
   qualitative sources. Of the 81 rule factors drafted, 64 are scored and **only 3 of those are
   `strong`**; 41 are `plausible` and 20 `folklore`. The other 17 are disabled alternatives or rules on
   missing data, and 25 more effects are recorded as known gaps.
2. **The best-supported weather rule for all three is rain over the previous ~30 days** (Tuscan oak
   forests, all macrofungi; Salerni et al. 2002). For *B. edulis* there is also an event lag: counts
   peak about **12 days after a ≥20 mm rain day** (Amiata). Gallinacci respond to sustained moisture
   rather than single storms, and their fruit bodies last about 44 days on average (Pilz et al. 2003).
   Their lag window is therefore long and flat.
3. **Season corrections to the PRD hypotheses:**
   - **Ovoli** peak in **September to early November** in Tuscany (median record 13 October), not
     July–October.
   - ***B. aereus*** is a lowland autumn fruiter. The IGP's July–September applies to uplands.
   - **Gallinacci** have a May–June mode, a July–August trough and a large October–November mode that
     runs into winter at low elevation.
4. **Tuscan "*Cantharellus cibarius*" is mostly not *C. cibarius* sensu stricto.** The European
   revision (Olariaga et al. 2017) excludes it from Mediterranean climates, so records are mostly
   *C. pallens* and *C. alborufescens*. The rules target *C. cibarius* **s.l.** using genus-level
   records.
5. **Hosts are the most reliable static signal.** Ovoli need oak or chestnut (strong). Chestnut is the
   strongest gallinacci habitat: present in 9 of 9 Tuscan chestnut plots against 1 of 4 limestone oak
   plots. Chestnut avoids limestone, so it doubles as a soil-pH proxy.
6. **Soil pH is the largest v1 gap for gallinacci** (pH 4.0–5.5 for the acidophilous members). It
   also matters for ovoli (siliceous, slightly acid; sources disagree) and appears in porcini notes.
   v1 will **over-score calcareous oak and hop-hornbeam cells** for gallinacci.
7. **Sightings are very sparse.** Tuscan fruit-body records: *B. edulis* 31, *B. reticulatus* 24,
   *B. aereus* 61, *B. pinophilus* 7 (iNaturalist, verifiable); ovoli 50; *Cantharellus* 116. They are
   mostly recent (2019 onward). Validate **porcini as a group**, pool seasons, and consider central-Italy
   records for testing rule *shape*.
8. **Four record traps** (details under Hand-offs):
   - 28 of 39 Tuscan GBIF *B. reticulatus* rows are soil-DNA `MATERIAL_SAMPLE`s.
   - GBIF's *A. caesarea* key holds about 785 US and Mexican records of other species.
   - "*Boletus pinicola*" does not match in the GBIF backbone.
   - GBIF keeps *C. cinereus* and *C. melanoxeros* inside *Cantharellus*.
9. **Open-Meteo serves every weather input the rules use**, in both the history and forecast APIs,
   under the same daily variable names (verified by calling both). The traps are model mixing in the
   history API and model-scaled soil moisture (see Weather variables).
10. **Drying wind, frost thresholds, the "thermal shock" trigger and soil-temperature bands are mostly
    lore.** No source gives wind speeds or durations, so those numbers are guesses for the backtest to
    keep or drop.

## Rules at a glance

Full parameters, sources and notes are in the YAML files; the evidence behind each rule id (POR-*,
OVO-*, GAL-*) is in the appendices. "×" is a multiplier; trapezoids are `[zero, full, full, zero]`.

### Porcini (four keys, group score = max over them)

| factor | *B. edulis* | *B. reticulatus* (= *aestivalis*) | *B. aereus* | *B. pinophilus* | confidence |
|---|---|---|---|---|---|
| season (`DD-MM`) | 01-07 → 01-09 … 15-11 → 20-12 | 01-05 → 01-06 … 30-09 → 15-11 | ≥600 m: 15-06 → 01-08 … 30-09 → 31-10; ≤400 m: 01-07 → 01-09 … 15-11 → 15-12 | spring 01-05 → 20-05 … 30-06 → 20-07; autumn 15-08 → 15-09 … 15-11 → 15-12 | plausible |
| top hosts | beech 1.0, chestnut 0.9, fir/spruce 0.9 | chestnut 1.0, deciduous oak 0.9 | deciduous oak 1.0, chestnut 0.9, evergreen oak 0.8, macchia 0.7 | beech 0.9, fir/spruce, chestnut, mixed 0.8 | plausible |
| altitude (m) | 200 → 700 … 1600 → 1900 | 0 → 150 … 1100 → 1500 | … 800 → 1250 | 300 → 800 … 1600 → 1900 | plausible |
| rain trigger (driver, weight 2) | 3-day rain 10 → 30 mm; lag 6 → 10 … 16 → 24 days | same | same | same | strong (*edulis*) / plausible |
| 30-day rain (driver) | 20 → 80 mm | same | same | same | strong (*edulis*) / plausible |
| 20-day mean air temp (driver) | 6 → 10 … 17 → 22 °C | 9 → 13 … 21 → 25 °C | 10 → 14 … 22 → 26 °C | 4 → 8 … 15 → 20 °C | plausible (low outside *edulis*) |
| heat spike (Tmax ≥8 °C above prior 30-day mean in last 14 d) | ×0.5 | ×0.75 | ×0.75 | ×0.5 | plausible |
| frost (≥2 nights ≤0 °C in 7 d) | ×0.2 | ×0.1, plus cold nights (≥3 nights ≤5 °C) ×0.5 | ×0.4 | ×0.2 | folklore |
| snow (≥1 cm in 3 d) | ×0 | ×0 | ×0 | ×0 | plausible / folklore |
| drying (days with ET0 ≥4, or ≥5 for the summer taxa) | ≥3 days in 7 → ×0.6 | ×0.6 | ×0.6 | ×0.6 | folklore |
| disabled alternatives | soil temperature, 30-day water balance, soil-moisture percentile, 60-day % of normal rain, 45-day drought | water balance | water balance | water balance | — |
| known gaps | aspect, temperature-drop bonus, lag lengthening in cold, 100 m wood-edge buffer, stand age/thinning/litter/soil | aspect, temperature drop, wood edge, orchard age | aspect, wood edge, soil | aspect, wood edge, soil | — |

### Ovoli (*Amanita caesarea*)

| factor | rule | confidence | scored |
|---|---|---|---|
| season | 01-06 → 01-09 … 05-11 → 30-11 | plausible | yes |
| habitat | deciduous oak 1.0, chestnut 0.9, evergreen oak 0.7, macchia and transitional scrub 0.4; conifers ≈0 | strong (hosts) | yes |
| altitude | full to 750 m → 0 at 1100 m | plausible | yes |
| rain trigger | 3-day rain 10 → 30 mm; lag 6 → 10 … 20 → 28 days (weight 1) | folklore | yes |
| 30-day rain | 25 → 75 mm | plausible | yes |
| soil temperature 0–7 cm, 14-day mean | 9 → 14 … 26 → 32 °C (upper edges are placeholders) | plausible | yes |
| evaporative demand | 7-day mean ET0 4 → 6 mm/day: ×1 → ×0.4 | plausible | yes |
| cold nights | 7-day mean Tmin 5 → 10 °C, floor 0.3 | plausible | yes |
| frost | any Tmin ≤0 °C in 7 days → 0 | folklore | yes |
| air temperature · soil moisture 0–7 cm · waterlogging | alternatives | plausible / folklore | no |
| gaps | south aspect near the upper limit, spring rain (Mar–May % of normal), drying wind (gust + RH), temperature-dependent lag, siliceous substrate, canopy openness and management | — | — |

### Gallinacci (*Cantharellus cibarius* s.l.)

| factor | rule | confidence | scored |
|---|---|---|---|
| season | ≤600 m: 15-04 → 10-05 … 15-12 → 25-01 (wraps the year); ≥1000 m: 01-06 → 01-07 … 15-10 → 15-11 | plausible | yes |
| habitat | chestnut 1.0, evergreen oak and beech 0.7, fir/spruce and mixed 0.6, deciduous oak and Mediterranean pine 0.5 | plausible (chestnut strong) | yes |
| altitude | full to 1000 m → 0 at 1700 m | plausible | yes |
| 30-day rain | 15 → 70 mm | plausible | yes |
| rain frequency | days with ≥5 mm in 20 days: 0 → 3 (floor 0.3, weight 0.5) | plausible | yes |
| rain trigger | 3-day rain 10 → 20 mm; lag 4 → 10 … 30 → 50 days | plausible | yes |
| soil temperature 0–7 cm, 7-day mean | 5 → 9 … 20 → 25 °C | folklore | yes |
| 60-day water balance | −150 → −30 mm: ×0.5 → ×1 | plausible | yes |
| 14-day drought | water balance −70 → −40 mm: floor 0.2 | plausible | yes |
| heat | 7-day mean Tmax 29 → 33 °C: floor 0.3 | folklore | yes |
| frost / hard frost / snow | Tmin ≤−2 °C on 2 of 7 nights ×0.3; Tmin ≤−5 °C → 0; ≥5 cm snow in 10 days → 0 | folklore | yes |
| drying | porcini rule at half effect (floor 0.8) | folklore | yes |
| two-flush season · air temperature · soil-moisture percentile · VPD heat | alternatives | — | no |
| soil pH 3.5 → 4.0 … 6.0 → 7.8 (floor 0.3) · lithology (calcareous share, floor 0.4) | `data: missing` | plausible | no |
| gaps | north/east aspect in summer below 600 m, growing degree-days since 1 January, acidophilous forest sub-types, nitrogen/stand age/litter/texture | — | — |

## Season cross-check against sightings

**Question:** do the season windows match when the species are actually recorded?

**Method.** All queries were run on 2026-09-17, and only aggregates are reported, never coordinates.

- **GBIF occurrence API** with `gadmGid=ITA.16_1` (Toscana) and a `month` facet. `MATERIAL_SAMPLE` rows
  are excluded.
- **iNaturalist**: the observation histogram for `place_id=13073` (Toscana), verifiable, all quality
  grades.
- **iNaturalist records for central Italy**: Tuscany plus Liguria, Emilia-Romagna, Umbria, Marche and
  Lazio, excluding obscured or private records and positional accuracy >1 km.
- **Observer effort.** Month counts mostly reflect when people go out and post fungi. So each species'
  monthly share is divided by the monthly share of **all fungi** recorded in central Italy on
  iNaturalist (55,353 observations, peaking in October). This ratio is the **enrichment**: >1 means the
  species is over-represented that month relative to effort.
- **Caveats.** The data are presence-only and small, and the records sit near towns and trails. All
  years were used, and the season and altitude numbers came partly from these same records, so treat
  them as **priors**. Refit them on train seasons only, or leave them untuned (see Hand-offs → M3).

**Tuscan record counts by month** (GBIF with soil samples excluded / iNaturalist verifiable):

| taxon | source | n | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | GBIF | 15 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 3 | 8 | 2 | 0 |
| | iNat | 31 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 | 7 | 15 | 5 | 0 |
| *B. reticulatus* | GBIF | 11 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 2 | 2 | 2 | 0 | 0 |
| | iNat | 24 | 0 | 0 | 0 | 0 | 1 | 6 | 4 | 2 | 7 | 3 | 1 | 0 |
| *B. aereus* | GBIF | 42 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 8 | 26 | 4 | 0 |
| | iNat | 61 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 5 | 16 | 32 | 6 | 0 |
| *B. pinophilus* | GBIF | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |
| | iNat | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 4 | 1 | 0 |
| *A. caesarea* | GBIF | 38 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 2 | 11 | 20 | 3 | 0 |
| | iNat | 50 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 2 | 17 | 26 | 2 | 0 |
| *Cantharellus* (genus) | GBIF | 48 | 1 | 1 | 0 | 0 | 3 | 5 | 0 | 1 | 1 | 20 | 13 | 3 |
| | iNat | 116 | 3 | 1 | 0 | 0 | 13 | 10 | 4 | 1 | 6 | 49 | 22 | 7 |

**Season gate at mid-month against enrichment** (central Italy iNaturalist; the gate is evaluated at a
typical elevation for the taxon):

| key @ elevation | row | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| porcini_edulis @ 1000 m | gate | 0 | 0 | 0 | 0 | 0 | 0 | .23 | .73 | 1 | 1 | 1 | .14 |
| | enrichment (n=57) | 0 | 0 | 0 | .2 | 0 | .7 | .9 | 1.8 | 3.1 | 1.7 | .5 | 0 |
| porcini_reticulatus @ 700 m | gate | 0 | 0 | 0 | 0 | .45 | 1 | 1 | 1 | 1 | .67 | 0 | 0 |
| | enrichment (n=56) | .4 | 0 | 0 | 0 | .9 | 4.2 | 2.7 | 1.8 | 2.6 | .8 | .1 | 0 |
| porcini_aereus @ 350 m | gate | 0 | 0 | 0 | 0 | 0 | 0 | .23 | .73 | 1 | 1 | 1 | 0 |
| porcini_aereus @ 750 m | gate | 0 | 0 | 0 | 0 | 0 | 0 | .64 | 1 | 1 | .52 | 0 | 0 |
| | enrichment (n=77) | 0 | 0 | .3 | 0 | .2 | .3 | 0 | 1.1 | 3.0 | 2.1 | .6 | 0 |
| ovoli_caesarea @ 350 m | gate | 0 | 0 | 0 | 0 | 0 | .15 | .48 | .82 | 1 | 1 | .60 | 0 |
| | enrichment (n=88) | 0 | 0 | 0 | 0 | .1 | .2 | .3 | .9 | 3.4 | 2.2 | .2 | 0 |
| gallinacci_cibarius @ 300 m | gate | .24 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gallinacci_cibarius @ 1100 m | gate | 0 | 0 | 0 | 0 | 0 | .47 | 1 | 1 | 1 | 1 | 0 | 0 |
| | enrichment, *C. cibarius* label (n=84) | .8 | .3 | 0 | .1 | .3 | 1.4 | .9 | .5 | 1.1 | 2.2 | .9 | .6 |

*B. pinophilus* (7 central-Italy records) is too sparse to check.

**What the cross-check changed:**

- ***B. reticulatus***: records stay at 0.8× in October (9 records), so the window's tail was extended
  from 31 October to 15 November.
- ***B. aereus***: 0 of 77 central-Italy records fall in July, against about 3 expected from effort.
  By elevation the peak is September at 600–900 m, October at 300–600 m and September–November below
  300 m. The window was
  split by elevation (a 400–600 m handover), and the upland window reaches full only on 1 August.
- **Ovoli**: the corrected window (peak September–October, a partial summer) matches the records. The
  August gate (0.82) is above the 0.9× enrichment on purpose, so that summer storm flushes can score
  when the moisture rules allow.
- **Gallinacci**: the lowland window deliberately stays open through summer. The July–August trough
  (0.5×–0.9×) is left to the heat, drought and moisture rules, because rainy summers do fruit.
- **Loose tails to watch**: *B. edulis* scores fully to mid-November (0.5× in November) and 0.14 in
  mid-December with no December records; ovoli score 0.6 in mid-November against 0.2×. Both are left
  for the backtest.

**Elevations of Tuscan iNaturalist records** (Copernicus DEM via the Open-Meteo elevation API)
against the altitude bands:

| taxon | n | p10 | median | p90 | max | band (zero → full … full → zero) |
|---|---|---|---|---|---|---|
| *B. edulis* | 27 | 478 | 1024 | 1386 | 1673 | 200 → 700 … 1600 → 1900 |
| *B. reticulatus* | 21 | 64 | 649 | 951 | 1402 | 0 → 150 … 1100 → 1500 |
| *B. aereus* | 50 | 41 | 352 | 629 | 789 | … 800 → 1250 |
| *B. pinophilus* | 6 | 519 | 692 | 1276 | 1296 | 300 → 800 … 1600 → 1900 |
| *A. caesarea* | 42 | 126 | 343 | 765 | 1182 | … 750 → 1100 |
| *C. cibarius* label | 41 | 79 | 302 | 854 | 1316 | … 1000 → 1700 |

All bands contain the bulk of the records. Low medians partly reflect observers near towns and the
coast.

## Weather variables: every rule mapped to Open-Meteo

**Verification.** Every variable below was requested on 2026-09-17 from the history API
(`archive-api.open-meteo.com/v1/archive`) and the forecast API (`api.open-meteo.com/v1/forecast`) with
`timezone=Europe/Rome`, for a Casentino point. A variable counts as available only if it returned
non-null values in both.

| rule input | Open-Meteo daily variable | unit | history | forecast | used by |
|---|---|---|---|---|---|
| rain amount, 30-day rain, rain frequency, drought | `precipitation_sum` | mm | ✓ | ✓ | all |
| snow | `snowfall_sum` | cm | ✓ | ✓ | porcini, gallinacci |
| air temperature band | `temperature_2m_mean` | °C | ✓ | ✓ | porcini (ovoli/gallinacci alternative) |
| frost, cold nights | `temperature_2m_min` | °C | ✓ | ✓ | all |
| heat, heat spike | `temperature_2m_max` | °C | ✓ | ✓ | porcini (anomaly), gallinacci |
| soil temperature band | `soil_temperature_0_to_7cm_mean` (also `7_to_28cm`) | °C | ✓ | ✓ | ovoli, gallinacci (porcini alternative) |
| soil moisture | `soil_moisture_0_to_7cm_mean`, `soil_moisture_7_to_28cm_mean` | m³/m³ | ✓ | ✓ | disabled everywhere in v1 (see flags) |
| drying, evaporative demand, water balance | `et0_fao_evapotranspiration` | mm | ✓ | ✓ | all |
| dry air | `vapour_pressure_deficit_max` (daily max only) | kPa | ✓ | ✓ | gallinacci alternative |
| drying wind (gaps only) | `wind_gusts_10m_max`, `wind_speed_10m_max`, `wind_direction_10m_dominant`, `relative_humidity_2m_min` | km/h, °, % | ✓ | ✓ | known gaps (compound wind + humidity rules) |

**Derived series** (computed by the engine from the above): `water_balance = precipitation_sum −
et0_fao_evapotranspiration`; `temperature_2m_max_anomaly_30d`; and climatology comparisons
(`percent_of_normal`, `percentile_of_normal`) that need the history backfill.

**Flags for the weather ingest (M2) and the engine (M3):**

1. **Model mixing in history.** The archive default (`best_match`) stitches ECMWF IFS 9 km (from
   2017), ERA5 and ERA5-Land, which breaks the homogeneity a multi-season backtest needs. Pin
   `models` explicitly.
   - `era5_seamless` returned every variable above for 2016.
   - `era5_land` alone returns **null** precipitation, ET0 and wind.
   - `ecmwf_ifs` has no data before 2017.
2. **Soil layers differ between forecast models.** ICON reports 0/6/18 cm, while ECMWF IFS and ERA5
   report 0–7/7–28 cm. Request the daily `soil_*_0_to_7cm_mean` names: they returned data in both APIs
   (from ECMWF IFS in the forecast). Keep the history and forecast layers identical.
3. **Model soil moisture is not field soil moisture.** Absolute m³/m³ thresholds from field studies do
   not transfer, and model values depend on the model's soil texture. v1 therefore keeps soil-moisture
   rules disabled, or expresses them as **percentiles against the cell's own climatology** once the
   backfill exists.
4. **Downscale soil temperature as well as air temperature.** Temperature bands are evaluated per
   1 km cell, so apply the elevation lapse-rate correction to `soil_temperature_*` too, not only to
   `temperature_2m_*`.
5. **VPD** is only available as a daily maximum. **Snowfall** is in cm (water-equivalent precipitation
   is already in `precipitation_sum`).

**Rules that need data or engine features v1 does not have** (all recorded as `enabled: false`
factors or `known_gaps`):

| need | rules | candidate |
|---|---|---|
| soil pH | gallinacci pH 4.0–5.5 (GAL-20); ovoli siliceous/slightly acid (OVO-17); porcini soil notes | SoilGrids 2.0 pH at 250 m (soft prior), Regione Toscana pedological DB (pH not confirmed) |
| lithology (calcareous share) | gallinacci (GAL-21), ovoli substrate | Regione Toscana 1:10,000 geological DB, reclassified once |
| forest sub-types by substrate | gallinacci acidophilous chestnut and oak types | Regione Toscana forest types, if M2 uses them |
| stand age, basal area, thinning, litter | *B. edulis* (30- vs 60-year fir, medium thinning best, litter removal harmful), gallinacci stand age | none in v1 |
| canopy openness, clearings, management | ovoli (open, cleared chestnut), gallinacci | Copernicus tree-cover density (later) |
| wood-edge buffer (open land within 100 m of woods) | porcini (IGP rule) | M2 grid geometry |
| climatology (percentiles, % of normal) | soil-moisture percentiles, 60-day % of normal rain, spring rain | M2 history backfill |
| engine features | aspect conditional on elevation/season; temperature-drop bonus; temperature-dependent lag; compound wind + humidity condition; calendar-anchored windows; growing degree-days since 1 January | schema v2 if the backtest shows value |

## Habitat vocabulary proposal for the grid

The rules score habitat through a small vocabulary. M2 owns the final list; this is what the rules
assume. The host-specific rules need **forest types by dominant tree**. Copernicus HRL Forest Type
only separates broadleaf from coniferous, which is **not enough**. The ISPRA 4th-level Corine Land
Cover (2018) maps cleanly (legend verified from the ISPRA map service); the Regione Toscana forest map
is the more detailed alternative.

| key | ISPRA CLC IV level | Tuscan examples |
|---|---|---|
| `evergreen_oak` | 3111 Boschi a prevalenza di querce e altre latifoglie sempreverdi | leccete, sugherete |
| `deciduous_oak` | 3112 Boschi a prevalenza di querce caducifoglie | cerrete, querceti di roverella |
| `mixed_broadleaf` | 3113 Boschi misti a prevalenza di altre latifoglie autoctone | ostrieti, carpineti, acero-frassineti |
| `chestnut` | 3114 Boschi a prevalenza di castagno | castagneti (coppice and fruit orchards) |
| `beech` | 3115 Boschi a prevalenza di faggio | faggete |
| `riparian` | 3116 Boschi a prevalenza di specie igrofile | pioppeti, saliceti, ontanete |
| `exotic_broadleaf` | 3117 Boschi ed ex-piantagioni a prevalenza di latifoglie esotiche | robinieti, eucalitteti |
| `mediterranean_pine` | 3121 Boschi a prevalenza di pini mediterranei e cipressi | pinete di pino marittimo e domestico |
| `mountain_pine` | 3122 Boschi a prevalenza di pini oro-mediterranei e montani | pinete di pino nero, pino silvestre |
| `fir_spruce` | 3123 Boschi a prevalenza di abeti | abetine (Vallombrosa, Camaldoli, Abetone) |
| `other_conifer` | 3124 larice e/o pino cembro; 3125 conifere esotiche | douglasiete |
| `mixed_broadleaf_conifer` | 3131 / 3132 Boschi misti a prevalenza di latifoglie / conifere | faggio + abete |
| `macchia` | 3231 Macchia alta; 3232 Macchia bassa e garighe | macchia mediterranea |
| `transitional_woodland_shrub` | 324 (3241) Aree a vegetazione boschiva e arbustiva in evoluzione | abandoned chestnut and oak regrowth |

Notes for M2:

- The mixed classes lose host identity, so prefer dominant type plus fractions.
- `macchia` and `transitional_woodland_shrub` may fall outside the "mostly woodland" mask but matter
  for *B. aereus* and ovoli. Either keep them as fractions in woodland cells, or apply the porcini
  100 m wood-edge rule.
- If the Regione Toscana forest types are used, keep the **acidophilous sub-types** (castagneto
  acidofilo, cerreta acidofila, pineta acidofila di pino nero). They are a free soil-pH proxy for
  gallinacci.
- The ovoli appendix suggests splitting chestnut **orchards** (open, 1.0) from **coppice** (0.7) if the
  source separates them.

## Rule config and scoring

The draft config is in [`species-rules/`](species-rules/README.md): six species keys
(`porcini_edulis`, `porcini_reticulatus`, `porcini_aereus`, `porcini_pinophilus`, `ovoli_caesarea`,
`gallinacci_cibarius`), `references.yaml` and JSON Schemas. The schema's shape:

- **Score** = Π gates (season, habitat, altitude) × Π stoppers × the weighted geometric mean of the
  drivers. Any driver at 0 zeroes the score (no rain, no fruiting), while partial values trade off.
- **Seven factor kinds** built on trapezoid responses: `season_window`, `habitat`, `static_band`,
  `rain_event`, `window_aggregate`, `count_days` and `days_since`.
- **Every factor** carries `source` (non-empty, resolving to `references.yaml`), `confidence`,
  `derived`, `data` (available / derived / missing) and `enabled`. Rules on missing data must be
  disabled; derived numbers must explain themselves in `notes`.
- **Breakdown.** Each factor's value and raw input, plus a proposed **impact**: its share of the
  score's log-shortfall. Impacts sum to 1, and a factor at 0 takes all the impact ("blocked by
  frost").
- **Verification.** The draft passes `validate.py`. That lint was itself checked against 16
  deliberately broken copies (empty source, unknown source id, unordered trapezoid, driver without a
  weight, unknown habitat key or variable, enabled rule on missing data, derived rule without notes,
  bad date, and more); it caught all 16, and the untouched control passed.

## Combined score: proposal for M3 to decide

**Proposal:**

1. **Group score.**
   - `porcini` = **max** over its four taxon keys. The breakdown comes from the winning key, so the UI
     can also say which porcino.
   - `ovoli` and `gallinacci` each have a single key.
   - Max, not sum, because the four porcini share the same rain logic; a sum would count it four
     times.
2. **Combined score** = **max over the three groups that are in season** (season gate > 0 for that
   cell and day), exposed as its own species key (`combined`) carrying `source_group`. The breakdown
   is the winning group's. No group in season gives a combined score of 0 with the reason
   "out of season".
3. **Tie-break** in a fixed order (porcini, ovoli, gallinacci) so results are deterministic.

**Why max.** It keeps the 0–1 index meaning: "the best conditions of the three, here, today". It
is explainable in one line ("combined 0.71 = ovoli"), and it never inflates.

**Alternatives rejected:**

- **Probabilistic OR** (`1 − Π(1 − s)`) treats scores as independent probabilities, which the PRD
  forbids. It also inflates cells where all three are mediocre.
- **Mean** dilutes a strong single-species signal and penalises cells outside one group's altitude
  band.
- **Capped sum** has the problems of both.

**Caveat to check in the backtest.** A max across groups assumes their scores are on comparable
scales. The groups use different drivers: porcini have a sharp event lag, gallinacci a long plateau
that stays high for weeks. If one group dominates the combined map, calibrate before taking the max,
for example by mapping each group's score to its percentile within that group's in-season
distribution, or by scaling by backtest lift. Report which group wins how often per season.

## Hand-offs to other cards

**M2 · Woodland grid**
- Use the habitat vocabulary above: CLC IV level or the Regione Toscana forest types, not HRL Forest
  Type.
- Keep macchia and transitional scrub as fractions, and keep the acidophilous forest sub-types.
- Consider the 100 m wood-edge buffer (porcini IGP rule).
- A lithology layer (calcareous share per cell) is the cheapest soil-pH proxy for later.

**M2 · Weather ingest**
- Pin history models (`era5_seamless` returned every rule variable).
- Use the 0–7 and 7–28 cm daily soil names in both APIs, and downscale soil temperature by elevation.
- Fetch `snowfall_sum`, `et0_fao_evapotranspiration`, `vapour_pressure_deficit_max`,
  `wind_gusts_10m_max`, `relative_humidity_2m_min` and `wind_direction_10m_dominant` as well as the
  basics.
- The backfill must support per-cell climatologies (percentiles, % of normal).

**M2 · Sightings ingest**

| group | GBIF taxon keys | iNaturalist taxa | traps |
|---|---|---|---|
| porcini | *B. edulis* 5954958; *B. reticulatus* 5954691 (includes *B. aestivalis* 5954988); *B. aereus* 8733688; *B. pinophilus* 5954949 | 48701; 350216; 333772; 335942 | drop `MATERIAL_SAMPLE` (the soil-DNA "Global soil organisms" dataset); map verbatim "*Boletus pinicola*" to 5954949 by hand; the four are often confused, so validate as a group |
| ovoli | *A. caesarea* 5240269 | 204588 | about 785 US/MX records belong to other species: never use the global set; dedupe observer-day-cell |
| gallinacci | *Cantharellus* genus 9623860, excluding *C. cinereus* 9226626 and *C. melanoxeros* 5249532 | genus 47348 | the name *C. cibarius* is misapplied to Mediterranean segregates; 111 of 116 records are from 2019–2025 |

**M3 · Model v1**
- Start from `species-rules/` (schema, config, scoring semantics and breakdown impact above).
- **Circularity.** Season windows and altitude bands used sightings from all years. Either freeze
  them as priors (do not tune them), or re-derive them on the train seasons before the hold-out.
- **Compare these alternative pairs**: rain vs water balance, air vs soil temperature, lag
  `[6, 10, 20, 28]` vs `[10, 15, 24, 32]` for ovoli, and the one- vs two-flush gallinacci season.
- **Test the folklore stoppers** (drying via ET0, frost thresholds) and drop them if they add no lift.
- **Validate porcini as a group**; for per-group shape tests, consider central-Italy records while
  keeping Tuscany for the hold-out.
- Decide the combined score (proposal above).

## Open questions

- Is the ovoli autumn peak driven by the return of rain or by cooling? The lore says warmth; the
  backtest can test a cooling term.
- Does *C. cibarius* s.str. occur in the Tuscan Apennine beech and fir belt at all? No sequenced
  Tuscan specimen was found. The answer matters only for a v2 split into Mediterranean and temperate
  gallinacci.
- Is the German *B. edulis* temperature optimum (13 °C) right for Tuscan populations? Amiata fruited
  in an 18.6 °C summer. Tune T1 first.
- Leads that were paywalled or blocked and could sharpen species-level parameters:
  - Laganà et al. 2002 (periodicity in Tuscan fir forests, likely monthly *Cantharellus* data);
  - Baptista et al. 2010 (chestnut macrofungi phenology, NE Portugal);
  - Gelardi 2020 (porcini host checklist);
  - the full text of Salerni et al. 2002.
