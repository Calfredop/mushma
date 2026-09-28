---
order: 11264
title: [region] Puglia
status: Done
complexity: complex
---
Region #15 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `puglia`, API id `puglia`, ISTAT COD_REG 16, names it "Puglia" / en "Apulia".
Little forest: the Gargano and the Murge; expect few woodland cells and few sightings.
Forest map candidate, to verify: SIT Puglia Uso del suolo 2011.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/puglia.yaml` (bbox from the ISTAT boundary, COD_REG 16, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-puglia-species.md) → `.gavin-root/docs/species-ecology/puglia.md` and `api/src/api/config/species/puglia/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard puglia` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/puglia.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/puglia.ts` (bounds including the Tremiti, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/puglia` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/puglia`, the next morning's daily job includes the region
- [ ] Decision: Puglia's woodland comes from the Region's Carta dei Tipi Forestali (2022, forest types, +3.3 % on INFC). It states no licence, so it is used as open by default (CAD art. 52), as Marche's REM map was, and credited CC BY 4.0. Keep it, or switch to UDS 2011 (IODL 2.0, no types, −11.5 % on INFC) with ISPRA's 2013 Carta della Natura for the types?
  Options: A) Keep the Carta dei Tipi Forestali (open by default) B) Switch to UDS 2011 + Carta della Natura C) Ask the Region first (email SIT Puglia)

Notes for the PR (2026-09-28): `region/puglia` is cut from `main` at 831165d and carries five commits.
One is Campania's shared fix, cherry-picked because Puglia's bbox needs it too: `fix(grid): skip DEM
tiles the bucket lacks over open sea` (same content as on `region/campania` and `region/calabria`, so
they merge cleanly). Stores are on the server (190 files, 97 MB), inert until main is deployed.
`.gavin-root/docs/regions/puglia.md` has the decisions (the Region's Carta dei Tipi Forestali for
the woodland, +3.3 % on INFC, used as open by default since it states no licence: the Decision item
above asks the human to confirm; national lapse rates kept; rain scale 0.93 + 0.34/km to 900 m from
the Protezione Civile's monthly gauge totals of 2016–2020; 1,105 woodland cells; 0 usable sightings,
so the priors ship; *B. pinophilus* dropped; 11 of 13 press contrasts hold) and the post-deploy
checks. The Tremiti's one woodland cell has no weather node and is not scored.
