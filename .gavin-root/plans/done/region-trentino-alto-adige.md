---
order: 5120
title: [region] Trentino-Alto Adige
status: Done
complexity: complex
---
Region #9 of `feat-full-italy-coverage.md`; the parent plan holds the decisions.
Blocked until the parent's foundation rail has deployed (its "Ready to ship" item and the deploy steps after it); the region rails are chained from it in three lanes.
Run on a rail with `DATA_DIR` at the shared data root; never commit data. Follow
README → "Adding a region" and `.gavin-root/docs/woodland-grid.md` → "Adding a region".

Facts: slug `trentino-alto-adige`, API id `trentino_alto_adige`, ISTAT COD_REG 4, names it "Trentino-Alto Adige" / en "Trentino-South Tyrol".
Two autonomous provinces with separate geoportals and bilingual it/de names in Bolzano;
spruce and larch, so *B. pinophilus* and *B. edulis* dominate the porcini group.
Forest map candidates, to verify: Provincia di Trento Tipi forestali and Provincia di
Bolzano Tipologie forestali (one region YAML may need two sources; if the loader cannot
take two, the foundation's forest card gets a follow-up before this rail continues).

- [x] Sources: the region's own land-use or forest map with an open licence (regional geoportale; CC BY, IODL 2.0 or equivalent), recorded in `sources.yaml` with attribution; if none is usable, CLC IV alone, and the region doc says why
- [x] Config: `api/src/api/config/regions/trentino_alto_adige.yaml` (bbox from the ISTAT boundary, COD_REG 4, forest source and class mapping, iNaturalist place id resolved by name, `model:` overrides only if the gauge check asks); `checks lattice` run for the region, national lapse rates kept unless the fit differs by more than 1 °C/km, either way recorded
- [x] [Species research](./region-trentino-alto-adige-species.md) → `.gavin-root/docs/species-ecology/trentino_alto_adige.md` and `api/src/api/config/species/trentino_alto_adige/` (start from Tuscany's files): season windows, host trees and habitat affinities, altitude bands, weather rules where regional literature exists; every rule cited with a confidence; regional references added to the shared bibliography; groups the region lacks dropped and said so; `sanity.yaml` with press or blog contrasts for this region's areas and years
- [x] Data: `api.regions.onboard trentino_alto_adige` through history build; forest area within ±10 % of INFC 2015 or explained; counts recorded in `.gavin-root/docs/regions/trentino_alto_adige.md`
- [x] Validation: backtest report and sanity check in the region doc; tune only if the train seasons hold at least 50 usable presences (record the count), else the priors ship and the doc says so; a gauge check if the provincial weather services publish open daily rain
- [x] Copy and registry: `web/src/regions/trentino-alto-adige.ts` (bounds, species offered, wikidata id verified, seo title and description on Tuscany's pattern, intro it + en of 2–3 sentences naming the region's known areas and seasons, no probability or edibility wording), one line in `web/src/regions/index.ts`, og image generated and committed, credits show the new sources
- [x] Ship: stores rsync'd to the server with the onboarding tool (the API serves the region once main is redeployed); api and web checks green; everything committed on the region branch (the agent never pushes: the rail pushes, opens the PR and, after the human merges it, deploys main); the region doc lists what to verify after that deploy: `/trentino-alto-adige` and its species pages serve real scores, the hub lists and colours the region, the sitemap has it, Lighthouse SEO 100 on `/trentino-alto-adige`, the next morning's daily job includes the region

Notes for the PR (2026-09-26): `region/trentino-alto-adige` was cut from `main` at `831165d` (all five
earlier regions merged), so its diff is this region's plus four shared changes every reviewer should see:
- `api/src/api/grid/build.py`: `forest.types` may be a list of layers, one per source (the "follow-up for
  the foundation's forest card" this card foresaw, done here with tests), and a class code YAML reads as a
  boolean (a bare `ON`) is rejected instead of silently matching nothing.
- `api/src/api/weather/cds.py`: a node up to 0.1° past the shared Italy-wide snowfall file (which stops at
  47.1° N) takes the file's edge row; five nodes here sit at 47.2° N.
- `api/src/api/registry.py`: `/overview` leaves out a region not scored through the date instead of
  answering 404 for the whole hub. This region's stores stop at 2026-09-20 (Open-Meteo's daily limit was
  spent before the forecast), so without this fix the hub map breaks from the deploy until the daily job
  has scored the region.
- `api/src/api/weather/bolzano_meteo.py` + `checks.py`: South Tyrol's open gauges for the rain check.
Expect merge conflicts with `region/lombardia` in `web/src/regions/index.ts`, `web/src/credits.ts`,
`api/src/api/config/species/references.yaml` (both append a block) and `api/src/api/weather/checks.py`
(`GAUGE_NETWORKS`); keep both sides. Stores are on the server, inert until main is deployed; the deploy
should run the daily job. `.gavin-root/docs/regions/trentino_alto_adige.md` has the decisions (both
provincial maps, rain scale ×0.75 from 17 South Tyrolean gauges, national lapse rates kept with Tmin and
Tmean +1.06 °C/km, tuning ran on 122 presences and kept nothing in the shipped configuration, 11/16 press
contrasts) and the post-deploy checks. The species research found the Bolzano picking law is L.P. 18/1991,
not 3/1991 as this card said.
