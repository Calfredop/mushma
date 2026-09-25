---
order: 18432
title: [region] Sardegna
status: To Do
complexity: complex
---
Region #19 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `sardegna`, API id `sardegna`, ISTAT COD_REG 20, names it "Sardegna" / en "Sardinia".
Strong porcini and ovoli tradition (Sardegna Foreste is already in the bibliography); cork
and holm oak, with *B. aereus* likely the leading porcini taxon.
Forest map candidate, to verify: Carta dell'uso del suolo 2008 (Regione Sardegna).

- [ ] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [ ] Config: `api/src/api/config/regions/sardegna.yaml` (bbox from the ISTAT boundary, COD_REG 20, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [ ] Species research → `.gavin-root/docs/species-ecology/sardegna.md` and `api/src/api/config/species/sardegna/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [ ] Data: `api.regions.onboard sardegna` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/sardegna.md`
- [ ] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [ ] Copy and registry: `web/src/regions/sardegna.ts` (bounds including the small islands, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [ ] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/sardegna` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/sardegna`, the next morning's daily job includes the region
