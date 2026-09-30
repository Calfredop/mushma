import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from api.weather.arpas import YEAR_SERVICES, parse_page, series_of, stations_of, year_services


def page(tmp_path: Path, rows: list[dict], name: str = "offset_0000000.json") -> Path:
    path = tmp_path / name
    path.write_text(json.dumps({"features": [{"attributes": row} for row in rows]}))
    return path


def row(code: str, day: str, mm: float | None, **extra: object) -> dict:
    return {
        "Cod_Staz": code,
        "Stazione": "ABBASANTARF",
        "wgs84_lon": 8.81417,
        "wgs84_lat": 40.13027,
        "quota": "328",
        "datam": day,
        "PCG": mm,
        **extra,
    }


def test_parse_page_reads_daily_rain_per_station(tmp_path: Path) -> None:
    daily = parse_page(page(tmp_path, [row("OR009B501", "02/11/2019", 12.4)]))

    assert list(daily.columns) == ["code", "name", "elevation_m", "lon", "lat", "date", "mm"]
    first = daily.iloc[0]
    assert (first["code"], first["name"], first["date"]) == (
        "OR009B501",
        "ABBASANTARF",
        date(2019, 11, 2),
    )
    assert (first["elevation_m"], first["mm"]) == pytest.approx((328.0, 12.4))
    assert (first["lon"], first["lat"]) == pytest.approx((8.81417, 40.13027))


def test_parse_page_drops_missing_rain_and_the_repeated_header_rows(tmp_path: Path) -> None:
    """A station without a rain gauge, or a day it missed, has no PCG: missing, not dry. The
    tables also hold a copy of the CSV header per station block (datam = "datam")."""
    rows = [
        row("OR009B501", "02/11/2019", None),
        row("datam", "datam", None),
        row("OR009B501", "03/11/2019", 0.0),
    ]

    daily = parse_page(page(tmp_path, rows))

    assert daily["date"].tolist() == [date(2019, 11, 3)]
    assert daily["mm"].tolist() == [0.0]


def test_parse_page_drops_negative_rain(tmp_path: Path) -> None:
    """La Maddalena's gauge logs -8920.4 mm one day: an error code, not rain."""
    rows = [row("SS002B532", "02/11/2019", -8920.4), row("SS002B532", "03/11/2019", 4.0)]

    daily = parse_page(page(tmp_path, rows))

    assert daily["mm"].tolist() == [4.0]


def test_parse_page_reads_the_2021_tables_upper_case_fields(tmp_path: Path) -> None:
    rows = [
        {
            "COD_STAZ": "NU010B501",
            "NOME": "BITTI",
            "WGS84_LON": 9.38,
            "WGS84_LAT": 40.48,
            "QUOTA": "549",
            "DATAM": "28/11/2021",
            "PCG": 3.2,
        }
    ]

    daily = parse_page(page(tmp_path, rows))

    assert daily["code"].tolist() == ["NU010B501"]
    assert daily["elevation_m"].tolist() == [549.0]
    assert daily["date"].tolist() == [date(2021, 11, 28)]


def test_parse_page_reads_an_empty_page(tmp_path: Path) -> None:
    daily = parse_page(page(tmp_path, []))

    assert daily.empty
    assert list(daily.columns) == ["code", "name", "elevation_m", "lon", "lat", "date", "mm"]
    assert daily[["elevation_m", "lon", "lat", "mm"]].dtypes.eq("float64").all()


def test_stations_of_lists_each_gauge_once() -> None:
    daily = pd.DataFrame(
        {
            "code": ["A", "A", "B"],
            "name": ["ONE", "ONE", "TWO"],
            "elevation_m": [10.0, 10.0, 900.0],
            "lon": [9.0, 9.0, 9.2],
            "lat": [40.0, 40.0, 40.1],
            "date": [date(2019, 1, 1), date(2019, 1, 2), date(2019, 1, 1)],
            "mm": [0.0, 1.0, 2.0],
        }
    )

    stations = stations_of(daily)

    assert list(stations.columns) == ["code", "name", "elevation_m", "lon", "lat"]
    assert stations["code"].tolist() == ["A", "B"]


def test_series_of_indexes_one_stations_days() -> None:
    daily = pd.DataFrame(
        {
            "code": ["A", "B", "A"],
            "date": [date(2019, 11, 2), date(2019, 11, 2), date(2019, 11, 3)],
            "mm": [5.0, 0.0, 1.5],
        }
    )

    assert series_of(daily, "A").to_dict() == {date(2019, 11, 2): 5.0, date(2019, 11, 3): 1.5}


def test_year_services_cover_the_published_years_in_the_range() -> None:
    assert list(year_services(date(2015, 6, 1), date(2017, 2, 1))) == [2016, 2017]
    assert list(year_services(date(2023, 1, 1), date(2024, 1, 1))) == []
    assert set(YEAR_SERVICES) == set(range(2016, 2023))
