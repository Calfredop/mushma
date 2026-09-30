---
title: Production deploy to mappafunghi.app
status: Done
priority: high
complexity: moderate
---
Traces to PRD → Architecture (Frontend, Backend, Basemap), Constraints (cost, freshness), Milestone 7 (production deploy) and the open last item of M4 · API ("Production deploy; verify the job ran and today's scores are served").

Free tiers everywhere except the API box: a new Hetzner CX23 in Falkenstein (~€7.31/month incl. VAT). The grimoria.app test server was ruled out on 2026-09-22: 0% CPU idle and swap 85% full before mushma. Fly is dropped: a Fly volume attaches to one machine only, so the scheduled job machine could never share its scores with the API machine.

- [x] DNS: mappafunghi.app zone on Cloudflare (Free), nameservers moved from Namecheap
- [x] Tiles: R2 bucket `mushma-tiles` with both PMTiles extracts; Protomaps Worker on `tiles.mappafunghi.app`
- [x] API: new CX23 (Docker CE image), API + Caddy from `deploy/compose.yaml` at `api.mappafunghi.app`, data copied from the local stores
- [x] Daily job: systemd timer 05:00 Europe/Rome; first run verified
- [x] Web: Vercel project (root `web`), env vars, `mappafunghi.app` + `www` redirect
- [x] Deploy files committed under `deploy/`; README Deploying section and PRD Architecture updated from Fly
- [x] End-to-end check on the live domain: today's scores, tiles, spot forecast

Done 2026-09-22. First daily run on the server: 120 s, all six steps ok, scores through 2026-09-29.
Monitoring (healthchecks.io heartbeat, uptime pinger, alert webhook, Sentry) is left for later:
the URLs go in `/opt/mushma/deploy/.env` on the server (README → Monitoring).
