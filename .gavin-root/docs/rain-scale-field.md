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
rain is CDS ERA5-Land, the history every region but Tuscany scores, read from the weather stores
and downscaled to the gauge exactly as to a cell: bilinear on the 0.2° lattice of land nodes, with
each network's own day cut (09–09, UTC or calendar days). A gauge's corner node that no store holds
is fetched from CDS first; every one missing on 2026-10-03 but two (Lombardia) was at sea. Until
2026-10-03 the reanalysis here was Open-Meteo's `era5_seamless` (see "CDS rain and the field").

A gauge counts in a season if it reports at least 80 % of the days (70 % for Sicily). Seasons are
pooled per gauge, and gauges whose ratio falls outside 0.33–3 are dropped.

| network | years (Apr–Nov) | gauges | pooled gauge / CDS | (gauge / `era5_seamless`) |
|---|---|---:|---:|---:|
| ARPA Piemonte | 2023–2025 | 272 | 0.77 | 0.77 |
| Provincia di Bolzano (South Tyrol) | 2022–2024 | 43 | 0.77 | 0.79 |
| ARSIAL SIARL (Lazio) | 2016, 2018, 2020 | 95 | 0.86 | 0.91 |
| ARPA Lombardia | 2023–2025 | 255 | 0.91 | 0.94 |
| ARPAE (Emilia-Romagna) | 2023–2025 | 305 | 0.94 | 0.93 |
| ARPAL (Liguria) | 2023–2025 | 171 | 1.00 | 1.02 |
| Servizio Idrografico (Umbria) | 2023–2025 | 85 | 1.02 | 1.02 |
| SIAS (Sicily) | Jun–Nov 2019 | 93 | 1.03 | 1.15 |
| SIR Toscana | 2023–2025 | 357 | 1.04 | 1.05 |
| ARPAS (Sardinia) | 2020–2022 | 299 | 1.13 | 1.17 |

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

- `(a0, b0)` is the national fit, 0.93 + 0.05 per km.
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
| log error | 0.188 | **0.184** | 0.187 | 0.191 | 0.198 | 0.213 | 0.244 |

Against `era5_seamless` (the 2026-10-01 field) the same widths scored 0.190, 0.186, 0.191, 0.196,
0.203, 0.217 and 0.252: CDS tells the gauges a little better at every width.

## The field

The intercept runs from 0.68 to 1.29 and `per_km` from −0.08 to 0.40. Far from gauges both sit at
the national value. Some examples, at 0 / 500 / 1,000 / 1,500 m:

| place | factor |
|---|---|
| Cortona (Tuscany, by the Umbrian border) | 0.88 / 0.94 / 1.00 / 1.00 |
| Lisciano Niccone (Umbria, 12 km east) | 0.89 / 0.96 / 1.01 / 1.01 |
| Abetone (Apennine ridge) | 0.90 / 1.04 / 1.18 / 1.32 |
| Monte Amiata | 0.91 / 0.98 / 1.04 / 1.04 |
| Aosta | 0.82 / 0.79 / 0.76 / 0.73 |

**Each network predicted from the others alone** (σ = 25 km, the network's own gauges left out;
log bias > 0 means the field would be too wet there):

- Within about ±0.1: Tuscany −0.00, Lombardia −0.01, Campania −0.02, Sicily −0.06, Liguria
  −0.07, Basilicata −0.07, Umbria −0.08.
- Veneto +0.12, South Tyrol +0.12, Puglia −0.14 and Lazio +0.15 differ more.
- Furthest off: Emilia-Romagna +0.17, Piemonte +0.20, Sardinia −0.22, Valle d'Aosta +0.29 and
  Calabria −0.45.

So a region without gauges takes its neighbours' level within about ±0.15 in most places, but not
everywhere. Islands, the Alps and Calabria differ from their neighbours, and only their own gauges
pin them.

## Before and after

This section is the switch to the field on 2026-10-01, when it was fitted on `era5_seamless`; the
CDS fit moves CDS rain by −11 % to +4 % along the borders (next section).

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

**Served, after the deploy** (live `/scores`, woodland within 10 km of the border, 25 Sep 2026, the
day `regions/umbria.md` measured the step; all 20 regions re-scored with the field on 1 Oct 2026):

| border | combined, before | combined, field | porcini, before | porcini, field |
|---|---|---|---|---|
| Tuscany / Umbria | 0.86 / 0.47 | 0.60 / 0.47 | 0.47 / 0.07 | 0.39 / 0.10 |
| Tuscany / Liguria | not measured | 0.91 / 0.99 | not measured | 0.56 / 0.86 |

The rain factor is now the same on both sides, so the gaps that remain come from elsewhere: each
region's own rules, and normals built from a different reanalysis (Tuscany's from `era5_seamless`,
Umbria's and Liguria's from CDS).

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

## CDS rain and the field

Card: `fix-rain-field-cds-vs-seamless.md` (2026-10-02 to 03).

The 2026-10-01 field was fitted on Open-Meteo `era5_seamless` rain, but every region except
Tuscany scores CDS ERA5-Land (`era5_land_cds`), and the two differ at the same node. Since
2026-10-03 the gauges are compared with CDS (Method), so CDS rows take the field alone.
`era5_seamless` rows also take CDS / `era5_seamless` at the cell: `model.yaml →
precipitation_scale.source_ratios` points `era5_seamless` at `config/rain_cds_per_seamless.csv`, a
lattice on the 0.2° weather points. Those rows are Tuscany's history, and every region's last few
reanalysis days, because CDS runs about 5 days behind.

```sh
cd api
uv run python -m api.weather.rain_field cds    # every local CDS store, plus config cds_fetch
uv run python -m api.weather.rain_field fit    # also writes config/rain_cds_per_seamless.csv
```

**Measured.** `cds` sums April–November rain 2019–2025 of both sources at every land node of all
20 regions (892 nodes), over the days both have. The CDS side is the region's local store. Six
regions' stores live only on the server (Tuscany, Umbria, Liguria, Emilia-Romagna, Piemonte,
Marche), so their nodes were fetched from the CDS time-series product into
`$DATA_DIR/weather/rain_field/cds_store/`. The `era5_seamless` side comes from the Open-Meteo
archive.

| region | nodes | seamless / CDS |
|---|---:|---:|
| Sicily | 66 | 0.905 |
| Puglia | 63 | 0.949 |
| Basilicata | 51 | 0.955 |
| Trentino-Alto Adige | 81 | 0.960 |
| Lombardia | 101 | 0.961 |
| Calabria | 48 | 0.965 |
| Lazio | 81 | 0.966 |
| Marche | 34 | 0.971 |
| Campania | 60 | 0.973 |
| Tuscany | 91 | 0.975 |
| Abruzzo | 55 | 0.976 |
| Sardinia | 61 | 0.977 |
| Valle d'Aosta | 27 | 0.977 |
| Molise | 32 | 0.979 |
| Liguria | 32 | 0.982 |
| Umbria | 30 | 0.983 |
| Emilia-Romagna | 93 | 0.989 |
| Veneto | 69 | 0.990 |
| Piemonte | 87 | 0.994 |
| Friuli-Venezia Giulia | 50 | 1.027 |

What the measurement shows:

- **`era5_seamless` rain is coarse ERA5.** 60 % of nodes share their season total exactly with a
  neighbour, in blocks on the 0.2° lattice; for CDS it is 8 %. So a node's ratio is mostly the
  ERA5 block against ERA5-Land's own 0.1° rain. In Valle d'Aosta one node reads CDS / seamless
  0.63 and the next one east 1.28. That is why the fit runs on CDS. Applied to CDS rows, this ratio would
  have put the blocks into every region's history. Applied to `era5_seamless` rows, it takes them
  out.
- **A node's ratio is its own.** Sicily's 2019–2021 and 2023–2025 node ratios agree at r 0.90
  (rms 0.06 in log, against a spread between nodes of 0.12). The lattice keeps each node's own
  value:
  - smoothed by an 8 km Gaussian, which moves a node by rms 0.014 in log;
  - pulled to 1 by a ridge worth 0.01 nodes, so a point 30 km or more from any node gets no
    correction (1,323 of the 3,599 lattice points are corrected, 0.72–1.42).
- **There is a year effect.** Most regions read about 0.95 in 2019–2021 and about 0.98–1.00 in
  2022–2025: Sicily 0.87–0.94, Tuscany 0.95–1.00. The pooled 2019–2025 ratio averages it.
- **The pseudo-gauges need no conversion.** Their six fits (`rain_field.yaml → pseudo`) were made
  against CDS already.

**What changes.**

- Gauge / CDS is within 5 % of gauge / seamless for most networks. Sicily moves most: 1.03 against
  1.15. Fitted on `era5_seamless`, Sicily's CDS rain ran about 12 % wet, the gap the card was
  opened for.
- The field reads 0.92–1.09 on Etna (0 to 1,500 m), against 1.10–1.24 before.
- Along the borders, the factor CDS rain gets moves by −11 % to +4 % (`borders --before HEAD`,
  `before_cds` / `after_cds`). Most borders stay within ±5 %. The largest move is the high-Alpine
  Lombardia – Trentino-Alto Adige border, at 2,600 m: −11 %. Then come Tuscany – Lazio, −5 %, and
  Umbria – Lazio and Lazio – Abruzzo, −4 %.

**Normals follow their source.** The rain normals now name the source most of a point's days came
from (`daily_normals`, column `source`), and a cell's rain normal is scaled as that source's rain,
so percent-of-normal does not depend on the scale. Tuscany's normals are `era5_seamless`; the other
regions' are CDS. Normals written before the column existed count as the Open-Meteo archive. So
each CDS region's normals have to be rebuilt (`api.history.build normals`, which `history update`
runs) before scores that read them are trusted. The time views' area rain (`api.history.build`)
scales each source with its own factor in the same way.

**Sicily, re-scored** (laptop, 2026-10-03, the largest gap). The history was scored from 18 March
2016 to 2 October 2026 on the CDS fit, then the train backtest and the sanity check were run
(`cds-field`). They are compared with the same run on the field fitted on `era5_seamless`
(`field-seamless`, 2026-10-02).

- Sanity check: 12 of 14 contrasts hold, against 13. The one that flips is Etna, Nebrodi and
  Peloritani against Sicani and Ficuzza, 1–25 October 2020: 0.565 against 0.559 before, now 0.500
  against 0.529. It was a near-tie both times. The old 0.88 + 0.10 regional fit failed the same two
  contrasts that fail now.
- The windows' means fall 3–36 % (median 7 %), as the drier CDS rain should give.
- Train backtest: only 3 porcini and 4 chanterelle presences, so it says nothing either way.
  Porcini `auc_local` is 0.46 before and after; chanterelles 0.60 and 0.56.

## Known limits

- **Sicily rests on one half-season** (June–November 2019): `api.weather.sias` reads June 2019 to
  June 2020 only.
- **Pseudo-gauges stand in for 278 real gauges**, carrying their region's old fit rather than
  measurements. Valle d'Aosta's own yearbook fit (0.58) is far below what its neighbours' gauges
  give (field ×0.76). The field keeps a 21 % gap to it there because the pseudo-gauges are few.
- **Totals, not timing.** As before, the scale corrects season totals. Missed convective cells
  and the wettest Prealps (`regions/veneto.md`) are not fixed by any factor.
- **Forecast rain** (`ecmwf_ifs`) is still not scaled.
