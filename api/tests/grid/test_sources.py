import json
import ssl
import threading
import urllib.error
import urllib.request
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import geopandas as gpd
import pytest
from shapely.geometry import box

from api.grid.sources import (
    copernicus_dem_tiles,
    download_ssl_context,
    extract_7z,
    fetch,
    fetch_arcgis_features,
    load_sources,
    read_region_boundary,
    soilgrids_url,
)


def test_every_source_carries_license_and_attribution() -> None:
    sources = load_sources()

    assert {"istat_boundaries", "copernicus_dem_glo30", "istat_localities"} <= set(sources)
    for source_id, source in sources.items():
        assert source.license, source_id
        assert source.attribution, source_id
        assert source.homepage.startswith("http"), source_id


def test_fetch_downloads_once_then_reuses_the_cached_file(tmp_path: Path) -> None:
    remote = tmp_path / "remote.txt"
    remote.write_text("v1")
    dest = tmp_path / "cache" / "raw" / "remote.txt"

    assert fetch(remote.as_uri(), dest) == dest
    remote.write_text("v2")
    fetch(remote.as_uri(), dest)

    assert dest.read_text() == "v1"
    assert not dest.with_suffix(".txt.part").exists()


def test_fetch_leaves_no_file_behind_when_the_download_fails(tmp_path: Path) -> None:
    dest = tmp_path / "raw" / "missing.zip"

    with pytest.raises(OSError):
        fetch((tmp_path / "does-not-exist.zip").as_uri(), dest)

    assert not dest.exists()
    assert list(dest.parent.glob("*")) == []


def test_download_context_trusts_the_intermediates_some_servers_leave_out() -> None:
    # static.regione.marche.it (the REM vegetation map) sends its leaf certificate alone.
    context = download_ssl_context()
    names = {
        dict(pair[0] for pair in cert["subject"]).get("commonName")
        for cert in context.get_ca_certs()
    }

    assert "GlobalSign RSA OV SSL CA 2018" in names
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname


def test_fetch_verifies_https_with_the_download_context(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: dict[str, object] = {}

    def fake_urlopen(request, timeout, context=None):  # noqa: ANN001, ANN202
        seen["context"] = context
        raise urllib.error.HTTPError(request.full_url, 404, "not found", {}, None)  # type: ignore[arg-type]

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    with pytest.raises(urllib.error.HTTPError):
        fetch("https://example.org/layer.zip", tmp_path / "layer.zip")

    assert isinstance(seen["context"], ssl.SSLContext)
    assert seen["context"].verify_mode == ssl.CERT_REQUIRED


def test_read_region_boundary_dissolves_the_region_and_reprojects(tmp_path: Path) -> None:
    # Two parts of region 9 and one of region 10, in UTM 32N like the ISTAT files.
    regions = gpd.GeoDataFrame(
        {"COD_REG": [9, 9, 10]},
        geometry=[
            box(600_000, 4_800_000, 610_000, 4_810_000),
            box(620_000, 4_800_000, 630_000, 4_810_000),
            box(700_000, 4_800_000, 710_000, 4_810_000),
        ],
        crs="EPSG:32632",
    )
    shp_dir = tmp_path / "Reg"
    shp_dir.mkdir()
    regions.to_file(shp_dir / "Reg.shp")
    archive = tmp_path / "limits.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        for part in shp_dir.iterdir():
            zf.write(part, f"Reg/{part.name}")

    boundary = read_region_boundary(archive, "Reg/Reg.shp", region_code=9, crs="EPSG:3035")

    assert boundary.geom_type == "MultiPolygon"
    assert boundary.area == pytest.approx(200e6, rel=1e-3)  # two 10 km squares, equal-area CRS
    assert 4_000_000 < boundary.bounds[0] < 5_000_000  # LAEA eastings, not UTM


def test_copernicus_dem_tiles_cover_the_bbox() -> None:
    tiles = copernicus_dem_tiles((9.68, 42.23, 12.38, 44.48))

    names = [name for name, _ in tiles]
    assert len(tiles) == 12
    assert "Copernicus_DSM_COG_10_N42_00_E009_00_DEM" in names
    assert "Copernicus_DSM_COG_10_N44_00_E012_00_DEM" in names
    name, url = tiles[0]
    assert url == f"https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"


def test_copernicus_dem_tiles_name_southern_and_western_hemispheres() -> None:
    names = [name for name, _ in copernicus_dem_tiles((-0.5, -0.5, -0.1, -0.1))]

    assert names == ["Copernicus_DSM_COG_10_S01_00_W001_00_DEM"]


def test_soilgrids_url_requests_a_wgs84_subset() -> None:
    url = soilgrids_url("phh2o", "5-15cm", (9.6, 42.15, 12.45, 44.55))

    assert url.startswith("https://maps.isric.org/mapserv?map=/map/phh2o.map&")
    assert "COVERAGEID=phh2o_5-15cm_mean" in url
    assert "SUBSET=long(9.6,12.45)" in url and "SUBSET=lat(42.15,44.55)" in url


def test_extract_7z_unpacks_once(tmp_path: Path) -> None:
    import py7zr

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "UCS.shp").write_text("shape")
    archive = tmp_path / "ucs.7z"
    with py7zr.SevenZipFile(archive, "w") as zf:
        zf.write(tmp_path / "src" / "UCS.shp", "SHP/UCS.shp")

    out = extract_7z(archive, tmp_path / "out")
    (out / "SHP" / "UCS.shp").write_text("kept")
    extract_7z(archive, tmp_path / "out")

    assert (out / "SHP" / "UCS.shp").read_text() == "kept"


class _FakeArcGIS(BaseHTTPRequestHandler):
    features = [
        {"type": "Feature", "properties": {"clc18": str(3111 + i)}, "geometry": None}
        for i in range(5)
    ]

    def do_GET(self) -> None:  # noqa: N802
        query = parse_qs(urlparse(self.path).query)
        offset, count = int(query["resultOffset"][0]), int(query["resultRecordCount"][0])
        page = self.features[offset : offset + count]
        body = {
            "type": "FeatureCollection",
            "features": page,
            "exceededTransferLimit": offset + count < len(self.features),
        }
        payload = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


def test_fetch_arcgis_features_pages_through_the_layer(tmp_path: Path) -> None:
    server = HTTPServer(("127.0.0.1", 0), _FakeArcGIS)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        layer = f"http://127.0.0.1:{server.server_port}/MapServer/4"
        pages = fetch_arcgis_features(
            layer, (9.6, 42.1, 12.5, 44.6), tmp_path / "clc", out_fields="clc18", page_size=2
        )
    finally:
        server.shutdown()

    assert [p.name for p in pages] == [
        "page_0000.geojson",
        "page_0001.geojson",
        "page_0002.geojson",
    ]
    codes = [f["properties"]["clc18"] for p in pages for f in json.loads(p.read_text())["features"]]
    assert codes == ["3111", "3112", "3113", "3114", "3115"]


class _FlakyServer(BaseHTTPRequestHandler):
    failures_left = 2

    def do_GET(self) -> None:  # noqa: N802
        if type(self).failures_left > 0:
            type(self).failures_left -= 1
            self.send_response(503)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"tif")

    def log_message(self, *args: object) -> None:
        pass


def test_fetch_retries_when_the_server_is_temporarily_unavailable(tmp_path: Path) -> None:
    server = HTTPServer(("127.0.0.1", 0), _FlakyServer)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        dest = fetch(
            f"http://127.0.0.1:{server.server_port}/ph.tif",
            tmp_path / "ph.tif",
            retries=3,
            backoff_s=0.01,
        )
    finally:
        server.shutdown()

    assert dest.read_bytes() == b"tif"
