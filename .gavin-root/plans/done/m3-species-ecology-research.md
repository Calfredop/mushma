---
order: 2
title: M3 · Species ecology research: cited rules per species
status: Done
priority: high
complexity: complex
---
Traces to PRD → Species (v1), Model (Factors, Score semantics, Known gaps), Principles (explainable).
Depends on: nothing. No code is needed, so this can start now, in parallel with M1. M3 Model v1 consumes the output.

Result (2026-09-17): `.gavin-root/docs/species-ecology.md` (synthesis, season cross-check, Open-Meteo mapping, habitat vocabulary, combined-score proposal, hand-offs), evidence appendices in `.gavin-root/docs/species-ecology/`, draft config + schema in `.gavin-root/docs/species-rules/`.

Turn foraging lore into rules an engine can encode, each with a source. Output: `.gavin-root/docs/species-ecology.md` plus a draft rule config (one file per species) that M3 will load. Prefer peer-reviewed phenology studies and Italian mycological societies (AMB, regional groups) over blogs, and mark each rule's confidence: strong / plausible / folklore.

- [x] [Porcini by sub-species (*B. aestivalis/reticulatus, B. aereus, B. edulis, B. pinophilus*): season windows in Tuscany, host trees, altitude bands, rain trigger (amount, lag), soil/air temperature bands, stoppers (drought, frost, drying wind), with sources](./porcini-by-sub-species-b-aestivalis-reticulatus-b-aereus-b-edulis-b-pinophilus-season-windows-in-tuscany-host-trees-altitude-bands-rain-trigger-amount-lag-soil-air-temperature-bands-stoppers-drought-frost-drying-wind-with-sources.md)
- [x] [Ovoli (*Amanita caesarea*): the same fields, with sources](./ovoli-amanita-caesarea-the-same-fields-with-sources.md)
- [x] [Gallinacci (*Cantharellus cibarius*): the same fields, with sources; note the soil-pH dependence we cannot model in v1](./gallinacci-cantharellus-cibarius-the-same-fields-with-sources-note-the-soil-ph-dependence-we-cannot-model-in-v1.md)
- [x] Cross-check season windows against GBIF monthly counts for Tuscany (a quick query, no pipeline needed)
- [x] Map every rule to a weather variable Open-Meteo actually provides (precipitation, Tmin/Tmax, soil temperature and moisture, wind, ET0/VPD) and to the habitat vocabulary the grid will carry; flag rules that need data we don't have
- [x] Draft the rule config skeleton (one file per species) with `source` and `confidence` fields, matching the schema M3 will validate
- [x] Propose the combined-score definition (e.g. max across species in season) for M3 to decide
