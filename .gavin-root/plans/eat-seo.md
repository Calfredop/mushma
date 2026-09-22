---
complexity: moderate
order: 6144
kind: plan
title: [ƒeat] SEO
status: To Do
---
Do a basic but comprehensive SEO optimization of the site. More regions beside
Tuscany will come soon, so the app segments per region.

Decided when this card was developed (2026-09-23):
- Region and species live in the path: `/toscana` (combined score, the region page),
  `/toscana/porcini`, `/toscana/ovoli`, `/toscana/gallinacci`. No trailing slash.
  Everything else (date, cell, view, comune…) stays in the query string, and
  canonicals drop it. First-time visitors land on the combined view instead of porcini.
- `/` permanently redirects to `/toscana` while Tuscany is the only region; it becomes
  a hub when region #2 arrives. Old `?species=` links land on the matching species path.
- Web side only: a slug-keyed region registry in `web/src/config.ts` with one entry.
  The API stays Tuscany-only; serving a second region is a future card.
- Search is Italian only: indexed titles, descriptions and copy are Italian. English
  stays the client toggle (no `/en/` routes, no hreflang).
- One route list is the source of truth for the prerendered pages, the sitemap and the
  Vercel routes, so the Terms/Privacy card (`feat-terms-and-conditions-privacy.md`)
  adds one line per page.
- Copy follows AGENTS.md: "conditions score", never probability; no edibility or
  identification claims.
- The rename (nested card `fix-rename-app.md`) runs first: every title and description
  below uses the new name.

- [ ] [Rename the app to Mappa Funghi](./fix-rename-app.md)
- [ ] Region registry: `REGION` in `web/src/config.ts` becomes a registry keyed by slug (`toscana`: it/en names, bounds, species offered, API region id `tuscany`); every current `REGION` use reads the active region; existing tests pass unchanged
- [ ] Path routing, tests first: `/:region` and `/:region/:species` parse into the URL state (`/toscana` = combined); the species switcher navigates between paths; `?species=` is rewritten to the path with `replaceState`, keeping the other params; `/` replaces to `/toscana` in the client too (dev, preview, installed PWA); unknown region or species shows the 404 page
- [ ] Root redirect at the edge: `/` → `/toscana` permanent in `web/vercel.json`, query string kept; PWA `start_url` becomes `/toscana`; e2e specs that open `/` still pass
- [ ] Per-page head: a Vite build step writes one prerendered HTML per route from `index.html` with its own `<title>`, meta description, canonical, Open Graph + Twitter card tags, JSON-LD (`WebApplication`) and `lang="it"`; the client updates title, description and canonical on navigation; a test checks the built HTML of every route
- [ ] Visible intro copy: 2–3 sentences for the region page and each species page (what the map shows, the season window, that the score is a conditions index), in both locales through i18n, shown in the UI without covering the map on a phone, and baked into each page's prerendered HTML
- [ ] `robots.txt` + `sitemap.xml` generated from the route list at build time, with absolute `https://mappafunghi.app` URLs (credits page included); robots points at the sitemap
- [ ] Real 404s: the catch-all rewrite in `web/vercel.json` becomes the route list plus a `404.html` (noindex, link back to `/toscana`); unknown paths return HTTP 404; offline, the service worker still opens the app
- [ ] Link-preview images: one 1200×630 og:image per page (`/credits` reuses the region page's), made by a committed script (Playwright screenshot of the map or a rendered SVG) into `web/public/og/`, referenced by absolute URL
- [ ] noindex the API: `X-Robots-Tag: noindex` on `api.mappafunghi.app` in `deploy/Caddyfile` (and on `tiles.mappafunghi.app` if the Protomaps Worker allows it without forking); the README notes the redeploy step for the human
- [ ] Search Console runbook in the README: Cloudflare DNS TXT verification for Google Search Console and Bing Webmaster Tools, submitting the sitemap, what to check afterwards
- [ ] Verify: `pnpm test`, `lint`, `format:check`, `build`, `test:e2e` green; Lighthouse SEO 100 (mobile) on `/toscana` and `/toscana/porcini` under `pnpm preview`; the deployed site shows a permanent redirect on `/`, 404 on an unknown path, and the right tags in each page's served HTML

Indexing itself (Google/Bing picking the pages up) is the human's follow-up after the
runbook, not a gate on this card.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
