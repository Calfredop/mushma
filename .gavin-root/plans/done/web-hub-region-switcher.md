---
kind: task
title: [foundation] Web: hub, region switcher, per-region SEO
parent: feat-full-italy-coverage.md
complexity: complex
---
The web app serves many regions: a hub at `/`, a region switcher and per-region SEO
from the registry. Context: `web/src/{regions,routes,config}.ts`, `web/src/App.tsx`,
`web/src/state/`, `web/src/api/{client,queries}.ts`, `web/src/seo/`,
`web/scripts/generate-og-images.mjs`, `web/src/i18n/locales/`, `web/vercel.json`,
`web/vite.config.ts`, and the SEO decisions in `.gavin-root/plans/archive/eat-seo.md`.
Build against the API card's contract (`/regions`, `/overview`, the `region`
parameter) using its fixtures. Decisions in the parent plan `feat-full-italy-coverage.md`.

- Registry as files: `web/src/regions/<slug>.ts`, one per region (slug, apiRegionId,
  names, bounds, maxBounds, species, wikidata, historyStart, and its copy in both
  locales: seo title, description, intro), plus `web/src/regions/index.ts` with one
  import line per region. Tuscany's copy moves out of `it.json` / `en.json` into its
  file; `prerender.ts`, `sitemap.ts`, `structuredData.ts` and the og script read the
  registry. No `import.meta.env` in these modules.
- `config.ts` loses the static `REGION` and `HISTORY_START`; everything reads the
  route's region. The API client passes `region`.
- Hub at `/`: an indexable page with its own head and og image, a national MapLibre
  view coloured per served region from `/overview` for the current species and date
  (unserved regions outlined only), tap → `/<slug>`, and below it the list of regions
  with their intro line. The `/` redirect leaves `vercel.json` and the client;
  `start_url` becomes `/`; an installed user goes to their last region if one is
  stored, else sees the hub. `/` joins the sitemap.
- Region switcher: a menu beside the species switcher (names in the UI locale) that
  navigates to `/<slug>` keeping species, date and view. A GPS fix or a place search
  result inside another served region offers to switch in one tap; outside every
  served region shows the generalised "outside the served regions" copy.
- The species switcher shows only the region's species.
- Offline: cached API responses stay per region; the hub works offline with the last
  `/overview`.
- Tests: routes for two regions, hub rendering, switcher navigation, the GPS prompt,
  prerender of every route; e2e updated for `/` as the hub. No hardcoded UI strings
  outside the registry copy; it and en complete.

Done when: `pnpm test`, `lint`, `format:check`, `build` and `test:e2e` are green with
Tuscany plus the fixture region; Lighthouse SEO 100 on `/`, `/toscana` and one
species page under the local static server the SEO card used.

Done (2026-09-24): Hub at `/` with `/overview` map + region list; file registry
(`regions/toscana.ts`, `umbria.ts`); RegionSwitcher; GPS/search switch offer;
API `region` on all queries; SEO/prerender/sitemap/og/PWA `start_url` `/`.
Verified: `pnpm test` (403), lint, format:check, build, `test:e2e` (19/19),
Lighthouse SEO 100 on `/`, `/toscana`, `/toscana/porcini`.
