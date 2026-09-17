"""Persist the grid as Parquet (queried with DuckDB) and export a WGS84 GeoJSON for the map.

Layout under ``$DATA_DIR/grid/<region>/``:

- ``cells.parquet``: one row per cell intersecting the region (GeoParquet, EPSG:3035 squares), with
  the WGS84 centre, woodland mask, habitat summary, terrain and place labels.
- ``cell_habitats.parquet``: long table ``(cell_id, habitat, fraction)``; fractions sum to 1 per
  woodland cell. Species rules score habitat as the sum of fraction x affinity.
- ``meta.json``: build metadata (sources, thresholds, counts).
- ``cells_wgs84.geojson``: woodland cells only, for the map.
"""

import json
import math
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyproj import Transformer

from api.grid.cells import parse_cell_id

# Decimal places per exported property; 0 means an integer. Unlisted floats keep 3 decimals.
MAP_ROUNDING = {"elevation_m": 0, "slope_deg": 0, "aspect_deg": 0, "forest_fraction": 2}
# 5 decimals of a degree is about 1 m, well under the 1 km cell size.
COORD_DECIMALS = 5


def write_grid(
    cells: gpd.GeoDataFrame, habitats: pd.DataFrame, out_dir: Path, meta: dict
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cells = cells.copy()
    centres = cells.geometry.centroid.to_crs("EPSG:4326")
    cells["lon"], cells["lat"] = centres.x.round(6), centres.y.round(6)

    paths = {
        "cells": out_dir / "cells.parquet",
        "habitats": out_dir / "cell_habitats.parquet",
        "meta": out_dir / "meta.json",
    }
    cells.to_parquet(paths["cells"], index=False)
    habitats.to_parquet(paths["habitats"], index=False)
    meta = {
        **meta,
        "cell_count": int(len(cells)),
        "woodland_cell_count": int(cells["woodland"].sum()),
    }
    paths["meta"].write_text(json.dumps(meta, indent=2, ensure_ascii=False, default=str) + "\n")
    return paths


def map_geojson(cells: pd.DataFrame, properties: list[str], crs: str = "EPSG:3035") -> dict:
    """Woodland cells as a GeoJSON FeatureCollection of WGS84 squares (``[lon, lat]``)."""
    woodland = cells[cells["woodland"]]
    to_wgs84 = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    features = []
    for record in woodland[["cell_id", *properties]].to_dict("records"):
        x, y, size = parse_cell_id(record["cell_id"])
        # Counter-clockwise from the lower-left corner (RFC 7946 right-hand rule).
        xs = np.array([x, x + size, x + size, x, x], dtype=float)
        ys = np.array([y, y, y + size, y + size, y], dtype=float)
        lons, lats = to_wgs84.transform(xs, ys)
        ring = [
            [round(float(lon), COORD_DECIMALS), round(float(lat), COORD_DECIMALS)]
            for lon, lat in zip(lons, lats, strict=True)
        ]
        features.append(
            {
                "type": "Feature",
                "id": record["cell_id"],
                "geometry": {"type": "Polygon", "coordinates": [ring]},
                "properties": {name: _json_value(name, record[name]) for name in properties},
            }
        )
    return {"type": "FeatureCollection", "features": features}


def write_map_geojson(cells: pd.DataFrame, properties: list[str], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(map_geojson(cells, properties), separators=(",", ":")))
    return path


def _json_value(name: str, value: object) -> object:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    if isinstance(value, np.bool_ | bool):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, float | np.floating):
        decimals = MAP_ROUNDING.get(name, 3)
        return int(round(float(value))) if decimals == 0 else round(float(value), decimals)
    return value
