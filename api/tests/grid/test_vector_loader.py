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


class _FakeArcGISByLayer(BaseHTTPRequestHandler):
    """Each MapServer layer holds one feature whose code is the layer id."""

    def do_GET(self) -> None:  # noqa: N802
        layer = urlparse(self.path).path.split("/")[-2]
        x0 = 4_400_000 + 1_000 * int(layer)
        body = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"legend": f"layer {layer}"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [x0, 2_300_000],
                                [x0 + 100, 2_300_000],
                                [x0 + 100, 2_300_100],
                                [x0, 2_300_100],
                                [x0, 2_300_000],
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


def test_read_vector_keeps_each_arcgis_part_in_its_own_cache(tmp_path: Path) -> None:
    # Lombardia's forest map is one MapServer sublayer per forest category.
    server = HTTPServer(("127.0.0.1", 0), _FakeArcGISByLayer)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/MapServer"
    download = {
        "parts": [
            {"arcgis_layer": f"{base}/1", "field": "legend"},
            {"arcgis_layer": f"{base}/3", "field": "legend"},
        ]
    }
    try:
        frames = read_vector(download, tmp_path / "cache", bbox_wgs84=(9.6, 42.1, 12.5, 44.6))
        again = read_vector(download, tmp_path / "cache", bbox_wgs84=(9.6, 42.1, 12.5, 44.6))
    finally:
        server.shutdown()

    assert sorted(frames["legend"]) == ["layer 1", "layer 3"]
    assert sorted(again["legend"]) == ["layer 1", "layer 3"]


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


class _FakeFilteredWFS(BaseHTTPRequestHandler):
    """A GeoServer WFS that answers a CQL_FILTER and refuses one sent with a BBOX, as GeoServer
    does ("BBOX and CQL_FILTER are mutually exclusive")."""

    requests: list[dict[str, list[str]]] = []

    def do_GET(self) -> None:  # noqa: N802
        query = parse_qs(urlparse(self.path).query)
        type(self).requests.append(query)
        if "BBOX" in query and "CQL_FILTER" in query:
            self.send_response(400)
            self.end_headers()
            return
        features = [
            {
                "type": "Feature",
                "properties": {"code": code, "flag": flag},
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
            for i, (code, flag) in enumerate([("31142", "-99994"), ("31249", "01")])
        ]
        payload = json.dumps({"type": "FeatureCollection", "features": features}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


def test_read_vector_sends_a_wfs_cql_filter_in_place_of_the_bbox(tmp_path: Path) -> None:
    _FakeFilteredWFS.requests = []
    server = HTTPServer(("127.0.0.1", 0), _FakeFilteredWFS)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    download = {
        "wfs": f"http://127.0.0.1:{server.server_port}/wfs",
        "type_name": "rv:ccs",
        "cql_filter": "clc_lvl_2 = '31'",
    }
    other = {**download, "cql_filter": "clc_lvl_2 = '32'"}
    try:
        frames = read_vector(download, tmp_path / "cache", bbox_wgs84=(10.9, 42.9, 12.2, 43.2))
        read_vector(download, tmp_path / "cache", bbox_wgs84=(10.9, 42.9, 12.2, 43.2))
        read_vector(other, tmp_path / "cache", bbox_wgs84=(10.9, 42.9, 12.2, 43.2))
    finally:
        server.shutdown()

    assert sorted(frames["code"]) == ["31142", "31249"]
    # The filter replaces the bbox, and each filter is cached on its own: the second read of the
    # first filter comes from the cache, the other filter is fetched.
    assert len(_FakeFilteredWFS.requests) == 2
    assert [q["CQL_FILTER"] for q in _FakeFilteredWFS.requests] == [
        ["clc_lvl_2 = '31'"],
        ["clc_lvl_2 = '32'"],
    ]
    assert all("BBOX" not in q for q in _FakeFilteredWFS.requests)


def test_read_vector_applies_where_and_columns_to_a_wfs_layer(tmp_path: Path) -> None:
    server = HTTPServer(("127.0.0.1", 0), _FakeFilteredWFS)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    download = {
        "wfs": f"http://127.0.0.1:{server.server_port}/wfs",
        "type_name": "rv:ccs",
        "cql_filter": "clc_lvl_2 = '31'",
    }
    try:
        frames = read_vector(
            download,
            tmp_path / "cache",
            bbox_wgs84=(10.9, 42.9, 12.2, 43.2),
            columns=["code"],
            where="flag = '-99994'",
        )
    finally:
        server.shutdown()

    assert list(frames["code"]) == ["31142"]
    assert "flag" not in frames.columns


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


def test_read_vector_reads_a_manual_download_saved_in_the_cache(tmp_path: Path) -> None:
    # Valle d'Aosta's forest map is downloaded by hand behind a login: the file is placed in the
    # source's cache under the name the config gives, and read like any zipped shapefile.
    _zip_layer(
        tmp_path / "cache" / "tipi.zip",
        "tipi",
        _frame(box(X0, Y0, X0 + 100, Y0 + 100), ca=["LC"]),
    )

    frames = read_vector(
        {
            "manual": "https://portal.example/repertorio",
            "file": "tipi.zip",
            "shapefile": "tipi.shp",
        },
        tmp_path / "cache",
    )

    assert list(frames["ca"]) == ["LC"]


def test_read_vector_says_where_to_get_a_missing_manual_download(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError) as error:
        read_vector(
            {
                "manual": "https://portal.example/repertorio",
                "file": "tipi.zip",
                "shapefile": "tipi.shp",
            },
            tmp_path / "cache",
        )

    assert "https://portal.example/repertorio" in str(error.value)
    assert str(tmp_path / "cache" / "tipi.zip") in str(error.value)


def test_read_vector_rejects_an_unknown_download_shape(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="download"):
        read_vector({"url": "https://example.com/x.bin"}, tmp_path / "cache")


def _cached_arcgis_pages(cache: Path, *features: dict) -> None:
    """Write ``features`` as an already-complete ArcGIS page cache, as the pager leaves it."""
    cache.mkdir(parents=True)
    page = {"type": "FeatureCollection", "features": list(features)}
    (cache / "page_0000.geojson").write_text(json.dumps(page))
    (cache / ".complete").touch()


def _square(x: float, **properties: str) -> dict:
    ring = [[x, Y0], [x + 100, Y0], [x + 100, Y0 + 100], [x, Y0 + 100], [x, Y0]]
    return {
        "type": "Feature",
        "properties": properties,
        "geometry": {"type": "Polygon", "coordinates": [ring]},
    }


def test_read_vector_filters_an_arcgis_layer_by_where(tmp_path: Path) -> None:
    """Sicily's forest map carries the land class and the forest type on every polygon; a group
    layer keeps one class with an OGR SQL ``where``, which an ArcGIS source must honour too."""
    cache = tmp_path / "cache"
    _cached_arcgis_pages(
        cache,
        _square(X0, DESCRIPTION="31a - boschi", CODCAMPO="CA1"),
        _square(X0 + 200, DESCRIPTION="32x - arbusteti", CODCAMPO="MM2"),
    )

    frame = read_vector(
        {"arcgis_layer": "http://127.0.0.1:9/MapServer/38"},
        cache,
        bbox_wgs84=(11.9, 35.4, 15.7, 38.9),
        where="DESCRIPTION = '31a - boschi' AND CODCAMPO IN ('CA1')",
    )

    assert list(frame["CODCAMPO"]) == ["CA1"]
    assert frame.crs.to_epsg() == 3035
