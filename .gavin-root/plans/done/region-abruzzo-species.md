---
kind: task
title: [region] Abruzzo — species research and rules
parent: region-abruzzo.md
complexity: complex
---
Species research for Abruzzo (child of `region-abruzzo.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-3`, branch `region/abruzzo`). API id
`abruzzo`, ISTAT COD_REG 13. The highest Apennine woodland: beech from about 900 m up to the
treeline at 1,800–1,900 m on the Gran Sasso, the Majella, the Sirente-Velino and in the Parco
Nazionale d'Abruzzo, Lazio e Molise (Pescasseroli, Opi, Villetta Barrea, Val Fondillo); the
siliceous sandstone of the Monti della Laga (Teramo side: Valle Castellana, Cortino, Crognaleto,
Rocca Santa Maria) with chestnut, Turkey oak, beech and the silver fir of Martese; the Alto
Sangro and the Altopiano delle Cinquemiglia (Roccaraso, Pescocostanzo, Bosco di Sant'Antonio);
the Valle Roveto and Marsica; the Alto Vastese (Castiglione Messer Marino, Rosello's silver fir);
downy oak, Turkey oak and hop-hornbeam in the hills; black-pine reforestation on the limestone
slopes. Most of the region is limestone; the Laga is the acid exception.

Deliver:
- `.gavin-root/docs/species-ecology/abruzzo.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/marche.md` and
  `species-ecology/umbria.md` (the nearest regions done so far).
- `api/src/api/config/species/abruzzo/` started from `tuscany/` (look at `marche/`, `umbria/`,
  `emilia_romagna/`, `piemonte/` for how other regions retuned): per-species YAML with season
  windows, habitat affinities and altitude bands retuned for Abruzzo; every factor cited with a
  confidence; groups or keys the region lacks dropped and the doc says so. Altitude bands matter
  here more than anywhere done so far: woodland reaches 1,900 m.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). The regional mushroom law (the current Abruzzo L.R. on
  picking epigeous mushrooms) belongs in the doc.
- `abruzzo/sanity.yaml`: press or blog contrasts for Abruzzo's areas (comuni) and years, written
  before any Abruzzo score exists, in the same format as the other regions'. Marche's
  `sanity.yaml` already reads a forager blog about the Teramo side of the Laga onto Marche comuni;
  here those contrasts belong to their own Abruzzo comuni. Every `comune` must be an ISTAT 2025
  comune name inside Abruzzo.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid maps Abruzzo's forest
types as `api/src/api/config/regions/abruzzo.yaml` says (read it; it may be the regional
Carta Tipologico-Forestale or CLC IV, the tree-to-habitat meaning is the same either way):
beech → `beech`; downy oak and Turkey oak → `deciduous_oak`; hop-hornbeam and other broadleaf
(maples, ash, invasive broadleaf on abandoned fields) → `mixed_broadleaf`; chestnut →
`chestnut`; holm oak → `evergreen_oak`; poplar and willow → `riparian`; robinia and ailanthus →
`exotic_broadleaf`; black-pine reforestation (with some fir, larch, Douglas fir above 900 m) and
the natural black pine of Villetta Barrea → `mountain_pine`; Aleppo-pine reforestation →
`mediterranean_pine`; beech with silver fir → `mixed_broadleaf_conifer`; juniper and
Mediterranean shrub → `macchia`; broom, rose and bramble scrub and the badland scrub →
`transitional_woodland_shrub`. Say in the doc which habitat holds which Abruzzo tree.

Do not commit and do not edit any plan card.
