import math
from pathlib import Path

import numpy as np
import pytest
import rasterio
from pyproj import Transformer
from rasterio.transform import from_origin
from shapely.geometry import box

from api.grid.cells import generate_grid
from api.grid.terrain import cell_stats, slope_aspect, terrain_for_cells

NAN = float("nan")


def test_a_plane_rising_to_the_south_faces_north() -> None:
    rows = np.arange(6, dtype=float)[:, None]  # row 0 is the northern edge
    dem = np.repeat(rows * 10.0, 6, axis=1)

    slope, aspect = slope_aspect(dem, pixel_m=10.0)

    assert slope[2:4, 2:4] == pytest.approx(45.0)
    assert aspect[2:4, 2:4] == pytest.approx(0.0)


def test_a_plane_rising_to_the_west_faces_east() -> None:
    cols = np.arange(6, dtype=float)[None, :]
    dem = np.repeat((5 - cols) * 5.0, 6, axis=0)

    slope, aspect = slope_aspect(dem, pixel_m=10.0)

    assert slope[2:4, 2:4] == pytest.approx(math.degrees(math.atan(0.5)))
    assert aspect[2:4, 2:4] == pytest.approx(90.0)


def test_flat_ground_has_no_aspect() -> None:
    slope, aspect = slope_aspect(np.full((4, 4), 250.0), pixel_m=25.0)

    assert np.all(slope == 0)
    assert np.all(np.isnan(aspect))


def test_cell_stats_for_a_flat_cell() -> None:
    stats = cell_stats(
        np.full((4, 4), 100.0), x_left=4_000_000, y_top=2_001_000, pixel_m=250.0, cell_size_m=1000
    )

    row = stats.iloc[0]
    assert row["cell_id"] == "1kmE4000N2000"
    assert (row["elevation_m"], row["slope_deg"], row["northness"]) == (100.0, 0.0, 0.0)
    assert np.isnan(row["aspect_deg"])


def test_cell_stats_for_a_north_facing_cell() -> None:
    dem = 400.0 + np.repeat(np.arange(4)[:, None] * 250.0, 4, axis=1)

    row = cell_stats(dem, x_left=4_000_000, y_top=2_001_000, pixel_m=250.0, cell_size_m=1000).iloc[
        0
    ]

    assert row["elevation_m"] == pytest.approx(775.0)
    assert (row["elevation_min_m"], row["elevation_max_m"]) == (400.0, 1150.0)
    assert row["slope_deg"] == pytest.approx(45.0)
    assert row["aspect_deg"] == pytest.approx(0.0)
    assert row["northness"] == pytest.approx(1.0)


def test_cell_stats_split_pixels_into_grid_cells() -> None:
    dem = np.empty((8, 8))
    dem[:, :4] = 100.0
    dem[:, 4:] = 400.0

    stats = cell_stats(dem, x_left=4_000_000, y_top=2_002_000, pixel_m=250.0, cell_size_m=1000)

    elevations = dict(zip(stats["cell_id"], stats["elevation_m"], strict=True))
    assert elevations == {
        "1kmE4000N2000": 100.0,
        "1kmE4001N2000": 400.0,
        "1kmE4000N2001": 100.0,
        "1kmE4001N2001": 400.0,
    }


def test_a_symmetric_ridge_has_no_dominant_aspect() -> None:
    profile = np.array([0.0, 250.0, 500.0, 750.0, 750.0, 500.0, 250.0, 0.0])
    dem = np.repeat(profile[:, None], 8, axis=1)  # ridge running east-west

    stats = cell_stats(dem, x_left=0, y_top=2000, pixel_m=250.0, cell_size_m=2000)
    row = stats.iloc[0]

    assert row["slope_deg"] > 30
    assert row["northness"] == pytest.approx(0.0, abs=1e-9)
    assert np.isnan(row["aspect_deg"])


def test_cell_stats_ignore_nodata_and_skip_empty_cells() -> None:
    dem = np.full((4, 8), 300.0)
    dem[:2, :4] = NAN  # half the west cell is outside the region
    dem[:, 4:] = NAN  # the east cell is entirely outside

    stats = cell_stats(dem, x_left=0, y_top=1000, pixel_m=250.0, cell_size_m=1000)

    assert stats["cell_id"].tolist() == ["1kmE0N0"]
    assert stats.iloc[0]["elevation_m"] == 300.0
    assert stats.iloc[0]["valid_fraction"] == 0.5


def _write_lat_ramp_geotiff(path: Path, lon0: float, lat0: float, lon1: float, lat1: float) -> None:
    """A WGS84 raster whose height falls 100 m per km going north (so it faces north)."""
    res = 1 / 3600
    width, height = round((lon1 - lon0) / res), round((lat1 - lat0) / res)
    lats = lat1 - (np.arange(height) + 0.5) * res
    metres_south_of_top = (lat1 - lats) * 111_320.0
    dem = np.repeat((1000.0 + 0.1 * metres_south_of_top)[:, None], width, axis=1)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=width,
        height=height,
        count=1,
        dtype="float32",
        crs="EPSG:4326",
        transform=from_origin(lon0, lat1, res, res),
    ) as dst:
        dst.write(dem.astype("float32"), 1)


def test_terrain_for_cells_warps_the_dem_onto_the_grid(tmp_path: Path) -> None:
    to_laea = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)
    x, y = to_laea.transform(11.0, 43.5)
    x0, y0 = int(x // 1000) * 1000, int(y // 1000) * 1000
    region = box(x0, y0, x0 + 3000, y0 + 2000)
    grid = generate_grid(region, cell_size_m=1000)
    tif = tmp_path / "dem.tif"
    _write_lat_ramp_geotiff(tif, 10.9, 43.4, 11.1, 43.6)

    terrain = terrain_for_cells([tif], grid, region, pixel_m=25.0, chunk_cells=2)

    assert sorted(terrain["cell_id"]) == sorted(grid["cell_id"])
    assert terrain["valid_fraction"].tolist() == pytest.approx([1.0] * 6)
    assert terrain["slope_deg"].tolist() == pytest.approx(
        [math.degrees(math.atan(0.1))] * 6, abs=0.3
    )
    # LAEA north is a few degrees off true north away from the projection centre (10°E).
    assert terrain["aspect_deg"].apply(lambda a: min(a, 360 - a)).max() < 5
    assert terrain["northness"].tolist() == pytest.approx([1.0] * 6, abs=0.01)
    by_id = terrain.set_index("cell_id")
    south, north = (
        by_id.loc[f"1kmE{x0 // 1000}N{y0 // 1000}"],
        by_id.loc[f"1kmE{x0 // 1000}N{y0 // 1000 + 1}"],
    )
    assert south["elevation_m"] - north["elevation_m"] == pytest.approx(100.0, abs=2.0)


def test_terrain_for_cells_ignores_dem_outside_the_region(tmp_path: Path) -> None:
    to_laea = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)
    x, y = to_laea.transform(11.0, 43.5)
    x0, y0 = int(x // 1000) * 1000, int(y // 1000) * 1000
    region = box(x0, y0, x0 + 500, y0 + 1000)  # only the western half of one cell
    grid = generate_grid(region, cell_size_m=1000)
    tif = tmp_path / "dem.tif"
    _write_lat_ramp_geotiff(tif, 10.9, 43.4, 11.1, 43.6)

    terrain = terrain_for_cells([tif], grid, region, pixel_m=25.0)

    assert terrain["valid_fraction"].tolist() == pytest.approx([0.5])
