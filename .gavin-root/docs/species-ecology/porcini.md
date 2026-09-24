# Porcini: *Boletus edulis*, *B. pinophilus*, *B. reticulatus* (= *B. aestivalis*), *B. aereus* (evidence appendix to species-ecology.md)

Research date: 2026-09-17. Research only, no code. Numbers marked **derived** are my conversions of
qualitative or out-of-region evidence into encodable parameters. They are starting points for the
backtest, not findings.

## Scope and taxonomy notes

- **What "porcino" covers.** In Tuscan and northern Apennine usage "porcini" means four species of
  *Boletus* sect. *Boletus*: *B. edulis*, *B. aereus*, *B. reticulatus* (= *B. aestivalis*) and
  *B. pinophilus* (= *B. pinicola*) [R1][R24]. The *Fungo di Borgotaro* IGP, whose area includes
  Pontremoli and Zeri (Lunigiana, Tuscany), covers exactly these four [R1][R2].
- **Molecular status.** Four well-supported European lineages: *B. edulis* s.l., *B. aereus*,
  *B. reticulatus* and *B. pinophilus*. *B. betulicola*, *B. persoonii*, *B. quercicola* and
  *B. venturii* fall inside *B. edulis* [R23]. Hall et al. still treated *B. edulis* s.l. as a complex
  of "at least five species (or sub-species)" [R22]. That older, lumped usage is common in the
  productivity literature.
- **Lumped data.** Almost all the quantitative weather–fruiting studies below are on *B. edulis* s.s.
  (Amiata [R3], Bielefeld [R6], Soria [R8][R11][R12]) or on whole fungal communities [R5][R7][R9][R16].
  **No quantitative weather study was found for *B. aereus*, *B. reticulatus* or *B. pinophilus*.**
  Their rules borrow the *B. edulis* rain logic, with season, habitat, altitude and temperature
  shifted using qualitative sources. Salerni & Perini's 2004 dataset is titled "*B. edulis* s.l.", but
  the 2023 re-analysis says the fruit bodies were *B. edulis* s.s. It left out six *B. pinophilus*
  finds [R3][R4].
- **Names in GBIF (backbone lookup, 2026-09-17) [R34].** *B. aestivalis* is a synonym of accepted
  *B. reticulatus* (key 5954691). *B. quercicola* and *B. betulicola* are synonyms of *B. edulis*
  (5954958). The name "*Boletus pinicola*" **does not match** a species: it is an illegitimate later
  homonym [R25], so records under that verbatim name fall to a higher rank. The ingest should map it
  to *B. pinophilus* (5954949) by hand. *B. aereus* is 8733688.
- **Vernacular trap.** "Moro" means *B. pinophilus* in the Borgotaro IGP [R1] but *B. aereus* in
  Lucca province usage ("moro, moreccio, bronzino, porcino nero") [R24]. Forum or folklore reports
  that give only a common name cannot be assigned to a taxon.
- **Identification noise.** *B. aereus* "has often been confused" with *B. aestivalis* [R25], and
  the four taxa are hard to separate in the field [R24]. Species-level sightings will be noisy.
- **Sightings are very sparse in Tuscany (GBIF, gadmGid ITA.16_1, 2026-09-17) [R34].** With
  coordinates: *B. aereus* 43 (42 iNaturalist), *B. reticulatus* 39, *B. edulis* 15, *B. pinophilus* 3.
  **28 of the 39 *B. reticulatus* records are `MATERIAL_SAMPLE` rows from the 2019 "Global soil
  organisms" dataset**: soil-sample (DNA) records, not fruit bodies. The backtest must filter
  `basisOfRecord` to `HUMAN_OBSERVATION` / `PRESERVED_SPECIMEN`. That leaves about 70 fruit-body
  records across all four taxa, so per-taxon validation is close to impossible. Validate the
  aggregate "porcini" score.

## Rules summary

Taxon codes: `edu` = *B. edulis*, `pin` = *B. pinophilus*, `ret` = *B. reticulatus/aestivalis*,
`aer` = *B. aereus*, `all` = shared by the four. Trapezoids are `[zero_before/below, full_from, full_to,
zero_after/above]`. Temperatures are °C, rain mm, lags days, dates `DD-MM` (Europe/Rome local days).

| id | taxon | factor | rule (plain words) | parameters | confidence | sources | data |
|---|---|---|---|---|---|---|---|
| POR-S1 | ret | season | Late-spring-to-summer fruiter, fading in early autumn | `[01-05, 01-06, 20-09, 31-10]` (derived) | plausible | R1 R2 R24 R26 | available |
| POR-S2 | aer | season | Summer to late autumn. Upland chestnut/oak sites peak Jul–Sep; lowland macchia/oak sites peak in autumn | `[15-06, 15-07, 31-10, 30-11]` (derived) | plausible | R1 R2 R24 R26 R27 | available |
| POR-S3 | edu | season | Main crop late summer to first snow; summer fruiting rare and left to the temperature rule | `[01-07, 01-09, 15-11, 20-12]` (derived) | plausible | R1 R2 R3 R24 R26 R27 | available |
| POR-S4 | pin | season | Two flushes: late spring and autumn (the earliest and latest of the four). Score = max of the two windows | spring `[01-05, 20-05, 30-06, 20-07]`; autumn `[15-08, 15-09, 15-11, 15-12]` (derived) | plausible (spring flush: low) | R1 R2 R24 R25 R26 R42 | available |
| POR-S5 | all | season × altitude | Keep the date window broad and let temperature (lapse-rate-corrected) shift timing with altitude. Optional explicit shift: autumn window 1.5 d earlier per +100 m above 600 m | `shift_days = -0.015 × (elev_m − 600)`, autumn only (derived) | plausible (extrapolated from central/northern Europe) | R20 | derived |
| POR-H1 | edu | habitat | Affinity per habitat key | beech 1.0, chestnut 0.9, fir_spruce 0.9, mixed_broadleaf_conifer 0.8, mountain_pine 0.5, deciduous_oak 0.5, mixed_broadleaf 0.4, other_conifer 0.3, evergreen_oak 0.2, mediterranean_pine 0.2, macchia 0.1, riparian 0.1, exotic_broadleaf 0.05, transitional_woodland_shrub 0.3 (derived) | plausible | R1 R2 R3 R24 R26 R27 R23 | available |
| POR-H2 | pin | habitat | Affinity per habitat key | beech 0.9, fir_spruce 0.8, chestnut 0.8, mixed_broadleaf_conifer 0.8, mountain_pine 0.6, other_conifer 0.3, mediterranean_pine 0.3, deciduous_oak 0.3, mixed_broadleaf 0.3, evergreen_oak 0.1, macchia 0.05, riparian 0.05, exotic_broadleaf 0.05, transitional_woodland_shrub 0.2 (derived) | plausible | R1 R2 R24 R25 R26 R23 | available |
| POR-H3 | ret | habitat | Affinity per habitat key | chestnut 1.0, deciduous_oak 0.9, mixed_broadleaf_conifer 0.6, beech 0.5, mixed_broadleaf 0.5, evergreen_oak 0.4, fir_spruce 0.3, mountain_pine 0.3, macchia 0.2, mediterranean_pine 0.2, other_conifer 0.2, riparian 0.15, exotic_broadleaf 0.05, transitional_woodland_shrub 0.4 (derived) | plausible | R1 R2 R24 R26 R23 R31 | available |
| POR-H4 | aer | habitat | Affinity per habitat key | deciduous_oak 1.0, chestnut 0.9, evergreen_oak 0.8, macchia 0.7, mediterranean_pine 0.4, mixed_broadleaf 0.4, mixed_broadleaf_conifer 0.4, beech 0.2, other_conifer 0.1, mountain_pine 0.1, fir_spruce 0.05, riparian 0.05, exotic_broadleaf 0.05, transitional_woodland_shrub 0.5 (derived) | plausible | R1 R2 R24 R26 R27 R28 R23 R32 | available |
| POR-H5 | all | habitat (edge) | Open land (shrub, meadow, pasture) within 100 m of a qualifying wood counts as productive | buffer 100 m around woodland; affinity = neighbouring wood's × 0.5 (0.5 derived) | plausible | R1 R2 | derived |
| POR-A1 | edu | altitude | Mid to high mountain; uncommon in low thermophilous woods | `[200, 700, 1600, 1900]` m (derived) | plausible | R3 R24 R25 R29 R1 | available |
| POR-A2 | pin | altitude | Cool, humid mountain sites; the summer form also in mid-altitude chestnut | `[300, 800, 1600, 1900]` m (derived) | plausible | R1 R24 R25 R29 | available |
| POR-A3 | ret | altitude | Hills to lower mountain (chestnut/oak belt), thinning out in the beech belt | `[0, 150, 1100, 1500]` m (derived) | plausible | R24 R25 R29 R30 | available |
| POR-A4 | aer | altitude | Coast to mid-hill; sunny chestnut stands at mid-mountain are its upper limit | `[0, 0, 800, 1250]` m (derived) | plausible | R24 R25 R26 R30 | available |
| POR-A5 | edu, pin | aspect | Below 1000 m, north-facing slopes are moister and cooler and hold the conifer hosts, but flat, E- and W-facing ground is normal for Tuscan woodland; only clearly sunny (south-facing) slopes lose credit; no aspect effect above | multiplier below 1000 m: N, flat and E/W 1.0 (normal terrain, full credit), S (135–225°) ~0.85 (derived) | folklore | R29 R35 R14 | available |
| POR-A6 | aer, ret | aspect | Tolerates or prefers sunny exposures | multiplier: S 1.0, E/W 1.0, N 0.9 (derived) | folklore | R24 | available |
| POR-R1 | all | rain trigger (amount) | A trigger is a heavy rain event over 1–3 days | 3-day rain sum ramp: 0 at ≤10 mm, 1 at ≥40 mm; one day ≥20 mm alone gives ≥0.5 (derived) | plausible | R3 R36 R35 | available |
| POR-R2 | all | rain trigger (lag) | Fruiting responds about 10–14 days after a trigger event, with a tail to about 3 weeks | lag trapezoid `[6, 10, 16, 24]` days (shape derived; peak from R3 day-12 signal) | strong (edu, Amiata) / plausible (other taxa) | R3 R5 R36 R38 | available |
| POR-R3 | all | lag × temperature | Lag lengthens in cool weather | if 10-day mean Tair after trigger < 10 °C, shift lag trapezoid +3 d (derived) | folklore | R38 R36 | available |
| POR-M1 | all | cumulative rain | Rain over the previous ~30 days drives fruiting abundance | 30-day rain sum ramp: 0 at ≤20 mm, 1 at ≥80 mm (derived from R6: fruiting at 2–4 mm/day over 26 d) | strong (existence) / plausible (thresholds) | R5 R6 R7 R3 | available |
| POR-M2 | all | soil moisture | Same-month soil moisture limits yield | 7–28 cm volumetric soil moisture, percentile vs cell's calendar-month climatology: 0 at ≤10th, 1 at ≥40th (derived) | plausible (Mediterranean pine, lumped community) | R7 R11 | available |
| POR-M3 | all | water balance | Evaporative demand, not just rain, controls yield | 30-day (P − ET0) ramp: 0 at ≤ −80 mm, 1 at ≥ 0 mm (derived) | plausible | R9 R15 R13 R10 | available |
| POR-M4 | all | seasonal preconditioning | Wet late summer / early season primes the autumn crop | 60-day rain vs cell climatology: multiplier 0.6 at ≤50 %, 1.0 at ≥100 % (derived); autumn window only | plausible | R16 R17 R8 R11 R5 | available |
| POR-T1 | edu | air temperature | Fruiting peaks at moderate multi-day mean temperature and is largely absent in cold spells | 20-day mean Tair trapezoid `[6, 10, 17, 22]` °C (derived: R6 optimum 13 °C, bulk 10–15; upper edge widened for Tuscan summer fruiting in R3) | plausible (extrapolated, Germany) | R6 R3 | available |
| POR-T2 | pin | air temperature | Most cold-tolerant of the four | 20-day mean Tair `[4, 8, 15, 20]` °C (derived) | plausible (low) | R25 R24 R6 | available |
| POR-T3 | ret | air temperature | Warm-season taxon ("fungo del caldo") | 20-day mean Tair `[9, 13, 21, 25]` °C (derived) | plausible (low) | R1 R24 R6 | available |
| POR-T4 | aer | air temperature | The most xerothermophilous of the four | 20-day mean Tair `[10, 14, 22, 26]` °C (derived) | plausible (low) | R1 R23 R24 R6 | available |
| POR-T5 | all | soil temperature | Alternative to T1–T4: apply the same taxon band to the 10-day mean soil temperature (0–7 cm). Pick one of air or soil, not both | same trapezoids as T1–T4 (derived; no porcini soil-temperature threshold found) | folklore | R6 R35 | available |
| POR-T6 | all | temperature drop | A cooling after warm weather, inside the lag window, helps trigger fruiting | if 7-day mean Tmax falls ≥3 °C vs the previous 7 days, 3–15 d before the date: ×1.1, capped at 1 (derived) | folklore | R35 R7 | available |
| POR-X1 | all | heat spike | A sudden Tmax spike suppresses fruiting for up to ~3 weeks | any day in last 14 d with Tmax ≥ (mean Tmax of the prior 30 d + 8 °C) or Tmax ≥ 30 °C: × 0.5 (edu, pin), × 0.75 (ret, aer) (derived) | plausible | R3 R7 R21 | available |
| POR-X2 | all | drought gate | Near-total failure when the fruiting period is dry | 45-day rain < 15 mm → score 0 (derived) | plausible | R6 R9 R5 | available |
| POR-X3 | all | frost | Hard frosts end the flush | ≥2 nights with Tmin ≤ 0 °C in last 7 d: × 0.2 (edu, pin), × 0.1 (ret), × 0.4 (aer) (derived) | folklore | R1 R6 R37 | available |
| POR-X4 | all | snow | Season ends with the first lying snow | snowfall ≥ 1 cm in last 3 d → × 0 (derived) | folklore | R1 R2 R37 | available |
| POR-X5 | ret | cold nights | The summer porcino stops with the first cold | Tmin ≤ 5 °C on ≥3 of last 7 nights: × 0.5 (derived) | folklore | R37 | available |
| POR-X6 | all | drying wind | Wind after rain (tramontana, grecale, maestrale) dries the topsoil and wastes the trigger | in the 7 d after a trigger, ≥2 days with max gust ≥ 40 km/h and mean RH ≤ 55 % (or ET0 ≥ 4 mm/d): trigger × 0.6 (all numbers derived; none in sources) | folklore | R39 R36 | available |
| POR-X7 | all | VPD | No porcini VPD threshold found; use ET0 in M3/X6 instead | none | — | — | available |
| POR-N1 | all | stand/soil/management | Stand age, basal area/thinning, litter, soil pH and texture matter but cannot be modelled in v1 | flag only (see "Not modellable") | strong (effects exist) | R4 R3 R8 R14 R12 R23 R33 | missing |

## Evidence by factor

### Season windows

- **Borgotaro IGP specification (northern Apennines, includes Pontremoli and Zeri in Tuscany)**
  [R1][R2], by taxon:
  - *B. aestivalis*: "epoca di produzione maggio–settembre", mainly in chestnut.
  - *B. pinicola/pinophilus*: a summer form "presente da giugno" mainly in chestnut, and an autumn
    form preferring beech and silver fir.
  - *B. aereus*: "da luglio a settembre", the most xerothermophilous.
  - *B. edulis*: "da fine settembre alla prima neve. Rare le forme estive."
  - The consolidated 2014 text sets a harvest period of 1 April to 30 November [R2]. That is a legal
    frame, not an ecological window.
- **Lucca province mycological article** [R24]:
  - *B. aestivalis* fruits "dalla tarda primavera alla fine dell'estate".
  - *B. edulis* "dall'estate al tardo autunno", coping well with the first cold.
  - *B. pinophilus* "dalla tarda primavera fino a tutto l'autunno".
  - *B. aereus* fruits "tipicamente in autunno" in Mediterranean macchia, and also in very sunny
    mid-mountain chestnut stands.
- **Siena mycological group** [R27]: *B. edulis* August–November. *B. aereus* from early summer to
  late autumn, in broadleaf woods and in pines with an *Erica scoparia* understorey.
- **Borgotaro porcini museum** [R26]:
  - *B. aestivalis*: late spring in warm years, through autumn.
  - *B. pinophilus*: spring through autumn.
  - *B. aereus*: warm periods from mid-June through late summer, low elevations.
  - *B. edulis*: summer to first snow.
- **Triveneto census texts by M. Floriani** [R25]: *B. pinophilus* is the earliest and latest fruiting
  of the four, "probably" because it copes better with cool climates. Record extremes (NE Italy, not
  Tuscany): *B. aereus* 18 Jan to 7 Dec; *B. reticulatus* 13 Feb to 16 Dec, both near Trieste at low
  altitude; *B. pinophilus* 12 May to 28 Oct in Trentino.
- **Amiata field data (*B. edulis* s.s., *Abies alba* plantation, ~1050 m)** [R3]: observed "mostly
  August–November". Peak month was October in 2000 (338 fruit bodies) and 2001 (584). In 2002 the
  peak moved to August (574) after a hot June and a rainy summer. The season shifts by about two
  months with the weather, which is why POR-S3 is kept broad.
- **Phenology trends** [R18][R19][R15]: European autumn fruiting seasons widened between 1970 and 2007
  and now end later [R18]. Swiss mycorrhizal fruiting was about 10 days later after 1991 [R19]. Some
  species now fruit in spring as well as autumn [R15]. Tune window edges on recent seasons.
- **Altitude and timing** [R20]: across central to northern Europe, altitude shifted mean fruiting by up to 30 days, with
  spring fruiting delayed and autumn fruiting advanced at higher altitude. POR-S5's 1.5 d/100 m is
  **derived** by spreading ~30 d over ~2000 m. Temperature (lapse-rate corrected) should do most of
  this work, so S5 is optional to avoid double counting.
- **GBIF sanity check, not used to set parameters** (same records as validation) [R34]:
  - Italy, fruit bodies plus a few samples: *B. edulis* mostly Jul–Oct (Aug peak, pulled by Alpine
    records); *B. reticulatus* Jun–Sep; *B. aereus* Sep–Nov (Oct peak); *B. pinophilus* May–Nov.
  - Tuscany: *B. aereus* 26 of 43 records in October, which supports the autumn lowland peak in R24
    over the Jul–Sep IGP window.
- Confidence: **plausible**. The windows rest on an institutional specification plus regional society
  texts that broadly agree; exact dates are derived.

### Hosts and habitat affinity

- **IGP eligible stands** [R1][R2]:
  - Broadleaves: beech, chestnut, Turkey oak and other oaks, hornbeam, hazel, aspen.
  - Conifers: silver and Norway spruce, black and Scots pine, Douglas fir (2014 text adds other
    *Pinus*).
  - Shrub, meadow and pasture land inside or bordering woods, up to 100 m from the wood edge, also
    counts as productive "because of the root system of the trees" → POR-H5.
- **Per taxon (Italian sources)**:
  - *B. reticulatus*: chestnut and oak mainly, rarer under beech, hazel, pine and fir [R24]; mainly
    chestnut [R1]; broadleaves, especially chestnut and oak, also under fir [R26].
  - *B. aereus*: oak and chestnut [R1][R26]; macchia with *Cistus*, *Arbutus*, *Ruscus* [R24]; holm
    oak, chestnut, *Arbutus* and *Erica* in Sardinia [R28]; pines with an *Erica scoparia* understorey
    [R27].
  - *B. edulis*: chestnut, beech and Norway spruce preferred, but with many other conifers and
    broadleaves, "indifferentemente al substrato" [R24]; beech, fir and chestnut [R1]; Amiata *Abies
    alba* plantation [R3].
  - *B. pinophilus*: fir, chestnut, beech, birch and many pines [R24]; chestnut in summer, beech and
    silver fir in autumn [R1]; often *Pinus sylvestris* but also broadleaves [R25].
- **Disagreement on *B. pinophilus*.** The Dutch-sampled phylogeny paper calls it "almost exclusively
  with *Pinus*", on poor, acid, sandy soil [R23]. Italian sources put it mainly with beech, fir and
  chestnut [R1][R24][R25]. For Tuscany I follow the Italian sources and give pines only a moderate
  affinity.
- **Cistus scrub.** *B. edulis* and *B. aereus* fruit in *Cistus ladanifer* scrublands in NW Spain,
  with mean yields of 37.8 and 22.5 kg/ha [R32] (snippet-only); B. edulis–rockrose climatic niche
  [R33]. That supports a non-zero `macchia` affinity, highest for *B. aereus*.
- **Black pine.** A black pine (*P. nigra*) plantation survey on Amiata (autumn 2014 to spring 2015)
  listed edible species without porcini [R43] (snippet-only; weak negative). `mountain_pine` stays
  moderate for *B. edulis*/*B. pinophilus* because the IGP lists black and Scots pine.
- **Chestnut orchard age.** *B. reticulatus* soil mycelium was more frequent in 40-year-old than young
  chestnut orchards; *B. edulis* was even across ages [R31] (Galicia, mycelium not fruit bodies).
  Not encodable in v1.
- **Proposed vocabulary addition: `transitional_woodland_shrub`** (CLC 3.2.4, young regrowth and
  scrub on abandoned land). The IGP treats shrubland within 100 m of woods as productive [R1][R2], and
  much abandoned chestnut and oak land in Tuscany sits in this class. If the woodland mask drops it,
  apply H5 as a buffer instead.
- `exotic_broadleaf` (robinia) gets 0.05 because no source links porcini to *Robinia*. That value rests on the general
  knowledge that it is not an ectomycorrhizal host (not verified here).
- All affinity numbers are **derived** from host rankings. Confidence **plausible**.

### Altitude and aspect

- **Taxon statements.** *B. edulis* is common "dalla media all'alta montagna" and infrequent at low
  altitude in thermophilous woods such as coastal macchia [R24]. *B. aereus* favours warm, dry lowland
  macchia but also reaches very sunny mid-mountain chestnut stands [R24] ("at low elevations" [R26]).
  *B. pinophilus* favours cool, humid places [R24].
- **Recorded extremes, NE Italy census** [R25]:

  | taxon | min (m) | max (m) |
  |---|---|---|
  | *B. aereus* | 10 | 1250 (mixed fir) |
  | *B. edulis* | 10 | 2175 |
  | *B. reticulatus* | 10 | 1927 |
  | *B. pinophilus* | 200 | 1898 |

  Extremes, not optima, and Alpine/Karst rather than Apennine.
- **Tuscan host belts** used to place the bands [R29]:
  - Beech dominates from 900 to 1700 (1800) m; on Amiata, beech types cover 800–1500 m and
    1500–1738 m.
  - Silver fir stands "normally between 900 and 1300 m (1500 at Abetone)". They reach 800 m only on
    poorly sunlit slopes; below 1000 m a north-facing preference becomes "fondamentale".
  - Chestnut rarely grows above ~1000 m in Tuscany [R30] (snippet-only).
- **Amiata *B. edulis* site**: mean elevation 1050 m [R3].
- **Aspect.** Slope, elevation and aspect were significant predictors of mushroom yield in Pyrenean
  pine stands [R14], but the abstract gives no direction. The north-facing preference below 1000 m
  (POR-A5) is inferred from host distribution [R29] and forager lore: shaded, north-facing slopes keep
  moisture in hot spells [R35]. Confidence **folklore** for the aspect multipliers.
- All band numbers are **derived**. Confidence **plausible**.

### Rain trigger (amount, lag)

- **Amiata, *B. edulis* s.s., daily observations 2000–2002** [R3]:
  - Very intensive rain days (R20, ≥20 mm) correlated positively with fruit-body counts "in
    particular on the twelfth day following the event": r = 0.623, 0.605 and 0.593 in three treatments
    with litter present.
  - Further positive R20 correlations on day 2 (medium thinning), day 18 (0.634) and day 20 (0.477).
    Treatment attribution for days 18 and 20 is my reading of the Table 2 layout.
  - Under heavy thinning, heavy rain was negative on days 13 and 19.
  - The authors link this to Salerni et al. 2002, where the greatest number of species fruited 10
    days after rain.
  - Caveat: 21 lags × 3 variables × 6 treatments were tested on 3 years of data, so single-day
    significance is fragile. The robust reading is "the response peaks about 10–14 days after a
    ≥20 mm day".
- **Tuscan oak forests, whole macrofungal community (lumped)** [R5]: correlations tested with rain in
  the 5, 10, 15 and 30 days before sampling. The highly significant fruit-body correlations were with
  the 30-day window (see Antecedent moisture).
- **Bielefeld beech, *B. edulis*, 10 years of daily data** [R6]: the best precipitation window was 26
  days (26–32 d at single sites). The authors note that studies without temperature in the model found
  shorter lags of under two weeks. Read POR-R2 (event lag) and POR-M1 (26–30-day accumulation) as
  complementary.
- **Forager lore**:
  - 30–80 mm falling over half a day to 2 days; first growth "10–22 days" after rain, "15 days
    ideal" [R36].
  - 40–50 to 90–100 mm spread over about two weeks; repeated moderate rain beats one downpour [R35].
  - A personal model: minimum 8 days with 60 mm at 14 °C, up to 14 days; longer in beech above
    1000 m than in chestnut at 600–700 m [R38] → POR-R3.
  - PRD hypothesis: ~30 mm, 10–15 days.
- **Parameters.** R1's 10→40 mm ramp is **derived** from R3's ≥20 mm event definition and the 30–80 mm
  lore. R2's `[6, 10, 16, 24]` is **derived**: the core covers R3's day-12 peak and R5's 10-day
  community peak, and the tail reaches R3's day 18–20 correlations and the lore's 22 days.
  Confidence: **strong** for a ~10–14 d lag in *B. edulis* (two Tuscan peer-reviewed studies agree);
  **plausible** when transferred to the other three taxa.

### Antecedent moisture

- **30-day rain.** "Highly significant correlations were found between the number of carpophores and
  rainfall in the 30 days preceding sampling" (Tuscan oak forests) [R5]. The same study found abundant
  annual rain necessary for fruiting, and spring rain related to autumn species richness [R5].
- **Bielefeld** [R6]: fruiting concentrated at 2–4 mm/day mean precipitation over the window
  (≈52–104 mm per 26 d). Precipitation had a linear positive effect with no upper threshold.
  POR-M1's 20→80 mm ramp over 30 d is **derived** from this.
- **Maritime pine, NE Spain (community, lumped)** [R7]: "Mushroom yield was primarily dependent on
  weather and soil moisture conditions during the same month, with the exception of precipitation,
  whose effects exhibited a one-month delay." → POR-M2 (same-month soil moisture) and M1 (~1-month
  rain). No absolute soil-moisture thresholds were given in the abstract, so M2 uses cell-relative
  percentiles (**derived**).
- **Water balance.** In a 15-year Mediterranean pine dataset, rain-based and water-balance-based
  models fitted equally well but diverged under warming: water-balance models predicted declining
  yields from rising evaporative demand [R9]. Fungi responded in "early spring and late
  summer–autumn" [R9]. Martínez de Aragón et al. 2007 (pre-Pyrenees pines, community yield) is
  summarised in [R15] as positively correlated with mean annual precipitation, with precipitation
  minus Sep/Oct evapotranspiration, and with minimum August soil temperature [R13 via R15].
  → POR-M3, thresholds **derived**.
- **Preconditioning.** Late-summer and early-autumn precipitation was the main driver in Pyrenean
  *P. sylvestris* [R16] and central Spanish *P. pinaster* stands [R17] (snippet-only; that *B. edulis*
  is among R17's species comes from a search summary). For *B. edulis* in Soria, autumn (Sep–Nov) precipitation correlated with
  sporocarp production, while previous summer, spring and winter rain showed no effect [R8]. Also in
  Soria, "wet conditions early in the production season together with cooler summers and mild autumns
  enhance the *B. edulis* growth", with soil conditions at the start of the season relevant to the
  annual total [R11]. In a species-level study, climate control acted "well before the fruiting
  season", with the timing of the summer–autumn rainfall signal the most relevant factor [R10].
  → POR-M4 (**derived**).
- **Summer drought legacy.** No porcini-specific quantitative legacy rule was found. *B. reticulatus*
  mycelium peaked when a high water deficit two months earlier combined with high soil moisture
  [R31]. That hints that a dry summer followed by a wet autumn is not harmful for that taxon, but the
  data are mycelium in an Atlantic chestnut orchard. Recorded as a hypothesis, not a rule.
- Confidence: **strong** that ~30-day rain and same-season moisture drive yield (consistent
  Tuscan + Mediterranean + central European field data, mostly lumped); **plausible** for the exact
  thresholds.

### Temperature

- ***B. edulis*, Bielefeld** [R6]: optimum lag window for temperature is 20 days. Fruiting was
  concentrated at 20-day means of 10–15 °C and largely absent at 5–10 °C, although those were the most
  common conditions. The quadratic optimum is ≈13 °C (differing <0.6 °C among models). This is a
  bioRxiv preprint (not peer-reviewed) from a cooler climate.
- **Tuscan fit.** At Amiata, *B. edulis* peaked in August 2002 [R3], when summer mean temperature at
  the station was 18.6 °C (Table 1). So Tuscan populations fruit above the German optimum. T1's upper
  shoulder is widened to 17/22 °C (**derived**). Air temperature has to be lapse-rate corrected to the
  cell elevation.
- **Other taxa.** No quantitative temperature data was found for the other three. The bands in T2–T4
  are **derived** by shifting the *B. edulis* band using:
  - *B. aereus*: "la specie più xerotermofila" [R1], "thermophilic" [R23], warm dry habitats [R24];
  - *B. reticulatus*: "fungo del caldo" [R1], "tipicamente termofila e xerofila" [R24];
  - *B. pinophilus*: cool climates, earliest and latest [R25]; cool humid sites [R24].
  Confidence **plausible (low)**.
- **Season-dependent temperature effect.** "High temperatures limited mushroom yield at the beginning
  of the fruiting season, but tended to enhance it towards the end" [R7]. Temperature drove autumn
  ectomycorrhizal fruiting phenology in Europe [R20]. Mean temperature explained *B. edulis* yield in
  *P. sylvestris* models [R12]. No temperature effect on *B. edulis* fruiting was detected in Soria
  [R8] (a disagreement).
- **Soil temperature.** No porcini-specific soil-temperature band was found in a primary source.
  García-Bustamante et al. analysed soil temperature for *B. edulis*, but the abstract reports no
  threshold [R11]. Minimum August soil temperature is a positive term in the pre-Pyrenees community
  model [R13 via R15]. Popular claims (soil not below ~6 °C; ideal "13–22 °C") were seen only in search
  snippets of commercial sites. POR-T5 therefore reuses the air bands on multi-day soil temperature
  and is **folklore**.
- **"Thermal shock".** No peer-reviewed support was found for a temperature drop triggering porcini.
  Popular weather-site writing says falling temperatures and cooler nights can matter more than rain
  [R35] (seen via search summary). POR-T6 is **folklore**, a small bonus the backtest can drop.

### Stoppers

- **Heat spikes.** At Amiata, extreme maximum-temperature events correlated negatively with
  *B. edulis* fruit bodies on days 1, 4, 7, 14, 15 and 19 after the event in unthinned and
  medium-thinned plots. The authors describe the spikes as "about 8 °C" above the period mean [R3].
  Heavily thinned plots showed a positive correlation on day 20. All species in a 127-taxon European
  analysis were "sensitive to extremes in daily recorded temperatures" [R21].
  → POR-X1: the +8 °C spike comes from R3. The absolute 30 °C and the multipliers are **derived**.
  Confidence **plausible** (single Tuscan study, many tests).
- **Drought.** Bielefeld's near-absence of fruit bodies in 2016 (4 fruit bodies vs 354 in 2020) was
  attributed to "exceptionally dry conditions during the peak fruiting period" [R6]. Rising
  evaporative demand predicts yield decline [R9]. In dry ecosystems (<650 mm/yr), current-year rain
  is the driving factor [R15]. X2's 45-day <15 mm gate is **derived**. Confidence **plausible**.
- **Frost and snow.**
  - *B. edulis* fruits "alla prima neve" [R1].
  - Bielefeld monitoring ran until "the first heavy frost" [R6] (a methods choice, but it implies
    frost ends fruiting).
  - At Amiata, extreme minimum temperatures correlated negatively only in one treatment, on day 4
    [R3].
  - Lore: in northern Italy late finds continue into Nov–Dec if it does not snow, cold wind does not
    blow constantly and night frosts do not pull daytime maxima below about +8 °C. *B. reticulatus*
    stops with the first cold; *B. aereus* holds on in mild winters without constant frost [R37].
  Thresholds in X3–X5 are **derived**. Confidence **folklore** (plausible for "snow ends *B. edulis*").
- **Drying wind.** Only forager lore: strong wind, especially tramontana, dries the soil and is the
  forager's "enemy number one"; there must be no wind after rain; late-season finds need the absence
  of cold dry tramontana/levante/maestrale [R39] (snippet-only). No source gives wind speeds or
  durations. Every number in X6 is **derived** and needs the backtest.
- **VPD.** No porcini source found. Use ET0 (M3, X6).

### Not modellable in v1

- **Stand age and structure.** On Amiata, *B. edulis* was present in 30-year-old fir stands and
  "replaced by *Boletus badius*" in 60-year-old stands [R4]. Stand basal area was "a strong factor"
  in the *B. edulis* yield model [R12]; basal area of 15–20 m²/ha maximised community yield in
  Pyrenean pines [R14]. Data: missing (no stand age/basal area layer).
- **Thinning and canopy.** Medium thinning (≈20 % basal area removed) gave the highest *B. edulis*
  production. Heavy thinning (≈40 %) cut counts by about a third versus the control [R3][R4]. Clear
  and partial cutting sharply reduced *B. edulis* soil mycelium with no recovery after 3 years [R8].
  Data: missing.
- **Litter.** Litter removal reduced *B. edulis* fruiting [R3][R4]. The IGP bans litter removal
  [R1][R2]. Data: missing.
- **Soil chemistry and texture.**
  - *B. aereus*: "heavy loamy, often somewhat calcareous soil" in the Dutch sample; *B. reticulatus*:
    clay or sand-mixed loam; *B. pinophilus*: "poor, acid, sandy soil"; *B. edulis*: various soils
    [R23].
  - Italian sources call *B. edulis* indifferent to substrate [R24].
  - Spanish *Cistus* sites were strongly acid loams [R33] (snippet-only).
  - Soil properties and geochemistry correlated with the fungal community at porcini-productive sites
    more strongly than vegetation or climate [R44] (snippet-only).
  - Candidate v2 layer: SoilGrids pH.
- **Previous-year carry-over and host vigour.** Yield responds to conditions in preceding years;
  heavy crops are often followed by poor ones; fruit-body counts correlate with tree-ring width
  [R15]. A multi-year "resource" term is conceivable later but has no porcini-specific parameters.
- **Harvest pressure.** Intensive weekly collection over four seasons did not reduce *B. edulis* soil
  mycelium [R8]. No need to model it.

## Disagreements and open questions

1. ***B. aereus* season.** IGP says July–September [R1][R2]. Lucca and Siena sources and Tuscan
   iNaturalist records point to an autumn (Oct–Nov) lowland peak [R24][R27][R34]. POR-S2 spans both.
   It may be better split by altitude (upland Jul–Sep, lowland/macchia Sep–Nov) if the backtest has
   enough records, which it likely does not.
2. ***B. pinophilus* hosts.** Pines-only (Netherlands, [R23]) vs beech, fir and chestnut (Italy,
   [R1][R24][R25]). The Italian view is used.
3. **Temperature effect on *B. edulis*.** Clear quadratic optimum in Germany [R6]; negative effect of
   heat spikes at Amiata [R3]; season-dependent effect in Catalonia [R7]; no effect in Soria [R8].
   The German optimum (13 °C) may not transfer to Tuscan populations. Tune T1 first.
4. **Lag length.** A ~12 d event lag [R3] vs a 26-day accumulation window [R6] vs a 1-month monthly
   lag [R7]. These measure different things. Keep both an event-lag factor (R2) and an accumulation
   factor (M1) and let the backtest weight them.
5. **Rain amount.** Lore ranges from 30–80 mm in 2 days [R36] to 40–100 mm over two weeks [R35].
   Peer-reviewed support exists only for "≥20 mm days matter" [R3] and "more rain is linearly better,
   no upper limit found" [R6]. Very intense rain (100 mm in hours) is claimed to be useless [R36],
   untested.
6. **No quantitative weather data exists for three of the four taxa.** Every T2–T4 and X5 number is
   an educated shift. Given about 70 Tuscan fruit-body records in total [R34], the backtest cannot
   calibrate them per taxon.
7. **Aggregate score.** The PRD's default for the combined score is "max across species". Porcini
   itself is an aggregate of four taxa with overlapping windows; max over taxa is the natural choice.
   A sum would double count the shared rain logic.
8. **Prior art, not a source.** An unsourced public Italian porcini index (GitHub "porcinit") uses lag
   = 20 − 0.6 × soil T bounded 8–18 d, a soil-T plateau 11–18 °C, and an altitude band that moves
   down from 800–1750 m in Jun–Aug to 150–1000 m in November. It cites no references. It is useful
   only as a sanity benchmark.
9. **Preconditioning vs same-season rain.** Community studies and one *B. edulis* study favour
   late-summer or early-season wetness [R11][R16][R17]. For *B. edulis* in Soria, only autumn
   (Sep–Nov) rain mattered and previous-summer rain had no detectable effect [R8]. POR-M4 is
   therefore a weak multiplier (floor 0.6); drop it if the backtest shows no lift.
10. **Leads checked but not used for rules.**
   - Sitta & Floriani 2008 [R40]: trade history; the abstract has no ecological parameters.
   - Gelardi 2020 checklist chapter [R41]: paywalled, likely good for per-taxon hosts.
   - Taye et al. 2016 and Martínez de Aragón et al. 2007: full texts not read (only abstract or
     secondary summaries).
   - Karavani et al. 2018 full text is open in the Lleida repository but sits behind a bot check; only
     the abstract was read.
   Worth a second pass if a species-level Mediterranean parameter is needed.

## References

- [R1] Disciplinare di produzione "Fungo di Borgotaro" IGP (older consolidated text, Arts. 1–9;
  hosted by Regione Toscana). http://prodtrad.regione.toscana.it/dopigp_img/7_74.doc `verified`
  (full text). Supports: four taxa and names; per-taxon habitat and months; eligible host species;
  100 m wood-edge rule; litter protection.
- [R2] Consorzio per la tutela dell'IGP Fungo di Borgotaro, Disciplinare (version 01/09/2014).
  https://www.fungodiborgotaro.com/ita/16/disciplinare/ `verified`. Supports: same per-taxon habitat
  and months as R1; harvest 1 Apr–30 Nov; extended conifer list.
- [R3] Salerni E., Paoli L., Perini C. (2023) Combined impact of forest management and climate change
  on *Boletus edulis* productivity: may mycosilviculture mitigate the effects of climate extremes?
  *Italian Journal of Mycology* 52: 76–88. https://doi.org/10.6092/issn.2531-7342/16464 `verified`
  (full PDF). Supports: Amiata *B. edulis* s.s. site data, monthly peaks, R20 day-12 lag signal,
  heat-spike suppression, thinning and litter effects, *B. pinophilus* sporadic in fir plantation.
- [R4] Salerni E., Perini C. (2004) Experimental study for increasing productivity of *Boletus edulis*
  s.l. in Italy. *Forest Ecology and Management* 201: 161–170.
  https://doi.org/10.1016/j.foreco.2004.06.027 `verified` (abstract, via Europe PMC). Supports: stand
  age (30 vs 60 yr), *B. badius* replacement, medium thinning positive, litter removal negative.
- [R5] Salerni E., Laganà A., Perini C., Loppi S., De Dominicis V. (2002) Effects of temperature and
  rainfall on fruiting of macrofungi in oak forests of the Mediterranean area. *Israel Journal of Plant
  Sciences* 50: 189–198. https://doi.org/10.1560/GV8J-VPKL-UV98-WVU1 `verified` (abstract). Supports:
  Tuscan oak forests (whole community, lumped): 30-day rain correlation, annual and spring rain.
  The 10-day species peak is cited from R3's discussion.
- [R6] Brejon Lamartinière E., Hoffman J.I. (2025, version posted 8 June 2026) Predicting porcini: a
  decade of sporocarp monitoring reveals the meteorological triggers of *Boletus edulis* fruiting in
  central European beech forests. bioRxiv preprint, not peer-reviewed.
  https://doi.org/10.64898/2025.12.12.693895 `verified` (full PDF). Supports: 20-day temperature
  window, optimum ≈13 °C, fruiting at 10–15 °C, 26-day precipitation window at 2–4 mm/day, drought
  year failure, frost end.
- [R7] Karavani A., De Cáceres M., Martínez de Aragón J., Bonet J.A., de-Miguel S. (2018) Effect of
  climatic and soil moisture conditions on mushroom productivity and related ecosystem services in
  Mediterranean pine stands facing climate change. *Agricultural and Forest Meteorology* 248: 432–440.
  https://doi.org/10.1016/j.agrformet.2017.10.024 `verified` (abstract, via Europe PMC). Supports:
  same-month soil moisture, 1-month precipitation delay, temperature effect by season stage (lumped
  community).
- [R8] Parladé J., Martínez-Peña F., Pera J. (2017) Effects of forest management and climatic
  variables on the mycelium dynamics and sporocarp production of the ectomycorrhizal fungus *Boletus
  edulis*. *Forest Ecology and Management* 390: 73–79. https://doi.org/10.1016/j.foreco.2017.01.025
  `verified` (abstract, via Europe PMC). Supports: autumn precipitation positive, no temperature
  effect, cutting reduces mycelium, harvesting no effect (*P. sylvestris*, Soria).
- [R9] Ágreda T., Águeda B., Olano J.M., Vicente-Serrano S.M., Fernández-Toirán M. (2015) Increased
  evapotranspiration demand in a Mediterranean climate might cause a decline in fungal yields under
  global warming. *Global Change Biology* 21: 3499–3510. https://doi.org/10.1111/gcb.12960 `verified`
  (abstract, via OpenAlex). Supports: water balance vs rain models, bimodal spring and
  late-summer–autumn response (guild level).
- [R10] Ágreda T., Águeda B., Fernández-Toirán M., Vicente-Serrano S.M., Olano J.M. (2016) Long-term
  monitoring reveals a highly structured interspecific variability in climatic control of sporocarp
  production. *Agricultural and Forest Meteorology* 223: 39–47.
  https://doi.org/10.1016/j.agrformet.2016.03.015 `verified` (abstract, via Europe PMC). Supports:
  climate control well before the season; timing of the summer–autumn rain signal (species named in
  the abstract: none).
- [R11] García-Bustamante E., González-Rouco J.F., García-Lozano E., Martínez-Peña F., Navarro J.
  (2021) Impact of local and regional climate variability on fungi production from *Pinus sylvestris*
  forests in Soria, Spain. *International Journal of Climatology* 41: 5625–5643.
  https://doi.org/10.1002/joc.7144 `verified` (abstract, via OpenAlex). Supports: *B. edulis* favoured
  by wet early season, cooler summers and mild autumns; start-of-season soil conditions.
- [R12] Martínez-Peña F., de-Miguel S., Pukkala T., Bonet J.A., Ortega-Martínez P., Aldea J.,
  Martínez de Aragón J. (2012) Yield models for ectomycorrhizal mushrooms in *Pinus sylvestris* forests
  with special focus on *Boletus edulis* and *Lactarius* group *deliciosus*. *Forest Ecology and
  Management* 282: 63–69. https://doi.org/10.1016/j.foreco.2012.06.034 `verified` (abstract, via
  Europe PMC). Supports: rainfall and temperature significant; basal area strong for *B. edulis*.
- [R13] Martínez de Aragón J., Bonet J.A., Fischer C.R., Colinas C. (2007) Productivity of
  ectomycorrhizal and selected edible saprotrophic fungi in pine forests of the pre-Pyrenees
  mountains, Spain: predictive equations for forest management of mycological resources. *Forest
  Ecology and Management* 252: 239–256. https://doi.org/10.1016/j.foreco.2007.06.040 `snippet-only`
  (content known only through R15, Table 4). Supports: annual precipitation, precipitation minus
  Sep/Oct evapotranspiration, minimum August soil temperature (community yield).
- [R14] Bonet J.A., Palahí M., Colinas C., Pukkala T., Fischer C.R., Miina J., Martínez de Aragón J.
  (2010) Modelling the production and species richness of wild mushrooms in pine forests of the
  Central Pyrenees in northeastern Spain. *Canadian Journal of Forest Research* 40: 347–356.
  https://doi.org/10.1139/X09-198 `verified` (abstract, via OpenAlex). Supports: basal area
  15–20 m²/ha; slope, elevation, aspect and autumn rainfall as predictors.
- [R15] Boddy L., Büntgen U., Egli S., Gange A.C., Heegaard E., Kirk P.M., Mohammad A., Kauserud H.
  (2014) Climate variation effects on fungal fruiting. *Fungal Ecology* 10: 20–33.
  https://doi.org/10.1016/j.funeco.2013.10.006 `verified` (author PDF:
  https://www.mn.uio.no/ibv/english/people/aca/haavarka/boddy-et-al-2014.pdf). Supports: review of
  yield drivers (Table 4), ET importance in the Mediterranean, preceding-year lags, variable
  temperature effects, season extension.
- [R16] Alday J.G., Martínez de Aragón J., de-Miguel S., Bonet J.A. (2017) Mushroom biomass and
  diversity are driven by different spatio-temporal scales along Mediterranean elevation gradients.
  *Scientific Reports* 7: 45824. https://doi.org/10.1038/srep45824 `verified` (abstract). Supports:
  late-summer–early-autumn precipitation as main driver; elevation not significant (community).
- [R17] Taye Z.M., Martínez-Peña F., Bonet J.A., Martínez-de-Aragón J., de-Miguel S. (2016)
  Meteorological conditions and site characteristics driving edible mushroom production in *Pinus
  pinaster* forests of Central Spain. *Fungal Ecology* 23: 30–41.
  https://doi.org/10.1016/j.funeco.2016.05.008 `snippet-only`. Supports: late summer and early autumn
  precipitation drive emergence and yield (*B. edulis* among the species).
- [R18] Kauserud H. et al. (2012) Warming-induced shift in European mushroom fruiting phenology.
  *PNAS* 109: 14488–14493. https://doi.org/10.1073/pnas.1200789109 `verified` (abstract). Supports:
  season widening and later end, 1970–2007; mycorrhizal seasons more compressed.
- [R19] Büntgen U., Kauserud H., Egli S. (2012) Linking climate variability to mushroom productivity
  and phenology. *Frontiers in Ecology and the Environment* 10: 14–19. https://doi.org/10.1890/110064
  `verified` (abstract). Supports: Swiss mycorrhizal fruiting 10 days later after 1991; precipitation
  and temperature determine activity. (The card's "Büntgen et al. 2012" could also mean the truffle
  drought paper cited in R15; not used.)
- [R20] Andrew C. et al. (2018) Explaining European fungal fruiting phenology with climate variability.
  *Ecology* 99: 1306–1315. https://doi.org/10.1002/ecy.2237 `verified` (abstract). Supports: altitude
  shifts fruiting by up to 30 d (spring delays, autumnal accelerations); temperature drives autumn
  ectomycorrhizal phenology.
- [R21] Andrew C. (2025) Not always optimal: fungal fruiting triggers indicate climate sensitivity in
  cooler regions. *Fungal Ecology* 75: 101416. https://doi.org/10.1016/j.funeco.2025.101416 `verified`
  (abstract). Supports: all 127 species sensitive to daily temperature extremes.
- [R22] Hall I.R., Lyon A.J.E., Wang Y., Sinclair L. (1998) Ectomycorrhizal fungi with edible fruiting
  bodies 2. *Boletus edulis*. *Economic Botany* 52: 44–56. https://doi.org/10.1007/BF02861294
  `verified` (abstract only; no climate numbers in the abstract). Supports: *B. edulis* s.l. as a
  complex; hosts in Fagaceae, Pinaceae, Betulaceae.
- [R23] Beugelsdijk D.C.M. et al. (2008) A phylogenetic study of *Boletus* section *Boletus* in
  Europe. *Persoonia* 20: 1–7. https://doi.org/10.3767/003158508X283692 (PMC:
  https://pmc.ncbi.nlm.nih.gov/articles/2865352) `verified`. Supports: four species; synonyms within
  *B. edulis*; per-species host and soil notes (Netherlands-centred sampling).
- [R24] Matteucci S. (2008) I *Boletus* del gruppo *edulis*, i "principi" del bosco. *MicoPonte* 2:
  4–14 (text version). https://www.micoponte.it/File/I%20Boletus%20del%20gruppo%20edulis,%20i%20principi%20del%20bosco.pdf
  `verified` (full text; the article speaks of Lucca province and Garfagnana). Supports: per-taxon
  habitat, season, altitude tendency and thermal preference; vernacular names.
- [R25] Censimento dei macromiceti (Federazioni dei gruppi micologici del Trentino-Alto Adige, Veneto,
  Friuli Venezia Giulia; hosted by MUSE), species pages with texts by M. Floriani: *B. aereus*
  https://www2.muse.it/bresadola/map_det.asp?sp=159002&ar=tv ; *B. edulis* …sp=356530 ;
  *B. aestivalis* …sp=172910 ; *B. pinophilus* …sp=309751. `verified`. Supports: phenology and
  altitude extremes (NE Italy), *B. pinophilus* earliest/latest, *B. aereus* mainly central-southern
  Italy and confused with *B. aestivalis*, nomenclature (*B. pinicola* illegitimate).
- [R26] Museo del Fungo Porcino di Borgotaro, "Gli habitat del Porcino".
  https://fungoporcinodiborgotaro.museidelcibo.it/il-prodotto/caratteristiche/gli-habitat-del-porcino/
  `verified`. Supports: per-taxon hosts and season; *B. aereus* at low elevations.
- [R27] Gruppo Micologico Naturalistico Siena, schede tecniche: *B. aereus*
  https://www.gruppomicologicosiena.it/cms/micologia/schede-tecniche-micologiche/72-boletus-aereus-bull ;
  *B. edulis* http://www.gruppomicologicosiena.it/cms/micologia/schede-tecniche-micologiche/97-boletus-edulis-bull
  `verified`. Supports: *B. aereus* early summer to late autumn, broadleaves and pines with "scopi";
  *B. edulis* August–November, plain to mountain.
- [R28] Sardegna Foreste, scheda *Boletus aereus*. https://www.sardegnaforeste.it/fungo/boletus-aereus
  `verified`. Supports: holm oak, chestnut, *Arbutus*/*Erica* macchia hosts.
- [R29] Regione Toscana, Giunta Regionale (1998) Boschi e macchie di Toscana – I tipi forestali
  (Mondino G.P., Bernetti G. et al.), parte IV (and parte I).
  https://www.regione.toscana.it/documents/10180/24010/I%20tipi%20forestali%20-%20parte%20IV/8fa2a8d0-3d68-48ed-8471-c44fc2c87f87
  `verified` (PDF). Supports: Tuscan beech belt 900–1700 (1800) m; fir 900–1300 (1500) m, north
  aspects below 1000 m; Amiata beech types.
- [R30] Arrigoni P.V., Viciani D. Caratteri fisionomici e fitosociologici dei castagneti toscani.
  *Parlatorea* 5: 55–99 (year not verified).
  https://www.researchgate.net/publication/236342898 `snippet-only`. Supports: chestnut rarely above
  ~1000 m in Tuscany.
- [R31] Santolamazza-Carbone S., Iglesias-Bernabé L., Landin M., Rueda E.B., Barreal M.E., Gallego P.P.
  (2023) Artificial intelligence unveils key interactions between soil properties and climate factors
  on *Boletus edulis* and *B. reticulatus* mycelium in chestnut orchards of different ages. *Frontiers
  in Soil Science* 3. https://doi.org/10.3389/fsoil.2023.1159793 `verified` (full text via WebFetch).
  Supports: *B. reticulatus* mycelium with prior water deficit + high soil moisture; more in mature
  orchards (Galicia, mycelium).
- [R32] Oria-de-Rueda J.A., Martín-Pinto P., Olaizola J. (2008) Bolete productivity of cistaceous
  scrublands in northwestern Spain. *Economic Botany* 62: 323–330.
  https://doi.org/10.1007/s12231-008-9031-x `snippet-only`. Supports: *B. edulis* and *B. aereus*
  fruit in *Cistus ladanifer* scrub (37.8 and 22.5 kg/ha).
- [R33] Alonso Ponce R. et al. (2011) Rockroses and *Boletus edulis* ectomycorrhizal association:
  realized niche and climatic suitability in Spain. *Fungal Ecology* 4: 224–232.
  https://doi.org/10.1016/j.funeco.2010.10.002 `snippet-only`. Supports: mesothermal, Mediterranean,
  humid climatic niche; strongly acid loam soils.
- [R34] GBIF API queries run 2026-09-17: species match
  (https://api.gbif.org/v1/species/match?name=Boletus%20aestivalis&kingdom=Fungi etc.) and occurrence
  facets for Tuscany
  (https://api.gbif.org/v1/occurrence/search?taxonKey=5954691&gadmGid=ITA.16_1&limit=0&facet=month&facet=basisOfRecord&facet=datasetKey)
  and Italy (`country=IT`). `verified` (own queries). Supports: name mapping, record counts, month
  distribution, `MATERIAL_SAMPLE` trap (dataset "Global soil organisms").
- [R35] 3bmeteo Funghi, "Pioggia e funghi: quanta ne deve cadere, e perché serve?"
  https://funghi.3bmeteo.com/pioggia-e-funghi-porcini/ `verified` (**folklore**; no sources cited).
  Supports: 40–50 to 90–100 mm over ~2 weeks; repeated moderate rain; taxon rain preferences. Its
  claims on north slopes and temperature drops were seen in other 3bmeteo pages via search summaries
  only.
- [R36] Funghi Magazine, "Quanti giorni dopo la pioggia nascono i funghi Porcini?"
  https://funghimagazine.it/quanti-giorni-dopo-la-pioggia-nascono-i-funghi-porcini/ `verified`
  (**folklore**). Supports: 30–80 mm in ½–2 days; 10–22 d to first growth, 15 d "ideal"; no wind after
  rain.
- [R37] Funghi Magazine, "Fino a quando nascono i Porcini".
  https://funghimagazine.it/fino-a-quando-nascono-i-porcini/ `verified` (**folklore**; the fetched
  summary was partly garbled, and the +8 °C claim matches a search snippet). Supports: end of season
  with snow, constant cold wind and frost; *B. reticulatus* stops with first cold; *B. aereus* hardier.
- [R38] "Prevedere l'uscita dei porcini" (blog, author "Giancarlo").
  http://prevedereuscitaporcini.blogspot.com/2016/12/ecco-i-giorni-necessari-per-far-sbucare.html
  `verified` (**folklore**, personal model). Supports: 8 d minimum at 60 mm / 14 °C, up to 14 d; longer
  in cooler high beech than in chestnut at 600–700 m.
- [R39] Forager pages on wind: Funghi Magazine, "Vento e freddo bloccheranno le nascite al Nord?"
  https://funghimagazine.it/vento-e-freddo-al-nord-tanti-porcini-al-centro-sud/ and Volpi del Vajolet,
  "Piccolo manuale e consigli per andare a funghi"
  https://www.volpidelvajolet.it/2017/09/piccolo-manuale-e-consigli-per-andare-a-porcini.html
  `snippet-only` (**folklore**). Supports: tramontana and other drying winds as the main enemy; no wind
  after rain.
- [R40] Sitta N., Floriani M. (2008) Nationalization and globalization trends in the wild mushroom
  commerce of Italy with emphasis on porcini (*Boletus edulis* and allied species). *Economic Botany*
  62: 307–322. https://doi.org/10.1007/s12231-008-9037-4 `snippet-only` (abstract start seen on the
  Springer page). Supports: nothing encodable; trade history.
- [R41] Gelardi M. (2020) Diversity, biogeographic distribution, ecology, and ectomycorrhizal
  relationships of the edible porcini mushrooms (*Boletus* s. str., Boletaceae) worldwide: state of the
  art and an annotated checklist. Springer book chapter. https://doi.org/10.1007/978-3-030-37378-8_8
  `snippet-only`. Supports: lead only (per-species hosts); not read.
- [R42] Micoweb, *Boletus pinophilus*. https://www.micoweb.it/boleti/boletus-pinophilus `verified`
  (amateur site, **folklore**-level). Supports: mainly autumnal, sporadic late spring; conifers and
  beech, chestnut, birch.
- [R43] Leonardi P., Graziosi S., Zambonelli A., Salerni E. (2017) The economic potential of mushrooms
  in an artificial *Pinus nigra* forest. *Italian Journal of Mycology* 46: 48–59.
  https://doi.org/10.6092/issn.2531-7342/7287 `snippet-only`. Supports: Amiata black pine survey edible
  species list without porcini (weak).
- [R44] Ambrosio E., Zotti M. (2015) Mycobiota of three *Boletus edulis* (and allied species)
  productive sites. *Sydowia* 67: 197–216.
  https://www.academia.edu/31148543/Mycobiota_of_three_Boletus_edulis_and_allied_species_productive_sites
  `snippet-only`. Supports: soil properties and geochemistry more strongly correlated with the
  community than vegetation and climate.
