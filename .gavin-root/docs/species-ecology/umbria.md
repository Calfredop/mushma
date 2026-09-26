# Species ecology: Umbria

Research date: 2026-09-25. Card: `region-umbria.md`. Rule files: `api/src/api/config/species/umbria/`.
It covers **fruiting conditions only**: seasons, hosts, altitude, weather and places. Nothing here
is about edibility or identifying specimens.

Umbria starts from Tuscany's rule set (`species/tuscany/`, evidence in `species-ecology.md` and the
three appendices next to this file). This page records the Umbrian evidence, and every place it
changes or confirms a Tuscan rule. The Umbrian sources have no numbers on weather and fruiting, so
**every weather rule is Tuscany's, unchanged**. All six keys and all three groups exist in Umbria;
**no group is dropped**.

## At a glance

| key | factor | Tuscany | Umbria | why |
|---|---|---|---|---|
| `porcini_aereus` | season: upland/lowland handover | 400 → 600 m | **800 → 1,000 m** | "o prima ma ad altitudini sopra gli ottocento mille metri" (Regione Umbria 2013, p. 144) |
| `porcini_aereus` | habitat: beech | 0.1 (non-host) | **0.3** (marginal) | "non disdegnando comunque anche il faggio" (ibid.) |
| `ovoli_caesarea` | altitude zero | 1,100 m | **1,000 m** | "ad altitudini inferiori agli 800/900 m" (ibid., p. 44) |
| `gallinacci_cibarius` | lowland season end | full to 15 Dec, 0 by 25 Jan | **full to 15 Nov, 0 by 15 Dec** | no coastal lowland; "da maggio a ottobre" (ibid., p. 163); records stop in November |
| `gallinacci_cibarius` | `season_two_flush` (disabled) autumn end | 15 Dec → 25 Jan | 15 Nov → 15 Dec | kept in line with the main season rule |
| every key | everything else | | unchanged | the Umbrian sources confirm seasons and hosts, or say nothing |

Every changed number is still a derived prior, as in Tuscany. The Tuscan-tuned choices (the rain
factor as a percentage of the cell's normal, habitat saturation at a 0.3 host share; see
`model-v1-validation.md`) are carried over as priors: Umbria has too few sightings to tune anything
(see Sightings).

## Sources

The anchor is the Region's own field guide, written with the Gruppo Micologico Ternano:
**Regione Umbria & GMT (2013), *Funghi e tartufi dell'Umbria*** (`regione_umbria_funghi2013`,
institutional, read in full). It gives each taxon's season, hosts and how common it is in Umbria.
Twelve references were added to the shared bibliography (`references.yaml`):

| id | kind | what it supports |
|---|---|---|
| `regione_umbria_funghi2013` | institutional | per-taxon season, hosts and frequency in Umbria |
| `regione_umbria_stato_foreste2009` | institutional | INFC 2005 forest categories; forest-soil pH survey |
| `regione_umbria_castagno2025` | institutional | where Umbrian chestnut grows, its belt, acid soils |
| `angelini2016_collestrada` | peer-reviewed | rain and humidity drive fruiting (Umbrian community study) |
| `angelini2017_umbria_checklist` | peer-reviewed | the Umbrian checklist (abstract only) |
| `umbria24_bistocchi2022`, `umbria24_loschi2023` | web | regional mycologists on "i nostri porcini" and ovoli |
| `umbriaoggi_dove_funghi2019`, `costacciaro_funghi_monte_cucco` | web | forager areas (folklore) |
| `mushma_umbria_occurrence_check_2026` | analysis | Umbrian iNaturalist/GBIF counts, aggregates only |
| `mushma_umbria_grid_check_2026` | analysis | habitat shares, elevation and pH of the Umbrian grid |

Also read, not cited in the rules: the regional collection law (L.R. 12/2000, ISPRA summary 2021),
which has **no season calendar**, only night-time bans, so unlike the Borgotaro IGP it gives no
season prior; and the *Piano di Tutela delle Acque* (2009) on where limestone, sandstone and
volcanic rocks lie.

## Regional context

### Oak woods, little chestnut, no fir

INFC 2005 (Regione Umbria 2009, pdf p. 6): "le cerrete (circa 120'000 ha), i boschi di roverella
(oltre 96'500 ha), gli ostrieti (circa 60'000 ha) e le leccete (circa 40.000 ha)". Coppice is 87 %
of the classified woods. The Umbrian grid (CLC IV level alone, `regions/umbria.md`) shows the same:

| habitat, share of the wooded area | Umbria | Tuscany |
|---|---|---|
| deciduous oak | **58.8 %** | 36.1 % |
| mixed broadleaf | 11.1 % | 4.9 % |
| evergreen oak | 9.6 % | 12.9 % |
| beech | 6.5 % (dominant cells at a mean 1,197 m) | 8.5 % (1,106 m) |
| chestnut | **1.5 %** | **18.7 %** |
| fir and spruce | **0** | 0.6 % |

Chestnut is a scattered, acid-soil habitat in Umbria: "la necessità imprescindibile dell'acidità dei
suoli", about 1,000 ha in the 500–600 m belt (Alto Tevere, Spoletino, Amerino, Orvietano, Pievese;
Regione Umbria / 3A-PTA 2025, pp. 66–67). CLC folds most small stands into oak.

### Calcareous soils

The regional forest-soil survey (Regione Umbria 2009, Tabella 6) found 29 of 318 horizons acid
(mean pH 5.3); even the sandstone, marnoso-arenacea and volcanic soils average pH 7.4, and the
calcareous ones 8.1. SoilGrids agrees at 250 m: **no Umbrian woodland cell is below pH 6.0**
(median 6.89). So:

- the disabled gallinacci pH rule stays disabled: it would lower every Umbrian cell alike;
- no calcareous penalty for ovoli (see below).

## Per taxon

### Porcini

The Umbrian porcino is the thermophilous pair. Giancarlo Bistocchi, Umbrian mycologist:
"i nostri porcini, ovvero i boletus aereus e aestivalis, prediligono temperature miti e molta
pioggia" (Umbria24, 2022). Luciano Loschi (Foligno): "I funghi porcini che crescono in Umbria in
ambienti xerofili, cioè caldi, in simbiosi con cerro, roverella, castagno" (Umbria24, 2023).

- ***B. edulis*.** "Cresce dalla tarda estate all'autunno inoltrato, a volte in stagioni particolari
  compare anche in primavera. Sia sotto latifoglia che sotto conifere (faggi, castagni ed abeti
  soprattutto). Poco comune in Umbria" (p. 141). Window, hosts and altitude band match Tuscany:
  **kept**. With no fir and little chestnut it scores almost only in the beech belt (Monte Cucco,
  the Apennine ridge, the Sibillini side of Norcia). No Umbrian records exist to test it.
- ***B. reticulatus* (= *aestivalis*).** "Specie xerofila, cresce a partire dal periodo estivo fino
  all'autunno, da maggio a ottobre in boschi soleggiati di latifoglia (castagno, quercia e faggio)
  … molto comune nella nostra regione" (p. 143). Matches Tuscany's window and host tiers: **kept**.
  Umbria's oak woods are its main habitat.
- ***B. aereus*.** "Specie autunnale, a volte anche a fine estate, o prima ma ad altitudini sopra
  gli ottocento mille metri. È più frequente in luoghi soleggiati ed asciutti, prediligendo boschi
  di querce e castagni, non disdegnando comunque anche il faggio" (p. 144). This independently
  supports the Tuscan split into a lowland autumn window and an earlier upland one, but puts the
  handover higher: **800 → 1,000 m** instead of 400 → 600 m. Beech becomes **marginal (0.3)**; the
  altitude gate (full to 800 m, 0 at 1,250 m) keeps it off the high beech. The 8 Umbrian records
  peak in September.
- ***B. pinophilus*.** "Cresce in autunno, con possibili ma non frequenti comparse primaverili, in
  boschi di latifoglia (faggio e querce) e sotto abete o pino. … non è comune in Umbria" (p. 142).
  **Kept**: the book makes the spring flush rarer but gives no dates, and the group score takes the
  max, so this key only matters in beech, where *B. edulis* already scores. Nothing was found on
  porcini in Umbrian black-pine plantations.

### Ovoli (*Amanita caesarea*)

"Predilige zone calde e secche, cresce in estate e autunno, in boschi di castagno, cerro e
roverella, ad altitudini inferiori agli 800/900 m" (p. 44). Crops came "da metà settembre" in 2023
(Loschi) and into October in 2022 (Bistocchi); the 3 Umbrian records are September and October.

- Season and hosts: **kept**.
- Altitude: zero at **1,000 m** instead of 1,100 m; full credit still ends at 750 m.
- Substrate: the Tuscan appendix leans towards siliceous soils, but the Umbrian book names roverella
  woods, which in Umbria grow mostly on limestone. The substrate stays a known gap; **no calcareous
  penalty** is added.

### Gallinacci (*Cantharellus* s.l.)

"Ubiquitario, cresce da maggio a ottobre in gruppi numerosi ad altitudini varie. Preferisce nel
centro Italia i boschi di latifoglia" (p. 163). The 6 Umbrian records are *C. pallens* (3),
*C. alborufescens* (1), *C. cibarius* (1) and one genus-level: the same Mediterranean segregates as
in Tuscany (`olariaga2017`), in May–June and October–November.

- Season: the lowland window now ends by **15 December** (full to 15 November). Tuscany's tail into
  January came from coastal and low records; Umbria has no coastal lowland (woodland p10 360 m) and
  no Umbrian record after November. The frost and snow rules still cut the late season. The
  mountain window is kept.
- Hosts: **kept**. Chestnut, the strongest host, is only 1.5 % of the Umbrian woods, so the habitat
  factor is low in most cells. The book's "boschi di latifoglia" is too generic, and there are no
  Umbrian plot data, to promote deciduous oak. **Watch gallinacci in the backtest and the sanity
  check.**
- Soil pH: stays disabled (see Calcareous soils).

## Weather

No Umbrian study links rain or temperature to fruiting for any of these taxa. The one Umbrian
community study, three years in the Collestrada oak woods near Perugia, says "changes of
meteorogical conditions, especially the rainfall level and relative humidity, during the growing
seasons and years have a major impact" (Angelini et al. 2016, abstract). The regional mycologists'
lore ("hanno bisogno di piogge, assenza di vento, sole di giorno e fresco di notte", Loschi 2023)
matches the Tuscan drying-wind, heat-spike and cold-night rules. **All weather rules, growth clocks
and terrain rules are Tuscany's, unchanged**; `salerni2002_oak` (Tuscan oak woods) is the closest
quantitative analogue for Umbria's cerrete. The rain scale is the national default unless the gauge
check says otherwise (`regions/umbria.md`, Validation).

## Sightings

Queried 2026-09-25 (aggregates only; no coordinates stored). Umbria is barely sampled:

| taxon | iNaturalist, verifiable (place 10875) | months |
|---|---|---|
| *B. edulis* | 0 (about 3 expected at the Tuscan rate) | |
| *B. reticulatus* | 5 | Jun 2, Sep 2, Oct 1 |
| *B. aereus* | 8 | Aug 1, Sep 5, Oct 1, Nov 1 |
| *B. pinophilus* | 0 | |
| *A. caesarea* | 3 | Sep 1, Oct 2 |
| *Cantharellus* | 6 | May 2, Jun 1, Oct 1, Nov 2 |
| all fungi | 1,714 | peak Oct–Nov |

GBIF has almost no Umbrian fruit-body records for these taxa; the 1,016-species Umbrian checklist
(Angelini et al. 2017) is not in GBIF. After the ingest's quality filters and the woodland-cell join,
**3 sightings** remain (`regions/umbria.md`). Nothing can be tuned or validated per taxon on
Umbrian records; the numbers only point the same way as the regional book.

## Press contrasts (`sanity.yaml`)

Twelve porcini contrasts from 2019–2025, each quoted from a source opened on 2026-09-25 and written
down before Umbria had any scores. `sanity.py` scores one group per run (porcini by default), so
ovoli claims were left out. Areas are ISTAT 2025 comuni or `'*'` (the whole region).

| id | higher | lower | window | source |
|---|---|---|---|---|
| `valnerina_2023` | Valnerina 2023 | rest of Umbria 2023 | 08-25 → 09-10 | Umbria24, 22 Sep 2023: "Buone raccolte di porcini … in Valnerina dove le piogge sono state più copiose" |
| `alta_valnerina_october_2023` | upper Nera and Corno 2023 | inland Umbria 2023 | 10-01 → 10-12 | funghimagazine, 12 Oct 2023: "In Umbria non si sta raccogliendo più quasi nulla, al di fuori sei [dei] settori Appenninici di confine" |
| `orvietano_2023` (weak) | Orvietano, normal | Orvietano 2023 | 09-15 → 11-20 | Orvietonews, 23 Nov 2023: "una stagione micologica non particolarmente generosa" |
| `umbria_2022_summer` | Umbria, normal | Umbria 2022 | 06-20 → 09-04 | Umbria24 and ANSA, 4 Sep 2022: "la siccità ha bloccato tutto" |
| `umbria_2022_autumn` | Umbria 2022 | Umbria, normal | 09-10 → 10-03 | Umbria24, 3 Oct 2022: "Per porcini e ovoli è una stagione eccezionale" |
| `marche_border_2021` | Umbria–Marche Apennine 2021 | Orvieto border 2021 | 08-28 → 09-10 | funghimagazine, 10 Sep 2021: "Meglio al confine tra Marche ed Umbria, meno bene al confine tra Umbria-Toscana-Lazio" |
| `umbria_2021_early_september` | Umbria, normal | Umbria 2021 | 08-28 → 09-10 | same article: the Perugia storm "non ha sortito alcuna nascita di funghi" (not independent of the one above) |
| `apennine_august_2019` | Umbria–Marche Apennine 2019 | inland Umbria 2019 | 08-05 → 08-16 | funghimagazine, 16 Aug 2019: "Appennino umbro marchigiano in pole" |
| `umbria_2024_autumn` | Umbria 2024 | Umbria, normal | 09-20 → 10-06 | funghimagazine, 27 Sep and 3 Oct 2024; La Nazione, 3 Oct 2024: "un anno da record" |
| `alta_valle_tevere_2024` | Alto Tevere 2024 | Alto Tevere, normal | 10-01 → 10-29 | Corriere di Arezzo, 29 Oct 2024: "raccolte da record … in tutto il territorio dell'Alta Valle del Tevere" |
| `umbria_2025_early` | Umbria 2025 | Umbria, normal | 08-25 → 09-25 | Umbria24, 25 Sep 2025: "raccolti sopra la media", "abbastanza uniforme in tutta la regione" |
| `acquasparta_sellano_2025` (moderate) | Acquasparta and Sellano 2025 | rest of Umbria 2025 | 09-01 → 09-13 | Corriere dell'Umbria, 13 Sep 2025: "Raccolte record … ad esempio nelle zone di Acquasparta e Sellano, per ora a macchia di leopardo" |

Caveats: `orvietano_2023` rests on a passing remark; `acquasparta_sellano_2025` names its areas "ad
esempio", so the safer fallback is the same area against its own normal; the Alto Tevere record of
2024 was found on the Tuscan side, and the claim covers the whole valley. No Umbria-specific source
was found for the 2017 drought. Left out: a Coldiretti estimate of "+25 % on 2018" (7 Sep 2019), and
a 2023 La Nazione piece that reprints Coldiretti's 2020 release word for word.

## Places, for the intro copy

Sourced areas: the beech woods of **Monte Cucco** (Costacciaro, Sigillo) for porcini; the
**Valnerina** (Norcia, Cascia, Preci and the Nera villages) for late-summer porcini; **Città della
Pieve and Pietrafitta**, then Terni, Perugia and Gubbio, for porcini and ovoli in 2022; the
chestnut belts of the **Alto Tevere**, the **Spoletino** (Montebibico), the **Amerino** and the
**Orvietano** for ovoli and summer porcini; the **Monti Martani** and **Monte Subasio** in forager
lore. No source names a gallinacci place in Umbria.

## Gaps and hand-offs

- **Tuning.** 3 usable sightings: the priors ship untuned (`regions/umbria.md`, Validation).
  Pooling Umbria with central Italy would be the next step.
- **Checklist localities.** The Umbrian checklist's locality table (Angelini et al. 2017, closed
  access) would say where each taxon was recorded; it is the best lead for a real habitat check.
- **Chestnut under-mapped.** CLC IV level hides most Umbrian chestnut stands in oak cells. An open
  regional forest map would fix it (`regions/umbria.md`, Sources).
- **Beech belt.** No Umbrian source gives its lower limit; the forest map, not an altitude rule,
  carries beech.
- **Substrate.** Umbria's soils are calcareous almost everywhere at the model's resolution; a
  lithology proxy calibrated in Tuscany would over-state acidity here.
