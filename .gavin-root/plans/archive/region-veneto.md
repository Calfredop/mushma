---
order: 4096
title: [region] Veneto
status: Done
complexity: complex
---
Region #10 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `veneto`, API id `veneto`, ISTAT COD_REG 5, names it "Veneto" / en "Veneto".
Dolomites and prealps down to a forestless plain.
Forest map candidates, to verify: Carta forestale regionale or Copertura del suolo 1:10k.

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/veneto.yaml` (bbox from the ISTAT boundary, COD_REG 5, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-veneto-species.md) → `.gavin-root/docs/species-ecology/veneto.md` and `api/src/api/config/species/veneto/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard veneto` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/veneto.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the regional ARPA publishes open daily rain
- [x] Copy and registry: `web/src/regions/veneto.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/veneto` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/veneto`, the next morning's daily job includes the region
- [x] Decision: 97 % of Veneto's woodland cells (3,896 of 4,025) fall inside the Trentino-Alto Adige, Lombardia or Friuli-Venezia Giulia bboxes, and putting Veneto first would take 5,625 of Trentino-Alto Adige's own cells instead. So I'm registering Veneto last, which changes nothing for the regions already live. Until fix-region-lookup-by-boundary ships, a GPS fix or search in Belluno, Asiago or the Lessinia made from the hub will offer the neighbouring region; inside /veneto everything works. Ship it like that, or should I do the boundary lookup on this branch first?
  Options: A) Ship registered last; do fix-region-lookup-by-boundary next B) Do the boundary lookup on region/veneto before the PR
  Answer (2026-10-02): Do the boundary lookup on region/veneto before the PR

Notes for the PR (2026-09-29): `region/veneto` was cut from `main` at `15039d2`. Besides the region's own
files, its diff has two shared changes every reviewer should see:
- `api/src/api/grid/sources.py`: a WFS source can send a `cql_filter` in place of the bbox (GeoServer refuses
  both together), cached per filter, and a WFS layer's pages are now read like the ArcGIS ones, so a group
  layer's `where` and `columns` apply to them. Veneto's forest map is the Region's Carta della copertura del
  suolo 2021 (IODL 2.0), one GeoServer layer of 407,081 polygons for the whole region, fetched as its 48,912
  forest and scrub polygons. Tested (`tests/grid/test_vector_loader.py`).
- `web/src/regions/index.ts`: Veneto is registered **last**, with a test that Trento and Pordenone stay in their
  regions: its bbox overlaps Trentino-Alto Adige's, Lombardia's and Friuli-Venezia Giulia's so much that 97 % of
  its woodland lies in theirs and it would take 5,625 of Trentino-Alto Adige's 7,698 woodland cells if it came
  first. From the hub, a fix in Belluno, Asiago or the Lessinia is offered the neighbour until
  `fix-region-lookup-by-boundary.md` ships (the Decision below is still open: option B means more work on this
  branch before the merge).
Expect merge conflicts with other region branches in `web/src/regions/index.ts`, `web/src/credits.ts` and
`api/src/api/config/species/references.yaml` (each appends a block); keep both sides. `sources.yaml` inserts
`rv_ccs2021` before `rm_rem_vegetazione`. Stores rsync'd to the server on 2026-09-29 (219 files, 277 MB, no
redeploy; `/regions` still without the region, `/status?region=veneto` 404): inert until main is deployed, which
should run the daily job. Everything is committed; api (1,008 passed, ruff clean) and web (491 tests, lint,
format, build) checks are green. `.gavin-root/docs/regions/veneto.md` has the decisions (INFC -4.4 %, national
lapse rates kept, rain scale 0.85 - 0.04/km from 153 ARPAV gauges' monthly totals, 14 train presences so the
priors ship, 9/16 press contrasts) and the post-deploy checks.
