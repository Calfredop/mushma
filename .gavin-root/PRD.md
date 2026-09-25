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

**Italy, region by region.** Tuscany is live; every other region is a standalone
`region-*` plan and its own rail, started only after the multi-region foundation
(`feat-full-italy-coverage`) is merged and deployed. Region definitions stay in
config (boundary, grid, data extents, forest source, species rules). The app
shows one region at a time; `/` is a national hub that lists and colours every
served region.

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
  altitude band, slope, and sun exposure (each species' preference for sunny or
  shady slopes, from the cell's slope, aspect and the day's sun path).
- **Growth clock and terrain microclimate.** Added after Model v1 (card
  `algo-more-factor`). Each species has a growth pace per cell-day: a cardinal
  temperature curve on topsoil temperature, slowed by dry air (VPD). The rain lag
  is counted in growth days, so a warm, humid spell brings a flush forward and a
  cold or dry one holds it back. Before scoring, each cell's temperatures and ET0
  are shifted by how much more or less sun its slope gets than flat ground. Every
  parameter is a derived prior; the train-season comparison is in
  `.gavin-root/docs/model-v1-validation.md`.
- **Score semantics.** A score is a 0–1 *index* of how favourable conditions
  are, not a calibrated probability. The UI calls it a "conditions score" and
  never shows "% chance" unless a backtest calibrates it. Decided in Model v1:
  a species' score is the max over its taxa (porcini has four rule sets, one
  per sub-species, and the breakdown names the winner), and the **combined**
  score is the max over the species in season, with the winner's breakdown
  (0 and no breakdown when none is in season). Max keeps the index meaning
  ("the best conditions of the three, here, today") and never inflates; a
  probabilistic OR would treat scores as probabilities. The API serves it as
  its own species key, `combined`.
- **Lag makes the outlook robust.** Porcini fruit roughly 10–15 days after
  rain, so the +7-day outlook is driven mostly by rain that has already fallen.
  The weather forecast mainly adds temperature, frost and drying. Use this in
  the "why" copy: the further out, the more the score rests on the forecast.
- **Validation.** Backtest past seasons against GBIF / iNaturalist occurrences:
  do sightings fall disproportionately in high-scoring cell-days? Split
  seasons into train and hold-out before tuning. Report lift and AUC per
  species and season against a habitat-only baseline, and tune thresholds on
  the train seasons only. Set accuracy targets after the first backtest.
  Split fixed in Model v1, before any score met a sighting: train on the
  seasons 2016–2023, hold out 2024 and 2025, and report 2026 only once it
  ends. Season windows, altitude bands and habitat affinities stay frozen,
  because the species research drew them partly from sightings of every year.
- **Known data traps.** Sightings are presence-only and biased toward trails,
  towns and popular areas. iNaturalist hides the exact location of some records
  (geoprivacy), so check coordinate uncertainty. Sparse species-days are noisy:
  the first Tuscany pull (GBIF + iNaturalist, 2026-09-17) kept only 134
  sightings across the three species after quality filtering and the
  woodland-cell join (121 once Model v1 dropped 28 soil-DNA samples and widened
  gallinacci to the *Cantharellus* genus), with no detectable town-proximity bias at cell
  resolution yet — too little data to call the trap above ruled out (see
  `.gavin-root/docs/sightings-profile.md`).
  Reanalysis rain is too dry in the hills: against 133 SIR Toscana gauges in
  woodland (2025) it holds about 70 % of the measured rain (79 % below 400 m,
  63 % above 800 m). Rain thresholds taken from gauge-based studies must be
  tuned on it or the rain rescaled (see `.gavin-root/docs/weather-ingest.md`).
  Model v1 rescales it before scoring, by 1.28 + 0.29 per km of cell height
  (fitted to the 2025 gauges, 0.99 of gauge rain on 2026), and the backtest
  compares that with the raw rain.
- **Known gaps (v1).** Soil chemistry (gallinacci prefer acidic soils) is not
  modelled; SoilGrids (ISRIC) or the Regione Toscana pedological map are
  candidates if the backtest shows it matters. Terrain shade cast by
  neighbouring ridges and canopy shade are not modelled: sun exposure comes
  from each cell's own slope and aspect only.
- **ML is not in v1.** It may come later if the rules plateau.

## Architecture

- **Frontend.** A static SPA built with Vite + React + TypeScript and MapLibre
  GL, hosted on **Vercel**. Uses i18n (it/en) and a PWA service worker.
- **Backend.** A small **Python + FastAPI** API plus a scheduled data pipeline,
  hosted on a small **Hetzner** cloud server (CX23) with Docker. The pipeline
  runs daily: it ingests weather history and forecast plus recent sightings,
  scores the grid and stores the results. The API serves scores, cell detail
  and breakdowns, hotspots, sightings and history. The frontend never
  computes the model.
  Decided at the production deploy (2026-09-22), replacing Fly.io, which M1
  had chosen over Railway: a Fly volume attaches to one machine only, so a
  scheduled job machine could never share its stores with the API machine, and
  Fly no longer has a free allowance. One server keeps the stores on one disk,
  runs the API behind Caddy and the pipeline from a systemd timer, for about
  €7.31/month with VAT. DNS, the web app and the basemap stay on free tiers
  (Cloudflare, Vercel, Cloudflare R2). Setup is in the README → Deploying.
- **Storage.** **DuckDB reading Parquet files** on the server's disk, not
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
- **Grid delivery.** A flat JSON array (`GET /scores`: `cell_id`, `lon`, `lat`,
  `score` per woodland cell), gzip-compressed over HTTP like everything else
  the API serves. Decided over vector tiles or a raster PNG: measured against
  the real M2/M3 grid (10,777 woodland cells for Tuscany), the whole-region
  payload for one species and day is ~740 KB raw and ~120 KB gzipped — under a
  sixth of the ~1 MB compressed budget, with room to keep `lon`/`lat` per cell
  (dropping them and relying on the client's cached `/grid` geometry would
  gzip to ~40 KB, but isn't needed at this size). A JSON array of ~11k points
  is also well inside what MapLibre's point/circle layers render smoothly, and
  keeping JSON avoids a second encoding the frontend (already built against
  this contract, M5) would have to learn. **Payload budgets hold per region**:
  the app loads one region at a time; a national overview uses a small
  aggregate endpoint (`GET /overview`) rather than every cell. Revisit only if
  a single region's grid grows much denser.
- **Multi-region API.** Every data route takes a `region` query parameter
  (default `tuscany`, so installed PWAs keep working). API ids are Italian
  slugs with underscores (`emilia_romagna`); Tuscany keeps `tuscany`.
  `GET /regions` lists served regions; `GET /overview` returns per-region mean
  score and share of woodland cells at or above `good_score` for the hub map.
- **Species rules per region.** Rule sets live under
  `config/species/<region>/` (Tuscany under `tuscany/`), sharing one
  bibliography. A region may omit a species group; the API's species list
  follows what that region has on disk.
- **Areas.** Aggregation for the seasonal outlook, history and hotspot labels
  uses **comuni** (ISTAT boundaries). A hotspot is a cluster of adjacent
  high-scoring cells, labelled by comune and nearest named place.
- **Weather downscaling.** Weather models are coarser than 1 km, so fetch
  weather on a coarser point set and downscale to cells. Adjust temperature by
  elevation (lapse rate); rain can be taken from the nearest or interpolated
  point. Request daily data in `Europe/Rome` so a day's rain is a local day.
  Decided in M2, with the history source updated for multi-region
  (`feat-full-italy-coverage`; details in `.gavin-root/docs/weather-ingest.md`):
  - **Sources.** History comes from the **Copernicus Climate Data Store**
    (ERA5-Land in bulk, no per-call cap), so a new region's 2016→today backfill
    does not burn Open-Meteo quota. Tuscany keeps its already-stored Open-Meteo
    archive history. The recent days and the +7-day forecast stay on Open-Meteo
    ECMWF IFS 9 km (`ecmwf_ifs`); seasonal stays on Open-Meteo's free tier. The
    daily job for 20 regions must fit about half of Open-Meteo's 10,000
    calls/day. Reanalysis wins over forecast for any day both have, and each
    downscaled value records which one it used.
  - **Points.** Every other ERA5-Land node, a 0.2° lattice (103 land nodes for
    Tuscany). The lattice stays 0.2° so the forecast seam is unchanged.
    Compared with the full 0.1° grid it needs about a third of the API calls.
    It loses about 0.3 °C on temperatures and 3 mm on wet 3-day rain totals
    (leave-out test, 2024).
  - **Downscaling.** Bilinear from the four surrounding nodes, sea nodes left
    out. Temperatures move to the cell's height at 4.2–4.5 °C/km (air) and
    3.7 °C/km (0–7 cm soil): the gradients ERA5-Land carries across Tuscany,
    in line with observed rates. The textbook 6.5 °C/km did worse.
  - **History depth.** Backfill from **2016-01-01**, newest year first. The
    seasons from 2019 hold 90 % of the dated Tuscan GBIF records for the three
    species, and ten years give the percent- and percentile-of-normal factors a
    first baseline. CDS bulk download replaces the Open-Meteo archive backfill
    that used to cost ~3,000 of 10,000 daily calls per year.
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
- **Analytics: self-hosted Umami.** Decided in the `feat-umami-integration`
  card. Umami + Postgres run on the same Hetzner box as the API, behind Caddy
  at `m.mappafunghi.app`, so usage (which species and views people use, how
  they find a spot, PWA installs) is visible without adding cost or handing
  visitor data to a third party. It loads only once a visitor accepts the
  cookie banner, and only in production (never previews, dev or the tunnel);
  Principles → Analytics never receives a location has what it's allowed to
  record.

### Candidate data sources

| Need | Source |
|---|---|
| Weather: history (ERA5-Land bulk) | Copernicus Climate Data Store (CDS) |
| Weather: recent days, +7-day forecast, seasonal | Open-Meteo (Forecast / ECMWF IFS, Seasonal APIs) |
| Observed regional rain (optional ground truth) | SIR Toscana (regional hydrological service), LaMMA; other regional ARPAs where open |
| Forest type / land cover | Per-region land-use / forest maps where open-licensed; Corine Land Cover IV as fallback; Copernicus HRL Forest Type |
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
- **Analytics never receives a location.** The URL can carry a tapped point
  or cell at ~1 m precision (`?at=`, `?cell=`); analytics (self-hosted Umami,
  Architecture) never sees it. Every pageview and event goes through a guard
  that strips query strings and collapses the path before it's sent, so
  species, view, date and search-vs-GPS-vs-map usage are visible, but never
  where anyone tapped, searched or stood.

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
- Species beyond porcini, ovoli and gallinacci (e.g. chiodini, prataioli, spugnole, tartufi).
- Foraging regulations info (permits/tesserino, daily limits, protected areas).
- Species cards with dangerous-lookalike warnings.
- An ML prediction model.
- Soil chemistry as a model input.

## Open questions

None.
