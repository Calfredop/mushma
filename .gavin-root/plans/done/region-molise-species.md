---
kind: task
title: [region] Molise — species research and rules
parent: region-molise.md
complexity: complex
---
Species research for Molise (child of `region-molise.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-1`, branch `region/molise`). API id
`molise`, ISTAT COD_REG 14, names "Molise" / en "Molise". Small (4,440 km², provinces Campobasso
and Isernia), between Abruzzo (north), Lazio (west), Campania (south) and Puglia (east); woodland
from the Adriatic dunes to about 2,000 m. INFC 2015 counts 153,248 ha of forest, and the Region's
forest-type map (DGR 252/2009) says oaks lead it, Turkey oak and downy oak, with beech in the
mountains and poplar along the rivers; about half is coppice.

- **The Matese** (limestone, the Molise side of the massif, Monte Miletto 2,050 m): beech from
  about 1,000 m up to the treeline; San Massimo (Campitello Matese), Roccamandolfi, Cantalupo nel
  Sannio, Bojano, San Polo Matese, Campochiaro, Guardiaregia, Sepino.
- **The Montagnola di Frosolone** (Frosolone, Sant'Elena Sannita, Macchiagodena, Duronia): beech
  and Turkey oak.
- **The Alto Molise** (sandstone and marl flysch, cold and snowy, 800–1,700 m): beech and Turkey
  oak, and the relict silver fir of the Abeti Soprani and Monte Campo (Pescopennataro, Capracotta),
  Collemeluccio (Pescolanciano) and the Montedimezzo MAB reserve (Vastogirardi); Agnone, San Pietro
  Avellana, Carovilli, Rionero Sannitico, Castel del Giudice, Sant'Angelo del Pesco, Belmonte del
  Sannio, Pietrabbondante.
- **The Mainarde and the upper Volturno** (the Molise side of the Parco Nazionale d'Abruzzo, Lazio
  e Molise): Pizzone, Castel San Vincenzo, Rocchetta a Volturno, Scapoli, Filignano, Montenero Val
  Cocchiara; and the hills round Venafro and Isernia.
- **The hills of the Basso Molise and the Fortore** (clay and flysch, Turkey oak and downy oak,
  some Hungarian oak): Bosco di Monte Mauro and Castelmauro, Trivento, Riccia (Bosco Mazzocca),
  Tufara, Gambatesa, Larino, Casacalenda, Guardialfiera, Montorio nei Frentani.
- **The coast**: Aleppo and stone pine on the dunes of Petacciato, Montenero di Bisaccia and
  Campomarino; holm oak is rare (about 1,800 ha, mostly supramediterranean).

Deliver:
- `.gavin-root/docs/species-ecology/molise.md`: the regional evidence (season windows, host trees
  and habitat affinities, altitude bands, weather rules where regional literature exists), each
  claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/abruzzo.md` and
  `species-ecology/campania.md` in this checkout (both neighbours are merged here, as are Lazio and
  Puglia). Say where Molise's evidence follows its neighbours' windows and where it departs (the
  Turkey-oak hills, the Alto Molise's late cold springs, the dry Basso Molise).
- `api/src/api/config/species/molise/` started from `tuscany/` (look at `abruzzo/`, `campania/`,
  `lazio/` and `puglia/` for how the neighbours retuned): per-species YAML with season windows,
  habitat affinities and altitude bands retuned for Molise; every factor cited with a confidence;
  groups or keys the region lacks dropped and the doc says so. Altitude bands matter: woodland
  runs from the coast to about 1,900 m on the Matese.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite; reuse an existing key when the neighbours already cite the
  source). The regional mushroom law (Molise's L.R. on picking epigeous mushrooms and its
  amendments, to find and verify) belongs in the doc.
- `molise/sanity.yaml`: press or blog contrasts for Molise's areas (comuni) and years (Primo Piano
  Molise, il Quotidiano del Molise, isNews, Molise Network, CBlive, Funghi Magazine's bulletins,
  mycological groups and forager blogs on the Alto Molise, Matese and Frosolone seasons), written
  before any Molise score exists, in the same format as the other regions'. Every `comune` must be
  an ISTAT 2025 comune name inside Molise. Molise's local press is thin: say in the doc where a
  contrast rests on one source.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Molise's forest from
ISPRA's Carta della Natura (2021, CORINE Biotopes codes) as `api/src/api/config/regions/molise.yaml`
says (read it): beech (41.18) → `beech`; downy oak, Turkey oak and Hungarian oak (41.731, 41.732,
41.741, 41.7511, 41.7512) → `deciduous_oak`; hop-hornbeam, ash-maple-hornbeam, ravine woods, aspen
and field elm → `mixed_broadleaf`; chestnut (only about 400 ha) → `chestnut`; holm oak →
`evergreen_oak`; poplar, willow and narrow-leaved ash along rivers → `riparian`; robinia, ailanthus
and the synanthropic woods → `exotic_broadleaf`; silver fir (42.15) → `fir_spruce`; conifers
planted outside their range (42.G_n, mostly black-pine reforestation) → `mountain_pine`; dune pine
woods → `mediterranean_pine`; Mediterranean macchia and dune juniper → `macchia`; deciduous and
broom scrub, bramble, hill juniper scrub → `transitional_woodland_shrub`. There is no
`mixed_broadleaf_conifer` or `other_conifer` here. Say in the doc which habitat holds which Molise
tree. The grid's numbers (habitat shares, elevations) land in `.gavin-root/docs/regions/molise.md`
→ "Woodland grid" while you work; read them when they are there.

Do not commit and do not edit any plan card.
