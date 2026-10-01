---
order: 5120
title: [region] Friuli-Venezia Giulia rain gauge check once ARPA FVG's archive answers
status: To Do
priority: low
complexity: moderate
---
Found by `region-friuli-venezia-giulia.md` (`.gavin-root/docs/regions/friuli_venezia_giulia.md` → Validation, rain gauges).

Friuli-Venezia Giulia has no gauge fit (it shipped with its rain scale off; since 2026-10-01 it takes the national rain field from its neighbours' gauges). ARPA FVG publishes daily rain for about 60 priority stations through the OSMER archive (https://www.meteo.fvg.it/archivio.php?ln=&p=dati; the page's form POSTs to `ajax/getStationData.php` with `a` year, `m` month or 99 for all, `g` day, `s` the station option value such as `TAR@Tarvisio@syn@46.510775@13.551886@794`, `t=H_3` for daily, `ln`, `o=visualizza`). The site's content is CC BY-SA 3.0 IT (note legali: credit "ARPA FVG - OSMER e GRN" and http://www.meteo.fvg.it/). On 2026-09-27 every `ajax/*.php` call answered HTTP 400, from curl and from the site's own pages in a browser alike, so the check could not run. The daily interpolated rain (`raster.php`, `ajax/getRasterLatLon.php`, 160+ stations) is a second source once it answers.

- [ ] Confirm the archive answers again (a browser, then a script) and what a daily response looks like (the day's cut: 00-24 or 09-09, UTC or local)
- [ ] `api/src/api/weather/arpa_fvg.py` reads the stations (from the archive page's options: code, name, lat, lon, height) and each station's daily rain, test first (as `api/weather/arpa_piemonte.py` and the Bolzano reader on `region/trentino-alto-adige`); wired into `GAUGE_NETWORKS` in `api/src/api/weather/checks.py`; raw downloads cached under `$DATA_DIR/raw/arpa_fvg/`
- [ ] `api.weather.checks gauges --region friuli_venezia_giulia` over 2019-2025: pooled ratio, height bands, drizzle, window-threshold shares, a gauge-total fit (a + b x km) as the other regions did
- [ ] Add the network to `api/src/api/config/rain_field.yaml` (`networks`), run `uv run python -m api.weather.rain_field collect --network friuli_venezia_giulia` and `fit`, check `rain_field borders` (Veneto and Friuli), then re-score the history and the served window (`api.regions.onboard friuli_venezia_giulia --from score` after removing the scores), re-run the backtest and sanity, rsync the stores, and update the region doc. Since 2026-10-01 there is no per-region `precipitation_scale` block: FVG already takes the national field from its neighbours (`.gavin-root/docs/rain-scale-field.md`)
