"""Shared raster plumbing: walk the grid in chunks and warp source rasters onto it."""

from collections.abc import Iterator

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.features
import rasterio.merge
import rasterio.warp
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from shapely.geometry import box
from shapely.geometry.base import BaseGeometry

from api.grid.cells import parse_cell_id

Bounds = tuple[float, float, float, float]


def grid_cell_size(grid: gpd.GeoDataFrame) -> int:
    return parse_cell_id(grid["cell_id"].iloc[0])[2]


def pixels_per_cell(cell_size_m: int, pixel_m: float) -> int:
    per_cell = round(cell_size_m / pixel_m)
    if per_cell * pixel_m != cell_size_m:
        raise ValueError(f"pixel_m {pixel_m} must divide the cell size {cell_size_m}")
    return per_cell


def grid_chunks(grid: gpd.GeoDataFrame, chunk_cells: int) -> Iterator[Bounds]:
    """Grid-aligned square chunks of ``chunk_cells`` cells that contain at least one grid cell."""
    cell_size_m = grid_cell_size(grid)
    ix = (grid["x_min"] // cell_size_m).to_numpy()
    iy = (grid["y_min"] // cell_size_m).to_numpy()
    for cx in range(ix.min(), ix.max() + 1, chunk_cells):
        for cy in range(iy.min(), iy.max() + 1, chunk_cells):
            inside = (ix >= cx) & (ix < cx + chunk_cells) & (iy >= cy) & (iy < cy + chunk_cells)
            if inside.any():
                x0, y0 = cx * cell_size_m, cy * cell_size_m
                yield x0, y0, x0 + chunk_cells * cell_size_m, y0 + chunk_cells * cell_size_m


def warp_to_grid(
    sources: list[rasterio.DatasetReader],
    dst_crs: object,
    bounds: Bounds,
    pixel_m: float,
    pad: int = 0,
    resampling: Resampling = Resampling.bilinear,
    nodata: float | None = None,
) -> np.ndarray | None:
    """Mosaic ``sources`` onto a north-up raster over ``bounds`` (plus ``pad`` pixels each side).

    Returns float64 with NaN where there is no data, or None if no source overlaps. ``nodata``
    overrides the sources' own no-data value.
    """
    x0, y0, x1, y1 = bounds
    width = round((x1 - x0) / pixel_m) + 2 * pad
    height = round((y1 - y0) / pixel_m) + 2 * pad
    padded = (x0 - pad * pixel_m, y0 - pad * pixel_m, x1 + pad * pixel_m, y1 + pad * pixel_m)
    dst_transform = from_origin(padded[0], padded[3], pixel_m, pixel_m)

    src_crs = sources[0].crs
    west, south, east, north = rasterio.warp.transform_bounds(
        dst_crs, src_crs, *padded, densify_pts=21
    )
    margin = 2 * max(abs(sources[0].res[0]), abs(sources[0].res[1]))
    window = (west - margin, south - margin, east + margin, north + margin)
    overlapping = [
        s
        for s in sources
        if s.bounds.left < window[2]
        and s.bounds.right > window[0]
        and s.bounds.bottom < window[3]
        and s.bounds.top > window[1]
    ]
    if not overlapping:
        return None

    if nodata is None:
        nodata = overlapping[0].nodata if overlapping[0].nodata is not None else -32767.0
    mosaic, src_transform = rasterio.merge.merge(
        overlapping, bounds=window, indexes=[1], dtype="float32", nodata=nodata
    )
    destination = np.full((height, width), np.nan, dtype="float32")
    rasterio.warp.reproject(
        source=mosaic[0],
        destination=destination,
        src_transform=src_transform,
        src_crs=src_crs,
        src_nodata=nodata,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        dst_nodata=np.nan,
        resampling=resampling,
    )
    return destination.astype("float64")


def block_view(a: np.ndarray, per_cell: int) -> np.ndarray:
    """``(rows, cols, per_cell**2)`` view of a raster made of whole cells."""
    rows, cols = a.shape[0] // per_cell, a.shape[1] // per_cell
    a = a[: rows * per_cell, : cols * per_cell]
    return a.reshape(rows, per_cell, cols, per_cell).swapaxes(1, 2).reshape(rows, cols, -1)


def region_mask(boundary: BaseGeometry, bounds: Bounds, pixel_m: float) -> np.ndarray:
    """Pixels of the grid-aligned raster over ``bounds`` whose centre lies in ``boundary``."""
    x0, y0, x1, y1 = bounds
    shape = (round((y1 - y0) / pixel_m), round((x1 - x0) / pixel_m))
    inside = boundary.intersection(box(x0, y0, x1, y1))
    if inside.is_empty:
        return np.zeros(shape, dtype=bool)
    return rasterio.features.geometry_mask(
        [inside], out_shape=shape, transform=from_origin(x0, y1, pixel_m, pixel_m), invert=True
    )
