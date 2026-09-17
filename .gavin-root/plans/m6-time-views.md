---
order: 10
title: M6 · Time views: historical replay + seasonal outlook
status: To Do
priority: medium
complexity: complex
---
Traces to PRD → Features 5 (seasonal outlook) and 6 (historical analysis), Principles (honest uncertainty), Milestone 6.
Depends on: M5 Frontend core, and the backfilled history from M2 Weather ingest and M3 Model v1.

- [ ] Pipeline: pre-aggregate season stats per species and comune (score-days above threshold, rain and temperature vs normal, sightings count)
- [ ] Climatology baselines (daily normals per weather point) from the backfilled history
- [ ] Seasonal forecast ingest (e.g. Open-Meteo Seasonal API) mapped to the same variables
- [ ] API: `GET /history/seasons`, `GET /history/season/{year}?species`, `GET /outlook?species&comune`, added to the OpenAPI contract with fixtures
- [ ] UI historical replay: pick a past date or season → map plus the sightings from that time
- [ ] UI season comparison: which years were good per species and comune, and which conditions drove them
- [ ] UI seasonal outlook: likely upcoming windows, clearly styled and worded as an outlook rather than a forecast
- [ ] i18n for all new copy; tests for the aggregation logic
