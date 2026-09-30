---
kind: task
title: [region] Lombardia — species research and rules
parent: region-lombardia.md
complexity: complex
---
Species research for Lombardia (child of `region-lombardia.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-2`, branch `region/lombardia`). API id
`lombardia`, ISTAT COD_REG 3. Alpine and prealpine valleys (Valtellina, Valchiavenna, Val
Camonica, the Orobie, Valsassina, Val Brembana/Seriana, Alto Garda bresciano), chestnut on the
lake slopes (Lario, Verbano/Varesotto, Iseo, Garda), the Oltrepò Pavese Apennine, little forest in
the Po plain. Unlike the regions done so far, Lombardia has large spruce, larch, fir and Scots-pine
forests up to the treeline (~2,000 m and more), so the altitude bands and conifer affinities matter.

Deliver:
- `.gavin-root/docs/species-ecology/lombardia.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/marche.md` and
  `species-ecology/emilia_romagna.md`.
- `api/src/api/config/species/lombardia/` started from `tuscany/` (look at `emilia_romagna/`,
  `liguria/`, `marche/`, `umbria/` for how other regions retuned): per-species YAML with season
  windows, habitat affinities and altitude bands retuned for Lombardia; every factor cited with a
  confidence; groups or keys the region lacks dropped and the doc says so.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite).
- `lombardia/sanity.yaml`: press or blog contrasts for Lombardia's areas (comuni) and years,
  written before any Lombardia score exists, in the same format as the other regions'.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid will map Lombardia's forest
types (spruce and fir → `fir_spruce`, larch and stone pine → `other_conifer`, Scots and mountain
pine → `mountain_pine`, beech, chestnut, oaks, hop-hornbeam → `mixed_broadleaf`, robinia →
`exotic_broadleaf`); check `api/src/api/config/regions/lombardia.yaml` once it exists for the
final mapping, and say in the doc which habitat holds which Lombard tree.

Do not commit and do not edit any plan card.
