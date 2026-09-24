"""Loader dispatch for any vector source declared in sources.yaml."""

import json
import threading
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import geopandas as gpd
import pytest
from shapely.geometry import box

from api.grid.sources import read_vector

X0, Y0 = 4_400_000, 2_300_000


def _frame(*geoms: object, **columns: list) -> gpd.GeoDataFrame:
    data = {name: values for name, values in columns.items()}
    return gpd.GeoDataFrame(data, geometry=list(geoms), crs="EPSG:3035")


def test_read_vector_loads_a_shapefile_from_a_zip(tmp_path: Path) -> None:
    layer = _frame(box(X0, Y0, X0 + 100, Y0 + 100), code=["311"])
    archive = tmp_path / "cover.zip"
    shp_dir = tmp_path / "shp"
    shp_dir.mkdir()
    layer.to_file(shp_dir / "cover.shp")
    with zipfile.ZipFile(archive, "w") as zf:
        for part in shp_dir.iterdir():
            zf.write(part, f"cover/{part.name}")

    frames = read_vector(
        {"url": archive.as_uri(), "shapefile": "cover.shp"},
        tmp_path / "cache",
    )

    assert list(frames["code"]) == ["311"]
    assert len(frames) == 1


def test_read_vector_loads_a_geopackage(tmp_path: Path) -> None:
    layer = _frame(box(X0, Y0, X0 + 100, Y0 + 100), code=["312"])
    gpkg = tmp_path / "cover.gpkg"
    layer.to_file(gpkg, layer="forest", driver="GPKG")

    frames = read_vector(
        {"url": gpkg.as_uri(), "geopackage": True, "layer": "forest"},
        tmp_path / "cache",
    )

    assert list(frames["code"]) == ["312"]


def test_read_vector_loads_a_named_layer_inside_a_zip(tmp_path: Path) -> None:
    layer = _frame(box(X0, Y0, X0 + 100, Y0 + 100), code=["313"])
    gpkg = tmp_path / "inner.gpkg"
    layer.to_file(gpkg, layer="woods", driver="GPKG")
    archive = tmp_path / "pack.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(gpkg, "data/inner.gpkg")

    frames = read_vector(
        {"url": archive.as_uri(), "layer": "woods", "member": "data/inner.gpkg"},
        tmp_path / "cache",
    )

    assert list(frames["code"]) == ["313"]


class _FakeArcGIS(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        body = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"clc18": "3111"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [4_400_000, 2_300_000],
                                [4_400_100, 2_300_000],
                                [4_400_100, 2_300_100],
                                [4_400_000, 2_300_100],
                                [4_400_000, 2_300_000],
                            ]
                        ],
                    },
                }
            ],
            "exceededTransferLimit": False,
        }
        payload = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


def test_read_vector_pages_an_arcgis_rest_layer(tmp_path: Path) -> None:
    server = HTTPServer(("127.0.0.1", 0), _FakeArcGIS)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        frames = read_vector(
            {
                "arcgis_layer": f"http://127.0.0.1:{server.server_port}/MapServer/4",
                "field": "clc18",
            },
            tmp_path / "cache",
            bbox_wgs84=(9.6, 42.1, 12.5, 44.6),
        )
    finally:
        server.shutdown()

    assert list(frames["clc18"]) == ["3111"]


class _FakeWFS(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        query = parse_qs(urlparse(self.path).query)
        assert query.get("SERVICE", ["WFS"])[0].upper() == "WFS"
        assert "GetFeature" in query.get("REQUEST", ["GetFeature"])
        body = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"code": "3231"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [11.0, 43.0],
                                [11.1, 43.0],
                                [11.1, 43.1],
                                [11.0, 43.1],
                                [11.0, 43.0],
                            ]
                        ],
                    },
                }
            ],
        }
        payload = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


def test_read_vector_fetches_a_wfs_layer(tmp_path: Path) -> None:
    server = HTTPServer(("127.0.0.1", 0), _FakeWFS)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        frames = read_vector(
            {
                "wfs": f"http://127.0.0.1:{server.server_port}/wfs",
                "type_name": "forest:cover",
                "output_format": "application/json",
            },
            tmp_path / "cache",
            bbox_wgs84=(10.9, 42.9, 11.2, 43.2),
        )
    finally:
        server.shutdown()

    assert list(frames["code"]) == ["3231"]


def test_read_vector_rejects_an_unknown_download_shape(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="download"):
        read_vector({"url": "https://example.com/x.bin"}, tmp_path / "cache")
