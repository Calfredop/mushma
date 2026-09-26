# Species ecology: Piemonte (regional appendix to species-ecology.md)

Research date: 2026-09-25 (dates Europe/Rome, units metric). Card: `region-piemonte-species.md`
(child of `region-piemonte.md`). Rule files: `api/src/api/config/species/piemonte/`. This appendix
records how the Tuscan rule set (`species/tuscany/`) was carried to Piemonte, what changed and why.
It covers **fruiting conditions only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(13 added for Piemonte, in one block at the end of the file). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every
number is a prior for the backtest; season windows, altitude bands and habitat affinities stay
frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

## Summary

1. **All three groups and all six keys are kept.** Porcini, ovoli and gallinacci are all picked and
   recorded in Piemonte. The one key in doubt, the thermophilic *B. aereus*, is kept: Piemonte has 23
   iNaturalist and 9 GBIF records of it, all below 800 m, the regional produce sheet has a "porcino
   nero ... diffuso alle basse quote, sotto gli 800 metri" (`piemonte_pat_funghi_vallate`), and
   forager bulletins place it in the hills south of the Po (`funghimagazine_2024_10_11`). Its band
   and season are cut to those hills.
2. **Piemonte is the first region with Alpine woods, and that is most of what changed.** The
   *B. edulis* season gains an earlier Alpine window (July-September, closed by 20 October), blended
   in from 1,200 m and alone from 1,600 m; altitude bands reach the tree line (about 2,300 m) for *B. edulis*, *B. pinophilus* and
   gallinacci; Scots pine becomes a full host of *B. pinophilus*; gallinacci are *C. cibarius*
   s.str. here, a temperate species of conifers and deciduous Fagaceae, so four host classes move
   up a tier.
3. **The hills move the warm taxa's windows.** Ovoli and *B. aereus* stop lower (1,000 m) and the
   ovoli season comes a month earlier (August-September). Every autumn tail that ran into December or
   January in Tuscany now closes by 30 November (gallinacci, *B. aereus*) or 31 October
   (*B. reticulatus*): Piedmontese records stop in November.
4. **Weather rules are all Tuscany's.** No Piedmontese study ties porcini, ovoli or gallinacci
   fruiting to rain or temperature in numbers. The Alpine cold is left to the existing frost, snow,
   cold-night and temperature rules, which read each cell's own weather; the porcini 30-day rain is
   already scored against each cell's normal. Details under Weather.
5. **Evidence is institutional and Alpine, not regional and quantitative.** Of the 13 new sources
   (all opened), 1 is peer-reviewed (Alpine fruiting shifts), 5 institutional (the IPLA forest
   types, the regional forest and rain reports, the picking law, the regional produce sheet), 3
   north-east Alpine census pages (society), 3 forager or bulletin pages (folklore) and 1 our own
   analysis. The Piedmontese sightings (151 *B. edulis*, 83 *B. reticulatus*, 50 ovoli, 79
   *Cantharellus* on iNaturalist) are the best of any region so far and carry most of the season and
   altitude changes.

## At a glance: what differs from Tuscany and why

| key | factor | Tuscany | Piemonte | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | one window 01-07 → 01-09 … 15-11 → 20-12 | same window below 1,200 m; **Alpine window 15-06 → 15-07 … 20-09 → 20-10 above 1,600 m**, blended 1,200-1,600 m | located records above 1,400 m: Jul 1, Aug 7, Sep 6, **Oct 0** (3.6 expected from effort); below 900 m the Tuscan Sep-Oct peak; handover on the montane-subalpine boundary (`ipla_tipi_forestali_2008`) | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **150 → 450 … 1,900 → 2,300** | records p10 427 m, p90 1,592 m, max 2,110 m; chestnut from the plain; woods to 2,307 m; NE Alpine max 2,175 m (`muse_censimento_edulis`) | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.6** | here mostly birch and hazel pioneer woods (IPLA BS), birch a host | plausible |
| *reticulatus* | season end | 30-09 → 15-11 | **30-09 → 31-10** | October 0.6×, November 0 of 83 records (8 expected) | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,200 → 1,600** | 5 of 33 located records above 1,200 m, 2 at 1,500-1,604 m | plausible |
| *aereus* | season | split by elevation (upland summer / lowland autumn, 400-600 m) | **one window 01-07 → 01-09 … 31-10 → 30-11** | no records above 800 m; October peak at every elevation; none in December | plausible |
| *aereus* | altitude | … 800 → 1,250 | **… 700 → 1,000** | "sotto gli 800 metri" (`piemonte_pat_funghi_vallate`); records max 793 m | plausible |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **1.0** | here almost all Scots pine; "frequentemente legato al pino silvestre" (`muse_censimento_pinophilus`) | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **300 → 600 … 1,800 → 2,200** | Scots pine and chestnut below 800 m; spruce and fir to the subalpine boundary; NE Alpine max 1,898 m | plausible |
| ovoli | season | 01-06 → 01-09 … 05-11 → 30-11 | **01-06 → 01-08 … 05-10 → 20-11** | August 2.1× and September 2.9× effort, October 0.6× (central Italy: 0.9×, 3.4×, 2.2×) | plausible |
| ovoli | altitude | … 750 → 1,100 | **… 800 → 1,000** | "fin verso gli 800/900 mt tra Langhe-Roero e sub-appennino Piemontese" (`funghimagazine_ovolo`); 28 of 29 records below 900 m | plausible |
| gallinacci | lowland season end | 15-12 → 25-01 | **31-10 → 30-11** (also in the disabled two-flush rule) | no December or January record of 79 (about 3 expected in each) | plausible |
| gallinacci | altitude | … 1,000 → 1,700 | **… 1,300 → 1,900** | records p90 1,304 m, 8 at 1,200-1,500 m; *C. cibarius* to 2,040 m in the NE Alps | plausible |
| gallinacci | habitat | fir/spruce 0.6, deciduous oak 0.3, mountain pine 0.3, mixed broadleaf 0.3 | **1.0, 0.6, 0.6, 0.6** | *C. cibarius* s.str. (58 of 66 species-level records), a temperate host generalist (`olariaga2017`); acidophilous sessile oak; Scots pine; birch | plausible |
| every key | slope stopper | x1 to 25°, x0.8 from 40° | **x1 to 34°, x0.8 from 45°** | the same rule on the Piedmontese grid: woodland p90 33.9° (Tuscany 26.2°), max 44.7° (41.7°); 41 % of Piedmontese woodland cells are steeper than 25° | as Tuscany (plausible) |
| every key | weather, growth clock, sun exposure | — | **unchanged** | no Piedmontese numbers (see Weather); on 15 Oct the sun ratio of woodland below 1,000 m runs p90 111 % (Tuscany 110 %) | as Tuscany |

Kept on purpose: every habitat tier not listed; *B. pinophilus* windows; the gallinacci mountain
window; *B. edulis* `other_conifer` at 0.3 (larch, see Porcini); the ovoli `sun_exposure` limits.

## Piemonte in brief

**Woods.** The grid reads Regione Piemonte's Carta forestale 2025 (IPLA categories; mapping and
areas in `.gavin-root/docs/regions/piemonte.md`). The 2016 map, as the regional environment report
gives it: "Castagneti (22%; 206.977 ha), Faggete (15%; 141.599 ha), Robinieti (12% 117.483 ha),
Larici-cembrete (10% 92.533 ha) e Boscaglie pioniere e d'invasione (8%; 74.995 ha)", 72 % of the
woods in the mountains (`rp_relazione_ambiente_foreste2024`). What the IPLA forest-type manual says
about the classes the rules care about (`ipla_tipi_forestali_2008`, verified, read in full for the
categories):

| habitat key | IPLA categories (2025 map, ha) | what is in it, for the rules |
|---|---|---|
| `chestnut` | CA 212,245 | "il castagno è diffuso ... dalla pianura a tutto il piano montano"; marginal "a quote superiori a 1000 m"; acidophilous and neutrophilous types in the Alps and the hills |
| `beech` | FA 145,080 | the montane forest of the Alps and the Apennine, "secondariamente" the hills; mostly aged coppice |
| `exotic_broadleaf` | RB 130,276 | robinia, largely replacing chestnut and oak in the plain and hills |
| `other_conifer` | LC 97,044, RI 21,549 | larch and stone pine (82 %) plus conifer plantations; larch is mixed into the endalpic spruce woods "fino al 40%" |
| `mixed_broadleaf` | BS 78,991, AF 49,091, OS 14,563 | more than half pioneer woods where "fra le specie più abbondanti a livello regionale vi sono la betulla, il nocciolo e il sorbo montano" |
| `deciduous_oak` | QR 48,046, QV 42,843, QC 38,769, CE 4,587 | sessile oak woods, "in tutti i casi ... popolamenti acidofili"; downy oak; pedunculate oak-hornbeam in the plain; little Turkey oak |
| `fir_spruce` | AB 15,305, PE 9,621 | silver fir 1,000-1,500 m (eutrophic) and above 1,500 m; subalpine spruce "a partire dai 1600 m" |
| `mountain_pine` | PS 15,436, PN 2,743 | Scots pine, "popolamenti montani, secondariamente planiziali e collinari"; mountain pine |
| `riparian` | SP 17,375, AN 5,188 | willows, poplars, alders |
| `mediterranean_pine` | PM 685 | maritime pine in the Appennino alessandrino |

Holm oak, cork oak and macchia are absent. The IPLA manual puts "i limiti tra il piano montano e
quello subalpino ... tra i 1500 m nel Piemonte settentrionale e i 1800 m nei settori endalpici
centromeridionali". On the grid, woodland cells run to 2,307 m (95th percentile 1,774 m; median
slope 22.8°, against 16.6° in Tuscany) (`regions/piemonte.md`).

**Climate** (`arpa_piemonte_precipitazioni2023`, 1958-2022 series). Annual rain has risen in the
Verbano, around Lago Maggiore, and fallen slightly elsewhere, most in the Biellese and between Cuneo
and Alessandria; winters and springs are more often in deficit, autumns more often in surplus.
Summer 2022 was the 15th driest since 1958, after a 111-day dry spell from 9 December 2021 to 29
March 2022. Forager bulletins single out the dry, warm down-slope wind (*favonio*, foehn) as the
flush-killer of the northern valleys: "aria secchissima, prevalentemente favonica ... che sta
inibendo nascite di Porcini anche tra la Valsesia ed il VCO" (Funghi Magazine, 2021-09-04; see Press
contrasts), which is what the ET0-based drying rules stand in for.

**Picking rules** (`lr_piemonte_24_2007`). L.R. 24/2007: 3 kg a day, no picking "dal tramonto alla
levata del sole", and "È vietata la raccolta di esemplari di Amanita cesarea allo stato di ovolo
chiuso". There is **no season calendar**, so the law gives no season prior. The regional produce
sheet (`piemonte_pat_funghi_vallate`) puts Piedmontese mushrooms "in tutte le vallate montane e
pedemontane piemontesi, con maggiore concentrazione nelle vallate cuneesi e in Val Sangone, da fine
aprile a metà novembre".

## Sightings (occurrence cross-check)

Queried 2026-09-25 (`mushma_occurrence_check_piemonte_2026`): GBIF with `gadmGid=ITA.13_1`
(soil-DNA `MATERIAL_SAMPLE` rows excluded; *Cantharellus* minus *C. cinereus* and *C. melanoxeros*),
iNaturalist place 10872 (verifiable), elevations from the Open-Meteo elevation API for open, accurate
(≤ 1 km) iNaturalist records only. Aggregates only; no coordinates are stored. Enrichment = the
taxon's monthly share ÷ the monthly share of all 26,797 Piedmontese iNaturalist fungi records (> 1:
over-represented for the effort; all fungi peak in October, 23.7 %, then September, 18.4 %).

| taxon | source | n | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | GBIF | 49 | | | | | 1 | 1 | 2 | 11 | 17 | 14 | 2 | 1 |
| | iNat | 151 | | | | | 3 | 2 | 5 | 27 | 62 | 48 | 3 | 1 |
| | enrichment | | | | | | 0.4 | 0.2 | 0.6 | 1.8 | 2.2 | 1.3 | 0.2 | 0.2 |
| *B. reticulatus* | GBIF | 26 | | | | | 1 | 6 | 6 | 1 | 7 | 5 | | |
| | iNat | 83 | | | | | 5 | 19 | 20 | 4 | 24 | 11 | | |
| | enrichment | | | | | | 1.1 | 4.2 | 4.4 | 0.5 | 1.6 | 0.6 | 0 | |
| *B. aereus* | GBIF / iNat | 9 / 23 | | | | | | | | 1 / 2 | 0 / 8 | 8 / 12 | 0 / 1 | |
| *B. pinophilus* | GBIF / iNat | 8 / 16 | | | | | | 0 / 3 | 1 / 1 | | 2 / 4 | 2 / 5 | 3 / 3 | |
| *A. caesarea* | GBIF | 18 | | | | | | 2 | | 7 | 5 | 2 | 2 | |
| | iNat | 50 | | | | | | 3 | 1 | 10 | 27 | 7 | 2 | |
| | enrichment | | | | | | | 1.1 | 0.4 | 2.1 | 2.9 | 0.6 | 0.4 | |
| *Cantharellus* | GBIF | 26 | | | | | 1 | | 3 | 11 | 6 | 5 | | |
| | iNat | 79 | | | | | 6 | 7 | 10 | 13 | 20 | 21 | 2 | |
| | enrichment | | | | | | 1.3 | 1.6 | 2.3 | 1.7 | 1.4 | 1.1 | 0.3 | 0 |

| taxon | located n | p10 | median | p90 | max (m) | by band |
|---|---|---|---|---|---|---|
| *B. edulis* | 82 | 427 | 859 | 1,592 | 2,110 | <300: 3, 300-600: 13, 600-900: 27, 900-1,200: 12, 1,200-1,500: 15, 1,500-1,800: 10, ≥1,800: 2 |
| *B. reticulatus* | 33 | 358 | 641 | 1,294 | 1,604 | 1,200-1,500: 3, 1,500-1,800: 2 |
| *B. aereus* | 14 | 218 | 406 | 756 | 793 | none above 800 m |
| *B. pinophilus* | 7 | 904 | 1,202 | 1,644 | 1,673 | min 672 m |
| *A. caesarea* | 29 | 326 | 559 | 781 | 2,120 | 28 below 900 m; the 2,120 m record is implausible |
| *Cantharellus* | 46 | 433 | 798 | 1,304 | 2,120 | 1,200-1,500: 8, 1,500-1,800: 0, ≥1,800: 1 |

**Months by elevation** (located records):

| taxon | band | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | < 900 m (n=43) | 1 | 2 | 2 | 5 | 15 | 16 | 2 | |
| | 900-1,400 m (n=24) | | | | 4 | 12 | 7 | 1 | |
| | ≥ 1,400 m (n=15) | | | 1 | 7 | 6 | **0** | | 1 |
| *B. aereus* | < 500 m / 500-1,000 m | | | | 0 / 1 | 3 / 0 | 6 / 3 | 1 / 0 | |
| *A. caesarea* | < 500 m (n=12) / 500-1,000 m (n=16) | | 0 / 3 | | 4 / 3 | 3 / 9 | 3 / 1 | 2 / 0 | |
| *Cantharellus* | < 900 m / 900-1,400 m / ≥ 1,400 m | 2 / 0 / 0 | 3 / 0 / 0 | 2 / 5 / 2 | 5 / 4 / 0 | 4 / 7 / 0 | 9 / 1 / 0 | 2 / 0 / 0 | |

**Species inside *Cantharellus*** (iNaturalist species counts): *C. cibarius* 58, *C. pallens* 4,
*C. friesii* 3, *C. ferruginascens* 1. In Tuscany the records were mostly the Mediterranean
segregates; here *C. cibarius* s.str., which "is broadly distributed in Europe, but not present in
areas with Mediterranean climate" (`olariaga2017`), dominates.

Caveats: presence-only, near trails and towns, recent (78 of 82 located *B. edulis* from 2016 on;
some records from 2026 are included in the counts), and the season and band changes were drawn from
these same records, so they are priors, not fits. The high-altitude *B. edulis* rows are few (15
records) and summer hikers raise Alpine effort in July-August; the October gap above 1,400 m is the
stronger half of the signal. GBIF adds little beyond iNaturalist in Piemonte. The single December
*B. edulis* record above 1,400 m and the 2,120 m ovoli and *Cantharellus* records look misdated or
misplaced.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Presence and areas** (institutional, plausible). The regional produce sheet names the four
  porcini "sotto piante d'alto fusto (querce, faggi, castagni)", in conifer, broadleaf, birch and
  poplar woods, most concentrated in the Cuneo valleys and the Val Sangone
  (`piemonte_pat_funghi_vallate`).
- **Hosts** (folklore). "I porcini dell'abete rosso sono: Boletus pinophilus, B. edulis"; Scots and
  black pine carry *B. reticulatus*, *B. pinophilus* and *B. edulis*; but in pure larch woods porcini
  are "altamente improbabile, se non del tutto impossibile" (`funghimagazine_alberi_porcini`). In
  the north-east Alpine census *B. pinophilus* is "frequentemente legato al pino silvestre" but not
  only (`muse_censimento_pinophilus`, society).
- **Altitude** (society and folklore). North-east Alpine records: *B. edulis* 10-2,175 m
  (`muse_censimento_edulis`), *B. pinophilus* 200-1,898 m. A Piedmontese forager page limits the
  common porcino to "2000 metri" and puts the porcino nero and the estatino "spesso a un'altitudine
  inferiore ai 700 m" (`cacciatoridifunghi_piemonte2023`). Fungi in the Alps fruit higher than in
  1960, most so the high-altitude, soil-dwelling species (`diez2020_alps`, peer-reviewed, strong for
  the direction, not for a number).
- ***B. aereus* in the north** (society and folklore). "Specie diffusa prevalentemente nell'Italia
  centro-meridionale, può essere comunque occasionalmente reperito anche nelle regioni alpine, in
  habitat idonei" (`muse_censimento_boletus`). In October 2024: "Candidati ad avere buone nascite di
  Aereus ovviamente tutti i boschi a Sud del Po, tra colline del Po-Monferrato-Langhe-Roero e
  pre-appennino Alessandrino", while "a Nord del Po non si è visto nascere un solo Porcino
  Nero/Boletus aereus" (`funghimagazine_2024_10_11`).
- **Records** (analysis). See Sightings: *B. edulis* peaks in September-October below 900 m and in
  August-September above 1,400 m; *B. reticulatus* in June-July and September; *B. aereus* in
  September-October below 800 m; *B. pinophilus* in June and September-November.

**Decisions** (numbers in the table above; reasons in each factor's `notes`):

- ***B. edulis* season: an Alpine window.** The subalpine flush comes in summer and ends before
  October; the Tuscan window (full September to mid-November) would leave Alpine cells in season
  into December, held only by frost and snow. The window is blended by elevation across 1,200-1,600
  m, the montane-subalpine boundary. Below 1,200 m the Tuscan window is kept: it fits the
  September-October peak, and the frost and snow stoppers end its November-December tail (November
  records are 0.2× the effort).
- ***B. edulis* altitude.** Down to the hill chestnut (zero at 150 m, the plain's robinia and riparian
  woods; full from 450 m) and up to the tree line (full to 1,900 m, zero at 2,300 m).
- ***B. edulis* larch.** `other_conifer` stays marginal (0.3): pure larch is not a porcini host, but
  Piedmontese larch is often mixed with spruce and stone pine, and 12 records lie at 1,500-2,110 m in
  the larch belt. With the habitat factor saturating at a 0.3 host share, a cell that is all larch
  still gets full habitat credit; if Alpine larch cells score too high in the sanity check or the
  backtest, this is the first number to lower (to 0.1).
- ***B. edulis* birch.** `mixed_broadleaf` to secondary (0.6): the class is mostly birch-hazel pioneer
  woods here (Tuscany: hop-hornbeam and hornbeam), and birch is a host (*B. betulicola* is a synonym,
  `beugelsdijk2008`).
- ***B. reticulatus*.** The tail closes on 31 October (the Tuscan draft date, before the central-Italy
  records widened it); the band's upper ramp moves up 100 m for the Alpine beech. The Piedmontese
  records show the summer mode strongly (June-July over 4× the effort) and an August trough (0.5×),
  which the weather rules, not the window, must make.
- ***B. aereus*.** One autumn window and a band cut to the hills (full to 700 m, zero at 1,000 m).
  The Tuscan upland summer window rested on the Borgotaro IGP's Apennine uplands; the Piedmontese
  records show no upland summer form (the 500-800 m records are August 1, October 3).
- ***B. pinophilus*.** Scots pine becomes a full host; the band moves down to 600 m (Scots pine and
  chestnut) and up to 1,800 m (spruce, fir, subalpine Scots pine). Its windows are kept (records
  fit both).

## Ovoli (*Amanita caesarea*)

**Regional evidence.** Picked and regulated: the regional law bans picking "Amanita cesarea allo
stato di ovolo chiuso" (`lr_piemonte_24_2007`), and the regional produce sheet lists the ovolo buono, "fungo reale"
(`piemonte_pat_funghi_vallate`). Altitude and range: "Assente oltre i 500 metri al Nord Ovest
italiano, oltre i 600 metri al Nord Est, fin verso gli 800/900 mt tra Langhe-Roero e sub-appennino
Piemontese. Piuttosto comune in alta Pianura Padana, soprattutto a Sud del Po, dall'Alessandrino"
(`funghimagazine_ovolo`, folklore). In 2024 the hill woods south of the Po "a fine
settembre-inizio ottobre hanno registrato anomale quanto massicce nascite di Ovoli Reali/A.caesarea"
(`funghimagazine_2024_10_11`, folklore): "anomale" for that date. Records: 50 iNaturalist and 18 GBIF,
peaking in September (2.9×) with a strong August (2.1×) and a weak October (0.6×); at 500-1,000 m
June-September, below 500 m August-November.

**Decisions.**

- **Season a month earlier**: full 1 August to 5 October, closed by 20 November. The tail keeps a
  ramp because the low hills fruit later and 2024 showed a big early-October flush; the cold-night
  and soil-temperature rules end the season.
- **Altitude**: full to 800 m, zero at 1,000 m. The north-west Alpine 500 m limit cannot be encoded
  in the same band as the Langhe's 800-900 m; the Alpine valleys' colder nights and soils hold the
  scores there.
- **Hosts kept.** The Piedmontese deciduous-oak class (sessile, downy and pedunculate oak) is all
  host ("si adatta bene anche tra alberi di Farnia, Rovere e Roverella", `funghimagazine_ovolo`).
  Robinia (13 % of the woods, much of it in the hills) stays non-host at 0.05, so robinia-dominated
  hill cells score low; that is intended.
- **Press note** (for context, not encoded): forager bulletins call ovoli north of the Po unusual
  almost every year since 2019 (details under Press contrasts), which reads as a real northward and
  upward spread or as more observers. The records do not settle it.

## Gallinacci (*Cantharellus* s.l., "galletti", "finferli")

**Regional evidence.** *C. cibarius* s.str. dominates the records (58 of 66 species-level
iNaturalist records), with a few *C. pallens*, *C. friesii* and *C. ferruginascens*. *C. cibarius*
is temperate: "not present in areas with Mediterranean climate" and, in southern Europe, found in
"rainy or locally damp sites" on acid soils; its epitype was collected "under Picea abies, with
Betula and Pinus", a Swiss collection "under Picea, Fagus and Pinus", others in *Pinus sylvestris*
forest and under chestnut (`olariaga2017`, peer-reviewed, strong for hosts and climate). North-east
Alpine census: *C. cibarius* from 10 m to 2,040 m, "Conifere e microselva alpina"
(`muse_censimento_cibarius`). Regional produce sheet: gallinaccio "reperibile tra giugno e
settembre, nei castagneti e nel bosco ceduo" (`piemonte_pat_funghi_vallate`). Records: May to
November with no summer trough (July 2.3×, August 1.7×), nothing in December or January.

**Decisions.**

- **Hosts**: fir/spruce to host (1.0); deciduous oak, mountain pine and mixed broadleaf to secondary
  (0.6). The Tuscan tiers were built on the Mediterranean segregates in Tuscan plots (deciduous oak
  1 of 4 calcicolous plots); in Piemonte the class is mostly acidophilous sessile oak and
  pedunculate oak-hornbeam in a temperate climate, Scots pine is a documented *C. cibarius* host, and
  the pioneer woods are birch. Beech stays secondary (0.6), larch marginal (0.3), chestnut host.
- **Season**: the lowland window closes by 30 November (full to 31 October); the mountain window is
  kept.
- **Altitude**: full to 1,300 m, zero at 1,900 m.
- **Soil pH and lithology** stay disabled. The Piedmontese woodland pH (SoilGrids median 6.27, lowest
  under fir, spruce, beech and larch; `regions/piemonte.md`) is more acid than Umbria's (6.89), so a
  pH rule could separate cells here; both factors stay disabled, as in Tuscany, because SoilGrids is
  a 250 m model and the rule was never validated. A backtest comparison is worth running here first.

## Weather rules: why none changed

- **No regional numbers.** No Piedmontese or Alpine study gives a rain amount, lag or temperature
  threshold for these taxa that improves on the Tuscan set, which already leans on
  temperate-climate evidence: the Swiss plot series for all fungi behind the gallinacci 30-day rain
  (`straatsma2001`), the German beech *B. edulis* temperatures (`brejon_hoffman2026_preprint`) and the
  Amiata lag (`salerni2023_amiata`).
- **Alpine cold.** The frost, snow, cold-night, air- and soil-temperature rules and the growth clock
  read each cell's own downscaled weather, so they already slow and end the season at altitude; the
  new *B. edulis* Alpine window only stops the gate from staying open where the weather rules would
  otherwise have to do all the work.
- **Wet north, dry south.** The porcini 30-day rain is a percentage of each cell's normal, so it adapts
  to the wet Verbano and the dry Alessandria plain alike. The absolute 30-day ramps of
  ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full more often in the north and less often in
  the south; ovoli barely grow in the wet north, and the gallinacci ramp is low anyway.
- **Foehn.** The drying rules (ET0 days for porcini and gallinacci, 7-day ET0 for ovoli) are the only
  stand-in for the *favonio* the northern press blames; the known gap `drying_wind` (gusts plus low
  humidity) would fit Piemonte better than Tuscany if the engine ever gets compound conditions.
- **Rain scale.** `precipitation_scale` was fitted on Tuscan gauges; the ARPA Piemonte gauge check is
  a region-config task (`regions/piemonte.md`), not a species one.

## Press contrasts (`sanity.yaml`)

`piemonte/sanity.yaml` holds 14 porcini contrasts from 2020-2025, written down on 2026-09-25 before
Piemonte had any scores. Every page below was opened, and each quote in the table was checked
against the page's text, except the two marked "not re-opened by me" (read by a research agent);
dates are the pages' own publication dates. Areas are ISTAT 2025 comuni or province sigle (18
areas, all names checked against the ISTAT list); "normal" is the area's mean over 2017-2025.
`sanity.py` scores one group per run, and the ovoli and gallinacci claims found were too vague to
test, so all 14 are porcini.

**How far to trust them.** Local papers rarely date and place a season; most of what they print
is Coldiretti releases, permit rules and single big finds. The one outlet that names Piedmontese
sub-areas week by week is **Funghi Magazine** (FM), and 10 of the 14 contrasts rest mainly on it.
FM mixes reader reports with rain-gauge reasoning, so several of these contrasts partly test the
rain data rather than observed fruiting (flagged below as "rain-led"). FM's editor belongs to the
Gruppo Micologico Biellese, as does the mycologist quoted by the Biella press, so the north's
sources are not fully independent.

| id | higher | lower | window | main source | second source | caveats |
|---|---|---|---|---|---|---|
| `biellese_2025_2024` | Biellese mountains 2025 | same, 2024 | 08-18 → 09-07 | [Giornale La Voce, 2025-09-01](https://www.giornalelavoce.it/news/attualita/622291/stagione-dei-funghi-2025-tra-raccolte-anticipate-boom-di-tesserini-e-turismo-culturale.html): "Rispetto al 2024, la raccolta è iniziata con 15-20 giorni di anticipo"; a buttata "abbondante e diffusa, a differenza dello scorso anno, quando i raccolti erano stati localizzati soprattutto nell'Oasi Zegna e limitati nel tempo" | [La Provincia di Biella, 2024-09-07](https://laprovinciadibiella.it/attualita/funghi-mai-cosi-pochi/): "la penuria di funghi ha raggiunto livelli difficilmente visti nel recente passato"; a small buttata after 18 August | the 2025 flush started only in mid-August (FM, 2025-08-08: "fino ad ora le nascite fungine nel Biellese sono state praticamente ferme"); both articles quote the same mycologist |
| `valsesia_2022_2021` | Valsesia 2022 | same, 2021 | 08-28 → 09-12 | [Notizia Oggi, 2022-09-09](https://notiziaoggi.it/attualita/raccolta-funghi-il-2022-e-un-anno-record/): "Raccolta funghi: il 2022 è un anno record"; "Complici le precipitazioni e i temporali dei giorni scorsi, la stagione ha fatto registrare un picco non indifferente" | [FM, 2021-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): foehn air "sta inibendo nascite di Porcini anche tra la Valsesia ed il VCO dove non si registra alcuna buttata"; [FM, 2021-09-10](https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/): "Biellese, Valsesia e Verbano Cusio Ossola di certo non ridono"; [FM, 2022-09-15](https://funghimagazine.it/meteo-funghi-15-09-2022/): Valsesia-Cusio "hanno dato ... il massimo che potevano nel corso degli ultimi 20 giorni" | "anno record" is a headline |
| `valsesia_ossola_2023_late` | Valsesia + Ossola, normal | same, 2023 | 08-15 → 09-08 | [Notizia Oggi, 2023-09-21](https://notiziaoggi.it/attualita/coi-funghi-la-valsesia-incassa-quasi-100mila-euro/): "Quest'anno la stagione è iniziata con un paio di settimane di ritardo" (Unione Montana Valsesia) | [FM, 2023-08-10](https://funghimagazine.it/aggiornamento-funghi-10-08-2023/): the mountains of Valsesia and VCO had "piogge assai inferiori", no porcini "almeno non prima di fine Agosto" | the same release ran in La Sesia (2023-09-16); the normal includes other dry Augusts (2021, 2024) |
| `alto_piemonte_vs_valsusa_2023` | provinces BI, VC, NO, VB, 2023 | inner Val di Susa and Pinerolese valleys, 2023 | 09-12 → 10-04 | [FM, 2023-10-04](https://funghimagazine.it/aggiornamento-porcini-04-10-2023/): "Biellese, Vercellese, Novarese e Verbano-Cusio-Ossola strabilianti, con super nascite ovunque, dal piano ai monti"; "Alpi Cozie risultano poco produttive per via di piogge non ottimali. Tolte le zone interene della Val Susa, con piogge insufficienti ..." | [FM, 2023-09-13](https://funghimagazine.it/aggiornamento-funghi-13-09-2023/): most productive "Eporediese, Biellese, Valsesia, Verbano-Cusio-Ossola"; "Torinese montano+Canavese" only "nascite buone ma non buttate importanti" | FM only |
| `torinese_vs_valsesia_ossola_june_2024` | Pinerolese and Val Sangone foothills, 2024 | Valsesia + Ossola, 2024 | 06-10 → 07-10 | [FM, 2024-06-14](https://funghimagazine.it/aggiornamento-funghi-14-06-2024/): red porcini in "la Val d'Ossola e Valsesia ... tutt'altro che degne di nota, addirittura del tutto assenti"; "ancora buoni ritrovamenti nel solito territorio Torinese" | [FM, 2024-06-28](https://funghimagazine.it/aggiornamento-funghi-28-06-2024/): "in alto Piemonte non si trova un fungo Porcino a pagarlo a peso d'oro"; "in alcune zone del Torinese ... si raccoglie bene ormai da inizio mese" | FM only; mostly *B. pinophilus*; the Torinese comuni are my reading of "primi pianori pedemontani"; FM blames too much rain in the north, which a rain rule scores as good (a real test) |
| `cuneo_valleys_2023_2024_vs_2021` | Cuneo valleys (Monregalese, Pesio, Vermenagna, Gesso, Stura, Alta Val Tanaro) 2023 and 2024 | same, 2021 | 09-05 → 09-20 | [Cuneo24, 2023-09-27](https://www.cuneo24.it/2023/09/con-20-e-boom-di-funghi-nelle-vallate-215096/) (Coldiretti Cuneo): "È boom di funghi nel Cuneese, specialmente nelle vallate prealpine dove, tra la seconda e la terza settimana di settembre, c'è stata una fuoriuscita eccezionale" | [Cuneodice, 2024-09-13](https://www.cuneodice.it/varie/cuneo-e-valli/funghi-bellone-cia-cuneo-ottima-stagione-ma-non-si-trascuri-la-manutenzione-dei-boschi_91941.html) (CIA Cuneo): "c'è stata una vera e propria esplosione di funghi, anche se non dappertutto"; [FM, 2021-09-18](https://funghimagazine.it/aggiornamento-meteofunghi-18-09-2021-prima-vera-buttata-di-funghi-porcini/): "restano a secco ampie zone del Cuneese" | Coldiretti's +20 % is against 2022; 2021 is rain-led; rain returned around Ormea, Ceva and Garessio on about 22 September 2021 (FM, 2021-09-24), hence the 20 September end |
| `cuneo_valleys_spring_2022_2021` | Cuneo valleys 2022 | same, 2021 | 05-20 → 06-12 | [FM, 2022-05-28](https://funghimagazine.it/boom-di-funghi-porcini-estatini-e-rossi-ecco-dove/): the Cuneo valleys, "dopo aver sofferto la siccità per oltre un anno intero, ora stanno tornando alla riscossa"; [FM, 2022-06-10](https://funghimagazine.it/aggiornamento-meteofunghi-11-06-2022/): the "splendida parentesi fungina ... delle valli del Cuneese" closed | [FM, 2021-06-24](https://funghimagazine.it/aggiornamento-meteofunghi-24-06-2021-funghi-porcini-si-inizia-a-fare-sul-serio/): red porcini "sempre col contagocce ... nel Cuneese ed Alpi Marittime"; La Provincia Granda column, 2022-06-07 ([archived](http://web.archive.org/web/20220705124304/http://www.provinciagranda.it/meteo-e-tradizioni/2022/06/07/news/funghi-ciliegie-rose-a-volonta-la-terra-e-secca-ma-l-annata-e-buona-9189/)): "Era da un po' di anni che non trovavamo tanti funghi", "nel 2021 ci era mancata l'avventura di imbatterci in un boleto qualsiasi" (not re-opened by me) | a spring flush in a drought year; the column is one person's wood near Mondovì |
| `valle_po_2025` | Valle Po 2025 | same, normal | 09-06 → 09-18 | [La Guida, 2025-09-17](https://laguida.it/2025/09/17/e-iniziato-a-sanfront-il-quotidiano-mercato-dei-funghi): "Parallelamente all'eccezionale fioriture di funghi porcini, il cui prezzo - vittima dell'abbondanza che ha investito tutta la Valle Po - è sceso nei giorni scorsi sino a 15 euro il chilogrammo" | Corriere di Saluzzo, 2025-09-18: the Region's president found "un buon numero di bei funghi porcini" at Gambasca on 15 September (not re-opened by me) | price and a politician's walk are indirect evidence |
| `cuneo_border_july_2024_2025` | Cuneo side of the Ligurian border and the Marittime, 2024 | same, 2025 | 07-15 → 07-31 | [FM, 2024-07-25](https://funghimagazine.it/aggiornamento-funghi-25-07-2024/): "A cavallo tra Liguria di Ponente-Cuneese ... dopo la lunghissima fase di nascite massicce di Porcini Rossi-Pinicola (B. pinophilus), durata molto più di un mese, inframezzata anche da brevi ma massicce buttate di Porcini Estatini/reticulatus" | [TargatoCN, 2025-07-31](https://www.targatocn.it/2025/07/31/leggi-notizia/argomenti/attualita/articolo/funghi-una-stagione-incerta-e-scarsa-che-ricade-sui-ristoranti-e-rivenditori.html): "Pochi funghi se non quasi nulla", "Una stagione imprevedibile e incomprensibile, incerta. Ma soprattutto scarsissima"; [FM, 2025-07-25](https://funghimagazine.it/aggiornamento-nascite-funghi-25-luglio-1-agosto-2025/): "Basso Piemonte ancora fermo: troppo vento, caldo e piogge insufficienti" | early July 2025 was good ("Cuneese e Imperiese sono partiti alla grande", [FM, 2025-07-10](https://funghimagazine.it/aggiornamento-nascite-funghi-11-18-luglio-2025/)), hence the 15 July start; the 2025 quote is a restaurateur's |
| `alto_tanaro_vs_marittime_2020` | Alta Val Tanaro, upper Monregalese and Cebano, 2020 | Alpi Marittime and the Occitan valleys to the Monviso, 2020 | 08-05 → 08-25 | [FM, 2020-08-14](https://funghimagazine.it/aggiornamento-meteofunghi-14-08-2020/): "Nel Cuneese discrete nascite in poche zone di confine con la Liguria, soprattutto in alto Monregalese e localmente anche nel Cebano ma siccità ad oltranza verso le Alpi Marittime con Argentera-Marguareis privi di piogge degne di nota da settimane e siccità nelle vallate Occitane fin sul Monviso" | FM, 2020-08-07 and 2020-09-04 (same outlet) | FM only, rain-led; the higher side is only "discrete"; Limone, Vernante and Briga Alta (Colle di Tenda, rain) left out of both sides |
| `marittime_vs_langhe_roero_2023` | Alpi Marittime 2023 | Alta Langa and Roero, 2023 | 08-12 → 08-28 | [FM, 2023-08-17](https://funghimagazine.it/aggiornamento-funghi-17-08-2023/): "In Piemonte l'unica doccia utile si è avuta sulle Alpi Marittime dove, ora se ne ricavano i primi buoni frutti" | [FM, 2023-08-30](https://funghimagazine.it/meteofunghi-30-08-2023-e-arrivato-il-ciclone-rea/): foragers discouraged "dal persistere della siccità e del caldo anomalo su tutta la fascia del Monferrato-Langhe e Roero" | FM only; the Marittime finds were "a quote elevate" (same bulletin), while the area mean covers every woodland cell of those comuni; "Porcini edulis di Ferragosto dalle Alpi Marittime" fits the new Alpine *B. edulis* window |
| `alessandria_valleys_vs_acquese_2020` | Val Borbera, Val Lemme, upper Scrivia, Val Curone, 2020 | upper Acquese (Ponzone, Pareto ...), 2020 | 09-05 → 09-30 | [FM, 2020-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2020/): on 29 August "mentre a Fraconalto in provincia di Alessandria cadono bel 241 millimetri di pioggia, a pochissima distanza a Ponzone non si va oltre i 2 millimetri" | [FM, 2020-09-21](https://funghimagazine.it/meteofunghi-21-09-2020/): "piogge monsoniche" on the Borbera and Staffora basins, "L'Alto Monferrato tutto continua a ricevere piogge effimere, se non del tutto assenti"; rain back at Ponzone and Pareto only in early October ([FM, 2020-10-08](https://funghimagazine.it/aggiornamento-meteofunghi-08-10-2020/)) | rain-led; the fruiting reports for the higher side come from the Ligurian and Lombard sides of the same ridges; Coldiretti called the Acquese one of the richest areas that year in text recycled from 2019 |
| `acquese_ovadese_2021` | Acquese and Ovadese, normal | same, 2021 | 08-15 → 09-30 | [FM, 2021-08-25](https://funghimagazine.it/funghi-porcini-e-il-turno-del-centro-italia/): "qua tra Acquese-Ponzonese ed Ovadese non cade una pioggia degna di nota, da almeno 5 mesi" | [FM, 2021-09-24](https://funghimagazine.it/aggiornamento-meteofunghi-24-09-2021-funghi-porcini-situazione-italia/): "Piogge che, ancora una volta hanno saltato di sana pianta buona parte del Piemonte meridionale dove la siccità prosegue ad oltranza" | rain-led (no fruiting inferred, not observed); ends before the 4 October 2021 flood; 2022-2023 picking restrictions do not affect scores |
| `marcarolo_vs_cuneese_october_2021` | Capanne di Marcarolo and upper Orba, 2021 | province of Cuneo minus its Ligurian border comuni, 2021 | 10-12 → 10-31 | [FM, 2021-10-24](https://funghimagazine.it/sorpresa-quando-tutti-tacciono-e-perche-nei-boschi-e-pieno-di-funghi-porcini-aggiornamento-meteofunghi-24-10-2021/): foragers crowd "il Marcarolo o l'alto Orba" after the flood; "Al solito è rimasto a secco quasi tutto il territorio cuneese, poche piogge in poche zone fortunate di confine con il savonese" | FM, 2021-10-15 (same outlet) | FM only; fruiting on the higher side is implied by the crowds; the 4 October flood was extreme |

**Left out.** Coldiretti Alessandria's "+20 %" with "Acquese e Ovadese" better than "Novese e
Tortonese" (AcquiNews, 2023-09-26): a single release in wording recycled across 2019, 2020 and 2023,
while the red swine-fever zone limited picking to residents until 22 September 2023. Coldiretti's
"+20 %" and "richest areas" statements of 2019 and 2020 (the same text both years). Ossola 2023
against 2024 (the 2024 side is two reader comments). Val Borbera 2016 (one forager's forecast,
"secondo me"). Ovadese 2017 (a passing remark in a truffle article). The Alta Langa and Roero in
October 2023, June 2024 mountains against the Langhe, and 2023 against 2022 in the Cuneo valleys
(both good years). Anything in 2022 inside the swine-fever zone (picking banned from 13 January
2022 in 114 comuni, among them Ovada, Voltaggio, Cabella Ligure, Fabbrica Curone, Ponzone and
Bosio). Ovoli in lower Valsesia 2025 ("mai vista prima", but ovoli north of the Po were called
unusual in 2019, 2021, 2023 and 2024 too) and gallinacci in the Alta Val Tanaro in August 2020 (one
sentence): too vague to test. Nothing season-level was found for 2016-2019 outside Coldiretti, and
nothing from the Asti press, La Stampa or Il Secolo XIX (not reachable by the search tool).

**Year picture from the press** (context, not scored):

| year | north (BI, VC, VB, TO) | Cuneo | Alessandria, Asti |
|---|---|---|---|
| 2016 | — | — | dry to early October, soil "dura come cemento" in the Val Borbera woods (OvadaOnline, 2016-10-04) |
| 2017 | — | drought, "un 2017 particolarmente negativo" (Cuneodice, 2018-09-21) | drought, poor mushrooms around Ovada (L'Ancora, 2017-11-18) |
| 2018 | late August to late September buttata in the alto Piemonte (FM) | good, early start after the August rain (Cuneodice, 2018-09-21) | — |
| 2019 | good late August (Biellese, Valsesia, Ossola), with ovoli in the Biellese | — | good second half of September at Pareto and the upper Bormida (FM) |
| 2020 | poor August, strong mid-September in the upper Biellese, Valsesia and VCO (FM) | dry summer; porcini only on the Ligurian border | 29 August rain split the south-east valleys (fruiting) from the Acquese (dry to October) |
| 2021 | poor to mid-September; a late October flush on the Valsesia-Cusio border | very dry to late October, a poor spring | drought to late September; flood on 4 October, then a late October flush at Marcarolo |
| 2022 | dry to mid-August, then strong late August to mid-September | good late-May spring flush, good late August to mid-September | swine-fever ban: no signal |
| 2023 | dry August, late start, then an exceptional mid-September to early October; the Cozie weaker | good late May; July-August only the Marittime; boom in mid-September | good late September Acquese and Ovadese (Coldiretti); weak early October |
| 2024 | very wet: June-July porcini in the Torinese, none in the north; poor Biellese summer; the 5 September deluge stopped flushes; better in October | near-continuous flushes June to October | good on the Ligurian-Piedmontese Apennine (FM); drought elsewhere until 23 September |
| 2025 | Biellese early and abundant from late August; the north ahead of the Val di Susa until the 9 September rain; ovoli unusually common in lower Valsesia | strong early July, scarce late July; exceptional mid-September in Valle Po | — |

2022 and 2024 were good autumns in Piemonte, unlike the Tuscan reading of 2022 as a dry year; 2021
was the region's worst late summer of the decade, in all three press areas.

## Open questions

- **Slope (settled by the region card).** The Tuscan band (x1 to 25°, about the Tuscan woodland
  p90) would have docked ordinary Alpine woods: Piedmontese woodland cells run median 22.8°, p90
  33.9°, max 44.7°. The band now follows the region's own grid by the same rule: x1 to 34°, x0.8
  from 45°. The sun-exposure band needed no move (below 1,000 m the sun ratio spreads as in
  Tuscany).
- **Larch.** Whether Alpine larch cells deserve full habitat credit for *B. edulis* (see Porcini); the
  sanity check's Alpine contrasts are the first test.
- ***B. edulis* high window.** 15 located records set it; the backtest should compare it with the
  single Tuscan window.
- **Ovoli spread.** If ovoli keep appearing in the Alpine valleys (press, 2019-2025), the 1,000 m zero
  and the earlier season may both need revisiting with more records.
- **Pooling.** Piemonte has enough records to test season shape per key (not to tune). Pooling it with
  the Aosta valley and Lombardy's Alpine records would give the first Alpine training set.
- **Leads not read:** the Amycoforest project (ALCOTRA 2007-2013, led by Regione Piemonte with IPLA),
  which set up porcini and ovoli demonstration sites at Bosio and Molare (Alessandria) and may hold
  plot data; the Piedmontese macrofungi of the Museo Regionale di Scienze Naturali (Torino).

## References added for Piemonte

| id | kind | verified | used for |
|---|---|---|---|
| `ipla_tipi_forestali_2008` | institutional | verified | forest categories, their areas and contents, the montane-subalpine boundary |
| `rp_relazione_ambiente_foreste2024` | institutional | verified | 2016 forest map shares |
| `arpa_piemonte_precipitazioni2023` | institutional | verified | rain trends and the 2022 drought |
| `lr_piemonte_24_2007` | institutional | verified | picking law: ovoli rule, no calendar |
| `piemonte_pat_funghi_vallate` | institutional | verified | Piedmontese porcini, porcino nero, gallinaccio: season, hosts, altitude |
| `muse_censimento_edulis` | society | verified | *B. edulis* altitude range in the north-east Alps |
| `muse_censimento_pinophilus` | society | verified | *B. pinophilus* and Scots pine; phenology; altitude |
| `muse_censimento_cibarius` | society | verified | *C. cibarius* altitude and conifer hosts in the north-east Alps |
| `diez2020_alps` | peer-reviewed | verified (abstract) | upward shift of fungal fruiting in the Alps |
| `funghimagazine_alberi_porcini` | web | verified | porcini hosts by tree; not in pure larch |
| `funghimagazine_2024_10_11` | web | verified | *B. aereus* south of the Po; the 2024 ovoli flush |
| `cacciatoridifunghi_piemonte2023` | web | verified | forager altitude limits |
| `mushma_occurrence_check_piemonte_2026` | analysis | verified | month counts, enrichment, elevations, *Cantharellus* species |

Existing references the Piedmontese changes lean on: `olariaga2017` (*C. cibarius* climate and
hosts), `funghimagazine_ovolo` (ovoli altitude by region, hosts), `muse_censimento_boletus` (*B.
aereus* in the north), `beugelsdijk2008` (*B. betulicola*), `straatsma2001` and
`brejon_hoffman2026_preprint` (temperate-climate evidence behind the kept weather rules).
