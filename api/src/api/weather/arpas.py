"""ARPAS rain gauges: the ground truth for Sardinia's reanalysis rain.

ARPAS (Agenzia Regionale per la Protezione dell'Ambiente della Sardegna) publishes one table a
year of its stations' daily data on its ArcGIS Online organisation ("Rete meteo ARPAS
2016-2023", the annual "dati meteo" of the ReteUnica and ReteFiduciaria networks): one row per
station and day with the station's code, name, height and position, and the day's rain (PCG, mm)
among other variables. The data are unvalidated, CC BY-NC-ND (the 2021 item and the SIRA portal
that serves the same network say so), and the SIRA portal gives its times in UTC, so a day is a
UTC day. A station without a rain gauge, or a day it missed, has no PCG: missing, not dry. The
tables are CSV imports and repeat the header once per station block (a row whose date is
"datam"). The 2021 table has upper-case field names.
"""

import json
from datetime import date, datetime
from pathlib import Path

import pandas as pd

SERVICE_URL = (
    "https://services6.arcgis.com/VdOe78ROZ6pyB2c8/arcgis/rest/services/{service}/FeatureServer/0"
)
YEAR_SERVICES = {
    2016: "dati_arpas_meteo_2016_noblanks",
    2017: "dati_arpas_meteo_2017_noblanks",
    2018: "dati_arpas_meteo_2018_noblank",
    2019: "dati_arpas_meteo_2019_noblank",
    2020: "dati_arpas_meteo_2020_noblank",
    2021: "dati_reti_arpas_2021",
    2022: "dati_arpas_meteo_2022_noblank",
}
PAGE_SIZE = 1000  # the layers' maxRecordCount
FIELDS = {
    "cod_staz": "code",
    "stazione": "name",
    "nome": "name",
    "quota": "elevation_m",
    "wgs84_lon": "lon",
    "wgs84_lat": "lat",
    "datam": "date",
    "pcg": "mm",
}
COLUMNS = ["code", "name", "elevation_m", "lon", "lat", "date", "mm"]
STATION_COLUMNS = ["code", "name", "elevation_m", "lon", "lat"]


def year_services(start: date, end: date) -> dict[int, str]:
    """``{year: layer url}`` for every published year from ``start`` to ``end``."""
    return {
        year: SERVICE_URL.format(service=service)
        for year, service in YEAR_SERVICES.items()
        if start.year <= year <= end.year
    }


def fetch_year(layer_url: str, folder: Path) -> list[Path]:  # pragma: no cover - network
    """Page a year's table into ``folder`` once (``offset_<n>.json``); return the pages."""
    import urllib.parse

    from api.grid.sources import fetch

    pages = []
    offset = 0
    while True:
        query = urllib.parse.urlencode(
            {
                "where": "1=1",
                "outFields": "*",
                "orderByFields": "ObjectId",
                "resultOffset": offset,
                "resultRecordCount": PAGE_SIZE,
                "f": "json",
            }
        )
        path = fetch(f"{layer_url}/query?{query}", folder / f"offset_{offset:07d}.json")
        data = json.loads(path.read_text())
        if "error" in data:
            path.unlink()
            raise OSError(f"ARPAS query failed: {data['error']}")
        pages.append(path)
        count = len(data["features"])
        if not count or not data.get("exceededTransferLimit"):
            return pages
        offset += count


def parse_page(path: Path) -> pd.DataFrame:
    """Daily rain per station (``COLUMNS``) from one cached page of a year's table."""
    rows = []
    for feature in json.loads(path.read_text())["features"]:
        attributes = {
            FIELDS[k.lower()]: v for k, v in feature["attributes"].items() if k.lower() in FIELDS
        }
        if attributes.get("mm") is None or attributes.get("date") == "datam":
            continue
        rows.append(
            (
                attributes["code"],
                attributes["name"],
                float(attributes["elevation_m"]),
                float(attributes["lon"]),
                float(attributes["lat"]),
                datetime.strptime(attributes["date"], "%d/%m/%Y").date(),
                float(attributes["mm"]),
            )
        )
    daily = pd.DataFrame(rows, columns=COLUMNS)
    return daily.astype({column: "float64" for column in ("elevation_m", "lon", "lat", "mm")})


def stations_of(daily: pd.DataFrame) -> pd.DataFrame:
    """Each gauge once (``code, name, elevation_m, lon, lat``), as its first row gives it."""
    return daily.drop_duplicates("code")[STATION_COLUMNS].reset_index(drop=True)


def series_of(daily: pd.DataFrame, code: str) -> pd.Series:
    """One station's daily rain in mm, indexed by date."""
    rows = daily[daily["code"] == code]
    return pd.Series(rows["mm"].to_numpy(), index=rows["date"].to_numpy(), dtype="float64")
