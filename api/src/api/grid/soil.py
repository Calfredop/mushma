"""Topsoil pH per cell from SoilGrids (ISRIC, 250 m).

SoilGrids stores pH in water x 10 as int16, with 0 where there is no prediction (sea, lakes,
urban). ``soil_ph`` is the 0-30 cm topsoil mean: each layer's cell mean weighted by the layer's
thickness. The v1 species rules do not use it (PRD known gaps); it is attached so the backtest can
check whether acidic soils matter for gallinacci.
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.enums import Resampling
from shapely.geometry.base import BaseGeometry

from api.grid.cells import cell_id
from api.grid.rasters import (
    block_view,
    grid_cell_size,
    grid_chunks,
    pixels_per_cell,
    region_mask,
    warp_to_grid,
)

# SoilGrids standard depths used for the topsoil, with their thickness in cm.
TOPSOIL_LAYERS = {"0-5cm": 5, "5-15cm": 10, "15-30cm": 15}
PH_SCALE = 10.0


def soil_ph_for_cells(
    layer_paths: dict[str, Path],
    grid: gpd.GeoDataFrame,
    boundary: BaseGeometry,
    pixel_m: float = 125.0,
    chunk_cells: int = 50,
) -> pd.DataFrame:
    """``(cell_id, soil_ph)`` for grid cells with SoilGrids data, weighting the given layers."""
    layers = {
        depth: _cell_means(path, grid, boundary, pixel_m, chunk_cells)
        for depth, path in layer_paths.items()
    }
    return depth_weighted_ph(layers)


def depth_weighted_ph(layers: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Combine per-layer ``(cell_id, ph)`` tables into a thickness-weighted ``soil_ph``."""
    weighted = None
    for depth, frame in layers.items():
        part = frame.set_index("cell_id")["ph"]
        weight = part.notna() * TOPSOIL_LAYERS[depth]
        values = (part.fillna(0.0) * weight).rename("sum"), weight.rename("weight")
        layer = pd.concat(values, axis=1)
        weighted = layer if weighted is None else weighted.add(layer, fill_value=0.0)
    assert weighted is not None, "no layers"
    weighted = weighted[weighted["weight"] > 0]
    return pd.DataFrame(
        {"cell_id": weighted.index, "soil_ph": (weighted["sum"] / weighted["weight"]).to_numpy()}
    ).reset_index(drop=True)


def _cell_means(
    path: Path, grid: gpd.GeoDataFrame, boundary: BaseGeometry, pixel_m: float, chunk_cells: int
) -> pd.DataFrame:
    cell_size_m = grid_cell_size(grid)
    per_cell = pixels_per_cell(cell_size_m, pixel_m)
    wanted = set(grid["cell_id"])
    frames = []
    with rasterio.open(path) as source:
        for x0, y0, x1, y1 in grid_chunks(grid, chunk_cells):
            chunk = warp_to_grid(
                [source],
                grid.crs,
                (x0, y0, x1, y1),
                pixel_m,
                resampling=Resampling.nearest,
                nodata=0,
            )
            if chunk is None:
                continue
            chunk = np.where(region_mask(boundary, (x0, y0, x1, y1), pixel_m), chunk, np.nan)
            blocks = block_view(chunk, per_cell)
            has_data = (~np.isnan(blocks)).any(axis=2)
            rows, cols = np.nonzero(has_data)
            means = np.nanmean(blocks[rows, cols], axis=1) / PH_SCALE
            ids = [
                cell_id(int(x0 + c * cell_size_m), int(y1 - (r + 1) * cell_size_m), cell_size_m)
                for r, c in zip(rows, cols, strict=True)
            ]
            frame = pd.DataFrame({"cell_id": ids, "ph": means})
            frames.append(frame[frame["cell_id"].isin(wanted)])
    if not frames:
        return pd.DataFrame({"cell_id": [], "ph": []})
    return pd.concat(frames, ignore_index=True)
