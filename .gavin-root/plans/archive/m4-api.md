---
order: 8
title: M4 · API + daily pipeline in production
status: Done
priority: high
complexity: moderate
---
Traces to PRD → Architecture (Backend, Areas), Features 1–4, Principles (Sightings privacy), Constraints (freshness, mobile performance), Open questions (grid delivery format), Milestone 4.
Depends on: M4 API contract + fixtures (the schema and its tests) and M3 Model v1 (the data).

The frontend never computes the model; it only reads from here. Every route must keep passing the contract's schema tests.

- [x] Decide how to deliver the grid to the map (vector tiles, compact JSON/binary grid, or raster PNG): prototype payload size and render speed for ~12k cells against the ~1 MB compressed budget; record the choice in the PRD
- [x] `GET /scores?species&date` returns the whole-region grid in the chosen format (species = one or combined)
- [x] `GET /spot?lat&lon&date` and `/cells/{id}` return per-species score, a 7-day outlook and the factor breakdown
- [x] `GET /hotspots?species&date` returns clusters of adjacent high-scoring cells, labelled by comune and nearest named place, plus sighting counts per cell nearby
- [x] `GET /sightings?species&since` returns sighting counts per cell (never coordinates) with source and license
- [x] Replace fixture mode with real storage behind the same routes; the contract tests pass against real data
- [x] CORS for the Vercel domains; cache headers (past dates immutable, today and forecast short-lived)
- [x] Scheduled daily job on Fly/Railway, finishing before 07:00 Europe/Rome: ingest weather and sightings → score past few days to +7 → store; structured logs and failure alerting
- [ ] Production deploy; verify the job ran and today's scores are served
