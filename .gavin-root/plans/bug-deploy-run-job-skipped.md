---
kind: task
title: [bug] deploy-api.sh --run-job never runs the job, and still exits 0
status: In Progress
priority: high
complexity: simple
---
Seen on both API deploys of 2026-09-29 (`deploy/deploy-api.sh --skip-tests` and `--skip-tests --run-job`, both deploying 15039d2): the output goes from `waiting for redis` straight to `==> Waiting for https://api.mappafunghi.app/health`. `redis ok`, `running the daily job now` and the `systemctl list-timers` line never print, the job never starts, and the script ends with `==> Deployed …` and exit 0. The closing `/status` check then warns that the scores predate the deployed rules and says to "rerun with --run-job", which does nothing again. The job had to be started by hand (`systemctl start mushma-daily.service` over ssh).

Cause: the server half of the script runs as `ssh … bash -s -- "$sha" "$RUN_JOB" <<'REMOTE'`, so bash reads the rest of that script from stdin as it goes. Line 100, `until docker compose exec -T redis redis-cli ping …`, reads stdin too: `-T` only turns off the TTY, and `docker compose exec` keeps stdin attached. The first ping drains the rest of the heredoc, so bash reaches EOF right after the loop and exits 0. Everything below it is skipped: the `REDIS_URL` check, the `--run-job` block and the timer line. The `docker compose exec -T api python - <<'PY'` step is safe, since its stdin is its own heredoc.

Since when: the Redis wait came in with da65dd2 (2026-09-28, "fix(deploy): wait for Redis before smoke tests and the daily job"). Every `--run-job` since then has been a no-op, including `deploy/rsync-region-data.sh <region> --redeploy --run-job`, which `exec`s `deploy-api.sh`. Regions onboarded since then were never re-scored on the server, and the national `/regions`, `/overview` and `/overview/trend` kept listing only the regions of the last 03:00 UTC run (Lazio, Sicilia and Valle d'Aosta were missing from the hub on 2026-09-29).

Fix:
1. Give the ping its own stdin: `docker compose exec -T redis redis-cli ping </dev/null`. Check the rest of the REMOTE block for any other command that reads stdin without a heredoc of its own (`docker compose exec`, `docker run -i`, `ssh`, `read`) and redirect it the same way.
2. Make a cut-short remote script fail instead of passing: end the REMOTE block with a sentinel line (e.g. `echo "remote: done"`) and have the local side die unless it saw it.
3. Check it on a real deploy: `deploy/deploy-api.sh --skip-tests --run-job` must print `redis ok`, `running the daily job now`, the job's events and the timer line, and the closing `/status` must show the deployed rules version.
4. Update the README's Deploying section if the output it describes changes.
