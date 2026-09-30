---
order: 3072
title: [region] Valle d'Aosta
status: Done
complexity: complex
---
Region #7 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `valle-d-aosta`, API id `valle_d_aosta`, ISTAT COD_REG 2, names it "Valle d'Aosta" / en "Aosta Valley".
Small and Alpine, bilingual it/fr place names; ovoli are probably absent (drop the group
if the research agrees); check the rain-scale clamp at 1700 m and the lapse rates, since
much of the woodland sits above Tuscany's fitted range.
Forest map candidate, to verify: the regional Carta forestale.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/valle_d_aosta.yaml` (bbox from the ISTAT boundary, COD_REG 2, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-valle-d-aosta-species.md) → `.gavin-root/docs/species-ecology/valle_d_aosta.md` and `api/src/api/config/species/valle_d_aosta/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard valle_d_aosta` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/valle_d_aosta.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/valle-d-aosta.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/valle-d-aosta` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/valle-d-aosta`, the next morning's daily job includes the region

Notes for the PR (2026-09-29): `region/valle-d-aosta` was cut from `main` at `25e4dec`. Besides the region's
own files, its diff has shared changes every reviewer should see:
- `api/src/api/live/repository.py`: the cell detail lists only the region's own groups. Valle d'Aosta has no
  ovoli (dropped by the species research: no record in the region from any source), and without this fix every
  tapped cell there answers 500. Tested.
- `api/src/api/grid/sources.py`: a `manual` download shape for a source saved by hand. The Region's forest map
  (Tipi forestali 2020, CC BY 4.0) is served only behind SPID; it was downloaded through the human's signed-in
  SCT-Outil session and stored in the shared `raw/rvda_tipi_forestali/`. Tested.
- `web/src/regions/index.ts`: Valle d'Aosta is registered **before Piemonte** (Piemonte's bbox holds all of it,
  and `findRegionAt` takes the first match). The web offers porcini and gallinacci only for this region.
- `web/src/App.tsx`, `web/src/map/*`: Prettier only (main failed `format:check`).
Expect merge conflicts with other region branches in `web/src/regions/index.ts`, `web/src/credits.ts` and
`api/src/api/config/species/references.yaml` (each appends a block); keep both sides.
Stores rsync'd to the server on 2026-09-29 (171 files, 59 MB, no redeploy; `/regions` still without the region,
`/status?region=valle_d_aosta` 404): inert until main is deployed, which should run the daily job. Everything is committed; api (956 passed, ruff clean) and web (452 tests, lint, format, build)
checks are green. `.gavin-root/docs/regions/valle_d_aosta.md` has the decisions (INFC -3.8 %, regional lapse
rates 5.3/5.6/5.9, rain scale 0.58 + 0.04/km from the Region's yearbook totals, 4 train presences so the priors
ship, 10/12 press contrasts) and the post-deploy checks.
