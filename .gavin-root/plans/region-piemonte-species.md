---
kind: task
title: [region] Piemonte — species research and rules
parent: region-piemonte.md
complexity: complex
---
Species research for Piemonte (child of `region-piemonte.md`). Work in the region's checkout
(`mushma-regions-3`, branch `region/piemonte`).

Deliver:
- `.gavin-root/docs/species-ecology/piemonte.md`: the regional evidence (season windows, host trees and
  habitat affinities, altitude bands, weather rules where regional literature exists), each claim
  cited, with a confidence (`strong` / `plausible` / `folklore`, as in `species-ecology.md`).
- `api/src/api/config/species/piemonte/` started from `tuscany/`: per-species YAML with season windows,
  habitat affinities and altitude bands retuned for Piemonte; every factor cited with a confidence;
  groups the region lacks dropped and the doc says so.
- Regional references added to the shared `api/src/api/config/species/references.yaml`.
- `piemonte/sanity.yaml`: press or blog contrasts for Piemonte's areas (comuni) and years.
- `uv run pytest tests/model/test_rules.py` passes; `uv run ruff check .` clean.

Do not commit and do not edit any plan card.
