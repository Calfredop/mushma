# Species ecology: Molise (regional appendix to species-ecology.md)

Research date: 2026-09-30 (dates Europe/Rome, units metric). Card: `region-molise-species.md` (child
of `region-molise.md`). Rule files: `api/src/api/config/species/molise/`. This appendix records how
the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Molise, what changed and
why. It covers **fruiting conditions only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(15 added for Molise, in one block at the end of the file, listed at the end of this page; the
neighbours' sources are reused under their own keys). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every number is
a prior for the backtest; season windows, altitude bands and habitat affinities stay frozen
(`model.yaml`, `backtest.frozen_factor_kinds`).

Molise sits between Abruzzo (north), Lazio (west), Campania (south) and Puglia (east), and all four are
merged in this checkout. The section [Where Molise follows its neighbours and where it
departs](#where-molise-follows-its-neighbours-and-where-it-departs) takes the card's three questions:
the Turkey-oak hills, the Alto Molise's late cold springs and the dry Basso Molise.

## Summary

1. **All three groups and all six keys are kept, on the thinnest regional evidence of any region so
   far.** The national checklist had 95 fungi on record for Molise, the fewest of any region, and
   calls Molise and Valle d'Aosta "the less investigated Regions" (`vda_onofri2003_checklist`), and
   iNaturalist holds 4 records of the six keys among 400 Molise fungi records: one *B. edulis*, one *B.
   reticulatus*, two *C. cibarius* (`mushma_occurrence_check_molise_2026`). The regional law sets
   minimum sizes for "Boletus edulis (Porcino) e relativo gruppo" and "Cantharellus cibarius
   (Gallinaccio)" and bans the closed ovolo (`lr_molise_4_2008`, art. 7.5). Funghi Magazine's national
   bulletins name Molise often: "Nel Molise collinare abbondano gli Aereus ed breve arriveranno anche
   gli Ovoli. In quello montano invece abbondano maggiormente Galletti ed Estatini" (September 2019,
   `funghimagazine_molise_2019_09_12`); "Porcini neri e Ovoli reali spuntati in Puglia, Molise e Sicilia
   interna" (August 2025, `funghimagazine_nascite_2025_08_22`). *B. pinophilus* has no Molise record or source of its own; it
   stays, as in Lazio, Umbria and the Marche, because the law regulates the whole porcini group, the
   Campania checklist has it on the shared Matese, and its hosts (16,600 ha of beech, the Alto Molise
   silver fir) are here.
2. **Molise is a Turkey-oak region with beech on top.** On ISPRA's Carta della Natura, which the grid
   reads, deciduous oak is 67 % of the woodland cells' wooded area (Turkey oak about 62 % of it, downy
   oak the rest), beech 13 %, hop-hornbeam and other mixed broadleaf 7 %, and chestnut only 0.3 %
   ("nella regione Molise raramente si riscontrano terreni adatti", `regione_molise_ctf2009`). The
   woodland is lower than Abruzzo's: grid median 728 m against 1,061 m, max 1,781 m.
3. **Five altitude bands move up, as in the neighbours.** The Molise beech runs from about 800-1,000 m
   to the tree line (map median 1,249 m, p90 1,540 m, max 1,916 m; `ispra348_2021_cnat_molise`,
   `mushma_molise_forest_composition_2026`):
   - *B. edulis* and *B. pinophilus*: full to 1,800 m, 0 at 2,000 m (Tuscany 1,600 → 1,900).
   - *B. reticulatus*: full to 1,600 m, 0 at 1,900 m (Tuscany 1,100 → 1,500), Campania's band. The one
     Molise record is in pure beech at Campitello Matese in August 2025, in a cell at 1,595 m, where
     the Tuscan band is 0.
   - Gallinacci: full to 1,400 m, 0 at 1,900 m (Tuscany 1,000 → 1,700).
   - The ovolo: full to 900 m, 0 at 1,200 m (Tuscany 750 → 1,100), because its Turkey-oak hosts climb
     higher here (p90 1,046 m for the closed Turkey-oak woods).
   - *B. aereus* keeps Tuscany's band.
4. **Three season windows move.**
   - The gallinacci mountain window opens a fortnight earlier (15 May → 15 June, Tuscany 1 June → 1
     July), as in Abruzzo and Campania; the two Molise records are in June and early July, and the
     Molise bulletins have chanterelles "In Appennino" by 1 June 2024 and in Molise in early June 2023.
   - The ovolo reaches full season on 1 August (Tuscany 1 September), as in Abruzzo: a Molise blog has
     it "dal mese di luglio", and the bulletins report ovoli in Molise in mid-August 2025.
   - *B. aereus*'s summer/autumn handover moves from 400-600 m to 600-800 m, as in Campania and Puglia,
     so the Molise oak hills (median 654 m) keep the black porcini the bulletins report there in
     September 2019 and mid-October 2022.
5. **What the habitat classes hold changes 13 affinities.** Molise's `mixed_broadleaf` is hop-hornbeam,
   old-field regrowth and ash-maple-hornbeam woods; `mountain_pine` is the planted conifers of the
   42.G_n class, Aleppo pine and cypress below about 700 m and black pine above; and
   `transitional_woodland_shrub` is thorn, Spartium, broom and juniper scrub. These move down, as in
   Abruzzo, Campania and Lazio. Deciduous oak becomes a secondary host of the chanterelles.
6. **Weather rules are all Tuscany's.** No Molise study ties fruiting to rain or temperature in
   numbers. The Alto Molise's cold springs and the Basso Molise's dry summers are left to the weather
   rules, which read each cell's own weather.
7. **Evidence.** Of the 15 new sources (all opened): 3 institutional (the picking law, the Region's
   forest-type map report, ISPRA's Carta della Natura report), 1 national dataset (INFC 2015), 9 web
   pages (folklore: 4 Funghi Magazine bulletins with Molise lines, 3 posts of a Molise forager blog, a
   generic forager page, an isNews feature), 2 our own analyses. No Molise study, society publication or
   record set exists to lean on. Most decisions rest on the Molise forest maps, the bulletins and the
   neighbours' evidence, reused and re-opened: the Campania Laceno pages and checklist, the Campania
   Matese society, the Abruzzo Laga blog, Funghi Magazine's calendars.

## Molise in brief

**Woods.** The grid reads ISPRA's Carta della Natura del Molise (1:25,000, 2021, drawn on the 2018
orthophotos; `ispra348_2021_cnat_molise`), with the class mapping in `config/regions/molise.yaml`
(`regions/molise.md`). The Region's own forest-type map (DGR 252/2009, `regione_molise_ctf2009`) is
published only as a PDF; its report gives the types, belts and places that say what each habitat key
holds. Areas and elevations below come from the habitat map itself, sampled on a 100 m lattice with
Copernicus GLO-30 heights (`mushma_molise_forest_composition_2026`). The map holds 181,300 ha under a
habitat key, 159,400 ha of it broadleaf or conifer wood; INFC 2015 gives a bosco of 153,248 ha
(`infc2015_molise`).

This table is **which habitat holds which Molise tree**:

| habitat key | share of the map's wood | Molise trees (Carta della Natura code, area) | elevation p10 / median / p90 (max) |
|---|---|---|---|
| `deciduous_oak` | 70.8 % | Turkey oak: temperate 41.741 (49,129 ha), Mediterranean 41.7511 (20,135), with Hungarian oak 41.7512 (1,195); downy oak: Mediterranean 41.732 (21,700), temperate 41.731 (20,620) | 378 / 654 / 955 m (1,399); 41.741 546 / 795 / 1,046 m |
| `beech` | 10.4 % | southern Apennine beech 41.18 (16,569 ha): Matese, Mainarde, Alto Molise | 1,035 / 1,249 / 1,540 m (1,916) |
| `mixed_broadleaf` | 7.5 % | hop-hornbeam 41.81 (5,275 ha); synanthropic woods on abandoned fields, orchards and pastures 4D_n (3,458: cherry, chestnut, walnut, hazel, maples, ash, some robinia); ash, maple and hornbeam 41.88_m (2,599); field elm 41.F1 (607); aspen, ravine woods | 404 / 725 / 1,028 m |
| `riparian` | 5.5 % | poplar 44.61 (8,221 ha), willow, narrow-leaved ash | 73 / 397 / 760 m |
| `mountain_pine` | 3.2 % | conifers planted outside their range 42.G_n (5,101 ha): Aleppo pine, cypress and other Mediterranean pines below about 700 m (round the Guardialfiera and Occhito reservoirs), black pine above, with some fir, cedar and Douglas fir; conifer plantations 83.31 (36) | 218 / 739 / 1,166 m |
| `evergreen_oak` | 1.2 % | supramediterranean holm oak 45.32 (1,510 ha: Monteroduni 1,020, Sant'Agapito, Colli a Volturno, Isernia); thermo-mesomediterranean 45.31 (327: Mafalda) | 188 / 470 / 701 m |
| `exotic_broadleaf` | 0.8 % | robinia and ailanthus 41.L_n (1,130 ha), exotic riparian 44.D2_n | 205 / 602 / 779 m |
| `chestnut` | 0.2 % | chestnut 41.9 (396 ha: San Massimo 196, Bojano 84, Campochiaro 61, Roccamandolfi, San Polo Matese) | 631 / 739 / 949 m |
| `fir_spruce` | 0.2 % | silver fir 42.15 (397 ha: Pescopennataro 309, the Abeti Soprani; Agnone 59; Sant'Angelo del Pesco, Pietrabbondante, Belmonte del Sannio) | 1,017 / 1,270 / 1,366 m |
| `mediterranean_pine` | 0.1 % | wooded dunes 16.29 (127 ha: Petacciato, Campomarino) | 3 / 7 / 12 m |
| `transitional_woodland_shrub` | (21,155 ha, outside the wood) | deciduous thorn scrub of rich soils 31.81 (9,083), Spartium 32.A (8,247), hill juniper 31.88 (1,460), broom 31.844 (1,309), bramble, riparian willow scrub | 355 / 715 / 1,084 m |
| `macchia` | (800 ha, outside the wood) | Mediterranean macchia 32.3 (708), dune juniper and sclerophyll dunes | 29 / 231 / 409 m |

There is no mixed broadleaf-conifer class and no "other conifer" class, so `mixed_broadleaf_conifer`
and `other_conifer` are empty in Molise. The mixed Turkey oak-silver fir and beech-silver fir stands of
the Alto Molise (660 and 90 ha on the regional map, `regione_molise_ctf2009`) fall into the oak and
beech polygons.

**The grid as built on 2026-09-30** (`regions/molise.md`, Woodland grid): 4,703 cells, **1,455
woodland cells**, forest 159,234 ha (+3.9 % against INFC 2015). Woodland cell elevation p10 433 m,
median 728 m, p90 1,146 m, max 1,781 m; 106 cells below 400 m, 439 at 600-800 m, 173 at 1,000-1,200
m, 93 at 1,200-1,500 m, 23 above 1,500 m, 7 above 1,600 m. The wooded area of those cells is deciduous
oak 67.3 %, beech 12.8 %, mixed broadleaf 7.4 %, transitional scrub 5.8 %, mountain pine 2.2 %,
riparian 2.1 %, evergreen oak 1.4 %, chestnut and fir 0.3 % each. Deciduous oak dominates 1,123
cells, beech 182 (median 1,242 m; Roccamandolfi 24, Campochiaro 18, Vastogirardi 15, Guardiaregia 13,
Capracotta and Pizzone 11), mixed broadleaf 98. Isernia holds 924 woodland cells (median 788 m),
Campobasso 531 (median 640 m); the coast and the Basso Molise plains hold almost none. Slope median
14.8° (p90 21.9°, 4.3 % above 25°), gentler than Tuscany's. Topsoil pH median 6.81 (p5 6.19, p95
7.32).

INFC 2015 (`infc2015_molise`) has the same picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| Turkey oak, Hungarian oak and other Mediterranean oaks | 51,975 | 33.9 % |
| downy, sessile and pedunculate oak | 48,198 | 31.5 % |
| beech | 14,839 | 9.7 % |
| other deciduous | 10,225 | 6.7 % |
| hygrophilous | 9,054 | 5.9 % |
| hop-hornbeam and hornbeam | 8,982 | 5.9 % |
| black and laricio pine | 2,343 | 1.5 % |
| Mediterranean pines | 2,184 | 1.4 % |
| silver fir | 1,172 (ES 57.5 %) | 0.8 % |
| holm oak | 1,172 | 0.8 % |
| chestnut | 391 (ES 99.8 %) | 0.3 % |

**Altitude belts** (`regione_molise_ctf2009`; `ispra348_2021_cnat_molise`):

| type | belt and where |
|---|---|
| beech, submontane (Faggeta submontana) | "tra gli 800 e i 1200 metri", with Turkey oak, maples and ash, "soprattutto sul massiccio del Matese e nella Comunità Montana dell'Alto Molise" (3,100 ha) |
| beech, montane (Faggeta montana) | "da 1000 a 1500 metri", pure beech, "lungo le catene montuose principali" (10,500 ha, 55 % high forest) |
| beech at the tree line (Faggeta altomontana) | "tra gli 800 e il limite superiore della vegetazione", sparse and shrubby on warm, rocky limestone slopes (1,200 ha); ISPRA: the southern beech "da quote massime attorno ai 1900 metri" down to about 700 m |
| silver fir (Abetina pura autoctona) | "a quote comprese tra gli 800 m ed i 1400 m", on the Alto Molise flysch: the Abeti Soprani south of Pescopennataro on Monte Campo, Bosco Canale, Montecastellare, Collemeluccio (343 ha) |
| Turkey oak | Cerreta mesoxerofila across the region except the Basso Molise and the upper Matese and Mainarde (31,094 ha); Cerreta mesofila in the north of the province of Isernia, the northern Mainarde, the eastern Matese and central Campobasso, "scende anche a quote relativamente basse" (29,336 ha); together "quasi il 40%" of the woods |
| downy oak | thermophilous "tra il livello del mare e gli 800 metri"; mesoxerophilous 27,672 ha, everywhere but the north-west of the Agnone area, mixing with Turkey oak higher up |
| hop-hornbeam | 400-800 m (secondary), 500-1,200 m (mesoxerophilous), 800-1,200 m (primitive, Matese), 500 to over 1,000 m (mesophilous, Matese) |
| chestnut | under 360 ha, "soprattutto nella zona sud occidentale della provincia di Campobasso" (the Matese foot) |
| conifer reforestation | basal: Aleppo pine with maritime and stone pine and cypress, "non si spingono altre i 700 metri", round the Occhito and Guardialfiera reservoirs (1,800 ha); submontane: 650-1,000 m, "per la maggior parte con pino nero", Aleppo pine too in the province of Campobasso, silver fir in the north of Isernia (2,434 ha); montane: black pine "nell'ambito della vegetazione delle faggete" (650 ha) |

**Substrate and climate** (`regione_molise_ctf2009`). The Matese and the Mainarde are limestone and
dolomite; the Alto Molise is sandstone and marl flysch (where the silver fir grows); the Frosolone,
Isernia, Venafro and Sepino hills are calcareous-marly; the centre and the Basso Molise are clay and
flysch, with badlands (calanchi) and Vertisols. The coast is Mediterranean, 14-16 °C, with "tre mesi
estivi con presenza di aridità" and a November rain maximum. Inland it is temperate: the upper Biferno
and Tappino hills 858 mm with "piogge estive abbondanti"; Guardiaregia and Roccamandolfi on the
Matese "precipitazioni annue molto abbondanti anche nel periodo estivo, tali da far sì che non ci
siano problemi di siccità"; Capracotta about 1,000 mm, "piogge estive abbondanti", two winter months
below 0 °C; Monte La Meta hyper-humid and cold even in summer. SoilGrids topsoil pH on the woodland
grid is 6.19-7.32 (5th-95th percentile).

**Regional law.** L.R. 19 febbraio 2008, n. 4, "Nuova disciplina in materia di raccolta e
commercializzazione dei funghi epigei" (BUR Molise n. 5 of 1 March 2008), as amended by L.R. 17/2010,
8/2016, 1/2017, 25/2017, 1/2018, 1/2020 and art. 12 of L.R. 7/2026 (the Consiglio regionale's text,
`lr_molise_4_2008`). It repealed L.R. 11/2000 and its amendments (40/2000, 20/2004, 35/2005).
- **Permit.** A regional card, valid across the region, after a course and an exam for residents;
  non-residents use their own region's permit; a yearly fee (art. 2-4).
- **Hours.** Picking "è consentita dall'alba al tramonto" (art. 5.1.a); no closed days.
- **Quantity.** "tre chilogrammi più un carpoforo" per person per day (art. 6.1).
- **Size.** Banned "per ragioni di carattere ecologico e sanitario": "Boletus edulis (Porcino) e
  relativo gruppo con diametro del cappello inferiore a cm. 3", "Cantharellus cibarius (Gallinaccio) con
  diametro del cappello inferiore a cm. 2", "Amanita caesarea allo stato di ovolo chiuso" (art. 7.5).
- **Places.** Banned in integral reserves; in national parks, nature reserves and regional parks unless
  their bodies allow it (so in the Molise side of the Parco Nazionale d'Abruzzo, Lazio e Molise and the
  Collemeluccio-Montedimezzo reserves); "nelle aree oggetto di rimboschimento e fino a quindici anni
  dall'impianto"; within 20 m of public roads (art. 7.3-7.4).
- **Temporary limits.** The Region "può disporre limitazioni, divieti temporanei, o interdizione alla
  raccolta di una o più specie" (art. 7.6).
- **What it leaves out.** No season calendar, closed days or altitude rule. None of it changes where
  or when the fungi fruit; it confirms the porcini group, the chanterelle and the ovolo as regional
  species.

## Where Molise follows its neighbours and where it departs

Every Molise decision below follows at least one neighbour; none rests on a Molise study, because none
exists. The card asked about three departures.

1. **The Turkey-oak hills: the rules are already built for them.** Turkey and downy oak are two thirds
   of the woods, more than in any neighbour (about 29 % in Abruzzo, 31-34 % in Campania, 41 % in
   Lazio, 51 % in Puglia). Deciduous oak is already a full host of *B. reticulatus*, *B. aereus* and the ovolo in
   Tuscany's rules, and a marginal one of *B. edulis* and *B. pinophilus* that still gives a pure oak
   cell full credit (the habitat response saturates at a host-weighted share of 0.3). What changes is:
   - the chanterelles, for which deciduous oak goes from 0.3 to 0.6, as in the Marche, Abruzzo,
     Campania and Lazio (one of the two Molise records is in a Turkey-oak cell);
   - the ovolo band, which now covers the Turkey oak up to 900 m in full and fades to 1,200 m, as in
     Abruzzo and Lazio, because the closed Turkey-oak woods here sit at a median 795 m.
   No Molise source compares porcini or ovoli yields in Turkey oak and downy oak; both stay in one
   class.
2. **The Alto Molise's late cold springs: left to the weather rules.** The Alto Molise (Capracotta,
   Agnone, Vastogirardi, San Pietro Avellana, Pescopennataro) is the coldest part of the region, with
   two winter months below 0 °C and snow, but also "piogge estive abbondanti" (`regione_molise_ctf2009`).
   The season windows are the same as on the Laga (Abruzzo) and the Campania Matese; a late spring
   shows up in the growth clock, the air- and soil-temperature bands and the cold-night and frost rules,
   which read each cell's own weather. No Molise source dates a late start in the Alto Molise; the press
   contrasts (below) are where it would show. The gallinacci mountain window opening on 15 May is the
   one change in this direction, and it follows the neighbours, not the Alto Molise.
3. **The dry Basso Molise: little woodland to score.** The coastal and low Campobasso hills have "tre
   mesi estivi con presenza di aridità" (`regione_molise_ctf2009`), but almost no woodland cells: 19
   comuni of the coast and the Basso Molise (Termoli, Campomarino, Petacciato, Montenero di Bisaccia,
   Guglionesi, San Martino in Pensilis, Larino, Ururi, Rotello, Santa Croce di Magliano and others) hold
   6 woodland cells between them, and only 106 of the 1,455 woodland cells are below 400 m. The porcini 30-day rain is scored against each cell's own normal, so
   it adapts; the absolute 30-day ramps of ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full
   less often in a dry July, which is what the lore expects. The *B. aereus* handover moves up so the
   hill oak keeps its autumn window; its end is not extended as in Campania (see the porcini section).

The one departure from a neighbour is **the summer porcino band**: it follows Campania (full to 1,600
m), not Abruzzo (1,500 m) or Lazio (1,400 m), because the one Molise record sits at 1,595 m in the
Matese beech.

## Occurrence cross-check (Molise)

Queried 2026-09-30 (`mushma_occurrence_check_molise_2026`): iNaturalist place 10871 (verifiable
records), GBIF `gadmGid=ITA.12_1`, elevations from the Copernicus GLO-30 DEM for open records accurate
to 1 km, and the comune and habitats of the record's cell on the grid of 2026-09-30. Aggregates only;
no coordinates are stored.

Molise has **400** verifiable iNaturalist fungi records (Abruzzo 2,792, Campania 4,437), 186 of them
from 2024-2025; October holds 23 % of them, November 13 %, July 12 %, August 11 %. GBIF has 763 fungi
records in Molise; for the six keys it adds only copies of iNaturalist records.

| taxon | records | when | where (cell) |
|---|---|---|---|
| *B. edulis* | 1 | 27 June 2009 | about 890 m, Sant'Angelo del Pesco (Alto Molise), a cell of 65 % scrub outside the woodland mask |
| *B. reticulatus* | 1 | 10 August 2025 | Campitello Matese (San Massimo), a pure beech cell at 1,595 m |
| *B. aereus* | 0 | | |
| *B. pinophilus* | 0 | | |
| *A. caesarea* | 0 | | |
| *Cantharellus* | 2 (*C. cibarius*) | 2 July 2009; 6 June 2023 | the same Sant'Angelo del Pesco cell (2009, same place as the *B. edulis*); a Turkey-oak woodland cell at 690 m, Busso (2023) |

Four records tune nothing. They say that the summer porcino reaches the high Matese beech in August
(where the Tuscan band is 0), and that chanterelles fruit in June and early July at 690-890 m. The
sightings backtest will have one or two Molise presences, so the priors ship.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **All four are named for Molise, none studied there** (folklore to plausible). A generic forager page
  says "In generale, è possibile raccoglierli da maggio fino alla fine di ottobre", with four porcini:
  the estatino "ai margini dei boschi di querce nelle zone esposte a sud", "già a maggio" where sunny,
  usually "fino ad agosto"; the black porcino "da metà estate (luglio) all'inizio dell'autunno (fine
  settembre)"; a mountain "porcino rosso" "da settembre ai primi giorni di novembre"; *B. edulis* when
  the temperature falls, low down "verso la fine di settembre fino alla fine di ottobre"
  (`cacciatoridifunghi_molise2023`, folklore; it names no place or tree beyond oaks). A Molise forager
  blog had "il re dei funghi: il Boletus edulis" being picked in the Molise woods in early September
  2025, "Dopo un lungo periodi di siccità" (`blog_tartufi_funghi_molise2025`, folklore). The law names
  the porcini group (`lr_molise_4_2008`).
- **The Centre-South calendar** (`funghimagazine_calendario_primavera_estate`, folklore). The estatini
  appear "già ad Aprile" in the hill woods of the Centre-South, "Entro fine Maggio" in the chestnut and
  then the beech, and in June "si concentrano soprattutto nei boschi di Faggio di medio-alta
  montagna"; in July the black porcini take over in the oak ("Nei boschi di Quercia collinari al posto
  dei Boletus reticulatus ecco arrivare i Porcini Neri"), and there are "primi ed assai sporadici
  ritrovamenti di Edulis sugli alti monti di confine tra Abruzzo-Lazio-Molise"; *B. aereus* reaches
  beech "Solo ad estate inoltrata ... quasi esclusivamente al Sud"; *B. pinophilus* is "piuttosto rari
  al Centro-Sud Italia", "più sporadici ancora" on the mountains between "Abruzzo-Molise-Campania".
- **The neighbours on the same massifs** (folklore). On the Campania Picentini the summer porcino
  "predilige il bosco di faggio" from 1,100 m "fino ai 1600-1700 m" (`laceno_boletus_aestivalis`); the
  black porcino is the porcino of the lower oak and chestnut, "Assente sotto faggio"
  (`laceno_boletus_aereus`). The Campania checklist lists *B. pinophilus* (`violante2002_campania_checklist`;
  the Campania appendix reads it in five areas, the Matese among them).
- **Molise bulletins** (Funghi Magazine, folklore; the rest are in the sanity contrasts below):
  - late June 2018: "Lazio, Abruzzo e Molise con ottime nascite in faggete appenniniche ma nascite
    contenute o assenti in boschi termofili o di collina" (`funghimagazine_molise_2018_07_01`);
  - September 2019: "Nel Molise collinare abbondano gli Aereus ed breve arriveranno anche gli Ovoli. In
    quello montano invece abbondano maggiormente Galletti ed Estatini" (`funghimagazine_molise_2019_09_12`);
  - mid-October 2022: "le grandi nascite in atto al momento in Toscana, Umbria, Marche, Abruzzo,
    Molise, Campania ... in gran parte si tratta di Porcini Neri"; *B. edulis* wants cold rain and
    "suoli acidi e non i suoli calcarei tipici delle aree a Sud dell'Appennino Settentrionale"
    (`funghimagazine_molise_2022_10_13`);
  - early August 2024, black porcini "a cavallo tra Chietino e Isernino"
    ([FM 2024-08-16](https://web.archive.org/web/20240816085355/https://funghimagazine.it/aggiornamento-funghi-16-08-2024/));
    early October 2024, "Porcini edulis stanno infatti fruttificando ad esempio sui monti
    dell'Appennino più meridionale tra Molise-Campania-Lucania"
    ([FM 2024-10-03](https://funghimagazine.it/funghi-04-10-2024-raccolte-di-porcini-ancora-strepitose-ecco-dove/));
  - November: weak Molise births expected in 2022 ("Aria fredda giungerà da Est impedendo nascite nelle
    Marche ed Abruzzo-Molise", FM 2022-11-12) and 2024 ("Non ci attendiamo ottime nascite in Molise e
    Abruzzo", FM 2024-11-08).
- **Local pages.** On the Molise Matese (Guardiaregia, Campochiaro) the beech "dai circa 1000 mt." has an
  undergrowth "ricco di Funghi (particolarmente Porcini)" (`isnews_guardiaregia_campochiaro2016`,
  folklore).
- **The record.** *B. reticulatus* in pure beech at 1,595 m on the Matese, 10 August 2025.

**Decisions.**

| key | factor | Tuscany | Molise | why | confidence |
|---|---|---|---|---|---|
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | 200 → 700 … **1,800 → 2,000** | the beech climbs to the tree line ("da quote massime attorno ai 1900 metri"; map max 1,916 m); Abruzzo, Campania and Lazio did the same; 7 woodland cells are above 1,600 m, so the change is small | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | hop-hornbeam on limestone, old-field regrowth and ash-maple-hornbeam; hop-hornbeam named only for the summer and black porcini (`camm_massi_polidori2022`) | plausible (weak) |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.3** | Aleppo pine and cypress below 700 m, black pine above, some fir; no Molise report; planted black pine has few, conifer-specific partners (`mrak2025_mycorrhiza`), no porcino among Aleppo-pine records (`ispra2018_mlg179_pino_aleppo`); the altitude band already discounts the low half | plausible (weak) |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | thorn, Spartium, broom and juniper scrub, no host | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,600 → 1,900** | the Molise record at 1,595 m in August beech (Tuscan band 0); southern beech "di medio-alta montagna" in June (FM), Laceno 1,100-1,700 m; southern records median 1,120 m; Molise beech median 1,249 m, as Campania's | plausible |
| *reticulatus* | habitat `mountain_pine` | 0.6 | **0.3** | as *edulis*; the oaks that have come into the wide-spaced low plantations keep it above non-host | plausible (weak) |
| *reticulatus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn and broom scrub, not chestnut and oak regrowth | plausible |
| *aereus* | season: summer/autumn handover | 400 → 600 m | **600 → 800 m** | "Nel Molise collinare abbondano gli Aereus" (mid-September 2019); Molise's mid-October 2022 flush "in gran parte ... Porcini Neri"; November black porcini in the Centre-South "a quote entro i 6-700 mt" under Turkey and downy oak (`funghimagazine_calendario_autunno2019`); the Molise oak median is 654 m and 439 woodland cells lie at 600-800 m, where the Tuscan split closed the season on 31 October (0.52 on 15 October at 650 m; now 0.88); Campania and Puglia made the same move | plausible (folklore sources) |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn and broom scrub | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | 300 → 800 … **1,800 → 2,000** | beech to the tree line, silver fir 800-1,400 m; as *edulis* and the neighbours | plausible (weak) |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **0.3** | black pine on limestone and Aleppo pine, not Scots pine; wants "terreni molto acidi" | plausible (weak) |
| *pinophilus* | habitat `mixed_broadleaf` | 0.3 | **0.1** | calcareous hop-hornbeam and old-field broadleaf (`funghimagazine_carpino_nero2026`, folklore) | plausible (weak) |
| *pinophilus* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | thorn and broom scrub | plausible |
| all four | other season windows, weather, stoppers, growth clock | — | kept | the Molise and Centre-South lore fits every other window; no regional numbers | as Tuscany |

Kept on purpose:
- **Deciduous oak** stays a full host of *B. reticulatus* and *B. aereus* and a marginal one (0.3, full
  credit on a pure cell) of *B. edulis* and *B. pinophilus*. No Molise source separates Turkey oak from
  downy oak.
- **Beech 0.6 for *B. reticulatus*** (Campania went to 1.0): 0.6 already gives any cell with half its
  woods in beech full credit, and the Molise record is in pure beech.
- **Beech 0.1 for *B. aereus*** (Abruzzo 0.3): "Assente sotto faggio" on the Laceno; Funghi Magazine
  has it in southern beech only in late summer; the altitude band (0 at 1,250 m) keeps it off most
  Molise beech (p10 1,035 m) anyway.
- **Mixed broadleaf 0.3 for *B. aereus*** (Campania and Lazio 0.6): 0.3 already gives a pure cell full
  credit; the class here is 29 % old-field regrowth.
- ***B. aereus*'s window dates** (upland summer 15 June → 1 August … 30 September → 31 October; lowland
  autumn 1 July → 1 September … 15 November → 15 December). Campania also moved the lowland end to 10
  January on Tyrrhenian lore about mild Decembers; no Molise source reports black porcini after
  October, and the November bulletins expect weak Molise births under cold east winds. The Alto Molise
  black porcini of early August (above 800 m) get the full upland window.
- ***B. reticulatus*'s window** (1 May → 1 June … 30 September → 15 November): the Molise page's "già a
  maggio" fits; no Molise source has April (Puglia's earlier start is not taken).
- ***B. aereus*'s altitude band** (full to 800 m, 0 at 1,250 m): the Molise oak is p90 955 m, so the band
  is full on most of it.

## Ovoli (*Amanita caesarea*)

**Regional evidence.** No Molise record. The law bans picking it "allo stato di ovolo chiuso"
(`lr_molise_4_2008`, art. 7.5). A Molise forager blog: "L'Amanita Caesarea, si trova dal mese di luglio
fino a settembre/ottobre nei boschi assolati, predilige i boschi di querce e castagno fino a oltre 1000
m" (`blog_tartufi_funghi_molise_ovolo2024`), and it is among the summer fungi "frequente nei territori
dell'alto Molise, la zona del Matese e nella zona del PNALM" (`blog_tartufi_funghi_molise_stagione2024`),
both folklore. Funghi Magazine: in mid-September 2019 in the Molise hills, after the black porcini, "a
breve arriveranno anche gli Ovoli" (`funghimagazine_molise_2019_09_12`); in October 2022 the ovoli "di
solito chiudono la buttata di Porcini Neri" (`funghimagazine_molise_2022_10_13`); "Porcini neri e Ovoli
reali spuntati in Puglia, Molise e Sicilia interna" in the third week of August 2025, with more births
expected in "alcune zone di Molise" (`funghimagazine_nascite_2025_08_22`). The hosts are here in bulk:
deciduous oak is two thirds of the woods.

**Decisions.**

| factor | Tuscany | Molise | why | confidence |
|---|---|---|---|---|
| season | 1 Jun → 1 Sep … 5 Nov → 30 Nov | 1 Jun → **1 Aug** … 5 Nov → 30 Nov | the Molise blog's "dal mese di luglio"; ovoli in Molise in the third week of August 2025 (0.75 on the Tuscan ramp); Abruzzo made the same move on the Laga; the end is kept (ovoli with the October black porcini) | plausible (a blog and national bulletins) |
| altitude | … 750 → 1,100 | … **900 → 1,200** | the Molise blog's oak and chestnut "fino a oltre 1000 m"; the closed Turkey-oak woods (41.741) sit at p10 546 m, median 795 m, p90 1,046 m (Alto Molise, northern Mainarde, eastern Matese); with the Tuscan band half of them would score under 0.87 and the top tenth under 0.16; the neighbours find it at 700-900 m (Laga) and 753-943 m (5 of 21 Lazio records); zero at IUCN's "only seldom above 1200 m"; Abruzzo and Lazio took the same band | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn, Spartium, broom and juniper scrub, not the heath and clearings with scattered oaks | plausible |
| habitat deciduous oak, chestnut 1.0; evergreen oak 0.6; macchia, mixed broadleaf 0.3; beech 0 | — | kept | no Molise evidence either way | strong (hosts) |
| weather rules, sun exposure | — | kept | no regional numbers | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "gallinacci", "galletti", "gallucci")

**Regional evidence.** The law's minimum size for "Cantharellus cibarius (Gallinaccio)"
(`lr_molise_4_2008`); two *C. cibarius* records, 6 June 2023 in a Turkey-oak cell at 690 m (Busso) and
2 July 2009 at about 890 m (Sant'Angelo del Pesco). The neighbours on both sides:
- the Campania side of the Matese: "con l'avvento dei mesi estivi, giugno e luglio, cominciano a
  spuntare" porcini and "galletti o finferli" (`amicomatese_non_solo_porcini2018`, a Campania society,
  2018);
- the Laceno: "Raggiunge il massimo della produzione da Maggio a Luglio", from the valley chestnut up
  to the beech, "prediligendo il faggio e la quercia" (`laceno_cantharellus_cibarius`, folklore);
- the Laga: the first gallucci in early May, "la cerreta" by late May, "molti" with the beech porcini
  in mid-June (`funghiteramani_blog`, folklore).
In ISPRA's national records *C. cibarius* is 1.81 % of the downy-oak records, with "un picco di
frequenza" there, and 1.8 % of the beech ones (`ispra2019_mlg187_flora_micologica`).
Molise bulletins and blog (folklore): "Molise e Abruzzo per ora vedono ancora nascite di Prugnoli sui
monti e di Finferli sui colli" (late May 2023); "i Finferli/Galletti risultano ben presenti anche in
Molise ma non i Porcini" (2 June 2023, `funghimagazine_aggiornamento_2023_06_02`) and "abbondano più che
mai Finferli/Galletti" (mid-June 2023, `funghimagazine_aggiornamento_2023_06_16`); on 1 June 2024 "In
Appennino nascite di soli Finferli e poco altro" in the Molise provinces
(`funghimagazine_semaforo_abruzzo_molise_2024`); *C. pallens* "diffusamente raccolti dalle Marche al
Molise ... nell'ultima decade di giugno" 2022; in September 2019 "In quello montano invece abbondano
maggiormente Galletti ed Estatini" (`funghimagazine_molise_2019_09_12`); mid-September 2024 "Nel Molise
ultime buone nascite sui monti, Porcini ultimi, Finferli"; and from October "in grande quantità il
gallinaccio" (`blog_tartufi_funghi_molise_stagione2024`).

**Decisions.**

| factor | Tuscany | Molise | why | confidence |
|---|---|---|---|---|
| season, mountain window (above 1,000 m, blended from 600 m) | 1 Jun → 1 Jul … 15 Oct → 15 Nov | **15 May → 15 Jun** … 15 Oct → 15 Nov | chanterelles "In Appennino" in the Molise provinces by 1 June 2024 and "ben presenti anche in Molise" on 2 June 2023; both Molise records June-early July; Matese "giugno e luglio"; Laceno peak "da Maggio a Luglio"; Laga from May; Abruzzo and Campania made the same move | plausible (bulletins and the neighbours) |
| season, lowland window | 15 Apr → 10 May … 15 Dec → 25 Jan | kept | "Finferli sui colli" in late May; the blog's October-December gallinacci fall inside it below 600-1,000 m; little Molise woodland lies below 600 m | plausible |
| altitude | … 1,000 → 1,700 | … **1,400 → 1,900** | beech median 1,249 m, p90 1,540 m; silver fir 800-1,400 m; with the Tuscan band half the beech would lose a third of its credit or more; Abruzzo, Campania and Lazio made the same move | plausible |
| habitat deciduous oak | 0.3 | **0.6** | two thirds of the woods; the Busso record in Turkey oak; the Laga "cerreta", the Laceno "quercia"; ISPRA's downy-oak "picco di frequenza"; the Marche, Abruzzo, Campania and Lazio made the same move | plausible |
| habitat `mountain_pine` | 0.3 | **0.1** | black pine on limestone above 700 m, Aleppo pine and cypress below; no *Cantharellus* among the Aleppo-pine records (`ispra2018_mlg179_pino_aleppo`) | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.3 | **0.1** | thorn, Spartium, broom and juniper scrub (Abruzzo and Campania; Lazio kept 0.3 on records in its oak-mantle scrub); the 2009 record's cell is mostly scrub but outside the woodland mask | plausible (weak) |
| habitat beech 0.6, chestnut and evergreen oak 1.0, macchia 0.3 | — | kept | beech 0.6 already gives a half-beech cell full credit and no Molise source ties chanterelles to beech (Abruzzo and Campania went to 1.0 on their own foragers); chestnut and holm oak are 1.5 % of the woods | plausible |
| soil pH, lithology | disabled | kept disabled | woodland topsoil pH 6.2-7.3; the chestnut belt is small; no lithology layer | plausible |
| weather rules | — | kept | no regional numbers | as Tuscany |

## Effect on the grid (habitat × altitude gates)

Computed on the 1,455 woodland cells of the grid of 2026-09-30, the Tuscan rule files against the
Molise ones (the season, weather and stoppers are not in it):

| key | habitat gate full (Tuscan → Molise) | altitude gate full | mean of habitat × altitude |
|---|---|---|---|
| *B. edulis* | 66 % → 31 % | 54 % → 55 % | 0.82 → 0.76 |
| *B. reticulatus* | 100 % → 100 % | 87 % → 99 % | 0.94 → 1.00 |
| *B. aereus* | 88 % → 88 % | 61 % → 61 % | 0.80 → 0.80 |
| *B. pinophilus* | 66 % → 31 % | 39 % → 39 % | 0.72 → 0.67 |
| ovoli | 88 % → 87 % | 53 % → 72 % | 0.73 → 0.82 |
| gallinacci | 66 % → 98 % | 80 % → 97 % | 0.93 → 0.99 |

- **Porcini group** (max over the four keys): 0.998 → 1.000. On the 182 beech-dominated cells *B.
  reticulatus* goes from 0.57 to 0.99, which gives the summer group score a key in the high beech; the
  group was already full there through *B. edulis*.
- ***B. edulis* and *B. pinophilus*** lose full habitat credit on a third of the cells. Most of it is
  hop-hornbeam, old-field regrowth and scrub diluting oak cells: with deciduous oak at 0.3 and mixed
  broadleaf at 0.1, a cell that is 80 % oak and 20 % hop-hornbeam scores 0.83 instead of 1. These cells
  still score through *B. reticulatus* and *B. aereus*, which are full on oak. Neither decision rested
  on the grid's shares.
- **Ovoli**: the band lifts the Turkey-oak cells at 750-1,200 m; the altitude gate is full on 72 % of
  woodland cells instead of 53 %, and the beech-dominated cells stay near 0 (0.02 → 0.08).
- **Gallinacci**: the deciduous-oak and altitude changes lift the gates on almost every cell.
- **Seasons** (not in the table): the *B. aereus* handover at 600-800 m keeps the autumn window on the
  hill oak (400-800 m) and costs it a little in early August. Its season gate on 1 August / 15 October / 5
  November is, at 500 m, 0.50 / 1.00 / 1.00 (Tuscan split 0.75 / 0.76 / 0.50) and, at 650 m, 0.62 /
  0.88 / 0.75 (Tuscan 1.00 / 0.52 / 0); below 400 m and above 800 m nothing changes. The ovolo gate is
  full from 1 August (Tuscan 0.67 on 1 August, 0.84 on 15 August).

## Weather rules: why none changed

- **Rain amount and lag.** No Molise source gives a rain amount or lag. The forager blog's "Dopo un
  lungo periodi di siccità, finalmente è arrivata a fine estate la pioggia" and the porcini that
  followed (`blog_tartufi_funghi_molise2025`) are what the rain trigger and the 30-day rain do. The
  Tuscan amount and lag ramps stay; Funghi Magazine's Centre-South lore ("30/40 millimetri, meglio se
  superiori ai 50", `funghimagazine_calendario_autunno2019`) sits at the top of the 10 → 30 mm ramp.
- **Temperature and cold springs.** The Alto Molise's cold is read from each cell's own weather by the
  growth clock, the temperature bands, the cold-night and frost rules. No Molise source gives a
  threshold.
- **Summer drought.** The coast and the low hills have three arid summer months, the Matese and the Alto
  Molise summer rain; the porcini 30-day rain is relative to each cell's normal, and the chestnut-free,
  low woods are few.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted on Tuscan gauges; checking it on
  Molise gauges is a region-config task (`regions/molise.md`), not a species one.
- **Slope and sun exposure.** Molise woodland is gentler than Tuscany's (median 14.8°, p90 21.9°, 4.3 %
  of cells over 25°), so the slope stopper barely acts; the notes say so. The sun-exposure stoppers act
  only below 900-1,100 m and were left alone.

## Groups and keys

Nothing is dropped. The six keys exist in Molise as far as its thin evidence can say: the law names
the porcini group, the chanterelle and the ovolo; iNaturalist has *B. edulis*, *B. reticulatus* and *C.
cibarius*; a national bulletin reports black porcini and ovoli in August 2025; *B. pinophilus* rests on
the neighbours (the Campania checklist on the Matese, Funghi Magazine's sporadic Abruzzo-Molise-Campania
mountains) and on its hosts, and the group score takes the max. `mixed_broadleaf_conifer` and
`other_conifer` are empty on the Molise map but stay in the rule files, as in every region; they score
no cell.

## Sanity contrasts

`molise/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written down on
2026-09-30, before any Molise score existed. The schema has no group field: contrasts are porcini unless
their id starts with `ovoli_` or `gallinacci_` (read those with `--group ovoli` / `--group
gallinacci`). "Normal" is the area's mean over 2017-2025.

**17 contrasts: 14 porcini, 1 ovoli, 2 gallinacci**, researched on 2026-09-30 by a research agent that
opened every cited page. Every quoted Italian phrase was then checked by script against the captured
page texts (all found, the pages' own typos included: "Ancora buona nascite", "ripeture", "ed breve",
"1l 2024"). Every comune is an ISTAT 2025 name inside Molise (checked against the ISTAT 2025 boundaries,
COD_REG 14), and every area has woodland cells on the grid of 2026-09-30.

**The sources are thin, and almost all one magazine.** Molise local press almost never says how a
mushroom season went: searches of Primo Piano Molise, il Quotidiano del Molise, isNews, Molise Network,
CBlive, Il Giornale del Molise, L'Eco dell'Alto Molise, Molise Tabloid, Altomolise.net and Teleregione
found lost foragers, permits, fines and recipes. **Sixteen of the 17 contrasts rest mainly on Funghi
Magazine's national bulletins** (read through Wayback Machine captures, or the live site where its
robots.txt allows), whose Molise lines are one or two sentences, often lumped with Abruzzo, Campania or
Puglia. The one that does not, `molise_2017_below_normal`, rests on a single sentence from a
Campobasso mushroom show. Local second sources: Il Giornale del Molise (2022), L'Eco dell'Alto Molise
(2024, the ASReM mycologist), the Blog dei Tartufi e Funghi del Molise (2024, 2025), Coldiretti's
Campagna Amica (2020). Nothing usable was found for 2016.

**Areas** (woodland cells on the grid of 2026-09-30):

| area | comuni or provinces | woodland cells |
|---|---|---|
| `molise` | the whole region | 1,455 |
| `cb` | province of Campobasso | 531 |
| `is` | province of Isernia | 924 |
| `alto_molise` | Agnone, Capracotta, Vastogirardi, San Pietro Avellana, Carovilli, Pescopennataro, Castel del Giudice, Sant'Angelo del Pesco, Rionero Sannitico, Belmonte del Sannio, Pietrabbondante, Pescolanciano, Roccasicura, Forlì del Sannio, Poggio Sannita, Castelverrino | 321 |
| `molise_montano` | the beech and fir belt: Capracotta, Vastogirardi, San Pietro Avellana, Pescopennataro, Castel del Giudice, Sant'Angelo del Pesco, Rionero Sannitico, Carovilli (Alto Molise tops); Roccamandolfi, Cantalupo nel Sannio, San Massimo (Campitello Matese), San Polo Matese, Campochiaro, Guardiaregia, Sepino, Bojano (Matese); Frosolone, Macchiagodena, Sant'Elena Sannita (Montagnola di Frosolone); Pizzone, Castel San Vincenzo, Scapoli, Rocchetta a Volturno, Filignano, Montenero Val Cocchiara (Mainarde) | 483 |
| `basso_molise_colline` | the hill oak of the Trigno, Biferno and Fortore: San Felice del Molise, Montemitro, Montefalcone nel Sannio, Guardialfiera, Casacalenda, Castelmauro, Roccavivara, Trivento, Lucito, Salcito, Petrella Tifernina, Morrone del Sannio, Ripabottoni, Castellino del Biferno, Lupara, Civitacampomarano, Riccia, Gambatesa, Tufara, Sant'Elia a Pianisi, Pietracatella, San Giovanni in Galdo, Campolieto, Toro | 224 |
| `confine_aq_is` | the Isernia comuni on the L'Aquila border: Pizzone, Castel San Vincenzo, Montenero Val Cocchiara, Rionero Sannitico, San Pietro Avellana, Castel del Giudice | 127 |

How places were read: Funghi Magazine's Molise "Sannio" semaforo area lists Poggio Sannita, Castelverrino,
Pietrabbondante, Vastogirardi, Capracotta, Pescopennataro, San Pietro Avellana, Montalto (a frazione of
Rionero Sannitico), Villa San Michele (a frazione of Vastogirardi) and Carovilli, so its Molise "Sannio"
is the Alto Molise; "a cavallo tra Chietino e Isernino" is the Alto Molise too; Campitello Matese is in
San Massimo; its "Monti della Meta molisani" are Pizzone, Castel San Vincenzo and Scapoli; its hill-oak
area "San Felice del Molise-Montemitro-Montefalcone nel Sannio e Guardialfiera, arrivando a
Casacalenda-Montorio nei Frentani" seeds `basso_molise_colline` (Montorio nei Frentani, 2 woodland
cells, left out). Small comuni inside the areas: Macchiagodena 4 woodland cells, Sant'Elena Sannita 3,
San Felice del Molise, Tufara and Toro 4 each; every area as a whole is large.

| id | group | higher | lower | main source (second sources) | weakness |
|---|---|---|---|---|---|
| `montano_june_2018_timing` | porcini | `molise_montano` 2018, 18 Jun-1 Jul | same, 3-16 Jun | [FM 2018-07-01](https://web.archive.org/web/20240417091132/https://funghimagazine.it/aggiornamento-funghi-01-luglio-2018/): "Lazio, Abruzzo e Molise con ottime nascite in faggete appenniniche" ([FM 2018-06-16](https://web.archive.org/web/20240614053245/https://funghimagazine.it/aggiornamento-funghi-16-giugno-2018/): "Molise ed Abruzzo fermi al palo per via del freddo o del vento di Levante-Tramontana") | one outlet; Molise lumped with Abruzzo; the mountain belt is read from "faggete appenniniche" |
| `montano_vs_colline_late_june` | porcini | `molise_montano` 2018 and 2022, 18-30 Jun | `basso_molise_colline`, same | FM 2018-07-01: "ma nascite contenute o assenti in boschi termofili o di collina" ([FM 2022-06-24](https://funghimagazine.it/siccita-e-funghi/): "in Molise, tranne che nei settori costieri o basso collinari") | each year rests on one sentence; the 2022 line is about all fungi |
| `molise_june_2022_2024` | porcini | whole region 2022, 16-30 Jun | same, 2024 | [FM 2022-07-01](https://web.archive.org/web/20240524103838/https://funghimagazine.it/molti-porcini-a-breve-vediamo-dove-01-07-2022/): "dalle Marche-Abruzzo-Molise alla Campania e Calabria dopo le piogge del 9/10 giugno" ([FM 2024-06-14](https://web.archive.org/web/20260318225204/https://funghimagazine.it/aggiornamento-funghi-14-06-2024/), [FM 2024-06-28](https://web.archive.org/web/20260318215340/https://funghimagazine.it/aggiornamento-funghi-28-06-2024/): "L'eccesso di calore ha mandato in letargo i miceli fungini di Campania, Molise") | national bulletin; Molise lumped with neighbours both years |
| `molise_september_vs_august_2019` | porcini | whole region 2019, 4-19 Sep | same year, 2-17 Aug | [FM 2019-09-12](https://web.archive.org/web/20240527073030/https://funghimagazine.it/la-grande-buttata-di-funghi-porcini-di-settembre-dove-piovuto-in-italia/): "Il Molise è superstar" ([FM 2019-08-01](https://web.archive.org/web/20240620075507/https://funghimagazine.it/funghi-porcini-ed-ovoli-nei-cesti-dove-piovuto-in-italia/): "nascite al momento scarse"; [FM 2019-08-16](https://web.archive.org/web/20240721235739/https://funghimagazine.it/buone-nascite-di-funghi-porcini-vediamo-dove-le-piogge-caduta-in-italia/); [FM 2019-09-27](https://web.archive.org/web/20240519045618/https://funghimagazine.it/dove-cercare-funghi-porcini-nellultimo-weekend-di-settembre-i-funghi-di-ottobre-il-ritorno-delle-grandi-piogge/)) | one outlet; the 16 August line is about the inland South; the season gate slightly favours September (see below) |
| `molise_september_2019_2020` | porcini | whole region 2019, 4-19 Sep | same, 2020 | FM 2019-09-12 ([FM 2020-09-04](https://web.archive.org/web/20240620083936/https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2020/): "Il caldo Africano in crescendo ha fatto cessare le nascite tra Marche-Abruzzo-Molise"; [FM 2020-09-21](https://web.archive.org/web/20240721222714/https://funghimagazine.it/meteofunghi-21-09-2020/): "Situazione pessima tra Molise, Campania, Puglia e Basilicata"; [Campagna Amica 2020-09-14](https://www.campagnamica.it/attualita/funghi-scatta-la-corsa-ai-porcini-e-boom-nei-boschi/)) | 2019 rests on FM only; the 2020 lines are macro-regional |
| `molise_2017_below_normal` | porcini | whole region, normal, 16 Sep-7 Oct | same, 2017 | [ugodugo.it 2017-10-09](https://www.ugodugo.it/tradizioni-e-prodotti/338-molise-terra-di-funghi): "nonostante la pessima annata dovuta alla scarsa piovosità" | **one source**, one sentence in a report on the Campobasso show; "annata" is the whole season, so the window is inferred; "normal" includes 2017 |
| `molise_2020_summer_vs_september` | porcini | whole region 2020, 24 Jul-10 Aug | same year, 1-18 Sep | [FM 2020-07-23](https://web.archive.org/web/20240522153936/https://funghimagazine.it/aggiornamento-meteofunghi-23-07-2020/): "Ottime piogge in Molise ... con ottime nascite già in atto o a breve tanto in collina-piano, quanto in montagna" ([FM 2020-08-07](https://web.archive.org/web/20240303091449/https://funghimagazine.it/aggiornamento-meteofunghi-07-08-2020/); FM 2020-09-04; FM 2020-09-21) | one outlet, four dated bulletins; timing contrast, the season gate slightly favours September for *B. edulis* |
| `cb_august_2020_2023` | porcini | province CB 2020, 1-18 Aug | same, 2023 | FM 2020-08-07 (FM 2020-07-23; [FM 2020-08-20](https://web.archive.org/web/20240522151747/https://funghimagazine.it/aggiornamento-meteofunghi-20-08-2020/); [FM 2023-07-28](https://web.archive.org/web/20240724155834/https://funghimagazine.it/aggiornamento-funghi-28-07-2023/), [FM 2023-08-17](https://web.archive.org/web/20240721230027/https://funghimagazine.it/aggiornamento-funghi-17-08-2023/): "Il Molise dovrà attendere giorni migliori", [FM 2023-08-24](https://web.archive.org/web/20240722000446/https://funghimagazine.it/aggiornamento-nascite-porcini-24-08-2023/)) | the 2023 side is inferred from South-wide and region-wide negatives; province CB so as to leave out the 2023 L'Aquila-Isernia border flush |
| `cb_vs_is_august_2020` | porcini | province CB 2020, 8-20 Aug | province IS, same | FM 2020-08-20: "soprattutto in provincia di Campobasso, molto meno, o nulla tra le province di Isernia e Chieti" | **one sentence**; the Isernia side of the Matese (Roccamandolfi, Cantalupo) may have had births ("presenti nel Matese") |
| `confine_aq_is_vs_cb_august_2023` | porcini | `confine_aq_is` 2023, 18-30 Aug | province CB, same | FM 2023-08-24: "La buttata eccezionale si sta registrando anche in territorio molisano tra la valle dell'Inferno ed i boschi di Barretta, quindi a cavallo tra le province di l'Aquila e Isernia" | **one bulletin**, relaying tourism operators (FM says its correspondents confirm); neither place name was found in a gazetteer ("Barretta" may be Barrea, AQ, next to Pizzone), so the area is the least certain one |
| `alto_molise_august_2024_2023` | porcini | `alto_molise` 2024, 30 Jul-12 Aug | same, 2023 | [FM 2024-08-06](https://web.archive.org/web/20260318214447/https://funghimagazine.it/aggiornamento-nascite-funghi-06-08-2024/): "Le piogge ripeture nella provincia di Isernia stanno dando locali nascite di Porcini" ([FM 2024-08-16](https://web.archive.org/web/20240816085355/https://funghimagazine.it/aggiornamento-funghi-16-08-2024/): "a cavallo tra Chietino e Isernino"; FM 2023-07-28; FM 2023-08-17) | "Chietino-Isernino" read as the Alto Molise; the 2023 side is inferred from generic negatives |
| `cb_late_august_2025_2023` | porcini | province CB 2025, 18 Aug-3 Sep | same, 2023 | [FM 2025-09-04](https://web.archive.org/web/20251220154140/https://funghimagazine.it/buttata-record-2025-annata-eccezionale-per-i-porcini/): "Il Molise è già saltato in aria sotto una pioggia di Porcini neri" ([FM 2025-08-21](https://web.archive.org/web/20250822194753/https://funghimagazine.it/aggiornamento-nascite-funghi-22-08-2025/); [FM 2025-08-29](https://web.archive.org/web/20250829134646/https://funghimagazine.it/aggiornamento-nascite-funghi-29-08-2025/); [Blog dei Tartufi e Funghi del Molise 2025-09-08](https://ilblogdeitartufiefunghimolisani.it/2025/09/08/e-tempo-di-porcini-ma-attenzione-alle-false-credenze/); FM 2023-08-24) | the 2025 lines name no province (CB chosen to avoid the 2023 border flush); florid prose; the blog is vague on place |
| `ovoli_cb_august_2025_2023` | ovoli | province CB 2025, 12-24 Aug | same, 2023 | FM 2025-08-21: "Porcini neri e Ovoli reali spuntati in Puglia, Molise e Sicilia interna" (FM 2023-08-17; FM 2023-08-24) | **one sentence** for 2025; the lower side is not about ovoli |
| `molise_october_2022_2023` | porcini | whole region 2022, 3-14 Oct | same, 2023 | [FM 2022-10-13](https://web.archive.org/web/20240421083643/https://funghimagazine.it/meteo-funghi-13-10-2022/): "le grandi nascite in atto al momento in Toscana, Umbria, Marche, Abruzzo, Molise, Campania" ([Il Giornale del Molise 2022-10-20](https://www.ilgiornaledelmolise.it/2022/10/20/santelia-a-pianisi-trovato-un-porcino-da-record-pesa-750-grammi/); [FM 2023-10-12](https://web.archive.org/web/20240521230836/https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "il vento di Tramontana ha di fatto bloccato ogni velleità porcina"; [FM 2023-10-27](https://web.archive.org/web/20240416195849/https://funghimagazine.it/aggiornamento-porcini-27-10-2023/)) | 2022 is a national list; the local find falls just after the window; FM 2023-10-27 admits "un solo cenno di buttata a fine settembre-inizio ottobre" |
| `molise_early_october_2024_2020` | porcini | whole region 2024, 1-12 Oct | same, 2020 | [FM 2024-10-03](https://funghimagazine.it/funghi-04-10-2024-raccolte-di-porcini-ancora-strepitose-ecco-dove/): "Nascite di Porcini senza sosta in alcune zone della Lucania occidentale, Campania, Molise" ([L'Eco dell'Alto Molise 2024-10-17](https://ecoaltomolise.net/scopri-il-mondo-dei-funghi-corsi-di-formazione-al-circolo-san-pio-per-il-patentino/): "quest'anno il bosco appare particolarmente florido"; [blog 2024-11-01](https://ilblogdeitartufiefunghimolisani.it/2024/11/01/raccolta-di-funghi-straordinaria/); [FM 2020-10-08](https://web.archive.org/web/20240416201403/https://funghimagazine.it/aggiornamento-meteofunghi-08-10-2020/): "Quanto al Molise, non ci sono notizie di ritrovamenti") | [FM 2024-09-27](https://web.archive.org/web/20240928144721/https://funghimagazine.it/aggiornamento-nascite-funghi-27-09-2024/) had Molise births "ridotte o ancora assenti", so the flush starts at the window's edge; the local quotes cover the season, not the dates; 2020 says "no news", not "no births" |
| `gallinacci_molise_june_2023_2024` | gallinacci | whole region 2023, 8-20 Jun | same, 2024 | [FM 2023-06-16](https://web.archive.org/web/20240417084120/https://funghimagazine.it/aggiornamento-funghi-16-06-2023/): "abbondano più che mai Finferli/Galletti" ([FM 2023-06-02](https://web.archive.org/web/20240620080011/https://funghimagazine.it/aggiornamento-funghi-02-06-2023/); FM 2024-06-14: "Anche i Finferli sono spariti sotto l'incalzare del gran caldo"; FM 2024-06-28) | national bulletin; 2024 had finferli earlier (1 June semaforo), so the window stays in mid-June |
| `gallinacci_molise_late_june_2022_2024` | gallinacci | whole region 2022, 20-30 Jun | same, 2024 | FM 2022-07-01: *C. pallens* "si sono già diffusamente raccolti dalle Marche al Molise ... nell'ultima decade di giugno" (FM 2024-06-28; FM 2024-06-14) | "dalle Marche al Molise" is a broad band; the 2024 line is about fungi in general |

**Season gates.** Most contrasts compare the same dates in two years or two areas, so the gate
cancels. Three are timing contrasts inside one year:
- `montano_june_2018_timing` (18 June-1 July against 3-16 June): the porcini group is carried by *B.
  reticulatus*, whose window is full in both, so the gate does not decide it.
- `molise_september_vs_august_2019` and `molise_2020_summer_vs_september`: *B. reticulatus* is full in
  both windows and *B. aereus* in the hills is full from 1 August (upland) or ramps to 1 September
  (lowland, below 600-800 m), and *B. edulis* ramps to 1 September; the gate slightly favours September
  on the low and the high cells. `molise_2020_summer_vs_september` asks the opposite, so it is the
  stricter test.

**Outlets that block AI agents** (robots.txt checked on 2026-09-30; nothing fetched from them): ANSA and
Il Mattino disallow Anthropic's crawlers; Termoli Online hides its robots.txt behind a Cloudflare
challenge; InfoOggi gives ClaudeBot a crawl delay and blocks its topic pages. Primo Piano Molise, il
Quotidiano del Molise, isNews, Molise Network, CBlive, Il Giornale del Molise, Altomolise.net, L'Eco
dell'Alto Molise, Molise Tabloid, Teleregione, Funghi Magazine (crawl delay 30 s), web.archive.org and
Campagna Amica allow them. A Quotidiano del Molise page on a 750 g porcino at Macchiagodena (October
2022) returns 404 and is not cited.

Candidates left out:
- May 2022 against May 2023 porcini: the 2022 side is a parenthesis ("con conseguenti buone nascite di
  Porcini in Campania e Molise a metà mese"), and the summer porcino window only ramps in from 1 May.
- Early October 2021 ("in diminuzione le nascite già in corso"): hedged, a decline.
- Forecasts rather than reports: the Sannio and the Matese molisano "tra le zone favorite" (September
  2021), Molise third in a September 2022 ranking, "sottotono" November 2022, ovoli "a breve" in
  September 2019.
- Gallinacci September 2019 against 2020: the 2020 side is not about chanterelles.
- Late August 2024 "buona fase con ottime nascite" in Molise: undated within August and confounded by
  over-picking.
- Gallinacci May 2025 ("ottime buttate di Finferli" in Abruzzo and Molise): May 2023 also had "Finferli
  sui colli", so no clean lower year.
- Lost-forager news clusters (October 2018, July and November 2020, September-October 2024, September
  2025): say nothing about fruiting.
- The Campania file's Molise-side Matese lines (2020, 2021, 2024) were not reused.

**Year picture from the sources** (context, not scored):
- **2016**: nothing usable.
- **2017**: dry and poor ("pessima annata dovuta alla scarsa piovosità", Campobasso show, 7-8 October).
- **2018**: mid-June stalled by cold east winds; a late-June flush in the beech, not in the hill oak;
  nothing on the autumn.
- **2019**: early August wet but "nascite al momento scarse"; September "Il Molise è superstar", black
  porcini in the hills, chanterelles and summer porcini in the mountains; late September "ancora
  discrete nascite".
- **2020**: first June births on the coast and hills; good late July to mid-August, above all in the
  province of Campobasso; September stopped by heat; early October "non ci sono notizie di
  ritrovamenti".
- **2021**: late June births rising; hot, dry August in the South; big early-September rains, wetter
  on the Molise side of the Matese; births declining in early October, stopped by cold in mid-October.
- **2022**: mid-May porcini; after the 9-10 June rains good inland births, *C. pallens* widely picked
  in late June; mid-October "grandi nascite", mostly black porcini; a weaker November.
- **2023**: May stalled; June abundant chanterelles but no porcini; a dry August but for an
  "eccezionale" flush on the L'Aquila-Isernia border after the rain of 16 August; an autumn blocked by
  wind ("nessuna vera buttata").
- **2024**: early June chanterelles, then heat and wind; summer and black porcini at the start of August
  on the Chieti-Isernia border; black porcini in early September, "ultime buone nascite sui monti" in
  mid-September; early October "senza sosta", with *B. edulis* on the southern mountains; "l'anno della
  raccolta di funghi straordinario" (blog).
- **2025**: May chanterelles; a scarce late June; black porcini and ovoli from about 20 August, "una
  pioggia di Porcini neri" by early September.
- **Upcoming data**: the Università del Molise and the AMB "Carlo Linneo" group began a mycological
  survey of Pescopennataro in October 2025
  ([L'Eco dell'Alto Molise 2025-10-19](https://ecoaltomolise.net/mappatura-micologica-pescopennataro-fa-sul-serio-obiettivo-una-banca-dati-sul-territorio/)).

## Open questions

- **Almost no records.** 4 records of the six keys in all Molise; the backtest will not be able to say
  anything about Molise alone. Pooling it with Abruzzo and Campania is the obvious step.
- **Turkey oak versus downy oak.** Two thirds of the woods are one class. Whether the black porcino,
  the ovolo and the chanterelles prefer the mesophilous Turkey oak of the Alto Molise or the warm downy
  oak of the hills is unknown here; the grid cannot split them without a new habitat key.
- **The *B. aereus* autumn.** The handover now sits at 600-800 m on bulletins that name Molise in
  September and October; no Molise source reports black porcini in November or December, so the
  lowland end stays 15 December. Early August on the 400-800 m oak loses a little (the upland summer
  window no longer fully covers it): the Alto Molise black porcini of August 2024 were reported on the
  Chieti-Isernia border, mostly higher.
- **Ovolo timing and heights.** The August start and the 1,200 m top rest on one Molise blog and
  national bulletins; no Molise record exists.
- **Chanterelles in late autumn.** The Molise blog has "in grande quantità il gallinaccio" from October
  to the turn of the year. Below 600 m the lowland window covers it; above 1,000 m the mountain window
  closes on 15 November. If the backtest ever has Molise autumn records, the mountain end is the thing
  to check.
- **Wind.** The Molise bulletins blame the Tramontana and cold east winds for wasted rain again and
  again ("il vento batte pioggia 1 a 0", October 2023). The drying stopper (ET0 as a proxy) is the only
  rule that reads it; a wind variable is not ingested.
- **The beech in midsummer.** As in Abruzzo, *B. reticulatus*' band now carries the July-August beech;
  *B. edulis* and *B. pinophilus* leave a gap from 20 July to mid-August, which only matters above 1,600
  m, where Molise has 7 cells.
- **Plantations.** `mountain_pine` mixes Aleppo pine and cypress (no host) below 700 m and black pine
  above; the grid gives the class one habitat. A split at 700 m would need a second habitat key.
- **Leads not read.** "Tipi forestali e preforestali della Regione Molise" (the Region's forest-type
  manual, not online); the Università del Molise vegetation work on the Alto Molise ("Faggete e cerrete
  mesofile nell'Alto Molise"); the Collemeluccio-Montedimezzo reserve's surveys (no fungi published);
  the AMB group of Bonefro and the A.M.A. Matese of Bojano, whose exhibitions list Molise species but
  publish no season data.
- **Sites that block AI agents.** The Parco Nazionale d'Abruzzo, Lazio e Molise (as the Abruzzo research
  found) was not opened.

## References added for Molise

| id | kind | verified | used for |
|---|---|---|---|
| `lr_molise_4_2008` | institutional | verified | picking rules; porcini group, chanterelle and ovolo as regional species |
| `regione_molise_ctf2009` | institutional | verified | forest types, belts, places, climate zones; chestnut rare; conifer reforestation by belt |
| `ispra348_2021_cnat_molise` | institutional | verified | what each Carta della Natura class holds (beech to 1,900 m, 42.G_n, 4D_n, silver fir) |
| `infc2015_molise` | dataset | verified | forest area and categories |
| `mushma_molise_forest_composition_2026` | analysis | verified | habitat areas and elevations on the map; grid elevation, shares, slope, pH |
| `mushma_occurrence_check_molise_2026` | analysis | verified | Molise record counts, months, cells |
| `cacciatoridifunghi_molise2023` | web | verified | Molise porcini season order (folklore) |
| `blog_tartufi_funghi_molise2025` | web | verified | *B. edulis* in the Molise woods after the late-summer rain of 2025 (folklore) |
| `blog_tartufi_funghi_molise_ovolo2024` | web | verified | ovolo July to September/October, oak and chestnut "fino a oltre 1000 m" (folklore) |
| `blog_tartufi_funghi_molise_stagione2024` | web | verified | summer fungi of the Alto Molise and Matese; gallinacci from October (folklore) |
| `funghimagazine_molise_2018_07_01` | web | verified | late-June porcini in the beech, not the hill oak (folklore) |
| `funghimagazine_molise_2019_09_12` | web | verified | black porcini in the hills, summer porcini and chanterelles in the mountains, ovoli after (folklore) |
| `funghimagazine_molise_2022_10_13` | web | verified | October black porcini in Molise; ovoli close the flush; *B. edulis* wants acid soils (folklore) |
| `funghimagazine_semaforo_abruzzo_molise_2024` | web | verified | only chanterelles in the Molise Apennine on 1 June 2024 (folklore) |
| `isnews_guardiaregia_campochiaro2016` | web | verified | the Matese beech from about 1,000 m "ricco di Funghi (particolarmente Porcini)" (folklore) |

Existing references the Molise changes lean on, each re-opened for this card:
`funghimagazine_calendario_primavera_estate` (Centre-South estatini in beech, sporadic edulis on the
Abruzzo-Lazio-Molise border, *B. pinophilus* rare), `funghimagazine_nascite_2025_08_22` (black porcini
and ovoli in Molise, August 2025, Wayback capture), `laceno_boletus_aestivalis`, `laceno_boletus_aereus`,
`laceno_cantharellus_cibarius`, `amicomatese_non_solo_porcini2018`, `violante2002_campania_checklist`,
`vda_onofri2003_checklist` (95 fungi on record for Molise; "Molise and Valle d'Aosta are the less
investigated Regions"), `funghiteramani_blog` (the 2014 and 2016 chanterelle posts),
`ispra2019_mlg187_flora_micologica`, `ispra2018_mlg179_pino_aleppo`, `mrak2025_mycorrhiza`,
`camm_massi_polidori2022`, `funghimagazine_carpino_nero2026`, `bonanomi2020_treeline` (abstract),
`iucn_caesarea2019`, `funghimagazine_calendario_autunno2019`, `funghimagazine_aggiornamento_2023_06_02`,
`funghimagazine_aggiornamento_2023_06_16` (the Molise chanterelle lines, via the research agent's
captures). The Campania and Lazio occurrence checks (`mushma_occurrence_check_campania_2026`,
`mushma_occurrence_check_lazio_2026`) are those branches' own analyses, cited as their appendices report
them.
