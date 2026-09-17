"""Weather points: the coarse lattice weather is fetched on, and how cells borrow from it.

Weather models are far coarser than the 1 km grid, so weather is fetched once per model node and
downscaled to cells (see ``api.weather.downscale``). The nodes form a regular lon/lat lattice at the
source model's spacing (ERA5-Land: 0.1°), optionally thinned by a stride. A node is named by its
coordinates, e.g. ``N43.80E011.80``, so ids are stable whatever the stride.

Only nodes on land carry ERA5-Land data; the caller filters them before computing weights, and a
cell whose lattice square has no land corner falls back to the nearest land node within reach.
"""

import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6371.0
METHODS = ("bilinear", "nearest")
# Tolerance, in lattice steps, that absorbs float noise when a coordinate sits on a node.
_INDEX_EPS = 1e-6


def point_id(lat: float, lon: float) -> str:
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{ns}{abs(lat):05.2f}{ew}{abs(lon):06.2f}"


def _node(index: np.ndarray, spacing_deg: float) -> np.ndarray:
    return np.round(index * spacing_deg, 6)


def candidate_points(cells: pd.DataFrame, spacing_deg: float) -> pd.DataFrame:
    """The lattice nodes at the corners of the lattice square around each cell centre."""
    i0 = np.floor(cells["lat"].to_numpy() / spacing_deg + _INDEX_EPS).astype(np.int64)
    j0 = np.floor(cells["lon"].to_numpy() / spacing_deg + _INDEX_EPS).astype(np.int64)
    nodes = {
        (i + di, j + dj) for i, j in zip(i0, j0, strict=True) for di in (0, 1) for dj in (0, 1)
    }
    index = np.array(sorted(nodes), dtype=np.int64).reshape(-1, 2)
    lat, lon = _node(index[:, 0], spacing_deg), _node(index[:, 1], spacing_deg)
    points = pd.DataFrame(
        {
            "point_id": [point_id(a, o) for a, o in zip(lat, lon, strict=True)],
            "lat": lat,
            "lon": lon,
        }
    )
    return points.sort_values("point_id", ignore_index=True)


def distance_km(
    lat1: np.ndarray, lon1: np.ndarray, lat2: np.ndarray, lon2: np.ndarray
) -> np.ndarray:
    """Great-circle distance (haversine); arguments broadcast."""
    lat1, lon1, lat2, lon2 = (np.radians(a) for a in (lat1, lon1, lat2, lon2))
    h = (
        np.sin((lat2 - lat1) / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(h))


def interpolation_weights(
    cells: pd.DataFrame,
    points: pd.DataFrame,
    spacing_deg: float,
    method: str,
    max_distance_km: float = 30.0,
) -> pd.DataFrame:
    """``(cell_id, point_id, weight)`` rows; each cell's weights sum to 1.

    ``bilinear`` weights the four corners of the cell's lattice square by position, dropping
    corners missing from ``points`` (sea) and renormalising. ``nearest`` takes the closest node.
    A bilinear cell with no usable corner falls back to the nearest node. That fallback, and
    ``nearest``, stop at ``max_distance_km``: a cell with nothing within reach gets no rows.
    """
    if method not in METHODS:
        raise ValueError(f"unknown interpolation method {method!r}; expected one of {METHODS}")
    available = set(points["point_id"])
    rows: list[tuple[str, str, float]] = []
    unassigned = []

    if method == "bilinear":
        for cell in cells.itertuples():
            y, x = cell.lat / spacing_deg, cell.lon / spacing_deg
            i0, j0 = int(np.floor(y + _INDEX_EPS)), int(np.floor(x + _INDEX_EPS))
            fy, fx = min(max(y - i0, 0.0), 1.0), min(max(x - j0, 0.0), 1.0)
            corners = [
                (i0, j0, (1 - fy) * (1 - fx)),
                (i0, j0 + 1, (1 - fy) * fx),
                (i0 + 1, j0, fy * (1 - fx)),
                (i0 + 1, j0 + 1, fy * fx),
            ]
            usable = []
            for i, j, w in corners:
                pid = point_id(*_node(np.array([i, j]), spacing_deg))
                if w > _INDEX_EPS and pid in available:
                    usable.append((pid, w))
            total = sum(w for _, w in usable)
            if total > 0:
                rows.extend((cell.cell_id, pid, w / total) for pid, w in usable)
            else:
                unassigned.append(cell)
    else:
        unassigned = list(cells.itertuples())

    if unassigned and len(points):
        lat = np.array([c.lat for c in unassigned])[:, None]
        lon = np.array([c.lon for c in unassigned])[:, None]
        dist = distance_km(
            lat, lon, points["lat"].to_numpy()[None, :], points["lon"].to_numpy()[None, :]
        )
        nearest = dist.argmin(axis=1)
        for cell, k, d in zip(
            unassigned, nearest, dist[np.arange(len(unassigned)), nearest], strict=True
        ):
            if d <= max_distance_km:
                rows.append((cell.cell_id, points["point_id"].iloc[k], 1.0))

    weights = pd.DataFrame(rows, columns=["cell_id", "point_id", "weight"])
    return weights.sort_values(["cell_id", "point_id"], ignore_index=True)


def footprint_elevation(cells: pd.DataFrame, points: pd.DataFrame, spacing_deg: float) -> pd.Series:
    """Mean DEM elevation of the grid cells whose centre is closest to each node, by point id."""
    lat = _node(np.round(cells["lat"].to_numpy() / spacing_deg), spacing_deg)
    lon = _node(np.round(cells["lon"].to_numpy() / spacing_deg), spacing_deg)
    ids = [point_id(a, o) for a, o in zip(lat, lon, strict=True)]
    means = cells.assign(point_id=ids).groupby("point_id")["elevation_m"].mean()
    return means.reindex(points["point_id"]).rename("dem_elevation_m")
