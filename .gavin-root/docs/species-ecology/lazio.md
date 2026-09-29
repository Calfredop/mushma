# Species ecology: Lazio (regional appendix to species-ecology.md)

Research date: 2026-09-28 (dates Europe/Rome, units metric). Card: `region-lazio-species.md` (child
of `region-lazio.md`). Rule files: `api/src/api/config/species/lazio/`. This appendix records how the
Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Lazio, what changed and why.
It covers **fruiting conditions only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(24 added for Lazio and 3 copied word for word from the Abruzzo and Campania branches, in one block
at the end of the file, listed at the end of this page). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every number is
a prior for the backtest; season windows, altitude bands and habitat affinities stay frozen
(`model.yaml`, `backtest.frozen_factor_kinds`).

Lazio sits between Tuscany and Umbria to the north and Campania to the south. The section [Where
Lazio follows central Italy and where it departs](#where-lazio-follows-central-italy-and-where-it-departs)
takes the card's questions one by one: the low volcanic beech, *B. aereus* in the volcanic chestnut
and oak, the summer drought on the coast.

## Summary

1. **All three groups and all six keys are kept.** The regional law sets a minimum size for
   "Boletus edulis e relativo gruppo (porcino)" and for the ovolo, bans the closed ovolo, and
   exempts "Cantharellus ... tutte le specie" from the size rule (`lr_lazio_32_1998`). iNaturalist
   has 30 porcini, 24 ovoli and 46 chanterelles from Lazio (`mushma_occurrence_check_lazio_2026`),
   more than the Marche, Abruzzo or Campania. *B. pinophilus* is the exception: no Lazio record and
   no Lazio source. It stays, as in Umbria and the Marche, because the law regulates the whole
   porcini group, the neighbouring Apennines have it, and the group score takes the max.
2. **The Lazio porcino is the summer and the black one in the low volcanic woods.** A Roman
   forager-mycologist finds *B. aestivalis* (= *reticulatus*) "sia sotto faggio che ... sotto cerro"
   at Monte Venere and "Frequente" in the oak and chestnut of the Mola di Oriolo, *B. aereus* "sotto
   cerro" (`fem_migliozzi_monte_venere2009`, `fem_migliozzi_mola_oriolo2009`, folklore). The Monte
   Rufeno reserve names *B. aereus* as its porcino (`parchilazio_monte_rufeno_funghi`). *B. aereus*
   is the best-recorded porcino in Lazio (14 records, 5 of the 8 inside a mapped wood in Turkey oak).
   *B. edulis* is the porcino of the Apennine beech and of the acid volcanic soils of the Cimini
   ("che cresce prevalentemente su terreni acidi", Lago di Vico reserve, `parchilazio_vico_funghi`).
   Its 6 Lazio records are unusable: none is inside a wood, three carry city street addresses.
3. **Lazio's woods are low and oak-dominated, with beech on top.** On the Region's forest map, as the
   grid reads it (`regione_lazio_carta_forestale2011`, `mushma_lazio_forest_composition_2026`),
   deciduous oak is 41 % of the woods (median 388 m), hop-hornbeam 16.5 %, beech 16.2 % (median 1,302
   m, to 1,915 m), chestnut 10.7 % (median 603 m, half of it on volcanic soils), holm and cork oak
   8.8 %. 41 % of the woods lie below 500 m. There is no fir wood.
4. **Five altitude bands move.** The Apennine beech reaches the tree line ("tra 1400 e 1800-1900 m"
   for the upper type; the highest Apennine tree line is on the Simbruini, `bonanomi2020_treeline`):
   - *B. edulis* and *B. pinophilus*: full to 1,800 m, 0 at 2,000 m (Tuscany 1,600 → 1,900).
   - *B. reticulatus*: full to 1,400 m, 0 at 1,700 m (Tuscany 1,100 → 1,500), because the Lazio beech
     sits about 120 m above the Marche one and the highest record is in beech at 1,433 m.
   - Gallinacci: full to 1,400 m, 0 at 1,900 m (Tuscany 1,000 → 1,700): records at 1,387-1,463 m in
     the Simbruini beech.
   - The ovolo: full to 900 m, 0 at 1,200 m (Tuscany 750 → 1,100): 5 of 21 located records at 753-943
     m.
   - *B. aereus* keeps Tuscany's band.
5. **The low volcanic beech needs no band change.** The "faggete depresse" of the Cimini, Vico,
   Allumiere and Monte Raschio (400-600 m) are small (788 ha of the map's 86,000 ha of beech lie
   below 700 m) and their porcino is *B. aestivalis*, whose band is full there. See the departures.
6. **What the habitat classes hold changes 14 affinities.** Lazio's `mixed_broadleaf` is 96 %
   hop-hornbeam on limestone, `mountain_pine` is black-pine reforestation, and
   `transitional_woodland_shrub` is broom, bramble and blackthorn scrub on abandoned land and at wood
   edges. So these move down for the acid-soil porcini and mostly for the others, as in the Marche,
   Abruzzo and Campania. Two moves rest on Lazio records: hop-hornbeam up for *B. aereus*, deciduous
   oak up for the chanterelles. Beech moves from 0 to 0.1 for the ovolo (two records in the low
   thermophilous beech). Lazio's macchia is real coastal macchia, so it keeps Tuscany's values.
7. **Season windows and weather rules are all Tuscany's.** The Lazio records and sources fit the
   Tuscan windows (September-October porcini and ovoli; chanterelles October to January on the
   coast). No Lazio study ties fruiting to rain or temperature in numbers.
8. **Evidence.** Of the 24 new sources (all opened): 1 peer-reviewed (the forest map's paper), 15
   institutional (the law, the forest map report, the soil atlas, the water plan, the park portal,
   the UNESCO beech sites, the Circeo forest, the chestnut PDO), 1 national dataset (INFC), 5 forager
   pages (folklore), and 2 our own analyses; plus the 3 shared entries.

## Lazio in brief

**Woods.** The grid reads the Region's Carta forestale su base tipologica (1:10,000, 2005-2007 imagery,
36 types in 17 categories; `regione_lazio_carta_forestale2011`, `chirici2014_carta_forestale_lazio`),
with the class mapping in `config/regions/lazio.yaml`. The shares and elevations below come from the
map itself, sampled on a 100 m lattice with Copernicus GLO-30 heights before the grid was built
(`mushma_lazio_forest_composition_2026`). The map has 619,200 ha of woods and scrub, 530,400 ha of
it woodland; INFC 2015 gives a bosco of 560,236 ha (`infc2015_lazio`).

This table is **which habitat holds which Lazio tree**:

| habitat key | Lazio forest types (map area) | share of the woods | elevation p10 / median / p90 |
|---|---|---|---|
| `deciduous_oak` | Turkey oak: Cerreta neutro-basifila collinare (58,503 ha), acidofila e subacidofila collinare (46,892), neutro-basifila submontana (17,382), acidofila submontana (8,165), Querceto a cerro e farnetto (14,387, the Hungarian oak of the coast and the Circeo); downy oak: Querceto a roverella mesoxerofilo (58,184), con cerro (13,696); Querceto a caducifoglie mediterranee xerofile (794); Querceto a farnia (64) | 41.1 % | 107 / 388 / 902 m |
| `mixed_broadleaf` | hop-hornbeam: Ostrieto mesofilo (59,253), Orno-ostrieto e boscaglie a carpinella (24,633); Bosco di forra (3,329: lime, maples, ash, hornbeam) | 16.5 % | 402 / 751 / 1,052 m |
| `beech` | Faggeta montana eutrofica (80,148), termofila e basso montana (5,368, the low "faggete depresse"), altomontana e rupestre (562) | 16.2 % | 998 / 1,302 / 1,620 m; p99 1,785, max 1,915 |
| `chestnut` | Castagneto su depositi vulcanici (27,984), dei substrati arenacei e marnosi (23,286), dei rilievi calcarei (4,804), su lave acide (368) | 10.7 % | 327 / 603 / 956 m; volcanic 497 m, sandstone 778 m |
| `evergreen_oak` | Lecceta mesoxerofila (41,468), costiera termofila (2,202), rupicola (331), con faggio (150); Sughereta con caducifoglie (2,093), costiera tipica (614) | 8.8 % | 92 / 483 / 860 m |
| `riparian` | Altri boschi igrofili (15,317), Saliceto ripariale (1,452) | 3.1 % | median 155 m |
| `mountain_pine` | Rimboschimento di pini e/o altre conifere montane (11,535): black pine, locally Douglas fir, firs, Weymouth pine | 2.2 % | 538 / 926 / 1,390 m |
| `mediterranean_pine` | Pineta di pino domestico (4,134: Castel Fusano, Castelporziano, Fregene, the Circeo), di altre specie termofile (2,546: Aleppo and maritime pine) | 1.2 % | median 66 m |
| `exotic_broadleaf` | Robinieto/ailanteto (1,201) | 0.2 % | median 300 m |
| `transitional_woodland_shrub` (not woodland) | Arbusteti temperati (64,013: broom, juniper, blackthorn, bramble and rose scrub at wood edges and on abandoned land), Boschi di neoformazione (9,859), Boscaglie a paliuro e terebinto (796) | 74,800 ha | median 445 m |
| `macchia` (not woodland) | Arbusteti a specie della macchia mediterranea (13,234: shrubby holm oak, lentisk, phillyrea, strawberry tree, heath) | 13,200 ha | median 217 m |
| `fir_spruce`, `other_conifer`, `mixed_broadleaf_conifer` | none on the map | 0 | |

INFC 2015 has the same picture by category (`infc2015_lazio`): Turkey oak and other Mediterranean
oaks 132,444 ha (23.6 % of the bosco), hop-hornbeam and hornbeam 97,974, downy, sessile and
pedunculate oak 81,764, beech 74,430 (13.3 %), other deciduous 54,024, holm oak 48,267, chestnut 35,792
(6.4 %; the map finds 56,443 ha), black and laricio pine 8,474, Mediterranean pines 7,344, cork oak
2,579, **silver fir 0**. No native fir stand is documented in Lazio.

**The woodland grid** (built by the region card on 2026-09-28, read here only; `regions/lazio.md`):
4,799 woodland cells, elevation median 726 m (p90 1,328 m, max 1,853 m; 2 % above 1,600 m), slope
median 19.3° (p90 27.1°), SoilGrids topsoil pH median 6.76 (5.94-7.50). The low beech keeps its own
cells: Monte Venere (94 % beech at 603 m), Monte Raschio (83 % at 469 m).

**Altitude belts:**

| type | altitude and where | source |
|---|---|---|
| Apennine beech | "Nel Lazio, il faggio copre quasi settantamila ettari di montagna, di solito tra gli 800 e i 1.800 metri"; montane beech "tra 900 e 1800 m", lower montane "generalmente tra 1000 e 1400 m", upper "tra 1400 e 1800-1900 m"; the altomontana type "fino al limite della vegetazione arborea"; the highest Apennine beech tree line is on the Simbruini | `parchilazio_faggio`, `regione_lazio_carta_forestale2011` pp. 53, 75, `bonanomi2020_treeline` |
| low beech ("faggete depresse") | "Boschi di bassa quota, generalmente di media e alta collina (500-800 m, eccezionalmente piccoli lembi anche a 300 m)" with hop-hornbeam, Turkey oak, chestnut and hornbeam, on water-holding pyroclastic or flysch soils; "discese fino a 500 m sui substrati vulcanici, es. Faggete di Oriolo e di Allumiere"; Monte Venere "da 570 metri fino a 853 metri"; Monte Raschio "between 400 and 550 m", about 80 ha, UNESCO since 2017; Monte Cimino about 60 ha "from the 1,054 m of the summit to 800-850 m"; also Monte Fogliano, the Tolfa and Monte Rufeno | `regione_lazio_carta_forestale2011` pp. 52-53, 76, `parchilazio_faggeta_monte_venere`, `faggetevetuste_monte_raschio`, `faggetevetuste_monte_cimino`, `parchilazio_faggio` |
| chestnut | "Interessano essenzialmente i versanti dei rilievi vulcanici", on limestone only where the soil has acidified; Monte Cimino "between 550 and 950 m"; the Castagna di Vallerano PDO "tra i 400 ed i 750 metri" on volcanic tuff; the commonest wood of the Castelli Romani ("boschi cedui monospecifici di castagno") | `regione_lazio_carta_forestale2011` p. 52, `faggetevetuste_monte_cimino`, `castagna_vallerano_dop`, `parchilazio_castelli_vegetazione` |
| Turkey oak | collinare on the volcanic plateaux (the Campagna Romana, the Sabatini, the Colli Albani), with *Erica arborea* and *Arbutus* on the Tolfa and Ceriti trachytes; submontane at the top of the Vulsini, Vicano, Sabatini and Albani volcanoes with hornbeam and "sporadico ... Fagus sylvatica", and on the Laga, Velino and Carseolani sandstone "spesso da Fagus sylvatica" | `regione_lazio_carta_forestale2011` pp. 47-48 |
| Circeo lowland forest | "oltre 3 mila ettari", "la più estesa foresta planiziaria di origine naturale in Italia", pedunculate, Turkey and Hungarian oak, holm and cork oak on the drier "lestre" | `carabinieri_foresta_circeo` |
| black pine | reforestation "Tipicamente nella fascia montana dei rilievi calcarei del Lazio (es. M. Simbruini, Serra Traversa, M. Cairo, Reatino) o substrati vulcanici (prevalentemente su M. Cimini)", and in the hop-hornbeam belt | `regione_lazio_carta_forestale2011` pp. 51, 76-77 |
| stone pine | old plantations "generalmente nell'ambito della duna consolidata e della duna antica" | `regione_lazio_carta_forestale2011` p. 54 |

**Substrate.** Two halves. The volcanic districts (Vulsini, Cimini, Vico, Sabatini, Colli Albani; 30.7 %
of the region) carry Andosols whose "orizzonti sil-andici, hanno una reazione da acida a neutra, mentre
gli orizzonti alu-andici variano da estremamente acidi ad acidi", Umbric Andosols around the Vico
and Bracciano calderas, under "castagneti da frutto e cedui, faggete, cerrete, boschi di roverella"
(`arsial_atlante_suoli2019`). The Apennines (Reatini, Simbruini, Ernici, Lepini, Ausoni, Aurunci) are
limestone with Rendzic Leptosols and Phaeozems; the Laga is sandstone. SoilGrids smooths this: every
Lazio woodland cell sits between pH 5.9 and 7.5.

**Climate** (`lazio_ptar2018`, after Blasi's phytoclimate of Lazio):
- The mountains (Terminillo, Gorzano, Meta): "P molto abbondante (1614 mm); Pest frequente e
  abbondante (277 mm)", no summer drought. The Cimini, the Vico caldera, the Colli Albani and Fiuggi:
  1,247-1,606 mm, drought absent or very weak.
- The Tolfa, Sabatini, inner Maremma and Campagna Romana: 810-1,519 mm, "un regime di aridità estiva
  che generalmente dura da due a tre mesi".
- The coast, the Agro Pontino and the low Viterbo hills: "inferiori ai 650 mm. Il periodo di aridità
  estiva è sempre presente, con una durata di circa 5 mesi"; on the Viterbo and Rome coast "P scarsa
  (593÷811 mm); Pest da 53 a 71 mm".

**Regional law.** L.R. 5 agosto 1998, n. 32, as amended up to L.R. 20/2024 (`lr_lazio_32_1998`):
- 3 kg per person per day (art. 3.1).
- Minimum cap 4 cm for the ovolo and "Boletus edulis e relativo gruppo (porcino)", none for the
  chanterelles (3.2, 3.2 bis); "vietata la raccolta della Amanita caesarea allo stato di ovolo
  chiuso" (3.4).
- A permit after a 14-hour course and a yearly contribution (art. 4); no picking at night (9.1); bans
  in integral reserves and in park areas their bodies choose (art. 10); temporary closures and, since
  L.R. 20/2024, the weekdays open to picking set by the Giunta (art. 11). The Region's page says
  picking is now allowed on every day of the week (https://www.regione.lazio.it/cittadini/agricoltura/Funghi).
- No season calendar and no altitude rule. None of it changes where or when the fungi fruit; it
  confirms the porcini group, the ovolo and the chanterelles as regional species.

## Where Lazio follows central Italy and where it departs

1. **The low volcanic beech: a real feature, handled by the summer porcino.**
   - The Cimini, Vico, the Sabatini and the Tolfa hold beech far below the Apennine belt: Monte
     Raschio at 400-550 m, Allumiere at 500-630 m, Monte Venere from 500-570 m, Monte Cimino above
     800-900 m. The map's low type is "Boschi di bassa quota ... (500-800 m ...)", mixed with
     hop-hornbeam, Turkey oak, chestnut and hornbeam.
   - It is small: 788 ha of the map's 86,000 ha of beech lie below 700 m, 3,322 ha below 900 m; 12
     woodland cells below 700 m are mostly beech.
   - Its fungi, in the one Lazio account that names them, are *B. aestivalis* under beech and Turkey
     oak "nei mesi di giugno, settembre ed ottobre", *B. aereus* and the ovolo under Turkey oak
     (Monte Venere), and "boleti del gruppo edulis" with "in quantità galletti" (Allumiere) (forager-
     mycologist, folklore).
   - With the Lazio bands the low beech gets full altitude credit for *B. reticulatus* (full from 150
     m), the ovolo (to 900 m) and the chanterelles (no lower limit). *B. edulis* scores 0.4-0.9 on it
     (Tuscany's 200 → 700 m ramp, kept: only the Lago di Vico reserve names *B. edulis* there, the
     forager-mycologists find *B. aestivalis*, and its Lazio records are unusable), *B. pinophilus*
     0.2-0.7. The porcini group is full there through *B. reticulatus*.
   - Two ovolo records fall inside the low thermophilous beech type, so beech moves from 0 to 0.1 for
     the ovolo: an allowance for those mixed woods, not a host.
2. ***B. aereus* in the volcanic chestnut and oak: yes, and mostly in the oak.**
   - Its 14 records run 26-937 m (median 384 m), in the Sabatini (Canale Monterano 3, Manziana,
     Trevignano), the Tolfa, the Vulsini (Acquapendente, Farnese), the Cimini (Canepina), the Colli
     Albani (Artena), the Rome coast and the Simbruini (Trevi nel Lazio).
   - Inside a mapped wood: Turkey oak 5, hop-hornbeam and ravine wood 2, chestnut 1. The lore agrees:
     "porcini di quercia" at Manziana, "sotto cerro" at Monte Venere; Monte Rufeno names it.
   - Chestnut is already a full host in Tuscany, and oak and macchia too. What changes is
     hop-hornbeam, up from 0.3 to 0.6 on the two records and on Marche evidence.
   - Tuscany's windows fit: September is its month (7 of 14, 3.9× the Lazio fungi effort), November
     its tail (3; the lowland window is full to 15 November and closes on 15 December).
3. **The summer drought on the coast: yes, and the weather rules already make it.**
   - The coast and the low hills get under 650 mm with about five dry months; the Cimini and the
     Apennines almost none (`lazio_ptar2018`). A forager page has the Tyrrhenian macchia of "Toscana
     e del Lazio" fruit "da novembre in avanti" (`bmeteo_macchia_mediterranea2025`, folklore).
   - The Lazio records show it: no ovolo in June or July, chanterelles mostly October-January on the
     coast (two January records at 48 and 243 m), porcini in September-November.
   - As in Tuscany, no calendar gap is written into the season windows: the rain, drought, heat and
     drying rules make it. The porcini 30-day rain is scored against each cell's own normal, so it
     adapts; the absolute ovoli and gallinacci ramps are full less often in a coastal summer.
   - The coast is the same Tyrrhenian coast Tuscany's windows were set on (the Maremma continues into
     the Viterbo coast), so the *B. aereus* lowland window is not stretched to January as Campania's
     was.
4. **The Apennine beech to the tree line: yes, as in Abruzzo and Campania.** The Lazio beech is
   higher than the Marche's (map median 1,302 m, p90 1,620 m, against 1,181 m on the Marche grid) and
   reaches 1,800-1,900 m. Five bands move up (Summary, point 4).
5. **Spring and early summer: as central Italy.** A forager page times the first spring porcini the
   same way in "Toscana, Lazio, Umbria e Campania", "dalla metà di maggio", *B. aestivalis* first
   (`bmeteo_porcini_maggio2026`). The Lazio *B. reticulatus* records run May-July and September-
   October, the chanterelles have a few February-June records: Tuscany's windows are kept.

## Occurrence cross-check (Lazio)

Queried 2026-09-28 (`mushma_occurrence_check_lazio_2026`):
- **iNaturalist**: place 8670 ("Lazio, IT"), verifiable records. Locations used only for open
  records accurate to 1 km or better; elevations from the Open-Meteo elevation API; the comune
  (ISTAT 2025) and the Carta forestale type at each located record.
- **GBIF**: `gadmGid=ITA.8_1`, `MATERIAL_SAMPLE` rows excluded. Apart from iNaturalist copies it
  holds only herbarium specimens (1 ovolo, 5 *Cantharellus*, 2020-2022).
- Aggregates only; no coordinates are stored.

Lazio has 11,498 iNaturalist fungi records (Tuscany 19,089, Campania 4,437), 90 % of them from 2020
on, with an April peak (15 % of the year's records) besides the autumn one.

| taxon | n | J | F | M | A | M | J | J | A | S | O | N | D | located: median (range) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 6 | | | | | | | | 1 | | 5 | | | none usable (see below) |
| *B. reticulatus* | 10 | | | | | 1 | 2 | 1 | | 4 | 2 | | | 654 m (75-1,433), n=9 |
| *B. aereus* | 14 | | | | | | 1 | | | 7 | 3 | 3 | | 384 m (26-937), n=14 |
| *B. pinophilus* | 0 | | | | | | | | | | | | | |
| *A. caesarea* | 24 | | | | | | | | 1 | 10 | 13 | | | 418 m (25-943), n=21 |
| *Cantharellus* | 46 | 2 | 1 | | 3 | 2 | 2 | | 1 | 9 | 16 | 8 | 2 | 348 m (5-1,463), n=38 |
| all fungi (share, %) | 11,498 | 4 | 5 | 5 | 15 | 7 | 6 | 4 | 4 | 13 | 16 | 14 | 7 | |

Enrichment (the taxon's monthly share ÷ the fungi share): the three porcini with records 2.9× in
September and 2.1× in October; the ovolo 3.3× and 3.4×; the chanterelles 1.5× in September, 2.2× in
October, 1.2× in November, about 1× in January.

The chanterelles are *C. cibarius* 22, *C. pallens* 9, *C. alborufescens* 3, *C. ferruginascens* 2
and 10 at genus level: the Mediterranean segregates Tuscany found (`olariaga2017`).

Where the located records fall on the forest map (inside a polygon; in brackets, within 250 m):

| taxon | deciduous oak | chestnut | beech | holm/cork oak | hop-hornbeam, ravine | scrub | other |
|---|---|---|---|---|---|---|---|
| *B. edulis* (5) | (2) | | | | | (1) | no wood within 250 m: 2 |
| *B. reticulatus* (9) | (1) | 2 (1) | 1 (July, 1,433 m) | | 1 (1) | (1) | none: 1 |
| *B. aereus* (14) | 5 (2) | 1 | | | 2 | (2) | riparian (1), none: 1 |
| *A. caesarea* (21) | 7 (2) | 4 (1) | 2 (low thermophilous type) | 2 | | (1) | stone pine (2) |
| *Cantharellus* (38) | 10 (6) | 4 (1) | 2 (montane, 1,387-1,463 m) | 4 (3) | 2 | 3 | none: 3 |

What the records show:
- **More than the neighbours, still too few to tune.** They confirm the months, the oak and chestnut
  hosts and, for the ovolo and the chanterelles, higher belts than Tuscany's.
- **The *B. edulis* records are not usable.** Three carry street addresses in Rome, Latina and
  Viterbo, and none of the five located lies inside a mapped wood: they were photographed away from
  where they were picked.
- **Observer effort sits near Rome.** The Sabatini (Canale Monterano, Manziana, Bracciano,
  Trevignano) and the Rome coast hold many records; the Apennines few.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Which porcino** (plausible / folklore). The law names the group
  (`lr_lazio_32_1998`). *B. aestivalis*: "Frequente" in the Mola di Oriolo's oak and chestnut, "è un
  po' più raro il Boletus aereus" there; at Monte Venere "relativamente facile riempire il canestro di
  porcini (Boletus aestivalis)" under beech and Turkey oak, "Più frequente, ma sotto cerro, Boletus
  aereus" (`fem_migliozzi_mola_oriolo2009`, `fem_migliozzi_monte_venere2009`). *B. aereus*: "il
  porcino (Boletus aereus Bull.)" of Monte Rufeno (`parchilazio_monte_rufeno_funghi`); "15 porcini di
  quercia", "gli aereus di cerro" at Manziana in August 2011 (`fem_macchia_grande_manziana2011`).
  *B. edulis*: "il ricercato porcino (Boletus edulis), che cresce prevalentemente su terreni acidi"
  in the Lago di Vico reserve (`parchilazio_vico_funghi`); at Allumiere "boleti del gruppo edulis"
  in the low beech (`fem_migliozzi_faggeto_allumiere2008`). *B. pinophilus*: nothing.
- **Hosts** (plausible). Turkey oak for *B. aereus* and *B. aestivalis*, beech for *B. aestivalis*
  (above); the records' habitats (Occurrence cross-check).
- **Season** (folklore). The Mola di Oriolo oak woods fill with russules "Già dalla fine del mese di
  Aprile e fino ai primi giorni di Novembre, salvo il periodo siccitoso estivo", and porcini come "In
  autunno"; *B. aestivalis* at Monte Venere "nei mesi di giugno, settembre ed ottobre"; "una stagione
  micologica abbastanza lunga (dalla primavera all'inverno)" there.
- **Hop-hornbeam and black pine** (plausible, from neighbours). No Lazio source puts porcini in
  either. The Marche evidence applies to the same limestone: Marche mycologists name carpino nero
  for the summer and black porcini (`camm_massi_polidori2022`), a forager magazine finds the acid-soil
  porcini "quasi sempre assenti" in calcareous hop-hornbeam (`funghimagazine_carpino_nero2026`), the
  Sibillini black-pine plantations give *Suillus*, not porcini (`camm_carassai2016`), and planted
  black pine holds few, conifer-specific partners (`mrak2025_mycorrhiza`).

**Decisions.**

| key | factor | Tuscany | Lazio | why | confidence |
|---|---|---|---|---|---|
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | 200 → 700 … **1,800 → 2,000** | the host beech to the tree line ("tra gli 800 e i 1.800 metri"; map p99 1,785 m, max 1,915 m; 11.7 % of it above 1,600 m); the highest Apennine tree line on the Simbruini | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | 96 % hop-hornbeam on limestone; "più rari ... a causa di suoli calcari" (magazine) | plausible (weak) |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.3** | black-pine plantations on limestone, some fir: as Abruzzo | plausible (weak) |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | broom, bramble and blackthorn scrub | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,400 → 1,700** | fruits in the Apennine beech; Lazio beech median 1,302 m vs Marche 1,181 m (Marche band 1,300 → 1,600); record in beech at 1,433 m in July | plausible |
| *reticulatus* | habitat `mountain_pine` | 0.6 | **0.3** | black-pine plantations, no Lazio report | plausible (weak) |
| *reticulatus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | scrub at wood edges and on abandoned land | plausible |
| *aereus* | habitat `mixed_broadleaf` | 0.3 | **0.6** | 2 of 8 in-wood records in hop-hornbeam and ravine wood; "cerro, castagno, carpino nero" (Marche mycologists) | plausible |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | scrub; 2 records within 250 m, none inside | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | 300 → 800 … **1,800 → 2,000** | as *B. edulis* | plausible (weak) |
| *pinophilus* | habitat `mixed_broadleaf` | 0.3 | **0.1** | calcareous hop-hornbeam | folklore to plausible |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **0.3** | black pine on limestone, not Scots pine | plausible (weak) |
| *pinophilus* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | scrub | plausible |
| all four | season, weather, stoppers, growth clock | — | kept | the records and the lore fit; no regional numbers | as Tuscany |

Kept on purpose:
- ***B. edulis*'s low end** (0 at 200 m, full from 700 m): the low beech scores through *B.
  reticulatus* (see the departures). Lowering it would give *B. edulis* full credit in the whole
  low volcanic chestnut, where no Lazio source puts it.
- ***B. aereus*'s band** (full to 800 m, 0 at 1,250 m): 13 of 14 records below 800 m, the highest
  at 937 m on the ramp.
- ***B. aereus*'s beech 0.1**: at Monte Venere it grows "sotto cerro", not under the beech.
- **Macchia 1.0 for *B. aereus***: Lazio's macchia is the coastal shrubland of holm oak, lentisk,
  phillyrea, strawberry tree and heath (map p. 79).
- ***B. reticulatus*'s beech 0.6**: a half-beech cell already gets full credit.
- **The *B. aereus* lowland window** (full to 15 November, 0 by 15 December): the November records
  sit on the ramp; see the departures.

On the Lazio grid (4,799 woodland cells, read-only), with the Lazio against the Tuscan values:
- **Habitat.** The gate is full on 48 % of cells for *B. edulis* (75 % Tuscan), 49 % for *B.
  pinophilus* (77 %), 81 % for *B. aereus* (77 %) and 98 % for *B. reticulatus* (98 %). The *B.
  edulis* and *B. pinophilus* cuts fall on the 972 hop-hornbeam cells, where the group still
  scores through *B. reticulatus* and *B. aereus*.
- **Altitude.** Full on 87 % of cells for *B. reticulatus* (75 %), 53 % for *B. edulis* (51 %), 43 %
  for *B. pinophilus* (41 %).
- **The porcini group** (the max over the four keys of habitat × altitude) averages 1.00 (Tuscan
  values 0.995): the changes move which porcino wins a cell, not whether the group can score.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.** The law's ovolo rules (`lr_lazio_32_1998`); Monte Rufeno's "l'ovulo (Amanita
  cesarea)" (`parchilazio_monte_rufeno_funghi`); the Lucretili park: "Cresce sotto latifoglie,
  preferibilmente sotto quercia e castagno e in boschi misti", on a page whose address calls it "un
  fungo estivo" (`parcolucretili_amanita_caesarea`).
- **Forager lore** (folklore). "Più frequente, ma sotto cerro, Boletus aereus e Amanita caesarea" at
  Monte Venere; ovoli "In autunno" in the Mola di Oriolo's oak woods; at Manziana, on 8 August 2011,
  "sono ricominciati ad apparire gli ovoli di Amanita caesarea" after a hot summer with heavy rain.
- **Records.** 24 (August 1, September 10, October 13), all research grade, 21 located at 25-943 m
  (median 418 m): the Circeo and Sabaudia, the Rome coast, the Sabatini, the Vulsini, the Cimini,
  the Colli Albani, the Lepini, the Cicolano and the Turano valley. Inside a wood: Turkey oak 7,
  chestnut 4, low thermophilous beech 2, holm oak 2.

**Decisions.**

| factor | Tuscany | Lazio | why | confidence |
|---|---|---|---|---|
| altitude | … 750 → 1,100 | … **900 → 1,200** | 5 of 21 located records at 753-943 m (Rocca di Papa, Supino, Pescorocchiano, Nespolo, Collalto Sabino); chestnut on sandstone median 778 m (p90 1,071 m), submontane Turkey oak 802-1,022 m; zero at IUCN's "only seldom above 1200 m" (Abruzzo made the same move) | plausible |
| habitat `beech` | 0.0 | **0.1** | 2 records (September) inside the low thermophilous beech of the volcanic hills, which holds Turkey oak and chestnut; an allowance, not a host | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | broom and bramble scrub, not heath and clearings with scattered oaks; 1 record within 250 m | plausible |
| habitat deciduous oak, chestnut 1.0; evergreen oak 0.6; macchia 0.3 | — | kept | the records and "preferibilmente sotto quercia e castagno"; coastal macchia with shrubby holm oak | strong (hosts) |
| season 01-06 → 01-09 … 05-11 → 30-11 | — | kept | September and October, 3.3× and 3.4× the effort; none in June-July | plausible |
| weather rules | — | kept | no regional numbers; the coast's dry summers are in the weather | as Tuscany |

On the Lazio grid the altitude gate is full on 66 % of woodland cells (52 % with the Tuscan band),
the habitat gate on 74 % (75 %), and habitat × altitude averages 0.75 (0.66).

## Gallinacci (*Cantharellus* s.l.: "galletti", "gallinacci")

**Regional evidence.**
- **Presence and standing.** The law exempts "Cantharellus ... tutte le specie" from the size rule
  (`lr_lazio_32_1998`). Rocca Priora, in the Castelli Romani chestnut, holds a festival whose
  "Protagonista assoluto" is "il Galletto" (`parchilazio_ti_presento_il_galletto`); the Castelli's
  commonest wood is chestnut coppice (`parchilazio_castelli_vegetazione`). Monte Rufeno names "il
  galletto (Cantharellus cibarius Fr.)".
- **Forager lore** (folklore). "In autunno è possibile riempire facilmente i canestri di galletti"
  in the Mola di Oriolo's downy- and Turkey-oak woods; "in quantità galletti" in the low beech of
  Allumiere.
- **Records.** 46, with the Mediterranean segregates (*C. pallens* 9, *C. alborufescens* 3, *C.
  ferruginascens* 2). October peak, September and November next, December and January on the coast,
  a few April-June and one February. Inside a wood: deciduous oak 10 (5 in acidophilous Turkey oak),
  chestnut 4, holm and cork oak 4, temperate scrub 3, hop-hornbeam and ravine wood 2, montane beech 2
  (Simbruini, 1,387 m in October and 1,463 m in August).

**Decisions.**

| factor | Tuscany | Lazio | why | confidence |
|---|---|---|---|---|
| altitude | … 1,000 → 1,700 | … **1,400 → 1,900** | the two highest records in the Simbruini beech at 1,387-1,463 m (Tuscan band 0.45 and 0.34); Lazio beech median 1,302 m, p90 1,620 m (Abruzzo and Campania made the same move) | plausible |
| habitat deciduous oak | 0.3 | **0.6** | 10 of 25 in-wood records, 5 of them in acidophilous Turkey oak, 6 more within 250 m; "canestri di galletti" in the Mola di Oriolo oaks; a quarter of Lazio's deciduous oak is acidophilous Turkey oak on volcanics and sandstone (the Marche, Abruzzo and Campania made the same move) | plausible |
| habitat `mountain_pine` | 0.3 | **0.1** | black pine on limestone; *Craterellus*, not *Cantharellus*, in the Marche plantations | plausible (weak) |
| habitat `transitional_woodland_shrub` 0.3 | — | kept | 3 in-wood records inside its temperate scrub, the mantle of the oak woods ("generalmente costituenti il mantello di querceti caducifogli") | plausible |
| habitat beech 0.6, chestnut and evergreen oak 1.0, macchia 0.3 | — | kept | beech 0.6 already gives a half-beech cell full credit; the Castelli "galletto"; the coastal holm-oak segregates | plausible |
| seasons (lowland wraps to 25 January; mountain 1 June → 15 November) | — | kept | October peak, coastal records into January; the two mountain records in August and October | plausible |
| soil pH, lithology | disabled | kept disabled | the chanterelles sit on acid volcanic soils and on limestone alike (*C. ferruginascens* and *C. alborufescens* are calcicolous); SoilGrids pH 5.9-7.5 on the Lazio woods | plausible |
| weather rules | — | kept | no regional numbers | as Tuscany |

On the Lazio grid the altitude gate is full on 92 % of woodland cells (74 % with the Tuscan band),
the habitat gate on 97 % (93 %), and habitat × altitude averages 0.97 (0.89).

## Weather rules: why none changed

- **Rain amount and lag.** No Lazio source gives a rain amount or lag for any of the three groups.
  The lore is qualitative: a "buttata" in the Manziana oaks after "abbondanti pioggie" in a hot
  August, soon over as the ground dried (`fem_macchia_grande_manziana2011`). A Centre-South forager
  magazine asks for storms "non ... inferiori ai 30/40 millimetri, meglio se superiori ai 50" for
  summer porcini (`funghimagazine_calendario_autunno2019`), at the top of the Tuscan 10 → 30 mm ramp.
  The Tuscan rules stay.
- **Summer drought and drying.** The coast has about five dry months, the Apennines none
  (`lazio_ptar2018`). The ET0 drying and heat rules and the relative 30-day rain already encode it;
  the absolute ovoli and gallinacci ramps are full less often in a coastal summer (noted in their
  files).
- **Temperature.** No Lazio figure. The air-temperature bands, the cold-night rules and the growth
  clock read each cell's own weather, so the high beech is already slower and later.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; the region card
  checks it on the Region's SIARL agrometeo gauges (`regions/lazio.md`).
- **Slope and sun exposure.** Lazio woods are steeper than Tuscany's (median 19.3°, p90 27.1°, 18 % of
  woodland cells over 25°), but the slope stopper's mean over woodland cells is 0.992 (p10 0.972;
  Tuscany 0.994): left alone. The sun-exposure stoppers were not rechecked.

## Groups and keys

Nothing is dropped. All six keys and all three groups stay:
- Porcini, ovoli and gallinacci all have Lazio records, Lazio sources and the law's rules.
- *B. pinophilus* has no Lazio record or source (above); it stays as in Umbria and the Marche.
- `fir_spruce`, `other_conifer` and `mixed_broadleaf_conifer` are not on the Lazio map (no fir wood,
  no mixed class) but stay in the rule files, as in every region; they score no cell.

## Sanity contrasts

`lazio/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written down
on 2026-09-28, before any Lazio score existed.

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_` (read those with `--group ovoli` / `--group gallinacci`). "Normal" is the area's mean
over 2017-2025.

**15 contrasts: 13 porcini, 1 ovoli, 1 gallinacci.** Every cited page was opened, and every quoted
Italian phrase was checked against the page text by script. Every comune is an ISTAT 2025 name
inside Lazio, and every area has woodland cells on the grid of 2026-09-28 (Marino, named by the
Castelli source, has none of its own); provinces are ISTAT sigle. The areas:

| area | comuni or provinces | woodland cells |
|---|---|---|
| `simbruini_ernici` | Filettino, Vallepietra, Jenne, Subiaco, Camerata Nuova, Cervara di Roma, Trevi nel Lazio, Guarcino, Collepardo, Vico nel Lazio | 387 |
| `cimini_sabatini_tolfa` | Viterbo, Soriano nel Cimino, Canepina, Caprarola, Ronciglione, Vetralla, Oriolo Romano, Manziana, Bracciano, Tolfa, Allumiere | 325 |
| `sabatini_tolfa` | Manziana, Oriolo Romano, Bracciano, Tolfa, Allumiere | 179 |
| `cimini` | Viterbo, Soriano nel Cimino, Canepina, Vallerano, Vetralla, Caprarola, Vitorchiano | 149 |
| `terminillo_reatini` | Rieti, Cantalice, Leonessa, Micigliano, Poggio Bustone, Rivodutri | 337 |
| `reatino_velino` | Rieti, Cantalice, Micigliano, Poggio Bustone, Rivodutri, Posta, Borbona, Cittareale | 317 |
| `castelli_romani` | Lariano, Monte Compatri, Velletri, Rocca Priora, Ariccia, Nemi, Rocca di Papa, Marino | 68 |
| `alta_sabina` | Collalto Sabino, Nespolo, Collegiove | 42 |
| provinces | `rieti_frosinone` (RI, FR: 2,794), `viterbo_roma_latina` (VT, RM, LT: 2,005), `roma_latina_frosinone` (2,617), `viterbo` (546), `viterbo_frosinone_latina` (2,038), `frosinone_latina` (1,492), `lazio` (4,799) | |

**The sources.** Lazio local press rarely says how a season went: it reports giant porcini,
poisonings, fines and festivals. Most contrasts rest on Funghi Magazine's national bulletins, whose
Lazio paragraph comes from readers' reports. The rest come from local press and from the dated
outing reports of the Associazione Micologica Ecologica Romana (A.M.E.R., ameronlus.it).
- **Local press:** Tusciaweb (Viterbo; mostly readers' photos of big porcini), Viterbonews24,
  RietiLife, Castelli Notizie and Terzo Binario.
- **A.M.E.R.:** its site showed a maintenance page on the evening of 2026-09-28. The research agent
  had read and saved its pages earlier that day, and the quotes were checked against those copies.

| id | group | higher | lower | main source (second sources) | weakness |
|---|---|---|---|---|---|
| `rieti_frosinone_vs_viterbo_roma_latina_2023` | porcini | provinces RI, FR 2023, 10-24 Sep | VT, RM, LT, same | [FM 2023-09-20](https://funghimagazine.it/aggiornamento-porcini-20-09-2023/): RI and FR "con ottime nascite in corso, pur senza "delirio""; VT, RM, LT "con nascite di Porcini scarse ma presenti" ([FM 2023-08-24](https://funghimagazine.it/aggiornamento-nascite-porcini-24-08-2023/): "Nel Lazio poco o nulla sta nascendo, salvo qualche sporadico ritrovamento tra Simbruini e confine Abruzzo-Frusinate") | the bulletin's tiers are its editor's judgement; province level; RM also holds the Simbruini |
| `simbruini_ernici_vs_tuscia_2023` | porcini | Simbruini-Ernici 2023, 30 Sep-14 Oct | Cimini, Sabatini, Tolfa, same | [FM 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "Qualche Porcino si raccoglie ancora sui soliti Monti Simbruini"; in the Viterbese "erano più i cercatori che non i Porcini nati", "Oriolo Romano-Tolfetano ormai sono terra bruciata" ([FM 2023-10-04](https://funghimagazine.it/aggiornamento-porcini-04-10-2023/): "Molto meglio il solito Frusinate montano"; [FM 2023-10-27](https://funghimagazine.it/aggiornamento-porcini-27-10-2023/): "tolte poche fortunate aree del Lazio interno tra Reatino e Frusinate") | one outlet; the higher side is modest and crowded; "terra bruciata" is partly picking pressure |
| `sabatini_tolfa_2023_timing` | porcini | Sabatini-Tolfa 2023, 30 Oct-15 Nov | same year, 1-20 Oct | [FM 2023-11-09](https://funghimagazine.it/aggiornamento-porcini-09-11-2023/): "le nascite di Porcini si registrano in quasi tutto il Lazio, ad eccezione delle zone montane superiori" (lower side FM 2023-10-12 above; A.M.E.R. 2023-10-12: "la situazione climatica non è favorevole alla produzione fungina"; A.M.E.R. Oriolo Romano 2023-11-19: "il prelibato Boletus aereus") | the November line is region-wide; the Oriolo report shows porcini present, not abundant; *B. reticulatus* ramps down from 30 September, but *B. aereus* and *B. edulis* are fully in season in both windows |
| `roma_latina_frosinone_vs_viterbo_2020` | porcini | RM, LT, FR 2020, 20 Sep-10 Oct | VT, same | [FM 2020-10-08](https://funghimagazine.it/aggiornamento-meteofunghi-08-10-2020/): "Il Viterbese per esempio è rimasto a secco non in termini di pioggia, quanto di nascite"; "Molto meglio le province di Roma, Latina e Frosinone con nascite che ... continuano ormai da settimane" ([Tusciaweb 2020-10-13](https://www.tusciaweb.eu/2020/10/girando-boschi-funghi-non-si-trovano-limmondizia-si/), a reader: "i funghi non si trovano ma l'immondizia sì") | province level; one outlet |
| `reatino_2020_timing` | porcini | Terminillo-Reatini 2020, 8-27 Sep | same year, 30 Sep-10 Oct | FM 2020-10-08: "parte del Reatino ... ha avuto ottime nascite fin quasi a fine Settembre per poi vedere un lunghissimo riposo vegetativo" ([FM 2020-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2020/): "Meglio verso il Terminillo", a forecast) | "parte del Reatino" is vague; *B. reticulatus* ramps down from 30 September, so the gate favours September a little |
| `viterbo_frosinone_latina_september_2019` | porcini | VT, FR, LT, normal, 1-20 Sep | same, 2019 | [FM 2019-09-20](https://funghimagazine.it/dove-stanno-nascendo-i-funghi-porcini-le-piogge-cadute-in-italia/): "Lazio decisamente sfortunato quest'anno"; "Il Viterbese soffre in silenzio ... così come anche il Frosinate o l'Agro Pontino" ([FM 2019-09-12](https://funghimagazine.it/la-grande-buttata-di-funghi-porcini-di-settembre-dove-piovuto-in-italia/): in the Viterbese "è sì piovuto ma non a sufficienza"; A.M.E.R. Cori 2019-09-19: "la siccità delle settimane precedenti ha in parte compromesso la raccolta") | one outlet; "normal" includes 2019 |
| `basso_lazio_2021_timing` | porcini (summer) | FR, LT 2021, 20 Aug-4 Sep | same year, 10-30 Sep | [FM 2021-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): "ottime nascite di funghi Porcini estivi del LAZIO", "di breve durata", "nel Basso Lazio c'è stato chi si è divertito" ([FM 2021-09-10](https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/): "ormai le buttate sono quasi del tutto terminate", "Bollino rosso per ... quasi tutto il Lazio"; [FM 2021-09-24](https://funghimagazine.it/aggiornamento-meteofunghi-24-09-2021-funghi-porcini-situazione-italia/): "calma piatta") | "Basso Lazio" read as FR and LT; the lower side is region-wide |
| `castelli_romani_2022_timing` | porcini | Castelli Romani 2022, 18 Aug-5 Sep | same year, 1 Jul-12 Aug | [Castelli Notizie 2022-08-23](https://www.castellinotizie.it/2022/08/23/raccolta-funghi-in-tanti-nei-boschi-dei-castelli-romani-a-caccia-di-porcini-e-ovuli/): the rains "hanno interrotto la lunga estate di prolungata siccità", "la prima "finestra" per i fungaioli", "In molti sono ritornati a casa coi canestri pieni" | the July side is inferred from the drought; one local outlet; `castelli_romani` is small (68 cells) |
| `reatino_velino_2022_2021` | porcini | Reatino and alto Velino 2022, 10-25 Sep | same, 2021 | [RietiLife 2022-09-20](https://www.rietilife.com/2022/09/20/giorni-fortunati-per-la-raccolta-porcini-nel-reatino-eccone-un-altro-da-quasi-2-kg/): "Sono giorni fortunati per la raccolta porcini nel Reatino", "nella zona di Poggio Bustone e nell'Alta valle del Velino" ([RietiLife 2022-09-17](https://www.rietilife.com/2022/09/17/fungo-porcino-da-record-nei-boschi-di-poggio-bustone/); 2021: FM 2021-09-10 and 2021-09-24 above) | the 2022 side rests on big-porcino stories; the 2021 side is region-wide and about the Sabina |
| `cimini_2022_2024` | porcini | Cimini 2022, 5-29 Sep | same, 2024 | [Viterbonews24 2024-09-29](https://www.viterbonews24.it/news/funghi-nella-tuscia,-una-stagione-che-si-fa-attendere_142571.htm): "i cercatori locali ancora non vedono i risultati sperati", in "San Martino al Cimino, Canepina, Vetralla e dintorni" (2022: [Tusciaweb 2022-09-11](https://www.tusciaweb.eu/2022/09/trovato-un-porcino-oltre-2-chili/), [2022-10-03](https://www.tusciaweb.eu/2022/10/due-chili-porcini-trovati-tutti-insieme-sui-cimini/): "quando il castagno ha dato tutto, grazie anche alla pioggia, e tocca alla quercia") | the 2022 side is readers' finds |
| `reatino_vs_cimini_2024` | porcini | Terminillo-Reatini 2024, 12-29 Sep | Cimini, same | Viterbonews24 2024-09-29: "Nelle zone vicine, come quelle di Rieti, Terni ... la stagione è già iniziata alla grande, con raccolte abbondanti. Qui, invece, si aspetta ancora con pazienza" (A.M.E.R. Collegiove 2024-09-14: "sia porcini (Boletus aereus) sia ovoli ... sia galletti"; [FM 2024-09-27](https://funghimagazine.it/aggiornamento-nascite-funghi-27-09-2024/): "ancora festa grande in ... Lazio") | "Rieti" is loose (city or province); [FM 2024-09-19](https://funghimagazine.it/aggiornamento-nascite-funghi-19-09-2024/) had "Porcini per ora scarsi" for Lazio; shares its lower side with `cimini_2022_2024` |
| `lazio_early_september_2025` | porcini | whole region 2025, 30 Aug-20 Sep | same, normal | [FM 2025-09-04](https://funghimagazine.it/buttata-record-2025-annata-eccezionale-per-i-porcini/): "Lazio e Toscana superstar. Nel Lazio non serve affannarsi: funghi ce ne sono per tutti, anche se non proprio ovunque"; "castagni, cerri, querce e carpini sono in piena buttata" ([FM 2025-08-29](https://funghimagazine.it/aggiornamento-nascite-funghi-29-08-2025/): "la pioggia del 21 agosto ha innescato le condizioni ideali"; [3BMeteo 2025-10-09](https://funghi.3bmeteo.com/ottobre-2025-che-fine-hanno-fatto-i-funghi/): September "esplosioni" of *B. aereus*, *B. aestivalis*, *A. caesarea* in "il Lazio" among others; [RietiLife 2025-09-21](https://www.rietilife.com/2025/09/21/terminillo-trovato-un-porcino-da-record-quasi-3-chili-di-peso/), Terminillo) | hyperbolic register; region-wide; "normal" includes 2025 |
| `viterbo_october_2016_2020` | porcini | VT 2016, 1-13 Oct | same, 2020 | [Terzo Binario 2016-10-17](https://www.terzobinario.it/raccolta-funghi-nel-parco-bracciano-martignano-partono-le-multe/): "L'autunno 2016 si sta rivelando un'ottima stagione per la raccolta di funghi ed in particolare porcini" (Tusciaweb readers' 2 kg porcini at Soriano nel Cimino, Barbarano Romano, Capranica and Canino, 5-13 Oct 2016; 2020: FM 2020-10-08 above) | 2016 rests on readers' finds and the neighbouring Bracciano-Martignano park, partly in RM; 2016 is the first season of the weather history |
| `ovoli_sabatini_tolfa_october_2016_2024_2023` | ovoli | Sabatini-Tolfa 2016 and 2024, 1-12 Oct | same, 2023 | FM 2023-10-12: "non si trova praticamente più nulla, neppure gli Ovoli, per lo più raccolti ancora immaturi", "Oriolo Romano-Tolfetano ormai sono terra bruciata" (Terzo Binario 2016-10-17: "porcini ... e ovoli (Amanita cesarea)"; A.M.E.R. Manziana 2024-10-05: a wood "estremamente umido", "la ricercatissima A. caesarea") | the 2024 side shows presence, not abundance; the 2023 shortfall is partly picking pressure, and FM 2023-09-20 had ovoli already in mid-September 2023 ("nel Lazio, già si trovano gli Ovoli") |
| `gallinacci_alta_sabina_june_2023_2018` | gallinacci | Collalto Sabino, Nespolo, Collegiove 2023, 12-30 Jun | same, 2018 | [A.M.E.R. Collalto Sabino 2023-06-18](https://www.ameronlus.it/blog/2023/06/30/report-uscita-collalto-sabino-18-giugno-2023/): "le intense piogge di questo mese", "veramente tante specie", *C. pallens* in the list ([A.M.E.R. 2018-06-30](https://www.ameronlus.it/blog/2018/06/30/report-uscita-collalto-sabino/): "scarsa produzione fungina dovuta alla secchezza causata dai forti venti", "Cantharellus ferruginascens (purtroppo pochi)") | two single-day outings; the 2018 one falls at the window's edge; small area (42 cells) |

**Season gates.** Most contrasts compare the same dates in two years or two areas, so the gate
cancels. For the timing contrasts:
- `reatino_2020_timing`: the gate favours September a little (*B. reticulatus* ramps down from 30
  September), as in the Marche and Abruzzo.
- `sabatini_tolfa_2023_timing`: the windows stop at 15 November, where the *B. aereus* and *B.
  edulis* windows are still full; *B. reticulatus* favours October.
- `basso_lazio_2021_timing` and `castelli_romani_2022_timing`: *B. reticulatus* is fully in season
  in both windows.

**Outlets that block AI agents** (robots.txt checked on 2026-09-28; nothing cited from them):
- The Citynews "Today" network (RomaToday, ViterboToday, LatinaToday, FrosinoneToday, RietiToday).
- Corriere di Viterbo and ilMeteo.it.
- ANSA, Il Messaggero, La Nazione, Il Sole 24 Ore.
- The Parco Nazionale del Circeo, Parco dei Monti Simbruini, Parco dei Monti Aurunci and parks.it
  (their robots.txt disallows all crawlers but search engines).
- Ciociaria Oggi, Latina Oggi and Civonline carry a long "bad bots" list without ClaudeBot. None of
  them is used as a source.

Tusciaweb, Viterbonews24, RietiLife, Castelli Notizie, Terzo Binario, A.M.E.R., Funghi Magazine and
3BMeteo allow them.

Candidates left out:
- **Cimini, October against late September 2024.** Readers' big porcini at Vitorchiano and the "alto
  Cimino". Its lower side would be the same Viterbonews24 piece a third time.
- **Viterbese, October against September 2019.** Readers' finds at Nepi and Ronciglione, against a
  reader's "Più immondizia che funghi" (10 Oct 2019). The September side is in
  `viterbo_frosinone_latina_september_2019` against normal.
- **"Funghi porcini, è boom di raccolta nella Tuscia"** (La Fune): the page is behind a JavaScript
  challenge and its date is unknown.
- **Ciociaria Oggi 2018-09-06, "stagione record":** Coldiretti's national wording, from a borderline
  outlet.
- **The coast.** A.M.E.R. at the Circeo (11-13 Nov 2022, "scarsa produzione fungina") has no 2023
  counterpart. A.M.E.R. at Castel Fusano (2 Nov 2024, "produzione scarsa") conflicts with Funghi
  Magazine of 8 Nov 2024.
- **2017.** No Lazio-specific statement was found.
- **Forecast-only lines** (FM 14-10-2021, 12-11-2022, 12-09-2024), and region-wide 2025 twins for
  ovoli and gallinacci from the national 3BMeteo sentence.

**Year picture from the sources** (context, not scored):
- **2016:** an excellent October in the Tuscia and the Sabatini, porcini and ovoli.
- **2017:** no Lazio source found; a national drought year.
- **2018:** thin coverage. A wind-dried late June at Collalto Sabino; varied species at Jenne and
  Monte Livata in mid-September.
- **2019:** a dry summer and a poor September across Lazio; heavy rain on 22 September; October finds
  in the Viterbese.
- **2020:** a dry August in the Viterbese. The Reatino was good through September, then stopped.
  Roma, Latina, Frosinone and the coast had weeks of births into October, and the Viterbese stayed
  below expectations.
- **2021:** a short, strong summer-porcini flush in late August, above all in the Basso Lazio. It was
  over by 10 September, with "calma piatta" in the Sabina on 24 September.
- **2022:** drought to mid-August, then full baskets in the Castelli. September was good in the
  Cimini and the Reatino.
- **2023:** almost nothing in August but the Simbruini. In mid-September Rieti and Frosinone were
  good, and Viterbo, Roma and Latina scarce. Early October was dry but for the Simbruini, the
  Frusinate montano and the alto Reatino. A broad flush came from late October on the coast and in
  the Sabatini.
- **2024:** scarce in mid-September. The Reatino was abundant by late September while the Tuscia
  waited. October brought the Cimini, and *B. aereus* and ovoli at Manziana. By 8 November Lazio
  had had about 15 days of picking.
- **2025:** a record early-September flush after the rain of 21 August ("Lazio e Toscana superstar"),
  and good results on the Terminillo on 21 September. No Lazio source covers October.

## Places, for the intro copy

Sourced areas:
- **Porcini:** the Monti Cimini (Monte Venere and Monte Fogliano above Lago di Vico); the Sabatini
  (Macchia Grande di Manziana, the Mola di Oriolo, Monte Raschio at Oriolo Romano); the Tolfa
  mountains and the Faggeto di Allumiere; Monte Rufeno; the Apennine beech of the Terminillo, the
  Simbruini and the Ernici (from the forest map and the records).
- **Ovoli:** the Turkey-oak woods of Monte Venere and Manziana, the Mola di Oriolo; Monte Rufeno; the
  Lucretili.
- **Gallinacci:** the Castelli Romani chestnut (Rocca Priora's "galletto"); the Mola di Oriolo oaks;
  the Allumiere beech; Monte Rufeno.

## Open questions and hand-offs

- ***B. edulis* in Lazio.** No usable record, one reserve page and the group name in the lore. The
  Apennine beech (Terminillo, Simbruini, Ernici, the Laga) is where it should be; a located record
  set (the ASL mycological inspectorates, the AMER exhibitions) would say whether it also fruits in
  the low volcanic beech and chestnut, which would argue for lowering its band's low end.
- ***B. pinophilus*.** No Lazio record or source; kept on the neighbours' evidence.
- **Hop-hornbeam and black pine** (18.9 % and 2.4 % of the grid's wooded area). The evidence against
  the acid-soil porcini there is the Marche's, on the same limestone.
- **The low beech.** 12 woodland cells; the ovolo's 0.1 beech allowance and *B. reticulatus*'s band
  carry it. The Monte Raschio and Monte Cimino UNESCO beech woods are small (about 80 and 60 ha).
- **The coast.** The Circeo forest, Castel Fusano and Castelporziano hold many of the ovolo and
  chanterelle records; the Quadraccia & Lunghini checklist of the Castelporziano macrofungi (1990,
  "Micoflora del Lazio II") would say more, but it is not online.
- **Leads not read.** Granito & Lunghini (2011) on the macrofungi of the Simbruini beech (Plant
  Biosystems 145: 381-396; publisher page 403, no abstract online); Blasi et al. (2010) on the
  vegetation series of Lazio (not found as a file); the Parco Nazionale del Circeo, Parco dei Monti
  Simbruini and Parco dei Monti Aurunci pages (their robots.txt disallows all crawlers but search
  engines, so they were not opened).

## References added for Lazio

| id | kind | verified | used for |
|---|---|---|---|
| `lr_lazio_32_1998` | institutional | verified | picking rules; porcini group, ovolo and chanterelles as regional species |
| `regione_lazio_carta_forestale2011` | institutional | verified | forest types, belts (beech, low beech, chestnut, Turkey oak), shrubland and plantation contents |
| `chirici2014_carta_forestale_lazio` | peer-reviewed | verified | the forest map, its areas by type |
| `infc2015_lazio` | dataset | verified | forest area and categories; no silver fir |
| `mushma_lazio_forest_composition_2026` | analysis | verified | habitat shares and elevations on the forest map |
| `mushma_occurrence_check_lazio_2026` | analysis | verified | month counts, elevations, habitats at the records |
| `parchilazio_faggio` | institutional | verified | beech 800-1,800 m and the "faggete depresse" |
| `parchilazio_faggeta_monte_venere` | institutional | verified | Monte Venere beech 570-853 m |
| `faggetevetuste_monte_raschio` | institutional | verified | Monte Raschio beech 400-550 m, 80 ha |
| `faggetevetuste_monte_cimino` | institutional | verified | Monte Cimino beech above 800-900 m; chestnut 550-950 m |
| `parchilazio_castelli_vegetazione` | institutional | verified | chestnut as the Castelli's commonest wood |
| `castagna_vallerano_dop` | institutional | verified | Cimini chestnut 400-750 m on volcanic tuff |
| `arsial_atlante_suoli2019` | institutional | verified | acid volcanic soils; limestone Apennines |
| `lazio_ptar2018` | institutional | verified | rain and summer drought by zone; beech belt |
| `carabinieri_foresta_circeo` | institutional | verified | the Circeo lowland oak forest |
| `parchilazio_vico_funghi` | institutional | verified | *B. edulis* on acid soils at Lago di Vico |
| `parchilazio_monte_rufeno_funghi` | institutional | verified | *B. aereus*, ovolo and galletto at Monte Rufeno |
| `parchilazio_ti_presento_il_galletto` | institutional | verified | the Castelli Romani chanterelle festival |
| `parcolucretili_amanita_caesarea` | institutional | verified | ovolo under oak and chestnut |
| `fem_migliozzi_faggeto_allumiere2008` | web | verified | porcini and chanterelles in the Allumiere low beech (folklore) |
| `fem_migliozzi_monte_venere2009` | web | verified | *B. aestivalis* under beech and Turkey oak, *B. aereus* and ovolo under Turkey oak (folklore) |
| `fem_migliozzi_mola_oriolo2009` | web | verified | oak and chestnut fungi, *B. aestivalis* frequent, season (folklore) |
| `fem_macchia_grande_manziana2011` | web | verified | August 2011 flush of oak porcini and ovoli at Manziana (folklore) |
| `bmeteo_macchia_mediterranea2025` | web | verified | the coastal macchia season from November (folklore) |

Copied from other branches, word for word (so the merges agree), and opened again here:
`bonanomi2020_treeline` (Abruzzo: the Apennine beech tree line, highest on the Simbruini),
`bmeteo_porcini_maggio2026` (Campania: spring porcini timing in "Toscana, Lazio, Umbria e Campania"),
`funghimagazine_calendario_autunno2019` (Campania: Centre-South rain lore, calcareous soils,
November black porcini).

Existing references the Lazio changes lean on: `camm_massi_polidori2022`, `camm_santini2007`,
`camm_carassai2016`, `funghimagazine_carpino_nero2026`, `funghimagazine_alberi_porcini`,
`mrak2025_mycorrhiza`, `mushma_marche_forest_composition_2026` (the Marche evidence on hop-hornbeam,
black pine and the summer porcino's belt), `iucn_caesarea2019` (ovolo "only seldom above 1200 m"),
`olariaga2017` (the *Cantharellus* segregates), `rt_tipi_forestali_p4` (the Tuscan beech belt).
