"""SIR Toscana rain gauges: the ground truth for checking the reanalysis rain.

The Servizio Idrologico Regionale publishes every station's daily series as open JSON (CC BY-SA
4.0, Regione Toscana open data "Stazioni meteo-idrologiche"). A gauge day is the rain from 09:00
the day before to 09:00 on the day (solar time), so it does not line up with the calendar days
Open-Meteo returns: :func:`gauge_day_totals` spreads calendar-day totals over gauge days.
"""

from datetime import date, timedelta

import pandas as pd

STATIONS_URL = "http://www.sir.toscana.it/archivio/dati.php?D=json_stations"
RAIN_SERIES = "PLUVIOMETRIA - Aggregazione a 24 ore (9-9)"
# V validated, P pre-validated. N (not validated), R (reconstructed) and @ (missing) are dropped.
KEPT_QUALITY = {"V", "P"}
# Hours of a gauge day (09:00 to 09:00) that fall on the previous calendar day.
HOURS_FROM_PREVIOUS_DAY = 15


def parse_stations(payload: dict, years: set[str]) -> pd.DataFrame:
    """Rain gauges with data in every one of ``years``."""
    rows = []
    for feature in payload["features"]:
        props = feature["properties"]
        inventory = props.get("Consistenza") or {}
        series = inventory.get(RAIN_SERIES) if isinstance(inventory, dict) else None
        if not series or not years <= set(series["Anni"][0]):
            continue
        lon, lat = feature["geometry"]["coordinates"][:2]
        rows.append(
            {
                "code": props["Codice"],
                "name": props["Nome"],
                "comune": props["Comune"],
                "province": props["Provincia"],
                "elevation_m": float(props["Quota mslm"]),
                "lon": float(lon),
                "lat": float(lat),
                "url": series["SorgenteDati"],
            }
        )
    return pd.DataFrame(rows)


def parse_series(payload: dict) -> pd.Series:
    """Validated daily rain in mm, indexed by the date the gauge day ends."""
    props = payload["properties"]
    if props.get("UnitaMisura") != "mm":
        raise ValueError(f"expected rain in mm, got {props.get('UnitaMisura')!r}")
    values = {
        date.fromisoformat(item["Data"][:10]): float(item["Valore"])
        for item in props["SerieDati"]
        if item["TipoValore"] in KEPT_QUALITY and item["Valore"] is not None
    }
    return pd.Series(values, dtype="float64")


def gauge_day_totals(calendar: pd.Series) -> pd.Series:
    """Calendar-day totals re-cut into 09:00-09:00 gauge days (uniform rain within a day)."""
    share = HOURS_FROM_PREVIOUS_DAY / 24
    totals = {}
    for day, value in calendar.items():
        previous = day - timedelta(days=1)
        if previous in calendar.index:
            totals[day] = share * calendar[previous] + (1 - share) * value
    return pd.Series(totals, dtype="float64")
