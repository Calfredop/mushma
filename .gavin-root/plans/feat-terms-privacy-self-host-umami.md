---
kind: task
title: Self-host Umami analytics on the Hetzner box
parent: feat-terms-and-conditions-privacy.md
complexity: moderate
---
Deploy self-hosted Umami on the production Hetzner server (`mushma-prod-01`), alongside the
existing API/Caddy stack in `deploy/`, so the frontend's consent-gated analytics (see the parent
Terms/Privacy card) has something real to point at.

- Add an `umami` service (+ its Postgres backing store, per Umami's *current* official Docker
  Compose recipe — check https://umami.is/docs/install for the current version, don't assume an
  old recipe) to `deploy/compose.yaml`, alongside `api` and `caddy`.
- Add a Caddy site block for `analytics.mappafunghi.app` (proposed subdomain, matching the
  `api.`/`tiles.` naming convention — confirm with Cosimo if he'd rather use a different name)
  reverse-proxying to the `umami` service, mirroring the existing `api.mappafunghi.app` block in
  `deploy/Caddyfile`.
- Add the DNS record for `analytics.mappafunghi.app` on Cloudflare, "DNS only" (unproxied),
  matching how `api.mappafunghi.app` is set up (README → Deploying) so Caddy can get its own Let's
  Encrypt certificate directly.
- Add Umami's required secrets (app secret, DB credentials) to `deploy/.env.example` and the
  server's real `deploy/.env`.
- Deploy: `cd /opt/mushma/deploy && docker compose up -d --build` on the server, then open
  `https://analytics.mappafunghi.app`, create the admin account, and add a website for
  `mappafunghi.app` to get its website ID and tracking script `src`.
- Document the new service in README → Deploying (the cost table and the `api/ → Hetzner`
  section), and hand the website ID + script `src` back for the frontend's
  `VITE_UMAMI_SRC`/`VITE_UMAMI_WEBSITE_ID` Vercel env vars (parent card).
- Confirm the Umami dashboard is reachable and receiving a real test pageview end-to-end before
  calling this done.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
