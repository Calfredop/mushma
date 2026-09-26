"""ARPA Lombardia rain gauges: ground truth for checking the reanalysis rain.

ARPA Lombardia publishes its Idro-Nivo-Meteo network on the Region's open-data portal
(dati.lombardia.it, CC0 1.0): the sensor registry (``nf78-nj6b``: sensor id, station, height,
WGS84 position) and every rain gauge's validated readings at up to 10-minute steps, one dataset per
period ("Precipitazioni dal 2011 al 2020", "Precipitazioni dal 2021"). A reading is stamped in CET
(solar time) at the end of its interval. The portal's SoQL sums the valid readings into days
server side, one request per year, and counts them: a day is kept when the gauge sent at least 90 %
of its usual count (144 for a 10-minute gauge, 24 for an hourly one). Days are CET calendar days,
the model's local days (an hour apart in summer), so :func:`api.weather.checks.calendar_days`
applies.
"""

import io
import urllib.parse

import pandas as pd

PORTAL = "https://www.dati.lombardia.it/resource"
# (first year, last year or None, Socrata dataset id) of the validated rain archives.
DATASETS = ((2011, 2020, "2kar-pnuk"), (2021, None, "pstb-pga6"))
STATIONS_URL = f"{PORTAL}/nf78-nj6b.csv?" + urllib.parse.urlencode(
    {"tipologia": "Precipitazione", "$limit": 5000}
)
# VA, VV: valid; NA, NV, NC invalid, NI uncertain, ND missing. -999 marks a missing value.
VALID_STATES = ("VA", "VV")
COMPLETE_SHARE = 0.9


def dataset_for(year: int) -> str:
    for first, last, dataset in DATASETS:
        if year >= first and (last is None or year <= last):
            return dataset
    raise ValueError(f"no ARPA Lombardia rain archive wired for {year}")


def daily_url(year: int) -> str:
    """One year of every gauge's valid readings summed into CET days, with their count."""
    states = ", ".join(f"'{state}'" for state in VALID_STATES)
    query = {
        "$select": "idsensore, date_trunc_ymd(data) AS day, sum(valore) AS rain_mm, "
        "count(valore) AS n",
        "$where": f"data >= '{year}-01-01T00:00:00' AND data < '{year + 1}-01-01T00:00:00' "
        f"AND valore >= 0 AND stato IN ({states})",
        "$group": "idsensore, day",
        "$order": "idsensore, day",
        "$limit": 1_000_000,
    }
    return f"{PORTAL}/{dataset_for(year)}.csv?{urllib.parse.urlencode(query)}"


def parse_stations(text: str) -> pd.DataFrame:
    """Rain sensors: ``code`` (sensor id), ``name``, ``elevation_m``, ``lon``, ``lat``."""
    raw = pd.read_csv(io.StringIO(text), dtype={"idsensore": str})
    return pd.DataFrame(
        {
            "code": raw["idsensore"],
            "name": raw["nomestazione"],
            "elevation_m": raw["quota"],
            "lon": raw["lng"].astype(float),
            "lat": raw["lat"].astype(float),
        }
    )


def parse_daily(text: str) -> pd.DataFrame:
    """One row per gauge and CET day: ``code``, ``date``, ``rain_mm`` and the readings ``n``."""
    raw = pd.read_csv(io.StringIO(text), dtype={"idsensore": str})
    return pd.DataFrame(
        {
            "code": raw["idsensore"],
            "date": pd.to_datetime(raw["day"]).dt.date,
            "rain_mm": raw["rain_mm"].astype(float),
            "n": raw["n"].astype(int),
        }
    )


def complete_days(daily: pd.DataFrame, share: float = COMPLETE_SHARE) -> pd.DataFrame:
    """Days on which a gauge sent at least ``share`` of its usual (median) count of readings."""
    usual = daily.groupby("code")["n"].transform("median")
    return daily[daily["n"] >= share * usual].reset_index(drop=True)


def series_of(daily: pd.DataFrame, code: str) -> pd.Series:
    rows = daily[daily["code"] == code]
    return pd.Series(
        rows["rain_mm"].to_numpy(dtype="float64"), index=list(rows["date"]), dtype="float64"
    ).sort_index()
