---
kind: task
title: [region] Puglia — species research and rules
parent: region-puglia.md
complexity: complex
---
Species research for Puglia (child of `region-puglia.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-3`, branch `region/puglia`). API id `puglia`,
ISTAT COD_REG 16, 257 comuni. The heel of Italy: mostly farmland (olive, vine, cereals) on
limestone, highest point 1,152 m (Monte Cornacchia, Monti Dauni). Woodland is scarce (INFC 2015
bosco 142,349 ha, 7 % of the region) and sits in a few blocks:

- **Gargano** (Monte Calvo 1,065 m; Foresta Umbra; Parco nazionale del Gargano): the "faggeta
  depressa", beech from about 300–400 m to the top on the northern slopes (Vico del Gargano,
  Monte Sant'Angelo, Ischitella), with holly and yew; Turkey oak and downy oak woods (Foresta
  Umbra, San Marco in Lamis, San Giovanni Rotondo, Carpino, Cagnano Varano, Rignano Garganico,
  Sannicandro Garganico), some chestnut (Cagnano Varano, San Marco in Lamis), holm oak and Aleppo
  pine on the coast (Vieste, Peschici, Mattinata, Rodi Garganico, Manfredonia's Monte Sacro). The
  Tremiti islands (Aleppo pine) belong to the region.
- **Monti Dauni / Subappennino Dauno** (Monte Cornacchia 1,152 m, Monte Crispianiano, Monte
  Saraceno): Turkey oak and downy oak, some beech on the tops (Faeto, Biccari, Roseto Valfortore,
  Alberona, Pietramontecorvino, Celle di San Vito), black-pine reforestation; comuni Bovino,
  Deliceto, Accadia, Sant'Agata di Puglia, Orsara di Puglia, Monteleone di Puglia, Anzano di
  Puglia, Castelluccio Valmaggiore, Volturara Appula, Motta Montecorvino, Volturino, Casalnuovo
  Monterotaro, Celenza Valfortore, Carlantino, San Marco la Catola, Casalvecchio di Puglia.
- **Murge**: the Alta Murgia (Parco nazionale; Altamura, Gravina in Puglia, Ruvo di Puglia,
  Minervino Murge, Spinazzola, Andria, Corato, Cassano delle Murge with the Mercadante forest,
  Santeramo in Colle, Acquaviva delle Fonti): downy oak, grassland and Aleppo-pine reforestation;
  the south-eastern Murge (Murgia dei Trulli: Martina Franca with the Bosco delle Pianelle, Noci,
  Alberobello, Locorotondo, Cisternino, Mottola, Gioia del Colle with the Bosco Romanazzi,
  Putignano, Castellana Grotte): the **Macedonian oak (fragno, *Quercus trojana*)**, found in Italy
  only here and in Basilicata, with downy oak and Turkey oak.
- **Arco ionico and the gravine** (Massafra, Castellaneta, Laterza, Ginosa, Palagianello,
  Crispiano, Grottaglie): Aleppo pine (natural stands on the gravine and coast, the pinete of
  Castellaneta Marina and Marina di Ginosa), holm oak, macchia.
- **Salento** (Lecce, Brindisi, Taranto provinces south of the Murge): relict holm oak (Bosco di
  Rauccio at Lecce), cork oak (Bosco di Santa Teresa and dei Lucci at Brindisi), the *Quercus
  macrolepis* (vallonea) of Tricase, coastal Aleppo pine and stone pine (Porto Selvaggio at Nardò,
  Ugento, Otranto), macchia with olive and lentisk.
- Rain: 450–650 mm a year on the Tavoliere and the Salento coast, 800–1,100 mm on the Gargano and
  the Monti Dauni; long summer drought.

Deliver:
- `.gavin-root/docs/species-ecology/puglia.md`: the regional evidence (season windows, host trees
  and habitat affinities, altitude bands, weather rules where regional literature exists), each
  claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in `species-ecology.md`).
  The southern precedents are on unmerged branches: Campania (`git show
  region/campania:.gavin-root/docs/species-ecology/campania.md`, `git show
  region/campania:api/src/api/config/species/campania/<file>`), Calabria (`region/calabria`, same
  paths) and Abruzzo (`region/abruzzo`); read them there, and `species-ecology/marche.md`,
  `umbria.md` on this branch. Say where Puglia departs from Campania and Calabria. The questions
  that matter most: **which keys fruit under the Macedonian oak** (fragno woods cover about
  22,000 ha; *B. aereus*, *B. reticulatus*, the ovolo, chanterelles?) and in the Murge's downy oak;
  **the Gargano's low-altitude beech** (is *B. edulis* there, and at what elevation and season);
  whether **Aleppo pine** (32,000 ha, the region's second woodland) hosts any of the six keys, or
  only other fungi (Lactarius, Suillus); and **the southern season** (spring and early-summer
  flushes after rain, the summer drought, autumn from October into December or later at low
  altitude). The region is known for its cardoncelli (*Pleurotus eryngii*) in the Murge: not in
  scope, but its folk calendars and press may still report porcini and ovoli.
- `api/src/api/config/species/puglia/` started from `tuscany/` (look at `campania/` and
  `calabria/` on their branches, and `marche/`, `umbria/` here, for how other regions retuned):
  per-species YAML with season windows, habitat affinities and altitude bands retuned for Puglia;
  every factor cited with a confidence; keys or groups the region lacks dropped and the doc says so
  (*B. pinophilus* is the likely candidate: the grid has only 1,400 ha of black-pine
  reforestation). Altitude bands matter: woodland runs from sea level to about 1,150 m, and the
  beech of the Foresta Umbra comes down to 300–400 m.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). The Campania, Calabria and Abruzzo branches add their own
  keys to the same file: don't reuse a key any of them defines (`git show
  region/<branch>:api/src/api/config/species/references.yaml`), and add yours in a block of their
  own at the end (not interleaved) so the branches merge cleanly. The regional law on picking
  epigeous mushrooms (to find and verify) belongs in the doc.
- `puglia/sanity.yaml`: press or blog contrasts for Puglia's areas (comuni) and years (Foggia,
  Bari, Taranto, Lecce and Brindisi local press, Funghi Magazine's national bulletins, the
  Gargano and Alta Murgia parks, mycological groups), written before any Puglia score exists, in
  the same format as the other regions'. Every `comune` must be an ISTAT 2025 comune name inside
  Puglia (note Presicce-Acquarica, formed 2019).
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Puglia's woodland from
Regione Puglia's **Carta dei Tipi Forestali** (ARIF and the Università di Bari, approved by DGR
1279/2022; FRA 2000 forest definition), its forest types mapped to habitats as follows
(`api/src/api/config/regions/puglia.yaml`, written in parallel), whole-map areas:

- `deciduous_oak` — 3111 cerrete, fragneti and vallonea: Macedonian oak (CE7 fragno of mesic soils
  20,558 ha, CE6 fragno of xeric soils 1,250), Turkey oak (CE1–CE5, CE9: 31,913), *Q. macrolepis*
  (CE8, 6 ha); 3110 downy oak (QU1–QU5: 20,741 ha, with holm oak or wild olive in QU3, with
  Turkey oak and hop-hornbeam in QU4, with *Carpinus orientalis* in QU5)
- `evergreen_oak` — 3117 leccete (LE1–LE8: 17,793 ha, thermophilous, typical, rupicolous,
  submontane with Turkey oak) and 3118 cork oak (78 ha, Brindisi)
- `mediterranean_pine` — 3120 Aleppo pine (30,980 ha: PA6 reforestation of the inland Murge
  12,575, PA1 coastal reforestation 3,499, natural stands with lentisk, holm oak, on the gravine and
  cliffs), 3122 BC1 other Mediterranean conifers (1,124 ha, cypress and stone pine)
- `mixed_broadleaf` — 3112 hop-hornbeam and hornbeam (OS1–OS5: 5,611 ha, *Carpinus orientalis*
  scrub-woods included) and 3116 other deciduous woods (BN2 invasion woods 6,577 ha, maple 248,
  aspen 9)
- `beech` — 3114 faggete (FA1–FA4: 4,009 ha; submontane beech with holly and yew, with Turkey oak,
  with hornbeam, and the "faggete abissali" of the Gargano's karst hollows)
- `riparian` — 3115 willow, poplar, elm and ash galleries (3,830 ha)
- `mountain_pine` — 3121 black and laricio pine reforestation (1,400 ha)
- `chestnut` — 3113 (698 ha; ISPRA's Carta della Natura maps 3,110 ha of chestnut, mostly at
  Cagnano Varano and San Marco in Lamis)
- `other_conifer` — 3122 BC2 montane reforestation with other conifers (283 ha)
- `macchia` — 323 (MM1 wild olive and lentisk 28,563 ha, coastal and dune macchia, *Quercus
  coccifera*, Phoenician juniper, garighe) and 3119 wild-olive formations (3,625 ha)
- `transitional_woodland_shrub` — 322 blackthorn scrub (10,284 ha), *Paliurus* pseudo-macchia
  (4,622), broom (3,136); 3140 wooded pastures (3,714 ha); tamarisk and shrub-willow scrub
- Left out: 321 grassland, bracken (AR3), poplar and other tree plantations (224x).

Say in the doc which habitat holds which Puglia tree (fragno is `deciduous_oak`).

Do not commit and do not edit any plan card.
