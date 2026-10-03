"""The fitted rain calibration field (``config/rain_scale_field.csv``, ``api.weather.rain_field``).

A regular lon/lat lattice of ``intercept``, ``per_km`` and ``max_elevation_m``. A cell's factor
is ``intercept + per_km x min(elevation, max_elevation_m) / 1000`` with all three read bilinearly at
the cell's position; positions off the lattice take its nearest edge. The same loader reads any
other lattice of named values (the ``era5_seamless`` / CDS rain ratio, ``ratio``).
"""

from dataclasses import dataclass
from functools import cache
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RainField:
    lats: np.ndarray  # ascending
    lons: np.ndarray  # ascending
    grids: dict[str, np.ndarray]  # field -> (lats, lons)

    def value(self, name: str, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
        """The lattice's ``name`` read bilinearly at each position."""
        lon, lat = np.asarray(lon, dtype=float), np.asarray(lat, dtype=float)
        grid = self.grids[name]
        fi = np.interp(lat, self.lats, np.arange(len(self.lats)))
        fj = np.interp(lon, self.lons, np.arange(len(self.lons)))
        i0 = np.minimum(np.floor(fi).astype(int), len(self.lats) - 2)
        j0 = np.minimum(np.floor(fj).astype(int), len(self.lons) - 2)
        dy, dx = fi - i0, fj - j0
        return (
            grid[i0, j0] * (1 - dy) * (1 - dx)
            + grid[i0, j0 + 1] * (1 - dy) * dx
            + grid[i0 + 1, j0] * dy * (1 - dx)
            + grid[i0 + 1, j0 + 1] * dy * dx
        )

    def factor(self, elevation_m: np.ndarray, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
        """The multiplier at each position and height (unknown heights count as sea level)."""
        lon, lat = np.asarray(lon, dtype=float), np.asarray(lat, dtype=float)
        elevation = np.clip(np.nan_to_num(np.asarray(elevation_m, dtype=float)), 0, None)
        top = self.value("max_elevation_m", lon, lat)
        return (
            self.value("intercept", lon, lat)
            + self.value("per_km", lon, lat) * np.minimum(elevation, top) / 1000
        )


@cache
def load_rain_field(path: Path) -> RainField:
    frame = pd.read_csv(path).sort_values(["lat", "lon"])
    lats, lons = np.unique(frame["lat"]), np.unique(frame["lon"])
    if len(frame) != len(lats) * len(lons) or len(lats) < 2 or len(lons) < 2:
        raise ValueError(f"{path}: not a full lon/lat lattice")
    grids = {
        name: frame[name].to_numpy(dtype=float).reshape(len(lats), len(lons))
        for name in frame.columns.drop(["lat", "lon"])
    }
    return RainField(lats, lons, grids)
