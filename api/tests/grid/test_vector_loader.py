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


class _FakePagedWFS(BaseHTTPRequestHandler):
    """A WFS 2.0 server that caps every response at two features, like GeoServer's maxFeatures."""

    total = 5
    cap = 2
    requests: list[dict[str, list[str]]] = []

    def do_GET(self) -> None:  # noqa: N802
        query = parse_qs(urlparse(self.path).query)
        type(self).requests.append(query)
        start = int(query.get("STARTINDEX", ["0"])[0])
        count = min(int(query.get("COUNT", [str(self.cap)])[0]), self.cap)
        features = [
            {
                "type": "Feature",
                "properties": {"fid": i, "code": f"31{i}"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [11.0 + i, 43.0],
                            [11.1 + i, 43.0],
                            [11.1 + i, 43.1],
                            [11.0 + i, 43.1],
                            [11.0 + i, 43.0],
                        ]
                    ],
                },
            }
            for i in range(start, min(start + count, self.total))
        ]
        body = {"type": "FeatureCollection", "features": features}
        payload = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


def test_read_vector_pages_a_capped_wfs_layer(tmp_path: Path) -> None:
    _FakePagedWFS.requests = []
    server = HTTPServer(("127.0.0.1", 0), _FakePagedWFS)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    download = {
        "wfs": f"http://127.0.0.1:{server.server_port}/wfs",
        "type_name": "forest:types",
        "page_size": 2,
        "sort_by": "fid",
    }
    try:
        frames = read_vector(download, tmp_path / "cache", bbox_wgs84=(10.9, 42.9, 16.2, 43.2))
        # A second read comes from the cached pages, not the server.
        again = read_vector(download, tmp_path / "cache", bbox_wgs84=(10.9, 42.9, 16.2, 43.2))
    finally:
        server.shutdown()

    assert sorted(frames["fid"]) == [0, 1, 2, 3, 4]
    assert len(again) == 5
    assert len(_FakePagedWFS.requests) == 3
    assert [q["STARTINDEX"][0] for q in _FakePagedWFS.requests] == ["0", "2", "4"]
    assert all(q["COUNT"] == ["2"] and q["SORTBY"] == ["fid"] for q in _FakePagedWFS.requests)


def _zip_layer(archive: Path, name: str, layer: gpd.GeoDataFrame) -> Path:
    shp_dir = archive.parent / f"_{name}"
    shp_dir.mkdir(parents=True)
    layer.to_file(shp_dir / f"{name}.shp")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w") as zf:
        for part in shp_dir.iterdir():
            zf.write(part, part.name)
    return archive


def test_read_vector_concatenates_parts_saved_under_their_own_names(tmp_path: Path) -> None:
    # Both provinces are served at a URL ending in ".../@@download/file", so each part names
    # the local file it is saved as.
    north = _zip_layer(
        tmp_path / "srv" / "north" / "file",
        "north",
        _frame(box(X0, Y0, X0 + 100, Y0 + 100), code=["11"]),
    )
    south = _zip_layer(
        tmp_path / "srv" / "south" / "file",
        "south",
        _frame(box(X0 + 200, Y0, X0 + 300, Y0 + 100), code=["210"]),
    )

    frames = read_vector(
        {
            "parts": [
                {"url": north.as_uri(), "file": "north.zip", "shapefile": "north.shp"},
                {"url": south.as_uri(), "file": "south.zip", "shapefile": "south.shp"},
            ]
        },
        tmp_path / "cache",
        where="code IN ('11', '210')",
    )

    assert sorted(frames["code"]) == ["11", "210"]
    assert frames.crs.to_epsg() == 3035
    assert (tmp_path / "cache" / "north.zip").is_file()
    assert (tmp_path / "cache" / "south.zip").is_file()


def test_read_vector_rejects_an_unknown_download_shape(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="download"):
        read_vector({"url": "https://example.com/x.bin"}, tmp_path / "cache")
