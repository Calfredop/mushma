"""Tests for CDS hourly → Europe/Rome daily aggregation (no live CDS call)."""

import numpy as np
import pandas as pd
import pytest

from api.weather.cds import (
    SOURCE_ID,
    aggregate_hourly_frame,
    bbox_of_points,
    resolve_cds_key,
    subsample_to_points,
)
from api.weather.store import WeatherStore


def _hourly_day(
    lat: float = 43.8, lon: float = 11.8, rain_m_per_hour: float = 0.001
) -> pd.DataFrame:
    """24 UTC hours on 2024-07-15, already per-hour increments (not cumulative)."""
    times = pd.date_range("2024-07-15", periods=24, freq="h", tz="UTC")
    # Cumulative-looking precip that resets: use increasing-then-reset pattern.
    cum_tp = np.cumsum(np.full(24, rain_m_per_hour))
    return pd.DataFrame(
        {
            "time": times,
            "lat": lat,
            "lon": lon,
            "t2m": 273.15 + 15.0 + 5.0 * np.sin(np.linspace(0, 2 * np.pi, 24)),
            "d2m": 273.15 + 10.0,
            "tp": cum_tp,
            "sf": np.zeros(24),
            "swvl1": np.full(24, 0.25),
            "swvl2": np.full(24, 0.28),
            "stl1": 273.15 + 16.0,
            "u10": np.full(24, 3.0),
            "v10": np.zeros(24),
            "ssrd": np.cumsum(np.where((np.arange(24) >= 8) & (np.arange(24) <= 16), 1.5e6, 0.0)),
        }
    )


def test_hourly_accumulation_ignores_float_noise_on_plateau() -> None:
    from api.weather.cds import _hourly_accumulation

    # SSRD overnight plateau with float32-ish ±1 J noise must not count as a reset.
    cum = np.array([0.0, 1e6, 5e6, 9.815910e6, 9.815909e6, 9.815911e6, 0.0, 1e5], dtype=float)
    inc = _hourly_accumulation(cum)
    assert inc[4] == 0.0
    assert inc[5] == pytest.approx(2.0)
    assert inc[6] == 0.0  # real reset to 0
    assert inc[7] == pytest.approx(1e5)


def test_cds_chunk_request_covers_a_week() -> None:
    from api.weather.cds import CdsChunkRequest, month_day_chunks

    chunks = month_day_chunks(2024, 1)
    assert chunks[0] == tuple(range(1, 8))
    assert chunks[-1][-1] == 31
    req = CdsChunkRequest(
        north=44.0, west=10.0, south=43.0, east=12.0, year=2024, month=1, days=chunks[0]
    )
    body = req.cds_request()
    assert body["month"] == ["01"]
    assert body["day"] == [f"{d:02d}" for d in range(1, 8)]
    assert "20240101-07_" in req.label


def test_aggregate_deaccumulates_across_local_midnight_not_per_group() -> None:
    """ERA5-Land accumulations reset at 00 UTC; Rome local days straddle that.

    Deaccumulating inside each local-day group treats the first hour's cumulative
    total as an increment and roughly doubles rain (and SSRD → ET0).
    """
    # Two UTC days, ERA5-Land shaped: 00:00 carries previous day's total, then
    # 01:00..23:00 / next 00:00 climb by 1 mm/h.
    times = pd.date_range("2024-01-01", periods=48, freq="h", tz="UTC")
    cum_tp = []
    for i in range(48):
        h = i % 24
        cum_tp.append(0.024 if h == 0 else h * 0.001)
    frame = pd.DataFrame(
        {
            "time": times,
            "lat": 43.8,
            "lon": 11.8,
            "t2m": 273.15 + 5.0,
            "d2m": 273.15 + 2.0,
            "tp": cum_tp,
            "sf": np.zeros(48),
            "swvl1": np.full(48, 0.25),
            "swvl2": np.full(48, 0.28),
            "stl1": 273.15 + 6.0,
            "u10": np.full(48, 2.0),
            "v10": np.zeros(48),
            "ssrd": np.zeros(48),
        }
    )
    daily = aggregate_hourly_frame(frame, "Europe/Rome")
    rain = (
        daily.loc[daily["variable"] == "precipitation_sum", ["date", "value"]]
        .sort_values("date")
        .reset_index(drop=True)
    )
    # First 00:00 is prior-day carryover (dropped); 47 mm of in-window rain.
    assert float(rain["value"].sum()) == pytest.approx(47.0, abs=0.05)
    assert float(rain["value"].max()) < 30.0


def test_aggregate_emits_all_eleven_daily_variables_for_one_local_day() -> None:
    daily = aggregate_hourly_frame(_hourly_day(), "Europe/Rome")
    assert set(daily["source"]) == {SOURCE_ID}
    assert set(daily["point_id"]) == {"N43.80E011.80"}
    variables = set(daily["variable"])
    assert variables >= {
        "precipitation_sum",
        "snowfall_sum",
        "temperature_2m_min",
        "temperature_2m_max",
        "temperature_2m_mean",
        "soil_temperature_0_to_7cm_mean",
        "soil_moisture_0_to_7cm_mean",
        "soil_moisture_7_to_28cm_mean",
        "et0_fao_evapotranspiration",
        "vapour_pressure_deficit_max",
        "wind_speed_10m_max",
    }
    rain = float(daily.loc[daily["variable"] == "precipitation_sum", "value"].iloc[0])
    # Europe/Rome (UTC+2 in July) shifts the last two UTC hours onto the next local day.
    # Series starts at 00 UTC (prior-day carryover → 0 increment), so 21 mm on this local date.
    assert rain == pytest.approx(21.0, abs=0.01)
    assert daily["date"].nunique() == 2  # spill into the next local morning
    wind = float(daily.loc[daily["variable"] == "wind_speed_10m_max", "value"].iloc[0])
    assert wind == pytest.approx(3.0 * 3.6, abs=0.01)


def test_aggregate_splits_utc_day_across_europe_rome_dst() -> None:
    # 2024-03-31 is DST start in Rome: 01:00 CET → 03:00 CEST.
    times = pd.date_range("2024-03-30 22:00", periods=8, freq="h", tz="UTC")
    rows = []
    for t in times:
        rows.append(
            {
                "time": t,
                "lat": 43.8,
                "lon": 11.8,
                "t2m": 280.0,
                "d2m": 275.0,
                "tp": 0.0,
                "sf": 0.0,
                "swvl1": 0.2,
                "swvl2": 0.2,
                "stl1": 280.0,
                "u10": 1.0,
                "v10": 0.0,
                "ssrd": 0.0,
            }
        )
    daily = aggregate_hourly_frame(pd.DataFrame(rows), "Europe/Rome")
    dates = sorted(daily["date"].unique())
    assert len(dates) >= 2  # spans two local dates around the transition


def test_subsample_keeps_only_configured_land_nodes() -> None:
    hourly = pd.concat(
        [_hourly_day(43.8, 11.8), _hourly_day(43.8, 12.0), _hourly_day(44.0, 11.8)],
        ignore_index=True,
    )
    points = pd.DataFrame(
        {
            "point_id": ["N43.80E011.80", "N44.00E011.80"],
            "lat": [43.8, 44.0],
            "lon": [11.8, 11.8],
            "land": [True, True],
        }
    )
    kept = subsample_to_points(hourly, points)
    assert set(zip(kept["lat"].round(2), kept["lon"].round(2), strict=True)) == {
        (43.8, 11.8),
        (44.0, 11.8),
    }


def test_bbox_pads_the_land_points() -> None:
    points = pd.DataFrame({"lat": [43.0, 44.0], "lon": [10.0, 12.0], "land": [True, True]})
    north, west, south, east = bbox_of_points(points, pad_deg=0.1)
    assert north == pytest.approx(44.1)
    assert south == pytest.approx(42.9)
    assert west == pytest.approx(9.9)
    assert east == pytest.approx(12.1)


def test_aggregate_upserts_into_the_weather_store(tmp_path) -> None:
    store = WeatherStore(tmp_path)
    daily = aggregate_hourly_frame(_hourly_day(), "Europe/Rome")
    store.upsert_daily(daily)
    path = store.partition_path(SOURCE_ID, 2024)
    assert path.exists()
    loaded = pd.read_parquet(path)
    assert len(loaded) == len(daily)


def test_resolve_cds_key_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("CDSAPI_KEY", "123:abc")
    assert resolve_cds_key() == "123:abc"


def test_resolve_cds_key_errors_when_missing(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CDSAPI_KEY", raising=False)
    monkeypatch.setattr("api.weather.cds.Path.home", lambda: tmp_path)
    with pytest.raises(Exception, match="CDS API key"):
        resolve_cds_key()
