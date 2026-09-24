# Gallinacci / finferli: *Cantharellus cibarius* s.l. (evidence appendix to species-ecology.md)

Research date: 2026-09-17. Scope: Tuscany. Research only, no code. This page covers conditions
only. It says nothing about edibility or how to identify specimens.

**Headline findings**

1. **The Tuscan "*C. cibarius*" is mostly not *C. cibarius* sensu stricto.** The current European
   revision says *C. cibarius* s.str. is absent from areas with a Mediterranean climate [R1]. In
   Tuscany the name covers a group: *C. pallens* (= *C. subpruinosus*), which prefers acid soils,
   *C. alborufescens*, which grows under evergreen oaks on limestone, and smaller shares of
   *C. ferruginascens* and *C. amethysteus*. The rules should target *C. cibarius* **s.l.**
2. **Acid soil is a real preference, but it is not an absolute rule for the group.** The
   acidophilous members prefer pH about 4.0–5.5 [R2]. The Tuscan group still occurs, rarely, on
   calcareous soil at pH 6.8–7.4 [R3], and one member prefers limestone [R1]. The best Tuscan
   plot data show about **10× lower abundance in calcicolous oak woods than in chestnut coppice**
   [R3], but host tree and substrate are confounded there (derived; see "Soil pH: known gap").
3. **Chestnut is the strongest habitat signal in Tuscany.** The group was present in 9/9
   chestnut-coppice plots, 5/10 evergreen-oak plots, 2/7 fir plots and 1/4 calcicolous oak plots
   [R3]. Chestnut does not thrive on limestone [R17], so a chestnut habitat class already stands
   in for acid soil in v1.
4. **Fruiting follows moisture over weeks, not single storms, and fruit bodies last a long
   time.** The best-supported rain window in Tuscany is the **30 days** before a count [R4]. In
   Finland, June–July rainfall drives the July–August chanterelle supply [R8]. Fruit bodies last
   **44 days on average**, sometimes more than 90 days [R2] (Pacific chanterelle, extrapolated).
   The hypothesis on the card is **confirmed** on these points.
5. **No chanterelle-specific numbers were found** for soil temperature, frost, drying wind or
   rain-to-fruiting lag in a Mediterranean climate. Those rules below are **derived** and have low
   confidence.
6. **Validation data are thin.** Tuscany has **116** verifiable iNaturalist records of
   *Cantharellus* and **48** GBIF records (genus level) [R25, R26]. Per-season backtests will be
   noisy, so pool the seasons.

---

## Scope and taxonomy notes

### What the common name covers

In Italy "gallinaccio", "finferlo" and "galletto" name the yellow-orange *Cantharellus* as a
group. Italian popular sources list "*C. cibarius*" from alpine fir woods to coastal pinewoods
[R30, R31]. After the multigene revision [R1], Europe has **eight** *Cantharellus* species:
*C. alborufescens*, *C. amethysteus*, *C. cibarius*, *C. ferruginascens*, *C. friesii*,
*C. pallens*, *C. roseofagetorum* (known from Georgia only) and *C. romagnesianus*. The revision
also proposes 16 synonyms [R1]. The ones that matter for the data are:

| accepted name [R1] | synonyms that matter for records [R1] | ecology per [R1] (verified) |
|---|---|---|
| *C. cibarius* | *C. cibarius* var. *atlanticus*, *C. parviluteus* | "broadly distributed in Europe, but not present in areas with Mediterranean climate". In the Iberian Peninsula "and probably elsewhere in South Europe" it has "a clear preference for acid soils and occurs in rainy or locally damp sites". Hosts are angiosperms or gymnosperms; the Spanish specimens came from under *Pinus sylvestris*, *Fagus*, *Castanea*, *Quercus robur* and *Betula*. |
| *C. pallens* | **= *C. subpruinosus***, *C. cibarius* var. *albidus*, var. *bicolor* | Widespread in the Mediterranean area. "Markedly acidophilous in the Mediterranean area" but on rich ground in Fennoscandia. The Italian specimens include Riciano (Monteriggioni, SI) in *Quercus cerris* + *Q. ilex* woodland, 9 Nov 2012. |
| *C. alborufescens* | *C. ilicis*, *C. henrici*, *C. lilacinopruinatus* | "Almost exclusively occurring in Mediterranean evergreen *Quercus* forests on calcareous soil", with one collection under *Castanea*. The Italian specimens include Fonte Murata (SI) in *Q. cerris* + *Q. ilex* woodland, 9 Nov 2012, and Molli (Sovicille, SI) at 500 m with *Castanea sativa*, 10 Nov 2012. |
| *C. ferruginascens* | *C. cibarius* var. *flavipes* | Temperate climates without summer drought, under deciduous Fagaceae and *Carpinus* **on calcareous soil**. The few Mediterranean sites are locally moist, under *Q. suber* **on acid ground**, so it "appears to switch its soil pH preference" in the Mediterranean. |
| *C. amethysteus* | *C. cibarius* var. *amethysteus*, *C. rufipes*, var. *umbrinus* | "Not present in areas of Mediterranean climate with summer drought". |
| *C. friesii*, *C. romagnesianus* | — | Different subgenera. No Tuscan records in GBIF or iNaturalist [R25, R26]. |

*C. roseofagetorum* is not relevant to Tuscany.

Two statements in [R1] hold for the whole group: **host specificity is low or absent** (for
example, *C. cibarius*, *C. pallens* and *C. amethysteus* each occur in pure angiosperm or pure
gymnosperm stands), and **climate, not host, seems to separate *C. alborufescens* from
*C. ferruginascens***.

### How records get lumped

- **GBIF backbone** (queried 2026-09-17 [R25]). *C. pallens*, *C. alborufescens*,
  *C. ferruginascens* and *C. amethysteus* are **separate accepted species**.
  *C. subpruinosus* → synonym of *C. pallens*; *C. ilicis* → *C. alborufescens*;
  *C. cibarius* var. *amethysteus* → *C. amethysteus*. So the backbone does not fold the
  segregates into *C. cibarius*. **Lumping happens at identification**: observers give the
  familiar name to any chanterelle, and older surveys used the broad pre-2000 concept (for
  example "Cantharellus cibarius Fr.: Fr." in the Siena plot tables [R3]).
- **Tuscan counts.** GBIF with `gadmGid=ITA.16_1` has 48 records of genus *Cantharellus*:
  *C. cibarius* 23 (22 from iNaturalist research grade and 1 preserved specimen), *C. pallens*
  12 (one filed as *C. subpruinosus*), *C. alborufescens* 4, *C. ferruginascens* 3,
  *C. melanoxeros* 3 and *C. cinereus* 3 [R25]. iNaturalist (place 13073, verifiable) has 116:
  *C. cibarius* 43, *C. pallens* 27, genus only 34, and 12 other segregates (*C. ferruginascens*
  4, *C. alborufescens* incl. forms 6, *C. amethysteus* 2) [R26].
- **Probable make-up of Tuscan "*C. cibarius*" records.** *C. cibarius* s.str. is said to be
  absent under a Mediterranean climate [R1]. Tuscan records labelled *C. cibarius* sit at a median
  **302 m**, and 22 of 43 are from October [R26]. So most of them are **probably *C. pallens*
  and *C. alborufescens***, possibly with some *C. ferruginascens*. Some *C. cibarius* s.str. may
  occur in the temperate Apennine and Amiata belt, but I found **no sequenced Tuscan
  specimen**: the Italian material in [R1] is *C. pallens* and *C. alborufescens* from Siena
  province plus northern Italian collections. This is an inference, not verified record by record.
- **Records under *Cantharellus* that are not gallinacci.** The GBIF backbone keeps
  *C. cinereus* and *C. melanoxeros* in *Cantharellus* [R25] (iNaturalist files them under
  *Craterellus*). **Exclude them**, along with *Craterellus* and *Hygrophoropsis*, from the
  gallinacci validation set.

### Recommendation

- **Target *C. cibarius* s.l.** = {*C. cibarius*, *C. pallens* (incl. *subpruinosus*),
  *C. alborufescens* (incl. *ilicis*, *lilacinopruinatus*), *C. ferruginascens*,
  *C. amethysteus*} plus genus-level *Cantharellus* records. Use one rule set. The data cannot
  support separate taxa: the largest segregate has 27 Tuscan records.
- **Possible v2 split**, noted only. A "Mediterranean" group (*C. pallens*, *C. alborufescens*)
  would cover low to mid elevation, oaks, chestnut and pines, and fruit in autumn, early winter
  and spring. A "temperate" group (*C. cibarius* s.str., *C. amethysteus*, *C. ferruginascens*)
  would cover beech and fir and fruit in summer and autumn. Soil pH works in **opposite
  directions** for *C. pallens* and *C. alborufescens*, so a pH rule for the s.l. target must be
  softened (see "Soil pH: known gap").

---

## Rules summary

Trapezoids: season `[zero_before, full_from, full_to, zero_after]` in `DD-MM`; altitude
`[zero_below, full_from, full_to, zero_above]` in m; other bands `[zero_below, full_from, full_to,
zero_above]` in their stated units. "×k" is a multiplier on the score. The `data` column says
whether the inputs are **available** (Open-Meteo or static per cell), **derived** (computed from
available inputs, such as GDD, P−ET0 or percentiles) or **missing** in v1. A number marked
**(derived)** came from a qualitative statement or from another climate; see the notes under
"Evidence by factor".

| id | taxon | factor | rule (plain words) | parameters | confidence | sources | data |
|---|---|---|---|---|---|---|---|
| GAL-01 | s.l. | scope | Score the gallinacci as one group. Build the validation set from the listed taxa and exclude look-alike genera and *C. cinereus* / *C. melanoxeros*. | include: *C. cibarius*, *C. pallens* (+*subpruinosus*), *C. alborufescens* (+*ilicis*, *lilacinopruinatus*), *C. ferruginascens*, *C. amethysteus*, *Cantharellus* sp.; exclude: *Craterellus* spp., *C. cinereus*, *C. melanoxeros*, *Hygrophoropsis* | strong | R1, R25, R26 | available |
| GAL-02 | s.l. | season (below 600 m) | A long, permissive window from spring to early winter. Let the moisture and heat rules make the summer gap, because rainy summers do produce fruiting. | `[15-04, 10-05, 15-12, 25-01]` (wraps past year end) **(derived)** | plausible | R1, R26, R28, R30, R31 | available |
| GAL-03 | s.l. | season (above 1000 m) | One summer–autumn window. Blend GAL-02 and GAL-03 linearly between 600 and 1000 m. | `[01-06, 01-07, 15-10, 15-11]` **(derived)** | folklore→plausible | R26, R30, R31, R32 | available |
| GAL-04 | s.l. | season, alternative | Two-flush variant, kept only to compare against GAL-02 in the backtest. | spring `[15-04, 10-05, 30-06, 31-07]`; autumn `[20-08, 20-09, 15-12, 25-01]` **(derived)** | folklore | R26, R28, R31 | available |
| GAL-05 | s.l. | habitat | Affinity by forest class, with chestnut highest. | chestnut 1.0; evergreen_oak 0.7; beech 0.7; fir_spruce 0.6; mixed_broadleaf_conifer 0.6; deciduous_oak 0.5; mediterranean_pine 0.5; mountain_pine 0.4; mixed_broadleaf 0.3; macchia 0.3; other_conifer 0.2; riparian 0.1; exotic_broadleaf 0.0 **(derived)** | plausible (chestnut: strong) | R1, R2, R3, R17, R18, R19, R20, R28, R30, R31 | available |
| GAL-06 | s.l. | altitude | Full from the coast to about 1000 m, fading out towards the top of the beech belt. | `[0, 0, 1000, 1700]` m **(derived)** | plausible | R3, R26, R29, R31, R32 | available |
| GAL-07 | s.l. | aspect (optional) | Below 600 m from June to September, give moister north- and east-facing slopes a slight edge, but flat and less-exposed ground is normal for Tuscan woodland and keeps full credit; only clearly sunny slopes lose it. | N/NE/E and flatter ×1.0 (normal terrain, full credit), S/SW/W ~×0.85 **(derived)** | folklore | R1 (moist-site preference), R32 | available |
| GAL-08 | s.l. | antecedent rain (30 d) | Fruiting needs a wet month. Score rises with rainfall over the previous 30 days. | P30 ramp: 0 at ≤ 15 mm, 1 at ≥ 70 mm **(derived)** | plausible | R4, R5, R6, R8 | derived |
| GAL-09 | s.l. | rain frequency | Several rain events matter more than one storm. | days with P ≥ 5 mm in the last 20 d: 0 → ×0.3; 1 → ×0.6; 2 → ×0.85; ≥ 3 → ×1.0 **(derived)** | plausible (R27) / folklore (R30) | R27, R30 | derived |
| GAL-10 | s.l. | lag after wetting | Fruit bodies appear about 1–2 weeks after a wetting event and last for weeks. The long tail encodes that persistence. | wetting event = P ≥ 20 mm within ≤ 3 d; lag trapezoid `[4, 10, 30, 50]` days **(derived)** | plausible | R2, R7, R9, R27, R31 | derived |
| GAL-11 | s.l. | soil moisture | Topsoil must stay moist. The mycelium lives in the upper 5–10 cm. | 7-day mean volumetric moisture, 0–7 cm (weight 0.6) and 7–28 cm (0.4). Ramp against the cell's own climatology for that month: 0 at ≤ p15, 1 at ≥ p40 **(derived)** | plausible | R2, R8 | derived |
| GAL-12 | s.l. | season-scale water balance | A dry preceding two months damps the whole flush. Spring rain helps autumn fruiting. | Σ(P − ET0) over 60 d: ×0.5 at ≤ −150 mm, ×1.0 at ≥ −30 mm **(derived)** | plausible | R4, R5, R8 | derived |
| GAL-13 | s.l. | soil temperature | A wide, cool-to-mild band. Lowland fruiting runs into December. | 0–7 cm, 7-day mean: `[5, 9, 20, 25]` °C **(derived)** | folklore/plausible (lab data only) | R10, R11, R26, R30 | available |
| GAL-14 | s.l. | air temperature (fallback) | Use only if soil temperature is not used. | Tmean, 7-day mean: `[4, 8, 21, 26]` °C **(derived)** | folklore | R10, R11, R30 | available |
| GAL-15 | s.l. | spring warmth gate (optional) | The spring window opens only after enough warmth has built up. This only binds at high elevation in Tuscany. | growing degree-days, base 5 °C, summed from 1 Jan: ≥ 430 °C·d (lower bound of 500 ± 70) | plausible (boreal, extrapolated) | R6 | derived |
| GAL-16 | s.l. | stopper: frost | Hard or repeated frost ends new fruiting. | Tmin ≤ −2 °C on ≥ 2 of the last 7 nights → ×0.3 for 10 d; any Tmin ≤ −5 °C or snowfall ≥ 5 cm in 3 d → ×0 for 10 d **(derived)** | folklore | R9 (qualitative) | available |
| GAL-17 | s.l. | stopper: drought | Two dry, high-evaporation weeks suppress fruiting. Floored at ×0.2 because fruit bodies persist and the Mediterranean segregates tolerate summer drought. | if P14 < 10 mm: Σ(P − ET0) over 14 d ramp ×1.0 at ≥ −40 mm → ×0.2 at ≤ −70 mm **(derived)** | plausible | R1, R2, R9, R26 | derived |
| GAL-18 | s.l. | stopper: heat / VPD | A sustained hot, dry-air spell suppresses fruiting. | 7-day mean Tmax: ×1 at ≤ 29 °C → ×0.3 at ≥ 33 °C; or 7-day mean daily max VPD: ×1 at ≤ 2.0 kPa → ×0.3 at ≥ 3.0 kPa (apply the stronger) **(derived)** | folklore | R26 (summer trough), R1 | available |
| GAL-19 | s.l. | stopper: drying wind | No gallinaccio-specific source found. Reuse the porcini drying-wind rule at half weight. | as porcini rule, weight ×0.5 | folklore (no source) | — | available |
| GAL-20 | s.l. | soil pH | Acidic soils favour the group, softened because *C. alborufescens* prefers limestone. **Flag only in v1.** | topsoil pH(H2O) 0–15 cm: `[3.5, 4.0, 6.0, 7.8]`, floor ×0.3 **(derived)** | plausible | R1, R2, R3, R10, R11, R12 | **missing** |
| GAL-21 | s.l. | substrate proxy (v1.1) | Cheaper stand-in for GAL-20: lithology class of the cell. | siliceous ×1.0; mixed ×0.7; calcareous ×0.4 (evergreen_oak on calcareous ×0.8) **(derived)** | plausible | R3, R1, R24 | missing (layer exists, not in grid yet) |

---

## Evidence by factor

### Season windows

**What sources say**

- **Tuscan specimens and plots.** Sequenced *C. pallens* and *C. alborufescens* were collected in
  Siena province on 9–10 November 2012 [R1]. The Siena plot surveys sampled monthly, "but
  discontinuous in summer when drought and high temperatures did not favour fungal fruiting"
  [R3].
- **Occurrence data, descriptive only** [R26]. Tuscan iNaturalist verifiable *Cantharellus*
  (n = 116) by month:

  | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | 3 | 1 | 0 | 0 | 13 | 10 | 4 | 1 | 6 | 49 | 22 | 7 |

  - There is a spring mode (May–June, 20% of records), a deep summer trough (July–August, 4%)
    and a large autumn mode (October–November, 61%) that runs into December and January.
  - By elevation: records below 300 m (n = 61) are almost all October–December. Records at
    300–600 m (n = 37) have a clear May peak (11) plus autumn. Records at 900 m and above (n = 9)
    fall in June–October.
  - The median elevation of April–July records is 376 m, against 241 m for October–December.
  - **Caveat.** These counts mix fruiting with observer effort (autumn foraging, holidays), and
    2019–2025 supply 111/116 records.
  - **Caveat (circularity).** I used all seasons for this description. If the orchestrator wants
    a clean hold-out, re-derive GAL-02 to GAL-04 from the training seasons only, or treat them as
    priors not to be tuned.
- **Regional mycological program** (Castilla y León, Spain) [R27]. *C. cibarius* is among the
  "summer" species, with good early-summer fruiting in June 2021.
- **Spanish mycological society** [R28]. *C. subpruinosus* (= *C. pallens*) "nace principalmente
  en primavera y otoño" (mostly in spring and autumn) under chestnut, cork oak and maritime pine,
  and appears sporadically in warm winters.
- **MUSE (Trento) macromycete census** [R29]. *C. alborufescens* records in north-east Italy span
  23 May to 28 November, at 25–1350 m.
- **Popular Italian sources (folklore).**
  - [R31]: in the lowlands finferli appear from May to November, with a big early-summer episode
    after a rainy June. In the mountains they come later, July to September.
  - [R30]: the Apennines June–October; Mediterranean lowlands extend into November–December.
  - [R32]: hills at 400–700 m start in late May after spring rains; 900–1200 m runs July–October.
- **Unverified.** A search-engine summary said Apennine–Adriatic areas fruit mainly in April–May
  and Tyrrhenian areas mainly in autumn. I could not find this on the fetched page, so it is not
  used; see Open questions.
- **Trend** [R16]. Across 486 European autumn-fruiting species the fruiting season has widened
  and ends later than in the 1970s. That argues for a permissive end to the window.

**Rules**

- **GAL-02 (derived).** Zero before mid-April and full from 10 May, from the May onset in
  [R26, R31, R32]. Full until 15 December and zero by 25 January, from the December–January
  lowland records [R26], the warm-winter note [R28] and the November Siena specimens [R1].
  Summer stays inside the window on purpose: [R31] reports early-summer flushes in rainy years,
  and a hard season gap would hide that from the backtest.
- **GAL-03 (derived).** Taken from the mountain windows in [R30, R31, R32] and the June–October
  records at 900 m and above [R26].
- **GAL-04** is the two-flush alternative, for comparison in the backtest.
- Confidence: plausible for GAL-02 (several independent indications), folklore to plausible for
  GAL-03 and GAL-04.

### Hosts and habitat affinity

**What sources say**

- **Tuscan plots** [R3], Table 1, 30 permanent plots in central-southern Tuscany, abundance as
  mDCv (maximum density of fruit bodies per visit; verified by reading the page image). The
  "C. cibarius" row reads:

  | forest type | plots with the species | mDCv values | mean mDCv per plot |
  |---|---|---|---|
  | chestnut coppices (Cs) | **9/9** | 5,1,3,3,2,3,1,3,1 | **2.44** |
  | evergreen oak woods, coast and inland hills (Qs) | **5/10** | 2,1,3,2,1 | 0.90 |
  | *Abies alba* woods, Mt Amiata and Casentino (Ab) | **2/7** | 2,4 | 0.86 |
  | calcicolous deciduous oak woods, *Q. cerris* / *Q. pubescens* on "calcare cavernoso", pH 6.8–7.4 (Qb) | **1/4** | 1 | 0.25 |

  The paper lists *C. cibarius* among the 37 broad-range species found in all four forest types.
- **Host range.** *C. cibarius* is recorded with 14 host genera, including *Abies*, *Carpinus*,
  *Castanea*, *Corylus*, *Fagus*, *Picea*, *Pinus*, *Populus*, *Pseudotsuga* and *Quercus*. The
  authors warn that this broad range belongs to the genus as a whole [R2, citing Danell 1999].
- **Hosts per segregate** [R1] (verified from the specimen lists).
  - *C. pallens*: *Q. ilex*, *Q. pubescens (humilis)*, *Q. cerris*, *Q. suber*, *Q. pyrenaica*,
    *Q. canariensis*, *Fagus*, *Corylus*, *Picea*.
  - *C. alborufescens*: evergreen oaks (*Q. ilex*, *Q. rotundifolia*) with *Q. pubescens* or
    *Pinus halepensis* nearby, once *Castanea*.
  - *C. cibarius* s.str. (Spain and France): *Pinus sylvestris*, *P. pinaster* on acid sand,
    *Fagus*, *Castanea*, *Q. robur*, *Betula*.
- **Other hosts.** *C. pallens* under *Castanea*, *Q. suber* and *Pinus pinaster* [R28]. Popular
  Italian sources name oak, chestnut and beech, plus spruce and silver fir in conifer woods
  [R31], and mention coastal pinewoods [R30].
- **Host soil preferences** (verified).
  - Chestnut "does not thrive on limestone, preferring well-drained, from very acidic to neutral
    soils and nutritionally poor sites" [R17].
  - *Q. pubescens* is "indifferent to pH" and prefers lime-rich soils in the north of its range
    [R19].
  - *Q. cerris* grows on weakly acid soils but also on shallow calcareous ones [R18].
  - Regione Toscana's own forest types split several classes by substrate: "Castagneto
    acidofilo", "Castagneto mesofilo su arenaria", "Castagneto mesotrofico su rocce vulcaniche
    del M. Amiata", "Cerreta acidofila…", "Querceto acidofilo di roverella a cerro", "Pineta
    acidofila di pino nero" [R20].

**Affinities (GAL-05, derived)**

Chestnut is the anchor at 1.0, and the other classes are scaled from [R3] where it gives numbers.

- **chestnut 1.0**: 9/9 plots and the highest abundance [R3]; a calcifuge host [R17]; hosts for
  *C. pallens* and *C. alborufescens* [R1, R28].
- **evergreen_oak 0.7**: 5/10 plots [R3]. Main host of *C. alborufescens* and a common host of
  *C. pallens* [R1]. It gets a higher weight than its plot frequency because it carries both the
  acid-soil and the calcareous-soil segregates.
- **beech 0.7**: well documented for *C. cibarius* s.str. and *C. pallens* [R1, R2, R31]. No
  Tuscan plot numbers.
- **fir_spruce 0.6**: 2/7 fir plots with fair abundance [R3]; *Abies* and *Picea* are hosts
  [R2, R31].
- **mixed_broadleaf_conifer 0.6**: mean of its parts.
- **deciduous_oak 0.5**: *Q. cerris* and *Q. pubescens* hosts [R1], but only 1/4 calcicolous
  plots [R3]. This class covers both acid-soil ("cerreta acidofila") and calcareous stands [R20],
  so without a substrate layer it gets a middle value.
- **mediterranean_pine 0.5**: *P. pinaster* host [R1, R28]; coastal pinewoods [R30]. 29/116 of
  Tuscan records sit below 100 m [R26], which is consistent with coastal woods but not checked
  habitat by habitat. *P. pinea* and *P. halepensis* have no specific evidence.
- **mountain_pine 0.4**: *P. sylvestris* is a host on acid soils [R1]. Tuscan black-pine
  plantations are often on poor or calcareous soils, although an acidophilous black-pine type
  exists [R20]. No direct data.
- **mixed_broadleaf 0.3**: *Carpinus* and *Corylus* hosts [R1, R2]; hop-hornbeam and ash woods
  have no data.
- **macchia 0.3**: *C. alborufescens* collected with *Q. pubescens*, *Viburnum tinus*, *Erica
  arborea* and *Rosmarinus* [R1], but only where a Fagaceae host is present. May fall outside the
  woodland mask.
- **other_conifer 0.2**: *Pseudotsuga* is a genus-level host [R2]. Cypress plantations are not
  ectomycorrhizal hosts (general knowledge, not source-checked).
- **riparian 0.1**: *Populus* is a genus-level host [R2], but these are wet sites.
- **exotic_broadleaf (robinia) 0.0**: no ectomycorrhizal host (general knowledge, not source-checked). Its
  nitrogen-rich soils also run against the low-nitrogen preference [R2].

**Vocabulary suggestion.** No new habitat term is needed. The M2 woodland-grid card should
consider keeping the **acidophilous vs calcicolous sub-types** of Regione Toscana's forest types
[R20]. For example, split `deciduous_oak` into acid and calcareous, and flag
`chestnut_acidophilous`. That would give v1 a soil-pH proxy for free (see "Soil pH: known gap").

### Altitude and aspect

**What sources say**

- **Tuscan plots** [R3]: coastal and inland evergreen oak (low elevation), calcicolous oak on
  Montagnola Senese (Mt Maggio, 658 m), chestnut coppices, and fir woods of Mt Amiata and
  Casentino (montane).
- **iNaturalist, Tuscany** [R26]. Elevations come from Open-Meteo's elevation service at the
  observation points; none of the records is obscured; median positional accuracy is about 30 m.
  - All *Cantharellus* (n = 116): p10 60 m, p25 101 m, median 289 m, p75 426 m, p90 740 m,
    maximum 1431 m.
  - Labelled *C. cibarius* (n = 43): median 302 m, p90 855 m, maximum 1316 m.
  - *C. pallens* (n = 27): median 218 m, p90 466 m.
  - *C. amethysteus* (n = 2): about 1046 m, in July.
  - Observers are concentrated near towns and the coast, so the low median partly reflects
    effort.
- ***C. alborufescens*** in the north-east Italian census: 25–1350 m [R29].
- **Popular sources.**
  - [R31]: finferli become "più rari dai 1500 m" (rarer from 1500 m up).
  - [R32]: ideal 300–1100 m, with good east or north-east exposure (folklore).
- **Aspect.** No quantitative source. In southern Europe *C. cibarius* s.str. is confined to
  "rainy or locally damp sites", and *C. ferruginascens* to "locally moist and humid sites" [R1].
  That suggests moisture-conserving slopes matter in summer at low elevation.

**Rules**

- **GAL-06 (derived):** `[0, 0, 1000, 1700]` m. Full from sea level (records down to 8 m [R26])
  to about 1000 m, then fading out: records thin above 1000 m and are rarer above 1500 m [R31].
  Tuscany's beech belt tops out around 1700–1800 m (general knowledge). Keep the altitude weight
  low; season and temperature already carry most of the elevation signal.
- **GAL-07 (derived, folklore):** a small north/east-facing bonus below 600 m in June–September
  only. Optional; the PRD allows v1 rules to skip aspect.

### Rain trigger (amount, lag)

**What sources say**

- **Tuscan oak forests** [R4], community-level: carpophore counts were tested against rain in
  the 5, 10, 15 and 30 days before sampling. "Highly significant correlations were found between
  the number of carpophores and rainfall in the 30 days preceding sampling." Rainfall was the main
  driver in autumn, the main fruiting period. These are all macrofungi, not *Cantharellus*
  separately; I saw the abstract only.
- **Boreal *C. roseocanus*** [R7]: "positive correlations were found between total rainfall 1 week
  prior to fructification, air temperature 2 weeks prior to fructification, and sporocarp
  productivity" (Canada, jack pine; extrapolated).
- **Boreal *C. cibarius*** [R6]: growing degree-days (base 5 °C) plus soil temperature (minimum
  500 ± 70 GDD) plus soil moisture or cumulative precipitation of **50–100 mm** best explained
  chanterelle yield 6–13 weeks before first appearance (Saskatchewan, jack pine; extrapolated).
- **Castilla y León program** [R27]: early-summer species, *C. cibarius* included, depend on the
  amount of rain, temperature, "y además por el número de eventos lluviosos que tienen lugar en
  los 15–20 días anteriores" (and on the number of rain events in the previous 15–20 days).
- ***C. formosus*, British Columbia** [R9]: after rains, "successive flushes every 2–3 weeks until
  cold weather precludes further fruiting".
- **Fruit-body longevity** [R2, citing Largent & Sime 1995 and Norvell 1995]: chanterelles "grow
  slowly (2 to 5 cm per month) and persist for an average of 44 days and occasionally more than
  90 days … so consistently high humidity might be especially important".
- **Popular Italian sources (folklore).** [R30]: "tre, quattro giorni di pioggia leggera ben
  distribuita, seguiti da notti fresche" (three or four days of light, well-spread rain followed
  by cool nights). [R31]: early-summer flush after "un mese piovoso di giugno" (a rainy June), and
  "piogge regolari" (regular rain) from summer into autumn.

**Rules (all derived)**

- **GAL-08:** 30-day rainfall ramp, 0 at ≤ 15 mm and full at ≥ 70 mm. The 30-day window comes
  from [R4], the only Tuscan quantitative result. The 50–100 mm cumulative figure comes from
  [R6]; I set full at 70 mm, near its lower-middle, because Tuscan autumn months often exceed
  that. The 15 mm zero is a judgement: less than one meaningful event in a month.
- **GAL-09:** a count of rain days in the last 20 days, from [R27]'s "number of rain events in
  15–20 days" and [R30]'s "3–4 days of light rain". Threshold ≥ 5 mm per day.
- **GAL-10:** lag trapezoid `[4, 10, 30, 50]` days after a wetting event (≥ 20 mm within 3 days).
  - Onset: rain about a week before correlates with productivity [R7], and the flush interval is
    2–3 weeks [R9]. So zero before day 4 and full from day 10.
  - Plateau and tail: fruit bodies last 44 days on average, sometimes more than 90 [R2]. So the
    plateau runs to day 30 and the tail to day 50.
  - **This is the main structural difference from porcini:** a longer plateau and a slow decay.
- The card's hypothesis, "responds to sustained moisture rather than single storms and persists
  longer than porcini", is **confirmed** as far as the literature allows: [R2, R4, R8, R27].
  Confidence plausible, because nothing is chanterelle-specific *and* Mediterranean.

### Antecedent moisture

**What sources say**

- **Tuscan oak forests** [R4]: "abundant annual rainfall was necessary for the fungal mycelium to
  fruit. Spring rainfall in particular seemed to be related to the number of species found in
  autumn."
- **Swiss plot, 21 years** [R5]: "Productivity was correlated with the precipitation from June
  until October" (all fungi).
- **Finland**, supply-model table verified [R8]. Annual *C. cibarius* purchases in eastern
  Finland over 1978–2016 rose with **June + July precipitation** (coefficient +0.0058 per mm,
  p < 0.05; R² 34.6%). The residual autocorrelation was strong, so weather explained the
  between-year variation only partly. Ceps and milk caps responded to August rain instead, which
  suggests chanterelles need rain about a month earlier than those species.
- **Mycelium depth** [R2, citing Danell 1994b]: "the chanterelle mycelium usually grows in the
  upper 5 to 10 cm of the soil". "High soil humidity during the fruiting season also allows
  mushrooms to continue growing without drying out" [R2, citing Kasparavičius 2000].

**Rules (derived)**

- **GAL-11:** topsoil moisture against the cell's own climatology for the month. Weight the
  0–7 cm layer higher, because the mycelium lives in the top 5–10 cm [R2].
  - Percentiles are used because Open-Meteo volumetric moisture depends on the model's soil
    texture, and no absolute threshold for chanterelles exists.
  - Zero at ≤ p15 and full at ≥ p40 is a guess to tune in the backtest.
- **GAL-12:** a 60-day P − ET0 multiplier (0.5 → 1.0) for the season-scale effects in [R4, R5,
  R8]. It is a multiplier with a 0.5 floor, not a gate, because the effect sizes are modest
  (R² about 0.35 in [R8]).
- **Summer drought legacy.** No source for how long a Mediterranean summer drought delays autumn
  chanterelles. In British Columbia, "an unusually hot and dry summer and early fall" pushed
  production to mid–late October [R9] (qualitative, other climate). GAL-12 handles this
  implicitly.

### Temperature

**What sources say**

- **No field study with chanterelle soil- or air-temperature bands** was found for Europe.
- **Lab mycelium.**
  - [R10]: growth was better at 20 and 24 °C than at 16 or 26 °C, and "optimum growth is achieved
    around 22 °C". Dutch strains.
  - [R11]: optimum 22.5 °C.
  - [R2, citing Danell 1994a]: 20 °C, 0.5 mm/day.
  - **Caveat:** these are mycelium in culture, not fruiting.
- **Field correlates (other climates).**
  - Air temperature 2 weeks before fruiting correlates positively with productivity [R7].
  - A GDD5 threshold of 500 ± 70 before first appearance [R6].
  - Warm spring weather promotes fruiting [R2, citing Dahlberg 1991].
  - Oregon: warm summers correlate with chanterelle abundance [R2, citing Norvell 1995; Norvell &
    Roger 1998]. In a cool oceanic climate warmth helps, while in Tuscany summer heat comes with
    drought.
  - Fruiting time of all fungi correlated with July–August temperatures in Switzerland [R5].
- **Popular Italian source (folklore)** [R30]: best fruiting "fra i 15 e i 24 °C" (between 15 and
  24 °C), with cool nights after rain.
- **Tuscan practice** [R26]: substantial lowland records in November–January, when shallow soil
  temperatures are well below 15 °C. That is general climate knowledge, not measured here.
- **Thermal shock:** no source found for *Cantharellus*. The "notti fresche" (cool nights) after
  rain [R30] is folklore; not encoded.

**Rules (derived, low confidence)**

- **GAL-13:** soil 0–7 cm, 7-day mean, `[5, 9, 20, 25]` °C.
  - Upper full limit 20 °C and zero at 25 °C: the mycelium optimum is about 20–24 °C [R10, R11],
    but fruiting in Tuscany collapses in July–August [R3, R26]. I place the zero where summer
    soils sit.
  - Lower limits 5 and 9 °C: they keep the December–January lowland records [R26] inside the
    band.
- **GAL-14:** the air-temperature fallback, shifted by about 1 °C.
- **GAL-15:** the GDD gate from [R6]. In Tuscan lowlands 430 °C·d is passed by spring (general
  climate knowledge, not computed here), so it binds only at high elevation. Optional.

### Stoppers

- **Drought (GAL-17, derived, plausible).**
  - [R1]: *C. cibarius* s.str. and *C. amethysteus* are absent where summers are dry; in the
    Mediterranean, *C. cibarius* s.str. and *C. ferruginascens* keep to damp sites.
  - The Tuscan summer trough in records [R26] and the plot surveys paused in summer drought [R3]
    both point the same way.
  - [R2]: "consistently high humidity might be especially important".
  - Against this, popular sources say chanterelles tolerate "moderate drought well" [R32], and
    Spanish popular pages say they endure drought once fruiting (search snippet only, not
    cited).
  - Hence a 14-day P − ET0 ramp with a **0.2 floor**, milder than a porcini-style cut-off.
- **Frost (GAL-16, derived, folklore).** The only source is qualitative: flushes continue "until
  cold weather precludes further fruiting" [R9]. The thresholds (Tmin ≤ −2 °C on two nights;
  ≤ −5 °C or snow) are my own and should match whatever the porcini draft sets, for consistency.
  Because fruit bodies persist [R2], a light-frost multiplier (×0.3) fits better than a hard zero.
- **Heat / evaporative demand (GAL-18, derived, folklore).** No source gives a threshold. The
  July–August collapse in Tuscany [R3, R26] is the only evidence, and it mixes heat with drought.
  Keep it separate from GAL-17 so the backtest can tell which one works.
- **Drying wind (GAL-19).** **No source found** for *Cantharellus*. Reuse the porcini
  tramontana/grecale rule at half weight: fruit bodies are long-lived and slow-drying [R2], so
  exposure matters less than for fast-rotting boletes. Folklore.
- **Picking and trampling** (not a weather stopper; noted for completeness). Picking does not
  reduce later chanterelle fruiting, while intense trampling depressed it temporarily [R2, citing
  Egli et al. 1990]. See also [R15] (not used for rules).

### Not modellable in v1

#### Soil pH: known gap

**The dependence and its sources**

- **Field range: pH 4.0–5.5.** "The golden chanterelle grows best in well-drained forest soils
  with low nitrogen content and a pH range of 4.0 to 5.5" [R2, p. 19, citing Danell 1994a [R13]
  and Jansen & van Dobben 1987 [R12]].
  - Northern California (*C. formosus*): nitrogen-poor soils at pH 4.0–5.5 [R9, citing Bergemann
    & Largent 2000].
- **Southern Europe, by taxon** [R1]: *C. cibarius* s.str. has "a clear preference for acid
  soils"; *C. pallens* is "markedly acidophilous in the Mediterranean area".
  - The exceptions point the other way: *C. alborufescens* grows on calcareous soil under
    evergreen oaks, and *C. ferruginascens* on calcareous soil in temperate Europe (but on acid
    ground in the Mediterranean).
  - **So the pH preference depends on taxon and climate.** In the Mediterranean the calcareous
    specialist in the group is *C. alborufescens*.
- **Tuscany** [R3]: the group occurs on neutral-basic "calcare cavernoso" soils (pH 6.8–7.4) but
  in only 1 of 4 plots, with the lowest possible abundance (mDCv 1). In chestnut coppices it
  occurs in 9 of 9 plots.
- **Dutch decline.** *C. cibarius* declined by about 60% of sites in 20 years in the Netherlands.
  Jansen & van Dobben attributed this to soil changes, partly from air pollution, meaning
  nitrogen and sulphur deposition [R12; R2]. That points to **low nitrogen** as important
  alongside acidity; excess N also reduces fruiting [R2].
- **Laboratory disagreement.** In culture, mycelium grows best at pH 5.5–6.0 and poorly at 3.5
  [R10, Table 5]; another strain peaked at pH 6.0 [R11]. The field acid preference probably
  reflects hosts, nitrogen and competition rather than a direct physiological optimum (my
  interpretation).

**How strong is it?**

- **Qualitatively strong:** every serious source agrees for the acidophilous members [R1, R2,
  R12].
- **Quantitatively weak:** there is no dose-response curve, and the Tuscan contrast rests on
  4 vs 9 plots.
- **Derived magnitude from [R3].** Mean abundance per plot is 0.25 in calcicolous oak against
  2.44 in chestnut, about **10× lower**, and presence is 25% against 100%. **But host and
  substrate are confounded:** calcicolous plots are oak, acid plots are chestnut. Treat 10× as an
  upper bound on the pure substrate effect.
- **For the s.l. target** the effect is diluted by *C. alborufescens* on calcareous evergreen-oak
  soils. Hence the floor of 0.3 in GAL-20 and the exception for evergreen oak in GAL-21.

**Proxies the grid could use later** (cheapest first)

1. **Host tree, already in v1.** The `chestnut` class carries most of the signal, since chestnut
   avoids limestone [R17]. No new data.
2. **Regional forest sub-types.** Regione Toscana's forest types split several classes by
   substrate ("…acidofilo/a", "…su arenaria", "…su rocce vulcaniche") [R20]. If M2 keeps these
   sub-types, a binary acid-substrate flag costs nothing.
3. **Lithology.** The Regione Toscana 1:10,000 geological database (Spatialite, over 500 areal
   unit codes) [R24] can be reclassified once into siliceous, mixed and calcareous. Compute the
   calcareous share of each 1 km cell. This is **GAL-21**. It is robust because rock type changes
   little, but it only approximates topsoil pH, since soils on limestone can be decalcified.
4. **SoilGrids 2.0** [R21]: global pH(H2O) at 250 m for 0–5 and 5–15 cm, with uncertainty
   layers. Aggregate to the cell mean or the share of area below pH 6. It reproduces coarse
   patterns but carries large local error [R21], so use it as a soft prior, not a gate.
5. **LUCAS topsoil pH** [R22]: EU map at about 500 m built from roughly 22,000 samples (per its
   abstract; the resolution is from general knowledge). The samples are mostly farmland, so it is
   weaker in forests.
6. **Regione Toscana 1:10,000 pedological database** [R23]: CC-BY Spatialite with soil units,
   capability and hydraulic properties. **Whether it contains pH was not verified.** Check before
   relying on it.

**How the absence of pH will bias v1 scores**

- **Over-scoring on calcareous and neutral-basic substrates** for deciduous oak (*Q. pubescens*
  and *Q. cerris* on limestone or marl), hop-hornbeam and mixed broadleaf, and black-pine
  plantations on calcareous ground. The Montagnola Senese plots in [R3] are a verified example.
  Here v1 will predict fair conditions where the acidophilous members are rare.
- **Roughly correct on calcareous evergreen oak**, because *C. alborufescens* lives there [R1].
- **Under-scoring is unlikely** from the missing pH itself. The main risk is under-weighting
  acid-soil deciduous oak and black pine, which GAL-05 averages down.
- **Effect on the backtest.** False positives in calcareous cells lower lift and AUC. With about
  116 sightings the effect may not be significant.
  - **Suggested check:** at equal score, compare sighting rates in siliceous and calcareous cells
    once a lithology layer exists. A ratio well below 1 for calcareous cells justifies adding
    GAL-21.
  - Beware that sightings may themselves cluster on popular siliceous chestnut areas (observer
    bias).

#### Other factors not modellable

- **Nitrogen and deposition** [R2, R12]: low-N soils favour fruiting, and fertilisation or
  deposition reduces it. Missing; effect likely small in Tuscany compared with the Netherlands
  (unverified).
- **Stand age and canopy.**
  - Plantations begin fruiting at 10–40 years [R2, citing Danell 1994a].
  - Greatest occurrence in 41–60-year jack pine at moderately open canopy [R6].
  - High stand density was favourable in [R7].
  - Chestnut coppice rotations in Tuscany make stand age relevant; no local data. Missing.
- **Moss, litter and understory** [R7]: frequent moss and lichen were positive, and ericaceous
  shrubs negative, in jack pine. [R9, citing Bergemann & Largent 2000]: moderate duff depth,
  needle cover below 30%. Missing.
- **Soil texture and drainage.** Well-drained soils [R2]; clay + silt was favourable on sandy
  soil [R7]; [R31] says "senza ristagni idrici" (without waterlogging). Missing, though SoilGrids
  texture could proxy it later.
- **Management.** Clearcutting can shrink or eliminate patches [R2]. Trampling depresses
  fruiting temporarily [R2]. Missing.

---

## Disagreements and open questions

**Disagreements**

1. **pH optimum: field vs lab.** The field range is 4.0–5.5 [R2], but mycelium grows best at
   pH 5.5–6.0 [R10, R11]. Not resolved; the field range is what matters for the grid.
2. **pH within the group.** The acidophilous *C. pallens* and *C. cibarius* s.str. contrast with
   the calcicolous *C. alborufescens* [R1]. *C. ferruginascens* switches with climate [R1], and
   *C. pallens* is on "rich ground" in Fennoscandia [R1]. A single s.l. pH rule is a compromise.
3. **Drought tolerance.** Popular sources call chanterelles tolerant of moderate drought [R32].
   The literature stresses sustained humidity [R2] and says the temperate taxa are absent under
   summer drought [R1]. Both can hold: the Mediterranean segregates tolerate drought better than
   *C. cibarius* s.str. The GAL-17 floor reflects this.
4. **Warmth.** Warm summers are positive in Oregon [R2, citing Norvell] and air warmth 2 weeks
   before fruiting is positive in Canada [R7]. In Tuscany, high summer temperatures coincide with
   no fruiting [R3, R26]. This is a climate-context difference, not a contradiction: warmth helps
   when moisture is not limiting.
5. **Which flush is bigger.** Popular sources stress an early-summer flush after a rainy June
   [R31]. Tuscan records peak in October–November [R26]. This may be real (lowland Mediterranean
   segregates fruit in autumn) or observer effort (autumn foraging). GAL-04 against GAL-02 in the
   backtest can inform this.
6. **Is it *C. cibarius* at all?** Popular Italian pages describe "*C. cibarius*" across all
   Italian habitats [R30, R31]. [R1] excludes *C. cibarius* s.str. from Mediterranean-climate
   areas.

**Open questions and leads not fully read**

- **Does *C. cibarius* s.str. occur in Tuscany** (Apennine beech and fir, Mt Amiata)? No Tuscan
  sequenced material found. This matters only for a v2 split.
- **East–west seasonality in Italy.** The claim that Adriatic and Apennine sides fruit mostly in
  spring and Tyrrhenian sides mostly in autumn appeared only in a search-engine summary.
  **Unverified; not used.** Worth a check against Tuscan records split by basin.
- **[R34] Laganà et al. 2002** on periodicity in Tuscan *Abies alba* forests may hold monthly
  *Cantharellus* data from Amiata and Casentino. Not accessed (paywall).
- **[R4] Salerni et al. 2002**, full text not accessed. The per-species correlations, if any, are
  unknown.
- **[R35] Baptista et al. 2010** on fruiting patterns in NE Portuguese chestnut, a Mediterranean
  chestnut analogue. Blocked by a captcha.
- **Danell 1994a thesis [R13]:** not accessed; the pH figure relies on the Pilz et al. summary
  [R2].
- **Finnish and Baltic leads.** Ohenoja (1993) and Salo were not found as accessible
  chanterelle-specific weather analyses. The Finnish evidence used here is the verified
  Tahvanainen table [R8]. Kasparavičius (Lithuania) is known only through [R2].
- **Italian societies** (AMB, Università di Siena beyond [R3, R4]): no Tuscany-specific
  *Cantharellus* phenology found.
- **Sample size for validation.** 116 iNaturalist and 48 GBIF records, mostly 2019–2025 [R25,
  R26]. Spring has only about 23 records. Expect wide confidence intervals; pool the seasons.
- **Circularity.** The month and elevation profiles [R26] used all seasons. See the note under
  Season windows.

---

## References

- [R1] Olariaga I., Moreno G., Manjón J.L., Salcedo I., Hofstetter V., Rodríguez D., Buyck B.
  (2017). *Cantharellus* (Cantharellales, Basidiomycota) revisited in Europe through a multigene
  phylogeny. *Fungal Diversity* 83: 263–292. https://doi.org/10.1007/s13225-016-0376-7 (PDF
  read at https://www.fungipedia.org/media/kunena/attachments/2683/CantharellusmonografiaEuropa.pdf).
  `verified`. Supports: the eight European species and their synonyms (*subpruinosus* =
  *pallens*); ecology, climate and soil preference per taxon; Tuscan specimens (Siena
  province); low host specificity.
- [R2] Pilz D., Norvell L., Danell E., Molina R. (2003). *Ecology and management of commercially
  harvested chanterelle mushrooms.* Gen. Tech. Rep. PNW-GTR-576. USDA Forest Service, PNW Research
  Station. https://research.fs.usda.gov/treesearch/5298 (PDF
  https://research.fs.usda.gov/download/treesearch/5298.pdf). `verified`. Supports: pH 4.0–5.5
  and low N (p. 19); 14 host genera, fruiting at stand age 10–40 years, weather effects, growth
  2–5 cm/month and 44-day mean persistence (p. 20); mycelium in the top 5–10 cm, N and
  deposition, picking and trampling (pp. 23–24); culture at 20 °C.
- [R3] Laganà A., Salerni E., Barluzzi C., Perini C., De Dominicis V. (1999). Mycocoenological
  studies in Mediterranean forest ecosystems: calcicolous deciduous oak woods of central-southern
  Tuscany (Italy). *Czech Mycology* 52(1): 1–16. https://czechmycology.org/_cm/CM52101.pdf
  `verified`. Supports: "*C. cibarius*" presence and abundance in 30 Tuscan plots by forest type
  (Table 1); soil pH 6.8–7.4 of the calcicolous plots; summer sampling gap during drought.
- [R4] Salerni E., Laganà A., Perini C., Loppi S., De Dominicis V. (2002). Effects of temperature
  and rainfall on fruiting of macrofungi in oak forests of the Mediterranean area. *Israel
  Journal of Plant Sciences* 50(3): 189–198. https://doi.org/10.1560/GV8J-VPKL-UV98-WVU1
  `verified` (abstract only, via OpenAlex). Supports: 30-day rainfall window; annual and spring
  rain effects in Tuscan oak forests (community level).
- [R5] Straatsma G., Ayer F., Egli S. (2001). Species richness, abundance, and phenology of
  fungal fruit bodies over 21 years in a Swiss forest plot. *Mycological Research* 105(5):
  515–523. https://doi.org/10.1017/S0953756201004154 (abstract at
  https://research.wur.nl/en/publications/species-richness-abundance-and-phenology-of-fungal-fruit-bodies-o).
  `verified` (abstract only). Supports: productivity vs June–October rain; fruiting time vs
  July–August temperature (all fungi).
- [R6] Ivanochko G., Svendsen E., Hrycan W., Tanino K. (2021). Characterization of chanterelle
  (*Cantharellus cibarius*) and pine mushrooms (*Tricholoma magnivelare*) in northern
  Saskatchewan. *Canadian Journal of Plant Science* 101: 853–870.
  https://doi.org/10.1139/cjps-2021-0136 `verified` (abstract only, via Semantic Scholar).
  Supports: GDD5 of 500 ± 70; cumulative precipitation of 50–100 mm; stand age 41–60 years;
  moderately open canopy.
- [R7] Rochon C., Paré D., Pélardy N., Khasa D.P., Fortin J.A. (2011). Ecology and productivity
  of *Cantharellus cibarius* var. *roseocanus* in two eastern Canadian jack pine stands. *Botany*
  89(10): 663–675. https://doi.org/10.1139/b11-058 `verified` (abstract only, via OpenAlex).
  Supports: rain 1 week before and air temperature 2 weeks before correlate with productivity;
  moss, C:N, stand density, texture.
- [R8] Tahvanainen V. (2020). *The availability and supply of marketed mushrooms in Eastern
  Finland.* Dissertationes Forestales 291. https://doi.org/10.14214/df.291 (PDF
  https://dissertationesforestales.fi/pdf/10325), summarising Tahvanainen V., Miina J., Kurttila
  M. (2019), Climatic and economic factors affecting the annual supply of wild edible mushrooms
  and berries in Finland, *Forests* 10(5): 385, https://doi.org/10.3390/f10050385. `verified`
  (dissertation Table 2 read; 2019 abstract via OpenAlex). Supports: June + July precipitation
  raises *C. cibarius* supply (coefficient 0.0058 per mm, R² 34.6%).
- [R9] Ehlers T., Hobby T. (2010). The chanterelle mushroom harvest on northern Vancouver Island,
  British Columbia: factors relating to successful commercial development. *BC Journal of
  Ecosystems and Management* 11(1&2): 72–83.
  https://jem-online.org/index.php/jem/article/download/55/25/383 `verified`. Supports: flushes
  every 2–3 weeks until cold weather; a hot, dry summer delayed production to late October; pH
  4.0–5.5 in northern California (citing Bergemann & Largent 2000). Concerns *C. formosus*.
- [R10] Straatsma G. (1986). *Physiology of mycelial growth of the mycorrhizal mushroom
  Cantharellus cibarius Fr.* PhD thesis, Landbouwhogeschool Wageningen.
  https://edepot.wur.nl/202849 `verified`. Supports: in vitro growth best at 20–24 °C (optimum
  about 22 °C) and pH 5.5–6.0 (Tables 2 and 5).
- [R11] Deshaware S., Marathe S.J., Bedade D., Deska J., Shamekh S. (2021). Investigation on
  mycelial growth requirements of *Cantharellus cibarius* under laboratory conditions. *Archives
  of Microbiology* 203(4): 1539–1545. https://doi.org/10.1007/s00203-020-02142-0 `verified`
  (PubMed abstract). Supports: in vitro optimum pH 6.0 and 22.5 °C.
- [R12] Jansen E., van Dobben H.F. (1987). Is decline of *Cantharellus cibarius* in the
  Netherlands due to air pollution? *Ambio* 16(4): 211–213.
  https://www.jstor.org/stable/4313357 `snippet-only`. Supports: marked Dutch decline linked to
  soil change, partly from air pollution (content also via [R2]).
- [R13] Danell E. (1994). *Cantharellus cibarius: mycorrhiza formation and ecology.* Acta
  Universitatis Upsaliensis, Comprehensive Summaries of Uppsala Dissertations from the Faculty of
  Science and Technology 35. http://uu.diva-portal.org/smash/record.jsf?pid=diva2:295603
  `snippet-only` (repository unreachable). Supports: the source of the pH 4.0–5.5 figure as cited
  in [R2].
- [R14] Danell E. (1994). Formation and growth of the ectomycorrhiza of *Cantharellus cibarius*.
  *Mycorrhiza* 5: 89–97. https://doi.org/10.1007/BF00202339 `snippet-only` (metadata only).
  Supports: mycelium in the top 5–10 cm, as cited in [R2].
- [R15] Egli S., Peter M., Buser C., Stahel W., Ayer F. (2006). Mushroom picking does not impair
  future harvests – results of a long-term study in Switzerland. *Biological Conservation*
  129(2): 271–276. https://doi.org/10.1016/j.biocon.2005.10.042 `snippet-only` (metadata only).
  Supports: context on harvest impact only; **not used for any rule**.
- [R16] Kauserud H. et al. (2012). Warming-induced shift in European mushroom fruiting phenology.
  *PNAS* 109(36): 14488–14493. https://doi.org/10.1073/pnas.1200789109 `verified` (abstract).
  Supports: widening fruiting seasons that end later; mycorrhizal seasons more compressed than
  saprotroph seasons.
- [R17] Conedera M., Tinner W., Krebs P., de Rigo D., Caudullo G. (2016). *Castanea sativa* in
  Europe: distribution, habitat, usage and threats. In: *European Atlas of Forest Tree Species.*
  Publ. Off. EU. https://forest.jrc.ec.europa.eu/media/atlas/Castanea_sativa.pdf `verified`.
  Supports: chestnut "does not thrive on limestone", very acidic to neutral soils.
- [R18] de Rigo D., Enescu C.M., Houston Durrant T., Caudullo G. (2016). *Quercus cerris* in
  Europe: distribution, habitat, usage and threats. In: *European Atlas of Forest Tree Species.*
  https://forest.jrc.ec.europa.eu/media/atlas/Quercus_cerris.pdf `verified`. Supports: grows on
  weakly acid to shallow calcareous soils.
- [R19] Pasta S., de Rigo D., Caudullo G. (2016). *Quercus pubescens* in Europe: distribution,
  habitat, usage and threats. In: *European Atlas of Forest Tree Species.*
  https://forest.jrc.ec.europa.eu/media/atlas/Quercus_pubescens.pdf `verified`. Supports:
  "indifferent to pH", prefers lime-rich soils in the north of its range.
- [R20] Regione Toscana, Giunta Regionale. *I tipi forestali* (series "Boschi e macchie di
  Toscana"), part I.
  https://www.regione.toscana.it/documents/10180/24010/I%20tipi%20forestali%20-%20parte%20I/50dd71a3-3925-488b-9b22-66672479dcb0
  `verified` (text extracted with a font-encoding workaround; forest-type names read, not the
  full descriptions). Supports: substrate-specific forest types ("Castagneto acidofilo",
  "Castagneto mesofilo su arenaria", "Castagneto mesotrofico su rocce vulcaniche del M. Amiata",
  "Cerreta acidofila…", "Querceto acidofilo di roverella a cerro", "Pineta acidofila di pino
  nero").
- [R21] Poggio L. et al. (2021). SoilGrids 2.0: producing soil information for the globe with
  quantified spatial uncertainty. *SOIL* 7: 217–240. https://doi.org/10.5194/soil-7-217-2021
  `verified` (abstract). Supports: 250 m global pH(H2O) at six depths, with uncertainty.
- [R22] Ballabio C. et al. (2019). Mapping LUCAS topsoil chemical properties at European scale
  using Gaussian process regression. *Geoderma* 355: 113912.
  https://doi.org/10.1016/j.geoderma.2019.113912 `verified` (abstract). Supports: an EU topsoil
  pH and CaCO3 map as a candidate proxy.
- [R23] Regione Toscana. DataBase Pedologico in scala 1:10.000 (Spatialite, CC-BY).
  https://dati.toscana.it/dataset/dbped/resource/966fbdd4-3ee9-4762-8954-4ceacd6e66a4
  `verified` (dataset page). Supports: an available regional soil database; the pH attribute is
  not confirmed.
- [R24] Regione Toscana. DataBase Geologico in scala 1:10.000 (Geoscopio DB Geologico).
  https://dati.toscana.it/dataset/dbg/resource/914208a2-693b-4bdd-b75e-9e25088946b1
  `snippet-only`. Supports: a lithology layer for a calcareous/siliceous reclassification.
- [R25] GBIF API queries, 2026-09-17: species match for *Cantharellus* names;
  `occurrence/search?taxonKey=…&gadmGid=ITA.16_1` with month, dataset, basis-of-record and
  species facets. https://api.gbif.org/v1/ `verified` (queried). Supports: backbone synonymy;
  Tuscan record counts by taxon.
- [R26] iNaturalist API, 2026-09-17: `observations?place_id=13073&taxon_id=47348&verifiable=true`
  (116 records), aggregated by month, taxon and elevation. Elevations from the Open-Meteo
  elevation API at each point; only aggregates are reported here.
  https://api.inaturalist.org/v1/ and https://api.open-meteo.com/v1/elevation `verified`
  (queried). Supports: Tuscan month and elevation profiles.
- [R27] Micocyl, Junta de Castilla y León (2021-06-15). Fructificación de especies típicas de
  inicio de verano.
  https://www.micocyl.es/noticias/fructificacion-de-especies-tipicas-de-inicio-de-verano
  `verified`. Supports: summer fruiting of *C. cibarius* tied to the amount of rain and the
  number of rain events in the previous 15–20 days.
- [R28] Sociedad Micológica Extremeña (MICOEX) (2016-09-17). *Cantharellus subpruinosus* =
  *Cantharellus pallens*. https://micoex.org/2016/09/17/cantharellus-subpruinosus/ `verified`.
  Supports: spring and autumn fruiting, sporadic in warm winters; chestnut, cork oak and maritime
  pine hosts.
- [R29] MUSE – Museo delle Scienze (Trento). Censimento dei macromiceti: *Cantharellus
  alborufescens*. https://www2.muse.it/bresadola/map_det.asp?sp=450082&ar=tv `verified`.
  Supports: NE Italy records at 25–1350 m, 23 May–28 November; association with *Q. ilex* and
  *Q. suber*.
- [R30] Oppicelli N. (2025-07-22). *Cantharellus cibarius*: il fungo più amato d'Europa. 3B Meteo
  Funghi. https://funghi.3bmeteo.com/cantharellus-cibarius/ `verified`; folklore. Supports:
  acid/subacid soils; 15–24 °C; 3–4 days of light rain then cool nights; regional seasons.
- [R31] Cacciatoridifunghi.it (2022-06-01). Dove si trovano i finferli o galletti?
  https://www.cacciatoridifunghi.it/blog/trova-i-funghi/dove-si-trovano-i-finferli-o-galletti/
  `verified`; folklore. Supports: May–November in lowlands, July–September in mountains, rarer
  above 1500 m; acid soils without waterlogging; early-summer flush after a rainy June.
- [R32] MyBoletus. Chanterelles in Europe: where to find them, season and habitat.
  https://myboletus.com/en/funghi/finferli/ `verified`; folklore. Supports: 300–1100 m; hill
  season from late May, 900–1200 m from July to October; E/NE exposure; "tolerates moderate
  drought".
- [R34] Laganà A., Angiolini C., Loppi S., Salerni E., Perini C., Barluzzi C., De Dominicis V.
  (2002). Periodicity, fluctuations and successions of macrofungi in fir forests (*Abies alba*
  Miller) in Tuscany, Italy. *Forest Ecology and Management* 169(3): 187–202.
  https://doi.org/10.1016/S0378-1127(01)00672-7 `snippet-only` (metadata only). Lead only; not
  used for rules.
- [R35] Baptista P., Martins A., Tavares R.M., Lino-Neto T. (2010). Diversity and fruiting pattern
  of macrofungi associated with chestnut (*Castanea sativa*) in the Trás-os-Montes region
  (Northeast Portugal). *Fungal Ecology* 3(1): 9–19. https://doi.org/10.1016/j.funeco.2009.06.002
  `snippet-only` (metadata only). Lead only; not used for rules.

(R33 intentionally unused.)
