# Species ecology: Veneto (regional appendix to species-ecology.md)

Research date: 2026-09-29 (dates Europe/Rome, units metric). Card: `region-veneto-species.md`
(child of `region-veneto.md`). Rule files: `api/src/api/config/species/veneto/`. This appendix
records how the Tuscan rule set (`species/tuscany/`) was carried to Veneto, what changed and why. It
covers **fruiting conditions only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(21 added for this region, in one block at the end of the file, keys prefixed `ven_` or with a
`_veneto_` infix). Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md):
**strong**, **plausible**, **folklore**. Every number is a prior for the backtest; season windows,
altitude bands and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`). The
two Alpine neighbours, Friuli-Venezia Giulia ([`friuli_venezia_giulia.md`](friuli_venezia_giulia.md))
and Trentino-Alto Adige ([`trentino_alto_adige.md`](trentino_alto_adige.md)), were the templates;
Lombardia ([`lombardia.md`](lombardia.md)) and Emilia-Romagna
([`emilia_romagna.md`](emilia_romagna.md)) were read for method and sources.

## Summary

1. **All three groups and all six keys are kept.** Every key has Veneto records and a regional
   source; the thin ones are the warm-hill taxa.
   - ***B. aereus*** has 5 iNaturalist records and 8 census points, on the Colli Euganei, the Berici,
     the Grappa and Baldo foothills; the Padova mycological group found it "nei boschi di castagni e
     querce a Laghizzolo (Monte Venda)" and calls it "presente nei Colli, ma di non facile
     ritrovamento" (`ven_ambpd_fn2008a`). Kept, with its band cut to the hills; the porcini group
     takes the max over its keys, so it cannot lower the group in the mountains.
   - **Ovoli** have 6 iNaturalist records (15-410 m) and 13 census points (the Euganei, the Berici,
     the Vicenza and Grappa foothills, the Valbelluna and Feltrino floor to 770 m, the Treviso plain's
     woods). On the Colli Euganei the species is "divenuta sempre più una rarità"
     (`ven_ambpd_fn2009a`). The regional law bans picking "AMANITA CAESAREA allo stato di ovolo
     chiuso" (`ven_lr23_1996`).
2. **Public records are thin; the census and the neighbours carry the numbers.**
   - Veneto has 12,721 iNaturalist fungi records, with 42 *B. edulis*, 19 *B. reticulatus* and 50
     *Cantharellus*; GBIF adds only copies.
   - The north-east census holds 687 Veneto points of the six taxa, 88 % of them in Belluno
     province, undated for the porcini and ovoli but **dated, with altitudes and habitat notes, for
     the chanterelles**: 293 *C. cibarius* records from 1990-2025, the first dated chanterelle set of
     any region so far.
   - The porcini seasons come from Friuli-Venezia Giulia's analysis of the Carinthian records next
     door, checked against Veneto's own records.
3. **Three regions in one.**
   - **The Dolomites** of Belluno (Cadore, Comelico, the Agordino, Zoldo, Cortina): spruce, fir,
     larch and Scots pine at a median 1,400 m. *B. edulis*, *B. pinophilus* and *C. cibarius*; the
     season ends in early October above 1,000-1,300 m.
   - **The Prealps** (the Asiago plateau, the Grappa, the Cansiglio, the Lessinia, the Baldo, the
     Pasubio and the Treviso Prealps): beech above 800 m, hop-hornbeam and manna ash below, spruce
     planted widely. All the mountain taxa, *B. reticulatus* and the chanterelles.
   - **The hills** (the Colli Euganei, the Berici, the Montello, Asolo, the Valpolicella): downy oak
     with hop-hornbeam, chestnut and robinia at 150-500 m. *B. aereus*, *B. reticulatus*, ovoli and the
     warm chanterelles; fruiting runs through October.
4. **Hop-hornbeam is the choice that matters.** The orno-ostrieti and ostrio-querceti are the
   region's commonest forest (81,000 ha, "circa un quinto dell'area forestale veneta",
   `ven_del_favero2000`), 42 % of the woods below 700 m. On limestone they hold *B. reticulatus* and
   *B. aereus* but "quasi sempre" no *B. edulis* or *B. pinophilus* (`funghimagazine_carpino_nero2026`).
   So the orno-ostrieti (`mixed_broadleaf`) drop to 0.1 for *B. edulis* and *B. pinophilus*, rise to
   0.6 for *B. aereus*, and stay 0.6 for *B. reticulatus* and 0.3 for ovoli and chanterelles.
5. **Weather rules are all Tuscany's.** No Veneto study ties these fungi to rain or temperature in
   numbers. The society notes (a dry autumn then early cold, a dry autumn then a week of rain: both poor;
   a rainy September: an early, rich flush) fit the Tuscan rules. The region's rain
   runs from 670 mm (Rovigo) to over 2,000 mm (Recoaro); the porcini 30-day rain is scored against each
   cell's own normal.
6. **Evidence.** The 21 new references were all opened:
   - 11 institutional (the picking law and its 2023 change, the Region's picking page, the Asiago
     plateau's rules, the forest typology and its map book, the forest report, four ARPAV climate
     sources);
   - 7 society (five issues of the Padova group's bulletin, the Treviso group's herbarium, the Trento
     group's primer);
   - 1 web, 2 own analyses.

   `sanity.yaml` holds 16 press contrasts (14 porcini, 1 gallinacci, 1 ovoli) across the Dolomites,
   the Prealps (Asiago, Lessinia, Grappa, Cansiglio) and the hills, 2016-2024, every quote checked
   against its page.

## At a glance: what differs from Tuscany and why

Trapezoids are `[zero, full, full, zero]`, dates `DD-MM`, altitudes in metres.

| key | factor | Tuscany | Veneto | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | 01-07 → 01-09 … 15-11 → 20-12 | **lowland 15-06 → 01-08 … 31-10 → 30-11 below 900 m; Alpine 01-07 → 25-07 … 25-09 → 25-10 above 1,300 m** (Friuli-Venezia Giulia's numbers) | Veneto records Jul 2.0×, Aug 3.4×, Sep 1.6×, Oct 0.5× the effort, none in November; Carinthian records next door switch shape across 1,000 m; latest Veneto records 14 Oct at 1,864 m and 20 Oct at 1,017 m | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **200 → 600 … 1,900 → 2,200** | records p10 969, median 1,369, p90 1,662, max 1,864 m; census 3 % below 600 m; subalpine spruce and larch-spruce to 1,900-2,100 m | plausible |
| *edulis* | habitat | deciduous oak 0.3, mixed broadleaf 0.3, other conifer 0.3, transitional 0.3 | **0.1, 0.1, 0.1, 0.1** | downy oak and hop-hornbeam on limestone, hop-hornbeam and manna ash (a fifth of the woods), larch, mugo pine and Vaia clearings | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,200 → 1,600** | records 329-1,154 m; census half the peak at 900-1,200 m | plausible |
| *reticulatus* | habitat | transitional 0.6 | **0.1** | here subalpine scrub and Vaia clearings | plausible |
| *aereus* | season | upland/lowland split at 400-600 m | **one window 15-06 → 01-08 … 31-10 → 30-11** | census (83 % FVG) peaks in October (43 %), second peak August; no Apennine uplands | plausible |
| *aereus* | altitude | … 800 → 1,250 | **… 700 → 1,000** | census 95 % below 600 m; Veneto chestnut p90 740 m, a Baldo record at 743 m | plausible |
| *aereus* | habitat | mixed broadleaf 0.3, transitional 0.6 | **0.6, 0.1** | hop-hornbeam woods are hosts; both located records in ostrio-querceto; subalpine scrub | plausible |
| *pinophilus* | season | spring + autumn windows, gap 20-07 → 15-08 | **lowland 01-05 → 01-06 … 31-10 → 30-11; Alpine 01-06 → 01-07 … 25-09 → 25-10; handover 900-1,300 m** | census May-October with no gap, 12 May to 28 October | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **400 → 700 … 1,700 → 2,100** | census mode 900-1,200 m, almost nothing below 600 m; Veneto points in the Dolomites | plausible |
| *pinophilus* | habitat | mountain pine 0.6, other conifer 0.3, mixed broadleaf 0.3, transitional 0.3 | **1.0, 0.1, 0.1, 0.1** | the class is native Scots pine ("frequentemente legato al pino silvestre"); larch; hop-hornbeam on limestone; scrub | plausible |
| ovoli | season | 01-06 → 01-09 … 05-11 → 30-11 | **01-06 → 01-08 … 31-10 → 30-11** | census (55 % FVG) Aug 33 %, Sep 30 %, Oct 24 %; Veneto records Jul-Oct, August 3.8× | plausible |
| ovoli | altitude | … 750 → 1,100 | **… 700 → 1,000** | Veneto records 15-410 m, a collection at 770 m (Valbelluna); NE forager limit 600 m | plausible |
| ovoli | habitat | transitional 0.6 | **0.1** | here subalpine scrub and Vaia clearings | plausible |
| gallinacci | season | lowland 15-04 → 10-05 … 15-12 → 25-01; mountain … 15-10 → 15-11; handover 600-1,000 m | **lowland 15-05 → 15-06 … 31-10 → 10-12; mountain 01-06 → 01-07 … 30-09 → 31-10**; handover kept at 600-1,000 m | 293 dated census records: none in winter; below 800 m 28 May-5 Nov, at 800-1,000 m already mountain-like, at 1,000 m and above 6 % in early October and none after but one | plausible |
| gallinacci | altitude | … 1,000 → 1,700 | **… 1,900 → 2,200** | records to 1,865 m; the census's highest north-east record at 2,040 m (Passo Valles) | plausible |
| gallinacci | habitat | beech 0.6, fir/spruce 0.6, deciduous oak 0.3, mountain pine 0.3, other conifer 0.3, transitional 0.3 | **1.0, 1.0, 0.6, 0.6, 0.1, 0.1** | *C. cibarius* s.str. in spruce, fir and beech (census notes: spruce 126, beech 54 of 293); the Euganean downy-oak woods' chanterelles; Scots pine; larch never alone; scrub | plausible |
| every key | slope stopper | x1 to 25°, x0.8 from 40° | **x1 to 35°, x0.8 from 50°** | the same rule on the region grid: woodland p90 35.3°, max 49.9° | as Tuscany (plausible) |
| every key | weather, growth clock, sun exposure, other stoppers | — | **kept** | no regional numbers; see Weather and Slope and sun exposure | as Tuscany |

Kept on purpose:
- the *B. reticulatus* season (Tuscany's, closing on 15 November), as Friuli-Venezia Giulia kept it;
- beech, chestnut and fir/spruce as hosts of *B. edulis* and *B. pinophilus*;
- mountain pine at 0.6 for *B. edulis* and *B. reticulatus* (not Friuli-Venezia Giulia's 0.3: here the
  class is native Scots pine, not black pine);
- mixed broadleaf (hop-hornbeam) at 0.6 for *B. reticulatus* and 0.3 for ovoli and gallinacci;
- the gallinacci handover at 600-1,000 m (Tuscany's, Trentino-Alto Adige's), not Friuli-Venezia Giulia's
  900-1,300 m: Veneto's dated records at 800-1,000 m already behave like mountain ones;
- the gallinacci and ovoli soil-pH and lithology rules, still disabled.

**What differs from the two Alpine neighbours.**
- **From Friuli-Venezia Giulia:** the same season-window dates for every key, including the single *B. aereus*
  window, but a higher *B. edulis* and gallinacci top (1,900 m full, like Trentino-Alto Adige: the
  Dolomite woods of Belluno climb higher than the Carnian ones), a higher *B. aereus* and ovoli
  plateau (700 m: the Prealps' warm south faces carry chestnut higher than the Karst), mountain pine
  kept at 0.6 for *B. edulis* and raised to 1.0 for *B. pinophilus* (Scots pine, not black pine), the
  hop-hornbeam woods lowered to 0.1 for *B. edulis* (FVG kept 0.3), and the gallinacci handover left at
  600-1,000 m (FVG moved it to 900-1,300 m).
- **From Trentino-Alto Adige:** *B. edulis* and *B. pinophilus* are split by elevation
  (Trentino-Alto Adige found no split in its 455 *B. edulis* records; Veneto's 34 located records are too few to
  test it, and 44 % of its woodland lies below 900 m, where Trentino-Alto Adige has little); the *B.
  reticulatus* season stays open to 15 November (TAA 20 October); the hop-hornbeam woods drop to 0.1
  for *B. edulis* (TAA kept 0.3); ovoli keep 0.0 on mountain pine (TAA 0.3 for its oak-Scots pine
  terraces: Veneto's Scots pine is above the ovolo band).

**Effect on the grid.** Habitat and altitude gates only, on the region grid's 4,025 woodland cells
(`mushma_veneto_forest_check_2026`):

| key | habitat gate full on (Tuscan → regional rules) | altitude gate full on | mean of both gates | both gates at the located records' cells vs the woodland mean (Tuscan → regional) |
|---|---|---|---|---|
| *edulis* | 94 % → 73 % | 58 % → 75 % | 0.89 → 0.87 | 0.90 vs 0.79 → 0.94 vs 0.79 (n=29) |
| *reticulatus* | 93 % → 91 % | 56 % → 64 % | 0.84 → 0.87 | 0.97 vs 0.70 → 0.99 vs 0.76 (n=13) |
| *aereus* | 22 % → 35 % | 38 % → 31 % | 0.53 → 0.46 | 1.00 vs 0.38 → 0.81 vs 0.36 (n=1) |
| *pinophilus* | 94 % → 77 % | 51 % → 63 % | 0.86 → 0.83 | 1.00 vs 0.73 → 1.00 vs 0.73 (n=2) |
| ovoli | 21 % → 19 % | 34 % → 31 % | 0.46 → 0.40 | 1.00 vs 0.33 → 1.00 vs 0.31 (n=2) |
| gallinacci | 93 % → 90 % | 50 % → 99 % | 0.86 → 0.98 | 0.69 vs 0.72 → 1.00 vs 0.96 (n=31) |

The *B. edulis* habitat gate loses full credit on 875 cells, 499 of them hop-hornbeam-dominated and
202 larch-dominated (median elevation 625 m); the Tuscan rules scored the Veneto records no better than the
woods for gallinacci (0.69 against 0.72), the regional ones put them near full credit.

And by area (mean of the two gates, regional rules; areas as in `sanity.yaml`):

| key | Dolomites | Asiago | Lessinia | Cansiglio-Alpago | Colli Euganei and Berici | hills with the Montello | province of Treviso |
|---|---|---|---|---|---|---|---|
| *edulis* | 0.96 | 0.97 | 0.94 | 0.93 | 0.42 | 0.36 | 0.66 |
| *reticulatus* | 0.71 | 0.78 | 0.96 | 0.94 | 0.96 | 0.88 | 0.93 |
| *aereus* | 0.13 | 0.16 | 0.58 | 0.45 | 0.99 | 0.90 | 0.74 |
| *pinophilus* | 0.93 | 0.96 | 0.91 | 0.90 | 0.48 | 0.39 | 0.61 |
| ovoli | 0.11 | 0.10 | 0.48 | 0.34 | 1.00 | 0.92 | 0.70 |
| gallinacci | 0.96 | 0.98 | 1.00 | 1.00 | 0.99 | 0.90 | 0.94 |

That is the census's map: *B. edulis*, *B. pinophilus* and *C. cibarius* in the Dolomites and on the
Prealps' plateaus, *B. aereus* and ovoli on the hills, *B. reticulatus* on both. The hills lose some
credit on the Montello and around Asolo, whose woods are 68 % robinia.

## Veneto in brief

**Woods.** The grid reads the Region's Carta della copertura del suolo 2021, whose forest classes are
the categories and types of the regional typology (`ven_del_favero2000`; mapping and codes in
`regions/veneto.md`).
- **Area:** 398,369 ha of forest on the grid, 4.4 % under INFC 2015's 416,704 ha of *bosco*; 10,227
  ha more are flagged as flattened by the Vaia storm of 29 October 2018, killed by bark beetle or
  burnt, and go to `transitional`.
- **By altitude:** 28 % of the forest lies below 600 m, 22 % at 600-1,000 m, 30 % at 1,000-1,500 m
  and 20 % above 1,500 m (`ven_raf2020`). The grid's 4,025 woodland cells run from 3 m to 2,154 m,
  median 994 m (p10 357 m, p90 1,619 m); 44 % lie below 900 m.
- **Forest regions** (`ven_del_favero2000`):
  - the **avanalpica** (the first Prealpine slopes and the hills, the Colli Euganei and Berici
    included) is "l'area di maggior diffusione dei castagneti, degli ostrio-querceti e degli
    orno-ostrieti"; on the Colli Euganei the ostrio-querceti sit on limestone and chestnut on the
    magmatic rocks;
  - the **esalpica** (the outer Prealps, carbonate): "sono abbondanti i consorzi, puri o misti, di
    carpino nero, che occupano circa un quinto dell'area forestale veneta", and "al di sopra degli 800
    m, agli orno-ostrieti si sostituiscono le faggete"; native black pine reaches its western limit
    along the Piave;
  - the **esomesalpica**, from 800-900 m on "il Monte Grappa, l'Altipiano dei Sette Comuni e il
    Cansiglio" and in the lower Agordino and the Feltrino: more spruce, spruce-beech and fir;
  - the **mesalpica**: fir and spruce-beech, and "le pinete di pino silvestre, che colonizzano ampi
    ambiti lungo l'alto corso del Piave e dei suoi affluenti";
  - the **endalpica** (the inner Dolomites): rain "attorno a 1000 mm annui" with a July maximum,
    stone pine above 1,500 m, larch and spruce.
- **Spruce plantations.** Spruce was planted on beech and hop-hornbeam sites between the wars and
  "si è poi spesso spontaneamente diffuso" (`ven_del_favero2006`); the 2006 map's conifer
  plantations are three quarters spruce and the region config types them `fir_spruce`.

**Which habitat holds which tree.** From the region config (`regions/veneto.yaml`, the Region's
Carta della copertura del suolo 2021, whose forest classes are the regional categories and types of
Del Favero et al. 2000) and the woodland grid (`mushma_veneto_forest_check_2026`; shares of the
wooded area of the 4,025 woodland cells, elevations of the cells weighted by each habitat's share).
The forest types inside each class and their elevations come from the older Carta regionale delle
categorie forestali (2006, same typology), sampled on a 100 m lattice:

| habitat key | Veneto types (2006 map, ha) | share | elevation p10 / median / p90 |
|---|---|---|---|
| `fir_spruce` | peccete (49,000: secondary montane spruce on beech sites 19,700, carbonate and silicate altimontane 23,600, subalpine 4,700), abieteti (23,000), conifer plantations (29,000 in all, three quarters spruce "su faggeta" or "su orno-ostrieto", the rest black pine 2,900, larch 3,000, stone and maritime pine on the coast 900) | 24.1 % | 840 / 1,304 / 1,675 m |
| `beech` | faggete (75,000): montane esalpica (28,800, median 1,163 m), submontane with hop-hornbeam (25,600, 860 m), altimontane, primitive, mesalpica | 21.2 % | 683 / 1,048 / 1,377 m |
| `mixed_broadleaf` | orno-ostrieti (55,400, median 593 m), aceri-frassineti and aceri-tiglieti (9,100), carpineti (4,100), birch (200) | 20.5 % | 335 / 621 / 939 m |
| `other_conifer` | lariceti (28,600, median 1,664 m) and larici-cembreti (5,500, 1,840-1,955 m) | 8.3 % | 1,260 / 1,672 / 1,922 m |
| `deciduous_oak` | ostrio-querceti (25,800: tipico 16,300, a scotano 9,500, median about 300 m), querco-carpineti (1,300), rovereti (600), the Euganean oak wood with Mediterranean elements (750) | 5.8 % | 159 / 328 / 627 m |
| `transitional_woodland_shrub` (not woodland) | mughete (27,900), green alder (2,500), shrubland (4,400), and forest flagged as flattened by Vaia or killed by bark beetle in 2021 (10,200 ha) | 5.2 % | 736 / 1,364 / 1,776 m |
| `chestnut` | castagneti (19,700): on magmatic substrates (8,000, median 371 m: the Colli Euganei trachyte, the Lessini and Agno basalts), xeric (5,400), mesic (4,500), with ash (1,700) | 4.8 % | 244 / 493 / 740 m |
| `mountain_pine` | Scots pine woods (12,700, 98 % in Belluno province: Auronzo, Ospitale, Cortina, Perarolo, Longarone, Val di Zoldo, Sedico), incl. the esalpica type with black pine (1,450) | 3.4 % | 644 / 1,082 / 1,448 m |
| `exotic_broadleaf` | robinieti (18,200: the Montello, the hills and the plain's edge) | 2.9 % | 151 / 295 / 571 m |
| `mixed_broadleaf_conifer` | piceo-faggeti (10,700), all in Belluno province | 2.7 % | 938 / 1,262 / 1,528 m |
| `riparian` | saliceti e formazioni riparie (9,100), black and grey alder (400), coastal wet woods (150) | 0.9 % | 104 / 299 / 1,005 m |
| `evergreen_oak` | lecceta (160 ha, Bosco Nordio and the coast) | 0.0 % | about 5 m |
| `macchia` | Euganean pseudomacchia (40), coastal scrub (190) | 0.0 % | |
| `mediterranean_pine` | none: the coastal stone and maritime pine plantations are typed with the conifer plantations (`fir_spruce`) | absent | |

Notes:
- **By province** (share of each province's woodland): Belluno is spruce and fir 32 %, beech 17 %,
  hop-hornbeam 17 %, larch 14 %, Scots pine 6 %, spruce-beech 5 %; Vicenza beech 33 %, spruce and fir
  21 %, hop-hornbeam 15 %, downy oak 12 %, chestnut 9 %; Verona hop-hornbeam 47 %, beech 20 %, downy
  oak 16 %; Treviso hop-hornbeam 32 %, beech 16 %, robinia 16 %, chestnut 13 %; Padova (43 woodland
  cells, the Colli Euganei) chestnut 39 %, robinia 35 %, downy oak 25 %.
- **Below 700 m** the woods are 42 % hop-hornbeam, 18 % downy oak, 13 % chestnut, 9 % robinia and 8
  % beech: the low porcini, the ovolo and the hills' chanterelles live or die by the hop-hornbeam
  and oak affinities.
- **Hop-hornbeam is the region's commonest broadleaf forest** (the card's "orno-ostrieti e
  ostrio-querceti", 81,000 ha). The grid splits it: the orno-ostrieti (hop-hornbeam and manna ash,
  median 593 m, mostly on the carbonate Prealps and the Belluno valleys) go to `mixed_broadleaf`, the
  ostrio-querceti (downy oak with hop-hornbeam on the warmest slopes, median about 300 m, Vicenza and
  Verona) to `deciduous_oak`.
- **Vaia.** The storm of 29 October 2018 and the bark beetle after it killed spruce on the Asiago
  plateau, in the Agordino and in Comelico; the 2021 map flags 10,227 ha, which the grid sends to
  `transitional`. Those cells lose porcini and chanterelle credit through the transitional
  affinities (0.1), which is what the dead hosts mean for mycorrhizal fruiting.
- **No chestnut in the Dolomites** and little on the Asiago plateau: the chestnut belt is the
  Vicenza Prealps' valleys (Valli del Pasubio, Valdagno, Recoaro Terme, Schio, Torrebelvicino), the
  eastern Lessinia basalts (Vestenanova, Roncà), the Colli Euganei, the Treviso hills (Miane, the
  Montello) and the Feltrino's south (Setteville).

**Climate.**
- **Rain** (`ven_arpav_atlante_prec2013`, 1950-2010): "dai circa 670 mm ... (Provincia di Rovigo)
  fino ad oltre 2030 mm nella zona di Recoaro"; the plain averages 884 mm, the mountains above 400 m
  1,466 mm. The outer Prealps are the wettest (Recoaro 1,950-2,000 mm, Tambre in the Cansiglio 1,535
  mm, Asiago 1,455 mm); the inner Dolomites the driest of the mountains ("si passa dai 1380 mm di
  Agordo ai 1020 mm di Caprile", Cortina about 1,015 mm, Cadore and Comelico 1,110-1,120 mm)
  (`ven_arpav_clima_cm`).
- **Regime:** "un massimo di apporti pluviometrici nei mesi di novembre e ottobre", a second maximum
  in April-June, a secondary minimum in July-September; in Cadore and Cortina "il massimo principale
  nel mese di giugno (anziché in autunno)".
- **Temperature:** lapse rates of 0.43-0.58 °C per 100 m by mountain community (Sette Comuni 0.57,
  Valle del Boite 0.46); Asiago (1,005 m) has means of 3.4 °C minimum and 12.6 °C maximum
  (`ven_arpav_clima_cm`). The region lane found the national lapse rates fit best
  (`regions/veneto.md`).
- **Drought years:** 2022, "l'anno meno piovoso a partire dal 1993", 31 % under the mean
  (`ven_arpav_2022`); 2017, 17 % under, 40 % in the centre-west (`ven_arpav_2017`); 2003, the
  plain's driest year of 1950-2010 (614 mm, `ven_arpav_atlante_prec2013`).

**Picking rules** (`ven_lr23_1996`, `ven_lr15_2023`, `ven_rv_raccolta_funghi`,
`ven_reggenza_funghi`). None of them changes where or when the fungi fruit, so none is encoded.
- **L.R. 23/1996** as amended to 2023: 3 kg a person a day, "di cui non più di Kg. 1" of the listed
  species, porcini, ovoli and *C. cibarius* among them; "E' vietata la raccolta dell'AMANITA CAESAREA
  allo stato di ovolo chiuso"; **no minimum cap size**; no searching at night.
- **Permits and days are local.** Unioni montane, provinces, Veneto Agricoltura (the regional
  forests: the Cansiglio, the Baldo), park managers and the Regole issue them and set the days; the
  default is Tuesday, Friday, Sunday and holidays. The Asiago plateau opens to non-residents on
  Tuesday, Friday and Sunday (EUR 12 a day).
- **Closed:** the Parco naturale delle Dolomiti d'Ampezzo, the Parco nazionale Dolomiti Bellunesi
  (residents excepted), the Sile park; the **Montello** is closed to non-residents (2025 days table).
- **Effect on the evidence:** picking on three days a week bunches reports and records on those days,
  and the Montello's closure thins its press and records.

## Sightings (occurrence cross-check)

Queried 2026-09-29 (`mushma_veneto_occurrence_check_2026`). Aggregates only; no coordinates are
stored.
- **iNaturalist:** place 13074 (Veneto, the id the region config uses), verifiable records, all
  years.
- **GBIF:** `gadmGid=ITA.20_1`. Every record of the six taxa is an iNaturalist copy but 2
  *Cantharellus*: GBIF adds nothing.
- **Elevations:** Copernicus GLO-30 tiles under the data root (the Open-Meteo quota is shared, so it
  was not used), for records that are not obscured and have an accuracy of 1 km or better.
- **Enrichment:** the taxon's monthly share ÷ the monthly share of all 12,721 Veneto iNaturalist
  fungi records, whose effort peaks in October (20.1 %), then September (17.8 %) and August (13.3 %).
- **Surroundings:** the forest types of the Region's Carta regionale delle categorie forestali (2006,
  the same typology as the grid's map) within 500 m of each located record, against the woods at the
  same elevations (p10-p90 of the records).
- **Census:** the north-east census map points (`muse_censimento_*`) recounted inside the ISTAT 2025
  Veneto boundary, by province and comune.

**Veneto has few public records.** 12,721 iNaturalist fungi records (Lombardia 36,719,
Trentino-Alto Adige 30,261, Friuli-Venezia Giulia 3,172), and 124 of the six taxa.

| taxon | iNaturalist (observers) | Jun | Jul | Aug | Sep | Oct | Nov | located: min / p10 / median / p90 / max (m) |
|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 42 (32) | | 7 | 19 | 12 | 4 | | 272 / 969 / 1,369 / 1,662 / 1,864 (n=34) |
| | enrichment | | 2.0 | 3.4 | 1.6 | 0.5 | | |
| *B. reticulatus* | 19 (13) | 2 | 8 | 1 | 7 | 1 | | 329 / 569 / 867 / 1,090 / 1,154 (n=13) |
| | enrichment | 1.9 | 5.2 | 0.4 | 2.1 | 0.3 | | |
| *B. aereus* | 5 (3) | | | 1 | 3 | | | 59 and 743 (n=2); 1 more record in May |
| *B. pinophilus* | 2 (2) | | | 1 | 1 | | | 1,121 and 1,159 (n=2) |
| *A. caesarea* | 6 (5) | | 1 | 3 | 1 | 1 | | 15 / - / 215 / - / 410 (n=4) |
| *Cantharellus* | 50 (30) | 3 | 12 | 15 | 13 | 3 | 2 | 34 / 364 / 1,028 / 1,577 / 1,865 (n=39) |
| | enrichment | 1.1 | 2.9 | 2.3 | 1.5 | 0.3 | 0.4 | |

*Cantharellus* also has 1 record in April and 1 in December (8 December 2025 at 1,626 m in Comelico,
probably old fruit bodies). 29 of the 42 *B. edulis* records are from 2020 on, 16 from 2025-2026.

**Half-months by elevation** (located records):

| taxon | band (n) | Jul 1-15 | Jul 16-31 | Aug 1-15 | Aug 16-31 | Sep 1-15 | Sep 16-30 | Oct 1-15 | Oct 16-31 | Nov |
|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | < 1,000 m (5) | 1 | | 2 | 1 | | 1 | | | |
| | 1,000-1,300 m (11) | | 3 | 2 | 1 | 4 | | | 1 | |
| | ≥ 1,300 m (18) | | 2 | 6 | 4 | 4 | 1 | 1 | | |
| *Cantharellus* | < 1,000 m (13) | | 1 | 3 | 1 | | 1 | 2 | | 2 |
| | 1,000-1,300 m (17) | 2 | 3 | 3 | 3 | 6 | | | | |
| | ≥ 1,300 m (9) | | 1 | 1 | 2 | 2 | 2 | | | |

(*Cantharellus* below 1,000 m: 1 record in late April and 2 in late June; above 1,300 m, the
December record.)

**Species inside *Cantharellus*** (iNaturalist): *C. cibarius* 25 (located median 1,159 m), *C.
amethysteus* 7, *C. pallens* 6 (at 364-702 m in hop-hornbeam and downy-oak woods), *C. friesii* 2, *C.
ferruginascens* 1 (30 November 2024, 374 m, above Lake Garda), genus only 9. As in the Alpine
neighbours, the chanterelle of the mountains is *C. cibarius* s.str.; the hills add the warm
segregates.

**Where the located records sit** (share of the forest map within 500 m, against the woods at the
same elevations):

| taxon (n, band) | spruce and fir | beech | mixed broadleaf | chestnut | deciduous oak | larch | Scots pine |
|---|---|---|---|---|---|---|---|
| *B. edulis* (33, 1,019-1,695 m) | 64 % / 47 % | 13 / 28 | 5 / 2 | 0 / 0 | 0 / 0 | 11 / 11 | 2 / 5 |
| *B. reticulatus* (13, 556-1,048 m) | 15 / 14 | 35 / 30 | 27 / 34 | 17 / 6 | 4 / 3 | 0 / 3 | 0 / 7 |
| *Cantharellus* (38, 389-1,601 m) | 45 / 28 | 25 / 27 | 8 / 21 | 4 / 4 | 9 / 3 | 6 / 6 | - |
| *A. caesarea* (4, 65-431 m) | 0 / 0 | 0 / 1 | 14 / 24 | 39 / 14 | 23 / 30 | 0 / 0 | 0 / 1 |

*A. caesarea* records also have robinia around them (24 % against 22 % of the woods). *B. aereus*
(2 records): ostrio-querceto, chestnut and robinia around both. *B. pinophilus* (2):
spruce and beech.

**The north-east census** (`muse_censimento_edulis`, `fvg_muse_censimento_aestivalis`,
`muse_censimento_boletus`, `muse_censimento_pinophilus`, `muse_censimento_caesarea`,
`muse_censimento_cibarius`, `muse_censimento_cantharellus`, `fvg_muse_censimento_ferruginascens`).
Veneto is the census's thinnest region: its federation contributes far fewer points than Trento's
or Friuli's, almost all from Belluno province. Map points inside Veneto (my recount on the ISTAT 2025
boundary):

| taxon | Veneto points (BL / VI / VR / TV / PD) | north-east total | where in Veneto |
|---|---|---|---|
| *B. edulis* | 206 (178 / 27 / 1 / 0 / 0) | 1,354 | Agordo 19, Falcade 17, Auronzo 15, Val di Zoldo 12, Borca 11, Rotzo 8, Santo Stefano, Ospitale and San Vito di Cadore 8, Gallio 6, Tambre 6 |
| *B. aestivalis* | 152 (129 / 15 / 1 / 3 / 4) | 861 | Ponte nelle Alpi 25, Belluno 22, Sedico 19, Borgo Valbelluna 12, Agordo 10, Posina 8 |
| *B. aereus* | 8 (0 / 2 / 1 / 2 / 3) | 308 | Torreglia 2, Cavaso del Tomba 2, Monte di Malo, Arcugnano, Caprino Veronese, Piombino Dese |
| *B. pinophilus* | 18 (14 / 4 / 0 / 0 / 0) | 246 | Comelico Superiore 4, Arsiero 4, Auronzo 2, Pieve di Cadore 2 |
| *A. caesarea* | 13 (5 / 3 / 0 / 2 / 3) | 268 | Torreglia 3, Monte di Malo 2, Borgo Valbelluna 2, Setteville, Sedico, Fonzaso, Val Liona, Cavaso del Tomba, Vedelago |
| *C. cibarius* | 290 (278 / 11 / 0 / 1 / 0) | 1,923 | Belluno 46, Val di Zoldo 17, Comelico Superiore 17, Falcade 16, Sospirolo 14, Gosaldo 13 |
| *C. amethysteus* | 44 (31 / 8 / 0 / 5 / 0) | 185 | Tambre 9, Alpago 7, Fregona 4 (the Cansiglio), Asiago 3 |
| *C. pallens* | 39 (21 / 15 / 1 / 2 / 0) | 411 | Posina 12, Val di Zoldo 5, Borgo Valbelluna 3 |
| *C. ferruginascens* | 11 (2 / 6 / 0 / 0 / 3) | 58 | Posina 4, Isola Vicentina 2, Cinto Euganeo, Vo', Rovolon |

- **Veneto lines on the census pages:** the highest *C. cibarius* of the whole north-east is
  Veneto's, "22 lug. 2001 - Passo Valles (Falcade, BL) Conifere e microselva alpina. 2040 m"; a
  collection "15 lug. 1993 | Canal di Limana (Borgo Valbelluna, BL) | _PICEA, FAGUS, CORYLUS, LARIX"
  at 950 m; an ovolo "25 set. 1994 | Col di Pera (Borgo Valbelluna, BL) | Sotto latifoglie. 770 m";
  the earliest *C. ferruginascens* on 18 May 2024 at Posina (618 m) in "Boschi misti di Ostrya
  carpinifolia, Fraxinus ornus, Acer e Carpinus ... presenza Castagno"; the lowest ovolo, 14 m, "(PD)"
  on 14 September 2020.
- **Dated chanterelles:** on the *Cantharellus* pages the map records are public, each with date,
  locality, altitude and habitat (for the porcini and the ovolo they read "Riservato"): 293 Veneto *C.
  cibarius* records and 123 of the segregates, used in the Gallinacci section.
- **Charts:** the month and altitude charts are north-east-wide and were read for Friuli-Venezia
  Giulia (tables in `friuli_venezia_giulia.md`); Veneto's share of them is small, so they are used as
  the north-east's shape, not Veneto's.

**Caveats.**
- **Presence only, near roads and huts**, and summer hikers raise the July-August effort.
- **Thin.** 42 *B. edulis* and 50 *Cantharellus* records cannot validate anything; the other four
  taxa have 2-19. The census shows where, mostly in Belluno, and has almost nothing from the Lessinia,
  the Baldo, the Grappa or the Treviso Prealps: absence there is absence of recorders.
- **Priors, not fits.** The season, band and habitat choices are drawn partly from these same records,
  so they stay frozen priors.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Which porcino where** (society, the census map and the records):
  - *B. edulis*: the Dolomites (the Agordino, Cadore, Comelico, Zoldo) and the Asiago plateau (Rotzo,
    Gallio, Asiago, Roana), with the located records at a median 1,369 m, spruce and fir 64 % of their
    surroundings; the Cansiglio beech from July to October (`fvg_campo2022_cansiglio`); on the Colli
    Euganei it is listed among the chestnut woods' fungi (`ven_ambpd_fn2007b`). The Asiago plateau's
    notes: "È frequente sotto conifere e faggi. Di solito si trova dal mese di luglio in poi"
    (`ven_reggenza_funghi`, folklore).
  - *B. reticulatus*: everywhere below about 1,200 m, above all in the Valbelluna (Ponte nelle Alpi,
    Belluno, Sedico: 66 census points), the Vicenza Prealps (Posina, Recoaro, Valli del Pasubio) and
    the Colli Euganei, where the Padova group lists it among the commonest fungi of the chestnut and
    the downy-oak woods (`ven_ambpd_fn2007b`, `ven_ambpd_fn2008a`) and found one on Monte Venda on 27
    April 2008 (`ven_ambpd_fn2008b`).
  - *B. aereus*: the Colli Euganei ("presente nei Colli, ma di non facile ritrovamento", found "A fine
    ottobre ... nei boschi di castagni e querce a Laghizzolo (Monte Venda)", `ven_ambpd_fn2008a`), the
    Berici, the Grappa and Baldo foothills; "rarissima invece nelle aree settentrionali,
    prevalentemente a quote collinari" (`ven_ambpd_fn2008a`), "praticamente assente nell'areale
    alpino" (`ven_gmb_primipassi`).
  - *B. pinophilus*: Comelico and Cadore, the Agordino, Arsiero; the Treviso Prealps (Madean,
    `ven_saccardo_erbario`); with spruce and beech as often as pine ("non solo con il pino ... ma spesso
    anche ad altre essenze (abete rosso, faggio, ecc.)", `ven_gmb_primipassi`).
- **Hop-hornbeam** (the region's commonest broadleaf forest):
  - in its woods "sono spesso presenti il Boletus reticulatus (estatino) e il Boletus aereus (porcino
    nero)", while "i Porcini più legati a suoli acidi" (*B. edulis*, *B. pinophilus*) are "quasi sempre
    assenti, o comunque molto rari nei contesti calcarei" (`funghimagazine_carpino_nero2026`,
    folklore);
  - the Colli Euganei's downy-oak, manna-ash and hop-hornbeam woods on limestone list *B. aereus* and
    *B. aestivalis* among their commonest fungi, not *B. edulis* (`ven_ambpd_fn2008a`);
  - 7 of the 13 located *B. reticulatus* records and both *B. aereus* ones have hop-hornbeam woods
    among the first two forest types within 500 m; the *B. edulis* records sit above the hop-hornbeam
    belt (mixed broadleaf 5 % of their surroundings);
  - next door in Trentino, *B. edulis* records below 1,000 m had hop-hornbeam in 4 % of their
    surroundings against 27 % of the woods (`mushma_taa_forest_check_2026`).
- **Larch and Scots pine.** Larch is no porcino partner (`taa_mandolini2025_larix`); the Veneto *B.
  edulis* records' surroundings hold it in the same share as the woods (11 %), because Dolomite larch
  stands mix with spruce. The Scots pine of the upper Piave basin is native (`ven_del_favero2000`),
  unlike Friuli-Venezia Giulia's black pine.

**Decisions** (numbers in the table above; the full reasoning is in each factor's `notes`):

- ***B. edulis* season: two windows blended at 900-1,300 m,** with Friuli-Venezia Giulia's numbers.
  - **Why split:** the Tuscan window would keep the Dolomite spruce in season into December, held
    only by frost and snow. Veneto's records are over-represented from July to September and
    under-represented in October (0.5×, 4 records; none in November), and next door the Carinthian
    records switch shape across 1,000 m.
  - **Alpine window:** full 25 July-25 September, closed by 25 October; the latest Veneto records at
    altitude are 14 October at 1,864 m (San Vito di Cadore) and a few in early October.
  - **Lowland window:** full 1 August-31 October, closed by 30 November, from mid-June: the Prealpine
    beech and chestnut below 900 m (44 % of the woodland cells) fruit later.
- ***B. edulis* altitude: full 600-1,900 m, zero at 200 m and 2,200 m.** The records reach 1,864 m and
  the woods 2,154 m; "dalla pianura fino a oltre 2000 m di quota" (`ven_gmb_primipassi`).
- ***B. edulis* hosts:**
  - **mixed broadleaf 0.3 → 0.1:** four fifths orno-ostrieti on limestone, half of them inside the
    band's plateau (median 621 m). At 0.3 a pure hop-hornbeam cell would get full credit; at 0.1 it
    gets a third, and a fifth of beech, chestnut or spruce in the cell restores full credit. This is
    the main difference from Friuli-Venezia Giulia and Trentino-Alto Adige, which kept 0.3 on smaller
    hop-hornbeam shares (14 % and 8 % of their woods, against 20 % here);
  - **deciduous oak 0.3 → 0.1:** nine tenths ostrio-querceti, median 328 m, as in Friuli-Venezia
    Giulia;
  - **larch (`other_conifer`) and subalpine scrub (`transitional`) 0.3 → 0.1**, as in the three Alpine
    neighbours; here `transitional` also holds the forest flattened by Vaia;
  - **mountain pine kept at 0.6** (Scots pine; Friuli-Venezia Giulia's 0.3 was for black pine).
- ***B. reticulatus*:**
  - the Tuscan season is kept (full to 30 September, closed by 15 November): the Veneto records run
    June to early October, and the lower woods stay mild into October;
  - the band reaches 1,200 m full, zero at 1,600 m, as in Friuli-Venezia Giulia (records 329-1,154 m;
    census half the peak at 900-1,200 m);
  - subalpine scrub drops to 0.1; hop-hornbeam stays secondary (0.6) and Scots pine secondary (0.6).
- ***B. aereus*:**
  - one window, full 1 August-31 October, closed by 30 November, from mid-June (the census's October
    peak and August flush; "in June ... tra la bassa Lessinia e Colli Berici / Euganei",
    `ven_fm_funghi_giugno`);
  - the band is cut to the hills: full to 700 m, zero at 1,000 m;
  - hop-hornbeam woods (`mixed_broadleaf`) rise to secondary (0.6), subalpine scrub drops to 0.1.
- ***B. pinophilus*:**
  - no summer gap, and an Alpine window above 900-1,300 m like *B. edulis*: the census profile runs
    May to October, "già all'inizio dell'estate" (`ven_gmb_primipassi`);
  - band 700-1,700 m full, zero at 400 m and 2,100 m;
  - Scots pine becomes a full host (1.0), as in Trentino-Alto Adige and Lombardia; larch, hop-hornbeam
    woods and subalpine scrub drop to 0.1.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Census:** 13 Veneto points (`muse_censimento_caesarea`): Torreglia (3, Colli Euganei), Monte di
  Malo (2), Val Liona (Colli Berici), Cavaso del Tomba (Grappa foothills), Borgo Valbelluna (2),
  Sedico, Fonzaso, Setteville (the Belluno valley floor) and Vedelago (Treviso plain); a 1994
  collection "Sotto latifoglie" at 770 m at Col di Pera (Borgo Valbelluna), the only Veneto altitude on the page;
  its lowest record of all, 14 m in Padova province (2020).
- **Records:** 6 iNaturalist (July 1, August 3, September 1, October 1); the 4 located at 15-410 m
  (Galzignano Terme, Orgiano, Santorso, Setteville), with chestnut, downy oak, hop-hornbeam and robinia
  around them.
- **Society:**
  - the Padova group lists it among the commonest fungi of the Colli Euganei's chestnut woods, their
    downy-oak and hop-hornbeam woods on limestone, and their warm oak woods with holm oak
    (`ven_ambpd_fn2007b`, `ven_ambpd_fn2008a`, `ven_ambpd_fn2009a`), and on the 136 m Monte Calbarina
    (`ven_ambpd_fn2008b`);
  - "La ricercatissima A. caesarea predilige boschi di latifoglie, a quote piuttosto basse, e periodi
    caldi. E' possibile il ritrovamento di quest'ultima specie nei nostri Colli Euganei, pur essendo
    divenuta sempre più una rarità" (`ven_ambpd_fn2009a`);
  - the Treviso group's herbarium has it from the Montello and the Sile park's lowland woods
    (`ven_saccardo_erbario`);
  - the Asiago plateau's notes: "cresce soprattutto nei boschi di castagni e querce ad una altitudine
    che solitamente non supera i 1000 m" (`ven_reggenza_funghi`, folklore).
- **Press:** "sono partite ottime buttate di funghi Porcini aereus e subito dopo di Ovoli reali" on the
  Veneto hills in mid-September 2020, and "pure Ovoli reali" in the plain's woods in early August
  2023 (Funghi Magazine; see Press contrasts).

**Decisions.**
- **Season:** full 1 August-31 October (Tuscany 1 September-5 November), from 1 June, closed by 30
  November, as in Friuli-Venezia Giulia: the census profile is August 33 %, September 30 %, October
  24 %; Veneto's records peak in August.
- **Altitude:** full to 700 m, zero at 1,000 m (Tuscany 750 → 1,100 m, Friuli-Venezia Giulia 650 →
  1,000 m): the 770 m collection sits on the ramp, the located records well inside.
- **Hosts:**
  - oak and chestnut stay hosts;
  - subalpine scrub drops to 0.1 (here mugo pine and Vaia clearings, four fifths above 1,000 m);
  - hop-hornbeam woods stay marginal (0.3): a pure orno-ostrieto cell still gets full credit; the
    Orgiano (Colli Berici) and Setteville records come from hop-hornbeam with downy oak, and the Padova
    group lists the ovolo in the Euganean hop-hornbeam and oak woods;
  - robinia stays at 0.05, although it surrounds the Colli Euganei record: it replaced the chestnut
    and oak that host the ovolo;
  - beech and Scots pine stay non-host, both above the band here.

## Gallinacci (*Cantharellus* s.l.: "finferli", "gialletti", "gallinacci")

**Regional evidence.**
- **The dated census records** (`mushma_veneto_occurrence_check_2026`, from the public census pages of
  `muse_censimento_cibarius` and `muse_censimento_cantharellus`). *C. cibarius*: 293 Veneto records
  (Belluno 282, Vicenza 11; 116 before 2000, 96 since 2016), with date, altitude and habitat:

| band (n) | May | Jun | Jul | Aug | Sep | Oct | Nov | latest |
|---|---|---|---|---|---|---|---|---|
| < 800 m (69) | 1 | 16 | 29 | 15 | 3 | 3 | 2 | 5 Nov 2001, 500 m, Belluno, "sotto faggio" |
| 800-1,000 m (32) | | 1 | 17 | 9 | 4 | 1 | | early October |
| 1,000-1,300 m (73) | | 4 | 21 | 31 | 12 | 5 | | first half of October |
| 1,300-1,600 m (65) | | | 15 | 30 | 16 | 3 | 1 | 1 Nov 1991, 1,380 m |
| ≥ 1,600 m (38) | | | 6 | 27 | 3 | 2 | | first half of October |

  Altitudes 400-2,040 m (median 1,144 m, p90 1,700 m); the habitat notes name spruce 126 times, beech
  54, larch 29 (never alone), pine 9, chestnut and oak 2 each, hop-hornbeam never. The median month is
  July below 800 m and August above.
- **The segregates** (census, Veneto): *C. pallens* 39 records at 399-1,681 m, May to July above all,
  12 of them at Posina, several under hop-hornbeam, hornbeam, ash and maple ("Boschi misti di Ostrya
  carpinifolia, Fraxinus ornus, Acer e Carpinus") and chestnut; *C. amethysteus* 43 at a median 1,089 m,
  August to October, mostly in the Cansiglio and Alpago beech; *C. ferruginascens* 11 at 65-865 m,
  peaking in October, on the Colli Euganei under chestnut, hop-hornbeam, downy oak and holm oak; *C.
  friesii* 30. No *C. alborufescens* record, though the Padova group lists "Cantharellus cibarius e
  var. alborufescens" in the Colli Euganei woods (`ven_ambpd_fn2007b`, `ven_ambpd_fn2008a`,
  `ven_ambpd_fn2009a`).
- **iNaturalist:** 50 records, *C. cibarius* 25 (median 1,159 m), the warm segregates in hop-hornbeam
  and downy-oak woods at 300-700 m; the latest at altitude 19 September, the latest low down 30
  November (*C. ferruginascens* above Lake Garda).
- **The Cansiglio beech:** *C. cibarius* June-September, *C. amethysteus* September-October
  (`fvg_campo2022_cansiglio`).
- **Press:** in mid-August 2019 in northern Veneto "le nascite di funghi Galletti risultano abbondanti,
  ma non quelle di funghi Porcini" (Funghi Magazine); "gialletti" among the species most present in
  the Belluno woods in late August 2019 (Corriere delle Alpi).

**Decisions.**
- **Season:**
  - the lowland window is full 15 June-31 October and closed by 10 December (Friuli-Venezia Giulia's),
    with no winter mode: the latest low records are early November (census) and late November (the
    warm segregates);
  - the mountain window is full 1 July-30 September and closed by 31 October: above 1,000 m 6 % of
    the dated records fall in the first half of October and none later but one;
  - the handover stays at 600-1,000 m (Tuscany's and Trentino-Alto Adige's): the records at 800-1,000 m
    already end like the mountain ones;
  - the disabled two-flush rule closes with the lowland window.
- **Altitude:** full to 1,900 m, zero at 2,200 m, so open on all but 1.3 % of the woodland cells: the
  census's highest north-east record, 2,040 m, is at Passo Valles (Falcade).
- **Hosts:**
  - beech and fir/spruce rise to host (1.0);
  - deciduous oak and Scots pine rise to secondary (0.6);
  - larch and subalpine scrub drop to 0.1;
  - hop-hornbeam stays marginal (0.3): thin for *C. cibarius* (8 % of the records' surroundings
    against 21 % of the woods, no Ostrya in the census notes), but home to *C. pallens* and *C.
    ferruginascens*, which the group includes.
- **Soil pH and lithology stay disabled.** The Veneto woodland's SoilGrids pH is a median 5.97, lowest
  under larch, spruce and spruce-beech; a pH rule would mostly repeat the spruce preference.

## Keys and groups dropped

None. Every key has Veneto records and a regional source.
- ***B. aereus*** is rare (5 iNaturalist records, 8 census points) and a hill porcino. Its band and
  host tiers keep it to the hills; the porcini group takes the max over its keys, so it cannot lower
  the group in the mountains.
- **Ovoli** are rare and declining but present on the Colli Euganei and Berici, the Prealps' foot and
  the Belluno valley floor.
- **Absent habitat keys.** `mediterranean_pine` is empty (the coastal stone and maritime pine
  plantations are typed with the conifer plantations under `fir_spruce`), `evergreen_oak` and `macchia`
  are a few hundred hectares on the coast and the Colli Euganei. Their affinities are left as
  Tuscany's rather than invented.

## Weather rules: why none changed

- **No regional numbers.** No Veneto study gives a rain amount, lag or temperature threshold for
  these taxa; no ULSS mycological inspectorate publishes season notes with ecological content, and
  the one University of Padova mycorrhiza paper found is about root tips in Emilia-Romagna, not
  fruiting in Veneto.
- **Society notes, all compatible with the Tuscan rules** (folklore; not encoded):
  - autumn 2007 on the Colli Euganei: a drought then early cold near 0 °C by mid-October, "Risultato:
    scarsità di crescita fungina nei Colli Euganei" (`ven_ambpd_fn2008a`): the drought and cold rules;
  - November 2008: after a dry autumn, a week of heavy rain brought only small species and "la quasi
    totale assenza di boleti, russule, amanite e lattari" (`ven_ambpd_fn2009a`): the 30-day and
    60-day rain rules against a single trigger;
  - September 2017 on the hills: a rainy month brought an early flush, "particolarmente proficue"
    from mid-September into early October (`ven_ambpd_fn2018`).
- **Rain climate:** from 670 mm on the Po delta to over 2,000 mm at Recoaro, and a June maximum in the
  inner Dolomites (`ven_arpav_atlante_prec2013`):
  - the porcini 30-day rain is a percentage of each cell's own normal, so it adapts;
  - the absolute 30-day ramps of ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full almost
    always on the outer Prealps and less often on the Colli Euganei and Berici in July and August,
    where ovoli and the warm chanterelles fruit later anyway.
- **Föhn and dry wind.** The press blames cold rain and wind in September 2021 and 2024 and the dry
  plain winds on the Garda woods in August 2021. The ET0-based drying rules are the only stand-in; the
  known gap `drying_wind` would suit the Prealps and the Dolomites.
- **Vaia.** The forest flattened in 2018 is `transitional` on the grid; its dead hosts no longer
  fruit, so the habitat affinities (0.1) handle it, not the weather.
- **Rain scale.** `precipitation_scale` was fitted on Tuscan gauges; a check against the ARPAV gauges
  is a region-config task (`regions/veneto.md`), not a species one.

## Slope and sun exposure

- **Slope, every key.** The band moves onto the region grid by the Tuscan rule: x1 up to about the
  woodland p90, x0.8 from about the maximum.
  - Woodland cells run p10 15.0°, p25 18.6°, median 23.8°, p75 30.0°, p90 35.3°, p95 37.5°, max
    49.9°; 45 % are steeper than 25°, 1.8 % steeper than 40°.
  - So x1 to 35° and x0.8 from 50°, like Trentino-Alto Adige (35/45), Friuli-Venezia Giulia (36/48)
    and Lombardia (35/46).
  - The Tuscan band would have docked 45 % of the cells (mean x0.96); this one docks 11 % (mean
    x0.996).
- **Sun exposure, kept.** On 15 October the woodland sun ratio runs p10 78 %, p25 90 %, median 101 %,
  p75 111 %, p90 120 % (below 1,000 m p10 80 %, median 101 %, p90 118 %; Tuscany p10 89 %, p90 111
  %).
  - The dry-side stoppers of *B. edulis* and *B. pinophilus* (x1 to 105 %) therefore dock 38 % of the
    woods below 1,000 m, most of them only slightly.
  - The shade-side ones of *B. reticulatus* and *B. aereus* (x1 from 95 %) touch about a third of the
    low woods and dock a tenth fully (x0.9 at 80 % or less); that of ovoli (x1 from 100 %, only above
    400-600 m) acts where the ovolo band is already closing.
  - The bands are statements about sun and drying, not Tuscan percentiles, so they are kept, as in
    the Alpine neighbours.

## Press contrasts (`sanity.yaml`)

`veneto/sanity.yaml` holds 16 contrasts, written down on 2026-09-29 before the region had any
scores: 14 porcini, 1 gallinacci (`gallinacci_...`, read with `--group gallinacci`) and 1 ovoli
(`ovoli_...`, `--group ovoli`).
- **Sources.** A research agent read the robots.txt of every outlet, then swept the Corriere delle
  Alpi, Tribuna di Treviso and Mattino di Padova sitemaps, AltoVicentinOnline, BellunoPress,
  OggiTreviso and Funghi Magazine's bulletins for 2016-2025 (24 candidates). I checked every quote
  in the table below against the page text: the local papers against the saved pages, the Funghi
  Magazine bulletins by opening them again (2026-09-29).
- **Areas.** 12 areas, by ISTAT 2025 comuni or province sigle. Every name resolves on the region
  grid (the merged comuni: Val di Zoldo, Alpago, Borgo Valbelluna, Setteville, Lusiana Conco, Pieve
  del Grappa, Valbrenta, Barbarano Mossano; Farra d'Alpago, Quero Vas, Alano di Piave, Cismon del
  Grappa and Crespano del Grappa no longer exist, and Sappada is in Friuli-Venezia Giulia since 2017).
- **Normal:** 2017-2025.

| area | woodland cells | median elevation | main habitats |
|---|---|---|---|
| `dolomites` (Cadore, Comelico, Agordino, Zoldo, Longarone: 39 comuni) | 1,301 | 1,398 m | spruce and fir 40 %, larch 23 %, Scots pine 9 % |
| `agordino` (16) | 343 | 1,422 m | spruce and fir 33 %, larch 30 %, mugo and Vaia 12 % |
| `asiago` (the Sette Comuni: 7) | 317 | 1,305 m | spruce and fir 52 %, beech 26 % |
| `lessinia` (10) | 138 | 878 m | beech 41 %, hop-hornbeam 39 % |
| `cansiglio_alpago` (Tambre, Alpago, Chies d'Alpago, Fregona) | 136 | 1,009 m | beech 36 %, hop-hornbeam 31 %, spruce 24 % |
| `prealps` (Asiago, Lessinia, Grappa: 27) | 730 | 1,059 m | beech 31 %, spruce and fir 31 %, hop-hornbeam 22 % |
| `prealps_pasubio` (the same with the Pasubio and Piccole Dolomiti: 34) | 949 | 1,007 m | beech 39 %, spruce and fir 25 %, hop-hornbeam 20 % |
| `colli` (Colli Euganei and Berici: 20) | 108 | 222 m | downy oak 61 %, chestnut 22 %, robinia 15 % |
| `hills` (the same with the Montello and Asolo hills: 30) | 161 | 227 m | downy oak 45 %, robinia 32 %, chestnut 19 % |
| `hills_valpolicella` (the same with the Valpolicella: 34) | 207 | 256 m | downy oak 41 %, robinia 25 %, chestnut 15 % |
| `belluno`, `treviso` (provinces) | 2,159, 363 | 1,180, 471 m | |

**How far to trust them.**
- **Local papers rarely sum up a season.** 7 contrasts rest on local papers quoting the Belluno
  group of the Associazione micologica Bresadola (Fabio Padovan, Claudio Sommavilla), the Ulss 1
  food-hygiene service, the Cansiglio naturalists and the Treviso groups. Three of them share the
  same lower side, the Belluno drought of August 2017.
- **Funghi Magazine carries the other 9.** Its weekly bulletins name the Agordino, the Dolomiti
  Bellunesi, the Asiago plateau, the Lessinia, the Grappa and the hills. It is one editor working
  from readers' reports and rain gauges, so several of these contrasts partly test the rain data.
  Only sentences describing fruiting that happened were used; forecasts were left out.
- **The west is thin.** No local source describes a Lessinia, Baldo, Colli Euganei or Colli Berici
  season: L'Arena and Il Giornale di Vicenza, which cover them, block AI agents. The Baldo appears
  only inside a Funghi Magazine list.

| id | higher | lower | window | main source | second sources | caveats |
|---|---|---|---|---|---|---|
| `dolomites_2019_2017_august` | Dolomites 2019 | Dolomites 2017 | 08-10 → 08-28 | [Corriere delle Alpi, 2019-08-29](https://www.corrierealpi.it/cronaca/funghi-tra-porcini-gialletti-e-russole-la-stagione-e-buona-jlojk87z): "La stagione è buona anche se non ci sono tanti funghi, se non in quota"; porcini the most present species (Padovan, Bresadola) | [Corriere delle Alpi, 2017-08-29](https://www.corrierealpi.it/cronaca/funghi-la-siccita-ne-impedisce-la-crescita-e0e2tn0t): "È una disperazione quest'anno ... Non c'è praticamente niente da raccogliere nei nostri boschi" (Sommavilla, Bresadola) | same group, same calendar day; in 2019 "nella parte bassa ... la produzione si è fermata", hence the Dolomite comuni only; Funghi Magazine (about 16 Aug 2019) had porcini "sporadici o addirittura assenti" in northern Veneto in mid-August |
| `dolomites_2018_2017_late_august` | Dolomites 2018 | Dolomites 2017 | 08-20 → 08-30 | [Funghi Magazine, 2018-08-31](https://funghimagazine.it/aggiornamento-funghi-1-settembre-2018/): "buone nascite in Veneto, ma molto meno buone nel Trentino e meno ancora in Alto Adige" | [Corriere delle Alpi, 2018-09-15](https://www.corrierealpi.it/cronaca/trovati-due-porcini-di-eccezionali-dimensioni-l1hvf8nk): an Alto Comelico haul "molto abbondante"; Corriere delle Alpi 2017-08-29 (above) | the 2018 side is region-wide; the Comelico haul is one anecdote in mid-September |
| `belluno_2023_2016_september` | province of Belluno 2023 | same, 2016 | 09-01 → 09-20 | [Corriere delle Alpi, 2016-09-21](https://www.corrierealpi.it/cronaca/sara-un-autunno-con-pochi-funghi-djbg1l34): "Assistiamo a un annata molto scarsa ... La produzione di porcini è stata abbastanza ridotta" (Padovan); fungi «notevolmente pochi» (Ulss 1) | [Funghi Magazine, 2023-09-20](https://funghimagazine.it/aggiornamento-porcini-20-09-2023/): Belluno and Treviso among "le province con ottime nascite in corso, pur senza “delirio”" | the 2023 side is a national province list |
| `dolomites_2023_2022_july` | Dolomites 2023 | Dolomites 2022 | 07-12 → 07-24 | [Funghi Magazine, 2023-07-20](https://funghimagazine.it/aggiornamento-funghi-20-07-2023/): "Ottime nascite anche in tutto l'alto Veneto da Agordo-Longarone fino alle Alpi Carniche" | [Corriere delle Alpi, 2022-07-29](https://www.corrierealpi.it/cronaca/funghi-la-stagione-non-decolla-lulss-ripristina-il-micologo-xrpqx002): "siccità e forte caldo da tre settimane impediscono la crescita dei miceli" (Bresadola); [FM 2023-07-28](https://funghimagazine.it/aggiornamento-funghi-28-07-2023/): the few edulis of the North "si sono trovati in Veneto, nel Friuli e Trentino Alto Adige" | the 2022 article is paywalled past its lead |
| `belluno_2022_september_vs_july` | province of Belluno, 20 Aug-5 Sep 2022 | same, 8-28 Jul 2022 | two windows | [Mattino di Padova, 2022-09-06](https://www.mattinopadova.it/regione/coldiretti-grazie-alle-piogge-e-boom-di-funghi-porcini-nei-boschi-veneti-hch5atv7): "è boom sulle Dolomiti di porcini, finferli", a Lorenzago di Cadore forager: "resta comunque una stagione da incorniciare" | Corriere delle Alpi 2022-07-29 (above): "Stagione semi compromessa" | the higher side is Coldiretti's wording plus one forager; both windows lie in the full season at altitude, so it tests the weather rules |
| `agordino_vs_lessinia_2023_august` | Agordino 2023 | Lessinia 2023 | 07-28 → 08-10 | [Funghi Magazine, 2023-08-10](https://funghimagazine.it/aggiornamento-funghi-10-08-2023/): "Una flessione sulle nascite ... zona di Rovereto-Pasubio e Lessinia. Meglio dalla Valsugana all'Agordino e su tutte le Dolomiti Bellunesi" | — | FM only; "flessione" is a decline, not nothing; the Lessinia line sits with southern Trentino |
| `asiago_2023_august_vs_july` | Asiago plateau, 1-10 Aug 2023 | same, 20-27 Jul 2023 | two windows | FM 2023-08-10: edulis "in buone quantità anche in zone molto frequentate ... quali l'Altopiano dei 7 Comuni o i monti trevigiani" | FM 2023-07-28: "Dall'Altopiano dei 7 Comuni riceviamo per esempio il report che ieri non si è trovato un solo Porcino", the woods still soaked | FM only; the lower side is one day's report, and blames too much water, which a rain rule reads as favourable (a real test) |
| `prealps_2022_august_vs_july` | Grappa, Lessinia, Asiago, 10-18 Aug 2022 | same, 10-31 Jul 2022 | two windows | [Funghi Magazine, 2022-08-18](https://funghimagazine.it/molti-funghi-in-molte-zone-ditalia/): "Partite le nascite anche in molte zone del Veneto montano, finalmente anche tra Grappa-Lessinia ed Alpiano dei 7 Comuni" | [AltoVicentinOnline, 2022-08-20](https://www.altovicentinonline.it/altri-comuni/i-primi-porcini-dopo-siccita/): the first porcini "dopo il lungo stop per la siccità" | the July side is implicit ("finalmente") |
| `cansiglio_2023_2016_early_october` | Cansiglio-Alpago 2023 | same, 2016 | 09-24 → 10-03 | [OggiTreviso, 2016-10-04](https://www.oggitreviso.it/oltre-100-tipi-di-funghi-cansiglio-146011): "CANSIGLIO - Per i funghi, non è una buona stagione" (Associazione Naturalistica Prealpi Cansiglio) | [Tribuna di Treviso, 2016-10-04](https://www.tribunatreviso.it/cronaca/weekend-micologico-successo-a-fregona-v6pcgmus): "Pur con condizioni non ottimali per la crescita dei funghi"; [FM 2023-10-04](https://funghimagazine.it/aggiornamento-porcini-04-10-2023/): porcini "in quantità ... sulla fascia pedemontana veneta e friulana", the peak at 700-1,500 m | the 2016 lines are about the whole season; the 2023 side is a regional belt, the Cansiglio read into it |
| `lessinia_2019_2024_september` | Lessinia 2019 | Lessinia 2024 | 09-10 → 09-20 | [Funghi Magazine, about 20 Sep 2019](https://funghimagazine.it/dove-stanno-nascendo-i-funghi-porcini-le-piogge-cadute-in-italia/): "è in Lessinia che al momento si registrano le nascite migliori" | [FM 2024-09-19](https://funghimagazine.it/aggiornamento-nascite-funghi-19-09-2024/): "riceviamo report di nascite bloccate tra Lessinia-Pasubio-7 comuni e Grappa" (cold and wind) | FM only; the 2019 page is undated (its rain log runs 12-19 September) |
| `hills_vs_dolomites_2020_september` | hills with the Valpolicella 2020 | Dolomites 2020 | 09-07 → 09-21 | [Funghi Magazine, 2020-09-21](https://funghimagazine.it/meteofunghi-21-09-2020/): "In Veneto le nascite sono diminuite sulle Dolomiti ma sono aumentate tra Lessinia-Baldo-Altopiano di Asiago ma meglio ancora sulle zone prealpine e collinari" | — | FM only; "diminuite" is relative; the regional gates favour the Dolomites in September (the Alpine *B. edulis* window is still full), so the weather rules must reverse it |
| `dolomites_vs_hills_2021_august` | Dolomites 2021 | Colli Euganei and Berici 2021 | 08-08 → 08-19 | [Funghi Magazine, 2021-08-19](https://funghimagazine.it/aggiornamento-meteofunghi-porcini-20-08-2021/): "Va' un po' meglio invece sulle Dolomiti dove i Boletus edulis risultano sempre più frequenti", "La Bolla Calda Africana ha interrotto bruscamente le nascite sui colli Berici e ancor di più sugli Euganei" | — | FM only; readers of a forager blog wrote "Bellunese....poco, praticamente nulla" the same week (not checked by me); with the 2020 pair above, a constant bias between hills and Dolomites cannot pass both |
| `hills_vs_prealps_2024_september` | hills 2024 | Asiago, Lessinia, Grappa and Pasubio 2024 | 09-08 → 09-19 | [Funghi Magazine, 2024-09-19](https://funghimagazine.it/aggiornamento-nascite-funghi-19-09-2024/): "Le zone del Veneto meridionale sembrano essere le più favorite", "Favoriti i colli pedemontani", "nascite bloccate tra Lessinia-Pasubio-7 comuni e Grappa" | — | FM only; "Veneto meridionale" is loose |
| `treviso_2016_july_vs_august` | province of Treviso, 25 Jun-31 Jul 2016 | same, August 2016 | two windows | [Tribuna di Treviso, 2016-11-12](https://www.tribunatreviso.it/cronaca/sul-montello-boom-di-funghi-mai-cosi-tanti-lmhurciy): "un periodo positivo tra fine giugno e luglio, fino a che di mezzo si è messa l'assenza di piogge che ha di nuovo rallentato la crescita" | — | a retrospective in the journalist's words; the headline boom is chiodini, not a target species |
| `gallinacci_belluno_2019_2017` | province of Belluno 2019 | same, 2017 | 08-05 → 08-28 | [Funghi Magazine, about 16 Aug 2019](https://funghimagazine.it/buone-nascite-di-funghi-porcini-vediamo-dove-le-piogge-caduta-in-italia/): northern Veneto's persistent rain, "In questo caso le nascite di funghi Galletti risultano abbondanti, ma non quelle di funghi Porcini" | Corriere delle Alpi 2019-08-29: gialletti among the species "maggiormente presenti"; Corriere delle Alpi 2017-08-29: "praticamente niente da raccogliere" where other years "avevano già iniziato a riempire ceste e cestini di porcini, finferli" | the 2017 side names no chanterelle directly; the FM page is undated (rain log 11-16 August) |
| `ovoli_hills_2020_2021` | hills 2020 | hills 2021 | 09-05 → 09-21 | FM 2020-09-21 (above): "nei boschi caldi termofili sono partite ottime buttate di funghi Porcini aereus e subito dopo di Ovoli reali" | FM 2021-08-19 (above): the heat stopped fruiting on the Berici and Euganei; [FM 2021-09-24](https://funghimagazine.it/aggiornamento-meteofunghi-24-09-2021-funghi-porcini-situazione-italia/): in many places of the Triveneto "non si è ancora avuta la classica “buttata” d'Agosto, neppure quella di Settembre" | FM only; the 2021 hill line is from mid-August, the September one Triveneto-wide |

**Left out:**
- **Outlets that block AI agents** (robots.txt checked on 2026-09-29; nothing fetched from them): Il
  Gazzettino, the Corriere del Veneto and corriere.it, L'Arena and Il Giornale di Vicenza (Athesis:
  ClaudeBot disallowed), il Dolomiti, L'Amico del Popolo, Qdpnews, Il Mattino, 7Gold Telepadova,
  VicenzaReport, ANSA, Rai TGR and the Today sites. The legacy `*.gelocal.it` addresses of the NEM
  papers disallow `anthropic-ai`; the current `corrierealpi.it`, `tribunatreviso.it` and
  `mattinopadova.it` domains, which carry the same articles, allow all agents and were used. The
  best unread leads, for a person to read: L'Arena 2022 on the Lessinia ("Funghi, cestini vuoti per
  tre mesi"), and Il Gazzettino's Belluno pieces (Padovan's "anno d'oro", a June 2022 Comelico boom).
- **Weak or conflicting:**
  - Cadore and Comelico 2025 (a Carabinieri forestali release: about 100 kg of mostly *B. edulis*
    seized): enforcement counts pickers as much as fungi;
  - northern against south-western Veneto in mid-August 2019 (FM's "Veneto sudoccidentale" is
    undefined, and conflicts with the Bresadola's good high ground the same weeks);
  - Comelico against the rest of the Dolomites in October 2023 ("al confine con l'Austria ed il
    Friuli" read as Comelico);
  - the Treviso mountains against Asiago in July 2023 (an anonymous comment);
  - Asiago 2025 against 2021 (Coldiretti Vicenza against blog comments, and FM called Asiago
    "discrete" in mid-August 2021);
  - Veneto September against early October 2024 and the pedemontana in September against October
    2023 (region-wide or belt-wide statements; kept as colour in the year picture);
  - finferli in the alto Veneto 2024 against 2022 (the 2022 side names no chanterelle).
- **Forecasts and rain reasoning:** the late-September 2024 outlooks, FM's province rankings.

**Year picture from the press** (context, not scored):

| year | Dolomites (Belluno) | Prealps (Asiago, Lessinia, Grappa, Pasubio, Baldo, Treviso Prealps, Cansiglio) | hills (Euganei, Berici, Montello, Asolo, Valpolicella) |
|---|---|---|---|
| 2016 | "annata molto scarsa" (21 Sep) | Cansiglio "non è una buona stagione" (4 Oct); Treviso porcini good late June-July, slowed in August | a chiodini boom on the Montello in November (not a target species) |
| 2017 | drought: "È una disperazione", nothing in late August | — | — |
| 2018 | "buone nascite in Veneto" late August; a big Comelico haul mid-September; Vaia on 29 October | — | — |
| 2019 | galletti abundant, porcini sporadic in mid-August (persistent rain); good "in quota" to about 20 August | estatini early around the Lessini, Baldo and Vicenza hills (July); the Lessinia best about 20 September, Asiago restarting | edulis, estatini, ovoli and aereus about 20 September |
| 2020 | good mid-August, declining by mid-September | better mid-September (Lessinia, Baldo, Asiago) | mid-September best: aereus, then ovoli |
| 2021 | edulis more frequent in the fir woods mid-August (readers disagree); September inhibited by cold rain and wind | Asiago "discrete" mid-August; almost nothing in the Triveneto into October | heat stopped the Berici and Euganei in mid-August |
| 2022 | drought: "semi compromessa" in July; a "boom" and "una stagione da incorniciare" by early September | first flush mid-August after the drought (Grappa, Lessinia, Asiago), less in the Valpolicella | — |
| 2023 | "Ottime nascite" in mid-July (Agordo-Longarone); the Agordino best in early August; Belluno "ottime" mid-September | nothing on the Asiago plateau on 27 July, good there by 10 August; a "flessione" in the Lessinia; Treviso "ottime", Verona and Vicenza "buone o discrete" mid-September; the pedemontana in quantity early October | estivi, neri and ovoli on the plain's woods in early August |
| 2024 | worse in the alto Veneto in September (rain, cold, snow); finferli good in late July | "nascite bloccate" in the Lessinia, Pasubio, Asiago and Grappa mid-September | the southern Veneto and the "colli pedemontani" favoured mid-September |
| 2025 | Cadore and Comelico porcini hauls (the forest police's seizures); a Triveneto "esplosione di edulis" in early August | an "eccezionale" flush in the Vicenza mountains in early August (Coldiretti) | — |

2017 and 2022 were the drought summers, as next door. 2023 was the best documented year, good in
the Dolomites from mid-July and on the Prealps from August. 2021 failed in the hills from heat and
in the mountains from cold rain and wind, as in Friuli-Venezia Giulia.

## Open questions

- **Hop-hornbeam for *B. edulis* and *B. pinophilus*.** 0.1 here, where Friuli-Venezia Giulia and
  Trentino-Alto Adige kept 0.3. The class is a fifth of Veneto's woods and on limestone, and the
  evidence is a forager magazine, the Colli Euganei lists and Trentino's records; Veneto's own *B.
  edulis* records are too few below 1,000 m to test it. The Lessinia, Baldo and Treviso Prealps
  contrasts (much hop-hornbeam at 600-900 m) and the backtest are the checks; the three Alpine regions
  should end on one value.
- **Larch.** 0.1 for every porcino and the chanterelles, as in the neighbours; Veneto's records are not
  depleted in larch cells (11 % against 11 %), because the Dolomite larch mixes with spruce. The census
  never names larch alone in 293 chanterelle notes.
- **Vaia and bark beetle.** 10,227 ha of flagged forest are `transitional` (0.1 for the mountain
  taxa). Clearings with surviving trees, edges and regrowth may still fruit; the bark-beetle kill is
  spreading after 2021 and the map will age. A newer damage layer, or a separate habitat key, would
  keep this honest.
- **Coastal pinewoods typed as `fir_spruce`.** The conifer plantations (31220) include the stone and
  maritime pine of Rosolina, Bibione and the Bosco Nordio, which the region config maps with the
  spruce plantations. Only 3 woodland cells lie in Venezia and Rovigo, and the porcini bands close
  above them, but gallinacci get full habitat credit there. `mediterranean_pine` would be the right
  key if the grid can tell them apart (the 2006 map's `specifiche` can).
- **The west is unread.** L'Arena and Il Giornale di Vicenza block AI agents, and the Museo di Storia
  Naturale di Verona allows only search engines: no Lessinia or Baldo source beyond Funghi Magazine,
  and no Baldo contrast. A person could read L'Arena's 2022 Lessinia piece ("Funghi, cestini vuoti per
  tre mesi").
- **The gallinacci handover.** Veneto's dated census records set it at 600-1,000 m, Friuli-Venezia
  Giulia chose 900-1,300 m on Carinthian ones: the backtest can compare them in the regions where both
  kinds of records exist.
- **Leads not read:**
  - books: *I funghi dei Colli Berici* (AMB Vicenza 2022), *Osserviamo i funghi nel Parco dei Colli
    Euganei* (AMB Padova 2023), *I funghi del Montello* (1990), *Atlante dei funghi del Vicentino*
    (2003), *Funghi del Cansiglio*;
  - the Parco Colli Euganei's rules (its robots.txt blocks all crawlers) and the Dolomiti Bellunesi
    park's (HTTP 403);
  - the official consolidated L.R. 23/1996 on consiglioveneto.it (HTTP 403; a publisher's
    consolidated text was used, and the 2023 amendment read on the BUR);
  - Veneto Agricoltura's *Funghi spontanei del Veneto* (scanned; it is a generic sellers' manual);
  - the census's underlying Veneto porcini and ovoli records, which are "Riservato" on the map: dated
    porcini records from the Federazione Micologica dei Gruppi Veneti would be Veneto's first porcini
    validation set.

## References added for Veneto

| id | kind | verified | used for |
|---|---|---|---|
| `mushma_veneto_occurrence_check_2026` | analysis | verified | Veneto record months, elevations, surroundings; census recount and the dated chanterelle records |
| `mushma_veneto_forest_check_2026` | analysis | verified | habitat contents and elevations, slope and sun ratios, gate effects |
| `ven_lr23_1996` | institutional | verified | picking law: 3 kg, the 1 kg species cap, the closed-ovolo ban, no cap size |
| `ven_lr15_2023` | institutional | verified | the 2023 change to the fee article |
| `ven_rv_raccolta_funghi` | institutional | verified | permits, default days, closed parks, the Montello |
| `ven_reggenza_funghi` | institutional | verified | Asiago plateau rules; ovolo and *B. edulis* notes |
| `ven_del_favero2000` | institutional | verified | forest regions, hop-hornbeam share, beech above 800 m, native Scots and black pine |
| `ven_del_favero2006` | institutional | verified | forest areas by category, spruce plantations |
| `ven_raf2020` | institutional | verified | forest by altitude band and province, pickers |
| `ven_arpav_atlante_prec2013` | institutional | verified | rain range, belts and regime |
| `ven_arpav_clima_cm` | institutional | verified | lapse rates, station means |
| `ven_arpav_2022` | institutional | verified | the 2022 drought |
| `ven_arpav_2017` | institutional | verified | the 2017 drought |
| `ven_ambpd_fn2007b` | society | verified | Colli Euganei chestnut woods' fungi |
| `ven_ambpd_fn2008a` | society | verified | *B. aereus* on the Colli Euganei; downy-oak and hop-hornbeam woods' fungi; the 2007 drought |
| `ven_ambpd_fn2008b` | society | verified | an April *B. reticulatus*; Monte Calbarina's fungi |
| `ven_ambpd_fn2009a` | society | verified | warm oak woods' fungi; the ovolo's rarity; the 2008 drought |
| `ven_ambpd_fn2018` | society | verified | the early, rich flush of September 2017 on the hills |
| `ven_saccardo_erbario` | society | verified | Treviso specimens of the ovolo, *B. pinophilus*, *B. aestivalis* |
| `ven_gmb_primipassi` | society | verified | *B. pinophilus* hosts and early start, *B. aereus* absent from the Alps, *B. edulis* to 2,000 m |
| `ven_fm_funghi_giugno` | web | verified | June *B. aereus* on the Veneto hills, June *B. pinophilus* in the alto Veneto |

Existing references the changes lean on, opened again for this card:
- `muse_censimento_edulis`, `muse_censimento_boletus`, `muse_censimento_pinophilus`,
  `muse_censimento_caesarea`, `muse_censimento_cibarius`, `muse_censimento_cantharellus`,
  `fvg_muse_censimento_aestivalis`, `fvg_muse_censimento_ferruginascens` (census pages, map points and
  the public Cantharellus records);
- `fvg_campo2022_cansiglio` (the Cansiglio beech checklist and its table);
- `funghimagazine_carpino_nero2026` (hop-hornbeam hosts);
- `funghimagazine_ovolo` (the north-eastern ovolo limit: "oltre i 600 metri al Nord Est").

Cited as the neighbours' appendices report them, not opened again: `taa_mandolini2025_larix`,
`taa_mandolini2024_cembra`, `mushma_taa_forest_check_2026`, `mushma_occurrence_check_taa_2026`,
`mushma_fvg_occurrence_check_2026`, `fvg_omg_observations`, `fvg_ktn_pilzschutz`,
`fvg_cebulec_pertot1985`.
