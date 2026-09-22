---
title: Deploy pipeline for the API, runnable as a gavin tool
status: Done
priority: medium
complexity: simple
---
Traces to PRD → Architecture (Backend on the Hetzner server) and the README → Deploying section written with the mappafunghi.app deploy card.

Pushing to `main` redeploys the web app on Vercel but not the API: the server only changes when someone SSHes in, pulls and rebuilds. One script does that whole path from the laptop, and a gavin tool runs it from the app.

- [x] `deploy/deploy-api.sh`: refuse unless on a clean `main` that matches `origin/main` (the server pulls from GitHub); run the API lint and tests; on the server `git pull --ff-only`, sync the systemd units when they changed, `docker compose up -d --build`, prune old images; wait for `/health`, print `/status` and the deployed commit. Flags: `--skip-tests`, `--run-job`
- [x] Verify it: `bash -n`/shellcheck, the refusal paths, and one real run against production (same commit, so a no-op rebuild)
- [x] Save it as a workspace gavin tool (`script` kind) with its flags as parameters
- [x] README → Deploying: ship an API change with the script

Done 2026-09-22. First real run (`ed36b61`): checks passed, the server pulled and rebuilt from cache
with no restart, and five live routes answered 200, in 50 s. The gavin tool is **Deploy API**
(`tool-258e375532a261d4a9934e76b0b118b9`, params `tests`, `run_job`).
