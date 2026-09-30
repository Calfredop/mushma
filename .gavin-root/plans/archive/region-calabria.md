---
order: 13312
title: [region] Calabria
status: Done
complexity: complex
---
Region #17 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `calabria`, API id `calabria`, ISTAT COD_REG 18, names it "Calabria" / en "Calabria".
Sila and Aspromonte, major porcini areas under pine, beech and chestnut.
No confident forest map candidate: search the regional geoportale, else CLC IV.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/calabria.yaml` (bbox from the ISTAT boundary, COD_REG 18, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-calabria-species.md) → `.gavin-root/docs/species-ecology/calabria.md` and `api/src/api/config/species/calabria/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard calabria` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/calabria.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/calabria.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/calabria` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/calabria`, the next morning's daily job includes the region

Notes for the PR (2026-09-28): `region/calabria` is cut from `main` at 831165d and carries five commits.
One is Campania's shared fix, cherry-picked because Calabria's bbox needs it too: `fix(grid): skip DEM
tiles the bucket lacks over open sea` (same content as on `region/campania`, so the two merge cleanly).
Stores are on the server (214 files, 435 MB), inert until main is deployed. `.gavin-root/docs/regions/calabria.md`
has the decisions (ISPRA and Regione Calabria's Carta della Natura 1:25,000 for the woodland, +18.5 %
on INFC bosco but +1.1 % once INFC's 84,768 ha of inaccessible woods are counted; national lapse rates
kept; rain scale 0.85 + 0.82/km to 1,300 m from the regional forest programme's station normals, since
Calabria's daily rain needs registration; 13 usable train presences, so the priors ship; 13 of 15 press
contrasts hold) and the post-deploy checks. SoilGrids' WCS answered 503 all morning, so the pH layers were
warped from ISRIC's static VRT (a one-off, described in the doc).
