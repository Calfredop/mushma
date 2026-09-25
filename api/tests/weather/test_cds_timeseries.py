"""The ERA5-Land time-series path: one CDS request per node, snowfall from the gridded dataset."""

import re
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from api.weather.cds import (
    SOURCE_ID,
    TIMESERIES_DATASET,
    TIMESERIES_VARS,
    CdsPointRequest,
    aggregate_hourly_frame,
    backfill_cds_timeseries,
    snowfall_requests,
)
from api.weather.store import WeatherStore

BBOX = (43.95, 11.65, 42.05, 13.55)  # north, west, south, east


def test_point_request_asks_the_time_series_product_for_one_node() -> None:
    request = CdsPointRequest(lat=43.0, lon=12.4, start=date(2015, 12, 31), end=date(2026, 9, 14))

    body = request.cds_request()

    assert request.dataset == TIMESERIES_DATASET
    assert body["variable"] == list(TIMESERIES_VARS)
    assert "snowfall" not in body["variable"]
    assert body["location"] == {"longitude": 12.4, "latitude": 43.0}
    assert body["date"] == ["2015-12-31/2026-09-14"]
    assert "N43.00E012.40" in request.label


def test_snowfall_comes_in_half_years_with_partial_months_on_their_own() -> None:
    requests = snowfall_requests(BBOX, date(2016, 1, 1), date(2017, 9, 14))

    spans = [(r.year, r.months, r.days) for r in requests]
    assert spans == [
        (2016, (1, 2, 3, 4, 5, 6), None),
        (2016, (7, 8, 9, 10, 11, 12), None),
        (2017, (1, 2, 3, 4, 5, 6), None),
        (2017, (7, 8), None),
        (2017, (9,), tuple(range(1, 15))),
    ]
    body = requests[-1].cds_request()
    assert body["variable"] == ["snowfall"]
    assert body["month"] == ["09"]
    assert body["day"] == [f"{d:02d}" for d in range(1, 15)]
    assert requests[0].cds_request()["day"] == [f"{d:02d}" for d in range(1, 32)]
    assert all(r.dataset == "reanalysis-era5-land" for r in requests)
    assert len({r.label for r in requests}) == len(requests)


def test_snowfall_split_starts_mid_month_too() -> None:
    requests = snowfall_requests(BBOX, date(2024, 3, 10), date(2024, 5, 31))

    assert [(r.months, r.days) for r in requests] == [
        ((3,), tuple(range(10, 32))),
        ((4, 5), None),
    ]


def test_aggregate_can_take_series_that_are_already_hourly_increments() -> None:
    times = pd.date_range("2024-07-15", periods=48, freq="h", tz="UTC")
    frame = pd.DataFrame(
        {
            "time": times,
            "lat": 43.0,
            "lon": 12.4,
            "t2m": 290.0,
            "d2m": 283.0,
            "tp": np.full(48, 0.001),
            "sf": np.zeros(48),
            "swvl1": 0.25,
            "swvl2": 0.28,
            "stl1": 291.0,
            "u10": 2.0,
            "v10": 0.0,
            "ssrd": np.zeros(48),
        }
    )

    daily = aggregate_hourly_frame(frame, "Europe/Rome", accumulated=())

    rain = daily[daily["variable"] == "precipitation_sum"].set_index("date")["value"]
    # 15 July local: 22:00 UTC on the 14th is missing, so 22 of the day's 24 hours are here.
    assert rain[date(2024, 7, 15)] == pytest.approx(22.0)
    assert rain[date(2024, 7, 16)] == pytest.approx(24.0)


class FakeClient:
    """Serves requests from memory; records which ones were fetched."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.fetched: list[str] = []

    def cache_path(self, request) -> Path:
        return self.root / f"{request.label}.zip"

    def ensure(self, request, log=print) -> Path:
        path = self.cache_path(request)
        if not path.exists():
            self.fetched.append(request.label)
            path.write_text(request.label)
        return path


NODES = pd.DataFrame(
    {
        "point_id": ["N43.00E012.40", "N42.80E012.60"],
        "lat": [43.0, 42.8],
        "lon": [12.4, 12.6],
        "land": [True, True],
        "grid_elevation_m": [400.0, 600.0],
        "dem_elevation_m": [380.0, np.nan],
    }
)


def fake_read(path: Path) -> pd.DataFrame:
    """Hourly frames shaped like the CDS NetCDF zips, keyed by the request label in the file."""
    label = path.read_text()
    if label.startswith("ts_"):
        lat, lon = (43.0, 12.4) if "N43.00E012.40" in label else (42.8, 12.6)
        times = pd.date_range("2024-02-28", "2024-03-02 23:00", freq="h")
        return pd.DataFrame(
            {
                "time": times,
                "lat": lat + 1e-12,  # the product's coordinates carry float noise
                "lon": lon - 1e-12,
                "t2m": 272.0,
                "d2m": 270.0,
                "tp": 0.0005,  # already per hour
                "swvl1": 0.3,
                "swvl2": 0.3,
                "stl1": 274.0,
                "u10": 1.0,
                "v10": 1.0,
                "ssrd": 0.0,
            }
        )
    # Snowfall over the bbox grid for exactly the days the request names, cumulative since 00 UTC
    # with the 00 UTC step carrying the previous day's total (ERA5-Land's convention); 1 mm of
    # water per hour everywhere.
    match = re.match(r"sf_(\d{4})(\d{2})-(\d{2})(?:_d(\d{2})-(\d{2}))?", label)
    assert match, label
    year, first_month, last_month = (int(match[i]) for i in (1, 2, 3))
    first_day = int(match[4]) if match[4] else 1
    start = pd.Timestamp(year, first_month, first_day)
    if match[5]:
        end = pd.Timestamp(year, last_month, int(match[5]), 23)
    else:
        end = pd.Timestamp(year, last_month, 1) + pd.offsets.MonthEnd(0) + pd.Timedelta(hours=23)
    times = pd.date_range(start, end, freq="h")
    cumulative = np.array([24.0 if t.hour == 0 else float(t.hour) for t in times]) * 0.001
    rows = []
    for lat, lon in [(43.0, 12.4), (42.8, 12.6), (43.9, 11.7)]:
        rows.append(pd.DataFrame({"time": times, "lat": lat, "lon": lon, "sf": cumulative}))
    return pd.concat(rows, ignore_index=True)


def test_backfill_writes_every_local_day_per_node_and_reruns_from_cache(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path / "store")
    client = FakeClient(tmp_path)
    start, end = date(2024, 2, 29), date(2024, 3, 2)

    summary = backfill_cds_timeseries(
        client, store, NODES, "Europe/Rome", start, end, log=lambda m: None, read=fake_read
    )

    assert sorted(label[:16] for label in client.fetched if label.startswith("ts_")) == [
        "ts_N42.80E012.60",
        "ts_N43.00E012.40",
    ]
    assert sorted(label[:16] for label in client.fetched if label.startswith("sf_")) == [
        "sf_202402-02_d29",
        "sf_202403-03_d01",
    ]
    daily = pd.read_parquet(store.partition_path(SOURCE_ID, 2024))
    days = sorted(set(pd.to_datetime(daily["date"]).dt.date))
    assert days == [start, date(2024, 3, 1), end]
    assert set(daily["point_id"]) == {"N43.00E012.40", "N42.80E012.60"}
    rain = daily[
        (daily["variable"] == "precipitation_sum") & (daily["point_id"] == "N43.00E012.40")
    ]
    assert rain["value"].tolist() == pytest.approx([12.0, 12.0, 12.0])  # 24 h x 0.5 mm, local days
    snow = daily[(daily["variable"] == "snowfall_sum") & (daily["point_id"] == "N43.00E012.40")]
    # 1 mm of water an hour -> 0.1 cm; local 29 Feb begins at 23:00 UTC on the 28th, which no
    # snowfall request covers, and the series' first 00 UTC step is carry-over.
    assert snow["value"].tolist() == pytest.approx([2.2, 2.4, 2.4])
    assert summary["fetched"] == len(client.fetched)

    client.fetched.clear()
    backfill_cds_timeseries(
        client, store, NODES, "Europe/Rome", start, end, log=lambda m: None, read=fake_read
    )
    assert client.fetched == []


def test_first_snowfall_hour_of_the_whole_range_is_not_counted_twice(tmp_path: Path) -> None:
    """The series starts at 00 UTC, whose value is the previous day's total, not an increment."""
    store = WeatherStore(tmp_path / "store")
    client = FakeClient(tmp_path)

    backfill_cds_timeseries(
        client,
        store,
        NODES,
        "Europe/Rome",
        date(2024, 3, 1),
        date(2024, 3, 1),
        log=lambda m: None,
        read=fake_read,
    )

    daily = pd.read_parquet(store.partition_path(SOURCE_ID, 2024))
    snow = daily[(daily["variable"] == "snowfall_sum") & (daily["point_id"] == "N43.00E012.40")]
    # Local 1 March = 23:00 UTC 29 Feb (no snowfall request covers it) .. 22:00 UTC 1 March;
    # the 00 UTC step is dropped as carry-over: 22 counted hours of 1 mm.
    assert snow["value"].tolist() == pytest.approx([2.2])
    assert date(2024, 3, 1) - timedelta(days=1) not in set(pd.to_datetime(daily["date"]).dt.date)


def test_client_waits_out_a_full_queue_and_retries(tmp_path, monkeypatch) -> None:
    import sys
    import types

    from api.weather.cds import CdsClient

    attempts = []

    class FakeCdsapiClient:
        def __init__(self, **kwargs) -> None:
            pass

        def retrieve(self, dataset, body, target) -> None:
            attempts.append(dataset)
            if len(attempts) == 1:
                raise RuntimeError(
                    "The job has been rejected\nNumber queued requests for this dataset is "
                    "temporarily limited. Please configure your scripts accordingly"
                )
            Path(target).write_bytes(b"zip")

    monkeypatch.setitem(sys.modules, "cdsapi", types.SimpleNamespace(Client=FakeCdsapiClient))
    client = CdsClient(cache_dir=tmp_path, key="uid:key", queue_wait_s=0)
    request = CdsPointRequest(lat=43.0, lon=12.4, start=date(2024, 1, 1), end=date(2024, 1, 2))

    path = client.ensure(request, log=lambda m: None)

    assert path.read_bytes() == b"zip"
    assert attempts == [TIMESERIES_DATASET, TIMESERIES_DATASET]


def test_client_does_not_retry_other_failures(tmp_path, monkeypatch) -> None:
    import sys
    import types

    from api.weather.cds import CdsClient

    class FakeCdsapiClient:
        def __init__(self, **kwargs) -> None:
            pass

        def retrieve(self, dataset, body, target) -> None:
            raise RuntimeError("Your request is too large")

    monkeypatch.setitem(sys.modules, "cdsapi", types.SimpleNamespace(Client=FakeCdsapiClient))
    client = CdsClient(cache_dir=tmp_path, key="uid:key", queue_wait_s=0)
    request = CdsPointRequest(lat=43.0, lon=12.4, start=date(2024, 1, 1), end=date(2024, 1, 2))

    with pytest.raises(RuntimeError, match="too large"):
        client.ensure(request, log=lambda m: None)
