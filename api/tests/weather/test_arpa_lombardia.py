"""ARPA Lombardia rain gauges (open data on dati.lombardia.it) for the rain check."""

import urllib.parse
from datetime import date

import pytest

from api.weather import arpa_lombardia

STATIONS = (
    '"idsensore","tipologia","unit_dimisura","idstazione","nomestazione","quota","provincia",'
    '"datastart","datastop","storico","cgb_nord","cgb_est","lng","lat","location","note"\n'
    '"2417","Precipitazione","mm","130","Brescia ITAS Pastori","149","BS",'
    '"1990-10-11T00:00:00.000",,"N","5042175","598502","10.26138219","45.52614578",'
    '"POINT (10.26138219 45.52614578)",\n'
    '"97","Precipitazione","mm","51","Tirano Madonna di Tirano","438","SO",'
    '"2002-01-01T00:00:00.000","2020-07-06T00:00:00.000","S","5118814","588943","10.15318792",'
    '"46.21708825","POINT (10.15318792 46.21708825)",\n'
)

DAILY = (
    '"idsensore","day","rain_mm","n"\n'
    '"2417","2025-10-01T00:00:00.000","0.00","144"\n'
    '"2417","2025-10-02T00:00:00.000","12.40","144"\n'
    '"2417","2025-10-03T00:00:00.000","3.00","143"\n'
    '"2417","2025-10-04T00:00:00.000","9.00","60"\n'
    '"97","2025-10-01T00:00:00.000","1.00","24"\n'
    '"97","2025-10-02T00:00:00.000","2.00","24"\n'
    '"97","2025-10-03T00:00:00.000","3.00","22"\n'
)


def test_parse_stations_reads_code_name_height_and_position() -> None:
    stations = arpa_lombardia.parse_stations(STATIONS)

    assert list(stations.columns) == ["code", "name", "elevation_m", "lon", "lat"]
    first = stations.iloc[0]
    assert first["code"] == "2417"
    assert first["name"] == "Brescia ITAS Pastori"
    assert first["elevation_m"] == 149
    assert first["lon"] == pytest.approx(10.26138219)
    assert first["lat"] == pytest.approx(45.52614578)


def test_parse_daily_reads_one_row_per_gauge_and_cet_day() -> None:
    daily = arpa_lombardia.parse_daily(DAILY)

    assert list(daily.columns) == ["code", "date", "rain_mm", "n"]
    assert daily.iloc[1].to_dict() == {
        "code": "2417",
        "date": date(2025, 10, 2),
        "rain_mm": 12.4,
        "n": 144,
    }


def test_complete_days_drops_days_short_of_the_gauges_usual_readings() -> None:
    # 10-minute gauges report 144 readings a day, hourly ones 24: each is held to its own count.
    daily = arpa_lombardia.complete_days(arpa_lombardia.parse_daily(DAILY))

    kept = {(row.code, row.date) for row in daily.itertuples()}
    assert ("2417", date(2025, 10, 3)) in kept  # 143 of 144
    assert ("2417", date(2025, 10, 4)) not in kept  # 60 of 144
    assert ("97", date(2025, 10, 3)) in kept  # 22 of 24 (92 %)


def test_daily_url_sums_valid_readings_of_one_year_from_the_right_dataset() -> None:
    older = urllib.parse.parse_qs(urllib.parse.urlsplit(arpa_lombardia.daily_url(2019)).query)
    newer = urllib.parse.urlsplit(arpa_lombardia.daily_url(2025))

    assert "2kar-pnuk" in arpa_lombardia.daily_url(2019)
    assert "pstb-pga6" in newer.path
    assert "sum(valore)" in older["$select"][0]
    where = older["$where"][0]
    assert "2019-01-01T00:00:00" in where and "2020-01-01T00:00:00" in where
    assert "valore >= 0" in where and "'VA'" in where and "'VV'" in where
    with pytest.raises(ValueError, match="2010"):
        arpa_lombardia.daily_url(2010)


def test_lombardia_reads_arpa_gauges_on_calendar_days(tmp_path) -> None:
    from api.weather.checks import GAUGE_NETWORKS

    folder = tmp_path / "arpa_lombardia"
    folder.mkdir()
    (folder / "stations.csv").write_text(STATIONS)
    (folder / "daily_2025.csv").write_text(DAILY)

    network = GAUGE_NETWORKS["lombardia"](tmp_path, date(2025, 10, 1), date(2025, 10, 4))

    assert sorted(network.gauges["code"]) == ["2417", "97"]
    gauge = next(g for g in network.gauges.itertuples() if g.code == "2417")
    assert network.series(gauge).to_dict() == {
        date(2025, 10, 1): 0.0,
        date(2025, 10, 2): 12.4,
        date(2025, 10, 3): 3.0,
    }
    calendar = network.series(gauge)
    assert network.day_totals(calendar) is calendar
