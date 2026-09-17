---
order: 1
title: M1 · Foundations: repo, tooling, CI, deploy skeletons
status: In Progress
priority: high
complexity: moderate
---
Traces to PRD → Milestones 1, Architecture, Constraints (cost), Open questions (storage).
Depends on: nothing. Every other card except the species research builds on this one.

- [x] `git init` and `.gitignore` (node, python, `.env`, `api/data/` and other local data caches). Create the GitHub repo and push.
- [x] Scaffold `web/`: Vite + React + TS (strict), pnpm, ESLint + Prettier, Vitest with a smoke test
- [x] Scaffold `api/`: uv project, FastAPI app with `GET /health`, Ruff, pytest with a smoke test
- [x] Pin runtimes: `.python-version` for uv, `.nvmrc` + `engines` for pnpm; CI uses the same versions
- [x] Decide storage for grid, scores and history (Postgres/PostGIS vs DuckDB/Parquet); estimate ~12k cells × 3 species × 365 days/year. Record the choice in the PRD and remove it from Open questions.
- [x] Choose Fly.io or Railway for the API. Railway has native cron jobs; Fly needs a scheduled Machine or supercronic. It must fit the chosen storage and the cost ceiling. Record it in the PRD.
- [ ] CI with GitHub Actions: lint + test for `web/` and `api/` on push and PR
- [x] Deploy skeletons: `web/` to Vercel, `api/` to Fly/Railway. The web app reads the API base URL from env.
- [x] Root README with dev commands for both apps
- [x] Replace the "planned" Layout section in AGENTS.md with the real layout and commands (CLAUDE.md and GEMINI.md import it)
- [x] Set `[worktree] setup` in `.gavin-root/config.toml` (e.g. `pnpm --dir web install`, `uv --directory api sync`)
