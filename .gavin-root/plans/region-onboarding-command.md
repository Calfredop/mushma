---
kind: task
title: [foundation] Region onboarding command and runbook
parent: feat-full-italy-coverage.md
complexity: moderate
---
One resumable command runs a region's whole data chain, so a region card is config,
research and this command. Depends on the other foundation cards of
`feat-full-italy-coverage.md`. Context: the CLIs in
`api/src/api/{grid,weather,sightings,model,history}/`, `api/src/api/jobs/daily.py`,
README.

- `uv run python -m api.regions.onboard <region> [--from STEP] [--only STEP]
  [--years 2016-2026]`: grid build → weather points → CDS history → Open-Meteo update
  → sightings fetch → score history (no factors) and the served window → history
  build (update + outlook) → backtest report → sanity check. Each step a child
  process as in the daily job, one JSON log line per step, skipped when its outputs
  exist, safe to re-run.
- Prints a summary (cells, woodland cells, INFC deviation, nodes, years stored,
  sightings kept, backtest AUCs per group, sanity contrasts passed) and writes it
  under a "Data" heading in `.gavin-root/docs/regions/<region>.md`, which the region
  card fills around.
- Honours `DATA_DIR`, so rails in worktrees share one data root and its raw caches.
- README → "Adding a region": the CDS key, the command, the rsync to the server, the
  deploy tool, what to check on the site afterwards. Save rsync + redeploy as a gavin
  tool the way `deploy-api-pipeline.md` did.
- Tests for step selection, resumption and the summary; `--only backtest` on Tuscany
  reproduces the current report numbers.

Done when: pytest and ruff green, the Tuscany dry run matches, the runbook reads top
to bottom.
