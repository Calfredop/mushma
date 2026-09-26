# Emilia-Romagna: regional retune of the porcini, ovoli and gallinacci rules (evidence appendix to species-ecology.md)

Research date: 2026-09-25. Card: Emilia-Romagna region, species research item. The rule files are in
`api/src/api/config/species/emilia_romagna/`. They were copied from `tuscany/` and changed only where
the evidence below says so. Numbers marked **derived** are my conversions of qualitative or
out-of-region evidence into parameters: they are priors for the backtest, not findings. This covers
**fruiting conditions only**: nothing here is about edibility or identifying specimens.

`[R1]`… are this appendix's references. Each one is an entry in
[`references.yaml`](../../../api/src/api/config/species/references.yaml) whose `cited_as` points
here. Entries already in the shared bibliography are cited by id, for example
`borgotaro_igp_rt`. Their evidence is in the Tuscan appendices ([porcini](porcini.md),
[ovoli](ovoli.md), [gallinacci](gallinacci.md)).

## Bottom line

- **All six keys and all three groups are kept.** Every porcini taxon, the ovolo and the
  chanterelles have records in the region ([R1][R2]). The Fungo di Borgotaro IGP is the reference
  source for the four porcini (`borgotaro_igp_rt`, `borgotaro_igp_2014`), and most of its area lies
  in this region. Nothing is dropped.
- **No study in the region measures fruiting against weather.** The rain, temperature, growth-clock
  and stopper rules are Tuscany's, **kept unchanged** in every file. The Emilian slope differs from
  the Tuscan one: it is more continental and more than 1 °C colder at the same height, and it gets
  less rain overall, though its western watershed tops 2000 mm ([R3][R7]). The rules already read
  each cell's own weather, and the porcini 30-day rain is scored against the cell's own normal. So
  the climate difference reaches the score without new thresholds.
- **What changes is timing, belts and one host.** Emilia-Romagna lies north of the Apennine
  watershed, and its records peak about a month earlier than Tuscany's:
  - *B. edulis* and the ovolo peak in September, not October;
  - the chanterelles fruit mainly in the mountains in summer and early autumn, with no
    December–January lowland mode.

  The thermophilous oak–chestnut belt ends lower, and beech carries more of the woods ([R3][R4]).
  So the ovolo band comes down, the summer porcino and chanterelle bands go up, and beech becomes a
  full chanterelle host.

## Changes at a glance

"Kept" means Tuscany's value is used unchanged. Trapezoids are `[zero, full, full, zero]`, with
dates as `DD-MM` and altitudes in metres.

| key | season | altitude (m) | habitat | weather |
|---|---|---|---|---|
| `porcini_edulis` | full from **15-08** (was 01-09); rest kept: 01-07 → 15-08 … 15-11 → 20-12 | kept `[200, 700, 1600, 1900]` | kept | kept |
| `porcini_reticulatus` | kept `[01-05, 01-06, 30-09, 15-11]` | **`[0, 150, 1250, 1650]`** (was `[0, 150, 1100, 1500]`) | kept | kept |
| `porcini_aereus` | upland window (≥600 m) kept; lowland window (≤400 m) **01-07 → 15-08 … 31-10 → 30-11** (was 01-07 → 01-09 … 15-11 → 15-12) | kept `[–, –, 800, 1250]` | kept | kept |
| `porcini_pinophilus` | early flush **15-05 → 01-06 … 15-07 → 05-08** (was 01-05 → 20-05 … 30-06 → 20-07); autumn kept | kept `[300, 800, 1600, 1900]` | kept | kept |
| `ovoli_caesarea` | **01-06 → 15-08 … 15-10 → 15-11** (was 01-06 → 01-09 … 05-11 → 30-11) | **`[–, –, 700, 1000]`** (was `[–, –, 750, 1100]`) | kept | kept |
| `gallinacci_cibarius` | lowland (≤600 m) **15-04 → 10-05 … 15-11 → 15-12**, no longer wrapping into January (was … 15-12 → 25-01); mountain kept; disabled two-flush alternative trimmed the same way | **`[–, –, 1300, 1800]`** (was `[–, –, 1000, 1700]`) | **beech 1.0** (was 0.6); rest kept | kept |

Every other factor is Tuscany's, with its Tuscan sources and confidence. That covers the rain
trigger and lag, 30-day rain, temperature bands, growth clock, heat, frost, snow, drying, sun
exposure, slope, the disabled alternatives and the known gaps.

- The notes of the kept factors say so where they quote Tuscan grid numbers (slope and sun-ratio
  percentiles). Recheck those on the Emilia-Romagna grid once it is built.
- Every changed factor keeps `status: draft`, `derived: true` and `confidence: plausible`. Its
  `notes` name the rule id used here (ER-POR-S3 and so on).
- The weather is unchanged, so the confidence counts per key are Tuscany's, apart from the source
  lists.

## The region in one page

**Forest belts** ([R3][R4][R5][R6]). The region has 563,263 ha of woodland, 25 % of its area (INFC
2005). It sits almost entirely in the Apennines: the plain holds only riparian strips, the Mesola
holm-oak wood and the coastal stone and maritime pine woods of Ravenna, San Vitale, Classe and
Cervia [R3].

- **Oak and chestnut.** Mixed and xerophilous oak woods (Turkey oak, downy oak) cover the hills
  and the lower mountain, up to about 800–1000 m [R3].
  - Turkey oak woods sit at 400–900 m, "subito sotto il piano del faggio", and climb to 1400 m on
    the *argille scagliose* [R3][R4].
  - Chestnut grows throughout the submontane belt, "sempre su versanti freschi" [R3].
  - Hop-hornbeam woods are among the three largest forest categories.
- **Beech.** Beech forms "una fascia pressoché continua tra 1000 e 1600-1700" m [R4].
  - Its lower, temperate part runs from 1000 to 1400 m in the west and from 700 to 1250 m in the
    east [R3]. Up to 1100–1200 m it mixes with Turkey oak and chestnut [R4].
  - Its upper limit is also the treeline, "intorno ai 1700 metri" [R3]. On Prado and Cusna, 80 % of
    the treeline lies between 1651 and 1775 m [R5]. The highest beech woods are at 1650 m on Monte
    Falco (Romagna) and 1800 m at Corno alle Scale (Emilia).
  - Above the beech, Emilia has grassland and bilberry heath [R4].
  - Only about 0.5 % of the hill and mountain woodland lies above 1600 m [R6].
- **Silver fir.** Fir occurs in fir–beech woods: Sasso Fratino and Campigna in the Casentinesi, the
  Abetina Reale, Monte Penna [R3]. In the Casentinesi the fir–beech mix runs from 900 to
  1250(1350) m [R4].
- **Conifer plantations.** Black pine and Douglas fir were planted from the 1920s to the 1950s
  [R3].
- **Management.** 80 % of the beech woods are coppice [R3]. In the Borgotaro IGP area, high forest
  yields markedly fewer mushrooms than coppice, and abandoned or aged woods yield fewer than tended
  ones [R11]. That is a known gap, not a rule (`porcini_edulis`, `stand_and_soil`).

**Against Tuscany.** Tuscany's beech belt is 900–1700(1800) m and its fir 900–1300(1500) m
(`rt_tipi_forestali_p4`), so the upper limits match. The difference is climatic: on the Po side
the warm belt ends lower. The January 0 °C isotherm sits at 1000 m on the Po side against 1300 m on
the Tuscan side. The "temperate-cool" climate starts at 682 m (Pavullo) against 1340 m (Boscolungo)
[R7].

**Climate** ([R3][R7][R8]).

- **Rain.** Rain peaks at over 2000 mm a year on the Emilia–Liguria watershed and falls to about
  1500 mm on the eastern ridge [R3]. Monchio delle Corti had 2061 mm in 1961–1990 [R8]. Rain falls
  to 1600–1800 mm at 800–900 m and 1000–1200 mm at 500–600 m [R3].
- **Seasonality.** The regime peaks in autumn: November is wettest and July driest (Sestola) [R7].
- **Temperature.** At the same height, Romagna is warmer than Emilia [R3].
- **Against Tuscany.** The Tuscan side is much rainier: over 2500 mm west of the watershed on the
  Livorno–Cimone transect, against no more than 1500 mm east of it [R7].
- **Recent change.** 1991–2015 was 1.1 °C warmer than 1961–1990, with "estati più aride e autunni
  più piovosi" [R8].

These facts back the belt and timing changes. They do not change a weather threshold: the rules
read the cell's own weather.

**Picking law** ([R9]). L.R. 6/1996 sets **no season or month window**:

- picking is allowed on Tuesday, Thursday, Saturday and Sunday, from an hour before sunrise to an
  hour after sunset;
- the limit is 3 kg a day, of which at most 1 kg of *A. caesarea* and *Calocybe gambosa*;
- closed ovoli may not be picked;
- the minimum cap is 3 cm for the porcini group and 2 cm for *C. cibarius*.

Parks and mountain unions add permits and local limits. The IGP harvest period (1 April–30
November, `borgotaro_igp_2014`) is also a legal frame, not an ecological window. None of these is
encoded: the app forecasts conditions, not what is legal to pick.

## Occurrence check (Emilia-Romagna)

**Method.** This follows the Tuscan season cross-check (species-ecology.md). It was run on
2026-09-25, and only aggregates are reported: no coordinates were stored or published [R2].

- **iNaturalist:** `place_id=96905` (Emilia-Romagna), verifiable, all quality grades; one month
  histogram per taxon.
- **Enrichment:** each taxon's monthly share divided by the monthly share of **all fungi** recorded
  in the region (15,865 observations; October 3,164, September 2,328, November 2,145). A value
  above 1 means the taxon is over-represented that month relative to observer effort.
- **Elevations:** from the Open-Meteo elevation service, at the records with open coordinates.
- **GBIF** (`gadmGid=ITA.6_1`) adds almost nothing independent: its records are mostly the same
  iNaturalist ones. It holds no `MATERIAL_SAMPLE` rows here.

| taxon | n | months with records | enrichment (>1 in bold) | elevation p10 / p25 / median / p75 / p90 / max (n) |
|---|---|---|---|---|
| *B. edulis* | 25 | Apr 1, Jul 1, Aug 4, Sep 17, Oct 2 | Aug **2.8**, Sep **4.6**, Oct 0.4 | 336 / 1069 / 1209 / 1407 / 1496 / 1586 (22) |
| *B. reticulatus* | 25 | May 2, Jun 4, Jul 4, Aug 4, Sep 9, Oct 2 | Jun **4.3**, Jul **3.6**, Aug **2.8**, Sep **2.5**, Oct 0.4 | 594 / 791 / 1105 / 1264 / 1376 / 1617 (16) |
| *B. aereus* | 11 | Apr 1, Sep 10 | Sep **6.2** | 308 / 376 / 504 / 688 / 1003 / 1386 (8) |
| *B. pinophilus* | 4 | Sep 2, Oct 2 | — | 1040 (1) |
| *A. caesarea* | 16 | Jul 1, Aug 2, Sep 11, Oct 2 | Aug **2.2**, Sep **4.7**, Oct 0.6 | 393 / 537 / 563 / 601 / 660 / 711 (7) |
| *Cantharellus* (genus) | 38 | May 3, Jun 5, Jul 7, Aug 5, Sep 11, Oct 6, Nov 1 | Jun **3.5**, Jul **4.1**, Aug **2.3**, Sep **2.0**, Oct 0.8, Nov 0.2 | 424 / 637 / 947 / 1176 / 1359 / 1652 (27) |

**By elevation** (records with open coordinates):

- *B. edulis*: 17 of 22 at 1000 m or higher, those from August to October (plus one in April).
- *B. reticulatus*: 10 of 16 at 1000 m or higher, June to October.
- *A. caesarea*: all 7 below 720 m, September and October.
- *Cantharellus*: below 600 m (n=6) May to November; 600–1000 m (n=9) July to October; 1000 m and
  higher (n=12) June to October.

***Cantharellus* names.** The records are *C. cibarius* 12, *C. pallens* 10, *C. amethysteus* 4,
*C. friesii* 1, and 11 at genus level. Both the temperate segregates (*cibarius* s.str.,
*amethysteus*) and the Mediterranean one (*pallens*) are present. Their elevations overlap
(medians 865 and 953 m), so no split by name is attempted.

**Against Tuscany.**

- Tuscan *B. edulis* and ovolo records peak in October; the median ovolo record is 13 October.
  Emilia-Romagna's peak in September.
- Tuscan *Cantharellus* records peak in October–November, run into December–January and have a
  median of 289 m. Emilia-Romagna's peak in June–September, stop in November and sit 650 m higher.

**A second, independent signal** comes from picking permits for the Albareto reserve, the IGP
heartland, in 2020 [R10]:

| Jun | Jul | Aug | Sep | Oct | Nov |
|---|---|---|---|---|---|
| 253 | 10 | 123 | 6,818 | 1,031 | 1 |

These count effort, not fruiting, in one year (a COVID year, with a stormy October), but they point
the same way as the records.

**Caveats.**

- The samples are tiny and presence-only, and the records sit near roads and towns.
- 2024–2026 supply most of the records.
- I used all seasons. So these numbers are priors, and the season, altitude and habitat gates stay
  frozen in the backtest (`model.yaml`, `frozen_factor_kinds`).

## Porcini

**What stays.**

- **Weather.** Every weather rule, growth clock and stopper of the four keys is kept. The only
  field study with numbers is still Amiata (`salerni2023_amiata`), a Tuscan fir plantation at
  about 1050 m. That is the same kind of site as the Emilian fir–beech belt, so it transfers here
  at least as well as it does elsewhere in Tuscany.
- **Hosts.** All four habitat tables are kept. The IGP host list they rest on belongs to Val Taro,
  in this region:
  - beech, chestnut, Turkey and other oaks, hornbeam, hazel and aspen;
  - silver fir and spruce, black and Scots pine, Douglas fir.

  The regional sources agree. The Casentinesi atlas has *B. edulis* in conifer and broadleaf woods
  alike, and *B. aestivalis* "soprattutto nei boschi di latifoglie, ma talvolta anche sotto
  conifere (Picea)" [R1]. Regione Emilia-Romagna restricts *B. reticulatus* "di preferenza … alle
  latifoglie" [R12].
- **Region-specific habitats.** Macchia and evergreen oak, hosts for *B. aereus* in Tuscany, are
  nearly absent here. Their affinities barely matter, and they are kept rather than invented.

**ER-POR-S3, *B. edulis* season: full from 15 August (was 1 September).**

- The IGP says "da fine settembre alla prima neve, rare le forme estive" (`borgotaro_igp_rt`).
- Three regional sources put it earlier:
  - the Casentinesi atlas (Romagna side): "dalla fine estate al tardo autunno" [R1];
  - Regione Emilia-Romagna: "da luglio all'autunno" [R12];
  - the park-side records span 4 July to 8 November [R1].
- The regional records are over-represented in August (2.8×) and September (4.6×) and
  under-represented in October (0.4×) [R2]. Central Italy's are over-represented from August to
  October (1.8×, 3.1×, 1.7×; `mushma_occurrence_check_2026`).
- The Albareto permits (September ≫ October ≫ August) agree on the September peak, but not on
  August [R10].
- So the plateau starts two weeks earlier and the ramp is unchanged. **The end is kept**: frost,
  snow and temperature already time the close on the colder Emilian side, and two October records
  are too few to cut on.
- Derived; plausible.

**ER-POR-S2, *B. aereus* lowland window: full 15 August–31 October, zero by 30 November (was
1 September–15 November, zero by 15 December).**

- The Tuscan autumn peak (October–November) comes from Lucca and Siena sources on macchia and holm
  oak. Emilia-Romagna has almost no macchia.
- Here *B. aereus* is a hill species. The Casentinesi atlas lists it among the thermophilous fungi
  missing from the park's mountain forests but "sicuramente" present "nelle aree collinari" [R1].
- The records are 10 of 11 in September (6.2×), with none in October or November [R2].
- The IGP (Val Taro) says July–September. The Piacenza-Apennine page puts it in autumn oak woods
  [R13].
- The upland window (≥600 m, full 1 August–30 September) is **kept**: it already follows the IGP,
  shifted to August for the missing July records.
- Derived; plausible.

**ER-POR-S4, *B. pinophilus* early flush: zero before 15 May, full 1 June–15 July, zero by
5 August (was full 20 May–30 June).**

- The IGP says the summer form is "presente da giugno" in chestnut, and the autumn form fruits in
  beech and silver fir.
- The Casentinesi atlas: "fa una prima comparsa all'inizio dell'estate e riappare poi ad autunno
  avanzato, con i primi freddi" [R1].
- Both are regional sources and both put the first flush in early summer, not late spring. Tuscany
  had it from May, on Trentino records.
- The autumn window is **kept**: the four regional records (September–October) fit it, and
  temperature does the "primi freddi" timing.
- The early flush remains the least certain window of the four taxa.

***B. reticulatus* season: kept.**

- The IGP says May–September. The Casentinesi atlas says "già all'inizio estate", with dated
  records from 25 June to 3 September [R1].
- The regional enrichment (June–September 4.3×, 3.6×, 2.8×, 2.5×; October 0.4×) has central
  Italy's shape.

**ER-POR-A1, *B. edulis* altitude: kept `[200, 700, 1600, 1900]`.**

- The plateau (700–1600 m) spans the chestnut belt and the whole beech belt (1000–1600/1700 m,
  lower in the east) [R3][R4].
- Above about 1700 m the woods end [R5]. The habitat gate removes that grassland, so the upper ramp
  does no harm.
- The regional records fit the band: p10 336 m, median 1209 m, p90 1496 m, max 1586 m [R2].
- Val Taro foragers put all four porcini "fra i 500 e i 1500 metri" under "cerri, querce, castagni
  e faggi", on mostly north-facing slopes [R14] (folklore).

**ER-POR-A3, *B. reticulatus* altitude: full to 1250 m (was 1100), zero at 1650 m (was 1500).**

- The summer porcino follows chestnut and oak. Here that belt runs into the lower beech belt: up to
  1100–1200 m the beech mixes with Turkey oak and chestnut, and Turkey oak reaches 1400 m on clay
  [R3][R4].
- The regional records sit higher than central Italy's (median 714 m, p90 1272 m):
  - median 1105 m, p75 1264 m, p90 1376 m, maximum 1617 m [R2];
  - the park dates them at Campigna and Sasso Fratino, at about 900–1100 m, from June [R1].
- The plateau ends at about the record p75, and the band reaches zero at the upper beech limit
  (Monte Falco 1650 m; the treeline is mostly at 1651–1775 m) [R4][R5].
- Some high records may be early *B. edulis*. The porcini group takes the max over its keys, so
  the overlap costs little.
- The habitat stays Tuscany's: a pure beech cell already saturates at the beech affinity of 0.6.

***B. aereus* altitude: kept `[–, –, 800, 1250]`.**

- The regional records sit inside the band: median 504 m, p75 688 m, p90 1003 m (n=8) [R2].
- The colder Emilian side (January 0 °C isotherm 300 m lower [R7]) is left to the temperature
  driver rather than a lower band. A lower band would count the cold twice.

***B. pinophilus* altitude: kept `[300, 800, 1600, 1900]`.** The band spans the chestnut and beech
belts. The one regional record with open coordinates is at 1040 m.

## Ovoli

**What stays.** The weather rules, the growth clock and the stoppers are kept.

- They come from Tuscan community studies, Open-Meteo climatology over the Tuscan season, and
  lore. No regional source adds numbers.
- The cold-nights stopper and the soil-temperature driver already close the season on the colder
  Emilian side.

**Hosts: kept.**

- Oak and chestnut are hosts. The Casentinesi atlas: "legata ai boschi termofili di castagni e
  querce" [R1]. Regione Emilia-Romagna: "in estate-autunno in boschi di latifoglie, soprattutto di
  castagni e querce, nelle radure, in terreno siliceo" [R12].
- The Piacenza-Apennine page adds acid-soil oak and chestnut woods, "prettamente termofila" [R13].
- The Casentinesi atlas notes the species is uncommon in the park and declining with the abandoned,
  once-"puliti" chestnut groves [R1]. That fits the Tuscan canopy-management gap (OVO-18/19), which
  stays a known gap.

**ER-OVO-01, season: full 15 August–15 October, zero by 15 November (was 1 September–5 November,
zero by 30 November).**

- Tuscany's window follows a median record of 13 October. The regional records peak a month
  earlier [R2]:
  - over-represented in August (2.2×) and September (4.7×; 11 of 16 records);
  - under-represented in October (0.6×), with none after October.
- The Piacenza-Apennine page: the ovolo is favoured by "le prime piogge di settembre" [R13].
- Funghi Magazine: fruiting "esclusivamente" June–October (`funghimagazine_ovolo`).
- The Casentinesi atlas has a late-spring and an autumn appearance [R1]. The early-summer ramp from
  1 June is **kept**, so a storm flush can score while the moisture rules do the limiting.
- Derived; plausible.

**ER-OVO-03, altitude: full to 700 m (was 750), zero at 1000 m (was 1100).**

- Tuscany's band follows the Italian p90 (752–769 m) and a record maximum of 943 m.
- On the Po side the thermophilous belt ends lower: the January 0 °C isotherm is 300 m lower, and
  the temperate-cool climate starts 650 m lower [R7].
- Funghi Magazine gives 800–900 m as the limit in the northern sub-Apennine hills, against about
  1000 m in the central-southern Apennines (`funghimagazine_ovolo`). InNatura calls it uncommon in
  northern Italy (`innatura_ovolo`).
- The regional records are all below 720 m (median 563 m, n=7) [R2]. The Casentinesi park has a
  single record in its mountain forests [R1].
- The plateau ends at the record maximum, and the band reaches zero just above the quoted northern
  limit.
- Derived; plausible.

## Gallinacci

**What stays.**

- **Weather.** All the weather rules are kept: rain over 30 days, rain frequency, the long-lag
  trigger, soil temperature, the 60-day water balance, heat, frost, snow and drying. No regional
  source adds numbers.
- **Soil pH.** The acid-soil rule stays disabled. The regional leaflet's "terreni silicei" [R12]
  supports it, and the Emilian Apennines have large calcareous and clay areas [R3][R4], but a
  soil-pH rule is a Tuscan card's decision (GAL-20). It is kept as is.

**Which chanterelles.**

- The European revision keeps *C. cibarius* s.str. out of Mediterranean climates (`olariaga2017`).
  So the Tuscan records are mostly *C. pallens* and *C. alborufescens*.
- The Emilian Apennines are sub-continental. The Casentinesi atlas lists *C. cibarius* among the
  "nordic" fungi of its forests and records *C. amethysteus* at Campigna and Camaldoli [R1].
- The regional records mix *C. cibarius* (12), *C. pallens* (10) and *C. amethysteus* (4) [R2].
- One s.l. rule set still fits. Its centre of gravity shifts to the mountains, in summer.

**ER-GAL-02, lowland season: full 10 May–15 November, zero by 15 December (was full to
15 December, zero by 25 January).**

- Tuscany's December–January lowland mode belongs to the coastal Mediterranean segregates.
- Emilia-Romagna has no record from December to April (n=38). Its lowland records (<600 m) run from
  May to November [R2]. The latest Casentinesi date is 17 November [R1].
- Regione Emilia-Romagna: "da giugno a novembre" [R12]. 3B Meteo: the Apennine season is "tra
  giugno e ottobre", with November only in the south and on the coast (`bmeteo_cantharellus`). The
  Piacenza-Apennine page: "da giugno" in oak and chestnut [R13].
- The spring start and the summer inside the window are **kept**. The moisture and heat rules make
  the summer gap, and rainy summers do fruit.
- The mountain window (≥1000 m, full 1 July–15 October) is **kept**. Records at 1000 m and above run
  from June to October, and at 600–1000 m from July to October [R2].
- The 600–1000 m handover is kept.
- The disabled two-flush alternative's autumn end is trimmed the same way.
- Derived; plausible.

**ER-GAL-05, habitat: beech moves from secondary (0.6) to host (1.0).**

- In Tuscany beech stayed secondary for want of plot numbers. Here the group fruits mainly in the
  mountains: the median record is 947 m, and 12 of 27 records are at 1000 m or higher, in the
  beech belt [R2].
- The temperate segregates that go with beech are recorded in the Casentinesi forests [R1]. The
  Apennine hosts are "faggi, querce e castagni" (`bmeteo_cantharellus`).
- Everything else is kept. Evergreen oak stays a host for the coastal segregates, but in this
  region it covers only the Mesola wood and patches in the Ravenna pinewoods [R3].
- A pure beech cell already saturated at 0.6. The change matters for mixed cells where beech is a
  minority.
- Derived; plausible.

**ER-GAL-06, altitude: full to 1300 m (was 1000), zero at 1800 m (was 1700).**

- The regional records: p10 424 m, median 947 m, p75 1176 m, p90 1359 m, max 1652 m [R2].
  Tuscany's: median 289 m, p90 740 m.
- The plateau ends at about the record p90, which is also the top of the eutrophic beech type
  (1000–1300(1400) m) [R4].
- The band reaches zero at 1800 m: the highest beech wood in Emilia (Corno alle Scale), above which
  there is heath and grassland [R4].
- The popular "rarer from 1500 m" (`cacciatoridifunghi_finferli`) sits on the ramp.
- Derived; plausible.

## Dropped keys and groups

None. Every key has regional records and a regional or IGP source (table above; `borgotaro_igp_rt`,
[R1]).

- ***B. pinophilus*** has the thinnest evidence: 4 iNaturalist records, and "piuttosto rara" in the
  Casentinesi park [R1]. But it is one of the four IGP porcini of Val Taro ("moro"), so it stays.
  The porcini group takes the max over its keys, so a weak key cannot lower it.
- ***B. aereus*** is a hill species here and absent from the mountain forests [R1]. Its altitude and
  habitat gates already keep it out of the beech belt.
- **Ovoli** are uncommon and declining [R1], but they have been recorded every recent year and are
  regulated by name in the regional law [R9].

## Sanity contrasts

`sanity.yaml` holds **12 porcini contrasts** on 9 seasons (2016–2025 except 2021, which appears only
among the normal years) and 13 areas, from the Piacenza Apennines to the Alto Savio. I opened every source and checked the quoted words on the
page myself; the table quotes them.

The areas are lists of ISTAT comuni. `api.model.sanity` matches them on the grid's `comune_name`,
and every name was checked against the ISTAT 2025 boundaries (COD_REG 8).

Contrasts of one year against "normal" years list the normal years (2017–2025) without the year
under test.

| id | kind | higher | lower | quote | source |
|---|---|---|---|---|---|
| `cerreto_2017_2016` | same area, two years | Ventasso 2017, 1–9 Oct | Ventasso 2016, 1–9 Oct | "l'anno scorso l'avevamo svangata con 30 chili mentre quest'anno le faggete ci hanno regalato oltre 200 chili" (Mondiale del fungo, Cerreto Laghi) | [blog, 11 Oct 2017](https://blogfunghi.parcoappennino.it/un-mondiale-da-sogno/) |
| `crinale_2019` | one year vs normal | Reggio–Parma crinale 2019, 6–20 Sep | same, other years | "in cinquant'anni che vado per funghi, una nascita del genere non l'avevo mai vista" | [blog, 18 Sep 2019](https://blogfunghi.parcoappennino.it/il-troppo-stroppia-o-no/) |
| `reggio_vs_valtaro_2019` | same year, two areas | Reggio–Parma crinale 2019, 8–16 Sep | Val Taro and Val Ceno 2019 | "la parte del leone la sta' facendo la parte reggiana … Valtaro e Valceno sono in ritardo" | [blog, 16 Sep 2019](https://blogfunghi.parcoappennino.it/sfogatevi-popolo-di-fungaioli/) |
| `ceno_vs_albareto_2018` | same year, two areas | Bardi, Varsi, Berceto, Corniglio 2018, 1–17 Aug | Albareto 2018 | "nascite abbondanti di estatini … Valceno … bercetese … Corniglio"; "Qui ad Albareto invece il porcino ancora è latitante" | [blog, 17 Aug 2018](https://blogfunghi.parcoappennino.it/venerdi-17-ma-non-per-tutti/) |
| `valtaro_aug_2017` | one year vs normal | Val Taro and Val Ceno, other years, 1–16 Aug | same, 2017 | "uno, due o forse tre funghi, ma di buttate da estivo manco l'ombra" | [blog, 16 Aug 2017](https://blogfunghi.parcoappennino.it/eccoci-qui/) |
| `valnure_2022` | one year vs normal | Farini, Ferriere 2022, 25 Aug–11 Sep | same, other years | "Era da vent'anni che non si raccoglieva così tanto, per quantità e qualità del fungo" | [Libertà, 11 Sep 2022](https://liberta.it/news/attualita/cronaca/lalta-val-nure-torna-il-paradiso-dei-fungaiolima-fioccano-le-multe/7242) |
| `modena_2022` | one year vs normal | Modena Apennines 2022, 20 Aug–13 Sep | same, other years | "un'annata record … come non si vedeva da tempo", after seasons "spesso scarse o addirittura prive di prodotto" | [Parco del Frignano, 13 Sep 2022](https://www.parks.it/parco.frignano/dettaglio.php?id=71099) |
| `west_vs_east_2023` | same year, two areas | Ligurian-border comuni (Piacenza, Parma) 2023, 1–12 Oct | Modena, Bologna and Romagna Apennines, Montefeltro 2023 | "migliori ad occidente, al confine con la Liguria … quasi assenti già in quella di Modena, del tutto assenti da Bologna a San Marino" | [Funghi Magazine, 12 Oct 2023](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/) |
| `frignano_2024_timing` | same area and year, two windows | Pievepelago, Riolunato 2024, 10–20 Jul | same, 28 Jul–6 Aug | "un exploit di rilievo a metà luglio con bottini abbondantissimi"; now "un momento di pausa … prolungata siccità" | [Carlino, 6 Aug 2024](https://www.ilrestodelcarlino.it/economia/boom-porcini-appennino-mirtilli-0794c3f3) |
| `valtrebbia_2025_timing` | same area and year, two windows | Bobbio, Coli 2025, 1–8 Sep | same, 16–31 Aug | "Poco prima di Ferragosto … c'era stata una 'buttata' moderata che si è esaurita in fretta"; "da questa settimana le piogge dello scorso lunedì hanno avviato la stagione del porcino" | [Libertà, 8 Sep 2025](https://liberta.it/news/attualita/record-di-porcini-in-val-trebbia-una-buttata-eccezionale/99289) |
| `parma_est_2020_timing` | same area and year, two windows | Unione Appennino Parma Est 2020, September | same, 3–20 Oct | "un settembre ricco e felice"; storms and tramontana "hanno letteralmente bloccato la crescita dei funghi porcini" | [ilParmense, 20 Oct 2020](https://www.ilparmense.net/raccolta-funghi-2020-ottima-stagione-appennino-parmense/) |
| `alto_savio_2024` | one year vs normal | Bagno di Romagna, Verghereto 2024, Sep–Oct | same, other years | the 2024 season was "fra le più copiose degli ultimi decenni" | [Carlino Cesena, 3 Apr 2025](https://www.ilrestodelcarlino.it/cesena/cronaca/tesserini-per-la-raccolta-funghi-771c9e32) |

**Caveats.**

- **One writer behind five contrasts.** Five contrasts come from the Parco dell'Appennino
  Tosco-Emiliano's mushroom blog ("Fra' Ranaldo", written from Albareto). It is one forager's dated
  account, not a survey.
- **`cerreto_2017_2016`.** Entries rose from about 500 to 690 between the two years, so the catch
  per head still rose about fivefold.
- **`valnure_2022` and `modena_2022`.** They describe the late-summer flush that followed the
  record-dry January–July of 2022. They are a good test of how the rules recover after a drought.
- **`alto_savio_2024`.** It is a season-level claim written the following spring, so its window is
  the whole of September–October.
- **Weather coverage.** `cerreto_2017_2016` reads October 2016. It needs the weather history to
  cover 2016 with at least 43 days of lookback before 1 October.
- **Candidates left out:**
  - two funghimagazine lines that are partly forecasts (late August 2025 Emilia vs Romagna; early
    November 2022);
  - Bologna 2022 vs 2023 (the 2022 side rests on single big finds);
  - Romagna 2023 vs 2024 and Modena 2023 vs 2024 (each pairs a season-level claim with another
    source).

  Borgotaro town itself has no strong "good year" claim among the pages found. It appears only on
  the low side (`ceno_vs_albareto_2018`) or as "late" (`reggio_vs_valtaro_2019`).

## Open questions

1. **The ovolo and chestnut decline.** The Casentinesi atlas ties the ovolo's retreat to the
   abandonment of tended chestnut groves [R1]. A canopy or management layer would matter more here
   than in Tuscany, where holm oak and macchia hold part of the ovolo habitat.
2. **A soil-pH proxy for gallinacci.** The regional forest map (Carta forestale 2025, WMS
   `aree_forestali`) uses types that split some classes by substrate. The Emilian clays and marls
   would make a pH proxy more useful than in Tuscany. It is not used: grid work, not a rule.
3. **Rain scale.** The `precipitation_scale` was fitted on Tuscan gauges. The Emilian slope is
   drier than the Tuscan one at the same height, except on the western watershed [R3][R7]. A gauge
   check against Arpae stations should decide whether this region needs its own `model:` override.
   That is not a species decision.
4. **Weak points.** The *B. pinophilus* early flush and the *B. edulis* mid-August start rest on
   qualitative sources and a handful of records. The backtest cannot tune them, because the season
   gates are frozen. If the region gets more records, re-derive them from the training seasons only.
5. **The Borgotaro "fungometro".** The Consorzio's daily ratings for Val Taro (fungodiborgotaro.com)
   would make a far better sanity series than press stories. Only the current year is online, and
   the web archive could not be reached from here.

## References

- [R1] Padovan F. (2009) *Atlante illustrato dei funghi del Parco. 845 specie di funghi nel Parco
  Nazionale delle Foreste Casentinesi* (texts F. Padovan, D. Ubaldi). Ente Parco Nazionale delle
  Foreste Casentinesi, Monte Falterona e Campigna. ISBN 978-88-95719-00-9.
  https://www.parcoforestecasentinesi.it/sites/default/files/images/cartella_ricerca/libro%20atlante%20funghi.pdf
  `verified` (full PDF). Supports: dated records and habitat notes for the park's Romagna and
  Tuscan sides:
  - *B. edulis* "dalla fine estate al tardo autunno";
  - *B. aestivalis* from early summer;
  - *B. pinophilus* early summer and "autunno avanzato", rare;
  - *A. caesarea* in thermophilous chestnut and oak woods, uncommon and declining;
  - *C. cibarius* 25 June–17 November, one of the "nordic" fungi;
  - *B. aereus* absent from the mountains, expected in the hills.
- [R2] mushma occurrence cross-check for Emilia-Romagna, 2026-09-25: iNaturalist (place 96905),
  GBIF (ITA.6_1) and the Open-Meteo elevation API. Aggregates only. `verified` (own queries).
  Supports: the Occurrence check section.
- [R3] Regione Emilia-Romagna (2016) *Piano Forestale Regionale 2014-2020, Quadro conoscitivo*.
  https://ambiente.regione.emilia-romagna.it/it/parchi-natura2000/foreste/pianificazione-forestale/piano-forestale-regionale/documenti-nuovo-piano-forestale-regionale/il-quadro-conoscitivo-del-piano-forestale-2014-2020/@@download/file
  `verified` (full PDF). Supports:
  - forest belts: beech lower subzone and treeline, Turkey oak on clay, chestnut on cool slopes;
  - climate: January 0 °C isotherm, rain gradient, Romagna warmer than Emilia;
  - forest statistics and the coppice share.
- [R4] Camerano P., Varese P., Grieco C. (IPLA) for Regione Emilia-Romagna (2006) *Prodromi della
  tipologia forestale dell'Emilia-Romagna*.
  https://ambiente.regione.emilia-romagna.it/it/parchi-natura2000/foreste/le-foreste-dellemilia-romagna/articoli-e-contributi/indagini/relazione200701.pdf/@@download/file/relazione200701.pdf
  `verified` (full PDF). Supports:
  - beech 1000–1600/1700 m, highest at Monte Falco 1650 m and Corno alle Scale 1800 m;
  - the lower beech belt mixing with Turkey oak and chestnut up to 1100–1200 m;
  - eutrophic beech 1000–1300(1400) m; Turkey oak 400–900 m;
  - Casentinesi fir–beech 900–1250(1350) m.
- [R5] Pezzi G., Bitelli G., Ferrari C., Girelli V.A., Gusella L., Masi S., Mognol A. (2007) Pattern
  temporale del limite altitudinale dei boschi di faggio nell'Appennino settentrionale. *Forest@*
  4(1): 79–87. https://doi.org/10.3832/efor0440-0040079 `verified` (full PDF). Supports: the
  Emilian treeline on Prado and Cusna lies between 1538 and 1804 m, 80 % of it at 1651–1775 m.
- [R6] Regione Emilia-Romagna (2006) *Inventario Forestale Regionale, risultati finali* (surveys
  1984–1994).
  https://ambiente.regione.emilia-romagna.it/it/parchi-natura2000/foreste/quadro-conoscitivo/inventari-e-carte-forestali/inventario-forestale/IFER_dati_finali.pdf/@@download/file/IFER_dati_finali.pdf
  `verified` (full PDF). Supports: woodland area by 200 m altitude class (about 0.5 % above
  1600 m); area by forest type.
- [R7] Rapetti F., Vittorini S. (1989) Aspetti del clima nei versanti tirrenico ed adriatico lungo
  l'allineamento Livorno-Monte Cimone-Modena. *Atti della Società Toscana di Scienze Naturali, Mem.
  A* 96: 159–192. http://www.stsn.it/AttiA1989/piccini-pranzini/rapetti-vittorini.pdf `verified`
  (full PDF). Supports the Tuscan vs Emilian slope comparison:
  - rain over 2500 mm west of the watershed, no more than 1500 mm east of it;
  - the Tuscan side over 1 °C warmer at the same height;
  - the January 0 °C isotherm at 1300 vs 1000 m;
  - the temperate-cool climate from 1340 vs 682 m.
- [R8] Antolini G., Pavan V., Tomozeiu R., Marletto V. (eds.) (2017) *Atlante climatico
  dell'Emilia-Romagna 1961-2015*. Arpae.
  https://www.arpae.it/it/temi-ambientali/clima/rapporti-e-documenti/atlante-climatico/atlante-climatico-1961-2015
  `verified` (full PDF). Supports: +1.1 °C (1991–2015 vs 1961–1990), drier summers and wetter
  autumns; municipal normals (Monchio delle Corti 2061 mm, Sestola 1046 mm).
- [R9] Regione Emilia-Romagna, L.R. 2 aprile 1996 n. 6 (consolidated with L.R. 38/2001, 7/2004,
  15/2011).
  https://demetra.regione.emilia-romagna.it/al/articolo?urn=er:assemblealegislativa:legge:1996%3B6
  `verified`. Supports: picking days, hours and quantities; no season window; the ovolo limits.
- [R10] Scuola Superiore Sant'Anna, Consorzio Comunalie Parmensi (c. 2023) *Progetto CO2SINK,
  allegato 2*. https://www.comunalie.com/dati/progetti/allegato2_202305275448.pdf `verified` (full
  PDF). Supports: Albareto picking permits in 2020 by month (Tabella 1).
- [R11] Consorzio per la tutela dell'IGP Fungo di Borgotaro, "La selvicoltura".
  https://www.fungodiborgotaro.com/ita/6/la-selvicoltura/ `verified`. Supports: oak and chestnut
  below, beech and planted fir above; coppice more productive than high forest; tended woods more
  productive than abandoned ones.
- [R12] Regione Emilia-Romagna, *Alcune delle specie più comuni di funghi commestibili presenti in
  Emilia-Romagna* (leaflet).
  https://ambiente.regione.emilia-romagna.it/it/parchi-natura2000/sistema-regionale/funghi-sottobosco-tartufi/funghi-allegati/funghi-commestibili/@@download/file
  `verified` (full PDF). Only the habitat and season lines are used:
  - *A. caesarea*: chestnut and oak, clearings, siliceous soil, summer–autumn;
  - *B. edulis*: "da luglio all'autunno";
  - *C. cibarius*: "da giugno a novembre", moist siliceous soils.
- [R13] Tasselli M. *I funghi nelle Quattro Province*. Dove comincia l'Appennino.
  https://www.appennino4p.it/funghi `verified` (**folklore**-level local page for the Piacenza,
  Pavia, Alessandria and Genoa Apennines). Supports:
  - *B. aestivalis* from June under oak and chestnut;
  - *B. edulis* in autumn under beech; *B. aereus* in autumn oak woods;
  - the ovolo after the first September rains;
  - finferli from June in oak and chestnut.
- [R14] montagnatore (2013) Andare a funghi in val Taro (blog).
  http://montagnatore.blogspot.com/2013/09/andare-funghi-in-val-taro.html `verified`
  (**folklore**). Supports: all four porcini at 500–1500 m under Turkey oak, oak, chestnut and beech
  in Val Taro; mostly north-facing woods.

**Shared references re-used here** (already in `references.yaml`, cited by id):

- `borgotaro_igp_rt`, `borgotaro_igp_2014`: the IGP months, hosts and harvest dates. The area is
  Berceto, Borgo Val di Taro, Albareto, Compiano, Tornolo and Bedonia, plus Pontremoli and Zeri in
  Tuscany. It sets no altitude limit.
- `museo_porcino_borgotaro`: Borgotaro porcini habitats.
- `salerni2023_amiata`: the only porcini field weather study.
- `matteucci2008_micoponte`, `muse_censimento_boletus`: taxon altitude and habitat notes.
- `funghimagazine_ovolo`: the ovolo's northern altitude limits and June–October season.
- `innatura_ovolo`, `iucn_caesarea2019`: ovolo range and altitude.
- `olariaga2017`: chanterelle segregates and climate.
- `bmeteo_cantharellus`: Apennine chanterelle season and hosts.
- `cacciatoridifunghi_finferli`: chanterelle altitude.
- `mushma_occurrence_check_2026`: central-Italy enrichment, for comparison.
- `rt_tipi_forestali_p4`: Tuscan belts, for comparison.
- `mushma_habitat_share_2026`: the four habitat levels.
