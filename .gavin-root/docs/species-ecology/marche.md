# Species ecology: Marche (regional appendix to species-ecology.md)

Research date: 2026-09-25 (dates Europe/Rome, units metric). Card: region Marche. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to the Marche
(`api/src/api/config/species/marche/`), what changed and why. It covers **fruiting conditions
only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(23 added for the Marche, listed at the end). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every
number is a prior for the backtest; season windows, altitude bands and habitat affinities stay
frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

## Summary

1. **All three groups are kept, with all six keys.** Porcini, ovoli and gallinacci are all on
   record in Marche sources: the regional mycological societies' bulletin (*Micologia nelle
   Marche*, CAMM) makes the "galletto" June's mushroom, the summer porcino July's and the "ovulo
   buono" September's (`camm_calendario2007`), and the regional law bans picking closed ovoli
   (`lr_marche_18_2022`, art. 8.4).
2. **The Marche porcino is mostly the summer one.** Marche mycologists find porcini that are "nella
   stragrande maggioranza dei casi" *B. aestivalis* (= *B. reticulatus*), from about 300 to 1300 m,
   mid-May to October (`camm_santini2007`). *B. edulis* and *B. pinophilus* are present but uncommon
   (`regione_umbria_funghi_tartufi2013`, for the same Umbria-Marche Apennines) and have no Marche
   record online. The chanterelles are mostly not *C. cibarius* s.str. but *C. ferruginascens*,
   which grows on calcareous soil, and *C. subpruinosus* (`camm_angelome2007_cantharellus`,
   `iucn_ferruginascens2025`).
3. **What changed is what the habitat classes hold.** The Marche woods are hop-hornbeam (44 % of the
   wooded area on the grid), downy and Turkey oak (29 %), beech (9 %) and black-pine reforestation
   (7 %); chestnut is only 2.4 %. The black-pine plantations and hop-hornbeam woods sit mostly on
   limestone, where Marche and forager sources report the summer and black porcini but not the
   acid-soil ones. So 18 affinities move, on the classes' Marche contents and on Marche evidence:
   hop-hornbeam up for *B. aereus*, down for *B. edulis* and *B. pinophilus*; black pine down for
   four taxa; beech and deciduous oak up for gallinacci; the small montane-heath and broom-scrub
   classes down for most keys.
4. **One altitude band moves:** *B. reticulatus* stays full to 1300 m (Tuscany 1100 m), because in
   the Marche it fruits in the beech woods up to about 1300 m (`camm_santini2007`,
   `camm_fabrizi2016_faggeta`). The Marche beech belt is Tuscany's ((900)-1000 to 1500-1600 m,
   `ipla_marche_inventario2000`), so every other band is kept.
5. **Season windows and weather rules are all kept.** The Marche records (23 porcini, 7 ovoli, 15
   *Cantharellus* on iNaturalist; almost nothing on GBIF) and the regional pages agree with the
   Tuscan windows. No Marche or central-Apennine study ties fruiting to rain or temperature in
   numbers.
6. **Evidence is thin but regional.** Of the 23 new sources (all opened), 1 is peer-reviewed (and
   not from the Marche), 5 institutional, 1 a national dataset (INFC), 10 from the Marche mycological
   societies (plausible), 4 forager pages (folklore) and 2 our own analyses. The changes rest on the societies' bulletin, the regional
   forest inventory and the REM vegetation map.

## Marche in brief

**Woods on the grid.** The Marche woodland grid (built 2026-09-25 from Regione Marche's REM natural
vegetation map, 1:50,000, edition of March 2019, typed by dominant species;
`mushma_marche_forest_composition_2026`): forest 259,734 ha (INFC 2015: 291,767 ha) on 2,370
woodland cells; woodland elevation median 669 m (5th-95th percentile 337-1,207 m, max 1,724 m);
slope median 22.2° (Tuscany 16.6°); topsoil pH median 6.73 (6.2-7.3). Shares are of the wooded
area (from the region card); elevations are cell elevations weighted by each habitat's share
(computed here from the grid files).

| habitat key | share of wooded area | what it is in the Marche | median elevation (p10-p90) |
|---|---|---|---|
| `mixed_broadleaf` | 44.0 % | hop-hornbeam (*Ostrya carpinifolia*) orno-ostrieti, a little hornbeam, ash, maple | 685 m (418-972) |
| `deciduous_oak` | 29.2 % | downy oak (*Q. pubescens*) and Turkey oak (*Q. cerris*), a few *Q. robur* | 617 m (367-880) |
| `beech` | 9.3 % | *Fagus sylvatica* | 1,181 m (936-1,449) |
| `mountain_pine` | 7.0 % | black-pine (*Pinus nigra*) reforestation, about 16,400 ha | 633 m (363-992) |
| `transitional_woodland_shrub` | 2.5 % | broom (*Spartium*), *Prunus*, *Crataegus*, *Cornus* scrub, elm pre-forest | 665 m |
| `chestnut` | 2.4 % | *Castanea sativa*, about 4,900 ha | 824 m (590-1,023) |
| `evergreen_oak` | 2.3 % | holm oak (Conero, Furlo, Frasassi and Rossa gorges) | 598 m |
| `riparian` | 1.6 % | poplar, willow, alder, elm | 460 m |
| `macchia` | 1.3 % | *Erica arborea*, *Juniperus oxycedrus*, *Ampelodesmos* on the limestone hills | 768 m |
| every other key | ≤ 0.1 % each | Aleppo and stone pine, robinia, fir plantings | |

The regional forest inventory (`ipla_marche_inventario2000`, 256,170 ha, 1:10,000) has the same
picture by category: downy oak 31.7 %, hop-hornbeam 24.1 %, Turkey oak 10.9 %, riparian 8.3 %, beech
7.8 %, reforestation 7.5 %, shrubland 2.8 %, holm oak 2.0 %, **chestnut 1.8 % (4,600 ha)**. INFC 2015
(`infc2015_marche`) gives chestnut 3,706 ha and black and laricio pine 10,377 ha. Chestnut is
Tuscany's commonest porcini and ovoli host; in the Marche it is a minor tree, and oak and
hop-hornbeam carry the thermophilous taxa.

**Altitude belts** (`ipla_marche_inventario2000`):

| type | altitude (m) and where |
|---|---|
| beech | "(900)-1000 e 1500-1600 m"; "diffusamente fino ad 800 m" in the rainy Catria and Laga, single trees to 500-600 m at Fonte Avellana; eutrophic on limestone (about 7,600 ha), mesoneutrophilous on the Laga sandstone (2,200 ha) |
| chestnut | "fra 400 e 1100 m", 300 m at Loro Piceno, 1400 m in the Fluvione valley; calcifuge, on the sandstone "del basso maceratese ed in tutto l'ascolano" (Tronto and Fluvione valleys, Acquasanta Terme, Montegallo), small nuclei between Montemonaco and Amandola, sporadic on limestone (upper Val Nerina, Esanatoglia, Urbania-Sant'Angelo in Vado, Monte Benedetto) |
| Turkey oak | to 1000-1100 m, "insinuandosi nelle Faggete"; on the marly sandstone of Pesaro-Urbino and the submontane belt of the limestone ridges |
| downy oak | hills to 700-800 m in the north, 1250-1300 m on the Sibillini |
| hop-hornbeam | to 1300 m on sunny slopes (Sibillini, upper Val Nerina); has "invaso ex-castagneti da frutto e cedui di faggio submontani" |
| black pine | reforestation, "pino nero d'Austria sui substrati calcarei, e del pino laricio sui substrati mesoneutrofili", largely in the beech belt: Carpegna, Cesane, Furlo, Montiego, Albacina, Cingoli, Fiastrone, Ussita, Visso, Vettore, Montagna dei Fiori |
| silver fir | native relicts only in the Laga (Macera della Morte) and near Fabriano; Bocca Trabaria is a plantation |

Tuscany's beech belt is 900-1700 (1800) m (`rt_tipi_forestali_p4`): the Marche beech belt is the
same, unlike Liguria's.

**Substrate.** Most Marche woods stand on the limestone of the Umbria-Marche ridges; the Laga
flysch (sandstone, "i suoli ... meno basici dell'intera regione") holds the only fruit-chestnut
orchards and the acidophilous beech; the Montefeltro and northern Pesaro-Urbino are on marly
sandstone and clays (`ipla_marche_inventario2000`).

**Climate** (`ogsm_marche_precipitazioni2002`, 102 stations, 1950-2000). Rain rises from the coast
(600-850 mm a year, the south coast 550-650 mm) through the hills (850-1100 mm) to the mountains
(over 1100 mm), with maxima on Monte Catria (1550-1700 mm) and the Sibillini (1500-1550 mm).
Autumn is the wettest season (315-480 mm in the mountains), summer the driest (195-285 mm in the
mountains, 105-165 mm on the coast), with the minimum in July-August.

**Regional law.** L.R. 18/2022 (in force from 1 January 2023, modified by L.R. 10/2026; it
repealed L.R. 17/2001): 3 kg per person per day for all species together, no picking of "amanita
caesarea allo stato di ovulo chiuso" or of *Boletus* with a cap under 3 cm, rules in protected areas
left to the park bodies, no fixed closed days or altitude limits (`lr_marche_18_2022`). None of it
changes where or when the fungi fruit; it confirms the ovolo as a regional species.

## Occurrence cross-check (Marche)

Queried 2026-09-25 (`mushma_occurrence_check_marche_2026`): GBIF with `gadmGid=ITA.11_1`
(soil-DNA `MATERIAL_SAMPLE` rows excluded), iNaturalist place 7029 (verifiable), elevations from
the Open-Meteo elevation API for open, accurate (≤ 1 km) iNaturalist records only. Aggregates only;
no coordinates are stored. Enrichment = the taxon's monthly share of its records ÷ the monthly
share of all 2,859 Marche iNaturalist fungi records (> 1: over-represented for the effort). The
histograms include 2026 to date.

| taxon | source | n | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | GBIF / iNat | 0 / 0 | | | | | | | | | | | | |
| *B. reticulatus* | GBIF | 2 | | | | | | | | | 2 | | | |
| | iNat | 15 | | | | | | 3 | 2 | | 8 | 2 | | |
| *B. aereus* | GBIF / iNat | 0 / 8 | | | | | | | | | 5 | 3 | | |
| *B. pinophilus* | GBIF / iNat | 0 / 0 | | | | | | | | | | | | |
| four porcini | iNat enrichment | 23 | | | | | | 2.7 | 2.2 | | 4.3 | 1.1 | | |
| *A. caesarea* | GBIF / iNat | 0 / 7 | | | | | | | | | 5 | 2 | | |
| | iNat enrichment | | | | | | | | | | 5.5 | 1.5 | | |
| *Cantharellus* (genus) | GBIF | 1 | | | | | | | | | | 1 | | |
| | iNat | 15 | 1 | | | | 2 | 7 | | | 2 | 2 | 1 | |
| | iNat enrichment | | 1.0 | | | | 1.7 | 9.7 | | | 1.0 | 0.7 | 0.3 | |

The Marche is thinly recorded: 2,859 iNaturalist fungi records against Liguria's 5,132, and every
porcini, ovolo and chanterelle record is from 2019 or later (most from 2023). Most of them are
obscured by their observers (13 of 15 *B. reticulatus*, 6 of 8 *B. aereus*, all 7 ovoli, 13 of 15
*Cantharellus*), so only a handful have usable elevations: *B. reticulatus* 823 and 986 m, *B.
aereus* 828 and 848 m, one *Cantharellus* at 190 m, no ovolo. They can confirm the months, not tune
anything. The sightings backtest will have very few Marche presences.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Which porcino** (plausible). "Nelle nostre zone rinveniamo porcini, che nella stragrande
  maggioranza dei casi sono B. aestivalis, da circa 300 m. s.l.m. a circa 1.300 m. s.l.m. nel
  periodo che va dalla metà di maggio sino a tutto settembre e parte di ottobre, con ovvie soste nei
  periodo di maggior secco" (`camm_santini2007`). For the same Apennines, *B. edulis* is "Poco comune
  in Umbria. Spesso viene confuso con Boletus aestivalis ... molto comune" and *B. pinophilus* "non è
  comune" (`regione_umbria_funghi_tartufi2013`). The Metauro valley database lists *B. aereus* and
  *B. aestivalis* at its sites (Cesane, Nerone, Catria, Bocca Trabaria), never *B. edulis* or *B.
  pinophilus* (`lavalledelmetauro_funghi`).
- **Hosts** (plausible). Marche mycologists: *B. aestivalis* "in boschi caldi con presenza di
  quercia, faggio, carpino nero in particolare nel periodo estivo"; *B. aereus* "in boschi termofili
  di latifoglie come cerro, castagno, carpino nero"; *B. pinophilus* with spruce and beech on
  "terreni molto acidi"; *B. edulis* with beech and fir, "ambienti freschi e umidi"
  (`camm_massi_polidori2022`). The habitat series lists *B. reticulatus* among the typical fungi of
  Marche beech and chestnut woods, *B. aereus* of Turkey-oak and chestnut woods
  (`camm_fabrizi2016_faggeta`, `camm_fabrizi2016_cerreta`, `camm_fabrizi2017_castagneto`); the
  Sibillini group puts *B. aereus* in the hill Turkey-oak woods "già dopo le piogge settembrine"
  (`camm_carassai2016`).
- **Hop-hornbeam** (folklore to plausible). A forager magazine: in hop-hornbeam woods "sono spesso
  presenti il Boletus reticulatus (estatino) e il Boletus aereus (porcino nero). Risultano invece
  quasi sempre assenti, o comunque molto rari nei contesti calcarei, i Porcini più legati a suoli
  acidi come Boletus edulis e Boletus pinophilus" (`funghimagazine_carpino_nero2026`); no *B.
  pinophilus* "tra i Carpini" (`funghimagazine_alberi_porcini`). *Ostrya* is an ectomycorrhizal
  host with mainly non-specific partners (`mrak2025_mycorrhiza`, Karst).
- **Black-pine reforestation** (plausible, by absence). The Sibillini group's autumn guide ends in
  "le pinete collinari realizzate principalmente con rimboschimenti di pino nero", and lists
  *Lactarius*, *Craterellus lutescens* and *Suillus* there, no porcini (`camm_carassai2016`); the
  Cesane (black pine on limestone, soils pH > 7) have no section-*Boletus* porcini in the Metauro
  lists. Planted *P. nigra* in the Karst held the fewest ectomycorrhizal partners, mostly
  conifer-specific (`mrak2025_mycorrhiza`). Against this: the Borgotaro IGP names "pino nero" among
  its eligible woods (`borgotaro_igp_2014`), and a forager magazine names *B. reticulatus*, *B.
  pinophilus* and (rarely) *B. edulis* under black pine (`funghimagazine_alberi_porcini`).
- **Season** (plausible / folklore). The Sibillini sequence: "All'inizio di settembre le fresche
  faggete ... seguite poi dai castagneti, in ottobre ... i boschi termofili di Cerro ... a novembre
  inoltrato nelle pinete collinari", after "le prime consistenti piogge di inizio settembre" when
  the summer was hot (`camm_carassai2016`). *B. pinophilus* "dalla primavera sino alle prime
  gelate invernali, quasi assente nel periodo estivo" (`camm_massi_polidori2022`); on the Laga it
  "apre e chiude la stagione" (`altotronto_porcini2017`, folklore). Forager page: porcino nero July
  to late September, porcino rosso September to early November, *B. edulis* late September to late
  October (`cacciatoridifunghi_marche2023`, folklore).

**Decisions.**

| key | factor | Tuscany | Marche | why | confidence |
|---|---|---|---|---|---|
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | here almost pure hop-hornbeam on limestone; Marche mycologists name carpino nero for the summer and black porcini, not this one; "quasi sempre assenti" in calcareous hop-hornbeam (magazine) | plausible (weak) |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.1** | black-pine plantations on limestone; no Marche report of porcini there; few, conifer-specific partners; the IGP eligibility is the only support | plausible (weak) |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | broom, *Prunus* and *Crataegus* scrub, no host | plausible |
| *reticulatus* | altitude | 0 → 150 … 1100 → 1500 | 0 → 150 … **1300 → 1600** | Marche porcini, mostly this taxon, "da circa 300 ... a circa 1.300 m"; typical of Marche beech woods | plausible |
| *reticulatus* | habitat `mountain_pine` | 0.6 | **0.3** | black-pine plantations, no Marche report; a magazine names it under black pine | plausible (weak) |
| *reticulatus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | broom scrub, oaks only at its edges | plausible |
| *aereus* | habitat `mixed_broadleaf` | 0.3 | **0.6** | hop-hornbeam named as a host by Marche mycologists ("cerro, castagno, carpino nero") | plausible |
| *aereus* | habitat `macchia` | 1.0 | **0.6** | montane *Erica arborea*-juniper-*Ampelodesmos* heath on limestone, without the *Cistus*, *Arbutus* and holm oak of Tuscan macchia | plausible (weak) |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | broom scrub | plausible |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **0.3** | black pine on limestone; wants "terreni molto acidi"; no Marche report; named under black pine by a magazine | plausible (weak) |
| *pinophilus* | habitat `mixed_broadleaf` | 0.3 | **0.1** | calcareous hop-hornbeam; no record "tra i Carpini" (magazine) | folklore to plausible |
| *pinophilus* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | broom scrub | plausible |
| all four | season, weather, stoppers, growth clock | — | kept | records and pages agree; no regional numbers | as Tuscany |

Kept on purpose: *B. reticulatus* `mixed_broadleaf` 0.6 and beech 0.6 (now with Marche support;
0.6 already gives full credit on any cell that is half hop-hornbeam or beech); *B. edulis* and *B.
pinophilus* altitude bands (the Marche beech belt is Tuscany's); *B. aereus* altitude …800 → 1250
(its hosts reach 1100-1400 m here and the Metauro database lists it on Nerone and Catria, but no
source places it higher; the two located records are at 828-848 m, on the upper ramp); deciduous
oak and chestnut as hosts for *reticulatus* and *aereus* (Turkey-oak and chestnut woods in every
Marche source). With the saturating habitat response, the *edulis* and *pinophilus* changes are
the ones that bite: on the Marche grid their habitat gate reaches full credit on 26 % and 30 % of
woodland cells, against 79 % with the Tuscan affinities, while *reticulatus* (full on 99 %) and
*aereus* (89 %) keep the porcini group's reach.

## Ovoli (*Amanita caesarea*)

**Regional evidence.** Presence: the regional law's ovolo rule (`lr_marche_18_2022`), September's
mushroom in the Marche societies' calendar (`camm_calendario2007`), a typical fungus of Marche
Turkey-oak woods "soprattutto nel periodo autunnale dopo abbondanti piogge e assenza di vento"
(`camm_fabrizi2016_cerreta`) and of chestnut woods "nel periodo estivo-autunnale"
(`camm_fabrizi2017_castagneto`); the "ovolo buono, cocchi" of the Sibillini chestnut woods
(`camm_carassai2016`); in the hill woods "con prevalenza di querce, castagno e carpino" up to about
600 m (`camm_para2008`); "boschi caldi di castagni e querce ... Più frequente in terreno siliceo.
Estate-autunno", photographed in a Turkey-oak wood in October 2012 (`lavalledelmetauro_funghi`).
For the same Apennines: "in boschi di castagno, cerro e roverella, ad altitudini inferiori agli
800/900 m" (`regione_umbria_funghi_tartufi2013`). Records: 7 iNaturalist (September 5, October 2;
5.5× the effort in September), none with a usable location.

**Decisions.**

| factor | Tuscany | Marche | why | confidence |
|---|---|---|---|---|
| habitat `macchia` | 0.3 | **0.1** | montane heath without the scattered holm and cork oak that made Tuscan macchia marginal | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | broom scrub, not heath and clearings with oaks | plausible |
| habitat `mixed_broadleaf` 0.3 | — | kept | hop-hornbeam is not named as a host, but oak is its usual companion and the Marche hill woods "di querce, castagno e carpino" hold ovoli | plausible |
| habitat deciduous oak, chestnut 1.0 | — | kept | every Marche source; with chestnut at 2.4 %, oak carries the ovolo here | strong (hosts) |
| season 01-06 → 01-09 … 05-11 → 30-11 | — | kept | September peak in the records and the calendar, autumn after heavy rain | plausible |
| altitude … 750 → 1100 | — | kept | "inferiori agli 800/900 m" | plausible |
| weather rules | — | kept | no regional numbers | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "galletti, gallucci, finferli")

**Regional evidence.** The Marche review of the genus (`camm_angelome2007_cantharellus`): *C.
cibarius* s.str. "sotto latifoglie, estate-autunno ... Nelle Marche è una specie poco frequente"
(a collection at Faete di Arquata del Tronto); *C. ferruginascens* "la specie di Cantharellus più
comune nelle nostre zone"; *C. subpruinosus* under chestnut (Pievebovigliana), *C. amethysteus*
under holm oak (Abbadia di Fiastra, Tolentino), all "sotto latifoglie, primavera-autunno". *C.
ferruginascens* grows with *Fagus*, *Quercus*, *Castanea* and *Carpinus* "on calcareous soil" in
temperate areas (`iucn_ferruginascens2025`). *C. subpruinosus* "fruttifica fino a tutto settembre,
abbastanza comune nelle faggete dei Sibillini" (`camm_carassai2016`); *C. pallens* is a typical
fungus of Marche beech, Turkey-oak and chestnut woods (`camm_fabrizi2016_faggeta`,
`camm_fabrizi2016_cerreta`, `camm_fabrizi2017_castagneto`). A forager magazine finds finferli
"spesso scarsi o assenti" in calcareous hop-hornbeam woods (`funghimagazine_carpino_nero2026`,
folklore), and the Sibillini black-pine plantations yield *Craterellus lutescens*, not
*Cantharellus* (`camm_carassai2016`). Records: 15 iNaturalist and 1 GBIF, with a strong June mode
(7 records, 9.7× the effort; the calendar's "galletto" month, `camm_calendario2007`).

**Decisions.**

| factor | Tuscany | Marche | why | confidence |
|---|---|---|---|---|
| habitat beech | 0.6 | **1.0** | *C. subpruinosus* "abbastanza comune nelle faggete dei Sibillini"; *C. pallens* typical of Marche beech; *C. ferruginascens* with *Fagus* | plausible |
| habitat deciduous oak | 0.3 | **0.6** | *C. pallens* typical of Marche Turkey-oak woods; the commonest Marche species grows with oak on calcareous soil, so Tuscany's calcareous-plot reading undersells it | plausible |
| habitat `mountain_pine` | 0.3 | **0.1** | black pine on limestone; *Craterellus*, not *Cantharellus*, reported there | plausible (weak) |
| habitat `macchia` | 0.3 | **0.1** | montane heath with no Fagaceae host | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.3 | **0.1** | broom scrub, no host | plausible |
| habitat `mixed_broadleaf` 0.3 | — | kept | "scarsi o assenti" on calcareous hop-hornbeam (magazine) against *C. ferruginascens* with *Carpinus* on calcareous soil (IUCN); 0.3 already gives a pure cell full credit | plausible |
| season (lowland wraps to 25-01; mountain 01-06 → 15-11) | — | kept | June mode and autumn tail in the records; June in the calendar; "fino a tutto settembre" in the Sibillini beech | plausible |
| altitude … 1000 → 1700 | — | kept | Sibillini beech woods inside the ramp | plausible |
| soil pH, lithology | disabled | kept disabled | the commonest Marche species is calcicolous; Marche woodland topsoil pH 6.2-7.3; an acid-soil gate would cut most of the region | plausible |
| weather rules | — | kept | no regional numbers | as Tuscany |

## Weather rules: why none changed

- **Rain amount and lag.** No Marche, Umbrian or Abruzzese source gives a rain amount or lag for any
  of the three groups. The Marche sources are qualitative and agree with the Tuscan rules: "le prime
  consistenti piogge di inizio settembre" after a hot summer start the season
  (`camm_carassai2016`), fungi come "dopo abbondanti piogge e assenza di vento"
  (`camm_fabrizi2016_cerreta`), porcini "una o due settimane" after gentle, steady rain
  (`altotronto_porcini2017`, folklore). The Tuscan rules (Amiata lag, national lore) stay.
- **Drying wind.** The "assenza di vento" and the Laga page's "forte vento secco per più giorni" are
  cited on the porcini drying stoppers; the ET0 proxy and its numbers are unchanged.
- **Temperature.** "i Porcini nascono di solito se la temperatura non è scesa sotto i 15°C per
  troppo tempo" (`altotronto_porcini2017`) is lore without a window or variable; the air-temperature
  bands and the growth clock already slow fruiting in cool spells.
- **Rain climate.** The Marche mountains are as wet as the Tuscan ones (Catria 1550-1700 mm,
  Sibillini 1500-1550 mm), the Adriatic hills drier (`ogsm_marche_precipitazioni2002`). The porcini
  30-day rain is scored against each cell's own normal, so it adapts; the absolute 30-day ramps of
  ovoli (25 → 75 mm) and gallinacci (15 → 70 mm) will be full less often in the dry low hills,
  which is where the records are fewest.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it on
  Marche gauges is a region-config task, not a species one.

## Sanity contrasts

`marche/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written down
before any Marche score existed (none had been computed on 2026-09-25).

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_` (read those with `--group ovoli` / `--group gallinacci`). "Normal" is the area's mean
over 2017–2025. 12 contrasts: 8 porcini, 2 ovoli, 2 gallinacci; press research on 2026-09-25, every
cited page opened and its quote checked. Areas: `laga` (Acquasanta Terme, Arquata del Tronto; 197
woodland cells), `laga_montegallo` (plus Montegallo; 240), `catria_nerone` (Cagli, Cantiano,
Frontone, Serra Sant'Abbondio, Apecchio, Piobbico, Acqualagna; 368), `southern_marche` (provinces
MC, FM, AP; 1,267) and `marche` (the whole region; 2,370). Comuni names checked against the ISTAT
2025 list and the Marche grid.

**The sources are thin, and mostly one blog.** Marche local press rarely reports how a mushroom
season went. The best-dated source is Bruno de Ruvo's forager blog (*Funghi Teramani*, then *A
spasso tra le nuvole*), which reports the Laga woods of the Teramo side (the Ceppo in Rocca Santa
Maria, Valle Castellana). Valle Castellana borders Acquasanta Terme, and in September 2019 the blog
and the Ascoli press (Cronache Picene) describe the same flush on both sides. Its contrasts are read
onto the Marche side of the massif, which is the main weakness of seven of the twelve.

| id | group | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|---|
| `laga_montegallo_2019_2017` | porcini | Laga + Montegallo 2019, 2–9 Sep | same, 2017 | [Cronache Picene 2019-09-09](https://www.cronachepicene.it/2019/09/09/funghi-raccolta-boom-nel-piceno-e-la-vendemmia-dei-porcini/147166/) ([Funghi Teramani 2019-09-05](https://funghiteramani.blogspot.com/2019/09/oramai-lo-sanno-anche-le.html); 2017: [2017-08-09](https://funghiteramani.blogspot.com/2017/08/2017-stagione-finita.html), [2017-09-14](https://funghiteramani.blogspot.com/2017/09/la-pioggia-e-arrivatae-adesso.html)) | the 2017 side is the Abruzzo slope only |
| `laga_2016_2017_turn_of_october` | porcini | Laga 2016, 25 Sep–10 Oct | same, 2017 | [Funghi Teramani 2016-10-03](https://funghiteramani.blogspot.com/2016/10/aggiornamento-del-0210il-clou-dei.html) ([2016-10-10](https://funghiteramani.blogspot.com/2016/10/aggiornamento-del-1010si-va-verso-il.html); [2017-10-02](https://funghiteramani.blogspot.com/2017/10/savo-quasi-per-dirvi.html), [2017-11-02](https://funghiteramani.blogspot.com/2017/11/e-finita.html)) | one blogger, Abruzzo side; the Ceppo beech woods |
| `laga_july_2016_2017` | porcini (summer) | Laga 2016, 1–20 Jul | same, 2017 | [Funghi Teramani 2016-07-04](https://funghiteramani.blogspot.com/2016/07/aggiornamento-dinizio-lugliotantissimi.html) ([2017-07-12](https://funghiteramani.blogspot.com/2017/07/stop-ai-funghisecondo-aggiornamento-di.html), [2017-07-21](https://funghiteramani.blogspot.com/2017/07/il-gran-seccoterzo-aggiornamento-di.html)) | one blogger, Abruzzo side |
| `laga_august_2018_2017` | porcini | Laga 2018, 15–31 Aug | same, 2017 | [Funghi Teramani 2018-08-21](https://funghiteramani.blogspot.com/2018/08/quarto-aggiornamento-di-agostoporcini.html) ([2017-08-09](https://funghiteramani.blogspot.com/2017/08/2017-stagione-finita.html)) | one blogger, Abruzzo side; 2017 shares its lower side with two other contrasts |
| `laga_2024_2020_late_august` | porcini | Laga 2024, 28 Aug–6 Sep | same, 2020 | [A spasso tra le nuvole 2024-09-02](https://www.aspassotralenuvole.it/post/cosa-succede-nei-nostri-boschi) ([Funghi Teramani 2020-08-24](https://funghiteramani.blogspot.com/2020/08/e-arrivata-lacqua.html), [2020-09-11](https://funghiteramani.blogspot.com/2020/09/pare-che-ci-siamo.html); [Funghi Magazine 2024-08-30](https://funghimagazine.it/aggioramento-funghi-e-porcini-30-08-2024/): "Buone nascite ... dai monti di confine tra Marche-Umbria-Lazio") | the 2020 side is inferred: dry to 24 August, first flush reported on 11 September |
| `laga_2025_timing` | porcini | Laga 2025, 8–20 Sep | same year, 1–12 Oct | [A spasso tra le nuvole 2025-10-11](https://www.aspassotralenuvole.it/post/game-over) ([2025-09-14](https://www.aspassotralenuvole.it/post/siamo-al-clou-della-stagione)) | Abruzzo side; the season gate slightly favours September (*B. reticulatus* ramps down from 30 Sep) |
| `catria_vs_southern_marche_2021` | porcini | Catria-Nerone 2021, 1–12 Sep | provinces MC, FM, AP, same window | [Funghi Magazine 2021-09-10](https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/) (reader report of 2021-09-07 on [FM 2021-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/); Corriere Adriatico 2021-09-10, not re-checked, see below) | national bulletin; "meglio al confine tra Marche ed Umbria" sits in its Umbria paragraph; the Catria side rests on the unchecked Corriere Adriatico piece |
| `marche_october_2022` | porcini | whole region 2022, 5–25 Oct | same, normal | [Funghi Magazine 2022-10-13](https://funghimagazine.it/meteo-funghi-13-10-2022/) ([FM 2022-10-28](https://funghimagazine.it/aggiornamento-porcini-28-10-2022/), reply of 2022-10-30: "bell'annata veramente per le Marche") | national bulletin, region-wide, lists the Marche with seven other regions |
| `ovoli_laga_2024` | ovoli | Laga 2024, 25 Aug–6 Sep | same, normal | [A spasso tra le nuvole 2024-09-02](https://www.aspassotralenuvole.it/post/cosa-succede-nei-nostri-boschi) ([Funghi Teramani, same text](https://funghiteramani.blogspot.com/2024/09/cosa-succede-sulle-nostre-montagne.html)) | one blogger, Abruzzo side; "normal" includes 2024 |
| `ovoli_laga_2020_timing` | ovoli | Laga 2020, 7–15 Sep | same year, 5–24 Aug | [Funghi Teramani 2020-09-11](https://funghiteramani.blogspot.com/2020/09/pare-che-ci-siamo.html) ([2020-08-24](https://funghiteramani.blogspot.com/2020/08/e-arrivata-lacqua.html)) | Abruzzo side; the August side is about drought, not observed absence of ovoli; the season gate favours September a little (0.7–0.9 in August) |
| `gallinacci_laga_june_2016_2025` | gallinacci | Laga 2016, 8–20 Jun | same, 2025 | [Funghi Teramani 2016-06-13](https://funghiteramani.blogspot.com/2016/06/aggiornamento-del-12-giugnoancora-acqua.html) ([2016-06-10](https://funghiteramani.blogspot.com/2016/06/ci-si-comincia-divertire-nel-bosco.html); [A spasso tra le nuvole 2025-06-16](https://www.aspassotralenuvole.it/post/a-breve-porcini)) | one blogger, Abruzzo side |
| `gallinacci_marche_june_2022_2024` | gallinacci | whole region 2022, 20–30 Jun | same, 2024 | [Funghi Magazine 2022-07-01](https://funghimagazine.it/molti-porcini-a-breve-vediamo-dove-01-07-2022/) ([FM 2024-06-14](https://funghimagazine.it/aggiornamento-funghi-14-06-2024/), [FM 2024-06-28](https://funghimagazine.it/aggiornamento-funghi-28-06-2024/)) | national bulletin; "dalle Marche al Molise" in 2022 and "Umbria e Marche" in 2024 |

**Outlets that block AI agents.** Il Resto del Carlino, Corriere Adriatico, ANSA and AnconaToday
disallow AI crawlers in their robots.txt. The research agent opened some of their pages before it
noticed. None of them is a main source here, and nothing from them was re-fetched. Corriere
Adriatico 2021-09-10 (the Catria-Nerone side of `catria_vs_southern_marche_2021`) is named as an
unchecked second source; someone should check it by hand.

Candidates left out:
- Montegallo against the Lago di Gerosa area, early September 2022 (Carlino only).
- Early September 2022 dry against a good October (the dry side is Carlino only). The CAMM
  bulletin's "tutto secco" of October 2022 was written in the summer, just after the new law.
- Piceno early September 2019 against 2020 (the 2020 side is region-wide and conflicts with the
  Laga blog's productive warm woods on 11 September 2020).
- Laga late September 2016 against 2023 (A spasso tra le nuvole calls 2023 "E' secco ... ad
  ottobre", but Funghi Magazine of 12 October 2023 has "ancora buone le nascite di Porcini sul Gran
  Sasso e Monti della Laga").
- Species-count proxies from the mycological exhibitions: Fabriano 2019 vs 2023, San Sisto
  (Montefeltro) 2018 vs 2025, Montottone 2019 vs 2023. They measure all fungi, the counts are made
  differently, and two of them rest on blocked outlets.
- Funghi Magazine's August 2023 and September-October 2024 region-wide statements (they contradict
  each other, or the seasonal gate alone would decide them).
- Single giant-porcino stories (Catria 2019, Sant'Angelo in Vado 2019, Serra Sant'Abbondio and
  Cingoli 2021).

**Year picture from the sources** (for context, not scored):
- 2016: very good on the Laga (summer and the turn of October).
- 2017: disastrous. Drought from June to October on the Laga and in the Montefeltro.
- 2018: good late August on the Laga; poor late September in the Montefeltro.
- 2019: a historic early-September flush in the Piceno chestnut and oak woods, then a dry October.
- 2020: dry August, a flush in the warm woods from about 7 September, poor mid-September to early
  October region-wide.
- 2021: good early September on Catria-Nerone, nothing in the south; good late October in the
  inner hills.
- 2022: finferli in late June, a dry summer, a very good October.
- 2023: a short flush after the first rain, then a dry late September and October.
- 2024: poor June; a huge late-August flush on the Laga, ovoli included.
- 2025: nothing in June and July; a beech flush in mid-September; over by early October after a
  cold week.

## Open questions

- **Black pine and hop-hornbeam.** Together 51 % of the Marche woods, and the evidence for or
  against porcini in them is an absence in Marche lists, one Karst study and forager magazines. A
  Marche record set with locations (the societies' exhibition records, AST mycological
  inspectorates) would settle it better than any page.
- **Slope and sun exposure.** Both stoppers were anchored on Tuscan grid percentiles. Marche woods
  are steeper (median 22.2°, 32 % of cells over 25°), but the slope stopper's mean over woodland
  cells is 0.984 (p10 0.937; Tuscany 0.994), as in Liguria, so it was left alone.
- **Substrate.** Ovoli prefer siliceous ground, gallinacci split (*C. ferruginascens* calcicolous,
  *C. cibarius* s.str. and *C. subpruinosus* acidophilous), and the Marche woods are mostly on
  limestone with the Laga sandstone as the exception. The REM map carries no substrate, the IPLA
  types do (eutrophic vs mesoneutrophilous beech); a lithology layer would let the disabled rules
  be tested.
- **B. aereus altitude.** Its Marche hosts reach 1100-1400 m and it is listed on Nerone, Catria and
  at Bocca Trabaria; the band's zero at 1250 m may be low here. Frozen for this backtest.
- **Few records.** 45 iNaturalist records for the three groups, most obscured; the backtest will
  say little about the Marche. The earthquake closures of 2016-2017 in the Sibillini and Laga thin
  the sightings there (not the scores).
- **Leads not read:** "I tipi forestali delle Marche" (IPLA 2001, the published book); ISPRA
  Siniscalco et al. (2014) on matching Italian macrofungi to habitat classes; the Metauro
  database's other species cards; the Umbrian macrofungi inventories by Angelini et al. (snippet
  only).

## References added for the Marche

| id | kind | verified | used for |
|---|---|---|---|
| `ipla_marche_inventario2000` | institutional | verified | forest categories, altitude belts, substrates, chestnut and black-pine localities |
| `infc2015_marche` | dataset | verified | forest area and category areas (chestnut, black pine) |
| `lr_marche_18_2022` | institutional | verified | ovolo and *Boletus* picking rules (presence); repeal of L.R. 17/2001 |
| `ogsm_marche_precipitazioni2002` | institutional | verified | Marche rain climatology |
| `regione_umbria_funghi_tartufi2013` | institutional | verified | per-taxon frequency, hosts, months and ovolo altitude on the Umbria-Marche Apennines |
| `iucn_ferruginascens2025` | institutional | verified | hosts and calcareous soil of the commonest Marche chanterelle |
| `mrak2025_mycorrhiza` | peer-reviewed | verified | hop-hornbeam as a host; planted black pine's few, conifer-specific partners |
| `camm_santini2007` | society | verified | *B. aestivalis* as the main Marche porcino, 300-1300 m, mid-May to October |
| `camm_angelome2007_cantharellus` | society | verified | the Marche *Cantharellus* species and their hosts |
| `camm_calendario2007` | society | verified | the month of galletto, porcino and ovolo |
| `camm_carassai2016` | society | verified | Sibillini season sequence, hosts, black-pine plantations without porcini |
| `camm_fabrizi2016_faggeta` | society | verified | Marche beech belt and its fungi |
| `camm_fabrizi2016_cerreta` | society | verified | Turkey-oak fungi; "dopo abbondanti piogge e assenza di vento" |
| `camm_fabrizi2017_castagneto` | society | verified | where the Marche chestnut woods are and their fungi |
| `camm_massi_polidori2022` | society | verified | per-taxon porcini hosts, incl. hop-hornbeam; *B. pinophilus* season |
| `camm_para2008` | society | verified | ovolo and *B. aereus* in the hill oak, chestnut and hornbeam woods |
| `lavalledelmetauro_funghi` | society | verified | Pesaro-Urbino occurrences, hosts and months of *B. aereus*, *B. aestivalis*, ovolo |
| `altotronto_porcini2017` | web | verified | taxa by belt on the Laga; rain, temperature and wind lore (folklore) |
| `cacciatoridifunghi_marche2023` | web | verified | porcini months (folklore) |
| `funghimagazine_alberi_porcini` | web | verified | porcini under black pine and hornbeams (folklore) |
| `funghimagazine_carpino_nero2026` | web | verified | porcini and finferli in calcareous hop-hornbeam woods (folklore) |
| `mushma_marche_forest_composition_2026` | analysis | verified | habitat shares and elevations on the Marche grid (REM map) |
| `mushma_occurrence_check_marche_2026` | analysis | verified | month counts, enrichment, located elevations |

Existing references the Marche changes lean on: `borgotaro_igp_2014` (IGP host list, "pino nero",
"carpino"), `rt_tipi_forestali_p4` (Tuscan beech belt, for comparison), `iucn_caesarea2019` and
`lagana1999_czech_mycol` (ovolo and chanterelle hosts and substrate).
