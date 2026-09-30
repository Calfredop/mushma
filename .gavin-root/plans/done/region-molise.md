---
order: 5120
title: [region] Molise
status: Done
complexity: complex
---
Region #13 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `molise`, API id `molise`, ISTAT COD_REG 14, names it "Molise" / en "Molise".
Small; Matese and the upper Molise woods.
No forest map candidate known: search the regional geoportale, else CLC IV.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/molise.yaml` (bbox from the ISTAT boundary, COD_REG 14, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-molise-species.md) → `.gavin-root/docs/species-ecology/molise.md` and `api/src/api/config/species/molise/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard molise` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/molise.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/molise.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/molise` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/molise`, the next morning's daily job includes the region
- [x] Human test: Rsync Molise's stores to the server (the agent's permission mode refused it): from mushma-regions-1, run `DATA_DIR=/Users/coalpila/CloudStation/Coding/mushma/api/data deploy/rsync-region-data.sh molise` (or the gavin tool "Rsync region data", region molise, redeploy no), then mark this passed

Notes for the PR (2026-09-30): `region/molise` is cut from `main` at 15039d2 and carries six commits,
Molise's own files only: species rules and 17 press contrasts, `molise.yaml` and its `sources.yaml` entry,
the web registry line (Molise registered last), og images and the credit, and the region doc. Expect merge
conflicts with other region branches in `web/src/regions/index.ts`, `web/src/credits.ts` and
`api/src/api/config/species/references.yaml` (each appends a block); keep both sides.
`.gavin-root/docs/regions/molise.md` has the decisions: ISPRA's Carta della Natura (2021, CC BY 4.0) for the
woodland, because the Region's forest-type map is a PDF and its geoportal no longer resolves; +3.9 % on INFC
(CLC IV alone −21.5 %); national lapse rates kept; rain scale 0.84 + 0.36/km clamped at 1,200 m, borrowed from
Lazio, Campania and Puglia (Molise's gauges are paid or behind a login); 1 train presence, so the priors ship;
13 of 17 press contrasts hold. It also lists the post-deploy checks. api (1006 passed, ruff clean) and web
(491 tests, lint, format, build) are green. The stores are on the server: the human ran the rsync on
2026-09-30 (204 files, 129 MB into `/srv/mushma-data`, file counts checked against local); the API serves
Molise once main is redeployed.
