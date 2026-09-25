# Species ecology: Liguria (regional appendix to species-ecology.md)

Research date: 2026-09-25 (dates Europe/Rome, units metric). Card: region Liguria. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Liguria
(`api/src/api/config/species/liguria/`), what changed and why. It covers **fruiting conditions
only**: nothing here is about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(14 added for Liguria, listed at the end). Confidence levels are the ones in
[`species-ecology.md`](../species-ecology.md): **strong**, **plausible**, **folklore**. Every
number is a prior for the backtest; season windows, altitude bands and habitat affinities stay
frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

## Summary

1. **All three groups are kept, with all six keys.** Liguria has porcini (four taxa), ovoli and
   gallinacci on record and in regional institutional sources. Ovoli are the least common but not
   absent: the Beigua park names "porcini ed ovoli" as the renowned mushrooms of its hinterland
   (Sassello, Urbe, Tiglieto; `parco_beigua_funghi2015`), the regional law gives *Amanita
   caesarea* its own 1 kg daily limit and bans picking closed ovoli (`lr_liguria_17_2014`, art. 4
   and 8), and Liguria has 24 iNaturalist ovoli records against 31 for the four porcini together
   (`mushma_occurrence_check_liguria_2026`).
2. **What changed is where the hosts are, not when or how the fungi fruit.** Liguria's beech and
   chestnut belts sit lower than Tuscany's (beech from 500–700 m, not 900 m), so the two
   beech-and-fir porcini (*B. edulis*, *B. pinophilus*) get lower altitude bands. Four habitat keys
   hold different trees in Liguria than in Tuscany (mixed woods are chestnut or oak with pine, not
   beech with fir; "Mediterranean pine" is mostly maritime pine; "other conifer" is mostly
   black-pine reforestation), so their affinities move for the taxa whose hosts they now contain.
3. **Season windows are all kept.** The Ligurian records (small: 1–46 iNaturalist records per
   key) and the regional pages agree with the Tuscan windows; nothing regional supports moving
   them.
4. **Weather rules are all kept.** No Ligurian or north-west Apennine study ties porcini, ovoli or
   gallinacci fruiting to rain or temperature in numbers. The only Ligurian quantitative porcini
   study (three Sassello plots, 2012–2014) found no local climate effect at plot scale
   (`ambrosio2024_dendrobiology`). The Ligurian autumn is wetter (`arpal_atlante_clima2013`); the
   porcini 30-day rain is already scored against each cell's own normal, so it adapts; the absolute
   30-day ramps of ovoli and gallinacci will simply be full more often in autumn.
5. **Evidence is thin.** Of the 14 new sources (all opened), 2 are peer-reviewed Ligurian studies, 7
   institutional (6 Ligurian plus the IUCN assessment), 3 forager or press pages (folklore) and 2
   our own analyses. No Ligurian source is quantitative about weather. The changes rest mostly on
   the regional forest-type atlas (plausible) plus single-site records.

## Liguria in brief

**Woods.** Measured on the Regione Liguria *Tipi forestali ed. 2025* map (IPLA legend) by the region
card (`mushma_liguria_forest_composition_2026`): land-use classes 311x+312+313 cover 352,600 ha.

| IPLA category | ha | share | habitat key |
|---|---|---|---|
| CA castagneti | 120,900 | 34 % | `chestnut` |
| OS orno-ostrieti | 62,900 | 18 % | `mixed_broadleaf` |
| FA faggete | 44,800 | 13 % | `beech` |
| QU querceti di roverella e rovere | 42,900 | 12 % | `deciduous_oak` |
| PC pinete di pino marittimo e d'Aleppo | 29,400 | 8 % | `mediterranean_pine` |
| LE leccete (a little sughera) | 22,300 | 6 % | `evergreen_oak` |
| PM pinete di pino silvestre (a little uncinato) | 9,200 | 3 % | `mountain_pine` |
| CE cerrete | 8,800 | 2 % | `deciduous_oak` |
| RI rimboschimenti (mostly pino nero; douglasia, abete rosso) | 6,700 | 2 % | `other_conifer` |
| LC lariceti (Alpi liguri) | 1,900 | 1 % | `other_conifer` |
| FR formazioni riparie / AB abetine / LM latifoglie mesofile | 1,400 / 900 / 500 | < 1 % each | `riparian` / `fir_spruce` / `mixed_broadleaf` |

Land-use 313 "boschi misti" (54,600 ha, mostly chestnut or oak with maritime or Scots pine) maps to
`mixed_broadleaf_conifer`, 323 macchia (13,500 ha) to `macchia`, 324 regrowth (22,800 ha) to
`transitional_woodland_shrub`.

**Altitude belts** (`rl_fotoatlante_tipi_forestali`, the interpretative atlas of the regional
forest-type map; `rl_tipi_forestali_2008` for the classification):

| type | altitude (m) |
|---|---|
| holm oak (xerophilous / mesoxerophilous), cork oak | 0–600 / 0–400, 0–200 |
| Aleppo pine; coastal maritime pine; inland maritime pine on ophiolites | 0–300; 0–600; 300–800 |
| thermophilous chestnut (var. maritime pine); fruit and acidophilous chestnut; neutrophilous chestnut | 100–500; 300–1000; 500–900 |
| downy oak (acidophilous, neutro-calcicolous); sessile oak; Turkey oak | 100–900; 500–1100; 200–1000 |
| hop-hornbeam | 100–1000 |
| beech: oligotrophic; mesotrophic and eutrophic; calcicolous | 700–1600; 500–1500; 800–1200 |
| Scots pine; mountain pine (*P. uncinata*) | 500–1600; 1400–1800 |
| silver fir; larch | 1300–1700; 1000–2000 |

Tuscany's beech belt is 900–1700 (1800) m (`rt_tipi_forestali_p4`): Ligurian beech comes down
several hundred metres lower, on the humid Apennine watershed.

**Climate** (`arpal_atlante_clima2013`, 94 rain and 34 temperature stations, 1961–2010). The
Levante is much rainier than the Ponente, in totals, rainy days and daily intensity. Autumn
(September–November) got rainier in 1981–2010 than in 1961–1990, the other seasons drier. The
province of Genova (outside Tigullio and Val d'Aveto) is the most exposed to intense daily rain. The
Ponente is milder than the Levante, and the coast has a smaller daily temperature range than the
interior. At Sassello (ARPAL station, 2012–2014) monthly rain averaged 97–155 mm, with months up
to 677 mm (`ambrosio2024_dendrobiology`).

## Occurrence cross-check (Liguria)

Queried 2026-09-25 (`mushma_occurrence_check_liguria_2026`): GBIF with `gadmGid=ITA.9_1`
(soil-DNA `MATERIAL_SAMPLE` rows excluded), iNaturalist place 96906 (verifiable), elevations from
the Open-Meteo elevation API for open, accurate (≤ 1 km) iNaturalist records only. Aggregates only;
no coordinates are stored. Enrichment = the taxon's monthly share of its records ÷ the monthly
share of all 5,132 Ligurian iNaturalist fungi records (> 1: over-represented for the effort).

| taxon | source | n | J | F | M | A | M | J | J | A | S | O | N | D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | GBIF | 10 | | | | | | | | | 2 | 8 | | |
| | iNat | 12 | | | | | | 1 | 1 | | 6 | 3 | 1 | |
| *B. reticulatus* | GBIF | 14 | 1 | | | | 3 | 2 | 2 | | 2 | 4 | | |
| | iNat | 14 | 1 | | | | 1 | 3 | | 1 | 4 | 4 | | |
| *B. aereus* | GBIF / iNat | 3 / 4 | | | | | | 0 / 1 | | | 1 / 2 | 2 / 1 | | |
| *B. pinophilus* | GBIF / iNat | 1 / 1 | | | | | | | | | 0 / 1 | 1 / 0 | | |
| four porcini | iNat enrichment | 31 | 1.0 | | | | 0.6 | 2.8 | 0.8 | 0.6 | 3.0 | 0.9 | 0.2 | |
| *A. caesarea* | GBIF | 11 | | | | | 1 | | 1 | | 4 | 4 | 1 | |
| | iNat | 24 | | | | | 1 | 1 | | 1 | 13 | 7 | 1 | |
| | iNat enrichment | | | | | | 0.8 | 0.7 | | 0.8 | 3.9 | 1.0 | 0.3 | |
| *Cantharellus* (genus) | GBIF | 29 | 1 | | | | | 4 | 2 | 1 | | 15 | 6 | |
| | iNat | 46 | 2 | | | | 2 | 6 | 3 | | 7 | 19 | 7 | |
| | iNat enrichment | | 1.4 | | | | 0.8 | 2.2 | 1.7 | | 1.1 | 1.5 | 1.1 | |

| taxon | located n | p10 | median | p90 | max (m) |
|---|---|---|---|---|---|
| *B. edulis* | 8 | 286 | 744 | 962 | 1057 |
| *B. reticulatus* | 10 | 363 | 681 | 1071 | 1120 |
| *B. aereus* | 1 | | 661 | | |
| *B. pinophilus* | 1 | | 1056 | | |
| *A. caesarea* | 17 | 275 | 454 | 676 | 781 |
| *Cantharellus* | 36 | 43 | 262 | 946 | 1533 |

The Ligurian iNaturalist records are recent (34 of 36 located *Cantharellus* and 17 of 17 ovoli from
2016 on). Presence-only, few and near roads and towns: they can confirm that a window or band holds
the records, not tune it.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence.**

- **Sassello plots** (`ambrosio2024_dendrobiology`, strong for presence, the only Ligurian
  peer-reviewed porcini site study; the fungal checklists of what are probably the same sites are in
  `ambrosio_zotti2015`). Three porcini sites surveyed 2012–2014 in April–June and
  September–November: a young chestnut coppice at 420–450 m (*B. edulis*), a Turkey-oak high forest at 340–380 m (*B. aereus*, *B. reticulatus*) and a beech
  high forest at 1000 m (*B. edulis*, *B. reticulatus*); 32, 50 and 73 porcini fruit bodies. Soil pH
  4.2–5.8 on calcschist, serpentine schist and conglomerate. At plot scale soil geochemistry, not the
  local climate, explained the fungal communities; at European scale the rain of the driest month
  was the main climatic predictor of *B. edulis* occurrence.
- **Hosts by valley** (institutional and folklore). The Aveto park: porcini picked "in boschi di
  castagno, cerro, faggio, carpino e frassino", beech porcini pale and elongated, chestnut porcini
  dark with a red stem (`parco_aveto_porcini`, plausible). Press and forager pages place porcini in
  the chestnut woods of the Fontanabuona, Valle Scrivia and Val Polcevera, and in chestnut and beech
  from Triora to Monte Ceppo and at Colle di Nava (`ilgiornale_boschi_liguri2010`, folklore). The
  *Fungo di Borgotaro* IGP area borders the Val d'Aveto and Val di Vara, and its host list includes
  "abete bianco e rosso, pino nero, silvestre ed altre specie di Pinus, duglasia"
  (`borgotaro_igp_2014`, plausible).
- **Season** (folklore). Ligurian pages: *B. edulis* "in piena estate ... fino ai primi freddi";
  *B. aestivalis* "tipicamente estiva, ma può essere incontrata già a Maggio"; *B. aereus* in
  thermophilous oak and chestnut, "anche in lecceta a pochi passi dal mare"; *B. pinophilus* "in
  tardo autunno, inverno fino all'inizio della primavera" (`liguriafood_funghi2018`). Another puts
  porcini "da maggio fino alla fine di ottobre", the "porcino nero" July–September, the mountain
  "porcino rosso" September to early November and lowland *B. edulis* late September to late
  October (`cacciatoridifunghi_liguria2023`). The Beigua park: "dopo le prime piogge di fine estate e
  per tutto il periodo autunnale" (`parco_beigua_funghi2015`, plausible).
- **Pines.** The IUCN assessment gives pines as *B. pinophilus*'s host, "pine forests and pine
  plantations of all ages" on acid, sandy soil (`iucn_pinophilus2019`, plausible), against the
  Italian sources' beech, fir and chestnut (`borgotaro_igp_rt`, `matteucci2008_micoponte`).

**Decisions.**

| key | factor | Tuscany | Liguria | why | confidence |
|---|---|---|---|---|---|
| *edulis* | altitude | 200 → 700 … 1600 → 1900 | **150 → 450** … 1600 → 1900 | beech from 500–700 m and chestnut 300–1000 m in Liguria; fruiting in Sassello chestnut at 420–450 m; the 8 located records all above the 150 m zero | plausible |
| *edulis* | habitat `other_conifer` | 0.3 | **0.6** | here mostly black-pine, Douglas-fir and spruce reforestation, all IGP hosts (like `mountain_pine`) | plausible |
| *edulis* | habitat `mediterranean_pine` | 0.1 | **0.3** | here mostly maritime pine, often next to chestnut: "altre specie di Pinus" are IGP hosts and *B. edulis* fruits in Spanish *P. pinaster* stands (`taye2016`, snippet-only) | plausible (weak) |
| *reticulatus* | habitat `other_conifer` | 0.1 | **0.3** | the Tuscan reading of "rarer under … pine" is black or Scots pine, which this class mostly is here | plausible (weak) |
| *aereus* | habitat `mixed_broadleaf_conifer` | 0.3 | **0.6** | class 313 is chestnut or oak (hosts) with maritime pine (secondary) here, not beech with fir | plausible |
| *pinophilus* | altitude | 300 → 800 … 1600 → 1900 | **250 → 600** … 1600 → 1900 | beech from 500–700 m, Scots pine from 500 m, acidophilous chestnut from 300 m | plausible |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **1.0** | Scots pine, the IUCN host; 9,200 ha at 500–1600 m | plausible |
| *pinophilus* | habitat `mediterranean_pine` | 0.3 | **0.6** | maritime pine inland at 300–800 m next to chestnut; pines are the IUCN host, but coastal stands are warm for this taxon (the altitude gate also cuts them) | plausible (weak) |
| *pinophilus* | habitat `other_conifer` | 0.3 | **0.6** | black-pine plantations ("pine plantations of all ages"), IGP-eligible | plausible |
| all four | season, weather, stoppers, growth clock | — | kept | records and pages agree; no regional numbers | as Tuscany |

Kept on purpose: *B. reticulatus* altitude 0 → 150 … 1100 → 1500 (Sassello plots at 340–380 m and
1000 m; records p10 363 m, max 1120 m); *B. aereus* altitude … 800 → 1250 (holm oak 0–600 m,
thermophilous chestnut 100–500 m); every season window. `mixed_broadleaf_conifer` stays 0.6 for
*edulis*, *reticulatus* and *pinophilus*: chestnut is a host of all three, so the Ligurian mix is at
least as good as Tuscany's beech-fir mix, and design keeps mixed classes below 1.

## Ovoli (*Amanita caesarea*)

**Regional evidence.** Presence: the Beigua park ("soprattutto porcini ed ovoli",
`parco_beigua_funghi2015`, plausible); the regional law's ovolo rules (`lr_liguria_17_2014`,
institutional); press and forager pages placing ovoli above Voltri (Mele), in the Val Polcevera and
in the Beigua park (`ilgiornale_boschi_liguri2010`, folklore); ovoli "nel periodo tardo
estivo-autunnale ... in prevalenza sotto castagni e querce, in zone calde e asciutte"
(`liguriafood_funghi2018`, folklore). Records: 24 iNaturalist and 11 GBIF, peaking in September
(3.9× the effort) with October at 1.0× and November 0.3×; located records at 275–781 m (median 454
m). Elsewhere, ovoli are described as uncommon in northern Italy (`innatura_ovolo`) and limited to
about 500 m in the north-west against about 1000 m in the Apennines (`funghimagazine_ovolo`).

**Decisions.**

| factor | Tuscany | Liguria | why | confidence |
|---|---|---|---|---|
| habitat `mixed_broadleaf_conifer` | 0.3 | **0.6** | class 313 is chestnut or oak with pine here; Tuscany's beech-fir mix held no ovoli host | plausible |
| season 01-06 → 01-09 … 05-11 → 30-11 | — | kept | the Ligurian September peak is earlier than Tuscany's September–October, but on 24 records; the cold-night and soil-temperature rules end the season | plausible |
| altitude … 750 → 1100 | — | kept | all 17 located records on the plateau (max 781 m); Liguria straddles the north-west and Apennine limits | plausible |
| beech 0 | — | kept | Ligurian beech comes down to 500 m, inside the band, but the "not in beech woods" sources are about the host | strong (hosts) |
| weather rules | — | kept | no regional numbers; 30-day rain (absolute 25 → 75 mm) will be full more often in the wetter Ligurian autumn | as Tuscany |

## Gallinacci (*Cantharellus* s.l., "galletti")

**Regional evidence.** The regional checklist has *C. cibarius* var. *alborufescens* in holm-oak wood
at 50 m on 26 November 2003 and var. *rufipes* in holm-oak wood at 190 m on 23 October 2001
(`zotti2008_checklist_liguria`, strong for presence). Pages place galletti at Santo Stefano d'Aveto
and finferli in the Beigua park (`ilgiornale_boschi_liguri2010`, folklore). Records: 46 iNaturalist
and 29 GBIF, the best-recorded group in Liguria, with a June mode (2.2× effort), an empty August,
an October peak (19 records, 1.5×), November (1.1×) and January records; located records from 43 m to
1533 m (median 262 m). The maritime pine is a documented host of *C. pallens*, with chestnut and cork
oak (`micoex2016_pallens`, plausible).

**Decisions.**

| factor | Tuscany | Liguria | why | confidence |
|---|---|---|---|---|
| habitat `mediterranean_pine` | 0.3 | **0.6** | marginal in Tuscany because only *P. pinaster* among its pines is a host; here the class is mostly *P. pinaster* | plausible |
| habitat `evergreen_oak` 1.0 | — | kept, now with Ligurian records | two holm-oak checklist records | plausible |
| season (lowland wraps to 25-01; mountain 01-06 → 15-11, blended 600–1000 m) | — | kept | Ligurian records have the same two modes and winter tail | plausible |
| altitude … 1000 → 1700 | — | kept | 3 of 36 located records above 1200 m, all inside the ramp | plausible |
| soil pH, lithology | disabled | kept disabled | Sassello porcini soils pH 4.2–5.8; the IPLA types split acidophilous and neutro-calcicolous variants, a free pH proxy if the grid keeps the type code (known gap updated) | plausible |
| weather rules | — | kept | no regional numbers; absolute 30-day ramp full more often in autumn | as Tuscany |

## Weather rules: why none changed

- **Rain amount and lag.** No Ligurian or north-west Apennine source gives a rain amount or lag for
  any of the three groups; the Sassello plots found no plot-scale climate effect
  (`ambrosio2024_dendrobiology`). The Tuscan rules (Amiata lag, national lore) stay.
- **Intense autumn rain.** Liguria's autumn storms are heavier and more frequent than Tuscany's, and
  getting more so (`arpal_atlante_clima2013`). The rain trigger saturates at 30 mm in three days, so
  a 150 mm event scores as a 30 mm one; national forager lore says excessive rain can inhibit
  fruiting, but nothing gives a threshold, so no "too much rain" stopper was added (open question).
- **Sea influence.** The coast's mild, narrow temperature range is what the weather itself carries:
  the temperature, frost and cold-night rules read each cell's own weather, and the season windows
  already reach December (porcini) and January (gallinacci) at low altitude.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges. Checking it on
  ARPAL's OMIRL gauges is a region-config task, not a species one.

## Sanity contrasts

`liguria/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written down
before any Ligurian score existed (none had been computed on 2026-09-25).

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_` (read those with `--group ovoli` / `--group gallinacci`). "Normal" is the area's mean
over 2017–2025. 11 contrasts: 9 porcini, 1 ovoli, 1 gallinacci; press research on 2026-09-25, every
page opened. Areas: `aveto_trebbia` (13 comuni from Santo Stefano d'Aveto to Torriglia),
`beigua_stura` (Sassello, Urbe, Stella, Pontinvrea, Tiglieto, Rossiglione, Campo Ligure, Masone,
Mele), `valbormida` (13 comuni from Calizzano and Bardineto to Millesimo), `arroscia_alpi_liguri`
(Mendatica, Triora and 11 more), `levante_inland` (Aveto-Trebbia plus 12 Val di Vara comuni) and
`savona` (province SV); comuni names checked against the ISTAT 2025 list.

| id | group | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|---|
| `aveto_2016_2017` | porcini | Aveto-Trebbia 2017, 30 Sep–15 Oct | same, 2016 | [forager blog, 2017-12-09](https://prevedereuscitaporcini.blogspot.com/2017/12/racconti-dai-boschi-della-liguria-con.html) ([LevanteNews 2016-10-09](https://www.levantenews.it/2016/10/09/raccolta-funghi-le-regola-rispettare-le-sanzioni/)) | 2017 side is a retrospective blog on hearsay, placed only "a confine con Emilia e Piemonte" |
| `aveto_2021_timing` | porcini | Aveto-Trebbia 2021, 3–20 Oct | same year, 25 Aug–25 Sep | [LevanteNews 2021-10-06](https://www.levantenews.it/2021/10/06/funghi-raccolta-al-via-le-regole-i-consorzi-le-sanzioni/) ([Mentelocale 2021-09-11](https://www.mentelocale.it/genova/13869-siccita-val-aveto-stop-temporaneo-raccolta-funghi.htm)) | written 3 days into the flush; the 20 Oct end is inferred; October is seasonally favoured |
| `aveto_2019_2021_early_september` | porcini | Aveto-Trebbia 2019, 1–14 Sep | same, 2021 | [LevanteNews 2019-09-09](https://www.levantenews.it/2019/09/09/raccolta-funghi-le-regole-da-seguire/) (Mentelocale 2021) | one-line season lead in a rules round-up |
| `aveto_july_2022_2024` | porcini (summer) | Aveto-Trebbia 2024, 1–25 Jul | same, 2022 | [Funghi Magazine 2024-07-25](https://funghimagazine.it/aggiornamento-funghi-25-07-2024/) ([FM 2022-08-02](https://funghimagazine.it/aggiornamento-meteofunghi-2-agosto-2022/)) | national bulletin, broad areas; the 2022 side is about rain, not finds |
| `sassello_2021_2022` | porcini | Beigua-Stura 2022, 1–15 Sep | same, 2021 | [RedazioneNews 2022-09-15](https://www.redazionenews.it/economia/2022/09/15/sassello-dopo-la-festa-amaretto-sotto-coi-funghi-stagione-boom/) ([IVG 2021-09-16](https://www.ivg.it/2021/09/funghi-raccolta-in-ritardo-lesperto-colpa-dei-cambiamenti-climatici-speriamo-nelle-piogge/)) | Sassello was in the 2022 swine-fever zone (affects sightings, not scores) |
| `ovoli_savonese_2021_2022` | ovoli | Beigua-Stura 2022, 28 Aug–15 Sep | same, 2021 | [Basilico 2022-10-25](https://www.basilico.it/2022/10/25/raccolta-funghi-in-liguria-nel-2022-annata-record-ma-lambiente-soffre/) (IVG 2021-09-16) | 2022 ovoli dated only loosely; "savonese" is broad |
| `sassello_july_2025` | porcini (summer) | Beigua-Stura 2025, 15–29 Jul | same, normal | [IVG 2025-07-28](https://www.ivg.it/2025/07/un-luglio-anomalo-e-piovoso-regala-buttate-di-porcini-estivi-nel-sassellese-e-in-alta-valbormida/) ([ArtesTV 2025-07-29](https://www.artestv.it/un-luglio-anomalo-e-piovoso-regala-buttate-di-porcini-estivi-nel-sassellese-e-in-alta-val-bormida/)) | ArtesTV reads as an embellished rewrite |
| `valbormida_2024` | porcini | Val Bormida 2024, 12 Sep–5 Oct | same, normal | [IVG 2024-09-17](https://www.ivg.it/2024/09/a-bardineto-e-calizzano-vietato-raccogliere-funghi-fino-a-domenica-22-settembre/) ([FM 2024-09-12](https://funghimagazine.it/aggiornamento-funghi-12-09-2024/)) | about conditions and a precautionary ban before the flush, not harvests |
| `bormida_vs_beigua_2020` | porcini | Val Bormida 2020, 1–20 Sep | Beigua-Stura, same window | [FM 2020-09-21](https://funghimagazine.it/meteofunghi-21-09-2020/) ([FM 2020-10-08](https://funghimagazine.it/aggiornamento-meteofunghi-08-10-2020/)) | FM only; "alto Bormida" may mean the Piedmont side |
| `levante_vs_savona_2023` | porcini | Aveto-Trebbia + Val di Vara 2023, 1–12 Oct | province of Savona, same window | [FM 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/) | FM only; the flush ran east to west around 1 October, so the west may just have faded first |
| `gallinacci_arroscia_2022_2025` | gallinacci | Arroscia-Alpi Liguri 2025, 28 Jun–15 Jul | same, 2022 | [FM 2025-06-27](https://funghimagazine.it/aggiornamento-nascite-funghi-27-06-2025/) (FM 2022-08-02) | FM only; the 2022 side is heat and drought, not observed absence |

Candidates left out: whole-Liguria 2017 and Val di Vara 2019 and 2021 August/September against
October (seasonality alone favours October, so they test little); September 2025 Aveto against the
upper Arroscia (the Imperia group's "non si prospetta una buona annata" conflicts with a
same-month "dal Levante al Ponente i cesti si riempiono"); ovoli in the Genoa hinterland in early
October 2024 (says ovoli were the commonest find, not that they beat a normal year).

**Year picture from the press** (for context, not scored): poor 2016, dry summer 2017 until 19
September, poor September 2021 (drought) with a strong October, poor June–August 2022 then a very
good September–October, good October 2023, good summer and September 2024, exceptional summer and
September 2025 in the east. 2022 was a good Ligurian autumn, unlike the Tuscan reading of 2022 as a
dry year.

**Swine-fever closures.** From January 2022 picking was banned, then allowed only after notifying
the Region, in 36 comuni of the African swine fever zone, among them Masone, Campo Ligure,
Rossiglione, Tiglieto, Mele, Stella, Urbe, Sassello, Pontinvrea and Torriglia; the Sassello
consortium suspended permit sales in September 2023 amid confusion over the rules. Sightings there
will be undercounted in 2022–2023 regardless of fruiting.

## Open questions

- **Slope and sun exposure.** Both stoppers were anchored on Tuscan grid percentiles (slope x1 to
  25°, about the Tuscan p90). Ligurian woods are steeper; recheck the percentiles on the Liguria grid
  before trusting these two factors there (they are frozen `static_band` priors for the backtest).
- **Excessive rain.** Does a very wet week (Liguria's autumn floods) suppress porcini fruiting? No
  source gives numbers; the backtest could compare October flood years.
- **Ovoli timing.** The Ligurian records peak in September, earlier than Tuscany's; worth rechecking
  with more seasons of records before moving the window (frozen for this backtest).
- ***B. pinophilus* hosts and season.** Italian (beech, fir, chestnut) and IUCN (pines) views are
  both encoded; a Ligurian page claims late-autumn-to-spring fruiting under beech and fir. One
  Ligurian record exists.
- **Rain scale.** Fit or check `precipitation_scale` against ARPAL OMIRL gauges in woodland cells.
- **Sightings in the swine-fever zone.** Picking restrictions in 2022–2023 (Beigua, Valle Stura,
  Torriglia) thin the records there; the backtest's effort correction may need to know.
- **Sanity groups.** `sanity.yaml` has no group field, so the ovoli and gallinacci contrasts are
  evaluated on whatever `--group` is passed; a per-contrast group would be cleaner (a change to
  `api.model.sanity`, not made here).
- **Leads not read:** Ambrosio E. (2015) PhD thesis on the *B. edulis* group (Università di Genova,
  likely Sassello phenology); Zotti & Pautasso (2013, Czech Mycology 65: 193–218) on macrofungi of
  Ligurian holm-oak woods (site down on 2026-09-25); Zotti & Zappatore (2006, Plant Biosystems 140) on
  beech woods of western Liguria; Ambrosio et al. (2018, Acta Mycologica 53: 1109) annotated checklist
  of the Sassello sites (site down).

## References added for Liguria

| id | kind | verified | used for |
|---|---|---|---|
| `ambrosio2024_dendrobiology` | peer-reviewed | verified | Sassello porcini sites: taxa by host and altitude, soil pH, no plot-scale climate effect |
| `zotti2008_checklist_liguria` | peer-reviewed | verified | *Cantharellus* in holm oak (October, November) |
| `arpal_atlante_clima2013` | institutional | verified | Ligurian rain and temperature climatology |
| `rl_fotoatlante_tipi_forestali` | institutional | verified | altitude belts per forest type |
| `rl_tipi_forestali_2008` | institutional | verified | IPLA classification |
| `lr_liguria_17_2014` | institutional | verified | ovoli and porcini picking rules (presence) |
| `parco_beigua_funghi2015` | institutional | verified | porcini and ovoli season in the Beigua woods |
| `parco_aveto_porcini` | institutional | verified | porcini host woods in the Val d'Aveto |
| `iucn_pinophilus2019` | institutional | verified | *B. pinophilus* pine hosts |
| `liguriafood_funghi2018` | web | verified | per-taxon season and hosts (folklore) |
| `cacciatoridifunghi_liguria2023` | web | verified | porcini seasons (folklore) |
| `ilgiornale_boschi_liguri2010` | web | verified | where porcini, ovoli and galletti are picked (folklore) |
| `mushma_liguria_forest_composition_2026` | analysis | verified | forest composition by habitat key |
| `mushma_occurrence_check_liguria_2026` | analysis | verified | month counts, enrichment, elevation quantiles |

Existing references the Ligurian changes lean on: `borgotaro_igp_2014` (IGP host list), `taye2016`
(*B. edulis* in *P. pinaster*), `micoex2016_pallens` (maritime pine as a *C. pallens* host),
`myboletus_ovoli` (not in beech woods), and `ambrosio_zotti2015` (Ligurian porcini sites, cited
here only).
