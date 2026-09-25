"""ARPA Liguria (OMIRL network) rain gauges: ground truth for checking Liguria's reanalysis rain.

Daily rain comes from Regione Liguria's "Ambiente in Liguria – Meteo" extraction service, one CSV
per year with every station in the region; station coordinates come from the OMIRL REST API
(the ``/stations/Pluvio`` list), joined through the codes and names of the service's station list.
Terms (arpal.liguria.it → Meteo → Servizi agli utenti): "I dati e i file messi a disposizione da
Arpal sono ad accesso libero e possono essere utilizzati per consultazione o elaborazioni
automatiche […] si raccomanda di citare Arpal come fonte ufficiale."

A daily value is the rain of a UTC day (the hourly values it sums are labelled in UTC), so it starts
1 h (winter) or 2 h (summer) after the local midnight of the calendar days the weather store holds:
:func:`utc_day_totals` re-cuts calendar-day totals into UTC days.
"""

import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

import pandas as pd

if TYPE_CHECKING:
    import httpx

SERVICE = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script"
OMIRL_STATIONS_URL = "https://omirl.regione.liguria.it/Omirl/rest/stations/Pluvio"
RAIN_PARAMETER = "PRECPBIWC1"  # PRECIPITAZIONE - Precipitazione cumulata (mm)
ROME = ZoneInfo("Europe/Rome")

_ROW = re.compile(r'^"(\d\d)/(\d\d)/(\d{4})","[^"]*","([^"]*)","[^"]*","([^"]*)"')
_STATION_ROW = re.compile(
    r"<TR>\s*<TD[^>]*>\s*<a[^>]*>([^<]+)</a>\s*</TD>\s*<TD[^>]*>([^<]*)</TD>\s*<TD[^>]*>([^<]*)</TD>"
    r"\s*<TD[^>]*>([^<]*)</TD>\s*<TD[^>]*>([^<]*)</TD>",
    flags=re.IGNORECASE,
)


def parse_daily_report(text: str) -> pd.DataFrame:
    """``(station_name, date, rain_mm)`` for every valid value in a regional daily extraction."""
    rows = []
    station = None
    for line in text.splitlines():
        if line.startswith('"Stazione",'):
            station = line.split(",", 1)[1].strip().strip('"')
            continue
        match = _ROW.match(line)
        if station is None or match is None:
            continue
        day, month, year, value, valid = match.groups()
        if not value or not valid.startswith("S"):  # "Sì"; "No" marks an invalid value
            continue
        rows.append((station, date(int(year), int(month), int(day)), float(value)))
    return pd.DataFrame(rows, columns=["station_name", "date", "rain_mm"])


def parse_station_list(html: str) -> pd.DataFrame:
    """``(code, name, province, basin, elevation_m)`` from the service's station list page."""
    rows = [
        {
            "code": code.strip(),
            "name": name.strip(),
            "province": province.strip(),
            "basin": basin.strip(),
            "elevation_m": float(height) if height.strip() else float("nan"),
        }
        for code, name, province, basin, height in _STATION_ROW.findall(html)
    ]
    return pd.DataFrame(rows, columns=["code", "name", "province", "basin", "elevation_m"])


def parse_omirl_stations(payload: list[dict]) -> pd.DataFrame:
    """``(code, lat, lon, elevation_m)`` for every OMIRL rain gauge."""
    return pd.DataFrame(
        [
            {
                "code": item["shortCode"],
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "elevation_m": float(item["alt"]),
            }
            for item in payload
            if item.get("lat") is not None and item.get("lon") is not None
        ],
        columns=["code", "lat", "lon", "elevation_m"],
    )


def gauge_stations(
    report: pd.DataFrame, station_list: pd.DataFrame, omirl: pd.DataFrame
) -> pd.DataFrame:
    """Each reported station's code and position: its name in the station list, then the one code
    of that name OMIRL places. A name no code or several codes resolve is dropped."""
    names = pd.DataFrame({"name": sorted(report["station_name"].unique())})
    located = names.merge(station_list[["code", "name"]], on="name").merge(omirl, on="code")
    located = located[~located.duplicated("name", keep=False)]
    return located[["code", "name", "lat", "lon", "elevation_m"]].reset_index(drop=True)


def utc_day_totals(calendar: pd.Series) -> pd.Series:
    """Local calendar-day totals re-cut into UTC days (uniform rain within a day)."""
    totals = {}
    for day, value in calendar.items():
        following = day + timedelta(days=1)
        if following not in calendar.index:
            continue
        offset = datetime(day.year, day.month, day.day, 12, tzinfo=ROME).utcoffset()
        share = offset.total_seconds() / 86400
        totals[day] = (1 - share) * value + share * calendar[following]
    return pd.Series(totals, dtype="float64")


def _session() -> "httpx.Client":  # pragma: no cover - network
    """A cookie-keeping client: the extraction service keeps its request state in the session."""
    import httpx

    return httpx.Client(follow_redirects=True, headers={"User-Agent": "mushma-gauge-check/0.1"})


def fetch_daily_report(year: int, cache_dir: Path) -> Path:  # pragma: no cover - network
    """One year of daily rain for every station, from the extraction service (cached)."""
    dest = cache_dir / f"daily_rain_{year}.csv"
    if dest.exists():
        return dest
    session = _session()
    session.get(f"{SERVICE}/PubAccessoDatiMeteo.asp", timeout=60)
    page = session.get(f"{SERVICE}/PubAccessoDatiMeteo12.asp", timeout=60).content.decode("latin-1")
    request_id = re.search(r"NAME=IdRichiesta VALUE=(\d+)", page).group(1)
    theme = {"Frequenza": "GG", "CodTema": "REGIONE", "IdRichiesta": request_id}
    session.post(
        f"{SERVICE}/PubAccessoDatiMeteo12.asp",
        data={**theme, "Azione": "INSERISCI_TEMA", "IdRichiestaCarto": ""},
        timeout=120,
    )
    session.get(
        f"{SERVICE}/PubAccessoDatiMeteo13.asp", params={**theme, "CodUbic": ""}, timeout=120
    )
    query = {
        **theme,
        "CodParam": RAIN_PARAMETER,
        "IdEstraz": "DE",
        "TipoOutput": "XLS",
        "Separatore": ";",
        "IdRichiestaCarto": "",
        "DataIniz": f"01/01/{year}",
        "InizOra": "00:00",
        "DataFine": f"31/12/{year}",
        "FineOra": "23:59",
    }
    result = session.get(f"{SERVICE}/PubAccessoDatiMeteoPost.asp", params=query, timeout=900)
    link = re.search(r'HREF="([^"]+\.csv)"', result.content.decode("latin-1"))
    if link is None:
        raise RuntimeError(f"ARPAL extraction for {year} returned no file")
    body = session.get(link.group(1), timeout=300).content.decode("latin-1")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body)
    return dest


def fetch_station_list(cache_dir: Path) -> Path:  # pragma: no cover - network
    dest = cache_dir / "stations.html"
    if dest.exists():
        return dest
    session = _session()
    session.get(f"{SERVICE}/PubAccessoDatiMeteo.asp", timeout=60)
    page = session.get(f"{SERVICE}/PubAccessoDatiMeteo12.asp", timeout=60).content.decode("latin-1")
    request_id = re.search(r"NAME=IdRichiesta VALUE=(\d+)", page).group(1)
    listing = session.get(
        f"{SERVICE}/ListaStazioni.asp", params={"id_richiesta": request_id}, timeout=120
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(listing.content.decode("latin-1"))
    return dest
