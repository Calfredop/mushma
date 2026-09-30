---
order: 3072
title: [region] Lazio
status: Done
complexity: complex
---
Region #4 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `lazio`, API id `lazio`, ISTAT COD_REG 12, names it "Lazio" / en "Lazio".
Cimini and Simbruini; Tuscany's neighbour to the south.
Forest map candidates, to verify: Carta dell'uso del suolo 1:10k or the regional forest typology map.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/lazio.yaml` (bbox from the ISTAT boundary, COD_REG 12, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-lazio-species.md) → `.gavin-root/docs/species-ecology/lazio.md` and `api/src/api/config/species/lazio/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard lazio` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/lazio.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/lazio.ts` (bounds including Ponza and the islands, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/lazio` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/lazio`, the next morning's daily job includes the region

Notes for the PR (2026-09-28): `region/lazio` is cut from `main` at 831165d and carries eight commits.
Two are shared fixes: `fix(grid): skip DEM tiles the bucket lacks over open sea` (the same patch as
the Campania, Calabria and Puglia branches; Lazio's bbox asks for the open-sea tile N40 E011) and
`fix(sightings): retry a server that hangs up without answering` (iNaturalist's effort histogram
drops about one connection in three). `api/src/api/config/species/references.yaml` gains a Lazio
block at the end of the file, like every region branch, so merging several region PRs conflicts
there only by position. Stores are on the server, inert until main is deployed.
`.gavin-root/docs/regions/lazio.md` has the decisions (the Region's Carta forestale su base
tipologica, 1:10,000, CC BY 4.0, −5.3 % on INFC; national lapse rates kept; rain scale 0.82 +
0.23/km from 92 open SIARL agrometeo gauges, extrapolated above 800 m; 12 usable train presences, so
the priors ship; 7 of 15 press contrasts hold, three misses near ties) and the post-deploy checks.
