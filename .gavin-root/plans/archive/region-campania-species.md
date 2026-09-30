---
kind: task
title: [region] Campania — species research and rules
parent: region-campania.md
complexity: complex
---
Species research for Campania (child of `region-campania.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-2`, branch `region/campania`). API id
`campania`, ISTAT COD_REG 15. Southern Apennine and Tyrrhenian woodland, from sea level to about
1,900 m: beech from about 1,000 m up on the Matese (Letino, Gallo Matese, San Gregorio Matese,
Piedimonte Matese), the Monti Picentini (Monte Cervialto, Terminio, Accellica, the Laceno plateau:
Bagnoli Irpino, Acerno, Montella, Volturara Irpina, Serino, Calvanico, Giffoni Valle Piana,
Campagna, Senerchia, Calabritto), the Partenio (Summonte, Ospedaletto d'Alpinolo, Mercogliano), the
Taburno-Camposauro (Cautano, Tocco Caudio, Vitulano, Bonea; the planted silver fir of the Taburno),
the Monti Alburni (Petina, Sicignano degli Alburni, Sant'Angelo a Fasanella, Ottati) and the
Cilento's Monte Cervati, Gelbison and Motola (Sanza, Piaggine, Valle dell'Angelo, Novi Velia,
Laurino; relict silver fir); chestnut, the region's signature wood, in wide belts at 400–1,000 m
(Irpinia: Montella, Serino, Avellino's hills; the volcanic Roccamonfina: Roccamonfina, Sessa
Aurunca, Conca della Campania, Marzano Appio; the Monti Lattari: Agerola, Tramonti; the Cilento:
Roccadaspide, Castel San Lorenzo, Stio, Magliano Vetere; Ischia's Epomeo); Turkey oak, downy oak
and hop-hornbeam in the hills of the Sannio and Irpinia; holm oak and Mediterranean macchia on the
coast and the islands (Capri, Ischia, Cilento coast, Monti Lattari); stone and Aleppo pine on the
coast (Castel Volturno, Pineta di Patria, Paestum, Vesuvius) and black-pine reforestation inland.
Soils: volcanic ash (acid to neutral) over much of the chestnut belt and around Vesuvius, Campi
Flegrei and Roccamonfina; limestone on the Matese, Picentini, Alburni, Lattari and Taburno; flysch
and sandstone in the Cilento.

Deliver:
- `.gavin-root/docs/species-ecology/campania.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/marche.md` and
  `species-ecology/umbria.md` (the nearest regions done so far). Campania is the first southern
  region: say where the southern evidence departs from the central-Italian windows (earlier spring
  flushes, a summer drought gap, later autumn at low altitude, *B. aereus* commoner in chestnut).
- `api/src/api/config/species/campania/` started from `tuscany/` (look at `marche/`, `umbria/`,
  `emilia_romagna/`, `piemonte/`, `liguria/` for how other regions retuned): per-species YAML with
  season windows, habitat affinities and altitude bands retuned for Campania; every factor cited
  with a confidence; groups or keys the region lacks dropped and the doc says so. Altitude bands
  matter: woodland runs from the coast to 1,900 m, and the thermophilous keys (*aereus*,
  *aestivalis*, ovoli) climb higher in the south.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). The regional mushroom law (Campania's L.R. on picking
  epigeous mushrooms, L.R. 8/2007 and its amendments, to verify) belongs in the doc.
- `campania/sanity.yaml`: press or blog contrasts for Campania's areas (comuni) and years
  (Irpinian, Salerno, Cilento and Caserta local press report the porcini seasons of the Laceno,
  Terminio, Picentini, Matese and Cilento), written before any Campania score exists, in the same
  format as the other regions'. Every `comune` must be an ISTAT 2025 comune name inside Campania.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Campania's forest
types as `api/src/api/config/regions/campania.yaml` says (read it once it exists; the regional
source is being chosen in parallel and may be the regional land-use map or CLC IV, the
tree-to-habitat meaning is the same either way): beech → `beech`; Turkey oak, downy oak,
Hungarian oak (farnetto) → `deciduous_oak`; hop-hornbeam and other broadleaf (maples, ash, alder
Alnus cordata, the mixed mesophilous woods) → `mixed_broadleaf`; chestnut (coppice and orchards)
→ `chestnut`; holm oak and cork oak → `evergreen_oak`; poplar and willow → `riparian`; robinia and
ailanthus → `exotic_broadleaf`; black-pine reforestation (with some fir, Douglas fir) →
`mountain_pine`; stone pine, Aleppo and maritime pine → `mediterranean_pine`; silver fir →
`fir_spruce`; broadleaf with conifers → `mixed_broadleaf_conifer`; Mediterranean macchia →
`macchia`; broom and bramble scrub, regrowth on abandoned fields → `transitional_woodland_shrub`.
Say in the doc which habitat holds which Campania tree.

Do not commit and do not edit any plan card.
