---
order: 1024
title: M3 · Model v1: species rules, scoring, backtest
status: In Progress
priority: high
complexity: complex
---
Traces to PRD → Species (v1), Model (Factors, Score semantics, Validation), Principles (explainable), Milestone 3.
Depends on: all three M2 cards (grid, weather, sightings) and M3 Species ecology research (the rules and draft config).

Rules are data with a cited source each, and every score returns its factor breakdown (AGENTS.md). Write tests first for the engine and every factor.

- [x] Rule config schema: factors (rain windows, cumulative rain, soil/air temp bands, soil moisture, drying via wind/ET0/VPD, cold nights via Tmin), season windows, habitats, altitude bands, weights, plus `source` and `confidence` per rule. The loader validates it and fails on any rule without a source.
- [x] Scoring engine: cell × species × day → score 0–1 plus an ordered factor breakdown (value, contribution, i18n key)
- [x] Encode the rules from `.gavin-root/docs/species-ecology.md` into the config, one file per species (porcini split by sub-species)
- [x] Define the combined score (PRD default: max across species in season) and expose it as its own species key
- [x] Pipeline step: score every woodland cell for a date range and store the results
- [x] Backtest harness: fix the train / hold-out season split first, then join past scores to sightings and compute lift and AUC per species and season against a habitat-only baseline, with corrections for sampling bias
- [ ] First validation report in `.gavin-root/docs/model-v1-validation.md`
- [ ] Tune thresholds and weights on the train seasons only; report hold-out separately; set accuracy targets in the PRD
- [ ] Sanity check known areas (Garfagnana, Casentino, Amiata, Mugello, Lunigiana) across a few seasons remembered as wet/good and dry/bad
