"""ARPA Piemonte rain gauges: the ground truth for Piemonte's reanalysis rain.

ARPA Piemonte's Meteoweb REST API (``utility.arpa.piemonte.it``, "Banca Dati Storica") serves every
station of the regional network with its position and height, and each measuring point's daily
values since the sensor started. Open data under CC BY 4.0 ("Fonte: Arpa Piemonte -
www.arpa.piemonte.it", arpa.piemonte.it/note-legali).

Per the data guide (*Banca Dati Storica — Guida alla lettura dei dati*, v1.7, 2026): the daily
precipitation is the rain and melted snow of 00:00-24:00 **UTC**, so :func:`arpal.utc_day_totals`
re-cuts the model's calendar days to match. Each value carries a class: ``M`` or ``A`` (manual or
automatic validation) then ``0``/``Z`` (recorded or computed, OK), ``*``/``Y`` (uncertain), ``X``
(not computable), ``3`` (snow melted in the gauge, possibly days later) or ``5`` (snowfall). The
check keeps rain marked OK only; a day it drops is left out of both sides of the comparison.

A measuring point (``PIE-<ISTAT comune>-<n>``) keeps its daily series when its station is renewed
or moved, so gauges are keyed by measuring point and placed at the current station.
"""

import json
from datetime import date
from pathlib import Path

import pandas as pd

API = "https://utility.arpa.piemonte.it/meteoidro"
STATIONS_URL = f"{API}/stazione_meteorologica/?format=json"
DAILY_URL = f"{API}/dati_giornalieri_meteo/"
RAIN_SENSOR = "PLUV"
VALID_RAIN = {"0", "Z"}
COLUMNS = ["code", "name", "lat", "lon", "elevation_m"]


def _measuring_point(url: str) -> str:
    """``PIE-001003-900`` from ``.../punti_misura_meteo/PIE-001003-900/?format=json``."""
    return url.rstrip("/").split("?")[0].rstrip("/").rsplit("/", 1)[-1]


def parse_stations(payload: dict) -> pd.DataFrame:
    """``code, name, lat, lon, elevation_m`` for every measuring point with a rain gauge, placed
    at its current (or latest) station."""
    rows = []
    for item in payload["results"]:
        if not any(s.get("id_parametro") == RAIN_SENSOR for s in item.get("sensori_meteo") or []):
            continue
        lat, lon = item.get("latitudine_n_wgs84_d"), item.get("longitudine_e_wgs84_d")
        if lat is None or lon is None:
            continue
        height = item.get("quota_stazione")
        rows.append(
            {
                "code": _measuring_point(item["fk_id_punto_misura_meteo"]),
                "name": item["denominazione"],
                "lat": float(lat),
                "lon": float(lon),
                "elevation_m": float(height) if height is not None else float("nan"),
                "current": item.get("data_fine") is None,
                "started": item.get("data_inizio") or "",
            }
        )
    if not rows:
        return pd.DataFrame(columns=COLUMNS)
    stations = pd.DataFrame(rows).sort_values(["code", "current", "started"])
    return stations.drop_duplicates("code", keep="last")[COLUMNS].reset_index(drop=True)


def parse_daily(pages: list[dict]) -> pd.Series:
    """One measuring point's daily rain in mm (UTC days), indexed by date, OK values only."""
    values = {}
    for page in pages:
        for row in page["results"]:
            mm, validity = row.get("ptot"), row.get("pclasse")
            if mm is None or not validity or validity[-1] not in VALID_RAIN or mm < 0:
                continue
            values[date.fromisoformat(row["data"])] = float(mm)
    return pd.Series(values, dtype="float64").sort_index()


def fetch_daily(
    code: str, start: date, end: date, cache_dir: Path
) -> list[dict]:  # pragma: no cover - network
    """Every page of one measuring point's daily values from ``start`` to ``end`` (cached)."""
    import httpx

    dest = cache_dir / f"{code}_{start:%Y%m%d}_{end:%Y%m%d}.json"
    if dest.exists():
        return json.loads(dest.read_text())
    pages = []
    url: str | None = DAILY_URL
    params: dict | None = {
        "format": "json",
        "fk_id_punto_misura_meteo": code,
        "data_min": start.isoformat(),
        "data_max": end.isoformat(),
    }
    with httpx.Client(timeout=120, headers={"User-Agent": "mushma-gauge-check/0.1"}) as client:
        while url:
            response = client.get(url, params=params)
            response.raise_for_status()
            page = response.json()
            pages.append({"results": page["results"]})
            url, params = page.get("next"), None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(pages))
    return pages
