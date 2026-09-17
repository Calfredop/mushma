from datetime import date, timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pytest

from api.grid.habitats import load_vocabulary
from api.model.config import load_model_config
from api.model.inputs import load_cells, load_weather
from api.weather.config import load_weather_config

from ..weather.test_downscale import _store

DAY = date(2026, 9, 10)


def write_grid(folder: Path) -> Path:
    """Three cells: two woodland (one high, one low), one farmland."""
    folder.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            "cell_id": ["1kmE4400N2300", "1kmE4401N2300", "1kmE4399N2300"],
            "woodland": [True, True, False],
            "elevation_m": [1000.0, 0.0, 50.0],
            "slope_deg": [20.0, 2.0, 1.0],
            "aspect_deg": [10.0, None, None],
            "northness": [0.9, 0.0, 0.0],
            "soil_ph": [5.5, None, 7.0],
            "lon": [11.0, 11.01, 10.99],
            "lat": [43.5, 43.5, 43.5],
        }
    ).to_parquet(folder / "cells.parquet")
    pd.DataFrame(
        {
            "cell_id": ["1kmE4400N2300", "1kmE4400N2300", "1kmE4401N2300"],
            "habitat": ["beech", "chestnut", "evergreen_oak"],
            "fraction": [0.75, 0.25, 1.0],
        }
    ).to_parquet(folder / "cell_habitats.parquet")
    return folder


def test_load_cells_keeps_woodland_cells_with_attributes_and_habitat_fractions(
    tmp_path: Path,
) -> None:
    cells = load_cells(write_grid(tmp_path / "grid"))

    assert cells.ids.tolist() == ["1kmE4400N2300", "1kmE4401N2300"]
    assert cells.attributes["elevation_m"].tolist() == [1000.0, 0.0]
    assert np.isnan(cells.attributes["soil_ph"][1])
    assert cells.habitat_names == load_vocabulary().habitats
    beech, chestnut = cells.habitat_names.index("beech"), cells.habitat_names.index("chestnut")
    assert cells.habitat_fractions[0, beech] == 0.75
    assert cells.habitat_fractions[0, chestnut] == 0.25
    assert cells.habitat_fractions.sum(axis=1).tolist() == [1.0, 1.0]


def _weights() -> pd.DataFrame:
    rows = []
    for cell in ("1kmE4400N2300", "1kmE4401N2300"):
        rows += [("bilinear", cell, "A", 1.0), ("nearest", cell, "A", 1.0)]
    return pd.DataFrame(rows, columns=["method", "cell_id", "point_id", "weight"])


def test_load_weather_scales_reanalysis_rain_by_cell_height_and_flags_forecast_days(
    tmp_path: Path,
) -> None:
    cells = load_cells(write_grid(tmp_path / "grid"))
    tomorrow = DAY + timedelta(days=1)
    store = _store(
        tmp_path / "weather",
        [
            ("era5_seamless", "A", DAY, "precipitation_sum", 10.0),
            ("era5_seamless", "A", DAY, "temperature_2m_mean", 12.0),
            ("ecmwf_ifs", "A", tomorrow, "precipitation_sum", 10.0),
            ("ecmwf_ifs", "A", tomorrow, "temperature_2m_mean", 12.0),
        ],
        {("era5_seamless", "A"): 500.0, ("ecmwf_ifs", "A"): 500.0},
    )

    weather = load_weather(
        duckdb.connect(),
        store,
        cells,
        _weights(),
        DAY,
        tomorrow,
        load_weather_config(),
        load_model_config(),
    )

    rain = weather.values["precipitation_sum"]
    assert rain[:, 0] == pytest.approx([10.0 * 1.57, 10.0 * 1.28])
    assert rain[:, 1].tolist() == [10.0, 10.0]  # forecast rain is not scaled
    assert weather.values["temperature_2m_mean"][1, 0] == pytest.approx(12.0 + 0.0045 * 500)
    assert weather.forecast.tolist() == [[False, True], [False, True]]
    assert [d.item() for d in weather.dates] == [DAY, tomorrow]
