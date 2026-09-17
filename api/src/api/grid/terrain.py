"""Terrain per cell from a DEM: elevation, slope and aspect.

The DEM is warped onto a raster aligned with the grid (``cell_size_m / pixel_m`` pixels per cell
side), slope and aspect are computed per pixel in metres, then pixels are reduced to cells. Pixels
outside the region boundary are dropped, so a border cell describes only its part inside the region.

- ``elevation_m``: mean height; ``elevation_min_m`` / ``elevation_max_m`` the range.
- ``slope_deg``: mean of the pixel slopes (not the slope of the mean surface).
- ``northness``: mean of cos(aspect) over pixels, with flat pixels counting as 0. +1 means the whole
  cell faces north, -1 south, 0 flat or facing every way.
- ``aspect_deg``: compass bearing the cell mostly faces (0 = N, 90 = E), the circular mean of pixel
  aspects. Null when the cell is flat or its slopes cancel out (no dominant facing).
- ``valid_fraction``: share of the cell's pixels that are inside the region and have DEM data.
"""

import warnings
from collections.abc import Sequence
from contextlib import ExitStack
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
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

# Below this slope a pixel has no meaningful aspect (DEM noise dominates).
FLAT_SLOPE_DEG = 2.0
# Minimum length of the mean aspect vector (0..1) for a cell to have a dominant facing.
MIN_ASPECT_CONSISTENCY = 0.1


def slope_aspect(dem: np.ndarray, pixel_m: float) -> tuple[np.ndarray, np.ndarray]:
    """Per-pixel slope (degrees) and aspect (compass degrees, NaN where flat).

    ``dem`` rows run north to south and columns west to east, as in a north-up raster.
    """
    d_row, d_col = np.gradient(dem, pixel_m)
    dz_east, dz_north = d_col, -d_row
    slope = np.degrees(np.arctan(np.hypot(dz_east, dz_north)))
    # Aspect is the downslope direction, measured clockwise from north.
    aspect = np.degrees(np.arctan2(-dz_east, -dz_north)) % 360.0
    return slope, np.where(slope > 0, aspect, np.nan)


def cell_stats(
    dem: np.ndarray, x_left: float, y_top: float, pixel_m: float, cell_size_m: int
) -> pd.DataFrame:
    """Reduce a grid-aligned DEM (NaN = no data) to one row of terrain stats per cell with data."""
    slope, aspect = slope_aspect(dem, pixel_m)
    return _reduce(dem, slope, aspect, x_left, y_top, pixel_m, cell_size_m)


def _reduce(
    dem: np.ndarray,
    slope: np.ndarray,
    aspect: np.ndarray,
    x_left: float,
    y_top: float,
    pixel_m: float,
    cell_size_m: int,
) -> pd.DataFrame:
    per_cell = pixels_per_cell(cell_size_m, pixel_m)

    def blocks(a: np.ndarray) -> np.ndarray:
        return block_view(a, per_cell)

    valid = ~np.isnan(dem)
    sloped = valid & (slope >= FLAT_SLOPE_DEG) & ~np.isnan(aspect)
    radians = np.radians(np.where(sloped, aspect, 0.0))
    n_valid = blocks(valid).sum(axis=2)
    has_data = n_valid > 0

    with warnings.catch_warnings(), np.errstate(invalid="ignore", divide="ignore"):
        warnings.simplefilter("ignore", RuntimeWarning)  # all-NaN blocks are dropped below
        mean_north = blocks(np.where(sloped, np.cos(radians), 0.0)).sum(axis=2) / n_valid
        mean_east = blocks(np.where(sloped, np.sin(radians), 0.0)).sum(axis=2) / n_valid
        elevation = blocks(dem)
        stats = {
            "elevation_m": np.nanmean(elevation, axis=2),
            "elevation_min_m": np.nanmin(elevation, axis=2),
            "elevation_max_m": np.nanmax(elevation, axis=2),
            "slope_deg": np.nanmean(blocks(np.where(valid, slope, np.nan)), axis=2),
        }
    dominant = np.hypot(mean_north, mean_east) >= MIN_ASPECT_CONSISTENCY
    bearing = np.degrees(np.arctan2(mean_east, mean_north)) % 360.0
    stats["aspect_deg"] = np.where(dominant, bearing, np.nan)
    stats["northness"] = mean_north
    stats["valid_fraction"] = n_valid / per_cell**2

    row_idx, col_idx = np.nonzero(has_data)
    x_min = np.round(x_left + col_idx * cell_size_m).astype(np.int64)
    y_min = np.round(y_top - (row_idx + 1) * cell_size_m).astype(np.int64)
    ids = [cell_id(int(x), int(y), cell_size_m) for x, y in zip(x_min, y_min, strict=True)]
    frame = pd.DataFrame({"cell_id": ids})
    for name, values in stats.items():
        frame[name] = values[row_idx, col_idx]
    return frame


def terrain_for_cells(
    dem_paths: Sequence[Path],
    grid: gpd.GeoDataFrame,
    boundary: BaseGeometry,
    pixel_m: float = 25.0,
    chunk_cells: int = 50,
) -> pd.DataFrame:
    """Terrain stats for every cell of ``grid`` from DEM tiles in any CRS.

    Works through the grid in square chunks of ``chunk_cells`` cells so memory stays bounded.
    ``boundary`` is in the grid's CRS; DEM pixels outside it are ignored.
    """
    cell_size_m = grid_cell_size(grid)
    pixels_per_cell(cell_size_m, pixel_m)
    wanted = set(grid["cell_id"])

    frames = []
    with ExitStack() as stack:
        sources = [stack.enter_context(rasterio.open(p)) for p in dem_paths]
        for x0, y0, x1, y1 in grid_chunks(grid, chunk_cells):
            # One pixel of padding lets slopes on the chunk edge see their neighbours.
            chunk = warp_to_grid(sources, grid.crs, (x0, y0, x1, y1), pixel_m, pad=1)
            if chunk is None:
                continue
            slope, aspect = slope_aspect(chunk, pixel_m)
            chunk, slope, aspect = (a[1:-1, 1:-1] for a in (chunk, slope, aspect))
            chunk = np.where(region_mask(boundary, (x0, y0, x1, y1), pixel_m), chunk, np.nan)
            stats = _reduce(chunk, slope, aspect, x0, y1, pixel_m, cell_size_m)
            frames.append(stats[stats["cell_id"].isin(wanted)])

    if not frames:
        raise ValueError("the DEM tiles do not overlap any grid cell")
    return pd.concat(frames, ignore_index=True).sort_values("cell_id", ignore_index=True)
