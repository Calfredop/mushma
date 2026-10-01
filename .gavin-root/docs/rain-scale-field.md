# Rain scale: one national field instead of 20 regional fits

Built 2026-10-01. Card: `[model] Rain calibration without steps at region borders`
(`plans/fix-rain-calibration-region-borders.md`). Traces to PRD → Weather (the reanalysis rain is
off against gauges), and to the region docs that each fitted their own scale.

Before scoring, the reanalysis rain is multiplied by `intercept + per_km × height (km)`, clamped at
a top height. Until now each region fitted its own `intercept` and `per_km` on its own gauges.
Neighbouring networks disagree, so the same raw rain was scaled ×1.37 on the Tuscan side of the
Umbrian border and ×1.00 across it. On 25 Sep 2026 the border band scored 0.86 against 0.47
(combined), a visible step on the map (`regions/umbria.md` → Validation). Seven other region docs
reported steps of their own.

Now one field covers Italy. At every node of a 0.25° lattice there is a local `intercept`,
`per_km` and top height, fitted on every open gauge at once. A cell reads the three bilinearly at
its own position. The field is `api/src/api/config/rain_scale_field.csv`, cited from
`model.yaml → precipitation_scale` (`field:`). No region overrides it any more.

```sh
cd api
uv run python -m api.weather.rain_field collect            # every network in config/rain_field.yaml
uv run python -m api.weather.rain_field collect --network tuscany
uv run python -m api.weather.rain_field fit                # writes config/rain_scale_field.csv
uv run python -m api.weather.rain_field borders --before <git rev>   # factors along every border
```

Intermediate files go to `$DATA_DIR/weather/rain_field/`: per-network gauge seasons, the
cross-validation scores, the fitted value at every gauge, and the border tables.

## Method

**Gauges.** Every station of the 10 networks with a parser in `api.weather.checks.GAUGE_NETWORKS`,
not only those in woodland. Each gauge's April–November total is compared with the reanalysis rain
over the same days. These are the months the scores use, and they avoid winter snow undercatch. The
rain is Open-Meteo's `era5_seamless`, downscaled to the gauge exactly as to a cell: bilinear on the
0.2° lattice of land nodes, with each network's own day cut (09–09, UTC or calendar days).
Open-Meteo serves no `era5_land` rain.

A gauge counts in a season if it reports at least 80 % of the days (70 % for Sicily). Seasons are
pooled per gauge, and gauges whose ratio falls outside 0.33–3 are dropped.

| network | years (Apr–Nov) | gauges | pooled gauge / reanalysis |
|---|---|---:|---:|
| ARPA Piemonte | 2023–2025 | 272 | 0.77 |
| Provincia di Bolzano (South Tyrol) | 2022–2024 | 43 | 0.79 |
| ARSIAL SIARL (Lazio) | 2016, 2018, 2020 | 95 | 0.91 |
| ARPAE (Emilia-Romagna) | 2023–2025 | 305 | 0.93 |
| ARPA Lombardia | 2023–2025 | 255 | 0.94 |
| Servizio Idrografico (Umbria) | 2023–2025 | 85 | 1.02 |
| ARPAL (Liguria) | 2023–2025 | 170 | 1.02 |
| SIR Toscana | 2023–2025 | 361 | 1.05 |
| SIAS (Sicily) | Jun–Nov 2019 | 95 | 1.15 |
| ARPAS (Sardinia) | 2020–2022 | 299 | 1.17 |

**Pseudo-gauges.** Six regions have no daily gauge series readable here, only yearbook totals or a
farm network: Basilicata, Calabria, Campania, Puglia, Valle d'Aosta and Veneto. Each joins as
pseudo-gauges at its own woodland cells, within the height range of its real gauges, each carrying
the region's published fit at that height. There are as many pseudo-gauges as real gauges behind
the fit (278 in all; `config/rain_field.yaml → pseudo`). Regions whose fit was borrowed (Abruzzo,
Marche, Molise) or missing (Friuli) add nothing: they take the field's value from their neighbours.

**Fit.** Each lattice node minimises

```
Σ w_i (ratio_i − a − b z_i)²  +  ridge ((a − a0)² + (b − b0)²),    w_i = exp(−d_i² / 2σ²)
```

- `(a0, b0)` is the national fit, 0.95 + 0.05 per km.
- The ridge is worth 2 gauges at distance zero, so a node far from any gauge stays near the
  national fit.
- The top height is the kernel-weighted 95th percentile of the gauge heights around the node, so
  the slope is not extrapolated above the gauges that set it.
- Every gauge weighs the same, as in Emilia-Romagna's ratio fit. This differs from Tuscany's
  original totals-through-the-origin fit.

**Choosing σ.** Each width was scored by spatial-block cross-validation: each 50 km square's gauges
are predicted from all the others, and the score is the root mean square of
`log(predicted / measured)`. A very wide kernel is one national fit; a very narrow one follows each
network. The data choose between them.

| σ | 15 km | **25 km** | 40 km | 60 km | 100 km | 200 km | national |
|---|---:|---:|---:|---:|---:|---:|---:|
| log error | 0.190 | **0.186** | 0.191 | 0.196 | 0.203 | 0.217 | 0.252 |

## The field

The intercept runs from 0.67 to 1.38 and `per_km` from −0.09 to 0.41. Far from gauges both sit at
the national value. Some examples, at 0 / 500 / 1,000 / 1,500 m:

| place | factor |
|---|---|
| Cortona (Tuscany, by the Umbrian border) | 0.88 / 0.95 / 1.01 / 1.01 |
| Lisciano Niccone (Umbria, 12 km east) | 0.89 / 0.96 / 1.01 / 1.01 |
| Abetone (Apennine ridge) | 0.92 / 1.05 / 1.17 / 1.29 |
| Monte Amiata | 0.94 / 1.04 / 1.11 / 1.11 |
| Aosta | 0.84 / 0.80 / 0.77 / 0.73 |

**Each network predicted from the others alone** (σ = 25 km, the network's own gauges left out;
log bias > 0 means the field would be too wet there):

- Within about ±0.1: Tuscany −0.00, Campania −0.01, Lombardia −0.03, Umbria −0.05, Basilicata
  −0.06, Liguria −0.10.
- Lazio +0.11, Puglia −0.12, Veneto +0.13 and South Tyrol +0.14 differ more.
- Furthest off: Sicily −0.15, Emilia-Romagna +0.17, Piemonte +0.22, Sardinia −0.25, Valle d'Aosta
  +0.31 and Calabria −0.41.

So a region without gauges takes its neighbours' level within about ±0.15 in most places, but not
everywhere. Islands, the Alps and Calabria differ from their neighbours, and only their own gauges
pin them.

## Before and after

**Along the borders.** For every pair of regions sharing a land border, `borders` puts points every
5 km along it. At each point it reads the old factor on each side and the field's, at the point's
GLO-30 height. The table shows medians over the points, the eight largest steps first; the rest are
in `borders.csv`.

| border | points | median m | before, side A | before, side B | step before | field (range) |
|---|---:|---:|---:|---:|---:|---|
| Piemonte – Liguria | 51 | 690 | ×0.74 | ×1.18 | 59 % | ×0.96 (0.88–1.16) |
| Tuscany – Lazio | 22 | 304 | ×1.37 | ×0.89 | 54 % | ×0.98 (0.91–1.04) |
| Lombardia – Emilia-Romagna | 67 | 34 | ×0.96 | ×0.65 | 49 % | ×0.71 (0.70–1.11) |
| **Tuscany – Umbria** | 31 | 324 | ×1.37 | ×1.00 | 38 % | ×0.94 (0.92–1.03) |
| Veneto – Emilia-Romagna | 21 | 2 | ×0.85 | ×0.62 | 37 % | ×0.83 (0.78–0.88) |
| Basilicata – Calabria | 27 | 821 | ×1.15 | ×1.52 | 32 % | ×1.15 (1.02–1.20) |
| Lazio – Abruzzo | 54 | 1,406 | ×1.14 | ×1.43 | 25 % | ×1.01 (0.98–1.10) |
| **Liguria – Tuscany** | 15 | 229 | ×1.09 | ×1.35 | 24 % | ×0.96 (0.89–1.23) |

With the field, both sides of a border read the same factor at the same point by construction.

**Scores in the border band.** Woodland cells within 10 km of the border on each side were scored
on one day, with the old scale and with the field, on the same weather (scratch script, local
stores). Tuscany, Umbria and Liguria have no stores on this laptop, so their border was not
re-scored here.

| border, day | before (A / B) | field (A / B) |
|---|---|---|
| Lazio / Abruzzo, 25 Sep 2026 | combined 0.13 / 0.21 | 0.12 / 0.12 |
| Lazio / Abruzzo, 20 Oct 2025 | combined 0.71 / 0.78, porcini 0.22 / 0.40 | 0.70 / 0.73, porcini 0.22 / 0.38 |
| Basilicata / Calabria, 20 Oct 2025 | combined 0.68 / 0.82, porcini 0.48 / 0.64 | 0.68 / 0.66, porcini 0.48 / 0.48 |
| Basilicata / Calabria, 25 Sep 2026 | combined 0.38 / 0.48 | 0.38 / 0.30 |

The remaining differences come from each region's own rules (season windows, habitats), not from
rain.

**Per region.** The table gives the mean factor over each region's woodland cells, or over its
gauges where its grid is not on this laptop: the old fit, the field, and the change.

| region | old | field | change |
|---|---:|---:|---:|
| Tuscany (gauges) | ×1.39 | ×1.01 | −27 % |
| Abruzzo | ×1.29 | ×1.01 | −22 % |
| Liguria (gauges) | ×1.12 | ×0.98 | −13 % |
| Friuli-Venezia Giulia | ×1.00 (off) | ×0.88 | −12 % |
| Calabria | ×1.55 | ×1.39 | −10 % |
| Campania, Molise | ×1.15, ×1.11 | ×1.06, ×1.02 | −8 % |
| Umbria, Basilicata, Puglia, Lazio, Veneto, Emilia-Romagna | | | −3 to +1 % |
| Sardinia | ×1.18 | ×1.22 | +3 % |
| Lombardia | ×0.94 | ×1.00 | +6 % |
| Piemonte (gauges) | ×0.74 | ×0.82 | +11 % |
| Trentino-Alto Adige | ×0.75 | ×0.86 | +15 % |
| Valle d'Aosta | ×0.64 | ×0.76 | +19 % |
| Sicily | ×0.96 | ×1.16 | +21 % |

The Tuscan drop is the largest, and it is real.
- The old 1.28 + 0.29 per km came from 133 woodland gauges in one year, 2025.
- Over all 361 SIR gauges in April–November, the reanalysis is about right: pooled 1.01 in 2023,
  0.99 in 2024 and 1.17 in 2025.
- `weather-ingest.md` had already found that the 2025 fit makes 2019–2025 about 16 % too wet.

Tuscany's rain-driver tuning (`mushma_rain_tuning_2026`) was done on the wetter rain, so **the
Tuscan backtest must be re-run** before the field is served.

## Known limits

- **The field is fitted on `era5_seamless` but scores CDS ERA5-Land.** Most regions' history is
  CDS (`era5_land_cds`). At their nodes, `era5_seamless` April–November rain is 0.89 (Sicily 2019)
  to 1.03 (Friuli 2024) of CDS:

  | region | seamless / CDS |
  |---|---:|
  | Sicily 2019 | 0.893 |
  | Lazio 2020 | 0.952 |
  | Sardinia 2021 | 0.954 |
  | South Tyrol 2023 | 0.964 |
  | Lombardia 2024 | 0.979 |
  | Campania 2024 | 0.983 |
  | Calabria 2024 | 0.987 |
  | Abruzzo 2024 | 0.987 |
  | Molise 2024 | 0.986 |
  | Puglia 2024 | 0.968 |
  | Basilicata 2024 | 0.993 |
  | Veneto 2024 | 0.995 |
  | Valle d'Aosta 2024 | 1.004 |
  | Friuli-Venezia Giulia 2024 | 1.031 |

  Those regions' scaled rain therefore runs up to 11 % wet (Sicily), 1–5 % in most, and about 3 %
  dry in Friuli. The fix is to fit against
  the source each region scores, or to carry a smooth seamless/CDS ratio. Follow-up card:
  `fix-rain-field-cds-vs-seamless.md`.
- **Sicily rests on one half-season** (June–November 2019): `api.weather.sias` reads June 2019 to
  June 2020 only.
- **Pseudo-gauges stand in for 278 real gauges**, carrying their region's old fit rather than
  measurements. Valle d'Aosta's own yearbook fit (0.58) is far below what its neighbours' gauges
  give (field ×0.76). The field keeps a 21 % gap to it there because the pseudo-gauges are few.
- **Totals, not timing.** As before, the scale corrects season totals. Missed convective cells
  and the wettest Prealps (`regions/veneto.md`) are not fixed by any factor.
- **Forecast rain** (`ecmwf_ifs`) is still not scaled.
