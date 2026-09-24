# Ovoli (ovolo buono): *Amanita caesarea* (evidence appendix to species-ecology.md)

Research date: 2026-09-17. Research only: no code. All numbers marked **derived** were
produced here from the cited evidence (method stated next to each); none of them is
a number printed by a source unless it carries a direct cite.

**Bottom line.** No peer-reviewed field study was found that links *A. caesarea*
fruiting to rain amount, lag or soil temperature in numbers. The species-specific
evidence is: hosts, habitat and altitude (peer-reviewed plot surveys in Tuscany, the
IUCN assessment, a national Red Data Book), a lab thermal optimum for mycelium, and a
phenology signal from Italian sightings. The weather rules below come from Tuscan
community-level fruiting studies (all macrofungi, not ovoli alone), Mediterranean
ectomycorrhizal yield models, Open-Meteo climatology over the observed season, and
forager lore. The backtest has to tune them.

The starting hypothesis in the card ("July–October after warm storms, oak and chestnut,
lower hills") is **partly corrected**. In Tuscany the main window is **September to
early November**, peaking in October. June–August flushes happen but are uncommon.

## Scope and taxonomy notes

- **Taxon.** *Amanita caesarea* (Scop.) Pers., sect. *Caesareae*. GBIF taxonKey
  `5240269`; iNaturalist taxon `204588` [R14, R15]. GBIF synonyms include *Agaricus
  caesareus*, *Amanita aurantiaca*, *Volvoamanita caesarea* and the colour forms/varieties
  *A. caesarea* f. *alba*, var. *alba*, f. *lutea*, var. *rubra*, var. *aurantia*
  [R14]. These fold into the species key, so a query on `5240269` already includes them.
- **Misapplied name outside Europe.** GBIF's `5240269` has 447 US and 338 Mexican records
  (of 3,828 worldwide) [R14]. They belong to other species of sect. *Caesareae*
  (*A. jacksonii* and relatives in North America; the East Asian taxa once treated as
  *A. caesarea* are now separate species [R13]). **For mushma, filter by country (Italy,
  or the Mediterranean if pooling) and never use the global record set for phenology or
  climate envelopes.**
- **Common name.** In Tuscany and Italy generally the species is "ovolo buono" (also
  "ovolo reale"). The vernacular "ovolo" is not unique to this species in Italy, so
  match records by scientific name or taxon key, never by vernacular text.
- **Native range.** Mediterranean and Black Sea basins (S Europe, N Africa, Caucasus,
  Ukraine/Crimea). North America and East Asia are excluded [R7]. Northern and Alpine
  records (Switzerland has 527 GBIF records) are warm-site outliers and should not set
  the Tuscan envelope.
- **Record volume (important for validation).** Italy: 208 GBIF records (148 from
  iNaturalist research-grade). **Tuscany: 39 GBIF records = 35 unique observer-days**,
  mostly 2019–2025, heavily in the provinces of Grosseto and Livorno. iNaturalist has
  50 Tuscan observations of any quality grade (47 research-grade) [R14, R15]. Duplicates
  exist (same observer, same day, same place): dedupe by observer, day and cell before
  counting.

## Rules summary

Trapezoids are `[zero_below, full_from, full_to, zero_above]` (dates `DD-MM`). "Data"
says whether the engine inputs exist in v1 (`available`), whether the parameters are
numbers derived here (`derived`; the inputs are still available), or whether the input
is not in v1 (`missing`).

| id | taxon | factor | rule (plain words) | parameters | confidence | sources | data |
|---|---|---|---|---|---|---|---|
| OVO-01 | A. caesarea | season window | Fruits from early summer, mostly Sept–early Nov in Tuscany; summer flushes are occasional and weather-limited | `season_trapezoid = [01-06, 01-09, 05-11, 30-11]`; autumn end shifts about −5 days per +100 m above 400 m (**derived**) | plausible | R1, R6, R7, R8, R14, R15, R21, R22 | derived |
| OVO-02 | A. caesarea | habitat / host, four levels (2026-09-24) | Obligate ectomycorrhizal partner of Fagaceae: deciduous oaks and chestnut first, evergreen oaks next; no host in conifer or robinia stands | affinity table below: host 1.0 (`deciduous_oak`, `chestnut`) / secondary 0.6 (`evergreen_oak`, `transitional_woodland_shrub`) / marginal 0.3 (`macchia`, `mixed_broadleaf`, `mixed_broadleaf_conifer`) / non-host 0-0.1 (rest), saturated to full credit from a 0.30 host-weighted share (**derived** ranking) | strong (host genera) / plausible (numeric ranking) | R1, R2, R5, R6, R7, R8, R17, R19, mushma_habitat_share_2026 | available |
| OVO-03 | A. caesarea | altitude | Sea level to mid-hills; thins out above ~750 m; practically absent above ~1100 m in Tuscany | `altitude_trapezoid_m = [0, 0, 750, 1100]` (**derived**) | plausible (well supported) | R1, R7, R14, R16, R17, R18, R21, R22 | derived |
| OVO-04 | A. caesarea | aspect | Warmer, sunnier slopes favoured, mainly near the upper altitude limit | optional multiplier: 1.0 on S-facing (135–225°); 0.8 on N-facing (315–45°) where slope > 10° and elevation > 500 m (**derived**) | folklore | R6, R18, R23, R25 (counter-example R1) | derived |
| OVO-05 | A. caesarea | rain trigger (amount) | A soaking rain event is needed; light showers do nothing | 3-day rain sum ramp: 0 at ≤ 10 mm, 1 at ≥ 30 mm (**derived**) | folklore | R23, R24 | derived |
| OVO-06 | A. caesarea | rain trigger (lag) | Fruit bodies appear one to three weeks after the trigger rain | `lag_trapezoid_days = [6, 10, 20, 28]` (**derived**) | folklore | R3, R23, R24 | derived |
| OVO-07 | A. caesarea | post-rain soil moisture | The rain only works if the topsoil stays moist for several days afterwards | mean soil moisture 0–7 cm over the 7 days after the trigger: 0 at ≤ 0.15, 1 at ≥ 0.22 m³/m³ (**derived**, Open-Meteo/ERA5-Land scale; tune) | plausible | R3, R16, R24 | derived |
| OVO-08 | A. caesarea | cumulative rain | Fruiting tracks rain over the preceding ~30 days | 30-day rain sum ramp: 0 at ≤ 25 mm, 1 at ≥ 75 mm (**derived**) | plausible (extrapolated from all-macrofungi Tuscan data) | R3, R11, R16 | derived |
| OVO-09 | A. caesarea | antecedent (spring) | Wet springs precede richer autumn fruiting (community-level); weak modifier | Mar–May rain as % of local normal: multiplier 0.8 at ≤ 60 %, 1.0 at ≥ 100 % (**derived**) | plausible (extrapolated) | R3 | derived |
| OVO-10 | A. caesarea | soil temperature | Warm soil needed; fruiting fades as the topsoil cools in November; summer heat alone does not stop it | 0–7 cm soil temp, mean of the lag window (trigger → score day): `[9, 14, 26, 32]` °C (**derived**; upper edges are placeholders) | plausible | R5 (lab), R14, R15, R16, R22 | derived |
| OVO-11 | A. caesarea | air temperature | Alternative to OVO-10 (do not use both at full weight) | 2 m Tmean, 7-day mean: `[8, 13, 25, 30]` °C (**derived**) | plausible | R16 (as OVO-10) | derived |
| OVO-12 | A. caesarea | stopper: cold nights | Cool nights end the season | 2 m Tmin, 7-day mean: multiplier 0 at ≤ 5 °C, 1 at ≥ 10 °C (**derived**) | plausible | R14, R16, R21, R22 | derived |
| OVO-13 | A. caesarea | stopper: frost | Any frost ends the flush for low-hill cells | any day Tmin ≤ 0 °C in the last 7 days → multiplier 0 (**derived**, generic; no ovoli source) | folklore | none specific | derived |
| OVO-14 | A. caesarea | stopper: evaporative demand | High ET0 after the rain dries the topsoil and cancels the trigger | ET0 7-day mean after trigger: multiplier 1 at ≤ 4 mm/d, 0.4 at ≥ 6 mm/d (**derived**) | plausible (extrapolated: pine forests, Spain) | R10, R16, R24 | derived |
| OVO-15 | A. caesarea | stopper: drying wind | Dry downslope/north winds after the storm cancel it within ~2 days | within 5 days after trigger, ≥ 2 days with max gust ≥ 40 km/h **and** min RH ≤ 35 % → multiplier 0.5 (**derived**, generic) | folklore | R24 | derived |
| OVO-16 | A. caesarea | waterlogging | Excess, standing water is unfavourable; well-drained soils preferred | optional: soil moisture 0–7 cm 7-day mean ≥ 0.40 m³/m³ → multiplier 0.8 (**derived**) | folklore | R8, R22, R25 | derived |
| OVO-17 | A. caesarea | soil substrate / pH | Prefers well-drained, siliceous, slightly acid soils; possibly scarce on limestone | not encodable in v1 (pH, lithology) | plausible (sources disagree) | R2, R5 (lab), R6, R23, R25 vs R18/R22 | missing |
| OVO-18 | A. caesarea | canopy / management | Open, sunny stands, clearings, edges and managed (cleared) chestnut orchards; declines with abandonment | not encodable in v1 (canopy cover, management) | plausible | R6, R8, R18, R19, R21 | missing |
| OVO-19 | A. caesarea | disturbance / N | Appears in burnt or recently worked areas (lore); harmed by fertilisation and N deposition | not encodable in v1 | folklore (fire) / plausible (N) | R7, R21 | missing |

## Evidence by factor

### Season windows

**What sources say**

- *Tuscany, plot studies (peer-reviewed).* 30 years of monthly (fortnightly in peak
  season) plot surveys by Università di Siena across 11 Tuscan permanent plots: "at
  intermediate altitudes, excluding the occasional carpophore in spring, production is
  practically limited to autumn". In coastal evergreen oak woods "the critical months are
  July and August, with drought and high temperatures". The hill belt has "two limiting
  periods, cold winters and arid summers" [R1]. This is community-level, not
  species-level, but it describes the same belt where ovoli grow. The deciduous-oak
  survey notes sampling was "discontinuous in summer when drought and high temperatures
  did not favour fungal fruiting" [R2], so these plot studies under-sample any summer
  flush.
- *SW Spain (lab team's field note).* "A thermophilic species which, in our climatic
  conditions, appears at the beginning of autumn, from October to mid-November when the
  climate is mild and rainy; if the spring is wet it can occasionally appear between
  spring and summer." Quoted in a UPM thesis citing Daza et al. 2006 [R6; original
  attribution to R5 is `snippet-only`].
- *Bulgaria (Red Data Book).* Fruit bodies "VI–X" (June–October) [R8].
- *Italian societies and lore.* "Estate e autunno" (summer and autumn) [R17, R18, R20].
  "Esclusivamente nei mesi estivi, giugno … ottobre" (only in the summer months, June
  to October), fruiting after a spell of steady heat [R22]. In Tuscany, from mid-May to
  November at low elevation [R21]. July–September with an August peak (a generic
  Italy-wide commercial guide) [R25].
- *Sightings (data, not literature).*
  - GBIF Italy, n = 173 dated records. Day-of-year percentiles: p5 01-07, p10 06-08,
    p25 06-09, **p50 26-09**, p75 19-10, p90 04-11, p95 08-11 [R14].
  - GBIF Tuscany, n = 39. Months: Jun 1, Jul 1, Aug 2, Sep 11, **Oct 21**, Nov 3.
    Percentiles: p5 06-08, p10 28-08, p25 11-09, **p50 13-10**, p75 23-10, p90 31-10,
    p95 04-11 [R14]. The latest Tuscan record is 21 Nov (a coastal Livorno hill).
  - iNaturalist Tuscany, all quality grades, n = 50. Jun 2, Jul 1, Aug 2, Sep 17,
    **Oct 26**, Nov 2. Weeks 36–44 hold 41 of 50 [R15]. iNaturalist Italy, n = 268:
    Jun 9, Jul 6, Aug 33, Sep 111, Oct 89, Nov 15 [R15].

**Numbers and confidence**

- `season_trapezoid = [01-06, 01-09, 05-11, 30-11]` is **derived**. `full_from` 01-09
  sits just after the Tuscan p10 (28-08) and before p25 (11-09). `full_to` 05-11 is
  about the Tuscan p95 (04-11). `zero_after` 30-11 covers the late coastal tail
  (21 Nov). `zero_before` 01-06 lets June–August storm flushes score (about 0.33 on
  1 Jul and 0.66 on 1 Aug) while the rain, moisture and ET0 rules do the real limiting
  in dry summers.
- Summer weight is deliberately partial. Summer records are 5/50 (iNat) and 4/39 (GBIF)
  in Tuscany, and 48/268 in Italy (Italy includes cooler northern and Apennine sites,
  where the summer share is plausibly higher).
- **Altitude shift (derived).** Fold it into temperature (OVO-10/12) rather than
  separate windows. If a fixed shift is needed, use about −5 days per +100 m above
  400 m on `full_to`/`zero_after`. Method: Open-Meteo climatology cools the 0–7 cm
  soil at about 0.14 °C/day through October (Montagnola Senese: 15.4 °C on 1–15 Oct,
  11.1 °C on 1–15 Nov) [R16], and a standard lapse rate of about 0.6 °C/100 m gives
  ~4–5 days/100 m. European data show altitude shifts autumn fruiting earlier by up to
  30 days, across all fungi [R12].
- Confidence **plausible**. The window agrees with the literature and with two
  independent sighting sets. **Circularity warning:** the sighting percentiles use all
  years. Re-derive `full_from`/`full_to` on train seasons only before the backtest.

### Hosts and habitat affinity

**What sources say**

- *Global assessment.* Ectomycorrhizal with Fagaceae, "typically *Quercus*" (*Q. cerris,
  robur, ilex* named), also *Fagus*, *Castanea*, *Carpinus*, *Corylus*, and "occasionally
  conifers" regionally. Habitats: "mainly in deciduous to sclerophyllous forests dominated
  by *Quercus*", plus dehesas, montados, mixed forests, grasslands with solitary trees and
  heaths [R7].
- *Tuscany, plot data.*
  - Across 11 plots on a coast-to-Apennine transect, the species was recorded **only in
    chestnut coppice St. 6** (550 m, NE-facing, sandstone; max density class 2, fruiting
    in 2 years). It was absent from four holm-oak plots (50–275 m), the other two
    chestnut coppices (525 m, 870 m) and four fir/beech plots (770–1210 m) [R1].
  - In the 30-plot synthesis for central-southern Tuscany it appears in **1 of 10
    evergreen-oak plots and 1 of 9 chestnut coppices**, and in **0 of 4 calcicolous
    deciduous-oak plots** (*Q. cerris* + *Q. pubescens*, limestone "calcare cavernoso",
    soil pH 6.8–7.4) and 0 of 7 fir plots [R2].
  - Read these as "rare in any single plot", not as a host ranking: plots are 0.1–0.2 ha
    and summer visits were sparse.
- *Spain.* Lab isolates came from fruit bodies under *Q. suber* and *Castanea sativa*
  [R5]. Habitat: thinned Fagaceae stands and clearings with heath (*Calluna*, *Erica*),
  *Cistus*/*Halimium* scrub and old marginal fields, around holm-oak, cork-oak,
  *Q. pyrenaica* and other oak woods, hazel and chestnut groves, "always well lit". Less
  in beech woods (dense, few clearings) and in strawberry-tree scrub [R6].
- *Bulgaria.* "Light and warm oak forests and mixed deciduous (oaks, beeches, sweet
  chestnut) forests" on drained soils [R8].
- *Italian institutions and societies.* Warm broadleaf woods (*Castanea*, *Quercus*),
  "spesso … in presenza di corbezzolo ed erica" (often with strawberry tree and heather)
  [R19, Sardinia's regional forest agency]. Under chestnut and Turkey oak [R17]. Under
  oaks of warm-Mediterranean zones (*Q. cerris*, *Q. frainetto*, *Q. ilex*…), secondarily
  chestnut, hornbeam and manna ash [R22]. Not in beech woods [R25]. Tuscany: chestnut and
  oaks; open oak woods, clearings, cleared fruit-chestnut groves, often with *Erica
  scoparia/arborea* [R21].

**Affinity per habitat key, four levels (2026-09-24, `mushma_habitat_share_2026`): host 1.0 / secondary 0.6 /
marginal 0.3 / non-host 0–0.1, requantised from the derived ranking below.** A good host is the baseline; only
poor or unsuitable woods pull the score down, and the habitat factor now saturates to full credit once about 30 %
of a cell's woods are worth a host, so a cell mostly in host wood is no longer diluted by the rest.

| key | level | rationale |
|---|---|---|
| `deciduous_oak` | **host** | Primary host group in Italy (*Q. cerris, Q. pubescens, Q. frainetto*) [R7, R17, R22]. Caveat: absent from the Tuscan calcicolous cerro/roverella plots [R2] (see OVO-17). |
| `chestnut` | **host** | Repeatedly named co-primary host [R5, R6, R17, R19, R21]; the only Tuscan plot record is in chestnut coppice [R1]. Lore says it declines in abandoned groves [R21]. |
| `evergreen_oak` | **secondary** | *Q. ilex* and *Q. suber* are confirmed hosts [R5, R7], but Tuscan plots (0/4 [R1], 1/10 [R2]) show it is clearly less typical than oak/chestnut. Dense leccete are shady; sugherete are open. The Maremma/Livorno sighting cluster sits in mosaics of cerrete, leccete and sugherete [R14] that the grid cannot separate. |
| `transitional_woodland_shrub` | **secondary** | Not in the source appendix, added in the merge: clearings, edges and heath with scattered oaks are repeatedly described as favoured [R6, R18, R21] — "open woodland/clearing/edge matters more than the host list suggests" (below). |
| `macchia` | **marginal** | Often next to *Arbutus/Erica* [R6, R19, R21], but those are not documented hosts; the real host is scattered *Q. ilex/Q. suber* within it, so it is a dilution class like the mixed types below, not a host habitat in its own right. May fall outside the woodland mask. |
| `mixed_broadleaf` | **marginal** | *Carpinus*, *Corylus* are listed hosts [R7]; ostrieti are often cool and calcareous. Only its oak/chestnut admixture is a host. |
| `mixed_broadleaf_conifer` | **marginal** | Only through its oak/chestnut component. |
| `mediterranean_pine` | **non-host (0.1)** | Coastal pinete often have an evergreen-oak understorey; no source names Mediterranean pines as a Tuscan host. |
| `exotic_broadleaf` (robinia) | **non-host (0.05)** | No host; often replaces old chestnut, so remnant hosts are possible. |
| `beech` | **non-host (0)** | *Fagus* listed [R7, R8], but "not in beech woods" [R25] and "less in beech woods" [R6]. In Tuscany beech is mostly above the altitude band. |
| `riparian` | **non-host (0)** | No host. |
| `mountain_pine` | **non-host (0)** | Conifers only "occasionally … in specific regions" [R7]; above the band. |
| `other_conifer` | **non-host (0)** | Same. |
| `fir_spruce` | **non-host (0)** | Not recorded in any Tuscan fir plot [R1, R2]; above the band. |

**Vocabulary notes (proposals, not additions).**

- Chestnut *orchards* (castagneti da frutto, managed, open canopy) and chestnut *coppice*
  (ceduo) probably differ for ovoli. Lore and the Spanish summary favour open, cleared
  or lightly worked chestnut groves [R6, R21]. If the M2 forest-type layer separates
  them, split `chestnut` into `chestnut_orchard` (1.0) and `chestnut_coppice` (0.7).
  Otherwise keep one key.
- "Open woodland / clearing / edge" matters more than the host list suggests
  [R6, R18, R21], but it is canopy structure, not a forest type. It belongs to a
  future canopy-cover modifier (see Not modellable).

**Confidence.** **Strong** that *Quercus* and *Castanea* are the hosts: several
consistent peer-reviewed or expert-assessed sources plus Tuscan plot records. The
numeric ranking is **plausible** and **derived**.

### Altitude and aspect

**What sources say**

- "Lowlands to lower mountain regions, only seldom above 1200 m" [R7].
- Italy: "fino a 900 m" (up to 900 m) [R17, R18]. Tuscany: up to 1000 m [R21].
  Regional lore puts it up to ~500 m in NW Italy, ~600 m in NE Italy, 800–900 m in
  some foothills, ~1000 m in the Apennines and 1200 m in the south [R22]. Typically
  200–900 m (a generic Italian guide) [R25].
- Tuscan plots: present at 550 m; absent at 770–1210 m (fir/beech) and at the 870 m
  chestnut plot [R1].
- **Sightings with elevation (derived).** Records with coordinate uncertainty ≤ 1 km,
  elevation from the Copernicus DEM via the Open-Meteo elevation API [R14, R16].
  - Italy, n = 92: min 15 m, p10 176, p25 279, **p50 424**, p75 623, **p90 769**,
    p95 840, **max 943 m**; none above 1000 m.
  - Tuscany, n = 26: min 64 m, p10 196, p25 260, **p50 343**, p75 459, **p90 752**,
    p95 820, **max 930 m**.
  - Only aggregates are reported here, never coordinates.
- **Aspect.**
  - South-facing, sunny clearings favoured: "esposizione a Sud, in particolare nelle
    radure" [R18]. S/SE slopes (Spain) [R23]. Heliophilous [R6]. Shaded aspects delay
    it [R25].
  - Counter-example: the only Tuscan plot record is NE-facing, on a 30° slope [R1].

**Numbers and confidence**

- `altitude_trapezoid_m = [0, 0, 750, 1100]` is **derived**. Full suitability from sea
  level to about the Tuscan/Italian p90 (752–769 m), falling to zero at 1100 m: between
  the highest Italian record (943 m), the ~1000 m Apennine lore, and IUCN's "seldom above
  1200 m". The lower edge is not limiting: records reach 15–64 m. Low coastal cells are
  limited by summer drought, and the weather rules cover that.
- Aspect (OVO-04): **folklore**, optional, applied only near the upper limit (> 500 m)
  where warmth is marginal. The multiplier is **derived**; v1 may skip it.
- Confidence **plausible**, well supported. Circularity warning as for the season
  window: the sighting percentiles use all years.

### Rain trigger (amount, lag)

**What sources say**

- *Tuscan oak forests (peer-reviewed; all macrofungi).* Weather correlated with number of
  species and fruit bodies, using rain and temperature over the 5, 10, 15 and 30 days
  before sampling. "Rainfall was the main influence on fruiting in the most important
  fruiting period (autumn). Highly significant correlations were found between the
  number of carpophores and rainfall in the 30 days preceding sampling" [R3; abstract
  only].
- *Spanish forager lore (ovoli-specific).* Needs rain episodes of "unos 15 o 20 l/m²"
  (about 15–20 mm), then "entre 18 y 22 días" (18–22 days) before fruit bodies appear
  [R23]. Another popular site repeats the same figures and is not independent.
- *Italian meteorological mushroom column (lore).*
  - For the Tyrrhenian hill belt of central Italy (Maremma laziale to the Tolfa hills,
    next to southern Tuscany): "se un temporale estivo scarica 30-50 mm in poche ore e
    il suolo resta umido per alcuni giorni, si possono osservare emergenze repentine di
    *Boletus aereus* e *Amanita caesarea*" (if a summer storm drops 30–50 mm in a few
    hours and the soil stays wet for a few days, sudden emergences of *B. aereus* and
    *A. caesarea* can be seen).
  - Generic statements in the same piece, not ovoli-specific:
    - Short violent storms of 10–15 mm mostly give no significant fruiting because the
      water only wets the litter.
    - Wait 8–10 days after a ≥ 25–30 mm storm.
    - In warm hill oak woods with Tmin around 18–20 °C, thermophilic porcini
      (*B. aereus*, *B. aestivalis*) can emerge after 10–11 days.
    - 15–20 days where Tmin drops below 10–12 °C [R24].
- *Italian lore.* A good summer storm can boost fruiting "purché" the water drains
  quickly without pooling [R22].
- **No peer-reviewed ovoli-specific rain amount or lag was found.** Baptista et al. 2010
  (chestnut orchards, NE Portugal) is the most likely candidate; only its metadata and a
  machine-generated summary were accessible ("species richness and carpophore abundance
  fluctuated across years … especially to rainfall") [R9, `snippet-only`].

**Numbers and confidence**

- **OVO-05 (derived):** 3-day rain sum, 0 at ≤ 10 mm, 1 at ≥ 30 mm. The lower edge
  follows "10–15 mm gives nothing" [R24]. The upper edge sits between the Spanish
  15–20 mm [R23] and the Italian 30–50 mm summer storms [R24]. A 3-day window captures
  multi-cell storms. **Folklore.**
- **OVO-06 (derived):** `lag_trapezoid_days = [6, 10, 20, 28]`.
  - `full_from` 10 d follows the warm-weather 8–11 d [R24]; that figure is for
    thermophilic porcini, extrapolated here to ovoli.
  - `full_to` 20 d is the middle of the Spanish 18–22 d [R23].
  - `zero_after` 28 d is about the 30-day window with the strongest Tuscan correlation
    [R3].
  - Optional refinement, also derived and folklore [R24]: shift the trapezoid 3–4 days
    earlier when the lag-window Tmin mean is ≥ 16 °C, and 3–4 days later when it is
    ≤ 11 °C.
  - **Folklore** (the lag has no scientific source).
- The PRD's porcini lag (~10–15 d) sits inside this trapezoid. Ovoli lore points
  somewhat longer (18–22 d); the backtest should compare [6, 10, 20, 28] with
  [10, 15, 24, 32].

### Antecedent moisture

**What sources say**

- Tuscan oak forests: "abundant annual rainfall was necessary for the fungal mycelium to
  fruit. Spring rainfall in particular seemed to be related to the number of species
  found in autumn" [R3] (community-level).
- Mediterranean ectomycorrhizal yield models (other hosts, same climate type):
  - *Pinus pinaster* stand, Spain, 15 years: "simple models based on early spring
    temperature and summer–autumn rainfall" predicted yields; water-balance models fit
    as well [R10].
  - *P. sylvestris* elevation gradient, Catalonia, 8 years: "the main driver of
    variation was late-summer–early-autumn precipitation" [R11].
- Tuscan chestnut coppices: "summer 1998 was particularly hot and dry, penalizing all
  species that fruit after the first rains, such as many saprotrophs" [R4].
- Lore pulls the other way for ovoli: it fruits after "un periodo di caldo costante con
  conseguente essiccamento della terra" (a spell of steady heat that dries the soil),
  if a storm follows [R22].
- **Open-Meteo climatology (2016–2025, local days) [R16].** Four Tuscan points: Montagnola
  Senese (grid 463 m), Colline Metallifere (499 m), Serchio valley near Garfagnana (209 m),
  Livorno hills (259 m).
  - **July–August:** rain 0.7–2.6 mm/day at the three southern and coastal points
    (about 20–80 mm per 30 days; Serchio valley 1.3–3.6 mm/day). ET0 4.1–5.7 mm/day.
    Soil moisture 0–7 cm 0.12–0.18 m³/m³.
  - **Second half of Sept–October (peak sightings):** rain 2.5–4.5 mm/day at the same
    three points (about 75–135 mm per 30 days; Serchio valley 6.2–10.4 mm/day). ET0
    1.5–3.2 mm/day. Soil moisture 0.23–0.31 m³/m³.

**Numbers and confidence**

- **OVO-07 (derived):** mean 0–7 cm soil moisture over the 7 days after the trigger,
  0 at ≤ 0.15, 1 at ≥ 0.22 m³/m³. Chosen so that typical dry-summer topsoil
  (0.12–0.18) scores 0–0.4 and typical peak-season topsoil (0.23–0.31) scores 1 [R16]. It encodes "the soil stays wet for a
  few days" [R24]. ERA5-Land moisture is model-scaled, so tune it in the backtest.
  **Plausible.**
- **OVO-08 (derived):** 30-day rain, 0 at ≤ 25 mm, 1 at ≥ 75 mm. The factor comes from
  [R3]; the edges come from the climatology above (dry-summer vs peak-season 30-day
  totals). **Plausible**, extrapolated from all macrofungi. It overlaps OVO-05/06:
  test "lagged event" vs "30-day sum" as alternatives, not both at full weight.
- **OVO-09 (derived):** spring (Mar–May) rain vs local normal as a weak multiplier
  (0.8 at ≤ 60 %, 1.0 at ≥ 100 %). **Plausible** [R3], community-level only.
- **No summer-drought legacy penalty for ovoli in v1.** The community-level evidence
  [R4] and the ovoli lore [R22] conflict. Current soil moisture (OVO-07) already
  captures the drought that matters. Flag it for the backtest.

### Temperature

**What sources say**

- **Lab (label: lab evidence).** Mycelium of Spanish isolates grew best at pH 6–7 with
  "optimal growth temperature 24–28 °C depending on the isolate" [R5]. This is radial
  growth in culture, not fruiting and not soil temperature. It supports the thermophilic
  label and suggests warm summer soils are not harmful to the mycelium.
- Thermophilic and heliophilous in every ecological summary [R6, R7 (warm habitats),
  R8 ("light and warm"), R17, R18, R19, R22]. Does not tolerate cold or cool
  temperatures (lore) [R22]. Cold soil prevents fruiting (generic guide) [R25].
- **No field study gives a soil or air temperature band for ovoli fruiting.** No source
  consulted reports a "thermal shock" (temperature-drop) trigger for ovoli. The Italian
  thermal-shock lore seen in search results is written about porcini.
- **Climatology over the observed season (derived) [R16].** Mean 0–7 cm soil temperature
  by half-month, range across the four Tuscan points:

  | half-month | soil 0–7 cm (°C) | Tmin (°C) | Tmean (°C) | sightings context |
  |---|---|---|---|---|
  | Jul 1–15 | 24.2–24.8 | 17.6–19.0 | 23.3–23.6 | rare summer flushes |
  | Aug 16–31 | 24.3–24.4 | 17.8–19.6 | 23.2–23.6 | Tuscan p5–p10 |
  | Sep 16–30 | 18.2–19.4 | 12.9–15.5 | 17.3–18.8 | p25 region |
  | Oct 1–15 | 15.4–16.8 | 10.4–13.2 | 14.8–16.4 | Tuscan p50 (13-10) |
  | Oct 16–31 | 14.4–16.0 | 10.1–12.9 | 14.1–15.9 | p75–p90 |
  | Nov 1–15 | 11.1–13.1 | 6.9–10.3 | 10.6–12.9 | p95 and tail |
  | Nov 16–30 | 8.1–10.5 | 4.2–7.6 | 7.8–10.3 | last records (to 21-11) |

**Numbers and confidence**

- **OVO-10 (derived):** 0–7 cm soil temperature, mean over the lag window (trigger day
  to score day): `[9, 14, 26, 32]` °C.
  - Lower edges: the bulk of Tuscan records falls at 14–16 °C half-month means; the
    tail runs through 11–13 °C and ends near 8–10 °C.
  - Upper edges (26 → full, 32 → zero) are **placeholders**. July–August records exist
    at 24–26 °C means, and the lab optimum is 24–28 °C. No source says heat stops
    fruiting when the soil is moist.
  - Evaluating over the lag window means the trigger rain must fall while the soil is
    still warm, which is the "warm soil after rain" of the hypothesis.
  - **Plausible**, but all numbers are derived.
- **OVO-11 (derived):** 2 m Tmean 7-day mean `[8, 13, 25, 30]` °C, from the same table
  (Tmean runs ~0.5–1 °C below the 0–7 cm soil mean in this season). Use it only if soil
  temperature is dropped. The 7–28 cm layer runs 0.5–1 °C warmer than 0–7 cm in autumn
  [R16]; if the engine prefers it, shift the band up by 1 °C.
- **Thermal shock: no source found for ovoli.** Do not encode.

### Stoppers

- **Cold nights (OVO-12, derived).** 7-day mean Tmin: multiplier 0 at ≤ 5 °C, 1 at
  ≥ 10 °C. Sightings thin out when half-month Tmin falls from 10–13 °C (late Oct) to
  7–10 °C (early Nov), and stop at 4–8 °C (late Nov) [R14, R16]. "Does not tolerate
  cold" [R22]; a Tuscan season "to November" [R21]. **Plausible.** It overlaps OVO-10;
  weight one of them lower.
- **Frost (OVO-13, derived).** Any Tmin ≤ 0 °C in the previous 7 days → 0. No
  ovoli-specific source. In the low Tuscan hills first frosts mostly come after the
  window, so impact should be small. **Folklore / generic.**
- **Drought after the storm / evaporative demand (OVO-14, derived).** ET0 7-day mean
  after the trigger: 1 at ≤ 4 mm/day, 0.4 at ≥ 6 mm/day.
  - In a Mediterranean pine stand, "increased atmospheric evaporative demand … might
    lead to a drop in fungal yields"; water-balance models outperformed rain-only models
    under warming [R10]. This is an extrapolation to oak/chestnut and to ovoli.
  - July–August ET0 in Tuscany is 4.1–5.7 mm/day; peak season is 1.5–3.2 [R16].
  - **Plausible.** It overlaps OVO-07 (soil moisture); keep one at full weight.
- **Drying wind (OVO-15, derived).** A few hours of dry downslope wind can take the air
  near the ground from nearly saturated to 20–30 % RH and cancel the rain within 48 h
  (lore, written about foehn winds in Piedmont and the Aosta valley) [R24]. The Tuscan
  equivalents would be tramontana/grecale outbreaks. Gust ≥ 40 km/h and RH ≤ 35 % are
  **derived** placeholders. **Folklore**; no ovoli-specific source.
- **Heat.** Not a stopper by itself for this species; see OVO-10 upper edges. VPD is
  not separately encoded (it overlaps ET0).
- **Waterlogging (OVO-16).** Well-drained soils [R8]; water must drain without pooling
  [R22]; waterlogging prevents fruiting [R25]. Threshold **derived**. **Folklore**, low
  priority.
- **Irregular fruiting.** In Spanish oak woods it can be absent for years (popular
  sources; `snippet-only`, not cited as a rule). Long-term Bulgarian observations show
  fewer fruit bodies over 10–30 years [R8]. Not encodable; it will show up as noise in
  the backtest.

### Not modellable in v1

- **Soil substrate / pH (OVO-17).**
  - Lab optimum pH 6–7 [R5]. Summarised as silicicolous, on slightly acid soils
    (pH ~6–6.5) [R6]. Spanish lore: siliceous soils, avoids limestone [R23].
    Acid-to-slightly-acid (generic guide) [R25].
  - Against: Italian popular sources say it grows on acid and carbonate-rich soils
    (`snippet-only`). The Tuscan plot data are the only field test: absent from all
    four calcicolous oak plots (pH 6.8–7.4) [R2], present on sandstone [R1]. Too few
    plots to conclude.
  - **Flag for SoilGrids / Regione Toscana soil map** if the backtest shows
    limestone-area oak cells over-predicting (e.g. Montagnola Senese).
- **Canopy openness, clearings, edges (OVO-18).** Consistently described as favouring
  light: well-lit clearings, "heliófila" (sun-loving) [R6]; sunny clearings [R18];
  "light and warm" forests [R8]; open oak woods, clearings, logged areas, sparse
  understorey [R21]. Needs canopy cover (e.g. Copernicus tree-cover density) → future
  modifier.
- **Management / abandonment.**
  - Declined where silviculture was abandoned; cleared fruit-chestnut groves favoured
    (Tuscan lore) [R21].
  - Benefits from shallow soil working as in chestnut plantations (Spanish summary
    citing Daza et al. 2006) [R6].
  - Forestry-related threats and intensification [R7]; selective logging, plantations
    and fires listed as threats in Bulgaria [R8].
  - Management history is not in v1 data.
- **Fire / recent disturbance (OVO-19).** Appears in areas that have burnt (Tuscan lore)
  [R21], while fires are a threat in [R8]. Contradictory and unencodable.
- **Nitrogen deposition and fertilisation.** Main European threats [R7]. Not in v1.
- **Stand age, litter depth.** Grows where organic matter is not abundant (Spanish
  summary) [R6]. No data in v1.
- **Understorey indicators** (*Erica*, *Calluna*, *Cistus*, *Arbutus*) [R6, R19, R21].
  They indicate open, acid, sunny stands. Not in the forest-type layer.

## Disagreements and open questions

1. **Season peak.**
   - "July–October" (card hypothesis) and "peak August" [R25] vs Tuscan data: the
     median record is 13 Oct and only ~10 % of records fall in June–August [R14, R15].
   - SW Spain is later still (October to mid-November) [R6].
   - Open: is the Tuscan autumn peak driven by the return of rain (moisture) or by
     cooling? The ovoli lore says warmth; the backtest can test a cooling term.
2. **Rain amount.** 15–20 mm per episode (Spain, [R23]) vs 30–50 mm summer storms
   (Italy, [R24]). Probably both are right at different ET0 (autumn vs summer), which is
   why OVO-07/OVO-14 carry the drying side.
3. **Lag.** 18–22 days for ovoli [R23] vs 8–11 days in warm weather (stated for
   thermophilic porcini and generic summer fungi, [R24]). Test two lag trapezoids.
4. **Soil chemistry.** Siliceous/acid preference [R6, R23] vs "acid and calcareous"
   (popular Italian sources, `snippet-only`). Tuscan calcicolous oak plots had none [R2].
5. **Aspect.** South-facing lore [R18, R23] vs the only Tuscan plot record facing NE
   [R1].
6. **Evergreen oak vs deciduous oak.** Confirmed hosts [R5, R7], yet rare in Tuscan
   holm-oak plots [R1, R2]. The Maremma/Livorno sighting cluster cannot resolve this at
   1 km.
7. **Beech.** A listed host [R7, R8] vs "not in beech woods" [R25]. Irrelevant in
   Tuscany once altitude is applied.
8. **Summer heat before rain.** A priming effect (lore, [R22]) vs community-level
   penalty [R4]. Not encoded; test it.
9. **Circularity.** Season and altitude numbers use Italian and Tuscan sightings from all
   years. Before tuning, re-derive them on train seasons only, and never on the hold-out
   seasons.
10. **Tiny validation sample.** 35 unique observer-days in Tuscany (GBIF), 50 iNat
    observations, concentrated in two provinces and 2019–2025. Expect wide confidence
    intervals for ovoli lift/AUC. Consider testing rule *shape* on central-Italy or
    Italy-wide records (Italy only, never the global key) while keeping Tuscany for the
    final hold-out.
11. **Leads not confirmed.**
    - "Daza et al. 2007": no 2007 *A. caesarea* paper by that team was found; its 2008
      papers are on *A. ponderosa*.
    - Baptista et al. 2010: full text not accessible, so no species-level result
      verified [R9].
    - Salerni et al. 2002: abstract only [R3].
    - No Spanish or Portuguese *Q. pyrenaica* or chestnut study with *A. caesarea* yield
      or phenology series was found.
    - AMB / *Rivista di Micologia* ovolo phenology notes were not found online.
12. **Upper temperature limits** (OVO-10/11) are unsourced placeholders.

## References

- [R1] Laganà A., Salerni E., Barluzzi C., De Dominicis V., Perini C. (2002). Fungi
  (Macromycetes) in various types of Mediterranean forest ecosystems (Tuscany, Italy).
  *Polish Botanical Journal* 47(2): 143–165.
  https://archive.org/details/polish-botanical-journal-47-002-143-165 `verified` (full
  text; Table 1, Table 2 p. 155 and the Periodicity section read). Supports: the only
  record in chestnut coppice St. 6 (550 m, NE, sandstone); absence from holm-oak and fir
  plots; autumn-limited fruiting in the hill belt; July–August drought as critical on
  the coast.
- [R2] Laganà A., Salerni E., Barluzzi C., Perini C., De Dominicis V. (1999).
  Mycocoenological studies in Mediterranean forest ecosystems: calcicolous deciduous oak
  woods of central-southern Tuscany (Italy). *Czech Mycology* 52(1): 1–16.
  https://czechmycology.org/_cm/CM52101.pdf `verified` (full text; Table 1 p. 9 read).
  Supports: presence in 1/10 evergreen-oak and 1/9 chestnut plots, 0/4 calcicolous
  deciduous-oak plots (pH 6.8–7.4); summer sampling gaps.
- [R3] Salerni E., Laganà A., Perini C., Loppi S., De Dominicis V. (2002). Effects of
  temperature and rainfall on fruiting of macrofungi in oak forests of the Mediterranean
  area. *Israel Journal of Plant Sciences* 50(3): 189–198.
  https://doi.org/10.1560/GV8J-VPKL-UV98-WVU1 `verified` (abstract only, via
  OpenAlex/Crossref). Supports: 30-day rainfall correlation, annual and spring rainfall
  effects (all macrofungi, Tuscan oak forests).
- [R4] Laganà A., Salerni E., Barluzzi C., Perini C., De Dominicis V. (2002). Macrofungi
  as long-term indicators of forest health and management in central Italy.
  *Cryptogamie, Mycologie* 23(1): 39–50.
  https://sciencepress.mnhn.fr/sites/default/files/articles/pdf/cryptogamie-mycologie2002v23f1a5.pdf
  `verified` (full text). Supports: the hot, dry summer of 1998 penalised species
  fruiting after the first rains (community-level).
- [R5] Daza A., Manjón J.L., Camacho M., Romero de la Osa L., Aguilar A., Santamaría C.
  (2006). Effect of carbon and nitrogen sources, pH and temperature on in vitro culture
  of several isolates of *Amanita caesarea* (Scop.:Fr.) Pers. *Mycorrhiza* 16(2):
  133–136. https://doi.org/10.1007/s00572-005-0025-6 `verified` (abstract, PubMed
  16292570). Supports (**lab**): optimum pH 6–7 and 24–28 °C for mycelial growth;
  isolates from *Q. suber* and *C. sativa* in SW Spain. The introduction's phenology
  statement is `snippet-only` (seen via R6 and a search snippet).
- [R6] Cano Cajigas J.M. (2015). *Respuesta molecular de Amanita caesarea (Scop.:Fr.)
  Pers. frente a distintas cepas rizobacterianas.* Proyecto Fin de Carrera, Universidad
  Politécnica de Madrid. https://oa.upm.es/38108/7/PFC_JOSE_MARIA_CANO_CAJIGAS.pdf
  `verified` (full text, pp. 17–18). Secondary source (undergraduate thesis) citing
  Daza et al. 2006. Supports: silicicolous, heliophilous, thermophilous ecology;
  clearings with heath and *Cistus*; host list; SW Spain October to mid-November with
  occasional spring–summer fruiting; pH ~6–6.5; benefit of shallow soil working.
- [R7] Gonçalves S.C. (2019). *Amanita caesarea*. The IUCN Red List of Threatened
  Species 2019: e.T125433663A125435485.
  https://doi.org/10.2305/IUCN.UK.2019-3.RLTS.T125433663A125435485.en (read via the
  Global Fungal Red List page https://redlist.info/iucn/species_view/208468) `verified`.
  Supports: native range, hosts, habitats, "only seldom above 1200 m", threats.
- [R8] Gyosheva M. *Amanita caesarea*. In: *Red Data Book of the Republic of Bulgaria*,
  Vol. 1 (Plants and Fungi). http://e-ecodb.bas.bg/rdb/en/vol1/Amacaesa.html `verified`.
  Supports: fruiting June–October; light, warm oak and mixed deciduous forests on
  drained soils; long-term decline; threats.
- [R9] Baptista P., Martins A., Tavares R.M., Lino-Neto T. (2010). Diversity and fruiting
  pattern of macrofungi associated with chestnut (*Castanea sativa*) in the
  Trás-os-Montes region (Northeast Portugal). *Fungal Ecology* 3(1): 9–19.
  https://doi.org/10.1016/j.funeco.2009.06.002 `snippet-only` (metadata verified via
  Crossref; abstract and full text not accessible). Supports: only the general
  statement that fruiting in a chestnut orchard fluctuated with rainfall.
- [R10] Ágreda T., Águeda B., Olano J.M., Vicente-Serrano S.M., Fernández-Toirán M.
  (2015). Increased evapotranspiration demand in a Mediterranean climate might cause a
  decline in fungal yields under global warming. *Global Change Biology* 21(9):
  3499–3510. https://doi.org/10.1111/gcb.12960 `verified` (abstract). Supports:
  water-balance / evaporative-demand control of Mediterranean ectomycorrhizal yields
  (pine forest; extrapolated).
- [R11] Alday J.G., Martínez de Aragón J., de-Miguel S., Bonet J.A. (2017). Mushroom
  biomass and diversity are driven by different spatio-temporal scales along
  Mediterranean elevation gradients. *Scientific Reports* 7: 45824.
  https://doi.org/10.1038/srep45824 `verified` (abstract). Supports: late-summer to
  early-autumn precipitation as main driver (pine forest; extrapolated).
- [R12] Andrew C., Heegaard E., Høiland K., et al. (2018). Explaining European fungal
  fruiting phenology with climate variability. *Ecology* 99(6): 1306–1315.
  https://doi.org/10.1002/ecy.2237 `verified` (abstract). Supports: altitude shifts
  autumn fruiting earlier by up to 30 days (all fungi, central/northern Europe).
- [R13] Kodaira M., et al. (2024). *Amanita satotamagotake* sp. nov., a cryptic species
  formerly included in *Amanita caesareoides*. *Mycoscience* 65(2): 49–67.
  https://doi.org/10.47371/mycosci.2023.12.001 `verified` (PMC11369313). Supports:
  sect. *Caesareae* taxonomy; *A. jacksonii* is North American; East Asian taxa once
  called *A. caesarea*.
- [R14] GBIF.org occurrence and species APIs, *Amanita caesarea* taxonKey 5240269,
  accessed 2026-09-17: https://api.gbif.org/v1/occurrence/search?taxonKey=5240269&country=IT
  and https://api.gbif.org/v1/species/5240269/synonyms `verified` (data queried
  directly). Supports: synonyms, country counts (incl. US/MX misapplications), Italian
  and Tuscan month and day-of-year distributions, elevation sample (coordinates used
  only for aggregates). Per-dataset citation (iNaturalist research-grade and others)
  needed if published.
- [R15] iNaturalist API, taxon 204588, places 13073 (Toscana) and 6973 (Italy),
  month-of-year, week-of-year and year histograms, accessed 2026-09-17:
  https://api.inaturalist.org/v1/observations/histogram?taxon_id=204588&place_id=13073&date_field=observed&interval=month_of_year
  `verified` (data queried directly). Supports: Tuscan and Italian month counts; record
  volume.
- [R16] Open-Meteo Historical Weather API (ERA5/ERA5-Land "best match"), daily 2016–2025,
  `timezone=Europe/Rome`, points 43.28N 11.20E; 43.02N 11.10E; 44.08N 10.45E;
  43.47N 10.42E (grid elevations 463, 499, 209, 259 m), variables: soil temperature
  0–7/7–28 cm, Tmin, Tmean, precipitation, soil moisture 0–7 cm, ET0;
  https://archive-api.open-meteo.com/v1/archive . Open-Meteo Elevation API (Copernicus
  DEM GLO-90) for record elevations. `verified` (data queried directly). Supports: all
  climatology-derived thresholds.
- [R17] Curti P. (rev. Cittadini M.). Scheda *Amanita caesarea*. AMINT – Funghi Italiani.
  https://www.funghiitaliani.it/Amanite/schede%20funghi/caesarea/Amanita%20caesarea.htm
  `verified`. Supports: warm, dry zones; under chestnut and Turkey oak; up to 900 m;
  summer–autumn.
- [R18] InNatura (content credited to AMINT). Ovolo buono.
  https://www.innatura.info/amanita-caesarea-2/ `verified`. Supports: south-facing sunny
  clearings; up to 900 m; summer–autumn; uncommon in northern Italy.
- [R19] Sardegna Foreste (Agenzia Forestas, Regione Sardegna). *Amanita caesarea*.
  https://www.sardegnaforeste.it/fungo/amanita-caesarea `verified`. Supports: warm
  broadleaf woods (*Castanea*, *Quercus*), often with *Arbutus* and *Erica*.
- [R20] Gruppo Micologico Naturalistico Ancona. Scheda *Amanita caesarea*.
  https://www.gruppomicologicoancona.it/micologia/ritrovamenti-e-schede/schede-descrittive/amanita-caesarea.html
  `verified`. Supports: warm climates; broadleaf woods in summer–autumn; chestnut–oak
  record (Monti Sibillini, 30 Sep 2012).
- [R21] "Angiolo" (2020-04-11). Repetita(?) juvant 4 – Ovolo e alcune Amanite. *Funghi in
  Toscana* (blog). https://funghintoscana.blogspot.com/2020/04/repetita-juvant-4-ovolo-e-alcune.html
  `verified`. **Folklore / local lore.** Supports: Tuscany mid-May to November, up to
  1000 m; open woods, clearings, burnt areas, cleared fruit-chestnut groves, *Erica*;
  decline with abandonment.
- [R22] Funghi Magazine. *Amanita caesarea* – Ovolo buono.
  https://funghimagazine.it/amanita-caesarea-ovolo-buono-funghi-commestibili/ `verified`.
  **Folklore.** Supports: June–October; fruits after steady heat; storm water must drain;
  regional altitude limits (NW ~500 m, NE ~600 m, Apennines ~1000 m, south 1200 m);
  hosts.
- [R23] Martínez P. *Amanita caesarea*, oronja placer del César. *La Casa de las Setas*
  (blog). https://lacasadelassetas.com/blog/amanita-caesarea-oronja-placer-del-cesar/
  `verified`. **Folklore.** Supports: rain episodes of 15–20 l/m²; 18–22 days lag;
  S/SE-facing sunny clearings; siliceous soils.
- [R24] Oppicelli N. (2026-07-01). Funghi a luglio: il segreto è leggere pioggia e vento.
  *Passione Funghi* – 3BMeteo. https://funghi.3bmeteo.com/funghi-a-luglio/ `verified`.
  **Folklore** (meteorologist's column, no data). Supports: 30–50 mm summer storms plus
  soil staying wet → sudden *A. caesarea* and *B. aereus* emergences in the Tyrrhenian
  hills of central Italy; 10–15 mm storms insufficient (generic); lags of 8–11 d in warm
  conditions (thermophilic porcini) to 15–20 d with cool nights (generic); dry downslope
  winds cancel rain within 48 h.
- [R25] MyBoletus. Ovoli (*Amanita caesarea*): guida per trovare il fungo dei re.
  https://myboletus.com/it/funghi/ovoli/ `verified`. **Folklore / commercial.** Supports:
  July–September peak August (Italy-wide); 200–900 m; not in beech woods; acid,
  well-drained soils; waterlogging and cold soil unfavourable; shaded aspects delay it.
