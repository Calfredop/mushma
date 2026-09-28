# Species ecology: Abruzzo (regional appendix to species-ecology.md)

Research date: 2026-09-26 (dates Europe/Rome, units metric). Card: `region-abruzzo-species.md`
(child of `region-abruzzo.md`). Rule files: `api/src/api/config/species/abruzzo/`. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Abruzzo, what
changed and why. It covers **fruiting conditions only**: nothing here is about edibility or
identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(8 added for Abruzzo, in one block at the end of the file, listed at the end of this page). Confidence
levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**, **plausible**,
**folklore**. Every number is a prior for the backtest; season windows, altitude bands and habitat
affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

## Summary

1. **All three groups and all six keys are kept.** Porcini, ovoli and gallinacci are all on record in
   Abruzzo: the Abruzzo mycologists' book has cards for *B. edulis*, *B. aestivalis* (=
   *reticulatus*), *B. aereus*, the ovolo and the chanterelle, each photographed in an Abruzzo wood
   (`amep_funghi_abruzzo_tieri`); a forager blog on the Teramo side of the Laga reports all four
   porcini ("il poker"), ovoli and "gallucci" season after season (`funghiteramani_blog`); the
   regional law sets a minimum size for porcini and bans picking the closed ovolo
   (`lr_abruzzo_34_2006`, art. 2); iNaturalist holds records of all six keys
   (`mushma_occurrence_check_abruzzo_2026`). Nothing is dropped.
2. **Abruzzo is a beech region, and it is high.** Beech is 31 % of the woods on the regional forest-type map and
   runs from about 1,000 m to the tree line (map median 1,385 m, p90 1,682 m, p99 1,824 m;
   `regione_abruzzo_ctf2009`, `mushma_abruzzo_forest_composition_2026`); the tree line passes 2,000 m
   on some central Apennine peaks (`bonanomi2020_treeline`). Half of the woodland cells on the grid
   are above 1,061 m, against 669 m in the Marche. So **five altitude bands move up** (only *B. aereus* keeps Tuscany's): *B. edulis* and
   *B. pinophilus* full to 1,800 m and zero at 2,000 m (Tuscany 1,600 → 1,900); *B. reticulatus* full
   to 1,500 m, zero at 1,800 m (Tuscany 1,100 → 1,500); gallinacci full to 1,400 m, zero at 1,900 m
   (Tuscany 1,000 → 1,700); and the ovolo full to 900 m, zero at 1,200 m (Tuscany 750 → 1,100),
   because its chestnut and Turkey-oak hosts sit higher here too.
3. **Two season windows move, on the Laga sequence.** The forager blog gives a dated, repeated
   sequence for the Laga: gallucci from early May under Turkey oak and chestnut, then summer porcini,
   then the "rossi" and the chanterelles in the beech, black porcini and ovoli with the summer heat,
   *B. edulis* in the beech from August, best late September. The ovolo now reaches full season from
   1 August (Tuscany 1 September), and the gallinacci mountain window ramps up 15 May → 15 June
   (Tuscany 1 June → 1 July). The porcini windows fit the sequence and are kept.
4. **What the habitat classes hold changes 17 affinities.** As the grid reads the regional map,
   Abruzzo's `macchia` is Juniperus oxycedrus scrub of the oak belt (2 % of the woods), not
   Mediterranean macchia; `mountain_pine` is black-pine reforestation (6.7 %); `mixed_broadleaf` is
   hop-hornbeam and the maples, ash and cherry that invade old fields (16.5 %);
   `transitional_woodland_shrub` is rose, bramble, broom and badland scrub. These move down for most
   keys. Beech becomes a full chanterelle
   host and a marginal black-porcino host, deciduous oak a secondary chanterelle host.
5. **Weather rules are all Tuscany's.** No Abruzzo study ties fruiting to rain or temperature in
   numbers. The Laga blog's lore (rain, then heat and no wind; drying wind wastes a rain; cold nights
   slow the flush) agrees with the Tuscan rules. The slope stopper was checked on the Abruzzo grid and
   left alone.
6. **Evidence is regional but thin.** Of the 8 new sources (all opened), 1 is peer-reviewed (the
   beech tree line), 2 institutional (the regional forest-type map's type sheets, the picking law), 1
   from an Abruzzo mycological society, 2 forager or company pages (folklore) and 2 our own analyses.
   Abruzzo has only 2,792 iNaturalist fungi records and 31 for the six keys, 18 of them from around
   one coastal wood. The changes rest on the regional forest map, the society's book and one forager's
   ten years of dated updates on the Laga.

## Abruzzo in brief

**Woods.** The grid reads the regional Carta Tipologico-Forestale (1:25,000, 2009, 33 forest and
shrub types; CC BY-NC 3.0, accepted on 2026-09-28), with the class mapping in
`api/src/api/config/regions/abruzzo.yaml` (`regions/abruzzo.md`). The type sheets of the map
(`regione_abruzzo_ctf2009`) and its polygons (`mushma_abruzzo_forest_composition_2026`) say what each
habitat key holds in Abruzzo. Areas and shares are of the 432,041 ha of woods and scrub the grid keeps
(the map has 454,254 ha; the montane juniper scrub and the mugo krummholz are left out, below);
elevations are area-weighted, from the Copernicus DEM at each polygon's representative point.

| habitat key | Abruzzo forest types (map area) | share | elevation p10 / median / p90 |
|---|---|---|---|
| `beech` | Faggeta montana (93,774 ha), Faggeta termofila e basso montana (29,925), Faggeta altomontana rupestre (11,648) | 31.3 % | 1,162 / 1,385 / 1,682 m |
| `deciduous_oak` | downy oak: Querceto di roverella mesoxerofilo (66,703), pioniero (14,888), tipico (8,204); Turkey oak: Cerreta mesofila (17,763), mesoxerofila (15,849) | 28.6 % | 356 / 775 / 1,115 m |
| `mixed_broadleaf` | hop-hornbeam: Ostrieto mesoxerofilo (21,973), mesofilo (11,352), Orno-ostrieto pioniero (8,183); Latifoglie di invasione miste e varie (maples, ash, cherry, walnut on old fields, 29,206); aspen woods (708); Boschi di forra (9) | 16.5 % | 373 / 890 / 1,209 m |
| `macchia` | Juniperus oxycedrus scrub "della fascia dei querceti e degli orno-ostrieti" (Arbusteto a prevalenza di ginepri mesoxerofili, 8,728); Mediterranean macchia (6 ha) | 2.0 % | 606 / 873 / 1,084 m |
| `mountain_pine` | conifer reforestation "nella fascia altocollinare e submontana" (18,978, mostly black pine) and "nella fascia montana" (9,712, black pine, silver and Greek fir, spruce, larch, Douglas fir above 900 m in the beech belt); natural black pine of Villetta Barrea and the Camosciara (387) | 6.7 % | 658 / 1,020 / 1,345 m |
| `riparian` | Pioppo-saliceto ripariale (27,985) | 6.5 % | 73 / 286 / 875 m |
| `transitional_woodland_shrub` | rose, bramble and blackthorn scrub (10,020), broom scrub (6,977), badland scrub (3,081) | 4.6 % | 220 / 710 / 1,202 m |
| `chestnut` | Castagneto neutrofilo-acidofilo (4,114), Castagneto da frutto (1,904) | 1.4 % | 684 / 894 / 1,073 m |
| `evergreen_oak` | holm oak: mesoxerofila (3,281), rupicola (1,276), costiera termofila (750; the Torino di Sangro wood, about 100 ha) | 1.2 % | 319 / 775 / 1,011 m |
| `exotic_broadleaf` | Robinieto-ailanteto (2,761) | 0.6 % | 86 / 346 / 772 m |
| `mediterranean_pine` | Aleppo-pine reforestation, "tra i 300 ed i 500 metri" (1,847) | 0.4 % | 44 / 395 / 627 m |
| `mixed_broadleaf_conifer` | Variante abete bianco (50) | < 0.1 % | 1,115 m |
| (left out of the woods) | juniper scrub "nella fascia montana e subalpina", Juniperus nana and J. communis (20,795); Mugheta appenninica, Pinus mugo krummholz above the beech on the Majella (1,418) | — | juniper 1,171 / 1,643 / 2,007 m; mugo 1,849 / 2,010 / 2,176 m |

The native silver fir (Martese in the Laga, Rosello and Castiglione Messer Marino in the Alto
Vastese) is mapped inside the beech types (the Faggeta montana lists *Abies alba* and *Taxus*), so
`beech` carries it; `fir_spruce` and `other_conifer` are empty in Abruzzo. The region config leaves
the montane juniper scrub and the mugo krummholz out of every group, as the Marche leaves its montane
heath out and INFC files both as other wooded land. No Abruzzo source names either as a host of
these fungi, so leaving them out only stops them diluting the cells around the tree line.

**The grid as built on 2026-09-28** (from the regional forest-type map;
`mushma_abruzzo_forest_composition_2026`): 11,189 cells, 3,782 woodland cells, 402,905 ha of forest
(-2.1 % against INFC 2015); cell elevation median 1,061 m (5th-95th percentile 449-1,661 m, 8.6 % of
woodland cells above 1,600 m, 0.8 % above 1,800 m, max 1,940 m; Marche median 669 m); beech 31 % of
the wooded area (cell elevation median 1,420 m, p10 1,110 m, p90 1,709 m), deciduous oak 29 %, mixed
broadleaf 17 %, mountain pine 7 %, riparian 6 %, transitional 5 %, macchia 2 %; beech dominates 1,538
woodland cells, deciduous oak 1,308, mixed broadleaf 551; slope median 19.9° (p90 28.2°; Tuscany 16.6°
and 26.2°); topsoil pH median 6.65 (p5 6.16, p95 7.33).

**Altitude belts** (`regione_abruzzo_ctf2009`, type sheets):

| type | belt and where |
|---|---|
| beech (Faggeta montana) | "localizzati sopra i 1000 metri", "dai 1000 metri fino al limite superiore della vegetazione"; the largest stands in the Parco Nazionale d'Abruzzo, the Majella and the Monti Pizi, the Velino-Sirente, the Laga, Monte di Campli, the Gran Sasso; on calcareous and arenaceous soils, with *Abies alba*, *Acer pseudoplatanus*, *Taxus* |
| beech at the tree line (Faggeta altomontana rupestre) | "Versanti caldi dai 1100 metri fino al limite superiore del bosco", sparse and shrubby, on shallow calcareous soil "con ridotta quantità di lettiera ed accentuata aridità edafica" (Majella, Mainarde, Camosciara, Monte Petroso) |
| lower beech (Faggeta termofila e basso montana) | the lower montane belt between the deciduous oaks and the beech; locally with silver fir and yew |
| Turkey oak | Cerreta mesoxerofila "dai 700 fino ai 1400 m", on calcareous or arenaceous soil; Cerreta mesofila 900-1,400 m on north slopes, deep sandstone soils, in mosaic with the lower beech |
| downy oak | "dal livello del mare fino ai 1300 metri" (tipico), 200 to 800-1,400 m (mesoxerofilo), over 1,000 m (pioniero); the subacidophilous downy oak of the Laga and northern Gran Sasso flysch |
| chestnut | fruit orchards "dai 500 agli 800 metri", "acidofile, su suoli ben drenati e privi di calcare attivo", in the Teramo and L'Aquila provinces; coppice on the Laga and Monte Verrico, in western L'Aquila province (Valle Roveto, Carseolano), "pressoché assenti" in Chieti and Pescara |
| hop-hornbeam | 300-1,000 m (pioneer), 800-1,000 m "a contatto con la faggeta" (mesophilous); mostly calcareous soils |
| conifer reforestation | "principalmente pino nero", the montane one "a quote generalmente superiori a 900 m ... nell'ambito della vegetazione delle faggete", on "substrati calcarei spesso erosi e degradati" (Assergi to Zizzoli, north of L'Aquila, the Pescara-Chieti border) |
| juniper scrub | montane: "ai limiti superiori del bosco (dai 1000 fino ai 2200 metri)", on limestone (left out of the woods); mesoxerophilous: "delle zone costiere, della fascia dei querceti e degli orno-ostrieti" (`macchia`) |
| holm oak | gorges and warm slopes 300-1,100 m (Vomano, Liri, Gole di Popoli, Salinello); coastal only at Torino di Sangro |

**Substrate.** Most of Abruzzo is limestone; the Laga flysch (sandstone and marl, the Teramo side:
Valle Castellana, Rocca Santa Maria, Cortino, Crognaleto) is the acid exception and holds the
fruit-chestnut orchards and the subacidophilous oak (`regione_abruzzo_ctf2009`). SoilGrids topsoil pH
on the woodland grid is 6.16-7.33 (5th-95th percentile).

**Regional law.** L.R. 8 novembre 2006, n. 34, as amended up to L.R. 14/2020 (consolidated text of
the regional council; `lr_abruzzo_34_2006`): 3 kg per person per day of all species together (art.
2.1), minimum cap 4 cm for the ovolo and the *Boletus edulis* group (art. 2.2), "vietata la raccolta
dell'Amanita caesarea allo stato di ovolo chiuso" (art. 2.3), a picking permit (art. 3), no picking
at night (art. 10.1), the parks and reserves keep their own rules (art. 11), temporary closures by
the regional Giunta (art. 12). No fixed closed days, season dates or altitude limits. None of it
changes where or when the fungi fruit; it confirms the ovolo and the porcini as regional species.

## Occurrence cross-check (Abruzzo)

Queried 2026-09-26 (`mushma_occurrence_check_abruzzo_2026`): iNaturalist place 10867 (verifiable),
GBIF with `gadmGid=ITA.1_1` (GBIF rows copied from iNaturalist left out), elevations from the
Copernicus GLO-30 DEM for open iNaturalist records accurate to 1 km, and the comune and dominant
habitat of the record's cell on the grid of 2026-09-28. Aggregates only; no coordinates are stored. Enrichment = the
taxon's monthly share of its records ÷ the monthly share of all 2,792 Abruzzo iNaturalist fungi
records.

| taxon | n (iNat / GBIF other) | months | located records |
|---|---|---|---|
| *B. edulis* | 3 / 0 | May 1, Sep 1, Oct 1 | Sep 1,576 m (Fano Adriano, beech), Oct 1,536 m (Pizzoferrato, beech) |
| *B. reticulatus* | 3 / 0 | Jun 1, Jul 1, Sep 1 | Jun 860 m (Castiglione Messer Marino, oak), Jul 1,525 m (Valle Castellana, beech), Sep 1,046 m (L'Aquila) |
| *B. aereus* | 4 / 0 | Oct 2, Nov 2 | 51-88 m, all at Torino di Sangro by the coastal holm-oak reserve, one observer |
| *B. pinophilus* | 1 / 0 | Jul 1 | 1,525 m (Valle Castellana, beech) |
| *A. caesarea* | 1 / 0 | Sep 1 (2018) | 927 m (Carsoli, oak) |
| *Cantharellus* (genus) | 19 / 2 | May 1, Jun 1, Jul 1, Sep 1, Oct 7, Nov 7, Dec 1 | 14 of 17 at 11-96 m at Torino di Sangro, Oct-Dec (*C. alborufescens* incl. var. *lilacinopruinatus*, *C. cibarius*, *C. pallens*); May 658 m (Carunchio, *C. pallens*), Jul 1,298 m (Valle Castellana beech, *C. pallens*), Oct 973 m (Montereale); GBIF: 2 Mushroom Observer records, Oct 2012, 813 m |
| *Cantharellus*, enrichment | | May 0.5, Jun 0.8, Jul 0.8, Sep 0.3, Oct 1.9, Nov 4.1, Dec 1.4 | |

Abruzzo is the most thinly recorded region so far: 31 records for the six keys, all from 2018 on, and
18 of them from around one coastal wood, mostly by one observer. They cannot tune anything. They do
say three things: porcini and chanterelles reach the high beech (1,298-1,576 m, July to October); the
coast around the Torino di Sangro holm-oak reserve holds both the black porcino and the Mediterranean
chanterelles late in autumn (October to December); and no Abruzzo porcino record comes from the conifer
plantations. On the grid 16 of those 18 coastal records fall in cells the forest map gives to downy oak
and that are outside the woodland mask (2 are in a holm-oak woodland cell), so the sightings backtest
will not see them; 10 of the 12 inland records with a location are in woodland cells (beech, oak,
chestnut).

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **All four are here** (plausible). The Abruzzo book's cards place *B. edulis* "nei boschi di
  latifoglie, principalmente in quelle di querce, castagni, faggi e nelle abetaie. Dall'estate al
  primo autunno" (photographed on the Cortino hills, TE); *B. aestivalis* in "querce, castagni e
  faggi. Da Maggio al primo autunno" (chestnut at Carsoli, AQ); *B. aereus* "in simbiosi con
  quercia e faggio, difficilmente nei boschi di conifere. Dalla fine dell'estate a novembre"
  (chestnut at Valle Castellana, TE), with the Monti della Laga as the porcini "habitat d'elezione"
  (`amep_funghi_abruzzo_tieri`). The Laga blog reports "le 4 specie di Boletus sezione edules" in one
  basket in August 2016 (`funghiteramani_blog`, 12 Aug 2016).
- **The Laga sequence** (folklore, but dated and repeated over ten seasons, `funghiteramani_blog`):
  the summer porcino first, from mid-May ("due primordi di Boletus reticulatus", 11 May 2015) in the
  Turkey-oak and chestnut woods "dai 700 m in su" (29 May 2017), while "il bosco che c'interessa
  adesso non è quello di faggio sopra ai 1300 m"; the "porcino rosso" in the beech from late May and
  June ("primi rossi al Ceppo", 5 Jun 2016; "Nel faggio l'unico fungo presente con bei soggetti é il
  porcino rosso", 20 Jun 2016), fading in July ("sta pian piano scomparendo dai cesti essendo un
  fungo che ama il fresco, lo ritroveremo a fine stagione", 6 Jul 2015) as the summer porcino takes
  over in the beech ("il Boletus pinophilus che tenterà a scomparire a breve per lasciare spazio al
  Boletus aestivalis", 3 Jul 2015); in August "Il faggio comincia a produrre molto bene con stupendi
  Boletus pinophilus, Boletus reticulats e qualche Boletus edulis, mentre se si resta più in basso il
  Boletus aereus é molto presente" (6 Aug 2014); *B. edulis* in the beech from August ("In montagna,
  nel faggio, adesso é facile trovare Boletus edulis", 31 Aug 2015), its best "fine mese se non
  addirittura la prima settimana di ottobre, il più classico periodo dei nostri luoghi" (12 Sep
  2016); the black porcino in "cerro e castagno" with the heat, July to late September ("fioriture di
  Boletus aereus" in the "boschi termofili", 26 Sep 2016); "i nostri boschi" 700-900 m on the Ascoli
  border for the late-August flush (27 Aug 2015).
- **Altitude** (plausible / folklore). A porcino "a circa 1350 mt" in the Ceppo (19 Jul 2015,
  `funghiteramani_blog`); the located records at 1,525-1,576 m in July, September and October
  (`mushma_occurrence_check_abruzzo_2026`); best "nelle zone tra i 1.200 e i 1.800 metri"
  (`nordal_porcini_italia2024`, a company blog, folklore). The host belt runs to the tree line
  (`regione_abruzzo_ctf2009`, `bonanomi2020_treeline`).
- **Conifer plantations** (plausible, by absence). No Abruzzo source puts porcini under the black-pine
  reforestation. The Laga blog's conifer entry is a late-September flush of "Tricholoma, Russula,
  Lactarius, Hygrophorus, Amanita" "sotto misto conifera" (30 Sep 2019), while its porcini are in the
  beech; the Abruzzo book has *B. aereus* "difficilmente nei boschi di conifere". The Marche evidence
  (planted *P. nigra* holds few, mostly conifer-specific partners, `mrak2025_mycorrhiza`; no porcini in
  the Sibillini black-pine plantations) applies to the same plantations on the same limestone.
- **Beech and the black porcino.** The book pairs *B. aereus* with oak and beech; the Laga blog writes
  "Presto vedremo il Boletus aereus sotto faggio" in 2024 as something new (2 Sep 2024). The four
  located records are all at Torino di Sangro, by the coastal holm-oak reserve.

**Decisions.**

| key | factor | Tuscany | Abruzzo | why | confidence |
|---|---|---|---|---|---|
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | 200 → 700 … **1,800 → 2,000** | beech, its host, from 1,000 m to the tree line (map p99 1,824 m); records at 1,536-1,576 m; "tra i 1.200 e i 1.800 metri" (folklore) | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | hop-hornbeam on limestone and invasive maple, ash and cherry; hop-hornbeam named only for the summer and black porcini | plausible (weak) |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.3** | black-pine reforestation on eroded limestone, no Abruzzo report; the montane plantings include fir and spruce, so not 0.1 as in the Marche | plausible (weak) |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | rose, bramble, broom and badland scrub, no host | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,500 → 1,800** | fruits in the Laga beech in July and August (blog; one record at 1,525 m); the Abruzzo beech sits about 240 m above the Marche one (grid medians 1,420 and 1,181 m), so the Marche band (1,300 → 1,600) moves up by as much | plausible |
| *reticulatus* | habitat `mountain_pine` | 0.6 | **0.3** | black-pine reforestation, no Abruzzo report (as the Marche) | plausible (weak) |
| *reticulatus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn and broom scrub, oaks only at its edges | plausible |
| *aereus* | habitat `macchia` | 1.0 | **0.3** | Juniperus oxycedrus scrub of the oak belt (606-1,084 m), hosts only in the downy oak it grows among, like the thorn and broom scrub; the Cistus-Arbutus-Erica macchia of Tuscany covers 6 ha here (0.1 while the class also held the montane junipers, before the grid left them out) | plausible (weak) |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn and broom scrub | plausible |
| *aereus* | habitat `beech` | 0.1 | **0.3** | "in simbiosi con quercia e faggio" (Abruzzo book), as Umbria; the blog calls it new under beech; the altitude band keeps it off most beech | plausible (weak) |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | 300 → 800 … **1,800 → 2,000** | every Abruzzo report is from the beech, which reaches the tree line; one record at 1,525 m | plausible |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **0.3** | black pine on limestone, not Scots pine; wants "terreni molto acidi" | plausible (weak) |
| *pinophilus* | habitat `mixed_broadleaf` | 0.3 | **0.1** | calcareous hop-hornbeam and old-field broadleaf | folklore to plausible |
| *pinophilus* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | thorn and broom scrub | plausible |
| all four | season, weather, stoppers, growth clock | — | kept | the Laga sequence fits every window; no regional numbers | as Tuscany |

Kept on purpose: the *B. edulis* window (the 1 July → 1 September ramp already gives August 0.5-1.0,
and the blog's peak is late September); the *B. pinophilus* windows (spring flush late May to early
July, autumn return, both as on the Laga), though the blog also has it on 6 August 2014 and 11 July
2018, in the gap between them; the *B. aereus* upland/lowland split at 400-600 m (upland summer on
the Laga, lowland autumn in the coastal records); the *B. aereus* altitude band (… 800 → 1,250 m: the
blog puts it "più in basso" than the beech, at 700-900 m); beech as a full host of *B. edulis* and *B.
pinophilus* and secondary for *B. reticulatus* (0.6 already gives a half-beech cell full credit);
hop-hornbeam secondary for *B. reticulatus* and marginal for *B. aereus* (0.3 gives a pure cell full
credit; two fifths of the class here is old-field broadleaf, no host).

On the grid of 2026-09-28, the habitat gate reaches full credit on 56 % of woodland cells for *B.
edulis* and *B. pinophilus* (79-80 % with the Tuscan affinities), 99 % for *B. reticulatus* and 84 %
for *B. aereus* (54 %, mostly the beech change); the altitude gate is full on 82 % of woodland cells
for *B. edulis* (74 %), 74 % for *B. pinophilus* (66 %) and 85 % for *B. reticulatus* (54 %). The mean
of habitat × altitude is 0.83, 0.93, 0.45 and 0.80 for the four keys (Tuscan rules on the same cells:
0.89, 0.70, 0.44, 0.85). The *B. reticulatus* band lifts the porcini group most. The *B. edulis* and
*B. pinophilus* habitat changes bite harder than on the CLC grid (which had hop-hornbeam at 7 % of the
woods): they cut full credit mostly on the 551 cells hop-hornbeam dominates, where the group still
scores through *B. reticulatus* (0.6) and *B. aereus* (0.3, full on a pure cell). Neither decision rested
on the grid's shares, so both stand.

## Ovoli (*Amanita caesarea*)

**Regional evidence.** Presence: the regional law's ovolo rules (`lr_abruzzo_34_2006`, art. 2.2 and
2.3); the Abruzzo book's card, "Cresce preferibilmente nei boschi di latifoglie, di preferenza quelle
di quercia, con esposizione sufficientemente assolata. Dall'estate all'autunno", photographed in the
wood of Goriano Sicoli (AQ) (`amep_funghi_abruzzo_tieri`). Timing and belt on the Laga
(`funghiteramani_blog`, folklore): after the black porcino, with the heat ("ancora latitante é la
Amanita caesarea ma arriverà dopo i neri", 6 Aug 2014; first the black porcino "e successivamente
... anche la Amanita caesarea", 18 Jul 2016); present on 9 and 16 August 2016 ("in boschetto termofilo di
cerro"); "Tantissimi porcini di cerro e castagno e anche ovoli di Amanita caesarea" "nei boschi di
circa 700-900 m di confine con la provincia ascolana" (27 Aug 2015); "a breve finirà la crescita della
Amanita caesarea ancora presente nel sottobosco del castagno e cerro" (7 Sep 2015); "Nei boschi caldi
hanno fatto la comparsa le Amanita caesarea" after a dry August (11 Sep 2020); and in 2024, "in pochi
la cercavano, era difficile incontrarla, alcuni anni non si vedeva proprio. Oggi è invadente" (2 Sep
2024). One iNaturalist record, September 2018 at 927 m (Carsoli). Hosts sit high: chestnut map
median 894 m (p90 1,073 m), Turkey oak 700-1,400 m.

**Decisions.**

| factor | Tuscany | Abruzzo | why | confidence |
|---|---|---|---|---|
| season | 01-06 → 01-09 … 05-11 → 30-11 | 01-06 → **01-08** … 05-11 → 30-11 | August is the ovolo's month on the Laga, from early August to early September; Piemonte made the same change on its records. The end is kept: no Abruzzo source covers October, and frost and cold nights end it at altitude | plausible (the Abruzzo shift rests on one forager's reports) |
| altitude | … 750 → 1,100 | … **900 → 1,200** | the Laga ovoli at 700-900 m, the one record at 927 m, hosts to 1,100-1,400 m; zero at IUCN's "only seldom above 1200 m" | plausible |
| habitat `macchia` 0.3 | — | kept | Juniperus oxycedrus scrub of the oak belt, with downy oak as the scattered host, as Tuscan macchia holds holm and cork oak (0.1 while the class also held the montane junipers) | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | thorn and broom scrub, not heath and clearings with oaks | plausible |
| habitat deciduous oak, chestnut 1.0 | — | kept | the book ("di preferenza quelle di quercia") and the blog ("cerro e castagno") | strong (hosts) |
| habitat `mixed_broadleaf` 0.3 | — | kept | no Abruzzo evidence either way | plausible |
| weather rules, sun exposure | — | kept | no regional numbers; "esposizione sufficientemente assolata" agrees with the Tuscan preference for sunny slopes | as Tuscany |

On the grid of 2026-09-28 the ovolo altitude gate is full on 34 % of woodland cells (21 % with the
Tuscan band), the habitat gate on 51 % (52 %), and the mean of habitat × altitude rises from 0.35 to
0.45.

## Gallinacci (*Cantharellus* s.l.: "gallucci", "galletti")

**Regional evidence.** The Abruzzo book's card: "Cresce prevalentemente nei boschi di latifoglie e di
conifere ... Dall'estate all'autunno", "si trova in tutti i boschi della Regione", photographed in a
chestnut wood at Carsoli (`amep_funghi_abruzzo_tieri`). On the Laga (`funghiteramani_blog`,
folklore) the chanterelles open the season: "i primi Cantharellus cibarius (gallucci)" on 7 May 2014;
"se visiteremo la cerreta ... sono gia presenti in discreta quantità gallucci e russule" (31 May
2014); "intorno agli 800 m tra cerro e castagno stanno nascendo i gallucci" (28 May 2015); "molti i
Cantharellus cibarius" with the beech porcini (13 Jun 2016); by the end of June "normalmente i
Cantharellus cibarius dovrebbero essere solo un ricordo" (28 Jun 2015); still, sporadic, at the Ceppo
in July (9 Jul 2015) and back after rain (27 Jul 2015). The records split in two: 14 of the 17 located
ones are Mediterranean segregates at Torino di Sangro, by the coastal holm-oak reserve, October to December
(*C. alborufescens*, *C. pallens*, *C. cibarius*), and three are inland (May 658 m, July 1,298 m in the
Laga beech, October 973 m). The holm-oak segregates are the ones `olariaga2017` places under
*Quercus ilex* on calcareous soil.

**Decisions.**

| factor | Tuscany | Abruzzo | why | confidence |
|---|---|---|---|---|
| season, mountain window (above 1,000 m, blended from 600 m) | 01-06 → 01-07 … 15-10 → 15-11 | **15-05 → 15-06** … 15-10 → 15-11 | first gallucci in early and late May, "molti" by mid-June on the Laga | plausible (the Abruzzo shift rests on one forager's reports) |
| season, lowland window | 15-04 → 10-05 … 15-12 → 25-01 | kept | the coastal holm-oak records run October to December (Umbria and the Marche have no such coast) | plausible |
| altitude | … 1,000 → 1,700 | … **1,400 → 1,900** | chanterelles in the Ceppo beech (about 1,300-1,500 m) in June and July; one record at 1,298 m; beech median 1,385 m, p90 1,682 m | plausible |
| habitat beech | 0.6 | **1.0** | the Laga chanterelles follow the season into the beech; *C. pallens* in the Laga beech; the Marche and Emilia-Romagna made the same change | plausible |
| habitat deciduous oak | 0.3 | **0.6** | "tra cerro e castagno", "la cerreta" on the Laga; *C. pallens* in an oak cell at Carunchio; the Marche made the same change | plausible |
| habitat `mountain_pine` | 0.3 | **0.1** | black pine on limestone; "sotto misto conifera" the blog lists other genera | plausible (weak) |
| habitat `macchia` | 0.3 | **0.1** | Juniperus oxycedrus scrub of the oak belt, open and often grazed, with at most scattered oak; the Abruzzo chanterelles are reported only from closed woods (the ovolo and black porcino, which fruit in sunny scrub, keep 0.3 there; the Marche has 0.1) | plausible (weak) |
| habitat `transitional_woodland_shrub` | 0.3 | **0.1** | thorn and broom scrub, no host | plausible |
| habitat evergreen oak, chestnut 1.0 | — | kept | 14 of 17 located records at Torino di Sangro by the holm-oak reserve (most in cells the map gives to downy oak); the book's photo in chestnut | plausible |
| soil pH, lithology | disabled | kept disabled | Abruzzo woodland topsoil pH 6.2-7.3; the commonest records are calcicolous segregates | plausible |
| weather rules | — | kept | no regional numbers | as Tuscany |

On the grid of 2026-09-28 the gallinacci altitude gate is full on 78 % of woodland cells (44 % with the
Tuscan band) and the habitat gate on 92 % (81 %); habitat × altitude rises from 0.72 to 0.90.

## Weather rules: why none changed

- **Rain amount and lag.** No Abruzzo source gives a rain amount or a lag in numbers. The Laga blog's
  forecasts are qualitative and agree with the Tuscan rules: "prossime buone/ottime crescite a 7-10
  giorni a partire dai boschi caldi di latifoglia" after rain (5 Jun 2016); a flush "entro 10 giorni"
  after a wet spell (15 Jun 2014). The Tuscan lag (Amiata) and amount ramps stay.
- **Drying wind.** "il vento freddino per diversi giorni ha seccato più del caldo" (23 Aug 2016), "il
  caldo e l'assenza di vento favoriranno le nuove crescite" (2 Jul 2018): the porcini drying stopper
  (ET0 proxy) already encodes this, unchanged.
- **Temperature.** Cold nights slow the season ("di notte in montagna si scende sotto i 10°, questo
  proprio non aiuta", 31 May 2014; "temperature notturne ... al di sotto della media", 20 Jun 2016),
  and the ovolo and black porcino wait for heat. The air-temperature bands, the cold-night rules and
  the growth clock read each cell's own weather, so the high beech is already slower and later.
- **Rain climate.** Abruzzo runs from dry Adriatic hills to wet mountain ridges; the porcini 30-day
  rain is scored against each cell's own normal, so it adapts; the absolute 30-day ramps of ovoli and
  gallinacci will be full less often in the dry low hills. No Abruzzo rain climatology was read for
  this card.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it on
  Abruzzo gauges is a region-config task (`regions/abruzzo.md`), not a species one.
- **Slope and sun exposure.** Abruzzo woodland is steeper than Tuscany's (median 19.9°, p90 28.2°, 21 %
  of cells over 25°), but the slope stopper's mean over woodland cells is 0.989 (p10 0.957; Tuscany
  0.994, Marche 0.984), too small to retune. The sun-exposure stoppers act only below 900-1,100 m and
  were left alone.

## Sanity contrasts

`abruzzo/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written
down before any Abruzzo score existed (none had been computed on 2026-09-26). The schema has no group
field: contrasts are porcini unless their id starts with `ovoli_` or `gallinacci_` (read those with
`--group ovoli` / `--group gallinacci`). "Normal" is the area's mean over 2017-2025.

**16 contrasts: 12 porcini, 2 ovoli, 2 gallinacci**, researched on 2026-09-26. Every cited page was
opened and every quoted Italian phrase was checked against the page text by script (and four sources
again by hand). Every comune is an ISTAT 2025 name inside Abruzzo and on the grid. Areas:
`laga_teramana` (Valle Castellana, Rocca Santa Maria, Cortino, Crognaleto, Torricella Sicura; 341
woodland cells), `ceppo` (Rocca Santa Maria; 49), `valle_castellana` (116), `marsica` (35 comuni of the
Marsica, the Carseolano and the Valle Roveto; 913), `abruzzo_southwest` (Carseolano, western Marsica,
Valle Roveto, Vallelonga, the Parco Nazionale d'Abruzzo comuni, Scanno, Castel di Sangro; 1,126),
`chieti_hills` (province CH minus the Majella-park comuni; 336), `gran_sasso_majella` (the beech comuni
of the Gran Sasso and the Majella; 431) and `abruzzo` (the whole region; 3,782). Every area has
woodland cells on the grid of 2026-09-28.

**The sources are thin and mostly one blog.** Abruzzo local press rarely says how a season went
(searches of Il Centro, IlCapoluogo, AbruzzoWeb, MarsicaLive, Terre Marsicane, Zonalocale and Il Germe
found mostly poisonings, fines, permits and recipes). As in the Marche, the best-dated source is Bruno
de Ruvo's forager blog (*Funghi Teramani*, then *A spasso tra le nuvole*), and 11 of the 16 contrasts
rest on it. It reports the Teramo side of the Laga: the Ceppo and the Bosco Martese, the Cavata, the
Valle Castellana chestnut and oak woods, the Vomano side. **The Ceppo is in the comune of Rocca Santa
Maria** (1,334 m), where it meets Valle Castellana, Cortino and Torricella Sicura: "Il Ceppo ricade nel
territorio del Comune di Rocca Santa Maria"
([Caput Frigoris](https://www.caputfrigoris.it/rete-meteo/ceppo/descrizione.htm)), and the blog's
"località Ceppo di Rocca Santa Maria (TE)"
([2016-07-25](https://funghiteramani.blogspot.com/2016/07/corso-di-rinnovo-al-ceppo.html)). The
contrasts the Marche file read onto Acquasanta Terme and Arquata del Tronto sit here on their own
comuni. Reused with the same pairing: 2016 vs 2017 at the turn of October, 2018 vs 2017 in late August,
2024 vs 2020 in late August, the 2025 timing, the 2024 ovoli, 2016 vs 2025 June chanterelles; the 2020
ovoli timing moves to Valle Castellana, the basin the post names. Changed: July (2016 vs 2017 became
2024 vs 2018) and early September (2019 vs 2016), to keep 2017 on only two lower sides.

| id | group | higher | lower | main source (second sources) | weakness |
|---|---|---|---|---|---|
| `laga_july_2024_2018` | porcini (summer) | Laga TE 2024, 3–18 Jul | same, 2018 | [A spasso tra le nuvole 2024-07-23](https://www.aspassotralenuvole.it/post/un-po-di-analisi-porcinara): "C'è stata una "sfungata" eccezionale di Boletus aestivalis, in certi boschi sembrava inesauribile" ([Funghi Magazine 2024-06-28](https://funghimagazine.it/aggiornamento-funghi-28-06-2024/): in Marche-Abruzzo porcini "li si potrà trovare senza dubbio da inizio prossima settimana"; 2018: [Funghi Teramani 2018-07-11](https://funghiteramani.blogspot.com/2018/07/secondo-aggiornamento-di-luglionon-va.html) "di porcini ce ne sono veramente pochi", [2018-07-21](https://funghiteramani.blogspot.com/2018/07/terzo-aggiornamento-di-luglioarrivera.html) "i funghi non ci sono") | one blogger; the 2024 post (23 July) does not date the flush; the window is bracketed by FM's 28 June forecast and the blog's "il bosco appare troppo secco" on 23 July |
| `laga_august_2018_2017` | porcini | Laga TE 2018, 18–31 Aug | same, 2017 | [Funghi Teramani 2018-08-21](https://funghiteramani.blogspot.com/2018/08/quarto-aggiornamento-di-agostoporcini.html) ([2018-08-24](https://funghiteramani.blogspot.com/2018/08/situazione-paradossalelanarchia-di-quota.html), Cavata "E' un momento buono per i funghi", repeated by [Il Centro 2018-08-26](https://www.ilcentro.it/teramo/assalto-dei-fungaioli-sulla-laga-%C3%A8-polemica-1.2004692); 2017: [2017-08-09](https://funghiteramani.blogspot.com/2017/08/2017-stagione-finita.html), [2017-08-29](https://funghiteramani.blogspot.com/2017/08/cosa-succedera.html)) | one blogger (Il Centro only quotes him); 2017 is also the lower side of `laga_2016_2017_turn_of_october` |
| `marsica_2018_early_september` | porcini | Marsica 2018, 27 Aug–3 Sep | same, normal | [Rete8 2018-09-03](https://www.rete8.it/cronaca/123marsica-boom-funghi-permesso-straordinario-carsoli/): "Il clima di questi giorni ha favorito nella Marsica una proliferazione straordinaria di porcini, galletti e altri tipi di funghi" (Coldiretti's national note of 2018-09-02 on [Virtù Quotidiane](https://www.virtuquotidiane.it/cronaca/funghi-stagione-record-dopo-le-abbondanti-piogge.html): "si annuncia una stagione da record"; the Laga blog, late August 2018) | a short TV-news piece with no named woods; "Marsica" is loose (35 comuni); the Coldiretti note is national and recycled wording; "normal" includes 2018 |
| `abruzzo_summer_2019` | porcini | whole region, normal, 1 Jul–25 Aug | same, 2019 | [AbruzzoWeb 2019-09-12](https://abruzzoweb.it/coldiretti-in-abruzzo-e-boom-funghi-con-le-prime-piogge-russole-e-porcini/) (Coldiretti Abruzzo): "nei mesi di luglio e di agosto, a causa della grande siccità, si era registrato un calo del 50-60% di funghi di bosco (principalmente Russole e Porcini)" (same note on [Virtù Quotidiane](https://www.virtuquotidiane.it/cronaca/in-abruzzo-e-boom-di-raccolta-di-funghi-ecco-il-decalogo-del-buon-raccoglitore.html); [Funghi Teramani 2019-09-02](https://funghiteramani.blogspot.com/2019/09/ragazzi-il-blog-ad-informarviboschi.html) "la stagione fino ad oggi è stata pessima") | a farmers'-union press note, region-wide, no method behind "50-60%"; "normal" includes 2019 |
| `laga_2019_2016_early_september` | porcini | Laga TE 2019, 3–12 Sep | same, 2016 | [Funghi Teramani 2019-09-05](https://funghiteramani.blogspot.com/2019/09/oramai-lo-sanno-anche-le.html) ([2019-09-13](https://funghiteramani.blogspot.com/2019/09/aggiornamento-del-1309preoccupa-il-secco.html); Coldiretti Abruzzo 2019-09-12: "l'improvviso boom della raccolta dei funghi settembrini"; 2016: [2016-08-30](https://funghiteramani.blogspot.com/2016/08/parliamo-di-funghi.html), [2016-09-05](https://funghiteramani.blogspot.com/2016/09/aggiornamento-del-0309dallestasi-alla.html)) | one blogger; the 2019 posts name no place (the flush was "tra cerro e castagno a quote relativamente basse", the beech still "in attesa" on 5 Sep), so the area is the blog's whole beat |
| `valle_castellana_vs_ceppo_2020` | porcini | Valle Castellana 2020, 7–14 Sep | Rocca Santa Maria (Ceppo), same | [Funghi Teramani 2020-09-11](https://funghiteramani.blogspot.com/2020/09/pare-che-ci-siamo.html): "quello più produttivo è il bacino di Valle Castellana e zone vicine, il Ceppo invece stenta con pochissimi ritrovamenti" | one post; adjacent comuni; the difference is mostly habitat (warm chestnut-oak woods vs the Ceppo's beech), and Rocca Santa Maria also holds lower oak woods; `ceppo` is small (49 cells) |
| `chieti_vs_gran_sasso_majella_2021` | porcini | Chieti hills (CH minus the Majella-park comuni) 2021, 28 Aug–6 Sep | Gran Sasso + Majella beech comuni, same | [Funghi Magazine 2021-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): oak-chestnut "breve ma intensa buttata" "tra le province di l'Aquila, alto Teramano e soprattutto Chieti", "mentre i Faggi appenninici risultano anche in Abruzzo ancora pigri e poco produttivi, in particolar modo tra Gran Sasso e Maiella" ([FM 2021-09-10](https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/): "Maiella e Gran Sasso hanno registrato fin'ora nascite col contagocce") | national bulletin; habitat claim mapped onto comuni (the beech comuni also hold oak, the Chieti hills a little beech); `chieti_hills` woodland is thin and scattered (336 cells, 39 of its 42 comuni under 15); the storms' date is only "seconda metà di Agosto" |
| `abruzzo_october_2022` | porcini | whole region 2022, 3–18 Oct | same, normal | [Funghi Magazine 2022-10-13](https://funghimagazine.it/meteo-funghi-13-10-2022/): "le grandi nascite in atto al momento in Toscana, Umbria, Marche, Abruzzo, Molise ..." ([A spasso tra le nuvole 2022-10-24](https://www.aspassotralenuvole.it/post/ma-%C3%A8-realmente-finita): the Laga season "è finita col botto ... una stagione che, per molti, è da incorniciare") | national bulletin, region-wide, Abruzzo one of nine regions, "in gran parte ... Porcini Neri"; the blog post is a season verdict, not dated to the window; mirrors `marche_october_2022` |
| `laga_vs_southwest_2023_october` | porcini | Laga TE 2023, 5–18 Oct | south-west Abruzzo (Carseolano, Marsica west, Valle Roveto, Vallelonga, PNALM, Castel di Sangro), same | [Funghi Magazine 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "in Abruzzo, ancora buone le nascite di Porcini sul Gran Sasso e Monti della Laga ... Nel resto della regione i venti di Tramontana hanno di fatto inficiato ogni nascita" ([A spasso tra le nuvole 2023-10-20](https://www.aspassotralenuvole.it/post/al-rosso-la-stagione-si-fermer%C3%A0): "questa parte della Laga sia stata così premiata da fruttificazioni di Boleti"; [FM 2023-10-04](https://funghimagazine.it/aggiornamento-porcini-04-10-2023/): Abruzzo "sfigati" by cold winds, woods "fermi") | national bulletin; the lower side is FM's residual "resto della regione", not a named place; the blog says other Teramo mountains "battono il passo" (so the Gran Sasso was left out of the higher side), and on 12 Oct it found only small porcini in a dry wood |
| `laga_2024_2020_late_august` | porcini | Laga TE 2024, 26 Aug–5 Sep | same, 2020 | [A spasso tra le nuvole 2024-09-02](https://www.aspassotralenuvole.it/post/cosa-succede-nei-nostri-boschi) (same text on [Funghi Teramani 2024-09-02](https://funghiteramani.blogspot.com/2024/09/cosa-succede-sulle-nostre-montagne.html); [Neve Appennino 2024-09-11](https://www.neveappennino.it/news/raccolte-spropositate-di-funghi-porcini-nella-zona-del-ceppo-alcuni-sono-venuti-quasi-alle-mani/): at Rocca Santa Maria "in questi giorni c'è stata una vera e propria raccolta da record"; [FM 2024-09-19](https://funghimagazine.it/aggiornamento-nascite-funghi-19-09-2024/): "In Abruzzo c'è stato il "delirio fungino" già a inizo mese"; reader on [FM 2024-09-12](https://funghimagazine.it/aggiornamento-funghi-12-09-2024/): "Nel teramano negli ultimi 15 gg porcini a quintali!"; 2020: [2020-08-24](https://funghiteramani.blogspot.com/2020/08/e-arrivata-lacqua.html), [2020-09-05](https://funghiteramani.blogspot.com/2020/09/siamo-ancora-in-attesa.html)) | the 2020 side is inferred for 26 Aug–5 Sep: dry to 24 Aug, rain, "non ho notizie confortanti" on 5 Sep, first flush reported on 11 Sep |
| `laga_2016_2017_turn_of_october` | porcini | Laga TE 2016, 25 Sep–10 Oct | same, 2017 | [Funghi Teramani 2016-10-03](https://funghiteramani.blogspot.com/2016/10/aggiornamento-del-0210il-clou-dei.html) ([2016-09-26](https://funghiteramani.blogspot.com/2016/09/aggiornamento-del-2509si-riparte.html), [2016-10-10](https://funghiteramani.blogspot.com/2016/10/aggiornamento-del-1010si-va-verso-il.html); 2017: [2017-10-02](https://funghiteramani.blogspot.com/2017/10/savo-quasi-per-dirvi.html), [2017-11-02](https://funghiteramani.blogspot.com/2017/11/e-finita.html) "si chiude un anno micologico sicuramente il più brutto della mia vita") | one blogger; 2016's clou is in the beech woods, and on 2016-09-19 he still wrote "i funghi non ci sono" |
| `laga_2025_timing` | porcini | Laga TE 2025, 8–20 Sep | same year, 1–12 Oct | [A spasso tra le nuvole 2025-10-11](https://www.aspassotralenuvole.it/post/game-over) ([2025-09-14](https://www.aspassotralenuvole.it/post/siamo-al-clou-della-stagione): "localizzata prevalentemente sui Monti della Laga ed in particolare al Ceppo") | one blogger; the September flush was "esclusivamente sotto faggio" and the chestnut-oak belt "quasi assente", so the whole-area mean may blur it; season gate (see below) slightly favours September |
| `ovoli_laga_2024` | ovoli | Laga TE 2024, 25 Aug–6 Sep | same, normal | [A spasso tra le nuvole 2024-09-02](https://www.aspassotralenuvole.it/post/cosa-succede-nei-nostri-boschi): "nascono così tanti porcini e anche ovoli"; the ovolo "Oggi è invadente" | one blogger; "Oggi è invadente" also describes a trend of recent years, not only 2024; "normal" includes 2024 |
| `ovoli_valle_castellana_2020_timing` | ovoli | Valle Castellana 2020, 7–15 Sep | same year, 10–24 Aug | [Funghi Teramani 2020-09-11](https://funghiteramani.blogspot.com/2020/09/pare-che-ci-siamo.html) ([2020-08-12](https://funghiteramani.blogspot.com/2020/08/aggiornamento-di-ferragosto.html), [2020-08-24](https://funghiteramani.blogspot.com/2020/08/e-arrivata-lacqua.html); [FM 2020-09-21](https://funghimagazine.it/meteofunghi-21-09-2020/): in the alto Reatino "con sconfinamenti nel confinante Abruzzo" "sono ancora protagonisti gli Ovoli reali") | the August side is drought, not an observed absence of ovoli; [FM 2020-08-07](https://funghimagazine.it/aggiornamento-meteofunghi-07-08-2020/) has "pochissime nascite nell'Aquilano ma migliori nel Teramano" for early August, so the lower window starts on 10 Aug, after the blog's "i funghi pare che non ci siano" |
| `gallinacci_laga_june_2016_2025` | gallinacci | Laga TE 2016, 8–18 Jun | same, 2025 | [Funghi Teramani 2016-06-13](https://funghiteramani.blogspot.com/2016/06/aggiornamento-del-12-giugnoancora-acqua.html) ([2016-06-10](https://funghiteramani.blogspot.com/2016/06/ci-si-comincia-divertire-nel-bosco.html); [A spasso tra le nuvole 2025-06-16](https://www.aspassotralenuvole.it/post/a-breve-porcini)) | one blogger; by 2016-06-20 the gallucci "tengono, ma in calo"; in late June 2025 FM reported porcini births in southern and western Abruzzo ([2025-07-03](https://funghimagazine.it/aggiornamento-nascite-funghi-4-11-luglio-2025/)), so the window stops at 18 June |
| `gallinacci_laga_july_2024_2025` | gallinacci | Laga TE 2024, 3–18 Jul | same, 2025 | [A spasso tra le nuvole 2024-07-23](https://www.aspassotralenuvole.it/post/un-po-di-analisi-porcinara) ([FM 2024-07-25](https://funghimagazine.it/aggiornamento-funghi-25-07-2024/): "Mitici sono stati quest'anno i raccolti di Finferli in Sila ... poi nell'Appennino Abruzzese-Laziale"; 2025: [A spasso tra le nuvole 2025-08-01](https://www.aspassotralenuvole.it/post/i-boschi-sono-pronti)) | the 2025 side is inferred from "un giugno ed un luglio poverissimi d'acqua" and "una scomparsa progressiva di varietà Micologica", which names no chanterelles; the 2024 flush is undated (as in `laga_july_2024_2018`, same window) |

**Season gates.** Most contrasts compare the same dates in two years or two areas, so the gate
cancels. `laga_2025_timing` (8-20 September vs 1-12 October) is partly decided by it: *B. reticulatus*
and upland *B. aereus* ramp down from 30 September, so the gate alone favours September a little (as in
the Marche). `ovoli_valle_castellana_2020_timing` (7-15 September vs 10-24 August) is not: the ovolo
gate is fully open from 1 August. The June chanterelle window sits on the mountain window's ramp (15
May → 15 June), but both years share it.

**Outlets that block AI agents** (robots.txt checked on 2026-09-26; nothing fetched from them): Il
Pescara and ChietiToday (Citynews), Il Messaggero, ANSA, Corriere Adriatico, Il Sole 24 Ore, La Stampa,
la Repubblica (the Marche research also found Il Resto del Carlino and AnconaToday). Il Centro,
AbruzzoWeb, Rete8, Virtù Quotidiane, Marsica-Web, Neve Appennino, Funghi Magazine, blogspot and
aspassotralenuvole.it allow them.

Candidates left out:
- Crognaleto and Campotosto vs the Ceppo, 8-18 August 2018 ("altri siti che guardano il Vomano pare
  siano molto più generosi, lo stesso Campotosto"): hearsay, Campotosto has 10 woodland cells. The best
  spatial spare.
- 2016 vs 2020 in early August, and ovoli 2016 vs 2020 in August: 2020 August already carries two lower
  sides, and Funghi Magazine has early August 2020 "migliori nel Teramano".
- 2016 vs 2017 in early July (the Marche pairing): dropped only to keep 2017 on two lower sides; swap it
  for `laga_july_2024_2018` if a dated summer flush matters more.
- Chanterelles in late June 2022 vs 2025 region-wide: late-June births in southern and western Abruzzo
  in 2025 (Funghi Magazine) spoil the lower side.
- Teramo hills late October vs late September 2021, and Teramano oak hills vs L'Aquila and Chieti in
  early October 2020: vague places or weak wording, and the season gate would decide the first.
- Marsica June to mid-September 2025 below normal (an ASL mycologist: "un po' inferiori"): too weak.
- Region-wide statements for 2024 (late September good, late October poor), the Chietino-Isernino black
  porcini of August 2024, late August 2024 on the Gran Sasso and Majella: national bulletins, 2024
  already carries three contrasts.
- A 2020 crowd of pickers at Sante Marie, Cappadocia and Tagliacozzo (Il Centro): a crowd, not a flush.
- Ceppo vs the other Teramo mountains, autumn 2023: conflicts with Funghi Magazine's "buone ... sul
  Gran Sasso", so only the Laga half went into `laga_vs_southwest_2023_october`.
- Laga vs Gran Sasso, mid-September 2025: the Gran Sasso side is only implied.

**Year picture from the sources** (context, not scored):

- **2016**: very good on the Laga. Chanterelles from late May, "molti" in mid-June; porcini
  "tantissimi" in early July and a "sfungata storica" in early August (ovoli present); dry collapse late
  August–early September; restart late September, clou at the turn of October; "un'annata molto
  soddisfacente".
- **2017**: disastrous. June fair (chanterelles), then "estremamente deficitaria" July, "tremendamente
  secco" August with beeches shedding leaves, rain only mid-September, a "morto" wood in October, "il
  più brutto della mia vita".
- **2018**: very wet May–June, cold; July poor; good late August on the Laga (Ceppo modest in
  mid-August, the Vomano side and Campotosto better); "proliferazione straordinaria" in the Marsica at
  the turn of September.
- **2019**: drought in July–August (Coldiretti Abruzzo: −50–60 %); a historic early-September flush in
  the chestnut, oak and hornbeam woods of the Laga, then the beech; dry October, season over by
  ~21 October.
- **2020**: early summer boletes of poor quality but chanterelles abundant, births around the Laga and
  PNALM in early July (FM); August "secco mai visto"; rain 24 August; warm woods (Valle Castellana)
  productive with ovoli from ~7 September, the Ceppo poor; most of Abruzzo low in mid-September (FM);
  some births in the Teramo oak hills in early October (FM).
- **2021**: rising births Marche–Abruzzo–Molise in late June (FM); late-August storms gave a short oak
  and chestnut flush (Chieti above all) while the Gran Sasso and Majella beech stayed idle; dry late
  September; good births in the inner hills on the Marche border in late October (FM).
- **2022**: porcini after the 9–10 June rains and C. pallens in late June "dalle Marche al Molise" (FM);
  edulis in mid-September (FM); "grandi nascite" in mid-October; on the Laga a season "da incorniciare",
  over by ~23 October, then a dry late October.
- **2023**: late, cold June; little rain at the start of September; a short flush from local showers
  around 20 September (the Ceppo favoured); Abruzzo "sfigati" by cold winds in late September; in
  October only the Gran Sasso and Laga still producing (FM 12 Oct), the rest blocked by Tramontana; the
  Ceppo still giving porcini on 20 October.
- **2024**: dry spring and a poor mid-June (FM); an exceptional B. aestivalis and C. pallens flush in
  early–mid July on the Laga; sporadic in mid-August; "delirio fungino" in late August–early September
  (Ceppo record, ovoli "invadente"); good late September–early October (FM); poor late October
  (Garbino).
- **2025**: snowy winter and wet spring, good St George's mushrooms; on the Laga chanterelles started
  then "zero assoluto" by mid-June, June–July "poverissimi d'acqua" (some *B. pinophilus*); births in
  southern and western Abruzzo in late June (FM); Marsica somewhat below average through mid-September
  (ASL); a beech flush on the Laga in mid-September (the chestnut-oak belt almost empty); over by early
  October after a cold week.

**Areas** (woodland cells on the grid of 2026-09-28, built from the regional forest-type map):

| area | comuni (woodland cells) | total |
|---|---|---|
| `laga_teramana` | Valle Castellana (116), Rocca Santa Maria (49), Cortino (45), Crognaleto (102), Torricella Sicura (29) | 341 |
| `ceppo` | Rocca Santa Maria (49) | 49 |
| `valle_castellana` | Valle Castellana (116) | 116 |
| `marsica` | Carsoli (90), Pereto (31), Rocca di Botte (24), Oricola (10), Sante Marie (34), Tagliacozzo (44), Cappadocia (45), Castellafiume (22), Scurcola Marsicana (0), Magliano de' Marsi (26), Massa d'Albe (0), Avezzano (2), Capistrello (37), Canistro (17), Civitella Roveto (36), Civita d'Antino (26), Morino (49), San Vincenzo Valle Roveto (39), Balsorano (48), Luco dei Marsi (24), Trasacco (15), Collelongo (40), Villavallelonga (65), Lecce nei Marsi (57), Gioia dei Marsi (41), Bisegna (33), Ortona dei Marsi (8), Pescina (1), Cerchio (0), Collarmele (3), Aielli (5), Celano (1), Ovindoli (27), San Benedetto dei Marsi (0), Ortucchio (13) | 913 |
| `abruzzo_southwest` | Carsoli (90), Pereto (31), Rocca di Botte (24), Oricola (10), Sante Marie (34), Tagliacozzo (44), Cappadocia (45), Castellafiume (22), Capistrello (37), Canistro (17), Civitella Roveto (36), Civita d'Antino (26), Morino (49), San Vincenzo Valle Roveto (39), Balsorano (48), Collelongo (40), Villavallelonga (65), Lecce nei Marsi (57), Gioia dei Marsi (41), Bisegna (33), Pescasseroli (70), Opi (40), Villetta Barrea (16), Civitella Alfedena (30), Barrea (36), Alfedena (38), Scanno (58), Scontrone (6), Castel di Sangro (44) | 1,126 |
| `chieti_hills` | province CH (550) excluding the Majella-park comuni Civitella Messer Raimondo (6), Fara Filiorum Petri (0), Fara San Martino (13), Gamberale (6), Guardiagrele (8), Lama dei Peligni (12), Lettopalena (9), Montenerodomo (13), Palena (54), Palombaro (5), Pennapiedimonte (22), Pizzoferrato (16), Pretoro (19), Rapino (10), Roccamontepiano (5), Taranta Peligna (6), Torricella Peligna (10); largest left: Castiglione Messer Marino (19), Carunchio (19), Schiavi di Abruzzo (18), Rosello (14) | 336 |
| `gran_sasso_majella` | Pietracamela (23), Fano Adriano (28), Isola del Gran Sasso d'Italia (42), Castelli (31), Farindola (26), Caramanico Terme (26), Sant'Eufemia a Maiella (14), Roccamorice (12), Salle (12), Serramonacesca (12), Pacentro (37), Campo di Giove (16), Cansano (28), Palena (54), Pennapiedimonte (22), Fara San Martino (13), Pretoro (19), Pizzoferrato (16) | 431 |
| `abruzzo` | provinces '*' | 3,782 |

Small areas: `ceppo` (49 cells) is the smallest; many single comuni in `chieti_hills` and `marsica`
have under 15 woodland cells, but the areas as wholes are large. Every area has woodland cells.

## Open questions

- **The high beech in midsummer.** Every Abruzzo source puts summer porcini, the "rossi" and the
  chanterelles in the beech in July and August. With the raised bands, *B. reticulatus* carries the
  July beech up to 1,500 m, but above that the group leans on *B. edulis*' ramp and *B. pinophilus*,
  whose windows leave a gap from 20 July to 15 August. A summer window at altitude (as Piemonte's
  Alpine window for *B. edulis*) would need records the region does not have; the sanity contrasts in
  July and August on the Laga will show whether it is missing.
- **Conifer plantations and hop-hornbeam.** Together 23 % of the woods on the grid; the evidence against
  porcini there is an absence in Abruzzo sources and the Marche and Karst evidence. The montane
  plantings include fir and spruce, which is why *B. edulis* keeps 0.3 there (Marche 0.1).
- **The coast.** 18 of the 31 records come from around the Torino di Sangro holm-oak wood, a 100 ha
  reserve. They support the lowland autumn windows of *B. aereus* and the chanterelles, but a single
  wood and observer cannot say how common that is along the Abruzzo coast, and 16 of them fall in
  cells outside the woodland mask (downy oak on the map), so the backtest will not use them.
- **Black porcino and beech.** 0.3 is a compromise between the book ("in simbiosi con quercia e
  faggio") and the blog (new under beech in 2024); it gives a pure beech cell full habitat credit, and
  only the altitude band keeps it off the high beech.
- **Montane juniper and mugo pine.** The region config leaves the montane juniper scrub (20,795 ha,
  median 1,643 m) and the Mugheta appenninica (median 2,010 m) out of the woods. The mugo is above
  every altitude band. The montane juniper was 70 % of what the card's mapping put in `macchia`; with
  it out, `macchia` is the oak-belt Juniperus oxycedrus scrub, and the black-porcino affinity went
  from 0.1 to 0.3 and the ovolo's back to Tuscany's 0.3 (Porcini and Ovoli tables).
- **Substrate.** The Laga sandstone is the acid exception in a limestone region; the forest map's
  types carry it (subacidophilous downy oak, acidophilous chestnut), but no rule reads substrate. A
  lithology layer would let the disabled gallinacci rules and the ovolo's siliceous preference be
  tested.
- **Leads not read.** The book "Funghi d'Abruzzo" (M. R. Tieri and N. Tieri) itself, beyond the AMEP
  cards; the Parco Nazionale d'Abruzzo's list of 342 fungi (its site disallows crawlers, see below);
  Granito & Lunghini (2011) on the macrofungi of the Simbruini beech woods next to the Valle Roveto
  (no abstract online); the Apennine tree-line table in Bonanomi et al. (2020) per mountain group.
- **Sites that block AI agents.** The Parco Nazionale d'Abruzzo, Lazio e Molise (`robots.txt`
  disallows all crawlers but a few search engines) and the regional tourism site abruzzoturismo.it
  (disallows ClaudeBot) were opened once before this was noticed; nothing from them is cited or used.

## References added for Abruzzo

| id | kind | verified | used for |
|---|---|---|---|
| `lr_abruzzo_34_2006` | institutional | verified | picking rules (ovolo, *Boletus* minimum size), presence |
| `regione_abruzzo_ctf2009` | institutional | verified | forest types, altitude belts, substrates, chestnut and conifer localities, the tree-line beech |
| `amep_funghi_abruzzo_tieri` | society | verified | per-taxon hosts and months in Abruzzo, with Abruzzo photo localities |
| `funghiteramani_blog` | web | verified | the Laga season sequence, belts, hosts, weather lore (folklore) |
| `bonanomi2020_treeline` | peer-reviewed | verified | Apennine beech tree line (mean 1,589 m, over 2,000 m on some peaks) |
| `nordal_porcini_italia2024` | web | verified | "tra i 1.200 e i 1.800 metri" for Abruzzo porcini (folklore) |
| `mushma_occurrence_check_abruzzo_2026` | analysis | verified | Abruzzo record counts, months, located elevations and habitats |
| `mushma_abruzzo_forest_composition_2026` | analysis | verified | habitat areas and elevations on the regional forest map; grid elevation, slope, pH |

Existing references the Abruzzo changes lean on: `camm_massi_polidori2022` (hop-hornbeam named for
the summer and black porcini; *B. pinophilus* on "terreni molto acidi"), `mrak2025_mycorrhiza`
(planted black pine's partners), `funghimagazine_carpino_nero2026` (acid-soil porcini absent from
calcareous hop-hornbeam, folklore), `regione_umbria_funghi2013` (*B. aereus* also under beech),
`olariaga2017` (the Mediterranean chanterelle segregates), `iucn_caesarea2019` (ovolo "only seldom
above 1200 m").
