"""Downscale point weather to 1 km cells.

For a cell, day and variable::

    value = Σ w_i v_i / Σ w_i  +  Γ · (Σ w_i z_i / Σ w_i − z_cell)

- ``w_i`` are the cell's interpolation weights for the variable's method (``bilinear`` or
  ``nearest``, from ``api.weather.points``). Points without data that day drop out and the rest are
  renormalised.
- ``v_i`` is the point's value from the most trusted source that has the day: reanalysis first,
  then forecast.
- The second term only applies to variables with a lapse rate ``Γ`` (temperatures): ``z_i`` is the
  mean height of the model grid cell the value came from (per source) and ``z_cell`` the cell's
  DEM height, so a cell above its points is cooler. Cells without a DEM height are not corrected.

Each output row carries ``source``: the least trusted source among the points it used, so a day
that leans on the forecast anywhere is labelled forecast.
"""

from dataclasses import dataclass
from datetime import date

import duckdb
import numpy as np
import pandas as pd

from api.weather.config import Variable
from api.weather.store import WeatherStore


def cell_weather(
    con: duckdb.DuckDBPyConnection,
    store: WeatherStore,
    cells: pd.DataFrame,
    weights: pd.DataFrame,
    start: date,
    end: date,
    variables: dict[str, Variable],
    source_order: list[str],
) -> duckdb.DuckDBPyRelation:
    """Daily ``(cell_id, date, variable, value, source)`` for ``cells`` between two dates."""
    rules = pd.DataFrame(
        [
            {
                "variable": v.name,
                "method": v.downscale,
                "lapse_c_per_m": (
                    v.lapse_rate_c_per_km / 1000 if v.lapse_rate_c_per_km is not None else None
                ),
            }
            for v in variables.values()
        ]
    ).astype({"lapse_c_per_m": "float64"})
    con.register("ds_rules", rules)
    con.register("ds_cells", cells[["cell_id", "elevation_m"]])
    con.register("ds_weights", weights[["method", "cell_id", "point_id", "weight"]])
    con.register("ds_point_cells", store.read_point_cells()[["source", "point_id", "elevation_m"]])
    store.best_daily(con, start, end, source_order).create_view("ds_best", replace=True)
    order = repr(list(source_order))
    return con.sql(
        f"""
        WITH used AS (
            SELECT w.cell_id, p.date, p.variable, p.source, w.weight, p.value,
                   pc.elevation_m AS point_elevation_m, r.lapse_c_per_m,
                   list_position({order}, p.source) AS source_rank
            FROM ds_best AS p
            JOIN ds_rules AS r USING (variable)
            JOIN ds_weights AS w ON w.point_id = p.point_id AND w.method = r.method
            JOIN ds_cells AS c ON c.cell_id = w.cell_id
            LEFT JOIN ds_point_cells AS pc ON pc.point_id = p.point_id AND pc.source = p.source
            WHERE r.lapse_c_per_m IS NULL OR pc.elevation_m IS NOT NULL
        )
        SELECT u.cell_id, u.date, u.variable,
               sum(u.weight * u.value) / sum(u.weight)
               + coalesce(
                   any_value(u.lapse_c_per_m)
                   * (sum(u.weight * u.point_elevation_m) / sum(u.weight) - c.elevation_m),
                   0
               ) AS value,
               arg_max(u.source, u.source_rank) AS source
        FROM used AS u
        JOIN ds_cells AS c USING (cell_id)
        GROUP BY u.cell_id, u.date, u.variable, c.elevation_m
        ORDER BY u.date, u.cell_id, u.variable
        """
    )


@dataclass(frozen=True)
class CellWeatherArrays:
    """Downscaled weather as dense arrays over consecutive days."""

    cell_ids: np.ndarray  # (cells,)
    dates: np.ndarray  # (days,) datetime64[D]
    values: dict[str, np.ndarray]  # variable -> (cells, days), NaN where no point has data
    source_rank: dict[str, np.ndarray]  # variable -> (cells, days): index into source_order, -1
    source_order: list[str]


def cell_weather_arrays(
    con: duckdb.DuckDBPyConnection,
    store: WeatherStore,
    cells: pd.DataFrame,
    weights: pd.DataFrame,
    start: date,
    end: date,
    variables: dict[str, Variable],
    source_order: list[str],
) -> CellWeatherArrays:
    """The same downscaling as :func:`cell_weather`, computed with matrix products instead of a
    join: fast enough to feed the model every woodland cell for a year at a time."""
    cell_ids = cells["cell_id"].to_numpy()
    cell_elevation = pd.to_numeric(cells["elevation_m"], errors="coerce").to_numpy(dtype=float)
    weights = weights[weights["cell_id"].isin(set(cell_ids))]
    point_ids = sorted(set(weights["point_id"]))
    cell_pos = {cell: i for i, cell in enumerate(cell_ids)}
    point_pos = {point: p for p, point in enumerate(point_ids)}
    one_day = np.timedelta64(1, "D")
    dates = np.arange(np.datetime64(start), np.datetime64(end) + one_day, dtype="datetime64[D]")
    shape = (len(cell_ids), len(dates))

    matrices: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for method, rows in weights.groupby("method"):
        w = np.zeros((len(cell_ids), len(point_ids)))
        i = rows["cell_id"].map(cell_pos).to_numpy()
        p = rows["point_id"].map(point_pos).to_numpy()
        w[i, p] = rows["weight"].to_numpy(dtype=float)
        linked = np.zeros_like(w)
        linked[i, p] = 1.0
        matrices[str(method)] = (w, linked)

    heights = np.full((len(source_order), len(point_ids)), np.nan)
    point_cells = store.read_point_cells()
    for row in point_cells[point_cells["source"].isin(source_order)].itertuples():
        if row.point_id in point_pos and pd.notna(row.elevation_m):
            heights[source_order.index(row.source), point_pos[row.point_id]] = row.elevation_m

    best = store.best_daily(con, start, end, source_order).df()
    best = best[best["point_id"].isin(point_pos)]
    values: dict[str, np.ndarray] = {}
    ranks: dict[str, np.ndarray] = {}
    for variable in variables.values():
        rows = best[best["variable"] == variable.name]
        point_values = np.full((len(point_ids), len(dates)), np.nan)
        point_rank = np.full((len(point_ids), len(dates)), -1)
        if not rows.empty:
            p = rows["point_id"].map(point_pos).to_numpy()
            d = (pd.to_datetime(rows["date"]).to_numpy().astype("datetime64[D]") - dates[0]).astype(
                int
            )
            point_values[p, d] = rows["value"].to_numpy(dtype=float)
            point_rank[p, d] = rows["source"].map(source_order.index).to_numpy()
        used = ~np.isnan(point_values)
        point_height = np.where(
            point_rank >= 0,
            heights[np.maximum(point_rank, 0), np.arange(len(point_ids))[:, None]],
            np.nan,
        )
        lapse = variable.lapse_rate_c_per_km
        if lapse is not None:
            used &= ~np.isnan(point_height)
        if variable.downscale not in matrices:
            values[variable.name] = np.full(shape, np.nan)
            ranks[variable.name] = np.full(shape, -1)
            continue
        w, linked = matrices[variable.downscale]
        used_f = used.astype(float)
        total = w @ used_f
        with np.errstate(invalid="ignore", divide="ignore"):
            value = (w @ np.where(used, point_values, 0.0)) / total
            if lapse is not None:
                mean_height = (w @ np.where(used, point_height, 0.0)) / total
                correction = lapse / 1000 * (mean_height - cell_elevation[:, None])
                value = value + np.where(np.isnan(cell_elevation)[:, None], 0.0, correction)
        has_rows = (linked @ used_f) > 0
        value[~has_rows] = np.nan
        rank = np.full(shape, -1)
        for r in range(len(source_order)):
            rank = np.where((linked @ (used & (point_rank == r)).astype(float)) > 0, r, rank)
        values[variable.name] = value
        ranks[variable.name] = rank
    return CellWeatherArrays(
        cell_ids=cell_ids,
        dates=dates,
        values=values,
        source_rank=ranks,
        source_order=list(source_order),
    )
