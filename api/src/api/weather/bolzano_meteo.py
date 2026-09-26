"""South Tyrol's rain gauges: the ground truth for the Bolzano half of Trentino-Alto Adige.

The Provincia autonoma di Bolzano's Ufficio Meteorologia e prevenzione valanghe publishes one
workbook per station ("Tageswerte Temperaturen und Niederschläge", data.civis.bz.it, CC0 1.0):
the daily rain since 1981 where available, the station's ETRS89/UTM32N position and its height.
A day's rain is the total from 09:00 CET of the day before to 09:00 CET of the labelled day, the
SIR Toscana convention (:func:`api.weather.sir.gauge_day_totals` re-cuts the model's days).
A missing day is ``---``. The workbooks are read with the standard library (an xlsx is zipped XML)
so the check needs no spreadsheet dependency.
"""

import json
import re
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree

import pandas as pd
from pyproj import Transformer

PACKAGE_URL = "https://data.civis.bz.it/api/3/action/package_show?id=precipitazioni-giornaliere"
COLUMNS = ["code", "name", "lat", "lon", "elevation_m"]
_NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_REF = re.compile(r"([A-Z]+)(\d+)")
_TO_WGS84 = Transformer.from_crs(25832, 4326, always_xy=True)


def parse_resources(package: dict) -> list[tuple[str, str]]:
    """``(station code, https url)`` of every station workbook in the portal's package."""
    out = []
    for resource in package["result"]["resources"]:
        url = resource.get("url") or ""
        if not url.lower().endswith(".xlsx"):
            continue
        code = url.rsplit("/", 1)[-1].split("-", 1)[0]
        out.append((code, url.replace("http://", "https://", 1)))
    return out


def _cells(path: Path) -> dict[str, dict[int, str]]:
    """Every non-empty cell of the first sheet as text, by column letter then row number."""
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ElementTree.fromstring(zf.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.iter(f"{{{_NS['x']}}}t")) for si in root]
        sheet = ElementTree.fromstring(zf.read("xl/worksheets/sheet1.xml"))
    cells: dict[str, dict[int, str]] = {}
    for cell in sheet.iterfind(".//x:c", _NS):
        value = cell.find("x:v", _NS)
        if value is None or value.text is None:
            continue
        match = _REF.fullmatch(cell.get("r", ""))
        if match is None:
            continue
        text = shared[int(value.text)] if cell.get("t") == "s" else value.text
        cells.setdefault(match[1], {})[int(match[2])] = text
    return cells


def _number(text: str | None) -> float | None:
    try:
        return float(str(text).replace(",", "."))
    except (TypeError, ValueError):
        return None


def parse_workbook(path: Path) -> tuple[dict, pd.Series]:
    """The station (``code, name, lat, lon, elevation_m``) and its daily rain in mm, by date."""
    cells = _cells(path)
    header = cells.get("H", {})
    x = _number(header.get(8, "").removeprefix("x:"))
    y = _number(header.get(9, "").removeprefix("y:"))
    if x is None or y is None:
        raise ValueError(f"{path.name}: no station coordinates in H8/H9")
    lon, lat = _TO_WGS84.transform(x, y)
    height = _number(header.get(10))
    station = {
        "code": cells.get("C", {}).get(9, path.stem.split("-", 1)[0]),
        "name": cells.get("C", {}).get(8, ""),
        "lat": float(lat),
        "lon": float(lon),
        "elevation_m": height if height is not None else float("nan"),
    }
    rain = {}
    rain_column = cells.get("D", {})
    for row, text in cells.get("C", {}).items():
        try:
            day = datetime.strptime(text, "%d.%m.%Y").date()
        except ValueError:
            continue
        mm = _number(rain_column.get(row))
        if mm is not None and mm >= 0:
            rain[day] = mm
    return station, pd.Series(rain, dtype="float64").sort_index()


def read_network(folder: Path, fetch) -> tuple[pd.DataFrame, dict[str, pd.Series]]:
    """Every station workbook (fetched once into ``folder``): the gauges and their daily rain."""
    package = json.loads(fetch(PACKAGE_URL, folder / "package.json").read_text())
    stations, series = [], {}
    for code, url in parse_resources(package):
        station, rain = parse_workbook(fetch(url, folder / f"{code}.xlsx"))
        stations.append(station)
        series[station["code"]] = rain
    gauges = pd.DataFrame(stations, columns=COLUMNS)
    return gauges.drop_duplicates("code").reset_index(drop=True), series
