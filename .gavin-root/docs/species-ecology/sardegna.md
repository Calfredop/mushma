# Species ecology: Sardegna (regional appendix to species-ecology.md)

Research date: 2026-09-30 (dates Europe/Rome, units metric). Card: `region-sardegna-species.md`
(child of `region-sardegna.md`). Rule files: `api/src/api/config/species/sardegna/`. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Sardinia,
what changed and why. It covers **fruiting conditions only**: nothing here is about edibility or
identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(97 added for Sardinia, plus the region card's rain check, in one block right after the Sicilia
entries, listed at the end of this page). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every number
is a prior for the backtest; season windows, altitude bands and habitat affinities stay frozen
(`model.yaml`, `backtest.frozen_factor_kinds`).

Sicily (`sicilia.md`) is the nearest precedent, then Calabria, Campania and Puglia.
[Where Sardinia departs](#where-sardinia-departs-from-sicily-and-central-italy) compares them.

## Summary

1. **Three groups and five keys are kept; *B. pinophilus* is dropped.** Porcini, ovoli and
   gallinacci all fruit in Sardinia. *B. pinophilus* has no Sardinian record on iNaturalist or GBIF,
   no page in the forestry agency's catalogue, only reader reports in Funghi Magazine, and none of
   its hosts (beech, fir, chestnut forest, natural mountain pine). Sardinia has **no regional law**
   on picking: the national L. 352/1993 and municipal rules apply.
2. **Sardinia has no porcini census.** The evidence is the forestry agency's pages, a review of
   Sardinian mycology (`sar_comandini2018_mycovisions`), plantation surveys, 57 iNaturalist records
   of the six keys, about 140 Funghi Magazine bulletins with a Sardinia paragraph and about 75
   local-press articles. Most season evidence is folklore; the host evidence is plausible.
3. ***B. aereus* leads.** "abbondante nei boschi della Sardegna" (the forestry agency), 18 of the 25
   porcini records, the default "Porcino Nero" of every bulletin. *B. reticulatus* is second; *B.
   edulis* is rare, in the upper cork and holm oak, the Barbagia's deciduous oak and chestnut and
   the Limbara's conifer plantations, and in mild winters.
4. **The woods are four fifths oak** (INFC 2015). Holm and cork oak (`evergreen_oak`) are 54 % of
   the grid's wooded area, downy oak s.l. 10 %; the chestnut (971 ha) is mostly hidden in the
   deciduous oak; beech, silver fir and spruce are absent. The conifer reforestation
   (`mediterranean_pine`, 16 %) is weak porcini ground (0.1), except for *B. edulis* in the upland
   plantations (0.3); the wild olive and carob woods (`mixed_broadleaf`, 7 %) and the tamarisk
   thickets move to non-host for every key.
5. **The macchia counts.** Three fifths of the Sardinian `macchia` class is evergreen-oak matorral
   and *Erica*-*Arbutus*-*Cistus* macchia: secondary for *B. aereus* and the ovolo (0.6), marginal
   for *B. reticulatus* (0.3) and *B. edulis* (0.1). The eucalyptus (1.3 %) has no Sardinian porcini
   report and stays 0.
6. **The season: a spring flush, a deep summer gap, an autumn that starts with the first good rain
   and peaks in November.**
   - Porcini Neri in April-June every year Funghi Magazine covers (2018-2025), in the lowland
     macchia and oak; the lower *B. aereus* window now opens on 1 April.
   - July-August nearly empty; the weather rules make the gap.
   - The autumn starts from late August (2018, 2024) to early November (2021, 2023); November holds
     22 % of all Sardinian fungi records on iNaturalist (Tuscany 13 %).
   - *B. aereus*, *B. edulis* and the chanterelles run into December and, in mild winters, January;
     the windows end on 10 January (chanterelles 15 February).
7. **The altitude bands follow the oak belt to 1,400 m.** The woods run from the coast to about
   1,550 m, with 96 % of woodland cells below 1,000 m. *B. aereus* is full to 1,100 m, the ovolo to
   1,000 m, *B. reticulatus* to 1,200 m; *B. edulis* and the chanterelles keep Tuscany's bands.
8. **Weather rules are all Tuscany's.** No Sardinian study ties fruiting to rain or temperature in
   numbers. The bulletins' lore (flushes about ten days after a good rain, repeated light rain
   better than storms, the maestrale wasting the rain) fits the Tuscan rules; the wind is recorded
   as a known gap.
9. **16 sanity contrasts** (13 porcini, 1 ovoli, 2 gallinacci), 10 of them resting mainly on Funghi
   Magazine, the rest on the local press and a hiking blog; 19 sightings on woodland cells for the
   backtest.

## Sardinia in brief

**Woods.** The grid maps Sardinia's woods from the ISPRA-Regione Carta della Natura habitat map
(1:50,000, 2011, University of Sassari; `sar_ispra_cnat_sardegna`, `config/regions/sardegna.yaml`,
settled in parallel by the region card). Its CORINE Biotopes classes say both the broad group and
the kind of wood. The grid (built 2026-09-30, `mushma_sardegna_woodland_grid_2026`) has 5,141
woodland cells of 25,026, 20.5 %, the highest share of any region so far, and 573,104 ha of forest
against INFC 2015's bosco of 626,140 ha (-8.5 %).

This table is **which habitat holds which Sardinian tree** (whole-map areas as the region card reads
them; grid shares are of the wooded area over woodland cells, macchia included):

| habitat key | Carta della Natura classes | ha | grid share | dominant cells (median height) | notes |
|---|---|---|---|---|---|
| `evergreen_oak` | leccete sarde 45.317 (195,034), leccete supramediterranee 45.323 (22,574), sugherete 45.21 (103,597) | 321,205 | 53.7 % | 3,097 (511 m) | holm oak two thirds, cork oak one third; Baunei, Bitti, Pula, Orgosolo, Urzulei, Sinnai, Alà dei Sardi, Buddusò |
| `mediterranean_pine` | conifer plantations 83.31 (94,522); Aleppo, stone and maritime pine 42.84, 42.83, 42.82 (2,169); wooded dunes 16.29 (3,489) | 100,180 | 15.5 % | 857 (567 m) | the post-war reforestation, maritime, Aleppo and stone pine with black pine, cedar, cypress and firs on the mountains (Limbara, Monte Lerno, Gennargentu, Marganai, Montarbu); CLC IV files 73 % of 83.31 as Mediterranean pine |
| `macchia` | silicicolous garrigue and macchia 32.3 (244,095), olive and lentisk macchia 32.211 (126,833), evergreen-oak matorral 32.11 (117,958), olive and lentisk matorral 32.12 (68,445), juniper 32.13 (33,774), calcicolous 32.4 (29,890), smaller classes | about 621,000 | 11.5 % | 56 | not woodland in the grid mask: it counts only inside woodland cells |
| `deciduous_oak` | querceti a roverella della Sardegna 41.72 (31,205), querceti mediterranei a roverella 41.732 (32,986) | 64,191 | 9.9 % | 585 (726 m) | *Q. pubescens* s.l.: *Q. ichnusae*, *Q. congesta*, *Q. virgiliana*, *Q. dalechampii*; holds most of the Barbagia's chestnut orchards; Fonni, Bonorva, Desulo, Macomer, Bono, Aritzo, Tonara |
| `mixed_broadleaf` | wild olive and carob woods 45.1 (57,038); hop-hornbeam 41.81 (208), holly 45.8 (53), aspen and birch 41.D1 (4) | 57,303 | 7.2 % | 463 (273 m) | thermo-Mediterranean olive woods, not oak; Paulilatino, Carbonia, Muravera |
| `exotic_broadleaf` | eucalyptus plantations 83.322 | 21,991 | 1.3 % | 76 (138 m) | Teulada, Siliqua, Palmas Arborea, Arborea |
| `riparian` | *Fraxinus angustifolia* 44.63 (5,671), poplar 44.61, willow 44.13, alder 44.91 | 6,759 | 0.4 % | | |
| `transitional_woodland_shrub` | tamarisk and oleander 44.81 (7,632), shrub willows 44.12 (2,740), broom and bramble classes | about 10,800 | 0.3 % | | not the regrowth of oak and chestnut the Tuscan class stands for |
| `chestnut` | *Castanea sativa* woods 41.9 | 971 | 0.2 % | 7 (1,005 m) | Desulo, Tonara, Santu Lussurgiu; the rest of the orchards are too small for 1:50,000 (the Aritzo cell reads deciduous oak 0.94, chestnut 0.02) |
| `other_conifer` | yew woods 42.A7 (Sos Niberos) | 100 | 0.0 % | | |

Sardinia has no `beech`, `fir_spruce`, `mountain_pine` or `mixed_broadleaf_conifer` class: beech,
silver fir and spruce are absent from the native woods, and the Carta della Natura has no mixed
class. Those affinities stay in the rule files and score no cell. Left out of the grid: the wooded
pasture (84.6, the open cork- and downy-oak dehesa, 112,668 ha), as CLC's agroforestry is
everywhere, and the Gennargentu's spiny oromediterranean heath (31.75, 13,682 ha).

INFC 2015 (`sar_infc2015`) has the same picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| holm oak | 255,463 | 40.8 % |
| cork oak | 152,755 | 24.4 % |
| sessile, downy and pedunculate oak | 87,780 | 14.0 % |
| other evergreen broadleaves | 38,004 | 6.1 % |
| Mediterranean pines | 34,633 | 5.5 % |
| other conifers | 13,055 | 2.1 % |
| other deciduous | 7,743 | 1.2 % |
| black, laricio and loricato pine | 5,225 | 0.8 % |
| hygrophilous | 3,359 | 0.5 % |
| chestnut | 1,866 | 0.3 % |
| plantations (broadleaf 24,392, conifer 1,493) | 25,885 | 4.1 % |

INFC has no beech, fir, spruce, larch, Scots pine, Turkey oak or hop-hornbeam category in Sardinia.
Holm and cork oak are two thirds of the bosco; with the downy oak, oaks are four fifths.

**Altitude belts:**

| type | altitude (m) and where | source |
|---|---|---|
| cork oak | "le sugherete dominano ... da pochi metri sul livello del mare fino a 800-1000 m" in the Gallura and on the Buddusò, Alà dei Sardi and Bitti plateaus; the granite series at 200-550 m (Gallura, Baronia, Mandrolisai, Ogliastra, Sarrabus, Sulcis-Iglesiente), the volcanic series at 50-700 m (Logudoro, Monte Acuto, Montiferru, Campeda, Alà, Bitti, Osidda) | `sar_bacchetta2009_vegetazione` |
| holm oak | thermophilous series to 400 m; the calcifuge series at 500-1,000 m (Limbara, Alà, Montiferru, Marghine-Goceano, Barbagie, Ogliastra, Monte Arci, Sette Fratelli, Linas, Monte Arcosu); montane holm oak with holly above 900 m (summits of the Limbara, Monte Lerno, Alà, Punta Masiennera in the Goceano, Montiferru), "climaciche tra i 700 e i 1200 metri"; calcicolous holm oak of the Supramonte, Monte Albo, the Tacchi and the Marganai | `sar_bacchetta2009_vegetazione` |
| deciduous oaks | *Q. ichnusae* at 300-950 m on basalt, andesite and trachyte (Logudoro, Marghine-Goceano, Barbagia di Ollolai and Belvì, Mandrolisai, Ogliastra); *Q. congesta* "tra 750 e 1400 m" on neutral-acid rock (Marghine, Monte Rasu, Barbagie, Gennargentu), with relict yew and holly; calcicolous *Q. virgiliana* at 100-400 m | `sar_bacchetta2009_vegetazione` |
| chestnut | "castagneti in forma di boschi ceduati, alternati a boschi di querce caducifoglie e Corylus avellana" in the western Gennargentu, upper Ogliastra and the Barbagia di Belvì; introduced "in ancient times"; the grid's few chestnut cells at a median 1,005 m | `sar_bacchetta2009_vegetazione`; `sar_comandini2018_mycovisions`; `mushma_sardegna_woodland_grid_2026` |
| pines | native only on the south-western coast (Aleppo pine, stone pine on the Portixeddu dunes) and at Monte Pino-Monti Ultana (maritime pine); the rest is plantation, lowland to the mountain tops (Limbara 1,061 m reads pine 1.00) | `sar_bacchetta2009_vegetazione`; `mushma_sardegna_woodland_grid_2026` |

On the grid the woods run from the coast to about 1,550 m: woodland cells median 517 m (p5-p95
136-967 m), only 3.9 % above 1,000 m and 0.6 % above 1,200 m. The evergreen oak sits at a median 511
m (201-904), the deciduous oak at 726 m (321-1,138). Sardinia's belts are Tuscany's without the
beech and fir: the oaks reach 1,400 m, as in Calabria, but most of the woods are below 900 m.

**Substrate.**
- Acid rock dominates the porcini country: the granite of the Gallura, Limbara, Alà-Buddusò-Bitti
  plateaus, Sette Fratelli and Sulcis; the schist and granite of the Gennargentu and Barbagie; the
  volcanics of the Montiferru, Marghine-Goceano, Logudoro and Monte Arci. The limestone is the
  Supramonte, the Tacchi of the Ogliastra and Sarcidano, the Marganai and the Sassarese tablelands
  (`sar_bacchetta2009_vegetazione`).
- The Sardinian deciduous oaks grow mostly on acid rock; only the *Q. virgiliana* series is
  calcicole.
- Soil is not modelled in v1 (the grid's SoilGrids pH median is 6.56).

**Climate.**
- **Two seasons.** The climate is "bistagionale": over 75 % of the rain falls in October-March,
  maxima in November-December, July 3-17 mm at the 26 stations of `sar_bacchetta2009_vegetazione`.
  ARPAS (`sar_chessa_delitala1997_clima`): "Il passaggio fra le due stagioni è particolarmente
  marcato fra settembre ed ottobre", monthly totals jumping "da valori di 40-60 mm a valori di
  80-160 mm" in the wet zones; "luglio ed agosto sono i mesi più secchi".
- **Totals.** Mean annual rain 764 mm, rising "circa 90 mm ogni 100 m"; Cagliari 441 mm, Desulo
  1,134 mm, Genna Silana 1,119 mm, Alà dei Sardi 989 mm, Tempio Pausania 804 mm, Macomer 916 mm
  (`sar_bacchetta2009_vegetazione`); 1,300 mm on the Limbara plantation
  (`sar_ambrosio2015_limbara_abete`). The wet zones are the Gennargentu (Barbagie, Ogliastra), the
  central Gallura under the Limbara, the Campeda and the Iglesiente, with the Sarrabus in
  November-February; the Nurra and the Campidano are dry (`sar_chessa_delitala1997_clima`).
- **Wind.** "i venti dominanti nella nostra Isola sono il Ponente e il Maestrale"; strong winds are
  commonest in December-March (`sar_chessa_delitala1997_clima`).
- **Snow.** At Vallicciola on the Limbara (1,040 m) 14.1 snowfall days and 21 days of lying snow a
  year, November to April, snow rarely lasting more than one or two days
  (`sar_chessa_delitala1997_clima`). The snow and frost stoppers are kept.

**Regional law.** Sardinia has **no regional law** on picking epigeous mushrooms.
- ISPRA's regional sheet lists only the national framework law, L. 352/1993: "La raccolta dei funghi
  epigei non è disciplinata da alcuna legge regionale" (`sar_ispra2021_raccolta_funghi`, April
  2021).
- In September 2024 the GrIG still called Sardinia the "unica regione in Italia" without "alcuna
  regolamentazione regionale", "diverse proposte di legge regionale, ma finora nessuna è arrivata al
  momento del voto" (`sar_castedduonline_grig_funghi2024`).
- The latest bill, PL 170 of 19 June 2020 (`sar_consregsardegna_pl170_2020`), would have brought
  permits after a course, 3 kg a day for amateurs and 10 kg for professionals, no picking "durante
  le ore notturne" and no closed ovolo; it lapsed with the XVI legislature. An earlier bill (PL 104,
  2010) listed about 30 marketable species (`sar_comandini2018_mycovisions`). No mushroom law turned
  up in searches of the Council's site up to September 2026.
- So the national law and municipal ordinances apply. None of it changes where or when the fungi
  fruit; the bills confirm the porcini, ovolo and chanterelles as the island's picked species.

## Which porcini Sardinia has

The card's first question. Sardinia has no census like Sicily's: the evidence is the forestry
agency's pages, a review of Sardinian mycology, plantation surveys, 25 iNaturalist records and
forager lore. Together they say one thing.

1. ***B. aereus* leads** (plausible).
   - The forestry agency: "È un fungo tipicamente meridionale, abbondante nei boschi della
     Sardegna", "sotto latifoglie, soprattutto leccio e castagno e in associazione con macchia
     mediterranea (corbezzolo, erica)", Sardinian name "Cordolinu reali"
     (`sardegna_foreste_aereus`); "uno dei primi porcini che cresce sotto le leccete dopo estati
     piovose" (`sar_sdl_porcino_nero_monte_nieddu`).
   - Among the edible mycorrhizal fungi of the cork-oak surveys of 1966-1973
     (`sar_comandini2018_mycovisions`).
   - 18 of the 25 Sardinian iNaturalist porcini records, from the Gallura to the Sette Fratelli
     (`mushma_occurrence_check_sardegna_2026`).
   - A Cagliari forager (folklore): "Il più comune è B. aereus, abbastanza diffuso è B. reticulatus.
     Da noi sono molto più rari i ritrovamenti di edulis ed il pinophilus mi è sconosciuto"
     (`sar_funghiemicologia_forum_assemini2009`).
2. ***B. reticulatus* is the second porcino** (plausible). "Porcino d' estate", "Boschi di
   latifoglie, specialmente castagno", "Nasce in estate, più raramente in autunno"
   (`sar_sardegna_foreste_reticulatus`). The four iNaturalist records are autumn ones in the
   Montiferru and at Oschiri. The Funghi Magazine bulletins put "Estatini" in the Sardinian macchia
   in May (see the season).
3. ***B. edulis* is rare, without its Tuscan hosts** (plausible).
   - No beech, fir or spruce in the native woods; 971 ha of mapped chestnut.
   - The agency's catalogue of about 64 fungi has no *B. edulis* page
     (`sar_sardegna_foreste_catalogo_funghi`), and a 2025 Sardinian field guide's index goes from
     *B. aereus* (p. 213) straight to *B. reticulatus* (p. 214) (`sar_puddu2025_funghi_sardegna`,
     snippet-only).
   - On record: in the cork-oak surveys of 1966-1973 (the old concept may have been broad) and among
     the 63 macromycetes of the Limbara's *Abies cephalonica* plantations (Ruggero & Contu 2007, via
     `sar_comandini2018_mycovisions`); three iNaturalist records, 13 September 2024 at Tempio
     Pausania, 17 October 2018 at Orgosolo, 6 November 2018 at Santu Lussurgiu (448 and 970 m where
     located).
   - In mild winters (folklore): after the December 2022 rains "Le sorprese più grandi però sono
     state rappresentate dalle 2 varietà di Porcino che non ti attenderesti di certo di poter
     trovare nel cuore dell'inverno: Porcini Autunnali (Boletus edulis) ed i Rossi Porcini
     Pinicola", "il chimismo dei suoli granitici sardi è praticamente perfetto"
     (`sar_fm_2023_01_03`); "alcuni Porcini edulis tra la macchia e nei Corbezzoli ... pure in
     Sardegna" on 16 December 2023 (`sar_fm_2023_12_16`).
   - Kept, with its hosts retuned (below).
4. ***B. pinophilus* is not on record** (plausible): **dropped**.
   - No iNaturalist or GBIF record (`mushma_occurrence_check_sardegna_2026`), no agency page, and
     "mi è sconosciuto" for the Cagliari forager.
   - The lore is split (all folklore). Against: "completamente assente sulle isole ed il sud, ad
     eccezione di alcune zone della Sila" (`sar_fishingmania_porcini2020`, wrong for Sicily, where
     Vasquez's census has 8 records); granite "ovunque in Sardegna, ma qua il clima caldo-ventoso
     ... impediscono ai Porcini Rossi di potersi insediare sull'isola" (`sar_fm_2021_06_24`). For:
     Funghi Magazine's species page, "Segnalazioni sporadiche provengono anche dal Gennargentu
     (Sardegna), dove alcuni lettori di Funghimagazine hanno riferito la sua presenza in annate
     particolarmente fresche e umide" (`sar_fm_pinophilus_scheda`), and the winter 2022-23 "Rossi
     Porcini Pinicola" (`sar_fm_2023_01_03`). Reader reports without a specimen, a photograph on
     record or a place.
   - Its hosts are not here: no beech, fir or chestnut forest, no Scots pine, and the black pine is
     plantation (INFC 5,225 ha). In Sicily its records were in Etna's natural laricio and in Nebrodi
     black pine mixed with beech; Sardinia has neither.
   - If it fruits at all, it is on the Gennargentu and in the Limbara's and Monte Lerno's montane
     conifer plantations, where *B. edulis*'s marginal deciduous-oak and pine credit already scores
     cool, humid conditions. Re-adding it is a copy of the Tuscan file if Sardinian records turn up
     (Open questions).

**Where Sardinia departs from Sicily.** Sicily's census made *B. reticulatus* the leading porcino,
the one of the chestnut and the spring; Sardinia's evidence makes *B. aereus* the leading one, the
porcino of the holm and cork oak and the macchia, because the island has so little chestnut and no
beech. *B. edulis* keeps a small place (Sicily's Etna beech and birch have no Sardinian equivalent),
and *B. pinophilus* has none.

## Cork oak, holm oak and the macchia

**Cork oak** (card question: porcini, ovolo and chanterelle ground in the Gallura and on the Alà
plateau).
- Sardinia holds most of Italy's cork oak: 152,755 ha in INFC 2015, 103,597 ha of sugherete on the
  Carta della Natura plus the wooded pasture of 84.6.
- The first "modern" Sardinian mycology was of the cork-oak woods (Valsecchi & Corrias 1966, Corrias
  & Diana-Corrias 1972, Diana-Corrias & Corrias 1973, for the Stazione Sperimentale del Sughero of
  Tempio Pausania): over 200 species, and "Several noteworthy edible mycorrhizal mushrooms (ECM)
  associated to cork oak are: Amanita caesarea ... Boletus aereus, B. edulis and B. fragrans"
  (`sar_comandini2018_mycovisions`).
- *Boletus* mycorrhizas were found in natural cork-oak stands on granite (Oschiri) and not in grazed
  ones (`sar_seddaiu2026_sugherete`).
- The Sardinian ovolo and chanterelle records cluster in the Gallura's cork oak (Tempio Pausania,
  Aggius, Calangianus, Luras, Sant'Antonio di Gallura) and on the Alà plateau (see the cross-check).
- The Gallura's cork oak is where the press puts the late *B. aereus* ("Durante una passeggiata tra
  le sugherete", `sar_galluraoggi_nero2024`; "le zone con sugherete esposte al sole ... le più
  calde" on the Sette Fratelli in late November, `sar_us_settefratelli2021`).
- In the grid holm and cork oak share one key, `evergreen_oak`: a full host for *B. aereus* and the
  chanterelles, secondary for the ovolo (0.6, which already saturates), marginal for *B.
  reticulatus* and now *B. edulis* (0.3, saturating). Nothing separates cork from holm oak in the
  rules; the evidence does not ask for it.

**Holm oak.** The largest class (217,600 ha on the map, 255,463 in INFC) and the porcini ground of
the Supramonte, Ogliastra, Sulcis-Iglesiente, Sette Fratelli and Monte Arci. The agency names it
first for *B. aereus*.

**The macchia** (card question: does anything we score fruit under *Arbutus*, *Erica*, *Cistus*?).
- The Sardinian `macchia` is about 621,000 ha, but only a fraction inside woodland cells counts
  (11.5 % of their wooded area). It is two fifths silicicolous garrigue and macchia with *Cistus*,
  *Erica* and *Arbutus* (32.3), a fifth evergreen-oak matorral (32.11), and a third wild olive,
  lentisk and juniper (32.211, 32.12, 32.13).
- *B. aereus*: yes (plausible). The agency's "in associazione con macchia mediterranea (corbezzolo,
  erica)"; Funghi Magazine's spring bulletins find it in the Sardinian macchia (folklore); *Cistus*
  scrub yields *B. aereus* in Spain (`oria_de_rueda2008`). **0.6** (Tuscany 1.0, Sicily 0.3): the
  oak matorral and the ericaceous macchia are ground, the olive-lentisk third is not.
- *B. reticulatus*: "Estatini o aereus ... ben presenti nella macchia mediterranea, quindi in
  Sardegna" (`fm_sicilia_2018_05_09`, folklore): **0.3** (Tuscany 0.1).
- *B. edulis*: "alcuni Porcini edulis tra la macchia e nei Corbezzoli ... pure in Sardegna"
  (`sar_fm_2023_12_16`, folklore); *Cistus* scrub yields *B. edulis* in Spain: **0.1** (Tuscany 0).
- Ovolo: "Spesso compare in presenza di corbezzolo ed erica" (`sardegna_foreste_caesarea`); in
  September 2019 "spesso abbondanti nei boschi di Corbezzolo, più umidi rispetto ai boschi di Cerro"
  around the Gennargentu and in the south (`sar_fm_2019_09_20`, folklore): **0.6** (Tuscany 0.3).
- Chanterelles: kept at 0.3.
- Arbutus woods may be mapped as macchia (32.3) or as holm oak; either way the rules now score them.
- The *Cistus* macchia's own mycobionts (*Leccinellum corsicum*, *Lactarius cistophilus* and
  *tesquorum*, *Hebeloma cistophilum*, *Russula cistoadelpha*) are the agency's macchia list
  (`sar_sardegna_foreste_catalogo_funghi`) and the traditional Sardinian pick
  (`sar_comandini2018_mycovisions`); none is scored.

## The reforestation, the eucalyptus and the olive woods

- **Conifer plantations (`mediterranean_pine`, 100,180 ha, 15.5 % of the grid's wooded area).** The
  class holds the whole post-war reforestation, maritime, Aleppo and stone pine in the lowlands and
  hills, black pine, cedar, cypress and firs on the mountains; the grid cannot tell them apart (the
  region card files all of 83.31 here, as CLC IV mostly does). Its dominant cells are in porcini
  country: Alà dei Sardi, Buddusò, Bitti, Seui, Aritzo, Pattada (Monte Lerno), Orgosolo.
  - The Sardinian pine fungi on record are *Suillus*, *Lactarius deliciosus*, *sanguifluus* and
    *vinosus*, *Hydnum* (`sar_comandini2018_mycovisions`, `sar_sardegna_foreste_catalogo_funghi`):
    no porcino, no ovolo. *B. aereus* and *B. reticulatus* keep **0.1** (Tuscany 0.6 for *B.
    aereus*, as in Sicily), the ovolo 0.1.
  - *B. edulis* rises to **0.3**: it is on record in the Limbara's Greek fir plantations (Ruggero &
    Contu 2007), next to silver fir, cedar and black pine; the altitude band (0 below 200 m, full
    from 700 m) keeps the lowland pines out, so the rise acts on the 255 plantation cells above 700
    m.
  - The chanterelles keep 0.3 (maritime pine is a documented host).
  - A plantation cell with holm-oak or cork-oak regrowth keeps full porcini credit through its oak
    share (30 % of hosts saturates).
- **Eucalyptus (`exotic_broadleaf`, 21,991 ha).** No Sardinian report of porcini, ovoli or
  chanterelles under eucalyptus was found (Sicily's Erei reports have no Sardinian counterpart).
  Every key keeps Tuscany's 0 (the ovolo 0.05).
- **Wild olive and carob woods (`mixed_broadleaf`, 57,303 ha).** Thermo-Mediterranean *Olea*,
  *Ceratonia* and lentisk woods, arbuscular hosts: every key drops to **0.1** (Tuscany 0.3-0.6), as
  Calabria did for its *Alnus cordata* class (bar *B. reticulatus*).
- **Tamarisk, oleander and shrub willows (`transitional_woodland_shrub`).** Not the oak and chestnut
  regrowth the Tuscan class stands for: every key drops to 0.1.

## The Sardinian season

The card's first question: an autumn from October into December or January once the first rains
start it; a spring flush in April-June in the cork and holm oak; how late *B. aereus* runs. No
Sardinian study has dated records like Sicily's census; the evidence is Funghi Magazine's bulletins
(about 140 pages with a Sardinia statement, 2018-2025, `sar_fm_*`), the local press (`sar_*` news
items), 57 iNaturalist records and the ARPAS climate note.

1. **A spring flush: yes, every year, mostly *B. aereus*** (plausible).
   - Funghi Magazine reports Porcini Neri in Sardinia in April-June of every year it covers: in the
     macchia from April 2018 (`fm_sicilia_2018_04_30`), spreading "nei boschi di collina e montagna"
     by mid-June (`sar_fm_2018_06_16`); limited and wind-bound in late May 2019
     (`sar_fm_2019_05_30`); "assai precoci di inizio Maggio" before a "disastroso" May in 2021
     (`sar_fm_2021_05_30`); "Porcini Neri in quantità ... per lo più sui settori meridionali" on 25
     May 2023 and "ottime nascite di Porcini Neri" in mid-June 2023 (`sar_fm_2023_05_25`,
     `sar_fm_2023_06_15`); "prime nascite importanti" on 17 May 2024 and Neri and Estivi after the
     rains of 19-20 May 2024 (`sar_fm_2024_05_17`, `sar_fm_2024_05_30`); "Porcini neri belli e
     carnosi" in sheltered oases on 9 May 2025 (`sar_fm_2025_05_09`).
   - The local press agrees: "raccolte straordinarie" in the Gallura woods in late May 2018
     (`sar_olbiait_maggio2018`); a porcino "di inizio stagione" at Seulo on 1 June 2023
     (`sar_us_seulo2023`); the Gallura's mycological inspectorate, normally open October-March,
     reopened in June 2023 because the May rains "hanno ... alimentato la crescita dei funghi"
     (`sar_aslgallura_giugno2023`).
   - 4 of the 18 iNaturalist *B. aereus* records are from 5 April to 28 May, the located May ones at
     a median 152 m.
   - *B. reticulatus* joins in some springs ("Estatini", May 2018, May 2024); the first ovoli come
     in late May (`fm_sicilia_2024_05_30`; one iNaturalist record, 25 May 2020); the chanterelles
     from the end of April (`fm_sicilia_2018_04_30`) and in the wet June of 2018.
   - The spring flush is Sardinia's surest difference from central Italy: Tuscany's *B. aereus*
     windows open on 15 June and 1 July.
   - What changed: the lower *B. aereus* window opens on 1 April, full from 1 May; *B. reticulatus*
     opens on 15 April, full from 15 May; the ovolo opens on 15 May.
2. **A summer gap: yes, deep; the weather makes it.**
   - July 3-17 mm at the stations (`sar_bacchetta2009_vegetazione`); "luglio ed agosto sono i mesi
     più secchi" (`sar_chessa_delitala1997_clima`).
   - The bulletins: "nascite di funghi praticamente nulle" (3 July 2019), "nascite nulle ... in
     tutta la Sardegna continuamente sferzata da venti caldi e secchi" (20 August 2020), the spring
     flush of 2023 "giunte al capolinea" by 23 June "Tolto ... l'alto Gennargentu"
     (`sar_fm_2023_06_23`). The high Gennargentu, the inland lakes and sheltered hollows are the
     summer refuges (`sar_fm_2020_06_25`).
   - Rainy summers break it: "fuori stagione" porcini at Lanusei in early July 2018
     (`sar_us_lanusei2018`) and a "super produzione" in August 2018
     (`sar_castedduonline_agosto2018`).
   - No calendar gap is written in: the rain, heat and drying rules make it, as in Sicily.
3. **The autumn: from the first good rain, late August to early November; peak in November.**
   - ARPAS: "Il passaggio fra le due stagioni è particolarmente marcato fra settembre ed ottobre",
     40-60 mm a month becoming 80-160 mm in the wet zones (`sar_chessa_delitala1997_clima`).
   - The start moves by two months between years: late August 2018 and 2024 ("per lo più Porcini
     Neri/Bronzini", `sar_fm_2024_08_30`); mid-September 2019 (south first); late September-early
     October 2016 and 2020; mid-October 2022 (west first) and 2025; mid-November 2021 ("riscossa",
     `sar_fm_2021_11_19`); early November 2023 ("Quasi a sorpresa", `sar_fm_2023_11_09`).
   - Among all Sardinian fungi on iNaturalist November holds 22 % of the records (Tuscany 13 %) and
     October 13 % (24 %).
   - The press ties each start to a rain: "Dopo le prime piogge" (Telti, 1 October 2016), "grazie
     alla pioggia di ieri" (Sette Fratelli, 2 October 2016), "La stagione delle piogge è arrivata
     prorompente nel Montiferru" (13 October 2022), "Dopo le piogge cadute abbondanti il 26 ottobre"
     a carpet of *B. aereus* at Gonnosfanadiga by 14 November 2024.
   - A flush can be short: in the Montiferru "la stagione dei porcini dura solo qualche settimana"
     (`sar_lns_montiferru2016`); in the Arburese the October 2020 window "si è definitivamente
     chiusa" by 31 October (`sar_nalife_ottobre2020`); at Monti and Berchidda the porcini "volge al
     termine" on 21 October 2018 while "è possibile raccogliere degli ottimi ovuli".
   - The rain-trigger lags do this; nothing in the calendar has to.
4. **How late *B. aereus* runs: into December, in mild years January.**
   - "da noi Novembre è ancora il mese dei porcini" (a Cagliari forager, 2009).
   - December 2022: "A dicembre le prime segnalazioni di ritrovamenti di Porcini Neri-Bronzini"
     after an autumn drought, with *B. edulis* between Christmas and early January
     (`sar_fm_2022_12_21`, `sar_fm_2023_01_03`); December 2023: "alcuni Porcini edulis" in the
     coastal macchia (`sar_fm_2023_12_16`); the Gallura's inspectorate extended into January 2024
     (`sar_aslgallura_proroga2023`).
   - Cold ends it: on the Sette Fratelli on 20 November 2021 "le temperature per i porcini sono già
     critiche" (`sar_us_settefratelli2021`).
   - What changed: *B. aereus*'s lower window is full to 30 November and ends on 10 January, as in
     Sicily; *B. edulis*'s is full to 30 November and ends on 10 January (Tuscany 15 November and 20
     December); the chanterelles' lowland window is full to 31 December and ends on 15 February.
5. **The wind.** The bulletins blame the maestrale and the dry winds for many failed flushes ("In
   Sardegna la presenza dei Porcini Neri è soggetta al vento", May 2019; "il vento ... sta
   distruggendo ogni tentativo di nascite", October 2021) and find the good ones in sheltered woods
   (`sar_fm_2020_10_23`). The drying stopper's ET0 stands for wind only in part; the *B. aereus*
   file records it as a known gap (`wind_after_rain`).

**Where Sardinia departs from Sicily.** Sicily's spring flush is *B. reticulatus* at 850-1,500 m in
chestnut, Turkey oak and beech; Sardinia's is *B. aereus* in the lowland macchia and oak. Sicily's
autumn peaks move between September and November by year; Sardinia's starts as late as November in
dry years and its fungal records peak in November. Both run *B. aereus* into December.

## Occurrence cross-check (Sardegna)

Queried 2026-09-30 (`mushma_occurrence_check_sardegna_2026`):
- **iNaturalist**: place 13071 ("Sardegna, IT"), verifiable records.
- **Elevations**: from the Open-Meteo elevation API, for open, non-obscured records with an accuracy
  of 1 km or better.
- **GBIF**: `gadmGid=ITA.14_1`. Mostly iNaturalist copies, plus 6 soil-DNA samples of *B. aereus*
  from one Santa Giusta site (excluded by the keys) and a few "Citizens for FunDive" records.
- Aggregates, dates and comune names only; no coordinates are stored.

Sardinia has 5,934 iNaturalist fungi records (Tuscany 19,151), 69 % of them from 2021 on.

| taxon | iNat n | Apr | May | Sep | Oct | Nov | Dec-Feb | located: median (range) |
|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 3 | | | 1 | 1 | 1 | | 448 and 970 m (n=2) |
| *B. reticulatus* | 4 | | | | 2 | 2 | | 769 m (n=1) |
| *B. aereus* | 18 | 1 | 3 | 5 | 5 | 4 | | 320 m (5-758), n=10 |
| *B. pinophilus* | 0 | | | | | | | |
| *A. caesarea* | 16 | | 1 | 4 | 5 | 6 | | 439 m (0-938), n=11 |
| *Cantharellus* | 16 | | 2 | 3 | | 6 | 5 | 319 m (25-691), n=7 |
| all fungi (share, %) | 5,934 | 7 | 9 | 6 | 13 | 22 | 15, 8, 5 | |

The chanterelles are *C. alborufescens* 5, *C. pallens* 5, *C. ferruginascens* 1 and 5 at genus
level; no *C. cibarius* s.s.

What the records show:
- **The season peaks in November.** Among all Sardinian fungi November holds 22 % of the records and
  December 15 %; in Tuscany October holds 24 % and November 13 %. The Sardinian season runs about a
  month later than the Tuscan one, as the rain does.
- ***B. aereus* has a spring**: 4 of 18 records in April-May (5 April 2020 at Palmas Arborea, 9 May
  2025 at Alghero, 25 May 2023, 28 May 2020 at Siniscola); the located May ones at a median 152 m.
- **The ovolo is late**: 6 of 16 records in November, the latest on 19 November; one in late May
  (25 May 2020, Sant'Antonio di Gallura).
- **The chanterelles run into winter**: records on 2-30 November, 21-30 December, 27 January and 14
  February, and two in May.
- **Few records to validate.** 57 records of the six keys (Sicily 49, Tuscany 290), 7 of them before
  2010. The region card counts 19 sightings of the five kept keys on woodland cells, all but one in
  evergreen-oak cells. The backtest will say little.

## Where Sardinia departs from Sicily and central Italy

Sicily's rules (`sicilia/`) and Sardinia's start from the same Tuscan files.

| factor | Tuscany | Sicilia | Sardegna | why Sardinia differs |
|---|---|---|---|---|
| keys | six | six | **five: *B. pinophilus* dropped** | no record, no host (Puglia did the same) |
| `macchia` for *B. aereus* | 1.0 | 0.3 | **0.6** | three fifths of the Sardinian class is oak matorral and Erica-Arbutus-Cistus macchia; the agency names corbezzolo and erica |
| `macchia` for *B. reticulatus*, the ovolo, *B. edulis* | 0.1, 0.3, 0 | 0.1, 0.3, 0 | **0.3, 0.6, 0.1** | "Estatini o aereus ... nella macchia"; ovoli "nei boschi di Corbezzolo"; winter *B. edulis* "tra la macchia e nei Corbezzoli" (all folklore) |
| `mixed_broadleaf`, every key | 0.3-0.6 | 0.3 (porcini) | **0.1** | the class is wild olive and carob woods here |
| `transitional_woodland_shrub`, every key | 0.3-0.6 | 0.1-0.3 | **0.1** | tamarisk, oleander and shrub willows here |
| `mediterranean_pine` for *B. aereus* | 0.6 | 0.1 | 0.1 | same move: no porcino in the Sardinian pine fungi |
| `mediterranean_pine` for *B. edulis* | 0.1 | 0.1 | **0.3** | the class holds the Limbara's montane fir, cedar and black pine plantations, where *B. edulis* is on record |
| `evergreen_oak` for *B. edulis* | 0.1 | 0.1 | **0.3** | the cork-oak surveys list it; winter finds on the granite (folklore) |
| `deciduous_oak` for *B. edulis* | 0.3 | 0.1 | **0.3** (kept) | the class holds the Barbagia chestnut and the montane Q. congesta |
| `deciduous_oak` for the chanterelles | 0.3 | 0.3 | **0.6** | Sardinian downy oaks grow on acid rock; the class holds the chestnut |
| `exotic_broadleaf` for *B. aereus*, *B. reticulatus* | 0 | 0.1 | **0** | no Sardinian eucalyptus report |
| `evergreen_oak` for the ovolo | 0.6 | 0.6 | 0.6 | already saturates |
| *B. aereus* windows | upland 15 Jun-31 Oct, lowland 1 Jul-15 Dec, handover 400-600 m | lowland from 15 Apr, upland from 15 May, lowland to 10 Jan, handover 1,000-1,200 m | **lowland from 1 Apr, full 1 May**-30 Nov, to 10 Jan; upland as Sicily; **handover 800-1,000 m** | spring Porcini Neri every year from April; few woods above 1,000 m |
| *B. reticulatus* window | 1 May → 1 Jun … 30 Sep → 15 Nov | 15 Apr → 15 May … 31 Oct → 15 Dec | 15 Apr → 15 May … **15 Nov → 20 Dec** | the Sardinian records are October-November, to 30 November |
| *B. edulis* window | 1 Jul → 1 Sep … 15 Nov → 20 Dec | kept | 1 Jul → 1 Sep … **30 Nov → 10 Jan** | winter finds in December-January (folklore) |
| ovolo window | 1 Jun → 1 Sep … 5 Nov → 30 Nov | 15 May → 1 Sep … 15 Nov → 10 Dec | as Sicily | 6 of 16 records in November; late-May ovoli |
| chanterelle lowland window | 15 Apr → 10 May … 15 Dec → 25 Jan | kept | 15 Apr → 10 May … **31 Dec → 15 Feb** | records in December, January and February |
| *B. aereus* altitude | … 800 → 1,250 | … 1,400 → 1,800 | … **1,100 → 1,450** | oaks to 1,400 m; woods to about 1,550 m |
| *B. reticulatus* altitude | 0 → 150 … 1,100 → 1,500 | … 1,700 → 2,000 | … **1,200 → 1,550** | deciduous oak to 1,400 m |
| *B. edulis* altitude | 200 → 700 … 1,600 → 1,900 | 400 → 800 … 2,000 → 2,250 | **kept** | records at 448 and 970 m |
| ovolo altitude | … 750 → 1,100 | … 1,000 → 1,350 | … 1,000 → 1,350 | same move; records to 938 m |
| chanterelle altitude | … 1,000 → 1,700 | … 1,400 → 1,900 | **kept** | records to 691 m |

Two things set Sardinia apart from Sicily:
- **No chestnut and no beech to speak of.** Sicily's porcini split by belt, *B. reticulatus* in the
  chestnut, *B. edulis* in the beech and birch. Sardinia's woods are four fifths oak, and *B.
  aereus* leads everywhere below 1,000 m.
- **The macchia and the lowland spring count more.** Sicily's census found no porcino in scrub;
  Sardinia's agency, bulletins and records put *B. aereus*, the ovolo and the chanterelles in the
  Erica-Arbutus macchia and the coastal oak from April.

From central Italy: the season is a month later in the autumn (peak November, not October), there is
a spring flush in the lowland oak and macchia, and the windows run into January.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*)

**Decisions.**

| key | factor | Tuscany | Sardegna | why | confidence |
|---|---|---|---|---|---|
| *aereus* | season | upland 15 Jun → 1 Aug … 30 Sep → 31 Oct; lowland 1 Jul → 1 Sep … 15 Nov → 15 Dec; handover 400-600 m | upland 15 May → 1 Jul … 31 Oct → 30 Nov; lowland **1 Apr → 1 May … 30 Nov → 10 Jan**; handover **800-1,000 m** | spring Porcini Neri every year (folklore, 4 of 18 records); peak November; December finds | plausible (weak) |
| *aereus* | habitat `macchia` | 1.0 | **0.6** | olive-lentisk third holds no host | plausible |
| *aereus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3, 0.6 | **0.1** | olive and carob woods; tamarisk and oleander | plausible |
| *aereus* | habitat `mediterranean_pine` | 0.6 | **0.1** | no porcino among the Sardinian pine fungi | plausible |
| *aereus* | altitude | … 800 → 1,250 | … **1,100 → 1,450** | oaks to 1,400 m | plausible |
| *reticulatus* | season | 1 May → 1 Jun … 30 Sep → 15 Nov | **15 Apr → 15 May … 15 Nov → 20 Dec** | spring "Estatini" (folklore); autumn records to 30 Nov | plausible (weak) |
| *reticulatus* | habitat `macchia` | 0.1 | **0.3** | "Estatini ... nella macchia mediterranea, quindi in Sardegna" | folklore |
| *reticulatus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.6 | **0.1** | no hazel, oak or chestnut in them here | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | 0 → 150 … **1,200 → 1,550** | deciduous oak to 1,400 m, chestnut to 1,100 m | plausible |
| *edulis* | season | 1 Jul → 1 Sep … 15 Nov → 20 Dec | 1 Jul → 1 Sep … **30 Nov → 10 Jan** | winter finds 2022-23 and December 2023 | folklore (tail) |
| *edulis* | habitat `evergreen_oak` | 0.1 | **0.3** | cork-oak surveys; Tempio record; winter finds | plausible (weak) |
| *edulis* | habitat `mediterranean_pine` | 0.1 | **0.3** | Limbara montane plantations; altitude band keeps lowland pine out | plausible (weak) |
| *edulis* | habitat `macchia` | 0 | **0.1** | "tra la macchia e nei Corbezzoli" | folklore |
| *edulis* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3 | **0.1** | as above | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | kept | records 448 and 970 m | plausible |
| all three | weather, stoppers, growth clock | — | kept | no Sardinian numbers | as Tuscany |

Kept on purpose:
- ***B. edulis* in deciduous oak at 0.3.** Sicily dropped it to 0.1, but Sardinia's deciduous-oak
  class holds the Barbagia chestnut and the Q. congesta woods at 750-1,400 m, the island's coolest
  broadleaf ground.
- **The three porcini as full hosts of `chestnut`.** 971 ha, but the 7 cells it dominates are the
  Desulo and Tonara orchards.

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.** In Voglino's list of 1893, in the cork-oak surveys of 1966-1973, photographed in
  mixed holm and cork oak at Santadi (`sar_comandini2018_mycovisions`); "Predilige i boschi caldi di
  latifoglie (Castanea, Quercus). Spesso compare in presenza di corbezzolo ed erica"
  (`sardegna_foreste_caesarea`).
- **Records.** 16 on iNaturalist, 25 May and 27 September-19 November, 0-938 m, median 439 m: the
  Gallura cork oak, the Alà plateau, Padru, the Sette Fratelli, the Sulcis coast, Cuglieri.
- **Season** (folklore). Autumn ovoli come with the first rains, ahead of the porcini: "Sui monti
  attorno al Gennargentu non sono mancate le prime nascite di Ovoli, spesso abbondanti nei boschi di
  Corbezzolo" and "Molto scarse le nascite invece di funghi Porcini" (`sar_fm_2019_09_20`,
  `sar_fm_2019_09_27`); porcini and ovoli together on the Sette Fratelli on 2 October 2016
  (`sar_castedduonline_settefratelli2016`); 5.6 kg of ovoli at Monte Nieddu on 7 October
  2016 (`sar_olbiait_nieddu2016`); "ottimi ovuli" at Monti and Berchidda as the porcini ended on 21
  October 2018 (`sar_olbiait_monti_berchidda2018`); at Castiadas on 30 October 2018 "in una radura
  ben esposta al sole, al limite di un bosco di lecci, ad un'altezza di circa 500 metri"
  (`sar_lns_castiadas_ovolo2018`); "Per tutto il mese di novembre è facile trovare ancora gli Ovoli"
  (`sar_funghiemicologia_forum_assemini2009`). First ovoli on sale from Sardinia in late May 2024
  (`fm_sicilia_2024_05_30`).

**Decisions.**

| factor | Tuscany | Sardegna | why | confidence |
|---|---|---|---|---|
| season | 1 Jun → 1 Sep … 5 Nov → 30 Nov | **15 May** → 1 Sep … **15 Nov → 10 Dec** | late-May ovoli; 6 of 16 records in November | plausible (weak) |
| habitat `macchia` | 0.3 | **0.6** | corbezzolo and erica (agency; bulletins, folklore) | plausible |
| habitat `transitional_woodland_shrub`, `mixed_broadleaf` | 0.6, 0.3 | **0.1** | tamarisk and oleander; olive and carob | plausible |
| altitude | … 750 → 1,100 | … **1,000 → 1,350** | hosts to 1,400 m in a warmer climate; records to 938 m | plausible (weak) |
| deciduous oak, chestnut 1.0; evergreen oak 0.6; conifers ≤ 0.1 | — | kept | "Castanea, Quercus" | strong (hosts) |
| weather rules | — | kept | no Sardinian numbers | as Tuscany |

## Gallinacci (*Cantharellus* s.l.: "galletti", "gallinacci")

**Regional evidence.**
- **Which species.** The Sardinian iNaturalist records are *C. alborufescens* (5) and *C. pallens*
  (5), one *C. ferruginascens*, five to genus: the Mediterranean segregates of holm and cork oak.
  "C. cibarius" is in Voglino's list of 1893 and the 2010 bill's list of marketable species
  (`sar_comandini2018_mycovisions`). The forestry agency has no chanterelle page, and the
  traditional Sardinian pick did not include them.
- **Places.** The Gallura (Tempio Pausania's Stazzo Sambucheddu, Aggius's Abba Fritta, Padru, Loiri
  Porto San Paolo, Aglientu), the Montiferru (Santu Lussurgiu under chestnut, and under "Quercus
  pubescens, Q.suber"; Scano di Montiferro), the Monte Arci (Morgongiori), Oristano and Cagliari.
- **Season.** Records in September, November (6), December (3), January and February (14 February
  2016, Morgongiori) and May (2). Folklore: the first "Galletti" in Sardinia by 30 April 2018,
  "insoliti ritrovamenti di Galletti" in June 2018, "Galletti" in the November 2021 riscossa, "molti
  Galletti/Gallinacci" in December 2022-January 2023, Galletti with the Porcini Neri in early
  October 2024.

**Decisions.**

| factor | Tuscany | Sardegna | why | confidence |
|---|---|---|---|---|
| season (lowland) | 15 Apr → 10 May … 15 Dec → 25 Jan | 15 Apr → 10 May … **31 Dec → 15 Feb** | December-February records; November-December peak of all fungi | plausible (weak) |
| habitat `deciduous_oak` | 0.3 | **0.6** | Sardinian downy oak on acid rock; holds the chestnut | plausible |
| habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3 | **0.1** | olive and carob; tamarisk and oleander | plausible |
| chestnut, evergreen oak 1.0; pines 0.3; macchia 0.3; altitude | — | kept | the records are in holm and cork oak country, 25-691 m | plausible |
| soil pH, lithology | disabled | kept disabled | | plausible |

## Weather rules: why none changed

- **Rain amount and lag.** No Sardinian source gives a rain amount or lag in numbers. The bulletins
  date flushes about ten days after a good rain (the spring of 2024: the rains of 19-20 May, "quasi
  ovunque oltre i 15/20 mm con punte fino a 30/40 mm", and on 31 May "Dov'è piovuto dopo il 19
  stanno già nascendo", `sar_fm_2024_05_30`), which fits the Tuscan porcini lag (ramp from 6 days,
  full from 10).
- **The autumn start.** ARPAS: "Il passaggio fra le due stagioni è particolarmente marcato fra
  settembre ed ottobre" (`sar_chessa_delitala1997_clima`). The rain trigger and the 30-day rain as a
  percentage of the cell's normal find it without a calendar rule.
- **Summer drought.** Deeper than in Tuscany (July 3-17 mm). The porcini's 30-day rain is relative
  to each cell's normal, so it adapts; the ovolo's and chanterelles' 30-day ramps are absolute
  (25-75 and 15-70 mm) and will rarely be full in a Sardinian summer, as in Sicily.
- **Wind.** The maestrale and ponente dominate (`sar_chessa_delitala1997_clima`); the drying stopper
  (ET0) already stands for wind, dry air and sun. The bulletins blame the wind for many failed
  flushes (`sar_fm_2019_05_30`, `sar_fm_2021_10_24`) and find the good ones in sheltered woods
  (`sar_fm_2020_10_23`); the *B. aereus* file records it as a known gap (`wind_after_rain`).
- **Cold.** Snow on the Limbara and Gennargentu from November to April, rarely lying more than a day
  or two; the frost and snow stoppers are kept.
- **Rain scale.** The region card fitted its own on 272 ARPAS stations, 1.00 + 0.34 per km
  (`mushma_sardegna_arpas_gauge_check_2026`); the rules' rain thresholds read the scaled rain.
- **Repeated light rain beats storms** (folklore): "dove le piogge sono state ripetute e non
  violente ... ora si iniziano a raccogliere i primi frutti" (`sar_fm_2024_08_30`); porcini "Molto
  scarse" after rains "più che violente ma brevissime" (`sar_fm_2019_09_27`). The 30-day rain driver
  and the chanterelles' rain-frequency driver already reward it.

## Groups and keys

**Dropped: *B. pinophilus*** (see [Which porcini Sardinia has](#which-porcini-sardinia-has)). No
Sardinian record on iNaturalist or GBIF, no page in the forestry agency's catalogue, unknown to a
Cagliari forager, and none of its hosts (beech, fir, chestnut forest, Scots or natural laricio pine)
grows here. As in Puglia, the porcini group keeps three keys (*B. edulis*, *B. reticulatus*, *B.
aereus*) in the shared tie-break order.

**Kept: the ovolo and the chanterelles** (card question: are they frequent enough?). Yes.
- The ovolo: 16 iNaturalist records from the Gallura, the Alà plateau, the Sette Fratelli, the
  Sulcis and the Montiferru, in the first Sardinian list (Voglino 1893), in the cork-oak surveys, on
  the forestry agency's pages, and on sale from Sardinia in late May (`fm_sicilia_2024_05_30`).
- The chanterelles: 16 iNaturalist records of *C. alborufescens* and *C. pallens* in the Gallura,
  Montiferru and Monte Arci, in Voglino's list and in the 2010 bill's list of marketable species.
  The forestry agency has no chanterelle page, and the traditional Sardinian pick did not include
  them (`sar_comandini2018_mycovisions`): they are less sought than on the mainland, not absent.

`beech`, `fir_spruce`, `mountain_pine` and `mixed_broadleaf_conifer` are not on the Sardinian map
but stay in the rule files, as in every region; they score no cell.

## Effect on the woodland cells

On the 5,141 woodland cells of the grid (`mushma_sardegna_woodland_grid_2026`), habitat and altitude
gates only (weather not included):

| key | habitat gate full: Tuscany → Sardegna | altitude gate full: Tuscany → Sardegna | mean habitat × altitude: Tuscany → Sardegna |
|---|---|---|---|
| *B. edulis* | 6.4 % → 32.6 % | 26.7 % → 26.7 % | 0.25 → 0.54 |
| *B. reticulatus* | 45.8 % → 54.6 % | 92.6 % → 93.6 % | 0.82 → 0.82 |
| *B. aereus* | 98.5 % → 79.5 % | 84.7 % → 98.4 % | 0.95 → 0.90 |
| ovolo | 81.8 % → 77.5 % | 79.7 % → 96.1 % | 0.84 → 0.89 |
| chanterelles | 95.8 % → 88.9 % | 96.1 % → 96.1 % | 0.98 → 0.94 |

What the table shows:
- **The oak country is untouched.** On the 2,993 cells at least half evergreen oak the best
  porcino's habitat × altitude is 1.00 (*B. aereus*), and 1.00 on the 704 cells at least 30 %
  deciduous oak or chestnut.
- **The porcini group loses the olive woods and the lowland plantations.** The best porcino's gates
  are 0.5 or more on 92.1 % of cells (Tuscan rules 99.2 %); the 408 cells below are dominated by
  wild olive and carob (247), conifer plantations (112) or eucalyptus (49).
- **The upland plantations keep their porcini through *B. edulis*.** On the 255 cells at least half
  conifer plantation above 700 m the best porcino averages 0.96 (*B. edulis* 0.93); on the 535 below
  700 m, 0.75 (*B. aereus*, through the oak and macchia around the pines).
- ***B. aereus*'s altitude gate opens**: full on 98.4 % of cells (84.7 % with the Tuscan band).

## Sanity contrasts

`sardegna/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written
down on 2026-09-30, before any Sardinia score existed. The schema has no group field: contrasts are
porcini unless their id starts with `ovoli_` or `gallinacci_`. "Normal" is the area's mean over
2017-2025.

**Areas.** Every comune was checked against the ISTAT 2025 list; all are in Sardinia, and every area
has woodland cells on the grid.
- `sardegna`: the whole region (`provinces: ['*']`), for the bulletins' island-wide verdicts.
- `gennargentu`: 20 comuni, Fonni, Desulo, Tonara, Aritzo, Belvì to Seui, Villagrande Strisaili,
  Orgosolo, Sorgono, Atzara, Meana Sardo (830 woodland cells, median 828 m).
- `gallura_limbara`: Tempio Pausania, Calangianus, Luras, Aggius, Luogosanto, Bortigiadas,
  Sant'Antonio di Gallura, Telti (229 cells).
- `montiferru_marghine`: the Montiferru (Santu Lussurgiu, Seneghe, Cuglieri, Bonarcado, Scano di
  Montiferro) and the Marghine-Goceano (Bono, Bolotana, Macomer, Silanus, Burgos, Anela, Bultei,
  Illorai, Nughedu San Nicolò, Bottidda, Esporlatu).
- `ovest`: the Montiferru and the Linas-Arburese (Arbus, Guspini, Gonnosfanadiga, Villacidro,
  Fluminimaggiore); `est`: the Supramonte, Ogliastra and Baronia (21 comuni, Oliena and Dorgali to
  Jerzu, Siniscola and Posada).
- `linas_arburese`; `sette_fratelli` (Burcei, Sinnai, Castiadas, San Vito, Villasalto, Muravera,
  Maracalagonis); `monte_arci` (Morgongiori, Ales, Pau, Marrubiu, Villa Verde, Usellus, Palmas
  Arborea, Santa Giusta, Siris, Masullas).
- `sud`: the Sulcis-Iglesiente without the Linas (14 comuni, Iglesias to Pula, Capoterra, Assemini,
  Uta), the Sette Fratelli and the Monte Arci.
- `gennargentu_ogliastra_sud`: the Gennargentu, the upper Ogliastra (Ulassai, Jerzu, Osini, Gairo,
  Lanusei, Ussassai), the Sulcis and the Sette Fratelli, for the ovoli of September 2019.

**The sources.**
- Funghi Magazine's national bulletins, read through Wayback Machine captures (the live site shows a
  captcha). A research agent read 391 captures (196 dated bulletins, 2018-2025); about 140 say
  something about Sardinia. Their Sardinia paragraphs come from readers and name sectors more often
  than places. Every quote below was re-checked here against the captured text.
- The local press: L'Unione Sarda, La Nuova Sardegna, Cagliaripad, Casteddu Online (whose older
  pages print a 2017 migration date; the real date is in the page metadata), Olbia.it, Gallura Oggi,
  the ASL Gallura, and NAlife, a hiking blog of the Arburese. About 75 articles were opened; many
  are giant-porcino stories, used only where they say how the season went. Every quote was
  re-checked.
- ANSA, Rai TGR, Sardinia Post and the Today network (CagliariToday, SassariToday) block AI agents
  in robots.txt and were not fetched; ANSA's 11 September 2018 item is used only through the
  IteNovas reprint.

| id | higher | lower | main source (second sources) | weakness |
|---|---|---|---|---|
| `gennargentu_2018_2020_early_september` | Gennargentu 2018, 25 Aug-15 Sep | same, 2020 | [IteNovas (ANSA) Sep 2018](https://www.itenovas.com/in-tavola/3431-funghi-sardegna-2018-e-annata-eccezionale.html): "già i primi funghi cominciano a vedersi nelle zone di montagna come Desulo, Tonara e Fonni" (Casteddu Online 2018-08-23; FM 2018-08-31; FM 2020-08-20, 2020-09-04; Campagna Amica 2020-09-14 "Cestini vuoti per adesso anche in Sardegna") | the 2020 side is island-wide |
| `sardegna_2018_2019_june` | Sardinia 2018, 5 Jun-5 Jul | same, 2019 | [FM 2018-06-16](https://web.archive.org/web/20220930220913/https://funghimagazine.it/aggiornamento-funghi-16-giugno-2018/): "Sardegna sempre protagonista" (FM 2018-07-01; FM 2019-07-03, 2019-07-08 "nascite ... quasi del tutto assenti") | one outlet |
| `sardegna_2023_2021_late_spring` | Sardinia 2023, 25 May-20 Jun | same, 2021 | [FM 2023-06-15](https://web.archive.org/web/20240417084120/https://funghimagazine.it/aggiornamento-funghi-16-06-2023/): "ottime nascite di Porcini Neri" (FM 2023-05-25; ASL Gallura 2023-06-09; L'Unione Sarda 2023-06-01; FM 2021-05-30 "disastroso", 2021-06-24) | FM's 15 June sentence is joint with Sicily |
| `sardegna_2023_timing_spring_vs_october` | Sardinia 2023, 25 May-20 Jun | same year, 1-25 Oct | [FM 2023-10-12](https://web.archive.org/web/20240521230836/https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "stendiamo un velo pietoso sulla siccitosa Sardegna" (FM 2023-05-25, 2023-06-15, 2023-10-27; ASL Gallura 2023-06-09, 2023-11-06) | tests the spring window against the autumn one |
| `sardegna_2023_timing_november` | Sardinia 2023, 10-25 Nov | same year, 1-25 Oct | [Cagliaripad 2023-11-19](https://www.cagliaripad.it/603472/autunno-ricco-di-grandi-porcini-ritrovamenti-a-ulassai-e-arbus/): "In Sardegna è un autunno ricco di porcini" (FM 2023-11-09; L'Unione Sarda 2023-11-13, 2023-11-14; Cagliaripad 2023-11-21; FM 2023-10-12) | FM 2023-11-09 has the south-east (Cagliaritano) still dry |
| `sardegna_2020_2021_october` | Sardinia 2020, 1-20 Oct | same, 2021 | [FM 2020-10-08](https://web.archive.org/web/20221201195648/https://funghimagazine.it/aggiornamento-meteofunghi-08-10-2020/): "La Sardegna sta vivendo un periodo abbastanza positivo" (FM 2020-10-23; NAlife 2020-10-31; FM 2021-10-09, 2021-10-24) | one outlet for the island |
| `gallura_vs_montiferru_marghine_2020_early_october` | Gallura 2020, 1-15 Oct | Montiferru and Marghine, same window | FM 2020-10-08: "i ritrovamenti migliori si possono fare nei settori Nord ed Est ... i settori Centroccidentali hanno avuto spesso forti venti" (FM 2020-10-23) | one bulletin; sectors, not comuni |
| `linas_arburese_2020_vs_2019_2025_october` | Linas-Arburese 2020, 1-15 Oct | same, 2019 and 2025 | [NAlife 2020-10-31](https://nalife.altervista.org/2020/10/31/ottobre-breve-guida-pratica-su-come-trovare-i-porcini-e-altro/): "quest'anno è nuovamente annata di porcini!" (NAlife 2019-10-05 "non c'è nemmeno traccia di qualche porcino"; NAlife 2025-10-12; FM 2025-10-16) | one pair of bloggers; 2019 is one walk on 5 October |
| `gallura_vs_sette_fratelli_2021_november` | Gallura 2021, 8-25 Nov | Sette Fratelli, same window | [L'Unione Sarda 2021-11-20](https://www.unionesarda.it/news-sardegna/provincia-cagliari/trova-un-porcino-da-un-chilo-sui-sette-fratelli-in-tanti-anni-mai-visto-uno-cosi-i9w0koet): "la pioggia nel sud Sardegna è arrivata tardi e le temperature per i porcini sono già critiche" (Olbia.it 2021-11-15 "Autunno piovoso, tempo di funghi"; La Nuova Sardegna 2021-11-22; FM 2021-11-19) | anecdotal; the Sette Fratelli forager still found a 1 kg porcino |
| `ovest_vs_est_2022_autumn` | west 2022, 10 Oct-25 Nov | east, same window | [FM 2022-11-05](https://web.archive.org/web/20240621071145/https://funghimagazine.it/aggiornamento-porcini-06-11-2022/): rains "sui settori occidentali, meno in quelli centrali, assai scarse sui settori orientali" (FM 2022-10-13; L'Unione Sarda 2022-10-13, Montiferru; FM 2022-11-19) | the November statements are partly forecasts |
| `sardegna_2024_2025_late_september` | Sardinia 2024, 20 Sep-10 Oct | same, 2025 | [FM 2024-10-03](https://web.archive.org/web/20260902134949/https://funghimagazine.it/funghi-04-10-2024-raccolte-di-porcini-ancora-strepitose-ecco-dove/): "stanno nascendo funghi Porcini non solo sui monti ma anche nelle foreste di collina e pure del piano" (FM 2024-09-27; L'Unione Sarda 2024-09-17; FM 2025-08-29, 2025-10-16; NAlife 2025-10-12) | the 2025 bulletins of 25 September and 23 October could not be read |
| `gallura_vs_sud_2024_november` | Gallura 2024, 20 Oct-20 Nov | south, same window | [Cagliaripad 2024-11-18](https://www.cagliaripad.it/631233/che-spettacolo-in-gallura-trovato-un-porcino-nero-di-quasi-2-kg/): "al Sud non ci sono state grandi nascite a causa della siccità al contrario del Nord" (Gallura Oggi 2024-11-23; Cagliaripad 2024-11-15) | two of the sources are the same foragers; a local flush at Gonnosfanadiga (Linas, not in `sud`) on 14 November |
| `monte_arci_2023_2024_november` | Monte Arci 2023, 5-25 Nov | same, 2024 | [Cagliaripad 2024-11-15](https://www.cagliaripad.it/631022/autunno-povero-di-grandi-porcini-piccoli-esemplari-a-monte-arci/): "Non è il grande autunno dei funghi porcini, come accaduto nel 2023" (Cagliaripad 2023-11-19; FM 2023-11-09) | the 2023 side is island-wide |
| `ovoli_gennargentu_sud_2019_2022_september` | Gennargentu, Ogliastra, Sulcis, Sette Fratelli 2019, 15-30 Sep | same, 2022 | [FM 2019-09-27](https://web.archive.org/web/20240519045618/https://funghimagazine.it/dove-cercare-funghi-porcini-nellultimo-weekend-di-settembre-i-funghi-di-ottobre-il-ritorno-delle-grandi-piogge/): "Buone, ed in alcuni casi anche abbondanti, le nascite di Ovoli" (FM 2019-09-20; FM 2022-09-15, 2022-09-23) | the 2022 side speaks of all fungi |
| `gallinacci_sardegna_2021_timing_november` | Sardinia 2021, 10-30 Nov | same year, 1-25 Oct | [FM 2021-11-19](https://web.archive.org/web/20240620084846/https://funghimagazine.it/funghi-porcini-novembre-2021/): "Galletti" in the Sardinian "riscossa" (FM 2021-10-09, 2021-10-24) | chanterelles named in a list |
| `gallinacci_sardegna_2022_timing_december` | Sardinia 2022, 10-31 Dec | same year, 1-31 Oct | [FM 2023-01-03](https://web.archive.org/web/20240614061006/https://funghimagazine.it/funghi-porcini-tutto-lanno/): "molti Galletti/Gallinacci ... anche nel cuore dell'inverno" (FM 2022-10-13, 2022-12-21) | the December side is a look back |

Candidates left out:
- Early October 2024 against early October 2023 (FM): kept only as the later windows above, because
  the late-September 2024 bulletins are missing from the archive.
- Late May 2023, south against north (FM 2023-05-25): the north side is a forecast.
- The semaforo tables (FM's traffic lights per Sardinian area, 26 captures): FM's own estimates from
  rain data and readers, partly model output.
- The Macomer "Santunna" show's species counts (153 in 2017, 200 in 2021, 230 in 2024): effort, not
  fruiting.
- The June 2017 Casteddu Online pieces (Vallermosa, Sette Fratelli): misdated October 2015 and 2016
  articles.
- Forecasts, sagre, giant porcini without a season verdict, rescues, fines and everything from 2026.

**Year picture from the sources** (context, not scored):
- **2016:** an early-October start after the first rains in the Gallura, the Montiferru and the
  Sette Fratelli, porcini and ovoli together (`sar_lns_telti2016`, `sar_lns_montiferru2016`,
  `sar_castedduonline_settefratelli2016`, `sar_olbiait_nieddu2016`).
- **2017:** thin: a start "È bastata un po' di pioggia" in late September (`sar_us_orroli2017`); a
  poor November at the Macomer show, "il clima ha influenzato pesantemente il numero di esemplari
  esposti" (`sar_cronachenuoresi_macomer2017`). Funghi Magazine's archive starts in 2018.
- **2018:** the wet year: spring from April in the macchia, June into the hills and mountains,
  "fuori stagione" porcini in July, an exceptional late August and September (Desulo, Tonara, Fonni,
  the Gallura), porcini waning in the Gallura by 21 October while the ovoli continued, "Le nascite
  di Neri e moltissimi altri funghi autunnali non si contano tra Sardegna, Sicilia, Calabria"
  (`funghimagazine_aggiornamento_2018_10_22`).
- **2019:** a dry, windy spring and summer; rain from late August; porcini in the south from
  mid-September, ovoli abundant in the Arbutus woods, porcini scarce to late September.
- **2020:** a modest spring; a very dry summer; a good first half of October, best in the north and
  east and the Arburese, over by the end of the month.
- **2021:** a disastrous May; drought and maestrale until November; the "riscossa" from
  mid-November, better in the Gallura than in the south.
- **2022:** porcini only in the south in spring; the driest summer "da decenni"; timid porcini in
  the west from mid-October, the west better than the east in November; Porcini Neri, *B. edulis*
  and chanterelles in December-January.
- **2023:** the best spring on record (late May-mid June); a dry October; porcini "quasi a sorpresa"
  from early November, a rich late November in the Barbagia, Ogliastra and Arburese.
- **2024:** a dry winter; a short late-May flush; Porcini Neri from late August; a good late
  September and October; in November the north better than the drought-hit south.
- **2025:** a real flush in early May; a dry summer; a weak October.

## Places, for the intro copy

Sourced areas:
- **Porcini** (mostly *B. aereus*, "porcino nero", Sardinian "cordolinu reali"):
  - The Gennargentu and Barbagia: Desulo, Tonara, Fonni, Aritzo, Seulo, Lodine, Tiana, Orgosolo; the
    high Gennargentu is the summer refuge.
  - The Gallura's cork oak and the Limbara: Tempio Pausania, Calangianus, Luras, Priatu, Telti,
    Sant'Antonio di Gallura; Monti and Berchidda on the Monte Acuto.
  - The Montiferru (Santu Lussurgiu, Scano di Montiferro, San Leonardo) and the Marghine (Badde
    Salighes, Bolotana).
  - The Ogliastra (Ulassai, Monte Armidda above Lanusei).
  - The south: the Sette Fratelli (Sinnai, Burcei), the Linas and Arburese (Gonnosfanadiga, Arbus,
    Montevecchio), the Marganai and Gutturu Mannu, the Monte Arci.
- **Ovoli:** the Gallura (Monte Nieddu, Tempio Pausania, Aggius, Calangianus, Monti and Berchidda),
  the Alà plateau, the Sette Fratelli and Castiadas, the Arbutus woods around the Gennargentu and in
  the south, the Sulcis coast.
- **Gallinacci:** the Gallura (Tempio Pausania, Aggius, Padru), the Montiferru and the Monte Arci.
- **Seasons:**
  - A spring flush of Porcini Neri in the lowland macchia and oak from April-May, in wet years into
    June and the hills; the first ovoli in late May.
  - A dry July-August, broken only by storms and on the high Gennargentu.
  - The main season from the first good autumn rain, late August to early November by year, peaking
    in November; *B. aereus* and the chanterelles into December and, in mild winters, January.

## Open questions and hand-offs

- **Habitat medians** (for the parent, answered by the build). The bands were read against the grid
  of 2026-09-30: evergreen oak median 511 m, deciduous oak 726 m, chestnut 1,005 m, woodland p95 967
  m, highest cell 1,384 m. No band cuts a host belt: *B. aereus* is full to 1,100 m, the ovolo to
  1,000 m, *B. reticulatus* to 1,200 m.
- **Forest area** (for the region card). The Carta della Natura gives 573,104 ha of forest on the
  grid, 8.5 % under INFC 2015's 626,140 ha, within the ±10 % the card asks. The wooded pasture
  (84.6, 112,668 ha of open cork and downy oak) is left out; if the backtest finds porcini sightings
  there, it is the first class to reconsider (`known_gaps.wooded_pasture` in the *B. aereus* file).
- **The chestnut is invisible.** The map files the Barbagia's chestnut orchards (Aritzo, Desulo,
  Tonara, Belvì) with the downy oak: 971 ha mapped, 1,866 ha in INFC, 772 ha of fruit orchards in
  the Region's land-use map (the region card's figure). The rules carry them through `deciduous_oak`
  (a full host for *B. aereus*, *B. reticulatus* and the ovolo, saturating for *B. edulis*,
  secondary for the chanterelles). A cell that is chestnut on the ground but oak on the map scores
  the same porcini.
- **The montane conifer plantations.** All of 83.31 is `mediterranean_pine`, the Limbara's fir,
  cedar and black pine included. *B. edulis* gets 0.3 there, the other porcini 0.1. If the region
  card can split the montane plantations (black pine, fir, cedar) into `mountain_pine` or
  `other_conifer`, *B. edulis* could take Tuscany's 0.6 there and 0.1 in the lowland pines.
- **The olive woods** (`mixed_broadleaf`, 7 % of the wooded area). At 0.1 for every key, 247
  woodland cells dominated by wild olive and carob fall below 0.5 on the best porcino's habitat and
  altitude gates. That is intended; the plantations (113 cells, low pine) and eucalyptus (49) are
  the rest.
- **Rain scale** (for the region card, done there). The region card fitted 1.00 + 0.34 per km on 272
  ARPAS stations (`mushma_sardegna_arpas_gauge_check_2026`): 1.07 at 200 m, 1.17 at 500 m, 1.27 at
  800 m (national 1.28 + 0.29). The reanalysis rains too often (1 mm or more on 28 % of days against
  the gauges' 21 %); the chanterelles' `rain_frequency` driver (days with 5 mm or more in 20) and
  the porcini's rain trigger may read it as wetter than it was. The absolute 30-day ramps of the
  ovolo and chanterelles see the scaled rain.
- ***B. pinophilus*** (dropped). If Sardinian records of it turn up (the Gennargentu readers'
  reports, the winter of 2022-23), re-add it from the Tuscan file with `deciduous_oak` and
  `mediterranean_pine` as marginal hosts and the Sardinian altitude band; until then *B. edulis*
  scores the same cool ground.
- **Slope and sun exposure.** Both stoppers are anchored on Tuscan grid percentiles. The Sardinian
  woodland cells run a median slope of 16.9° with 9.5 % above 25°, close to Tuscany's (median 16.6°,
  p90 26.2°), so the slope band is kept. The sun ratio's percentiles on the Sardinian grid were not
  computed here; the island is 2-4° further south, so the autumn sun ratios of steep south and north
  slopes spread a little less than in Tuscany.
- **The ovolo and chanterelle 30-day ramps** are absolute and were set on Tuscan climatology; the
  Sardinian lowlands are drier, so they will bind more often in September.
- ***B. edulis* under evergreen oak.** Raised to 0.3 on weak evidence (the cork-oak surveys of
  1966-1973, the Tempio record, winter folklore). With its cooler temperature band it can win the
  porcini group in cool late-autumn weather in the upper cork and montane holm oak; if the backtest
  shows it scoring holm oak the sightings do not support, lower it back to 0.1.
- **The backtest will be thin.** The region card counts 19 sightings of the five keys on woodland
  cells, all but one in evergreen-oak cells: porcini at Calangianus, Sant'Antonio di Gallura, Santa
  Giusta (Monte Arci), Tempio Pausania and Iglesias; ovoli at Alà dei Sardi, Sant'Antonio di
  Gallura, Sinnai, Calangianus and Uta; chanterelles at Scano di Montiferro, Domusnovas and
  Nurallao. The priors ship; the sanity contrasts are the better check.
- **Funghi Magazine carries most contrasts.** 10 of the 16 contrasts rest mainly on it; its Sardinia
  paragraphs come from readers and name sectors. The archive misses late September-October 2024 and
  mid-May to June 2025.
- **Leads not read.** The Sardinian mycological literature is mostly in print or behind
  ResearchGate: Valsecchi & Corrias (1966) and Corrias & Diana-Corrias (1972-1973) on the cork-oak
  macromycetes; Brotzu & Colomo (2007, 2009) *I funghi della Sardegna* and *Guida agli ambienti
  micologici della Sardegna*; Ruggero & Contu (2007) and Ruggero (2014) on the Limbara; Ambrosio et
  al. (2014) on the Limbara fir plantation; Contu's notes in *Micologia e Vegetazione Mediterranea*;
  Puddu (2025).

## References added for Sardegna

| id | kind | verified | used for |
|---|---|---|---|
| `sar_ispra2021_raccolta_funghi` | institutional | verified | no regional picking law |
| `sar_consregsardegna_pl170_2020` | institutional | verified | the lapsed 2020 bill |
| `sar_castedduonline_grig_funghi2024` | web | verified | no regional law in 2024; first rains of September 2024 |
| `sar_comandini2018_mycovisions` | peer reviewed | verified | review: cork-oak surveys, Limbara plantations, Voglino 1893, the 2010 bill, climate |
| `sar_bacchetta2009_vegetazione` | peer reviewed | verified | forest belts and altitudes, rain totals and seasonality |
| `sar_infc2015` | dataset | verified | forest area and categories |
| `sar_ispra_cnat_sardegna` | dataset | verified | the forest map and its classes |
| `mushma_sardegna_woodland_grid_2026` | analysis | verified | grid shares, elevations, dominant cells, slope |
| `mushma_occurrence_check_sardegna_2026` | analysis | verified | iNaturalist and GBIF counts, months, heights |
| `sar_sardegna_foreste_reticulatus` | institutional | verified | B. reticulatus hosts and season |
| `sar_sardegna_foreste_catalogo_funghi` | institutional | verified | the agency catalogue: no B. edulis, B. pinophilus or chanterelle page; conifer and macchia fungi |
| `sar_sdl_porcino_nero_monte_nieddu` | institutional | verified | B. aereus under holm oak after rainy summers |
| `sar_ambrosio2015_limbara_abete` | peer reviewed | verified | the Limbara conifer plantation |
| `sar_seddaiu2026_sugherete` | peer reviewed | verified | Boletus mycorrhizas in natural cork oak |
| `sar_funghiemicologia_forum_assemini2009` | web | verified | which porcino is commonest; November season; hosts (folklore) |
| `sar_fishingmania_porcini2020` | web | verified | B. pinophilus "assente sulle isole" (folklore) |
| `sar_puddu2025_funghi_sardegna` | monograph | snippet-only | a Sardinian guide lists B. aereus and B. reticulatus only |
| `sar_chessa_delitala1997_clima` | institutional | verified | ARPAS climate: seasons, wet zones, wind, snow |
| `sar_lns_telti2016` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_castedduonline_settefratelli2016` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_lns_montiferru2016` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_olbiait_maggio2018` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_lanusei2018` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_castedduonline_agosto2018` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_itenovas_annata2018` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_olbiait_monti_berchidda2018` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_lns_castiadas_ovolo2018` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_nalife_gonnosfanadiga2019` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_campagnamica_porcini2020` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_lns_intossicazioni2020` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_nalife_ottobre2020` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_bolotana_aereus2020` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_olbiait_calangianus2021` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_lns_calangianus2021` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_settefratelli2021` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_montiferru2022` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_seulo2023` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_aslgallura_giugno2023` | institutional | verified | season and sanity contrasts |
| `sar_aslgallura_novembre2023` | institutional | verified | season and sanity contrasts |
| `sar_aslgallura_proroga2023` | institutional | verified | season and sanity contrasts |
| `sar_castedduonline_gonnosfanadiga2023` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_lodine2023` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_tiana2023` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_cagliaripad_ulassai_arbus2023` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_cagliaripad_ulassai2023` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_castedduonline_gonnosfanadiga2024` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_cagliaripad_arci2024` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_cagliaripad_gallura2024` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_galluraoggi_nero2024` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_nalife_austis2025` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2018_06_16` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2018_07_01` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2018_08_31` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2019_05_30` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2019_07_03` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2019_07_08` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2019_09_12` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2019_09_20` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2019_09_27` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2020_06_25` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2020_08_20` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2020_09_04` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2020_10_08` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2020_10_23` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2021_05_30` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2021_06_24` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2021_10_09` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2021_10_24` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2021_11_19` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_08_26` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_09_15` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_09_23` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_10_13` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_11_05` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_11_19` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2022_12_21` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_01_03` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_05_25` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_06_15` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_06_23` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_10_12` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_10_27` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_11_09` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2023_12_16` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2024_05_17` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2024_08_30` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2024_09_27` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2024_10_03` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2025_05_09` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2025_08_29` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2025_10_16` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_2024_05_30` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_fm_pinophilus_scheda` | web | verified | B. pinophilus reader reports from the Gennargentu (folklore) |
| `sar_us_desulo2024` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_olbiait_nieddu2016` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_us_orroli2017` | web | verified | season lore and sanity contrasts (folklore) |
| `sar_cronachenuoresi_macomer2017` | web | verified | season lore and sanity contrasts (folklore) |
| `mushma_sardegna_arpas_gauge_check_2026` | analysis | verified | the region card's rain scale (added at its request) |

Existing references the Sardinian rules lean on and that were opened again:
`sardegna_foreste_aereus`, `sardegna_foreste_caesarea`, `fm_sicilia_2018_04_30`,
`fm_sicilia_2018_05_09`, `fm_sicilia_2024_05_30`, `funghimagazine_nascite_2026_04_23`,
`funghimagazine_nascite_2026_05_08`, `funghimagazine_aggiornamento_2018_10_22`; and, unopened,
`oria_de_rueda2008` (snippet-only, the Spanish *Cistus* yields) and the Tuscan levels and medians
(`mushma_habitat_share_2026`, `mushma_occurrence_check_2026`).
