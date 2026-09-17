"""Place labels per cell: the comune and the nearest inhabited locality, both from ISTAT.

The comune drives area aggregation (seasonal outlook, history) and search; the nearest place gives
hotspots a human label ("near Badia Prataglia").
"""

import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyogrio

# ISTAT locality types kept as place labels: 1 centro abitato, 2 nucleo abitato. Left out:
# 3 località produttiva (industrial areas) and 4 case sparse (scattered houses).
INHABITED_LOCALITY_TYPES = {1, 2}


def read_comuni(
    archive: Path, comuni_member: str, provinces_member: str, region_code: int, crs: str
) -> gpd.GeoDataFrame:
    """The region's comuni from the ISTAT boundary archive, with the province abbreviation."""
    comuni = gpd.read_file(f"zip://{archive}!{comuni_member}")
    provinces = gpd.read_file(f"zip://{archive}!{provinces_member}", ignore_geometry=True)
    comuni = comuni[comuni["COD_REG"] == region_code].merge(
        provinces[["COD_UTS", "SIGLA"]], on="COD_UTS", how="left"
    )
    comuni = comuni.rename(
        columns={"PRO_COM_T": "comune_code", "COMUNE": "comune_name", "SIGLA": "province"}
    )
    return comuni[["comune_code", "comune_name", "province", "geometry"]].to_crs(crs)


def assign_comuni(grid: gpd.GeoDataFrame, comuni: gpd.GeoDataFrame) -> pd.DataFrame:
    """For each cell, the comune that covers the largest share of it (null if none does)."""
    pieces = gpd.overlay(
        grid[["cell_id", "geometry"]],
        comuni.to_crs(grid.crs),
        how="intersection",
        keep_geom_type=True,
    )
    pieces["overlap"] = pieces.geometry.area
    best = pieces.sort_values(["cell_id", "overlap"], ascending=[True, False]).drop_duplicates(
        "cell_id"
    )
    return grid[["cell_id"]].merge(
        best[["cell_id", "comune_code", "comune_name", "province"]], on="cell_id", how="left"
    )


def read_istat_localities(
    archive: Path, bbox_wgs84: tuple[float, float, float, float], crs: str
) -> gpd.GeoDataFrame:
    """Inhabited localities (ISTAT Basi territoriali 2021 points) inside a lon/lat bbox."""
    with zipfile.ZipFile(archive) as zf:
        member = next(n for n in zf.namelist() if n.endswith(".shp"))
    points = pyogrio.read_dataframe(f"/vsizip/{archive}/{member}", columns=["NOME", "TIPO_LOC"])
    points = points[points["TIPO_LOC"].astype(int).isin(INHABITED_LOCALITY_TYPES)].to_crs(
        "EPSG:4326"
    )
    lon_min, lat_min, lon_max, lat_max = bbox_wgs84
    inside = points.geometry.x.between(lon_min, lon_max) & points.geometry.y.between(
        lat_min, lat_max
    )
    places = points.loc[inside, ["NOME", "geometry"]].rename(columns={"NOME": "place_name"})
    return places.reset_index(drop=True).to_crs(crs)


def nearest_place(grid: gpd.GeoDataFrame, places: gpd.GeoDataFrame) -> pd.DataFrame:
    """For each cell, the nearest settlement to its centre and the distance in km."""
    centres = grid.geometry.centroid
    places = places.to_crs(grid.crs).reset_index(drop=True)
    (cell_idx, place_idx), distance = places.sindex.nearest(
        centres, return_all=False, return_distance=True
    )
    order = np.argsort(cell_idx)
    return pd.DataFrame(
        {
            "cell_id": grid["cell_id"].to_numpy()[cell_idx[order]],
            "place_name": places["place_name"].to_numpy()[place_idx[order]],
            "place_distance_km": distance[order] / 1000.0,
        }
    )
