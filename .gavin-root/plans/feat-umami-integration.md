---
complexity: moderate
order: 8192
kind: plan
title: [feat] umami integration
status: To Do
---
Self-hosted Umami analytics for mappafunghi.app, to see how the group and portfolio
visitors use the app. Traces to PRD → Architecture (backend on the Hetzner box, under
€10/month) and Principles → Sightings privacy.

**Decided (don't re-litigate):**
- Self-hosted on the Hetzner CX23: Umami + Postgres in `deploy/compose.yaml`, behind
  Caddy at `m.mappafunghi.app` ("DNS only" on Cloudflare, like `api.`).
- No cookies, so no consent banner. Tracks pageviews (`/`, `/credits`) and these events:
  species and view (Now/Seasons/Outlook) switches; spot opened, with its method (`map`,
  `search`, `gps`, `hotspot`); date moves, as the offset from today (`-6`…`+7`) or
  `replay`; PWA install accepted; language switched.
- **Never send a location.** The URL carries `?at=lat,lon` at ~1 m and `?cell=`
  (`web/src/state/urlState.ts`), and by default Umami records every
  `pushState`/`replaceState` URL. So: `data-exclude-search` on the script, plus a
  `data-before-send` guard that strips any query string from `url` and `referrer` and
  drops any event property not on an allowlist. Events never carry coordinates, cell
  ids, comune codes, place names or dates.
- The tracker script and collect endpoint get neutral names (none of `umami`, `track`,
  `stats`, `analytics`, `collect`, `send`, `event`) so generic blocklists miss them. Do
  Not Track is not honoured.
- Only production counts: the script loads only in a production build with the env vars
  set, with `data-domains=mappafunghi.app`, so previews, dev, tests and the tunnel send
  nothing.
- Out of scope: privacy/legal copy (the "Terms and conditions + privacy" card covers
  Umami), backups of the Umami DB (the analytics data is disposable), custom
  dashboards/reports.

**Done:** a visit to mappafunghi.app, including one opened with `?at=…`, shows up in the
Umami dashboard as `/` with no query string. Every event arrives with only its allowed
properties. The daily job still passes with Umami running.

- [ ] Spike: pin a current Umami release (and Postgres major) from the official docker-compose. Confirm whether the pinned image applies `TRACKER_SCRIPT_NAME` and `COLLECT_API_ENDPOINT` at runtime or only at build time, and that its tracker supports `data-exclude-search` and `data-before-send`. Any rename that only works at build time falls back to Caddy rewrites. Write down what you found in this card before going on.
- [ ] Server stack in the repo: `umami` and `umami-db` services in `deploy/compose.yaml` (pinned images, healthcheck + `depends_on`, `mem_limit`, the same log rotation, `DISABLE_TELEMETRY=1`, a named DB volume); secrets in a gitignored `deploy/umami.env` with a committed `umami.env.example`; a `m.mappafunghi.app` site in `deploy/Caddyfile`. Check: `docker compose config` passes, and locally the tracker is served at its renamed path.
- [ ] `web/src/analytics.ts`, test first. `initAnalytics()` (called from `main.tsx`) injects the script only when `import.meta.env.PROD` is true and `VITE_UMAMI_SRC` + `VITE_UMAMI_WEBSITE_ID` are set, with `data-exclude-search`, `data-domains` from `VITE_UMAMI_DOMAINS`, and the before-send guard. `track()` takes a typed event union and does nothing when the tracker isn't loaded. Vitest covers: no script when unconfigured, the attributes, the guard stripping queries and dropping unknown keys.
- [ ] Wire the events where the actions happen (species/view handlers in `App.tsx`, map tap, `PlaceSearch`, `useLocate`, hotspot select, `DateStrip`/`TimeBar`/replay, `InstallBanner`, `LanguageSwitcher`), plus one light test that a UI action calls `track` with the right payload. `pnpm test`, `lint`, `format:check` and `build` pass.
- [ ] Local end-to-end: Umami running locally; `pnpm build && pnpm preview` with the env vars pointed at it; open a `?at=…&species=ovoli` link, switch species, change the day, open a spot by search. In Umami's Postgres, `website_event` has no URL query and no referrer query, exactly one pageview, and each event carries only its allowed keys.
- [ ] Docs: README → Deploying (table row, Umami setup, the web env vars set on Vercel **Production only**), `web/.env.example` (commented out), PRD → Architecture (self-hosted Umami and why) and PRD → Principles (analytics never receives a location).
- [ ] Commit only the files you touched. Then **stop and ask the human to push** (or to OK a push): the server pulls from GitHub and Vercel deploys from `main`.
- [ ] Rollout. Ask the human for a Cloudflare `A` record `m` → the server's IP, DNS only (and for the host, if you don't have it). Then over SSH as root: `git pull`, create `deploy/umami.env` with generated secrets, `docker compose up -d`, wait for Caddy's certificate. Log in, replace the default `admin`/`umami` password (give it to the human in chat, never write it to a file), and create the website "Mappa Funghi" / `mappafunghi.app`. Ask the human to set `VITE_UMAMI_SRC`, `VITE_UMAMI_WEBSITE_ID` and `VITE_UMAMI_DOMAINS` on Vercel (Production only) and redeploy.
- [ ] Server headroom: with Umami up, run `systemctl start mushma-daily` once. It must pass (`journalctl -u mushma-daily`). Note the peak `free -m` and `docker stats` figures in this card.
- [ ] Live check: open `https://mappafunghi.app/?at=43.5,11.2` and trigger each event. The dashboard shows `/` with no query and the events with their properties, and a Vercel preview deployment sends nothing. Record the result here.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
