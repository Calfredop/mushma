---
kind: task
title: [region] Marche — species research and rules
parent: region-marche.md
complexity: complex
---
Species research for Marche (child of `region-marche.md`). Work in the region's checkout
(`mushma-regions-2`, branch `region/marche`).

Deliver:
- `.gavin-root/docs/species-ecology/marche.md`: the regional evidence (season windows, host trees and
  habitat affinities, altitude bands, weather rules where regional literature exists), each claim
  cited, with a confidence (`strong` / `plausible` / `folklore`, as in `species-ecology.md`).
- `api/src/api/config/species/marche/` started from `tuscany/`: per-species YAML with season windows,
  habitat affinities and altitude bands retuned for Marche; every factor cited with a confidence;
  groups the region lacks dropped and the doc says so.
- Regional references added to the shared `api/src/api/config/species/references.yaml`.
- `marche/sanity.yaml`: press or blog contrasts for Marche's areas (comuni) and years.
- `uv run pytest tests/model/test_rules.py` passes; `uv run ruff check .` clean.

Do not commit and do not edit any plan card.
