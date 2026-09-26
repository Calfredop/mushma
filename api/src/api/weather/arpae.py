"""ARPAE Emilia-Romagna rain gauges: ground truth for checking the reanalysis rain.

ARPAE-SIMC publishes every station's observations as open data ("Meteo - dati osservati" on
dati.arpae.it, CC BY 4.0): one gzipped line-delimited JSON file per month, each line one station and
time in the DB-All.e layout (BUFR codes: B13011 precipitation in kg/m² = mm, timerange
``[1, 0, seconds]`` an accumulation ending at the line's time). A station's daily total is kept for
two day cuts; this module reads the one ending at 08:00 UTC, i.e. 09:00-09:00 CET, the same gauge
day as SIR Toscana's, so :func:`api.weather.sir.gauge_day_totals` and
:func:`api.weather.checks.compare_gauge` apply unchanged.
"""

import json
from collections.abc import Iterable
from datetime import date, datetime, timedelta

import pandas as pd

HISTORY_URL = "https://dati-simc.arpae.it/opendata/osservati/meteo/storico/{month}.json.gz"
DAILY = [1, 0, 86400]
# 08:00 UTC = 09:00 CET: the end of a 09:00-09:00 gauge day in solar time.
GAUGE_DAY_END = "T08:00:00Z"
# Citizen-science (RMAP) and urban stations are not the regional gauge networks.
EXCLUDED_NETWORKS = {"rmap", "urbane"}
STATION_COLUMNS = ["code", "name", "network", "elevation_m", "lon", "lat"]


def month_urls(start: date, end: date) -> list[tuple[str, str]]:
    """``(YYYY-MM, url)`` for every month from ``start`` to ``end``."""
    months = []
    cursor = date(start.year, start.month, 1)
    while cursor <= end:
        name = f"{cursor:%Y-%m}"
        months.append((name, HISTORY_URL.format(month=name)))
        cursor = (cursor + timedelta(days=32)).replace(day=1)
    return months


def parse_daily_rain(lines: Iterable[str]) -> pd.DataFrame:
    """One row per station and gauge day: station fields, ``date`` (day end) and ``rain_mm``."""
    rows = []
    for line in lines:
        # Cheap pre-filter: most lines are sub-daily observations.
        if "86400" not in line or GAUGE_DAY_END not in line:
            continue
        record = json.loads(line)
        if record["network"] in EXCLUDED_NETWORKS or not record["date"].endswith(GAUGE_DAY_END):
            continue
        station: dict = {}
        rain = None
        for item in record["data"]:
            values = item["vars"]
            if "timerange" not in item:
                station = values
            elif item["timerange"] == DAILY and "B13011" in values:
                rain = values["B13011"]["v"]
        if rain is None:
            continue
        rows.append(
            {
                "code": f"{record['network']}:{record['lon']}:{record['lat']}",
                "name": (station.get("B01019") or {}).get("v"),
                "network": record["network"],
                "elevation_m": (station.get("B07030") or {}).get("v"),
                "lon": record["lon"] / 1e5,
                "lat": record["lat"] / 1e5,
                "date": datetime.fromisoformat(record["date"].replace("Z", "+00:00")).date(),
                "rain_mm": float(rain),
            }
        )
    return pd.DataFrame(rows, columns=[*STATION_COLUMNS, "date", "rain_mm"])


def gauge_series(rain: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, pd.Series]]:
    """Stations (one row each) and each station's daily rain indexed by the day it ends."""
    stations = rain.drop_duplicates("code")[STATION_COLUMNS].reset_index(drop=True)
    series = {
        code: pd.Series(
            group["rain_mm"].to_numpy(dtype="float64"), index=list(group["date"]), dtype="float64"
        ).sort_index()
        for code, group in rain.groupby("code")
    }
    return stations, series
