import gzip
import json
import urllib.parse
from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd
import pytest

from api.weather.config import load_weather_config
from api.weather.openmeteo import Client, RateBudget
from api.weather.seasonal import (
    SeasonalRequest,
    fetch_seasonal,
    parse_seasonal,
    seasonal_requests,
)

FETCHED = datetime(2026, 9, 18, 5, 0, tzinfo=UTC)
POINTS = [("N43.80E011.80", 43.8, 11.8), ("N43.00E011.00", 43.0, 11.0)]


def _config():
    return load_weather_config().seasonal


def _request(granularity: str = "weekly", points=POINTS) -> SeasonalRequest:
    spec = _config()
    return SeasonalRequest(
        endpoint=spec.endpoint,
        source=spec.source,
        points=points,
        granularity=granularity,
        variables=spec.variables,
        timezone="Europe/Rome",
        forecast_days=spec.forecast_days[granularity],
    )


def _weekly_location(times: list[str], precip: list, anomaly: list, temp_anom: list) -> dict:
    return {
        "latitude": 43.7,
        "longitude": 11.7,
        "elevation": 1276.0,
        "weekly_units": {
            "time": "iso8601",
            "precipitation_mean": "mm",
            "precipitation_anomaly": "mm",
            "temperature_2m_mean": "°C",
            "temperature_2m_anomaly": "K",
        },
        "weekly": {
            "time": times,
            "precipitation_mean": precip,
            "precipitation_anomaly": anomaly,
            "temperature_2m_mean": [12.0 if t is not None else None for t in temp_anom],
            "temperature_2m_anomaly": temp_anom,
        },
    }


# --- SeasonalRequest ---------------------------------------------------------------------------


def test_the_url_asks_for_the_mapped_means_and_anomalies_in_local_time() -> None:
    query = urllib.parse.parse_qs(urllib.parse.urlparse(_request().url()).query)

    assert query["latitude"] == ["43.8,43"]
    assert query["longitude"] == ["11.8,11"]
    assert query["timezone"] == ["Europe/Rome"]
    assert query["forecast_days"] == [str(_config().forecast_days["weekly"])]
    assert set(query["weekly"][0].split(",")) == {
        "precipitation_mean",
        "precipitation_anomaly",
        "temperature_2m_mean",
        "temperature_2m_anomaly",
    }
    assert "monthly" not in query


def test_a_monthly_request_asks_for_monthly_values() -> None:
    query = urllib.parse.parse_qs(urllib.parse.urlparse(_request("monthly").url()).query)

    assert "monthly" in query and "weekly" not in query


def test_the_weight_counts_every_location_like_a_daily_request() -> None:
    request = _request()
    variables = len(request.api_variables)

    per_location = max(1.0, variables / 10 * request.forecast_days / 14)
    assert request.weight() == pytest.approx(per_location * len(POINTS))


def test_requests_batch_points_under_the_weight_cap() -> None:
    config = load_weather_config()
    points = [(f"P{i}", 43.0, 11.0) for i in range(250)]

    requests = seasonal_requests(config, points, "Europe/Rome")

    assert {r.granularity for r in requests} == {"weekly", "monthly"}
    assert sum(len(r.points) for r in requests) == 2 * len(points)
    assert all(r.weight() <= config.max_request_weight for r in requests)


# --- parse_seasonal ----------------------------------------------------------------------------


def test_weekly_values_map_to_the_weather_stores_variables() -> None:
    request = _request(points=POINTS[:1])
    payload = _weekly_location(
        ["2026-09-14", "2026-09-21", "2026-11-02"],
        [19.2, 3.6, None],
        [-5.7, -21.4, None],
        [1.0, 1.9, None],
    )

    rows = parse_seasonal(payload, request, FETCHED)

    rain = rows[rows["variable"] == "precipitation_sum"].sort_values("start")
    assert rain["start"].tolist() == [date(2026, 9, 14), date(2026, 9, 21)]  # nulls dropped
    assert rain["end"].tolist() == [date(2026, 9, 20), date(2026, 9, 27)]
    assert rain["value"].tolist() == pytest.approx([19.2, 3.6])
    assert rain["anomaly"].tolist() == pytest.approx([-5.7, -21.4])
    temperature = rows[rows["variable"] == "temperature_2m_mean"]
    assert temperature["anomaly"].tolist() == pytest.approx([1.0, 1.9])
    assert set(rows["kind"]) == {"week"}
    assert set(rows["point_id"]) == {"N43.80E011.80"}
    assert set(rows["source"]) == {_config().source}


def test_monthly_periods_end_on_the_last_day_of_the_month() -> None:
    request = _request("monthly", points=POINTS[:1])
    location = _weekly_location(
        ["2026-09-01", "2027-02-01"], [68.5, 77.3], [-9.5, 12.8], [2.9, 1.2]
    )
    payload = {
        **{k: v for k, v in location.items() if not k.startswith("weekly")},
        "monthly_units": location["weekly_units"],
        "monthly": location["weekly"],
    }

    rows = parse_seasonal(payload, request, FETCHED)

    rain = rows[rows["variable"] == "precipitation_sum"].sort_values("start")
    assert rain["end"].tolist() == [date(2026, 9, 30), date(2027, 2, 28)]
    assert set(rows["kind"]) == {"month"}


def test_a_unit_other_than_the_expected_one_is_rejected() -> None:
    request = _request(points=POINTS[:1])
    payload = _weekly_location(["2026-09-14"], [1.0], [0.0], [0.0])
    payload["weekly_units"]["precipitation_mean"] = "inch"

    with pytest.raises(ValueError, match="precipitation_mean"):
        parse_seasonal(payload, request, FETCHED)


def test_a_multi_location_response_is_split_by_point() -> None:
    request = _request()
    one = _weekly_location(["2026-09-14"], [1.0], [0.5], [0.1])
    two = _weekly_location(["2026-09-14"], [2.0], [0.5], [0.1])

    rows = parse_seasonal([one, two], request, FETCHED)

    rain = rows[rows["variable"] == "precipitation_sum"].set_index("point_id")["value"]
    assert rain.to_dict() == {"N43.80E011.80": 1.0, "N43.00E011.00": 2.0}


# --- fetch_seasonal ----------------------------------------------------------------------------


def _cache(client: Client, request: SeasonalRequest, payload) -> None:
    path = client.cache_path(request)
    path.parent.mkdir(parents=True, exist_ok=True)
    envelope = {"fetched_at": FETCHED.timestamp(), "url": request.url(), "payload": payload}
    path.write_bytes(gzip.compress(json.dumps(envelope).encode()))


def test_fetch_reads_every_request_and_keeps_only_the_latest_run(tmp_path: Path) -> None:
    config = load_weather_config()
    budget = RateBudget(per_minute=500, per_hour=4500, per_day=9000)
    client = Client(cache_dir=tmp_path / "raw", budget=budget, now=lambda: FETCHED.timestamp())
    points = pd.DataFrame(
        {"point_id": ["N43.80E011.80"], "lat": [43.8], "lon": [11.8], "land": [True]}
    )
    weekly, monthly = seasonal_requests(config, [("N43.80E011.80", 43.8, 11.8)], "Europe/Rome")
    _cache(client, weekly, _weekly_location(["2026-09-14"], [1.0], [0.5], [0.1]))
    location = _weekly_location(["2026-10-01"], [60.0], [5.0], [0.3])
    _cache(
        client,
        monthly,
        {
            **{k: v for k, v in location.items() if not k.startswith("weekly")},
            "monthly_units": location["weekly_units"],
            "monthly": location["weekly"],
        },
    )

    rows = fetch_seasonal(client, config, points, "Europe/Rome", max_age_s=None)

    assert sorted(set(rows["kind"])) == ["month", "week"]
    assert client.calls == 0  # both answered from the cache
