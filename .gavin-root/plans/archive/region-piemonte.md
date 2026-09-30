---
order: 3072
title: [region] Piemonte
status: Done
complexity: complex
---
Region #6 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `piemonte`, API id `piemonte`, ISTAT COD_REG 1, names it "Piemonte" / en "Piedmont".
Alps and Apennines with wide chestnut belts.
Forest map candidate, to verify: Carta forestale regionale (tipi forestali).

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/piemonte.yaml` (bbox from the ISTAT boundary, COD_REG 1, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-piemonte-species.md) → `.gavin-root/docs/species-ecology/piemonte.md` and `api/src/api/config/species/piemonte/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard piemonte` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/piemonte.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/piemonte.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/piemonte` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/piemonte`, the next morning's daily job includes the region

Notes for the PR (2026-09-26): `region/piemonte` was fast-forwarded onto `region/umbria` (its PR still
open) for the shared CDS, sightings and onboarding fixes, and took three shared commits from
`region/liguria` (WFS paging and one-map forest read, the og-image registry script, the openrsync fix);
until those PRs merge, this PR's diff includes them. It also carries a shared fix every later region
needs: `api/src/api/history/seasons.py` kept the season table under the history build's 256 MB cap
(Piemonte's 1,180 comuni ran it out of memory; the server's daily job would have failed the same way).
Stores are on the server, inert until main is deployed. `.gavin-root/docs/regions/piemonte.md` has the
decisions (Carta forestale 2025, rain scale x0.74, national lapse rates kept with Tmin +1.04 °C/km,
tuning ran on 53 presences and nothing held on the hold-out) and the post-deploy checks.
