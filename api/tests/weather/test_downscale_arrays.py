"""``cell_weather_arrays`` must downscale exactly like ``cell_weather``, the reference
implementation, only as dense ``(cells, days)`` arrays."""

from datetime import date, timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pytest

from api.weather.config import Variable
from api.weather.downscale import cell_weather, cell_weather_arrays
from api.weather.store import WeatherStore

from .test_downscale import CELLS, DAY, ORDER, VARIABLES, WEIGHTS, _store


def _both(store: WeatherStore, cells, weights, start, end, variables=VARIABLES):
    reference = cell_weather(
        duckdb.connect(), store, cells, weights, start, end, variables, ORDER
    ).df()
    arrays = cell_weather_arrays(
        duckdb.connect(), store, cells, weights, start, end, variables, ORDER
    )
    return reference, arrays


def _assert_same(reference: pd.DataFrame, arrays, variables) -> None:
    dates = [d.item() for d in arrays.dates]
    for name in variables:
        expected = np.full((len(arrays.cell_ids), len(dates)), np.nan)
        expected_rank = np.full(expected.shape, -1)
        rows = reference[reference.variable == name]
        for row in rows.itertuples():
            i = list(arrays.cell_ids).index(row.cell_id)
            j = dates.index(pd.Timestamp(row.date).date())
            expected[i, j] = row.value
            expected_rank[i, j] = ORDER.index(row.source)
        np.testing.assert_allclose(arrays.values[name], expected, rtol=1e-9, equal_nan=True)
        assert arrays.source_rank[name].tolist() == expected_rank.tolist(), name


def test_arrays_match_the_reference_on_a_mixed_fixture(tmp_path: Path) -> None:
    tomorrow = DAY + timedelta(days=1)
    store = _store(
        tmp_path,
        [
            ("era5_seamless", "A", DAY, "precipitation_sum", 10.0),
            ("ecmwf_ifs", "B", DAY, "precipitation_sum", 30.0),
            ("era5_seamless", "A", DAY, "temperature_2m_mean", 10.0),
            ("era5_seamless", "B", DAY, "temperature_2m_mean", 14.0),
            ("ecmwf_ifs", "A", tomorrow, "temperature_2m_mean", 8.0),
            ("era5_seamless", "B", tomorrow, "snowfall_sum", 4.0),
        ],
        {("era5_seamless", "A"): 850.0, ("era5_seamless", "B"): 250.0, ("ecmwf_ifs", "A"): 1050.0},
    )

    reference, arrays = _both(store, CELLS, WEIGHTS, DAY, tomorrow)

    assert arrays.cell_ids.tolist() == ["c1", "c2"]
    assert [d.item() for d in arrays.dates] == [DAY, tomorrow]
    _assert_same(reference, arrays, VARIABLES)


def test_arrays_match_the_reference_on_random_weather_with_gaps(tmp_path: Path) -> None:
    rng = np.random.default_rng(7)
    points = [f"P{i}" for i in range(6)]
    days = [date(2024, 9, 1) + timedelta(days=i) for i in range(10)]
    rows = []
    for source in ORDER:
        for point in points:
            for day in days:
                for name in VARIABLES:
                    if rng.random() < 0.6:
                        rows.append((source, point, day, name, float(rng.normal(10, 5))))
    heights = {(s, p): float(rng.uniform(0, 1500)) for s in ORDER for p in points}
    del heights[("ecmwf_ifs", "P3")]  # a forecast point without a model height
    store = _store(tmp_path, rows, heights)
    cell_ids = [f"c{i}" for i in range(8)]
    cells = pd.DataFrame(
        {"cell_id": cell_ids, "elevation_m": [*rng.uniform(0, 1600, 7).tolist(), None]}
    )
    weights = []
    for cell in cell_ids:
        chosen = rng.choice(points, size=4, replace=False)
        w = rng.uniform(0.1, 1, 4)
        weights += [("bilinear", cell, p, x) for p, x in zip(chosen, w / w.sum(), strict=True)]
        weights.append(("nearest", cell, str(chosen[0]), 1.0))
    weights = pd.DataFrame(weights, columns=["method", "cell_id", "point_id", "weight"])

    reference, arrays = _both(store, cells, weights, days[0], days[-1])

    _assert_same(reference, arrays, VARIABLES)


def test_a_variable_with_no_rows_is_all_missing(tmp_path: Path) -> None:
    store = _store(
        tmp_path,
        [("era5_seamless", "A", DAY, "precipitation_sum", 10.0)],
        {("era5_seamless", "A"): 850.0},
    )
    variables = {
        **VARIABLES,
        "vapour_pressure_deficit_max": Variable("vapour_pressure_deficit_max", "kPa", "bilinear"),
    }

    arrays = cell_weather_arrays(
        duckdb.connect(), store, CELLS, WEIGHTS, DAY, DAY, variables, ORDER
    )

    assert np.isnan(arrays.values["vapour_pressure_deficit_max"]).all()
    assert arrays.values["precipitation_sum"][:, 0] == pytest.approx([10.0, 10.0])
