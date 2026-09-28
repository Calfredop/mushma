---
order: 15360
kind: note
labels: memory
title: `api.regions.onboard` needs the region's species rules even for its early steps
status: To Do
---
While a region's species research is still running, run the early onboarding steps' own commands (`api.weather.ingest points|backfill --source cds|update --region <r>`, `api.sightings.ingest fetch --region <r>`) instead of `api.regions.onboard <r> --only …`, which refuses to start until `config/species/<r>/` exists.

Why: `step_specs` loads the rules to plan the score step, so even `--only points` fails with "no species rules for region" (Puglia lane, 2026-09-28).
