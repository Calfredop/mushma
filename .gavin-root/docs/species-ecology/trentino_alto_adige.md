# Species ecology: Trentino-Alto Adige (regional appendix to species-ecology.md)

Research date: 2026-09-26 (dates Europe/Rome, units metric). Card:
`region-trentino-alto-adige-species.md` (child of `region-trentino-alto-adige.md`). Rule files:
`api/src/api/config/species/trentino_alto_adige/`. This appendix records how the Tuscan rule set
(`species/tuscany/`) was carried to Trentino-Alto Adige (South Tyrol in English), what changed and
why. It covers **fruiting conditions only**: nothing here is about edibility or identifying
specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(17 added for this region, in one block at the end of the file, keys prefixed `taa_` or with a
`_taa_` infix). Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md):
**strong**, **plausible**, **folklore**. Every number is a prior for the backtest; season windows,
altitude bands and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).
Piemonte ([`piemonte.md`](piemonte.md)) was the Alpine template; the Lombardia appendix (branch
`region/lombardia`) was read for ideas only, and none of its sources is cited here unless it was
opened again for this card.

## Summary

1. **All three groups and all six keys are kept.** Every key has records in the region and a
   society or institutional source for it here.
   - ***B. aereus* is marginal:** 3 iNaturalist records, and the north-east census maps it in 6
     squares of Trentino (the Adige valley at Trento and Pomarolo, the Brentonico plateau, Fornace,
     the Val di Cembra, Spormaggiore) and none in South Tyrol (`muse_censimento_boletus`,
     `mushma_occurrence_check_taa_2026`). It is kept with its band cut to the low hills. Its hosts
     are rare here, so the habitat gate confines it to few cells, and the porcini group takes the
     max over its keys, so it cannot lower the group.
   - **Ovoli are rare but present in both provinces:** 12 iNaturalist records, 17 census squares
     in Trentino and 6 in South Tyrol, collections from Appiano (665 m, 1924) to Capriana (1,050 m,
     2014) (`taa_muse_censimento_caesarea`). Kept, on the warm terraces and low valleys.
2. **The most Alpine region so far.** The grid's woodland has its median at 1,407 m (Piemonte 838
   m) and is 53 % spruce and fir, 14 % larch and stone pine (`regions/trentino_alto_adige.md`). The
   records sit high too: *B. edulis* median 1,406 m, *Cantharellus* 1,347 m. So the changes are
   Alpine: bands reach the subalpine spruce, larch and stone pine drop to non-host, Scots pine
   rises, and the mountain-pine and green-alder scrub, which here fill the `transitional`
   class, is non-host for all six keys.
3. **Seasons: shorter autumns, no split for *B. edulis*.** The 455 *B. edulis* records run July to
   early October at every elevation: the peak moves from September (1,000-1,300 m) to August
   (above 1,600 m), but the start and the end do not. So *B. edulis* gets one window, full from
   mid-July to 30 September and closed by 31 October, where Piemonte and Lombardia split theirs
   by elevation. Every other taxon ends earlier than in Tuscany. *B. pinophilus* gets one
   May-October window with no summer gap.
4. **Weather rules are all Tuscany's.** No study from the region ties these fungi to rain or
   temperature in numbers. The cold is left to the frost, snow and temperature rules on each
   cell's weather, and the porcini 30-day rain is already scored against each cell's own normal.
5. **Evidence.** Of the 17 new references, all opened:
   - 2 peer-reviewed (South Tyrolean larch and stone pine root tips);
   - 9 institutional (both provinces' forest typologies and forest pages, and their picking rules);
   - 2 society (census pages the shared file lacked);
   - 2 web (press);
   - 2 our own analyses.

   The records carry most of the numbers: 763 iNaturalist records of the six taxa, the best set
   of any region so far, joined to the region grid and to Trentino's forest-type map.
   `sanity.yaml` holds 16 press contrasts (14 porcini, 2 gallinacci) across both provinces,
   2019-2025, every main source opened and its quote checked.

## At a glance: what differs from Tuscany and why

Trapezoids are `[zero, full, full, zero]`, dates `DD-MM`, altitudes in metres.

| key | factor | Tuscany | Trentino-Alto Adige | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | 01-07 → 01-09 … 15-11 → 20-12 | **15-06 → 15-07 … 30-09 → 31-10**, one window at every elevation | 455 records: Oct 0.4×, Nov 0.1× the effort; located records start and end alike in every band (below 1,300 m first half of Oct 4, second 0; above 1,600 m 6 and 0) | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **200 → 500 … 1,900 → 2,300** | records p10 1,022, median 1,406, p90 1,810, max 2,170 m; census max 2,175 m in Trentino; spruce to 2,000-2,200 m | plausible |
| *edulis* | habitat `other_conifer`, `transitional` | 0.3, 0.3 | **0.1, 0.1** | only larch and stone pine here, no *Boletus* on their roots in South Tyrol; record cells above 1,500 m 21 % larch against 27 % of the woods; transitional = mughete and green alder | plausible |
| *reticulatus* | season | 01-05 → 01-06 … 30-09 → 15-11 | **01-05 → 01-06 … 15-09 → 20-10** | 42 records: Sep 0.6×, Oct 0 (about 6 expected); located 3 June to 14 September | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | **0 → 150 … 1,300 → 1,700** | records p90 1,275, p95 1,360, max 1,945 m (census max 1,927 m); montane beech and fir | plausible |
| *aereus* | season | upland summer / lowland autumn, split at 400-600 m | **one window 01-07 → 15-08 … 20-10 → 20-11** | no Apennine uplands, no macchia; census profile peaks in October and stops in November | plausible |
| *aereus* | altitude | … 800 → 1,250 | **… 800 → 1,100** | census squares 200-1,000 m; South Tyrol's colline oak woods end near 750 m | plausible |
| *pinophilus* | season | spring + autumn windows, gap 20-07 → 15-08 | **01-05 → 25-05 … 10-10 → 10-11** | 45 records 1.0-1.5× the effort in every month May to October; census 12 May to 28 October | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **400 → 700 … 1,800 → 2,200** | records 725-1,927 m, p90 1,567 m; Scots pine from 379 m, spruce to 2,000 m | plausible |
| *pinophilus* | habitat | mountain pine 0.6, other conifer 0.3, transitional 0.3 | **1.0, 0.1, 0.1** | "frequentemente legato al pino silvestre"; record surroundings 18 % Scots pine against 8 % of the woods at 1,000-1,500 m | plausible |
| ovoli | season | 01-06 → 01-09 … 05-11 → 30-11 | **01-06 → 15-07 … 30-09 → 31-10** | records Jul 2, Aug 4, Sep 4, Oct 1; census collections July-September | plausible |
| ovoli | altitude | … 750 → 1,100 | **… 900 → 1,200** | records 484-906 m; collections to 1,050 m (1,300 m max) on warm terraces | plausible |
| ovoli | habitat | mountain pine 0.0, transitional 0.6 | **0.3, 0.1** | oak-Scots pine woods ("sotto pino e quercia", Pergine 880 m); transitional = subalpine scrub | plausible |
| gallinacci | season | lowland 15-04 → 10-05 … 15-12 → 25-01; mountain … 15-10 → 15-11 | **lowland 15-05 → 15-06 … 31-10 → 30-11; mountain … 15-09 → 20-10** | 206 records: Sep 0.8×, Oct 0.4×, none in winter to speak of; above 1,000 m 15 records in early Sep, 5 late Sep, 2 Oct | plausible |
| gallinacci | altitude | … 1,000 → 1,700 | **… 1,700 → 2,100** | records p90 1,727, p95 1,767 m; census to 2,040 m | plausible |
| gallinacci | habitat | fir/spruce 0.6, mountain pine 0.3, other conifer 0.3, transitional 0.3 | **1.0, 0.6, 0.1, 0.1** | *C. cibarius* s.str. (169 of 191); record surroundings 62 % spruce against 30 % of the woods at 1,000-1,500 m | plausible |
| every key | slope stopper | x1 to 25°, x0.8 from 40° | **x1 to 35°, x0.8 from 45°** | the same rule on the region grid: woodland p90 34.5°, max 44.7° (median 26.9°) | as Tuscany (plausible) |
| every key | weather, growth clock, sun exposure, other stoppers | — | **kept** | no regional numbers; see Weather and Slope and sun exposure | as Tuscany |

Kept on purpose:
- beech as a *B. edulis* host, although the records sit in it less than the woods do;
- mixed broadleaf at 0.3 for *B. edulis* and gallinacci (here hop-hornbeam, which the records avoid);
- the *reticulatus* and ovoli hosts apart from the two changes above;
- the gallinacci and ovoli soil-pH and lithology rules, still disabled.

**Effect on the grid.** Habitat and altitude gates only, on the region grid's 7,698 woodland
cells, with the located records in woodland cells (`mushma_taa_forest_check_2026`):

| key | records | habitat gate full on (Tuscan → regional rules) | altitude gate full on | gates at record cells vs woodland mean (Tuscan → regional) |
|---|---|---|---|---|
| *edulis* | 194 | 99 % → 94 % | 59 % → 88 % | 0.83 vs 0.76 → 0.99 vs 0.95 |
| *reticulatus* | 20 | 92 % → 90 % | 27 % → 41 % | 0.84 vs 0.41 → 0.95 vs 0.57 |
| *aereus* | 1 | 8 % → 7 % | 11 % → 11 % | 0.00 vs 0.13 → 0.00 vs 0.12 (the one record, at 1,650 m, is a likely misidentification) |
| *pinophilus* | 29 | 99 % → 94 % | 55 % → 76 % | 0.94 vs 0.74 → 0.97 vs 0.89 |
| ovoli | 4 | 7 % → 8 % | 9 % → 16 % | 0.33 vs 0.10 → 0.43 vs 0.16 |
| gallinacci | 140 | 98 % → 94 % | 21 % → 75 % | 0.47 vs 0.46 → 0.96 vs 0.88 |

Under the Tuscan rules the Alpine records lost credit to the altitude bands (gallinacci at record
cells 0.47, no better than the woodland average). Under the regional rules every key keeps its
records near full credit and still scores the woodland lower on average.

## Trentino-Alto Adige in brief

**Woods.** Two provinces, two forest maps, one grid (`regions/trentino_alto_adige.md`: 7,698
woodland cells; forest 369,289 ha in Trentino and 342,994 ha in South Tyrol).
- **Trentino** (`taa_pat_foreste_trentino`, `taa_pat_tipi_forestali_2018`):
  - "I boschi in Trentino ricoprono una superficie di 390.463 ettari, pari al 63% del territorio
    provinciale"; by forest type spruce 32 %, beech 14 %, larch 13 % and silver fir 11 %.
  - Three districts:
    - the *esalpica*, "quote generalmente inferiori ai 1000 m", hop-hornbeam and manna ash, along
      the Adige, the Val dei Laghi and the Val di Non;
    - the *mesalpica*, "quote incentrate intorno ai 1000 m", fir and beech (Primiero, Tesino,
      Valsugana, the Piné and Lavarone plateaus, the Val di Cembra, the outer Giudicarie);
    - the *endalpica*, the Dolomites, Lagorai, Adamello and Cevedale with "fondovalle a quota
      superiore ai 1000 m", spruce, larch and stone pine.
- **South Tyrol** (`taa_bz_hauptbaumarten`, `taa_bz_wald_flaechen`, `taa_bz_waldtypisierung2010`):
  - by growing stock spruce 60 %, larch 19 %, pine 10 %, stone pine 6 %, fir 3 %, broadleaves 2 %;
  - 339,270 ha of forest, 46 % of the province, most of it at 1,000-2,000 m and "over two thirds"
    on slopes steeper than 40 %;
  - the Vinschgau is "den trockensten und kontinentalsten Raum der Ostalpen", with "weit
    ausgedehnte montane Kiefern- und Lärchenwälder am Sonnenhang";
  - the south (Adige and Isarco valleys) has "Hopfenbuchen- und Flaumeichenwäldern, darüber
    Eichen-Kiefernwälder und Eichen-Kastanien-Mischwälder".

**Which habitat holds which tree.** From the region config (`regions/trentino_alto_adige.yaml`),
with Trentino's areas from its forest-type map (`mushma_taa_forest_check_2026`; South Tyrol's map
is typed by site group, so its areas are in the region doc):

| habitat key | Trentino types (label) | South Tyrol groups | Trentino ha (share), median m |
|---|---|---|---|
| `fir_spruce` | peccete (PE, PEX), abieteti (AB) | Peccete subalpine, Peccete montane, Piceo-abieteti | 157,088 (40.1 %), 1,454 |
| `other_conifer` | lariceti (LA, LAX), larici-cembrete (LC), cembrete (CB) | Larici-cembrete, Lariceti | 62,526 (16.0 %), 1,824 |
| `beech` | faggete (FA, except FA_con) | Faggete | 46,990 (12.0 %), 1,097 |
| `mountain_pine` | pinete di pino silvestre o nero (PS) | Pinete | 34,720 (8.9 %), 917 |
| `mixed_broadleaf` | orno-ostrieti (OO), aceri-frassineti and aceri-tiglieti (AF, AT), formazioni transitorie (TR) | Orno-ostrieti, Boschi di latifoglie | 31,271 (8.0 %), 792 |
| `transitional_woodland_shrub` (not woodland) | mughete (MU), ontano verde (OA) | Mughete e bassofusti di ontano verde | 22,459 (5.7 %), 1,857 |
| `mixed_broadleaf_conifer` | faggeta mesalpica con conifere (FA_con) | Piceo-abieti-faggete, Querco-pinete | 15,286 (3.9 %), 1,276 |
| `deciduous_oak` | ostrio-querceti (OQ), querceti (QR, QC) | Querceti (with chestnut in places) | 12,646 (3.2 %), 599 |
| `exotic_broadleaf` | robinieti (RO) | — | 4,965 (1.3 %), 667 |
| `evergreen_oak` | lecceta (LE, Alto Garda) | — | 1,739 (0.4 %), 345 |
| `riparian` | ontanete (OB, ON) | Boschi ripariali | 1,342 (0.3 %), 1,105 |
| `chestnut` | castagneti (CS) | — | 754 (0.2 %), 730 |
| `mediterranean_pine`, `macchia` | — | — | absent |

Chestnut is nearly absent from both maps: in Trentino it is typed onto the category it replaced
("castagneto su …", `taa_pat_tipi_forestali_2018`), and South Tyrol's oak-chestnut woods are
mapped as `deciduous_oak`. So chestnut-bound porcini and ovoli lean on the oak and pine classes
here.

**Altitude belts.**
- Trentino (`taa_pat_tipi_forestali_2018`):
  - montane beech "tra 1000 e 1500 m", high beech 1,400-1,800 m;
  - fir from about 600 m to about 1,600 m, at most over 1,800 m;
  - spruce from 900-1,000 m to "intorno ai 2000 m, con punte massime sino a 2200 m";
  - stone pine from 1,500 m to over 2,300 m (best at 1,800-2,100 m), larch woods "raramente
    superano i 2100-2200 m";
  - secondary larch woods lie below 1,500-1,600 m, or to 1,800-1,900 m, "su potenziale pecceta".
- South Tyrol (`taa_bz_waldtypisierung2010`):
  - submontane "sonnseitig von rund 750 bis max. 1150 m";
  - high-montane spruce and fir 800-1,600 m on shady and 1,000-1,800 m on sunny slopes;
  - subalpine spruce from 1,450-1,600 (1,700) m shady and 1,600-1,900 m sunny, a 200-400 m belt;
  - then "der hochsubalpine Lärchen-Zirbenwald".
- On the grid: woodland median 1,407 m, p95 1,992 m, max 2,427 m.

**Climate.**
- South Tyrol's annual rain runs from 650 mm (the Vinschgau; under 600 mm in its larch zone) to
  1,200 mm in the Staulagen of the Passeier, Pflersch and Ridnaun valleys and the Dolomites
  (`taa_bz_waldtypisierung2010`).
- Trentino runs from the submediterranean Garda and Adige floor to "clima rigido e continentale"
  in the endalpic valleys (`taa_pat_tipi_forestali_2018`).
- The press blames wind as often as drought: "Zu trocken, zu windig, zu heiß" (2021); "Die
  Trockenheit, der Wind, die hohen Temperaturen" (2022); in Trentino "Luglio è stato pessimo per
  il freddo e soprattutto per il clima ventoso che secca lo strato superficiale del terreno"
  (l'Adige, 2021-09-22). See Press contrasts.

**Picking rules.** None of them changes where or when the fungi fruit, so none is encoded.
- **Trento** (`taa_pat_funghi_raccolta`, `taa_pat_funghi_limite_2025`): L.P. 11/2007 and its
  decree D.P.P. 23/2009; 7:00-19:00, "due chilogrammi al giorno per persona", raised to 3 kg from
  2 August 2025; no calendar, no species rule found.
- **Bolzano** (`taa_bz_pilzesammeln`, `taa_bz_pilzsammelgebuehr2024`):
  - the law is L.P. 18/1991 (the card's "3/1991" did not match the Forstdienst's page);
  - picking only on even calendar days, 7-19 h;
  - 2 kg in the home comune, 1 kg with the paid permit, 3 kg on one's own land;
  - banned in Karneid, Tiers, Welschnofen and on the Kohlern.
- The even-day rule halves South Tyrol's picking days, which thins sightings, not scores.

## Sightings (occurrence cross-check)

Queried 2026-09-26 (`mushma_occurrence_check_taa_2026`). Aggregates only; no coordinates are
stored.
- **GBIF** with `gadmGid=ITA.17_1`: almost all its records are iNaturalist copies (*B. edulis* 154
  of 162), plus NABU naturgucker, Observation.org and a few herbarium specimens.
- **iNaturalist** place 10874 (Trentino-Alto Adige, the id the region config uses), verifiable
  records; province splits from places 33199 (Trento) and 33198 (Bolzano).
- **Elevations** from Copernicus GLO-90 (the Open-Meteo elevation API had hit its daily limit),
  for records that are not obscured and have an accuracy of 1 km or better.
- **Enrichment** = the taxon's monthly share ÷ the monthly share of all 30,261 fungi records of
  the region, whose effort peaks in August (23.8 %), then September (18.4 %) and July (15.7 %).
- **Census** = the north-east Italian census pages (`muse_censimento_*`, `taa_muse_censimento_*`):
  their relative monthly profiles (all three regions of the north-east) and the map squares
  counted inside each province.

| taxon | records (TN / BZ) | M | J | J | A | S | O | N |
|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 455 (360 / 95) | 1 | 3 | 101 | 205 | 117 | 26 | 2 |
| | enrichment | 0.0 | 0.1 | 1.4 | 1.9 | 1.4 | 0.4 | 0.1 |
| *B. reticulatus* | 42 (29 / 13) | | 10 | 15 | 12 | 5 | 0 | |
| | enrichment | | 2.7 | 2.3 | 1.2 | 0.6 | 0 | |
| *B. aereus* | 3 (2 / 1) | | | | 2 | 1 | | |
| *B. pinophilus* | 45 (32 / 13) | 3 | 6 | 7 | 12 | 9 | 8 | |
| | enrichment | 1.0 | 1.5 | 1.0 | 1.1 | 1.1 | 1.3 | |
| *A. caesarea* | 12 (8 / 4) | | | 2 | 4 | 4 | 1 | |
| *Cantharellus* | 206 (127 / 79) | 1 | 12 | 74 | 72 | 31 | 10 | 3 |
| | enrichment | 0.1 | 0.6 | 2.3 | 1.5 | 0.8 | 0.4 | 0.5 |

Winter records (not in the table): *A. caesarea* 1 in January, *Cantharellus* 2 in January and 1
in March, all probably misdated or dried.

| taxon | located (TN / BZ) | min | p10 | median | p90 | max (m) |
|---|---|---|---|---|---|---|
| *B. edulis* | 227 (154 / 73) | 499 | 1,022 | 1,406 | 1,810 | 2,170 |
| *B. reticulatus* | 26 (16 / 10) | 501 | 665 | 931 | 1,275 | 1,945 |
| *B. aereus* | 1 | | | 1,650 | | |
| *B. pinophilus* | 29 (22 / 7) | 725 | 988 | 1,270 | 1,567 | 1,927 |
| *A. caesarea* | 6 (2 / 4) | 484 | | 709 | | 906 |
| *Cantharellus* | 161 (93 / 68) | 243 | 849 | 1,347 | 1,727 | 2,161 |

**Half-months by elevation** (located records):

| taxon | band (n) | Jul 1-15 | Jul 16-31 | Aug 1-15 | Aug 16-31 | Sep 1-15 | Sep 16-30 | Oct 1-15 | Oct 16-31 | Nov |
|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | < 1,000 m (20) | 0 | 5 | 3 | 2 | 6 | 3 | 1 | 0 | 0 |
| | 1,000-1,300 m (55) | 4 | 8 | 7 | 2 | 14 | 15 | 3 | 0 | 1 |
| | 1,300-1,600 m (87) | 4 | 12 | 12 | 27 | 17 | 11 | 2 | 2 | 0 |
| | ≥ 1,600 m (65) | 2 | 7 | 14 | 19 | 10 | 5 | 6 | 0 | 1 |
| *Cantharellus* | < 1,000 m (27) | 6 | 3 | 2 | 2 | 3 | 2 | 1 | 1 | 2 |
| | 1,000-1,300 m (47) | 5 | 16 | 11 | 6 | 5 | 1 | 0 | 0 | 0 |
| | 1,300-1,600 m (53) | 11 | 6 | 12 | 10 | 7 | 4 | 0 | 0 | 0 |
| | ≥ 1,600 m (34) | 4 | 12 | 6 | 7 | 3 | 0 | 0 | 2 | 0 |

(*B. edulis* June: 1 at 1,000-1,300 m and 1 at 1,600 m or higher; *Cantharellus* June: 3, 3, 3
and 0 by band.)

**Species inside *Cantharellus*** (iNaturalist): *C. cibarius* 169 (located median 1,374 m), genus
only 15, *C. friesii* 8, *C. pallens* 8 (median 918 m), *C. amethysteus* 5, *C. enelensis* 1. As
in Piemonte, the chanterelle of the region is *C. cibarius* s.str.

**Census map squares** (north-east census; squares inside each province):

| taxon | Trentino | South Tyrol |
|---|---|---|
| *B. edulis* | 91 | 41 |
| *B. aestivalis* (*reticulatus*) | 51 | 11 |
| *B. aereus* | 6 | 0 |
| *B. pinophilus* | 36 | 15 |
| *A. caesarea* | 17 | 6 |
| *C. cibarius* | 388 | 41 |

The census is Trentino-heavy (the Trento federation's own survey), so the province split says
little; the absence of *B. aereus* squares in South Tyrol is still worth noting.

**Caveats.**
- **Presence-only records**, near trails and huts; summer hikers raise the Alpine effort in
  July-August, which the enrichment divides out only in part.
- **Obscured porcini.** 187 of the 455 *B. edulis* records are obscured by their observers and
  left out of the elevations and the half-months.
- **Recent years.** 381 of the 455 *B. edulis* records are from 2020 on, 53 of them from 2026.
- **Priors, not fits.** The season, band and habitat choices were drawn partly from these same
  records, all years included, so they stay frozen priors.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Records** (analysis, above). *B. edulis* peaks in August (1.9× the effort) with July and
  September at 1.4×; October is 0.4× and November nothing to speak of. *B. reticulatus* is a June-July
  porcino (2.7×, 2.3×) that fades in September and is absent in October. *B. pinophilus* holds 1.0-1.5×
  in every month from May to October.
- **Census** (society; `muse_censimento_edulis`, `muse_censimento_pinophilus`,
  `taa_muse_censimento_aestivalis`, `muse_censimento_boletus`):
  - *B. edulis* to 2,175 m, its maximum a Trentino record of 2 September 2019; collections
    "Sotto Picea abies" at Vetriolo (1,500 m) and at Piné (930 m, 1926); its north-east profile
    peaks in August and ends with a record on 3 November.
  - *B. pinophilus*: "Tra le specie del genere Boletus è quella più precoce e più tardiva";
    "pur essendo frequentemente legato al pino silvestre" also with other trees, broadleaves
    included; earliest 12 May and latest 28 October, both at Baselga di Piné in spruce and Scots
    pine at 910-1,120 m; to 1,898 m.
  - *B. aestivalis* (*reticulatus*) to 1,927 m in Trentino (29 August 2010); its profile runs
    May to October with a July peak.
  - *B. aereus* "può essere comunque occasionalmente reperito anche nelle regioni alpine, in
    habitat idonei"; to 1,250 m; one 1926 collection at Piné (930 m).
- **Larch and stone pine** (peer-reviewed, strong for the absence of a porcini mycorrhiza):
  - larch root tips at 1,700-1,900 m at Prettau (Predoi, Ahrntal) and in the Schnalstal held 68
    ectomycorrhizal species, dominated by larch specialists, and no *Boletus* or *Cantharellus*,
    although the Prettau stands "were interspersed with Pinus cembra and Picea abies individuals"
    (`taa_mandolini2025_larix`);
  - stone pine root tips at four South Tyrolean sites held none either; "The P. cembra bolete
    (Suillus plorans) is the most important symbiotic partner" (`taa_mandolini2024_cembra`);
  - what larch cells hold besides larch is spruce: secondary larch woods stand "su potenziale
    pecceta", sometimes with "una struttura biplana di larice su peccio o abete"
    (`taa_pat_tipi_forestali_2018`).
- **Where the records sit** (analysis, `mushma_taa_forest_check_2026`):
  - on the region grid, *B. edulis* record cells at 1,500 m or higher are 21 % larch and stone
    pine and 74 % spruce and fir, against 27 % and 67 % over the woodland there;
  - Trentino's forest-type map within 500 m of the 91 Trentino records at 1,000-1,500 m: 62 %
    spruce, 20 % fir, 8 % beech, against 30 %, 22 % and 25 % of the woods there;
  - below 1,000 m (11 records) the hop-hornbeam woods hold 4 % of the surroundings against 27 % of
    the woods;
  - *B. pinophilus* (16 records at 1,000-1,500 m): Scots pine 18 % against 8 %.
- **Local voices** (folklore):
  - "In einigen Jahren hat die Pilzsaison schon Mitte Juli begonnen" (`taa_orf_tirol_2019_08_09`);
  - in 2021 a Fiemme mycologist: "Un tempo i funghi si trovavano di più a fondovalle, intorno agli
    800 metri. Oggi fa più caldo, e bisogna salire fino ai 1500 metri di quota" (l'Adige,
    2021-09-22), in line with the uphill shift of Alpine fruiting since 1960 (`diez2020_alps`,
    peer-reviewed, strong for the direction only).

**Decisions** (numbers in the table above; the full reasoning is in each factor's `notes`):

- ***B. edulis* season: one window.**
  - **What:** full from 15 July to 30 September, closed by 31 October, at every elevation.
  - **Why one window:** Piemonte and Lombardia split the window by elevation because their high
    records stopped earlier. Here the start and the end do not move with elevation: the first
    half of October holds 4 records below 1,300 m and 6 at 1,600 m or higher, the second half
    none in either. Only the peak moves (September low, August high), and the air-temperature
    rule and the growth clock, which read each cell's own weather, make that shift.
  - **Why the autumn tail is cut:** October is 0.4× and November 0.1× the effort. The Tuscan
    window, full to 15 November, would leave the gate open where only frost and snow could close
    it.
- ***B. edulis* altitude:**
  - **What:** full from 500 m to 1,900 m, zero at 200 m and 2,300 m.
  - **Why the top:** the records reach 2,170 m and the spruce and larch-stone pine woods
    2,200-2,300 m.
  - **Why the bottom:** the valley floors hold orchards, vineyards, riparian woods and robinia,
    and the lowest hosts are chestnut and Scots pine on the slopes.
- ***B. edulis* larch (0.3 → 0.1)** (Lombardia reached the same value on its own evidence;
  Piemonte kept 0.3):
  - larch itself is no *Boletus* partner, and the class holds nothing else here;
  - a pure larch cell now gets a third of full credit, and one with a quarter of spruce full credit;
  - on the grid the gate at 0.1 averages 0.98 at the records above 1,500 m and 0.95 over the
    woodland; at 0.3 it was 1.00 for both and told them apart not at all.
- ***B. edulis* beech kept at 1.0** although the records sit in beech less than the woods do.
  Beech is a documented host (a north-east census collection in a "Bosco di faggio" at 800 m),
  and the records' spruce bias may be where people walk.
- **Transitional woodland/shrub (0.3 or 0.6 → 0.1) for all four porcini:** here the class is
  mountain-pine krummholz and green alder at 1,500-2,200 m, which the region config keeps out of
  the woodland mask but in the habitat mix. Neither is a porcini host, and they hold 5 % of the
  surroundings of the Trentino *B. edulis* records above 1,500 m against 14 % of the woods.
- ***B. reticulatus*:**
  - season full to 15 September, closed by 20 October;
  - band up 200 m, to the montane beech and fir (full to 1,300 m, zero at 1,700 m);
  - hosts kept: beech, spruce/fir and Scots pine were already secondary, and they are where the
    records sit (Trentino surroundings: spruce 29 %, beech 18 %, Scots pine 18 %, fir 11 %).
- ***B. aereus*:**
  - one window, full 15 August to 20 October, closed by 20 November; the Tuscan upland/lowland
    split came from the Apennine IGP uplands and the macchia, which the region lacks;
  - zero at 1,100 m; the 1,650 m record in spruce is left out as a likely misidentification.
- ***B. pinophilus*:**
  - one window from May to early November, with no summer gap;
  - Scots pine becomes a full host, larch non-host;
  - band from 700 m to 1,800 m, zero at 400 m and 2,200 m.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Census** (society; `taa_muse_censimento_caesarea`):
  - 17 map squares in Trentino (Pergine, Trento, the Val di Cembra, Vallagarina, the Brentonico
    plateau) and 6 in South Tyrol (Oltradige, Bassa Atesina, Lana, the Renon and Castelrotto
    slopes);
  - collections: Gocciadoro (Trento, 200 m, 1900); Appiano (665 m, 1924-1925); Piné (930 m,
    1926); Lago di Restel near Pergine, "A lato di una strada, sotto pino e quercia" (880 m,
    2002); Capriana, "Bosco misto con presenza di querce" (1,050 m, 2014);
  - its highest record: Capriana, 1,300 m, in a "Bosco misto di pino, abete rosso e larice";
  - the north-east profile, on the census's relative scale: July 58, August 200, September 179,
    October 146, November 8.
- **Records:** 12 iNaturalist (July 2, August 4, September 4, October 1), 6 located at 484-906 m
  (Bolzano, Caldaro, Pergine, Tesimo, Barbiano, Baselga di Pinè), their Trentino surroundings 39 %
  Scots pine and 36 % robinia.
- **Belts:** in South Tyrol the colline belt holds "Eichen-Kiefernwälder und
  Eichen-Kastanien-Mischwälder" up to about 750 m, and the submontane belt runs "sonnseitig von
  rund 750 bis max. 1150 m" (`taa_bz_waldtypisierung2010`). In Trentino the sessile oak woods,
  "tipici di pendici povere e secche", are "spesso in contatto e in rapporto di sostituzione con
  formazioni a dominanza di pino silvestre" (`taa_pat_tipi_forestali_2018`).
- **A forager limit** of "oltre i 600 metri al Nord Est" (`funghimagazine_ovolo`, folklore) is
  exceeded by the records here: the warm belts sit higher in the inner Alpine valleys.
- **No press claim** about ovoli in the region was found (see Press contrasts).

**Decisions.**
- **Season** full from 15 July to 30 September, closed by 31 October (Tuscany: full September to 5
  November). The June ramp stays for storm flushes; the cold-night and soil-temperature rules
  end the tail.
- **Altitude:** full to 900 m, zero at 1,200 m (Tuscany: 750 → 1,100 m).
- **Hosts:**
  - mountain pine 0.0 → 0.3: below 1,000 m it is Scots pine mixed with oak, where the ovolo is
    collected; the host is the oak inside it, hence marginal, as for mixed broadleaf;
  - South Tyrol's *Querco-pinete* map to `mixed_broadleaf_conifer`, already 0.3;
  - transitional 0.6 → 0.1: here it is subalpine scrub, far above the band;
  - robinia stays at 0.05, although it holds a third of the Trentino records' surroundings: it
    replaced chestnut and oak but is no host.

## Gallinacci (*Cantharellus* s.l.: "finferli", "gallinacci", "Pfifferlinge")

**Regional evidence.**
- **Which chanterelle.** *C. cibarius* s.str. is 169 of 191 species-level records. The census
  collections of the region are all in conifer woods: "Bosco misto con prevalenza di abete rosso"
  at 1,350 and 1,420 m, "Bosco subalpino di conifere" at 1,700 m (Rabbi), "Bosco misto con
  prevalenza di pino silvestre" at Piné (910 m) (`muse_censimento_cibarius`).
- **Records.**
  - July is 2.3× the effort, August 1.5×, September 0.8×, October 0.4×.
  - Above 1,000 m: 15 records in the first half of September, 5 in the second, 2 in October.
  - Below 1,000 m the 27 records spread from 25 May to 6 November.
- **Hosts from the records** (Trentino surroundings, `mushma_taa_forest_check_2026`):
  - at 1,000-1,500 m: spruce 62 % against 30 % of the woods, fir 14 % against 22 %, beech 7 %
    against 25 %;
  - below 1,000 m: spruce 34 % against 11 %, Scots pine 15 % against 21 %, hop-hornbeam 8 %
    against 27 %;
  - on the grid, record cells at 1,500 m or higher are 14 % larch and stone pine against 27 % of
    the woodland there.
- **Larch:** no *Cantharellus* on South Tyrolean larch or stone pine roots (`taa_mandolini2025_larix`,
  `taa_mandolini2024_cembra`).
- **Press:** in 2023 "distese di finferli" in the Val Pusteria, the season "iniziata bene già alla
  fine di luglio" (`taa_altoadige_2023_08_08`).

**Decisions.**
- **Hosts:**
  - fir/spruce to host (1.0);
  - Scots pine to secondary (0.6);
  - larch and stone pine to non-host (0.1);
  - transitional (subalpine scrub) to non-host (0.1).

  Beech stays secondary: it is a documented chanterelle host elsewhere, but the records here sit
  in it less than the woods do. Mixed broadleaf and deciduous oak stay marginal; chestnut and holm oak
  stay host but are nearly absent.
- **Season:**
  - lowland window full to 31 October, closed by 30 November, with no winter mode;
  - mountain window full to 15 September, closed by 20 October;
  - the handover stays at 600-1,000 m, because the 1,000-1,300 m records already behave like
    mountain ones;
  - the disabled two-flush rule ends on 30 November too.
- **Altitude:** full to 1,700 m, zero at 2,100 m.
- **Soil pH and lithology stay disabled.** The grid's woodland pH is a median 6.28, lowest under
  spruce and fir (5.90) (`regions/trentino_alto_adige.md`). A pH rule would therefore mostly
  repeat the spruce preference; compare it in the backtest before enabling.

## Keys and groups dropped

None. Every key has regional records and a regional source.
- ***B. aereus*** is the weakest key (3 records, 6 census squares, none in South Tyrol). It is kept
  for Trentino's low woods, where it can only raise the porcini group score.
- **Ovoli** are rare but present in both provinces.
- **Absent habitat keys.** `mediterranean_pine` and `macchia` are absent, and `evergreen_oak` is a
  few Garda cliffs. Their affinities are left as Tuscany's rather than invented; they cannot
  affect a score here.

## Weather rules: why none changed

- **No regional numbers.** No study from the region gives a rain amount, lag or temperature
  threshold for these taxa. The Tuscan set already rests on temperate evidence (Swiss plots,
  German beech, Amiata).
- **Alpine cold.** The frost, snow, cold-night, air- and soil-temperature rules and the growth
  clock read each cell's own downscaled weather, so they slow and end the season at altitude.
  They are also what shifts the *B. edulis* peak from September at 1,000 m to August at 1,800 m
  (see Porcini).
- **Dry inner valleys, wet margins.** From under 600 mm in the Vinschgau larch zone to 1,200 mm and
  more on the southern and northern margins:
  - the porcini 30-day rain is a percentage of each cell's normal, so it adapts;
  - the absolute 30-day ramps of ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full less
    often in the Vinschgau, where ovoli are absent and chanterelle records are few.
- **Wind.** The press blames dry wind with heat (2021, 2022). The ET0-based drying rules are the
  only stand-in; the known gap `drying_wind` (gusts plus low humidity) would suit this region.
- **Rain scale.** `precipitation_scale` was fitted on Tuscan gauges; the check against Bolzano's
  and Trento's gauges is a region-config task (`regions/trentino_alto_adige.md`), not a species one.

## Slope and sun exposure

- **Slope, every key.** The band moves onto the region grid by the Tuscan rule: x1 up to about the
  woodland p90, x0.8 from about the maximum.
  - The 7,698 woodland cells run p10 17.6°, median 26.9°, p75 31.0°, p90 34.5°, max 44.7°
    (Trentino and South Tyrol alike, p90 34.8° and 34.1°); 62 % are steeper than 25°.
  - So x1 to 35° and x0.8 from 45°, as Piemonte (34/45) and Lombardia (35/46) did.
- **Sun exposure, kept.** On 15 October the woodland cells below 1,000 m run p10 73 %, median 98
  %, p75 110 %, p90 121 % of flat ground's sun (Tuscany 89/100/105/110 %).
  - The dry-side stoppers of *B. edulis* and *B. pinophilus* (x1 to 105 %) therefore dock about a
    third of the low woods, and the shade-side ones of *B. reticulatus*, *B. aereus* (≤ 80 %:
    about a fifth) and ovoli more than in Tuscany.
  - The bands are statements about sun and drying, not Tuscan percentiles, so they are kept; each
    file's `notes` says so and the backtest can test them.

## Press contrasts (`sanity.yaml`)

`trentino_alto_adige/sanity.yaml` holds 16 contrasts, written down on 2026-09-26 before the region
had any scores: 14 porcini and 2 gallinacci (ids starting `gallinacci_`, read with `--group
gallinacci`). No ovoli claim was found.
- **Sources.** Two research agents searched the Italian and the German press. I opened every main
  source and every quoted second source and checked each quote against the page's text.
- **Areas.** 13 areas, by ISTAT 2025 comuni or province sigle (TN, BZ, `*` for the region). Every
  name was checked against the region grid, which carries ISTAT's bilingual forms for South Tyrol
  ("Brunico/Bruneck"), so the file uses them. The card's example names ("Brunico", "Malles
  Venosta") would match no cell.
- **Normal:** 2017-2025.

| area | woodland cells | median elevation |
|---|---|---|
| `fiemme` (8 comuni) | 293 | 1,588 m |
| `alta_valsugana` (Levico, Pergine, Caldonazzo, Mocheni valley, Piné, Bedollo) | 207 | 1,209 m |
| `valsugana_tesino` (17) | 401 | 1,325 m |
| `southern_trentino` (Idro, Garda, Ledro, Rovereto-Pasubio, Ala, Avio: 15) | 641 | 1,020 m |
| `vallagarina_low` (10 valley comuni) | 123 | 871 m |
| `western_valleys` (Val di Sole, Val di Non, Val Venosta: 48) | 1,147 | 1,579 m |
| `dolomites` (Fiemme, Fassa, Primiero, Val Gardena, Val Badia: 26) | 910 | 1,634 m |
| `pusteria` (20) | 750 | 1,637 m |
| `isarco_wipptal` (17) | 645 | 1,556 m |
| `trentino`, `south_tyrol`, `south_tyrol_without_east`, `region` | 4,002, 3,696, 3,259, 7,698 | 1,275, 1,541, 1,509, 1,407 m |

**How far to trust them.**
- **Weekly bulletins.** Six contrasts rest mainly on Funghi Magazine (FM). It is one writer who
  mixes readers' reports with rain-gauge reasoning, so those partly test the rain data (flagged
  "rain-led" below).
- **Local mycologists.** The Trentino contrasts rest mostly on l'Adige and il Dolomiti quoting the
  Gruppo Micologico Bresadola and valley groups.
- **Province-wide sources.** The South Tyrolean ones rest on the Tageszeitung, Alto Adige, ORF and
  stol.it leads, mostly province-wide.
- **Opposite pairs.** Two cross-province contrasts go opposite ways in consecutive Julys (2024
  Trentino ahead, 2025 South Tyrol ahead), so a constant bias between the provinces cannot pass
  both.

| id | higher | lower | window | main source | second sources | caveats |
|---|---|---|---|---|---|---|
| `fiemme_2019_2021` | Fiemme 2019 | Fiemme 2021 | 08-20 → 09-20 | [Trentino, 2019-11-07](https://www.giornaletrentino.it/cronaca/fiemme-e-fassa/nonostante-la-tempesta-vaia-ottima-annata-per-i-fungaioli-1.2175281): "scarsa crescita nei mesi di giugno-luglio, mentre molto meglio sono andati i mesi di agosto e settembre" (Magnifica Comunità di Fiemme) | [l'Adige, 2021-09-22](https://www.ladige.it/cronaca/funghi-e-una-stagione-scarsa-ma-ci-sono-ancora-speranze-o-e-gia-finita-nbdtqrvo): porcini "un paio di volte, e poi basta ... la stagione è stata misera misera" (Cavalese-Predazzo mycologist) | storm Vaia closed some 2019 zones; FM (2021-08-15) put Fiemme among the best areas in mid-August 2021, hence the 20 August start |
| `alta_valsugana_2020_2021` | Alta Valsugana 2020 | same, 2021 | 08-20 → 09-25 | [l'Adige, 2020-09-10](https://www.ladige.it/territori/pergine/funghi-una-buona-stagione-agosto-doro-e-purtroppo-anche-i-primi-intossicati-jm5241fz): "Soprattutto ad agosto ... c'è stata una buona raccolta" | [l'Adige, 2020-09-26](https://www.ladige.it/montagna/freddo-e-nevicate-in-quota-ma-nella-neve-ci-sono-ancora-le-ultime-brise-di-stagione-b5po3kye) (Vezzena: "una stagione davvero fortunata"); l'Adige 2021-09-22: "ottima fino alla metà di agosto, poi un 'rebalton' meteorologico"; [FM, 2021-08-15](https://funghimagazine.it/funghi-trentino-alto-adige-16-08-2021-dove-cercarli-dopo-ferragosto/): "Segni di cedimento delle nascite appunto in Valsugana, Baselga di Pine'" | 2020 side is a group secretary and a reader's photo |
| `trentino_july_2023_2022` | Trentino 2023 | Trentino 2022 | 07-10 → 07-31 | [il Dolomiti, 2023-08-02](https://www.ildolomiti.it/societa/2023/raccolta-dei-funghi-per-evitare-di-imbattersi-in-quelli-velenosi-succede-piu-frequentemente-di-quel-che-si-pensi-ce-la-casetta-di-piazza-vittoria): July "così ricco ... la raccolta estiva di quest'anno è iniziata prima" (Bresadola) | [il Dolomiti, 2022-07-20](https://www.ildolomiti.it/ambiente/2022/troppo-caldo-e-siccita-e-i-funghi-nei-boschi-non-ci-sono-lesperto-speriamo-nella-pioggia): "quasi completa assenza di funghi" | the 2023 article also says Trentino started "con un po' di ritardo rispetto alle altre regioni"; Trentino only, since South Tyrol had "l'assenza pressoché totale di funghi" in mid-July 2023 (Alto Adige, 2023-07-22, read by an agent) |
| `vallagarina_low_2024` | Vallagarina floor comuni, normal | same, 2024 | 07-20 → 08-02 | [l'Adige, 2024-08-02](https://www.ladige.it/montagna/pochi-funghi-e-non-si-capisce-il-perche-i-micologi-aspettano-ancora-la-buttata-giusta-di-agosto-kt7e89th): "butta male ... In questo periodo, di solito, ce ne sono tanti"; "Nascite di porcini assenti nel fondovalle ... e nelle zone collinari" (Gruppo Barbacovi) | — | the same report has summer porcini "insolitamente presenti" above 1,000 m, and the valley comuni reach that high; Ala and Avio left out for that reason |
| `region_early_august_2025` | region 2025 | region, normal | 07-25 → 08-08 | [l'Adige, 2025-08-13](https://www.ladige.it/cronaca/il-caldo-fermera-pure-i-funghi-ma-finora-e-unottima-stagione-u1uiizgw): "Fino alla settimana scorsa la raccolta è andata bene", "finora è un'ottima stagione" (Bresadola) | [FM, 2025-08-21](https://funghimagazine.it/aggiornamento-nascite-funghi-22-08-2025/): "la grande buttata che ha interessato soprattutto Trentino-Alto Adige", "Porcini ovunque"; [Alto Adige, 2025-08-10](https://www.altoadige.it/cronaca/bressanone-il-porcino-da-record-da-1-5-chilogrammi-1.4146223) (Bressanone) | heat ended it about 8 August; the Val di Sole group called mid-August poor (La Voce del Trentino, 2025-08-17, read by an agent) |
| `west_vs_dolomites_2023` | western valleys 2023 | Dolomites 2023 | 09-25 → 10-12 | [FM, 2023-10-04](https://funghimagazine.it/aggiornamento-porcini-04-10-2023/): "a volontà, tranne che sulle Dolomiti, dov'è piovuto meno" | [FM, 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "assai bene sui settori occidentali e settentrionali del Trentino A.A, molto meno ... su tutte le Dolomiti" | FM only, rain-led; the higher side is my reading of "occidentali" (Sole, Non, Venosta) |
| `valsugana_vs_southern_trentino_2023` | Valsugana-Tesino 2023 | southern Trentino 2023 | 08-01 → 08-10 | [FM, 2023-08-10](https://funghimagazine.it/aggiornamento-funghi-10-08-2023/): "Una flessione ... sui settori Sud del Trentino, tra Lago d'Idro e Lago di Garda, zona di Rovereto-Pasubio e Lessinia. Meglio dalla Valsugana all'Agordino" | [FM, 2023-08-24](https://funghimagazine.it/aggiornamento-nascite-porcini-24-08-2023/): "in drastica diminuzione o già assenti ... a Sud di Trento" | FM only |
| `south_tyrol_september_vs_august_2023` | South Tyrol, 12-25 Sep 2023 | South Tyrol, 1-17 Aug 2023 | two windows, one year | [FM, 2023-09-20](https://funghimagazine.it/aggiornamento-porcini-20-09-2023/): Bolzano among "le province con ottime nascite in corso" | FM 2023-08-10: "Le nascite di Porcini restano scarse e localmente anche assenti su tutto il Sud Tirolo" | FM only; both windows lie inside the full *B. edulis* season, so it tests the weather rules |
| `isarco_2025_2023` | Isarco-Wipptal 2025 | same, 2023 | 08-01 → 08-17 | Alto Adige, 2025-08-10: "i funghi stanno spuntando abbondanti" (Bressanone) | FM 2023-08-10: "Scarse anche da Bolzano a Bressanone-Vipiteno e Brennero" | the 2025 line is about "funghi" in a record-porcino story |
| `south_tyrol_2021_poor` | South Tyrol, normal | same, 2021 | 08-01 → 09-15 | [Tageszeitung, 2021-10-04](https://www.tageszeitung.it/2021/10/04/schlechtes-pilzjahr/): "Zu trocken, zu windig, zu heiß"; "Steinpilze gab es hingegen extrem wenige oder teilweise sogar keine" (Karl Kob) | FM 2021-08-19 (read by an agent) | one expert; 27 fines as a proxy |
| `south_tyrol_2019_late` | South Tyrol, normal | same, 2019 | 07-15 → 08-08 | [ORF Tirol, 2019-08-09](https://tirol.orf.at/stories/3007859/): "Späte Pilzsaison in Südtirol"; "bisher nur wenige Schwammerln" | Alto Adige 2019-08-13 (read by an agent): "In questo periodo ci sono pochi porcini e finferli" | a stol.it lead of 2019-07-29 has "ideale Bedingungen", apparently release boilerplate |
| `trentino_vs_south_tyrol_august_2019` | Trentino 2019 | South Tyrol without its eastern valleys, 2019 | 08-05 → 08-16 | [FM, 2019-08-16](https://funghimagazine.it/buone-nascite-di-funghi-porcini-vediamo-dove-le-piogge-caduta-in-italia/): "La provincia di Bolzano perciò, tolte alcune aree orientali, risulta di molto più improduttiva rispetto a quella di Trento" | l'Adige [2019-08-17](https://www.ladige.it/territori/giudicarie-rendena/confiscato-un-quintale-di-funghi-ai-cercatori-appassionati-ma-ingordi-saranno-regalati-alle-case-di-riposo-dpsh3tqa) ("eccezionalmente buono", Giudicarie) and [2019-08-23](https://www.ladige.it/territori/non-sole/in-un-giorno-confiscati-133-kg-di-porcini-un-fungaiolo-ne-aveva-29-chili-e-mezzo-nascosti-nel-vano-della-ruota-ysyenszh) ("copiosa produzione", upper Val di Non) | rain-led; "aree orientali" read as Val Badia and the upper Pusteria |
| `trentino_vs_south_tyrol_july_2024` | Trentino 2024 | South Tyrol 2024 | 07-15 → 07-25 | [FM, 2024-07-25](https://funghimagazine.it/aggiornamento-funghi-25-07-2024/): "Soprattutto in Trentino ... buone o persino già ottime nascite di Porcini edulis ... Più timide le nascite di edulis in Alto Adige" | — | FM only; the Vallagarina floor was poor at the same time (see above) |
| `south_tyrol_vs_trentino_july_2025` | South Tyrol 2025 | Trentino 2025 | 07-01 → 07-12 | [FM, 2025-07-10](https://funghimagazine.it/aggiornamento-nascite-funghi-11-18-luglio-2025/): "tutto l'Alto Adige: in piena fase positiva ... i primi edulis!"; "Trentino: ha sofferto di più il gran caldo, specie nei fondovalle dell'Adige" | — | FM only, partly a forecast |
| `gallinacci_pusteria_2023_2022` | Pusteria 2023 | same, 2022 | 07-25 → 08-08 | [Alto Adige, 2023-08-08](https://www.altoadige.it/cronaca/bolzano/funghi-stagione-esplosa-ma-attenzione-ai-velenosi-1.3559689): "distese di finferli ... val Pusteria e valli limitrofe", "temperature gradevoli e non torride come lo scorso anno" (Bresadola, Bolzano) | [stol.it, 2022-07-15](https://www.stol.it/artikel/chronik/noch-herrscht-flaute-im-korb) (lead): "bisher gibt es im Wald wenig zu holen – außer einigen Pfifferlingen" | one expert; the 2022 side is province-wide and mid-July |
| `gallinacci_trentino_2024_2025` | Trentino 2024 | Trentino 2025 | 07-10 → 07-27 | [l'Adige, 2025-07-27](https://www.ladige.it/cronaca/raccolta-funghi-limite-a-tre-chili-lesperto-potrebbe-essere-una-buona-stagione-rgjl6zqp): "rispetto allo scorso anno sembra diminuita la quantità di finferli" (Bresadola) | FM 2024-07-25: "al Nord abbondano solamente Finferli-Galletti"; l'Adige 2024-08-02: finferli "ben presenti dai colli ai monti lagarini" | one expert's impression |

**Left out:**
- **Weak or conflicting:**
  - the upper Val di Non 2019 against 2021 (confiscations, which count pickers as well);
  - Trentino 2019 against 2020 for porcini and 2020 against 2019 for finferli (one interview, in
    conflict with Fiemme and Pergine);
  - the Fiemme 2019 zones (a whole-season list of places, confounded by storm Vaia);
  - Val di Sole mid-August 2025 (it contradicts the province-wide reports of the same weeks).
- **FM statements too vague to place:** Fiemme and Primiero against the Valsugana in mid-August
  2021; the Dolomites against the west of the Adige in September 2019; the Regglberg against the
  Isarco in August 2021; the Trentino south against the north in September 2024.
- **Anonymous forum posts:** the Vinschgau against the Pusteria and Val Badia in August 2021.
- **Season-level leads only:** South Tyrol 2024 against 2023 for chanterelles ("dieses Jahr setzt
  noch einen drauf", stol.it lead); South Tyrol September against August 2018; 2017 against 2016
  (Touring Club, national); 2025 "etwas länger ... als im Vorjahr" (a forecast).
- **Single-sided or out of range:**
  - early porcini in May 2018 (Piné, Val di Non) and May 2024 (Civezzano);
  - the Chiese and Levico in 2016 (compared with 2015);
  - Fiemme permit revenue 2018 against 2019 (Vaia);
  - the mid-September 2025 boom (il T).
- **Outlets not read:** Rai's TGR and Tagesschau pages blocked the tools; stol.it articles are
  behind a paywall, so only titles and leads were used; l'Adige's pre-2023 URLs now 404 (live
  addresses or the Wayback Machine were used); Funghi Magazine's 2018-2020 index pages are empty.

**Year picture from the press** (context, not scored):

| year | Trentino | South Tyrol |
|---|---|---|
| 2016 | porcini late (early August "ancora piuttosto indietro"), finferli abundant; Levico peak late August | — |
| 2017 | hot, dry June-July (poor in Val di Sole); good September-October | — |
| 2018 | very early May porcini; a fortunate September; high Fiemme permit revenue | hot summer, weak late August, rainy early September good for porcini |
| 2019 | poor June-July; boom August to early September (Giudicarie, Val di Non, Lagorai, Fiemme) | late start, few porcini or finferli to mid-August, the east better than the west; good early September |
| 2020 | less productive than 2019 but more finferli; good August at Pergine, a lucky September at Vezzena | late July start, heavy early-August rain |
| 2021 | late and poor ("misera"), a brief mid-August flush in the east | "kein gutes Pilzjahr": porcini almost absent |
| 2022 | good spring; drought in July, nearly empty; some recovery by mid-August | drought, a mid-July lull, modest by mid-August |
| 2023 | early, rich July; the south faded in August; the west better than the Dolomites in late September and October | nearly nothing to about 20 July, then good finferli from late July (Pusteria); porcini scarce in August, good around 20 September |
| 2024 | very early May porcini; poor late July on the Vallagarina floor, good higher; abundant finferli | "hervorragend", better than 2023, mainly finferli; porcini weaker than in Trentino |
| 2025 | a big flush late July to early August ("porcini ovunque"), stopped by heat about 8 August; fewer finferli than 2024; another boom in mid-September | early July start ahead of Trentino, a rainy summer, abundant around Bressanone |

## Open questions

- **Larch.** 0.1 here, as in Lombardia; Piemonte kept 0.3. The evidence is strong that larch
  roots hold no *Boletus* or *Cantharellus*, and the records are only mildly depleted in larch
  cells (21 % against 27 %). Two tests:
  - the backtest;
  - the Dolomites and Pusteria contrasts, whose woods are larch-rich.

  The three Alpine regions should end on one value.
- ***B. edulis* single window.** The high records here end as late as the low ones, unlike
  Piemonte's (none of 15 above 1,400 m in October) and Lombardia's. The backtest should compare the
  single window with the Piemonte-style split.
- **Chestnut.** Nearly absent from both maps, so chestnut porcini, ovoli and chanterelles are
  scored through the oak, pine and mixed classes. If the low-valley scores look too low, typing
  "castagneto su …" stands as chestnut would help (a grid question).
- **Ovoli on Scots pine.** The 0.3 on mountain pine rests on census collections "sotto pino e
  quercia" and on the oak-pine belts. A few more records would show whether pure Scots-pine
  stands of the porphyry terraces deserve it.
- **Sun exposure.** The Alpine spread of sun ratios is much wider than Tuscany's. Whether the
  stoppers should be re-anchored is a backtest question for all the Alpine regions together.
- **Leads not read:**
  - the Federazione dei Gruppi Micologici del Trentino-Alto Adige's own publications (census
    reports, the Bollettino del Gruppo Micologico Bresadola);
  - the Naturmuseum Südtirol's exhibitions and any South Tyrolean macrofungi checklist;
  - the Agrar- und Forstbericht's yearly picking-fine counts per forest inspectorate (a possible
    season index).

## References added for Trentino-Alto Adige

| id | kind | verified | used for |
|---|---|---|---|
| `mushma_occurrence_check_taa_2026` | analysis | verified | record months, enrichment, elevations, provinces, census squares |
| `mushma_taa_forest_check_2026` | analysis | verified | forest composition, records against woods, gate checks, slope and sun ratios on the grid |
| `taa_muse_censimento_caesarea` | society | verified | ovolo profile, collections and altitude in the region |
| `taa_muse_censimento_aestivalis` | society | verified | *B. reticulatus* profile and maximum altitude |
| `taa_pat_tipi_forestali_2018` | institutional | verified | Trentino's forest districts, belts, larch on spruce sites, oak-pine contact |
| `taa_pat_foreste_trentino` | institutional | verified | Trentino forest area and main types |
| `taa_pat_funghi_raccolta` | institutional | verified | Trento picking rules |
| `taa_pat_funghi_limite_2025` | institutional | verified | Trento's 3 kg limit from August 2025 |
| `taa_bz_waldtypisierung2010` | institutional | verified | South Tyrol's growth regions, belts and rain |
| `taa_bz_hauptbaumarten` | institutional | verified | South Tyrol's tree-species shares |
| `taa_bz_wald_flaechen` | institutional | verified | South Tyrol's forest area, elevation and slopes |
| `taa_bz_pilzesammeln` | institutional | verified | Bolzano picking law and banned areas |
| `taa_bz_pilzsammelgebuehr2024` | institutional | verified | Bolzano even-day rule, limits and fee |
| `taa_mandolini2025_larix` | peer-reviewed | verified (full text) | no *Boletus* or *Cantharellus* on South Tyrolean larch |
| `taa_mandolini2024_cembra` | peer-reviewed | verified (full text) | no *Boletus* or *Cantharellus* on stone pine |
| `taa_altoadige_2023_08_08` | web | verified | season start and finferli in the Pusteria, 2023 |
| `taa_orf_tirol_2019_08_09` | web | verified | "Mitte Juli" season start; the late 2019 season |

Existing references the changes lean on, opened again for this card:
- `muse_censimento_edulis`, `muse_censimento_pinophilus`, `muse_censimento_cibarius`,
  `muse_censimento_boletus` (census pages);
- `diez2020_alps` (abstract);
- `funghimagazine_ovolo` (the north-east ovolo limit).
