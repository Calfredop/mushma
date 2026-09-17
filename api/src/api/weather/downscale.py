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

from datetime import date

import duckdb
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
