# Species ecology: Sicilia (regional appendix to species-ecology.md)

Research date: 2026-09-28 (dates Europe/Rome, units metric). Card: `region-sicilia-species.md`
(child of `region-sicilia.md`). Rule files: `api/src/api/config/species/sicilia/`. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Sicily, what
changed and why. It covers **fruiting conditions only**: nothing here is about edibility or
identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(34 added for Sicily, in one block right after the Liguria entries, listed at the end of this
page). Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**,
**plausible**, **folklore**. Every number is a prior for the backtest; season windows, altitude bands
and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

Calabria (branch `region/calabria`, not merged yet) is the nearest precedent: the same laricio pine,
the same southern season. [Where Sicily departs](#where-sicily-departs-from-calabria-and-central-italy)
compares the two and the central-Italian windows.

## Summary

1. **All three groups and all six keys are kept.** Porcini, ovoli and gallinacci all fruit in
   Sicily, and the regional law names the porcini group and bans the closed ovolo. *B. pinophilus* is
   kept although it is rare (8 dated records in three years, none on iNaturalist); the doc and its
   file say so.
2. **Sicily has one quantitative porcini source, and it drives most changes.** Vasquez's doctoral
   census of the Sicilian Boletales (University of Catania, 2010-2013;
   `vasquez2013_boletales_sicilia`) lists 236 dated porcini records with place, height, wood and
   number of fruit bodies, mostly from Etna and the Nebrodi. They are one team's collections, not a
   survey with fixed effort, so they count as plausible. A habitat affinity changed only where these
   records and the Sicilian sources' own words agree.
3. **The Sicilian porcini split by belt.**
   - *B. reticulatus* ("purcini siddu", 116 records) is the commonest, the porcino of the chestnut
     woods and of the spring.
   - *B. aereus* ("purcini niuri", 82) is the porcino of the downy, Turkey, holm and cork oak.
   - *B. edulis* ("testa di fagu", 30) is an autumn porcino of the high beech and Etna birch.
   - *B. pinophilus* ("testa russa", 8) is the one porcino of the pine table, "in realtà molto più
     raro".
4. **Etna's laricio pine is weak porcini ground.** Of 22 Boletales the census found under Sicilian
   pine, the only porcino is *B. pinophilus*, twice in the pure laricio of the Pineta Ragabo. So
   `mountain_pine` becomes a full host for *B. pinophilus* only and a non-host (0.1) for *B. edulis*
   and *B. reticulatus*. Mixed pine-beech and pine-chestnut cells keep full credit through their
   broadleaves.
5. **The season: a spring flush, a summer gap, and a long autumn at low altitude.**
   - Every census year had porcini in May-June (*B. reticulatus* above all, 850-1,500 m, Nebrodi and
     Etna). Funghi Magazine's bulletins put the first ones in the coastal macchia from late April and
     the first ovoli in late May; *B. reticulatus* and the lower *B. aereus* window now open in
     mid-April, the ovolo's in mid-May.
   - July and August are nearly empty. The weather rules make that gap, not the calendar.
   - The autumn runs from September; its peak came in October 2011, November 2012 and September 2013.
   - *B. aereus* runs into December in the holm and cork oak, and the census sampled those woods only
     in October-December.
   - 14 press contrasts (11 from Funghi Magazine) are written down in `sanity.yaml`, most setting
     Etna, the Nebrodi and the Peloritani against the Sicani, Ficuzza and Madonie, or a good year
     against a dry one.
6. **The hosts sit high.** The Sicilian chestnut reaches 1,700-1,800 m, holm oak 1,500 m, beech
   2,000 m on Etna. The census's porcini records are high too: *B. aereus* median 1,000 m, *B.
   reticulatus* 1,240 m, *B. edulis* 1,500 m (Tuscan iNaturalist medians 352, 649 and 1,054 m).
   The full-credit limits of the altitude bands move up 250-600 m.
7. **A third of Sicily's woods are plantations, and the rules treat them as poor porcini ground.**
   - The Aleppo, stone pine and cypress reforestation (`mediterranean_pine`, 55,000 ha) becomes a
     non-host for *B. aereus* (0.1).
   - The eucalyptus (`exotic_broadleaf`, 39,000 ha) gets 0.1 for *B. aereus* and *B. reticulatus*,
     folklore, for the Erei reports of porcini under eucalyptus.
   - The chanterelles keep the pines at 0.3: all the Sicilian chanterelle specimens with a habitat
     come from stone-pine and cedar plantations over holm oak.
8. **Weather rules are all Tuscany's.** No Sicilian study ties fruiting to rain or temperature in
   numbers. The census's lore (the tramontana after scant rain is "fatale per la crescita dei
   carpofori"; hazel fruits first after rain, oak and beech a week or more later) fits the Tuscan
   rules.
9. **Very few records to validate.** iNaturalist has 49 records of the six keys in Sicily (Calabria
   118, Tuscany 290), none of *B. pinophilus*. The backtest will say little; the census is the better
   check.

## Sicily in brief

**Woods.** The grid maps Sicily's woods from the Regione Siciliana's Carta forestale regionale (SIF,
1:10,000, forest types after La Mantia et al.; `config/regions/sicilia.yaml`, written in parallel).
Only its class 31a (boschi, 321,618 ha) counts as forest. The rules were drafted before the grid
existed, so the areas below are whole-map areas as the region card reads them
(`sif_carta_forestale_sicilia`); the habitat medians and dominant cells will come from the build.

This table is **which habitat holds which Sicilian tree**:

| habitat key | Carta forestale types | ha | share of 31a | notes |
|---|---|---|---|---|
| `deciduous_oak` | downy oak s.l. QU2 thermophilous (33,473), QU5 on siliceous soils (42,523), QU4 on limestone (7,545), QU3 (4,064), sessile oak QU1 (529); Turkey oak CE2 montane (16,413), CE1 thermophilous with *Q. gussonei* (8,850) | 113,397 | 35 % | *Q. virgiliana*, *Q. congesta*, *Q. dalechampii* are in the downy-oak types |
| `mediterranean_pine` | Mediterranean conifer reforestation RI3 (53,315: Aleppo, stone and maritime pine, cypress); PM1 Aleppo pine of the south-east (374), PM2 maritime pine of Pantelleria (345), PM3 stone pine (164), PM4 naturalised pines (796) | 54,994 | 17 % | almost all planted |
| `evergreen_oak` | holm oak LE1-LE4 (24,239); cork oak SU1 coastal (7,731), SU2 inland (11,297), SU3 Iblean volcanites (2,436) | 45,703 | 14 % | holm oak reaches 1,500 m |
| `exotic_broadleaf` | eucalyptus reforestation RI1 (38,818); robinia, ailanthus, other aliens BS5-BS7 | about 40,200 | 12.5 % | |
| `beech` | FA1 on siliceous soils, Nebrodi (13,785); FA2 on Etna's lavas (1,168); FA3-FA4 calcicolous, Madonie (1,841) | 16,794 | 5.2 % | |
| `riparian` | FR1 oriental plane, FR2 poplar and willow, FR3 shrub willows, FR4 tamarisk and oleander, FR5 narrow-leaved ash | 14,059 | 4.4 % | |
| `mixed_broadleaf` | broadleaf reforestation RI2 (8,158), other native broadleaves BA1 (4,256), Etna birch BS1 (352), aspen BS2, manna ash BS3, field elm BS4, hop-hornbeam OS1-OS2 | about 12,800 | 4 % | the Etna birch is a *B. edulis* host |
| `chestnut` | CA1 thermophilous (7,361), CA2 montane mesophilous (4,518) | 11,879 | 3.7 % | |
| `mountain_pine` | laricio pine PL1-PL3 (3,681, Etna); montane conifer reforestation RI4 (7,197: black pine, laricio, cedar) | 10,878 | 3.4 % | cedar is here, not in `other_conifer` |
| `macchia` | MM0-MM9 (oleaster and *Euphorbia dendroides*, *Calicotome*, *Spartium*, carbonate and siliceous macchia-gariga, dwarf palm, rosaceous scrub) | 126,665 | shrubland class | not woodland in the grid mask |
| `transitional_woodland_shrub` | montane scrub AS1-AS5 (*Genista aetnensis*, broom, *Erica arborea* of the Peloritani, holly stands, rosaceous scrub, 39,257); sparse woods 31b (12,752); temporarily unstocked woods 31c (8,896) | 60,905 | other classes | |

Sicily has no `fir_spruce`, `other_conifer` or `mixed_broadleaf_conifer` wood. *Abies nebrodensis*
survives as fewer than thirty trees on the Madonie (`wikipedia_parco_madonie`). Those affinities stay
in the rule files and score no cell. Hazel orchards (Nebrodi, Etna, Peloritani), which the census
found the first ground to fruit after rain, are farmland and outside the grid.

The reforestation (RI1-RI4) is 107,488 ha, a third of 31a. INFC 2015 (`infc2015_sicilia`) has the same
picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| sessile, downy and pedunculate oak | 71,887 | 25.2 % |
| Mediterranean pines | 45,327 | 15.9 % |
| other evergreen broadleaves (mostly eucalyptus) | 39,151 | 13.7 % |
| Turkey oak, Hungarian, Macedonian and valonia oak | 30,989 | 10.9 % |
| holm oak | 19,536 | 6.8 % |
| cork oak | 17,261 | 6.0 % |
| beech | 15,165 | 5.3 % |
| other deciduous | 13,237 | 4.6 % |
| other conifers | 9,299 | 3.3 % |
| chestnut | 8,720 | 3.1 % |
| black, laricio and loricato pine | 7,493 | 2.6 % |
| hygrophilous | 4,929 | 1.7 % |
| hop-hornbeam and hornbeam | 1,737 | 0.6 % |

INFC's bosco is 285,489 ha; the Carta forestale's 31a is 321,618 ha, 13 % more (a hand-off, below).

**Altitude belts:**

| type | altitude (m) and where | source |
|---|---|---|
| beech | Nebrodi above 1,200-1,400 m to the crest (1,847 m), "per più di 10.000 ettari"; Madonie above 1,000 m, "optimum a 1600-1700 metri"; Etna "in massima parte fra 1400 e 2000 m", down to about 800 m in the damp valleys of the east flank; "al di sopra dei 1000 m fino ai 1800-2000 m sui versanti N, N-W dell'Etna" | `parks_nebrodi_ambiente`; `wikipedia_parco_madonie`; `hortus_catinensis_etna_boschi`; `vasquez2013_boletales_sicilia` p. 161 |
| laricio pine | "quasi esclusivamente sull'Etna ... da 1000 a 2000 m di quota", 5,654 ha, 87 % pure stands, 1,200 ha in Linguaglossa's Pineta Ragabo; the north flank's upper belt at 1,600-1,900 m above beech at 1,000-1,600 m | `barreca2010_pineta_ragabo`; `seiler2021_etna_treering` |
| Etna birch | above 1,400 m, "si spinge sino a 2000 m"; the census's birch sites at 1,550-1,850 m | `hortus_catinensis_etna_boschi`; `vasquez2013_boletales_sicilia` p. 166 |
| chestnut | "tra i 300 m e i 1700-1800 m"; on Etna "al di sopra di 800-900 metri" (Tarderia, Milia, Zafferana) | `vasquez2013_boletales_sicilia` p. 158; `hortus_catinensis_etna_boschi` |
| Turkey oak, *Q. gussonei*, downy oak | Nebrodi "piano supramediterraneo" at 800-1,200/1,400 m, Turkey oak "dominante nelle aree più fresche"; Etna's Turkey oak at 1,200-1,500 m on the east flank; Madonie downy oak "dai 400 ai 1200 metri" | `parks_nebrodi_ambiente`; `hortus_catinensis_etna_boschi`; `wikipedia_parco_madonie` |
| holm oak | Madonie 400-1,000 m; forests of *Q. ilex* "that reach an altitude of 1500 m well above the maximum elevation found in other parts of Italy" | `wikipedia_parco_madonie`; `ferraro2022_checklist_sicilia` |
| cork oak | Nebrodi to 600-800 m; Madonie "fra 40 e 1000 metri" | `parks_nebrodi_ambiente`; `wikipedia_parco_madonie` |

Sicily's belts are Calabria's pushed higher again:
- The beech reaches 2,000 m on Etna, as in Calabria, but starts higher, at 1,200-1,400 m, except in
  damp valleys.
- The oaks and chestnut reach 1,400-1,800 m, against 1,100-1,200 m in Calabria.
- The laricio belt, 1,000-2,000 m, is Etna's alone.

**Substrate.**
- The Nebrodi are flysch and quartzarenite with acid soils, the Peloritani schist, Etna lava and
  pyroclastics, the Madonie limestone with quartzarenite, the Iblei limestone with volcanites at
  Buccheri and Monte Lauro (region card).
- The census: "La maggior parte delle specie di Boletales prediligono un terreno siliceo o argilloso"
  (p. 62). The ovolo "su substrarti acidi" (`micologiamessinese_caesarea`).
- Soil is not modelled in v1. The acid Nebrodi, Peloritani and Etna soils are where most records are.

**Climate.**
- **Totals.** Mean annual rain at the Sicilian gauges ranges "from 400 mm to 1300 mm"
  (`arnone2013_rainfall_sicily`). The census gives about 1,500 mm in the Nebrodi beech and about 1,000
  mm in the Turkey oak, "concentrate nel mese di Novembre e la massima siccità nel mese di Luglio"
  (pp. 147, 162). The region card has 1,000-1,400 mm on the Nebrodi, Madonie and Peloritani crests and
  the east flank of Etna, 400-600 mm on the south coast and inland.
- **Season.** The dry season runs "from April to September"; annual rain decreased over 1956-2005,
  "mainly due to a reduction in the seasonal rainfall during the wet period (fall and winter)"
  (`arnone2013_rainfall_sicily`).
- **Beech climate.** The census's beech stations: coldest month -0.77 °C, warmest 16.12 °C, mean 6.37
  °C, "oromediterranea con ombro-clima umido" (p. 162). The Etna birch stations at 1,550-1,850 m have
  "inverni ... freddi e nevosi (con nevicate che si protraggono da fine autunno a primavera inoltrata)"
  and about three months of drought (pp. 165-166).
- **Snow** lies on the high ground in winter; the snow and frost stoppers are kept.

**Regional law.** L.R. 1 febbraio 2006, n. 3 (`lr_sicilia_3_2006`, GURS n. 6 of 3 February 2006).
- **Amendments.** None found. ISPRA's 2021 summary (`ispra2021_raccolta_funghi_sicilia`) reprints the
  2006 articles unchanged, and the Region's 2023 notice (`regione_sicilia_tesserino_funghi2023`) acts
  through administrative decrees (D.A. 236/2023, D.A. 362/2023) on issuing and renewing the permit.
  The census records the implementing species lists (D.P. 19 November 2007, D.P. 4 August 2009) and
  the 4 cm minimum cap for the porcini (pp. 101-104). No amending law turned up in the searches; this
  should be re-checked against the Region's consolidated texts when its portal is reachable (it
  refused connections on 2026-09-28).
- **Permits and quantities.** A regional permit after a 15-hour course: amateurs "sino a quattro
  chilogrammi di funghi al giorno", professionals twelve (art. 2).
- **Ovolo.** "E' vietata la raccolta e la commercializzazione di esemplari del genere Amanita caesarea
  allo stato di ovolo chiuso" (art. 4 c. 5).
- **Hours and places.** No picking "durante le ore notturne" (art. 4 c. 1); bans in areas closed for
  silvicultural or natural reasons, reclaimed landfills and industrial zones (art. 5); temporary
  suspensions where picking has impoverished the woods (art. 6).
- **What it leaves out.** No season calendar and no altitude rule. None of it changes where or when
  the fungi fruit; it confirms the porcini group and the ovolo as regional species.

## The Sicilian porcini census

`vasquez2013_boletales_sicilia` is a University of Catania doctoral thesis (XXVI cycle, 2010-2013,
tutor P. Minissale). It maps the Sicilian Boletales by habitat and lists every dated record with its
place, height, wood, number of fruit bodies and collector (pp. 299-309 for the porcini). It is the
only Sicilian source with numbers. Its limits:
- One team's collections, with the author's own sampling calendar per habitat, so the month counts
  mix fruiting and effort.
- Mostly Etna (103 porcini records) and the Nebrodi (89), with the Peloritani (10) and 22 in the
  Iblei, Erei and western Sicily, not counting 12 dated exhibition specimens. No Madonie record.
- Three years only.

Month counts of the porcini records (a few are dated exhibition specimens):

| taxon | n | M | J | J | A | S | O | N | D | located height |
|---|---|---|---|---|---|---|---|---|---|---|
| *B. reticulatus* (as *B. aestivalis*) | 116 | 18 | 35 | 12 | 7 | 16 | 18 | 9 | 1 | 530-1,900 m, median 1,240 (p10 846, p90 1,450; n=113) |
| *B. aereus* | 82 | 3 | 5 | 1 | 5 | 13 | 25 | 26 | 4 | 300-1,700 m, median 1,000 (p10 520, p90 1,400; n=77) |
| *B. edulis* | 30 | | | | 1 | 11 | 9 | 8 | 1 | 800-2,000 m, median 1,500 (p10 1,000; n=27) |
| *B. pinophilus* | 8 | | | | | 2 | 3 | 3 | | 1,300-1,700 m (n=7) |

By year (all four porcini): 2011 May 4, June 27, July 11, September 1, October 27, November 5; 2012
May 7, June 6, August 2, September 12, October 10, November 31, December 6; 2013 May 10, June 7, July
2, August 11, September 29, October 18, November 10.

Habitat shares of the dated records, each record split evenly between the trees it names:

| taxon (records) | chestnut | deciduous oak | holm and cork oak | beech | Etna birch | hazel | pine | other |
|---|---|---|---|---|---|---|---|---|
| *B. reticulatus* (112) | 54 % | 16 % | 7 % | 14 % | – | 7 % | 2 % (mixed only) | eucalyptus, stone pine 0.5 each |
| *B. aereus* (77) | 18 % | 43 % | 26 % | 5 % | (a photo at 1,800 m) | 5 % | 1 % (mixed only) | eucalyptus 1 |
| *B. edulis* (27) | 13 % | 2 % | – | 48 % | 22 % | – | 11 % (1 pure laricio) | stone pine, poplar |
| *B. pinophilus* (7) | 7 % | – | – | 29 % | – | – | 50 % (2 pure laricio) | yew with beech 14 % |

The habitat chapters (pp. 142-177) add the seasons the census found in each wood:
- **Evergreen oaks and macchia:** sampled "nei mesi di Ottobre, Novembre e Dicembre, poiché, nei
  restanti, o per la siccità o per la temperatura molto bassa, i funghi generalmente non producono
  corpi fruttiferi" (p. 144).
- **Deciduous oaks:** "la maggior parte dei corpi fruttiferi sono stati rinvenuti nei mesi di Giugno,
  Ottobre e Novembre" (p. 147).
- **Pine:** 22 Boletales, "uno scarso numero", not sampled in July-September, "quando i funghi
  generalmente non producono corpi fruttiferi o per la siccità o per la temperatura troppo elevata"
  (pp. 151-152).
- **Chestnut:** sampled in May, June, July, September, October and November (p. 159).
- **Beech:** the season "inizia ... con lo sciogliersi delle nevi a fine aprile per continuare,
  precipitazioni permettendo, fino al mese di novembre; a volte si interrompe durante i mesi più
  caldi" (p. 161).
- **Hazel:** "il primo habitat a produrre sporofori fungini e boleti subito dopo le piogge, sia tardo
  primaverili-estive che autunnali, anticipando di qualche giorno la fruttificazione dei funghi nei
  castagni ... e anche di una o più settimane quella nelle querce ... e nei faggi" (p. 155).

## Porcini under Etna's laricio pine

The card's first question: which porcini fruit under the laricio, and how strongly. The grid files the
Etna laricio (PL1-PL3, 3,681 ha) and the montane black pine, laricio and cedar reforestation (RI4,
7,197 ha) as `mountain_pine`.

**Which porcino.** *B. pinophilus*, and it is rare (plausible).
- The census's pine table (Aleppo, stone and laricio pine, 22 Boletales) names only one porcino, *B.
  pinophilus*, "in habitat, Pineta Ragabo di Linguaglossa" (p. 151). The table is mostly *Suillus*,
  *Chroogomphus* and *Tapinella*.
- *B. pinophilus* records: pure laricio at the Pineta Ragabo, 1,700 m (5 November 2011, 3 fruit bodies;
  13 September 2013, 2); black pine with beech or chestnut at Floresta, Nebrodi, 1,300 m (28 October
  2011, 30 October and 7 November 2013); beech with yew at Alcara li Fusi, 1,400 m (September-October
  2013).
- *B. edulis* has one record in pure laricio (Pineta Ragabo, 1,300 m, 17 November 2012, one fruit body)
  and four in pine mixed with beech or chestnut (Monte Timpa Rossa 1,800 m, Floresta 1,300 m, Colle
  San Rizzo 800 m twice). Its main ground on Etna is the beech and birch of the north flank (Monte Timpa
  Rossa, Rifugio Citelli, Monti Sartorius, Monte Maletto).
- *B. reticulatus* and *B. aereus* have no pine-only record.
- *B. pinophilus* is "in realtà molto più raro" than *B. edulis* (p. 5), has no iNaturalist or GBIF
  record, and is in the checklist for Catania, Messina and Palermo only
  (`ferraro2022_checklist_sicilia`).
- The press agrees (folklore). No 2016-2025 source names porcini in the Etna pinewoods. Funghi
  Magazine finds the island's "clima caldo-ventoso, con scarse nevicate invernali e pochi shock
  termici" makes it "poco adatta per questa varietà di Porcino" (`fm_sicilia_2021_06_24`), reports
  "Sporadici Porcini Rossi ... sull'Etna, alle quate superiori" in late May 2023
  (`fm_sicilia_2023_06_02`) and "tra Etna e Nebrodi, i meno comuni edulis e pinicola" in November 2025
  (`fm_sicilia_2025_11_08`). Its calendar puts *B. edulis* in the pine of the Sila and in the beech "del
  resto del Sud" (`fm_calendario_autunno2019_sicilia`).

**How strongly.** Much less than in Calabria. In the Calabrian ISPRA tables *B. pinophilus* is 8th of
933 species under laricio. In Sicily the census found it 8 times in three years, against 116 *B.
reticulatus*. Pure laricio is poor porcini ground here; mixed pine with beech or chestnut is where
*B. edulis* and *B. reticulatus* turn up.

**What the rules do.**
- `mountain_pine` becomes a full host (1.0) for *B. pinophilus* and a non-host (0.1) for *B. edulis*
  and *B. reticulatus*; *B. aereus* stays at 0.
- A cell with 30 % of beech or chestnut keeps full credit for every porcino, so Etna's mixed upper belt
  and the Peloritani chestnut-black pine are untouched.
- A pure laricio cell now scores porcini only through *B. pinophilus*. Because it is rare, a high score
  there is a statement about conditions for a scarce taxon. The backtest cannot test it (no records);
  see Open questions.

**Natural stands and plantations.** The Carta forestale separates them (PL1-PL3 against RI4) but the
habitat vocabulary has one key. The census's pine records are in the natural laricio of the Pineta
Ragabo and in Nebrodi black pine plantations (Floresta), so both are treated alike.

## Turkey oak and *Q. gussonei*

The card asked whether the Nebrodi's Turkey oak and *Q. gussonei* are the island's main porcini host.
- **They are porcini ground, not the main one** (plausible). Turkey oak appears in 7 *B. reticulatus*
  and 7 *B. aereus* records: "Il Cerro" at San Fratello (846 m, May-June 2011), Portella dei Bufali at
  Cesarò and Flascio (1,150-1,200 m, October 2013, with downy oak), the Bosco della Cerrita on Etna
  (1,300-1,400 m, June and September), Monte Maletto (1,450-1,510 m). None is *B. edulis*.
- The Nebrodi's largest single harvest in the census is in downy oak at Portella dei Bufali, Cesarò,
  1,200 m: *B. aereus* 80 fruit bodies on 9 September and 50 on 13 September 2013.
- The census never names *Q. gussonei*; its "Quercus cerris" and "Quercus pubescens" records on the
  Nebrodi include the belt where it grows.
- On the Nebrodi the census's porcini are split between chestnut (Floresta, Ucria, the Zappa), downy
  and Turkey oak (Cesarò, Caronia, Semantile) and beech (Monte Soro, Portella Femmina Morta, Torti).
  `deciduous_oak` stays a full host for *B. aereus*, *B. reticulatus* and the ovolo, and drops to 0.1
  for *B. edulis*.

## The reforestation

About a third of the woods are post-war plantations.
- **Mediterranean conifers (`mediterranean_pine`, RI3 53,315 ha: Aleppo, stone and maritime pine,
  cypress).** The census's pine table includes Aleppo and stone pine and has no *B. aereus*, *B.
  reticulatus* or *B. edulis*. Its only porcino records with stone pine are in holm oak or chestnut. So
  the porcini keep or get 0.1 (*B. aereus* drops from 0.6). The chanterelles keep 0.3: the five
  Peloritani chanterelle specimens with a habitat (`mushma_occurrence_check_sicilia_2026`) all grew in
  stone pine, cypress and cedar plantations mixed with holm oak (Colle San Rizzo, Dinnammare, 350-1,000
  m), and the map files such stands as reforestation.
- **Eucalyptus (`exotic_broadleaf`, RI1 38,818 ha).** Mycologists of the Erei "affermare che in
  eucalipteto puro riescano a crescere addirittura Boletus della Sezione Boletus (porcini) - Boletus
  aereus e Boletus aestivalis" at Piazza Armerina, Pergusa and Aidone; the census saw the photographs
  and specimens but "dubitiamo del fatto che questi 'straordinari eucalipteti' siano totalmente assenti
  di plantule appartenenti al genere Quercus e/o Castanea" (pp. 176-177). Its records there are in
  eucalyptus with downy oak or chestnut (16-17 November 2012). Forager lore has *B. reticulatus* "tra
  Calabria e Sicilia ... persino ... sotto le piante di Eucalipto" (`fm_calendario_autunno2019_sicilia`).
  *B. aereus* and *B. reticulatus* get 0.1 (folklore); the other keys keep 0 (the ovolo 0.05).
- **Montane conifers (RI4) and broadleaf reforestation (RI2)** are in `mountain_pine` and
  `mixed_broadleaf` (above and below).

## The Sicilian season

The card asked when the autumn starts, whether there is a spring flush on the Nebrodi and Madonie,
and how late *B. aereus* runs in the cork and holm oak.

1. **A spring flush: yes, on the Nebrodi and Etna, mostly *B. reticulatus*** (plausible).
   - Every census year had porcini in May-June: 31 records in 2011, 13 in 2012, 17 in 2013. The first
     date is 11 May (2013, holm and downy oak at 1,150 m on Etna).
   - They are 850-1,500 m in chestnut, Turkey oak and beech: Floresta, Ucria and San Fratello on the
     Nebrodi; Milo, Maletto, Ragalna and the Cerrita on Etna.
   - *B. aereus* joins with a few records (23 May-12 June); *B. edulis* and *B. pinophilus* never do.
   - The bulletins agree and add the coast (folklore): "Estatini o aereus per ora sono sempre ben
     presenti nella macchia mediterranea, quindi in Sardegna, Sicilia" (`fm_sicilia_2018_05_09`), *B.
     aereus* in the macchia "ormai da qualche settimana" on 30 April 2018 (`fm_sicilia_2018_04_30`),
     porcini "in boschi non troppo distanti dal mare, in particolar modo a Nord ed Est oltre che
     sull'Etna" on 22 May 2020 (`fm_sicilia_2020_05_22`), and in the rainy May of 2023 *B. aereus*
     "anche e soprattutto nelle Macchie, in boschetti, gruppetti di alberi isolati", chanterelles in
     the damp woods and "Sporadici Porcini Rossi ... sull'Etna, alle quate superiori"
     (`fm_sicilia_2023_06_02`). The best late-May *B. aereus* finds of 2019 were "alle falde dell'Etna e tra
     le falde tirreniche di Nebrodi-Peloritani e Madonie" (`fm_sicilia_2019_05_30`), the one mention of
     a Madonie spring flush.
   - The first ovoli come in late May too: "nel Lazio, in Campania, Calabria e Sicilia, si sono già
     trovati i primi Ovoli Reali" (`fm_sicilia_2023_05_25`), "Già se ne vendono i primi esemplari
     provenienti dalla Calabria, Sicilia e Sardegna" (`fm_sicilia_2024_05_30`).
   - What changed: *B. reticulatus* opens on 15 April and is full from 15 May (Tuscany 1 May and 1
     June); *B. aereus*'s lower window opens on 15 April and its upper one on 15 May; the ovolo's opens
     on 15 May (1 June). *B. pinophilus* keeps its Tuscan spring window for the sporadic upper-Etna
     flush.
2. **A summer gap: yes, deeper than in central Italy; the weather makes it.**
   - The census found July-August the emptiest months (26 of 236 records), mostly beech at 1,380-1,900
     m in July 2011 and a late-August flush in 2013.
   - The pine and holm oak were not even sampled in summer, for "siccità" or "temperatura troppo
     elevata".
   - The dry season is April-September (`arnone2013_rainfall_sicily`).
   - As in Tuscany and Calabria, no calendar gap is written in: the heat, drought and drying rules do
     it.
3. **The autumn: from September at altitude, October-December below.**
   - The census's autumn peak moved by year: October 2011 (27), November 2012 (31), September 2013 (29).
   - At 1,200-1,600 m (beech, high oak) the records are September-October. In the holm, cork and downy
     oak below 1,000 m they run from October to December.
   - Among all Sicilian fungi on iNaturalist, October holds 21 % of the records, November 14 %,
     December 11 % and January 5 % (`mushma_occurrence_check_sicilia_2026`).
   - What changed: *B. reticulatus* is full to 31 October and ends on 15 December; *B. aereus*'s lower
     window is full to 30 November and ends on 10 January; the ovolo's plateau runs to 15 November
     and ends on 10 December.
   - The press dates the autumn by the rain: in 2018 "già in agosto si sono raccolte grandi quantità
     dei pregiati porcini dell'Etna" after a rainy summer (`lasicilia_bronte118_funghi2018`); in 2024
     "Da fine agosto finalmente sono tornate frequenti le piogge" and the season was "perfetta"
     (`fm_sicilia_2024_09_19`); in 2022 and 2025, dry until October, it started in mid-October.
   - The flush can be short at altitude. On the northern Nebrodi and Peloritani "i Neri sono già
     arrivati al capolinea" by 19 September 2024, and a Bronte forager puts "il periodo ideale" at
     Monte Minardo "solo fino a metà settembre" (`lasicilia_minardo_porcino2024`, folklore). The
     census still found *B. aereus* at Monte Minardo on 25 November 2011 and 1 December 2012, so the
     windows keep the late autumn and the weather decides.
4. **How late *B. aereus* runs in cork and holm oak: into December.**
   - The census's last records: 1 December (holm oak, Monte Minardo, 1,100 m), 2 December (*Q.
     virgiliana*, Mineo, 350 m), 6 December (cork and holm oak, Caronia, 300 m, 10 fruit bodies), 8
     December (downy oak, Milo, 780 m).
   - The evergreen-oak woods were sampled in October-December only, so January is untested.
   - The window's zero on 10 January (as Calabria's) is plausible but weak.
5. **When the first autumn rains start it.** The census gives no rain dates. Its lore ties the
   flushes to rain ("non appena le piogge lo permettono"), with hazel first and oak and beech one or more
   weeks later; a Milo forager waits "almeno sette, otto giorni" after heavy rain
   (`lasicilia_bronte118_funghi2018`). The start moves by a month or more between years: late August in
   2018 and 2024, early September in 2021, the first days of October in 2020 and 2023, mid-October in
   2022 and 2025 (Sanity contrasts). The rain-trigger lags do this.

## Where Sicily departs from Calabria and central Italy

Calabria's rules (on its branch) and Sicily's start from the same Tuscan files.

| factor | Tuscany | Calabria | Sicilia | why Sicily differs |
|---|---|---|---|---|
| `mountain_pine` for *B. pinophilus* | 0.6 | 1.0 | 1.0 | same move: the only porcino of the pine table |
| `mountain_pine` for *B. edulis*, *B. reticulatus* | 0.6 | 0.1 | 0.1 | same move |
| `deciduous_oak` for *B. edulis* | 0.3 | 0.3 | **0.1** | no oak-only record; Sicilian downy oak is low and warm |
| `chestnut` for *B. pinophilus* | 1.0 | 0.3 | **0.1** | not in the census's chestnut table |
| `beech` for *B. reticulatus* | 0.6 | 1.0 | 1.0 | same move: 13 pure-beech records |
| `macchia` for *B. aereus* | 1.0 | 0.3 | 0.3 | same move: oleaster, *Euphorbia*, *Calicotome*, dwarf palm |
| `mediterranean_pine` for *B. aereus* | 0.6 | 0.1 | 0.1 | same move: none under Aleppo or stone pine |
| `beech` for *B. aereus* | 0.1 | 0.3 | 0.3 | same move: Nebrodi beech at 1,500-1,600 m |
| `exotic_broadleaf` for *B. aereus*, *B. reticulatus* | 0 | 0 | **0.1** | the Erei eucalyptus reports (folklore) |
| `evergreen_oak` for the ovolo | 0.6 | 1.0 | **0.6** | no Sicilian evidence that holm oak equals the deciduous hosts; 0.6 already gives full credit on a pure cell |
| pines for the chanterelles | 0.3 | 0.1 | **0.3** | the Sicilian specimens are in pine plantations over holm oak |
| *B. edulis* window start | 1 July | 1 June | **1 July** | no spring or early-summer record; "l'autunnale" |
| *B. reticulatus* window | from 1 May, full 1 Jun-30 Sep, 0 by 15 Nov | full 1 Jun-31 Oct, 0 by 15 Dec | **from 15 Apr, full 15 May**-31 Oct, 0 by 15 Dec | 18 May records; coastal "Estatini" in early May; runs to 2 December |
| *B. aereus* windows | upland 15 Jun-31 Oct, lowland 1 Jul-15 Dec, handover 400-600 m | both from 15 May; lowland to 10 Jan; 600-800 m | **lowland from 15 Apr**, upland from 15 May; lowland to 10 Jan; **handover 1,000-1,200 m** | macchia *B. aereus* from late April; the oak belt reaches 1,200-1,400 m |
| *B. pinophilus* windows | spring and autumn | kept | kept | autumn records; "Sporadici Porcini Rossi" on upper Etna in late May 2023 |
| ovolo window | 1 Jun → 1 Sep … 5 Nov → 30 Nov | 15 May → 1 Aug … 5 Nov → 30 Nov | **15 May → 1 Sep … 15 Nov → 10 Dec** | first ovoli in late May; 7 of 12 records in October-November |
| *B. edulis* altitude | 200 → 700 … 1,600 → 1,900 | 200 → 700 … 1,800 → 2,000 | **400 → 800 … 2,000 → 2,250** | nothing below 800 m; beech at 2,000 m on Etna |
| *B. reticulatus* altitude | 0 → 150 … 1,100 → 1,500 | … 1,600 → 1,900 | … **1,700 → 2,000** | records to 1,900 m |
| *B. aereus* altitude | … 800 → 1,250 | … 1,000 → 1,350 | … **1,400 → 1,800** | records to 1,700 m, median 1,000 m |
| *B. pinophilus* altitude | 300 → 800 … 1,600 → 1,900 | 300 → 800 … 1,800 → 2,000 | **500 → 1,000 … 2,000 → 2,250** | records at 1,300-1,700 m |
| ovolo altitude | … 750 → 1,100 | … 1,000 → 1,350 | … 1,000 → 1,350 | same move, hosts and climate only |
| chanterelle altitude | … 1,000 → 1,700 | … 1,500 → 1,900 | … **1,400 → 1,900** | Etna records at 1,393 and 1,585 m |

Two things set Sicily apart from Calabria:
- **The chestnut porcino leads.** In Calabria's record tables *B. edulis* leads in the beech and fir
  and *B. aereus* in the oaks. In Sicily *B. reticulatus* is half of all the porcini records, leads in
  the chestnut and in the beech's summer, and makes the spring flush.
- **The pine is poor.** Calabria's Sila laricio is *B. pinophilus* ground by record share; Sicily's
  Etna laricio has two *B. pinophilus* records in three years.

From central Italy: the windows reach later into the autumn at low altitude, and the full-credit
limits of the altitude bands sit 250-600 m higher.

## Occurrence cross-check (Sicilia)

Queried 2026-09-28 (`mushma_occurrence_check_sicilia_2026`):
- **iNaturalist**: place 96908, verifiable records.
- **Elevations**: from the Open-Meteo elevation API, for open, non-obscured records with an accuracy
  of 1 km or better.
- **GBIF**: `gadmGid=ITA.15_1`. Mostly iNaturalist copies and soil-DNA samples, plus five preserved
  chanterelle specimens from the Peloritani.
- Aggregates only; no coordinates are stored.

Sicily has 5,448 iNaturalist fungi records (Tuscany 19,136), 88 % of them from 2021 on.

| taxon | iNat n | Jun | Jul | Aug | Sep | Oct | Nov | located: median (range) |
|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 2 | | | | 1 | 1 | | 826 m (n=1) |
| *B. reticulatus* | 10 | 3 | 1 | 1 | 3 | 2 | | 1,247 m (466-1,801), n=6 |
| *B. aereus* | 12 | | 1 (2026) | 1 | 3 | 6 | 1 | 450-938 m, n=4 |
| *B. pinophilus* | 0 | | | | | | | |
| *A. caesarea* | 12 | | | 1 | 4 | 5 | 2 | 455 m (163-680), n=5 |
| *Cantharellus* | 13 | | | 1 (2026) | | 6 | 6 | 349-1,585 m, n=5 |
| all fungi (share, %) | 5,448 | 3 | 2 | 3 | 7 | 21 | 14 | December 11, January 5, April 19, May 9 |

The chanterelles are *C. cibarius* 3, *C. ferruginascens* 3 and *C. pallens* 1, plus 6 at genus or
subgenus level. April's 19 % of all fungi is spring species and observer events, not porcini.

What the records show:
- **Too few to tune or even to cross-check most keys.** They agree with the census on months and
  heights: *B. reticulatus* in June and September-October at 466-1,801 m; *B. aereus* September-
  November; the ovolo late August to late November; the chanterelles October-November.
- **The ovolo is late.** 7 of 12 records are October-November, one on 28 November, against a Tuscan
  window that ends on 30 November.
- **No *B. pinophilus* at all.**

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence** beyond the census:
- **Hosts** (folklore). The Messina guide (`micologiamessinese_edules`): *B. aereus* "in boschi di
  latifoglie, specialmente sotto quercia o castagno e nella macchia mediterranea"; *B. reticulatus*
  "nei boschi termofili di latifoglie (castagno, quercia, faggio) e nella macchia mediterranea, più
  raro presso conifere". On the Nebrodi "i porcini (Boletus aereus, B. reticulatus, B.edulis) ...
  fanno la parte del leone" (`micologiamessinese_nebrodi`).
- **Season** (folklore). The Etna mycoflora (`pavone_signorello_funghi_etna`): *B. edulis* "Dalla
  fine dell'estate all'autunno inoltrato", *B. aereus* "Dall'inizio dell'estate a tutto l'autunno".
  The Messina guide: *B. reticulatus* "dalla primavera al primo autunno". Funghi Magazine's bulletins
  (`fm_sicilia_*`) date the spring, the early-autumn *B. edulis* on Etna "oltre i 1200 mt."
  (`fm_sicilia_2019_09_20`) and the Etna beech's "enorme crescita di Boletus Edulis" of September 2024
  (`feelingetna_timparossa2024`); see [The Sicilian season](#the-sicilian-season).
- **Presence.** The checklist (`ferraro2022_checklist_sicilia`): *B. aereus*, *B. edulis* and *B.
  reticulatus* in all nine provinces, *B. pinophilus* in Catania, Messina and Palermo.

**Decisions.**

| key | factor | Tuscany | Sicilia | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | 1 Jul → 1 Sep … 15 Nov → 20 Dec | kept | 30 records 29 Aug-1 Dec, none in spring; "l'autunnale" | plausible |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.1** | one fruit body in pure laricio in three years; not in the pine table | plausible |
| *edulis* | habitat `deciduous_oak` | 0.3 | **0.1** | no oak-only record | plausible |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | *Genista*, broom, *Erica* scrub | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | kept | holds the Etna birch, 22 % of the records | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **400 → 800 … 2,000 → 2,250** | records 800-2,000 m, median 1,500 m; beech to 2,000 m | plausible |
| *reticulatus* | season | 1 May → 1 Jun … 30 Sep → 15 Nov | **15 Apr → 15 May** … **31 Oct → 15 Dec** | 18 May records; coastal "Estatini" in early May (folklore); records to 2 December | plausible |
| *reticulatus* | habitat `beech` | 0.6 | **1.0** | 13 pure-beech records | plausible |
| *reticulatus* | habitat `mountain_pine` | 0.6 | **0.1** | none in the pine table; 2 mixed records | plausible |
| *reticulatus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.6 | **0.3** | a few hosts among non-hosts | plausible |
| *reticulatus* | habitat `exotic_broadleaf` | 0 | **0.1** | Erei eucalyptus reports | folklore |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,700 → 2,000** | records to 1,900 m, p90 1,450 m | plausible |
| *aereus* | season | upland 15 Jun → 1 Aug … 30 Sep → 31 Oct; lowland 1 Jul → 1 Sep … 15 Nov → 15 Dec; handover 400-600 m | upland **15 May → 1 Jul … 31 Oct → 30 Nov**; lowland **15 Apr → 1 Jun … 30 Nov → 10 Jan**; handover **1,000-1,200 m** | spring records 23 May-12 June at 840-1,300 m; macchia *B. aereus* from late April (folklore); records to 8 December below 1,100 m, to October above 1,200 m | plausible (weak) |
| *aereus* | habitat `macchia` | 1.0 | **0.3** | mostly non-ectomycorrhizal scrub; no scrub record | plausible |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | scrub and sparse woods | plausible |
| *aereus* | habitat `mediterranean_pine` | 0.6 | **0.1** | none in the pine table | plausible |
| *aereus* | habitat `beech` | 0.1 | **0.3** | Nebrodi beech at 1,500-1,600 m | plausible (weak) |
| *aereus* | habitat `exotic_broadleaf` | 0 | **0.1** | Erei eucalyptus reports | folklore |
| *aereus* | altitude | … 800 → 1,250 | … **1,400 → 1,800** | records 300-1,700 m, p90 1,400 m | plausible |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **1.0** | the pine table's only porcino | plausible |
| *pinophilus* | habitat `chestnut` | 1.0 | **0.1** | not in the chestnut table | plausible |
| *pinophilus* | habitat `deciduous_oak`, `mediterranean_pine`, `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3 | **0.1** | no record | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **500 → 1,000 … 2,000 → 2,250** | records 1,300-1,700 m; laricio 1,000-2,000 m | plausible |
| *pinophilus* | season | spring 1 May → 20 May … 30 Jun → 20 Jul; autumn 15 Aug → 15 Sep … 15 Nov → 15 Dec | kept | census records 13 Sep-7 Nov; "Sporadici Porcini Rossi" on upper Etna, 1 June 2023; on Etna and the Nebrodi on 8 November 2025 | folklore (spring) |
| all four | weather, stoppers, growth clock | — | kept | no Sicilian numbers; the lore agrees | as Tuscany |

Kept on purpose:
- ***B. edulis* in chestnut (1.0).** 3.5 of 27 records, and the census lists it among the chestnut
  Boletales; the altitude band keeps it to the upper chestnut.
- ***B. aereus* and *B. reticulatus* in evergreen oak.** *B. aereus* stays a host (26 % of its
  records, cork oak included); *B. reticulatus* stays 0.3, which is already full credit on a pure
  cell (100 fruit bodies in holm oak at 1,300 m on Etna, 5 September 2013).
- **The *B. edulis* window.** Unlike Calabria's "precoce" *B. edulis*, the Sicilian one is autumnal.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.** "fùnciu d'ovu", among the prized species of the chestnut, beech, hazel and oak woods
  (census p. 4); in all nine provinces (checklist); abundant on the Nebrodi
  (`micologiamessinese_nebrodi`); the regional law bans the closed ovolo.
- **Hosts and season** (folklore). "Cresce, rapidamente, con clima caldo-umido da agosto a settembre in
  boschi termofili di Querce e Castagni, su substrarti acidi" (`micologiamessinese_caesarea`).
- **Spring** (folklore). The first ovoli in late May: "nel Lazio, in Campania, Calabria e Sicilia, si
  sono già trovati i primi Ovoli Reali" (`fm_sicilia_2023_05_25`); "Già se ne vendono i primi
  esemplari provenienti dalla Calabria, Sicilia e Sardegna" (`fm_sicilia_2024_05_30`).
- **Records.** 12 iNaturalist records, 26 August to 28 November (October 5, November 2), 163-680 m, on
  the Peloritani and Nebrodi, the northern Madonie (Gratteri's Bosco San Giorgio, Cefalù, Pollina) and
  Castiglione di Sicilia on Etna.

**Decisions.**

| factor | Tuscany | Sicilia | why | confidence |
|---|---|---|---|---|
| season | 1 Jun → 1 Sep … 5 Nov → 30 Nov | **15 May** → 1 Sep … **15 Nov → 10 Dec** | first ovoli in late May 2023 and 2024 (folklore); records 26 Aug-28 Nov, 7 of 12 in October-November | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | *Genista*, broom and *Erica* scrub, not heath with scattered oaks | plausible |
| altitude | … 750 → 1,100 | … **1,000 → 1,350** | hosts to 1,400-1,800 m; as Calabria; no Sicilian height data above 680 m | plausible (weak) |
| deciduous oak, chestnut 1.0; evergreen oak 0.6; macchia 0.3; conifers 0; beech 0 | — | kept | "Querce e Castagni" | strong (hosts) |
| weather rules | — | kept | no Sicilian numbers | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "jadduzzi")

**Regional evidence.**
- **Which species.** The checklist has *C. cibarius* var. *cibarius* in all nine provinces, *C.
  alborufescens*, *C. amethysteus*, *C. friesii* and *C. pallens* in Catania, Messina and Palermo, and
  *C. ferruginascens* in Catania, Messina and Trapani (`ferraro2022_checklist_sicilia`).
- **Hosts** (folklore). *C. alborufescens* "Cresce in boschi termofili preferibilmente di Leccio ma è
  stato ritrovato (Monti Peloritani) anche associato ad altre latifoglie (Quercus e Castanea) ed
  aghifoglie (Cedrus misto con Pinus)" (`micologiamessinese_cantharellaceae`).
- **Specimens.** Five on the Peloritani (Åbo Akademi herbarium via GBIF): *C. pallens*, *C.
  ferruginascens* and *C. romagnesianus*, 350-1,000 m, 31 October-3 November 2018 and 2 October 2020, in
  "Mixed woods with mainly Quercus ilex and Pinus domesticus", "mainly Cedrus sp., Quercus ilex,
  Quercus virgiliana s.l., Pinus domesticus".
- **Spring** (folklore). "tra la Sardegna, Sicilia, Elba e Macchia Mediterranea, si sono già trovati i
  primi esemplari" on 30 April 2018 (`fm_sicilia_2018_04_30`); in the rainy May of 2023 "i
  Finferli/Galletti ... risultano ben presenti nei boschi scuri e ben umidi, al riparo dal vento"
  (`fm_sicilia_2023_06_02`).
- **Records.** 13 iNaturalist records, 10 October to 30 November (plus one in August 2026), 349-1,585
  m: the Etna chestnut belt (Nicolosi, Pedara), the Nebrodi (Sinagra, Caronia), the Madonie
  (Cefalù) and the Sicani (Sambuca di Sicilia).

**Decisions.**

| factor | Tuscany | Sicilia | why | confidence |
|---|---|---|---|---|
| altitude | … 1,000 → 1,700 | … **1,400 → 1,900** | Etna records at 1,393 and 1,585 m; beech from 1,000-1,400 m | plausible (weak) |
| season (both windows), habitat, weather | — | kept | the records fall inside the windows; the Peloritani specimens back holm oak, chestnut and the pine plantations | plausible |
| soil pH, lithology | disabled | kept disabled | | plausible |

## Weather rules: why none changed

- **Rain amount and lag.** No Sicilian source gives a rain amount or lag in numbers. The census's
  "non appena le piogge lo permettono" and the hazel-first order fit the Tuscan lag plateaus, and so
  does a Milo forager's "Dopo una grande pioggia per i porcini bisogna aspettare almeno sette, otto
  giorni" (`lasicilia_bronte118_funghi2018`, folklore): the porcini lag ramps up from 6 days and is
  full from 10.
- **Drying.** "poche piogge, in periodi dell'anno non favorevoli, generalmente accompagnate da forte
  vento di tramontana, fatale per la crescita dei carpofori" (census p. 163) agrees with the drying
  stopper. So do the bulletins: in June 2022 Sicily stayed "ferma al chiodo nonostante le piogge
  importanti di Maggio, a causa del successivo insistere di caldissimi venti Sciroccali o di
  Libeccio"; in September 2021 in the west "il caldo ed il vento hanno bloccato ogni velleità
  riproduttiva"; in October 2020 the south and west, "continuamente sferzati dal vento", had sporadic
  births (Sanity contrasts).
- **Summer drought.** Deeper than in Tuscany. The porcini's 30-day rain is a percentage of each cell's
  normal, so it adapts; the ovolo and chanterelle 30-day ramps are absolute and will rarely be full in
  a Sicilian summer.
- **Cold.** The census's evergreen-oak "temperatura molto bassa" in winter and the snow on the high
  ground are the frost and snow stoppers' job.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it is a
  region-card task.

## Groups and keys

Nothing is dropped. All six keys have Sicilian evidence:
- the census's dated records (four porcini);
- the checklist (all six);
- the regional law (porcini group, ovolo);
- iNaturalist records of every key but *B. pinophilus*.

*B. pinophilus* was the one candidate to drop (card question). It stays: 8 dated records on Etna and
the Nebrodi, 3 provinces in the checklist, a dialect name, and the only porcino of the census's pine
table. Its file says it is the rarest porcino here.

`fir_spruce`, `other_conifer` and `mixed_broadleaf_conifer` are empty in Sicily but stay in the rule
files, as in every region.

## Sanity contrasts

`sicilia/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written
down on 2026-09-28, before any Sicily score existed.

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_`. "Normal" is the area's mean over 2017-2025.

**Areas.** Every comune was checked against the ISTAT 2025 list; all are in Sicily.
- `etna`: 18 comuni around the volcano, Linguaglossa, Castiglione di Sicilia, Randazzo, Bronte and
  Maletto on the north and west, Nicolosi, Ragalna, Pedara, Trecastagni, Zafferana Etnea, Milo and
  Sant'Alfio on the south and east. Randazzo and Bronte also reach into the Nebrodi; no contrast sets
  Etna against the Nebrodi.
- The Nebrodi (19 comuni, Cesarò to Sinagra) and the Peloritani (11, Messina to Barcellona Pozzo di
  Gotto) appear only joined to Etna: `etna_nebrodi`, `etna_peloritani`, `etna_nebrodi_peloritani`.
- `madonie`: 15 comuni, Castelbuono to Cefalù.
- `sicani_ficuzza`: the Sicani (Santo Stefano Quisquina to Prizzi) and the Ficuzza comuni (Corleone,
  Godrano, Monreale, Marineo, Mezzojuso): Funghi Magazine's west and south.
- `sicani_erei` and `sicani_erei_iblei`: the Sicani with the Erei (Piazza Armerina, Aidone, Nicosia,
  Sperlinga) and the Iblei (Buccheri, Giarratana, Chiaramonte Gulfi, Palazzolo Acreide, Ferla).

**The sources are mostly one magazine.**
- Sicilian local press rarely gives a dated verdict on a season. It reports giant porcini, sagre,
  rescues and fines.
- The Giornale di Sicilia and the Gazzetta del Sud block AI agents in robots.txt, and the Today
  network (MessinaToday, CataniaToday, PalermoToday) forbids AI use; none was fetched.
- 11 of the 14 contrasts rest on Funghi Magazine's national bulletins. Their Sicily paragraphs come
  from readers' reports and name sectors of the island more often than places: "settori Est" is Etna
  and the Messinese, "Nord" the Nebrodi, Madonie and Tyrrhenian Peloritani, "Ovest" the Trapanese and
  Palermitano, "Sud" the Agrigentino and Ragusano.
- Funghi Magazine's archived bulletins start in April 2018, so nothing from it covers 2016-2017.
- A research agent read about 240 bulletins through Wayback Machine captures (the live site shows a
  captcha) and the Sicilian pages. Every quote below was re-checked here against the fetched text.
- Three contrasts rest on other outlets: La Sicilia (2018, 2024) and an Etna trekking guide (2024).

| id | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|
| `etna_2018_2017_late_summer` | Etna 2018, 10 Aug-30 Sep | same, 2017 | [La Sicilia 2018-09-28, via Bronte118](https://www.bronte118.it/speciale-funghi-i-piu-buoni-sul-terreno-calcare-delletna/): "già in agosto si sono raccolte grandi quantità dei pregiati porcini dell'Etna", prices "scesi fino a sette euro al chilo" (FM 2018-08-31 "nascite di funghi eccezionali"; an Etna forager on Steemit, 2018-08-31: 2017 "piuttosto fallimentare", 2018 "piuttosto soddisfacenti") | the 2017 side is one forager looking back |
| `etna_2018_2025_august` | Etna 2018, August | same, 2025 | [FM 2025-08-29](https://web.archive.org/web/20250829134646/https://funghimagazine.it/aggiornamento-nascite-funghi-29-08-2025/): "Sicilia: al momento le probabilità di nascite sono molto basse" (FM 2025-08-01 "fuori dai giochi"; La Sicilia 2018) | the 2025 side is worded for all Sicily |
| `etna_nebrodi_peloritani_june_2018_2021_vs_2022_2024` | Etna, Nebrodi, Peloritani 2018 and 2021, 5-22 Jun | same, 2022 and 2024 | [FM 2021-06-24](https://web.archive.org/web/20210725030935/https://funghimagazine.it/aggiornamento-meteofunghi-24-06-2021-funghi-porcini-si-inizia-a-fare-sul-serio/): "ottime le nascite ... con buona continuità tra Etna e Nebrodi" (FM 2018-06-16, 2018-07-01; FM 2022-06-10 "ferma al chiodo"; FM 2024-06-14, 2024-06-28) | one outlet; the windows avoid the late-May flushes of 2022 and 2024 |
| `etna_peloritani_vs_sicani_ficuzza_2020_late_june` | Etna and Peloritani 2020, 15 Jun-10 Jul | Sicani and Ficuzza, same window | [FM 2020-06-25](https://web.archive.org/web/20200929081804/https://funghimagazine.it/aggiornamento-funghi-25-giugno-2020/): "buoni i settori orientali ... più asciutti i boschi dei settori Ovest" (FM 2020-07-03, 2020-07-10) | one outlet; "Ovest" is a sector, not comuni |
| `etna_nebrodi_peloritani_vs_sicani_ficuzza_2020_october` | Etna, Nebrodi, Peloritani 2020, 1-25 Oct | Sicani and Ficuzza, same window | [FM 2020-10-23](https://web.archive.org/web/20201204163307/https://funghimagazine.it/meteofunghi-23-10-2020/): "Sud ed Ovest dell'isola ... nascite del tutto sporadiche o persino localmente assenti" (FM 2020-10-08, 2020-10-15) | one outlet, three bulletins in a row |
| `etna_nebrodi_peloritani_2020_2022_early_october` | same areas 2020, 1-15 Oct | same, 2022 | [FM 2022-11-05](https://web.archive.org/web/20221129141843/https://funghimagazine.it/aggiornamento-porcini-06-11-2022/): "fino ad Ottobre le nascite sono state quasi del tutto assenti" (FM 2020-10-08, 2020-10-15; FM 2022-10-28 "siccitose Sicilia e Sardegna") | the 2022 side is a look back |
| `etna_vs_sicani_erei_2021_september` | Etna 2021, 12-30 Sep | Sicani and Erei, same window | [FM 2021-09-24](https://web.archive.org/web/20211024074056/https://funghimagazine.it/aggiornamento-meteofunghi-24-09-2021-funghi-porcini-situazione-italia/): "lunghissime code d'auto" around Etna; "Tra Sicilia centrale e meridionale ... è sempre la siccità a farla da padrona" (FM 2021-09-10) | one outlet |
| `sicani_erei_iblei_2024_2021_september` | Sicani, Erei, Iblei 2024, 12-30 Sep | same, 2021 | [FM 2024-09-19](https://funghimagazine.it/aggiornamento-nascite-funghi-19-09-2024/): "situazione perfetta come non accadeva da tempo ... tra Sicani, Erei e Iblei oltre che sull'Etna" (FM 2024-08-16 rain; FM 2021-09-24) | one outlet |
| `sicani_ficuzza_vs_etna_2022_november` | Sicani and Ficuzza 2022, 25 Oct-20 Nov | Etna, same window | [FM 2022-11-05](https://web.archive.org/web/20221129141843/https://funghimagazine.it/aggiornamento-porcini-06-11-2022/): births continue in "il Trapanese e a tratti il Palermitano, l'Agrigentino", none of note in the east "tranno che localmente sull'Etna" (FM 2022-11-12, 2022-11-19) | FM swaps east and west twice in these bulletins; the provinces it names are unambiguous; the later bulletins are partly forecasts |
| `etna_nebrodi_vs_madonie_2023_october` | Etna and Nebrodi 2023, 1-15 Oct | Madonie, same window | [FM 2023-10-12](https://web.archive.org/web/20231012124159/https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "ancor meglio sui Nebrodi, ottime sull'Etna, appena sufficienti sulle Madonie" (FM 2023-10-27) | one outlet; FM also quotes a reader for whom nothing grew on the Nebrodi |
| `etna_nebrodi_2023_timing_october` | Etna and Nebrodi 2023, 1-15 Oct | same year, 20 Oct-10 Nov | [FM 2023-10-27](https://web.archive.org/web/20231027093132/https://funghimagazine.it/aggiornamento-porcini-27-10-2023/): "una buona buttata ... nella prima quindicina di ottobre", since then rain "quasi dappertutto, salvo che sulla Sicilia" (FM 2023-11-09) | the late side is partly inferred from weather |
| `etna_nebrodi_peloritani_2024_timing_late_summer` | same areas 2024, 25 Aug-30 Sep | same year, 10 Jun-10 Aug | [La Sicilia 2024-09-04](https://www.lasicilia.it/news/buongusto/2250580/il-fungo-porcino-dell-etna-da-record-trovato-sul-monte-minardo-a-bronte-e-pesantissimo.html): "Sono circa dieci giorni che piove ... una condizione ideale", about 10 kg in a day at Monte Minardo (FM 2024-06-14 "la siccità si fa sempre più pesante"; FM 2024-08-30 "finalmente si raccoglie!"; FM 2024-09-19) | the La Sicilia piece is a giant-porcino story |
| `etna_nebrodi_2024_2025_september` | Etna and Nebrodi 2024, September | same, 2025 | [Feeling Etna Trekking 2024-09-24](https://feelingetnatrekking.com/2024/09/24/i-porcini-della-faggeta-timparossa/): "la faggeta del Timparossa ha regalato un'enorme crescita di Boletus Edulis" (FM 2024-09-19; FM 2025-08-29, 2025-09-18, 2025-10-16) | the 2025 side is FM only, worded for all Sicily |
| `etna_nebrodi_2025_timing_autumn` | Etna and Nebrodi 2025, 12 Oct-15 Nov | same year, 1 Aug-30 Sep | [FM 2025-11-08](https://web.archive.org/web/20251220120016/https://funghimagazine.it/aggiornamento-nascite-08-11-2025/): "Continuano le nascite di Porcini ... tra Etna e Nebrodi, i meno comuni edulis e pinicola" (FM 2025-08-01, 2025-08-29, 2025-10-16) | one outlet |

There is no ovoli or gallinacci contrast: no source gives a verdict on two windows. The dated
mentions are late-May ovoli (2023, 2024) and first chanterelles at the end of April 2018, used in the
season rules instead.

**Outlets that block AI agents** (not fetched): Giornale di Sicilia (gds.it), Gazzetta del Sud,
MessinaToday, CataniaToday, PalermoToday.

Candidates left out:
- QdS (2022-10-14), "nascite di funghi come da anni non succedeva": a paraphrase of a national
  bulletin that says the late-summer storms spared "le isole maggiori".
- 2018 autumn against normal (FM: births "non si contano tra Sardegna, Sicilia, Calabria"): worded for
  the whole South.
- Etna and Peloritani against the Nebrodi and Madonie in August 2020: FM 2020-08-14 also had births on
  the Nebrodi and Madonie "a tratti", so the gap is small.
- May against June 2023: FM 2023-06-01 already reported "quasi insperate nascite" from the May rains.
- Forecasts ("è lecito attendersi", "sarà festa grande"), sagre, giant porcini, fines, rescues, and
  everything from 2026.

**Year picture from the sources** (context, not scored):
- **2016:** no dated verdict found.
- **2017:** a torrid summer and a poor late summer on Etna ("fallimentare").
- **2018:** abundant June and early July; an exceptional, rainy August on Etna; an autumn where births
  "non si contano" across the South.
- **2019:** a good late May on Etna and the Tyrrhenian slopes; a dry summer; a patchy September, with
  the first *B. edulis* on Etna above 1,200 m by 20 September.
- **2020:** the east good and the west poor all summer; "massicce e talvolta persino sbalorditive"
  births in the north and east in early October.
- **2021:** a good June on Etna and the Nebrodi; a torrid summer; car queues on Etna in September while
  the centre and south stayed dry.
- **2022:** "ferma al chiodo" in June; almost nothing until October; late October and November in the
  west (Trapanese, Palermitano, Agrigentino).
- **2023:** a rainy May with *B. aereus* in the macchia and chanterelles; a hot summer; a short good
  flush in the first half of October (Etna best, Madonie barely sufficient); a dry November.
- **2024:** a drought until mid-August; storms of up to 200 mm on the Iblei; "situazione perfetta" in
  September, with a *B. edulis* boom in Etna's Timparossa beech; porcini into November.
- **2025:** a good late May; "fuori dai giochi" through August and September; the season from mid-
  October, still going on 8 November with *B. edulis* and *B. pinophilus* on Etna and the Nebrodi.

## Places, for the intro copy

Sourced areas:
- **Porcini.**
  - The Nebrodi: Floresta (Pizzo Inferno, Favoscuro, the Castagnera), Ucria, Cesarò (Portella dei
    Bufali, the Torti), Monte Soro and Portella Femmina Morta, the Bosco di Semantile, Caronia, San
    Fratello, Castell'Umberto, Tortorici.
  - Etna: the north flank's beech and birch (Monte Timpa Rossa, Monte Maletto, Rifugio Citelli, Monti
    Sartorius, Sant'Alfio's Parrini, the Timparossa beech of Castiglione di Sicilia), the Pineta Ragabo
    of Linguaglossa, the chestnut and oak of Milo, Fornazzo (Zafferana Etnea), Pedara's Tardaria,
    Ragalna's Milia, the Bosco della Cerrita, and Bronte's Monte Minardo; the woods between Bronte and
    Randazzo.
  - The Peloritani: Colle San Rizzo (Messina), Castroreale.
  - In good years also the Sicani, Erei and Iblei (September 2024) and the Palermitano and
    Trapanese (November 2022).
  - Cork and holm oak lower down: Caronia, Partinico's Monte Mirto, the Bosco Scorace, the Iblei's
    Bosco di Baulì (Palazzolo Acreide) and Ferla, Piazza Armerina in the Erei.
- **Ovoli:** the Peloritani and Nebrodi hills, the northern Madonie (Gratteri, Cefalù, Pollina),
  Castiglione di Sicilia.
- **Gallinacci:** the Peloritani holm oak and pine (Colle San Rizzo, Dinnammare), the Etna chestnut
  belt (Nicolosi, Pedara), the Nebrodi (Sinagra, Caronia).
- **Seasons:**
  - The first *B. aereus*, *B. reticulatus* and chanterelles in the coastal macchia from late April,
    the first ovoli in late May.
  - May-June porcini, mostly *B. reticulatus*, in the chestnut, Turkey oak and beech of the Nebrodi
    and Etna.
  - A dry July-August, broken by storms in the high beech.
  - The main season from September at altitude and October-December below; when it starts depends on
    the first good rain, from late August (2018, 2024) to mid-October (2022, 2025).
  - Fornazzo (Milo) holds the first of the Etna mushroom festivals.
  - *B. aereus* into December in the holm and cork oak.

## Open questions and hand-offs

- **Habitat medians** (for the parent). The bands were set from sources and records before the grid
  existed. Check them against the build's habitat medians: if the beech median is well under 1,400 m
  or the chestnut's over 1,200 m, say so and the bands can be re-read.
- **Forest area** (for the region card). The Carta forestale's class 31a is 321,618 ha, 13 % over
  INFC 2015's bosco of 285,489 ha (the checklist quotes a "forest area of Sicily" of 512,121 ha with
  58 types, which must include scrub).
- **Plantation cells** (for the parent). About a third of 31a is reforestation (RI1-RI4). Pure
  Mediterranean-pine and eucalyptus cells get low porcini and ovolo habitat gates (0-0.1), but full
  chanterelle credit in the pines (0.3 saturates). Look at which group wins the combined score in
  those cells once the grid exists.
- **The laricio and *B. pinophilus*.** A pure laricio cell scores porcini only through the rarest
  key. No Sicilian record can test it; the census is the only evidence.
- **The eucalyptus 0.1.** Rests on the Erei reports, which the census doubts. Where the Carta
  forestale's RI1 polygons hold oak or chestnut, it may also be the map, not the fungus.
- **Rain scale** (for the weather or region card). No Sicilian gauge check was made here.
- **Slope and sun exposure.** Both stoppers are anchored on Tuscan grid percentiles. Check them on the
  Sicily grid once it is built: Etna's slopes are long and even, the Nebrodi rounded, the Madonie
  steep.
- **The regional law's amendments.** None found; the Region's portal (pti.regione.sicilia.it) refused
  connections, so the consolidated text could not be checked.
- **Madonie and Sicani.** No porcini record with a date: the census worked on Etna and the Nebrodi.
  The press mentions the Madonie a few times (late May 2019, summer 2020, October 2023) and names the
  Sicani only in 2024; otherwise it speaks of the island's west and south.
- **How long *B. aereus* lasts at altitude.** Forager lore ends the Bronte season in mid-September;
  the census has *B. aereus* on the same mountain on 25 November and 1 December. The windows keep the
  census; the sanity contrasts for October and November will show whether the scores agree.
- **Funghi Magazine's sectors.** Most contrasts rest on one magazine that names sectors of the island,
  mapped here to comuni by hand (see the sanity file header). The November 2022 bulletins swap east
  and west twice; the provinces they name decide.
- **Leads not read.** The Sicilian mycological literature the census cites is in print only: Napoli
  (1999, 2000) on the Etna chestnut and edible species, Signorello on Etna's Turkey oak and chestnut
  cenoses, Spagnolo & Russo (1997) *I funghi del Parco dei Nebrodi*, Mannina (1999) on the Bosco di
  Scorace, the *Rivista di Micologia Siciliana* of the AMB Gruppo Jonico Etneo. The Regional forest plan
  2021-2025 chapters (pti.regione.sicilia.it) could not be downloaded.

## References added for Sicilia

| id | kind | verified | used for |
|---|---|---|---|
| `vasquez2013_boletales_sicilia` | thesis | verified | the census: porcini records by month, height and wood; habitat seasons; law summary |
| `ferraro2022_checklist_sicilia` | peer-reviewed | verified | presence by province of the six taxa; holm oak to 1,500 m |
| `lr_sicilia_3_2006` | institutional | verified | the picking law |
| `ispra2021_raccolta_funghi_sicilia` | institutional | verified | the law in force, unchanged |
| `regione_sicilia_tesserino_funghi2023` | institutional | verified | the 2023 permit decrees |
| `micologiamessinese_edules` | web | verified | porcini hosts and seasons (folklore) |
| `micologiamessinese_caesarea` | web | verified | ovolo season and hosts (folklore) |
| `micologiamessinese_cantharellaceae` | web | verified | chanterelle hosts, *C. alborufescens* under holm oak (folklore) |
| `micologiamessinese_nebrodi` | web | verified | Nebrodi belts and fungi (folklore) |
| `pavone_signorello_funghi_etna` | institutional | verified | Etna seasons of *B. edulis* and *B. aereus* |
| `hortus_catinensis_etna_boschi` | institutional | verified | Etna forest belts |
| `barreca2010_pineta_ragabo` | peer-reviewed | verified | laricio 1,000-2,000 m, 5,654 ha |
| `seiler2021_etna_treering` | peer-reviewed | verified | Etna's beech and pine belts |
| `parks_nebrodi_ambiente` | web | verified | Nebrodi belts |
| `wikipedia_parco_madonie` | web | verified | Madonie belts, *Abies nebrodensis* |
| `sif_carta_forestale_sicilia` | dataset | verified | the forest map and its types (areas from the region card) |
| `infc2015_sicilia` | dataset | verified | forest area and categories |
| `arnone2013_rainfall_sicily` | peer-reviewed | verified | rain totals and the dry season |
| `mushma_occurrence_check_sicilia_2026` | analysis | verified | iNaturalist and GBIF counts, months, heights; Tuscany comparison |
| `fm_sicilia_2018_04_30` | web | verified | *B. aereus* and chanterelles in the macchia by late April (folklore) |
| `fm_sicilia_2018_05_09` | web | verified | "Estatini o aereus" in the Sicilian macchia in early May (folklore) |
| `fm_sicilia_2019_05_30` | web | verified | late-May 2019 *B. aereus* on Etna, Nebrodi, Peloritani and Madonie (folklore) |
| `fm_sicilia_2019_09_20` | web | verified | first *B. edulis* on Etna above 1,200 m in September (folklore) |
| `fm_calendario_autunno2019_sicilia` | web | verified | *B. edulis* in the southern beech, not pine; *B. reticulatus* under eucalyptus (folklore) |
| `fm_sicilia_2020_05_22` | web | verified | spring porcini near the sea and on Etna (folklore) |
| `fm_sicilia_2021_06_24` | web | verified | June 2021 flush; Sicily "poco adatta" for *B. pinophilus* (folklore) |
| `fm_sicilia_2023_05_25` | web | verified | the first ovoli in late May (folklore) |
| `fm_sicilia_2023_06_02` | web | verified | May 2023: *B. aereus* in the macchia, chanterelles, red porcini on upper Etna (folklore) |
| `fm_sicilia_2024_05_30` | web | verified | the first Sicilian ovoli on sale in late May (folklore) |
| `fm_sicilia_2024_09_19` | web | verified | September 2024; the short *B. aereus* flush on the northern Nebrodi (folklore) |
| `fm_sicilia_2025_11_08` | web | verified | November 2025 *B. aereus*, *B. edulis*, *B. pinophilus* on Etna and the Nebrodi (folklore) |
| `lasicilia_bronte118_funghi2018` | web | verified | the August 2018 Etna flush; porcini 7-8 days after heavy rain (folklore) |
| `lasicilia_minardo_porcino2024` | web | verified | rain and porcini at Monte Minardo, September 2024; a mid-September end (folklore) |
| `feelingetna_timparossa2024` | web | verified | the 2024 *B. edulis* boom in Etna's Timparossa beech (folklore) |

Existing references the Sicily changes lean on: `mushma_habitat_share_2026` and
`mushma_occurrence_check_2026` (the Tuscan levels and medians).
