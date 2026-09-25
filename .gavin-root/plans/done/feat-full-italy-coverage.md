---
order: 3072
kind: plan
title: [feat] full italy coverage
status: Done
complexity: complex
---
Coverage of every region. This needs scientific and common knowledege web search for scientific/multi-enforced data + meteorological data. Each region must have its SEO optimizations. We will file a cards for each region; each region its Gavin’s rail.
This also need a region switcher for the UI.

Decided when this card was developed (2026-09-24):
- Tuscany stays live throughout. Every other region is a standalone plan
  (`region-<slug>.md`, 19 of them) and its own rail, started only after the
  foundation below is merged and deployed. Order: neighbours first (Emilia-Romagna,
  Liguria, Umbria, Lazio, Marche), then north to south; two or three rails at a time.
- Weather history comes from the Copernicus CDS (ERA5-Land in bulk, no per-call
  cap) instead of the Open-Meteo archive. Forecast and seasonal stay on Open-Meteo's
  free tier, and the daily job for 20 regions must fit about half of its 10,000
  calls/day. The weather lattice stays 0.2° so the forecast seam is unchanged.
  Tuscany keeps its stored history.
- Forest: each region uses its own regional land-use or forest map where one exists
  with an open licence, CLC IV level as the fallback. The loader reads any vector
  source declared in config.
- Species rules are per region: `config/species/<region>/` holds a full, cited rule
  set per region (Tuscany's files move under `tuscany/`), sharing the bibliography.
  The backtest report and the press-contrast sanity check run for every region;
  tuning only where the train seasons hold at least 50 usable presences, otherwise
  the researched priors ship and the report says so.
- `/` becomes the hub: a national overview map coloured per served region from a
  small aggregate endpoint (tap to enter) and the list of regions. The app shows one
  region at a time (the ~1 MB payload budget holds per region); a region menu sits
  beside the species switcher, and a GPS fix or a search inside another served
  region offers to switch.
- SEO per region: title and description follow Tuscany's pattern with the region's
  name; the intro (it + en) is written per region by its card, naming its known
  areas and seasons; og images, sitemap and prerendered heads come from the registry.
- API ids for new regions are the Italian slug with underscores (`emilia_romagna`);
  Tuscany keeps `tuscany`. Every API data route takes `region` (default `tuscany`,
  so installed PWAs keep working).
- Adding a region means adding files plus one index line, never editing shared
  strings, so region rails do not conflict.

Foundation (this plan's rail), in order:

- [x] PRD: Current focus becomes Italy region by region (Tuscany live, the rest as `region-*` plans); Architecture records the CDS history source, per-region rule sets, the hub aggregate endpoint and that payload budgets hold per region; "Regions beyond Tuscany" leaves Not in v1
- [x] [Weather history from the Copernicus CDS](./weather-history-cds.md)
- [x] [Forest sources per region](./grid-forest-sources-per-region.md)
- [x] [Species rules per region](./species-rules-per-region.md)
- [x] [API and daily job serve many regions](./api-multi-region.md)
- [x] [Web: hub, region switcher, per-region SEO](./web-hub-region-switcher.md)
- [x] Basemap: `web/scripts/extract-basemap.sh` extracts all of Italy (bbox 6.6,35.4,18.6,47.1, same zooms) as `italy.pmtiles` and `italy-terrain.pmtiles`; sizes recorded and inside the R2 free tier; README tells the human how to upload them and repoint `VITE_BASEMAP_URL` / `VITE_TERRAIN_URL` (the rail holds for that before it pushes)
- [x] [Region onboarding command and runbook](./region-onboarding-command.md)
- [x] Tuscany through the new path: the onboarding command re-runs Tuscany's changed steps; CDS history for 2024 matches the stored Open-Meteo history within the tolerances the weather card set; a scored test window matches today's scores within 0.01; the grid rebuild is identical
- [x] Ready to ship: everything above committed on main (the agent never pushes); the rail's next steps hold for the basemap upload, push main, deploy the API and hold again for the human to verify `/` as the hub with Tuscany alone, `/toscana` unchanged, old `/` and `?species=` links landing, and the next morning's daily job green with its call count logged; then the rail starts the first region rails (Emilia-Romagna, Liguria, Umbria)

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
