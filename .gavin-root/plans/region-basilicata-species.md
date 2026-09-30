---
kind: task
title: [region] Basilicata — species research and rules
parent: region-basilicata.md
complexity: complex
---
Species research for Basilicata (child of `region-basilicata.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-1`, branch `region/basilicata`). API id
`basilicata`, ISTAT COD_REG 17, names "Basilicata" / en "Basilicata" (also called Lucania). About
10,000 km², provinces Potenza and Matera, between Campania (west), Puglia (north and east) and
Calabria (south), with a short Tyrrhenian coast at Maratea and the Ionian coast of the Metapontino.
Woodland from the Ionian dunes to about 2,000 m on the Pollino. INFC 2015 counts 288,020 ha of
forest ("bosco"); Turkey oak leads it by far, then downy oak, beech in the mountains, holm oak,
*Alnus cordata* and hop-hornbeam; chestnut is small.

- **The Pollino** (the Lucanian side of the national park: Terranova di Pollino, San Severino
  Lucano with the Bosco Magnano, Viggianello, Rotonda, Chiaromonte, Castelsaraceno, Latronico,
  Episcopia, Francavilla in Sinni, Noepoli, Cersosimo, San Costantino Albanese, San Paolo Albanese):
  beech to about 1,900–2,000 m, relict silver fir, the Bosnian pine (*pino loricato*) on the
  limestone summits, Turkey oak and downy oak lower.
- **The Lagonegrese and Maratea** (Monte Sirino 2,005 m and Lago Laudemio, Monte Alpi, Monte
  Raparo: Lagonegro, Lauria, Nemoli, Rivello, Trecchina, Maratea, Moliterno): beech, chestnut, very
  wet on the Tyrrhenian side.
- **The Val d'Agri and the Monti della Maddalena** (Marsico Nuovo, Marsicovetere, Paterno,
  Viggiano, Grumento Nova, Sarconi, Tramutola): beech, Turkey oak.
- **The central Lucanian Apennine**: the Sellata, Volturino and Arioso (Abriola, Calvello, Pignola
  with the Bosco di Rifreddo's silver fir and beech, Anzi, Laurenzana with its fir wood, Sasso di
  Castalda, Brienza); the Gallipoli Cognato forest and the Piccole Dolomiti Lucane (Accettura,
  Oliveto Lucano, Calciano, Castelmezzano, Pietrapertosa: Turkey oak); Monte Li Foi (Picerno),
  Ruoti, Muro Lucano, Bella, Ruvo del Monte, San Fele, Vietri di Potenza.
- **The Vulture** (extinct volcano, Monte Vulture 1,326 m, volcanic soils: Rionero in Vulture,
  Atella, Melfi, Rapolla, Barile, the Laghi di Monticchio): beech, chestnut, Turkey oak.
- **The Materano**: the Murgia materana (Matera, Montescaglioso: holm oak, *Quercus trojana*
  fragno, downy oak), the clay hills and calanchi (Aliano, Craco, Stigliano, Tricarico, Irsina),
  Aleppo-pine reforestation, and the **Ionian coast** pine woods on the dunes (Policoro with the
  Bosco Pantano, Scanzano Jonico, Pisticci, Bernalda, Metaponto, Nova Siri).

Deliver:
- `.gavin-root/docs/species-ecology/basilicata.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/calabria.md`,
  `species-ecology/campania.md` and `species-ecology/puglia.md` in this checkout (the three
  neighbours are merged here). Say where Basilicata's evidence follows its neighbours' windows and
  where it departs (the Turkey-oak hills, the high Pollino and Sirino, the dry Materano and
  Ionian coast, the late cold springs of the Potentino).
- `api/src/api/config/species/basilicata/` started from `tuscany/` (look at `calabria/`,
  `campania/`, `puglia/` and `abruzzo/` for how the neighbours retuned): per-species YAML with
  season windows, habitat affinities and altitude bands retuned for Basilicata; every factor cited
  with a confidence; groups or keys the region lacks dropped and the doc says so. Altitude bands
  matter: woodland runs from the coast to about 2,000 m (beech median about 1,260 m, Turkey oak
  about 910 m, chestnut about 870 m on the map).
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite; reuse an existing key when a neighbour already cites the
  source). Add yours in one block of their own at the end of the file, so the unmerged
  `region/molise` and `region/veneto` branches, which append blocks too, merge cleanly. The
  regional mushroom law (Basilicata's L.R. on picking epigeous mushrooms and its amendments, to
  find and verify) belongs in the doc.
- `basilicata/sanity.yaml`: press or blog contrasts for Basilicata's areas (comuni) and years (La
  Nuova del Sud, il Quotidiano del Sud, SassiLive, TRM, Lucania TV, ivl24, Funghi Magazine's
  national bulletins, mycological groups and forager blogs on the Pollino, Sirino, Sellata,
  Vulture and Gallipoli Cognato seasons, mushroom festivals), written before any Basilicata score
  exists, in the same format as the other regions'. Every `comune` must be an ISTAT 2025 comune
  name inside Basilicata. Say in the doc where a contrast rests on one source.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Basilicata's forest
from ISPRA's Carta della Natura (1:50,000, 2012–2013, CORINE Biotopes codes) as
`api/src/api/config/regions/basilicata.yaml` says (read it). Whole-map areas:

- `deciduous_oak` — 41.7511 Turkey oak 113,397 ha (median 913 m), 41.732 downy oak 36,184 (673 m),
  41.737B southern Italian white oak 19,129 (568 m), 41.7512 Turkey oak with farnetto 16,614
  (847 m), 41.782 *Quercus trojana* (fragno) 249
- `beech` — 41.18 southern Italian beech woods 28,494 ha (median 1,259 m, 10th–90th percentile
  982–1,468 m)
- `evergreen_oak` — 45.324 supramediterranean holm oak 11,975 ha (607 m), 45.31A southern holm
  oak 3,501 (277 m)
- `mixed_broadleaf` — 41.C1 *Alnus cordata* 9,656 ha (1,028 m), 41.81 hop-hornbeam 5,413 (805 m),
  41.41 ravine woods 171
- `riparian` — 44.61 poplar 10,228 ha, 44.14 and 44.13 willow, 44.513 black alder, 44.63
  narrow-leaved ash (13,421 ha together)
- `chestnut` — 41.9 chestnut woods 4,253 ha (median 867 m)
- `other_conifer` — 83.31 conifer plantations 18,676 ha, median 474 m but split: Aleppo pine on
  the clay hills and the Ionian side (56 % below 600 m, 10th percentile 141 m) and black pine in
  the mountains (90th percentile 1,225 m). One code, one habitat, so here `other_conifer` means
  "conifer plantations, Aleppo pine low and black pine high": set its affinities for that mix and
  let the altitude bands separate them.
- `mediterranean_pine` — 42.84 Aleppo pine 1,407 ha (median 196 m), 16.29 wooded dunes 1,148 (the
  Ionian coast's planted stone and Aleppo pine)
- `mountain_pine` — 42.711 *pino loricato* 320 ha (Pollino)
- `fir_spruce` — 42.15 southern Apennine silver fir 177 ha (1,129 m)
- `exotic_broadleaf` — 83.324 robinia 305 ha
- `macchia` — 32.211 low macchia of wild olive and lentisk 29,316 ha (median 269 m), 32.4 and 32.3
  garighe and macchia, 32.215 *Cytisus*, 32.11, 32.13, 16.27, 16.28, 45.1 olive and carob
- `transitional_woodland_shrub` — 31.81 deciduous thickets 24,592 ha (966 m), 31.8A bramble 26,540
  (694 m), 31.844 broom, 31.88 juniper, 44.12 shrub willows, 44.81 tamarisk and oleander
- Left out (not woodland): 83.325 broadleaf and 83.322 eucalyptus plantations, 32.23
  *Ampelodesmos* steppe, 31.863 bracken, garighe, grassland, rock.

There is no `mixed_broadleaf_conifer` here. Say in the doc which habitat holds which Basilicata
tree. The grid's numbers (habitat shares, elevations) land in `.gavin-root/docs/regions/basilicata.md`
→ "Woodland grid" while you work; read them when they are there.

Do not commit and do not edit any plan card.
