---
kind: task
title: [region] Lazio — species research and rules
parent: region-lazio.md
complexity: complex
---
Species research for Lazio (child of `region-lazio.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-1`, branch `region/lazio`). API id
`lazio`, ISTAT COD_REG 12. Tuscany's neighbour to the south, from the sea to about 2,200 m, with
two very different halves:

- **The volcanic districts** (acid to neutral soils on tuff and ash): the Monti Cimini (Soriano nel
  Cimino, Canepina, Vallerano, Caprarola, Ronciglione, Vitorchiano, Viterbo; the "depressed" beech
  of Monte Cimino at 900–1,050 m and Monte Venere, one of the UNESCO ancient beech forests, and a
  wide chestnut belt), the Monti Sabatini round Lake Bracciano (Manziana's Macchia Grande Turkey
  oak, Oriolo Romano's beech of Monte Raschio at about 450–550 m, Bracciano, Trevignano), the Monti
  Volsini round Lake Bolsena (Bolsena, Acquapendente, Monte Rufeno reserve, the Bosco del Sasseto)
  and the Colli Albani / Castelli Romani (Rocca di Papa, Rocca Priora, Lariano, Velletri, Nemi,
  Monte Compatri: chestnut coppice). The Tolfa mountains (Tolfa, Allumiere) are Turkey oak,
  chestnut and some cork oak on flysch and volcanics.
- **The limestone Apennines** (beech from about 1,000 m to the treeline at 1,800–1,900 m): the
  Monti Reatini and the Terminillo (Leonessa, Cantalice, Micigliano, Rieti), the Monti della Laga on
  the Lazio side (Amatrice, Accumoli; sandstone, with chestnut, Turkey oak and beech), the Cicolano
  and the Monti Carseolani (Borgorose, Pescorocchiano, Fiamignano), the Monti Simbruini (Subiaco,
  Jenne, Vallepietra, Cervara di Roma, Camerata Nuova, Filettino and Campo Staffi, Monte Livata),
  the Monti Ernici (Guarcino, Collepardo, Fiuggi, Vico nel Lazio, Campocatino), the Lazio side of
  the Parco Nazionale d'Abruzzo, Lazio e Molise and the Mainarde (Picinisco, Settefrati, San Donato
  Val di Comino, Campoli Appennino, Forca d'Acero), the Monti Lucretili and Prenestini (Licenza,
  Percile, Guadagnolo), the Monti Lepini (Carpineto Romano, Montelanico, Segni, Norma, Sezze), the
  Ausoni and the Aurunci (Lenola, Pico, Vallecorsa, Esperia, Spigno Saturnia, Campodimele, Monte
  Petrella); Turkey oak, downy oak and hop-hornbeam below the beech.
- **The coast and the islands**: holm oak and cork oak, stone-pine woods (Castel Fusano and
  Castelporziano in Rome, Fregene, Sabaudia), the Circeo National Park's lowland forest (Sabaudia,
  San Felice Circeo: Turkey, Hungarian and pedunculate oak, cork oak), macchia on the Pontine
  islands (Ponza, Ventotene, Zannone) and the Gaeta–Sperlonga coast.

Deliver:
- `.gavin-root/docs/species-ecology/lazio.md`: the regional evidence (season windows, host trees
  and habitat affinities, altitude bands, weather rules where regional literature exists), each
  claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/umbria.md` and
  `species-ecology/marche.md` in this checkout. The neighbouring regions done on other branches
  are readable with git: `git show region/campania:.gavin-root/docs/species-ecology/campania.md`,
  `git show region/abruzzo:.gavin-root/docs/species-ecology/abruzzo.md` and their
  `api/src/api/config/species/<region>/` files (`git show region/campania:api/src/api/config/species/campania/porcini.yaml`,
  and so on). Lazio sits between Tuscany/Umbria and Campania: say where its evidence follows the
  central-Italian windows and where it departs (the low volcanic beech of the Cimini and Sabatini,
  *B. aereus* in the Tolfa and Castelli chestnut and oak, the summer drought on the coast).
- `api/src/api/config/species/lazio/` started from `tuscany/` (look at `umbria/`, `marche/` here
  and `campania/`, `abruzzo/` on their branches for how other regions retuned): per-species YAML
  with season windows, habitat affinities and altitude bands retuned for Lazio; every factor cited
  with a confidence; groups or keys the region lacks dropped and the doc says so. Altitude bands
  matter: woodland runs from the coast to 1,900 m, and the beech also grows unusually low (450 m
  at Monte Raschio, 900 m on the Cimino).
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). If a reference already exists on the campania or abruzzo
  branch, reuse its exact key and entry so the branches merge cleanly. The regional mushroom law
  (Lazio's L.R. on picking epigeous mushrooms, L.R. 32/1998 and its amendments, to verify) belongs
  in the doc.
- `lazio/sanity.yaml`: press or blog contrasts for Lazio's areas (comuni) and years (Viterbo,
  Rieti, Frosinone and Castelli Romani local press, the Funghi Magazine bulletins, forager blogs on
  the Cimini, Terminillo, Simbruini, Tolfa and Castelli seasons), written before any Lazio score
  exists, in the same format as the other regions'. Every `comune` must be an ISTAT 2025 comune
  name inside Lazio.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Lazio's forest types
as `api/src/api/config/regions/lazio.yaml` says (read it once it exists; the regional source is
being chosen in parallel and may be a regional land-use or forest map, ISPRA's Carta della Natura
or CLC IV; the tree-to-habitat meaning is the same either way): beech → `beech`; Turkey oak,
downy oak, Hungarian oak (farnetto), pedunculate oak → `deciduous_oak`; hop-hornbeam and other
broadleaf (maples, ash, hornbeam, the mixed mesophilous woods) → `mixed_broadleaf`; chestnut
(coppice and orchards) → `chestnut`; holm oak and cork oak → `evergreen_oak`; poplar, willow and
alder → `riparian`; robinia and ailanthus → `exotic_broadleaf`; black-pine reforestation (with some
fir, Douglas fir) → `mountain_pine`; stone pine, Aleppo and maritime pine → `mediterranean_pine`;
silver fir → `fir_spruce`; broadleaf with conifers → `mixed_broadleaf_conifer`; Mediterranean
macchia → `macchia`; broom and bramble scrub, regrowth on abandoned fields →
`transitional_woodland_shrub`. Say in the doc which habitat holds which Lazio tree.

Do not commit and do not edit any plan card.
