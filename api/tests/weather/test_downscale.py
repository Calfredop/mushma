from datetime import UTC, date, datetime
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from api.weather.config import Variable
from api.weather.downscale import cell_weather
from api.weather.store import WeatherStore

FETCHED = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)
DAY = date(2024, 10, 3)
ORDER = ["era5_seamless", "ecmwf_ifs"]
VARIABLES = {
    "precipitation_sum": Variable("precipitation_sum", "mm", "bilinear"),
    "snowfall_sum": Variable("snowfall_sum", "cm", "nearest"),
    "temperature_2m_mean": Variable("temperature_2m_mean", "°C", "bilinear", 6.5),
}


def _store(
    tmp_path: Path, rows: list[tuple], elevations: dict[tuple[str, str], float]
) -> WeatherStore:
    store = WeatherStore(tmp_path)
    frame = pd.DataFrame(rows, columns=["source", "point_id", "date", "variable", "value"])
    frame["fetched_at"] = FETCHED
    store.upsert_daily(frame)
    store.upsert_point_cells(
        pd.DataFrame(
            [
                {
                    "source": source,
                    "point_id": pid,
                    "model_lat": 0.0,
                    "model_lon": 0.0,
                    "elevation_m": elevation,
                    "fetched_at": FETCHED,
                }
                for (source, pid), elevation in elevations.items()
            ]
        )
    )
    return store


def _weights(*rows: tuple[str, str, str, float]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["method", "cell_id", "point_id", "weight"])


CELLS = pd.DataFrame({"cell_id": ["c1", "c2"], "elevation_m": [1350.0, None]})
WEIGHTS = _weights(
    ("bilinear", "c1", "A", 0.75),
    ("bilinear", "c1", "B", 0.25),
    ("nearest", "c1", "B", 1.0),
    ("bilinear", "c2", "A", 1.0),
    ("nearest", "c2", "A", 1.0),
)


def _values(result: pd.DataFrame, cell_id: str, variable: str) -> list[float]:
    rows = result[(result.cell_id == cell_id) & (result.variable == variable)]
    return rows.sort_values("date")["value"].tolist()


def _run(store: WeatherStore, start: date = DAY, end: date = DAY, **kw) -> pd.DataFrame:
    return cell_weather(
        duckdb.connect(),
        store,
        kw.get("cells", CELLS),
        kw.get("weights", WEIGHTS),
        start,
        end,
        VARIABLES,
        ORDER,
    ).df()


def test_precipitation_is_the_weighted_mean_of_the_points(tmp_path: Path) -> None:
    store = _store(
        tmp_path,
        [
            ("era5_seamless", "A", DAY, "precipitation_sum", 10.0),
            ("era5_seamless", "B", DAY, "precipitation_sum", 30.0),
        ],
        {("era5_seamless", "A"): 850.0, ("era5_seamless", "B"): 400.0},
    )

    result = _run(store)

    assert _values(result, "c1", "precipitation_sum") == [pytest.approx(15.0)]
    assert _values(result, "c2", "precipitation_sum") == [pytest.approx(10.0)]


def test_temperature_is_corrected_from_the_point_heights_to_the_cell_height(
    tmp_path: Path,
) -> None:
    store = _store(
        tmp_path,
        [
            ("era5_seamless", "A", DAY, "temperature_2m_mean", 10.0),
            ("era5_seamless", "B", DAY, "temperature_2m_mean", 14.0),
        ],
        {("era5_seamless", "A"): 850.0, ("era5_seamless", "B"): 250.0},
    )

    result = _run(store)

    # Weighted mean 11 °C at a weighted height of 700 m, moved up to 1350 m at 6.5 °C/km.
    assert _values(result, "c1", "temperature_2m_mean") == [pytest.approx(11.0 - 0.0065 * 650)]
    # A cell without a DEM height keeps the uncorrected value.
    assert _values(result, "c2", "temperature_2m_mean") == [pytest.approx(10.0)]


def test_each_variable_uses_its_own_interpolation_method(tmp_path: Path) -> None:
    store = _store(
        tmp_path,
        [
            ("era5_seamless", "A", DAY, "snowfall_sum", 0.0),
            ("era5_seamless", "B", DAY, "snowfall_sum", 4.0),
        ],
        {("era5_seamless", "A"): 850.0, ("era5_seamless", "B"): 1400.0},
    )

    result = _run(store)

    assert _values(result, "c1", "snowfall_sum") == [pytest.approx(4.0)]


def test_a_point_missing_a_day_is_left_out_and_the_weights_renormalised(tmp_path: Path) -> None:
    store = _store(
        tmp_path,
        [("era5_seamless", "B", DAY, "precipitation_sum", 30.0)],
        {("era5_seamless", "A"): 850.0, ("era5_seamless", "B"): 400.0},
    )

    result = _run(store)

    assert _values(result, "c1", "precipitation_sum") == [pytest.approx(30.0)]
    assert _values(result, "c2", "precipitation_sum") == []


def test_forecast_days_use_the_forecast_model_heights_and_are_labelled(tmp_path: Path) -> None:
    tomorrow = date(2024, 10, 4)
    store = _store(
        tmp_path,
        [
            ("era5_seamless", "A", DAY, "temperature_2m_mean", 10.0),
            ("ecmwf_ifs", "A", DAY, "temperature_2m_mean", 99.0),  # reanalysis wins
            ("ecmwf_ifs", "A", tomorrow, "temperature_2m_mean", 8.0),
        ],
        {("era5_seamless", "A"): 850.0, ("ecmwf_ifs", "A"): 1050.0},
    )
    cells = pd.DataFrame({"cell_id": ["c2"], "elevation_m": [1050.0]})

    result = _run(store, DAY, tomorrow, cells=cells)

    assert _values(result, "c2", "temperature_2m_mean") == [
        pytest.approx(10.0 - 0.0065 * 200),
        pytest.approx(8.0),
    ]
    assert result.sort_values("date")["source"].tolist() == ["era5_seamless", "ecmwf_ifs"]


def test_a_cell_drawing_on_reanalysis_and_forecast_is_labelled_forecast(tmp_path: Path) -> None:
    store = _store(
        tmp_path,
        [
            ("era5_seamless", "A", DAY, "precipitation_sum", 10.0),
            ("ecmwf_ifs", "B", DAY, "precipitation_sum", 30.0),
        ],
        {("era5_seamless", "A"): 850.0, ("ecmwf_ifs", "B"): 400.0},
    )

    result = _run(store, cells=CELLS[CELLS.cell_id == "c1"])

    assert result[["cell_id", "value", "source"]].values.tolist() == [
        ["c1", pytest.approx(15.0), "ecmwf_ifs"]
    ]
