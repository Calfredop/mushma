---
order: 5120
title: [region] Friuli-Venezia Giulia rain gauge check once ARPA FVG's archive answers
status: To Do
priority: low
complexity: moderate
---
Found by `region-friuli-venezia-giulia.md` (`.gavin-root/docs/regions/friuli_venezia_giulia.md` → Validation, rain gauges).

Friuli-Venezia Giulia has no gauge fit (it shipped with its rain scale off; since 2026-10-01 it takes the national rain field from its neighbours' gauges). ARPA FVG publishes daily rain for about 60 priority stations through the OSMER archive (https://www.meteo.fvg.it/archivio.php?ln=&p=dati; the page's form POSTs to `ajax/getStationData.php` with `a` year, `m` month or 99 for all, `g` day, `s` the station option value such as `TAR@Tarvisio@syn@46.510775@13.551886@794`, `t=H_3` for daily, `ln`, `o=visualizza`). The site's content is CC BY-SA 3.0 IT (note legali: credit "ARPA FVG - OSMER e GRN" and http://www.meteo.fvg.it/). On 2026-09-27 every `ajax/*.php` call answered HTTP 400, from curl and from the site's own pages in a browser alike, so the check could not run. The daily interpolated rain (`raster.php`, `ajax/getRasterLatLon.php`, 160+ stations) is a second source once it answers.

**Re-checked 2026-10-02: still down.** `archivio.php` loads (200) and its station list is intact (`<option data-start="YYYY" value="CODE@Name@syn@lat@lon@height">`, retired stations named "(fino al dd/mm/yyyy)"). But `ajax/getStationData.php` and `ajax/getRasterLatLon.php` answer 400 "Bad Request" to every request: from curl with the session cookie, `X-Requested-With` and Referer set, and from the archive page itself in Chrome (same-origin fetch, daily `H_3` and hourly `H_2`, one month or `99`). The 400 comes from PHP (it sets `PHPSESSID`), not Apache: an unknown `ajax/*.php` answers 302. No fallback exists. The regional open-data portal (dati.friuliveneziagiulia.it) has only stale OSMER sets ("Meteo - dati delle stazioni regionali", last updated 2016-08) and a 2019 sensor list, with no daily rain. The first item stays open.

**Next check: on or after 2026-10-23** (the human chose to wait, 2026-10-02). The quick test is one POST to `ajax/getStationData.php` with the Tarvisio station above, `a=2024 m=10 g=1 t=H_3 ln= o=visualizza`. While it answers 400, put the card back in To Do with the date of the check. Once it answers, carry on down the checklist. A one-time cloud routine runs this check at 2026-10-23 09:00 Europe/Rome and reports only, without editing the card: https://claude.ai/code/routines/trig_01S6KTk3LQ8e2SihzumcWj1A

- [ ] Confirm the archive answers again (a browser, then a script) and what a daily response looks like (the day's cut: 00-24 or 09-09, UTC or local)
- [ ] `api/src/api/weather/arpa_fvg.py` reads the stations (from the archive page's options: code, name, lat, lon, height) and each station's daily rain, test first (as `api/weather/arpa_piemonte.py` and the Bolzano reader on `region/trentino-alto-adige`); wired into `GAUGE_NETWORKS` in `api/src/api/weather/checks.py`; raw downloads cached under `$DATA_DIR/raw/arpa_fvg/`
- [ ] `api.weather.checks gauges --region friuli_venezia_giulia` over 2019-2025: pooled ratio, height bands, drizzle, window-threshold shares, a gauge-total fit (a + b x km) as the other regions did
- [ ] Add the network to `api/src/api/config/rain_field.yaml` (`networks`), run `uv run python -m api.weather.rain_field collect --network friuli_venezia_giulia` and `fit`, check `rain_field borders` (Veneto and Friuli), then re-score the history and the served window (`api.regions.onboard friuli_venezia_giulia --from score` after removing the scores), re-run the backtest and sanity, rsync the stores, and update the region doc. Since 2026-10-01 there is no per-region `precipitation_scale` block: FVG already takes the national field from its neighbours (`.gavin-root/docs/rain-scale-field.md`)
- [x] Decision: ARPA FVG's OSMER archive has answered HTTP 400 since at least 2026-09-27, in a browser too, and there is no other source of daily FVG rain. What now? FVG already takes the national rain field from its neighbours' gauges.
  Options: A) Keep waiting; re-check in a few weeks B) Email ARPA FVG OSMER to report the broken archive / ask for a 2019-2025 daily rain export C) Close the card: the national field from the neighbours is enough
  Answer (2026-10-02): Keep waiting; re-check in a few weeks
