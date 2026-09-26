import json
from datetime import date

import pytest

from api.weather.arpae import gauge_series, month_urls, parse_daily_rain


def _record(
    network: str,
    lon: int,
    lat: int,
    when: str,
    name: str,
    height: float,
    daily: float | None,
    hourly: float = 0.2,
) -> str:
    data = [
        {
            "vars": {
                "B01019": {"v": name},
                "B05001": {"v": lat / 1e5},
                "B06001": {"v": lon / 1e5},
                "B07030": {"v": height},
            }
        },
        {
            "timerange": [1, 0, 3600],
            "level": [1, None, None, None],
            "vars": {"B13011": {"v": hourly}},
        },
        {
            "timerange": [0, 0, 900],
            "level": [103, 2000, None, None],
            "vars": {"B12101": {"v": 288.15}},
        },
    ]
    if daily is not None:
        data.append(
            {
                "timerange": [1, 0, 86400],
                "level": [1, None, None, None],
                "vars": {"B13011": {"v": daily}},
            }
        )
    return json.dumps(
        {"version": "0.1", "network": network, "lon": lon, "lat": lat, "date": when, "data": data}
    )


LINES = [
    # 08:00 UTC closes the 09:00-09:00 (CET) gauge day that ends on 1 October.
    _record("simnpr", 1036000, 4448000, "2025-10-01T08:00:00Z", "Bosco di Corniglio", 983.0, 12.4),
    # The same station's 00-24 UTC total is a different day and is not kept.
    _record("simnpr", 1036000, 4448000, "2025-10-02T00:00:00Z", "Bosco di Corniglio", 983.0, 30.0),
    _record("simnpr", 1036000, 4448000, "2025-10-02T08:00:00Z", "Bosco di Corniglio", 983.0, 0.0),
    # Sub-daily records carry no daily total.
    _record("simnpr", 1036000, 4448000, "2025-10-02T09:00:00Z", "Bosco di Corniglio", 983.0, None),
    _record("agrmet", 1016786, 4500695, "2025-10-01T08:00:00Z", "Zibello", 31.0, 3.0),
    # Citizen and urban networks are left out.
    _record("rmap", 1100000, 4450000, "2025-10-01T08:00:00Z", "Garden", 50.0, 9.9),
    _record("urbane", 1134000, 4449000, "2025-10-01T08:00:00Z", "Bologna urbana", 60.0, 9.9),
]


def test_parse_daily_rain_keeps_the_0800_utc_gauge_days() -> None:
    rain = parse_daily_rain(LINES)

    assert sorted(rain["network"].unique()) == ["agrmet", "simnpr"]
    corniglio = rain[rain["name"] == "Bosco di Corniglio"].set_index("date")
    assert corniglio["rain_mm"].to_dict() == {date(2025, 10, 1): 12.4, date(2025, 10, 2): 0.0}
    first = corniglio.iloc[0]
    assert first["lon"] == pytest.approx(10.36)
    assert first["lat"] == pytest.approx(44.48)
    assert first["elevation_m"] == 983.0
    assert first["code"] == "simnpr:1036000:4448000"


def test_gauge_series_splits_stations_from_their_daily_rain() -> None:
    stations, series = gauge_series(parse_daily_rain(LINES))

    assert set(stations["code"]) == {"simnpr:1036000:4448000", "agrmet:1016786:4500695"}
    assert list(stations.columns) == ["code", "name", "network", "elevation_m", "lon", "lat"]
    assert series["agrmet:1016786:4500695"].to_dict() == {date(2025, 10, 1): 3.0}


def test_month_urls_cover_the_months_of_a_range() -> None:
    urls = month_urls(date(2025, 11, 20), date(2026, 1, 3))

    assert [name for name, _ in urls] == ["2025-11", "2025-12", "2026-01"]
    assert urls[0][1].endswith("/opendata/osservati/meteo/storico/2025-11.json.gz")
