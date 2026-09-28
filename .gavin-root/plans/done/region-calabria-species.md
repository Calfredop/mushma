---
kind: task
title: [region] Calabria — species research and rules
parent: region-calabria.md
complexity: complex
---
Species research for Calabria (child of `region-calabria.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-2`, branch `region/calabria`). API id
`calabria`, ISTAT COD_REG 18. The toe of Italy, from sea level to 2,267 m, five mountain blocks
between two seas:

- **Pollino** (the Calabrian side: Morano Calabro, Castrovillari, Frascineto, Civita, San Lorenzo
  Bellizzi, Cerchiara di Calabria, Alessandria del Carretto, Saracena, Mormanno, Laino Borgo, San
  Donato di Ninea, Sant'Agata di Esaro) and the **Monti di Orsomarso** (Orsomarso, Verbicaro,
  Papasidero, Grisolia): beech up to about 1,900–2,000 m, relict silver fir, Apennine black pine,
  the Bosnian pine (*pino loricato*, *Pinus heldreichii*) on the limestone summits (Serra
  Dolcedorme 2,267 m, Serra di Crispo), Turkey oak and downy oak lower.
- **Catena Costiera** (the Paolana coastal range, Monte Cocuzzo 1,541 m: Fuscaldo, Paola, San Fili,
  Cerisano, Fiumefreddo Bruzio, Longobardi, Lago, Aiello Calabro): beech on the crest, chestnut
  belts, holm oak towards the Tyrrhenian; very wet (Tyrrhenian orographic rain).
- **Sila** (Sila Greca, Sila Grande, Sila Piccola; Botte Donato 1,928 m; granite and gneiss, acid
  soils; snow in winter): the Calabrian black pine (*pino laricio*, *Pinus nigra* subsp. *laricio*)
  dominant at 1,000–1,600 m, much of it replanted after the war; beech above about 1,300 m on the
  moister slopes; chestnut, Turkey oak and *Alnus cordata* lower. The best-known porcini ground of
  southern Italy: Camigliatello Silano (Spezzano della Sila), Lorica (San Giovanni in Fiore, Casali
  del Manco), San Giovanni in Fiore, Longobucco, Bocchigliero, Acri, Celico, Spezzano Piccolo,
  Taverna and Villaggio Mancuso, Albi, Magisano, Zagarise, Sersale, Cotronei, Savelli, Mesoraca,
  Petronà, Aprigliano, Parenti, Rogliano, Colosimi, Carlopoli; the **Reventino** (Soveria Mannelli,
  Decollatura, Platania) south of it. Camigliatello holds a mushroom festival every October.
- **Serre** (Serre Vibonesi and Catanzaresi, Monte Pecoraro 1,423 m: Serra San Bruno, Mongiana,
  Fabrizia, Spadola, Brognaturo, Simbario, Nardodipace, Stilo, Bivongi, Pazzano, Cardinale,
  Chiaravalle Centrale, Torre di Ruggiero): silver fir with beech (Bosco di Santa Maria, Archiforo),
  chestnut; and Monte Poro (Vibo Valentia) with chestnut.
- **Aspromonte** (Montalto 1,955 m, granite and gneiss: Santo Stefano in Aspromonte with Gambarie,
  San Luca and Polsi, Delianuova, Scido, Cosoleto, Sinopoli, Oppido Mamertina, Platì, Cittanova,
  Molochio, Mammola, Canolo, Gerace, Roccaforte del Greco, Bova, Bagaladi, Cardeto, Africo): beech,
  laricio pine, silver fir, chestnut, holm oak.
- Low down: holm oak and cork oak (Tyrrhenian hills, the Catanzaro isthmus, the Sila foothills),
  Aleppo pine on the dry Ionian coast (Crotone, Rossano, Cirò, the Reggio Ionian hills), stone pine
  on dunes, Mediterranean macchia, *Spartium* scrub, eucalyptus plantations. The Tyrrhenian slopes
  get 1,500–2,000 mm a year, the Ionian coast 600–800 mm.

Deliver:
- `.gavin-root/docs/species-ecology/calabria.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Campania, the first southern region, is the nearest precedent: its doc and
  rules are on the unmerged branch `region/campania` (`git show
  region/campania:.gavin-root/docs/species-ecology/campania.md`, `git show
  region/campania:api/src/api/config/species/campania/<file>`, and `region/campania`'s
  `references.yaml`), so read them there; also `species-ecology/marche.md` and `umbria.md` on this
  branch. Say where Calabria departs from Campania and from the central-Italian windows. Two
  questions matter most: **porcini under laricio pine in the Sila** (which keys fruit there —
  *B. pinophilus*, *B. edulis* — when, and how strongly: the pine is `mountain_pine` in the
  grid and covers about 100,000 ha, the region's second woodland after beech), and the **southern
  season** (early summer flushes after rain, a summer drought gap, autumn from September into
  November or later at low altitude; *B. aereus* in chestnut, oak and holm oak).
- `api/src/api/config/species/calabria/` started from `tuscany/` (look at `campania/` on its branch,
  and `marche/`, `umbria/`, `emilia_romagna/`, `piemonte/`, `liguria/` here, for how other regions
  retuned): per-species YAML with season windows, habitat affinities and altitude bands retuned for
  Calabria; every factor cited with a confidence; groups or keys the region lacks dropped and the
  doc says so. Altitude bands matter: woodland runs from the coast to about 2,000 m, beech tree line
  near 1,900–2,000 m on the Pollino, the laricio belt at 1,000–1,600 m.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). Campania's branch adds its own keys to the same file:
  don't reuse a key it defines, and add yours in a block of their own (not interleaved with
  Campania's) so the two branches merge cleanly. The regional mushroom law (L.R. Calabria 30/2001
  on picking epigeous mushrooms, and its amendments, to verify) belongs in the doc.
- `calabria/sanity.yaml`: press or blog contrasts for Calabria's areas (comuni) and years (Cosenza,
  Catanzaro, Crotone, Vibo and Reggio local press, Funghi Magazine's national bulletins, the Sila
  park, report porcini seasons in the Sila, Pollino, Serre and Aspromonte), written before any
  Calabria score exists, in the same format as the other regions'. Every `comune` must be an ISTAT
  2025 comune name inside Calabria (note Casali del Manco, formed 2017 from Pedace, Serra Pedace,
  Spezzano Piccolo, Casole Bruzio and Trenta; Corigliano-Rossano, 2018).
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Calabria's woodland
from ISPRA and Regione Calabria's **Carta della Natura della Regione Calabria, carta degli habitat
1:25,000 (2023)** (`api/src/api/config/regions/calabria.yaml`, written in parallel), CORINE
Biotopes codes to habitats, whole-map areas:

- `beech` — 41.18 southern Italian beech woods (100,254 ha)
- `deciduous_oak` — 41.732 downy oak (72,496 ha), 41.7511 Turkey oak (29,010), 41.7512 Turkey oak
  with Hungarian oak / farnetto (45,324), 41.7513 sessile oak, 44.4 floodplain pedunculate oak
- `chestnut` — 41.9 chestnut woods (83,645 ha), 83.12 chestnut orchards (1,683)
- `mixed_broadleaf` — 41.C1 *Alnus cordata* woods (13,923 ha), 41.81 hop-hornbeam (1,421), 41.4
  ravine woods, 41.D aspen
- `evergreen_oak` — 45.31 thermo- and meso-Mediterranean holm oak (56,521 ha), 45.32
  supra-Mediterranean holm oak (38,979), 45.21 cork oak (10,787), 45.8 holly
- `mountain_pine` — 42.65 laricio pine (8,439 ha), 42.G_n conifers planted outside their range
  (70,157 ha, mostly laricio reforestation in the Sila and the Presila, some Douglas fir), 83.31
  conifer plantations (19,401), 42.612 Apennine black pine (540, Pollino), 42.711 *pino loricato*
  (387, Pollino). INFC 2015 counts 73,443 ha of "pinete di pino nero, laricio e loricato" in
  Calabria, 15 % of its high forest.
- `fir_spruce` — 42.15 southern Apennine silver fir (3,423 ha, Serre, Aspromonte, Pollino)
- `mediterranean_pine` — 42.84 Aleppo pine (11,943 ha), 42.83 stone pine (1,672), 16.29 wooded dunes
- `riparian` — 44.61 poplar (7,719 ha), 44.513 black alder, 44.14 willow, 44.71 plane
- `exotic_broadleaf` — 41.L_n (4,141 ha, robinia, ailanthus), 44.D2_n
- `macchia` — 32.214 lentisk, 32.215 *Cytisus*, 32.11 evergreen-oak matorral, 32.3 macchia,
  32.22, 32.12, 32.13, 16.27, 16.28 (about 70,000 ha)
- `transitional_woodland_shrub` — 32.A *Spartium* (30,150 ha), 31.844 broom, 31.81 deciduous scrub,
  31.8A bramble, 44.12 and 44.81 riparian scrub, 31.87 recently burnt or felled woodland (about
  58,000 ha)
- Left out (not woodland): 83.325 broadleaf plantations (22,723 ha, mostly eucalyptus), 32.23
  *Ampelodesmos* steppe, 31.863 bracken, grassland, orchards.

Say in the doc which habitat holds which Calabria tree.

Do not commit and do not edit any plan card.
