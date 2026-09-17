"""Sanity checks on the ingested Tuscany weather (skipped until `api.weather.ingest points` ran).

Physical ranges are loose on purpose: they catch unit mix-ups and parsing errors, not weather.
"""

from datetime import date

import duckdb
import pandas as pd
import pytest

from api.grid.sources import data_dir
from api.weather.config import load_weather_config
from api.weather.downscale import cell_weather
from api.weather.store import WeatherStore

STORE = WeatherStore(data_dir() / "weather" / "tuscany")
GRID_DIR = data_dir() / "grid" / "tuscany"
pytestmark = pytest.mark.skipif(not STORE.points_path.exists(), reason="Tuscany weather not built")

RANGES = {
    "precipitation_sum": (0, 400),
    "snowfall_sum": (0, 150),
    "temperature_2m_min": (-30, 35),
    "temperature_2m_max": (-20, 46),
    "temperature_2m_mean": (-25, 40),
    "soil_temperature_0_to_7cm_mean": (-15, 45),
    "soil_moisture_0_to_7cm_mean": (0, 0.7),
    "soil_moisture_7_to_28cm_mean": (0, 0.7),
    "et0_fao_evapotranspiration": (0, 12),
    "vapour_pressure_deficit_max": (0, 8),
    "wind_speed_10m_max": (0, 150),
}


@pytest.fixture(scope="module")
def points() -> pd.DataFrame:
    return pd.read_parquet(STORE.points_path)


@pytest.fixture(scope="module")
def weights() -> pd.DataFrame:
    return pd.read_parquet(STORE.weights_path)


def test_the_point_set_is_the_land_part_of_the_configured_lattice(points: pd.DataFrame) -> None:
    spacing = load_weather_config().points.spacing_deg
    land = points[points["land"]]

    assert ((points[["lat", "lon"]] / spacing).round(6) % 1 == 0).all(axis=None)
    if spacing == 0.2:
        assert 80 <= len(land) <= 130  # 103 when built on 2026-09-17
    assert land["grid_elevation_m"].corr(land["dem_elevation_m"]) > 0.85


def test_nearly_every_woodland_cell_has_weights_that_sum_to_one(weights: pd.DataFrame) -> None:
    cells = pd.read_parquet(GRID_DIR / "cells.parquet", columns=["cell_id", "woodland"])
    woodland = set(cells.loc[cells["woodland"], "cell_id"])

    served = set(weights["cell_id"])
    assert len(woodland - served) <= 5  # islands out of reach
    assert served <= woodland
    totals = weights.groupby(["method", "cell_id"])["weight"].sum()
    assert totals.to_numpy() == pytest.approx(1.0)


def test_stored_values_are_physically_plausible() -> None:
    if not STORE.daily_files():
        pytest.skip("no daily weather yet")
    ranges = duckdb.sql(
        f"SELECT variable, min(value), max(value) FROM read_parquet('{STORE.daily_glob}') "
        "GROUP BY variable"
    ).fetchall()

    assert {variable for variable, _, _ in ranges} == set(RANGES)
    for variable, low, high in ranges:
        allowed_low, allowed_high = RANGES[variable]
        assert allowed_low <= low and high <= allowed_high, (variable, low, high)


def test_every_point_with_a_past_year_has_all_of_it() -> None:
    # Holds while the backfill runs too: it stores whole batches of points, one year at a time.
    if not STORE.daily_files():
        pytest.skip("no daily weather yet")
    config = load_weather_config()
    counts = duckdb.sql(
        f"""
        SELECT year(date) AS y, point_id, count(DISTINCT date) AS days, count(*) AS n
        FROM read_parquet('{STORE.daily_glob}')
        WHERE source = '{config.history.model}' AND year(date) < year(current_date)
        GROUP BY 1, 2
        """
    ).df()

    for row in counts.itertuples():
        days_in_year = (date(row.y + 1, 1, 1) - date(row.y, 1, 1)).days
        assert row.days == days_in_year, (row.y, row.point_id)
        assert row.n == days_in_year * len(config.variables), (row.y, row.point_id)


def test_downscaled_temperature_falls_with_height_across_woodland_cells(
    weights: pd.DataFrame,
) -> None:
    config = load_weather_config()
    day = STORE.last_complete_date(config.history.model, list(weights["point_id"].unique()))
    if day is None:
        pytest.skip("no complete reanalysis day yet")
    cells = pd.read_parquet(GRID_DIR / "cells.parquet", columns=["cell_id", "elevation_m"])
    cells = cells[cells["cell_id"].isin(weights["cell_id"])]
    variables = {"temperature_2m_mean": config.variables["temperature_2m_mean"]}

    result = cell_weather(
        duckdb.connect(), STORE, cells, weights, day, day, variables, config.source_order
    ).df()

    merged = result.merge(cells, on="cell_id")
    assert len(merged) >= len(cells) - 5
    assert merged["value"].corr(merged["elevation_m"]) < -0.5
