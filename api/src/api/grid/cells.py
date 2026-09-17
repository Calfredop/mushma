"""Grid cells on the EEA reference grid.

Cells are squares in a projected CRS (EPSG:3035 for the EEA grid), aligned to multiples of the cell
size. A cell is named by its lower-left corner in cell-size units, e.g. ``1kmE4321N2345`` is the
1 km cell whose corner is at E 4 321 000 m, N 2 345 000 m. The id depends only on the corner, so it
is stable across rebuilds and matches other EEA-grid datasets.
"""

import re

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry.base import BaseGeometry

_ID_RE = re.compile(r"^(\d+)(km|m)E(\d+)N(\d+)$")


def _resolution_label(size_m: int) -> tuple[str, int]:
    if size_m >= 1000 and size_m % 1000 == 0:
        return f"{size_m // 1000}km", size_m
    return f"{size_m}m", size_m


def cell_id(x_min: int, y_min: int, size_m: int) -> str:
    """EEA reference grid code for the cell with lower-left corner ``(x_min, y_min)``."""
    if x_min % size_m or y_min % size_m:
        raise ValueError(f"corner ({x_min}, {y_min}) is not a multiple of the {size_m} m cell size")
    label, unit = _resolution_label(size_m)
    return f"{label}E{x_min // unit}N{y_min // unit}"


def parse_cell_id(code: str) -> tuple[int, int, int]:
    """Inverse of :func:`cell_id`: ``(x_min, y_min, size_m)``."""
    match = _ID_RE.match(code)
    if not match:
        raise ValueError(f"not an EEA grid cell code: {code!r}")
    number, unit, east, north = match.groups()
    size_m = int(number) * (1000 if unit == "km" else 1)
    return int(east) * size_m, int(north) * size_m, size_m


def generate_grid(
    boundary: BaseGeometry, cell_size_m: int, crs: str = "EPSG:3035"
) -> gpd.GeoDataFrame:
    """All grid cells whose area overlaps ``boundary`` (given in ``crs``).

    ``region_fraction`` is the share of the cell's area inside the boundary. Cells that only touch
    the boundary along an edge or at a corner are left out.
    """
    x0, y0, x1, y1 = boundary.bounds
    xs = np.arange(np.floor(x0 / cell_size_m), np.ceil(x1 / cell_size_m), dtype=np.int64)
    ys = np.arange(np.floor(y0 / cell_size_m), np.ceil(y1 / cell_size_m), dtype=np.int64)
    xx, yy = (a.ravel() * cell_size_m for a in np.meshgrid(xs, ys))
    squares = shapely.box(xx, yy, xx + cell_size_m, yy + cell_size_m)

    shapely.prepare(boundary)
    candidates = shapely.intersects(boundary, squares)
    xx, yy, squares = xx[candidates], yy[candidates], squares[candidates]
    inside = shapely.area(shapely.intersection(squares, boundary)) / cell_size_m**2
    keep = inside > 0

    grid = gpd.GeoDataFrame(
        {
            "cell_id": [
                cell_id(int(x), int(y), cell_size_m)
                for x, y in zip(xx[keep], yy[keep], strict=True)
            ],
            "x_min": xx[keep],
            "y_min": yy[keep],
            "region_fraction": inside[keep],
        },
        geometry=squares[keep],
        crs=crs,
    )
    return grid.sort_values("cell_id", ignore_index=True)
