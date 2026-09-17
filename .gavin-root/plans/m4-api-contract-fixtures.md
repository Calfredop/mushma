---
order: 3
title: M4 · API contract + fixtures
status: To Do
priority: high
complexity: moderate
---
Traces to PRD → Architecture (Backend, API contract first, Areas), Features 1–4, Principles (Sightings privacy, Honest uncertainty), Milestone 4.
Depends on: M1 Foundations. Unblocks M5 Frontend core, so the web app is built in parallel with M2/M3 instead of after the whole data layer.

Lock the shape of the API before the data exists.

- [ ] OpenAPI schema for `GET /scores`, `GET /spot`, `GET /cells/{id}`, `GET /hotspots`, `GET /sightings`, with response models: score (0–1 index), ordered factor breakdown (key, value, contribution, i18n key), hotspot (cluster of cells + comune + place label), sighting counts per cell (never exact coordinates)
- [ ] Fixture data: a few dozen realistic cells across Tuscany × a 14-day window × 3 species, hand-shaped so the map, spot panel, why breakdown and hotspots all have something to show
- [ ] Fixture mode in the FastAPI app (`MUSHMA_FIXTURES=1`) serving those files through the real routes, so `web/` runs without a database
- [ ] Generate the TypeScript client from the OpenAPI schema into `web/`, with a CI check that it is up to date
- [ ] Schema tests that every endpoint must pass, in fixture mode now and against the real implementation once M4 lands
