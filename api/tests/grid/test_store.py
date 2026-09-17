import json
from pathlib import Path

import duckdb
import pandas as pd
import pytest
from shapely.geometry import box

from api.grid.cells import generate_grid
from api.grid.store import map_geojson, write_grid

X0, Y0 = 4_453_000, 2_199_000  # Monte Amiata


def _cells() -> pd.DataFrame:
    grid = generate_grid(box(X0, Y0, X0 + 2000, Y0 + 1000), cell_size_m=1000)
    grid["woodland"] = [True, False]
    grid["forest_fraction"] = [0.92, 0.31]
    grid["dominant_habitat"] = ["beech", "chestnut"]
    grid["elevation_m"] = [1549.46, 1201.2]
    grid["comune_name"] = ["Castel del Piano", "Abbadia San Salvatore"]
    return grid


def _habitats() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "cell_id": ["1kmE4453N2199", "1kmE4453N2199", "1kmE4454N2199"],
            "habitat": ["beech", "chestnut", "chestnut"],
            "fraction": [0.8, 0.2, 1.0],
        }
    )


def test_write_grid_stores_parquet_that_duckdb_can_query(tmp_path: Path) -> None:
    paths = write_grid(_cells(), _habitats(), tmp_path, meta={"region": "tuscany"})

    con = duckdb.connect()
    woodland = con.execute(
        f"SELECT cell_id, dominant_habitat FROM '{paths['cells']}' WHERE woodland"
    ).fetchall()
    beech = con.execute(
        f"SELECT fraction FROM '{paths['habitats']}' "
        "WHERE cell_id = '1kmE4453N2199' AND habitat = 'beech'"
    ).fetchone()
    assert woodland == [("1kmE4453N2199", "beech")]
    assert beech == (pytest.approx(0.8),)


def test_write_grid_adds_the_wgs84_centre_of_each_cell(tmp_path: Path) -> None:
    paths = write_grid(_cells(), _habitats(), tmp_path, meta={})

    cells = pd.read_parquet(paths["cells"])
    amiata = cells.set_index("cell_id").loc["1kmE4453N2199"]
    assert amiata["lon"] == pytest.approx(11.62, abs=0.02)
    assert amiata["lat"] == pytest.approx(42.89, abs=0.02)


def test_write_grid_records_build_metadata(tmp_path: Path) -> None:
    paths = write_grid(_cells(), _habitats(), tmp_path, meta={"region": "tuscany"})

    meta = json.loads(paths["meta"].read_text())
    assert meta["region"] == "tuscany"
    assert meta["cell_count"] == 2
    assert meta["woodland_cell_count"] == 1


def test_map_geojson_has_only_woodland_cells_in_lon_lat_order() -> None:
    collection = map_geojson(_cells(), properties=["dominant_habitat", "elevation_m"])

    assert collection["type"] == "FeatureCollection"
    assert [f["id"] for f in collection["features"]] == ["1kmE4453N2199"]
    feature = collection["features"][0]
    ring = feature["geometry"]["coordinates"][0]
    assert feature["geometry"]["type"] == "Polygon"
    assert len(ring) == 5 and ring[0] == ring[-1]
    for lon, lat in ring:
        assert 11.5 < lon < 11.8 and 42.8 < lat < 43.0
    assert feature["properties"] == {"dominant_habitat": "beech", "elevation_m": 1549}


def test_map_geojson_rings_are_counter_clockwise_and_rounded() -> None:
    ring = map_geojson(_cells(), properties=[])["features"][0]["geometry"]["coordinates"][0]

    signed_area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:], strict=False))
    assert signed_area > 0  # RFC 7946 right-hand rule
    assert all(round(v, 5) == v for point in ring for v in point)
