---
order: 14336
title: [region] Sicilia
status: In Progress
complexity: complex
---
Region #18 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `sicilia`, API id `sicilia`, ISTAT COD_REG 19, names it "Sicilia" / en "Sicily".
Etna, Nebrodi and Madonie; the small islands (Eolie, Egadi, Pelagie, Pantelleria) sit
inside the bounds, so expect sea nodes and a wide bbox.
Forest map candidate, to verify: the regional Carta forestale.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/sicilia.yaml` (bbox from the ISTAT boundary, COD_REG 19, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-sicilia-species.md) → `.gavin-root/docs/species-ecology/sicilia.md` and `api/src/api/config/species/sicilia/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard sicilia` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/sicilia.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional weather service publishes open daily rain
- [x] Copy and registry: `web/src/regions/sicilia.ts` (bounds including the small islands, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/sicilia` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/sicilia`, the next morning's daily job includes the region

Notes for the PR (2026-09-28): `region/sicilia` is cut from `main` at 831165d and carries eight commits.
Two are shared fixes cherry-picked from other region branches, same content there: `fix(grid): skip DEM
tiles the bucket lacks over open sea` (as on `region/calabria` and `region/campania`) and `fix(grid): page
an ArcGIS layer by what the server returned` (as on `region/abruzzo`; `region/lombardia` fixes the same
lines differently). One is new and shared: `fix(grid): an ArcGIS forest layer honours where, and is paged
once per region`. Another adds SIAS gauges to the rain check. Stores are on the server (210 files, 195 MB),
inert until main is deployed. `.gavin-root/docs/regions/sicilia.md` has the decisions: the Regione
Siciliana's SIF Carta forestale regionale (1:10,000, open by default under CAD art. 52) for the woodland;
+12.7 % on INFC bosco, +2.9 % once INFC's low woods, boscaglie and inaccessible woods are counted; national
lapse rates kept; rain scale 0.88 + 0.10/km fitted on 94 SIAS gauges (June 2019 to May 2020, the one whole
year the open data hold); 7 usable train presences, so the priors ship; 12 of 14 press contrasts hold. It
also lists the post-deploy checks. Pantelleria's and Salina's 8 woodland cells are out of the weather's
reach and stay unscored.
