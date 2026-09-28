# Species ecology: Puglia (regional appendix to species-ecology.md)

Research date: 2026-09-28 (dates Europe/Rome, units metric). Card: `region-puglia-species.md`
(child of `region-puglia.md`). Rule files: `api/src/api/config/species/puglia/`. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Puglia, what
changed and why. It covers **fruiting conditions only**: nothing here is about edibility or
identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(31 added for Puglia, in one block at the end of the file, listed at the end of this page).
Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**,
**plausible**, **folklore**. Every number is a prior for the backtest; season windows, altitude bands
and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

The southern precedents are Campania, Calabria and Abruzzo, on their unmerged branches
(`region/campania`, `region/calabria`, `region/abruzzo`). [Where Puglia departs from Campania and
Calabria](#where-puglia-departs-from-campania-and-calabria) compares the three rule sets.

## Summary

1. **Five keys are kept; *B. pinophilus* is dropped.** Porcini, ovoli and gallinacci are all
   reported in Puglia, but by forager bulletins more than by records: iNaturalist holds one porcino
   (a *B. aereus* in Murge downy oak), one ovolo and four chanterelles among 2,961 Apulian fungi
   records, and GBIF nothing independent (`mushma_occurrence_check_puglia_2026`). No Puglia source or
   record names *B. pinophilus*, and Puglia lacks its hosts: no fir, 1,401 ha of black-pine plantations
   on limestone, 699 ha of chestnut. *B. edulis* is kept, on thin evidence, for the Gargano beech.
2. **Puglia is an oak region with a pine skin.** Half the woodland is deciduous oak: Turkey oak on
   the Gargano and the Monti Dauni, downy oak on the Murge, and the Macedonian oak (fragno) of the
   Murgia dei Trulli. A fifth is Aleppo pine, half of it planted. Beech is 2.7 %, chestnut 0.5 %
   (`mushma_puglia_forest_composition_2026`, `infc2015_puglia`).
3. **The fragno is a full host for the black and summer porcini and the ovolo, and a secondary one
   for the chanterelles.** No Puglia source names a key under *Quercus trojana*. It files with the
   deciduous oaks, where these keys are hosts, because it is an ectomycorrhizal oak
   (`daskalopoulos2024_trojana_tuber`) of warm, sunny, Cistus-rich woods on terra rossa
   (`puglia_manuale_tipi_forestali2025`), and because the black porcino, the chanterelle and the
   ovolo are among the commonest species of the national downy-oak records
   (`ispra2019_mlg187_flora_micologica`). The black porcini of late May and June are reported from the
   Salento and the Murge (folklore).
4. **The Gargano's low beech is a porcino and chanterelle habitat, and the altitude bands already
   reach it.** The beech sits at a median 742 m (p10 549 m), 16.5 % of it below 600 m, and the "faggete
   abissali" go down to about 250 m. The *B. edulis* band gives the beech-rich cells 0.6-1.0 and is
   kept; the chanterelles make beech a full host.
5. **The Aleppo pine hosts none of the keys.** In the nearest record tables (Calabria), none of 802
   records from Aleppo-pine plantations and 20 from natural stands is a porcino, an ovolo or a
   chanterelle; *Suillus* dominate (`ispra2018_mlg179_pino_aleppo`, `ispra2018_mlg180_pino_aleppo`),
   as they do among the Apulian iNaturalist records. `mediterranean_pine` becomes a non-host for *B.
   aereus* and the chanterelles.
6. **The southern season: early, broken by summer, long.** The summer porcino is reported from late
   April, the black porcino and the chanterelles from May; July and August bring 6-11 % of the year's
   rain; the autumn peaks in November and runs to January at low altitude. Four windows move:
   *B. reticulatus* opens a fortnight earlier, *B. aereus*'s lowland window runs from mid-May to 10
   January, the chanterelles' mountain window opens in mid-May and their lowland one in mid-March.
7. **Weather rules are all Tuscany's.** No Puglia study ties fruiting to rain or temperature in
   numbers. The forager lore agrees with the Tuscan rules: a 30 mm storm in a heat wave gave a short
   flush in 2025, and dry east winds "annullando l'effetto delle piogge" is what the drying stopper
   does. One new known gap records the fog and dew that keep the Gargano beech alive.
8. **Evidence is the thinnest of any region so far.** Puglia has no regional mycological checklist,
   atlas or record table online. Of the 31 new sources, all opened:
   - 1 is peer-reviewed (the fragno ectomycorrhiza) and 1 a vegetation chapter of the Università di
     Bari.
   - 9 are institutional (the picking law, two park acts, the regional forest-type manual, the ASL
     Bari season, the UNESCO beech page, three ISPRA manuals).
   - 2 are datasets (INFC 2015, the regional rain annals) and 2 our own analyses.
   - 16 are forager, magazine or food-blog pages (folklore), 14 of them Funghi Magazine bulletins.

## Puglia in brief

**Woods.** The region card maps Puglia's woods from Regione Puglia's Carta dei Tipi Forestali (ARIF
and the Università di Bari, DGR 1279/2022, FRA 2000 definition; `config/regions/puglia.yaml`, written
in parallel). The rules were drafted before the woodland grid existed, so the shares and heights below
come from the map itself (`mushma_puglia_forest_composition_2026`):
- exact polygon areas per ISTAT 2025 comune and province;
- heights from Copernicus GLO-30 on a 100 m lattice;
- approximate 1 km woodland cells built from the same lattice: a cell counts when broadleaf and
  conifer woods cover half of it. 1,106 cells qualify, holding 55 % of the woodland; Puglia's woods
  are that fragmented.

The map has 205,362 ha of woods, macchia and scrub under a habitat key, 147,173 ha of it broadleaf or
conifer woodland. INFC 2015 gives a bosco of 142,349 ha (`infc2015_puglia`), 3.4 % less.

This table is **which habitat holds which Puglia tree**:

| habitat key | share of woods and scrub (of woodland) | Puglia forest types (map codes, area) | median elevation (p10-p90) |
|---|---|---|---|
| `deciduous_oak` | 36.3 % (50.6 %) | Turkey oak CE1-CE4, CE9 (31,935 ha); **Macedonian oak (fragno)** CE7 mesic soils (20,559 ha) and CE6 xeric soils (1,250 ha); downy oak QU1-QU5 (20,754 ha); vallonea CE8 (6 ha) | 467 m (323-795); fragno 393 m, max 520; downy oak 442 m; Turkey oak 657 m, max 1,132 |
| `macchia` | 17.6 % | wild olive and lentisk MM1 (79 %), wild-olive woods AB1-AB2, coastal and dune macchia, garigue, *Quercus coccifera* MM3 (1 %), Phoenician juniper | 189 m (17-411) |
| `mediterranean_pine` | 15.6 % (21.8 %) | Aleppo pine: reforestation, coastal PA1 (3,499 ha) and inland PA6 (12,579 ha, the Alta Murgia 5,956); natural or secondary, with lentisk PA2, with holm oak PA3, on cliffs and gravine PA5, PA7 (14,911 ha); cypress and stone pine BC1 (1,125 ha) | 234 m (12-566) |
| `transitional_woodland_shrub` | 10.7 % | blackthorn AR1 (47 %), *Paliurus* pseudo-macchia AR4 (21 %), wooded pastures 3140 (17 %), broom AR2 (14 %), tamarisk and willow scrub BI3 | 460 m (126-772) |
| `evergreen_oak` | 8.7 % (12.1 %) | holm oak LE1-LE8 (17,798 ha); cork oak SU1 (78 ha, Brindisi) | 386 m (91-661) |
| `mixed_broadleaf` | 6.1 % (8.5 %) | young woods of elm, manna ash, maple and cherry on abandoned fields BN2 (53 %); hop-hornbeam and *Carpinus orientalis* OS1-OS5 (45 %); maple and aspen | 586 m (320-813) |
| `beech` | 1.95 % (2.7 %) | FA2 with holly and yew (2,453 ha), FA4 with Turkey oak (1,070), FA3 "faggete abissali" (341), FA1 with hornbeam (146) | 742 m (549-802), 261-992 |
| `riparian` | 1.9 % (2.6 %) | willow and poplar galleries BI1 (3,690 ha), elm and southern ash BI2, maple and southern ash BI5 | 183 m |
| `mountain_pine` | 0.7 % (1.0 %) | black and laricio pine plantations PM1 (1,401 ha; Monti Dauni 971, Gargano 426) | 854 m (681-1,009) |
| `chestnut` | 0.34 % (0.5 %) | chestnut CA1 (699 ha; San Marco in Lamis 342, Vico del Gargano 122, Monte Sant'Angelo 85) | 658 m (435-796) |
| `other_conifer` | 0.14 % | montane reforestation with other conifers BC2 (283 ha) | 607 m |

The map has no mixed broadleaf-conifer class, so `mixed_broadleaf_conifer` is empty in Puglia; nor
does Puglia have fir, spruce or exotic broadleaf woods (`fir_spruce`, `exotic_broadleaf`).

Where the woods are:
- **Foggia holds 62 % of the woodland**: the Gargano (651 of the 1,106 woodland cells) and the Monti
  Dauni (157).
- **Beech, chestnut and black pine are only in the province of Foggia.** 99 % of the beech is on the
  Gargano: Monte Sant'Angelo 1,951 ha, Vieste 907, Vico del Gargano 860, Ischitella 202. The Monti
  Dauni hold 37 ha, at Roseto Valfortore and Faeto.
- **The fragno is 82 % in the Murgia dei Trulli** and 58 % in the province of Taranto: Martina Franca
  5,567 ha, Mottola 4,662, Noci 2,725, Gioia del Colle 1,839, Laterza 1,692.
- **The Aleppo pine** is natural or old on the Gargano coast (Vieste 5,005 ha, Peschici, Vico,
  Mattinata) and planted inland on the Murge (Altamura 1,100 ha, Gravina 1,029, Cassano delle Murge
  927, Minervino Murge 829) and on the Ionian coast (Castellaneta, Palagiano).
- **The Salento** holds 7 woodland cells: its woods are holm-oak relicts, 78 ha of cork oak at
  Brindisi, macchia and coastal pine.

INFC 2015 (`infc2015_puglia`) has the same picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| Turkey oak, farnetto, fragno, vallonea | 38,728 | 27.2 % |
| Mediterranean pines | 27,718 | 19.5 % |
| downy, sessile and pedunculate oak | 25,865 | 18.2 % |
| holm oak | 17,364 | 12.2 % |
| other deciduous | 11,538 | 8.1 % |
| other evergreen broadleaves | 5,150 | 3.6 % |
| beech | 4,661 (ES 28.6 %) | 3.3 % |
| hop-hornbeam and hornbeam | 4,661 | 3.3 % |
| other conifers | 2,331 | 1.6 % |
| black pines | 1,554 | 1.1 % |
| chestnut | 1,165 (ES 57.5 %) | 0.8 % |
| hygrophilous | 388 | 0.3 % |
| cork oak, fir, spruce, larch | 0 | 0 % |

**Altitude belts.** Puglia's highest point is 1,152 m; the approximate woodland cells have a median of
492 m (p10 248 m, p90 789 m) and 36 % of them are above 600 m.

| type | altitude (m) and where | source |
|---|---|---|
| beech | FA2, "la faggeta submontana più diffusa ... (es. Foresta Umbra nel Gargano, tra 600 e 1000 m s.l.m.)"; the "faggete abissali" "arrivando fino a circa 250 m s.l.m.", in the forre of the Bosco di Ischitella e Carpino; on the Monti Dauni only "modestissimi nuclei" at Roseto Valfortore and Faeto; the map: median 742 m, 16.5 % below 600 m | `puglia_manuale_tipi_forestali2025`, `mushma_puglia_forest_composition_2026` |
| why the beech is low | "nella parte orientale dell'altopiano ... il Cerro è sostituito dal Faggio come a Foresta Umbra e Bosco Sfilzi"; beech replaces Turkey oak "nelle aree in cui l'aridità estiva viene periodicamente compensata da precipitazioni occulte notturne"; sea winds that "condensano l'umidità sotto forma di piogge o nebbie" | `macchia2000_vegetazione_clima_puglia`, `puglia_manuale_tipi_forestali2025` |
| Turkey oak | the Monti Dauni and the Gargano plateau "da 600 ad oltre 800 m di quota"; the Monti Dauni's most widespread wood; map median 657 m, top 1,132 m | `macchia2000_vegetazione_clima_puglia`, `puglia_manuale_tipi_forestali2025` |
| downy oak | the NW Murge, the Foggia plain, the Monti Dauni flanks to 500-600 m and the Gargano at 400-850 m; absent from the top of the Alta Murgia, where steppe grassland takes over; map median 442 m | `macchia2000_vegetazione_clima_puglia` |
| fragno | the SE Murge: "Turi, Castellana, Locorotondo, Martina Franca, Ceglie Messapico, Mottola, Castellaneta, Santeramo in Colle e Acquaviva delle Fonti", "quasi totalmente degradati a pascoli arborati"; map 310-470 m, none above 520 m | `macchia2000_vegetazione_clima_puglia`, `mushma_puglia_forest_composition_2026` |
| holm oak | the Brindisi-Lecce plain (Rauccio), the Gargano at 150-400 m, the escarpments of the SE Murge | `macchia2000_vegetazione_clima_puglia` |
| Aleppo pine | coasts, cliffs and gravine; 20th-century reforestation "ben oltre la sua potenziale distribuzione autoctona" | `puglia_manuale_tipi_forestali2025` |
| black pine | 1960s plantations of the Gargano and the Sub-Appennino Dauno, "tendente alla monocoltura"; map median 854 m | `puglia_manuale_tipi_forestali2025` |

Puglia's belts are the southern Apennine ones squeezed down. The Gargano beech (median 742 m) sits
about 470 m below Campania's (1,211 m) and 530 m below Calabria's (1,270 m), at the height of
Campania's chestnut (658 m), and no wood reaches 1,200 m.

**Substrate.** "Il substrato pugliese è costituito in prevalenza da rocce carbonatiche": Jurassic
limestone on the Gargano, Cretaceous limestone on the Murge, calcarenite in the Salento. On them lie
the terre rosse, "generalmente decarbonatati nei livelli superficiali" (`puglia_manuale_tipi_forestali2025`).
The regional manual gives the beech soils a "reazione chimica neutra o leggermente basica", the
fragno woods "neutro-subacidofili", and calls the chestnut "spiccatamente acidofilo", so it keeps to
acid pockets of the Foresta Umbra. Limestone is the ground a forager magazine blames for *B. edulis*
being rarer in the Centre-South (folklore, quoted in the Campania appendix).

**Climate.** Puglia is dry, and wettest in its woods. Rain at the Protezione Civile stations, means
over the complete years of 1991-2020 (`pcpuglia_annali_pioggia_mensile`; heights from GLO-30):

| station | height | year (mm) | July + August (mm, share) | September-November share | wettest month |
|---|---|---|---|---|---|
| Bosco Umbra (Foresta Umbra) | 779 m | 1,151 | 101 (8.7 %) | 30.6 % | December |
| San Marco in Lamis (Gargano) | 554 m | 993 | 81 (8.2 %) | 32.2 % | September (December over the full record) |
| Vico del Gargano | 452 m | 967 | 78 (8.1 %) | 33.3 % | December |
| Monte Sant'Angelo (Gargano) | 792 m | 712 | 59 (8.2 %) | 34.1 % | November |
| Faeto (Monti Dauni) | 802 m | 949 | 91 (9.6 %) | 28.4 % | November |
| Orsara di Puglia (Monti Dauni) | 690 m | 860 | 83 (9.6 %) | 27.6 % | November |
| Martina Franca (fragno, 1994-2020) | 448 m | 883 | 65 (7.3 %) | 32.9 % | November |
| Noci (fragno) | 411 m | 702 | 63 (9.0 %) | 31.9 % | November |
| Mercadante (Alta Murgia pine) | 399 m | 667 | 52 (7.8 %) | 31.3 % | November |
| Altamura (Alta Murgia) | 468 m | 602 | 60 (10.0 %) | 29.7 % | November |
| Castellaneta (Arco ionico) | 231 m | 599 | 45 (7.5 %) | 35.6 % | November |
| Lecce (Salento) | 44 m | 655 | 43 (6.5 %) | 37.3 % | November |
| Foggia (Tavoliere) | 76 m | 488 | 45 (9.2 %) | 30.4 % | November |

- The Gargano park gives the same range, from "550 mm of annual rainfall" on the coast to "1,200 mm in
  Foresta Umbra" (`faggetevetuste_gargano`).
- **The summer is dry but not rainless.** July and August bring 6-11 % of the year, 40-100 mm, against
  4-8 % in Campania and 3-4 % in the Sila. Summer storms reach the Gargano and the Monti Dauni.
- **Autumn is the wet season,** a third of the year in September-November, with November (December on
  the Gargano) the wettest month.

**Regional law.** L.R. 25 agosto 2003, n. 12 (`lr_puglia_12_2003`), in force, as amended by L.R.
14/2006, L.R. 3/2012 and L.R. 35/2020.
- **Quantity and permit.** 3 kg per person a day, over the age of 14, with a regional permit issued
  by the comune after a 12-hour course (art. 2-3); 10 kg with a professional permit. The consolidated
  text renews the permit every five years. There is no separate ovolo limit, unlike Campania's 1 kg.
- **Size.** "È vietata la raccolta dell'Amanita Caesarea allo stato d'ovolo chiuso e di tutti gli
  ovoli chiusi appartenenti allo stesso genere". Caps under 3 cm are banned; "Cantharellus (tutte le
  specie)" may be picked from 2 cm (art. 2).
- **Days and hours.** "tutti i giorni della settimana" since 2006 (the 2003 text allowed only even
  days and Sundays), but not "dopo il tramonto e fino alle ore sette" (art. 2 c. 9).
- **Places.** Banned, "salvo diversa disposizione dei competenti organismi di gestione", in nature
  reserves and in the areas of national parks and regional reserves that their bodies identify (art.
  5). The Gargano park's founding decree allows "la raccolta di funghi, tartufi ed altri prodotti del
  bosco, nel rispetto delle vigenti normative, degli usi civici e consuetudini locali"
  (`pn_gargano_dpr1995`). The Alta Murgia park's draft regulation allows it under the regional law but
  bans it "nelle aree oggetto di imboschimento" and for twelve months after a fire
  (`pn_altamurgia_regolamento2015`; no record of its approval was found).
- **Poor years and rare species.** The Region may ban species "in pericolo di estinzione" for limited
  periods (art. 5 c. 9).
- **What it leaves out.** No season calendar and no altitude rule. The ASL Bari's mycological control
  service plans for a season "dal 1° settembre al 31 gennaio di ogni anno"
  (`asl_bari_ispettorato_micologico`), cardoncelli included. None of this changes where or when the
  fungi fruit; the law confirms the ovolo and the chanterelles as regional species.

## The Macedonian oak and the Murge's downy oak

This was the card's first question: which keys fruit under the fragno (*Quercus trojana*, about 22,000
ha) and in the Murge's downy oak.

**What is known.** Little, and none of it names the fragno.
- **No Puglia source or record** names a porcino, the ovolo or a chanterelle under *Q. trojana*.
  iNaturalist has 44 located fungi records in fragno woods, none of them a key
  (`mushma_occurrence_check_puglia_2026`); Puglia has no regional checklist or record table like
  Calabria's.
- **The fragno is an ectomycorrhizal oak.** In pot trials it formed ectomycorrhizae with *Tuber
  aestivum* at 45-87 % colonisation (`daskalopoulos2024_trojana_tuber`, strong for that pairing,
  plausible for the keys). Nothing suggests it partners with fewer fungi than the other oaks.
- **Its woods are warm, sunny oak woods.** The regional manual describes them as "mesoxerofili
  neutro-subacidofili", with Cistus, lentisk, Phillyrea and Viburnum tinus in the shrub layer and a
  "chiaro carattere termofilo", "spesso degradati a pascoli alberati e macchie"
  (`puglia_manuale_tipi_forestali2025`). That is the habitat the black porcino and the ovolo prefer.
- **Nationally, the keys are among the commonest species of the downy-oak records.** Of 1,072
  downy-oak records (324 species), *B. aereus* is 1.81 % and *C. cibarius* 1.81 %, second only to
  *Armillaria tabescens* (1.90 %); the ovolo is 1.24 %. The chanterelle "ha, in questa tipologia di
  boschi, un picco di frequenza ... rispetto ad altri tipi di copertura arborea del suolo". *B. edulis*
  and *B. reticulatus* are not among the frequent species (`ispra2019_mlg187_flora_micologica`).
- **The one Apulian porcino record** is a *B. aereus* in typical downy oak in the Murge, September 2016,
  435 m (`mushma_occurrence_check_puglia_2026`).
- **The forager bulletins** find the first black porcini "in Salento e nelle Murge" in early June 2023,
  the summer porcini "sporadici tra Murge, Daunia e Gargano", and chanterelles "per lo più"
  (`funghimagazine_aggiornamento_2023_06_02`, folklore).

**Verdict.** The fragno files with `deciduous_oak`, as the region card maps it (CE6, CE7) and as INFC
counts it. For each key:

| key | `deciduous_oak` affinity | reading for the fragno and the Murge downy oak | confidence |
|---|---|---|---|
| *B. aereus* | 1.0 (host) | the black porcino of the warm oak woods; the only Apulian record; national downy-oak share 1.81 % | plausible |
| *B. reticulatus* | 1.0 (host) | "sporadici tra Murge, Daunia e Gargano"; an oak and chestnut porcino everywhere | plausible (weak) |
| ovolo | 1.0 (host) | national downy-oak share 1.24 %; thermophilous, of sunny oak woods | plausible |
| chanterelles | 0.6 (secondary, from 0.3) | the national downy-oak peak; abundant in Puglia in May-June 2023 | plausible |
| *B. edulis* | 0.3 (marginal, kept) | not among the frequent downy-oak species; the altitude band keeps it off the Murge anyway | plausible |

The fragno's cells (the Murgia dei Trulli, 141 cells) keep full habitat and altitude credit for *B.
aereus*, the ovolo and the chanterelles under both rule sets (`mushma_puglia_forest_composition_2026`).
The backtest cannot check it: there are no records there.

## The Gargano's low beech

The card's second question: is *B. edulis* in the Gargano's low beech, and at what height and season?

**The beech.** 4,011 ha, 99 % on the Gargano, median 742 m. The main type (FA2, 2,453 ha) is the
Foresta Umbra's at 600-1,000 m; the "faggete abissali" (FA3, 341 ha) of the Ischitella and Carpino
ravines go down to about 250 m (map minimum 261 m, median 534 m) by thermal inversion and sea fog.
Its soils are deep, fresh and neutral to slightly basic (`puglia_manuale_tipi_forestali2025`,
`mushma_puglia_forest_composition_2026`). It lives on 1,000-1,200 mm of rain, the most in Puglia
(`faggetevetuste_gargano`, `pcpuglia_annali_pioggia_mensile`).

**Which porcino.** Unknown in Puglia.
- No Puglia source or record names *B. edulis*. The one forager page that names Gargano porcini says
  "soprattutto Boletus aereus e B. reticulatus" (`myboletus_puglia`, folklore); the bulletins speak of
  summer porcini "sporadici tra Murge, Daunia e Gargano" (`funghimagazine_aggiornamento_2023_06_02`).
- iNaturalist has 75 located fungi records in the Gargano beech (FA2) and no porcino among them
  (`mushma_occurrence_check_puglia_2026`). Porcini are picked more than photographed; this is not a
  proof of absence.
- Nationally *B. edulis* is the commonest species of the beech records (2.1 %), with *B. reticulatus*
  and *B. pinophilus* at 1.0 % (`ispra2019_mlg187_flora_micologica`).

**Verdict.** *B. edulis* is kept, with beech and chestnut as its hosts and Tuscany's altitude band (0
at 200 m, full from 700 m). The band already reaches the beech: the cells that are at least 30 % beech
lie at 494-805 m, median 732 m, where it gives 0.6-1.0, and the mean habitat × altitude over them is
0.93. Only the abyssal beech of the ravines loses most of it. Lowering the band would also open the
Murge oak (median 393-442 m) to *B. edulis*, since deciduous oak's marginal 0.3 saturates the habitat
gate in a pure oak cell. Confidence is plausible for the habitat and weak for the presence.

**When.** No Puglia source dates a beech porcino. The Gargano's season is autumn: "il picco autunnale
arriva tipicamente a novembre, a volte fino a dicembre" (`myboletus_puglia`); the chanterelles grow
"principalmente nei boschi di faggio e quercia" (`sedicipuglia_galletto2024`), from May on the
Gargano (`funghimagazine_nascite_2026_05_08`).
The *B. edulis* window (full September to mid-November, to 20 December) is kept.

**The chanterelles and the beech.** Beech becomes a full chanterelle host (from 0.6), as in Campania,
Calabria and Abruzzo: *C. cibarius* is 1.8 % of the national beech records
(`ispra2019_mlg187_flora_micologica`) and the Puglia blog names "boschi di faggio e quercia" first.

**A known gap.** The Gargano beech depends on fog and dew the reanalysis rain does not see; see
[Weather rules](#weather-rules-why-none-changed).

## The Aleppo pine

The card's third question: does the Aleppo pine (the region's second woodland, 30,988 ha on the map)
host any of the keys, or only *Lactarius* and *Suillus*?

**Only other fungi, as far as any record shows.**
- **It is mostly planted.** "L'attuale massiccia diffusione di Pinus halepensis nella regione è
  prevalentemente attribuibile a massicci interventi antropici"; its native presence in Puglia "rimane
  dubbia e comunque fosse storicamente molto limitata" (`puglia_manuale_tipi_forestali2025`). On the map
  16,077 ha are reforestation (PA1 coastal, PA6 inland); 14,911 ha are natural or secondary stands on
  the Gargano coast, the cliffs and the gravine.
- **The nearest record tables have no key.** In Calabria, 802 records from Aleppo-pine plantations
  (227 species) are led by *Suillus collinitus* 7.1 %, *S. bellinii* 6.1 % and *S. mediterraneensis*
  5 %, with *Lactarius sanguifluus* 2.3 %; the only boletes are *B. erythropus* and *B. fragrans*
  (`ispra2018_mlg179_pino_aleppo`). The 20 records of natural Aleppo pine (the Pistacio-Pinetum
  halepensis the Puglia manual names for the Gargano and the Tremiti) are *Peziza*, *Geopora* and
  *Suillus* (`ispra2018_mlg180_pino_aleppo`). The national dune-pine records have no porcino, ovolo or
  chanterelle among their frequent species (`ispra2019_mlg187_flora_micologica`).
- **The Apulian records agree.** iNaturalist has 238 located fungi records in Aleppo pine and none of
  the keys; *Suillus* are the commonest ectomycorrhizal genus of the Apulian records (62, *S.
  collinitus* 21) (`mushma_occurrence_check_puglia_2026`).
- **The press.** "Il Salento è un'esplosione di funghi nelle pinete litoranee" after the October 2018
  storms, next to the black porcini of the region's oak (`funghimagazine_aggiornamento_2018_10_22`);
  the bulletin does not say the pinewood fungi were porcini.

**Verdict.** `mediterranean_pine` goes to non-host 0.1 for *B. aereus* (Tuscany 0.6, for a pine with an
Erica understorey) and the chanterelles (Tuscany 0.3, for maritime pine), as in Calabria; it was
already 0.1 for *B. edulis*, *B. reticulatus* and the ovolo. A pure Aleppo-pine cell keeps a third of
full habitat credit; a cell mixed with oak keeps full credit through the oak.

## Where Puglia departs from Campania and Calabria

All three rule sets start from the same Tuscan files.

| factor | Tuscany | Campania | Calabria | Puglia | why Puglia |
|---|---|---|---|---|---|
| *B. pinophilus* | kept | kept | kept | **dropped** | no record or source; no fir, black pine only as 1,401 ha of plantations on limestone |
| `beech` for *B. reticulatus* | 0.6 | 1.0 | 1.0 | **0.6** | the Puglia beech is low (742 m); the south's summer porcino of the high beech belt has no belt to climb |
| *B. reticulatus* altitude | 0 → 150 … 1,100 → 1,500 | 1,600 → 1,900 | 1,600 → 1,900 | **full from sea level** … 1,100 → 1,500 | the first finds are coastal ("lungo i litorali") |
| *B. reticulatus* window start | 1 May → 1 Jun | kept | kept | **15 Apr → 15 May** | first Puglia finds in late April and early May |
| *B. reticulatus* window end | 15 Nov | kept | 15 Dec | kept | no late Puglia report |
| `macchia` for *B. aereus* | 1.0 | 1.0 | 0.3 | 0.3 | olive and lentisk, as Calabria's lentisk and Cytisus |
| `mediterranean_pine` for *B. aereus*, chanterelles | 0.6, 0.3 | kept | 0.1, 0.1 | 0.1, 0.1 | Aleppo pine, no record (the Calabrian tables) |
| `mixed_broadleaf` for *B. aereus* | 0.3 | 0.6 | 0.1 | 0.3 | hop-hornbeam and invasion woods, neither Campania's hornbeam-chestnut mix nor Calabria's *Alnus cordata* |
| `mixed_broadleaf` for *B. reticulatus* | 0.6 | 0.6 | 0.3 | 0.3 | invasion woods and hop-hornbeam, little hazel |
| `mountain_pine` for *B. edulis*, *B. reticulatus* | 0.6 | 0.6 | 0.1 | **0.3** | 1960s black-pine plantations (as Abruzzo) |
| `macchia` for the ovolo and the chanterelles | 0.3 | 0.3 | 0.3 | **0.1** | olive-lentisk macchia, almost no Fagaceae in it |
| `evergreen_oak` for the ovolo | 0.6 | 0.6 | 1.0 | 0.6 | no Puglia evidence to match Calabria's cork-oak shares; 78 ha of cork oak |
| `beech`, `deciduous_oak` for the chanterelles | 0.6, 0.3 | 1.0, 0.6 | 1.0, 0.6 | 1.0, 0.6 | same move |
| *B. aereus* windows | upland 15 Jun, lowland 1 Jul → 15 Dec; handover 400-600 m | lowland to 10 Jan; 600-800 m | both from 15 May; upland to 30 Nov | **lowland 15 May → 10 Jan, upland Tuscany's; 600-800 m** | May finds are lowland (Salento, Murge); the Gargano plateau and Monti Dauni keep the upland window |
| *B. aereus*, ovolo altitude | 800 → 1,250; 750 → 1,100 | kept | 1,000 → 1,350 both | kept | hosts no higher than in Tuscany; the bands cover 91 % and 85 % of cells |
| *B. edulis* altitude, window | 200 → 700 … 1,600 → 1,900; from 1 Jul | 1,800 → 2,000 | 1,800 → 2,000; from 1 Jun | kept | no wood above 1,152 m; no early Puglia *B. edulis* |
| chanterelle mountain window | from 1 Jun | from 15 May | from 15 May | from 15 May | same move |
| chanterelle lowland window | 15 Apr → 10 May … 15 Dec → 25 Jan | kept | kept | **15 Mar → 15 Apr** … 15 Dec → 25 Jan | late-winter finds in the Salento and on the Gargano |
| chanterelle altitude | 1,000 → 1,700 | 1,400 → 1,900 | 1,500 → 1,900 | kept | full on 99.7 % of cells |

In short: Campania and Calabria moved bands up to follow high hosts; Puglia's hosts are low, so it
moves none up and opens one down. It shares Calabria's reading of the Mediterranean classes (lentisk
macchia and Aleppo pine are not hosts) and goes further for the ovolo and the chanterelles, because
its macchia is olive and lentisk almost throughout.

## The southern season

The card asked about spring and early-summer flushes, the summer drought, and an autumn from October
into December or later. Each verdict rests on Puglia's evidence, which is almost all forager lore.

1. **Early flushes: yes, for the summer porcino, the black porcino and the chanterelles.**
   - *B. reticulatus*: "i primi timidi Porcini estivi ... anche in Puglia ... qualche segnalazione
     arriva dal Tarantino e dal Foggiano" on 26 April 2025 (`funghimagazine_nascite_2025_04_26`); "In
     Puglia si sono già registrati i primissimi ritrovamenti" on 9 May 2025, first "lungo i litorali"
     (`funghimagazine_nascite_2025_05_09`); once "precocissimi in ... Puglia"
     (`funghimagazine_nascite_2026_04_23`).
   - *B. aereus*: the first of 2019 "Dal Salento ... in boschi di Leccio-Sughera-Quercia" by 31 May
     (`funghimagazine_boletus_gallery2019`); "in Salento e nelle Murge" in early June 2023
     (`funghimagazine_aggiornamento_2023_06_02`); expected "in Salento-Gargano" in early May 2026
     (`funghimagazine_nascite_2026_05_08`).
   - Chanterelles: "sporadici Galletti" in the Salento and on the Gargano in mid-March 2024
     (`funghimagazine_aggiornamento_2024_03_14`); "persino di Galletti/Finferli nella Macchia
     Mediterranea" after a rainy April 2023 (`funghimagazine_meteofunghi_2023_04_28`); "per lo più
     Finferli" in Puglia on 2 June 2023, "abbondano più che mai" in Puglia-Basilicata by mid-June
     (`funghimagazine_aggiornamento_2023_06_16`); the first of 2026 "in zone assolate del Salento, ma
     anche nel Gargano" by 8 May.
   - What changed: *B. reticulatus* opens on 15 April (full 15 May), *B. aereus*'s lowland window on 15
     May (full 15 June), the chanterelles' mountain window on 15 May and their lowland window on 15
     March (full 15 April).
2. **A summer drought gap: yes, broken by storms. The weather makes it.**
   - July and August bring 6-11 % of the year's rain, 40-60 mm on the Murge and the coasts and about
     100 mm in the Foresta Umbra (`pcpuglia_annali_pioggia_mensile`).
   - Storms still give flushes: "Porcini neri e Ovoli reali spuntati in Puglia" in late August 2025
     (`funghimagazine_nascite_2025_08_22`), after 30 mm fell "nel cuore di una bolla africana"
     (`funghimagazine_buttata_record_2025`).
   - Dry east winds are the Puglia forager's enemy: "correnti secche e persistenti che disidratano il
     terreno, annullando l'effetto delle piogge" (`funghimagazine_nascite_2025_05_09`), which the
     Tuscan drying stopper (ET0) already does.
   - As in Tuscany, Campania and Calabria, no calendar gap is written in. The porcini's 30-day rain is
     scored against each cell's own normal, so it adapts to Puglia's dry summer; the ovolo and
     chanterelle 30-day ramps are absolute and will seldom be full in a Puglia July.
3. **A later autumn at low altitude: yes.**
   - The autumn is the wet season (a third of the year's rain in September-November) and peaks
     "tipicamente a novembre, a volte fino a dicembre" (`myboletus_puglia`); "Le nascite di Neri ...
     non si contano tra ... Puglia" in late October 2018 (`funghimagazine_aggiornamento_2018_10_22`).
   - The ASL Bari plans its mycological service to 31 January (`asl_bari_ispettorato_micologico`).
   - Two of the four Apulian chanterelle records are from December and January
     (`mushma_occurrence_check_puglia_2026`); "tra Salento, coste joniche ed isole, è ancora possibile
     trovare anche i più classici Cantharellus cibarius" at Christmas 2022
     (`funghimagazine_natale_2022_12_21`), and "Puglia (tutta dov'è piovuto durante gli ultimi 15
     giorni)" is among the places for chanterelles in January 2024
     (`funghimagazine_aggiornamento_2024_01_12`).
   - The autumn comes late and from the north-west: the bulletins expect it "dapprima sul Gargano e
     Daunia poi anche nelle Murge e resto della regione", with the Salento last (see the sanity
     contrasts).
   - What changed: *B. aereus*'s lowland window is full to 30 November and ends on 10 January, as in
     Campania and Calabria. The chanterelles' lowland window already ran to 25 January, *B. edulis*'s
     to 20 December. Frost and snow end it on the Gargano plateau and the Monti Dauni.
4. **The cardoncello season is not the porcini season.** *Pleurotus eryngii* (out of scope) is the
   region's commonest recorded edible: 55 iNaturalist records, all October-April, none in May-September,
   mostly on the coastal Tavoliere with no wood within 500 m (`mushma_occurrence_check_puglia_2026`). Its
   folk calendars and the ASL's autumn-to-January service follow it, not the porcini.

## Occurrence cross-check (Puglia)

Queried 2026-09-28 (`mushma_occurrence_check_puglia_2026`):
- **iNaturalist**: place 13069 ("Apulia, IT"), verifiable records. Elevations come from Copernicus
  GLO-30 (not the Open-Meteo elevation API the earlier regions used), for open, non-obscured records
  with an accuracy of 1 km or better, deduplicated by observer, day and 1 km cell.
- **Habitat**: the Carta dei Tipi Forestali type at and within 500 m of each located record.
- **GBIF**: `gadmGid=ITA.2_1`, soil-DNA `MATERIAL_SAMPLE` rows excluded, and records without
  coordinates by stateProvince.
- Aggregates only; no coordinates are stored.

Puglia has 2,961 iNaturalist fungi records (Campania 4,437, Calabria 3,053, Tuscany 19,089) from 488
observers, 91 % since 2020; a third of them are lichens. The effort peaks in November-December.

| taxon | iNat n | months | located: height, habitat |
|---|---|---|---|
| *B. edulis* | 0 | | |
| *B. reticulatus* | 0 | | |
| *B. aereus* | 1 | September (2016) | 435 m, typical downy oak (QU1), the Murge |
| *B. pinophilus* | 0 | | |
| *A. caesarea* | 1 | October (2015) | the Gargano, accuracy 7.8 km (nominally a Turkey-oak polygon at about 708 m) |
| *Cantharellus* | 4 | October 2, December 1, January 1 | 3-537 m; the Murgia dei Trulli, the Monti Dauni, the Salento |
| *Pleurotus eryngii* (context) | 55 | October-April | mostly below 100 m on the Tavoliere |
| all fungi (share, %) | 2,961 | J 10, F 9, M 4, A 10, M 6, J 3, J 4, A 5, S 6, O 11, N 18, D 15 | median 328 m |

The chanterelles are *C. cibarius* 3 and 1 at genus level. GBIF has no porcino; its ovolo, chanterelle
and cardoncello records are iNaturalist copies, and its 2,249 georeferenced Apulian fungi are mostly
lichen herbarium specimens. No Università di Bari dataset holds the keys.

What the records show:
- **Nothing to tune on.** One porcino in 2,961 fungi records. The sightings backtest will have almost
  no Puglia presences; Puglia's rules are as good as the evidence behind them and no better.
- **The absence is not only an absence of observers.** 75 located fungi records fall in the Gargano
  beech, 44 in fragno woods, 238 in Aleppo pine and 236 in deciduous oak, with none of the keys but the
  one *B. aereus*. Porcini are rare in Puglia, rarely photographed, or both.
- **The neighbours add little.** Basilicata and Molise have 2 *B. edulis*, 2 *B. reticulatus*, 1 *B.
  aereus*, 1 ovolo and 2 *C. cibarius* on iNaturalist. The southern mainland pool of the Campania
  appendix (mostly Calabria) is the comparison: *B. aereus* median 415 m (n=6), ovolo 328 m (7),
  *Cantharellus* 414 m (25).

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*)

**Regional evidence** beyond what is above:
- **Which porcino** (folklore). The forager bulletins name the black porcino ("Porcini Neri") and the
  summer porcino ("Porcini estivi", *B. reticulatus*) in Puglia and nothing else; the one forager
  page on the Gargano says "soprattutto Boletus aereus e B. reticulatus" and "La Murgia e i boschi della
  Daunia offrono ambienti di querceto con Boletus aereus" (`myboletus_puglia`).
- **Where** (folklore). The Salento's holm and cork oak, the Murge, the Daunia and the Gargano; first
  near the coast, where "il mare mitiga e ammorbidisce gli estremi" (`funghimagazine_nascite_2025_05_09`).
- **Weather** (folklore). A 30 mm storm in a heat wave gave a short, big flush in late August 2025;
  drying east winds undo rain; "non servono nubifragi da 100 mm ... meglio boschi costantemente umidi
  che allagati" (`funghimagazine_nascite_2025_08_22`).

**Decisions.**

| key | factor | Tuscany | Puglia | why | confidence |
|---|---|---|---|---|---|
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | hop-hornbeam and *C. orientalis* on limestone, elm, ash and maple on old fields | plausible |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | blackthorn, *Paliurus*, broom, wooded pastures | plausible |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.3** | 1960s black-pine plantations on limestone, no Puglia report (as Abruzzo) | plausible (weak) |
| *edulis* | known gap `occult_precipitation` | — | **new** | the Gargano beech's fog and dew | plausible |
| *reticulatus* | season | 1 May → 1 Jun … 30 Sep → 15 Nov | **15 Apr → 15 May** … 30 Sep → 15 Nov | first Puglia finds in late April and early May | folklore |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | **open** … 1,100 → 1,500 | first finds "lungo i litorali"; 8 % of cells below 200 m | folklore |
| *reticulatus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub`, `mountain_pine` | 0.6 | **0.3** | few hosts in each (above) | plausible |
| *aereus* | season | upland 15 Jun → 1 Aug … 30 Sep → 31 Oct; lowland 1 Jul → 1 Sep … 15 Nov → 15 Dec; handover 400-600 m | upland kept; lowland **15 May → 15 Jun … 30 Nov → 10 Jan**; handover **600-800 m** | May-June finds in the Salento and the Murge; November-December peak; ASL season to January | folklore |
| *aereus* | habitat `macchia` | 1.0 | **0.3** | wild olive and lentisk, not Cistus-Arbutus-Erica | plausible |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn and broom scrub; wooded pastures keep it above 0.1 | plausible |
| *aereus* | habitat `mediterranean_pine` | 0.6 | **0.1** | Aleppo pine: no porcino in 822 Calabrian records | plausible |
| all three | weather, stoppers, growth clock | — | kept | no Puglia numbers; the lore agrees | as Tuscany |

Kept on purpose:
- ***B. edulis*'s altitude band and `deciduous_oak` 0.3.** See [The Gargano's low
  beech](#the-garganos-low-beech).
- **`beech` 0.6 for *B. reticulatus* and 0.1 for *B. aereus*.** No Puglia source ties either to the
  beech; the Gargano beech is mixed with Turkey oak (FA4) and hornbeam, which carry them.
- ***B. aereus* in evergreen oak (1.0)**: "boschi di Leccio-Sughera-Quercia" in the Salento.
- ***B. aereus*'s altitude band** (full to 800 m, 0 at 1,250 m): full over 91 % of the cells.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.** The picking law bans the closed ovolo (`lr_puglia_12_2003`, art. 2). "Porcini neri e
  Ovoli reali spuntati in Puglia" in late August 2025 (`funghimagazine_nascite_2025_08_22`, folklore);
  ovoli in the Gargano's woods (`myboletus_puglia`, folklore); one iNaturalist record, Gargano, October
  2015.
- **Hosts.** No Puglia source names one. Nationally the ovolo is 1.24 % of the downy-oak records
  (`ispra2019_mlg187_flora_micologica`).
- **Season and height.** No Puglia source; the record is from October.

**Decisions.**

| factor | Tuscany | Puglia | why | confidence |
|---|---|---|---|---|
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | blackthorn, *Paliurus* and broom scrub, not heath and clearings with scattered oaks; the Murge's wooded pastures keep it at 0.3 | plausible |
| habitat `macchia` | 0.3 | **0.1** | olive and lentisk: the scattered holm and cork oak that gave Tuscany's macchia its credit are rare in it | plausible |
| habitat deciduous oak (fragno included) and chestnut 1.0, evergreen oak 0.6 | — | kept | national downy-oak share; sunny, warm oak woods | plausible to strong (hosts) |
| season 1 Jun → 1 Sep … 5 Nov → 30 Nov | — | kept | late-August 2025 flush; October record; no early or late Puglia date | plausible |
| altitude … 750 → 1,100 | — | kept | full on 85 % of cells; thins only over the Turkey oak above 750 m | plausible |
| weather rules | — | kept | a storm in a heat wave fits the Tuscan soil-temperature and drying rules | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "galletti", "finferli")

**Regional evidence.**
- **Frequency.** The group best reported in spring: "per lo più Finferli" in Puglia in early June 2023
  (`funghimagazine_aggiornamento_2023_06_02`), "abbondano più che mai" by mid-June
  (`funghimagazine_aggiornamento_2023_06_16`); the first of 2026 in the sunny Salento and on the Gargano
  by 8 May (`funghimagazine_nascite_2026_05_08`). All folklore.
- **Hosts.** "principalmente nei boschi di faggio e quercia, in particolare nel Parco Nazionale del
  Gargano e nella Foresta Umbra", "anche nei boschi misti del Subappennino Daunio e dell'Alta Murgia"
  (`sedicipuglia_galletto2024`, folklore). Nationally *C. cibarius* is 1.81 % of the downy-oak records
  (its peak), 1.8 % of the beech and 0.9 % of the holm-oak records (`ispra2019_mlg187_flora_micologica`).
  None is among 822 Calabrian Aleppo-pine records.
- **Which species.** The four Apulian records are *C. cibarius* (3) and one at genus level. No Puglia
  source records *C. pallens* or *C. alborufescens*; the holm-oak segregates are not excluded.
- **Records.** October to January, 3-537 m.
- **Winter and early spring** (folklore). Chanterelles in the Salento's macchia and coastal woods at
  Christmas 2022 (`funghimagazine_natale_2022_12_21`) and across Puglia in January 2024
  (`funghimagazine_aggiornamento_2024_01_12`); "sporadici Galletti" in the Salento and on the Gargano
  in mid-March 2024 (`funghimagazine_aggiornamento_2024_03_14`); in the macchia in April 2023
  (`funghimagazine_meteofunghi_2023_04_28`).

**Decisions.**

| factor | Tuscany | Puglia | why | confidence |
|---|---|---|---|---|
| season: lowland window | 15 Apr → 10 May … 15 Dec → 25 Jan | **15 Mar → 15 Apr** … 15 Dec → 25 Jan | chanterelles in March 2024 and April 2023 in the Salento, on the Gargano and in the macchia; the temperature and rain rules keep a cold or dry March at zero | folklore |
| season: mountain window | 1 Jun → 1 Jul … 15 Oct → 15 Nov | **15 May → 15 Jun** … 15 Oct → 15 Nov | May-June 2023 abundance; first 2026 finds on the Gargano by 8 May | plausible (folklore sources) |
| habitat `beech` | 0.6 | **1.0** | 1.8 % of the national beech records; "boschi di faggio e quercia" | plausible |
| habitat `deciduous_oak` | 0.3 | **0.6** | the national downy-oak peak; the Murge's oak on decalcified terra rossa, not Tuscany's calcicolous plots | plausible |
| habitat `mediterranean_pine` | 0.3 | **0.1** | Aleppo pine: none in the Calabrian tables | plausible |
| habitat `mountain_pine` | 0.3 | **0.1** | black-pine plantations on limestone (as the Marche and Calabria) | plausible (weak) |
| habitat `macchia` | 0.3 | **0.1** | olive and lentisk, no Fagaceae host | plausible |
| habitat `transitional_woodland_shrub` | 0.3 | **0.1** | thorn and broom scrub (as Campania, Abruzzo) | plausible |
| chestnut, evergreen oak 1.0; lowland window end (25 Jan); altitude | — | kept | records and reports to January; the band is full on 99.7 % of cells | plausible |
| soil pH, lithology | disabled | kept disabled | the acid-soil preference is better read from the hosts on Puglia's limestone | plausible |
| weather rules | — | kept | no Puglia numbers | as Tuscany |

## Weather rules: why none changed

- **Rain amount and lag.** No Puglia source gives an amount or lag in numbers. The one amount in the
  lore, a 30 mm storm that set off a short flush in a heat wave (`funghimagazine_buttata_record_2025`),
  sits at the top of the Tuscan 10 → 30 mm ramp.
- **Drying.** "correnti secche e persistenti che disidratano il terreno, annullando l'effetto delle
  piogge" (`funghimagazine_nascite_2025_05_09`) is the Tuscan drying stopper, driven by ET0, which
  includes wind.
- **Summer drought.** The porcini's 30-day rain adapts, being a percentage of the cell's normal; the
  ovolo and chanterelle ramps are absolute.
- **Fog and dew** (new known gap, `occult_precipitation` on *B. edulis*). The Gargano beech exists
  because summer drought "viene periodicamente compensata da precipitazioni occulte notturne"
  (`macchia2000_vegetazione_clima_puglia`) and sea winds "condensano l'umidità sotto forma di piogge o
  nebbie" (`puglia_manuale_tipi_forestali2025`). Neither is in the reanalysis rain. "spesso la rugiada
  notturna fa più miracoli di un temporale violento" (`funghimagazine_nascite_2025_08_22`, folklore).
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it is a
  region-card task (`regions/puglia.md`). The Protezione Civile's annals (`pcpuglia_annali_pioggia_mensile`)
  give open monthly totals to 2020 at 164 stations, including the Foresta Umbra (Bosco Umbra, 779 m,
  1,151 mm); see Open questions.

## Groups and keys

**Dropped: *B. pinophilus*.** No Apulian record on iNaturalist or GBIF, and no Puglia source names it
(`mushma_occurrence_check_puglia_2026`). Its hosts are not here:
- In Italy it is a porcino of beech, fir and chestnut in cool, humid mountains, and in Calabria of the
  Sila's laricio pine (Tuscany's POR-H2; Calabria's appendix).
- Puglia has no fir. Its black and laricio pine is 1,401 ha of 1960s plantations on limestone
  (`puglia_manuale_tipi_forestali2025`); the Marche and Abruzzo gave their own black-pine plantations
  on limestone 0.3 for it, because it wants "terreni molto acidi".
- Its chestnut is 699 ha; its beech is low (median 742 m), below the Tuscan band's full credit (800 m).
- A mycological association of Santeramo in Colle shows a *B. pinophilus* photograph in its gallery
  (https://www.associazionemicologicaamamto.it/), with no place or date; that is not a record.
- If it fruits in Puglia at all, it is in the Gargano beech, which *B. edulis* already covers.

The porcini group keeps three keys (*B. edulis*, *B. reticulatus*, *B. aereus*), in the shared
tie-break order. `mixed_broadleaf_conifer`, `fir_spruce` and `exotic_broadleaf` are not on the Puglia
map but stay in the rule files, as in every region; they score no cell.

## Effect on the woodland cells

On the 1,106 approximate woodland cells (`mushma_puglia_forest_composition_2026`):

| key | habitat gate full: Tuscany → Puglia | altitude gate full: Tuscany → Puglia | mean habitat × altitude: Tuscany → Puglia |
|---|---|---|---|
| *B. edulis* | 46.5 % → 18.5 % | 21.8 % → 21.8 % | 0.52 → 0.46 |
| *B. reticulatus* | 78.1 % → 76.5 % | 94.0 % → 100 % | 0.89 → 0.90 |
| *B. aereus* | 97.2 % → 81.2 % | 91.0 % → 91.0 % | 0.97 → 0.89 |
| ovolo | 80.9 % → 79.7 % | 85.1 % → 85.1 % | 0.86 → 0.85 |
| chanterelles | 94.5 % → 80.4 % | 99.7 % → 99.7 % | 1.00 → 0.90 |

What the table shows:
- **The porcini group loses the Aleppo pine and nothing else.** The best porcino's habitat × altitude
  is 0.5 or more on 88.8 % of cells (Tuscan rules 99.9 %). The 124 cells below are all dominated by
  Aleppo pine (123) or riparian woods (1).
- **The oak country is untouched.** On the 624 cells dominated by deciduous oak and the 141 of the
  Murgia dei Trulli, *B. aereus*, *B. reticulatus*, the ovolo and the chanterelles keep mean gates of
  0.95-1.00.
- **The beech keeps its porcini.** On the 52 cells that are at least 30 % beech, *B. edulis* averages
  0.93 and *B. reticulatus* and the chanterelles 1.00.
- **Why *B. edulis*'s habitat gate fell.** Cells mixing deciduous oak with hop-hornbeam, invasion woods
  or scrub lose the marginal credit those classes gave; its altitude band keeps it off most of them
  anyway.

## Sanity contrasts

`puglia/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written down
on 2026-09-28, before any Puglia score existed.

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_`. "Normal" is the area's mean over 2017-2025.

**Areas.** Every comune was checked against the ISTAT 2025 list (COD_REG 16, 257 comuni): all 72
names are in Puglia. ISTAT spells it "San Nicandro Garganico", not "Sannicandro"; the other spelling
would silently match nothing.
- `puglia`: the whole region.
- `gargano`: 14 comuni of the promontory, Vico del Gargano to Manfredonia.
- `monti_dauni`: 25 comuni, the card's 22 plus Panni, Castelnuovo della Daunia and Rocchetta
  Sant'Antonio.
- `gargano_dauni`: the two together, for bulletins that name "Gargano e Daunia".
- `arco_ionico`: Ginosa, Laterza, Castellaneta, Palagianello, Mottola, Massafra and Putignano, as the
  2021 bulletin draws it.
- `murge`: 23 comuni, the Alta Murgia and the south-eastern Murge.
- `salento`: provinces LE and BR, less the Murge comuni of Brindisi (Fasano, Cisternino, Ceglie
  Messapica, Ostuni, Villa Castelli).
- `murge_taranto_salento`: provinces TA, LE and BR plus the south-eastern Murge comuni of Bari.

**The sources are thin, and all from one magazine.**
- Puglia's local press never gives a dated verdict on a porcini, ovoli or chanterelle season. It
  reports cardoncelli (out of scope, and never used as evidence here), picking courses, lost pickers
  and giant finds.
- All 13 contrasts rest on Funghi Magazine's national bulletins, whose Puglia lines come from readers'
  reports. They are usually one sentence, often region-wide or about "il Foggiano", and they sometimes
  contradict each other. Most contrasts draw on 2-4 bulletins.
- The live site refuses scripts, so the bulletins were read through Wayback Machine captures. The
  research agent read 211 of them and every quote was re-checked against the extracted text; ten
  were checked again here.
- Dates are the bulletins' publication dates, which can be a day off the date in the page's address.
- No source covers 2016-2017: the bulletins' Puglia lines start in 2018.

There are 13 contrasts: 10 porcini, 1 ovoli and 2 gallinacci. FM is Funghi Magazine; each main
source links a Wayback capture.

| id | group | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|---|
| `puglia_early_june_2020_vs_2018_2021` | porcini (summer) | Puglia 2020, 1-15 Jun | Puglia 2018 and 2021 | [FM 2020-06-11](https://web.archive.org/web/20200929073545/https://funghimagazine.it/aggiornamento-funghi-11-giugno-2020/): summer porcini "in Puglia anche sotto Querce isolate o nelle Pinete litoranee" (FM 2020-05-22; FM 2018-06-16: "Puglia insolitamente ferma ... la Foresta Umbra sembra poltrire"; FM 2021-06-24: "ha bloccato sul nascere ogni tentativo di avvio di stagione") | 2020 rests on one clause; region-wide |
| `gargano_dauni_early_august_2020_vs_2021_2023_2025` | porcini (summer) | Gargano and Monti Dauni 2020, 1-18 Aug | same, 2021, 2023, 2025 | [FM 2020-08-14](https://web.archive.org/web/20200926054742/https://funghimagazine.it/aggiornamento-meteofunghi-14-08-2020/): "Ultime nascite per il Gargano, Bosco di Lucerna e Sub-Appennino Dauno" (FM 2020-07-23: "ottime nascite attese a brevissimo"; FM 2021-08-19: "non dovrebbero aver innescato alcuna nascita"; FM 2023-08-17; FM 2025-08-08: "troppo isolate e post-caldo africano") | the 2020 side is partly forecast and "ultime"; the lower sides are mostly region-wide |
| `gargano_dauni_late_august_2022_vs_2023` | porcini | Gargano and Monti Dauni 2022, 20 Aug-5 Sep | same, 2023 | [FM 2022-08-26](https://web.archive.org/web/20220826073117/https://funghimagazine.it/nuovo-boom-di-porcini/): "7) EMILIA ROMAGNA, LIGURIA e PUGLIA, limitatamente al Gargano e Daunia" (FM 2022-09-05; FM 2023-08-24: "Assenza di nascite tra Molise-Puglia e Basilicata non tirrenica") | Puglia 7th in a national ranking; the 2023 side is region-wide |
| `arco_ionico_early_september_2021_vs_2019` | porcini (summer) | Arco ionico 2021, 31 Aug-12 Sep | same, 2019 | [FM 2021-09-04](https://web.archive.org/web/20210922081914/https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): "una ottima buttata di Porcini estivi ... fin su parte del Tarantino di Ginosa-Laterza-Massafra fin su Putignano" (FM 2021-09-10; FM 2019-09-05: "lunghissimo periodo siccitoso e ben torrido"; FM 2019-09-20: "nascite ancora modeste o del tutto assenti") | the 2021 flush is described from the Basilicata side and spills into Puglia |
| `gargano_vs_monti_dauni_september_2021` | porcini | Gargano 2021, 8-22 Sep | Monti Dauni, same window | [FM 2021-09-24](https://web.archive.org/web/20211024074056/https://funghimagazine.it/aggiornamento-meteofunghi-24-09-2021-funghi-porcini-situazione-italia/): "La timida buttata del Gargano ... mentre nel resto della Puglia non sono segnalati che pochi Galletti e Russule" (FM 2021-09-04: "E' andata però meglio sul Gargano") | a "timida" flush; the Dauni side is "il resto della Puglia" |
| `gargano_vs_monti_dauni_october_2020` | porcini | Gargano 2020, 10-23 Oct | Monti Dauni, same window | [FM 2020-10-23](https://web.archive.org/web/20201204163307/https://funghimagazine.it/meteofunghi-23-10-2020/): "Stesso discorso per il Foggiano, con maggior presenza di funghi autunnali in Gargano, rispetto al Sub-Appennino Dauno" | "funghi autunnali", not porcini by name; one line |
| `murge_vs_salento_october_2020` | porcini | Murge 2020, 10-23 Oct | Salento, same window | FM 2020-10-23 (same page): in the Murge "tra le querce, anche isolate, là dove si mantiene l'umidità al riparo dal vento, anche funghi Porcini"; "Salento spesso sferzato dal vento, con nascite ridotte al lumicino" | the Murge sentence starts with cardoncelli; one bulletin; the Salento has 7 woodland cells |
| `puglia_autumn_2018_vs_2021_2023` | porcini | Puglia 2018, 15 Oct-10 Nov | Puglia 2021 and 2023 | [FM 2018-10-22](https://web.archive.org/web/20190723060659/https://funghimagazine.it/aggiornamento-funghi-22-ottobre-2018/): "Le nascite di Neri e moltissimi altri funghi autunnali non si contano tra ... Basilicata e Puglia" (FM 2018-11-10, 2018-11-16: "oltre ai Bronzini aereus abbondano"; FM 2021-10-24: "colpo di grazia, soprattutto in Murgia e Salento"; FM 2021-11-19: "Porcini sono scarsini"; FM 2023-10-27: "nascite quasi non pervenute") | region-wide; 2018 lumps in other fungi |
| `murge_taranto_salento_late_october_2022_vs_2021_2023` | porcini | south-eastern Murge, TA, LE, BR 2022, 20 Oct-5 Nov | same, 2021 and 2023 | [FM 2022-11-05](https://web.archive.org/web/20221129141843/https://funghimagazine.it/aggiornamento-porcini-06-11-2022/): "La Puglia sta sperimentando un buon periodo di nascite sia di Porcini che di Cardoncelli, soprattutto sui settori Est delle Murge, nel Tarantino e Salento" (FM 2022-10-28; FM 2021-10-24, 2021-11-19; FM 2023-10-27, 2023-11-09) | cardoncelli in the same sentence; overlaps the previous contrast's years |
| `puglia_2025_timing_august` | porcini | Puglia 2025, 14-26 Aug | same year, 10 Jul-8 Aug | [FM 2025-08-21](https://web.archive.org/web/20250822194753/https://funghimagazine.it/aggiornamento-nascite-funghi-22-08-2025/): "Porcini neri e Ovoli reali spuntati in Puglia, Molise e Sicilia interna" (FM 2025-09-04: "una buttata mordi-e-fuggi clamorosa. Breve, certo, ma memorabile"; FM 2025-07-17: "Situazione molto difficile"; FM 2025-08-08) | where in Puglia is unknown; a short flush; dates inferred |
| `ovoli_puglia_2025_timing_august` | ovoli | Puglia 2025, 14-26 Aug | same year, 10 Jul-8 Aug | FM 2025-08-21, the same line | a presence line, not a verdict on the year; the ovolo's season gate rises between the two windows |
| `gallinacci_puglia_spring_2023_normal` | gallinacci | Puglia 2023, 20 May-16 Jun | same, normal | [FM 2023-06-15](https://web.archive.org/web/20230703082634/https://funghimagazine.it/aggiornamento-funghi-16-06-2023/): "Puglia-Basilicata dove, però di contro abbondano più che mai Finferli/Galletti" (FM 2023-05-25: "in Puglia spiccano i Finferli/Galletti"; FM 2023-06-01; FM 2023-04-27) | region-wide; "più che mai" is rhetoric; normal includes 2023 |
| `gallinacci_puglia_december_2023_normal` | gallinacci | Puglia 2023, 8-22 Dec | same, normal | [FM 2023-12-16](https://web.archive.org/web/20231216111000/https://funghimagazine.it/aggiornamento-funghi-16-12-2023/): "tra Lazio, Campania e Puglia si stanno trovando ancora i più estivi Cantharellus cibarius e Cantharellus pallens!" (FM 2023-12-22: "tranne la Puglia, che ha avuto un buon incremento di nascite fungine") | the lowland window is on its down-ramp after 15 December; normal includes 2023 |

**Outlets that block AI agents** (robots.txt, not fetched): FoggiaToday, BariToday, TarantoToday and
BrindisiReport (the Today network), LeccePrima, Quotidiano di Puglia and ANSA block Claude agents by
name; ilgargano.it, Norba Online, Telerama and parks.it block every agent. LecceToday did not
resolve, Corriere di Taranto returns 403 on robots.txt, Brindisi Libera and quisalento sit behind a
captcha, and funghiitaliani.it's forum returns 403. Coldiretti's sites return 404 on robots.txt and
were not used, as in Campania.

Candidates left out:
- **Puglia's normal September against September 2019**: Puglia's normal September is itself poor.
- **September 2020**: "Situazione pessima ... poche buttatine di rapidissima durata, soprattutto
  nella Foresta Umbra" (FM 2020-09-21); no clean higher side.
- **Late May 2024 against 2023, and September 2024**: the bulletins contradict themselves (a Gargano
  flush in May 2024, then "Per la prima volta da inizio anno si è finalmente trovato qualche Porcino
  anche in Puglia" on 27 September).
- **Spring 2025**: the May and June bulletins are not archived, and a paraphrase of the live pages
  cannot be checked word for word.
- **Forecasts**: early September 2025, the Dauno in September 2019, November 2024.
- **Chanterelles in November 2021**: no lower side.
- **Local press**: a 2019 picking course, lost pickers in 2018 and 2021, Coldiretti pieces from
  2005-2006.

**Year picture from the sources** (context, not scored):
- **2016-2017:** no source.
- **2018:** a quiet June ("insolitamente ferma"); a very strong October-November, black porcini "non
  si contano", the Salento's pinewoods "un'esplosione", the Gargano "a tappeto".
- **2019:** a few black porcini in the Salento and the Murge in late May and early July; heat in
  August; September "modeste o del tutto assenti".
- **2020:** summer porcini in early June; storm flushes on the Gargano, the Monti Dauni and the Murge
  from late July to mid-August; a "pessima" September; porcini among the Murge oaks in October, the
  Gargano ahead of the Dauno, the Salento "al lumicino".
- **2021:** June blocked by dry wind; an August drought; an early-September flush on the Arco ionico;
  a timid Gargano flush; October-November "scarsini".
- **2022:** summer porcini "localmente" in late May; the Gargano and Daunia in late August; a good
  late October in the eastern Murge, the Tarantino and the Salento.
- **2023:** a rainy spring and chanterelles "più che mai" in May-June; no porcini through summer and
  autumn; a "strepitoso" December for chanterelles.
- **2024:** a flush on the Gargano and the Murge in late May; June heat; almost nothing until late
  September.
- **2025:** timid summer porcini in the Tarantino and the Foggiano in April-May; a dry July; a short
  mid-August burst of black porcini and ovoli.

What the bulletins add for the rules (folklore, not cited in the rule files):
- **The autumn arrives from the north-west and ends in the Salento.** Births "potrebbero partire
  dapprima sul Gargano e Daunia poi anche nelle Murge e resto della regione" (FM 2021-10-14); "Le
  nascite si assottigliranno però a breve, tranne che in Salento" (FM 2022-11-05). Coldiretti hoped to
  start the season "da metà ottobre" in 2020 (AGI, 2020-09-13).
- **Heat and wind stop fruiting.** "Oltre i 30° le nascite fungine diventano progressivamente più
  improbabili" (FM 2024-07-11); "il vento di Tramontana o Grecale ha dato il colpo di grazia" (FM
  2021-10-24); porcini "là dove si mantiene l'umidità al riparo dal vento" (FM 2020-10-23). The Tuscan
  heat and drying (ET0) stoppers carry both; see Open questions on wind.

## Places, for the intro copy

Sourced areas:
- **Porcini:** the Gargano's Foresta Umbra and its Turkey oak (the black and summer porcini); the
  Monti Dauni (the Daunia); the Murge and the Macedonian-oak woods of the Murgia dei Trulli (Martina
  Franca, Mottola, Noci); the holm and cork oak of the Salento, where the first black porcini of the
  year are found.
- **Ovoli:** the Gargano; late-summer flushes after storms.
- **Gallinacci:** the Gargano beech and oak, the Monti Dauni, the Alta Murgia; the Salento's macchia and
  coastal woods from late autumn to January and again from March.
- **Seasons:** the summer porcino from late April, the black porcino and the chanterelles from May and
  June; summer storms; the main season from October to December, running into January at low altitude.
- **Not in the app:** the Murge's cardoncello, October to April.

## Open questions and hand-offs

- **Rain scale and gauges** (for the region card). The Protezione Civile Puglia publishes open monthly
  totals to 2020 for 164 stations (`pcpuglia_annali_pioggia_mensile`); the region card has since
  checked the reanalysis against them (`mushma_puglia_gauge_check_2026`, `regions/puglia.md`). The woods
  sit at the rainy end of the region: the Foresta Umbra (1,151 mm), the Gargano's north side (Vico 967
  mm, San Marco in Lamis 993 mm) and the Monti Dauni (Faeto 949 mm) against 488 mm at Foggia, so a coarse
  reanalysis cell over the Gargano mixes the 550 mm coast with the 1,200 mm forest.
- **Wind.** Three bulletins name dry north and north-east winds (Tramontana, Grecale) as what ends a
  Puglia flush, in the Murge and the Salento above all. The drying stopper reads ET0, which includes
  wind but also sun and heat. The ingest already fetches `wind_speed_10m_max`, which no rule reads yet;
  a wind stopper for the backtest to try would be a model-wide change, not a Puglia one.
- **Fog on the Gargano.** The beech's water comes partly as fog and dew
  (`macchia2000_vegetazione_clima_puglia`); the rain rules will read the Foresta Umbra as drier than it
  is. Recorded as the known gap `occult_precipitation`.
- **Slope and sun exposure.** Both stoppers are anchored on Tuscan grid percentiles; check them on the
  Puglia grid once built. The Murge are gentle and the Gargano's ravines steep.
- **Fragmentation.** Only 55 % of the woodland falls in cells that are half wooded
  (`mushma_puglia_forest_composition_2026`); a 25 ha threshold would take 79 %. If the grid keeps the
  half-wooded mask, much of the fragno (the xeric stands are small: "la maggior parte di essi non
  supera il mezzo ettaro", `puglia_manuale_tipi_forestali2025`) and of the Salento's woods will not be
  scored.
- ***B. edulis* in Puglia.** Kept for the Gargano beech on national evidence only. A dated Gargano find,
  or a local mycological group's list, would settle it; so would a regional checklist, which Puglia
  lacks.
- **The fragno.** No record anywhere ties a key to *Q. trojana*. The North Macedonian checklist of
  basidiomycetes (macfungi.com) lists *Quercetum trojanae* woods as habitats of other species but gives
  no habitat for the porcini, ovolo or chanterelle; a survey of those woods, or of the Murge's, would
  settle it.
- **Chanterelle species.** Puglia's are *C. cibarius* on the records. The holm-oak segregates are not
  documented, but a bulletin names *C. pallens* with *C. cibarius* in "Lazio, Campania e Puglia" in
  December 2023 (the sanity contrasts) and a Santeramo association's gallery shows *C. alborufescens*.
  Evergreen oak stays a full host on the Tuscan evidence.
- **Leads not read.** The Parco nazionale dell'Alta Murgia's current regulation (only the 2015 draft
  was found); the Gargano park's mushroom rules beyond the 1995 safeguard measures; the AMB groups of
  Foggia, Bari and Taranto (no public species lists found); Francini (1953), *Il pino d'Aleppo in
  Puglia*.

## References added for Puglia

| id | kind | verified | used for |
|---|---|---|---|
| `lr_puglia_12_2003` | institutional | verified | the picking law in force |
| `pn_gargano_dpr1995` | institutional | verified | picking allowed in the Gargano park |
| `pn_altamurgia_regolamento2015` | institutional | verified | Alta Murgia draft rules: no picking in plantations and burnt areas |
| `ispra2019_mlg187_flora_micologica` | institutional | verified | national record shares in downy oak, beech, holm oak and dune pines |
| `ispra2018_mlg179_pino_aleppo` | institutional | verified | no key in 802 Calabrian Aleppo-pine plantation records |
| `ispra2018_mlg180_pino_aleppo` | institutional | verified | no key in the natural Aleppo-pine records |
| `daskalopoulos2024_trojana_tuber` | peer-reviewed | verified | the fragno is an ectomycorrhizal host |
| `macchia2000_vegetazione_clima_puglia` | monograph | verified | vegetation belts; beech and fog |
| `puglia_manuale_tipi_forestali2025` | institutional | verified | the forest types: belts, soils, origins |
| `infc2015_puglia` | dataset | verified | forest area and categories |
| `pcpuglia_annali_pioggia_mensile` | dataset | verified | monthly rain at the stations, 1991-2020 |
| `faggetevetuste_gargano` | institutional | verified | Foresta Umbra area and rain |
| `asl_bari_ispettorato_micologico` | institutional | verified | the ASL season, September to January |
| `funghimagazine_boletus_gallery2019` | web | verified | first black porcini in the Salento, May 2019 (folklore) |
| `funghimagazine_aggiornamento_2018_10_22` | web | verified | October black porcini; the Salento's pinewood fungi (folklore) |
| `funghimagazine_aggiornamento_2023_06_02` | web | verified | black porcini in the Salento and the Murge, summer porcini on the Gargano, chanterelles, June 2023 (folklore) |
| `funghimagazine_aggiornamento_2023_06_16` | web | verified | chanterelles abundant in Puglia-Basilicata, June 2023 (folklore) |
| `funghimagazine_nascite_2025_04_26` | web | verified | first summer porcini, late April 2025 (folklore) |
| `funghimagazine_nascite_2025_05_09` | web | verified | first finds on the coast; drying east winds (folklore) |
| `funghimagazine_nascite_2025_08_22` | web | verified | black porcini and ovoli, late August 2025 (folklore) |
| `funghimagazine_buttata_record_2025` | web | verified | a short flush after 30 mm in a heat wave, 2025 (folklore) |
| `funghimagazine_nascite_2026_04_23` | web | verified | the summer porcino once very early in Puglia (folklore) |
| `funghimagazine_nascite_2026_05_08` | web | verified | first black porcini and chanterelles on the Gargano and in the Salento, May 2026 (folklore) |
| `funghimagazine_natale_2022_12_21` | web | verified | *C. cibarius* in the Salento at Christmas 2022 (folklore) |
| `funghimagazine_meteofunghi_2023_04_28` | web | verified | chanterelles in the Puglia macchia, April 2023 (folklore) |
| `funghimagazine_aggiornamento_2024_01_12` | web | verified | chanterelles across Puglia, January 2024 (folklore) |
| `funghimagazine_aggiornamento_2024_03_14` | web | verified | chanterelles in the Salento and on the Gargano, March 2024 (folklore) |
| `myboletus_puglia` | web | verified | Gargano porcini "soprattutto" aereus and reticulatus; November-December peak (folklore) |
| `sedicipuglia_galletto2024` | web | verified | chanterelles in beech and oak, Gargano, Daunia, Alta Murgia (folklore) |
| `mushma_puglia_forest_composition_2026` | analysis | verified | habitat shares and heights on the Carta dei Tipi Forestali; gate effects |
| `mushma_occurrence_check_puglia_2026` | analysis | verified | month counts, heights and habitats of the records |

Existing references the Puglia changes lean on:
- `rt_tipi_forestali_p4`: the Tuscan beech belt, for comparison.
- `mushma_habitat_share_2026`: the four-level affinity scale.
