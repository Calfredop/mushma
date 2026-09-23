---
kind: task
title: [bug] Spot and cell forecasts 500 between midnight and the daily job
status: In Progress
priority: high
complexity: simple
---
Seen live on 2026-09-24 at 00:08 Europe/Rome: `GET https://api.mappafunghi.app/cells/1kmE4393N2265` and `GET /spot?lat=43.465&lon=10.954` both returned 500 and the app's spot panel said "Non riesco a caricare la previsione per questo punto". `/status` reported `scored_through: 2026-09-30` (from the 2026-09-23 run), and `/scores` and `/hotspots` were fine.

Cause (read, not yet reproduced in a test): `LiveRepository._forecast` in `api/src/api/live/repository.py` asks for today..today+7 and raises `RuntimeError("incomplete … outlook")` when fewer than 8 days are stored. After midnight in Rome, today+7 isn't scored until the 05:00 daily job runs, so every spot and cell detail fails for about five hours each night. The same thing happens all day if a daily run fails.

Fix it test-first (AGENTS.md: TDD for model and data code): a live-repository test where the store ends at today+6 should still return a forecast. Decide whether to return the days that are stored (the web `SpotPanel` must then handle fewer than 8 bars) or a clear non-500 error the UI can explain. Keep the `why` breakdown per day unchanged. Then ship with `deploy/deploy-api.sh`.
