"""Regione Umbria Servizio Idrografico rain gauges: the ground truth for Umbria's reanalysis rain.

The regional hydrographic service publishes every gauge's daily rain as open data (CC BY,
dati.regione.umbria.it, "Servizio Idrografico Dati Precipitazioni Storico" and "... Anno
Corrente"): one CSV row per rain sensor and day, ``CUMDAY`` in mm, with the station's latitude and
longitude but no height, so the check bands gauges by their grid cell's DEM height instead.

Some sensors are listed twice under two type codes with the same values, and a few stations carry
two rain sensors: a station-day is the mean of its rows. One value in the 2016+ archive is plainly
broken (7,062.8 mm at Moiano on 17 October 2017), so daily totals above ``MAX_PLAUSIBLE_MM`` are
dropped; Umbria's heaviest real days are about 250 mm.
"""

from datetime import date
from typing import IO

import pandas as pd

HISTORY_URL = (
    "https://dati.regione.umbria.it/dataset/1ebabf7c-97f6-4ec6-b716-975899140118/resource/"
    "65b788a9-0f3b-4e62-aa58-5441f9cd38e4/download/"
    "rilevazioni_precipitazioni_storico_dati_giornalieri.zip"
)
CURRENT_YEAR_URL = (
    "https://dati.regione.umbria.it/dataset/8d60fe37-7ec1-412a-abf0-25c03caaf270/resource/"
    "dc8a39db-1d1c-4b14-8e7d-ede0adc1022c/download/"
    "rilevazioni_precipitazioni_anno_corrente_dati_giornalieri.csv"
)
MAX_PLAUSIBLE_MM = 500.0
COLUMNS = ["code", "name", "comune", "lat", "lon", "date", "mm"]


def parse_daily(source: str | IO) -> pd.DataFrame:
    """Daily rain per station: ``code, name, comune, lat, lon, date, mm``, one row per day."""
    raw = pd.read_csv(source, dtype={"ID_STAZIONE": str})
    raw = raw[(raw["UNITA_MISURA"] == "mm") & raw["CUMDAY"].notna()]
    raw = raw[(raw["CUMDAY"] >= 0) & (raw["CUMDAY"] <= MAX_PLAUSIBLE_MM)]
    if raw.empty:
        return pd.DataFrame(columns=COLUMNS)
    raw = raw.assign(
        date=[
            date(int(y), int(m), int(d))
            for y, m, d in zip(raw["ANNO"], raw["MESE"], raw["GIORNO"], strict=True)
        ]
    )
    daily = (
        raw.groupby(["ID_STAZIONE", "date"], sort=True)
        .agg(
            name=("NOME_STAZIONE", "first"),
            comune=("COMUNE", "first"),
            lat=("LATITUDINE", "first"),
            lon=("LONGITUDINE", "first"),
            mm=("CUMDAY", "mean"),
        )
        .reset_index()
        .rename(columns={"ID_STAZIONE": "code"})
    )
    return daily[COLUMNS]


def gauges_covering(
    daily: pd.DataFrame, start: date, end: date, min_coverage: float = 0.8
) -> pd.DataFrame:
    """Stations with a value on at least ``min_coverage`` of the days from ``start`` to ``end``."""
    window = daily[(daily["date"] >= start) & (daily["date"] <= end)]
    needed = min_coverage * ((end - start).days + 1)
    counts = window.groupby("code")["date"].nunique()
    kept = counts[counts >= needed].index
    stations = window[window["code"].isin(kept)].drop_duplicates("code")
    return stations[["code", "name", "comune", "lat", "lon"]].reset_index(drop=True)


def series_of(daily: pd.DataFrame, code: str) -> pd.Series:
    """One station's daily rain in mm, indexed by date."""
    rows = daily[daily["code"] == code]
    return pd.Series(rows["mm"].to_numpy(), index=rows["date"].to_numpy(), dtype="float64")
