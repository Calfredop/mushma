# Species ecology: Campania (regional appendix to species-ecology.md)

Research date: 2026-09-27 (dates Europe/Rome, units metric). Card: `region-campania-species.md`
(child of `region-campania.md`). Rule files: `api/src/api/config/species/campania/`. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Campania, what
changed and why. It covers **fruiting conditions only**: nothing here is about edibility or
identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(31 added for Campania, in one block at the end of the file, listed at the end of this page).
Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**,
**plausible**, **folklore**. Every number is a prior for the backtest; season windows, altitude bands
and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

Campania is the first southern region. The section [Where the south departs from central
Italy](#where-the-south-departs-from-central-italy) takes the expected departures one by one.

## Summary

1. **All three groups and all six keys are kept.** Porcini, ovoli and gallinacci are common in
   Campania. The regional checklist, 25 years of fieldwork in 16 areas, puts *C. cibarius* and *B.
   edulis* in its second-highest frequency class and *B. aereus* in the 70-80 % class
   (`violante2002_campania_checklist`). The ovolo is in 11 of its 16 areas. The regional law caps
   ovoli at 1 kg a day and bans the closed ovolo (`lr_campania_8_2007`, art. 6). The picking rules
   name all four porcini (`campania_dgr179_2008_funghi`). *B. pinophilus* is the rare one: 5 areas and
   no public record, but the checklist, the regional atlas and the picking rules all have it, so it
   stays.
2. **The Campania porcino is the black one low down and the summer one high up.** The regional atlas
   (`roca2007_funghi_campania`) and a detailed Picentini forager site (Laceno.net, folklore) agree on
   the split. In the Laceno's words:
   - *B. aereus* is "l'essenza fungina principale" of the lower oak and chestnut woods, and "Assente
     sotto faggio".
   - *B. aestivalis* (= *reticulatus*) is "la qualità più diffusa del genere Boletus", and it
     "predilige il bosco di faggio", from 1,100 m to 1,600-1,700 m.
   - *B. edulis* "non è molto diffusa nella Regione Campania": the highest beech in late autumn, and
     the coldest chestnut.
3. **Summer porcini sit about 450 m higher than in Tuscany.** The located *B. reticulatus* records
   have a median of 1,118 m in Campania and 1,120 m on the southern mainland, against 649 m in Tuscany
   (`mushma_occurrence_check_campania_2026`). Every southern July record is at 1,200-1,500 m. So its
   altitude band moves up (full to 1,600 m, 0 at 1,900 m) and beech becomes a full host.
4. **The beech belt reaches the tree line.** Campania's beech runs from about 900 m to "1800-1900
   metri" (`filesi2010_serie_campania`, `campania_pfg2026`). On the habitat map it sits at a median of
   1,211 m, p90 1,453 m, max 1,874 m (`mushma_campania_forest_composition_2026`). The beech-hosted keys
   (*B. edulis*, *B. pinophilus*, gallinacci) get bands that reach it.
5. **Two season windows move.**
   - *B. aereus*'s summer/autumn handover moves from 400-600 m to 600-800 m, where half of its chestnut and
     Turkey-oak hosts are.
   - *B. aereus*'s lowland window stays full to 30 November and closes on 10 January (Tuscany 15
     December).
   - The gallinacci mountain window opens a fortnight earlier, from mid-May (Laceno, the Matese
     society).
6. **What the habitat classes hold moves 11 affinities.** Campania's woods are mapped from ISPRA's
   Carta della Natura habitat map. Its `transitional_woodland_shrub` is bramble, broom and Spartium,
   so it goes down for every key. Its `mixed_broadleaf` is hop-hornbeam, hornbeam and *Alnus
   cordata*, so it goes down for *B. edulis* and up for *B. aereus*. Beech goes up for *B.
   reticulatus* and the chanterelles, and deciduous oak goes up for the chanterelles.
7. **Weather rules are all Tuscany's.** No Campania or southern-Apennine study ties fruiting to rain or
   temperature in numbers. The regional lore (rain, then sultry heat and no wind; summer storms for
   *aereus*; "aridi mesi estivi") agrees with the Tuscan rules.
8. **Evidence is regional but thin on numbers.** Campania has only 42 iNaturalist records of the six
   keys, and GBIF adds no others. Of the 31 new sources, all opened:
   - 2 are peer-reviewed (the regional checklist and a rain study).
   - 12 are institutional (the atlas, the forest plans, the chestnut PGIs, the picking law and its
     acts, and local product sheets).
   - 1 is a vegetation monograph, 3 are datasets and 1 is a mycological society page.
   - 10 are forager, press or tourist pages (folklore), and 2 are our own analyses.

## Campania in brief

**Woods.** The region card maps Campania's woods from ISPRA and ARPA Campania's Carta della Natura
habitat map (1:25,000, 2017, CORINE Biotopes codes; `config/regions/campania.yaml`). The shares and
elevations in the table come from the map itself, sampled on a 100 m lattice with Copernicus GLO-30
heights, because the rules were drafted before the grid was built
(`mushma_campania_forest_composition_2026`). The map has 473,700 ha of woods and scrub, 420,800 ha of
it broadleaf or conifer woodland; INFC 2015 gives a bosco of 403,927 ha.

The woodland grid, built later the same day (`regions/campania.md`), agrees. It has 3,733 woodland
cells:
- **Elevation.** Median 700 m (p10 311 m, p90 1,214 m, max 1,718 m).
- **Slope.** Median 19.9° (p90 29.1°; 24 % of cells over 25°).
- **Topsoil pH** (SoilGrids). Median 6.6 (p10 6.2, p90 7.0).
- **Habitat.** Averaged over cells, the wooded area is deciduous oak 30.8 %, chestnut 20.1 %, beech
  19.2 %, mixed broadleaf 14.0 %, evergreen oak 8.4 %, transitional scrub 2.6 %, conifer plantations
  2.2 % and macchia 1.0 %. The grid drops the scrub-dominated cells, so scrub weighs less than on the
  map.

This table is **which habitat holds which Campania tree**:

| habitat key | share | Campania trees (Carta della Natura code) | median elevation (p10-p90) |
|---|---|---|---|
| `deciduous_oak` | 34.3 % | Turkey oak 41.7511 (63 %), downy oak 41.732 (37 %), Turkey oak with Hungarian oak 41.7512 | 512 m (202-833); Turkey oak 596 m |
| `chestnut` | 15.9 % | chestnut woods 41.9 (68 %), fruit orchards 83.12 (32 %) | 658 m (338-947) |
| `beech` | 13.8 % | southern Apennine beech 41.18 | 1,211 m (965-1,453), max 1,874 m |
| `mixed_broadleaf` | 10.7 % | hop-hornbeam, hornbeam, ash, maple and mixed thermophilous woods 41.8 (76 %), *Alnus cordata* 41.C1 (23 %), ravine woods, birch, aspen | 770 m (420-1,088); *A. cordata* 934 m |
| `evergreen_oak` | 7.8 % | holm oak 45.31 (63 %) and 45.32 (supra-Mediterranean, 35 %), cork oak 45.21 | 371 m (141-775) |
| `transitional_woodland_shrub` | 6.3 % | bramble 31.8A (32 %), deciduous scrub 31.81 (29 %), *Spartium* 32.A (24 %), broom 31.844 (11 %), *Genista aetnensis*, hazel and willow scrub | 630 m (229-959) |
| `macchia` | 4.9 % | silicicolous *Erica-Arbutus-Cistus* macchia 32.3 (70 %), lentisk 32.214 (11 %), calcicolous macchia 32.4 (8 %), *Cytisus* 32.215 (8 %), coastal juniper and *Euphorbia* | 236 m (85-538) |
| `mountain_pine` | 2.7 % | conifer plantations 83.31, mostly black pine (with Douglas fir and some fir) | 642 m (213-1,024) |
| `riparian` | 2.4 % | poplar 44.61 (90 %), willow, alder, plane | 181 m |
| `mediterranean_pine` | 0.7 % | stone pine 42.83, Aleppo pine 42.84, wooded dunes 16.29 | 227 m |
| `exotic_broadleaf` | 0.5 % | robinia and ailanthus 41.Lcn, exotic riparian | 276 m |
| `fir_spruce` | < 0.1 % | southern Apennine silver fir 42.15 (88 ha) | 1,075 m |
| `other_conifer` | < 0.1 % | cypress 42.A1 | 562 m |

The map has no mixed broadleaf-conifer class, so `mixed_broadleaf_conifer` is empty in Campania.
The small relict fir of the Cilento (Monte Motola, Cervati) sits inside the beech polygons. The
planted fir of the Taburno (18.64 ha of pure fir, planted from 1838;
`campania_foreste_demaniali2007`) is too small to show.

INFC 2015 (`infc2015_campania`) has the same picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| Turkey oak group | 74,644 | 18.5 % |
| downy and sessile oak | 60,934 | 15.1 % |
| beech | 56,244 | 13.9 % |
| chestnut | 55,986 | 13.9 % |
| hop-hornbeam and hornbeam | 53,030 | 13.1 % |
| holm oak | 37,485 | 9.3 % |
| other deciduous | 34,386 | 8.5 % |
| hygrophilous | 11,048 | 2.7 % |
| Mediterranean pines | 9,146 | 2.3 % |
| black and laricio pine | 5,524 | 1.4 % |
| silver fir, spruce | 0 | 0 % |

**Chestnut is the region's signature wood, and it is lower than in central Italy.** Campania's fruit
orchards are "circa un quarto della superficie nazionale" (`campania_pfg2026`, p. 32). They grow on
"suoli ... a reazione acida originati dal materiale piroclastico (ceneri, pomici e lapilli)" of
Vesuvius and Roccamonfina, and are largest at Montella, Serino, Roccadaspide and Roccamonfina. On the
habitat map the chestnut median is 658 m; the Marche's is 824 m.

**Altitude belts:**

| type | altitude (m) and where | source |
|---|---|---|
| beech | "da 900 a 1300-1400 metri" (thermophilous), above 1400-1500 m on the Picentini and in the Cilento; tree line "1800-1900 metri"; "faggete depresse ... (meno di 500 m)" at Serino, San Martino Valle Caudina, Roccamonfina; "sul Cervati la faggeta chiusa si spinge fino a circa 1800 m" | `filesi2010_serie_campania` pp. 4-5, `campania_pfg2026` p. 30 |
| beech meets Turkey oak | "a circa 900 m di quota" (Mandria); beech "a partire da circa 1000 m" (Vesolo, Cervati) | `campania_foreste_demaniali2007` |
| silver fir | with beech on the Alburni, Cervati, Motola and Picentini; the largest beech-fir stand on the north side of Monte Motola; planted on the Taburno and at Trevico | `filesi2010_serie_campania` p. 5, `campania_pfg2026` pp. 31, 38 |
| chestnut (Turkey-oak series now under chestnut) | 800-1100 m on volcanic ash (Picentini), 600-700 to 1000-1100 m, "(250) 400 e 800 metri" on siliceous rock; the Castagna di Montella PGI "dai 500 ai 1.000 metri"; the Marrone di Roccadaspide PGI above 250 m | `filesi2010_serie_campania` pp. 5-6, `castagna_montella_igp`, `marrone_roccadaspide_igp` |
| downy oak | 100-400 m on limestone; 100-200 to 400 (500) m on acid pyroclastics and flysch (Somma-Vesuvio, Cilento) | `filesi2010_serie_campania` pp. 8, 10 |
| holm oak | Cilento, Cuma-Astroni, Monte Massico, the south face of the Matese; the carbonate massifs | `campania_pfg2026` p. 33 |
| coastal pines | stone, Aleppo and maritime pine of the Domitian coast and Salerno-Capaccio, planted for the 1950s reclamation; the Castel Volturno pinewood killed by *Toumeyella* | `campania_pfg2026` pp. 41, 49 |
| black pine | reforestation on the Vallo di Diano limestone, early at the Laceno and on the Matese; Vesuvius pinewoods are *P. pinea* and *P. pinaster* | `campania_pfg2026` p. 41, `filesi2010_serie_campania` p. 8 |

Tuscany's beech belt is 900-1700 (1800) m (`rt_tipi_forestali_p4`). Campania's starts at the same
height but climbs about 100-200 m higher. Its area-weighted distribution (p10 965 m, median 1,211 m, p90
1,453 m) is the Marche's (936, 1,181, 1,449 m).

**Substrate.** The chestnut belt stands on volcanic ash, whose andosols are weakly to strongly acid at
Roccamonfina and moderately acid to neutral where the ash covers limestone. Around Vesuvius and on
Ischia the soils are weakly to moderately alkaline. The Matese, Picentini, Alburni, Lattari and
Taburno are limestone, with thin, weakly alkaline soils. The Cilento flysch is moderately acid
(`campania_sistemi_terre_250k`, `campania_pfg2009`). The Roccadaspide PGI gives Cilento chestnut
soils "pH compreso tra 4,5 e 6,5" (`marrone_roccadaspide_igp`). This is why the chestnut, the
chanterelle's and the acid-soil porcini's main host, sits on acid ground even inside limestone
massifs.

**Climate.**
- West of the Apennine chain, orographic rain reaches "maximum values up to 1700-2000 mm", falling to
  700-900 mm in the rain shadow to the east (`allocca2014_hess`). The high reliefs get "picchi sino
  a 2.200 mm annui"; the coast is "per lo più inferiori a 1.000 mm annui, di cui solo 1/3 in estate",
  with an autumn-winter maximum (`campania_pfg2009`).
- The summer is very dry. At five Centro Funzionale stations, 2001-2020 (`arpac_clima_indicatori2023`):
  - Avellino averages 1,195 mm a year, with 37 mm in July and 31 in August.
  - Salerno averages 1,196 mm, with 19 and 30 mm.
  - Napoli averages 1,058 mm, with 25 and 20 mm.
  - November is the wettest month everywhere; July and August together are 4-8 % of the year.
- The Serino chestnut PGI notes "estati con periodi anche siccitosi tra giugno ed agosto"
  (`marrone_serino_igp`).

**Regional law.** L.R. 24 luglio 2007, n. 8 (`lr_campania_8_2007`) and its implementing act DGR
179/2008 (`campania_dgr179_2008_funghi`, amended by DGR 472/2008 and 813/2010).
- **Amendments.** The consolidated text has one textual amendment: art. 20 c. 1-bis, on volunteer
  guards, added by L.R. 1/2009. L.R. 14/2015 moved the provinces' permit functions to the Region
  without amending the law (`lr_campania_14_2015`).
- **Quantity.** 3 kg per person a day, "di cui non più di chilogrammi uno delle specie Amanita
  caesarea (Ovolo buono) e Calocybe gambosa (Prugnolo)" (art. 6.1).
- **Size.** Picking the closed ovolo is banned (6.3), and so are porcini caps under 3 cm. DGR
  179/2008 names the group: "Boletus edulis (Porcino) e relativo gruppo (Boletus aereus, Boletus
  reticulatus = Boletus aestivalis, Boletus pinicola)". Chanterelle caps under 2 cm are banned too.
- **Days and hours.** Picking is allowed "tutti i giorni della settimana, da un'ora prima della levata
  del sole ad un'ora dopo il tramonto" (7.1).
- **Places.** Picking is banned in integral reserves (7.2), and "nei castagneti da frutto ... nei
  periodi in cui è in atto la raccolta delle castagne" (7.5).
- **Poor years.** The Region may lower the quantities "in presenza di particolari condizioni
  climatiche stagionali e di ridotta frequenza della crescita" (DGR 179/2008, Allegato C).
- **What it leaves out.** The law sets no season calendar and no altitude rule. None of it changes
  where or when the fungi fruit; it confirms all four porcini and the ovolo as regional species.

## Where the south departs from central Italy

The card asked for five departures from the central-Italian windows. Each verdict below is on
Campania's evidence.

1. **Earlier spring flushes: no, except for the mountain chanterelles.**
   - The atlas has *B. aestivalis* "dalla tarda primavera all'autunno", and the Roccamonfina porcino
     "matura da fine primavera ad ottobre" (`campania_pat_porcino_roccamonfina`). Both match
     Tuscany's window, which already opens in May.
   - A forager page times the first spring porcini the same way in "Toscana, Lazio, Umbria e
     Campania", "dalla metà di maggio" (`bmeteo_porcini_maggio2026`).
   - No Campania record of any of the six falls in February-May. The southern mainland has none of
     *B. reticulatus* in May (Tuscany 1 of 24).
   - The one earlier start is the chanterelle in the mountains. On the Laceno it peaks "da Maggio a
     Luglio" from the valley chestnut up to the beech (`laceno_cantharellus_cibarius`), so its
     mountain window opens a fortnight earlier.
2. **A summer drought gap: yes, and deeper, but the weather makes it.**
   - July and August bring 4-8 % of the year's rain (`arpac_clima_indicatori2023`).
   - The Matese society's season excludes "gli aridi mesi estivi" (`amicomatese_non_solo_porcini2018`).
     A forager magazine calls August summer porcini "del tutto assenti tra Centro e Sud Italia, salvo
     a quote elevate dell'Appennino" (`funghimagazine_calendario_autunno2019`).
   - Campania's all-fungi records dip to 4-5 % a month in June-August.
   - Summer storms still give flushes: in July 2026 summer porcini came "decisamente più abbondanti
     nelle faggete e nei castagneti" than in the low oak woods (`funghimagazine_nascite_2026_07_10`).
   - As in Tuscany, no calendar gap is written into the season windows: the rain, drought and heat
     rules make it. What changes is where the summer flush can score: the *B. reticulatus* band now
     reaches the beech belt.
3. **A later autumn at low altitude: yes, for *B. aereus*; the other windows already cover it.**
   - Campania's fungi records run later than Tuscany's: 27 % in November-December against 21 %.
   - Its chanterelles fall 48 % in October and 33 % in November-December, with records in December
     and January.
   - Southern *B. edulis* has 3 December records, against none in Tuscany. The only Campania *B.
     aereus* is a January record near sea level.
   - A forager magazine has black porcini under oak and chestnut "a quote entro i 6-700 mt" in
     November, and porcini "tra macchia e bosco mediterraneo al Centro-Sud Italia, anche durante
     l'imminente mese di dicembre" in mild years.
   - So the *B. aereus* lowland window now closes on 10 January (Tuscany 15 December), and its
     handover moves up to 600-800 m.
   - The chanterelle lowland window already runs to 25 January, *B. edulis* to 20 December and *B.
     pinophilus* to 15 December (the atlas: "fino all'inizio dell'inverno"); all kept.
4. ***B. aereus* commoner in chestnut: plausible, and already in the rules.**
   - It is in the 70-80 % frequency class, in 13 of 16 areas (`violante2002_campania_checklist`).
   - It is the main porcino of the lower oak and chestnut woods (`laceno_boletus_aereus`) and one of
     the two best-known porcini on Vesuvius (`oasi_vesuvio_funghi`).
   - Chestnut is already a full host for it in Tuscany. What changes is that its hop-hornbeam and
     hornbeam woods move up, and more of its chestnut gets the autumn window.
   - No source compares its frequency with central Italy's in numbers.
5. **Thermophilous keys climbing higher: yes for *B. reticulatus*, not shown for *B. aereus* and the
   ovolo.**
   - *B. reticulatus* is the clear case: Laceno 1,100 m to "1600-1700 m", records about 450 m above
     Tuscany's. Band moved to full at 1,600 m, 0 at 1,900 m.
   - *B. aereus* is "Assente sotto faggio" on the Laceno and has no Campania altitude figure. Its
     southern records show no clear rise (median 415 m, n=6, against 352 m).
   - The ovolo is "irriperibile al Lago Laceno per la quota e per le essenze arboree"; the lake lies at
     1,100 m. Its located records are at 148-306 m.
   - Both keep Tuscany's bands. They already run to 1,250 m and 1,100 m, which covers the hosts:
     chestnut p95 1,028 m, Turkey oak p95 983 m.

## Occurrence cross-check (Campania)

Queried 2026-09-27 (`mushma_occurrence_check_campania_2026`):
- **GBIF**: `gadmGid=ITA.5_1`, soil-DNA `MATERIAL_SAMPLE` rows excluded.
- **iNaturalist**: place 9703, verifiable records. Elevations come from the Open-Meteo elevation API,
  for open, non-obscured records with an accuracy of 1 km or better.
- **Southern mainland pool**: Campania, Basilicata, Calabria, Molise and Apulia, which is mostly
  Calabria.
- Aggregates only; no coordinates are stored.

Campania is thinly recorded. There are 4,437 iNaturalist fungi records (Tuscany 19,089), 94 % of
them from 2020 on. The 23 GBIF records of the six taxa are all copies of iNaturalist ones.

| taxon | iNat n | J | F | M | A | M | J | J | A | S | O | N | D | located: median (range) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 5 | | | | | | 2 | 1 | 1 | 1 | | | | 1,148 m (335-1,219), n=3 |
| *B. reticulatus* | 10 | | | | | | 2 | 2 | | 5 | 1 | | | 1,118 m (415-1,345), n=8 |
| *B. aereus* | 1 | 1 | | | | | | | | | | | | 29 m, n=1 |
| *B. pinophilus* | 0 | | | | | | | | | | | | | |
| *A. caesarea* | 5 | | | | | | | | | 3 | 1 | 1 | | 289 m (148-306), n=3 |
| *Cantharellus* | 21 | 1 | | | | | 1 | | | 2 | 10 | 6 | 1 | 319 m (10-1,184), n=15 |
| all fungi (share, %) | 4,437 | 6 | 6 | 6 | 7 | 5 | 4 | 4 | 5 | 12 | 19 | 15 | 12 | |

The chanterelles are *C. cibarius* 11, *C. pallens* 5 and *C. amethysteus* 1, plus 4 at genus level.

Elevations, located records of the southern mainland against Tuscany:

| taxon | south, median (n) | Tuscany, median (n) |
|---|---|---|
| *B. reticulatus* | 1,120 m (27) | 649 m (19) |
| *B. edulis* | 1,202 m (16) | 1,054 m (22) |
| *B. pinophilus* | 1,152 m (11) | 692 m (6) |
| *B. aereus* | 415 m (6) | 352 m (42) |
| *A. caesarea* | 328 m (7) | 364 m (32) |
| *Cantharellus* | 414 m (25) | 283 m (93) |

What the records show:
- **Too few to tune.** They confirm the months and, for the beech-belt taxa, the heights. They tune
  nothing, and the sightings backtest will have very few Campania presences.
- **The cool-climate porcini sit higher in the south.** *B. reticulatus* is the only one with enough
  records to be clear; *B. edulis* and *B. pinophilus* point the same way.
- **No sign of a rise for the ovolo and *B. aereus*.** Their samples are tiny.
- **The season ends later.** The effort and the chanterelles run into November-January.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Which porcino** (plausible to strong for presence).
  - The checklist's frequency classes put *B. edulis* just below the >90 % class and *B. aereus* in
    the 70-80 % class. Its distribution table has *B. edulis* in 14 of 16 areas, *B. aereus* 13, *B.
    reticulatus* 9 and *B. pinophilus* 5 (Matese, Alburni, Cervati, Cilento, Somma-Vesuvio)
    (`violante2002_campania_checklist`).
  - The atlas calls *B. aestivalis* "specie molto frequente" and *B. edulis* "il classico porcino
    autunnale"; *B. pinophilus* grows "a gruppi non numerosi" (`roca2007_funghi_campania`).
  - The Picentini forager site finds 3 of the 4 porcini, *B. aestivalis* the commonest
    (`laceno_boletus_aestivalis`). *B. edulis* "non è molto diffusa nella Regione Campania"
    (`laceno_boletus_edulis`).
  - The checklist's *B. edulis* spans the islands and the coast, so it probably lumps summer and
    autumn white porcini; the Laceno reading is used for habitat.
- **Hosts** (plausible / folklore).
  - Atlas: *B. aereus* "specialmente nei boschi radi di Quercus spp. e/o Castanea sativa"; *B.
    aestivalis* "nei boschi caldi di latifoglie e di conifere"; *B. edulis* "predilige climi freschi e
    luoghi non soleggiati".
  - Laceno: *B. aereus* in "bosco di querce (cerro, roverella, leccio), ma non disdegna il castagno e il
    carpino. Assente sotto faggio". *B. aestivalis* "predilige il bosco di faggio"; *B. edulis* in "i
    boschi di faggio più alti" and "nei castagneti più freddi".
  - The Partenio has "Porcini (sia di Castagno che di Faggio)", aereus and aestivalis among them, "nei
    boschi di querce della pianura, nei castagneti, nelle faggete e nelle abetaie di alta montagna"
    (`cm_partenio_porcino`).
  - Roccamonfina: "tra boschi di querce, carpini e castagni", *B. aereus*, *B. edulis* and *B.
    reticulatus* (`guideslow_porcino_roccamonfina`).
  - Vesuvius: "Porcini (Boletus aereus e Boletus reticulatus)" (`oasi_vesuvio_funghi`).
  - A forager magazine calls *B. edulis* "più rari ... nel resto del Centro-Sud Italia ... a causa di
    suoli calcari" (`funghimagazine_calendario_autunno2019`).
- **Altitude** (folklore, with the records).
  - Laceno: *B. aestivalis* "dalle faggete a 1100 m ai piedi dell'altopiano, fino ai 1600-1700 m
    delle vette più alte del Raiamgra e del Cervialto"; *B. aereus* "a quote più basse".
  - No Campania figure exists for *B. edulis* and *B. pinophilus*, beyond "i boschi di faggio più
    alti".
- **Season and weather** (plausible / folklore).
  - Atlas: *B. aereus* "dall'estate all'autunno"; *B. aestivalis* "dalla tarda primavera
    all'autunno"; *B. edulis* "dalla fine dell'estate a quasi tutto l'autunno"; *B. pinophilus*
    "dalla primavera all'autunno e fino all'inizio dell'inverno".
  - Laceno: *B. aestivalis* "a seguito di forti piogge seguite da periodi lunghi di caldo umido e
    assenza di vento". *B. aereus*: "conviene sempre visitare le località colpite dai temporali dopo
    qualche giorno di temperature afose". *B. edulis*: "soprattutto nei periodi finali
    dell'autunno".
  - Matese: porcini and galletti from "giugno e luglio", the autumn "da settembre ad inizio
    novembre" (`amicomatese_non_solo_porcini2018`).

**Decisions.**

| key | factor | Tuscany | Campania | why | confidence |
|---|---|---|---|---|---|
| *edulis* | altitude | 200 → 700 … 1600 → 1900 | 200 → 700 … **1800 → 2000** | the host beech climbs to "1800-1900 metri"; southern records median 1,202 m; almost no cell is above 1,600 m, so the change is small | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | hop-hornbeam on limestone and *Alnus cordata*; no Campania source names them for this taxon; "più rari ... a causa di suoli calcari" (magazine) | plausible (weak) |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | bramble, broom, *Spartium*: no host | plausible |
| *reticulatus* | altitude | 0 → 150 … 1100 → 1500 | 0 → 150 … **1600 → 1900** | Laceno 1,100 to 1,600-1,700 m in beech; records median 1,118 m (Campania) and 1,120 m (south), Tuscany 649 m; July records at 1,200-1,500 m | plausible |
| *reticulatus* | habitat `beech` | 0.6 | **1.0** | "predilige il bosco di faggio, dove nelle grandi buttate diventa il padrone incontrastato" (Laceno); Partenio porcini "di Faggio"; July 2026 flush "più abbondanti nelle faggete e nei castagneti" | plausible (folklore sources, consistent records) |
| *reticulatus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | bramble and broom scrub, not chestnut and oak regrowth | plausible |
| *aereus* | season: summer/autumn handover | 400 → 600 m | **600 → 800 m** | November black porcini "entro i 6-700 mt" (magazine); half of the chestnut and Turkey oak lies above 600 m | folklore |
| *aereus* | season: lowland autumn end | full to 15 Nov, 0 on 15 Dec | **full to 30 Nov, 0 on 10 Jan** | porcini "anche durante l'imminente mese di dicembre" in mild years (magazine); a January record at sea level; frost and temperature rules still stop it | folklore |
| *aereus* | habitat `mixed_broadleaf` | 0.3 | **0.6** | "non disdegna il castagno e il carpino" (Laceno), "tra boschi di querce, carpini e castagni" (Roccamonfina); the *A. cordata* quarter of the class is no host, hence not 1.0 | plausible (weak) |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | bramble and broom scrub | plausible |
| *pinophilus* | altitude | 300 → 800 … 1600 → 1900 | 300 → 800 … **1800 → 2000** | on the high limestone massifs (Matese, Alburni, Cervati), whose beech reaches the tree line; southern records 797-1,638 m | plausible (weak) |
| *pinophilus* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | bramble and broom scrub | plausible |
| all four | weather, stoppers, growth clock | — | kept | no regional numbers; the lore agrees | as Tuscany |

Kept on purpose:
- ***B. aereus*'s altitude band** (full to 800 m, 0 at 1,250 m); see the departures above.
- ***B. aereus*'s beech 0.1**: "Assente sotto faggio".
- **Macchia 1.0 for *B. aereus***: 70 % of Campania's macchia is the silicicolous
  *Erica-Arbutus-Cistus* type it fruits in.
- **`mountain_pine` 0.6 for *B. edulis*, *B. reticulatus* and *B. pinophilus***: no Campania source
  says whether porcini fruit under the black-pine plantations. The Marche lowered it on its own
  evidence; see Open questions.
- ***B. reticulatus*'s window**: no earlier start.

Effect on the 3,733 woodland cells of the grid:
- **Habitat.** The gate reaches full credit on 68 % of cells for *B. edulis* (82 % with the Tuscan
  affinities), 77 % for *B. pinophilus* (82 %), 83 % for *B. aereus* (79 %) and 98 % for *B.
  reticulatus* (unchanged). *B. reticulatus* and *B. aereus* keep the porcini group's reach.
- **Altitude.** The *B. reticulatus* gate is full on 98 % of cells, against 82 % with the Tuscan band.
  The *B. edulis* and *B. pinophilus* bands change almost nothing, because no cell is above 1,718 m.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.**
  - The regional law's 1 kg cap and closed-ovolo ban (`lr_campania_8_2007`).
  - 11 of the checklist's 16 areas, from Ischia and the Campi Flegrei to the Matese, Picentini,
    Alburni and Cervati (`violante2002_campania_checklist`).
  - The atlas: "in boschi di latifoglie specie in ambienti caldi e soleggiati"
    (`roca2007_funghi_campania`).
- **Laceno** (`laceno_amanita_caesarea`, folklore).
  - "Cresce dall'estate all'autunno soprattutto nei luoghi esposti a sud e molto caldi".
  - "nei numerosi castagneti che contornano Bagnoli Irpino, irriperibile al Lago Laceno per la quota e
    per le essenze arboree".
  - "nasce dopo piogge (non abbondanti) in periodi caldissimi e secchi"; "L'habitat ideale sono i
    boschi di castagno e quelli di quercia".
- **Records.** 5 iNaturalist: September 3, October 1, November 1, at 148-306 m. They are 5.1× the
  fungi effort in September.

**Decisions.**

| factor | Tuscany | Campania | why | confidence |
|---|---|---|---|---|
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | bramble and broom scrub, not the heath and clearings with scattered oaks that made it secondary in Tuscany | plausible |
| habitat chestnut, deciduous oak 1.0; evergreen oak 0.6; macchia 0.3 | — | kept | "boschi di castagno e quelli di quercia" (Laceno); Campania macchia is mostly *Erica-Arbutus-Cistus*, often with holm oak (the forest plan counts a "macchia mediterranea a dominanza di leccio") | strong (hosts) |
| season 01-06 → 01-09 … 05-11 → 30-11 | — | kept | September peak; the November record sits on the ramp | plausible |
| altitude … 750 → 1100 | — | kept | absent at the Laceno lake (1,100 m), where the band is already 0; no located record above 306 m | plausible |
| weather rules | — | kept | "dopo piogge (non abbondanti) in periodi caldissimi e secchi" fits the Tuscan soil-temperature and evaporative-demand rules | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "gallinacci", "galletti", "finferli")

**Regional evidence.**
- **Frequency and hosts.**
  - The atlas: "molto comune e diffuso ovunque, dai boschi collinari di latifoglie a quelli montani di
    conifere; dalla tarda primavera all'autunno", "abbondante già subito dopo i primi temporali
    estivi" (`roca2007_funghi_campania`).
  - The checklist has *C. cibarius* in 14 of 16 areas. It lists only four *Cantharellus*, none of the
    Mediterranean segregates (`violante2002_campania_checklist`); iNaturalist has *C. pallens* (5 of
    21 records).
- **Laceno** (`laceno_cantharellus_cibarius`, folklore).
  - "Nasce da Maggio a Novembre", longer in warm years, "il massimo della produzione da Maggio a
    Luglio".
  - It moves from "i castagneti della valle tra Bagnoli I. e i confini con Montella, fino ai boschi di
    Faggio tra Valle d'Acera e Piano del Cupone", where good August rain fills the basket.
  - "prediligendo il faggio e la quercia", not disdaining chestnut.
- **Matese.** Galletti "con l'avvento dei mesi estivi, giugno e luglio"
  (`amicomatese_non_solo_porcini2018`).
- **Records.** 21 iNaturalist, 48 % in October and 33 % in November-December. 3 are October finds at
  900-1,200 m; the rest are low (median 319 m). The May-July peak of the lore is barely in the
  records (one June record), which follow the autumn observer effort.

**Decisions.**

| factor | Tuscany | Campania | why | confidence |
|---|---|---|---|---|
| season: mountain window | 1 Jun → 1 Jul … 15 Oct → 15 Nov | **15 May → 15 Jun** … 15 Oct → 15 Nov | Laceno May-July peak moving up into the beech; Matese "giugno e luglio"; atlas "dalla tarda primavera" | plausible (folklore sources) |
| habitat `beech` | 0.6 | **1.0** | "prediligendo il faggio e la quercia" (Laceno), August harvests in the beech; the Marche and Abruzzo made the same move | plausible |
| habitat `deciduous_oak` | 0.3 | **0.6** | "prediligendo ... la quercia" (Laceno); atlas "dai boschi collinari di latifoglie"; deciduous oak is a third of Campania's woods | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.3 | **0.1** | bramble and broom scrub | plausible |
| altitude … 1000 → 1700 | — | … **1400 → 1900** | beech, now a full host, sits at median 1,211 m; with the Tuscan band half of it would lose 30 % or more of its credit | plausible |
| lowland window (wraps to 25 Jan), chestnut and evergreen oak 1.0, macchia 0.3 | — | kept | records into December-January; "castagneti della valle"; the holm-oak segregates are not documented in Campania but not excluded | plausible |
| soil pH, lithology | disabled | kept disabled | acid chestnut soils on volcanic ash inside limestone massifs: a lithology gate would mislabel them | plausible |
| weather rules | — | kept | "Cresce dopo abbondanti piogge, soprattutto nei punti più umidi del bosco" (Laceno) fits the Tuscan rain rules | as Tuscany |

On the grid the habitat gate is full on 98 % of woodland cells (94 % with the Tuscan affinities), and
the altitude gate on 98 % (77 %).

## Weather rules: why none changed

- **Rain amount and lag.** No Campania or southern-Apennine source gives an amount or lag in numbers,
  apart from generic Centre-South forager thresholds: summer porcini need storms of "30/40 millimetri,
  meglio se superiori ai 50", over 100 mm for mass flushes (`funghimagazine_calendario_autunno2019`).
  These sit at the top of the Tuscan 10 → 30 mm ramp and do not contradict it.
- **Drying and heat.** The regional lore matches the Tuscan drying-wind, heat-spike and cold-night
  rules: "assenza di vento" (Laceno) and dry heat for the ovolo. The ET0 thresholds were set for
  low-altitude Tuscan summers and are kept.
- **Summer drought.** It is deeper than in Tuscany. The porcini 30-day rain is scored against each
  cell's own normal, so it adapts. The absolute 30-day ramps of ovoli (25 → 75 mm) and gallinacci
  (15 → 70 mm) will simply be full less often in a Campania July, which is where the records are
  fewest.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it is a
  region-config task. The Region's agrometeorological network publishes daily rain for 2001-2025 with
  no registration (https://agricoltura.regione.campania.it/meteo/archivio_meteo.html; the site's TLS
  certificate had expired on 2026-09-27). The Centro Funzionale has 199 + 178 rain gauges, but
  whether they are open was not checked.

## Groups and keys

Nothing is dropped. All six keys have Campania evidence: the checklist, the atlas, the picking rules
and, except *B. pinophilus*, iNaturalist records. `mixed_broadleaf_conifer` is not on the Campania map
but stays in the rule files, as in every region; it simply scores no cell.

## Sanity contrasts

`campania/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written down
on 2026-09-27, before any Campania score existed.

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_` (read those with `--group ovoli` / `--group gallinacci`). "Normal" is the area's mean
over 2017-2025.

There are 13 contrasts: 11 porcini, 2 gallinacci, and no ovoli, because no Campania source judges an
ovolo year. The areas are:
- `bagnoli_laceno`: Bagnoli Irpino, Montella, Nusco, Cassano Irpino.
- `matese_casertano`: 13 comuni of the Caserta side of the Matese.
- `cilento_interno`: 36 comuni of the inland Cilento and the southern Vallo di Diano (Cervati,
  Gelbison, the Golfo di Sapri hinterland).
- `irpinia` (province AV), `salerno` (province SA) and `campania` (the whole region).

Every comune was checked against the ISTAT 2025 list (all in Campania, each area in one province);
provinces are ISTAT sigle, as the grid's `province` column holds them.

**The sources are thin, and mostly one magazine.**
- Campania local press rarely says how a season went: it reports sagre, controls and giant finds.
  Most contrasts rest on Funghi Magazine's national bulletins, whose Campania paragraphs come from
  readers' reports.
- The live site shows a captcha, so the bulletins were read through Wayback Machine captures of the
  cited URLs.
- The local sources are Palazzo Tenta 39 (Bagnoli Irpino), Irpinianews, InfoCilento (a Coldiretti
  note) and binews.
- The research agent opened every page and copied the quotes. Two were re-checked here against the
  archived pages.

| id | group | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|---|
| `laceno_2016` | porcini | Bagnoli-Laceno 2016, 15 Sep-2 Oct | same, normal | [Palazzo Tenta 39, 2016-10-02](http://www.palazzotenta39.it/public/archives/75605): "Grande annata di funghi, a Bagnoli e in tutto il comprensorio" ([Irpinianews 2016-09-25](http://www.irpinianews.it/intervista-ad-un-cercatore-funghi-irpino-un-anno-prospero/)) | a cultural association's site, inside a giant-porcino story; the second source is hedged ("potrebbe") and from other Irpinian hills |
| `salerno_2018_2017` | porcini | province SA 2018, 20 Aug-4 Sep | SA 2017 | [InfoCilento 2018-09-04](https://www.infocilento.it/2018/09/04/coldiretti-si-preannuncia-stagione-da-record-per-i-funghi/) (Coldiretti): "È boom di porcini e gallinacci in tutte le aree montane", after "un 2017 particolarmente negativo per gli effetti della siccità" | one farmers'-union note; the 2017 side is one line |
| `campania_june_2018_2024` | porcini (summer) | whole region 2018, 8-28 Jun | same, 2024 | [FM 2018-06-16](https://funghimagazine.it/aggiornamento-funghi-16-giugno-2018/): "Campania protagonista" (FM 2018-07-01; 2024 side FM 2024-06-14, 2024-06-28: "L'eccesso di calore ha mandato in letargo i miceli fungini di Campania") | region-wide national bulletin |
| `campania_september_2019` | porcini | whole region, normal, 1-25 Sep | same, 2019 | [FM 2019-09-20](https://funghimagazine.it/dove-stanno-nascendo-i-funghi-porcini-le-piogge-cadute-in-italia/): "Campania-Basilicata-Puglia con nascite ancora modeste o del tutto assenti" (FM 2019-09-27) | one outlet; "normal" includes 2019 |
| `campania_2020_timing` | porcini | whole region 2020, 1-23 Oct | same year, 25 Aug-21 Sep | [FM 2020-10-23](https://funghimagazine.it/meteofunghi-23-10-2020/): "periodo florido per la Campania" (FM 2020-10-15; lower side FM 2020-09-04, 2020-09-21: "Situazione pessima") | timing contrast from one outlet; the season gate may favour one window |
| `matese_vs_cilento_2020` | porcini (summer) | Matese casertano 2020, 28 Jul-10 Aug | Cilento interno, same window | [FM 2020-08-07](https://funghimagazine.it/aggiornamento-meteofunghi-07-08-2020/): "Ancora buona nascite nel Molise e nel vicino Matese campano. Nel resto della Campania pochissime nascite con siccità nel Salernitano" (FM 2020-07-23, 2020-07-30) | one outlet; "Salernitano" read as the inland Cilento |
| `irpinia_vs_matese_2021` | porcini | province AV 2021, 8-22 Sep | Matese casertano, same window | [FM 2021-09-24](https://funghimagazine.it/aggiornamento-meteofunghi-24-09-2021-funghi-porcini-situazione-italia/): "L'Irpinia ha dato ... Potrebbe migliorare la situazione nel Matese" ([binews 2021-09-19](https://www.binews.it/attualita/irpinia-e-fungomania-centinaia-e-centinaia-gli-amanti-dei-porcini-in-montagna-intanto-scattano-i-controlli/); FM 2021-09-04) | the Matese side is inferred from "potrebbe migliorare" |
| `campania_august_2022` | porcini | whole region 2022, 15-31 Aug | same, 2019 and 2021 | [FM 2022-08-26](https://funghimagazine.it/nuovo-boom-di-porcini/): "La CAMPANIA sta finalmente vivendo una stagione fungina come non si ricordava da tempo" (Coldiretti via Irno24 and Il Denaro 2022-09-05: "+50%"; FM 2019-08-16, 2021-08-12) | Coldiretti is a press release; the 2021 side is macro-regional |
| `cilento_vs_irpinia_2023` | porcini | Cilento interno 2023, 15-28 Aug | province AV, same window | [FM 2023-08-24](https://funghimagazine.it/aggiornamento-nascite-porcini-24-08-2023/): "poco o nulla sull'Appennino Campano ma, buone nascite ... in Cilento" (FM 2023-08-17) | one outlet; "Appennino Campano" read as Irpinia |
| `irpinia_vs_matese_2023` | porcini | province AV 2023, 1-12 Oct | Matese casertano, same window | [FM 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "Al momento nel Matese campano non stanno nascendo Porcini"; "buone quantità di Porcini estivi tra Irpinia, Taburno, Partenio, Picentini e Lattari" (FM 2023-10-04) | the Matese had a short flush just before the window |
| `cilento_vs_matese_2024` | porcini (summer) | Cilento interno 2024, 8-16 Aug | Matese casertano, same window | [FM 2024-08-16](https://funghimagazine.it/aggiornamento-funghi-16-08-2024/): "il Matese ha già dato, ora è tutto finito"; "meglio nel Cilento interno" (FM 2024-08-06) | one outlet; "Matese" may mean the Molise side |
| `gallinacci_salerno_2018_2017` | gallinacci | province SA 2018, 20 Aug-4 Sep | SA 2017 | InfoCilento 2018-09-04, as `salerno_2018_2017` | the same single note |
| `gallinacci_campania_june_2023` | gallinacci | whole region 2023, 28 May-16 Jun | same, normal | [FM 2023-06-16](https://funghimagazine.it/aggiornamento-funghi-16-06-2023/): "abbondano più che mai Finferli/Galletti" (FM 2023-06-02: "in abbondanza in Campania stessa") | region-wide; "più che mai" is rhetoric; normal includes 2023 |

**Outlets that block AI agents** (robots.txt, not fetched): ANSA, Il Mattino, the Today network
(AvellinoToday, SalernoToday, NapoliToday, CasertaNews), Cilento Notizie, Il Vescovado, Amalfi News,
Positano Notizie, Il Sole 24 Ore, La Nazione, Il Resto del Carlino. La Città di Salerno and Voce di
Strada hide their robots.txt behind a Cloudflare challenge, and Zerottonove, Le Cronache and Il
Mattino di Salerno did not answer. Coldiretti.it returns 403 on its robots.txt; the research agent
had opened two national Coldiretti pages before noticing, and neither is cited.

Candidates left out:
- **Naples area, autumn 2025.** One reader wrote twice under Funghi Magazine bulletins ("quest'anno
  da noi zero funghi"); the only source was that reader.
- **Irpinia above the Cilento, early October 2023.** The Cilento side is a forecast.
- **Any ovoli contrast.** The only Campania-specific ovoli line (Irpinian porcini "sostituiti ...
  dalle Amanite caesaree", FM 2021-09-24) shows presence, not a good or bad year.
- **Gallinacci June 2023 against June 2024.** The 2024 timing is unclear.
- **Hedged or vague pieces.** Matese and Salernitano against the Cilento in October 2020; Cilento and
  Irpinia in early November 2018; August-September 2025; Cusano Mutri 2025.
- **Single giant-porcino finds.**

**Year picture from the sources** (context, not scored):
- **2016:** a very good early autumn around Bagnoli.
- **2017:** drought.
- **2018:** a strong June; a late-August boom in the Salerno mountains; good into early November.
- **2019:** a dry August and September; rain only at the end of September.
- **2020:** an early-August flush on the Matese while the Salernitano was dry; a bad late August and
  September; massive October flushes.
- **2021:** June cut short by heat; an Irpinian and Partenio flush in September ending with ovoli.
- **2022:** June porcini, a rainy August "come non si ricordava da tempo", big flushes in September
  and October.
- **2023:** abundant chanterelles in late May and June; the Cilento in August; Irpinia, Partenio,
  Taburno, Picentini and Lattari in early October, not the Matese.
- **2024:** June heat; the Matese in early August, the Cilento in mid-August; a late-September flush
  of all four porcini.
- **2025:** short August flushes; a dry autumn around Naples.

## Places, for the intro copy

Sourced areas:
- **Porcini:** the Laceno and the Picentini around Bagnoli Irpino (Cervialto, Raiamagra, Croci di
  Acerno); the Partenio; Roccamonfina and Monte La Frascara; Vesuvius; Irpinia, the Taburno and the
  Monti Lattari; the Matese; the inland Cilento and the Salerno mountains.
- **Chestnut belt:** Montella, Serino and Monte Terminio, Giffoni, Roccadaspide, Roccamonfina.
- **Ovoli:** the chestnut groves around Bagnoli Irpino.
- **Gallinacci:** the Bagnoli-Montella chestnut and the Valle d'Acera and Piano del Cupone beech; the
  Matese.

## Open questions and hand-offs

- **Black-pine plantations (`mountain_pine`, 2.7 %).** No Campania source says whether porcini
  fruit under them. The Marche lowered them on its own evidence (Sibillini plantations with
  *Suillus*, no porcini). The Carta della Natura's 83.31 may also hold some of the Vesuvius stone-
  and maritime-pine plantations, which the vegetation series names. A look at 83.31's polygons on
  Vesuvius would settle which habitat they belong to.
- ***B. aereus* altitude and the ovolo's.** Kept at Tuscany's on thin evidence both ways. The
  Laceno says no beech, and the forager magazine sees *B. aereus* reaching 900-1,000 m in beech. A
  located Campania record set would decide.
- **Chanterelle segregates.** No Campania literature records *C. pallens*, *C. alborufescens* or
  *C. ilicis*; iNaturalist has 5 *C. pallens*. Evergreen oak stays a full host on the Tuscan
  evidence.
- **Slope and sun exposure.** Both stoppers were anchored on Tuscan grid percentiles. The slope
  stopper was checked on the Campania grid and left alone: its mean over woodland cells is 0.987 (p10
  0.945), as in the Marche (0.984).
- **Rain scale.** For the region card: the regional agrometeorological network's open daily rain is
  the obvious gauge set.
- **Few records.** 42 iNaturalist records for the six keys; the backtest will say little about
  Campania. Pooling with the southern mainland (174 records, mostly Calabria) is the next step.
- **Leads not read.**
  - Violante's Campania papers on Vesuvius, the Appennino Campano and the Valle delle Ferriere (not
    online).
  - A macrofungi study of the Cilento's old-growth beech, chestnut and oak (academia.edu, 403).
  - The Cilento park's picking regulation (loads by JavaScript).
  - The Castagna di Roccamonfina PGI text.

## References added for Campania

| id | kind | verified | used for |
|---|---|---|---|
| `violante2002_campania_checklist` | peer-reviewed | verified | frequency and distribution of the six taxa in 16 areas |
| `roca2007_funghi_campania` | institutional | verified | per-taxon season and habitat in the regional atlas |
| `laceno_boletus_aestivalis` | web | verified | summer porcino in beech, 1,100-1,700 m (folklore) |
| `laceno_boletus_aereus` | web | verified | black porcino in low oak and chestnut, absent under beech (folklore) |
| `laceno_boletus_edulis` | web | verified | *B. edulis* rare, high beech and cold chestnut (folklore) |
| `laceno_amanita_caesarea` | web | verified | ovolo around Bagnoli, not on the Laceno plateau (folklore) |
| `laceno_cantharellus_cibarius` | web | verified | galletti May-November, peak May-July, beech and oak (folklore) |
| `amicomatese_non_solo_porcini2018` | society | verified | Matese season: dry summer months, porcini and galletti from June-July |
| `cm_partenio_porcino` | institutional | verified | Partenio porcini of chestnut and beech |
| `campania_pat_porcino_roccamonfina` | institutional | verified | Roccamonfina porcino, late spring to October |
| `guideslow_porcino_roccamonfina` | web | verified | Roccamonfina hosts incl. hornbeam (folklore) |
| `oasi_vesuvio_funghi` | web | verified | *B. aereus* and *B. reticulatus* on Vesuvius (folklore) |
| `funghimagazine_nascite_2026_07_10` | web | verified | southern summer flush in beech and chestnut; *B. aereus* to 900-1,000 m in beech (folklore) |
| `funghimagazine_calendario_autunno2019` | web | verified | Centre-South rain lore, August gap, November and December porcini (folklore) |
| `bmeteo_porcini_maggio2026` | web | verified | spring porcini timing, Campania with Tuscany (folklore) |
| `infc2015_campania` | dataset | verified | forest area and categories |
| `campania_pfg2026` | institutional | verified | beech, chestnut, oak, fir and pine: places, belts, soils |
| `campania_pfg2009` | institutional | verified | land systems, climate, forest by altitude |
| `filesi2010_serie_campania` | monograph | verified | vegetation belts and the beech tree line |
| `campania_foreste_demaniali2007` | institutional | verified | Taburno fir; beech-Turkey oak contact heights |
| `campania_sistemi_terre_250k` | dataset | verified | soil reaction by land system |
| `castagna_montella_igp` | institutional | verified | chestnut orchards 500-1,000 m |
| `marrone_roccadaspide_igp` | institutional | verified | Cilento chestnut above 250 m, pH 4.5-6.5 |
| `marrone_serino_igp` | institutional | verified | acid ash soils; dry June-August spells |
| `allocca2014_hess` | peer-reviewed | verified | rain up to 1,700-2,000 mm on the Apennine ridge |
| `arpac_clima_indicatori2023` | dataset | verified | monthly rain at five stations, 2001-2020 |
| `lr_campania_8_2007` | institutional | verified | the picking law in force |
| `campania_dgr179_2008_funghi` | institutional | verified | porcini group, chanterelle and ovolo rules |
| `lr_campania_14_2015` | institutional | verified | permits moved to the Region |
| `mushma_campania_forest_composition_2026` | analysis | verified | habitat shares and elevations on the Carta della Natura |
| `mushma_occurrence_check_campania_2026` | analysis | verified | month counts, elevations, southern and Tuscan comparison |

Existing references the Campania changes lean on:
- `funghimagazine_ovolo`: its "1200 m in the south" is not specific to Campania.
- `rt_tipi_forestali_p4`: the Tuscan beech belt, for comparison.
- `olariaga2017`: the *Cantharellus* segregates; it has no Campania specimens.
