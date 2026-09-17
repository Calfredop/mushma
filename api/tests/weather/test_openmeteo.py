import json
import threading
from datetime import UTC, date, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

from api.weather.openmeteo import (
    BudgetExhausted,
    Client,
    DailyRequest,
    RateBudget,
    RateLimited,
    parse_daily,
)

ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
FORECAST = "https://api.open-meteo.com/v1/forecast"
POINTS = [("N43.80E011.80", 43.8, 11.8), ("N43.90E011.80", 43.9, 11.8)]
UNITS = {"precipitation_sum": "mm", "temperature_2m_min": "°C"}
FETCHED = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)


def _history(points=POINTS, variables=("precipitation_sum", "temperature_2m_min"), **kw):
    defaults = dict(
        endpoint=ARCHIVE,
        model="era5_seamless",
        points=list(points),
        units={v: UNITS[v] for v in variables},
        timezone="Europe/Rome",
        start_date=date(2024, 10, 1),
        end_date=date(2024, 10, 3),
    )
    return DailyRequest(**{**defaults, **kw})


def _location(lat: float, lon: float, elevation: float, daily: dict, units: dict = UNITS) -> dict:
    return {
        "latitude": lat,
        "longitude": lon,
        "elevation": elevation,
        "timezone": "Europe/Rome",
        "daily_units": {"time": "iso8601", **{k: units[k] for k in daily if k != "time"}},
        "daily": daily,
    }


# --- requests and their weight ---------------------------------------------------------------


def test_history_request_asks_for_raw_model_cells_in_local_days() -> None:
    query = parse_qs(urlparse(_history().url()).query)

    assert query["latitude"] == ["43.8,43.9"] and query["longitude"] == ["11.8,11.8"]
    assert query["elevation"] == ["nan,nan"]
    assert query["cell_selection"] == ["nearest"]
    assert query["daily"] == ["precipitation_sum,temperature_2m_min"]
    assert query["timezone"] == ["Europe/Rome"]
    assert query["models"] == ["era5_seamless"]
    assert query["start_date"] == ["2024-10-01"] and query["end_date"] == ["2024-10-03"]
    assert query["temperature_unit"] == ["celsius"]
    assert query["precipitation_unit"] == ["mm"]
    assert query["wind_speed_unit"] == ["kmh"]


def test_forecast_request_uses_past_and_forecast_days() -> None:
    request = _history(
        endpoint=FORECAST,
        model="ecmwf_ifs",
        start_date=None,
        end_date=None,
        past_days=14,
        forecast_days=8,
    )

    query = parse_qs(urlparse(request.url()).query)

    assert query["past_days"] == ["14"] and query["forecast_days"] == ["8"]
    assert "start_date" not in query
    assert request.days == 22


def test_weight_follows_the_open_meteo_formula() -> None:
    # Open-Meteo: per location max(1, max(vars/10, vars/10 * days/14)), summed over locations.
    one_var_20_years = _history(
        points=POINTS[:1],
        variables=("precipitation_sum",),
        start_date=date(2000, 1, 1),
        end_date=date(2020, 12, 31),
    )
    eleven_vars_a_year = DailyRequest(
        endpoint=ARCHIVE,
        model="era5_seamless",
        points=POINTS[:1] * 100,
        units={f"variable_{i}": "mm" for i in range(11)},
        timezone="Europe/Rome",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
    )
    short = _history()  # 2 variables, 3 days: each location counts once

    assert one_var_20_years.weight() == pytest.approx(54.79286, rel=1e-5)
    assert eleven_vars_a_year.weight() == pytest.approx(100 * 1.1 * 365 / 14)
    assert short.weight() == 2


# --- parsing ---------------------------------------------------------------------------------


def test_parse_daily_returns_long_rows_and_model_cells() -> None:
    payload = [
        _location(
            43.800003,
            11.800003,
            850.0,
            {
                "time": ["2024-10-01", "2024-10-02"],
                "precipitation_sum": [0.8, 23.8],
                "temperature_2m_min": [8.4, None],
            },
        ),
        _location(
            43.899998,
            11.800003,
            1012.0,
            {
                "time": ["2024-10-01", "2024-10-02"],
                "precipitation_sum": [1.0, None],
                "temperature_2m_min": [7.0, 6.5],
            },
        ),
    ]

    rows, cells = parse_daily(payload, _history(), fetched_at=FETCHED)

    assert list(rows.columns) == ["source", "point_id", "date", "variable", "value", "fetched_at"]
    assert len(rows) == 6  # nulls dropped
    first = rows[(rows.point_id == "N43.80E011.80") & (rows.variable == "precipitation_sum")]
    assert list(first["date"]) == [date(2024, 10, 1), date(2024, 10, 2)]
    assert list(first["value"]) == [0.8, 23.8]
    assert set(rows["source"]) == {"era5_seamless"}
    assert cells.to_dict("records") == [
        {
            "source": "era5_seamless",
            "point_id": "N43.80E011.80",
            "model_lat": pytest.approx(43.8, abs=1e-4),
            "model_lon": pytest.approx(11.8, abs=1e-4),
            "elevation_m": 850.0,
            "fetched_at": FETCHED,
        },
        {
            "source": "era5_seamless",
            "point_id": "N43.90E011.80",
            "model_lat": pytest.approx(43.9, abs=1e-4),
            "model_lon": pytest.approx(11.8, abs=1e-4),
            "elevation_m": 1012.0,
            "fetched_at": FETCHED,
        },
    ]


def test_parse_daily_accepts_a_single_location_object() -> None:
    request = _history(points=POINTS[:1])
    daily = {"time": ["2024-10-01"], "precipitation_sum": [2.0], "temperature_2m_min": [9.0]}
    payload = _location(43.8, 11.8, 850.0, daily)

    rows, cells = parse_daily(payload, request, fetched_at=FETCHED)

    assert len(rows) == 2 and list(cells["point_id"]) == ["N43.80E011.80"]


def test_parse_daily_rejects_unexpected_units() -> None:
    daily = {"time": ["2024-10-01"], "precipitation_sum": [0.1]}
    payload = [
        _location(43.8, 11.8, 850.0, daily, {"precipitation_sum": "inch"}),
        _location(43.9, 11.8, 900.0, daily),
    ]

    with pytest.raises(ValueError, match="inch"):
        parse_daily(payload, _history(variables=("precipitation_sum",)), fetched_at=FETCHED)


def test_parse_daily_rejects_a_response_for_other_locations() -> None:
    payload = [_location(43.8, 11.8, 850.0, {"time": ["2024-10-01"], "precipitation_sum": [0.1]})]

    with pytest.raises(ValueError, match="2 locations"):
        parse_daily(payload, _history(variables=("precipitation_sum",)), fetched_at=FETCHED)


# --- rate budget -----------------------------------------------------------------------------


class FakeClock:
    def __init__(self, now: float) -> None:
        self.now = now
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


T0 = datetime(2026, 9, 17, 10, 30, 10, tzinfo=UTC).timestamp()


def test_budget_waits_for_the_next_minute_when_the_minute_is_spent() -> None:
    clock = FakeClock(T0)
    budget = RateBudget(per_minute=500, per_hour=4000, per_day=8000, clock=clock, sleep=clock.sleep)

    budget.acquire(300)
    budget.acquire(150)
    budget.acquire(300)  # 750 > 500: wait until 10:31 (plus a margin)

    assert len(clock.sleeps) == 1
    assert datetime.fromtimestamp(clock.now, UTC).minute == 31
    assert budget.used_today == 750


def test_budget_lets_one_heavy_request_through_an_empty_minute() -> None:
    clock = FakeClock(T0)
    budget = RateBudget(per_minute=500, per_hour=4000, per_day=8000, clock=clock, sleep=clock.sleep)

    budget.acquire(900)

    assert clock.sleeps == []


def test_budget_waits_for_the_next_utc_hour_when_the_hour_is_spent() -> None:
    clock = FakeClock(T0)
    budget = RateBudget(
        per_minute=5000, per_hour=1000, per_day=8000, clock=clock, sleep=clock.sleep
    )

    budget.acquire(800)
    budget.acquire(400)

    resumed = datetime.fromtimestamp(clock.now, UTC)
    assert (resumed.hour, resumed.minute) == (11, 1)


def test_budget_stops_when_the_day_is_spent_unless_told_to_wait() -> None:
    clock = FakeClock(T0)
    budget = RateBudget(
        per_minute=9000, per_hour=9000, per_day=1000, clock=clock, sleep=clock.sleep
    )
    budget.acquire(900)

    with pytest.raises(BudgetExhausted):
        budget.acquire(200)

    budget.wait_for_day = True
    budget.acquire(200)
    resumed = datetime.fromtimestamp(clock.now, UTC)
    assert (resumed.day, resumed.hour) == (18, 0)
    assert budget.used_today == 200


def test_budgets_sharing_a_ledger_count_each_others_calls(tmp_path: Path) -> None:
    clock = FakeClock(T0)
    ledger = tmp_path / "usage.json"
    limits = dict(per_minute=9000, per_hour=9000, per_day=1000, clock=clock, sleep=clock.sleep)

    RateBudget(**limits, ledger=ledger).acquire(700)
    later = RateBudget(**limits, ledger=ledger)

    assert later.used_today == 700
    with pytest.raises(BudgetExhausted):
        later.acquire(400)
    clock.now += 86400
    assert RateBudget(**limits, ledger=ledger).used_today == 0


def test_budgets_running_side_by_side_see_each_others_calls(tmp_path: Path) -> None:
    clock = FakeClock(T0)
    ledger = tmp_path / "usage.json"
    limits = dict(per_minute=9000, per_hour=9000, per_day=1000, clock=clock, sleep=clock.sleep)
    backfill = RateBudget(**limits, ledger=ledger)
    update = RateBudget(**limits, ledger=ledger)

    backfill.acquire(400)
    update.acquire(300)
    backfill.acquire(200)

    assert RateBudget(**limits, ledger=ledger).used_today == 900
    with pytest.raises(BudgetExhausted):
        update.acquire(200)


# --- client: HTTP, retries, rate limits, cache -----------------------------------------------


class FakeOpenMeteo(BaseHTTPRequestHandler):
    responses: list[tuple[int, dict]] = []
    hits: list[str] = []

    def do_GET(self) -> None:  # noqa: N802
        type(self).hits.append(self.path)
        queue = type(self).responses
        status, body = queue.pop(0) if len(queue) > 1 else queue[0]
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


OK_BODY = [
    _location(
        43.8,
        11.8,
        850.0,
        {"time": ["2024-10-01"], "precipitation_sum": [0.8], "temperature_2m_min": [8.4]},
    ),
    _location(
        43.9,
        11.8,
        1012.0,
        {"time": ["2024-10-01"], "precipitation_sum": [1.0], "temperature_2m_min": [7.0]},
    ),
]


@pytest.fixture
def server():
    FakeOpenMeteo.responses = []
    FakeOpenMeteo.hits = []
    httpd = HTTPServer(("127.0.0.1", 0), FakeOpenMeteo)
    threading.Thread(target=httpd.serve_forever, args=(0.01,), daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}/v1/archive"
    httpd.shutdown()


def _client(tmp_path: Path, clock: FakeClock, **kw) -> Client:
    budget = RateBudget(per_minute=500, per_hour=4000, per_day=8000, clock=clock, sleep=clock.sleep)
    return Client(cache_dir=tmp_path / "cache", budget=budget, sleep=clock.sleep, backoff_s=1, **kw)


def test_client_fetches_once_then_serves_the_cache(tmp_path: Path, server: str) -> None:
    FakeOpenMeteo.responses = [(200, OK_BODY)]
    clock = FakeClock(T0)
    client = _client(tmp_path, clock)
    request = _history(endpoint=server)

    first = client.fetch(request)
    second = client.fetch(request)

    assert first == second == OK_BODY
    assert len(FakeOpenMeteo.hits) == 1
    assert client.budget.used_today == request.weight()


def test_client_refetches_a_cached_response_older_than_max_age(tmp_path: Path, server: str) -> None:
    FakeOpenMeteo.responses = [(200, OK_BODY)]
    clock = FakeClock(T0)
    client = _client(tmp_path, clock, now=lambda: clock.now)
    request = _history(endpoint=server)

    client.fetch(request, max_age_s=3600)
    clock.now += 1800
    client.fetch(request, max_age_s=3600)
    clock.now += 3600
    client.fetch(request, max_age_s=3600)

    assert len(FakeOpenMeteo.hits) == 2


def test_client_forgets_a_cached_response(tmp_path: Path, server: str) -> None:
    FakeOpenMeteo.responses = [(200, OK_BODY)]
    client = _client(tmp_path, FakeClock(T0))
    request = _history(endpoint=server)

    client.fetch(request)
    client.forget(request)
    client.fetch(request)

    assert len(FakeOpenMeteo.hits) == 2


def test_client_retries_server_errors_with_backoff(tmp_path: Path, server: str) -> None:
    FakeOpenMeteo.responses = [(502, {}), (503, {}), (200, OK_BODY)]
    clock = FakeClock(T0)

    payload = _client(tmp_path, clock).fetch(_history(endpoint=server))

    assert payload == OK_BODY
    assert clock.sleeps == [1, 2]


def test_client_waits_out_a_minutely_rate_limit(tmp_path: Path, server: str) -> None:
    reason = "Minutely API request limit exceeded. Please try again in one minute."
    FakeOpenMeteo.responses = [(429, {"error": True, "reason": reason}), (200, OK_BODY)]
    clock = FakeClock(T0)

    payload = _client(tmp_path, clock).fetch(_history(endpoint=server))

    assert payload == OK_BODY
    assert datetime.fromtimestamp(clock.now, UTC).minute == 31


def test_client_stops_on_a_daily_rate_limit(tmp_path: Path, server: str) -> None:
    reason = "Daily API request limit exceeded. Please try again tomorrow."
    FakeOpenMeteo.responses = [(429, {"error": True, "reason": reason})]

    with pytest.raises(RateLimited, match="Daily"):
        _client(tmp_path, FakeClock(T0)).fetch(_history(endpoint=server))

    assert not list((tmp_path / "cache").rglob("*.json.gz"))


def test_client_reports_the_reason_of_a_bad_request(tmp_path: Path, server: str) -> None:
    reason = "Cannot initialize WeatherVariable from invalid String value rain_total"
    FakeOpenMeteo.responses = [(400, {"error": True, "reason": reason})]

    with pytest.raises(ValueError, match="rain_total"):
        _client(tmp_path, FakeClock(T0)).fetch(_history(endpoint=server))

    assert len(FakeOpenMeteo.hits) == 1
