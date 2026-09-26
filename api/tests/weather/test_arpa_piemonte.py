from datetime import date

import pytest

from api.weather.arpa_piemonte import parse_daily, parse_stations

BASE = "https://utility.arpa.piemonte.it/meteoidro"


def station(
    code: str,
    name: str,
    *,
    started: str = "1993-07-22",
    ended: str | None = None,
    sensors: tuple[str, ...] = ("PLUV", "TERMA"),
    lat: float = 45.3125,
    lon: float = 7.31028,
    height: int | None = 1006,
) -> dict:
    return {
        "url": f"{BASE}/stazione_meteorologica/{code}-{started}/?format=json",
        "sensori_meteo": [
            {"id_parametro": parameter, "data_inizio": started, "data_fine": None}
            for parameter in sensors
        ],
        "denominazione": name,
        "longitudine_e_wgs84_d": lon,
        "latitudine_n_wgs84_d": lat,
        "quota_stazione": height,
        "data_inizio": started,
        "data_fine": ended,
        "fk_id_punto_misura_meteo": f"{BASE}/punti_misura_meteo/{code}/?format=json",
    }


def day(when: str, mm: float | None, validity: str | None = "MZ") -> dict:
    return {"data": when, "ptot": mm, "pclasse": validity, "tmin": 3.0, "tclasse": "MZ00"}


def test_parse_stations_reads_rain_gauges_by_measuring_point() -> None:
    gauges = parse_stations({"results": [station("PIE-001003-900", "ALA DI STURA")]})

    assert list(gauges.columns) == ["code", "name", "lat", "lon", "elevation_m"]
    assert gauges.to_dict("records") == [
        {
            "code": "PIE-001003-900",
            "name": "ALA DI STURA",
            "lat": pytest.approx(45.3125),
            "lon": pytest.approx(7.31028),
            "elevation_m": 1006.0,
        }
    ]


def test_parse_stations_skips_stations_without_a_rain_gauge_or_position() -> None:
    gauges = parse_stations(
        {
            "results": [
                station("PIE-001010-900", "ANDRATE", sensors=("TERMA", "IGRO")),
                {**station("PIE-001011-900", "NOWHERE"), "latitudine_n_wgs84_d": None},
                station("PIE-001012-900", "KEPT"),
            ]
        }
    )

    assert gauges["code"].tolist() == ["PIE-001012-900"]


def test_parse_stations_keeps_the_current_station_of_a_moved_measuring_point() -> None:
    gauges = parse_stations(
        {
            "results": [
                station("PIE-004003-900", "OLD SITE", started="1990-01-01", ended="2012-05-31"),
                station("PIE-004003-900", "NEW SITE", started="2012-06-01", height=640),
            ]
        }
    )

    assert gauges["name"].tolist() == ["NEW SITE"]
    assert gauges["elevation_m"].tolist() == [640.0]


def test_parse_daily_keeps_rain_marked_ok() -> None:
    series = parse_daily(
        [
            {"results": [day("2025-06-01", 0.0), day("2025-06-02", 12.8, "AZ")]},
            {"results": [day("2025-06-03", 3.2, "M0")]},
        ]
    )

    assert series.index.tolist() == [date(2025, 6, 1), date(2025, 6, 2), date(2025, 6, 3)]
    assert series.tolist() == [0.0, 12.8, 3.2]
    assert series.dtype == "float64"


def test_parse_daily_drops_missing_uncertain_and_snow_days() -> None:
    series = parse_daily(
        [
            {
                "results": [
                    day("2025-01-01", None, None),  # no value
                    day("2025-01-02", 4.0, "MY"),  # calculated, uncertain
                    day("2025-01-03", 4.0, "A*"),  # recorded, uncertain
                    day("2025-01-04", 4.0, "MX"),  # not computable
                    day("2025-01-05", 9.0, "M3"),  # melted snow, possibly days later
                    day("2025-01-06", 6.0, "M5"),  # snowfall caught by the gauge
                    day("2025-01-07", -1.0, "MZ"),
                    day("2025-01-08", 2.0, "MZ"),
                ]
            }
        ]
    )

    assert series.index.tolist() == [date(2025, 1, 8)]
