# Species ecology: Lombardia (regional appendix to species-ecology.md)

## Summary for the region doc

All three groups and all six keys are kept for Lombardia (`api/src/api/config/species/lombardia/`, copied from Tuscany), and every weather rule and growth clock is Tuscany's, unchanged, because no Lombard or Alpine study gives better numbers. Lombardia is the first region with large spruce, larch and Scots-pine woods up to the tree line (fir/spruce 15 % and larch/stone pine 10 % of the wooded area on the grid built from Regione Lombardia's Carta forestale), so the changes are Alpine: *B. edulis* and *B. pinophilus* get an Alpine summer window blended in above 900–1,300 m and bands reaching 2,100–2,200 m; larch and stone pine (`other_conifer`) drop to non-host (0.1) for *B. edulis*, *B. pinophilus* and gallinacci, because root-tip studies find no *Boletus* on them and the Lombard records sit in spruce; Scots pine (`mountain_pine`; the mughete are not woodland) becomes a full host of *B. pinophilus*; the gallinacci, mostly *C. cibarius* s.str., take beech and spruce/fir as full hosts, a band to 2,100 m and no winter mode; *B. reticulatus*, *B. aereus* and ovoli end earlier (31 October, 20 November, 15 November) and *B. aereus* stays in the hills (zero at 1,100 m); the slope stopper moves onto the Lombard grid (x1 to 35°, x0.8 from 46°; woodland median 27.5°). The evidence is 403 Lombard iNaturalist records of the six taxa (aggregates only, also joined to the grid's habitats), about 9,800 SwissFungi records from the neighbouring Alps and Lombard society and institutional pages, with 44 new references, all opened. `sanity.yaml` holds 14 press contrasts from 2017–2025 (10 porcini, 2 gallinacci, 2 ovoli) in seven areas, from Valtellina, the Orobie bergamasche and Val Camonica to the upper Valle Staffora, the Oltrepò and the alto Varesotto; every main source was opened and its quote checked.

---

Research date: 2026-09-26 (dates Europe/Rome, units metric). Card: `region-lombardia-species.md`
(child of `region-lombardia.md`). This appendix records how the Tuscan rule set
(`api/src/api/config/species/tuscany/`) was carried to Lombardia (`species/lombardia/`), what changed
and why. It covers **fruiting conditions only**: nothing here is about edibility or identifying
specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(44 added for Lombardia, listed at the end). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every
number is a prior for the backtest; season windows, altitude bands, habitat affinities and the slope
band stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`). Rule ids LOM-* are named in each
changed factor's `notes`.

## Summary

1. **All three groups and all six keys are kept.** Every taxon has Lombard records
   (`mushma_occurrence_check_lombardia_2026`) and a Lombard society or institutional source.
   - The ovolo is regulated by name: "sono vietati ... la raccolta di funghi decomposti e di ovuli
     chiusi di Amanita cesarea" (`lomb_lr31_2008_funghi`, art. 98).
   - It has 24 iNaturalist records in 7 of 12 provinces.
   - *B. aereus* is the weakest key: 9 records, all but one below 600 m, and absent from the
     1,700-species Stelvio checklist (`gm_alta_valtellina_stelvio`). It is kept, with its band cut to
     the hills.
2. **Lombardia is conifer country above 1,000 m.** On the grid:
   - fir/spruce is 15.2 % of the wooded area and larch/stone pine 9.7 %;
   - the woods reach 2,328 m, and the Upper Valtellina tree line lies at 2,300–2,440 m
     (`lomb_masseroli2016_treeline`);
   - 70 % of the located *B. edulis* records and 40 % of the *Cantharellus* records are at 1,000 m
     or higher.

   So the high-altitude windows and bands carry most of the changes, as in Piemonte (region/piemonte
   branch). On larch this appendix goes one step further than Piemonte, on evidence Piemonte did not
   have (below).
3. **What changes:**
   - **Season:** an Alpine summer window for *B. edulis* and *B. pinophilus*; earlier ends for *B.
     reticulatus*, *B. aereus*, ovoli and gallinacci; no winter chanterelles.
   - **Altitude:** bands follow the Alpine belts.
   - **Habitat:** host tiers move for five of the six keys, where the Lombard classes hold different
     trees (larch, Scots pine, hop-hornbeam) or the Alpine evidence says so (beech and spruce for
     gallinacci, beech for *B. reticulatus*).
   - **Slope stopper:** moved onto the Lombard grid.
4. **Weather rules are all kept.** No Lombard or Alpine study gives a rain, lag or temperature
   threshold for these taxa. The Alpine numbers found (3BMeteo, Funghi Magazine, a German Red-List
   portrait) sit inside the Tuscan settings. The Lombard rain climate runs from 650 mm (Livigno) to
   2,300 mm (the lake ridges). That is left to the cell's own weather and to the percent-of-normal
   porcini rain rule.
5. **Evidence: regional plus the neighbouring Alps.** The 44 new sources were all opened:
   - 7 peer-reviewed (none of them Lombard fungal field data);
   - 12 institutional;
   - 11 society pages (Lario, Valtellina, Brescia, Milan, Trento and the north-east Italian census);
   - 2 datasets and 4 own analyses;
   - 8 forager and bulletin pages (folklore).

   The quantitative weight comes from the Lombard iNaturalist records (403 records of the six taxa)
   and SwissFungi (the Swiss national fungi records, about 9,800 of these taxa, including the Ticino
   and Graubünden valleys on the Lombard border).

## At a glance: what differs from Tuscany and why

Trapezoids are `[zero, full, full, zero]`, dates `DD-MM`, altitudes in metres.

| key | factor | Tuscany | Lombardia | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | one window 01-07 → 01-09 … 15-11 → 20-12 | **lowland 01-07 → 15-08 … 31-10 → 05-12 below 900 m; Alpine 01-07 → 01-08 … 25-09 → 25-10 above 1,300 m** | records ≥1,300 m: Jul 1, Aug 21, Sep 19, Oct 9, none after 31 Oct; SwissFungi 1,401–1,800 m p95 6 Oct; below 600 m Lombard records run to 28 Nov | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **100 → 400 … 1,800 → 2,200** | records p10 480, p95 1,827, max 2,157 m; SwissFungi p99 1,858 m, records at 2,140 m on the Valchiavenna border | plausible |
| *edulis* | habitat `other_conifer` | 0.3 | **0.1** | here only larch and stone pine: no *Boletus* on their roots; records above 1,500 m sit in spruce | plausible |
| *reticulatus* | season end | 30-09 → 15-11 | **30-09 → 31-10** | October 0.1× the effort, none in November; SwissFungi October 0.15× | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | **0 → 150 … 1,250 → 1,650** | records p90 1,323 m, beech to about 1,480 m | plausible |
| *reticulatus* | habitat | beech 0.6, fir/spruce 0.6, mountain pine 0.6 | **beech 1.0, fir/spruce 0.3, mountain pine 0.3** | beech 45 % of SwissFungi partners; "più raro nei boschi di conifere" | plausible |
| *aereus* | season | upland/lowland split (400–600 m) | **one window 01-07 → 15-08 … 15-10 → 20-11** | no Apennine upland form, no macchia; records Aug–Oct; SwissFungi p95 17 Oct | plausible |
| *aereus* | altitude | … 800 → 1,250 | **… 700 → 1,100** | records p90 725 m; SwissFungi south of the Alps max 982 m | plausible |
| *aereus* | habitat `mixed_broadleaf` | 0.3 | **0.6** | hop-hornbeam and hornbeam are hosts (SwissFungi hornbeam 11 %) | plausible |
| *pinophilus* | season | spring + autumn windows with a summer gap | **lowland 01-05 → 20-05 … 10-11 → 10-12 below 900 m; Alpine 01-07 → 25-07 … 25-09 → 25-10 above 1,300 m** | no summer gap in Lombard or Swiss records; above 1,000 m no spring record | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **200 → 500 … 1,700 → 2,100** | Scots-pine heaths of the high plain; SwissFungi p95 1,700, max 2,025 m | plausible |
| *pinophilus* | habitat | mountain pine 0.6, other conifer 0.3, mixed broadleaf 0.3 | **1.0, 0.1, 0.1** | Scots pine its commonest partner; larch not a host; no record among hornbeams | plausible |
| ovoli | season | 01-06 → 01-09 … 05-11 → 30-11 | **01-06 → 01-08 … 20-10 → 15-11** | Lombard Aug 8, Sep 7, Oct 7, Nov 0; SwissFungi Aug 149, Sep 170, Oct 167, Nov 0 | plausible |
| gallinacci | season | lowland wraps to 25-01, mountain to 15-11; handover 600–1,000 m | **lowland 15-05 → 15-06 … 31-10 → 30-11; mountain 01-06 → 01-07 … 30-09 → 31-10; handover 900–1,300 m** | no Dec–Apr records; the Alpine peak is Jul–Aug; the 600–1,000 m records peak in October | plausible |
| gallinacci | altitude | … 1,000 → 1,700 | **… 1,600 → 2,100** | records p90 1,511, p95 1,660 m; NE-Alpine census 48 % at 1,200–1,800 m, max 2,040 m | plausible |
| gallinacci | habitat | beech 0.6, fir/spruce 0.6, mountain pine 0.3, other conifer 0.3 | **1.0, 1.0, 0.6, 0.1** | beech, spruce and fir are the Alpine partners; Scots pine enriched in the records; larch pages list no chanterelle | plausible |
| every key | slope stopper | x1 to 25°, x0.8 from 40° | **x1 to 35°, x0.8 from 46°** | same rule on the Lombard grid: p90 35.1°, max 46.4° | as Tuscany |
| every key | weather, growth clock, sun exposure, other stoppers | — | **kept** | no Lombard numbers; see Weather | as Tuscany |

Kept on purpose:
- ovoli altitude and hosts, and *B. edulis*/*B. pinophilus* fir/spruce as host;
- chestnut as host for every porcino that had it;
- mixed broadleaf at 0.3 for *B. edulis* and gallinacci;
- the gallinacci and ovoli soil-pH and lithology rules, still disabled.

**Effect on the grid** (the habitat and altitude gates only, `mushma_lombardia_forest_composition_2026`):

| key | habitat gate full on (Tuscan → Lombard rules) | altitude gate full on | gates at record cells vs all woodland (Lombard rules) |
|---|---|---|---|
| *edulis* | 92 % → 86 % of woodland cells | 57 % → 85 % | 0.98 vs 0.90 (92 records) |
| *reticulatus* | 89 % → 80 % | 63 % → 72 % | 0.95 vs 0.80 (20) |
| *aereus* | 43 % → 55 % | 41 % → 33 % | 0.58 vs 0.44 (7) |
| *pinophilus* | 92 % → 73 % | 49 % → 76 % | 1.00 vs 0.80 (12) |
| ovoli | 42 % (kept) | 37 % (kept) | 0.93 vs 0.44 (14) |
| gallinacci | 92 % → 87 % | 56 % → 90 % | 0.99 vs 0.91 (100) |

Under the Tuscan rules the Alpine records lost credit to the altitude bands (*edulis* 0.87 at the
record cells, gallinacci 0.78). The one record the Lombard rules lose is the *B. aereus* record at
1,077 m, in a beech cell.

## Lombardia in brief

**Woods on the grid.** The Lombardia woodland grid was built 2026-09-26 (region card) from Regione
Lombardia's Carta forestale. That map is the forest perimeter of L.R. 31/2008 with the PIF real forest
types (Del Favero's typology), filled in from DUSAF where a PIF has none.
- **Size:** 6,018 woodland cells; 592,447 ha of forest (INFC 2015: 621,968 ha,
  `infc2015_lombardia`; ERSAF 2023: 618,403 ha, `ersaf_stato_foreste2023`).
- **Terrain of the woodland cells:** elevation median 921 m (p95 1,781 m, max 2,328 m); slope median
  27.5° (Tuscany 16.6°); SoilGrids topsoil pH median 6.0 (p10 5.6, p90 6.5).
- **Left out by the map:** green-alder scrub (17,056 ha) and mountain-pine scrub (mughete, 7,631 ha).
- **How the table is built:** shares are of the wooded area on woodland cells. The class contents
  are the Carta forestale's category areas, computed here from the map; elevations are cell
  elevations weighted by each habitat's area. Source for all of it:
  `mushma_lombardia_forest_composition_2026`.

| habitat key | share | the Lombard trees in it (Carta forestale class, ha) | median elevation (p10–p90) |
|---|---|---|---|
| `mixed_broadleaf` | 24.6 % | hop-hornbeam (orno-ostrieti 72,481), maple-ash and maple-lime (aceri-frassineti 38,282), birch and hazel (betuleti e corileti 13,935), hornbeam; most untyped "Latifoglie DUSAF" cells borrow a type from their neighbours | 811 m (488–1,186) |
| `chestnut` | 15.7 % | castagneti 72,795, 49 % typed on carbonate and 42 % on silicate rock by the map's type names; fruit orchards 408 | 655 m (391–963) |
| `fir_spruce` | 15.2 % | Norway spruce (peccete montane 28,760, altimontane 24,419, secondarie 9,066, sostituzione 6,087) and silver fir (abieteti 8,309) | 1,408 m (1,024–1,761) |
| `beech` | 14.3 % | faggete submontane 21,320, montane 37,395, altimontane 4,261, primitive 2,686 | 1,060 m (749–1,373) |
| `other_conifer` | 9.7 % | larch (lariceti 53,682) and larch-stone pine (larici-cembreti e cembrete 6,889), nothing else | 1,609 m (1,189–1,979) |
| `deciduous_oak` | 6.4 % | downy oak 19,054, sessile oak 11,086, Turkey oak 3,770, pedunculate oak 2,023, oak-hornbeam 2,807 | 568 m (273–986) |
| `mixed_broadleaf_conifer` | 5.3 % | spruce-beech (piceo-faggeti 9,662), DUSAF mixed woods 11,702, recent plantings (69 % conifer) 9,476 | 1,031 m (320–1,405) |
| `exotic_broadleaf` | 3.5 % (8.0 % of all forest, most of it off the woodland cells) | robinia (robinieti misti 32,794, puri 5,792), late cherry | 360 m (232–602) |
| `riparian` | 2.7 % | alder, willow, riparian DUSAF | 466 m (83–878) |
| `mountain_pine` | 2.1 % | Scots pine only: montane pinete 8,234 (mostly the provinces of Sondrio and Brescia), planiziali 2,527 (the brughiere of the Ticino and Varese high plain) | 840 m (341–1,485) |
| `transitional_woodland_shrub` | 0.5 % | tall shrub-woodland (DUSAF 3241) | 793 m |
| `evergreen_oak` | < 0.1 % | holm oak on the Garda and Lario cliffs (296 ha) | 545 m |
| `mediterranean_pine`, `macchia` | 0 | absent | |

The regional inventories agree:
- ERSAF 2023 by category: castagneti 11.7 %, orno-ostrieti 11.4 %, peccete 11.1 %, faggete 10.8 %,
  lariceti and larici-cembreti 9.8 %, robinia and other "formazioni antropogene" 8.1 %
  (`ersaf_stato_foreste2023`).
- INFC 2015: spruce 87,863 ha, chestnut 82,079, hop-hornbeam and hornbeam 81,720, beech 66,650,
  larch and stone pine 53,420; no Mediterranean pine or holm oak (`infc2015_lombardia`).

**Altitude belts** (`ersaf_specie_forestali2019`, `lomb_habitat_manual2018`,
`parco_orobie_valt_conifere`, `lomb_masseroli2016_treeline`; p5–p95 of each class from
`mushma_lombardia_forest_elevation_2026`):

| type | altitude (m) and where |
|---|---|
| robinia | "fino ad un massimo di 800 m"; mapped 88–556 (median 298) |
| chestnut | "Collina e bassa montagna fino ai 900 m di quota", soil "Acido"; mapped 303–928 (median 619) |
| downy and sessile oak | downy oak "fino ai 1000 m", calcareous; mapped 211–922 and 221–1,162 |
| hop-hornbeam | "fino ai 1000 m", "Calcareo superficiale"; mapped 300–1,171 (median 726) |
| beech | "dai 600 ai 1500 m"; low beech with chestnut "in genere sotto i 1300 m", high beech with conifers "in genere oltre i 1100 m"; mapped 591–1,674 |
| silver fir | "900-1500 m"; mapped 884–1,570 |
| Norway spruce | "dai 900 fino ai 1800 m"; only in the Alpine chain, "mancando in tutta la fascia prealpina"; montane spruce to about 1,550 m, subalpine "dai 1500 metri circa fino al limite superiore del bosco" (Orobie); mapped 1,010–1,964 |
| Scots pine | the high-plain brughiere (285–437 m) and the mountains (507–1,625 m, silicate inner valleys median 1,259 m) |
| larch, stone pine | larch "tra i 1000 e i 2000 m", "Lariceti, larici-cembreti e foreste di abete rosso"; larch pioneer woods on abandoned pastures "spesso accompagnate dall'abete rosso"; mapped larch 1,029–2,050, larch-stone pine 1,718–2,230 |
| tree line | Upper Valtellina 2,300–2,440 m by limiting landform, the climatic tree line higher (Masseroli et al. 2016) |

**Forest regions and substrate** (`lomb_boschi_lombardia2004`, `lomb_andreis_sartori2009`):
- **Oltrepò Pavese:** Apennine; sandstone and marl; downy oak, hop-hornbeam and Turkey oak, beech at
  the top, chestnut.
- **Moraine hills and high plain (avanalpica, planiziale):** oak-hornbeam, chestnut, Scots-pine heath,
  "ampiamente sostituita ... dai robinieti".
- **Outer Prealps (esalpica):**
  - the eastern part (Bergamo and Brescia Prealps, Garda, Iseo, southern Lario) is "tipica dei
    substrati carbonatici": downy oak, hop-hornbeam and Scots pine below, beech above;
  - the western part (Valsassina, Alto Lario occidentale, alto Varesotto) is "tipica dei substrati
    silicatici": chestnut and oak below, beech above.
- **Mesalpica (Valtellina, Val Camonica):** conifers, "in particolare i due abeti".
- **Endalpica (Bormiese, alta Valmalenco, alta Val Camonica):** spruce, with larch and stone pine
  above.

The substrate split matters for the disabled soil rules and for which chanterelle grows where; see
Open questions.

**Climate** (`lomb_ceriani_carelli_precip`, `lomb_arpa_clima`, `lomb_masseroli2016_treeline`).
- **Annual rain:** 850–950 mm by the Po, about 1,000 mm at Milan and Brescia, 1,400–1,600 mm on the
  first Prealps and over 2,000 mm on the lake ridges (Vararo 2,326 mm, Magreglio 2,196, Valcanale
  2,240).
- **Drier valleys:** Garda has 850–1,200 mm; Val Camonica gets drier up-valley (Lovere 1,191, Temù
  982). The driest area is "l'alta Valtellina ed ... l'area di Livigno", 700–900 mm (Trepalle 646,
  Bormio 724), where the rain "mainly falls during the summer".
- **Seasonal regime:** region-wide the station medians peak in May (104 mm) and November (114 mm)
  and hold 76–90 mm a month in summer, largely from thunderstorms.
- **Temperature:** the plain averages about 14 °C a year (1991–2020).

**Picking law** (`lomb_lr31_2008_funghi`). L.R. 31/2008, arts. 96–112:
- "La raccolta dei funghi è gratuita su tutto il territorio regionale", but Comunità montane and
  parks may charge a contribution;
- dawn to dusk, 3 kg per person per day;
- "sono vietati ... la raccolta di funghi decomposti e di ovuli chiusi di Amanita cesarea";
- no season calendar and no altitude rule; minimum sizes are left to Giunta acts.

None of it changes where or when the fungi fruit, so none of it is encoded.

## Occurrence cross-check (Lombardia)

**Method.** Queried 2026-09-26 (`mushma_occurrence_check_lombardia_2026`); aggregates only, no
coordinates stored.
- **GBIF:** `gadmGid=ITA.10_1`. It held no soil-DNA `MATERIAL_SAMPLE` rows and none of the excluded
  *Cantharellus* keys.
- **iNaturalist:** place 10870 ("Lombardia", admin level 10, the id the region config uses),
  verifiable records.
- **Elevations:** from the Open-Meteo elevation API, for records that are not obscured and have an
  accuracy of 1 km or better (or none stated).
- **Enrichment:** the taxon's monthly share ÷ the monthly share of all 36,719 Lombard iNaturalist
  fungi records. October carries 22 % of that effort, so October enrichments read low.
- **GBIF is not independent:** 83 % of its records are iNaturalist copies. The rest are 32 Swiss
  National Fungi Databank records from the border (27 *Cantharellus*, 5 *B. edulis*) and 1
  Observation.org record.
- **Coverage:** the histograms include 2026 to date.

| taxon | source | n | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | iNat | 170 | | | | | 2 | 2 | 10 | 50 | 72 | 31 | 3 | |
| | enrichment | | | | | | 0.2 | 0.3 | 1.0 | **2.8** | **2.7** | 0.8 | 0.2 | |
| *B. reticulatus* | iNat | 38 | | | | | | 6 | 8 | 11 | 12 | 1 | | |
| | enrichment | | | | | | | **3.6** | **3.7** | **2.7** | **2.0** | 0.1 | | |
| *B. aereus* | iNat | 9 | | | | | | | | 2 | 4 | 3 | | |
| *B. pinophilus* | iNat | 16 | | | | | | | 2 | 5 | 5 | 4 | | |
| *A. caesarea* | iNat | 24 | | | | | | 2 | | 8 | 7 | 7 | | |
| | enrichment | | | | | | | 1.9 | | **3.1** | **1.8** | 1.3 | | |
| *Cantharellus* | iNat | 146 | | | | | 1 | 7 | 31 | 25 | 26 | 47 | 9 | |
| | enrichment | | | | | | 0.1 | 1.1 | **3.8** | **1.6** | 1.1 | **1.5** | 0.5 | |

**Elevations** (located records):

| taxon | located n | p10 | median | p75 | p90 | max (m) | ≥ 1,000 m |
|---|---|---|---|---|---|---|---|
| *B. edulis* | 110 | 480 | 1,266 | 1,504 | 1,705 | 2,157 | 77 (70 %) |
| *B. reticulatus* | 27 | 239 | 732 | 1,036 | 1,323 | 1,824 | 10 |
| *B. aereus* | 8 | 195 | 408 | 511 | 725 | 1,077 | 1 |
| *B. pinophilus* | 13 | 572 | 1,351 | 1,447 | 1,636 | 1,683 | 10 |
| *A. caesarea* | 20 | 324 | 440 | 623 | 783 | 1,018 | 2 (one find) |
| *Cantharellus* | 116 | 351 | 828 | 1,286 | 1,511 | 2,307 | 46 |

**Months by elevation** (located records):

| taxon | band | Jun | Jul | Aug | Sep | Oct | Nov | median date |
|---|---|---|---|---|---|---|---|---|
| *B. edulis* | ≥ 1,500 m (28) | | 1 | 13 | 8 | 6 | | 30 Aug |
| | 1,000–1,500 m (49) | | 3 | 18 | 21 | 7 | | 6 Sep |
| | 600–1,000 m (18) | 1 | 1 | 4 | 9 | 3 | | 17 Sep |
| | < 600 m (15) | | | 2 | 5 | 6 | 2 | 1 Oct |
| *B. reticulatus* | < 600 / 600–1,000 / ≥ 1,000 m | 1/1/1 | 1/2/4 | 3/3/1 | 4/1/4 | 1/0/0 | | 28 Aug / 9 Aug / 27 Jul |
| *Cantharellus* | ≥ 1,500 m (15) | | 4 | 6 | 3 | 2 | | 21 Aug |
| | 1,000–1,500 m (31) | 2 | 11 | 6 | 8 | 4 | | 16 Aug |
| | 600–1,000 m (32) | 2 | 3 | 5 | 5 | 14 | 3 | 5 Oct |
| | < 600 m (38) | 1 | 3 | 5 | 5 | 19 | 5 | 7 Oct |

The latest dates: *B. edulis* at 1,300 m and above 31 October (none later); below 600 m 28 November.
*Cantharellus* lowland 28 November; nothing in December to April anywhere (one May record).

**Which habitats hold the records.** Each located record was joined to its grid cell, and the cell's
habitat fractions were averaged. They are compared with the mean over woodland cells in the same
elevation band. Counts only, no coordinates. Records' cells, % of woods (woodland in brackets):

| taxon, band (n) | fir/spruce | larch (`other_conifer`) | beech | chestnut | deciduous oak | mixed broadleaf | Scots pine | robinia |
|---|---|---|---|---|---|---|---|---|
| *B. edulis* ≥ 1,500 m (28) | **66** (40) | 30 (48) | 0 (4) | | | 3 (3) | 0 (2) | |
| *B. edulis* 1,000–1,500 m (49) | **52** (26) | 11 (10) | 13 (28) | 4 (4) | | 10 (19) | 1 (2) | |
| *B. edulis* < 1,000 m (33) | 4 (2) | 1 (1) | **18** (9) | **31** (25) | 6 (11) | 24 (32) | 0 (2) | 11 (7) |
| *B. reticulatus* 1,000–1,500 m (9) | 22 (26) | 3 (10) | **45** (28) | 13 (4) | 3 (2) | 11 (19) | | |
| *B. reticulatus* < 1,000 m (17) | 2 (2) | | 5 (9) | **32** (25) | 14 (11) | 22 (32) | | 14 (7) |
| *B. pinophilus* all (13) | **52** | 13 | 5 | 10 | 0 | 2 | 5 | 1 |
| *A. caesarea* < 1,000 m (18) | | | 2 (9) | **31** (25) | **31** (11) | 20 (32) | | 12 (7) |
| *Cantharellus* ≥ 1,500 m (15) | **50** (40) | 31 (48) | 0 (4) | | | 6 (3) | | |
| *Cantharellus* 1,000–1,500 m (31) | **53** (26) | 13 (10) | 7 (28) | 5 (4) | 1 (2) | 18 (19) | 1 (2) | |
| *Cantharellus* < 1,000 m (70) | 2 (2) | 1 (1) | **28** (9) | 22 (25) | 6 (11) | 16 (32) | **11** (2) | 9 (7) |

(*B. pinophilus* woodland baseline for all elevations: fir/spruce 15, mixed broadleaf 25, Scots pine 2.)

**Species inside *Cantharellus*:** *C. cibarius* 88 (median 1,142 m), genus only 21, *C. pallens* 10,
*C. friesii* 10, *C. romagnesianus* 6, *C. amethysteus* 6, *C. ferruginascens* 3. Each of the small
segregates has a median below 700 m, and 21 of their 35 records are from October–November. 44 % of
the records still need an ID, so the names are weak evidence.

**Neighbours** (iNaturalist enrichment against each place's own fungi effort):
- *B. edulis* peaks in August in Trentino-Alto Adige (July 1.4, August 1.9, September 1.4, October 0.4)
  and in Ticino.
- *Cantharellus* peaks in July–August in Trentino and falls below 1 from September.

**Caveats.**
- **Presence-only records.** They sit near trails and towns, and summer hikers raise the Alpine
  effort in July–August (Trentino's effort peaks in August).
- **Obscured *B. edulis*.** 21 % of its records are obscured by their observers, and they are left
  out of the elevations.
- **Recent years.** 31–68 % of each taxon's records are from 2023–2026.
- **Geography.** 88–100 % of each taxon's located records are north of 45.6° N. The Oltrepò
  Apennine has at most 2 records per taxon and cannot be checked from records; its rules rest on the
  Emilia-Romagna evidence next door.
- **Frozen priors.** The season, band and habitat choices below were drawn partly from these same
  records, all years included, so they stay frozen priors.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional and Alpine evidence.**

*Which porcino where* (plausible):
- **Lario society habitat series** (`gm_cantu_como_ambienti2021`, `gm_cantu_como_schede_boletus`):
  - the spruce wood ("dai 1200 m ai 2000 m", "normalmente condivide il territorio con il larice")
    and the beech wood list *B. edulis* and *B. pinophilus*;
  - the chestnut wood lists *B. reticulatus* and *B. edulis*; the birch wood *B. edulis*;
  - the Scots-pine brughiera lists *B. edulis* and *B. pinophilus*; the oak-hornbeam *B.
    reticulatus*;
  - the larch wood: "Il larice è una pianta molto selettiva per la crescita di funghi", *Suillus
    grevillei* only;
  - *B. aereus* in "boschi di latifoglie di Castagno e Cerro con terreno asciutto e siliceo ... più
    raro nel Nord Italia".
- **Brescian mycologists** (`dogali2022_porcini_camonica`, `dogali2022_aestivalis_camonica`):
  - first porcini "dalla fine di maggio alla metà di giugno", mostly *B. aestivalis*;
  - *B. edulis* "specialmente nei boschi di conifere (abeti e pini) ma anche nei boschi di latifoglie
    con preferenza per faggi, meno frequente presso noccioli e castagni";
  - *B. pinophilus* "associato preferibilmente al Pino silvestre";
  - *B. aereus* "prevalentemente nei querceti e nei castagneti ... Non molto comune".
- **The Stelvio checklist** (`gm_alta_valtellina_stelvio`):
  - *B. edulis* and *B. pinophilus* in "Boschi di aghifoglie e latifoglie";
  - *B. reticulatus* in broadleaf woods only;
  - no *B. aereus*.
- **The Oltrepò** (`gmm_corso2016_habitat_lombardia`): "Boletus aereus sotto cerro", "Boletus
  aestivalis sotto castagno".

*Hosts from the neighbouring Alps* (plausible for hosts; `swissfungi_wsl`,
`mushma_swissfungi_check_2026`). The partner tree SwissFungi recorders name:

| taxon | main partners | larch |
|---|---|---|
| *B. edulis* (n=2,062) | spruce and fir 58 %, beech 24 %, oak 4 %, pines 4 % | 2 % |
| *B. pinophilus* (n=100) | pines about 48 %, spruce and fir 22 %, beech 15 % | 5 % |
| *B. reticulatus* (n=1,213) | beech 45 %, spruce and fir 27 %, oak 17 % | |
| *B. aereus* (n=88) | oak 40 %, beech 31 %, hornbeam 11 % | |

No taxon names robinia as a partner.

*Larch and stone pine* (strong for the absence of a mycorrhiza; plausible for how much spruce is
mixed in):
- **Root-tip surveys in South Tyrol** (`mandolini2024_larix`, `mandolini2022_cembra`): larch at
  1,760–1,910 m held 68 ectomycorrhizal taxa, dominated by larch specialists. The stands were
  "interspersed with Pinus cembra and Picea abies individuals", yet the article names no *Boletus*.
  Stone pine at 2,000–2,100 m held 20 taxa, again no *Boletus*.
- **Foragers** (`funghimagazine_laricino`, `funghimagazine_edulis`): "Non micorriza il Larice"; porcini
  among larches only "a patto che nelle immediate vicinanze ci siano uno o più Abeti rossi o Abeti
  bianchi (ma anche Faggi)".
- **Lombard records:** above 1,500 m the record cells are 66 % spruce and fir and 30 % larch, against
  40 % and 48 % over woodland (table above).

*Altitude* (strong out-of-region data; `treindl_leuchtmann2019`, `mushma_swissfungi_check_2026`):
- *B. edulis* is "typically associated with spruce (Picea abies) or pine (Pinus spp.) at the
  subalpine level and is rarely found above tree line".
- SwissFungi has records at 2,140 m (Castasegna, on the Valchiavenna border) and 2,210 m; p95 1,700 m,
  p99 1,858 m. WSL warns that its subalpine records are under-sampled (`waldwissen_swissfungi2018`).
- In the North, *B. aereus* is "non oltre i 500 mt ..., raramente fino a 600 mt" (`funghimagazine_aereus`,
  folklore, stricter than the records).

*Season* (plausible and folklore; `funghimagazine_calendario_autunno`,
`funghimagazine_calendario_primavera_estate`):
- ***B. edulis*, Alps:** first in August "oltre i 1400 mt e fino ed oltre i 2000 mt", and the "prime
  nevicate / gelate" end the Alpine spruce season in October. Beech and chestnut at 500–1,300 m fruit
  on, and November finds are "non oltre i 6/700m entro la metà del mese".
- ***B. pinophilus*:** in the North from late April or mid-May at 500–900 m; back in October "in ...
  Valtellina e Prealpi Lombarde, anche tra gli Abeti". "Tra le specie del genere Boletus è quella più
  precoce e più tardiva" (`gmb_trento_galleria_pinophilus`).
- **The two agree:** SwissFungi has *B. edulis* at 1,401–1,800 m from 25 July to 6 October (p5–p95)
  and below 600 m from 1 July to 2 November; *B. pinophilus* has no spring record above 1,000 m.

**Decisions** (numbers in the table above; the full reasoning is in each factor's `notes`):

- **LOM-POR-S3, *B. edulis* season: two windows blended by elevation.**
  - **Why:** the Tuscan window (full to 15 November) would keep Alpine spruce cells in season into
    December, held only by frost and snow.
  - **Alpine window:** full 1 August–25 September, closed by 25 October. The Lombard October records
    at altitude (18 %) are more than the Swiss (10 %), so it closes later than Piemonte's 20 October.
  - **Lowland window:** full 15 August–31 October, closed by 5 December (November 0.2× the effort).
  - **Handover at 900–1,300 m:** where the high beech with conifers starts ("in genere oltre i 1100
    m") and where the record months switch to the August–September shape.
- **LOM-POR-A1, *B. edulis* altitude: 100 → 400 … 1,800 → 2,200.** From the lake-slope and moraine
  chestnut ("dalla pianura alla montagna") to the subalpine spruce and larch. Below 100 m there are
  only the plain's robinia and riparian woods, non-hosts anyway.
- **LOM-POR-H1, *B. edulis* larch: 0.3 → 0.1.** In Tuscany `other_conifer` was marginal because it
  held Douglas fir, an IGP host. Here it holds only larch (89 %) and stone pine.
  - A pure larch cell now gets a third of full credit.
  - A larch cell with a quarter of spruce gets full credit.
  - 27 of the 28 records above 1,500 m keep full credit, while 30 % of woodland cells above
    1,500 m lose it. At 0.3 every woodland cell above 1,500 m was full, so the gate told the records
    nothing.
  - Kept: spruce, fir, beech and chestnut as hosts; mixed broadleaf at 0.3 (the records below
    1,000 m sit in it only a little less than the woodland does, 24 % against 32 %).
- **LOM-POR-S1, *B. reticulatus* season end: zero by 31 October.**
  - The Lombard records end on 24 September, plus one on 17 October.
  - SwissFungi October is 0.15× the effort.
  - "fino alla fine di settembre e, a volte, anche in ottobre" (Dogali).
- **LOM-POR-A3, *B. reticulatus* altitude: full to 1,250 m, zero at 1,650 m** (Emilia-Romagna's
  band). Ten of the 27 located records are at 1,000 m or higher, in beech.
- **LOM-POR-H3, *B. reticulatus* hosts: beech 0.6 → 1.0; fir/spruce and mountain pine 0.6 → 0.3.**
  - Beech: 45 % of Swiss partners, and the 1,000–1,500 m record cells are 45 % beech against 28 %.
  - Conifers: "più raro nei boschi di conifere (abeti e pini)"; "Rari gli estatini nei boschi di
    Conifere".
- **LOM-POR-S2, *B. aereus*: one window, full 15 August–15 October, zero by 20 November.** The
  Tuscan upland/lowland split came from the Apennine IGP uplands and the Tuscan macchia; Lombardia
  has neither.
- **LOM-POR-A4, *B. aereus* altitude: full to 700 m, zero at 1,100 m.** The one record at 1,077 m
  (a beech cell) falls outside; SwissFungi south of the Alps has none above 982 m.
- **LOM-POR-H4, *B. aereus* mixed broadleaf: 0.3 → 0.6**, as in the Marche: the class here is mostly
  hop-hornbeam and hornbeam, both hosts.
- **LOM-POR-S4, *B. pinophilus* season: lowland spring–autumn window and an Alpine summer window,
  blended like *B. edulis*.** Neither the Lombard (July–October) nor the Swiss records below 1,000 m
  (May to November, effort ratio 1.0–1.3 from June to October) show the Tuscan summer gap. The
  hot-summer lull in the lowlands is left to the heat and drying rules.
- **LOM-POR-A2, *B. pinophilus* altitude: 200 → 500 … 1,700 → 2,100.** It covers the Scots-pine
  heaths of the high plain (285–437 m), the spring chestnut at 500–900 m and the subalpine spruce.
- **LOM-POR-H2, *B. pinophilus* hosts: Scots pine 0.6 → 1.0; larch 0.3 → 0.1; mixed broadleaf 0.3
  → 0.1.**
  - Fir and spruce stay host: 8 of the 13 located records are at 1,000–1,500 m in cells that are 65 %
    spruce and fir.
  - The records' cells hold 2 % mixed broadleaf against 25 % of woodland.

Kept for all four: the rain, temperature and growth-clock rules and every stopper except slope
(Weather, below).

## Ovoli (*Amanita caesarea*)

**Regional and Alpine evidence.**

*Presence:*
- Regulated by name in the regional law (`lomb_lr31_2008_funghi`).
- "È presente nei boschi di latifoglie, in particolare di querce e castagni"
  (`lomb_manuale_funghi2009`).
- On the Lario, in the downy-oak and hornbeam wood "sul Monte Barro (Lc), sopra Bellagio e nella zona
  del Lago del Piano e Carlazzo" (`gm_cantu_como_ambienti2021`).
- In Valtellina it "cresce solo sotto latifoglie con decisa preferenza per il castagno e, un po'
  meno, per le querce; è più facile trovarlo su terreni silicei, ma difficilmente si sviluppa oltre i
  700-800 metri di altitudine" (`amr_martino_anzi_universoalpino`).
- The Oltrepò is a regular ovolo area ("Negli anni passati accadeva spesso di trovarne in quantità
  ... nell'Oltrepo' pavese", `funghimagazine_ovoli_2025`, folklore).

*Records:*
- **Lombard iNaturalist:** 24 records in 7 provinces, none from the Oltrepò; the records' cells are
  31 % deciduous oak and 31 % chestnut below 1,000 m.
- **SwissFungi** (`swissfungi_wsl`): 537 records, August 149, September 170, October 167, November 0;
  87 % at or below 600 m, highest 1,104 m.
- **Distribution next door:** the 13 Ticino grid cells run from the Mendrisiotto to Biasca, with none
  in the valleys that border Valtellina and Valchiavenna.
- **North-east Italian census** (`muse_censimento_caesarea`): August 33 %, September 30 %, October 24
  %; highest 1,300 m.
- **Status:** VU in Switzerland, with "einem offensichtlichen Verlust an Standorten"; nitrogen
  deposition is named as a threat "im südlichen Tessin", next to Varese and Como
  (`senn_irlet2007_rl_ch`).
- **Lag:** after July rain, summer porcini come in about two weeks and the ovolo "etwa zehn Tage
  danach" (`karasch_rlz_caesarea`). That is about a 3–4 week lag, longer than the Tuscan 8–11 days; it
  is a check for the backtest, not a rule.

**Decisions.**

| factor | Tuscany | Lombardia | why | confidence |
|---|---|---|---|---|
| season (LOM-OVO-01) | 01-06 → 01-09 … 05-11 → 30-11 | **01-06 → 01-08 … 20-10 → 15-11** | Lombard records Aug 8, Sep 7, Oct 7 (last 22 Oct), Nov 0; Swiss and NE-Alpine records alike; the June ramp kept for storm flushes (two June records) | plausible |
| altitude | … 750 → 1,100 | kept | records p90 783 m, highest 1,018 m (one find); SwissFungi highest 1,104 m; "difficilmente ... oltre i 700-800 metri"; Emilia-Romagna's zero at 1,000 m would cut the maxima | plausible |
| habitat | oak and chestnut hosts, robinia 0.05, beech 0 | kept | every Lombard source names oak and chestnut; robinia holds 11 % of the record cells' woods (hill robinia replaced chestnut and oak) but is no host; the Swiss beech partners are mixed oak-beech stands | strong (hosts) |
| weather | — | kept | no Lombard numbers | as Tuscany |

The inner Alpine valleys need no rule of their own: their woods are conifers above 1,000 m, which
the habitat and altitude gates already zero. Warm valley floors with oak or chestnut can hold the
ovolo (Trentino records in the Adige and Cembra valleys, `muse_censimento_caesarea`). In 2022 and
2025 the press reported ovoli in bassa Valtellina for the first time; see Open questions.

## Gallinacci (*Cantharellus* s.l.: "finferli", "giallini", "gallinacci")

**Regional and Alpine evidence.**

*Which chanterelles:*
- The Lombard records are mostly *C. cibarius* s.str. (88 of 146, median 1,142 m); the Mediterranean
  and oak segregates (*C. pallens*, *C. ferruginascens*) sit lower and later.
- The Milan society's three habitat types (`gm_milanese_cantharellaceae`):
  - "Mediterraneo" (*C. alborufescens*, combined from a holm-oak enclave at Brescia);
  - "Termofilo-submediterraneo (quercia, carpino, faggio appenninico)" (*C. pallens*, *C.
    ferruginascens*);
  - "Alpino-subalpino (peccio, abete bianco, pino silvestre, castagno, faggio)" (*C. cibarius*, *C.
    friesii*).
- *C. cibarius* s.str. "is broadly distributed in Europe, but not present in areas with Mediterranean
  climate" (`olariaga2017`).

*Hosts:*
- **SwissFungi** (1,696 *C. cibarius* records naming a partner): *Fagus* 878, *Picea* 593, *Abies* 422,
  *Quercus* 72, *Larix* 52, *Pinus sylvestris* 30.
- **Lombard societies:** *C. cibarius* in the spruce wood and the chestnut wood (Lario); "moltissimi
  Cantarelli" in beech (Valtellina); their larch pages name only *Suillus*.

*Altitude:*
- "dal livello del mare fino ai 2000 metri di altezza" (`amr_martino_anzi_universoalpino`).
- North-east Italian census (`muse_censimento_cantharellus`): 28 % of *C. cibarius* at 1,200–1,500 m,
  20 % at 1,500–1,800 m, highest 2,040 m.
- SwissFungi: 9.5 % at 1,601–2,000 m, highest 2,148 m.

*Season:*
- SwissFungi *C. cibarius*: June 10 %, July 27 %, August 30 %, September 21 %, October 8 %, November
  1 %.
- December flushes only "nelle isole o nelle macchie mediterranee più fresche" (`bmeteo_cantharellus`).
- The Lombard records split by elevation: July–August above 1,000 m, an October peak below 1,000 m.

**Decisions.**

| factor | Tuscany | Lombardia | why | confidence |
|---|---|---|---|---|
| lowland window (LOM-GAL-02) | 15-04 → 10-05 … 15-12 → 25-01 | **15-05 → 15-06 … 31-10 → 30-11** | no December–April record (one May record region-wide, 0.1× the effort); lowland records to 28 November | plausible |
| mountain window | 01-06 → 01-07 … 15-10 → 15-11 | **01-06 → 01-07 … 30-09 → 31-10** | records at 1,300 m and above end on 2 October; Swiss October 8 %; not cut harder, because Swiss autumn fruiting has come later since 1991 (`buntgen2013_gcb`) | plausible |
| handover | 600 → 1,000 m | **900 → 1,300 m** | the 600–1,000 m records peak in October like the lowland ones (14 of 32) | plausible |
| `season_two_flush` (disabled) | autumn to 25-01 | autumn **31-10 → 30-11** | kept in line with the main rule | folklore |
| altitude (LOM-GAL-06) | … 1,000 → 1,700 | **… 1,600 → 2,100** | records p90 1,511, p95 1,660 m; census 48 % at 1,200–1,800 m; "fino ai 2000 metri"; the subalpine woods end at 2,100–2,200 m | plausible |
| habitat (LOM-GAL-05) | beech 0.6, fir/spruce 0.6, mountain pine 0.3, larch 0.3 | **1.0, 1.0, 0.6, 0.1** | the Alpine partners; record cells enriched in spruce and fir above 1,000 m and in beech (28 % vs 9 %) and Scots pine (11 % vs 2 %) below; larch 3 % of Swiss partners, and the 15 records above 1,500 m keep full credit at 0.1 | plausible |
| habitat, other classes | chestnut 1.0, oak 0.3, mixed broadleaf 0.3 | kept | the record cells hold less oak (6 % vs 11 %) and mixed broadleaf (16 % vs 32 %) than the woodland | plausible |
| soil pH, lithology | disabled | kept disabled | see Open questions | plausible |
| weather | — | kept | "temperature moderate, comprese fra i 15 e i 24 °C" (`bmeteo_cantharellus`) fits | as Tuscany |

## Keys and groups dropped

None. Every key has Lombard records and a Lombard or Alpine source (above).
- ***B. aereus*** is thin (9 records) and absent from the Alpine valleys. Its band and windows keep
  it to the warm hills, and the porcini group takes the max over its keys, so it cannot lower the
  group.
- **Ovoli** are uncommon and regulated, but present in 7 provinces.
- **Absent habitat keys:** `macchia` and `mediterranean_pine` are absent from Lombardia and
  `evergreen_oak` is negligible. Their affinities are left as Tuscany's rather than invented; they
  cannot affect a Lombard score.

## Weather rules: why none changed

- **Rain amount and lag.** No Lombard or Alpine source gives a rain amount or lag for these taxa in
  numbers from data. The forager numbers found agree with the Tuscan rules:
  - "le prime due settimane dopo una pioggia abbondante" (3BMeteo);
  - estatini after "accumuli che non devono essere inferiori ai 30/40 millimetri" in the Alps
    (`funghimagazine_calendario_autunno`);
  - 30–40 mm for *B. aereus* (`bmeteo_aereus`).

  The rain trigger is full from 30 mm over 3 days. Karasch's 3–4 week ovolo lag
  (`karasch_rlz_caesarea`) is noted for the backtest.
- **Temperature.** The Alpine numbers fall inside the current bands:
  - maxima of "20–23 °C in media a 1.500 metri" and minima "sotto i 12 °C" in the alta Valtellina in
    August (`bmeteo_funghi_agosto2026`);
  - *B. aereus* at 15–24 °C (`bmeteo_aereus`).

  The cold of the Alps is left to the frost, snow, cold-night, air- and soil-temperature rules and
  the growth clock. They read each cell's own downscaled weather, and the new Alpine windows only
  stop the gates from staying open where those rules would otherwise do all the work.
- **Rain climate.** The Prealps get 1,400–2,300 mm a year, the inner valleys 650–900 mm.
  - The porcini 30-day rain is scored against each cell's own normal, so it adapts.
  - The absolute 30-day ramps of ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full more
    often in the Prealps and less often in Alta Valtellina. There the ovolo is absent and chanterelle
    records are few.
- **Foehn.** The press blames the dry north wind (*favonio*) for failed flushes: "LOMBARDIA E SVIZZERA
  MERIDIONALE soccombono sotto un favonio costante e maledetto" (Funghi Magazine, 4 September 2021;
  see Sanity). The ET0-based drying rules are the only stand-in, and the known gap `drying_wind`
  (gusts plus low humidity) would suit Lombardia.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted on Tuscan gauges. A check against
  ARPA Lombardia gauges is a region-config task (`regions/lombardia.md`), not a species one.

## Slope and sun exposure

- **Slope, every key.** The band moves onto the Lombard grid by the Tuscan rule: x1 up to about the
  woodland p90, x0.8 from about the maximum. Lombard woodland cells run p10 15.6°, median 27.5°,
  p75 31.7°, p90 35.1°, max 46.4°, and 63 % of them are steeper than 25°. The Tuscan band (x1 to 25°)
  would have docked 63 % of them (mean x0.95); the new one (x1 to 35°, x0.8 from 46°) docks 10 %
  (mean x0.995).
- **Sun exposure, kept.** On 15 October the woodland sun ratio runs p10 71 %, median 100 %, p90 122 %
  (below 1,000 m p10 76 %, p90 119 %), against Tuscany's p10 89 %, p90 111 %. The rule reads each
  cell's own sun, so steep north and south slopes in the Alps get the species' preference where it
  is real. The bands are ecological, not Tuscan percentiles to re-anchor.

## Sanity contrasts

`lombardia/sanity.yaml` holds 14 contrasts: 10 porcini, 2 gallinacci (`gallinacci_...`) and 2 ovoli
(`ovoli_...`). They were written down on 2026-09-26, before any Lombardia score existed.
- **Sources:** press and blog research on 2026-09-26. Every main source was opened and its quote
  checked against the page by me; the second sources were read by a research agent.
- **Areas:** 7, all ISTAT 2025 comuni, every name checked against the Lombardia grid:

  | area | comuni | woodland cells | median elevation |
  |---|---|---|---|
  | `valtellina` | 44 | 822 | 1,499 m |
  | `orobie_bergamasche` (alta Val Brembana, alta Val Seriana, Val di Scalve) | 35 | 451 | 1,230 m |
  | `valcamonica` | 28 | 462 | 1,359 m |
  | `alta_valle_staffora` (Varzi, Brallo di Pregola, Santa Margherita di Staffora, Menconico) | 4 | 156 | 886 m |
  | `oltrepo_appennino` | 12 | 273 | 721 m |
  | `varesotto_alto` (Lema, Veddasca, Valcuvia, Valganna) | 23 | 167 | 652 m |
  | `bassa_valtellina` (Colico to Sondrio, the chestnut belt) | 28 | 294 | 1,066 m |

- **"Normal":** 2017–2025. The two ovoli contrasts list their lower years by hand, leaving out 2024
  (ovoli "a chili ... persino al Nord Italia") and, for bassa Valtellina, 2022 (ovoli "persino in
  Valtellina, dove non erano mai stati segnalati prima").

| id | group | higher | lower | window | main source (second sources) | weakness |
|---|---|---|---|---|---|---|
| `valcamonica_2023_2025_2024` | porcini | Val Camonica 2023, 2025 | same, 2024 | 08-01 → 08-12 | [Giornale di Brescia 2024-08-12](https://www.giornaledibrescia.it/cronaca/fa-ancora-troppo-caldo-per-andare-a-funghi-i4d6ldtt): "I cercatori hanno ancora i cestini vuoti" (Gazzetta delle Valli 2023-08-18 "annata record"; GdB 2025-08-01 "fungo-mania", 2025-08-13 "boom di porcini sui monti bresciani") | 2024 "perlomeno fino a ora" |
| `valcamonica_2018_2017` | porcini | Val Camonica 2018 | same, 2017 | 08-01 → 08-20 | [RadioVera (Coldiretti) 2018-09-20](https://www.radiovera.net/2018/09/20/funghi-boom-di-raccolta-in-valle-camonica/): "Dopo un 2017 particolarmente negativo per gli effetti della siccità" (GdB 2018-08-07 "raccolte record ... in alta Valcamonica") | the 2017 side is one sentence written a year later |
| `orobie_2025_2022_2024` | porcini | Orobie 2025 | same, 2022 and 2024 | 08-01 → 08-12 | [Valbrembanaweb 2025-08-10](https://valbrembanaweb.com/boom-di-funghi-tesserino-obbligatorio-da-san-giovanni-bianco-fino-a-foppolo/) (Prima Bergamo 2022-08-13 "la stagione è completamente ferma"; Prima Bergamo 2024-08-08 "si soffre l'assenza di porcini") | 2025 rests on social-media photos; 2024 covers Val Seriana only |
| `orobie_2021_aug_sep` | porcini | Orobie 2021 | same year | 07-28 → 08-15 vs 09-01 → 09-15 | [L'Eco di Bergamo 2021-09-13](https://www.ecodibergamo.it/stories/premium/valle-brembana/funghi-stagione-difficile-senza-piogge-e-la-grandine-ha-rovinato-le-fioriture_1406857_11/): "la maggior parte delle fioriture ci sono state tra la fine di luglio e l'inizio di agosto" (Eco 2021-08-15) | the season gates are full on both sides above 1,300 m: a good test of the weather rules |
| `valtellina_2025_2022` | porcini | Valtellina 2025 | same, 2022 | 08-05 → 08-13 | [La Provincia di Sondrio 2022-08-10](https://www.laprovinciaunicatv.it/stories/sondrio/sondrio-e-cintura/caldo-secco-funghi-non-nascono-finora-poco-nulla-deve-piovere-o_1436362_11/): "la nascita dei funghi in provincia è stata pressoché assente" (La Provincia 2025-08-10; Italia a Tavola 2025-08-16 "quantità mai viste da anni") | different outlets for the two years |
| `valtellina_2021_aug_jul` | porcini | Valtellina 2021 | same year | 08-08 → 08-19 vs 07-20 → 08-04 | [La Provincia di Sondrio 2021-08-19](https://www.laprovinciaunicatv.it/stories/sondrio/morbegno-e-bassa-valle/sono-arrivati-funghi-e-loro-rischi-lasciate-casa-lansia-o_1404836_11/): "fino a due settimane fa ... i funghi erano 'uccel di bosco'" | one ATS mycologist; the wet July without a night-day swing tests the temperature rules, not the rain |
| `valtellina_2020_2021_sep` | porcini | Valtellina 2020 | same, 2021 | 09-01 → 09-12 | [Funghi Magazine 2020-09-21](https://funghimagazine.it/meteofunghi-21-09-2020/): "Valtellina non-stop con nascite senza sosta" (FM 2020-09-28; FM 2021-09-04 "trovare 3 o 4 funghi freschi sta diventando un'impresa") | one national bulletin; Valtellina named in long lists |
| `staffora_2021_2025` | porcini | upper Staffora 2021 | same, 2025 | 06-26 → 07-10 | [oltrepolombardo 2025-09-09](https://www.oltrepolombardo.com/2025/09/09/boom-di-funghi-in-valle-staffora-centinaia-di-persone-alla-ricerca-dei-prelibati-porcini/): "i mesi di giugno e luglio con crescite praticamente nulle" (oltrepolombardo 2021-07-03 "E' boom di funghi") | same outlet and expert; 2025 blamed on heavy rain, which a rain rule reads as favourable |
| `staffora_vs_varesotto_2025` | porcini | upper Staffora 2025 | alto Varesotto 2025 | 09-02 → 09-09 | oltrepolombardo 2025-09-09: "da qualche giorno nei boschi della nostra zona si trovano i porcini" (VareseNews 2025-09-09 "Non c'è un fungo a vista") | two climates; one Varese observer |
| `varesotto_2019_2022` | porcini | alto Varesotto 2019 | same, 2022 | 08-12 → 08-25 | [VareseNews 2022-08-26](https://www.varesenews.it/2022/08/porcini-latitanti-cronaca-stagione-particolare/1492499/): "pronosticassi potenziali buttate di porcini anche prima di ferragosto. Invano" (Luino Notizie 2019-09-17 "grosse raccolte ... fin dal 12/13 agosto") | the same observer both years; 2019 written afterwards |
| `gallinacci_valtellina_2024_2022` | gallinacci | Valtellina 2024 | same, 2022 | 07-22 → 08-04 | [La Provincia di Sondrio 2024-08-04](https://www.laprovinciaunicatv.it/stories/sondrio/valchiavenna/tanti-funghi-ma-ce-chi-mastica-amaro-o_2402540_11/): "Enormi distese di giallini ... dai 1500 metri di quota in su" (La Provincia 2022-08-10 "scarse quantità di finferli") | 2024 only above 1,500 m; "giallini" = finferli locally |
| `gallinacci_orobie_2024_2022` | gallinacci | Orobie 2024 | same, 2022 | 07-08 → 07-24 | [Prima Bergamo 2022-08-13](https://primabergamo.it/attualita/caldo-e-siccita-in-bergamasca-non-mancano-solo-i-funghi-non-ce-vita-nel-sottobosco/): "nemmeno l'ombra di porcini, finferli e chiodini" (Val Brembana forum 2024-07-20; FM 2024-07-25 "massiccia buttata di Finferli") | weak: one forum user and one bulletin line on the higher side |
| `ovoli_oltrepo_2025_normal` | ovoli | Oltrepò 2025 | same, 2017–2023 | 09-03 → 09-17 | [Funghi Magazine 2025-09-17](https://funghimagazine.it/funghi-arancioni-ovoli-reali-le-finte-uova-che-stanno-facendo-impazzire-i-social/): "Stessa cosa in Emilia Romagna e Oltrepo' pavese, anche qua panieri stracolmi" | one sentence; ovoli are regular in the Oltrepò, so the gap may be small |
| `ovoli_bassa_valtellina_2025_normal` | ovoli | bassa Valtellina 2025 | same, 2017–2021 and 2023 | 09-03 → 09-17 | same article: "Ovoli reali abbondanti o mai visti prima anche da Colico-Morbegno fino alle porte di Sondrio" | same article; the Lombard habitat for ovoli there is chestnut on the Costiera dei Cech |

**Outlets that block AI agents.** These outlets' robots.txt disallow Claude or all AI crawlers, and
none was read:
- Il Giorno;
- La Provincia Pavese and its archive;
- the Citynews network (SondrioToday, BresciaToday, LeccoToday, QuiComo, and the unreachable
  VareseToday, BergamoToday, ComoToday);
- Bresciaoggi and Gazzetta di Mantova;
- corriere.it and its local editions;
- ANSA, Il Sole 24 Ore.

The best unchecked lead is La Provincia Pavese of 2018-09-20 ("annata storica", Oltrepò 2018 against
2017), for someone to read by hand. No dated reports were found for Alto Garda, Valvestino, Val
Sabbia, Val Trompia or Iseo.

**Candidates left out:**
- Varesotto 2018 against 2017 (the same observer as `varesotto_2019_2022`);
- the Lario 2019 against 2020 (Coldiretti releases, province-wide);
- Valsassina 2024 (loosely dated);
- Val Brembana forum-only contrasts (2019 against 2020, 2018 against 2021);
- Val Brembana ticket takings (they count people, and the scheme grew);
- Val Camonica 2016 ("così così");
- region-wide Funghi Magazine statements that the calendar alone would decide.

**Year picture from the press** (context, not scored):
- **2016:** poor to mediocre.
- **2017:** drought.
- **2018:** very good (porcini from May, records in early August, an exceptional September).
- **2019:** very good from mid-August, especially in the Prealps and Orobie.
- **2020:** late and uneven, then an excellent September in Valtellina and the Orobie.
- **2021:** a short flush from late July to mid-August, then *favonio* and drought.
- **2022:** drought to mid-August, some fruiting above 1,300 m after late-August rain.
- **2023:** nothing from late June to late July, a record early August in Val Camonica, a big late
  September.
- **2024:** a wet spring, mass finferli in July, poor summer porcini, a late-August Oltrepò flush,
  abundant ovoli nationally.
- **2025:** exceptional early to mid-August porcini, then September ovoli.

## Open questions

- **Larch.**
  - *B. edulis*, *B. pinophilus* and gallinacci now give pure larch cells a third of full credit. The
    evidence is strong that larch itself is no porcini host, weaker on how much spruce the mapped
    lariceti hold.
  - The backtest and the Valtellina contrasts are the first test. If records keep turning up in
    larch-dominated cells, move back to 0.3.
  - Piemonte (region/piemonte branch) kept 0.3 and named 0.1 as the next step; the two regions
    should end on one value.
- **The Oltrepò.** The Apennine south has at most 2 records per taxon. Its rules rest on
  Emilia-Romagna's evidence next door and on the two Staffora contrasts.
- **Ovoli spreading.** Ovoli were reported in bassa Valtellina in 2022 and 2025 "dove non erano mai
  stati segnalati prima". If that continues, the habitat and the 1,100 m zero may need revisiting
  with more records.
- **Soil.** Lombard woodland topsoil is more acid (pH median 6.0) than Umbria's or the Marche's. The
  Carta forestale types name the substrate (carbonate or silicate) for most classes. The disabled
  soil-pH and lithology rules could be tested here first, especially for gallinacci:
  - *C. cibarius* is "legato a particolari condizioni di acidità del terreno" (Valtellina society);
  - half of the Lombard chestnut and three quarters of the beech are typed on carbonate rock.
- **Summer effort bias.** Alpine records come from holiday hikers in July–August (Trentino's effort
  peaks in August), which may overstate August at altitude; October effort is also lower up high.
- **Leads not read:**
  - Del Favero (2002), *I tipi forestali nella Regione Lombardia* (not online; the belts above come
    from ERSAF and the habitat manual instead);
  - Meraldi (1999), *I funghi del Parco Nazionale dello Stelvio* (book);
  - the AMB groups of Sondrio, Bergamo, Lecco, Varese and Pavia (not found);
  - Kraft (1956) on *A. caesarea* in Switzerland.
- **For the merge.** The region/piemonte branch adds Alpine references too. `funghimagazine_alberi_porcini`
  exists on both branches with different citation text, and Piemonte's `muse_censimento_cibarius`
  covers one of the pages in this branch's `muse_censimento_cantharellus`. The ids here were chosen
  not to collide.

## References added for Lombardia

| id | kind | verified | used for |
|---|---|---|---|
| `amr_martino_anzi_universoalpino` | society | verified | Valtellina: chanterelle altitude, months, soil; ovolo hosts and 700–800 m limit; larch page |
| `bmeteo_aereus` | web | verified | *B. aereus* in the Alps, temperature and rain lore (folklore) |
| `bmeteo_funghi_agosto2026` | web | verified | Alpine August temperatures for porcini (folklore) |
| `buntgen2013_gcb` | peer-reviewed | verified (abstract) | later autumn fruiting in Swiss inventories since 1991 |
| `dogali2022_aestivalis_camonica` | society | verified | *B. aestivalis* hosts and season in Brescia |
| `dogali2022_porcini_camonica` | society | verified | the four porcini's hosts and seasons in Brescia |
| `ersaf_specie_forestali2019` | institutional | verified | tree altitude belts and soils in Lombardia |
| `ersaf_stato_foreste2023` | institutional | verified | forest area and categories |
| `funghimagazine_aereus` | web | verified | *B. aereus* altitude and hosts in the North (folklore) |
| `funghimagazine_calendario_autunno` | web | verified | northern autumn porcini calendar by altitude (folklore) |
| `funghimagazine_calendario_primavera_estate` | web | verified | northern spring-summer porcini calendar (folklore) |
| `funghimagazine_edulis` | web | verified | *B. edulis* hosts, not larch (folklore) |
| `funghimagazine_laricino` | web | verified | porcini in larch woods only with spruce, fir or beech nearby (folklore) |
| `funghimagazine_ovoli_2025` | web | verified | ovoli in the Oltrepò and bassa Valtellina, 2025 (folklore) |
| `gm_alta_valtellina_stelvio` | society | verified | Stelvio checklist: porcini habitats, no *B. aereus* |
| `gm_cantu_como_ambienti2021` | society | verified | Lario habitats and their porcini, chanterelles and ovoli |
| `gm_cantu_como_schede_boletus` | society | verified | Lario species sheets for the four porcini |
| `gm_milanese_cantharellaceae` | society | verified | chanterelle segregates and their habitats |
| `gmb_trento_galleria_pinophilus` | society | verified | *B. pinophilus* and Scots pine; earliest and latest porcino |
| `gmm_corso2016_habitat_lombardia` | society | verified | Oltrepò: *B. aereus* under Turkey oak, *B. aestivalis* under chestnut |
| `infc2015_lombardia` | dataset | verified | INFC 2015 Lombardia forest categories |
| `karasch_rlz_caesarea` | institutional | verified | ovolo altitude limit, months, lag, nutrient status |
| `lomb_andreis_sartori2009` | peer-reviewed | verified | substrate split of Lombard woods |
| `lomb_arpa_clima` | institutional | verified | Lombard temperature and monthly rain regime |
| `lomb_boschi_lombardia2004` | institutional | verified | forest regions and substrates |
| `lomb_ceriani_carelli_precip` | institutional | verified | Lombard annual rain map |
| `lomb_habitat_manual2018` | institutional | verified | beech and spruce belts; larch pioneer woods |
| `lomb_lr31_2008_funghi` | institutional | verified | picking law: ovolo rule, no calendar |
| `lomb_manuale_funghi2009` | institutional | verified | ovolo hosts (oak and chestnut) |
| `lomb_masseroli2016_treeline` | peer-reviewed | verified | Upper Valtellina tree line; inner-Alpine rain |
| `mandolini2022_cembra` | peer-reviewed | verified | no *Boletus* on stone pine |
| `mandolini2024_larix` | peer-reviewed | verified | no *Boletus* on larch |
| `muse_censimento_caesarea` | society | verified | ovolo months and altitude in the north-east Alps |
| `muse_censimento_cantharellus` | society | verified | chanterelle altitude and months in the north-east Alps |
| `mushma_lombardia_forest_composition_2026` | analysis | verified | habitat shares, class contents, terrain of the Lombard grid |
| `mushma_lombardia_forest_elevation_2026` | analysis | verified | elevation of each forest category |
| `mushma_occurrence_check_lombardia_2026` | analysis | verified | Lombard record months, elevations and habitats |
| `mushma_swissfungi_check_2026` | analysis | verified | SwissFungi altitude, dates and partners |
| `parco_orobie_valt_conifere` | institutional | verified | Orobie spruce belts, larch above |
| `senn_irlet2007_rl_ch` | institutional | verified | ovolo status and nitrogen threat next door |
| `swissfungi_wsl` | dataset | verified | Swiss records of the six taxa |
| `taniguchi2007_robinia` | peer-reviewed | verified (abstract) | robinia reduces ectomycorrhizae |
| `treindl_leuchtmann2019` | peer-reviewed | verified | *B. edulis* at the tree line; Swiss records above 2,000 m |
| `waldwissen_swissfungi2018` | institutional | verified | SwissFungi under-samples the subalpine belt |

Existing references the Lombard changes lean on:
- `borgotaro_igp_rt`, `borgotaro_igp_2014`, `muse_censimento_boletus`, `iucn_pinophilus2019`,
  `micoweb_pinophilus` (porcini hosts and seasons);
- `funghimagazine_alberi_porcini`, `funghimagazine_carpino_nero2026` (hop-hornbeam and hornbeam);
- `iucn_caesarea2019`, `funghimagazine_ovolo` (ovolo range);
- `olariaga2017`, `bmeteo_cantharellus` (chanterelle segregates, climate and season);
- `mushma_occurrence_check_2026` (central Italy, for comparison).
