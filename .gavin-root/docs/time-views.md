# Time views: historical replay, season comparison and seasonal outlook

Card: M6 · Time views. Traces to PRD → Features 5 (seasonal outlook) and 6 (historical analysis),
Principles (honest uncertainty, sightings privacy), Architecture (areas are comuni) and Milestone 6.

## What the app shows

| view | question it answers | data behind it |
|---|---|---|
| **Replay a day** | what did the map look like on 12 October 2024, and what was found then? | the stored daily scores (`GET /scores?date=`) plus sighting counts per cell for the 14 days either side (`GET /sightings?since&until`) |
| **Replay a season** | where were conditions good in 2024? | good days per woodland cell over the season (`GET /history/season/{year}`) plus the season's sighting counts |
| **Season comparison** | which years were good here, and what drove them? | per-year and per-month stats for Tuscany or one comune (`GET /history/seasons`) |
| **Seasonal outlook** | how is this season going, and when might the next good windows come? | the season so far against normal, the same weeks in past seasons, and the rain leading into them (`GET /outlook`) |
| **Plausible species** | which species does this zone's woodland suit, and how did each fare? | per species and taxon, the share of the zone's woodland whose habitat and altitude suit it, and its good days per season (`GET /species`) |

`GET /comuni` lists the comuni with woodland for the area picker. The web app puts the three views
on tabs in the sheet (Now, Seasons, Outlook). A calendar button beside the date strip replays any
past day; picking a season in the Seasons tab puts it on the map with its own legend; the season's
best day can be replayed from there. Once a zone (comune) is picked, the Seasons and Outlook tabs
list its plausible species under the picker, and a chosen season's stats break its good days down
by species and taxon.

## Definitions

- **Good day.** A cell-day whose conditions score is at least **0.6**: the two darkest classes of the
  map scale. The hotspot threshold (0.5) is too lenient for comparing seasons: in the scored 2025
  season it marked 80–90 % of Tuscany's woodland as good every week from September to mid-October
  for porcini, so every year would look alike. At 0.6 a woodland cell had a median of 59 good porcini
  days in 2025 (quartiles 41 and 72) and September stood out from October (80 % vs 39 % of
  cell-days). Aggregation, not a species rule, so it lives in `config/history.yaml` with this note.
- **Good days (area).** For an area (Tuscany or a comune), the sum over days of the share of its
  woodland cells that were good that day: a typical cell's good days. It does not grow with the
  size of the comune, so comuni compare fairly, and a day that missed some cells (weather gaps)
  counts by the cells it has.
- **Season.** A calendar year, as in the backtest. History stops at yesterday: today and the
  forecast days are on the map but not in a season's record. Rain and temperature are summarised
  over the observed days of the species' **season window**, the span of its rule files'
  `season_window` gates (the earliest `zero_below` to the latest `zero_above` across the group's
  keys), so porcini's rain is May–December and ovoli's June–November. Good days count the whole
  year: the season gate already zeroes the rest.
- **Normal.** Weather normals are daily means per weather point over the complete reanalysis years
  inside the configured baseline (2016–2025), smoothed with a centred 31-day window, rebuilt on
  every update so they follow the backfill. A season's "typical" good days are the median over the
  complete scored seasons inside the same baseline, to the same day of the year for the season
  under way. Every response lists the years it actually used, so a thin baseline shows.
- **Plausible species.** A taxon (a rule set: the four porcini keys, the ovolo, the gallinaccio)
  is plausible in a woodland cell when its static gates, habitat affinity times the altitude band
  (weather and season aside: the backtest's `static` baseline), reach **0.5**: a moderate host, as
  the rule files rank hosts, inside the altitude band. A species group is plausible where any of
  its taxa is, as its score is the best of its taxa. An area's **fit share** is the share of its
  woodland cells where a taxon or group is plausible. Aggregation, not a species rule, so the 0.5
  lives in `config/history.yaml` (`plausible_fit`). Gallinacci on pure Turkey or downy oak sit
  exactly at 0.5 and count.
- **Good days per taxon.** Each taxon key's own good days, counted like a group's from its own
  stored scores. A group's good days count the cell-days any of its taxa was good, so a group's
  taxa never add up to it.
- **Area weather.** An area's daily rain and temperature are a weighted mean of the weather points,
  with the weights of the downscaling (`weights.parquet`) averaged over the area's woodland cells.
  That is exactly the mean of the downscaled cells: downscaling is linear in the point values, so
  rain keeps the model's height scaling and temperature its lapse-rate offset, and actuals and
  normals go through the same weights. Forecast days are kept (for the outlook) but flagged and
  left out of a season's weather.

## Pipeline

```
weather store ──► climatology/normals.parquet  (per point, day of year)
     │                         │
     ▼                         ▼
area weights ──► history/area_weather (per area, day: rain, temp, normals, forecast flag)
score store ───► history/area_days    (per area, species, day: cells, good cells, mean)
             ├─► history/cell_seasons (per cell, species, year: good days)
             └─► history/taxon_seasons (per area, taxon key, year: good days)
grid habitats + species rules ──► history/area_fit.parquet (per area, taxon or group: fit share)
sightings ─────► history/area_sightings (per area, species, day: counts, never coordinates)
                               │
                               ▼
               history/seasons.parquet, history/months.parquet
Open-Meteo Seasonal ──► outlook/seasonal.parquet (per point, week or month)
                               └──► history/area_seasonal.parquet
```

Commands (`api/`):

```sh
uv run python -m api.model.pipeline score --start 2016-01-01 --end 2025-12-31 --no-factors
uv run python -m api.history.build update --years 2016-2026   # normals + per-area tables
uv run python -m api.weather.seasonal fetch                   # EC46 weekly + SEAS5 monthly
uv run python -m api.history.build outlook                    # the long-range rows per area
```

The daily job (`api.jobs.daily`) runs `history.build update` for the current year, then
`weather.seasonal fetch` and `history.build outlook`, after scoring, so a long-range outage never
holds back today's map. The seasonal fetch costs about 450 weighted Open-Meteo calls (103 points,
weekly 46 days + monthly 150 days).

**Memory.** The job machine has 1 GB. Every aggregation over area-days runs in DuckDB on one
connection capped at 256 MB (spilling to `$DATA_DIR/tmp/duckdb`), reading the stored partitions
as relations, with hash aggregates rather than window sorts. Measured peak RSS of the daily
`update`: 610–640 MB with twelve seasons stored (4.3 M area-days), about 5 seconds; a first
pandas version peaked at 1.6 GB with five, so the cap is what keeps it flat as seasons are added.
With the taxon seasons and habitat fit added (2026-09-19), a five-year `update --years 2022-2026`
peaked at 644 MB in 15 seconds.

## Seasonal forecast

Open-Meteo's Seasonal Forecast API serves ECMWF's EC46 (51 members, 46 days, daily runs) and SEAS5
(7 months, monthly runs) at about 36 km. It is raw model output, not bias-corrected, and meant to be
read as an area tendency (warmer, cooler, wetter, drier than usual). mushma therefore uses its
**weekly** (EC46) and **monthly** (SEAS5) ensemble means **with their anomalies against the model's
own hindcast climate**, not the raw daily values against the ERA5 normals: comparing a coarse model
with its own climate removes most of its bias. The variables map onto the weather store's names
(`config/weather.yaml` → `seasonal`): `precipitation_mean` / `precipitation_anomaly` →
`precipitation_sum`, `temperature_2m_mean` / `temperature_2m_anomaly` → `temperature_2m_mean`.
ECMWF opened its real-time catalogue under CC BY 4.0 in October 2025; the credits page lists it.

## Outlook

For a species and area, the outlook lists the weeks starting after the 7-day forecast that end
within EC46's 46 days, then up to three months (SEAS5), clipped to the species' season window. The
periods come from the calendar, not from the stored long-range rows, so a missing fetch shows as
periods without a tendency rather than as no periods. Each period carries:

- **Past seasons.** In how many of the baseline seasons the same calendar days were good here: at
  least a quarter of the area's woodland cell-days scored 0.6 or more. Shown as a tally of dots
  ("good in 3 of 4 past seasons"), never as a chance.
- **Rain signal.** Rain over the period's **lead window** as a share of normal: the period shifted
  back by the plateau of the species' `rain_event` lag in its rule files (porcini 10–16 days,
  ovoli 10–20, gallinacci 10–30). Observed and 7-day-forecast days use the reanalysis against the
  ERA5 normals; days beyond use the long-range weeks, then months, each against its own climate,
  spread evenly over their days.
- **Tilt.** `better` when the lead-window rain is at least 125 % of normal, `worse` at 75 % or less,
  `usual` in between, `unknown` without enough days of data. The bands are in `config/history.yaml`
  with sources and a confidence (plausible, not backtested); the API returns them with the lead so
  the "how to read it" text quotes the live values.

The UI calls it an outlook, never a forecast, and draws it with a **stipple**, the second signature
next to the forecast hatch: solid is observed, hatched is forecast, stippled is outlook.

## Caching

A day's `/scores` and `/hotspots` are cached for ten minutes while the daily job still re-scores
it (today −6 to +7: new reanalysis days replace forecast weather) and for a day after that, as
history can be re-scored. Nothing is `immutable` any more: M4 marked every past day so, which was
already wrong for the six days the job re-scores. A replayed day's hotspots count only the
sightings up to that day. The web app's query cache follows the same split.

## Privacy

Sightings leave the store only as counts: per cell (as before, now also for a date span) and per
area and day in the history tables, which the API serves only as per-year and per-month totals.
Records flagged obscured count towards Tuscany but not towards a comune, because their cell is a
town centroid that may sit in the wrong comune.

## Check on real data (2026-09-18)

Run locally over the weather backfilled so far (complete 2022–2025, 2021 partial) and seasons
2022–2026 scored with the current rules:

| porcini, Tuscany | good days | typical | rain vs normal | temperature vs normal |
|---|---|---|---|---|
| 2022 | 44 | 53 | 96 % | +0.5 °C |
| 2023 | 49 | 53 | 116 % | +0.2 °C |
| 2024 | 60 | 53 | 115 % | −0.2 °C |
| 2025 | 56 | 53 | 83 % | −0.4 °C |
| 2026 to 17 Sep | 4 | 19 to date | 87 % | +1.7 °C |

The Garfagnana comuni (Careggine, Fosciandora, Pieve Fosciana) top 2024; the dry, hot 2026 reads
"worse than usual" so far, and the outlook for early October leans worse (lead-window rain about a
quarter of normal) before returning to usual by late October. The season map for one species and
year is about 870 KB of JSON and 149 KB gzipped (the API now gzips responses over 1 KB).

### Plausible species (2026-09-19)

Fit shares from the current rules and grid, and 2025 good days per taxon:

| comune | porcini | *B. edulis* | *B. pinophilus* | *B. reticulatus* | *B. aereus* | ovoli | gallinacci |
|---|---|---|---|---|---|---|---|
| Abetone Cutigliano | 100 % | 100 % (80 d) | 100 % (80 d) | 37 % (26 d) | 17 % (6 d) | 11 % (4 d) | 43 % (25 d) |
| Careggine | 100 % | 100 % (76 d) | 95 % (61 d) | 95 % (71 d) | 62 % (26 d) | 48 % (23 d) | 95 % (52 d) |
| Montalcino | 99 % | 0 % (0 d) | 0 % (0 d) | 23 % (6 d) | 98 % (39 d) | 95 % (36 d) | 87 % (39 d) |
| Tuscany | 93 % | 30 % (15 d) | 21 % (10 d) | 72 % (29 d) | 76 % (32 d) | 71 % (35 d) | 62 % (29 d) |

The porcini group is plausible almost everywhere, because *B. aereus* and *B. reticulatus* cover
the low hills that *B. edulis* and *B. pinophilus* leave out; the taxa are what tell a mountain
comune from a hill one.

## Known gaps

- Only the seasons the backfill and the history scoring have reached have stats; each response
  lists the years behind its baseline. Seasons 2016–2021 need scoring once the backfill completes.
- The seasonal forecast is area-scale (36 km): a comune's signal is mostly its region's.
- Comuni whose woodland no weather point reaches (Isola del Giglio) are left out of the area list.
- The tilt uses rain only. Temperature anomalies are shown but do not move it: their effect flips
  with the time of year (a warm October helps porcini, a hot August does not), and v1 has no cited
  rule for that.
- The web labels a season better or worse than usual at ±15 % of its typical good days: a wording
  choice beside numbers that are always shown, not a model rule.
