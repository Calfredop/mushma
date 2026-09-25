import json
import threading
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import duckdb
import pandas as pd
import pytest

from api.weather.config import load_weather_config
from api.weather.ingest import backfill, build_points, history_requests, update
from api.weather.openmeteo import MAX_SLEEP_S, Client, RateBudget
from api.weather.store import WeatherStore

TODAY = date(2026, 9, 17)
UNITS = {
    "precipitation_sum": "mm",
    "temperature_2m_mean": "°C",
    "soil_moisture_0_to_7cm_mean": "m³/m³",
}


class FakeOpenMeteo(BaseHTTPRequestHandler):
    """Synthetic daily weather: value = latitude + day of month; nodes north of 44.05 are sea."""

    hits: list[dict] = []
    # The archive has no data from this day on (reanalysis delay).
    archive_until = TODAY - timedelta(days=6)

    def do_GET(self) -> None:  # noqa: N802
        query = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
        type(self).hits.append(query)
        variables = query["daily"].split(",")
        if "start_date" in query:
            first = date.fromisoformat(query["start_date"])
            last = date.fromisoformat(query["end_date"])
        else:
            first = TODAY - timedelta(days=int(query["past_days"]))
            last = TODAY + timedelta(days=int(query["forecast_days"]) - 1)
        days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
        forecast = "archive" not in self.path
        locations = []
        lats = [float(v) for v in query["latitude"].split(",")]
        lons = [float(v) for v in query["longitude"].split(",")]
        for lat, lon in zip(lats, lons, strict=True):
            sea = lat > 44.05

            def value(day: date, lat: float = lat, sea: bool = sea) -> float | None:
                if sea or (not forecast and day >= type(self).archive_until):
                    return None
                return round(lat + day.day + (0.5 if forecast else 0.0), 2)

            locations.append(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "elevation": 0.0 if sea else 500.0 + (100.0 if forecast else 0.0),
                    "daily_units": {"time": "iso8601", **{v: UNITS[v] for v in variables}},
                    "daily": {
                        "time": [d.isoformat() for d in days],
                        **{v: [value(d) for d in days] for v in variables},
                    },
                }
            )
        body = json.dumps(locations if len(locations) > 1 else locations[0]).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def base_url():
    FakeOpenMeteo.hits = []
    FakeOpenMeteo.archive_until = TODAY - timedelta(days=6)
    httpd = HTTPServer(("127.0.0.1", 0), FakeOpenMeteo)
    threading.Thread(target=httpd.serve_forever, args=(0.01,), daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()


def _config(base_url: str, **budget):
    config = load_weather_config()
    history = replace(
        config.history, endpoint=f"{base_url}/v1/archive", start_date=date(2024, 11, 1)
    )
    forecast = replace(
        config.forecast, endpoint=f"{base_url}/v1/forecast", past_days=7, forecast_days=3
    )
    return replace(
        config,
        points=replace(config.points, stride=1, max_distance_km=30),
        history=history,
        forecast=forecast,
        variables={k: v for k, v in config.variables.items() if k in UNITS},
        max_request_weight=40,
        budget=replace(config.budget, **budget),
    )


def _client(tmp_path: Path, config) -> Client:
    budget = RateBudget(
        per_minute=1e9, per_hour=1e9, per_day=config.budget.per_day, sleep=lambda s: None
    )
    return Client(cache_dir=tmp_path / "raw", budget=budget, sleep=lambda s: None)


def _cells() -> pd.DataFrame:
    # Four woodland cells around Vallombrosa and one on the ridge whose northern corners are sea.
    return pd.DataFrame(
        {
            "cell_id": ["a", "b", "c", "d", "e"],
            "lat": [43.73, 43.76, 43.84, 43.87, 44.02],
            "lon": [11.55, 11.58, 11.52, 11.56, 11.55],
            "elevation_m": [1000.0, 900.0, 700.0, 600.0, 1200.0],
            "woodland": [True, True, True, True, True],
        }
    )


def _backfill(client: Client, config, store: WeatherStore, points: pd.DataFrame, end: date):
    return backfill(client, config, store, points, "Europe/Rome", end=end, today=TODAY)


def _land_points(tmp_path: Path, base_url: str, **budget):
    config = _config(base_url, **budget)
    store = WeatherStore(tmp_path / "weather")
    client = _client(tmp_path, config)
    build_points(client, config, "Europe/Rome", _cells(), store, log=lambda m: None)
    return config, store, pd.read_parquet(store.points_path)


def test_build_points_keeps_land_nodes_and_their_weights(tmp_path: Path, base_url: str) -> None:
    config, store, points = _land_points(tmp_path, base_url)

    assert set(points["point_id"]) == {
        f"N{lat:05.2f}E{lon:06.2f}"
        for lat in (43.7, 43.8, 43.9, 44.0, 44.1)
        for lon in (11.5, 11.6)
    }
    sea = points[~points["land"]]
    assert set(sea["point_id"]) == {"N44.10E011.50", "N44.10E011.60"}
    weights = pd.read_parquet(store.weights_path)
    assert set(weights["method"]) == {"bilinear", "nearest"}
    assert not set(weights["point_id"]) & set(sea["point_id"])
    totals = weights.groupby(["method", "cell_id"])["weight"].sum()
    assert totals.to_numpy() == pytest.approx(1.0)
    probe_cells = store.read_point_cells()
    assert set(probe_cells["source"]) == {"era5_land"}
    assert FakeOpenMeteo.hits[0]["models"] == "era5_land"


def test_history_requests_run_newest_year_first_within_the_weight_limit(tmp_path: Path) -> None:
    config = _config("http://example.invalid")
    points = [(f"P{i:02d}", 43.0 + i / 10, 11.0) for i in range(12)]

    start, end = date(2023, 11, 1), date(2025, 2, 10)
    requests = history_requests(config, points, "Europe/Rome", start, end)

    spans = [(r.start_date, r.end_date) for r in requests]
    assert spans[0] == (date(2025, 1, 1), date(2025, 2, 10))
    assert spans[-1] == (date(2023, 11, 1), date(2023, 12, 31))
    assert sorted(set(spans), reverse=True) == list(dict.fromkeys(spans))
    assert all(r.weight() <= config.max_request_weight or len(r.points) == 1 for r in requests)
    assert len([r for r in requests if r.start_date.year == 2024]) == 3  # 12 x 7.8 calls / 40
    year_2024 = [p for r in requests if r.start_date.year == 2024 for p in r.points]
    assert sorted(year_2024) == points


def test_backfill_fills_the_store_and_a_rerun_fetches_nothing(
    tmp_path: Path, base_url: str
) -> None:
    config, store, points = _land_points(tmp_path, base_url)
    client = _client(tmp_path, config)
    hits_before = len(FakeOpenMeteo.hits)

    status = _backfill(client, config, store, points, end=date(2025, 3, 31))
    rerun = _backfill(client, config, store, points, end=date(2025, 3, 31))

    land = points[points["land"]]
    days = (date(2025, 3, 31) - date(2024, 11, 1)).days + 1
    count = duckdb.execute(f"SELECT count(*) FROM read_parquet('{store.daily_glob}')").fetchone()
    assert status.done and rerun.done
    assert count == (len(land) * days * len(UNITS),)
    assert rerun.fetched == 0
    assert len(FakeOpenMeteo.hits) - hits_before == status.fetched
    value = duckdb.execute(
        f"SELECT value FROM read_parquet('{store.daily_glob}') WHERE point_id = 'N43.80E011.60' "
        "AND date = DATE '2025-01-07' AND variable = 'precipitation_sum'"
    ).fetchone()
    assert value == (pytest.approx(43.8 + 7),)


def test_backfill_pauses_when_the_daily_budget_runs_out_and_resumes(
    tmp_path: Path, base_url: str
) -> None:
    # The 2025 chunk weighs 15.4 calls and the 2024 one 10.5: a budget of 20 stops between them.
    config, store, points = _land_points(tmp_path, base_url, per_day=20)
    end = date(2025, 3, 31)

    first = _backfill(_client(tmp_path, config), config, store, points, end=end)
    second = _backfill(_client(tmp_path, config), config, store, points, end=end)

    assert not first.done and first.fetched >= 1
    assert second.done
    count = duckdb.execute(
        f"SELECT count(DISTINCT date) FROM read_parquet('{store.daily_glob}')"
    ).fetchone()
    assert count == ((end - date(2024, 11, 1)).days + 1,)
    # Nothing fetched twice: the second run only asked for what the first did not store.
    history = [h for h in FakeOpenMeteo.hits if h["models"] == "era5_seamless"]
    assert len({h["start_date"] + h["latitude"] for h in history}) == len(history)


def test_update_adds_recent_reanalysis_and_the_forecast(tmp_path: Path, base_url: str) -> None:
    config, store, points = _land_points(tmp_path, base_url)
    client = _client(tmp_path, config)

    update(client, config, store, points, "Europe/Rome", today=TODAY)

    con = duckdb.connect()
    start, end = TODAY - timedelta(days=14), TODAY + timedelta(days=5)
    best = store.best_daily(con, start, end, config.source_order).df()
    by_day = best[best.point_id == "N43.80E011.60"].groupby("date")["source"].first()
    assert by_day[pd.Timestamp(TODAY - timedelta(days=7))] == "era5_seamless"
    assert by_day[pd.Timestamp(TODAY - timedelta(days=5))] == "ecmwf_ifs"
    assert by_day.index.max() == pd.Timestamp(TODAY + timedelta(days=2))
    assert set(store.read_point_cells()["source"]) == {"era5_land", "era5_seamless", "ecmwf_ifs"}
    archive = [h for h in FakeOpenMeteo.hits if h["models"] == "era5_seamless"]
    assert archive[0]["start_date"] == str(TODAY - timedelta(days=config.history.recent_days))


def test_a_settled_chunk_that_came_back_incomplete_is_not_kept_in_the_cache(
    tmp_path: Path, base_url: str
) -> None:
    config, store, points = _land_points(tmp_path, base_url)
    FakeOpenMeteo.archive_until = date(2025, 3, 20)  # the archive is unexpectedly late
    client = _client(tmp_path, config)

    status = _backfill(client, config, store, points, end=date(2025, 3, 31))

    assert not status.done
    assert status.incomplete
    assert not list((tmp_path / "raw" / "era5_seamless").glob("20250101-*"))


def test_run_until_done_sleeps_through_rate_limits_and_network_errors() -> None:
    from api.weather.ingest import BackfillStatus, run_until_done

    outcomes = [
        BackfillStatus(fetched=3, paused="Daily API request limit exceeded."),
        OSError("network is unreachable"),
        BackfillStatus(fetched=2),
    ]
    sleeps: list[float] = []
    now = [datetime(2026, 9, 17, 23, 0, tzinfo=UTC).timestamp()]
    started: list[datetime] = []

    def run() -> BackfillStatus:
        started.append(datetime.fromtimestamp(now[0], UTC))
        outcome = outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        now[0] += seconds

    status = run_until_done(run, sleep=sleep, clock=lambda: now[0], log=lambda m: None)

    assert status.done and status.fetched == 2
    assert started[1] == datetime(2026, 9, 18, 0, 1, 5, tzinfo=UTC)  # just after 00:00 UTC
    assert max(sleeps[:-1]) <= MAX_SLEEP_S  # short steps re-read the clock if the machine slept
    assert sleeps[-1] == 600


def test_run_until_done_gives_up_on_chunks_that_stay_incomplete() -> None:
    from api.weather.ingest import BackfillStatus, run_until_done

    calls = []

    def run() -> BackfillStatus:
        calls.append(1)
        return BackfillStatus(incomplete=["20250101-20251231"])

    status = run_until_done(run, sleep=lambda s: None, clock=lambda: 0.0, log=lambda m: None)

    assert not status.done and len(calls) == 3


def test_write_meta_records_the_credits_the_app_must_show(tmp_path: Path) -> None:
    from api.weather.ingest import write_meta

    store = WeatherStore(tmp_path / "weather")

    path = write_meta(load_weather_config(), store, region="tuscany")

    meta = json.loads(path.read_text())
    credits = meta["sources"]
    assert credits["open_meteo"]["attribution"] == "Weather data by Open-Meteo.com, CC BY 4.0"
    assert credits["open_meteo"]["homepage"] == "https://open-meteo.com/"
    assert credits["copernicus_era5_land"]["license"] == "CC BY 4.0"
    assert set(credits) == {
        "open_meteo",
        "copernicus_era5_land",
        "copernicus_cds",
        "ecmwf_open_data",
    }
    assert meta["history"]["model"] == "era5_seamless" and meta["forecast"]["model"] == "ecmwf_ifs"
    assert meta["cds"]["model"] == "era5_land_cds"
    assert meta["source_order"] == ["era5_land_cds", "era5_seamless", "ecmwf_ifs"]
    assert meta["points"]["spacing_deg"] == 0.2
    assert meta["variables"]["temperature_2m_min"]["lapse_rate_c_per_km"] == 4.2
