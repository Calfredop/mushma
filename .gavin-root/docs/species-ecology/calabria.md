# Species ecology: Calabria (regional appendix to species-ecology.md)

Research date: 2026-09-28 (dates Europe/Rome, units metric). Card: `region-calabria-species.md`
(child of `region-calabria.md`). Rule files: `api/src/api/config/species/calabria/`. This appendix
records how the Tuscan rule set (`api/src/api/config/species/tuscany/`) was carried to Calabria, what
changed and why. It covers **fruiting conditions only**: nothing here is about edibility or
identifying specimens.

Citations are the ids in [`references.yaml`](../../../api/src/api/config/species/references.yaml)
(46 added for Calabria, in one block before the Piemonte block, listed at the end of this page).
Confidence levels are the ones in [`species-ecology.md`](../species-ecology.md): **strong**,
**plausible**, **folklore**. Every number is a prior for the backtest; season windows, altitude bands
and habitat affinities stay frozen (`model.yaml`, `backtest.frozen_factor_kinds`).

Campania (branch `region/campania`, not merged yet) was the first southern region and is the nearest
precedent. [Where Calabria departs](#where-calabria-departs-from-campania-and-central-italy) compares
the two, and [The southern season](#the-southern-season) takes the central-Italian windows one by one.

## Summary

1. **All three groups and all six keys are kept.** Porcini, ovoli and gallinacci are common in
   Calabria, and the regional mycological groups have recorded all six for decades. Nothing is
   dropped.
2. **Calabria has a quantitative host table, and it drives most changes.** Two ISPRA manuals
   (`ispra2018_mlg180_calabria_foreste`, `ispra2018_mlg179_calabria_rimboschimenti`) file about
   45,000 records of the Calabrian mycological groups under their habitats and give each species'
   share of each habitat's records. These are frequencies of records, not yields or dates, so they
   count as plausible. A habitat affinity changed only where these shares and the Calabrian
   mycologists' own words agree.
3. **The Sila's laricio pine is *B. pinophilus* ground, not *B. edulis* ground.**
   - Of the 5,464 laricio records, *B. pinophilus* is 0.9 %, the 8th of 933 species. *B. edulis* is
     0.3 % and *B. reticulatus* 0.1 %; there is no *B. aereus*.
   - Lavorato (1996): *B. pinophilus* is "molto diffuso sotto i pini silani secolari". *B. edulis*
     is "molto diffuso sotto faggio ... meno diffuso sotto altre latifoglia e aghifoglia".
   - Dialect keeps the split: "Sillu 'e pinu" against "Sillu 'e fagu" in Acri.
   - So `mountain_pine` (13.8 % of the woods, mostly laricio) becomes a **full host for *B.
     pinophilus*** and a **non-host (0.1) for *B. edulis* and *B. reticulatus***. The chanterelles
     move to 0.1 too. Mixed pine-beech cells keep full credit for every porcino through their beech.
4. **The southern season: earlier, a deep summer gap the weather makes, and a long low-altitude
   tail.**
   - The Calabrian mycologists call the ovolo, *B. edulis*, *B. reticulatus* and the chanterelles
     "precoce". Several windows open two to four weeks earlier.
   - July and August bring 3-4 % of the year's rain even at 1,000-1,350 m in the Sila
     (`bissanti1973_neve_sila`). No calendar gap is written in: the rain, heat and drying rules make
     it, and the July flushes of the Sila, Serre and Catena Costiera still score.
   - *B. aereus* runs to January at low altitude. *B. reticulatus* runs to "periodo quasi
     natalizio", and the chanterelles to January.
5. **The hosts sit 150-250 m higher than in Tuscany and Campania.**
   - On the habitat map the chestnut's median height is 816 m (Campania 658 m) and the beech's 1,270
     m (Campania 1,211 m).
   - The altitude bands of *B. aereus*, the ovolo, *B. reticulatus* and the chanterelles move up.
     *B. edulis* and *B. pinophilus* reach the tree line, as in Campania.
6. **What the habitat classes hold changes several affinities.**
   - Calabria's `macchia` is mostly lentisk and *Cytisus* scrub (63 %), `mediterranean_pine` is
     Aleppo pine (82 %), `mixed_broadleaf` is *Alnus cordata* (86 %) and
     `transitional_woodland_shrub` is *Spartium* and broom (78 %). Each moves down where Tuscany had
     it as a host or secondary.
   - The evergreen oaks move up for the ovolo. Holm oak is 90 % of the class and cork oak 10 %; cork
     oak has the highest ovolo, *B. aereus* and chanterelle shares of any habitat.
7. **Weather rules are all Tuscany's.** No Calabrian study ties fruiting to rain or temperature in
   numbers. The Calabrian field notes agree with the Tuscan lags: ovoli 10-12 days after the last
   useful rain, *B. edulis* and *B. aereus* about 15 (`bosco_grande2004_caesarea_cocuzzo`).
8. **More records than Campania, still too few to tune.** Calabria has 118 iNaturalist records of
   the six keys (Campania 42), all from 2011 on and mostly from 2021 on.

## Calabria in brief

**Woods.** The region card maps Calabria's woods from ISPRA and Regione Calabria's Carta della Natura
habitat map (1:25,000, 2023, CORINE Biotopes codes; `config/regions/calabria.yaml`, written in
parallel). The rules were drafted before the woodland grid existed. So the shares and heights below
come from the map itself (`mushma_calabria_forest_composition_2026`):
- The map was rasterised on a 100 m lattice with Copernicus GLO-30 heights.
- Approximate 1 km woodland cells were built from the same lattice. A cell counts as woodland when
  broadleaf and conifer cover half of it; 5,718 cells qualify.

The map has 714,800 ha of woods, macchia and scrub, 586,700 ha of it broadleaf or conifer woodland.
INFC 2015 gives a bosco of 495,177 ha (`infc2015_calabria`). The map runs 18 % over INFC, which
[Open questions](#open-questions-and-hand-offs) hands to the region card.

This table is **which habitat holds which Calabria tree**:

| habitat key | share | Calabria trees (Carta della Natura code) | median elevation (p10-p90) |
|---|---|---|---|
| `deciduous_oak` | 20.6 % | downy oak 41.732 (49 %), Turkey oak with Hungarian oak 41.7512 (31 %), Turkey oak 41.7511 (20 %), a little sessile oak 41.7513 | 586 m (230-983); downy 404, Hungarian 724, Turkey 834 m |
| `evergreen_oak` | 14.9 % | holm oak 45.31 (53 %) and 45.32 (supra-Mediterranean, 37 %), cork oak 45.21 (10 %), holly | 554 m (234-914); cork oak 297 m |
| `beech` | 14.0 % | southern Italian beech 41.18 | 1,270 m (883-1,640), max 2,045 m |
| `mountain_pine` | 13.8 % | conifers planted outside their range 42.G_n (71 %; the regional "Rimboschimenti di Pinus nigra", i.e. laricio reforestation), conifer plantations 83.31_m (20 %), laricio pine 42.65 (8.5 %), Apennine black pine 42.612 and pino loricato 42.711 (under 1 %) | 1,201 m (754-1,459); 42.G_n 1,223 m, 83.31_m 844 m, 42.65 1,390 m |
| `chestnut` | 12.0 % | chestnut woods 41.9 (98 %), fruit orchards 83.12 | 816 m (521-1,087) |
| `macchia` | 9.8 % | lentisk 32.214 (35 %), *Cytisus* 32.215 (28 %), evergreen-oak matorral 32.11 (24 %), Mediterranean macchia 32.3 (9 %), *Euphorbia*, olive-lentisk, dune scrub | 315 m |
| `transitional_woodland_shrub` | 8.1 % | *Spartium* 32.A (52 %), broom 31.844 (26 %), deciduous scrub 31.81, bramble 31.8A, burnt or felled woodland 31.87, riparian scrub | 717 m |
| `mixed_broadleaf` | 2.3 % | *Alnus cordata* 41.C1 (86 %), hop-hornbeam 41.81 (9 %), ravine woods, aspen | 767 m |
| `mediterranean_pine` | 2.0 % | Aleppo pine 42.84 (82 %), stone pine 42.83, wooded dunes 16.29 | 367 m |
| `riparian` | 1.5 % | poplar 44.61 (73 %), black alder, willow, plane | 194 m |
| `exotic_broadleaf` | 0.6 % | robinia and ailanthus 41.L_n | 333 m |
| `fir_spruce` | 0.5 % | southern Apennine silver fir 42.15 (1,514 ha of it in Serra San Bruno) | 1,076 m (900-1,603) |

The map has no mixed broadleaf-conifer class, so `mixed_broadleaf_conifer` is empty in Calabria. The
Sila's mixed laricio-beech woods sit in pine and beech polygons side by side.

`mountain_pine` is the Sila above all:
- San Giovanni in Fiore holds 14,974 ha of it, Longobucco 10,652, Casali del Manco 4,994 and
  Taverna 4,896.
- The Pollino has about 2,000 ha (Morano Calabro, Castrovillari). The province of Reggio, mostly
  the Aspromonte, has 9,500 ha, and that of Vibo, the Serre, 4,500 ha.
- ISPRA's conversion table (`ispra_cdn_calabria_legenda2024`) maps the regional class "42.67 -
  Rimboschimenti di Pinus nigra" to the national 42.G_n. So the 70,000 ha of 42.G_n are the laricio
  plantations of 1955-1970, and 42.65 keeps the natural laricio. It also maps the regional "42.1B1 -
  Rimboschimenti di Abies alba" to 83.31_m, which the region card files as mountain pine; see Open
  questions.

INFC 2015 (`infc2015_calabria`) has the same picture by category:

| INFC 2015 category | ha | share of bosco |
|---|---|---|
| beech | 79,413 | 16.0 % |
| black, laricio and loricato pine | 73,443 | 14.8 % |
| chestnut | 68,966 | 13.9 % |
| sessile, downy and pedunculate oak | 53,790 | 10.9 % |
| holm oak | 48,692 | 9.8 % |
| other deciduous | 45,153 | 9.1 % |
| Turkey oak and Hungarian oak | 43,593 | 8.8 % |
| other evergreen broadleaves | 21,143 | 4.3 % |
| Mediterranean pines | 17,474 | 3.5 % |
| hygrophilous | 12,872 | 2.6 % |
| other conifers | 12,561 | 2.5 % |
| cork oak | 5,224 | 1.1 % |
| hop-hornbeam and hornbeam | 4,477 | 0.9 % |
| silver fir | 3,731 | 0.8 % |

84 % of the black-pine category is laricio, and 94 % of the laricio is on the Sila plateau
(`calabria_pfr2024`, pp. 46-47). About 110,000 ha were reforested between 1955 and 1967, laricio "nel
Castanetum freddo e Fagetum caldo" (pp. 48-49).

**Altitude belts:**

| type | altitude (m) and where | source |
|---|---|---|
| beech | the forest limit; lower limit "da 1.400 a 1.000 m" east and west, down to 600-700 m in humid spots; pure beech "fino a 1.700/1.800 metri"; Aspromonte 900-1,000 to 1,900 m; "a quote superiori ai 1000 metri, Fagus sylvatica è l'essenza arborea dominante" | `calabria_pfr2024` pp. 45, 105-109; `ispra2018_mlg180_calabria_foreste` p. 68 |
| pino loricato | 1,800-2,000 m on the Pollino limestone | `calabria_pfr2024` p. 46 |
| laricio pine | Sila 900-1,400 m, Aspromonte 700-1,600 m; natural stands 800-1,000 to 1,500-1,600 m, plantations 900 to 1,200-1,300 m; Sila Greca "da 1000 a 1300 metri", beech above; pine on south-facing slopes, beech on north-facing ones | `ispra2018_mlg180_calabria_foreste` p. 191; `nicolaci2014_laricio_sila`; `lavorato_rotella2004_pini_sila_greca`; `parcosila_vegetazione` |
| silver fir | Serre 820-1,400 m; Aspromonte 1,100-1,800 m; Gariglione (Sila Piccola) 1,200-1,500 m | `ispra2018_mlg180_calabria_foreste` p. 14; `calabria_pfr2024` pp. 45-46 |
| chestnut | Catena Costiera 500-1,000 m; Sila 600/700-1,000/1,100 m; Sila Greca "la fascia del castagno e delle querce tra i 600 ed i 1100 metri"; western Aspromonte 300-1,200 m | `calabria_pfr2024` pp. 43-44; `lavorato_rotella2004_pini_sila_greca` |
| Turkey oak | up to about 1,200 m, meeting the beech | `calabria_pfr2024` p. 42 |
| holm oak | 450/500 to 1,100/1,200 m | `calabria_pfr2024` p. 37 |
| cork oak | 50/100 to 600/650 m, mostly in the province of Catanzaro | `calabria_pfr2024` p. 38 |
| Aleppo pine | sea level to about 900 m, the Alto Ionio | `calabria_pfr2024` pp. 38-40 |

Calabria's belts are those of Campania pushed up and stretched:
- The beech reaches 1,900-2,000 m (Campania "1800-1900 metri").
- The chestnut and oak belt runs to 1,100-1,200 m.
- The laricio belt at 900-1,600 m has no counterpart in Campania.

**Substrate.**
- The Sila, Serre and Aspromonte are granite, gneiss and schist, with "reazione acida" umbric
  Dystrudepts (`calabria_pfr2024`, pp. 22-25). The Sila granite weathers to "sabbioni"
  (`pn_sila_geografia_web`).
- The Pollino is limestone and dolomite, with neutral Hapludolls.
- The only forest-soil pH found is under Aspromonte laricio at 1,100 m: 4.96-5.64
  (`muscolo2021_laricio_soil`).
- *C. ferruginascens* was collected only on the acid Sila soils, "pH 5-5,5"
  (`caroti2015_cantharellaceae_calabria`).
- This is why the acid-soil porcini, *B. edulis* and *B. pinophilus*, are common here, unlike on the
  limestone massifs of central and southern Italy.

**Climate.**
- **Totals.** The mountains get 1,000-2,000 mm a year and the coast 600-900 mm; the regional mean is
  about 1,150 mm. "Over 70% of the yearly precipitation occurs from October to March, with
  negligible monthly values from June to September" (`terranova2011_rain_events`).
- **Tyrrhenian and Ionian.** The Tyrrhenian side gets "piogge tra le più abbondanti dell'Italia
  Meridionale": Laghitello on the Catena Costiera has 1,928 mm, Serra San Bruno 1,772, Gambarie
  1,608 and Camigliatello 1,634. Reggio has 594 mm. By season the rain is "per circa il 40% in
  inverno, il 30% in autunno, dal 21 al 26% in primavera e dal 4 al 9% in estate", and 3 % on parts
  of the Ionian coast (`calabria_pfr2024`, pp. 11-12).
- **The Sila summer.** Seven Sila stations at 1,005-1,358 m (1951-1967) had July and August
  together at 3.0-3.8 % of the year. Camigliatello got 30 mm in July, 28 in August and 243 in
  November (`bissanti1973_neve_sila`). The Sila park puts summer at "solo il 7-10%", with a dry
  season "tra poco più di 2 mesi a meno di un mese" (`pn_sila_geografia_web`).
- **Snow.** On the Sila it "può iniziare a cadere in novembre per finire in maggio". There are 20-25
  snow days a year, and "la neve copre il suolo per circa 60 - 80 giorni all'anno"; Camigliatello
  has 85, of which 2 in November and 11 in December (`bissanti1973_neve_sila`). Above 1,400-1,600 m snow lies for six months (`nicolaci2014_laricio_sila`).

**Regional law.** L.R. 26 novembre 2001, n. 30 (`lr_calabria_30_2001`, the consolidated text updated
to L.R. 19/2026).
- **Amendments.**
  - L.R. 31 marzo 2009, n. 9 rewrote the law and added the truffle title.
  - L.R. 47/2011 and 69/2012 changed the permits.
  - L.R. 53/2017 changed the truffles only.
  - L.R. 12 giugno 2026, n. 19 (`lr_calabria_19_2026`) moved permits to the comuni and Azienda
    Calabria Verde, made them valid for ten years and changed the truffle rules.
  - L.R. 24/2002 only deferred the entry into force of some articles.
  - L.R. 13 agosto 2026, n. 26 repeats n. 19, but its promulgation was revoked on 17 August 2026.
- **Quantity.** "limite massimo giornaliero di 3 (tre) Kg", up to 5 kg for residents of mountain
  comuni (art. 5). There is no separate ovolo limit, unlike Campania's 1 kg.
- **Size.** "vietata la raccolta dell'Amanita Caesarea allo stato di Ovolo chiuso" (art. 2 c. 1 e).
  The minimum caps are 5 cm for the ovolo and 4 cm for "Boletus edulis e relativo gruppo (Porcini)";
  chanterelles fall under the 3 cm default (art. 3). Annex D protects "Amanita caesarea forma alba"
  and "Boletus edulis var. citrinus".
- **Days and hours.** Picking is allowed "solo nelle ore diurne" (art. 3 c. 3), with no weekday rule.
- **Places.** Picking is banned in integral reserves, in areas the Giunta names, and in urban green
  and contaminated areas (art. 5-bis). There is no chestnut-orchard ban, unlike Campania.
- **Poor years.** The Giunta "può stabilire limiti quantitativi o divieti alla raccolta, anche
  differenziati per specie e per periodi temporali" (art. 5 c. 7).
- **The Aspromonte park.** No picking in zone A, and none "nelle aree di nuovo rimboschimento e nelle
  aree percorse da incendi prima che siano trascorsi dieci anni" (`pn_aspromonte_regolamento2016`,
  art. 20).
- **What it leaves out.** No season calendar and no altitude rule. None of it changes where or when
  the fungi fruit; it confirms the porcini group and the ovolo as regional species.

## The Sila's laricio pine and the porcini

This was the card's first question: which porcini fruit under the laricio pine, when, and how
strongly.

**Which porcino.** *B. pinophilus* (plausible, from several agreeing Calabrian sources).
- **Record shares.** In the ISPRA laricio table (5,464 records, 933 species) *B. pinophilus* is 0.9 %
  of records, level with *Russula delica* and *Tricholoma equestre*, 8th of all species. *B. edulis*
  is 0.3 % and *B. reticulatus* 0.1 %. There is no *B. aereus* and no ovolo. The commonest species
  are *Lactarius deliciosus* (the Sila's "rosito"), *Suillus* and *Chroogomphus*
  (`ispra2018_mlg180_calabria_foreste`, pp. 192-204).
- **Lavorato (1996).** *B. pinophilus* is "molto diffuso sotto i pini silani secolari (Pinus nigra
  var. calabrica) e meno diffuso sotto faggio" (`lavorato1996_boletaceae_calabria`).
- **Lavorato & Rotella (2004).** Twelve years of observation under the Sila Greca pines list
  "Boletus pinophilus ... localmente comune sotto pino silano", its var. *fuscoruber*, and "Cantharellus
  cibarius ... poco comune". They do not list *B. edulis* (`lavorato_rotella2004_pini_sila_greca`).
- **Dialect.** The dialect names tie *B. pinophilus* to the pine:
  - Acri: "Sillu 'e pinu" for *B. pinophilus*, "Sillu 'e fagu" for *B. edulis*
    (`ambsg_manuale_corso_micologia`).
  - Cosenza: "cozza 'e pinu".
  - Reggio: "Zappinaro", "con riferimento alla sua tendenza ad associarsi ai grandi Pini
    dell'Aspromonte" (`miceli2019_sua_maesta_porcino`).
- **The press.** Funghi Magazine's June bulletins find the spring *B. pinophilus* flush "nelle pinete
  del Pollino, della Sila e dell'Aspromonte" (2020) and "soprattutto in alta Sila" (2021); see the
  sanity contrasts.

**How strongly.** For *B. pinophilus* the pine is as good as the beech: 0.9 % of the laricio records,
0.6 % (plus 0.3 % var. *fuscoruber*) of the Sila beech records. For the other porcini the beech is far
better:

| taxon | laricio (5,464) | Sila beech | silver fir (329) | chestnut (3,192) |
|---|---|---|---|---|
| *B. pinophilus* | **0.9** | 0.6 (+0.3 var.) | – | 0.1 |
| *B. edulis* | 0.3 | 2.7 | **3.3** | 0.7 |
| *B. reticulatus* | 0.1 | 1.4 | – | **1.8** |
| *B. aereus* | – | 0.1 | – | 0.8 |
| *Cantharellus* | 0.3 | 2.4 | 0.3 (*C. amethysteus*) | **2.7** |

So the laricio woods are not the main porcino ground of the Sila in record terms. The porcini are
1.3 % of the pine records against about 5 % of the Sila beech records. The pine is simply where *B.
pinophilus* lives.

Two things temper this:
- The laricio records are dominated by the rosito and *Suillus*, which foragers seek there.
- The Sila's best *B. edulis* ground, in forager lore, is the mixed summit country, "boschetti di
  faggio, siano essi puri o misti all'altra essenza primaria della Sila: il pino laricio"
  (`lupo_talmamax_re_porcino_sila`). A 2024 foray found *B. pinophilus* and *B. edulis* late in "un
  bosco misto a predominanza di faggio e pino laricio" (`amer2024_weekend_sila`).

The rules handle that mix through the habitat response: a cell with 30 % of beech gets full credit
for *B. edulis* however much pine it has.

**Natural stands and plantations.** The data cannot separate them.
- The ISPRA reforestation manual has only 40 records under *Pinus nigra* plantations, and no porcino
  among them (`ispra2018_mlg179_calabria_rimboschimenti`).
- The "natural" laricio table probably includes the old plantations: "Nel cuore della Sila si trovano
  le più vecchie pinete di laricio impiantate in Italia" (MLG 180, p. 192).
- Lavorato ties *B. pinophilus* to the "pini silani secolari". The park ties the rosito to "giovani
  pinete di laricio" (`parcosila_funghi`).
- On the habitat map 71 % of `mountain_pine` is the 1955-1970 reforestation (42.G_n), all in one
  habitat key. The rules treat it like the natural pine; see Open questions.

**When.** *B. pinophilus* has two seasons in the Sila.
- **Spring, May-June.** "ottime nascite di Porcini rossi-Pinicola in Sila, Pollino e localmente anche
  tra Serre-Aspromonte" on 28 May 2022 (`funghimagazine_porcini_maggio2022`). "I primi Boletus
  pinophilus ... in maggio-giugno, occasionalmente anche alla fine del mese di aprile ... in
  particolare sulle montagne della Calabria" (`bmeteo_pinophilus_oppicelli2024`).
- **Autumn, September-November.** A dated record under pine at 1,300 m on 18 November 1994
  (`lavorato_rotella1995_mappatura_cosenza`). The 19 iNaturalist records fall in June (5) and
  September-November (13), none in July or August.
- **The end.** No Calabrian source dates it. The snow ("può iniziare a cadere in novembre") and frost
  stoppers do it.
- The Tuscan windows (spring 1 May-20 July, autumn 15 August-15 December) already fit, and are kept.

**Where.** The Pollino's pino loricato has two records in the ISPRA tables and no porcino. The
Aspromonte laricio (about 4,000 ha) has no porcino record, but "Zappinaro" and the 2020 flush "nelle
pinete ... dell'Aspromonte" put *B. pinophilus* there too.

## Where Calabria departs from Campania and central Italy

Campania's rules (on its branch) and Calabria's start from the same Tuscan files.

| factor | Tuscany | Campania | Calabria | why Calabria differs |
|---|---|---|---|---|
| `mountain_pine` for *B. pinophilus* | 0.6 | 0.6 | **1.0** | the Sila laricio is its habitat (above) |
| `mountain_pine` for *B. edulis*, *B. reticulatus* | 0.6 | 0.6 | **0.1** | a ninth and a fourteenth of their Sila-beech shares |
| `chestnut` for *B. pinophilus* | 1.0 | 1.0 | **0.3** | 0.1 % of the chestnut records; no Calabrian source names it |
| `macchia` for *B. aereus* | 1.0 | 1.0 | **0.3** | lentisk and *Cytisus* scrub, not Campania's *Erica-Arbutus-Cistus* |
| `mediterranean_pine` for *B. aereus* | 0.6 | 0.6 | **0.1** | Aleppo pine: none of 822 records |
| `mixed_broadleaf` for *B. aereus* | 0.3 | 0.6 | **0.1** | *Alnus cordata* here, hop-hornbeam there |
| `evergreen_oak` for the ovolo | 0.6 | 0.6 | **1.0** | holm and cork oak as good as the deciduous oaks |
| `deciduous_oak` for the chanterelles | 0.3 | 0.6 | 0.6 | same move |
| `beech` for *B. reticulatus* and the chanterelles | 0.6 | 1.0 | 1.0 | same move |
| `beech` for *B. aereus* | 0.1 | 0.1 | **0.3** | 0.8 % of the Aspromonte beech records |
| *B. aereus* altitude | full to 800, 0 at 1,250 m | kept | **full to 1,000, 0 at 1,350 m** | hosts 150-250 m higher |
| ovolo altitude | full to 750, 0 at 1,100 m | kept | **full to 1,000, 0 at 1,350 m** | "fino a circa 1200 m"; ideal 600-900 m |
| chanterelle altitude | full to 1,000, 0 at 1,700 m | 1,400 → 1,900 m | **1,500 → 1,900 m** | the beech sits 60-190 m higher |
| *B. edulis*, *B. pinophilus* altitude | 1,600 → 1,900 m | 1,800 → 2,000 m | 1,800 → 2,000 m | same move |
| *B. reticulatus* altitude | 1,100 → 1,500 m | 1,600 → 1,900 m | 1,600 → 1,900 m | same move |
| *B. aereus* windows | start 15 June / 1 July | kept | **both start 15 May** | "da maggio a dicembre" |
| *B. aereus* lowland end, handover | 15 Dec; 400-600 m | 10 Jan; 600-800 m | 10 Jan; 600-800 m | same move |
| *B. aereus* upland end | 31 Oct | kept | **30 Nov** | the submontane Presila "da maggio a dicembre" |
| *B. edulis* window start | 1 July | kept | **1 June** | "si comporta come una specie precoce" |
| *B. reticulatus* window end | 15 Nov | kept | **15 Dec** | "quasi natalizio" on Monte Cocuzzo |
| ovolo window | full from 1 Sep | kept | **full from 1 Aug, ramp from 15 May** | "piuttosto precoce ... nel periodo estivo" |
| chanterelle mountain window | from 1 June | from 15 May | from 15 May | same move |

## The southern season

The card asked about early-summer flushes, the summer gap, and a late autumn. Each verdict below
rests on Calabria's evidence.

1. **Earlier flushes: yes, for five of the six keys.**
   - Lavorato: "Le specie pregiate e commerciabili, in annate umide, anticipano il loro sviluppo già
     nel mese di maggio, come per esempio il gallinaccio ed alcuni porcini"
     (`lavorato2018_calabrone_consigli`).
   - The Acri museum cards (ISPRA MLG 184/185) date the Calabrian seasons:
     - *B. aereus* "da maggio a dicembre".
     - *B. edulis* "si comporta come una specie precoce ... già in primavera come prima fioritura".
     - The ovolo "da maggio a novembre".
     - The chanterelle "fa le sue prime comparse primaverili a maggio".
   - *B. reticulatus* is "precoce già in giugno" (Lavorato 1996).
   - The ovolo is "piuttosto precoce, solitamente si sviluppa nel periodo estivo"
     (`lavorato2013_calabrone_caesarea`).
   - The first southern chanterelles and *B. aereus* came in early June 2019
     (`funghimagazine_giugno2019`).
   - The spring *B. pinophilus* flush of the Sila is in the sanity contrasts (May 2023; June 2018,
     2020, 2021).
   - What changed: *B. aereus* opens on 15 May, *B. edulis* ramps from 1 June, the ovolo is full from 1
     August, and the chanterelles' mountain window opens on 15 May. *B. pinophilus* and *B.
     reticulatus* already opened in May in Tuscany.
2. **A summer drought gap: yes, deeper than in central Italy, but broken by storms. The weather
   makes it.**
   - July and August bring 3-4 % of the year's rain in the Sila, 4-9 % of it falls in summer
     region-wide, and 3 % on the Ionian coast.
   - In early August 2025 "Calabria, Sicilia e Sardegna restano ancora fuori dai giochi, salvo
     micro-zone montane umide" (`funghimagazine_nascite_2025_08_01`).
   - Storms still give July and August flushes:
     - 2020: Sila Grande in late July, Sila and Aspromonte in mid-August.
     - 2022: the Sila "quasi ininterrottamente".
     - 2025: the Sila Piccola in early July (`informacalabria_porcini2025`).
     - 2026: Serra San Bruno in July (`noidicalabria_serra_porcini2026`).
     - 2023: the Sila "ha sfornato funghi Porcini senza sosta dal mese di Maggio a fine anno"
       (`funghimagazine_2023_dodici_mesi`).
   - As in Tuscany and Campania, no calendar gap is written in. The porcini's 30-day rain is scored
     against each cell's own normal, so it adapts. The ovolo and chanterelle 30-day ramps are
     absolute and will rarely be full in a Calabrian July.
3. **A later autumn at low altitude: yes.**
   - *B. aereus* runs "da maggio a dicembre". In the South it goes on "addirittura in pieno periodo
     natalizio" in holm and cork oak (`bmeteo_boletus_aereus`). "Al Sud, invece, la stagione
     prosegue" in November 2025 (`funghimagazine_nascite_2025_11_08`).
   - *B. reticulatus* "non è rara anche in periodo quasi natalizio" on Monte Cocuzzo.
   - *C. pallens* is found "a quote basse anche a gennaio" (`caroti2015_cantharellaceae_calabria`).
   - Calabria's fungi records run late: 24 % in October, 14 % in November, 9 % in December.
   - What changed: *B. aereus* runs to 10 January below 600-800 m and to 30 November above. *B.
     reticulatus* runs to 15 December. The chanterelles' lowland window already ran to 25 January.
   - In the Sila, snow from November and frost end the season whatever the window.
4. ***B. aereus* in chestnut, oak and holm oak: yes, oak first.**
   - It is the commonest species of the Turkey oak records ("la specie micologica più frequente"). It
     is 2.4-2.6 % of the downy and Hungarian oak records, 5.4 % of the cork oak, 1.1 % of the holm oak
     and 0.8 % of the chestnut ones.
   - The Acri card: "diffuso in maggioranza sotto quercia, specialmente nelle zone submontane della
     Presila, ma anche sotto castagno, leccio".
   - All three stay full hosts.
5. **Thermophilous keys higher: yes, because their hosts are higher.**
   - The chestnut and oak belt runs to 1,100-1,200 m.
   - The ovolo grows "fino a circa 1200 m", best at 600-900 m (`bosco_grande2004_caesarea_cocuzzo`).
   - The bands of *B. aereus* and the ovolo move up 200-250 m. *B. reticulatus* follows the beech.

## Occurrence cross-check (Calabria)

Queried 2026-09-28 (`mushma_occurrence_check_calabria_2026`):
- **iNaturalist**: place 9323, verifiable records.
- **Elevations**: from the Open-Meteo elevation API, for open, non-obscured records with an accuracy
  of 1 km or better.
- **Habitat**: the Carta della Natura habitat at and around each located record, deduplicated by
  observer, day and site.
- **GBIF**: `gadmGid=ITA.4_1`. Its 27 records of the six taxa are all copies of iNaturalist ones.
- Aggregates only; no coordinates are stored.

Calabria has 3,053 iNaturalist fungi records (Campania 4,437, Tuscany 19,089), mostly from 2021 on.

| taxon | iNat n | J | F | M | A | M | J | J | A | S | O | N | D | located: median (range) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *B. edulis* | 30 | | | | | | | | 1 | 12 | 10 | 5 | 2 | 1,247 m (534-1,462), n=11 |
| *B. reticulatus* | 36 | | | | | | 5 | 9 | 2 | 19 | 1 | | | 1,105 m (797-1,485), n=18 |
| *B. aereus* | 7 | | | | | | | | 2 | 1 | 3 | 1 | | 253-828 m, n=3 |
| *B. pinophilus* | 19 | | | | | | 5 | | | 3 | 5 | 5 | | 1,152 m (797-1,638), n=11 |
| *A. caesarea* | 15 | | | 1 | | | 1 | | 2 | 3 | 7 | 1 | | 328-932 m, n=4 |
| *Cantharellus* | 11 | | | | | | | 1 | 2 | 4 | 3 | 1 | | 482-1,585 m, n=5 |
| all fungi (share, %) | 3,053 | 4 | 3 | 4 | 4 | 8 | 4 | 6 | 8 | 12 | 24 | 14 | 9 | |

The chanterelles are *C. cibarius* 3, *C. pallens* 3 and *C. amethysteus* 1, plus 4 at genus level.

Located records against Tuscany's (place 13073, same method):

| taxon | Calabria, median (n) | Tuscany, median (n) |
|---|---|---|
| *B. edulis* | 1,247 m (11) | 1,054 m (22) |
| *B. reticulatus* | 1,105 m (18) | 649 m (19) |
| *B. pinophilus* | 1,152 m (11) | 692 m (6) |
| *B. aereus* | 253-828 m (3) | 352 m (42) |
| *A. caesarea* | 328-932 m (4) | 364 m (32) |
| *Cantharellus* | 482-1,585 m (5) | 283 m (93) |

What the records show:
- **Too few to tune.** They confirm the months and the heights of the mountain taxa. They cluster
  in the Sila, where most observers are.
- **The summer porcino is a mountain porcino here.** Its July records sit at 1,329-1,485 m, and 10
  of its 18 located records are above 1,000 m.
- **Pine and porcini.** Deduplicated, 11 *B. edulis*, 12 *B. reticulatus* and 10 *B. pinophilus*
  records have usable positions.
  - Mountain pine dominates the 500 m around 5, 5 and 4 of them: the porcini of the records are
    found in the pine country of the Sila.
  - At the point itself only 2, 1 and 0 fall in pine polygons, the rest in beech and chestnut.
  - At 1 km accuracy this cannot say more.
- **No spring record of *B. aereus* or the ovolo.** The "precoce" windows rest on the Calabrian
  mycologists, not the records. The ovolo's records peak in October (7 of 15), against Lavorato's
  "raramente in autunno"; the window keeps both.

## Porcini (*B. edulis*, *B. reticulatus*, *B. aereus*, *B. pinophilus*)

**Regional evidence** beyond what is above:
- **Hosts** (plausible).
  - Lavorato (1996): *B. aereus* "(noto con il nome sillu e cerza) è diffuso sotto castagne (Castanea)
    e quercia (Quercus)". *B. reticulatus* "Sotto latifoglia in genere".
  - The Sila Greca society: *B. aereus* "non può vegetare né con i pini né con i larici ma solo sotto
    latifoglie (querce e castagno)" (`grande_funghi_silagreca`).
  - The Rossano macchia belt, up to 700-800 m: porcini "sotto castagno, quercia, lecci", not under
    the shrubs (`iacoi2003_macchia_rossano`).
  - Lavorato's Cistus key has *B. aereus* only from the Circeo, in Lazio (`lavorato1991_micoflora_cisto`).
  - The Acri card: *B. edulis* "molto diffuso prima nei castagneti poi sotto altre latifoglie e abeti"
    (`ispra2018_mlg184_acri_vol1`). It disagrees with Lavorato's "meno diffuso sotto altre latifoglia"
    on chestnut, so chestnut stays a full host for *B. edulis*.
- **Season** (plausible / folklore).
  - The Sila porcini PAT sheet: "Da settembre fino a novembre e, più limitatamente, in agosto, si ha
    in Sila la maggiore produzione di funghi" (`vivigreen_pat_porcini_silani`, a copy of the Region's
    sheet, whose PDF is truncated on its server).
  - A forager sequence: *B. aereus* "il primo a fruttificare fin già dalla fine di aprile", *B.
    pinophilus* in May, *B. reticulatus* "da fine maggio-giugno ... fino al mese di ottobre", *B.
    edulis* "l'ultimo a comparire, proprio dopo le piogge pre-autunnali" (`lupo_talmamax_re_porcino_sila`).
- **Weather** (plausible). "Dopo 10-12 giorni dall'ultima pioggia utile, i primi carpofori di Amanita
  caesarea ... altrettando accade al quindicesimo giorno per Boletus edulis ed aereus"
  (`bosco_grande2004_caesarea_cocuzzo`). This sits inside the porcini's full lag of 10-16 days.

**Decisions.**

| key | factor | Tuscany | Calabria | why | confidence |
|---|---|---|---|---|---|
| *edulis* | season | 1 Jul → 1 Sep … 15 Nov → 20 Dec | **1 Jun** → 1 Sep … 15 Nov → 20 Dec | "precoce ... già in primavera" (Acri card); records August-December | plausible (weak) |
| *edulis* | habitat `mountain_pine` | 0.6 | **0.1** | 0.3 % of laricio records against 2.7 % Sila beech and 3.3 % fir; not listed under the Sila pines; "meno diffuso sotto ... aghifoglia" | plausible |
| *edulis* | habitat `mixed_broadleaf` | 0.3 | **0.1** | *Alnus cordata* | plausible |
| *edulis* | habitat `transitional_woodland_shrub` | 0.3 | **0.1** | *Spartium* and broom | plausible |
| *edulis* | altitude | 200 → 700 … 1600 → 1900 | 200 → 700 … **1800 → 2000** | beech to the tree line; records median 1,247 m | plausible |
| *reticulatus* | season | 1 May → 1 Jun … 30 Sep → 15 Nov | 1 May → 1 Jun … **31 Oct → 15 Dec** | "quasi natalizio" (Monte Cocuzzo); a 15 October record | plausible (weak) |
| *reticulatus* | habitat `beech` | 0.6 | **1.0** | among the commonest in all beech types; 1.4 % Sila beech ≈ 1.8 % chestnut; July records in beech | plausible |
| *reticulatus* | habitat `mountain_pine` | 0.6 | **0.1** | 0.1 % of laricio records | plausible |
| *reticulatus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.6 | **0.3** | *Alnus cordata*; broom scrub | plausible |
| *reticulatus* | altitude | 0 → 150 … 1100 → 1500 | 0 → 150 … **1600 → 1900** | records median 1,105 m (Tuscany 649 m); beech median 1,270 m | plausible |
| *aereus* | season | upland 15 Jun → 1 Aug … 30 Sep → 31 Oct; lowland 1 Jul → 1 Sep … 15 Nov → 15 Dec; handover 400-600 m | upland **15 May → 1 Jul … 31 Oct → 30 Nov**; lowland **15 May → 15 Jun … 30 Nov → 10 Jan**; handover **600-800 m** | "da maggio a dicembre ... zone submontane della Presila" (Acri card); Christmas flushes in holm and cork oak (folklore) | plausible (weak) |
| *aereus* | habitat `macchia` | 1.0 | **0.3** | 63 % lentisk and *Cytisus*; porcini under the oaks, not the shrubs | plausible |
| *aereus* | habitat `transitional_woodland_shrub` | 0.6 | **0.3** | broom scrub | plausible |
| *aereus* | habitat `mediterranean_pine` | 0.6 | **0.1** | Aleppo pine, no record in 822 | plausible |
| *aereus* | habitat `mixed_broadleaf` | 0.3 | **0.1** | *Alnus cordata* | plausible |
| *aereus* | habitat `beech` | 0.1 | **0.3** | 0.8 % of Aspromonte beech records; "Faggio, quasi esclusivamente al Sud" (folklore) | plausible (weak) |
| *aereus* | altitude | … 800 → 1250 | … **1000 → 1350** | chestnut and oak belt to 1,100 m; chestnut p90 1,087 m | plausible (weak) |
| *pinophilus* | habitat `mountain_pine` | 0.6 | **1.0** | the laricio porcino (above) | plausible |
| *pinophilus* | habitat `chestnut` | 1.0 | **0.3** | 0.1 % of chestnut records; no Calabrian source names it; one iNaturalist site keeps it above non-host | plausible (weak) |
| *pinophilus* | habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3 | **0.1** | *Alnus cordata*; broom scrub | plausible |
| *pinophilus* | altitude | 300 → 800 … 1600 → 1900 | 300 → 800 … **1800 → 2000** | beech and laricio to the tree line; records to 1,638 m | plausible |
| all four | weather, stoppers, growth clock | — | kept | no Calabrian numbers; the lore agrees | as Tuscany |

Kept on purpose:
- ***B. edulis* in chestnut (1.0).** The two Calabrian sources disagree. The record share (0.7 %) is a
  quarter of the Sila beech's.
- ***B. aereus* in evergreen oak (1.0).** Cork oak has its highest share, and holm oak is named in
  the Acri card.
- ***B. pinophilus* windows.** The Calabrian spring flush fits the Tuscan May-July window.
- ***B. reticulatus* in evergreen oak (0.3)** and in deciduous oak (1.0). Hungarian oak is low
  (0.4 %) but downy and Turkey oak high (1.1 %, 1.7 %).

## Ovoli (*Amanita caesarea*)

**Regional evidence.**
- **Presence.** The regional law bans the closed ovolo (art. 2) and protects its white form. It is
  "Molto ricercato ma non molto diffuso" in the Sila park (`parcosila_funghi`), and "sempre meno
  frequente" in recent years (Lavorato 2013).
- **Hosts.** It is 4.8 % of the cork oak records, 1.8 % of the chestnut, 1.6 % of the downy oak, 1.1
  % of the Hungarian oak, 0.9 % of the holm oak and 0.4 % of the Turkey oak records. There is none in
  beech, laricio or Aleppo pine. The cork-oak woods "sono caratterizzate da una notevole frequenza"
  of it and of *B. aereus* and chanterelles (`ispra2018_mlg180_calabria_foreste`, p. 108).
- **Lavorato (2013).** "cresce sotto latifoglie, specialmente in luoghi soleggiati con la presenza di
  castagno". Of the conifer reports, "ne siamo dubbiosi". It "cresce fino a circa 1200 m di quota".
- **Monte Cocuzzo** (`bosco_grande2004_caesarea_cocuzzo`, society field notes).
  - It was found "sotto castagno, querceti, faggio, sotto carpino nero, cerro, preferendo
    abitualmente gli spazi aperti".
  - It "nasce dai 300-400 m. e sino alla soglia della vetta di Monte Cocuzzo 1500 m. circa, tuttavia
    l'altitudine ideale ... è tra i 600 e 900 metri".
  - It was "reperita da agosto ad ottobre con sporadiche presenze sino alla prima decade di novembre".
  - It follows hot summers: "ha bisogno di una sorta di accumulo abbondante di calore". The Acri card
    has it "Particolarmente abbondante nelle stagioni estive piovose".
- **Records.** 15 iNaturalist records, 7 of them in October; the located ones are at 328-932 m.

**Decisions.**

| factor | Tuscany | Calabria | why | confidence |
|---|---|---|---|---|
| season | 1 Jun → 1 Sep … 5 Nov → 30 Nov | **15 May → 1 Aug** … 5 Nov → 30 Nov | "piuttosto precoce ... nel periodo estivo"; "da maggio a novembre"; the October records keep the end | plausible |
| habitat `evergreen_oak` | 0.6 | **1.0** | holm oak 0.9 % ≈ Hungarian oak 1.1 %; cork oak 4.8 %; "sotto castagno, quercia, lecci" (Rossano) | plausible |
| habitat `transitional_woodland_shrub` | 0.6 | **0.3** | *Spartium* and broom, not heath with scattered oaks | plausible |
| habitat `mixed_broadleaf` | 0.3 | **0.1** | *Alnus cordata* (one Monte Cocuzzo find under hop-hornbeam) | plausible (weak) |
| habitat `beech` | 0.0 | **0.1** | none in the beech records; four fruit bodies in pure beech at 1,200 m (Monte Cocuzzo, 2004) | folklore |
| altitude | … 750 → 1100 | … **1000 → 1350** | "fino a circa 1200 m"; ideal 600-900 m; chestnut p90 1,087 m | plausible |
| chestnut, deciduous oak 1.0; macchia 0.3; conifers 0 | — | kept | "specialmente sotto castagno" | strong (hosts) |
| weather rules | — | kept | 10-12 days after the last useful rain fits the lag plateau | as Tuscany |

A new known gap, `summer_heat`, records the hot-summer lore. Encoding it needs a calendar-anchored
summer window, which the engine does not have.

## Gallinacci (*Cantharellus* s.l.: "gallinelle", "galletti")

**Regional evidence.**
- **Which species.** The Calabrian monograph of the family (`caroti2015_cantharellaceae_calabria`)
  describes *C. cibarius*, *C. pallens* ("Nell'area mediterranea riteniamo che sia questo il
  Cantharellus più diffuso"), *C. ferruginascens*, *C. amethysteus* and *C. friesii*. It names *C.
  ilicis* and *C. alborufescens* only as look-alikes. In the ISPRA beech table, the determiners
  entered the chanterelle as "C. alborufescens", filed under *C. cibarius*.
- **Seasons.**
  - *C. cibarius* "nel mese di maggio e da agosto a gennaio".
  - *C. pallens* "comune dopo le prime piogge in primavera e poi ... da agosto a dicembre, a quote
    basse anche a gennaio".
  - *C. ferruginascens* "da luglio a novembre".
  - The Acri card: "fa le sue prime comparse primaverili a maggio, poi da agosto a gennaio è
    abbondante sotto castagno, querce, faggio" (`ispra2018_mlg185_acri_vol2`).
- **Hosts.**
  - It is the commonest species of the chestnut records (2.7 %). It is 7.0 % of the cork oak, 2.6 %
    of the Turkey oak, 2.4 % of the downy oak and 2.4 % of the Sila beech records. It is only 0.6 %
    of the holm oak, 0.4 % of the Hungarian oak and 0.3 % of the laricio records, and "poco comune
    sotto pino silano".
  - *C. pallens* and *C. ferruginascens* are named under "leccio".
- **Records.** 11 iNaturalist records, July-November, 482-1,585 m.

**Decisions.**

| factor | Tuscany | Calabria | why | confidence |
|---|---|---|---|---|
| season: mountain window | 1 Jun → 1 Jul … 15 Oct → 15 Nov | **15 May → 15 Jun** … 15 Oct → 15 Nov | "prime comparse primaverili a maggio"; the first June harvests in the South | plausible |
| habitat `beech` | 0.6 | **1.0** | 2.4 % of Sila beech records ≈ chestnut; "abbondante sotto castagno, querce, faggio" | plausible |
| habitat `deciduous_oak` | 0.3 | **0.6** | downy and Turkey oak ≈ chestnut, Hungarian oak low; "diffuso sotto castagno e querce" | plausible |
| habitat `mountain_pine`, `mediterranean_pine` | 0.3 | **0.1** | 0.3 % of laricio records, "poco comune"; none in Aleppo pine | plausible |
| habitat `mixed_broadleaf`, `transitional_woodland_shrub` | 0.3 | **0.1** | *Alnus cordata*; broom scrub | plausible |
| altitude | … 1000 → 1700 | … **1500 → 1900** | beech median 1,270 m, p90 1,640 m; records to 1,585 m | plausible |
| evergreen oak 1.0, chestnut 1.0, macchia 0.3, lowland window (wraps to 25 Jan) | — | kept | "leccio" named for *C. pallens* and *C. ferruginascens*; *C. cibarius* under *Phillyrea* and *Arbutus* at Rossano; "a quote basse anche a gennaio" | plausible |
| soil pH, lithology | disabled | kept disabled | the acid Sila soils are the hosts' soils anyway | plausible |
| weather rules | — | kept | no Calabrian numbers | as Tuscany |

Evergreen oak is kept as a host although its record share is half the chestnut's: the Calabrian
monograph names holm oak among the hosts of the family's commonest Mediterranean species. The poplar
galleries have 3.4 % "C. alborufescens", but out of 116 records; riparian stays 0.1.

## Weather rules: why none changed

- **Rain amount and lag.** No Calabrian source gives a rain amount in numbers. The generic forager
  threshold, "30-40 mm complessivi (limite minore)" for *B. aereus* (`bmeteo_boletus_aereus`), sits
  at the top of the Tuscan 10 → 30 mm ramp. The Monte Cocuzzo lags (10-12 days for the ovolo, about
  15 for the porcini) fall inside the Tuscan plateaus.
- **Heat and drying.** "se queste superano i 29-30 gradi, la sua crescita diventa difficile" (*B.
  aereus*, folklore) agrees with the Tuscan heat rules. Hot, dry wind stopping fruiting in November
  2025 agrees with the drying stopper.
- **Summer drought.** It is deeper than in Tuscany. The porcini's 30-day rain adapts, being a
  percentage of the cell's normal; the ovolo and chanterelle ramps are absolute.
- **Snow.** The Sila's snow from November to May is what ends the mountain season. The snow and
  frost stoppers are kept.
- **Rain scale.** `model.yaml`'s `precipitation_scale` was fitted to Tuscan gauges; checking it is a
  region-card task. ARPACAL's Centro Funzionale publishes daily station data free of charge but not
  openly: "copia della propria carta d'identita'" is needed to register, and "I dati non sono
  cedibili a terzi" (`arpacal_cfm_dati_storici`). The scanned yearbooks (Annali idrologici) stop in
  2000.

## Groups and keys

Nothing is dropped. All six keys have Calabrian evidence:
- the ISPRA record tables;
- the Acri museum cards;
- the regional monographs (Boletaceae, Cantharellaceae);
- the regional law (porcini group, ovolo);
- iNaturalist records of every key.

`mixed_broadleaf_conifer` is not on the Calabria map but stays in the rule files, as in every region;
it simply scores no cell. `other_conifer` is empty too: the region card files every conifer
plantation as `mountain_pine`.

## Effect on the woodland cells

On the approximate 1 km woodland cells (5,718, built from the habitat lattice; the grid itself was
being built in parallel), the Tuscan and Calabrian gates compare as follows
(`mushma_calabria_forest_composition_2026`):

| key | habitat gate full: Tuscany → Calabria | altitude gate full: Tuscany → Calabria |
|---|---|---|
| *B. edulis* | 72 % → 50 % | 63 % → 66 % |
| *B. reticulatus* | 94 % → 80 % | 73 % → 97 % |
| *B. aereus* | 67 % → 72 % | 44 % → 65 % |
| *B. pinophilus* | 74 % → 59 % | 53 % → 56 % |
| ovolo | 64 % → 64 % | 39 % → 65 % |
| chanterelles | 97 % → 85 % | 65 % → 94 % |

What the table shows:
- **The porcini group keeps its reach.** The best key's habitat and altitude gates are both above 0.5
  on 99 % of cells with either rule set.
- **The pine goes to *B. pinophilus*.** On the 857 cells that are mostly mountain pine, the product of
  its habitat and altitude gates averages 0.98, against 0.54 for *B. edulis* (0.98 with the Tuscan
  affinities). The porcino of a pure laricio cell is now *B. pinophilus*, as the Calabrian sources
  say.
- **Why the habitat gates fell.** *B. edulis*, *B. pinophilus* and the chanterelles lose pure-pine,
  broom and alder cells.
- **Why the altitude gates rose.** The bands follow hosts that sit higher than in Tuscany.

## Sanity contrasts

`calabria/sanity.yaml` replaces the Tuscan areas and contrasts. Windows and sources were written
down on 2026-09-28, before any Calabria score existed.

The schema has no group field: contrasts are porcini unless their id starts with `ovoli_` or
`gallinacci_`. "Normal" is the area's mean over 2017-2025.

**Areas.** Every comune was checked against the ISTAT 2025 list; all are in Calabria.
- `sila`: 21 comuni, from Spezzano della Sila (Camigliatello), San Giovanni in Fiore and Casali del
  Manco (Lorica) to Acri, Longobucco, Taverna and Petronà.
  - Casali del Manco holds the former Spezzano Piccolo, Pedace, Serra Pedace, Casole Bruzio and
    Trenta.
  - `sila_grande` and `sila_piccola_greca` are its parts.
- `pollino_interno`: 8 comuni, Castrovillari to Saracena.
- `sila_costiera`: the Sila plus the 7 comuni of the Catena Costiera.
- `costiera_orsomarso`: the Catena Costiera plus 7 comuni of the Orsomarso.
- `pollino_orsomarso_costiera`: all three.
- `serre_aspromonte`: 13 Serre and 18 Aspromonte comuni.
- `aspromonte_serre_vibonesi`: the Tyrrhenian Aspromonte and the Serre Vibonesi.

**The sources are mostly one magazine.**
- Calabrian local press rarely gives a dated verdict on a season. It reports giant porcini, sagre
  and controls.
- 14 of the 15 contrasts rest on Funghi Magazine's national bulletins. Their Calabria paragraphs come
  from readers' reports, and each contrast draws on 2-5 separate bulletins.
- The live site shows a captcha, so the bulletins were read through Wayback Machine captures.
- The research agent opened about 170 bulletins and checked every quote. Three were re-checked here
  (2021-10-14, 2023-10-12, 2024-08-16), and the 2022-05-28 page on the live site.
- The one local-press contrast (2016) rests on three outlets.

| id | group | higher | lower | main source (second source) | weakness |
|---|---|---|---|---|---|
| `sila_2016_normal` | porcini | Sila 2016, 6-24 Sep | same, normal | [EcodelloJonio 2016-09-24](https://ecodellojonio.it/articoli/funghi-e-boom-di-raccolta-porcini-in-sila): "Non si vedeva una stagione di funghi così da diversi anni ... è un boom di funghi" (Parola di Vita 2016-09-23; Cosenza Post 2016-09-20) | 2016 is the first year of weather history; the boom was region-wide |
| `sila_2021_2019_early_september` | porcini | Sila 2021, 30 Aug-10 Sep | Sila 2019 | [FM 2021-09-04](https://web.archive.org/web/20210922081914/https://funghimagazine.it/aggiornamento-meteofunghi-04-09-2021-porcini-giganti/): "Momento felice per la CALABRIA superiore" (FM 2021-09-10; 2019: Coldiretti via LaC News24 2019-09-08, "in modo sporadico soltanto sulla Sila") | the 2019 side rests on "sporadico" and a later "finalmente" |
| `sila_mid_august_2020_2022_vs_2019_2024` | porcini | Sila 2020 and 2022, 8-22 Aug | Sila 2019 and 2024 | [FM 2020-08-14](https://web.archive.org/web/20200926054742/https://funghimagazine.it/aggiornamento-meteofunghi-14-08-2020/): "le grandi nascite di funghi Porcini in Sila" (FM 2022-08-26; FM 2019-08-29; FM 2024-08-16, "La Sila ha fin'ora prodotto ben poco") | one outlet; late August 2024 picked up, so the window ends on 22 August |
| `sila_grande_2020_2025_late_july` | porcini | Sila Grande 2020, 20 Jul-5 Aug | same, 2025 | [FM 2020-07-30](https://web.archive.org/web/20200806093926/https://funghimagazine.it/aggiornamento-meteofunghi-30-07-2020/): "ancora buone nascite in Sila Grande nei pressi di Camigliatello" (FM 2025-07-17, 2025-08-01: "fuori dai giochi") | one outlet; 2025 worded for all Calabria |
| `sila_late_june_2018_2020_2021_vs_2024_2025` | porcini | Sila 2018, 2020, 2021, 18-30 Jun | Sila 2024, 2025 | [FM 2018-07-01](https://web.archive.org/web/20190820041455/https://funghimagazine.it/aggiornamento-funghi-01-luglio-2018/): "Calabria a tutta birra ... alle pinete della Sila" (FM 2020-06-25, 2021-06-24; FM 2024-06-28, 2025-07-03: heat) | one outlet; mostly *B. pinophilus* and summer porcini |
| `sila_2023_timing_autumn` | porcini | Sila 2023, 22 Sep-12 Oct | same year, 1-15 Sep | [FM 2023-10-12](https://web.archive.org/web/20231012124159/https://funghimagazine.it/aggiornamento-porcini-12-10-2023/): "3 differenti buttate sovrapposte" (FM 2023-09-27; lower side FM 2023-09-06, 2023-09-13: "sporadiche") | the lower side is sporadic, not nil |
| `sila_vs_serre_aspromonte_2023_october` | porcini | Sila 2023, 3-20 Oct | Serre and Aspromonte, same window | FM 2023-10-12: "Nulla ci risulta esser nato sulla Limina e allo Zomaro" (FM 2023-10-27: "Serre ed Aspromonte con nascite col contagocce") | one outlet; some porcini were still found under the Serre fir |
| `sila_vs_pollino_orsomarso_costiera_2023_october` | porcini | Sila 2023, 3-20 Oct | Pollino, Orsomarso and Catena Costiera, same window | FM 2023-10-12: "Sono del tutto cessate le nascite sul Pollino, Orsomarso e Catena Costiera" (FM 2023-10-04) | one outlet; October only |
| `sila_costiera_vs_pollino_2021_autumn` | porcini | Sila and Catena Costiera 2021, 15 Sep-15 Oct | inner Pollino, same window | [FM 2021-10-14](https://web.archive.org/web/20211024080903/https://funghimagazine.it/funghi-porcini-gia-al-capolinea-probabilmente-no/): "ottima annata ... soprattutto tra Sila e Catena Costiera ... tranne che sul Pollino" (FM 2021-09-24, 2021-10-09, 2021-11-19; Quotidiano del Sud 2021-11-15) | FM is the only source for the Pollino side; repeated in five bulletins |
| `pollino_costiera_vs_serre_aspromonte_2022_autumn` | porcini | Pollino, Orsomarso, Catena Costiera 2022, 20 Oct-5 Nov | Serre and Aspromonte, same window | [FM 2022-11-05](https://web.archive.org/web/20221129141843/https://funghimagazine.it/aggiornamento-porcini-06-11-2022/): "Boom di nascite tra Pollino e Catena Costiera ... Tra Serre e Aspromonte nascite sottotono" | one bulletin; window inferred |
| `costiera_orsomarso_vs_serre_aspromonte_2023_august` | porcini | Catena Costiera and Orsomarso 2023, 14-26 Aug | Serre and Aspromonte, same window | [FM 2023-08-24](https://web.archive.org/web/20230824101516/https://funghimagazine.it/aggiornamento-nascite-porcini-24-08-2023/): "Situazione nettamente migliore in Calabria tirrenica" (FM 2023-08-17) | one outlet |
| `aspromonte_serre_2020_2024_august` | porcini | Tyrrhenian Aspromonte and Serre Vibonesi 2020, 8-20 Aug | same, 2024 | [FM 2020-08-20](https://web.archive.org/web/20200926061118/https://funghimagazine.it/aggiornamento-meteofunghi-20-08-2020/): "ottime in Aspromonte grazie ad intensi e ripetuti temporali" (FM 2020-08-14; FM 2024-08-16) | one outlet; the best 2020 flush was on the Costa Viola, just outside the comuni |
| `sila_2020_timing_autumn` | porcini | Sila 2020, 28 Sep-20 Oct | same year, 1-20 Sep | [FM 2020-10-08](https://web.archive.org/web/20201028021842/https://funghimagazine.it/aggiornamento-meteofunghi-08-10-2020/): "le nascite migliori sono in assoluto la Toscana e la Calabria" (FM 2020-10-15, 2020-10-23; lower side FM 2020-09-04, 2020-09-21) | the October wording is region-wide; the Sila's September was "leggermente meglio" than elsewhere |
| `sila_spring_2023_vs_2020_2022` | porcini (spring) | Sila 2023, 10-20 May | Sila 2020 and 2022 | [FM 2023-05-18](https://web.archive.org/web/20230518160013/https://funghimagazine.it/aggiornamento-18-05-2023/): "bei ritrovamenti di Porcini Rossi-Pinicola in Sila e Pollino" (FM 2023-05-25; FM 2020-05-22 "timidissime"; FM 2022-05-12 "In Sila è ancora presente la neve") | *B. pinophilus* only; by 28 May 2022 the Sila had "ottime nascite", so the window ends on 20 May |
| `ovoli_sila_piccola_greca_2019_timing` | ovoli | Sila Piccola and Sila Greca 2019, 10-20 Sep | same, 22 Aug-8 Sep | [FM 2019-09-20](https://web.archive.org/web/20191016204920/https://funghimagazine.it/dove-stanno-nascendo-i-funghi-porcini-le-piogge-cadute-in-italia/): "l'esplosione di nascite di Aereus e pure di Ovoli ... tutto insieme e poi nulla più" (Coldiretti via LaC 2019-09-08) | the lower side is inferred from general remarks |

There is no gallinacci contrast. The only candidate compares May 2023, when the chanterelles
"abbondano ... soprattutto" (FM 2023-05-25), with May 2022, but the 2022 side has no chanterelle
verdict.

**Outlets that block AI agents** (robots.txt, not fetched): Gazzetta del Sud, ReggioToday (the Today
network), FreshPlaza, greenMe. ANSA, Il Sole 24 Ore and La Nazione were not fetched, on the strength
of earlier regions' checks.

Candidates left out:
- The satirical 2024 Camigliatello piece ("La Sagra del Fungo ... senza funghi!").
- Coldiretti percentages with no window: Calabria +30 % in 2022, Sila +10 % in 2023.
- Serra San Bruno 2024 ("un'ottima annata"), which hangs on one giant find.
- 2026 stories, outside the weather history.
- Forecasts ("avranno", "potrebbe").
- A late-October 2022 line on *B. pinophilus* alone.
- Reserves:
  - early July 2022-2023 against 2025, which overlaps the June contrast;
  - the Sila Piccola against the Serre in September 2019;
  - the western against the eastern Sila in August 2023, too fine for 1 km rain.

**Year picture from the sources** (context, not scored):
- **2016:** a September boom across the Sila, Serre and Pollino.
- **2017:** no Calabrian source.
- **2018:** strong late June in the Sila pine; exceptional late-August flushes on the Tyrrhenian coast;
  a good autumn.
- **2019:** hot and dry until mid-September; a short *B. aereus* and ovolo burst in the pre-Sila.
- **2020:** a *B. pinophilus* exploit in late June; the Sila and Aspromonte in mid-August; a poor
  first half of September; massive flushes in October.
- **2021:** *B. pinophilus* in June; dry until late August; an "ottima annata" in the Sila and Catena
  Costiera, the Pollino poor throughout.
- **2022:** a cold, late May; continuous flushes from late June to August; late October and November
  on the Pollino and Catena Costiera; the Serre and Aspromonte poor.
- **2023:** the strongest year, "da maggio a metà ottobre"; the Sila far ahead in October.
- **2024:** June heat; a poor summer; *B. aereus* on the coasts in the autumn.
- **2025:** a very poor July; a mid-August flush; a quiet September; the season running on in
  November.

## Places, for the intro copy

Sourced areas:
- **Porcini.**
  - The Sila: Camigliatello and the Sila Grande summits (Monte Scuro, Monte Nero), Lorica, the Sila
    Greca around Acri and Longobucco, the Sila Piccola around Taverna, Villaggio Mancuso and Petronà.
  - The Pollino and Orsomarso.
  - The Catena Costiera (Monte Cocuzzo).
  - The Serre (Serra San Bruno, Archiforo, Ferdinandea).
  - The Aspromonte (Gambarie, Zervò, the Costa Viola).
- **The spring *B. pinophilus*:** the Sila, Pollino and Aspromonte pinewoods in May and June.
- **Ovoli:** the chestnut and oak of the Catena Costiera (Cerisano, Mendicino), the pre-Sila between
  the Sila Piccola and the Sila Greca, and the Rossano hills.
- **Gallinacci:** the chestnut, oak and beech of the province of Cosenza; the cork-oak woods.
- **Seasons:**
  - May-June for *B. pinophilus* and the first chanterelles.
  - Storm-driven summer porcini in July and August in the mountains.
  - The main season from September to November.
  - *B. aereus* into December at low altitude.
  - Camigliatello's mushroom festival in October.

## Open questions and hand-offs

- **Laricio plantations against natural laricio.** 71 % of `mountain_pine` is the 1955-1970
  reforestation (42.G_n). The ISPRA plantation table has only 40 *Pinus nigra* records and no porcino
  among them. The "natural" laricio table, with *B. pinophilus* 8th of 933 species, probably includes
  the oldest plantations. The rules treat the two alike, as the habitat vocabulary has one key for
  both. The backtest can tell whether porcini records fall short in 42.G_n cells.
- **83.31_m holds the fir plantations** (for the region card). ISPRA's conversion table sends the
  regional "Rimboschimenti di Abies alba" to 83.31_m. The region card files 83.31_m (19,400 ha,
  median 844 m) as `mountain_pine`. *B. edulis* is the top species of the fir plantation records (4.6
  %), but gets 0.1 in `mountain_pine`. If the plantation polygons can be told apart, the fir ones
  belong in `fir_spruce`. Most 83.31_m polygons are low (p10 284 m), so most are probably not fir.
- **Forest area** (for the region card). The habitat map's broadleaf and conifer woodland is 586,700
  ha, 18 % over INFC 2015's bosco of 495,177 ha. The grid build will show whether the woodland mask
  brings it within the ±10 % the card asks for.
- **Rain scale** (for the region card). ARPACAL's daily data need registration with an identity card
  and may not be passed on. No open gauge set was found.
- **Slope and sun exposure.** Both stoppers are anchored on Tuscan grid percentiles. Check them on
  the Calabria grid once it is built.
- **The chanterelle names.** The ISPRA beech and poplar rows entered as "C. alborufescens" are read
  as the determiners' name for the local chanterelle. The monograph does not record *C.
  alborufescens* in Calabria.
- **The ovolo's peak.** Lavorato: "raramente in autunno". The records and Monte Cocuzzo put it in
  September-October. The window keeps both; the backtest will say.
- **Few records.** 118 iNaturalist records of the six keys, mostly Sila porcini. The backtest will
  say little about the ovolo and the chanterelles.
- **Leads not read.**
  - The Calabria chapter of Blasi (2010), *La vegetazione d'Italia* (no file online).
  - Lavorato & Rotella's book *Funghi in Calabria* and *La Sila e i Funghi* (1991), not online.
  - The Sila park's new regulation (BURC 7 August 2026), announced but not linked.
  - The Region's PAT sheet PDFs, truncated on its server.

## References added for Calabria

| id | kind | verified | used for |
|---|---|---|---|
| `ispra2018_mlg180_calabria_foreste` | institutional | verified | per-habitat record shares of the six taxa; laricio, beech and fir belts |
| `ispra2018_mlg179_calabria_rimboschimenti` | institutional | verified | plantation record shares: no porcino under *Pinus nigra*, Aleppo pine or Douglas fir; *B. edulis* top in fir plantations |
| `ispra2018_mlg184_acri_vol1` | institutional | verified | Calabrian seasons of *B. aereus*, *B. edulis*, the ovolo |
| `ispra2018_mlg185_acri_vol2` | institutional | verified | Calabrian season and hosts of the chanterelle |
| `lavorato1996_boletaceae_calabria` | society | verified | the four porcini's Calabrian hosts and names; *B. reticulatus* "precoce già in giugno" |
| `lavorato_rotella2004_pini_sila_greca` | society | verified | fungi under the Sila Greca pines; Sila Greca belts |
| `lavorato_rotella1995_mappatura_cosenza` | society | verified | dated 1994 records with habitat and height |
| `lavorato2013_calabrone_caesarea` | society | verified | ovolo early, to 1,200 m, chestnut, dialect names |
| `lavorato2018_calabrone_consigli` | society | verified | May starts in wet years |
| `caroti2015_cantharellaceae_calabria` | society | verified | Calabrian chanterelles, seasons and hosts |
| `bosco_grande2004_caesarea_cocuzzo` | society | verified | ovolo heights, months, lags; *B. reticulatus* near Christmas |
| `grande_funghi_silagreca` | society | verified | *B. aereus* only under broadleaves; Christmas porcini |
| `iacoi2003_macchia_rossano` | society | verified | porcini and ovoli under the oaks of the macchia belt |
| `lavorato1991_micoflora_cisto` | society | verified | no Calabrian Cistus record of *B. aereus* |
| `ambsg_manuale_corso_micologia` | society | verified | Acri dialect names of the four porcini |
| `amer2024_weekend_sila` | society | verified | late-October porcini in mixed beech and laricio |
| `miceli2019_sua_maesta_porcino` | web | verified | "Zappinaro" and the Aspromonte pines (folklore) |
| `parcosila_funghi` | institutional | verified | Sila park: porcini with broadleaves and conifers; ovolo scarce |
| `parcosila_vegetazione` | institutional | verified | pine on south slopes, beech on north slopes |
| `pn_sila_geografia_web` | institutional | verified | Sila rain and dry season |
| `vivigreen_pat_porcini_silani` | web | verified | the Sila porcini PAT season |
| `masaf2023_pat_calabria` | institutional | verified | "Funghi porcini silani 'sillo'" as a traditional product |
| `lupo_talmamax_re_porcino_sila` | web | verified | Sila forager sequence and places (folklore) |
| `funghimagazine_porcini_maggio2022` | web | verified | May *B. pinophilus* flush in the Sila (folklore) |
| `bmeteo_pinophilus_oppicelli2024` | web | verified | *B. pinophilus* from May on the Calabrian mountains (folklore) |
| `bmeteo_boletus_aereus` | web | verified | *B. aereus* rain and heat lore, Christmas flushes (folklore) |
| `funghimagazine_calendario_primavera2019` | web | verified | Centre-South spring and summer sequence (folklore) |
| `funghimagazine_giugno2019` | web | verified | first southern chanterelles and *B. aereus* in June (folklore) |
| `funghimagazine_nascite_2025_08_01` | web | verified | the August gap (folklore) |
| `funghimagazine_nascite_2025_11_08` | web | verified | the southern November season (folklore) |
| `funghimagazine_2023_dodici_mesi` | web | verified | the 2023 Sila season, May to December (folklore) |
| `informacalabria_porcini2025` | web | verified | early-July porcini in the Sila Piccola (folklore) |
| `noidicalabria_serra_porcini2026` | web | verified | July porcini around Serra San Bruno (folklore) |
| `lr_calabria_30_2001` | institutional | verified | the picking law in force |
| `lr_calabria_19_2026` | institutional | verified | its latest amendment |
| `pn_aspromonte_regolamento2016` | institutional | verified | Aspromonte park picking rules |
| `infc2015_calabria` | dataset | verified | forest area and categories |
| `calabria_pfr2024` | institutional | verified | belts, reforestation history, soils, climate |
| `nicolaci2014_laricio_sila` | peer-reviewed | verified | laricio heights, plantations, Sila rain and snow |
| `bissanti1973_neve_sila` | peer-reviewed | verified | Sila monthly rain and snow |
| `terranova2011_rain_events` | peer-reviewed | verified | Calabria rain totals and season |
| `muscolo2021_laricio_soil` | peer-reviewed | verified | soil pH under Aspromonte laricio |
| `ispra_cdn_calabria_legenda2024` | institutional | verified | 42.G_n = *Pinus nigra* reforestation; fir plantations in 83.31_m |
| `arpacal_cfm_dati_storici` | web | verified | ARPACAL daily data need registration |
| `mushma_calabria_forest_composition_2026` | analysis | verified | habitat shares and heights on the Carta della Natura; gate effects |
| `mushma_occurrence_check_calabria_2026` | analysis | verified | month counts, heights, habitats of the records; Tuscany comparison |

Existing references the Calabria changes lean on:
- `rt_tipi_forestali_p4`: the Tuscan beech belt, for comparison.
- `olariaga2017`: the *Cantharellus* segregates, for the synonym list.
