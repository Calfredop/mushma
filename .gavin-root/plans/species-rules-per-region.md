---
kind: task
title: [foundation] Species rules per region
parent: feat-full-italy-coverage.md
complexity: moderate
---
Rules become per region. Context: `api/src/api/config/species/` (README, six rule
files, `references.yaml`), `api/src/api/model/{rules,config,sanity,backtest,tuning,
pipeline}.py`, `api/src/api/config/model.yaml`, `.gavin-root/docs/species-ecology.md`.
Decisions in the parent plan `feat-full-italy-coverage.md`.

- Layout: `config/species/<region>/<key>.yaml`; Tuscany's six files move to
  `config/species/tuscany/`. `references.yaml`, `README.md` and `model.yaml` stay
  shared. `load_rules(region)` loads one region's set; every caller (live repository,
  pipeline, backtest, tuning, sanity, history plausible) passes its region.
- A region's set may omit a group (no ovoli in an Alpine region): the groups in
  `model.yaml` list the keys, the region's files say which exist, and the API's
  species list follows.
- `precipitation_scale` (fitted on Tuscan gauges) becomes overridable per region in a
  `model:` block of the region YAML; national values by default.
- Sanity contrasts move from Python constants in `sanity.py` to
  `config/species/<region>/sanity.yaml` (areas by comuni or provinces, windows,
  source URL); Tuscany's are ported as they are and `sanity.py` reads YAML.
- Tests parametrized over every region directory: files validate, variables exist,
  references resolve; a Tuscany score for a test window is unchanged after the move.
- The species README documents the layout and how a region card starts from
  Tuscany's files.

Done when: pytest and ruff green, Tuscany scores unchanged, the sanity check runs
from YAML with today's result.

Done (2026-09-24): Species rules live under `config/species/<region>/` (Tuscany moved
intact); `load_rules(region)` + callers updated; `precipitation_scale` overridable via
`model:` on the region YAML; sanity contrasts in `tuscany/sanity.yaml` (6/11 hold on
local scores). pytest 802 passed, ruff clean; Tuscany species SHA and wet-score freeze
unchanged. Parent checklist left for the parent agent.

Done (2026-09-24): rules under `species/tuscany/`; `load_rules(region)` wired through
callers; sanity from YAML; README documents the layout; model+grid pytest green.
