---
order: 6144
title: [region] Basilicata
status: Done
complexity: complex
---
Region #16 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `basilicata`, API id `basilicata`, ISTAT COD_REG 17, names it "Basilicata" / en "Basilicata".
Pollino and Vulture woods.
Forest map candidate, to verify: the regional Carta forestale.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/basilicata.yaml` (bbox from the ISTAT boundary, COD_REG 17, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-basilicata-species.md) → `.gavin-root/docs/species-ecology/basilicata.md` and `api/src/api/config/species/basilicata/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard basilicata` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/basilicata.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/basilicata.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/basilicata` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/basilicata`, the next morning's daily job includes the region

Notes for the PR (2026-09-30): `region/basilicata` is cut from `main` at 15039d2 and carries five commits,
Basilicata's own files only: species rules and 14 press contrasts, `basilicata.yaml` and its `sources.yaml`
entry, the web registry line (Basilicata registered after Calabria and before Puglia, because Puglia's bbox
holds all of Basilicata), og images and the credit, and the region doc. Expect merge conflicts with
`region/molise` and `region/veneto` in `web/src/regions/index.ts`, `web/src/regions/index.test.ts`,
`web/src/credits.ts` and `api/src/api/config/species/references.yaml` (each appends a block); keep both
sides. `.gavin-root/docs/regions/basilicata.md` has the decisions: ISPRA's Carta della Natura (1:50,000,
2013, CC BY 4.0) for the woodland, because the Region's Carta forestale (2006) is not published as data
and its geoportal refused every connection; −1.2 % on INFC; national lapse rates kept; rain scale 1.04 +
0.14/km clamped at 920 m from ALSIA's published station totals (the Centro Funzionale's daily data did not
answer); 0 usable presences, so the priors ship and there is no backtest AUC; 12 of 14 press contrasts
hold (the misses are both early-season porcini). It also lists the post-deploy checks. api (1006 passed,
ruff clean) and web (491 tests, lint, format, build) are green. The stores are on the server (202 files,
203 MB into `/srv/mushma-data`, file counts checked against the server's); the API serves Basilicata once
main is redeployed.
