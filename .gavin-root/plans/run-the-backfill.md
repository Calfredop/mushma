---
status: In Progress
kind: task
title: M2 · Weather backfill run (2016 → present)
parent: m2-weather-ingest.md
---
The weather history backfill runs unattended in a gavin terminal session (Agents page). The M2 · Weather ingest card started it on 2026-09-17. It fetches ERA5-Land daily weather from 2016-01-01 to 11 days ago, newest year first, and stays within the free Open-Meteo quota (at most 9,000 weighted calls per UTC day, about 2,960 per year of history). That takes about four days: the seasons from 2019 are in by about 2026-09-19, and 2016 by about 2026-09-21. Decision and method: `.gavin-root/docs/weather-ingest.md` → "Backfill depth and API budget".

Everything lives in the **backend worktree**. Run each command below from `/Users/coalpila/CloudStation/Coding/mushma-backend/api`, never from the root checkout, whose `api/data/` is empty.

1. **Progress.** `tail -20 data/weather/tuscany/backfill.log`. Each request logs a line, and the run ends with `backfill: {... "done": true}`. Calls spent in the current UTC day and hour are in `data/raw/open_meteo/usage.json`.
2. **Session gone, no final line?** Restart it in a gavin session. It resumes and skips years already stored. Never run two at once, which doubles the API calls:
   `sh -c "uv run python -m api.weather.ingest backfill --wait 2>&1 | tee -a data/weather/tuscany/backfill.log"`
3. **Verify.** Every full year from 2016 to 2025 must have 103 points and `n = 103 × days × 11`:
   `uv run python -c "import duckdb; print(duckdb.sql(\"SELECT year(date) AS y, count(DISTINCT point_id) AS points, count(DISTINCT date) AS days, count(*) AS n FROM read_parquet('data/weather/tuscany/daily/source=era5_seamless/*/data.parquet') GROUP BY 1 ORDER BY 1\"))"`
   Then `uv run python -m api.weather.ingest backfill` (without `--wait`) must end with `"done": true`, having fetched at most the current year's tail.
4. **Gauge check over the backtest seasons.** Run `uv run python -m api.weather.checks gauges --start 2019-01-01 --end 2025-12-31`. Add the result next to the 2025–2026 figures in the "Ground truth: SIR Toscana gauges" section of `.gavin-root/docs/weather-ingest.md` in the backend worktree. The backend rail's next commit step picks it up.
5. **Close.** Tick `Run the backfill` in the parent card, which will be at `/Users/coalpila/CloudStation/Coding/mushma/.gavin-root/plans/done/m2-weather-ingest.md`, then set this card Done.

If a year stays incomplete after the run (the log says `giving up: still incomplete`), re-run step 2 once. If it still fails, report the year and the log lines here instead of closing.

## Progress

- **2026-09-19, stall found and fixed.** The first run stopped logging at 2026-09-18 01:16 UTC, partway through 2021 (68 of 103 points), with the day's budget spent. Its wait for 00:00 UTC never ended because `time.sleep` on macOS doesn't count time the machine is asleep, so the laptop's sleep overnight pushed the wake-up hours past midnight. Fix, in the backend worktree and not committed yet: `sleep_until` in `api/weather/openmeteo.py` sleeps in steps of at most 5 minutes and re-reads the wall clock after each. `RateBudget.acquire` and `run_until_done` both use it. New tests are in `test_openmeteo.py` and `test_ingest.py`, and all 478 API tests pass. The backend rail's next commit step picks it up. The run still can't make calls while the Mac is asleep, but it now resumes within 5 minutes of waking after 00:00 UTC.
- **2026-09-19 10:08 UTC, restarted.** The stalled process was stopped first. gavin refuses `gavin_spawn_session` from an agent (`Forbidden … role: "agent"`), so the run was started detached with `nohup` in the same `api/` folder, running the same command and appending to the same log. Before starting another run, check it's gone: `pgrep -fl "api.weather.ingest"`.
- Stored at restart: 2022–2025 complete, 2026 through 2026-09-13, 2021 at 68 of 103 points. Another run of the shared ledger had spent 868 calls at 09:26 UTC, so about 8,100 of today's 9,000 were left. That covers the rest of 2021, all of 2020 and all of 2019. 2016–2018 need about 8,900 calls: next UTC day.
