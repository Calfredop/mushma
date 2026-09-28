"""SIAS rain gauges: the ground truth for Sicily's reanalysis rain.

The Regione Siciliana's open-data portal (dati.regione.sicilia.it, CC BY 4.0) publishes the
hourly rain of the Servizio Informativo Agrometeorologico Siciliano's 96 stations ("SIAS -
Precipitazioni", unvalidated data), one zip of semicolon CSV per month from June 2019 to July
2022, and the station list with heights and positions ("Elenco sensori meteo"). Hours are in solar
time (24 rows on the daylight-saving days), so a day is its 24 hourly totals.

Only June 2019 to May 2020 are whole. From mid-2020 each monthly file holds the first few hours of
each day, so a day counts only when all 24 hours are there: a short day is missing, not dry.
January to May 2019 are listed but hold only the header.
"""

import csv
import io
import zipfile
from datetime import date
from pathlib import Path

import pandas as pd

MONTH_URL = (
    "https://dati.regione.sicilia.it/download/dataset/sias-precipitazioni/filesystem/"
    "sias-precipitazioni_csv_{label}.zip"
)
STATIONS_URL = (
    "https://dati.regione.sicilia.it/download/dataset/elenco-sensori-meteo/filesystem/"
    "elenco-sensori-meteo_csv_rsd.zip"
)
FIRST_MONTH = date(2019, 6, 1)
LAST_MONTH = date(2022, 7, 1)
RAIN_PARAMETER = "65"  # "Precipitazioni totali orarie", mm
HOURS_PER_DAY = 24
COLUMNS = ["code", "date", "mm"]


def month_urls(start: date, end: date) -> list[tuple[str, str]]:
    """``(YYYY_MM, url)`` for every published month from ``start`` to ``end``."""
    first = max(date(start.year, start.month, 1), FIRST_MONTH)
    last = min(date(end.year, end.month, 1), LAST_MONTH)
    urls = []
    month = first
    while month <= last:
        label = f"{month.year}_{month.month:02d}"
        urls.append((label, MONTH_URL.format(label=label)))
        month = date(month.year + month.month // 12, month.month % 12 + 1, 1)
    return urls


def _only_csv(archive: Path) -> io.TextIOWrapper:
    bundle = zipfile.ZipFile(archive)
    (name,) = [n for n in bundle.namelist() if n.endswith(".csv")]
    return io.TextIOWrapper(bundle.open(name), encoding="latin-1")


def parse_month(archive: Path) -> pd.DataFrame:
    """Daily rain per station (``code, date, mm``) from a monthly zip, whole days only."""
    rows = [
        (row["ID_STAZ"], row["DATARIL"][:10], float(row["VALORE"]))
        for row in csv.DictReader(_only_csv(archive), delimiter=";")
        if row["ID_PAR"] == RAIN_PARAMETER and row["VALORE"]
    ]
    if not rows:
        return pd.DataFrame(columns=COLUMNS)
    hourly = pd.DataFrame(rows, columns=["code", "day", "mm"])
    daily = hourly.groupby(["code", "day"], sort=True).agg(mm=("mm", "sum"), hours=("mm", "size"))
    daily = daily[daily["hours"] == HOURS_PER_DAY].reset_index()
    daily["date"] = [date.fromisoformat(day) for day in daily["day"]]
    return daily[COLUMNS].reset_index(drop=True)


def parse_stations(archive: Path) -> pd.DataFrame:
    """The station list: ``code, name, elevation_m, lon, lat``."""
    rows = [
        (
            row["ID_STAZ"],
            row["DESC_STAZ"],
            float(row["ALTIT"]),
            float(row["X_LON"]),
            float(row["Y_LAT"]),
        )
        for row in csv.DictReader(_only_csv(archive), delimiter=";")
    ]
    return pd.DataFrame(rows, columns=["code", "name", "elevation_m", "lon", "lat"])


def series_of(daily: pd.DataFrame, code: str) -> pd.Series:
    """One station's daily rain in mm, indexed by date."""
    rows = daily[daily["code"] == code]
    return pd.Series(rows["mm"].to_numpy(), index=rows["date"].to_numpy(), dtype="float64")
