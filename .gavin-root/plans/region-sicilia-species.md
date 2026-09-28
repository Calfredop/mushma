---
kind: task
title: [region] Sicilia — species research and rules
parent: region-sicilia.md
complexity: complex
---
Species research for Sicilia (child of `region-sicilia.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-3`, branch `region/sicilia`). API id
`sicilia`, ISTAT COD_REG 19. The island, from sea level to Etna (3,357 m; woodland to about
2,000 m), with the small islands (Eolie, Egadi, Ustica, Pantelleria, Pelagie), which hold almost no
woodland. Its woods are 10–12 % of the land and over a third of the high forest is post-war
reforestation. The mountain blocks:

- **Nebrodi** (Monte Soro 1,847 m; flysch and quartzarenite, acid soils; the island's largest
  woods): beech above about 1,300–1,400 m, Turkey oak (*Quercus cerris*) and the endemic
  *Q. gussonei* at 800–1,400 m, downy oak s.l. (*Q. virgiliana*, *Q. congesta*, *Q.
  dalechampii*), cork oak and holm oak lower, holly, chestnut. Comuni: Cesarò, San Fratello,
  Floresta, Ucria, Tortorici, Longi, Alcara li Fusi, Galati Mamertino, Caronia (Bosco di Caronia),
  Mistretta, Capizzi, Santa Domenica Vittoria, Randazzo, Bronte, Maniace, San Teodoro, Militello
  Rosmarino, Castel di Lucio, Castell'Umberto, Raccuja, Sinagra.
- **Madonie** (Pizzo Carbonara 1,979 m; limestone and quartzarenite): beech at 1,400–1,900 m
  (Piano Battaglia, Piano Zucchi, the Nebrodi fir relict at Polizzi), holm oak, downy oak, cork
  oak (Pollina, San Mauro Castelverde), chestnut, pine reforestation. Comuni: Castelbuono, Isnello,
  Petralia Sottana, Petralia Soprana, Polizzi Generosa, Collesano, Geraci Siculo, Gangi,
  Sclafani Bagni, Scillato, Caltavuturo, Pollina, San Mauro Castelverde, Gratteri, Cefalù.
- **Etna** (volcanic soils): laricio pine (*Pinus nigra* subsp. *calabrica*) at 1,000–1,900 m
  (Linguaglossa, Castiglione di Sicilia, Randazzo, Bronte, Nicolosi, Ragalna), beech at the
  tree line on the north and east (Monte Spagnolo, Monte Nero), Etna birch (*Betula aetnensis*),
  chestnut at 500–1,500 m on the east (Zafferana Etnea, Milo, Sant'Alfio, Mascali, Trecastagni,
  Pedara, Viagrande), downy oak and Turkey oak lower, *Genista aetnensis* scrub on young lava.
- **Peloritani** (Messina, schist): chestnut, holm oak, pine and *Erica arborea*
  (Monforte San Giorgio, Fiumedinisi, Santa Lucia del Mela, Castroreale, Novara di Sicilia,
  Messina's Colle San Rizzo and Monte Ciccia reforestation).
- **Sicani and Palermo mountains**: Bosco della Ficuzza and Rocca Busambra (Corleone, Godrano,
  Monreale, Marineo: Turkey oak, *Q. gussonei*, downy oak, cork oak, holm oak), Bosco della
  Quisquina (Santo Stefano Quisquina, Bivona, Castronovo di Sicilia, Cammarata, Palazzo Adriano,
  Prizzi): oak woods and reforestation.
- **Iblei and Erei** (limestone plateau, volcanites at Buccheri and Monte Lauro): cork oak on
  the volcanites, holm oak in the *cave*, Aleppo pine near Vittoria, pine and eucalyptus
  reforestation (Buccheri, Giarratana, Chiaramonte Gulfi, Palazzolo Acreide; Piazza Armerina and
  Aidone's Bosco di Rossomanno, Nicosia and Sperlinga in the Erei).
- Climate: Mediterranean with a long dry summer (June–September) and rain from October to March,
  1,000–1,400 mm on the Nebrodi, Madonie and Peloritani crests and the east flank of Etna, 400–600
  mm on the south coast and inland; snow on the high ground in winter.

Deliver:
- `.gavin-root/docs/species-ecology/sicilia.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Calabria is the nearest precedent: its doc and rules are on the unmerged
  branch `region/calabria` (`git show region/calabria:.gavin-root/docs/species-ecology/calabria.md`,
  `git show region/calabria:api/src/api/config/species/calabria/<file>`, and that branch's
  `references.yaml`); also Campania and Puglia on `region/campania` and `region/puglia`, and
  `species-ecology/marche.md` and `umbria.md` on this branch. Say where Sicily departs from
  Calabria and from the central-Italian windows. Questions that matter most: **the season** (autumn
  from October into December or later, when do the first autumn rains start it; is there a spring
  flush in May–June on the Nebrodi and Madonie; how late *B. aereus* runs in the cork and holm oak
  woods); **porcini under Etna's laricio pine** (which keys, how strongly: the grid files it
  `mountain_pine`, about 3,700 ha, plus 7,200 ha of montane conifer reforestation); **Turkey oak
  and *Q. gussonei*** (the Nebrodi's main porcini host?); **the reforestation** (53,000 ha of
  Mediterranean conifer plantations, Aleppo and stone pine, cypress: `mediterranean_pine`; 39,000
  ha of eucalyptus: `exotic_broadleaf`); and whether *B. pinophilus*, *B. reticulatus*, *A.
  caesarea* and *C. cibarius* are frequent enough in Sicily to keep.
- `api/src/api/config/species/sicilia/` started from `tuscany/` (look at `calabria/`,
  `campania/`, `puglia/` on their branches, and `marche/`, `umbria/`, `emilia_romagna/`,
  `piemonte/`, `liguria/` here, for how other regions retuned): per-species YAML with season
  windows, habitat affinities and altitude bands retuned for Sicily; every factor cited with a
  confidence; groups or keys the region lacks dropped and the doc says so. Altitude bands matter:
  the beech belt runs to about 1,900–2,000 m (Madonie, Nebrodi, Etna), the laricio belt on Etna to
  about 1,900 m, oaks from the coast to about 1,400 m.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). Several unmerged region branches add their own keys to this
  file (`region/calabria`, `region/campania`, `region/puglia`, `region/abruzzo`,
  `region/lombardia`, `region/friuli-venezia-giulia`, `region/trentino-alto-adige`): don't reuse a
  key any of them defines (check with `git show <branch>:api/src/api/config/species/references.yaml`).
  Put all of yours in **one block of their own, inserted right after the `zotti2008_checklist_liguria`
  entry** (before `altotronto_porcini2017`), with a comment header like Calabria's, so the branches
  merge cleanly: the others insert at the end of the file or before the Piemonte block. The
  regional mushroom law (Sicily's law on picking epigeous mushrooms, and its amendments, to verify)
  belongs in the doc.
- `sicilia/sanity.yaml`: press or blog contrasts for Sicily's areas (comuni) and years (Giornale di
  Sicilia, La Sicilia, MessinaToday, CataniaToday, PalermoToday, BlogSicilia, local Nebrodi and
  Madonie outlets, Funghi Magazine's national bulletins, the park authorities, mycological groups),
  reporting porcini (and ovoli or chanterelle, if any) seasons on the Nebrodi, Madonie, Etna,
  Peloritani, Ficuzza and Sicani, written before any Sicily score exists, in the same format as
  the other regions'. Every `comune` must be an ISTAT 2025 comune name inside Sicily (Misiliscemi
  was formed in 2021 from Trapani).
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Sicily's woodland from
the Regione Siciliana's **Carta forestale regionale** (SIF, Comando del Corpo Forestale, 1:10,000,
forest types after La Mantia et al. 2000–2001; `api/src/api/config/regions/sicilia.yaml`, written in
parallel). Only its class "31a boschi" (321,618 ha) counts as forest; the type codes (`CODCAMPO`)
map to habitats as follows, whole-map areas of 31a:

- `deciduous_oak` — QU2 thermophilous downy oak (33,473 ha), QU5 downy oak on siliceous soils
  (42,523), QU4 xerophilous downy oak on limestone (7,545), QU3 mesoxerophilous downy oak (4,064),
  QU1 sessile oak (529); CE2 montane Turkey oak (16,413), CE1 thermophilous *Q. gussonei* Turkey
  oak (8,850)
- `evergreen_oak` — LE1–LE4 holm oak (24,239 ha: pioneer rock, thermo-Mediterranean coastal and
  Iblean *cave*, xerophilous meso-Mediterranean, mesoxerophilous with holly); SU1 coastal cork oak
  (7,731), SU2 inland cork oak (11,297), SU3 cork oak on the Iblean volcanites (2,436)
- `beech` — FA1 mesophilous beech on siliceous soils (13,785 ha, Nebrodi), FA2 beech on Etna's
  lavas (1,168), FA3 and FA4 calcicolous beech (1,841, Madonie)
- `chestnut` — CA1 thermophilous (7,361 ha), CA2 montane mesophilous (4,518)
- `mountain_pine` — PL1–PL3 laricio pine (3,681 ha, Etna), RI4 montane conifer reforestation
  (7,197: black pine, laricio, cedar)
- `mediterranean_pine` — RI3 Mediterranean conifer reforestation (53,315 ha: Aleppo pine, stone
  pine, maritime pine, cypress), PM1 Aleppo pine of the south-east (374), PM2 maritime pine of
  Pantelleria (345), PM3 stone pine (164), PM4 naturalised Mediterranean pines (796)
- `exotic_broadleaf` — RI1 eucalyptus reforestation (38,818 ha), BS5 robinia, BS6 ailanthus, BS7
  other aliens (1,390)
- `mixed_broadleaf` — RI2 broadleaf reforestation (8,158 ha), BA1 other native broadleaves
  (4,256), BS1 Etna birch (352), BS2 aspen, BS3 manna ash, BS4 field elm, OS1–OS2 hop-hornbeam
- `riparian` — FR1 oriental plane, FR2 poplar and willow, FR3 shrub willows, FR4 tamarisk and
  oleander, FR5 narrow-leaved ash (14,059 ha)
- `macchia` — MM0–MM9 (126,665 ha of the shrubland class: oleaster and *Euphorbia dendroides*,
  *Calicotome*, *Spartium*, carbonate and siliceous macchia-gariga, dwarf palm, rosaceous scrub)
- `transitional_woodland_shrub` — AS1–AS5 montane scrub (39,257 ha: *Genista aetnensis* on Etna,
  broom, *Erica arborea* of the Peloritani, holly stands, rosaceous scrub), sparse woods (31b,
  12,752 ha) and temporarily unstocked woods (31c, 8,896 ha)
- Left out: wood plantations (arboricoltura da legno, 6,823 ha), grassland and pasture.

The build will give each habitat's median elevation and dominant cells; the parent session will
send them. Say in the doc which habitat holds which Sicilian tree.

Do not commit and do not edit any plan card.
