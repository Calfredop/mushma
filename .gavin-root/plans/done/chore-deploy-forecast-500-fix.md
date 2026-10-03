---
kind: task
title: [chore] Deploy the forecast/factors 500 fix and check every region
status: Done
priority: medium
complexity: simple
---
The fix for [bug-cell-forecast-500-puglia.md](done/bug-cell-forecast-500-puglia.md) and [bug-factors-porcini-500.md](done/bug-factors-porcini-500.md) (commit "fix(api): serve the cell forecast and factors when a factor row is missing or out of range") is on branch `backlog/2026-09-30`. It reaches production only after the Backlog rail's PR is merged, because `deploy/deploy-api.sh` deploys only a clean, pushed `main`.

1. After the PR is merged: put the root checkout on `main`, pull, and run the "Deploy pulled main" tool (tests yes, run_job no), or `deploy/deploy-api.sh`.
2. Run `uv run --project api python deploy/check-live-cells.py 10`. It checks every served region's `/factors` per species, then 10 random `/cells/{id}` per region, at about one request a second so the rate limiter doesn't answer 429. Expect "0 not 200".
3. If a region reports days without a breakdown, the store has a winner whose factor row is missing or out of range. Find the reason in the API logs: `docker compose logs api | grep "no breakdown from\|served as null"` on the server (in /opt/mushma/deploy). File a bug card with what they show.

A pre-deploy run of the same script (2026-09-30, on the old code) is recorded on bug-cell-forecast-500-puglia.md.

## Outcome (2026-10-02)

- **Deploy: nothing to do.** The fix (`a7208fa`) reached `origin/main` through the merge of `backlog/2026-09-30` (`de9e525`), and the server checkout in `/opt/mushma` was already on `0beb997`, which contains it. The API container had been rebuilt at 12:54 UTC the same day (the libexpat deploy). No redeploy was run. The unpushed local commit `03ef252` (ssh keepalive in `deploy/deploy-api.sh`) is not on the server, and it does not touch the API code.
- **Live check** (`uv run --project api python deploy/check-live-cells.py 10`, ~13:00 UTC): 259 requests across 20 regions, **0 not 200**, and 0 forecast days without a breakdown in every region.
- **API logs** (`docker compose logs api | grep "no breakdown from\|served as null"` in `/opt/mushma/deploy`): 0 lines. The container was only a few minutes old, so this covers the check's own requests, not a full day of traffic. The 05:00 daily job writes new stores, so a rerun of the check after tomorrow's job would cover them.
- No bug card needed.
