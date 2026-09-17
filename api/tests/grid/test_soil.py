from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import rasterio
from pyproj import Transformer
from rasterio.transform import from_origin
from shapely.geometry import box

from api.grid.cells import generate_grid
from api.grid.soil import depth_weighted_ph, soil_ph_for_cells


def _write_ph_geotiff(path: Path, fill: np.ndarray) -> None:
    """SoilGrids-like int16 raster (pH x 10, 0 = no data) over 10.9–11.1 E, 43.4–43.6 N."""
    res = 0.002
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=fill.shape[1],
        height=fill.shape[0],
        count=1,
        dtype="int16",
        crs="EPSG:4326",
        transform=from_origin(10.9, 43.6, res, res),
    ) as dst:
        dst.write(fill.astype("int16"), 1)


def _region_at(lon: float, lat: float, width_km: int = 2) -> tuple[object, int, int]:
    x, y = Transformer.from_crs(4326, 3035, always_xy=True).transform(lon, lat)
    x0, y0 = int(x // 1000) * 1000, int(y // 1000) * 1000
    return box(x0, y0, x0 + width_km * 1000, y0 + 1000), x0, y0


def test_soil_ph_is_the_cell_mean_rescaled_from_soilgrids_units(tmp_path: Path) -> None:
    tif = tmp_path / "ph.tif"
    _write_ph_geotiff(tif, np.full((100, 100), 55))
    region, _, _ = _region_at(11.0, 43.5)
    grid = generate_grid(region, cell_size_m=1000)

    ph = soil_ph_for_cells({"0-5cm": tif}, grid, region)

    assert ph["soil_ph"].tolist() == pytest.approx([5.5, 5.5])


def test_soil_ph_ignores_no_data_pixels(tmp_path: Path) -> None:
    values = np.full((100, 100), 70)
    values[::2, :] = 0  # every other row (about 220 m) has no data
    tif = tmp_path / "ph.tif"
    _write_ph_geotiff(tif, values)
    region, _, _ = _region_at(11.0, 43.5, width_km=1)
    grid = generate_grid(region, cell_size_m=1000)

    ph = soil_ph_for_cells({"0-5cm": tif}, grid, region)

    assert ph["soil_ph"].tolist() == pytest.approx([7.0])


def test_topsoil_ph_weights_each_layer_by_its_thickness() -> None:
    layers = {
        "0-5cm": pd.DataFrame({"cell_id": ["a", "b"], "ph": [5.0, 6.0]}),
        "5-15cm": pd.DataFrame({"cell_id": ["a", "b"], "ph": [6.0, np.nan]}),
        "15-30cm": pd.DataFrame({"cell_id": ["a", "b"], "ph": [7.0, 6.0]}),
    }

    ph = depth_weighted_ph(layers).set_index("cell_id")["soil_ph"]

    assert ph["a"] == pytest.approx((5 * 5.0 + 10 * 6.0 + 15 * 7.0) / 30)
    assert ph["b"] == pytest.approx(6.0)  # missing layer drops out of the weights
