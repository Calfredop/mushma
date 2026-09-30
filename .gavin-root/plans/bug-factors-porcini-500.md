---
kind: task
title: [bug] /factors must not 500 when a porcini leaf has no factor rows
status: To Do
priority: low
complexity: moderate
---
On 2026-09-29, from the 03:00 UTC daily run until a manual re-score at 12:41-12:54 UTC, `GET https://api.mappafunghi.app/factors?species=porcini&date=2026-09-29&region=puglia` returned 500 (plain `Internal Server Error`), for `date=2026-10-05` too. Analysis mode for porcini was broken in those regions.

- porcini 500 in `abruzzo`, `calabria` and `puglia` only; 200 in the other ten served regions. ovoli and gallinacci 200 everywhere.
- After the re-score (deployed 15039d2, every region re-scored) all three return 200. It no longer reproduces.
- It never reproduced on the local stores either (`api/data/scores/<region>`, scored 2026-09-28): `LiveRepository(Path("data"), region=r).get_factors("porcini", date(2026, 9, 29))` succeeds for all of them.

The cause is not known, and the stores that failed were overwritten by the re-score. Two candidates:
- The 03:00 run wrote an incomplete factors tier for some porcini leaf keys in those regions (a partial or failed write).
- Stores written by one version of the code were read by another. The 03:00 run's code and the code serving at 11:30 are not recorded anywhere we can see. The only reader change between main's 2026-09-28 state and ce32536 was a group filter in `_forecast`. `rules_version` can't settle this: it hashes the shared `references.yaml`, so it changes for every region whenever any region adds a reference.

Likely the same failure as [bug-cell-forecast-500-puglia.md](bug-cell-forecast-500-puglia.md); do them together.

Steps:
1. Look for errors in the 2026-09-29 run of the daily job: `journalctl -u mushma-daily --since "2026-09-29 04:50" --until "2026-09-29 05:20"` on the server (Europe/Rome times), especially abruzzo, calabria and puglia. The API container's own logs from before the redeploys that day are gone (`docker compose up` recreated it).
2. Test-first (AGENTS.md: TDD for model and data code): a live-repository test where the winners name a porcini leaf key whose factors tier has no rows for that day (or for some cells). Today this should 500 in `get_factors` → `winner_values` (`api/src/api/live/repository.py`); confirm that it does.
3. Make `get_factors` degrade instead: leave those cells' values null, or drop the cells, rather than raising. Keep the chips (the factor columns) unchanged.
4. If step 1 shows a partial write, have the daily job fail loudly (or retry) instead of leaving a store the API can't read.
5. Ship with `deploy/deploy-api.sh` and check the URL above. Until [bug-deploy-run-job-skipped.md](bug-deploy-run-job-skipped.md) is fixed, re-score by hand if the stores should be rewritten.
