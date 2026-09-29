# Species ecology: Valle d'Aosta (regional appendix to species-ecology.md)

Research date: 2026-09-29 (dates Europe/Rome, units metric). Card: `region-valle-d-aosta-species.md`
(child of `region-valle-d-aosta.md`). Rule files: `api/src/api/config/species/valle_d_aosta/`. This
appendix records how the Tuscan rule set (`species/tuscany/`) was carried to Valle d'Aosta (Aosta
Valley, Vallée d'Aoste), what changed and why. It covers **fruiting conditions only**: nothing here is
about edibility or identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(21 added for this region, in one block at the end of the file, keys prefixed `vda_` or with a `_vda_`
infix). Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**,
**plausible**, **folklore**; each claim below carries one in brackets. Every number is a prior for the
backtest; season windows, altitude bands and habitat affinities stay frozen (`model.yaml`,
`backtest.frozen_factor_kinds`). Piemonte ([`piemonte.md`](piemonte.md)) shares the region's forest
typology (IPLA); Trentino-Alto Adige ([`trentino_alto_adige.md`](trentino_alto_adige.md)) and Lombardia
([`lombardia.md`](lombardia.md)) were read for how the Alpine regions retuned.

## Summary

1. **Two groups, four keys: porcini (three keys) and gallinacci. Ovoli and *B. aereus* are dropped.**
   - **Ovoli: no record anywhere in the region** (details under Keys and groups dropped). Not in
     iNaturalist or GBIF, not in the regional checklist of 1,031 reports since 1850
     (`vda_marra2001_macromiceti`), not in a full-season survey of the region's downy-oak and chestnut
     woods (`vda_marra2000_lago_villa`). The Bassa Valle woods below the altitude the species reaches in
     north-west Italy are a few dozen square kilometres. The nearest records are 7.5 km away in the
     Canavese and 34 km away across the main ridge in Valais. The group is dropped, the file
     `ovoli_caesarea.yaml` is not created, and the doc says what would bring it back.
   - ***B. aereus* has no record either** (region, Valais, the Italian side of the neighbourhood, the
     checklist, the oak-chestnut survey), and the Piedmontese press saw none north of the Po in 2024.
     `porcini_aereus.yaml` is not created; *B. reticulatus* and *B. edulis* cover the Bassa Valle's
     chestnut and oak.
2. **The most Alpine region so far.** Approximated from satellite tree cover (the region grid did not
   exist yet), its woods have their median at 1,566 m (Trentino-Alto Adige 1,407 m) and a p90 of 1,998 m;
   larch and stone pine are 44 % of the woods (`vda_carta_forestale_2020`). The changes are Alpine: an
   Alpine season window for *B. edulis*, one May-November window for *B. pinophilus*, bands reaching the
   subalpine belt, Scots pine a full host of *B. pinophilus*, spruce, fir and beech full hosts of the
   chanterelle.
3. **Larch was the biggest choice.** `other_conifer` (larch and stone pine) drops to non-host (0.1) for
   *B. edulis*, *B. pinophilus* and gallinacci, as in Trentino-Alto Adige, Lombardia and
   Friuli-Venezia Giulia and unlike Piemonte (0.3). The region's own typology puts the other trees in
   its larch stands at no more than 14 % of stems, and larch roots carry no *Boletus*. Old Valdostan
   collections in larch woods are the case for 0.3, which is the first knob to turn (see Porcini).
4. **Weather rules are all Tuscany's.** The one Valdostan fruiting study that speaks about weather (Mont
   Avic, 1997-1999) agrees with them in words: flushes about two weeks after rain, delayed by cold nights
   and by days of dry wind, ended by hard frost (`vda_peretti1999_mont_avic`). The region's dry central
   valley (about 550 mm a year at Aosta) is left to each cell's own rain normal.
5. **Evidence: thin records, old literature, one bulletin.** 21 new references, all opened:
   - 1 peer-reviewed;
   - 6 institutional (the regional forest typology and map, climate, the 2022 drought and rain, the
     1977 picking law);
   - 4 society (the regional checklist, two regional surveys, a Haute-Savoie naturalists' group);
   - 8 web (Funghi Magazine bulletins, folklore);
   - 2 our own analyses.

   The region has the fewest records of any so far (17 *B. edulis*, 9 *Cantharellus* on iNaturalist),
   so the season and band numbers lean on the neighbouring Alps (iNaturalist within 30-60 km, SwissFungi
   in Valais) and on the region's older mycological records. `sanity.yaml` holds 12 porcini contrasts
   from 2019-2025 across the valleys, all resting on Funghi Magazine (the Valdostan papers print no
   season comparisons).

## At a glance: what differs from Tuscany and why

Trapezoids are `[zero, full, full, zero]`, dates `DD-MM`, altitudes in metres.

| key | factor | Tuscany | Valle d'Aosta | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | one window 01-07 → 01-09 … 15-11 → 20-12 | **below 900 m 01-07 → 15-08 … 31-10 → 30-11; above 1,300 m 20-06 → 25-07 … 05-10 → 31-10**, blended in between | neighbourhood records at 1,400 m or higher run late July to October; Mont Avic flushes late August to 21 October; nothing after October | plausible |
| *edulis* | altitude | 200 → 700 … 1,600 → 1,900 | **200 → 500 … 1,900 → 2,300** | neighbourhood p90 1,847, p95 1,897 m; Mont Avic to 2,000 m; potential forest to about 2,300 m | plausible |
| *edulis* | habitat `other_conifer`, `transitional` | 0.3, 0.3 | **0.1, 0.1** | larch no host; larch stands at most 14 % other trees; transitional = green-alder scrub | plausible |
| *reticulatus* | season | 01-05 → 01-06 … 30-09 → 15-11 | **01-05 → 01-06 … 15-09 → 20-10** | region's records all June; Valais June 6.1×, September 0.3×, October 0 | plausible |
| *reticulatus* | altitude | 0 → 150 … 1,100 → 1,500 | **0 → 150 … 1,300 → 1,700** | neighbourhood records p90 1,771 m, census to 1,927 m | plausible |
| *reticulatus* | habitat `mixed_broadleaf`, `transitional` | 0.6, 0.6 | **0.3, 0.1** | mixed broadleaf here is ash-maple-lime and rocky pioneer scrub (hazel about 1 %); transitional = green alder | plausible |
| *pinophilus* | season | spring + autumn windows, gap 20-07 → 15-08 | **01-05 → 25-05 … 10-10 → 10-11** | first finds late May 2024 at 800-1,000 m, "insolita buttata" June-July 2024, collections to 10 October | plausible |
| *pinophilus* | altitude | 300 → 800 … 1,600 → 1,900 | **400 → 700 … 1,900 → 2,300** | records 1,750-1,850 m at Mont Avic, 1,799 m at Courmayeur; Valais to 2,001 m | plausible |
| *pinophilus* | habitat | mountain pine 0.6, other conifer 0.3, transitional 0.3 | **1.0, 0.1, 0.1** | Scots pine its commonest partner; Val Ferret and Mont Avic collections under pine | plausible |
| gallinacci | season | lowland 15-04 → 10-05 … 15-12 → 25-01; mountain … 15-10 → 15-11 | **lowland 15-05 → 15-06 … 31-10 → 30-11; mountain 01-06 → 01-07 … 30-09 → 31-10** | *C. cibarius* s.str., no winter mode; neighbourhood October 1.1×, Valais 0.6×, November near 0 | plausible |
| gallinacci | altitude | … 1,000 → 1,700 | **… 1,850 → 2,250** | neighbourhood p90 1,855, p95 2,016 m; region records to 2,023 m | plausible |
| gallinacci | habitat | beech 0.6, fir/spruce 0.6, mountain pine 0.3, other conifer 0.3, transitional 0.3 | **1.0, 1.0, 0.6, 0.1, 0.1** | Swiss partners beech 550, spruce 294, fir 256 of 1,271 | plausible |
| ovoli | whole group | kept | **dropped** | no record in the region from any source | plausible |
| *aereus* | whole key | kept | **dropped** | no record in the region, in Valais or on the Italian side of the neighbourhood | plausible |
| every key | slope stopper | x1 to 25°, x0.8 from 40° | **x1 to 36°, x0.8 from 45°** | approximated woodland p90 36.5°, max 44.4° | as Tuscany (plausible) |
| every key | weather, growth clock, sun exposure, other stoppers | — | **kept** | no numbers from the region; see Weather | as Tuscany |

Kept on purpose:
- *B. edulis* mountain pine at 0.6, although it fruited under *Pinus uncinata* at Mont Avic;
- mixed broadleaf at 0.3 for *B. edulis* and gallinacci (Piemonte raised it for its birch woods; here
  birch is 790 of 12,125 ha);
- the *B. reticulatus* hosts other than the two lowered;
- the gallinacci soil-pH and lithology rules, still disabled.

**Effect on the altitude gates** (the habitat gates need the region's forest map, which the region card
builds). On the 1,174 approximated woodland cells (`mushma_vda_terrain_check_2026`), the share at full
altitude credit moves from the Tuscan to the regional bands as follows:

| key | Tuscan band | regional band |
|---|---|---|
| *edulis* | 49 % (mean gate 0.66) | 79 % (0.94) |
| *reticulatus* | 21 % (0.33) | 33 % (0.46) |
| *pinophilus* | 45 % (0.65) | 76 % (0.92) |
| gallinacci | 16 % (0.37) | 76 % (0.92) |
| *aereus* (dropped) | 8 % (0.18) | — |
| ovoli (dropped) | 7 % (0.13) | — |

## Valle d'Aosta in brief

**Woods.** The regional forest map (Carta forestale, revised 2020) has 98,869 ha of forest, 94,425 ha
of it woods, 28.7 % of the region, in 17 IPLA categories (`vda_carta_forestale_2020`) [strong]. The
typology book (`vda_tipi_forestali_2007`) [strong] describes them:
- **Larch** is "la specie forestale più diffusa in Valle d'Aosta". Its dominance was made by "la
  contestuale e sistematica eliminazione del pino cembro e delle altre conifere". In the larch stands
  "Le altre specie presenti, rappresentate soprattutto da conifere, non superano nel complesso il 14% del
  numero ed il 6 % del volume", mostly in the lower layers. The tree that "più spesso accompagna il
  larice" is spruce, with wide larch-spruce mixtures in the Val Veny, the Gran San Bernardo valley,
  Valpelline and the La Thuile valley. Near the tree line the larch woods are "generalmente quasi puri".
- **The larch category by type** (2020): half is the subalpine *Larici-cembreto su rodoreto-vaccinieto*
  (21,800 ha), a fifth the *Lariceto montano* (8,664 ha), then the mesoxerophilous subalpine larch wood
  (6,130 ha), larch on boulder fields (3,372 ha) and grazed larch (1,687 ha).
- **Spruce** is the second conifer (19 % of stems), most in the wetter side valleys west of Aosta
  (Cogne, Rhêmes, Gran San Bernardo, Valdigne) and at Brusson and in the Valle di Gressoney. **Silver
  fir** is 2 % of stems, mostly endalpic stands between Pontey and Aymavilles, in Valpelline, at Quart,
  Cogne, Morgex, La Salle and La Thuile.
- **Scots pine** (16 % of stems) forms an almost unbroken belt on the sunny side of the central valley
  between Verrayes and Morgex. **Mountain pine** is erect *Pinus uncinata* (95 % of its category), the
  largest stand at Mont Avic.
- **Broadleaves**: chestnut (8 % of stems) "ha una diffusione prevalente nella Bassa Valle, fino a
  Châtillon"; downy oak on the low and middle south-facing slopes of the central valley up to Morgex;
  beech only in the Bassa Valle between Pont-Saint-Martin and Montjovet (about 2 %); sessile oak a
  few dozen hectares.

**Which habitat holds which tree.** The region config (`regions/valle_d_aosta.yaml`) did not exist
when this card was written; the mapping below is the card's, as Piemonte did with the same IPLA
categories. Check it against the region config once it lands.

| habitat key | IPLA categories (2020 map) | ha | share of forest |
|---|---|---|---|
| `other_conifer` | LC Lariceti e Cembrete; RI Rimboschimenti | 43,089 + 1,310 | 44.9 % |
| `fir_spruce` | PE Peccete; AB Abetine | 13,545 + 1,762 | 15.5 % |
| `mountain_pine` | PS Pinete di pino silvestre; PN Pinete di pino montano | 9,614 + 3,247 | 13.0 % |
| `mixed_broadleaf` | BS Boscaglie pioniere e d'invasione; AF Acero-tiglio-frassineti | 6,171 + 5,954 | 12.3 % |
| `chestnut` | CA Castagneti | 4,720 | 4.8 % |
| `deciduous_oak` | QR Querceti di roverella; QV Querceti di rovere | 3,846 + 68 | 4.0 % |
| `transitional_woodland_shrub` (not woodland) | OV Arbusteti subalpini (green alder); AS Arbusteti | 2,775 + 647 | 3.5 % |
| `beech` | FA Faggete | 1,154 | 1.2 % |
| `riparian` | AN Alneti planiziali e montani; SP Saliceti e Pioppeti ripari | 674 + 167 | 0.9 % |
| `exotic_broadleaf` | RB Robinieti | 126 | 0.1 % |
| `evergreen_oak`, `mediterranean_pine`, `macchia`, `mixed_broadleaf_conifer` | — | — | absent |

Inside `mixed_broadleaf`, 94 % of the ash-maple-lime woods are invasion woods on abandoned land, and the
pioneer woods are rocky pioneer scrub (2,829 ha), other pioneer scrub (1,938 ha), montane birch (790 ha),
aspen (479 ha) and hazel (135 ha).

**Altitude belts** (`vda_tipi_forestali_2007`) [strong]:
- the montane-subalpine boundary is at about 1,800 m, 1,600 m in the wetter *mesalpic* sector (the
  Bassa Valle below the Montjovet gorge and the lower Gressoney and Ayas valleys), where limits sit
  150-200 m lower;
- "Sopra i 2.000 m larice e pino cembro sono le uniche specie arboree"; grasslands with forest potential
  reach "in media fino ai 2.300 m di quota" (`vda_carta_forestale_2020`);
- spruce (1,000) 1,200-1,800 (2,000) m; Scots pine (500) 600-1,600 (1,700) m; *Pinus uncinata*
  1,300-2,200 m; chestnut "sin verso i 1.000 m"; downy oak from 300 m at Pont-Saint-Martin to 1,400 m on
  sunny slopes; beech 700-1,500 m.
- On the approximated woodland cells (`mushma_vda_terrain_check_2026`): median 1,566 m, p10 853 m, p90
  1,998 m, max 2,225 m; 186 of 1,174 cells below 1,000 m and 56 below 700 m.

**Climate.**
- The central valley is a rain shadow: "la zona di Aosta registra mediamente circa 550 mm annui, le
  zone prossime ai rilievi di confine con la Francia si attestano intorno a 750 mm l'anno mentre al
  confine con il Piemonte la precipitazione media è circa 950 mm l'anno" (`vda_cf_inquadramento_climatico`)
  [strong].
- Autumn is the main rain maximum and spring the second (`vda_tipi_forestali_2007`).
- 2022 was "L'ANNO PIÙ CALDO E SICCITOSO DEGLI ULTIMI 80 ANNI" (`vda_siccita_2022`): Aosta 414 mm,
  Saint-Vincent 364 mm, Verrès 371 mm, against 868-873 mm at Breuil-Cervinia and Courmayeur
  (`vda_annuario_2023_precipitazioni`) [strong].
- The press blames the foehn (*favonio*) and dry wind for failed flushes almost every year (see Press
  contrasts) [folklore].

**Picking rules** (`vda_lr16_1977_funghi`) [strong]. The law in force is still L.R. 16/1977:
- 1 kg a day per person in the woods;
- no picking on farmland except "pascoli al di sopra dell'altitudine di 1800 metri";
- no picking "da un'ora dopo il tramonto ad un'ora prima del levar del sole";
- always "subordinata al consenso del proprietario".

There is no calendar, no permit and no species named, so the law gives no season prior and no ovolo
rule. It thins sightings (1 kg, owners' consent), not scores.

## Sightings (occurrence cross-check)

Queried 2026-09-29 (`mushma_occurrence_check_vda_2026`). Aggregates only; no coordinates are stored.

- **The region** (iNaturalist place 10882, verifiable; GBIF `gadmGid=ITA.19_1`). 2,794 fungi records
  in all (July 37 %, August 23 %). GBIF adds nothing for these taxa: every row is an iNaturalist copy,
  and there is no herbarium specimen of any of the six.
- **The neighbourhood**: a box 45.3-46.45° N, 6.6-8.2° E, reaching 30-60 km beyond the region into the
  Canavese, Biellese and Valsesia edges, southern Valais and the Savoie and Haute-Savoie border valleys.
  iNaturalist verifiable records against 21,410 fungi records there. Elevations from the Open-Meteo
  elevation API for records that are not obscured and have an accuracy of 1 km or better. Counted by
  observer-day where stated.
- **Valais** (SwissFungi on GBIF, canton Vs, against its 38,176 Valais fungi records; altitudes from
  the SwissFungi atlas). Valais is the region's twin across the Great St Bernard: a dry inner-Alpine
  valley of larch, spruce and Scots pine.
- **Enrichment** = the taxon's monthly share ÷ the month's share of all fungi records in the same set
  (> 1: over-represented for the effort).

| taxon | region (iNat) | box (iNat) | box enrichment Jun / Jul / Aug / Sep / Oct / Nov | Valais (SwissFungi) | Valais enrichment Jun / Jul / Aug / Sep / Oct / Nov |
|---|---|---|---|---|---|
| *B. edulis* | 17 (Jul 3, Aug 6, Sep 5, Oct 3) | 132 | 0 / 0.4 / 1.7 / 1.8 / 1.0 / 0.6 | 110 | 0.2 / 2.2 / 1.8 / 0.9 / 0.7 / 0.5 |
| *B. reticulatus* | 3 (all June) | 21 | 3.9 / 1.2 / 1.3 / 1.1 / 0.4 / 0 | 17 | 6.1 / 2.3 / 1.4 / 0.3 / 0 / 0 |
| *B. aereus* | 0 | 1 (Haute-Savoie, 893 m) | — | 0 | — |
| *B. pinophilus* | 3 (Jul, Aug, Sep) | 6 | — | 15 | 1.1 / 0.7 / 1.3 / 1.8 / 0.9 / 0 |
| *A. caesarea* | 0 | 3, all in Piemonte | — | 1 (1997) | — |
| *Cantharellus* | 9 (all *C. cibarius*) | 95 | 0.2 / 1.5 / 1.7 / 1.0 / 1.1 / 0 | 135 | 0.5 / 1.6 / 2.1 / 0.95 / 0.6 / 0.13 |

| taxon | located | p10 | median | p90 | p95 | max (m) |
|---|---|---|---|---|---|---|
| *B. edulis*, region | 8 | | 1,605 | | | 1,833 (min 1,341) |
| *B. edulis*, box | 97 | 1,140 | 1,596 | 1,847 | 1,897 | 2,110 |
| *B. edulis*, Valais | 68 | | 1,586 | | | 1,922 (min 556) |
| *B. reticulatus*, box | 17 | 608 | 1,212 | 1,771 | | 1,830 |
| *Cantharellus*, region | 8 | | | | | 2,023 (min 1,273) |
| *Cantharellus*, box | 81 | 779 | 1,443 | 1,855 | 2,016 | 2,120 |
| *Cantharellus*, Valais | 95 | | 1,586 | | | 2,018 (min 442) |
| *B. pinophilus*, Valais | 13 | | 1,426 | | | 2,001 (min 611) |

**Half-months by elevation** (box, located observer-days):

| taxon | band (n) | Jul 1-15 | Jul 16-31 | Aug 1-15 | Aug 16-31 | Sep 1-15 | Sep 16-30 | Oct 1-15 | Oct 16-31 | Nov |
|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | < 900 m (5) | | | | | 1 | 1 | 1 | | 2 |
| | 900-1,400 m (25) | | | 2 | 1 | 9 | 9 | 3 | 1 | |
| | ≥ 1,400 m (58) | | 4 | 13 | 19 | 8 | 10 | 3 | 1 | |
| *Cantharellus* | < 900 m (8) | | 1 | 2 | | 1 | 2 | 1 | 1 | |
| | 900-1,400 m (27) | 2 | 8 | 6 | 1 | 3 | 6 | 1 | | |
| | ≥ 1,400 m (38) | 1 | 7 | 10 | 8 | 3 | 4 | 5 | | |

**Caveats.**
- **Very few regional records**: the region's own counts can show what occurs, not a season shape. The
  box is dominated by Valais (Swiss) and French records.
- **One observer, one wood**: 5 of the region's 9 chanterelle records are one observer's on 2 and 4
  October 2024 at 1,910-2,023 m in the upper Val d'Ayas.
- **Implausible records**: the box's 2,110-2,120 m records on the Mombarone ridge (a *B. edulis* and an
  ovolo) look misplaced, as the Piemonte appendix found.
- **Presence-only records**, near trails; summer hikers raise July-August effort. The parks (Gran
  Paradiso, Mont Avic) forbid picking to non-residents, and the law caps picking at 1 kg, which thins
  sightings, not fruiting.

**Older regional records.** The regional checklist (`vda_marra2001_macromiceti`) [plausible] gathers
1,031 reports since 1850: 455 Basidiomycota and 33 Ascomycota. It has *B. edulis*, *B. pinophilus*,
*B. aestivalis* (*reticulatus*) and *C. cibarius*, but no *A. caesarea* and no *B. aereus*. Its data
are 40 % from Cogne, then Piccolo San Bernardo-La Thuile, the Lago di Villa reserve, Mont Avic and the
Val Ferret, with sporadic records elsewhere. Region-wide, "Molise and Valle d'Aosta are the less
investigated Regions" of Italy (`vda_onofri2003_checklist`) [strong], so an absence there is weak
evidence on its own.

## Porcini (*B. edulis*, *B. reticulatus*, *B. pinophilus*)

**Regional evidence.**

- **Season** (plausible to folklore).
  - Records, in the tables above: the neighbourhood's high records run from late July to October, and
    Valais peaks in July-August.
  - **Mont Avic** (`vda_peretti1999_mont_avic`) [plausible]. Mountain-pine woods at 1,330-2,100 m were
    visited from mid-June in 1998 and 1999. *B. edulis* appeared only from 25 August (1999) or
    mid-September (1997, 1998) and lasted to 8-21 October, up to 2,000 m. Nothing showed in June or
    July.
  - **Older collections** (`vda_marra2001_macromiceti`) [plausible]:
    - *B. edulis* at La Thuile on 26 August 1929, at Cogne in August-September (1969-1977), in the Val
      Ferret in September 1980;
    - *B. edulis* at the Lago di Lolair (1,184 m, Scots pine and spruce) between 16 June and 9 August
      2000;
    - *B. pinophilus* at Cogne in September 1971, in the Val Ferret on 25 September and 10 October 1979.
  - **Funghi Magazine** [folklore]:
    - *B. edulis* first appears in the last days of July: 2021, "I primi edulis si sono trovati in Val
      d'Aosta, grazie al ritorno delle piogge" (`vda_fm_2021_08_06`); also 2024 and 2025.
    - It is over by mid-October in the west: 2023, "le nascite sono al momento del tutto cessate sui
      settori Ovest della regione" on 12 October (`vda_fm_2023_10_12`).
    - Red porcini (*B. pinophilus*) appeared at the end of May 2024 at "800/1000 metri" in the south-east
      (`vda_fm_2024_05_31`) and made "una bellissima e insolita buttata" in June-July 2024
      (`vda_fm_2024_07_25`).
    - Summer porcini (*reticulatus*) come in late June to early August "a fondovalle" and "tra le
      faggete".
- **Hosts** (plausible):
  - *B. edulis* was collected in "Boschi frondoso-laricini" at La Thuile (1,800 m), "In un bosco di
    larici" in the Val Ferret, in "Picea-Larix" at Cogne, and under Scots pine and spruce at Lolair;
  - *B. pinophilus* in "boschi di Larix, Betula verrucosa, Sorbus aucuparia e Pinus sylvestris" in the
    Val Ferret and under *Pinus uncinata* at Mont Avic (`vda_marra2001_macromiceti`,
    `vda_peretti1999_mont_avic`);
  - *B. aestivalis* is the only porcino of the Lago di Villa downy-oak and chestnut survey
    (`vda_marra2000_lago_villa`);
  - Funghi Magazine's reports speak of "abetaie", "boschi di Abete o misti Abete/Faggio" and "boschi
    misti a base di Pino o Abete con Faggi o Castagni" (`vda_fm_2024_06_14`) [folklore]; none of the
    2016-2025 bulletins read ties porcini to larch woods.
- **Altitude** (plausible). The region's records sit at 1,341-1,833 m; Mont Avic fruited to 2,000 m;
  in 2025 Funghi Magazine gave "Quota ideale per le nascite: 1200–1600 m" [folklore].

**Larch: the weighing.** Larch and stone pine are 44 % of the region's woods, so their affinity moves
more of the map than any other number here. The class is `other_conifer`.

For non-host (0.1):
- Larch root tips at 1,700-1,900 m in South Tyrol held 68 ectomycorrhizal species and no *Boletus* or
  *Cantharellus*; the sampling avoided the interspersed spruce and stone pine on purpose
  (`taa_mandolini2025_larix`). Stone pine roots held none either (`taa_mandolini2024_cembra`) [strong].
- Among Swiss records naming a partner tree, larch is 25 of 960 for *B. edulis* (2.6 %), 2 of 37 for
  *B. pinophilus* and 32 of 1,271 for *C. cibarius* (`mushma_occurrence_check_vda_2026`) [plausible].
- The region's larch stands hold at most 14 % other trees by number and 6 % by volume, and near the
  tree line they are "generalmente quasi puri" (`vda_tipi_forestali_2007`) [strong]. So a
  host-weighted share of about 0.1 is what a pure larch cell carries.
- 73 % of the larch category is subalpine types (larch-stone pine on rhododendron and vaccinium,
  mesoxerophilous subalpine larch, boulder-field larch, stone pine) (`vda_carta_forestale_2020`).
- Forager lore: the larch wood's "habitat esclude completamente la presenza di funghi Porcini", unless
  "nelle immediate vicinanze ci siano uno o più Abeti rossi o Abeti bianchi (ma anche Faggi)"
  (`funghimagazine_laricino`) [folklore].
- Trentino-Alto Adige, Lombardia and Friuli-Venezia Giulia chose 0.1.

For marginal (0.3):
- Old Valdostan collections of *B. edulis*, *B. pinophilus* and *C. cibarius* in larch woods (La Thuile,
  Val Ferret, Cogne) (`vda_marra2001_macromiceti`) [plausible].
- The larch dominance is partly a management product, and the category shifts with the spruce and fir
  categories through their larch and spruce/fir variants (`vda_carta_forestale_2020`).
- Piemonte, on the same IPLA typology, kept 0.3.

**Decision:** 0.1 for *B. edulis*, *B. pinophilus* and gallinacci.
- **Effect:** with the habitat gate saturating at a host share of 0.30, a pure larch cell gets a third
  of full credit, and a cell with a fifth of spruce, fir, pine or beech gets full credit.
- **First knob:** if the sanity check or the backtest finds the larch valleys too low (Valdigne,
  Valpelline, upper Ayas, Valtournenche; the `cervino` sanity area's woods have their median at 1,834
  m), raise it to 0.3.
- **Better fix, a grid question:** if the forest map carries the larch variants with spruce or fir,
  mapping those polygons to `fir_spruce` would beat either number.

**Decisions** (numbers in the table above; reasons in each factor's `notes`):
- ***B. edulis* season: an Alpine window**, blended in from 900 m and alone from 1,300 m, as in
  Lombardia and Friuli-Venezia Giulia.
  - **What:** full from 25 July to 5 October, closed by 31 October.
  - **Why the handover is low:** the records at 900-1,400 m already start and end like the high ones,
    so the handover follows the records rather than the 1,800 m montane-subalpine boundary.
  - **Below 900 m** the window runs full from mid-August to the end of October and closes by 30
    November. That is the Bassa Valle's chestnut and the sunny slopes.
- ***B. edulis* altitude:** full to 1,900 m, zero at 2,300 m (the tree line); full from 500 m, zero at
  200 m.
- ***B. edulis* habitat:** larch-stone pine and green-alder scrub to non-host. Mountain pine stays
  secondary: Scots pine plus *Pinus uncinata*, under which *B. edulis* fruited at Mont Avic.
- ***B. reticulatus*:**
  - season full to 15 September, closed by 20 October;
  - band up to the montane spruce and fir (full to 1,300 m, zero at 1,700 m);
  - mixed broadleaf and transitional lowered;
  - a marginal key, whose hosts are a tenth of the woods.
- ***B. pinophilus*:**
  - one window from May to early November, with no summer gap (the Trentino-Alto Adige shape);
  - Scots pine and mountain pine a full host, larch non-host;
  - band 700-1,900 m, zero at 400 m and 2,300 m.

## Gallinacci (*Cantharellus* s.l.: "finferli", "galletti", "chanterelles")

**Regional evidence.**
- **Which chanterelle.** *C. cibarius* s.str.:
  - all 9 regional species-level records;
  - the checklist has *C. cibarius*, *C. cinereus* and *C. aurora*, and none of the Mediterranean
    segregates the Tuscan tiers were built on (`vda_marra2001_macromiceti`) [plausible].
- **Collections and hosts:**
  - under spruce at Cogne ("Abete rosso"; "Picea-Larix", 1 September 1982);
  - in larch, birch, rowan and Scots pine woods in the Val Ferret (25 September and 10 October 1979);
  - in "Boschi di larice" at La Thuile (1,800-1,900 m, "Esemplari piccoli");
  - in Scots pine and spruce at Lolair (June-August 2000);
  - under *Pinus uncinata* at Mont Avic, 25 August to 8 October 1999, at 1,500-1,850 m
    (`vda_peretti1999_mont_avic`) [plausible].
- **Timing** (folklore):
  - first chanterelles in early July: 2020, "le prime interessanti nascite di Galletti/Finferli nei
    boschi più umidi dei settori occidentali, e a Nord della Dora da Valpelline a Gressoney"
    (`vda_fm_2020_07_03`); 2022, "in quantità ... in regione" (`vda_fm_2022_07_01`);
  - in 2024, "moltissimi Finferli" in the valleys flooded at the end of June, where no porcini came
    (`vda_fm_2024_07_25`).
- **Swiss partners** (`mushma_occurrence_check_vda_2026`) [plausible]: beech 550, spruce 294, fir 256,
  oak 44, larch 32 and Scots pine 18 of 1,271 records naming a tree.

**Decisions.**
- **Hosts:**
  - fir/spruce and beech to host (1.0);
  - mountain pine to secondary (0.6: Scots pine and *Pinus uncinata*, the Mont Avic collections);
  - larch-stone pine and green-alder scrub to non-host (0.1), with the same first knob as for
    porcini;
  - downy oak stays marginal: it is the dry, sunny woodland of the central valley.
- **Season:**
  - lowland window full mid-June to 31 October, closed 30 November; no winter mode;
  - mountain window full 1 July to 30 September, closed 31 October;
  - the handover stays at 600-1,000 m;
  - the disabled two-flush rule also closes on 30 November.
- **Altitude:** full to 1,850 m, zero at 2,250 m, a little above Trentino-Alto Adige because the belts
  are higher here.
- **Soil pH and lithology stay disabled.** The region's substrates are mostly siliceous (gneiss and
  schists, with calcschists in places), but the region grid's pH has not been computed yet.

## Keys and groups dropped

### Ovoli (*Amanita caesarea*): dropped

**Evidence of absence.**
- **Records:** none in iNaturalist (2,794 fungi records in the region) or GBIF
  (`mushma_occurrence_check_vda_2026`) [plausible].
- **Regional checklist:** its Amanitas are citrina, crocea, fulva, gemmata, lepiotoides, muscaria,
  pantherina, phalloides, porphyria, rubescens and vaginata (`vda_marra2001_macromiceti`) [plausible].
  The same source notes the death cap "relativamente abbondante dalla bassa valle fino all'altezza del
  castello di Ussel": the Bassa Valle's broadleaf Amanitas were watched.
- **Survey:** the one full-season survey of the region's downy-oak and chestnut woods ran at the Lago di
  Villa, Challand-Saint-Victor, 820-969 m, from 2 November 1999 to 13 November 2000. It listed six
  ectomycorrhizal Amanitas, none of them *A. caesarea* (`vda_marra2000_lago_villa`) [plausible].
- **Picking law and press:** the 1977 law names no species (`vda_lr16_1977_funghi`). No bulletin or
  paper read mentions ovoli in the region.
- **Altitude:** the species is "Assente oltre i 500 metri al Nord Ovest italiano"
  (`funghimagazine_ovolo`) [folklore]. The region's woods begin at about 300 m in the Bassa Valle, and
  only 56 of the 1,174 approximated woodland cells lie below 700 m. Under the Tuscan band (full to 750
  m, zero at 1,100 m) 7 % of the cells would get full altitude credit.

**Why absence is not proven.**
- The region is Italy's least recorded for fungi (`vda_onofri2003_checklist`) [strong], and the Bassa
  Valle chestnut belt between Pont-Saint-Martin and Montjovet has hardly been surveyed.
- The species is close:
  - Chiaverano, in the Canavese, 639 m, October 2023: 7.5 km from the regional border;
  - Masino, 414 m, 2022: 22.6 km;
  - Savièse above Sion in Valais, 1,069 m, "Quercus, Pinus, Juniperus, mousse", 29 September 1997: 34
    km, across the main ridge, on a dry inner-Alpine adret like the central valley's;
  - SwissFungi's Swiss records reach 1,104 m (`mushma_occurrence_check_vda_2026`).
- In Haute-Savoie, "Avec le réchauffement climatique on la trouve de plus en plus fréquemment plus au
  nord" (`vda_faverges_amanite_2023`) [folklore].

**What would bring it back:** a dated, located find in the Bassa Valle (Pont-Saint-Martin, Donnas,
Perloz, Lillianes, Bard, Hône, Arnad, Issogne, Verrès, Montjovet), from the Associazione Micologica
Valdostana, the USL mycological inspectorate or a verified iNaturalist record. The group would then
come back as in Piemonte:
- band full to 700 m, zero at 900-1,000 m;
- season August-September;
- hosts: chestnut and downy oak.

Until then an ovoli score would be a guess outside the evidence. With no key, the group is omitted from
the region's species list (`species/README.md`).

### *B. aereus* (porcino nero): dropped

- **Records:** none in the region's iNaturalist, GBIF or SwissFungi Valais records; one in the whole
  neighbourhood, in Haute-Savoie at 893 m (`mushma_occurrence_check_vda_2026`) [plausible].
- **Literature:** absent from the regional checklist and from the Lago di Villa survey, whose only
  porcino is *B. aestivalis* (`vda_marra2001_macromiceti`, `vda_marra2000_lago_villa`) [plausible].
- **Press:** absent from every Valdostan Funghi Magazine report read. In Piemonte in 2024 "a Nord del Po
  non si è visto nascere un solo Porcino Nero/Boletus aereus" (`funghimagazine_2024_10_11`) [folklore].
- **The north in general:** the north-east census allows it only "occasionalmente ... nelle regioni
  alpine, in habitat idonei" (`muse_censimento_boletus`) [plausible].

Its hosts exist (chestnut 4,720 ha, downy oak 3,846 ha), but the porcini group takes the max over its
keys, and *B. reticulatus* and *B. edulis* already score those woods. A key with no evidence of fruiting
would only add summer-autumn scores to the Bassa Valle.

## Weather rules: why none changed

- **No regional numbers.** No Valdostan study gives a rain amount, lag or temperature threshold.
- **Mont Avic agrees in words** (`vda_peretti1999_mont_avic`) [plausible]. The factor `notes` quote
  it:
  - in 1997 fruit bodies came "solo dopo le piogge del 2-3/9 e del 13/9", abundant on the 16th,
    13-14 days after the first rain (the *B. edulis* lag is full at 10-16 days);
  - the rain of 28 August gave nothing, "probabilmente a causa dell'abbassamento delle temperature
    minime", which the growth clock's cold slow-down stands for;
  - in 1998 a rainless September with "forte vento per diversi giorni consecutivi" delayed the flush to
    October, which the ET0 drying rule stands for;
  - -10 °C on 28 October 1997 ended fruiting (the frost stoppers).
- **A dry central valley.** 550 mm a year at Aosta against about 950 mm on the Piedmontese border and
  more at altitude (`vda_cf_inquadramento_climatico`):
  - the porcini 30-day rain is a percentage of each cell's own normal, so it adapts;
  - the gallinacci 30-day ramp (15 → 70 mm) will bind more often on the dry adret, where chanterelle
    hosts are few anyway.
- **Foehn.** Funghi Magazine blames "vento favonico" or "vento secco" in 2020, 2021, 2022, 2023 and
  2025. The ET0 drying rules are the only stand-in; the known gap `drying_wind` (gusts plus low
  humidity) would suit this region best of all.
- **Rain scale and lapse rates** are region-config questions (`regions/valle_d_aosta.md`); the card
  notes that much of the woodland sits above the 1,700 m clamp of the national rain scale.

## Slope and sun exposure

- **Slope, every key.** The region grid did not exist, so the woods were approximated by the 1 km
  cells at least half covered by trees on ESA WorldCover 2021, with slopes from the Copernicus 30 m
  DEM by the grid's own method (`mushma_vda_terrain_check_2026`).
  - The 1,174 cells run p10 20.4°, median 28.5°, p75 32.8°, p90 36.5°, max 44.4°, and 72 % are
    steeper than 25°: the steepest woods of any region so far.
  - By the Tuscan rule (x1 to about the p90, x0.8 from about the max), the band is x1 to 36° and x0.8
    from 45°.
  - **Recheck on the region grid once it is built.**
- **Sun exposure, kept.** On 15 October the approximated woodland cells below 1,000 m run p10 66 %,
  median 98 %, p90 124 % of flat ground's sun (Tuscany 89/100/110 %; Trentino-Alto Adige 73/98/121 %).
  The steep valley sides spread the ratio as wide as in Trentino-Alto Adige, so the dry-side stoppers
  dock about two fifths of the low woods and the shade-side ones about 30 %. The bands are statements
  about sun and drying, not percentiles, so they are kept; each file's `notes` says so.

## Press contrasts (`sanity.yaml`)

`valle_d_aosta/sanity.yaml` holds 12 porcini contrasts from 2019-2025, written down on 2026-09-29 before
the region had any scores.

**Sources.**
- **Valdostan papers:** a research agent searched AostaSera, AostaOggi, Gazzetta Matin, La Vallée
  Notizie, Bobine.tv, 12vda and Valledaostaglocal. They print seizures, USL notices and single finds,
  but no season comparisons. La Stampa Aosta and Rai TGR could not be read.
- **So every contrast rests on Funghi Magazine (FM):** one editor's weekly bulletins, mixing reader
  reports with rain-gauge reasoning. Several contrasts partly test the rain data ("rain-led" below).
- **Checked:** I opened every main and second source and checked each quote against the page's text;
  dates are the pages' own publication dates.

**Areas.** Areas are ISTAT 2025 comuni, every name checked against the ISTAT list. The list writes
"Etroubles" and "Emarèse" without an accent on the E. The approximated woodland cells per area give
their size:

| area | comuni | approximated woodland cells | median elevation |
|---|---|---|---|
| `lys` | Valle di Gressoney (7) | 112 | 1,541 m |
| `cervino` | Valtournenche, Antey-Saint-André, La Magdeleine, Chamois, Torgnon | 53 | 1,834 m |
| `rosa_cervino` | Lys, Ayas, Brusson, Challand-Saint-Anselme and Cervino (15) | 238 | 1,657 m |
| `gran_paradiso` | Cogne, Valsavarenche, Rhêmes-Notre-Dame, Rhêmes-Saint-Georges, Introd, Aymavilles | 109 | 1,678 m |
| `east_of_aosta` | from Quart and Brissogne down to Pont-Saint-Martin, side valleys included (39) | 646 | 1,473 m |
| `west_of_aosta` | from Sarre and Aymavilles up to Courmayeur, the Gran Paradiso valleys and Valgrisenche (17) | 307 | 1,616 m |
| `north_of_dora` | the adret and the left-bank valleys (Valdigne north side, Gran San Bernardo, Valpelline, Saint-Barthélemy, Cervino, Ayas, Lys; 40) | 623 | 1,597 m |
| `south_of_dora` | the envers and the right-bank valleys (La Thuile, Valgrisenche, Gran Paradiso valleys, Cogne, Clavalité, Mont Avic, Champorcher; 23) | 370 | 1,576 m |
| `region` | all (`*`) | 1,174 | 1,565 m |

Comuni that straddle the Dora (Courmayeur, Morgex, Aosta, Châtillon, Chambave, Montjovet, Verrès,
Pont-Saint-Martin and a few others) are left out of both Dora areas. **Normal:** 2017-2025.

| id | higher | lower | window | main source | second sources | caveats |
|---|---|---|---|---|---|---|
| `region_2023_2022_mid_august` | region 2023 | region 2022 | 08-12 → 08-26 | [FM, 2023-08-17](https://funghimagazine.it/aggiornamento-funghi-17-08-2023/): "Dopo lunga attesa, registriamo finalmente discrete o buone nascite di funghi Porcini anche in Val d'Aosta"; "In tutta la regione le piogge sono state abbastanza democratiche" | [FM, 2022-08-18](https://funghimagazine.it/molti-funghi-in-molte-zone-ditalia/): "l'intera Val d'Aosta, con poche eccezioni per i settori orientali" among the zones "leggermente o assai più sfavorite"; [FM, 2022-08-26](https://funghimagazine.it/nuovo-boom-di-porcini/): "Fanalino di coda Val d'Aosta, baciata da piogge sempre troppo brevi, irrisorie e spesso seguite da vento secco"; [ANSA, 2022-08-19](https://www.ansa.it/canale_terraegusto/notizie/mondo_agricolo/2022/08/19/maltempo-molti-funghifinalmente-primi-porcini-dopo-siccita_26841a57-da53-423f-a241-ffd3c238a715.html): "In ritardo ad oggi la raccolta in Valle d'Aosta" | FM only (ANSA quotes FM); 2023 was "discrete o buone", not a boom; 2022 partly rain-led |
| `region_2021_2022_august` | region 2021 | region 2022 | 08-05 → 08-20 | [FM, 2021-08-06](https://funghimagazine.it/aggiornamento-meteofunghi-porcini-06-08-2021/): "Dopo anni di simil-siccità, finalmente è piovuto copiosamente ... si sono registrate importanti nascite di funghi, anche e soprattutto Porcini" | [FM, 2021-08-12](https://funghimagazine.it/aggiornamento-meteofunghi-porcini-12-08-2021/): "proseguono le nascite"; the 2022 bulletins above | FM only; by 12 August 2021 the flush was mostly adult fruit bodies |
| `region_2021_august_normal` | region 2021 | region, normal | 08-01 → 08-31 | [FM, 2021-09-10](https://funghimagazine.it/aggiornamento-meteofunghi-10-09-2021-tanti-funghi-porcini/): "dopo un lungo mese di ottime nascite ... la super buttata è ormai giunta al capolinea" | FM 2021-08-06 (above) | FM only; FM's 2023 recap called "gli ultimi anni" before 2023 "siccitosi e poveri", in tension with this |
| `gran_paradiso_2019_2020_august` | Gran Paradiso valleys 2019 | same, 2020 | 08-10 → 08-25 | [FM, 2019-08-16](https://funghimagazine.it/buone-nascite-di-funghi-porcini-vediamo-dove-le-piogge-caduta-in-italia/): "principalmente a Sud nelle valli del Gran Paradiso e soprattutto ad Est al confine col Piemonte"; [FM, 2019-08-29](https://funghimagazine.it/grandi-nascite-di-funghi-porcini-ma-troppi-funghi-nel-cesto-le-piogge-cadute-in-italia/): "la buttata prosegue ancora nei settori delle vallate del Gran Paradiso" | [FM, 2020-08-20](https://funghimagazine.it/aggiornamento-meteofunghi-20-08-2020/): "le valli del Gran Paradiso a secco da settimane" | FM only; the 2020 side is rain-led |
| `lys_vs_gran_paradiso_august_2020` | Valle di Gressoney 2020 | Gran Paradiso valleys 2020 | 08-05 → 08-25 | FM 2020-08-20: "cenni di nascite ad Est al confine con Valsesia e Biellese ... con le valli del Gran Paradiso a secco da settimane" | [FM, 2020-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2020/): "Qualche discreta nascita ... soprattutto nella valle di Gressoney" | a poor August everywhere: "cenni" against nothing |
| `lys_vs_cervino_august_2020` | Valle di Gressoney 2020 | Cervino valleys 2020 | 08-05 → 08-31 | FM 2020-09-04: "soprattutto nella valle di Gressoney al confine con la Valsesia, non al confine con le valli del Cervino" | [FM, 2020-08-07](https://funghimagazine.it/aggiornamento-meteofunghi-07-08-2020/): "Valle di Gressoney con cenni di sconfinamento anche in Valle d'Aosta orientale" | low levels; the lower side is one clause |
| `rosa_cervino_vs_gran_paradiso_september_2019` | Rosa and Cervino valleys 2019 | Gran Paradiso valleys 2019 | 09-12 → 09-20 | [FM, 2019-09-20](https://funghimagazine.it/dove-stanno-nascendo-i-funghi-porcini-le-piogge-cadute-in-italia/): "le prime nascite si registrano già ad Oriente ... nelle valli del Rosa e del Cervino. A giorni dovrebbero partire anche nelle valli del Gran Paradiso" | — | the start of a flush only; FM only |
| `south_vs_north_dora_late_august_2021` | south of the Dora 2021 | north of the Dora 2021 | 08-22 → 09-04 | [FM, 2021-09-04](https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): "a Sud della Dora Baltea le nascite rallentano o cessano"; "Assai peggio a Nord della Dora dove il vento favonico ha letteralmente prosciugato ogni cenno d'acqua presente nei boschi" | — | both sides declining; tests the foehn (ET0 drying) |
| `east_vs_west_autumn_2023` | east of Aosta 2023 | west of Aosta 2023 | 09-20 → 10-10 | [FM, 2023-10-04](https://funghimagazine.it/aggiornamento-porcini-04-10-2023/): "accumuli nettamente inferiori ad Ovest di Aosta ma più consistenti sui settori Est dove le nascite di funghi Porcini continuano ininterrotte ormai da settimane" | [FM, 2023-10-12](https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "del tutto cessate sui settori Ovest"; [FM, 2023-09-20](https://funghimagazine.it/aggiornamento-porcini-20-09-2023/): heavy rain on 13 September over "Aosta Est" | partly rain-led, but "continuano ininterrotte" is an observation |
| `south_vs_north_dora_september_2024` | south of the Dora 2024 | north of the Dora 2024 | 09-12 → 09-20 | [FM, 2024-09-19](https://funghimagazine.it/aggiornamento-nascite-funghi-19-09-2024/): "nelle zone a nord della Dora Baltea fa ancora molto freddo e le nascite sembrano bloccate o rallentate"; "Situazione leggermente migliore a sud della Dora" | — | "leggermente"; early buttons only; tests the temperature rules |
| `region_june_july_2024_normal` | region 2024 | region, normal | 06-20 → 07-15 | [FM, 2024-06-28](https://funghimagazine.it/aggiornamento-funghi-28-06-2024/): "Chi l'avrebbe mai detto, eppure in Val d'Aosta si stanno raccogliendo bene funghi Porcini, per lo più Porcini rossi-pinicola" | [FM, 2024-07-25](https://funghimagazine.it/aggiornamento-funghi-25-07-2024/): "massicce (per lo più passate in sordina) nascite di Porcini Rossi-Pinicola", "una bellissima e insolita buttata" | mostly *B. pinophilus* and *B. reticulatus*; floods at the end of June hit the Gran Paradiso and Cervino-Rosa valleys |
| `region_late_july_vs_early_august_2025` | region, 26 Jul-1 Aug 2025 | region, 6-14 Aug 2025 | two windows, one year | [FM, 2025-08-01](https://funghimagazine.it/aggiornamento-nascite-01-08-agosto-2025/): "piccola sorpresa. Senza piogge violente ma con clima fresco, si segnalano buone nascite su tutto il territorio, dai fondovalle ai monti" | [FM, 2025-08-08](https://funghimagazine.it/aggiornamento-nascite-funghi-08-14-agosto-2025/): "Nascite molto localizzate. Le zone più alte sono state colpite da caldo, vento e grandinate" | both windows inside the full season, so it tests the weather rules; hail is not modelled |

**Left out.**
- **Weak or one-sided:**
  - eastern VdA "allo sbocco sul Piemonte" against the rest in July 2022 ("qualche timidissimo cenno");
  - the flooded valleys against the rest in late July 2024 (the higher side is "in valle");
  - southern against northern VdA in June 2024 (sporadic finds);
  - late June 2024 against early July 2023 (in 2023 the foehn ended a flush that had begun);
  - September 2025 against September 2022: the 2025 side is a Corpo forestale seizure of 19 kg at
    Issogne and 10 kg at La Salle (AostaSera, 2025-09-27) and a list of crowded spots, which count
    pickers, not fruiting;
  - a Morgex forager's photo in August 2019 (Valledaostaglocal);
  - the 2020 hail on the Piedmontese border (retrospective, unplaced).
- **Contradictory:** chanterelles in the flooded valleys, "moltissimi Finferli" on 25 July 2024 and
  "persino pochi Finferli" on 16 August 2024.
- **No gallinacci contrast.** The chanterelle notes found are one-sided (first flushes in July 2020 and
  2022, "Ottimi" after rain in early August 2024) or the contradictory pair above.
- **No 2016-2018 season report** was found for the region.

**Year picture from the press** (context, not scored; FM unless stated):

| year | Valle d'Aosta |
|---|---|
| 2016-2018 | no regional season report found |
| 2019 | first chanterelles and porcini in early August; mid-August flush in the Gran Paradiso valleys and the east; declining in the east by early September; new flushes in the Rosa and Cervino valleys around 20 September |
| 2020 | early July *B. edulis* in the west (Courmayeur) and chanterelles; a poor August ("col contagocce"), only the Gressoney valley; the Gran Paradiso valleys dry |
| 2021 | after "anni di simil-siccità", first *B. edulis* in late July and "un lungo mese di ottime nascite" to early September; the north of the Dora dried by foehn |
| 2022 | the driest year in 80 years (`vda_siccita_2022`); chanterelles in quantity in early July, porcini blocked by wind; "Fanalino di coda" in August; modest in September |
| 2023 | foehn stopped the early-summer red porcini; "finalmente discrete o buone" from mid-August; continuous in the east into early October, over in the west by 12 October; FM's recap: "il ritorno dei Porcini, finalmente in quantità" |
| 2024 | red porcini from late May, "insolita buttata" in June-July; floods on 29-30 June in the Gran Paradiso and Cervino-Rosa valleys (chanterelles, no porcini); 36 °C at Aosta in early August; early buttons south of the Dora in mid-September, the north still cold |
| 2025 | hail at Cogne and Pila in early July; first *B. edulis* in conifers in late July; "buone nascite su tutto il territorio" on 1 August, then "molto localizzate"; a strong mid-September flush (crowds at Pontboset, Brusson, Gressan, Champdepraz) |

## Open questions

- **Larch.** 0.1 here, as in the eastern Alpine regions; Piemonte kept 0.3 on the same typology. Three
  tests:
  - the sanity contrasts in the larch-rich `cervino` and `west_of_aosta` areas;
  - the backtest, when there are presences to test with;
  - whether the regional forest map carries the larch variants with spruce or fir (a grid mapping
    question for the region card).

  The four Alpine regions should end on one value.
- **Ovoli.** Ask the Associazione Micologica Valdostana or the USL mycological inspectorate whether
  ovoli are ever brought in from the Bassa Valle. The *A. caesarea* and Valle d'Aosta chapters of
  Suriano & Sitta's *Etnomicologia in Italia* (not online) would say whether the region ever ate them.
- ***B. edulis* window split.** The handover (900-1,300 m) rests on neighbourhood records, not
  regional ones. The backtest should compare it with Trentino-Alto Adige's single window.
- **Slope and sun on the real grid.** Both were approximated from WorldCover and the DEM; recheck
  them when the region grid exists.
- **Rain.** The central valley's rain shadow is extreme (364 mm at Saint-Vincent in 2022). Whether
  ERA5-Land resolves it is a gauge-check question for the region card.
- **Leads not read:**
  - Suriano & Sitta's book;
  - the Associazione Micologica Valdostana's own records;
  - Rai TGR Valle d'Aosta and La Stampa Aosta (blocked or not indexed);
  - the Corpo forestale's yearly seizure counts, a possible season index.

## References added for Valle d'Aosta

| id | kind | verified | used for |
|---|---|---|---|
| `mushma_occurrence_check_vda_2026` | analysis | verified | regional, neighbourhood and Valais records: months, enrichment, elevations, Swiss partner trees, nearby ovoli |
| `mushma_vda_terrain_check_2026` | analysis | verified | approximated woodland elevation, slope and sun ratio; altitude-gate coverage |
| `vda_tipi_forestali_2007` | institutional | verified (PDF) | forest types, belts, larch composition and history |
| `vda_carta_forestale_2020` | institutional | verified (PDF) | category and type areas, 2020 |
| `vda_cf_inquadramento_climatico` | institutional | verified | the central valley's rain shadow |
| `vda_annuario_2023_precipitazioni` | institutional | verified (PDF) | 2022 rain totals |
| `vda_siccita_2022` | institutional | verified (PDF) | 2022 the hottest, driest year in 80 |
| `vda_lr16_1977_funghi` | institutional | verified | picking law: no calendar, no species rule |
| `vda_marra2001_macromiceti` | society | verified (PDF) | regional checklist; old collections, hosts, dates, altitudes |
| `vda_marra2000_lago_villa` | society | verified (page images) | oak-chestnut survey: no ovoli, no *B. aereus* |
| `vda_peretti1999_mont_avic` | society | verified (page images) | Mont Avic fruiting dates, altitudes, weather in words |
| `vda_onofri2003_checklist` | peer-reviewed | verified (PDF) | the region is Italy's least recorded for fungi |
| `vda_faverges_amanite_2023` | society | verified | ovoli spreading north in Haute-Savoie |
| `vda_fm_2020_07_03` | web | verified | first *B. edulis* and chanterelles, July 2020 |
| `vda_fm_2021_08_06` | web | verified | first *B. edulis* late July 2021 |
| `vda_fm_2022_07_01` | web | verified | chanterelles in quantity, July 2022 |
| `vda_fm_2023_10_12` | web | verified | season end in the west, October 2023 |
| `vda_fm_2024_05_31` | web | verified | first *B. pinophilus* at 800-1,000 m, May 2024 |
| `vda_fm_2024_06_14` | web | verified | pinophilus hosts and sunny southern slopes |
| `vda_fm_2024_06_28` | web | verified | pinophilus and reticulatus flush, June 2024 |
| `vda_fm_2024_07_25` | web | verified | the 2024 pinophilus buttata, reticulatus, flooded valleys |

Existing references the changes lean on, opened again for this card:
- `taa_mandolini2025_larix` (full text via Europe PMC) and `taa_mandolini2024_cembra` (abstract);
- `funghimagazine_laricino`, `funghimagazine_ovolo`, `funghimagazine_2024_10_11`;
- `muse_censimento_edulis`, `muse_censimento_cibarius`, `muse_censimento_pinophilus`;
- `swissfungi_wsl` (the atlas REST service, partner trees and altitude extremes).

Existing references cited without reopening: `mushma_swissfungi_check_2026`, `diez2020_alps`,
`olariaga2017`, `taa_muse_censimento_aestivalis`, `muse_censimento_boletus`.
