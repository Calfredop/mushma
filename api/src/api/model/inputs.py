"""Load what the engine scores from the M2 stores: woodland cells from the grid, and their
downscaled daily weather, prepared as ``config/model.yaml`` says."""

from datetime import date
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from api.grid.habitats import load_vocabulary
from api.model.arrays import Cells, Weather
from api.model.config import ModelConfig
from api.model.rules import GRID_ATTRIBUTES
from api.weather.config import WeatherConfig
from api.weather.downscale import cell_weather_arrays
from api.weather.store import WeatherStore


def load_cells(grid_dir: Path) -> Cells:
    """Woodland cells, ordered by cell id, with their attributes and habitat fractions."""
    columns = ["cell_id", "woodland", *sorted(GRID_ATTRIBUTES)]
    cells = pd.read_parquet(grid_dir / "cells.parquet", columns=columns)
    cells = cells[cells["woodland"]].sort_values("cell_id").reset_index(drop=True)
    habitats = load_vocabulary().habitats
    long = pd.read_parquet(grid_dir / "cell_habitats.parquet")
    fractions = (
        long[long["cell_id"].isin(set(cells["cell_id"]))]
        .pivot_table(index="cell_id", columns="habitat", values="fraction", aggfunc="sum")
        .reindex(index=cells["cell_id"], columns=habitats)
        .fillna(0.0)
    )
    return Cells(
        ids=cells["cell_id"].to_numpy(dtype=object),
        attributes={
            name: pd.to_numeric(cells[name], errors="coerce").to_numpy(dtype=float)
            for name in sorted(GRID_ATTRIBUTES)
        },
        habitat_names=habitats,
        habitat_fractions=fractions.to_numpy(dtype=float),
    )


def load_weather(
    con: duckdb.DuckDBPyConnection,
    store: WeatherStore,
    cells: Cells,
    weights: pd.DataFrame,
    start: date,
    end: date,
    weather_config: WeatherConfig,
    model_config: ModelConfig,
) -> Weather:
    """Downscaled weather for ``cells`` from ``start`` to ``end``, with reanalysis rain scaled by
    cell height and each cell-day flagged when any variable came from the forecast."""
    order = weather_config.source_order
    arrays = cell_weather_arrays(
        con,
        store,
        pd.DataFrame({"cell_id": cells.ids, "elevation_m": cells.attributes["elevation_m"]}),
        weights,
        start,
        end,
        weather_config.variables,
        order,
    )
    values = dict(arrays.values)
    scale = model_config.precipitation_scale
    if scale.enabled and "precipitation_sum" in values:
        rank = arrays.source_rank["precipitation_sum"]
        scaled_ranks = [order.index(s) for s in scale.sources if s in order]
        factor = scale.factor(cells.attributes["elevation_m"])[:, np.newaxis]
        values["precipitation_sum"] = np.where(
            np.isin(rank, scaled_ranks),
            values["precipitation_sum"] * factor,
            values["precipitation_sum"],
        )
    forecast_rank = order.index(weather_config.forecast.model)
    forecast = np.zeros((len(cells), len(arrays.dates)), dtype=bool)
    for rank in arrays.source_rank.values():
        forecast |= rank == forecast_rank
    return Weather(dates=arrays.dates, values=values, forecast=forecast)
