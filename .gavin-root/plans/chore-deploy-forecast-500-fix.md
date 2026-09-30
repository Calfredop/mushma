---
kind: task
title: [chore] Deploy the forecast/factors 500 fix and check every region
status: To Do
priority: medium
complexity: simple
---
The fix for [bug-cell-forecast-500-puglia.md](done/bug-cell-forecast-500-puglia.md) and [bug-factors-porcini-500.md](done/bug-factors-porcini-500.md) (commit "fix(api): serve the cell forecast and factors when a factor row is missing or out of range") is on branch `backlog/2026-09-30`. It reaches production only after the Backlog rail's PR is merged, because `deploy/deploy-api.sh` deploys only a clean, pushed `main`.

1. After the PR is merged: put the root checkout on `main`, pull, and run the "Deploy pulled main" tool (tests yes, run_job no), or `deploy/deploy-api.sh`.
2. Run `uv run --project api python deploy/check-live-cells.py 10`. It checks every served region's `/factors` per species, then 10 random `/cells/{id}` per region, at about one request a second so the rate limiter doesn't answer 429. Expect "0 not 200".
3. If a region reports days without a breakdown, the store has a winner whose factor row is missing or out of range. Find the reason in the API logs: `docker compose logs api | grep "no breakdown from\|served as null"` on the server (in /opt/mushma/deploy). File a bug card with what they show.

A pre-deploy run of the same script (2026-09-30, on the old code) is recorded on bug-cell-forecast-500-puglia.md.
