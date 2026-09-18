"""Areas the time views aggregate over: the whole region and each comune (PRD -> Architecture ->
Areas), and how weather points roll up into them.

An area's daily weather is the mean of its woodland cells' downscaled weather. Downscaling is
linear in the point values (``api.weather.downscale``), so that mean is itself a weighted sum of
the points: each cell's interpolation weights, normalised, averaged over the area's cells. A
per-cell factor (the model's height scaling of reanalysis rain) folds into the same weights, and a
lapse-rate correction becomes one constant offset per area. Normals go through the same weights as
the actuals, so an anomaly compares like with like.
"""

import numpy as np
import pandas as pd

REGION_KIND = "region"
COMUNE_KIND = "comune"


def _woodland(cells: pd.DataFrame) -> pd.DataFrame:
    return cells[cells["woodland"].astype(bool)]


def area_members(cells: pd.DataFrame, region_id: str) -> pd.DataFrame:
    """``area_code, cell_id``: every woodland cell once in its comune and once in the region."""
    woodland = _woodland(cells)
    comuni = woodland[woodland["comune_code"].notna()]
    return pd.concat(
        [
            pd.DataFrame({"area_code": region_id, "cell_id": woodland["cell_id"]}),
            pd.DataFrame({"area_code": comuni["comune_code"], "cell_id": comuni["cell_id"]}),
        ],
        ignore_index=True,
    )


def area_table(cells: pd.DataFrame, region_id: str, region_name: str) -> pd.DataFrame:
    """``area_code, kind, name, province, cells, lon, lat`` (the mean of the cell centres)."""
    woodland = _woodland(cells)
    region = pd.DataFrame(
        [
            {
                "area_code": region_id,
                "kind": REGION_KIND,
                "name": region_name,
                "province": None,
                "cells": len(woodland),
                "lon": float(woodland["lon"].mean()),
                "lat": float(woodland["lat"].mean()),
            }
        ]
    )
    comuni = (
        woodland[woodland["comune_code"].notna()]
        .groupby("comune_code", as_index=False)
        .agg(
            name=("comune_name", "first"),
            province=("province", "first"),
            cells=("cell_id", "count"),
            lon=("lon", "mean"),
            lat=("lat", "mean"),
        )
        .rename(columns={"comune_code": "area_code"})
        .assign(kind=COMUNE_KIND)
        .sort_values("name", kind="stable")
    )
    columns = ["area_code", "kind", "name", "province", "cells", "lon", "lat"]
    return pd.concat([region, comuni[columns]], ignore_index=True)[columns]


def _normalised_cell_weights(weights: pd.DataFrame, method: str) -> pd.DataFrame:
    rows = weights[weights["method"] == method][["cell_id", "point_id", "weight"]]
    totals = rows.groupby("cell_id")["weight"].transform("sum")
    return rows.assign(weight=rows["weight"] / totals)


def area_point_weights(
    members: pd.DataFrame,
    weights: pd.DataFrame,
    method: str,
    cell_factor: pd.Series | None = None,
) -> pd.DataFrame:
    """``area_code, point_id, weight``: per area, the mean over its cells of each cell's
    normalised ``method`` weights, times ``cell_factor`` (indexed by cell id) when given. Cells
    without weights (out of reach of every weather point) are left out of the mean."""
    cell_weights = _normalised_cell_weights(weights, method)
    if cell_factor is not None:
        factor = cell_weights["cell_id"].map(cell_factor).fillna(1.0)
        cell_weights = cell_weights.assign(weight=cell_weights["weight"] * factor)
    joined = members.merge(cell_weights, on="cell_id", how="inner")
    served = joined.groupby("area_code")["cell_id"].nunique()
    summed = joined.groupby(["area_code", "point_id"], as_index=False)["weight"].sum()
    summed["weight"] = summed["weight"] / summed["area_code"].map(served)
    return summed


def lapse_offsets(
    members: pd.DataFrame,
    weights: pd.DataFrame,
    method: str,
    cells: pd.DataFrame,
    point_heights: pd.Series,
    lapse_c_per_km: float,
) -> pd.Series:
    """Per area, the mean over its cells of the downscaling's lapse-rate correction
    ``lapse x (weighted point height - cell height)``. Cells without a height get none, as in the
    downscaling."""
    cell_weights = _normalised_cell_weights(weights, method)
    cell_weights = cell_weights.assign(height=cell_weights["point_id"].map(point_heights))
    cell_weights = cell_weights[cell_weights["height"].notna()]
    mean_height = (cell_weights["weight"] * cell_weights["height"]).groupby(
        cell_weights["cell_id"]
    ).sum() / cell_weights.groupby("cell_id")["weight"].sum()
    elevation = cells.set_index("cell_id")["elevation_m"]
    correction = (
        lapse_c_per_km / 1000 * (mean_height - elevation.reindex(mean_height.index))
    ).fillna(0.0)
    joined = members[members["cell_id"].isin(correction.index)]
    return (
        joined.assign(correction=joined["cell_id"].map(correction))
        .groupby("area_code")["correction"]
        .mean()
    )


def _matrix(weights: pd.DataFrame, areas: list[str], points: list[str]) -> np.ndarray:
    matrix = np.zeros((len(areas), len(points)))
    area_pos = {a: i for i, a in enumerate(areas)}
    point_pos = {p: i for i, p in enumerate(points)}
    rows = weights[weights["point_id"].isin(point_pos)]
    np.add.at(
        matrix,
        (rows["area_code"].map(area_pos).to_numpy(), rows["point_id"].map(point_pos).to_numpy()),
        rows["weight"].to_numpy(dtype=float),
    )
    return matrix


def aggregate_to_areas(
    values: pd.DataFrame,
    weights: pd.DataFrame,
    scaled_weights: pd.DataFrame | None = None,
    offset: pd.Series | None = None,
) -> pd.DataFrame:
    """``area_code, date, value`` from point values ``point_id, date, value`` (and ``scaled``).

    Rows flagged ``scaled`` use ``scaled_weights`` (e.g. reanalysis rain with the model's height
    scaling); the rest use ``weights``. Points without a value that day drop out and the rest are
    renormalised by their share of the plain weights; an area with none of its points is NaN.
    ``offset`` (per area) is added last."""
    areas = sorted(weights["area_code"].unique())
    points = sorted(set(weights["point_id"]) | set(values["point_id"]))
    dates = sorted(values["date"].unique())
    point_pos = {p: i for i, p in enumerate(points)}
    date_pos = {d: i for i, d in enumerate(dates)}

    grid = np.full((len(points), len(dates)), np.nan)
    scaled = np.zeros((len(points), len(dates)), dtype=bool)
    p = values["point_id"].map(point_pos).to_numpy()
    d = values["date"].map(date_pos).to_numpy()
    grid[p, d] = values["value"].to_numpy(dtype=float)
    if "scaled" in values:
        scaled[p, d] = values["scaled"].to_numpy(dtype=bool)

    plain = _matrix(weights, areas, points)
    boosted = _matrix(scaled_weights, areas, points) if scaled_weights is not None else plain
    present = ~np.isnan(grid)
    filled = np.where(present, grid, 0.0)
    total = plain @ np.where(present & ~scaled, filled, 0.0) + boosted @ np.where(
        present & scaled, filled, 0.0
    )
    coverage = plain @ present.astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        result = np.where(coverage > 0, total / coverage, np.nan)
    if offset is not None:
        result = result + offset.reindex(areas).fillna(0.0).to_numpy()[:, None]

    return pd.DataFrame(
        {
            "area_code": np.repeat(areas, len(dates)),
            "date": np.tile(np.array(dates, dtype=object), len(areas)),
            "value": result.ravel(),
        }
    )
