---
order: 2
title: M3 · Species ecology research: cited rules per species
status: To Do
priority: high
complexity: complex
---
Traces to PRD → Species (v1), Model (Factors, Score semantics, Known gaps), Principles (explainable).
Depends on: nothing. No code is needed, so this can start now, in parallel with M1. M3 Model v1 consumes the output.

Turn foraging lore into rules an engine can encode, each with a source. Output: `.gavin-root/docs/species-ecology.md` plus a draft rule config (one file per species) that M3 will load. Prefer peer-reviewed phenology studies and Italian mycological societies (AMB, regional groups) over blogs, and mark each rule's confidence: strong / plausible / folklore.

- [ ] Porcini by sub-species (*B. aestivalis/reticulatus, B. aereus, B. edulis, B. pinophilus*): season windows in Tuscany, host trees, altitude bands, rain trigger (amount, lag), soil/air temperature bands, stoppers (drought, frost, drying wind), with sources
- [ ] Ovoli (*Amanita caesarea*): the same fields, with sources
- [ ] Gallinacci (*Cantharellus cibarius*): the same fields, with sources; note the soil-pH dependence we cannot model in v1
- [ ] Cross-check season windows against GBIF monthly counts for Tuscany (a quick query, no pipeline needed)
- [ ] Map every rule to a weather variable Open-Meteo actually provides (precipitation, Tmin/Tmax, soil temperature and moisture, wind, ET0/VPD) and to the habitat vocabulary the grid will carry; flag rules that need data we don't have
- [ ] Draft the rule config skeleton (one file per species) with `source` and `confidence` fields, matching the schema M3 will validate
- [ ] Propose the combined-score definition (e.g. max across species in season) for M3 to decide
