# Species ecology: Friuli-Venezia Giulia (regional appendix to species-ecology.md)

Research date: 2026-09-27 (dates Europe/Rome, units metric). Card:
`region-friuli-venezia-giulia-species.md` (child of `region-friuli-venezia-giulia.md`). Rule files:
`api/src/api/config/species/friuli_venezia_giulia/`. This appendix records how the Tuscan rule set
(`species/tuscany/`) was carried to Friuli-Venezia Giulia (FVG), what changed and why. It covers
**fruiting conditions only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(29 added for this region, in one block at the end of the file, keys prefixed `fvg_` or with a
`_fvg_` infix). Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md):
**strong**, **plausible**, **folklore**. Every number is a prior for the backtest; season windows,
altitude bands and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).
Piemonte ([`piemonte.md`](piemonte.md)) was the template; the Trentino-Alto Adige and Lombardia
appendices (branches `region/trentino-alto-adige`, `region/lombardia`) were read for method, and
none of their sources is cited here unless it was opened again for this card.

## Summary

1. **All three groups and all six keys are kept.** The thin keys are well recorded here once the
   right record set is found:
   - ***B. aereus*** has no iNaturalist or GBIF record in FVG, but 255 records in the north-east
     census (MUSE), 230 of them on the Trieste Karst. FVG holds 83 % of all the census's records of
     it. It is the Karst porcino, in October above all.
   - **Ovoli** have 147 census records, 127 on the Trieste Karst, the rest in the Cividale hills, the
     moraine hills and the Pordenone foothills. The regional law bans picking "Amanita cesarea allo
     stato di ovolo chiuso" (`fvg_lr25_2017`).
2. **Public records are almost empty; the census and the neighbours carry the numbers.**
   - FVG has 3,172 iNaturalist fungi records (Lombardia 36,719), with 14 *B. edulis*, 5
     *Cantharellus* and 1 ovolo. GBIF adds almost nothing.
   - The census holds about 2,400 undated FVG records of the six taxa. They show where each taxon
     grows, not when.
   - Timing comes from next door: the Austrian Mycological Society's dated Carinthian records with
     recorder elevations (`fvg_omg_observations`, about 1,000 records), Slovene iNaturalist (about
     700) and the census's own month and altitude charts, half of them FVG's for four of the taxa.
3. **Two regions in one.**
   - **The mountains:** the Carnian and Tarvisio spruce, fir and beech hold *B. edulis*, *B.
     pinophilus* and chanterelles. There the season is split by elevation: above 900-1,300 m it
     ends in early October, as it does in Carinthia (Lombardia and Piemonte made the same split).
   - **The Karst and the low hills** (oak, hop-hornbeam, chestnut) hold *B. aereus*, *B.
     reticulatus*, ovoli and a second chanterelle pole. There fruiting runs through October: "in
     particolare nei mesi di ottobre e novembre" on the Trieste Karst (`fvg_cebulec_pertot1992`).
4. **Black pine is not a porcino tree here.**
   - Three quarters of the `mountain_pine` class, 15 % of the region's woods, is black pine: native
     in the Prealpine valleys, planted on the Karst from the second half of the 1800s.
   - An 11-year survey of the Trieste Karst lists the plantations' fungi and no *Boletus* among
     them (`fvg_cebulec_pertot1985`, `fvg_cebulec_pertot1992`). The Slovene Karst black pine held no
     *Boletus* mycelium (`mrak2025_mycorrhiza`).
   - So the class drops to marginal for *B. edulis* and *B. reticulatus*, stays secondary for *B.
     pinophilus*, and stays non-host for *B. aereus* and ovoli.
5. **Weather rules are all Tuscany's.** No FVG, Slovene or Carinthian study ties these fungi to rain
   or temperature in numbers. The qualitative statements found (steady rain over 2-4 days, a flush
   within about a week, the bora drying the Karst) fit the Tuscan rules. The region's rain runs from
   1,000 mm on the coast to over 3,300 mm on the Musi. The porcini 30-day rain already scores it
   against each cell's own normal.
6. **Evidence.** The 29 new references were all opened:
   - 10 institutional (the picking law, the forest typology, INFC, ARPA climate reports, Tarvisio
     forest, the Slovene protection decree, the Region's species names);
   - 12 society (the census pages, two Karst surveys, Carinthian checklists, Friulian and Slovene
     society pages, the Cansiglio checklist next door);
   - 2 datasets, 3 press, 2 own analyses.

   `sanity.yaml` holds 16 press contrasts (14 porcini, 1 gallinacci, 1 ovoli) across the Alps,
   Prealps, hills and Karst, 2016-2025. Every main source was opened and each quote checked against
   the page.

## At a glance: what differs from Tuscany and why

Trapezoids are `[zero, full, full, zero]`, dates `DD-MM`, altitudes in metres.

| key | factor | Tuscany | Friuli-Venezia Giulia | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | 01-07 → 01-09 … 15-11 → 20-12 | **lowland 15-06 → 01-08 … 31-10 → 30-11 below 900 m; Alpine 01-07 → 25-07 … 25-09 → 25-10 above 1,300 m** | Carinthian records: October or later 22-40 % below 1,000 m, 5 % at 1,000-1,400 m, 2 % above; Slovene Julian Alps to 25 October; latest census record 3 November (Ovaro, 946 m) | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **200 → 600 … 1,800 → 2,200** | census mode 1,200-1,500 m, 3 % below 600 m; woods end at 1,700-1,900 m | plausible |
| *edulis* | habitat | deciduous oak 0.3, mountain pine 0.6, other conifer 0.3, transitional 0.3 | **0.1, 0.3, 0.1, 0.1** | Karst oak scrub: no *B. edulis* in 11 years; black pine; larch; mugo and green alder | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,200 → 1,600** | census 16 % at 900-1,200 m, 8 % at 1,200-1,500 m; Carnian squares | plausible |
| *reticulatus* | habitat | mountain pine 0.6, transitional 0.6 | **0.3, 0.1** | black pine brought no *Boletus*; subalpine scrub | plausible |
| *aereus* | season | upland/lowland split at 400-600 m | **one window 15-06 → 01-08 … 31-10 → 30-11** | census (83 % FVG) peaks in October (43 %), second peak August | plausible |
| *aereus* | altitude | … 800 → 1,250 | **… 600 → 900** | census 95 % below 600 m | plausible |
| *aereus* | habitat | mixed broadleaf 0.3, transitional 0.6 | **0.6, 0.1** | hop-hornbeam woods are hosts; subalpine scrub | plausible |
| *pinophilus* | season | spring + autumn windows, gap 20-07 → 15-08 | **lowland 01-05 → 01-06 … 31-10 → 30-11; Alpine 01-06 → 01-07 … 25-09 → 25-10; handover 900-1,300 m** | census May-October with no gap; Carinthia to 20-26 October low down, September high up | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **400 → 700 … 1,700 → 2,100** | census nothing at 300-600 m, mode 900-1,200 m; Carinthia 490-1,450 m | plausible |
| *pinophilus* | habitat | other conifer 0.3, mixed broadleaf 0.3, transitional 0.3 | **0.1, 0.1, 0.1** | larch; calcareous hop-hornbeam; scrub | plausible |
| ovoli | season | 01-06 → 01-09 … 05-11 → 30-11 | **01-06 → 01-08 … 31-10 → 30-11** | census (55 % FVG) August 33 %, September 30 %, October 24 % | plausible |
| ovoli | altitude | … 750 → 1,100 | **… 650 → 1,000** | FVG squares all below about 600 m; absent from Carinthia "über 400 m" | plausible |
| ovoli | habitat | transitional 0.6 | **0.0** | here subalpine scrub | plausible |
| gallinacci | season | lowland 15-04 → 10-05 … 15-12 → 25-01; mountain … 15-10 → 15-11; handover 600-1,000 m | **lowland 15-05 → 15-06 … 31-10 → 10-12; mountain 01-06 → 01-07 … 30-09 → 31-10; handover 900-1,300 m** | no winter mode; Carinthian records at altitude end in September | plausible |
| gallinacci | altitude | … 1,000 → 1,700 | **… 1,800 → 2,100** | census mode 1,200-1,500 m, 20 % at 1,500-1,800 m | plausible |
| gallinacci | habitat | beech 0.6, fir/spruce 0.6, deciduous oak 0.3, other conifer 0.3, transitional 0.3 | **1.0, 1.0, 0.6, 0.1, 0.1** | *C. cibarius* s.str.; Carnian pole in spruce-fir-beech, Karst pole in oak woods | plausible |
| every key | slope stopper | x1 to 25°, x0.8 from 40° | **x1 to 36°, x0.8 from 48°** | the same rule on the region grid: woodland p90 36.2°, max 48.6° | as Tuscany (plausible) |
| every key | weather, growth clock, sun exposure, other stoppers | — | **kept** | no regional numbers; see Weather and Slope and sun exposure | as Tuscany |

Kept on purpose:
- the *B. reticulatus* season (Tuscany's, closing on 15 November): the census still has 10 % of its
  records in October;
- beech, chestnut and fir/spruce as hosts of *B. edulis* and *B. pinophilus*;
- mountain pine at 0.6 for *B. pinophilus* (not the 1.0 of the Scots-pine regions);
- the gallinacci and ovoli soil-pH and lithology rules, still disabled.

**Effect on the grid.** Habitat and altitude gates only, on the region grid's 3,304 woodland cells
(`mushma_fvg_forest_check_2026`):

| key | habitat gate full on (Tuscan → regional rules) | altitude gate full on | mean of both gates (Tuscan → regional) |
|---|---|---|---|
| *edulis* | 98 % → 88 % | 62 % → 71 % | 0.80 → 0.83 |
| *reticulatus* | 98 % → 98 % | 66 % → 74 % | 0.82 → 0.87 |
| *aereus* | 23 % → 32 % | 44 % → 29 % | 0.39 → 0.31 |
| *pinophilus* | 98 % → 88 % | 53 % → 63 % | 0.74 → 0.72 |
| ovoli | 23 % → 22 % | 40 % → 32 % | 0.32 → 0.29 |
| gallinacci | 97 % → 97 % | 61 % → 100 % | 0.84 → 0.99 |

And by area (mean of the two gates, regional rules; areas as in `sanity.yaml`):

| key | Carnia | Tarvisiano | Dolomiti Friulane (PN) | Julian Alps and Prealps | hills | Karst |
|---|---|---|---|---|---|---|
| *edulis* | 0.97 | 0.99 | 0.95 | 0.91 | 0.25 | 0.08 |
| *reticulatus* | 0.81 | 0.78 | 0.89 | 0.90 | 0.91 | 0.91 |
| *aereus* | 0.11 | 0.03 | 0.17 | 0.27 | 0.90 | 0.98 |
| *pinophilus* | 0.91 | 0.99 | 0.85 | 0.78 | 0.08 | 0.02 |
| ovoli | 0.08 | 0.05 | 0.13 | 0.28 | 0.91 | 0.98 |
| gallinacci | 1.00 | 0.99 | 1.00 | 0.99 | 0.93 | 1.00 |

That is the census's map. *B. edulis* and *B. pinophilus* sit in the mountains, with 4 and 1 of
their FVG census points on the Karst. *B. aereus* and ovoli sit on the Karst and in the hills.
*B. reticulatus* and chanterelles have both poles.

## Friuli-Venezia Giulia in brief

**Woods.** The grid reads the Region's Tipologie forestali 2013 map, typed by Del Favero's regional
typology (`fvg_del_favero2016`; mapping and codes in `regions/friuli_venezia_giulia.md`).
- **Area:** the map holds 308,000 ha of forest (grid build 2026-09-27, 7 % under INFC 2015's
  332,556 ha of *bosco*).
- **Inventory:** INFC 2015 counts 323,362 ha of *boschi alti*, 41 % of the region, of which
  faggete 90,645 ha (28 %), spruce 44,597, black pine 31,554, larch 12,971 and chestnut 12,264
  (`fvg_infc2015_categorie`).
- **Grid:** the 3,304 woodland cells run from 6 m to 1,898 m, median 874 m (p10 312 m, p90 1,402
  m).

**Which habitat holds which tree.** From the region config and the forest-type map
(`mushma_fvg_forest_check_2026`; forest groups only, centroid elevations from Copernicus GLO-30):

| habitat key | FVG types (ha) | share | median elevation (p10-p90) |
|---|---|---|---|
| `beech` | faggete: submontane, montane (esalpica and mesalpica), altimontane, subalpine (79,339) | 25.7 % | 1,060 m (682-1,350) |
| `mountain_pine` | native black pine (35,160: "submontana con ostria", "tipica", "con faggio", primitive), Scots pine (8,300, mostly Val Canale), pine plantations (3,659, 2,556 of them on the Karst) | 15.3 % | 785 m (408-1,182) |
| `mixed_broadleaf` | orno-ostrieti (18,249), aceri-frassineti and aceri-tiglieti (14,401), new woodland (5,338), carpineti (2,599), birch and hazel (1,782) | 14.0 % | 594 m (335-871) |
| `mixed_broadleaf_conifer` | piceo-faggeti (27,225) and abieti-piceo-faggeti (11,535) | 12.6 % | 1,200 m (923-1,452) |
| `fir_spruce` | peccete (28,858), abieteti and piceo-abieteti (7,841), spruce plantations (1,733) | 12.5 % | 1,263 m (752-1,622) |
| `deciduous_oak` | ostrio-querceti, the Karst's downy oak and hop-hornbeam scrub (18,324); rovereti, incl. the "rovereto tipico carsico" (1,403); lowland querco-carpineti (1,390) | 6.8 % | 254 m (93-499) |
| `chestnut` | castagneti, on the flysch of the Natisone, Torre and Judrio valleys, the Collio and the Pordenone foothills (17,852) | 5.8 % | 393 m (202-573) |
| `exotic_broadleaf` | robinieti (10,370) | 3.4 % | 184 m (75-312) |
| `other_conifer` | larch woods (4,674), multi-species conifer plantations (1,353), larch plantations (293) | 2.1 % | 1,574 m (829-1,787) |
| `riparian` | golenal, fluvial-terrace and marsh woods, black alder (5,226) | 1.7 % | 54 m |
| `evergreen_oak` | ostrio-lecceta of the Trieste coast (250) | 0.1 % | 11 m |
| `transitional_woodland_shrub` (not woodland) | mughete (12,880), green alder (3,789), subalpine willow | (16,957 ha) | 1,604 m |
| `mediterranean_pine`, `macchia` | — | absent | |

Notes:
- The Lignano and Grado coastal pinewoods, planted from the 1930s on native black pine with
  maritime, stone and Aleppo pine (`fvg_del_favero2016`), are barely mapped. No cell carries
  `mediterranean_pine`, so its affinities are left as Tuscany's.
- Del Favero's forest regions frame the rules:
  - the **endalpica** and **mesalpica** (Carnia, Val Canale, 1,400-1,900 mm): spruce, fir,
    spruce-beech, larch at the tree line "a mo' di cimosa delle peccete";
  - the **esalpica** (the Prealps, 1,800 mm to over 3,000 mm): beech "domina nettamente", black
    pine on the rough carbonate slopes;
  - the **avanalpica** (foothills and hills, 1,400-1,800 mm): chestnut on the silicate flysch,
    orno-ostrieti and ostrio-querceti on limestone;
  - the **carsica**: "l'ostrio-querceto a scotano, spesso sostituito da piantagioni di pino nero".
- **Belts:** the montane-subalpine spruce limit lies "fra 1300 e 1600-1800 m"; in Tarvisio "Sopra i
  1700 m s.l.m. le formazioni forestali cedono il passo ad arbusteti a pino mugo"
  (`fvg_tarvisio_foresta`).
- **Tarvisio:** the state forest covers 23,300 ha at 600-2,500 m, spruce 55 %, beech 30 %, other
  conifers 15 %.

**Climate** (`fvg_arpa_clima2023`, `fvg_arpa_schede_rr2023`, 1991-2020):
- **Rain:** coast 900-1,000 mm; plain and hills 1,100-1,800 mm; Prealps 2,400-3,400 mm "(da primato
  europeo)", over 3,300 mm on the Musi chain (Taipana, Lusevera, Resia); inner Alps 1,400-1,600 mm.
- **Regime:** February driest; a first peak in May; July-August lower with frequent storms ("1
  giorno su 2 in estate si hanno temporali"); November wettest (450 mm at Musi). On the Karst July is
  the driest month (75-80 mm) and September-November the wettest.
- **Temperature:** about 0.7 °C per 100 m, with strong inversions; Tarvisio is colder than the rest
  at equal height.
- **Wind:** the bora, dry and cold, makes the Karst the region's driest air, mostly in winter but
  "non è raro nelle altre stagioni". The press also blames the warm foehn for drying the hills and the
  Karst in autumn 2023 (see Press contrasts).
- **Drought years:** 2003, 2012 (Karst dieback of hop-hornbeam, downy oak and black pine,
  `fvg_arpa_impatti_cc2018`) and 2022, the hottest year on record, with rain 30-50 % below normal
  (`fvg_arpa_report2022`).

**Picking rules** (`fvg_lr25_2017`). None of them changes where or when the fungi fruit, so none is
encoded.
- L.R. 25/2017 (not the forest law 9/2007), text in force from 8 August 2026: 3 kg a person a day; a
  permanent permit after an oral exam, plus a yearly fee (EUR 60 region-wide); searching from one
  hour before sunrise to one hour after sunset.
- **No season calendar and no odd/even days.**
- Banned: "Amanita cesarea allo stato di ovolo chiuso", *B. edulis*-group caps under 3 cm, picking
  in regional reserves and biotopes; the two regional parks set their own rules.
- **Next door:**
  - Slovenia allows 2 kg a day, and *A. caesarea* is a protected species there
    (`fvg_si_uredba_gliv2011`);
  - Carinthia allows 2 kg a day, and porcini and chanterelles only "vom 15. Juni bis 30. September"
    (`fvg_ktn_pilzschutz`).

  Both thin the neighbours' records: Slovene ovoli are rare in public data, and Carinthian October
  records fall partly because picking stops.
- **Names:** the Region's list calls *C. cibarius* "gialletto o galletto" and *C. lutescens* / *C.
  tubaeformis* "finferle" (`fvg_rafvg_funghi2005`), so Friulian "finferli" may mean *Craterellus*.
  The press contrasts below use "gialletti"/"galletti" only.

## Sightings (occurrence cross-check)

Queried 2026-09-27 (`mushma_fvg_occurrence_check_2026`). Aggregates only; no coordinates are stored.
- **iNaturalist:** place 10869 (FVG), 10464 (Kärnten), 8228 (Slovenia), 33203 (Belluno), verifiable
  records.
- **GBIF:** `gadmGid=ITA.7_1` (FVG) and `AUT.2_1` (Carinthia), country SI.
- **Elevations:** from the Copernicus GLO-30 tiles (the Open-Meteo quota is shared, so it was not
  used), for records that are not obscured and have an accuracy of 1 km or better. Carinthian
  Austrian Mycological Society records carry the recorder's elevation.
- **Enrichment:** the taxon's monthly share ÷ the monthly share of all the place's iNaturalist fungi.

**FVG itself.** 3,172 iNaturalist fungi records (August 491, September 624, October 498).

| taxon | iNaturalist | GBIF (iNaturalist copies) | north-east census points in FVG (UD / PN / GO / TS) |
|---|---|---|---|
| *B. edulis* | 14 (9 observer-days: Aug 4, Sep 4, Oct 1), located at 210-1,246 m | 10 (9) | 539 (530 / 5 / 0 / 4) |
| *B. reticulatus* | 2 (May, Aug) | 1 | 468 (168 / 31 / 0 / 269) as *B. aestivalis* |
| *B. aereus* | 0 | 0 | 255 (25 / 0 / 0 / 230) |
| *B. pinophilus* | 2 (Aug, Oct) | 2 | 32 (31 / 0 / 0 / 1) |
| *A. caesarea* | 1 (Trieste Karst, 27 Oct 2020, about 190 m) | 0 | 147 (10 / 7 / 3 / 127) |
| *Cantharellus* | 5 (Jul-Oct; 2 *C. cibarius*, 2 *C. friesii*) | 3 | 952 (606 / 17 / 0 / 329) *C. cibarius* |

**The north-east census** (`muse_censimento_edulis`, `fvg_muse_censimento_aestivalis`,
`muse_censimento_boletus`, `muse_censimento_pinophilus`, `fvg_muse_censimento_caesarea`,
`muse_censimento_cibarius`).
- **What it is:** the survey of the Trentino-Alto Adige, Veneto and FVG mycological federations,
  hosted by MUSE, with about 200,000 records.
- **Map points:** each is one record, most on the centre of a 3' × 5' square, with no date or
  altitude. The counts above are my recount of the points inside the ISTAT 2025 FVG provinces; the
  research agent's count, which left out the squares whose centre falls across the border, is a
  little lower (*B. edulis* 490, *B. pinophilus* 28, the others within 5 %).
- **Where they fall:**
  - *B. edulis*: Rigolato 158, Ampezzo 44, Tarvisio 42, Prato Carnico 41, Sappada 35, San Leonardo
    26 (Natisone valleys);
  - *B. aereus*: San Dorligo della Valle 92, Monrupino 71, Trieste 54, Cividale 17;
  - ovoli: Trieste 69, San Dorligo 42;
  - *C. cibarius*: Forni Avoltri 211, San Dorligo 211, Ampezzo 77.
- **Charts:** each species page draws a month chart and an altitude chart for the whole north-east
  (tallest bar = 200). For four taxa FVG is half or more of the records:

| taxon (FVG share) | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* (36 %) | | | | | | 9 | 89 | **200** | 148 | 48 | 2 | |
| *B. aestivalis* (52 %) | | 1 | | | 14 | 142 | **200** | 173 | 94 | 68 | 2 | 1 |
| *B. aereus* (83 %) | 4 | 1 | | | | 30 | 46 | 116 | 55 | **200** | 7 | 1 |
| *B. pinophilus* (11 %) | | | | | 33 | 116 | 63 | 129 | **200** | 81 | | |
| *A. caesarea* (55 %) | 6 | | | | | 6 | 58 | **200** | 179 | 146 | 8 | |
| *C. cibarius* (50 %) | 1 | | | | 10 | 73 | 154 | **200** | 115 | 51 | 11 | 2 |

| taxon | <300 | 300-600 | 600-900 | 900-1,200 | 1,200-1,500 | 1,500-1,800 | 1,800-2,100 m |
|---|---|---|---|---|---|---|---|
| *B. edulis* | 4 | 13 | 59 | 128 | **200** | 95 | 20 |
| *B. aestivalis* | 86 | **200** | 159 | 96 | 48 | 10 | 3 |
| *B. aereus* | 127 | **200** | 14 | 1 | 1 | | |
| *B. pinophilus* | 2 | | 68 | **200** | 132 | 49 | 10 |
| *A. caesarea* | **200** | 104 | 60 | 31 | 4 | | |
| *C. cibarius* | 48 | 123 | 81 | 113 | **200** | 141 | 14 |

- **Extremes worth quoting:** the latest *B. edulis* of the whole census is Friulian ("3 nov.
  2024 - Villa Val (Ovaro, UD) 946 m"); the latest ovolo is 14 November 2004 at 175 m in Trieste; the
  lowest records of *B. edulis*, *B. aestivalis*, *B. aereus* and *C. cibarius* are all at 10 m in
  lowland woods at Cervignano del Friuli.
- **Winter dates:** a few January and December Karst "records" of porcini, ovoli and chanterelles,
  two taxa on the same day by one recorder, look like recording dates. They make the small
  January-December bars and do not open winter windows.

**Carinthia** (`fvg_omg_observations`). Austrian Mycological Society records since 1990, recorder
elevations, by band:

| taxon | band | n | Jun | Jul | Aug | Sep | Oct | Nov | p95 date | October or later |
|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | < 600 m | 20 | 4 | | 1 | 7 | 8 | | 23 Oct | 40 % |
| | 600-1,000 m | 74 | 5 | 5 | 24 | 24 | 15 | 1 | 23 Oct | 22 % |
| | 1,000-1,400 m | 105 | 3 | 12 | 37 | 48 | 5 | | 28 Sep | 5 % |
| | ≥ 1,400 m | 41 | | 9 | 22 | 9 | 1 | | 9 Sep | 2 % |
| *Cantharellus* | < 600 m | 75 | 18 | 9 | 3 | 14 | 29 | | 23 Oct | 39 % |
| | 600-1,000 m | 138 | 22 | 10 | 53 | 31 | 19 | 3 | 22 Oct | 16 % |
| | 1,000-1,400 m | 158 | 8 | 26 | 53 | 64 | 7 | | 28 Sep | 4 % |
| | ≥ 1,400 m | 73 | 1 | 18 | 37 | 15 | 2 | | 13 Sep | 3 % |
| *B. pinophilus* (all years) | < 1,000 m | 31 | 5 | 2 | 1 | 14 | 9 | | 26 Oct | 29 % |
| | 1,000-1,400 m | 10 | | 1 | 2 | 7 | | | 23 Sep | 0 % |

- **Elevations** (recorder values, all years): *B. edulis* 415-1,900 m (median 1,050 m, n=290),
  *Cantharellus* to 1,900 m (median 950 m, n=546).
- **Species:** *B. aereus* has 11 records, none since 1965; *A. caesarea* none.
- **iNaturalist enrichment:** *B. edulis* August 1.9, September 2.1, October 0.5; *Cantharellus*
  July 2.5, August 1.4, October 0.4. *Cantharellus* records are 114 *C. cibarius* of 124 identified
  to species.

**Slovenia.**
- **iNaturalist:**
  - *B. edulis* (81 records) peaks later than in Carinthia: September 2.1, October 1.4. Located
    records (n=57) run 235-1,486 m, median 637 m. At 1,000-1,400 m, 5 of 17 are from October, the
    latest 28 October (Pokljuka, Karawanks).
  - *B. reticulatus* (396, 342 of them from one Dolenjska observer): June 4.0, July 3.9, August
    2.4, September 0.3, October 0.5. Median 470 m, max 1,607 m.
  - *Cantharellus* (191): June 3.0, July 1.8, then about 1 into October. Below 600 m, 32 of 83 are
    from October or later, the latest 14 December on the coast. 139 of the 164 identified to species
    are *C. cibarius*.
  - Ovoli: 10 records, all obscured as a protected taxon, September 3.1x the effort.
- **Boletus informaticus maps** (`fvg_bi_maps`), quadrants of about 6 × 6 km:
  - *B. aereus* in 105 quadrants; in the west only Goriška, Brda, the lower Vipava valley, the Karst
    and Istria;
  - *A. caesarea* in 142 quadrants, lowland and hills, with the upper Soča dots all pre-2000;
  - none of the taxa is mapped by month.

**Belluno** (Veneto, next to Carnia and the Cansiglio): 19 *B. edulis* (July-October, median 1,156
m) and 24 *Cantharellus* iNaturalist records; too few to use beyond agreement.

**Caveats.**
- **Undated census points.** The census map points have no dates. The phenology charts are
  north-east-wide, and only for *B. aereus* are they mostly FVG's.
- **Next door is not FVG.** Carinthia's slopes face north and are colder, and its law ends picking
  on 30 September. Slovenia's records are mostly Dolenjska and the Dinaric plateaus.
- **Priors, not fits.** The season, band and habitat choices are drawn partly from these same
  records and charts, all years included, so they stay frozen priors.
- **Nothing to validate on.** With about 20 public FVG records a season, the backtest cannot tune
  anything here. The sanity contrasts and the census's map are the checks.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Which porcino where** (society, the census map):
  - *B. edulis*: Carnia, the Tarvisiano and the Natisone valleys, with a herbarium collection in a
    beech wood at 800 m (Lovea, Arta Terme, 18 September 1993); 5 records in the Pordenone Prealps
    and 4 on the Karst.
  - *B. reticulatus*: everywhere, from the Karst (269) to Carnia, Aviano and Barcis.
  - *B. aereus*: the Trieste Karst and Cividale only.
  - *B. pinophilus*: the Carnian valleys and Tarvisio.
  - A Udine mycologist in 2016: the porcino nero is "Ancora presente, ma raro"
    (`fvg_ilpiccolo_2016_09_11`).
- **The Karst survey** (`fvg_cebulec_pertot1985`, `fvg_cebulec_pertot1992`; society journal). It
  covers 1,280 ha at Basovizza-Lipizza, 300-476 m, 1980-1990: hop-hornbeam and downy oak, sessile
  oak, black-pine plantations and doline hornbeam.
  - Porcini found: *B. aereus* "poco frequente", *B. aestivalis* "raro"; **no *B. edulis***.
  - The fungi the black pine brought: *Suillus*, *Chroogomphus*, *Tricholoma*, *Cantharellus
    lutescens*, no *Boletus*. In the plantations "vengono a mancare le rispettive specie
    micorriziche" of the broadleaves.
  - Fruiting peaks "in particolare nei mesi di ottobre e novembre".
- **Next door:**
  - Slovenia: *B. aereus* "največ pod hrasti in kostanji"; *B. pinophilus* "raste največ pod bori,
    tudi pod bukvami", May to November; *B. reticulatus* "mikorizna z listavci" (`fvg_gobe_si`).
  - Carinthia: *B. pinophilus* "Überall in Kärnten als Kiefernbegleiter"
    (`fvg_sperdin1975_roehrlinge`).
  - Karawanken: *B. edulis* in warm Scots pine and beech-mixed woods at about 1,000 m
    (`fvg_friebes2017_ferlach`).
- **Season, locally** (press, folklore):
  - normally "la prima buttata di fine giugno riguarda le zone basse";
  - "sono le piogge settembrine che allungano la raccolta fino a metà ottobre"
    (`fvg_ilpiccolo_2016_09_11`);
  - a porcino at Zuglio on 12 November 2019 was "raccolto fuori stagione, segno che, mentre i monti
    si imbiancano di neve, poco più a valle prosegue la stagione dei funghi porcini"
    (`fvg_messaggeroveneto_2019_11_13`).

**Decisions** (numbers in the table above; the full reasoning is in each factor's `notes`):

- ***B. edulis* season: two windows blended at 900-1,300 m.**
  - **Why split:** the Carinthian records change shape across 1,000 m. Below it the season runs to
    late October; above it October holds 2-5 % of the records. The Tuscan window would keep Carnian
    spruce cells in season into December, held only by frost and snow.
  - **Alpine window:** full 25 July-25 September, closed by 25 October. The later close than
    Carinthia's records suggest allows for the Slovene late-October records at 1,200-1,450 m and for
    Carinthia's picking stop on 30 September.
  - **Lowland window:** full 1 August-31 October, closed by 30 November, with a ramp from mid-June
    for the low zones' late-June flush.
- ***B. edulis* altitude: full 600-1,800 m.** The census has 3 % of its records below 600 m, and the
  woods end at 1,700-1,900 m. The ramp from 200 m runs through the chestnut belt.
- ***B. edulis* hosts:**
  - **deciduous oak 0.3 → 0.1:** the class is 87 % Karst and Prealpine ostrio-querceti on
    limestone, where 11 years of survey found no *B. edulis*;
  - **mountain pine 0.6 → 0.3:** mostly black pine, with no porcino in the Karst plantations. Pure
    pine cells still get full credit under the 0.3 saturation; if the Prealpine black pine scores high
    in the sanity check or the backtest, 0.1 is the next step;
  - **larch (`other_conifer`) and subalpine scrub (`transitional`) 0.3 → 0.1:** as in
    Trentino-Alto Adige and Lombardia.
- ***B. reticulatus*:**
  - the Tuscan season is kept, since the census has 10 % of its records in October;
  - the band reaches 1,200 m full, zero at 1,600 m, for the Carnian squares;
  - black pine drops to marginal (0.3) and subalpine scrub to non-host (0.1).
- ***B. aereus*:**
  - one window, full 1 August-31 October, closed by 30 November: the census has an August flush and
    an October peak;
  - the band is cut to the plateau and the hills: full to 600 m, zero at 900 m;
  - hop-hornbeam woods (`mixed_broadleaf`) rise to secondary (0.6), as in the Marche: a documented
    host (`funghimagazine_carpino_nero2026`), and the Karst plot where it was found is hop-hornbeam
    and oak wood.
- ***B. pinophilus*:**
  - no summer gap, and an Alpine window above 900-1,300 m like *B. edulis*;
  - band 700-1,700 m full, zero at 400 m and 2,100 m;
  - larch, subalpine scrub and hop-hornbeam woods drop to non-host (0.1);
  - mountain pine stays secondary (0.6), not full: it is mostly black pine here.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Census:** 147 FVG points (`fvg_muse_censimento_caesarea`), on the Trieste and Gorizia Karst,
  around Cividale, Majano and Trasaghis, and along the Pordenone foothills from Caneva and Polcenigo
  to Travesio. No square above about 600 m but one at Sappada, read as an outlier.
- **Karst survey:** "A. caesarea ... - raro" on the Basovizza plot (`fvg_cebulec_pertot1985`).
- **Friulian society:** "specie termofila, predilige i boschi di quercia e castagno. Raro ma fedele
  ai luoghi di crescita" (`fvg_ambf_caesarea`).
- **Press:** a decade-long decline, "ormai si trova raramente nel Cividalese"
  (`fvg_ilpiccolo_2016_09_11`), but "tantissimi porcini e ovuli" on the Trieste Karst in October 2017
  (`fvg_ilpiccolo_2017_10_12`), and "Ovoli più del solito ... soprattutto in provincia di Udine e
  Trieste, principalmente sui colli vitivinicoli" in 2025 (Funghi Magazine, 2025-09-17).
- **Next door:**
  - Slovenia: lowlands and hills, the Karst by the Italian border, Brda and Tolmin, protected, on
    poor calcareous soil "zlasti pod kostanji in bukvami", July-October (`fvg_bi_maps`,
    `fvg_gobe_si`);
  - Carinthia: never recorded; in 1983 "die Meereshöhe (in Kärnten über 400 m)" was blamed, and the
    nearest populations placed "In der Umgebung von Laibach oder Triest"
    (`fvg_sperdin1983_amanita`).

**Decisions.**
- **Season:** full 1 August-31 October (Tuscany 1 September-5 November), from 1 June, closed by 30
  November. The census profile (55 % FVG) is August 33 %, September 30 %, October 24 %, November 1
  %.
- **Altitude:** full to 650 m, zero at 1,000 m (Tuscany 750 → 1,100 m). No source gives an FVG
  limit. The FVG squares are all low, and the north-east forager limit is "600 metri"
  (`funghimagazine_ovolo`).
- **Hosts:**
  - oak and chestnut stay hosts;
  - subalpine scrub drops to non-host (0.0);
  - beech stays non-host, though Slovene pages name it: FVG's beech sits at a median 1,060 m, above
    the band;
  - black pine stays non-host: the Karst cells get their credit from the oak woods around the
    plantations (77 % of the Trieste woodland is the deciduous-oak class).

## Gallinacci (*Cantharellus* s.l.: "gialletti", "galletti")

**Regional evidence.**
- **Census:** about 950 FVG points (`muse_censimento_cibarius`) in two poles:
  - **the Carnian and Tarvisio mountains** (Forni Avoltri, Rigolato, Ampezzo, Prato Carnico,
    Tarvisio), with a herbarium collection in beech at 800 m;
  - **the Trieste Karst** (about 330: San Dorligo della Valle, Trieste, Monrupino, Muggia).
- **Karst survey:** *C. cibarius* "raro" and its var. *pallidus* "poco frequente" on the Basovizza
  plot in 1980-84.
- **Warm segregates on the Karst coast:** *C. alborufescens* (latest 28 November, Miramare) and *C.
  ferruginascens* (peak October, latest 28 December in a holm-oak wood at Miramare)
  (`muse_censimento_alborufescens`, `fvg_muse_censimento_ferruginascens`).
- **Next door:**
  - the Cansiglio beech woods: *C. cibarius* June-September (`fvg_campo2022_cansiglio`);
  - Carinthia and Slovenia: mostly *C. cibarius* s.str. (114 of 124 and 139 of 164 species-level
    iNaturalist records); in Carinthia the season ends in September above 1,400 m and runs to late
    October below 1,000 m (table above).
- **Press:** in 2016 "I gialletti da record, i porcini si fanno attendere", seen "un po' ovunque, a
  luglio e poi ancora ad agosto" (`fvg_ilpiccolo_2016_09_11`).

**Decisions.**
- **Season:**
  - the lowland window is full 15 June-31 October and closed by 10 December (the slow close keeps
    the Karst's October-November fruiting and the warm segregates, with no January tail);
  - the mountain window is full 1 July-30 September and closed by 31 October;
  - the handover moves up to 900-1,300 m;
  - the disabled two-flush rule closes with the lowland window.
- **Altitude:** full to 1,800 m, zero at 2,100 m, so open on all FVG woodland (the census has 20
  % of its records at 1,500-1,800 m).
- **Hosts:**
  - beech and fir/spruce rise to host (1.0);
  - deciduous oak to secondary (0.6), for the Karst pole;
  - larch and subalpine scrub drop to 0.1;
  - black pine stays marginal (0.3): the Karst pine's own chanterelle is *Craterellus lutescens*.
- **Soil pH and lithology stay disabled.** FVG woodland is the most acid so far (SoilGrids median
  5.56), so a pH rule would dock almost nothing, and the Karst pole sits on limestone red soils where
  SoilGrids is least reliable.

## Keys and groups dropped

None. Every key has FVG records in the census and a regional source.
- ***B. aereus*** is common on the Karst (census 230 points), rare elsewhere. Its band and host
  tiers keep it to the Karst and the hills; the porcini group takes the max over its keys, so it
  cannot lower the group in the mountains.
- **Ovoli** are rare but present on the Karst, in the hills and the Pordenone foothills.
- **Absent habitat keys.** `mediterranean_pine` and `macchia` are absent, and `evergreen_oak` is
  250 ha of Trieste coast. Their affinities are left as Tuscany's rather than invented.

## Weather rules: why none changed

- **No regional numbers.**
  - No FVG, Slovene or Carinthian study gives a rain amount, lag or temperature threshold for these
    taxa; the Slovenian Forestry Institute publishes no fruiting forecast.
  - The only field result is that Karst mycelium grew more in the year with a wetter spring
    (`mrak2025_mycorrhiza`), which is not a fruiting rule.
- **Qualitative statements, all compatible with the Tuscan rules** (research-agent notes, folklore;
  not encoded):
  - "Regnet es zwei bis drei Tage lang und wird es danach wieder warm, dann wachsen die Pilze ...
    binnen einer Woche" (ORF Kärnten, 2019);
  - downpours run off, "etwa drei bis vier Tage herunterregnen" is needed (Gailtal, 2026);
  - enough August rain for a September flush (Ljubljana society, 2024);
  - "la natura carsica dei suoli triestini favorisce un rapidissimo drenaggio della pioggia" (Funghi
    Magazine, 2021).

  The porcini rain trigger (full from 30 mm over 3 days, lag 10-16 growth days) and the gallinacci
  rain-frequency rule already reward steady rain over a single storm.
- **Rain climate:**
  - from 1,000 mm on the coast to over 3,300 mm on the Musi, one of Europe's rainiest places;
  - the porcini 30-day rain is scored against each cell's own normal, so it adapts;
  - the absolute 30-day ramps of ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full almost
    always in the Prealps and less often on the Karst in July, where ovoli and the Karst chanterelles
    fruit later anyway.
- **Bora and foehn.** The press blames drying winds on the Karst (the bora; a warm foehn in October
  2023). The ET0-based drying rules are the only stand-in; the known gap `drying_wind` (gusts plus
  low humidity) would suit the Karst better than any region so far.
- **Karst drainage.** Thin, fast-draining limestone soils make the same rain count for less on the
  Karst. The engine has no soil water model beyond reanalysis soil moisture, so this is left to the
  backtest.
- **Rain scale.** `precipitation_scale` was fitted on Tuscan gauges; a check against the ARPA FVG
  gauges is a region-config task (`regions/friuli_venezia_giulia.md`), not a species one.

## Slope and sun exposure

- **Slope, every key.** The band moves onto the region grid by the Tuscan rule: x1 up to about the
  woodland p90, x0.8 from about the maximum.
  - Woodland cells run p10 14.3°, median 27.0°, p75 32.3°, p90 36.2°, max 48.6°; 60 % are steeper
    than 25°.
  - So x1 to 36° and x0.8 from 48°, like Piemonte (34/45), Trentino-Alto Adige (35/45) and
    Lombardia (35/46).
  - The Tuscan band would have docked 59 % of the cells (mean x0.95); this one docks 11 % (mean
    x0.996).
- **Sun exposure, kept.** On 15 October the woodland sun ratio runs p10 72 %, median 101 %, p90 122 %
  (below 1,000 m p10 78 %, p90 120 %; Tuscany p10 89 %, p90 111 %).
  - The dry-side stoppers of *B. edulis* and *B. pinophilus* (x1 to 105 %) therefore dock about
    two fifths of the low woods.
  - The shade-side ones of *B. reticulatus* and *B. aereus* (x1 from 95 %) dock about a third of
    them, a tenth fully; that of ovoli (x1 from 100 %, only above 400-600 m) about half the cells it
    applies to, most of which the ovoli band already keeps out.
  - The bands are statements about sun and drying, not Tuscan percentiles, so they are kept.

## Press contrasts (`sanity.yaml`)

`friuli_venezia_giulia/sanity.yaml` holds 16 contrasts, written down on 2026-09-27 before the region
had any scores: 14 porcini, 1 gallinacci (`gallinacci_...`, read with `--group gallinacci`) and 1
ovoli (`ovoli_...`, `--group ovoli`).
- **Sources.** A research agent swept the Messaggero Veneto and Il Piccolo sitemaps for May-November
  2016-2025 (about 140 mushroom articles), the sitemaps of the Friulian local sites, and Funghi
  Magazine's bulletins. I checked every quote in the table against the page text, and re-opened the
  local main sources live.
- **Areas.** 12 areas, by ISTAT 2025 comuni (with the bilingual Karst names, which is how the grid
  carries them) or province sigle. Every name resolves on the region grid. Fogliano Redipuglia and
  Ronchi dei Legionari have no woodland cell and add nothing.
- **Normal:** 2017-2025.

| area | woodland cells | median elevation | main habitats |
|---|---|---|---|
| `carnia` (28 comuni) | 905 | 1,068 m | beech, fir/spruce, spruce-beech |
| `tarvisiano` (Tarvisio, Malborghetto Valbruna, Pontebba) | 356 | 1,178 m | spruce-beech, fir/spruce |
| `fvg_alps` (Carnia, Val Canale, Canal del Ferro, Resia: 36) | 1,606 | 1,073 m | beech, fir/spruce, spruce-beech, pine |
| `giulie` (Julian Alps and Prealps, Valli del Natisone: 15) | 772 | 916 m | spruce-beech, beech, hop-hornbeam, pine |
| `dolomiti_friulane_pn` (Val Cellina, Val Tramontina and foothills: 11) | 562 | 925 m | beech, black pine |
| `fvg_hills` (Colli Orientali, Collio, the Tagliamento and Pordenone hills: 19) | 139 | 249 m | chestnut, robinia, oak |
| `carso` (Trieste and Gorizia Karst: 12) | 180 | 215 m | downy oak and hop-hornbeam, black pine |
| `hills_and_carso`, `pordenone`, `trieste`, `region` | 319, 809, 135, 3,304 | 234, 864, 261, 874 m | |

**How far to trust them.**
- **Local papers rarely sum up a season.** Only 6 contrasts rest on local newspapers quoting named
  Friulian mycologists (Centro micologico friulano, Udine; AMB Bresadola Trieste).
- **Funghi Magazine carries the other 10.** Its weekly bulletins name Carnia, the Carnic and Julian
  Alps, the Dolomiti Friulane, the Karst and the provinces. It is one editor working from readers'
  reports and rain gauges, so several of these contrasts partly test the rain data. Only sentences
  describing fruiting that happened were used; forecasts were left out.
- **The Prealps and the hills are thin.** No local article describes a Val Cellina, Val Tramontina,
  Cansiglio-side, Val d'Arzino, Val Torre or Collio season.

| id | higher | lower | window | main source | second sources | caveats |
|---|---|---|---|---|---|---|
| `carnia_vs_hills_2017` | Carnia 2017 | hills 2017 | 08-25 → 09-30 | [Messaggero Veneto, 2017-10-31](https://www.messaggeroveneto.it/cronaca/funghi-annata-negativa-si-salva-solo-lautunno-q5qnwrip): "addirittura disastrose nella fascia collinare, per poi migliorare dalla fine di agosto, ma soltanto in Carnia" (Lucio Fassetta, Centro micologico friulano) | — | one expert; "fascia collinare" read as the FVG hills; part of the hill decline is long-term ("la progressiva scomparsa dei prati stabili") |
| `carnia_vs_tarvisiano_2017` | Carnia 2017 | Tarvisiano 2017 | 08-25 → 10-15 | same article, subtitle: "La Carnia meglio del Tarvisiano, in collina poche soddisfazioni" | body: "nelle altre zone le buone buttate sono state brevi e direi episodiche" | the ranking is the editor's subtitle; the body names Tarvisio only for fly agarics |
| `carso_2017_2016_autumn` | Karst 2017 | Karst 2016 | 09-21 → 10-12 | [Il Piccolo, 2017-10-12](https://www.ilpiccolo.it/cronaca/fvg-il-meteo-perfetto-regala-a-porcini-e-ovuli-un-autunno-da-record-p8k6lur7): "Da tre settimane il meteo è cambiato, regalando fioriture a dir poco eccezionali, un aumento dell'80% rispetto al 2016" (Massimo Tassin, AMB Bresadola Trieste) | [Il Piccolo, 2016-10-09](https://www.ilpiccolo.it/cronaca/mostra-micologica-dei-funghi-del-carso-r5gcxk87): the same group "in ansia causa il perdurare della siccità di inizio mese", fungi "Appena ora" starting | "+80 %" is one president's impression, framed region-wide |
| `alps_2016_late_summer` | Alps, normal | Alps 2016 | 06-20 → 08-31 | [Il Piccolo, 2016-09-11](https://www.ilpiccolo.it/cronaca/gialletti-da-record-e-zero-porcini-nellestate-anomala-dei-funghi-achmqfo8): "quest'anno siamo dovuti salire oltre i 1.500 metri per trovare i primi porcini"; "il Boletus Edulis è stato il grande assente di questa estate" (Udine mycologists) | — | the same was said of Austria and Slovenia; first porcini about 1 September near Paluzza |
| `alps_2020_2021_september` | Alps 2020 | Alps 2021 | 08-25 → 09-20 | [Funghi Magazine, 2021-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): "la stagnazione di piogge fredde ha bloccato ogni possibile nascita" (Carnia, north Friuli) | [FM 2020-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2020/) "nascite in crescendo con apice verso la fine del mese"; [FM 2020-09-21](https://funghimagazine.it/meteofunghi-21-09-2020/) "la buttata-non-stop si è un po' fermata"; [Il Friuli, 2021-11-14](https://www.ilfriuli.it/gusto/il-mistero-dei-porcini-scomparsi/): 2021 "una certa carenza" of porcini and galletti, 2020 "era stato molto buono" (Centro micologico friulano) | the local source blames drought and wind, FM cold rain; both agree on the outcome |
| `alps_2021_august_vs_september` | Alps, 8-20 Aug 2021 | Alps, 28 Aug-30 Sep 2021 | two windows | [FM, 2021-08-20](https://funghimagazine.it/aggiornamento-meteofunghi-porcini-20-08-2021/): "buone nascite di Porcini dai colli pedemontani alle Prealpi ed Alpi" | [FM 2021-08-12](https://funghimagazine.it/aggiornamento-meteofunghi-porcini-12-08-2021/) "Carnia, Alpi e Prealpi Giulie sono al momento in ottima forma"; [FM 2021-09-10](https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/) cold rain and wind "ha inibito le nascite così come accaduto nella vicina Carnia e sulle Alpi Giulie" | FM only; the Alpine gate is full across both windows, so it tests the weather rules |
| `alps_2023_2024_late_july` | Alps 2023 | Alps 2024 | 07-15 → 07-25 | [FM, 2023-07-20](https://funghimagazine.it/aggiornamento-funghi-20-07-2023/): "Ottime nascite ... fino alle Alpi Carniche e più ad Est su tutte le Giulie" | [FM, 2024-07-25](https://funghimagazine.it/aggiornamento-funghi-25-07-2024/): "non in Friuli Venezia Giulia dove sui monti è ancora primavera" | FM only; the 2023 flush started about 15 July (FM 2023-07-13 "relegate alle alte quote") |
| `alps_vs_hills_carso_october_2023` | Alps 2023 | hills + Karst 2023 | 09-28 → 10-12 | [FM, 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "le nascite sono del tutto cessate in collina, proseguono invece in alta quota sulle Alpi Carniche e Giulie ... A secco invece il Carso, arso e riarso dal caldo vento favonico" | [FM, 2023-10-27](https://funghimagazine.it/aggiornamento-porcini-27-10-2023/): "ottime in Friuli Venezia Giulia" | FM only; the regional gates favour the hills in October (the Alpine window is closing), so the weather rules must reverse it: a hard test |
| `carso_2023_2024_august` | Karst 2023 | Karst 2024 | 08-01 → 08-17 | [FM, 2023-08-17](https://funghimagazine.it/aggiornamento-funghi-17-08-2023/): "l'exploit del Carso e dei confini con la Slovenia dove si stanno trovando in contemporanea tutte 4 le specie di Porcini" | [FM, 2024-08-16](https://funghimagazine.it/aggiornamento-funghi-16-08-2024/): "sul Carso non sta nascendo nulla per siccità dovuta alla canicola" | FM only, but observational on both sides |
| `carso_2023_august_vs_autumn` | Karst, 1-17 Aug 2023 | Karst, 14 Sep-12 Oct 2023 | two windows | FM 2023-08-17 (above) | [FM 2023-09-06](https://funghimagazine.it/aggiornamento-porcini-06-09-2023/) "le nascite della buttata di Agosto sono già un lontano ricordo"; [FM 2023-09-20](https://funghimagazine.it/aggiornamento-porcini-20-09-2023/) Trieste "con assenza attuale di nascite"; FM 2023-10-12 "A secco invece il Carso" | FM only; both windows lie in the full lowland season |
| `region_2025_2024_early_august` | region 2025 | region 2024 | 07-20 → 08-10 | [FM, 2025-08-01](https://funghimagazine.it/aggiornamento-nascite-01-08-agosto-2025/): "Friuli V.G. : è boom totale, dal piano alla montagna" | [FM 2025-07-25](https://funghimagazine.it/aggiornamento-nascite-funghi-25-luglio-1-agosto-2025/) "buone nascite fungine ovunque, soprattutto di Porcini edulis"; FM 2024-07-25 and [2024-08-16](https://funghimagazine.it/aggiornamento-funghi-16-08-2024/) "timide nascite per eccesso di precipitazioni"; [friulioggi, 2025-09-24](https://www.friulioggi.it/cronaca/esposte-specie-incredibile-record-festa-funghi-budoia-24-settembre-2025/): "questa è stata una stagione particolarmente favorevole" (Gruppo micologico Sacilese) | FM says the 2025 peak had passed by 25 July; 2024's shortfall was from too much rain, which a rain rule reads as favourable (a real test) |
| `dolomiti_friulane_vs_giulie_july_2024` | Dolomiti Friulane (PN) 2024 | Julian Alps and Prealps 2024 | 07-01 → 07-11 | [FM, 2024-07-12](https://funghimagazine.it/aggiornamento-porcini-12-07-2024/): the Julian Alps and Prealps "le più bersagliate dai temporali ... nascite per lo più di soli Finferli. Porcini estivi e dove possibile anche Rossi e sporadici Edulis ... nel Parco Naturale delle Dolomiti Friulane e relative pedemontane" | — | FM only; storms (too much rain) again |
| `pordenone_vs_trieste_september_2023` | province of Pordenone 2023 | province of Trieste 2023 | 09-13 → 09-20 | [FM, 2023-09-20](https://funghimagazine.it/aggiornamento-porcini-20-09-2023/): Pordenone among "le province con ottime nascite in corso, pur senza" delirio; Trieste among "le province con assenza attuale di nascite" | — | a national province list, no local voice; consistent with the Karst contrast above |
| `hills_2023_2017_early_august` | hills 2023 | hills 2017 | 07-25 → 08-10 | [FM, 2023-08-10](https://funghimagazine.it/aggiornamento-funghi-10-08-2023/): "non solo ottime ma persino massicce, incluse le zone pianeggianti e collinari attorno a Pordenone, Udine, Gorizia e, persino attorno a Trieste" | Messaggero Veneto 2017-10-31 (above) | mixed sources; the 2023 hill porcini were mostly *B. reticulatus* and *B. aereus* |
| `gallinacci_alps_2016_2021` | Alps 2016 | Alps 2021 | 07-01 → 08-31 | Il Piccolo 2016-09-11: "I gialletti da record, i porcini si fanno attendere"; "Li si è visti un po' ovunque, a luglio e poi ancora ad agosto" | Il Friuli 2021-11-14: the shortage touched "la famiglia dei boleti (porcini) e dei cantarelli (galletti)" | the 2021 side is a whole-season verdict with no window |
| `ovoli_carso_2017_2016` | Karst 2017 | Karst 2016 | 09-21 → 10-12 | Il Piccolo 2017-10-12: ovoli up 80 % on 2016, "tantissimi porcini e ovuli" | Il Piccolo 2016-09-11: "Ovuli e mazze di tamburo tra i grandi assenti"; Il Piccolo 2016-10-09 (drought into early October) | 2016's ovolo absence is partly a decade-long decline |

**Left out:**
- **Il Gazzettino** (Udine and Pordenone editions), probably the richest outlet for Carnia and the
  Pordenone Prealps: its robots.txt disallows AI agents. The agent had opened two of its pages before
  noticing, and nothing from them is used. A Carnia 2020 against 2016 summer contrast rested on one of
  them. A person could read it: "Funghi, è una stagione da record: finferli al top", 2020-08-27.
- **Also blocked:** Rai TGR FVG (its terms forbid AI use) and the Citynews sites UdineToday,
  PordenoneToday and TriestePrima (robots.txt). Novi Matajur, the Slovene weekly of the Natisone
  valleys, answered 403.
- **Paywalled or thin:** the Messaggero Veneto and Il Piccolo are paywalled from 2022, and their
  2022, 2023 and 2025 sitemaps are incomplete.
- **Single big finds**, used only as colour: Lauco 2016, Forni di Sopra 2018 ("Il 2018 passerà alla
  storia in Carnia come un anno da ricordare"), Alta Carnia, Zoncolan and Zuglio 2019, Matajur 2022.
- **Forecasts and rain reasoning:**
  - Funghi Magazine's province rankings and October-November 2022 forecasts;
  - the Karst early-season hints of 2024 (sporadic);
  - Carnia against the border hills in September 2021 (half forecast);
  - the region 2023 against 2022 pair (2022 side rain reasoning).
- **Weak or out of range:**
  - Coldiretti's national releases;
  - the Budoia festival species counts (effort-driven);
  - the Slovene Goriška exhibitions of 2021 (poor), 2022 ("Letos je leto jurčkov") and 2024
    (average): cross-border, and 2022 conflicts with Funghi Magazine's Triveneto reading.
- **Permits:** no per-year permit counts are published. The Region's 2026 fee transfers imply at
  least about 3,400 region-wide permits paid in 2025.

**Year picture from the press** (context, not scored):

| year | Alps (Carnia, Tarvisiano, Julian Alps) | Prealps | hills | Karst |
|---|---|---|---|---|
| 2016 | a month late; no porcini below 1,500 m in summer, first ones about 1 Sept at Paluzza; record gialletti July-August | — | ovoli rare in the Cividalese | drought into early October; fungi starting about 8 Oct |
| 2017 | poor to late August, then good "soltanto in Carnia"; October good | "brevi e ... episodiche" flushes | "addirittura disastrose" | late Sept-mid Oct boom, porcini and ovoli +80 % on 2016 |
| 2018 | cold rain to July; "un anno da ricordare" in Carnia (late summer) | — | — | — |
| 2019 | poor early August, strong 18 Aug-5 Sept; restart about 20 Sept; a porcino at Zuglio on 12 Nov | — | — | — |
| 2020 | good from late July, rising to the end of August; eased about 20 Sept; "molto buono" | Dolomiti Friulane good late July | lesser in the low hills (mid-Aug) | lesser (mid-Aug) |
| 2021 | a mid-August flush, then cold rain, wind and drought: a shortage of porcini and galletti | Valli del Natisone: "pochi funghi" | some porcini in the east Friulian hills late Oct | early-August ovoli and porcini neri, dry by Ferragosto |
| 2022 | drought; dry late July, "sfavorite" mid-August; porcini "quasi assenti" late October | — | discrete early November on the Gorizia hills | discrete early November |
| 2023 | stopped by rain early July; flush from 15 July, abundant late July-mid Aug; nothing early Sept; still "ottime" in the interior Alps mid-October | Pordenone "ottime" mid-Sept | "massicce" early August; over by late August; ceased by October | all four porcini in early August; dry mid-Sept to mid-Oct (foehn) |
| 2024 | "ancora primavera" late July; timid mid-August (too much rain); few porcini in September | Dolomiti Friulane porcini, Julian Prealps only finferli (early July) | — | sporadic early porcini (late May-June); nothing mid-August (35 °C) |
| 2025 | Tarvisio over by early July, western Carnia good 10 July; "boom totale, dal piano alla montagna" 1 Aug | "stagione particolarmente favorevole" (Budoia) | ovoli "più del solito" on the wine hills | nothing yet about 21 Aug |

2023 was a good summer in the mountains and on the Karst in August. 2021 was the worst late summer
of the decade in FVG, as in Piemonte and Lombardia. 2024 failed from too much rain in the Julian
Alps and from heat on the Karst.

## Open questions

- **Black pine.**
  - `mountain_pine` is 15 % of FVG's woods and three quarters black pine.
  - The rules make it marginal for *B. edulis* (0.3) on Karst evidence, but nothing tells us about
    the native dolomite pinewoods of the Prealps, and 0.3 still gives a pure pine cell full credit.
  - The Dolomiti Friulane contrast (much black pine) and the backtest are the first checks; 0.1 is
    the next step for *B. edulis* if Prealpine pine cells score high.
- **The Karst's drainage and wind.** Thin limestone soil, the bora and a warm foehn dry the Karst
  faster than the rain rules assume. Two Karst contrasts (2023 August against September, 2024
  August) and the October 2023 Alps-against-Karst one test it. The known gap `drying_wind` would
  suit the Karst best.
- **Undated census.** The census's FVG map points show where each taxon grows, but the months come
  from north-east-wide charts. The Federazione dei Gruppi Micologici del FVG (Gemona) keeps the
  underlying records. Dated FVG records from it would be the first real FVG validation set: a lead
  worth asking for.
- **The Julian Alps' late season.** Slovene records at 1,200-1,450 m reach late October, Carinthian
  ones stop in early October (partly the picking law). The Alpine windows close by 25 October; the
  sanity contrasts for October 2023 are the check.
- **Larch.** 0.1 here, as in Trentino-Alto Adige and Lombardia (Piemonte kept 0.3). FVG's larch is
  2 % of the woods and sits at the tree line, so the choice barely matters here.
- **Leads not read:**
  - the printed *Glive Slovenije* (Jurc, Piltaver, Ogris 2005), whose records carry month and
    quadrant;
  - the Austrian fungi database (its terms forbid passing data on without permission);
  - the current Carinthian Pilzverordnung annex (the Austrian legal database showed a bot check);
  - the Gruppo Micologico Sacilese booklets;
  - Il Gazzettino (see Left out).

## References added for Friuli-Venezia Giulia

| id | kind | verified | used for |
|---|---|---|---|
| `mushma_fvg_occurrence_check_2026` | analysis | verified | FVG, Carinthian and Slovene record months and elevations; census recount |
| `mushma_fvg_forest_check_2026` | analysis | verified | habitat contents and elevations, slope and sun ratios, gate effects |
| `fvg_omg_observations` | dataset | verified | Carinthian dated records with elevations |
| `fvg_bi_maps` | dataset | verified | Slovene distribution of *B. aereus* and ovoli |
| `fvg_lr25_2017` | institutional | verified | picking law: ovolo rule, no calendar |
| `fvg_del_favero2016` | institutional | verified | forest regions, black pine, chestnut, belts, larch |
| `fvg_infc2015_categorie` | institutional | verified | forest area and categories |
| `fvg_arpa_clima2023` | institutional | verified | rain belts and regime, lapse rate, bora |
| `fvg_arpa_schede_rr2023` | institutional | verified | rain by zone, Karst regime |
| `fvg_arpa_impatti_cc2018` | institutional | verified | 2012 Karst dieback; black pine planted in the 1800s |
| `fvg_arpa_report2022` | institutional | verified | the 2022 drought |
| `fvg_tarvisio_foresta` | institutional | verified | Tarvisio forest composition and tree line |
| `fvg_si_uredba_gliv2011` | institutional | verified | ovolo protected in Slovenia |
| `fvg_rafvg_funghi2005` | institutional | verified | regional common names (galletto, finferle) |
| `fvg_ktn_pilzschutz` | society | verified | Carinthia's 15 June-30 September picking window |
| `fvg_cebulec_pertot1985` | society | verified (scan) | Karst survey: no *B. edulis*, black pine's fungi |
| `fvg_cebulec_pertot1992` | society | verified (scan) | Karst fruiting in October-November; plantations |
| `fvg_campo2022_cansiglio` | society | verified | Cansiglio beech: *B. edulis*, *C. cibarius* months |
| `fvg_ambf_caesarea` | society | verified | ovolo hosts and rarity in Friuli |
| `fvg_muse_censimento_aestivalis` | society | verified | *B. reticulatus* FVG points, months, altitude |
| `fvg_muse_censimento_caesarea` | society | verified | ovolo FVG points, months, altitude |
| `fvg_muse_censimento_ferruginascens` | society | verified | warm Karst chanterelle, October-December |
| `fvg_sperdin1975_roehrlinge` | society | verified (agent, browser) | *B. pinophilus* with pine in Carinthia |
| `fvg_sperdin1983_amanita` | society | verified (agent, browser) | no ovoli in Carinthia; Trieste and Ljubljana |
| `fvg_friebes2017_ferlach` | society | verified (agent, browser) | Karawanken *B. edulis*, *C. cibarius* hosts |
| `fvg_gobe_si` | society | verified | Slovene hosts and months of the six taxa |
| `fvg_ilpiccolo_2016_09_11` | web | verified | season timing lore; porcino nero rare; ovolo decline |
| `fvg_ilpiccolo_2017_10_12` | web | verified | Karst autumn 2017 porcini and ovoli |
| `fvg_messaggeroveneto_2019_11_13` | web | verified | November porcino in lower Carnia |

Existing references the changes lean on, opened again for this card:
- `muse_censimento_edulis`, `muse_censimento_boletus`, `muse_censimento_pinophilus`,
  `muse_censimento_cibarius`, `muse_censimento_alborufescens` (census pages and charts);
- `mrak2025_mycorrhiza` (Slovene Karst mycelium);
- `funghimagazine_carpino_nero2026` (hop-hornbeam hosts);
- `funghimagazine_alberi_porcini` (larch);
- `funghimagazine_ovolo` (north-eastern ovolo limit).
