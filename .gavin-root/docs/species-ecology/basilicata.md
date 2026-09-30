# Species ecology: Basilicata (regional appendix to species-ecology.md)

Research date: 2026-09-30 (dates Europe/Rome, units metric). Card: `region-basilicata-species.md`
(child of `region-basilicata.md`). Rule files: `api/src/api/config/species/basilicata/`. This
appendix records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to
Basilicata (Lucania), what changed and why. It covers **fruiting conditions only**: nothing here is
about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(19 added for Basilicata, in one block at the end of the file, listed at the end of this page;
new keys carry a `bas_` prefix so the unmerged Molise and Veneto blocks cannot collide). Confidence
levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**, **plausible**,
**folklore**. Every number is a prior for the backtest; season windows, altitude bands and habitat
affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

Basilicata's three neighbours are merged in this checkout: Campania (west), Calabria (south) and
Puglia (north and east). The Lucanian side of the Pollino is the same massif as Calabria's, so
Calabria's record tables are the nearest regional evidence.
[Where Basilicata follows its neighbours and where it departs](#where-basilicata-follows-its-neighbours-and-where-it-departs)
takes the card's four questions (the Turkey-oak hills, the high Pollino and Sirino, the dry Materano
and Ionian coast, the late cold springs of the Potentino), and
[the table](#the-rule-changes-against-the-neighbours) compares the four rule sets.

## Summary

1. **All three groups and all six keys are kept.** The regional law names the porcini, the ovolo and
   the chanterelle (`bas_lr_48_1998`); the Pollino's forager mycologist lists all four porcini in the
   park (`bas_discoverpollino_porcini`); Funghi Magazine's bulletins report black and summer porcini,
   *B. edulis* and chanterelles in Basilicata (the sanity contrasts); iNaturalist has one ovolo, on the
   Pollino. The ovolo and *B. pinophilus* are the thin ones: *B. pinophilus* has no Basilicata
   record, but its hosts (high beech and fir) are here and the Calabrian side of the Pollino records
   it in beech (`ispra2018_mlg180_calabria_foreste`). Nothing is dropped.
2. **Basilicata is Turkey-oak country, and its Turkey oak is high.** Deciduous oak is 63.4 % of the
   wooded area on the grid, the highest share of any region so far; the Turkey oak sits at a median
   913 m on the map, the chestnut at 867 m and the beech at 1,259 m
   (`mushma_basilicata_forest_composition_2026`). The Turkey oak is the submontane forest "fra 500 e
   1200 m" (`bas_linee_forestali2013`, `bas_borghetti2024_boschi`). So the black porcino's and the
   ovolo's bands climb to Calabria's (full to 1,000 m, 0 at 1,350 m), and the beech keys' bands to
   Campania's and Calabria's.
3. **No Basilicata record table exists; Calabria's is the nearest.** The ISPRA manuals built from
   the Calabrian mycological groups' 45,000 records include a Pollino beech table and big Turkey-oak
   (801 records) and farnetto (792) tables. *B. aereus* is "la specie micologica più frequente" of
   the Turkey oak (3.1 %); the chanterelle is 2.6 % of it; *B. edulis* is 1.4 % of the Pollino beech
   (`ispra2018_mlg180_calabria_foreste`). Affinities move only where these shares and the neighbours'
   moves agree.
4. **`other_conifer` here means "conifer plantations, Aleppo pine low and black pine high".** The
   Carta della Natura has one code (83.31) for both: 56 % of it lies below 600 m. The porcini keep
   Tuscany's values and let the altitude bands separate the two (*B. edulis* and *B. pinophilus*
   stay marginal 0.3, scoring only the upper, black-pine, Douglas-fir and silver-fir plantations; *B.
   aereus* and the ovolo stay 0, *B. reticulatus* 0.1). The chanterelles, whose band does not reach
   down to exclude the Aleppo pine, move from 0.3 to non-host 0.1: none of 842 Calabrian plantation
   records of Aleppo or black pine is a chanterelle (`ispra2018_mlg179_calabria_rimboschimenti`).
5. **The southern season: the black porcino from May, a deep summer gap, a long western autumn.**
   Funghi Magazine's bulletins (86 of them with a Basilicata line, 2018-2025) date the first black
   porcini to mid- and late May ("Nascite abbondanti di Porcini Neri" by 16 May 2025,
   `bas_fm_2025_05_16`), the chanterelles to late May and June, a summer gap broken only on the high
   Sirino and Pollino (`bas_fm_2023_07_13`), and flushes in the west into November
   (`bas_fm_2022_11_05`). So *B. aereus*'s windows open on 1 May (a fortnight before Calabria's) and
   run to 30 November in the uplands and 10 January in the lowlands; the chanterelles' mountain window
   opens on 15 May. The other windows are Tuscany's.
6. **Weather rules are all Tuscany's.** No Basilicata study ties fruiting to rain or temperature in
   numbers. One known gap is added, as in Puglia: the holly beech lives on fog as well as rain.
7. **Records: almost none.** Basilicata has 757 iNaturalist fungi records and 4 of the six keys
   (`mushma_occurrence_check_basilicata_2026`); the sightings ingest kept none on a woodland cell
   (`regions/basilicata.md`). The backtest will say nothing about Basilicata on its own.
8. **The sources, all opened.** Of the 19 new sources, 1 is peer-reviewed (the Lucanian forests and
   their climate), 5 institutional (the picking law and ISPRA's summary of it, the two national
   parks' decrees, the regional forest programme), 1 a dataset (INFC 2015), 10 web pages (8 Funghi
   Magazine bulletins, the Pollino's forager mycologist and the ALSIA gauge network; folklore except
   the last) and 2 our own analyses. The rules also lean on the Calabrian ISPRA record tables and on
   11 Funghi Magazine bulletins already in the bibliography, all opened again.

## Basilicata in brief

**Woods.** The grid reads ISPRA's Carta della Natura habitat map of Basilicata (1:50,000, 2012-2013,
CORINE Biotopes codes; `config/regions/basilicata.yaml`). The region's own Carta forestale (INEA,
2006) is not published as data. The grid holds 284,433 ha of forest, 1.2 % under INFC 2015's bosco
of 288,020 ha (`bas_infc2015`), in 2,545 woodland cells (`regions/basilicata.md`).

This table is **which habitat holds which Basilicata tree** (areas on the whole map; shares of the
wooded area on the grid; `mushma_basilicata_forest_composition_2026`):

| habitat key | share of wooded area | Basilicata trees (Carta della Natura code, ha) | median height |
|---|---|---|---|
| `deciduous_oak` | 63.4 % | Turkey oak 41.7511 (113,397), downy oak 41.732 (36,184), southern Italian white oak 41.737B (19,129), Turkey oak with farnetto 41.7512 (16,614), *Quercus trojana* (fragno) 41.782 (249) | 913, 673, 568, 847 m; oak-dominated cells 785 m |
| `beech` | 12.7 % | southern Italian beech 41.18 (28,494), holly beech below and *Campanula* beech at the tree line | 1,259 m (p10-p90 982-1,468); beech cells 1,334 m |
| `transitional_woodland_shrub` | 5.6 % | bramble 31.8A (26,540), deciduous thickets 31.81 (24,592), tamarisk and oleander, shrub willows, broom, juniper | 694, 966 m |
| `mixed_broadleaf` | 5.5 % | *Alnus cordata* 41.C1 (9,656; 63 %), hop-hornbeam 41.81 (5,413; 36 %), ravine woods | 1,028, 805 m |
| `evergreen_oak` | 4.7 % | supra-Mediterranean holm oak 45.324 (11,975), southern holm oak 45.31A (3,501); no cork oak | 607, 277 m |
| `other_conifer` | 3.9 % | conifer plantations 83.31 (18,676): Aleppo pine on the clay hills and the Ionian side, black pine in the mountains, with some Douglas fir, silver fir and cypress | 474 m (p10 141, p90 1,225; 56 % below 600 m) |
| `chestnut` | 1.6 % | chestnut woods 41.9 (4,253), mostly volcanic: the Vulture (Atella, Rionero, Melfi), Trecchina | 867 m |
| `riparian` | 0.9 % | poplar 44.61, willow, black alder, narrow-leaved ash (13,421) | 282 m |
| `macchia` | 0.9 % | low macchia of wild olive and lentisk 32.211 (29,316, 84 %), garighe and macchia 32.3-32.4, *Cytisus*, dune macchia, olive and carob | 269 m |
| `mediterranean_pine` | 0.5 % | Aleppo pine 42.84 (1,407), wooded dunes 16.29 (1,148): the Ionian coast's planted stone and Aleppo pine (Policoro, Scanzano, Pisticci, Bernalda) | 196, 7 m |
| `mountain_pine` | 0.1 % | *pino loricato* 42.711 (320): the Pollino's summits and Monte La Spina | 1,211 m |
| `fir_spruce` | 0.1 % | southern Apennine silver fir 42.15 (177): largest share 0.42 of a cell in the Abetina di Laurenzana | 1,129 m |
| `exotic_broadleaf` | < 0.1 % | robinia 83.324 (305) | |

There is no mixed broadleaf-conifer class, so `mixed_broadleaf_conifer` is empty in Basilicata. At
1:50,000 the small fir and pine stands inside larger woods are lumped with their surroundings: the
Rifreddo's fir and beech are mapped as Turkey oak, Piano Ruggio's pine and fir planting as beech
(`regions/basilicata.md`).

INFC 2015 (`bas_infc2015`) has the same picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| Turkey oak, farnetto, fragno, vallonea | 130,692 | 45.4 % |
| sessile, downy and pedunculate oak | 43,077 | 15.0 % |
| other deciduous | 29,872 | 10.4 % |
| beech | 26,820 | 9.3 % |
| hygrophilous | 12,975 | 4.5 % |
| holm oak | 10,371 | 3.6 % |
| Mediterranean pines | 8,933 | 3.1 % |
| hop-hornbeam and hornbeam | 7,084 | 2.5 % |
| chestnut | 5,955 | 2.1 % |
| other conifers | 5,150 | 1.8 % |
| black, laricio and loricato pine | 2,610 | 0.9 % |
| other evergreen broadleaves | 1,864 | 0.6 % |
| silver fir | 746 | 0.3 % |
| broadleaf plantations | 1,522 | 0.5 % |
| cork oak, spruce, larch, Scots pine | 0 | 0 % |

**Where the woods are** (`regions/basilicata.md`):
- **Turkey oak** everywhere in the Potentino's hills: the most oak-dominated cells are in Accettura
  (the Gallipoli Cognato forest), Lauria, Abriola, Terranova di Pollino, Bella, San Chirico Raparo,
  Forenza and Tricarico.
- **Beech** on the Pollino (Viggianello, Terranova di Pollino, San Severino Lucano), the Sellata and
  Arioso (Abriola, Calvello), the Sirino and Lagonegrese (Lauria, Rivello) and the Maddalena (Marsico
  Nuovo).
- ***Alnus cordata* and hop-hornbeam** in the Lagonegrese and the Raparo (Moliterno, Lagonegro,
  Lauria, Castelsaraceno, Rivello).
- **Chestnut**, small and volcanic, on the Vulture; **holm oak** at Maratea, Lagonegro and the Agri
  and Sauro hills.
- **The conifer plantations** dominate 84 cells: black pine at Marsico Nuovo and Viggiano, Aleppo
  pine at Matera, Irsina, Pomarico and Montalbano Jonico.

**Altitude belts:**

| type | altitude (m) and where | source |
|---|---|---|
| Lauretum (holm oak, macchia, Aleppo pine) | 71 % of the region; warm subzone to 300 m on the Ionian coast, medium to 500-600 m, cold subzone the pre-Apennine | `bas_linee_forestali2013` p. 29 |
| Turkey oak | the submontane forest "fra 500 e 1200 m"; the typical Turkey oak "fino alla quota di circa 1000 m", a submontane variant "a quote superiori a 1000 m" with maples and beech; farnetto on the warm clay plateaus | `bas_linee_forestali2013` pp. 33-34, `bas_borghetti2024_boschi` |
| downy oak | "frequente nella collina materana", coppices with Mediterranean shrubs | `bas_linee_forestali2013` p. 34 |
| chestnut (Castanetum) | "da 800-900 m fino a 1200-1300 m"; chestnut woods 2.4 % of the forest, notably Monticchio on the Vulture; map median 867 m | `bas_linee_forestali2013` pp. 29, 36 |
| beech (Fagetum) | "soprattutto al di sopra dei 1000 m"; the zone runs "fino a 1800-1900 metri", largest on the Vulturino, the Lagonegrese and the Pollino; relict low beech on Monte Li Foi, at Brienza and on the Vulture | `bas_linee_forestali2013` pp. 29, 32-33 |
| silver fir | mixed with beech on the Pollino (Terranova di Pollino, Bosco Rubbio; Francavilla in Sinni, Bosco Vaccarizzo; Carbone) and with beech and Turkey oak at Laurenzana and Ruoti; map median 1,129 m | `bas_borghetti2024_boschi`, `bas_linee_forestali2013` p. 33 |
| pino loricato | the Pollino (Serra Crispo, Serra delle Ciavole) and Monte La Spina, above the high beech; map median 1,211 m | `bas_linee_forestali2013` p. 36, `ispra2018_mlg180_calabria_foreste` p. 188 |
| Aleppo pine | natural and planted "dell'Arco jonico, in provincia di Matera, fra i fiumi Bradano e Sinni", reforestation from the 1930s over 90 % Aleppo pine; on the clay hills with cypress, Atlas cedar and black pine | `bas_linee_forestali2013` p. 36 |
| Picetum | above 1,900 m, the highest summits of the Sirino and the Pollino | `bas_linee_forestali2013` p. 29 |

Basilicata's belts are Calabria's minus the laricio: the beech reaches the tree line at about
1,900-2,000 m (the highest woodland cell, beech on the Pollino at Chiaromonte, averages 1,926 m), and
the Turkey oak climbs to 1,200 m. The woodland cells sit at a median 816 m (p5-p95 400-1,396 m).

**Substrate.** The woodland cells' SoilGrids topsoil pH is 6.57 at the median (6.15-7.14), between
Calabria's acid granite (6.30) and Puglia's limestone (`regions/basilicata.md`). The Turkey oak
forms "associazioni finali" on sandstone and limestone ("su arenarie e calcari", `bas_linee_forestali2013`
p. 34), the pino loricato grows "su dolomie, calcari dolomitici" (`ispra2018_mlg180_calabria_foreste` p.
188), and the Vulture is a volcano. No Basilicata forest-soil pH was found. Soil pH stays a disabled
rule.

**Climate** (`bas_linee_forestali2013`, p. 28; `bas_borghetti2024_boschi`):
- **Three climates.** The eastern hills of the Materano get "tra 550 e 700 millimetri" a year,
  wettest in November-December, driest in August. The Apennine gets 650-1,000 mm on its eastern side
  and "tra 780 e 1700 mm nel settore centro-occidentale ove possono raggiungere anche valori intorno
  ai 2000 mm sulle quote più alte (oltre 1200 m.)". The Ionian foothills get 500 mm in the north and
  850 mm in the south-west.
- **The season.** Rain falls "prevalentemente nel periodo invernale ed autunnale e diminuiscono
  sensibilmente nel periodo estivo", sometimes in few, torrential days.
- **West and east.** The Ionian side is "più vulnerabile" to heat and drought; on the western
  Apennine "l'esposizione alle correnti tirreniche umide garantisce regimi di precipitazioni in
  grado di mitigare gli effetti delle ondate di calore". Spring frosts have damaged the beech, and
  the 2017 drought made thousands of hectares shed their leaves early (`bas_borghetti2024_boschi`).
- **Fog.** The commonest beech, the Aquifolio-Fagetum with holly, grows where moisture is
  "assicurata sia da buoni livelli di piovosità che da fenomeni di precipitazioni occulte"
  (`bas_linee_forestali2013` p. 33).

**Regional law.** L.R. 14 dicembre 1998, n. 48 (`bas_lr_48_1998`), amended by L.R. 26 novembre 2001,
n. 43. The Region's page names only these two laws; ISPRA's summary of April 2021 lists L.R. 43/2001 as
the only amendment (`bas_ispra_raccolta_funghi2021`). The Region's own consolidated archive
(atticonsiglio.consiglio.basilicata.it) refused connections on 2026-09-30, so a later omnibus
amendment cannot be ruled out.
- **Quantity.** "non più di 2 Kg. di funghi" a day, 10 kg with the special permit (art. 4 c. 3, both
  lowered from 3 and 15 kg by L.R. 43/2001). The ovolo and the St George's mushroom are capped at 1 kg
  (c. 4), as Campania caps them.
- **Size.** "È vietata la raccolta dell'ovulo buono (Amanita cesarea) allo stadio di ovulo chiuso, di
  porcini con cappello inferiore a 4 cm. di diametro e di ... gallinaccio (Cantharellus cibarius) con
  cappello inferiore a 2 cm. di diametro" (c. 5).
- **Days and hours.** "tutti i giorni della settimana da un'ora prima della levata del sole ad un'ora
  dopo il tramonto" (c. 1).
- **Permits.** Personal (6 months or a year), tourist (1 or 7 days, in one comune), special and
  scientific (art. 3, replaced by L.R. 43/2001); a 12-hour course for the personal permit.
- **Places.** Banned in integral reserves, in the areas of national and regional parks "individuate
  dagli organismi di gestione" and in areas the Giunta closes (art. 6). The Pollino park's founding
  decree allows "la raccolta di funghi, tartufi ed altri prodotti del bosco, nel rispetto delle
  vigenti normative, degli usi civici e consuetudini locali" in the whole park, zone 1 included
  (`bas_pn_pollino_dpr1993`, art. 3), and the Appennino Lucano park's decree saves "la raccolta di
  funghi, tartufi e degli altri prodotti del bosco nel rispetto delle vigenti normative e degli usi
  civici" (`bas_pn_appennino_lucano_dpr2007`, art. 3). The Gallipoli Cognato regional park sets its
  own picking rules; its site blocks every agent in robots.txt, so they were not read.
- **Poor years.** The Giunta "può ulteriormente limitare o vietare la raccolta" (art. 6 c. 3).
- **What it leaves out.** No season calendar and no altitude rule. None of it changes where or when
  the fungi fruit; it confirms the porcini, the ovolo and the chanterelle as regional species.

## Where Basilicata follows its neighbours and where it departs

The card asked where Basilicata's evidence follows its neighbours' windows and where it departs.

1. **The Turkey-oak hills: Calabria's reading, pushed further.**
   - Nearly two thirds of the woods are deciduous oak, mostly Turkey oak at 500-1,200 m, with
     farnetto on the warm clay plateaus and downy oak in the Materano hills. The fragno, Puglia's
     special case, is 249 ha here.
   - The Calabrian Turkey-oak and farnetto tables (1,593 records) make it *B. aereus*'s wood (3.1 %
     and 2.6 %, the commonest species of the Turkey oak), a good chanterelle wood (2.6 %, farnetto
     0.4 %), and a *B. reticulatus* wood (1.7 %); the ovolo is commoner in the downy oak (1.6 %) than
     in the Turkey oak (0.4 %) (`ispra2018_mlg180_calabria_foreste`).
   - What follows: deciduous oak stays a full host for *B. aereus*, *B. reticulatus* and the ovolo and
     becomes secondary for the chanterelles, as in Campania, Calabria and Puglia. *B. aereus* and the
     ovolo take Calabria's bands (full to 1,000 m, 0 at 1,350 m) because the Turkey oak sits at a
     median 913 m, higher than Calabria's (834 m) and far above Tuscany's.
2. **The high Pollino and Sirino: Campania's and Calabria's bands, without Calabria's laricio.**
   - The beech runs "fino a 1800-1900 metri" (`bas_linee_forestali2013`); the highest woodland cell
     averages 1,926 m. *B. edulis* and *B. pinophilus* get bands full to 1,800 m, *B. reticulatus* and
     the chanterelles bands full to 1,600 and 1,400 m, as in Campania and Calabria; beech becomes a
     full host for *B. reticulatus* and the chanterelles.
   - Basilicata has no laricio. Its `mountain_pine` is 320 ha of pino loricato on the summits, with
     "solo due rilevamenti" in the Calabrian tables, neither a porcino (one a chanterelle). So Calabria's
     laricio moves (*B. pinophilus* 1.0, *B. edulis* and *B. reticulatus* 0.1) are not copied: *B.
     pinophilus* keeps Tuscany's 0.6, *B. edulis* and *B. reticulatus* take the 0.3 that Abruzzo and
     Puglia gave their black pine.
   - The silver fir is 177 ha, mixed with beech and Turkey oak (Laurenzana, Ruoti, the Pollino's Bosco
     Rubbio and Vaccarizzo; `bas_borghetti2024_boschi`): a *B. edulis* host (3.3 % of the Calabrian fir
     records), too small to matter on the grid.
   - The Sirino and the Lagonegrese are the wettest woods of the region ("intorno ai 2000 mm sulle
     quote più alte", `bas_linee_forestali2013`), with *Alnus cordata* between the oak and the beech;
     `mixed_broadleaf` goes down for the beech porcini, the summer porcino and the chanterelles
     and stays marginal for *B. aereus* and the ovolo, whose hop-hornbeam third can hold a host.
3. **The dry Materano and the Ionian coast: Puglia's reading of the Mediterranean classes.**
   - The eastern hills get 550-700 mm and the northern Ionian foothills 500 mm
     (`bas_linee_forestali2013`). Their woods are downy oak, holm oak, the wild-olive and lentisk
     macchia, and Aleppo pine, natural on the Arco jonico and planted on the clay hills.
   - As in Puglia (and Calabria), the macchia goes down for *B. aereus* (0.3), the ovolo and the
     chanterelles (0.1); `mediterranean_pine` and the conifer plantations go to non-host for *B.
     aereus* and the chanterelles.
   - *B. aereus*'s lowland window (handover at 600-800 m) covers these hills, full to 30 November and
     running to 10 January, as in Campania, Calabria and Puglia.
   - Puglia's March chanterelles and April summer porcini are not copied: no Basilicata source reports
     them, and the coast has no host wood; the one "Lucania costiera" line on early summer porcini is
     a memory of the past ("un tempo precocissimi", `funghimagazine_nascite_2026_04_23`).
   - The Murgia materana's cardoncello (*Pleurotus eryngii*) is out of scope, as in Puglia.
4. **The late cold springs of the Potentino: the weather, not the calendar.**
   - The Potentino's woods are high: the woodland cells sit at a median 816 m, the oak-dominated ones
     at 785 m, the beech ones at 1,334 m. The eastern Apennine has mean January-February lows of 3-3.5
     °C (`bas_linee_forestali2013` p. 28), and late spring frosts have damaged the Lucanian beech
     (`bas_borghetti2024_boschi`).
   - No calendar delay is written in. The windows that open in May (*B. aereus* on 1 May, the
     mountain chanterelles on 15 May) open there too, and the cold does the delaying: the growth clock
     runs slowly in cold topsoil (about 65 % pace at 9 °C), and the frost and snow stoppers end the
     autumn.
   - The bulletins show the spring starting late in cold years and early in mild ones: "Basilicata
     ferma al palo" on 16 June 2018, the region "fermi al palo" on 18 May 2023, and in May 2025 "le
     temperature miti, non eccessivamente calde, hanno giocato un ruolo chiave" (`bas_fm_2025_05_16`).
     That is the temperature rules' job, not the calendar's.

## The conifer plantations (`other_conifer`)

The card's special case. The Carta della Natura files every conifer plantation under one code,
83.31 (18,676 ha, 3.9 % of the wooded area), and the grid gives a code one habitat, so
`other_conifer` in Basilicata means two woods:
- **Aleppo pine, low.** 56 % of the plantations lie below 600 m (p10 141 m): the reforestation of the
  Materano's clay hills and the Arco jonico, "oltre il 90%" Aleppo pine, with some cypress and
  Atlas cedar (`bas_linee_forestali2013` p. 36). The plantation-dominated cells of Matera, Irsina,
  Pomarico and Montalbano Jonico.
- **Black pine, high.** The upper tenth lies above 1,225 m: black pine, with Douglas fir and silver
  fir in some regional forests (Fossa Cupa at Abriola, the Rifreddo at Pignola;
  `bas_linee_forestali2013` Tab. 7.1). The plantation-dominated cells of Marsico Nuovo and Viggiano.

What fruits under them, from the Calabrian plantation tables
(`ispra2018_mlg179_calabria_rimboschimenti`, `ispra2018_mlg179_pino_aleppo`), the nearest record
base:
- **Aleppo-pine plantations** (802 records, 227 species): *Suillus* and *Lactarius sanguifluus*; no
  porcino, ovolo or chanterelle.
- **Black-pine plantations** (40 records, 15 species): ubiquitous forest species only; no porcino and
  no chanterelle.
- **Native fir, spruce and larch plantations** (806 records): *B. edulis* the top species (4.6 %),
  *B. pinophilus* 0.6 %, the chanterelle 0.6 %.
- **Douglas-fir plantations** (623 records): no porcino, ovolo or chanterelle among them.

So each key's affinity is set for the mix, with the altitude band doing the separating:

| key | `other_conifer` | Tuscany | why | where it scores |
|---|---|---|---|---|
| *B. edulis* | 0.3 (kept) | 0.3 | marginal: the fir plantations are hosts, black pine and Douglas fir are not | the band (0 at 200 m, full from 700 m) keeps it off the Aleppo pine; the one Basilicata *B. edulis* record is in a plantation-and-scrub cell at 827 m |
| *B. pinophilus* | 0.3 (kept) | 0.3 | as *B. edulis* | band 300 → 800 m |
| *B. reticulatus* | 0.1 (kept) | 0.1 | non-host | nowhere much |
| *B. aereus* | 0 (kept) | 0 | no porcino in the Aleppo or black-pine tables | nowhere |
| ovolo | 0 (kept) | 0 | none in any Calabrian plantation table | nowhere |
| chanterelles | **0.1** | 0.3 | none in 842 Aleppo and black-pine plantation records; the band is full to 1,400 m, so it cannot exclude the low Aleppo pine | a pure plantation cell keeps a third of full habitat credit |

`mediterranean_pine` (the natural Aleppo pine and the Ionian dune pine woods, 0.5 %) follows the same
evidence and goes to 0.1 for *B. aereus* and the chanterelles, as in Calabria and Puglia. The mixed
cells keep full credit through their oak or beech.

## The rule changes against the neighbours

All four rule sets start from the same Tuscan files.

| factor | Tuscany | Campania | Calabria | Puglia | Basilicata | why Basilicata |
|---|---|---|---|---|---|---|
| *B. pinophilus* | kept | kept | kept | dropped | kept | high beech and fir; the Pollino evidence |
| `mountain_pine` for *B. edulis*, *B. reticulatus* | 0.6 | 0.6 | 0.1 | 0.3 | **0.3** | pino loricato, not laricio; no porcino in its two records |
| `mountain_pine` for *B. pinophilus* | 0.6 | 0.6 | 1.0 | — | 0.6 | the Pollino's spring "Pinicola" (folklore); no laricio table here |
| `chestnut` for *B. pinophilus* | 1.0 | 1.0 | 0.3 | — | **0.3** | the Calabrian chestnut table (0.1 %) |
| `beech` for *B. reticulatus* | 0.6 | 1.0 | 1.0 | 0.6 | **1.0** | the beech belt is high, as Campania's and Calabria's |
| *B. reticulatus* altitude | 0 → 150 … 1,100 → 1,500 | 1,600 → 1,900 | 1,600 → 1,900 | open … 1,100 → 1,500 | **1,600 → 1,900** | beech median 1,259 m |
| `mixed_broadleaf` for *B. reticulatus*, `transitional_woodland_shrub` for it and *B. aereus* | 0.6 | 0.6, 0.3 | 0.3 | 0.3 | **0.3** | *Alnus cordata* and hop-hornbeam; bramble and thickets |
| `macchia` for *B. aereus* | 1.0 | 1.0 | 0.3 | 0.3 | **0.3** | wild olive and lentisk |
| `mediterranean_pine` for *B. aereus*, chanterelles | 0.6, 0.3 | kept | 0.1, 0.1 | 0.1, 0.1 | **0.1, 0.1** | Aleppo pine, no record in the Calabrian tables |
| `mixed_broadleaf` for *B. aereus* | 0.3 | 0.6 | 0.1 | 0.3 | 0.3 | a third hop-hornbeam |
| *B. aereus* windows | upland 15 Jun, lowland 1 Jul → 15 Dec; handover 400-600 m | lowland to 10 Jan; 600-800 m | both from 15 May; upland to 30 Nov; lowland to 10 Jan | lowland 15 May → 10 Jan; upland Tuscany's | **both from 1 May**; upland to 30 Nov; lowland to 10 Jan; 600-800 m | abundant black porcini by mid-May 2025; western flushes into November |
| *B. aereus*, ovolo altitude | 800 → 1,250; 750 → 1,100 | kept | 1,000 → 1,350 both | kept | **1,000 → 1,350 both** | Turkey oak median 913 m |
| `evergreen_oak` for the ovolo | 0.6 | 0.6 | 1.0 | 0.6 | 0.6 | holm oak only, no cork oak |
| `macchia` for the ovolo and the chanterelles | 0.3 | 0.3 | 0.3 | 0.1 | **0.1** | wild olive and lentisk (as Puglia) |
| `transitional_woodland_shrub` for the ovolo | 0.6 | 0.3 | 0.3 | 0.3 | **0.3** | bramble, thickets, broom |
| ovolo window | 1 Jun → 1 Sep … 5 Nov → 30 Nov | kept | 15 May → 1 Aug | kept | kept | no Basilicata date but a September record |
| `other_conifer` for the chanterelles | 0.3 | 0.3 | 0.3 | 0.3 | **0.1** | here it is Aleppo and black-pine plantations |
| `beech`, `deciduous_oak` for the chanterelles | 0.6, 0.3 | 1.0, 0.6 | 1.0, 0.6 | 1.0, 0.6 | **1.0, 0.6** | same move |
| chanterelle mountain window | from 1 Jun | from 15 May | from 15 May | from 15 May | **from 15 May** | same move |
| chanterelle lowland window | 15 Apr → 25 Jan | kept | kept | from 15 Mar | kept | no late-winter report |
| chanterelle altitude | 1,000 → 1,700 | 1,400 → 1,900 | 1,500 → 1,900 | kept | **1,400 → 1,900** | beech p90 1,468 m (Campania 1,453 m) |
| *B. edulis*, *B. pinophilus* altitude | 1,600 → 1,900 | 1,800 → 2,000 | 1,800 → 2,000 | kept (*edulis*) | **1,800 → 2,000** | Fagetum to 1,800-1,900 m |
| *B. edulis* window | from 1 Jul | kept | from 1 Jun | kept | kept | no early Basilicata *B. edulis* |

In short: Basilicata takes Calabria's heights and southern *B. aereus* season (its hosts are as high
or higher), Campania's and Calabria's beech moves, and Puglia's reading of the Mediterranean classes;
its own departures are the pino loricato (not laricio) and the conifer plantations (Aleppo and black
pine under one code).

## The southern season

The card asked about spring flushes, the summer drought and a late autumn. Almost all the Basilicata
evidence is Funghi Magazine's (folklore): 86 bulletins of 2018-2025 with a Basilicata line, read by a
research agent and re-checked here (quotes and dates in the sanity contrasts and their sources).

1. **Early flushes: yes, the black porcino first, low and on the Tyrrhenian side.**
   - *B. aereus* "segnalati ... in Basilicata" by 30 May 2019 (`fm_sicilia_2019_05_30`); "Porcini
     estivi e rari Neri Lucani" around the Golfo di Maratea, in the Potentino and on the pre-Pollino
     in late May 2024, after the rains of 18-19 May (`fm_sicilia_2024_05_30`); "Nascite abbondanti di
     Porcini Neri" by 16 May 2025, when "La Lucania tirrenica ha visto una insolita quanto inaspettata
     nascita di Boletus aereus in tutti i boschi a prevalenza di querce" (`bas_fm_2025_05_16`).
   - Summer porcini: "Discrete nascite di Porcini Estatini tra Campania-Basilicata-Calabria" on 28 May
     2022 (`funghimagazine_porcini_maggio2022`); the first Lucanian births of 2020 on 11 June, "soprattutto
     nel Metapontino ed immediato entroterra".
   - Chanterelles: "Già ben presenti ... Calabria-Puglia-Basilicata" on 30 May 2019; "Mai come
     quest'anno in Basilicata si sono travati ... così tanti Finferli in primavera" on 1 June 2023.
   - Late years exist: "ferma al palo" through June 2018; "fermi al palo" in May 2023, with the black
     porcini only in mid-June ("moltissimi Porcini Aereus, soprattutto in collina in boschi misti",
     `bas_fm_2023_06_23`).
   - What changed: *B. aereus* opens on 1 May (full 1 June below 600 m, 1 July above 800 m); the
     chanterelles' mountain window opens on 15 May. *B. reticulatus* already opened on 1 May.
2. **A summer drought gap: yes, deep, and the weather makes it.**
   - "nascite bloccate dal caldo-secco" in early July 2020; "Puglia e Basilicata si possono godere il
     mare e l'estate" in July 2023; "L'eccesso di calore ha mandato in letargo i miceli fungini" in late
     June 2024; "Situazione molto difficile: piogge scarsissime o assenti, caldo e vento non danno
     tregua" in July 2025.
   - The one recurring exception is the high ground: "Nascite scarsissime o assenti in Lucania, salvo
     in alta quota sul Sirino e vicine cime di Lauria-Lagonegro" (`bas_fm_2023_07_13`); "resiste
     qualcosa tra Sirino e Pollino" in June 2024. The raised bands of *B. reticulatus* and *B. edulis*
     keep that ground in.
   - The season restarts with the August storms: the Basentana in mid-August 2020, the bassa Basentana
     in early September 2021, the whole west from mid-August 2022 ("In terza posizione la BASILICATA",
     `bas_fm_2022_08_26`), the Tyrrhenian side in late August 2023, "dopo Ferragosto" in 2025.
   - As in Tuscany and the other southern regions, no calendar gap is written in. The porcini's 30-day
     rain is scored against each cell's own normal; the ovolo and chanterelle ramps are absolute.
3. **A later autumn: yes, in the west.**
   - "buone o ottime nascite di funghi, soprattutto Porcini, nei settori Ovest e Sud" in late October
     2020 (`bas_fm_2020_10_23`); "nascite davvero importanti, diffuse e talvolta persino massicce" in the
     west in October 2022, with more expected after mid-November (`bas_fm_2022_11_05`); black porcini
     that "non si contano" in late October 2018 (`funghimagazine_aggiornamento_2018_10_22`); the 2023
     season starting only in early November, first "lungo le coste tirreniche di Lucania".
   - Chanterelles into December: "ottimi raccolti ... [in] parte di Basilicata, sia tirrenica che di
     confine con la Puglia" in mid-December 2023 (`bas_fm_2023_12_16`).
   - What changed: *B. aereus* runs to 30 November above 800 m and 10 January below 600 m. The
     chanterelles' lowland window already ran to 25 January, *B. edulis*'s to 20 December.
4. **West against east.** The bulletins' commonest Basilicata pattern: the Tyrrhenian-facing west (the
   Lagonegrese, Maratea, the Sinni and Pollino, the Val d'Agri, the western Potentino) produces while
   "i soliti settori Est" (the Materano and the Metapontino) stay dry (`bas_fm_2022_08_26`,
   `bas_fm_2022_09_05`, `bas_fm_2022_11_05`). The exceptions run the other way: the Metapontino in June
   2020 and 2021, the bassa Basentana in September 2021. No rule encodes the pattern: the rain does,
   and five sanity contrasts test it.

## Occurrence cross-check (Basilicata)

Queried 2026-09-30 (`mushma_occurrence_check_basilicata_2026`):
- **iNaturalist**: place 8763 ("Basilicata, IT"), verifiable records. Elevations from the EU-DEM (25
  m) through the OpenTopoData API, for open, non-obscured records with an accuracy of 1 km or better
  (the Open-Meteo elevation API the earlier regions used was left alone: its quota is shared with the
  weather ingest).
- **GBIF**: `gadmGid=ITA.3_1`.
- Aggregates only; no coordinates are stored.

Basilicata has 757 iNaturalist fungi records from 198 observers, 88 % since 2020 (Puglia 2,961,
Calabria 3,053, Campania 4,437, Tuscany 19,089). A quarter of them fall in August.

| taxon | iNat n | date | place, height |
|---|---|---|---|
| *B. edulis* | 1 | 5 December 2023 | Pietrapertosa (the Gallipoli Cognato park), 827 m, in a cell of conifer plantation and scrub |
| *B. reticulatus* | 1 | 7 September 2022 | Chiaromonte (the Pollino); not located to 1 km; needs ID |
| *B. aereus* | 1 | 18 May 2024 | Fardella (the Val Sinni below the Pollino), 946 m |
| *B. pinophilus* | 0 | | |
| *A. caesarea* | 1 | 16 September 2024 | San Severino Lucano (the Pollino); not located to 1 km |
| *Cantharellus* | 0 | | |
| all fungi (share, %) | 757 | J 3, F 4, M 3, A 5, M 8, J 8, J 8, A 24, S 6, O 14, N 11, D 6 | |

GBIF holds only the *B. edulis* and *B. aereus* records, both iNaturalist copies; its 1,738 Basilicata
fungi records hold no other key. The sightings ingest kept neither on a woodland cell
(`regions/basilicata.md`).

What the records show:
- **Nothing to tune on.** Four records, all from 2022-2024. The backtest will have no Basilicata
  presences; the rules are as good as the evidence behind them.
- **Two dates that fit the southern windows.** An upland *B. aereus* on 18 May (the new May
  opening) and a *B. edulis* on 5 December (the Tuscan tail).
- **The heights fit the bands.** Both located records are at 827-946 m, inside every changed band.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence** beyond what is above:
- **Which porcino** (folklore). All four are named on the Pollino: *B. aereus* with a "presenza
  massiccia nel nostro Parco Nazionale del Pollino", "Capu niviru", "non ... solo sotto quercia ...
  [ma] sotto una moltitudine di latifoglie quali castagno e faggio" (`bas_discoverpollino_porcini`).
  The bulletins speak of "Porcini neri" and "Porcini estivi" in Basilicata far more than of *B.
  edulis* (the sanity contrasts).
- **Record shares on the Calabrian side of the massif** (plausible;
  `ispra2018_mlg180_calabria_foreste`):

  | taxon | Pollino beech | Turkey oak (801) | farnetto (792) | downy oak (368) | holm oak (390) | chestnut (3,192) |
  |---|---|---|---|---|---|---|
  | *B. edulis* | **1.4** | 0.2 | – | 0.3 | – | 0.7 |
  | *B. reticulatus* | 0.8 | 1.7 | 0.4 | 1.1 | 0.3 | **1.8** |
  | *B. aereus* | – | **3.1** | 2.6 | 2.4 | 1.1 | 0.8 |
  | *B. pinophilus* | 0.6 | 0.1 | – | – | – | 0.1 |

  The Pollino beech table holds 209 taxa; the Calabrian silver fir (329 records) has *B. edulis* as
  its top species (3.3 %).
- **The summer flush in the beech** (folklore). In July 2026 summer porcini came "sul Pollino, nella
  Lucania occidentale", "decisamente più abbondanti nelle faggete e nei castagneti" than in the lower
  oak woods (`funghimagazine_nascite_2026_07_10`).
- **Timing** (folklore). The bulletins' Basilicata sequence: black porcini first, low and on the
  Tyrrhenian side, from mid-May; summer porcini with them; in late summer "Dapprima i
  Porcini Neri (B. aereus) delle basse quote, tra pianori vallivi e colli interni, successivamente
  Porcini Neri e Porcini Estatini degli alti colli e monti, decisamente più rari i Porcini edulis,
  soprattutto sul Pollino, Sirino e quote montane più elevate" (`bas_fm_2022_08_26`); in 2022 the
  "boschi montani con Estatini e persino Edulis, mai così abbondanti come quest'anno"
  (`bas_fm_2022_09_05`); in October and November the west (`bas_fm_2020_10_23`, `bas_fm_2022_11_05`).

**Decisions.**

| key | factor | Tuscany | Basilicata | why | confidence |
|---|---|---|---|---|---|
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | *Alnus cordata* (63 %) and hop-hornbeam (36 %) | plausible |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | bramble, deciduous thickets, broom | plausible |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.3** | pino loricato: two Calabrian records, no porcino; shares cells with beech | plausible (weak) |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | 200 → 700 … **1,800 → 2,000** | Fagetum "fino a 1800-1900 metri"; highest woodland cell 1,926 m | plausible |
| *edulis* | known gap `occult_precipitation` | — | **new** | the holly beech lives on fog as well as rain | plausible |
| *reticulatus* | habitat `beech` | 0.6 | **1.0** | among the commonest in every Calabrian beech type, 0.8 % of the Pollino beech; the July 2026 flush in the Pollino's beech | plausible |
| *reticulatus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub`, `mountain_pine` | 0.6 | **0.3** | *Alnus cordata* and hop-hornbeam; scrub; pino loricato | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,600 → 1,900** | beech now a host, median 1,259 m; southern records median 1,120 m | plausible |
| *aereus* | season | upland 15 Jun → 1 Aug … 30 Sep → 31 Oct; lowland 1 Jul → 1 Sep … 15 Nov → 15 Dec; handover 400-600 m | upland **1 May → 1 Jul … 31 Oct → 30 Nov**; lowland **1 May → 1 Jun … 30 Nov → 10 Jan**; handover **600-800 m** | abundant black porcini by 16 May 2025, late May 2019 and 2024, a record at 946 m on 18 May; October flushes in the west (2018, 2020, 2022) with more expected after mid-November 2022 | folklore |
| *aereus* | habitat `macchia` | 1.0 | **0.3** | 84 % wild olive and lentisk, not Cistus-Arbutus-Erica | plausible |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | bramble, deciduous thickets, broom | plausible |
| *aereus* | habitat `mediterranean_pine` | 0.6 | **0.1** | Aleppo pine: no porcino in 822 Calabrian records | plausible |
| *aereus* | altitude | … 800 → 1,250 | … **1,000 → 1,350** | Turkey oak "fra 500 e 1200 m", median 913 m | plausible |
| *pinophilus* | habitat `chestnut` | 1.0 | **0.3** | 0.1 % of the Calabrian chestnut records; not among the national chestnut's frequent species | plausible (weak) |
| *pinophilus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3 | **0.1** | *Alnus cordata*, hop-hornbeam; scrub | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | 300 → 800 … **1,800 → 2,000** | beech and fir to the tree line | plausible |
| all four | weather, stoppers, growth clock | — | kept | no Basilicata numbers | as Tuscany |

Kept on purpose:
- **`other_conifer` 0.3 for *B. edulis* and *B. pinophilus***: see [the conifer plantations](#the-conifer-plantations-other_conifer).
- ***B. edulis* in deciduous oak (0.3)**: 0.2-0.3 % of the Calabrian Turkey and downy oak records; the
  band spares the high Turkey oak where it meets the beech.
- ***B. aereus* in beech (0.1)**: no *B. aereus* in the Pollino beech records, against the Pollino
  lore's "castagno e faggio". The band (0 at 1,350 m) keeps it off most beech anyway.
- ***B. aereus* in `mixed_broadleaf` (0.3)**: between Calabria's 0.1 (86 % *Alnus cordata*) and
  Campania's 0.6 (hornbeam and chestnut mixes); here a third of the class is hop-hornbeam.
- ***B. pinophilus* in `mountain_pine` (0.6)**: the spring "Porcini rossi-Pinicola" of the Pollino's
  pine woods (`funghimagazine_porcini_maggio2022`, folklore); 320 ha, it barely matters.
- ***B. edulis*, *B. reticulatus* and *B. pinophilus* windows**: no Basilicata source calls them early
  or late, as the Calabrian museum cards do.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.** The regional law caps the "Amanita cesarea (ovulo buono)" at 1 kg a day and bans the
  closed ovolo (`bas_lr_48_1998`, art. 4). One iNaturalist record, San Severino Lucano, 16 September
  2024. Funghi Magazine gives no verdict on ovoli in Basilicata: the one Basilicata sentence that
  names them (September 2019) puts them in the neighbouring Subappennino Dauno.
- **Hosts** (plausible). No Basilicata source names one. On the Calabrian side it is 1.6 % of the
  downy-oak records, 1.1 % of the farnetto, 0.9 % of the holm oak and 0.4 % of the Turkey oak ones
  (`ispra2018_mlg180_calabria_foreste`); 2.4 % of the national chestnut records, its fourth commonest
  species (`ispra2019_mlg187_flora_micologica`).
- **Height** (plausible, from Calabria). "cresce fino a circa 1200 m di quota"
  (`lavorato2013_calabrone_caesarea`); on Monte Cocuzzo from 300-400 m to about 1,500 m, "l'altitudine
  ideale ... è tra i 600 e 900 metri" (`bosco_grande2004_caesarea_cocuzzo`); forager lore has it "fin
  verso i 1000 mt in Appennino" in the Centre-South and "fin verso i 1200" in Calabria
  (`funghimagazine_ovolo`, folklore).

**Decisions.**

| factor | Tuscany | Basilicata | why | confidence |
|---|---|---|---|---|
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | bramble, deciduous thickets, broom; not heath with scattered oaks | plausible |
| habitat `macchia` | 0.3 | **0.1** | wild olive and lentisk, almost no oak (as Puglia) | plausible |
| altitude | … 750 → 1,100 | … **1,000 → 1,350** | Turkey oak median 913 m, chestnut 867 m; "fino a circa 1200 m" | plausible |
| season | 1 Jun → 1 Sep … 5 Nov → 30 Nov | kept | no Basilicata date but a September record; Calabria's summer start rests on Calabrian museum cards and society notes | plausible |
| deciduous oak, chestnut 1.0; evergreen oak 0.6; `mixed_broadleaf` 0.3; beech 0 | — | kept | no cork oak (Calabria's reason for 1.0); hop-hornbeam a third of the mixed class | strong (hosts) |
| weather rules | — | kept | no Basilicata numbers | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "gallinaccio", "galletti", "finferli")

**Regional evidence.**
- **Presence.** "gallinaccio (Cantharellus cibarius)" in the regional law (`bas_lr_48_1998`). No
  Basilicata record on iNaturalist or GBIF, and no Basilicata checklist says which species.
- **Hosts** (plausible). On the Calabrian side chanterelles are among "le specie maggiormente
  frequenti in tutte le tipologie" of beech, 1.4 % of the Pollino beech records (entered as "C.
  alborufescens"); 2.6 % of the Turkey oak, 2.4 % of the downy oak and 2.7 % of the chestnut records,
  0.4 % of the farnetto (`ispra2018_mlg180_calabria_foreste`); none in the Aleppo or black-pine
  plantations (`ispra2018_mlg179_calabria_rimboschimenti`).
- **Season** (folklore). Chanterelles were "Già ben presenti ... talvolta già anche abbondanti come
  in Sicilia, Calabria-Puglia-Basilicata e Campania" on 30 May 2019 (`fm_sicilia_2019_05_30`), and
  the first good harvests of early June 2019 came "nei soli boschi termofili, essenzialmente a base di
  Quercia ... tra Calabria, Basilicata, Campania" (`funghimagazine_giugno2019`). "Mai come quest'anno
  in Basilicata si sono travati, e si stanno ancora trovando, così tanti Finferli in primavera" on 1
  June 2023 (`funghimagazine_aggiornamento_2023_06_02`); "Puglia-Basilicata" had them "più che mai" in
  mid-June (`funghimagazine_aggiornamento_2023_06_16`), then came "i grandi raccolti di Finferli della
  Lucania" (`bas_fm_2023_06_23`). In June 2024 "Anche i Finferli sono spariti sotto l'incalzare del gran
  caldo" (`vda_fm_2024_06_14`). In mid-December 2023 there were "ottimi raccolti" in the Tyrrhenian and
  Apulian-border parts (`bas_fm_2023_12_16`).

**Decisions.**

| factor | Tuscany | Basilicata | why | confidence |
|---|---|---|---|---|
| season: mountain window | 1 Jun → 1 Jul … 15 Oct → 15 Nov | **15 May → 15 Jun** … 15 Oct → 15 Nov | early-June harvests in the oak; as all four neighbours | plausible (folklore sources) |
| habitat `beech` | 0.6 | **1.0** | commonest species of the Calabrian beech; 1.8 % of the national beech records | plausible |
| habitat `deciduous_oak` | 0.3 | **0.6** | Turkey and downy oak as rich as chestnut in the Calabrian tables, farnetto poor | plausible |
| habitat `other_conifer` | 0.3 | **0.1** | Aleppo and black-pine plantations: none in 842 records | plausible |
| habitat `mediterranean_pine` | 0.3 | **0.1** | Aleppo pine and dune pine: none in the tables | plausible |
| habitat `mixed_broadleaf`, `transitional_woodland_shrub`, `macchia` | 0.3 | **0.1** | *Alnus cordata* and hop-hornbeam; scrub; wild olive and lentisk | plausible |
| altitude | … 1,000 → 1,700 | … **1,400 → 1,900** | beech median 1,259 m, p90 1,468 m (as Campania) | plausible |
| chestnut, evergreen oak 1.0; `mountain_pine` 0.3; lowland window | — | kept | one of the two loricato records is a chanterelle; no late-winter Basilicata report | plausible |
| soil pH, lithology | disabled | kept disabled | no Basilicata soil evidence | plausible |
| weather rules | — | kept | no Basilicata numbers | as Tuscany |

## Weather rules: why none changed

- **Rain amount and lag.** No Basilicata source gives an amount or lag in numbers. The generic
  forager threshold for *B. aereus*, "30-40 mm complessivi (limite minore)" (`bmeteo_boletus_aereus`),
  sits at the top of the Tuscan 10 → 30 mm ramp. The bulletins' Basilicata lore agrees with the Tuscan
  rules: flushes follow rain and then mild warmth ("le nascite attuali sono dovute alle piogge del
  18/19", May 2024; "le temperature miti, non eccessivamente calde, hanno giocato un ruolo chiave", May
  2025), heat stops them ("L'eccesso di calore ha mandato in letargo i miceli fungini", June 2024), and
  wind wastes rain ("il vento ha ridotto al minimo i risultati", June 2025; "il vento di Tramontana o
  Grecale ha dato il colpo di grazia ... così come sulla vicina Lucania", October 2021).
- **Summer drought.** The Materano and the Ionian side are dry and "più vulnerabile"; the western
  Apennine is cushioned by Tyrrhenian air (`bas_borghetti2024_boschi`). The porcini's 30-day rain is a
  percentage of each cell's own normal, so it adapts; the ovolo and chanterelle 30-day ramps are
  absolute and will seldom be full in a dry July.
- **Cold.** Frost and snow end the season on the Potentino uplands, the Sirino and the Pollino; the
  frost and snow stoppers are kept. Spring frosts in the beech (`bas_borghetti2024_boschi`) are what
  the growth clock's cold pace and the frost stopper already read.
- **Fog** (new known gap, `occult_precipitation` on *B. edulis*). The holly beech's moisture comes
  partly from "precipitazioni occulte" (`bas_linee_forestali2013`), which the reanalysis rain does not
  see.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it is a
  region-card task. See [Open questions](#open-questions-and-hand-offs) for the gauge networks.

## Groups and keys

Nothing is dropped. All six keys have Basilicata evidence: the regional law (porcini, ovolo,
chanterelle), the Pollino forager mycologist (four porcini), the bulletins, and iNaturalist records of
four keys. *B. pinophilus* rests on the Pollino evidence alone; its habitat is the high beech and fir,
which *B. edulis* shares, so keeping it changes the porcini group score little.

`mixed_broadleaf_conifer` is not on the Basilicata map but stays in the rule files, as in every
region; it scores no cell.

## Effect on the woodland cells

The grid was built while these rules were written; the gate-by-gate comparison against the Tuscan
rules over the 2,545 woodland cells is a hand-off (below). What the grid's summaries already show
(`mushma_basilicata_forest_composition_2026`):
- **The oak country keeps its porcini, now at full height.** The 1,838 oak-dominated cells sit at a
  median 785 m. *B. aereus*'s new band is full there and to 1,000 m; the Tuscan band would have given
  the median Turkey oak (913 m) 0.75. The ovolo's goes from 0.53 to 1.0 at 913 m.
- **The beech cells get their summer porcino and chanterelles.** The 308 beech-dominated cells sit at
  a median 1,334 m: the Tuscan *B. reticulatus* band gave 0.42 there, the new one 1.0; the chanterelle
  band 0.52 → 1.0. *B. edulis* was already full there.
- **What loses credit.** Pure *Alnus cordata* and hop-hornbeam cells (116, Lagonegrese and Raparo) keep
  a third of full habitat credit for *B. edulis*, *B. pinophilus* and the chanterelles; low
  conifer-plantation cells lose the chanterelles; macchia and dune-pine cells lose *B. aereus* and the
  ovolo. These are few: macchia and Mediterranean pine dominate 21 cells.

## Sanity contrasts

`basilicata/sanity.yaml` holds Basilicata's areas and contrasts. Windows and sources were written
down on 2026-09-30, before any Basilicata score existed.

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_`. "Normal" is the area's mean over 2017-2025.

**Areas.** Every comune was checked against the ISTAT 2025 list (COD_REG 17, 131 comuni): all 71
names are in Basilicata. ISTAT spells "Sant'Angelo Le Fratte" with a capital L and "Francavilla in
Sinni", not "sul Sinni"; other spellings would silently match nothing.
- `basilicata`: the whole region; `potenza`: province PZ.
- `materano`: province MT less the Gallipoli Cognato park's comuni in it (Accettura, Calciano,
  Oliveto Lucano), because the 2022 bulletins count the Dolomiti Lucane among the productive areas while
  the rest of the province stayed dry.
- `ovest_sud`: 60 comuni of the western and southern Potentino, the bulletins' "settori Ovest e Sud":
  the Tyrrhenian side and the Lagonegrese (Maratea to Latronico), the Raparo, the Val d'Agri, the
  Sellata and Arioso, the Maddalena and the Melandro, the Campanian border (Muro Lucano to Ruvo del
  Monte) and the Lucanian Pollino (Terranova di Pollino to San Paolo Albanese).
- `lucania_tirrenica`: Maratea, Trecchina, Rivello, Nemoli, Lagonegro, Lauria, the two Castelluccio and
  Latronico.
- `non_tirrenica`: both provinces less `lucania_tirrenica` and the Pollino and upper Sinni comuni the
  August 2023 rain reached.
- `basentana_bradano`: the "bassa Basentana tra Basento-Bradano e confine pugliese": Matera, Miglionico,
  Montescaglioso, Pomarico, Ferrandina, Grottole, Grassano, Bernalda.

**The sources are mostly one magazine.**
- Basilicata's local press almost never says how a season went. The research agent searched SassiLive,
  ivl24, PotenzaNews, TRM, LucaniaTV, TuttoH24, Basilicata24, Il Metapontino, Il Quotidiano del Sud, La
  Siritide, the Region's news agency and Coldiretti Basilicata (about 100 mushroom articles): lost
  pickers, poisonings, seizures, courses, Covid-era bans and event promotion. Two items carry a verdict:
  a La Siritide piece from San Severino Lucano on the late, long 2020 season, and a Coldiretti
  Basilicata note on SassiLive calling 2017 "l'annata nera ... provocata dalla siccità". Both were
  opened again here. No Basilicata mushroom festival was found cancelled or held without mushrooms.
- 12 of the 14 contrasts rest on Funghi Magazine's national bulletins alone, whose Basilicata lines come
  from readers' reports. They are usually one or two sentences, often worded for "Puglia e Basilicata"
  or the whole region, and sometimes hedge with a forecast; forecasts were never used as a side.
- The research agent opened 363 Wayback captures and 13 live pages (the live site answered a plain
  browser request, with no captcha; 11 bulletins of 2024-2025 have no capture), found 86 bulletins
  with a Basilicata line, and checked every quote by script. Every quote below was checked again here
  against the page.
- The bulletins begin in March 2018; only the Coldiretti note covers 2017, and nothing covers 2016.
  Dates are the publication dates on the page, which can be a day off the address.
- **Single sources.** Twelve contrasts rest on one outlet; `ovest_sud_october_2020_2022_vs_2023` has La
  Siritide as a second outlet for 2020, and `basilicata_october_2018_vs_2017` takes each side from a
  different outlet (FM for 2018, one Coldiretti note for 2017). Within Funghi Magazine, the higher side
  of five rests on a single bulletin: `basentana_bradano_early_september_2021_vs_2022_2023` (FM
  2021-09-04; the 09-10 line is half a forecast), `ovest_sud_vs_materano_autumn_2022` (FM 2022-11-05,
  both sides), `basilicata_late_october_2018_vs_2023` (FM 2018-10-22),
  `basilicata_2024_timing_late_may_vs_june` (FM 2024-05-30) and `ovest_sud_september_2021_vs_2019_2020`
  (FM 2021-09-10). The other eight draw on 2-4 bulletins a side.

FM is Funghi Magazine; each main source links the capture or page read.

| id | group | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|---|
| `basilicata_ovest_sud_late_august_2022_vs_2024` | porcini | west and south 2022, 15 Aug-10 Sep | same, 2024 | [FM 2022-08-26](https://web.archive.org/web/20220902074404/https://funghimagazine.it/nuovo-boom-di-porcini/amp/): "3) In terza posizione la BASILICATA", "ottime nascite in particolar modo tra Lauria e Golfo di Maratea" (FM 2022-08-18: "Ottime nascite in Cilento e Potentino"; FM 2022-09-05; lower FM 2024-08-16: "Poco è nato tra Sinni e Pollino"; FM 2024-08-30: "non sufficienti a scatenare nascite porcine") | the 2024 verdict is worded for Puglia and Basilicata together and concedes a few porcini in the west |
| `potenza_vs_materano_late_summer_2022` | porcini | province PZ 2022, 20 Aug-8 Sep | MT less the Gallipoli Cognato comuni, same window | [FM 2022-09-05](https://web.archive.org/web/20220905122706/https://funghimagazine.it/perche-nascono-tanti-funghi-tutti-insieme/): "pressoché assenti in provincia di Matera, abbondanti invece nel Potentino fin sul Tirreno" (FM 2022-08-26: "Meno favorite ... la provincia di Matera e Metapontino") | one author; MT holds only 315 woodland cells |
| `lucania_tirrenica_vs_non_tirrenica_late_august_2023` | porcini | Tyrrhenian Basilicata 2023, 18 Aug-10 Sep | the rest, less the Pollino, same window | [FM 2023-08-24](https://web.archive.org/web/20230824101516/https://funghimagazine.it/aggiornamento-nascite-porcini-24-08-2023/): "buone nascite ... nella Lucania tirrenica"; "Assenza di nascite tra Molise-Puglia e Basilicata non tirrenica" (FM 2023-09-06: "Buttata ancora buona sulla Lucania tirrenica"; FM 2023-08-17 on the rain) | "buone" is a moderate verdict, partly "aumenteranno"; 9 comuni on the higher side |
| `basentana_bradano_early_september_2021_vs_2022_2023` | porcini (summer) | bassa Basentana 2021, 30 Aug-15 Sep | same, 2022 and 2023 | [FM 2021-09-04](https://web.archive.org/web/20210922081914/https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): "una ottima buttata di Porcini estivi appena iniziata nella bassa Basentana" (FM 2021-09-10; lower FM 2022-09-05, FM 2023-08-24) | one bulletin, "appena iniziata"; few woodland cells; the Puglia contrast `arco_ionico_early_september_2021_vs_2019` uses the same line |
| `ovest_sud_october_2020_2022_vs_2023` | porcini | west and south 2020 and 2022, 5-31 Oct | same, 2023 | [FM 2023-10-12](https://web.archive.org/web/20231012124159/https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "In Basilicata, tutta, non si registrano nascite di funghi degne di nota ... ivi incluso alto Sinni e Pollino" (higher FM 2020-10-23, 2022-10-13, 2022-11-05; [La Siritide 2020-10-21](https://www.lasiritide.it/article.php?articolo=15570), San Severino Lucano: "un mese di ottobre umido e non freddo che ha permesso di prolungare la stagione dei funghi"; lower FM 2023-10-04, 2023-10-27) | the 2022 October verdict is partly a look back from 5 November; 2023-10-27 allows "qualche piccolo cenno" on the Tyrrhenian side, and its Calabria paragraph gives "Il Pollino" "alcune brevissime ma buone buttate" |
| `ovest_sud_vs_materano_autumn_2022` | porcini | west and south 2022, 10 Oct-5 Nov | MT less the Gallipoli Cognato comuni, same window | [FM 2022-11-05](https://web.archive.org/web/20221129141843/https://funghimagazine.it/aggiornamento-porcini-06-11-2022/): "i soliti settori Est rimangono all'asciutto e quindi anche senza funghi. Più fortunati i settori Ovest" (FM 2022-10-13) | one bulletin for both sides |
| `basilicata_late_october_2018_vs_2023` | porcini | whole region 2018, 12-31 Oct | same, 2023 | [FM 2018-10-22](https://web.archive.org/web/20190723060659/https://funghimagazine.it/aggiornamento-funghi-22-ottobre-2018/): "Le nascite di Neri ... non si contano tra Sardegna, Sicilia, Calabria, Basilicata e Puglia" (lower FM 2023-10-12, 2023-10-27) | the 2018 line lists five regions |
| `basilicata_october_2018_vs_2017` | porcini | whole region 2018, 12-31 Oct | same, 2017 | [SassiLive 2018-09-23](https://www.sassilive.it/economia/lavoro/con-lautunno-si-prevede-boom-di-funghi-e-tartufi-anche-in-basilicata/) (Coldiretti Basilicata): "Dopo un 2017 particolarmente negativo per gli effetti della siccità che ha lasciato a mani vuote molti appassionati ricercatori" (higher FM 2018-10-22) | Coldiretti's national template with a Basilicata quote; the 2018 side lists five regions |
| `basilicata_spring_2024_2025_vs_2023` | porcini | whole region 2024 and 2025, 12 May-2 Jun | same, 2023 | [FM 2024-05-30](https://web.archive.org/web/20240624072920/https://funghimagazine.it/aggiornamento-funghi-31-05-2024/): "Exlpoit a sorpresa per la Basilicata", "una piccola apoteosi porcina" (FM 2025-05-16 and 2025-05-30, live pages; lower FM 2023-05-18: "sembrano fermi al palo", 2023-05-25, 2023-06-01) | the 2025 pages are live, modified in 2026; the 2023 lines are regional lists |
| `basilicata_2024_timing_late_may_vs_june` | porcini | whole region 2024, 20 May-2 Jun | same year, 8-30 Jun | [FM 2024-05-30](https://web.archive.org/web/20240624072920/https://funghimagazine.it/aggiornamento-funghi-31-05-2024/) (lower FM 2024-06-14: "I bei raccolti della Basilicata sono oramai terminati da diversi giorni, resiste qualcosa tra Sirino e Pollino"; FM 2024-06-28: "letargo") | the season gates rise between the two windows, so it tests the heat rules against the calendar; the high Sirino and Pollino held on |
| `basilicata_late_june_2022_vs_2018_2024` | porcini | whole region 2022, 14-30 Jun | same, 2018 and 2024 | [FM 2022-06-24](https://web.archive.org/web/20220629220257/https://funghimagazine.it/siccita-e-funghi/): "Basilicata temporaneamente protagonista ... il resto della regione sta vivendo un piccolo exploit di nascite" (FM 2022-07-01; lower FM 2018-06-16, 2018-07-01: "ferma al palo"; FM 2024-06-14, 2024-06-28) | "piccolo exploit"; 2023 left out (porcini absent on 15 June, "moltissimi" by 23 June) |
| `ovest_sud_september_2021_vs_2019_2020` | porcini | west and south 2021, 4-20 Sep | same, 2019 and 2020 | [FM 2021-09-10](https://web.archive.org/web/20210922080423/https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/): "Nascite ancora ottime si registrano in Basilicata occidentale e sud occidentale fin sul Sinni-Pollino" (FM 2021-09-04; lower FM 2019-09-20, 2019-09-27, 2020-09-04, 2020-09-21) | the lower sides are regional lists; by 24 September 2021 porcini were "sempre più rari", so the window is short |
| `basilicata_late_august_2025_vs_2024` | porcini | whole region 2025, 18 Aug-5 Sep | same, 2024 | [FM 2025-09-04](https://web.archive.org/web/20251220154140/https://funghimagazine.it/buttata-record-2025-annata-eccezionale-per-i-porcini/): "Molise, Basilicata e Calabria travolte da un'esplosione nera e marrone" (FM 2025-08-29: "piccole buttate mordi-e-fuggi già osservate dopo Ferragosto"; lower FM 2024-08-16, 2024-08-30) | a hyperbolic editorial; the 29 August bulletin says "piccole" |
| `gallinacci_basilicata_spring_2023_normal` | gallinacci | whole region 2023, 28 May-20 Jun | same, normal | [FM 2023-06-01](https://web.archive.org/web/20230601201646/https://funghimagazine.it/aggiornamento-funghi-02-06-2023/): "Mai come quest'anno in Basilicata si sono travati ... così tanti Finferli in primavera" (FM 2023-06-15: "abbondano più che mai Finferli/Galletti"; FM 2023-06-23) | normal includes 2023; no Basilicata chanterelle record to cross-check |

There is no ovoli contrast: no source gives a Basilicata ovolo year. There are 14 contrasts: 13 porcini
and 1 gallinacci.

**Outlets that block AI agents** (robots.txt, not fetched): ANSA, Il Sole 24 Ore, and the Gallipoli
Cognato park's site (every agent). Unreachable on 2026-09-30: La Nuova del Sud (a broken redirect),
trm.tv (trmtv.it answered), the Pollino park's site, Il Mattino di Basilicata, basilicatanet.it, the
Regional Council's sites and the Vulture park's site. The AMINT forum's search is script-rendered and
returned nothing.

Candidates left out:
- **October against early November 2023** (the 2023 season starting only in November, first on the
  Tyrrhenian coast): the higher side reports an onset, with no word on abundance.
- **Late June 2023**: the bulletins contradict each other within a week.
- **Forecasts**: early September 2019 ("potrebbero avere buone nascite"), the Basentana in August 2020,
  mid-November 2022, late June 2025, the Vulture in October 2024.
- **Mid-August 2020** ("inattese nascite anche in alcune aree della Basilicata e Puglia"): no area and
  no clean lower side.
- **2026 bulletins**: outside the weather history.

**Year picture from the sources** (context, not scored):
- **2016:** no source.
- **2017:** "un 2017 particolarmente negativo per gli effetti della siccità" (Coldiretti).
- **2018:** "ferma al palo" through June, only the low Mediterranean woods; a dry July; black porcini
  "non si contano" in late October.
- **2019:** first black porcini in late May, sporadic in June; a small July flush; modest or no births
  in September, a few around Sapri, Lauria-Lagonegro and the Pollino.
- **2020:** first summer porcini in the Metapontino in June; heat in July; the Basentana in mid-August;
  a "pessima" September; a late, long autumn ("i funghi siano spuntati con grande ritardo", La
  Siritide), good to very good porcini in the west and south in late October.
- **2021:** a short June flush in the Metapontino; the bassa Basentana and the west and south-west
  "ancora ottime" in early September; drought and wind in late September and October.
- **2022:** summer porcini in late May; black porcini in late June; from mid-August "una delle migliori
  stagioni fungine degli ultimi decenni" in the west (third region in Italy), the east dry; massive
  October flushes in the west.
- **2023:** a late spring, then chanterelles "più che mai" and black porcini in mid-June; a hot, empty
  July; the Tyrrhenian side only in late August; a dry October; births from early November; chanterelles
  in December.
- **2024:** a late-May "apoteosi porcina", over by mid-June; a hot summer with almost nothing; black
  porcini ending in mid-September, then "Nascite di Porcini senza sosta in alcune zone della Lucania
  occidentale" in early October and black porcini "tra Cilento-Basilicata" in mid-October.
- **2025:** abundant black porcini by mid-May; a dry July and early August; a burst after Ferragosto.

## Places, for the intro copy

Sourced areas:
- **Porcini:** the Turkey oak of the Potentino's hills and the Gallipoli Cognato forest (black
  porcini); the beech of the Pollino (Terranova di Pollino, Viggianello, San Severino Lucano, Rotonda),
  the Sirino and Lagonegrese, the Sellata and the Maddalena (summer porcini and *B. edulis*).
  In good years the Golfo di Maratea, Lauria and Lagonegro, the Val d'Agri and the whole Appennino
  Lucano park, the Dolomiti Lucane and the Vulture; the bassa Basentana and the Metapontino's valleys
  in some Junes and Septembers.
- **Ovoli:** the oak and chestnut belt, San Severino Lucano on the Pollino. No dated Basilicata report.
- **Gallinacci:** the oak woods in early summer, the beech in late summer and autumn.
- **Seasons:** black porcini from late May, summer porcini from late May and in summer storms in the
  beech, the main season in September-November, black porcini into November and December low down.

## Open questions and hand-offs

- **The gate effect on the grid** (for the region card). Compare the Tuscan and Basilicata habitat
  and altitude gates over the 2,545 woodland cells, as Calabria and Puglia did on approximate cells:
  the grid is on the parent's data directory, not in this checkout.
- **Rain scale and gauges** (for the region card). ALSIA's Servizio Agrometeorologico Lucano has
  44 stations with near-continuous daily rain since 2000, open after registration (`bas_alsia_sal2021`);
  the Region's Centro Funzionale publishes historical station data on
  centrofunzionale.regione.basilicata.it, which refused connections on 2026-09-30. The gradient is
  steep, "intorno ai 2000 mm" on the Sirino and Lagonegrese against 500-700 mm in the Materano
  (`bas_linee_forestali2013`), and most of the sanity contrasts are west against east, so the rain scale
  matters more here than the region's size suggests.
- **The conifer plantations.** The one-code, two-woods reading of `other_conifer` rests on the median
  heights. If the Region's new forest map (due August 2027, `regions/basilicata.md`) splits Aleppo
  from black pine, the Aleppo pine belongs in `mediterranean_pine` and the black pine in
  `mountain_pine`, and the affinities above can go back to the neighbours'.
- **Small stands lumped at 1:50,000.** The Rifreddo's fir and beech are mapped as Turkey oak, Piano
  Ruggio's pine and fir as beech (`regions/basilicata.md`); *B. edulis* and *B. pinophilus* lose a
  little credit in the first, none in the second.
- **Slope and sun exposure.** Both stoppers are anchored on Tuscan grid percentiles. The Basilicata
  woodland slope median is 16.3° with 6 % of cells above 25° (`regions/basilicata.md`), close to
  Tuscany's (16.6°, p90 26.2°), so the slope stopper should behave as there.
- ***B. pinophilus*.** Kept on the Pollino evidence. A dated Basilicata find, or the Venturella et al.
  (2016) list for the Appennino Lucano park (below), would settle it.
- **Leads not read.**
  - Tagliavini O. and R. (2003, 2nd ed.), *Atlante dei funghi commestibili della Basilicata*
    (Consiglio regionale, Quaderni DR): the regional atlas of more than 200 species with habitat
    notes. The Consiglio's server (consiglio.basilicata.it) refused every connection on 2026-09-30;
    the only mirror found (tartufipollino.it) holds pages 362-373, morels, cup fungi and truffles.
    Search snippets say it lists *B. aereus* and *B. edulis* on the acid brown soils of the western
    Potentino (Montrone di Oppido Lucano, Torretta di Pietragalla, Cupolicchio di San Chirico) and the
    chanterelles and *B. edulis* in the beech and fir; not cited, as not opened.
  - Venturella G. et al. (2016), "Diversity of macrofungi and exploitation of edible mushroom
    resources in the National Park 'Appennino Lucano, Val d'Agri, Lagonegrese'", *Plant Biosystems*
    150: 1030-1037 (doi 10.1080/11263504.2014.1000997): 249 taxa with ecological notes; paywalled.
  - The Gallipoli Cognato park's species pages and picking rules (robots.txt blocks every agent).
  - The Region's rain annals and daily data on the Centro Funzionale, and the consolidated law
    archive: the Region's hosting (rsdi, centrofunzionale, atticonsiglio, consiglio) refused
    connections on 2026-09-30, as the region card found.
  - Nolè et al. (2018), the late spring frost in the Lucanian beech (*Annals of Forest Science* 75:
    83): its abstract did not load.
  - Rana et al. (2013), first Basilicata and Puglia records of fungi and myxomycetes (*Micologia e
    Vegetazione Mediterranea* 28: 57-88), was opened: its new records (from Turkey oak and beech near
    Abriola, Bella and elsewhere) include none of the six keys.

## References added for Basilicata

| id | kind | verified | used for |
|---|---|---|---|
| `bas_lr_48_1998` | institutional | verified | the picking law in force, with L.R. 43/2001 |
| `bas_ispra_raccolta_funghi2021` | institutional | verified | the law in force in April 2021; L.R. 43/2001 the only amendment |
| `bas_pn_pollino_dpr1993` | institutional | verified | picking allowed in the whole Pollino park |
| `bas_pn_appennino_lucano_dpr2007` | institutional | verified | picking allowed in the Appennino Lucano park |
| `bas_infc2015` | dataset | verified | forest area and categories |
| `bas_linee_forestali2013` | institutional | verified | climate, belts, forest types, plantations (Aleppo pine, black pine, Douglas and silver fir), fog in the holly beech |
| `bas_borghetti2024_boschi` | peer-reviewed | verified | Turkey oak 500-1,200 m, silver fir stands, west-east climate, spring frosts |
| `bas_discoverpollino_porcini` | web | verified | the Pollino's four porcini; *B. aereus* "presenza massiccia" (folklore) |
| `bas_alsia_sal2021` | web | verified | the Lucanian agrometeorological network, 44 stations since 2000 |
| `bas_fm_2020_10_23` | web | verified | October porcini in the west and south, 2020 (folklore) |
| `bas_fm_2022_08_26` | web | verified | the 2022 sequence: black porcini low first, then high; *B. edulis* rarer, on the Pollino and Sirino; the east dry (folklore) |
| `bas_fm_2022_09_05` | web | verified | the 2022 season; summer porcini and *B. edulis* in the montane woods; Potenza against Matera (folklore) |
| `bas_fm_2022_11_05` | web | verified | massive October flushes in the west, the east dry, more expected after mid-November (folklore) |
| `bas_fm_2023_06_23` | web | verified | chanterelles then black porcini in mid-June 2023 (folklore) |
| `bas_fm_2023_07_13` | web | verified | the summer gap, broken only on the high Sirino (folklore) |
| `bas_fm_2023_12_16` | web | verified | chanterelles in December 2023 (folklore) |
| `bas_fm_2025_05_16` | web | verified | abundant black porcini by mid-May 2025, in the Tyrrhenian oak woods (folklore) |
| `mushma_basilicata_forest_composition_2026` | analysis | verified | habitat areas, heights and grid shares on the Carta della Natura |
| `mushma_occurrence_check_basilicata_2026` | analysis | verified | the four records, fungi effort, heights |

Existing references the Basilicata changes lean on (all opened again):
- `ispra2018_mlg180_calabria_foreste`, `ispra2018_mlg180_pino_aleppo`,
  `ispra2018_mlg179_calabria_rimboschimenti`, `ispra2018_mlg179_pino_aleppo` (Calabria, Puglia): the
  record tables of the Calabrian side of the Pollino and the plantations.
- `ispra2019_mlg187_flora_micologica` (Puglia): national beech and chestnut record shares.
- `bosco_grande2004_caesarea_cocuzzo`, `lavorato2013_calabrone_caesarea`,
  `caroti2015_cantharellaceae_calabria` (Calabria): the ovolo's height and the chanterelle's season
  next door.
- Funghi Magazine bulletins with Basilicata lines: `funghimagazine_boletus_gallery2019`,
  `fm_sicilia_2019_05_30`, `funghimagazine_giugno2019`, `funghimagazine_aggiornamento_2018_10_22`,
  `funghimagazine_porcini_maggio2022`, `funghimagazine_aggiornamento_2023_06_02`,
  `funghimagazine_aggiornamento_2023_06_16`, `fm_sicilia_2024_05_30`, `vda_fm_2024_06_14`,
  `funghimagazine_nascite_2026_04_23`, `funghimagazine_nascite_2026_07_10`; and the general
  `funghimagazine_calendario_autunno2019`, `bmeteo_boletus_aereus`, `funghimagazine_ovolo`.
- `mushma_occurrence_check_campania_2026`: the southern mainland's record heights.
- `mushma_habitat_share_2026`: the four-level affinity scale.
