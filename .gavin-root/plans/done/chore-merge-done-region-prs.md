---
title: [chore] Merge the done region PRs (#6–#12) onto main
status: Done
priority: high
---
Seven region cards are Done but their PRs never reached main: #6 Trentino-Alto Adige, #7 Lombardia, #8 Friuli-Venezia Giulia, #9 Campania, #10 Abruzzo, #11 Calabria, #12 Puglia. Their rails were dropped from the orchestration, so nothing merged them. Land them the way #1–#5 landed: local merge commits "Merge region/<slug> (#N): <Name>" pushed to main.

`merge/region-prs-6-9` (local, never pushed) already holds #6–#9 merged over origin/main 831165d; build on it after reviewing its conflict resolutions.

- [x] Remove the stale model-v1 rail (worktree gone, branch already merged)
- [x] Review the conflict resolutions in `merge/region-prs-6-9`
- [x] Merge #10 Abruzzo, #11 Calabria and #12 Puglia on top, resolving the shared registry files (regions/index.ts, credits.ts, sources.yaml, references.yaml)
- [x] API checks green: pytest, ruff check, ruff format --check
- [x] Web checks green: lint, format:check, vitest, build
- [x] Push to main; PRs #6–#12 show merged
- [x] Hand the deploy ("Deploy pulled main") and the running Lazio/Sicilia rails' follow-up to the human

Landed 2026-09-28 as 430f971 (fast-forward of origin/main from 831165d); CI green on main; PRs #6–#12 show merged.
Only real code conflict: Lombardia and Abruzzo both fixed ArcGIS paging for capped servers (`offset += len(features)`); kept Lombardia's version and its stricter test.
The web redeploys on Vercel by itself; the API still needs "Deploy pulled main" (all seven regions' stores were rsync'd per their region docs).
