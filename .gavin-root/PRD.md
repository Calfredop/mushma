# mushma — Product Requirements

> This PRD is the lead document for development in this workspace. The main agent
> session reads it first; plans in `.gavin*/plans/` should trace back to it.

## Vision

A small single-page app that uses public data, open APIs and foraging/mycology
knowledge to estimate where and when wild edible mushrooms are likely to be
fruiting — today, over the next week, across the season, and in past seasons.

## Audience

- **Friends / a small group** of Tuscan foragers — must be understandable
  without explanation and usable on a phone in the field.
- **Portfolio / showcase** — the data work and the visuals should look good
  and be explainable. Transparency ("why this score") matters as much as accuracy.

## Current focus

**Tuscany, Italy only.** Keep the region definition in config (boundary, grid,
data extents) so another region could be added later without a rewrite.

### Species (v1)

| Common name (IT) | Taxon | Rough ecology (starting hypotheses, to validate) |
|---|---|---|
| Porcini | *Boletus edulis* group (*edulis, aereus, aestivalis/reticulatus, pinophilus*) | Late spring–autumn by sub-species; chestnut, beech, oak, fir/pine; ~10–15 days after significant rain (~30 mm+) with mild soil temps (~12–20 °C); stopped by drying wind and cold nights. |
| Ovoli | *Amanita caesarea* | Thermophilic, ~July–October; oak (cerro, roverella) and chestnut, lower hills; needs warm soil after rain. |
| Gallinacci / finferli | *Cantharellus cibarius* | Long season ~June–November; broadleaf and conifer woods, acidic soils; responds to sustained moisture, persists longer than porcini. |

The ecology column is a starting point only. Each rule must cite its source and
be tuned against sightings (see Model). Soil chemistry is not modelled in v1
(see Model → Known gaps).

## Features (v1)

1. **Conditions map.** A map of Tuscany's woodland cells colored by a
   fruiting-conditions score, per species (and combined), with a date control
   from past to today to +7 days.
2. **Spot forecast.** Tap the map, search a place, or use GPS to get a score per
   species for today plus a 7-day outlook.
3. **"Why this score" breakdown.** For any cell and day, show the factors that
   contributed (rain N days ago, cumulative rain, soil/air temperature, drying,
   habitat type, altitude, season window) and how much each one weighed.
4. **Hot places right now.** A ranked list of the top-scoring areas, plus recent
   public sightings (iNaturalist / GBIF) in Tuscany shown per cell as a
   real-world signal (see Principles → Sightings privacy).
5. **Seasonal outlook.** How the current season is shaping up per species and
   area: rain and temperature compared with normal, and likely upcoming windows
   based on climatology and seasonal forecast data.
6. **Historical analysis.** Browse past seasons: replay daily scores for past
   dates, compare them with the sightings recorded at the time, and see which
   conditions made good years.
7. **Offline / PWA.** Installable, and caches the latest forecast (and map data
   for the area you're viewing) so it works in the woods without signal.
8. **Italian + English UI.** Italian by default; English for the portfolio audience.

All seven milestones below are v1; there is no smaller cut.

## Model

- **Approach: per-species rules, validated against sightings.** Rules turn
  weather history and forecast, habitat (forest type), altitude/aspect and
  season into a 0–1 score per cell, species and day. Rules are transparent and
  data-driven (config with cited sources), and every factor is exposed for the
  "why" breakdown.
- **Factors.** Each is a rule with a cited source: rain amount and lag windows,
  cumulative rain, soil and air temperature bands, soil moisture, drying (wind,
  ET0 / vapour-pressure deficit), cold nights (Tmin), season window, habitat,
  altitude band, and optionally aspect.
- **Score semantics.** A score is a 0–1 *index* of how favourable conditions
  are, not a calibrated probability. The UI calls it a "conditions score" and
  never shows "% chance" unless a backtest calibrates it. The **combined** score
  across species is defined in Model v1 (default proposal: the max across
  species that are in season).
- **Lag makes the outlook robust.** Porcini fruit roughly 10–15 days after
  rain, so the +7-day outlook is driven mostly by rain that has already fallen.
  The weather forecast mainly adds temperature, frost and drying. Use this in
  the "why" copy: the further out, the more the score rests on the forecast.
- **Validation.** Backtest past seasons against GBIF / iNaturalist occurrences:
  do sightings fall disproportionately in high-scoring cell-days? Split
  seasons into train and hold-out before tuning. Report lift and AUC per
  species and season against a habitat-only baseline, and tune thresholds on
  the train seasons only. Set accuracy targets after the first backtest.
- **Known data traps.** Sightings are presence-only and biased toward trails,
  towns and popular areas. iNaturalist hides the exact location of some records
  (geoprivacy), so check coordinate uncertainty. Sparse species-days are noisy.
- **Known gaps (v1).** Soil chemistry (gallinacci prefer acidic soils) is not
  modelled; SoilGrids (ISRIC) or the Regione Toscana pedological map are
  candidates if the backtest shows it matters. Aspect is attached to cells but
  v1 rules may not use it.
- **ML is not in v1.** It may come later if the rules plateau.

## Architecture

- **Frontend.** A static SPA built with Vite + React + TypeScript and MapLibre
  GL, hosted on **Vercel**. Uses i18n (it/en) and a PWA service worker.
- **Backend.** A small **Python + FastAPI** API plus a scheduled data pipeline,
  hosted on **Fly.io**. The pipeline runs daily: it ingests weather
  history and forecast plus recent sightings, scores the grid and stores the
  results. The API serves scores, cell detail and breakdowns, hotspots,
  sightings and history. The frontend never computes the model.
  Decided over Railway: Fly Machines run the daily pipeline on a native
  `--schedule` flag with no extra cron tooling, and Fly's per-VM + per-GB
  volume pricing is cheaper at this scale than Railway's Hobby plan floor.
- **Storage.** **DuckDB reading Parquet files** on a Fly Volume, not
  Postgres/PostGIS. At ~12k cells × 3 species × 365 days ≈ 13M rows/year the
  workload is a daily batch write followed by read-mostly analytical queries —
  a good fit for columnar Parquet, and DuckDB queries it directly with no
  separate database server to run or pay for. Static grid geometry (cell
  polygons, habitat, terrain) ships to the map separately from the daily score
  table and doesn't need a spatial database either.
- **API contract first.** The OpenAPI schema and fixture data are written
  before the data layer exists, so the frontend is built in parallel with the
  pipeline instead of after it.
- **Grid.** About 1 km cells over Tuscany, **woodland cells only** (a cell
  counts if it's mostly forest), each with forest type, elevation, slope and
  aspect attached. Use a projected equal-area grid (e.g. EPSG:3035, the EEA
  reference grid) and convert to WGS84 for the map.
- **Areas.** Aggregation for the seasonal outlook, history and hotspot labels
  uses **comuni** (ISTAT boundaries). A hotspot is a cluster of adjacent
  high-scoring cells, labelled by comune and nearest named place.
- **Weather downscaling.** Weather models are coarser than 1 km, so fetch
  weather on a coarser point set and downscale to cells. Adjust temperature by
  elevation (lapse rate); rain can be taken from the nearest or interpolated
  point. Request daily data in `Europe/Rome` so a day's rain is a local day.
- **Basemap: self-hosted.** Decided in M5. Two files, both extracted by
  `web/scripts/extract-basemap.sh` and pinned to a build date:
  - a Tuscany extract of the **Protomaps** daily OpenStreetMap build (vector
    tiles, maxzoom 14, ~190 MB), styled with `@protomaps/basemaps`;
  - a Tuscany extract of **Mapterhorn** elevation (maxzoom 11, ~33 MB) for
    hillshade, because foragers read the terrain.

  Both go in a **Cloudflare R2** bucket (free tier: 10 GB storage, free
  egress). The Protomaps Cloudflare Worker serves them as plain z/x/y tiles on
  the free Workers plan (100k requests/day), so no custom domain is needed;
  one can serve the files directly later. That is **€0/month** at our traffic.
  Glyphs and sprites come from Protomaps' `basemaps-assets` until M7
  self-hosts them. Attribution: "Protomaps © OpenStreetMap" (ODbL) and
  "© Mapterhorn".

  Rejected options (terms checked 2026-09-17):
  - MapTiler: the free plan is capped at 100k requests/month and suspends
    when exceeded, and the next plan is $30/month. Its terms allow only a
    temporary per-user browser cache and forbid bulk tile downloads.
  - OpenFreeMap: no SLA, and its terms forbid automated collection, which
    covers pre-fetching an area.
  - Stadia: non-commercial cap and a 100 MB offline limit, and it's unclear
    whether a PWA counts as a mobile app.
  - tile.openstreetmap.org: "Offline use is not permitted".

  Owning the extract is the only option that clearly allows M7's offline
  caching. One catch for M7: the Cache API can't store `206` range responses,
  so cache the Worker's z/x/y responses or per-area extracts, never raw
  PMTiles range requests.

### Candidate data sources

| Need | Source |
|---|---|
| Weather: precipitation, Tmin/Tmax, soil temperature and moisture, wind, ET0 / VPD; history, forecast, seasonal | Open-Meteo (Historical/ERA5-Land, Forecast, Seasonal APIs) |
| Observed regional rain (optional ground truth) | SIR Toscana (regional hydrological service), LaMMA |
| Forest type / land cover | Regione Toscana land-use & forest maps (Geoscopio), Corine Land Cover, Copernicus HRL Forest Type |
| Elevation / slope / aspect | TINITALY DEM (INGV, 10 m) or Copernicus DEM GLO-30 |
| Soil (optional, v1 gap) | SoilGrids (ISRIC), Regione Toscana pedological map |
| Sightings | GBIF occurrence API (includes iNaturalist research-grade), iNaturalist API for the most recent records |
| Boundaries / place names | ISTAT boundaries (region, comuni) |
| Basemap and hillshade | Protomaps build of OpenStreetMap, Mapterhorn terrain (self-hosted extracts; see Architecture → Basemap) |
| Place search | Photon (komoot), OpenStreetMap data |

Respect each source's license and attribution requirements (e.g. Open-Meteo CC
BY 4.0, per-dataset GBIF licenses, Copernicus). Show credits in the app.

## Principles

- **Forecast conditions, never edibility.** The app never says a mushroom is
  safe to eat and does not identify specimens. Show a clear disclaimer.
- **Explainable over clever.** Every score can be traced back to its inputs.
- **Honest uncertainty.** Scores are an index, not a probability. Beyond ~7
  days is an outlook, not a forecast, and the UI must make that clear.
- **Sightings privacy.** Public sightings are shown as counts per 1 km cell,
  never as exact coordinates, and records the source obscured are never
  re-sharpened. The app must not become a map of anyone's spots.

## Constraints

- **Cost.** Free or cheap tiers; target under ~€10/month all in (hosting,
  basemap, storage).
- **Freshness.** The daily pipeline finishes before 07:00 Europe/Rome so
  morning foragers see today's scores.
- **Mobile performance.** First map paint under ~3 s on 4G; the whole-region
  score payload under ~1 MB compressed.
- **Licensing.** Every source's license permits this use, and each is credited
  in the app.

## Milestones

1. **Foundations.** Repo, tooling, CI (lint + tests), deploy skeletons (Vercel + Fly/Railway).
2. **Data layer.** Tuscany woodland 1 km grid with habitat and terrain;
   weather ingest (history + forecast); sightings ingest.
3. **Model v1.** Species ecology research with cited rules; rules for porcini,
   ovoli and gallinacci; a backtest harness and the first validation report.
4. **API.** Contract and fixtures first; then scores by date and species, cell
   detail with breakdown, hotspots, sightings, history.
5. **Frontend core.** Map, spot forecast, "why" breakdown, hotspots, i18n.
6. **Time views.** Historical replay and seasonal outlook.
7. **PWA and polish.** Offline caching, mobile UX, credits, disclaimer, production deploy.

## Out of scope

- **Native mobile apps.** It's web only, but it must work well on a phone and be installable as a PWA.

## Not in v1 (undecided / later)

- User accounts, logging the group's own finds, and social features.
- Regions beyond Tuscany.
- Species beyond porcini, ovoli and gallinacci (e.g. chiodini, prataioli, spugnole, tartufi).
- Foraging regulations info (permits/tesserino, daily limits, protected areas).
- Species cards with dangerous-lookalike warnings.
- An ML prediction model.
- Soil chemistry as a model input.

## Open questions

- How to deliver the grid to the map: vector tiles, a compact binary/JSON grid, or raster PNGs?
- How far back to backfill history (bounded by the ERA5-Land archive and API rate limits).
