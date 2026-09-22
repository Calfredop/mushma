"""External data sources: catalog, cached downloads and readers.

Every source the grid uses is listed in ``config/sources.yaml`` with its license and the
attribution the app must show. Downloads land under ``$DATA_DIR/raw/`` (gitignored) and are
fetched once; delete a file to fetch it again.
"""

import json
import math
import os
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import yaml
from shapely.geometry.base import BaseGeometry

SOURCES_FILE = Path(__file__).resolve().parent.parent / "config" / "sources.yaml"
API_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    homepage: str
    license: str
    attribution: str
    notes: str = ""
    download: dict | None = None


def load_sources() -> dict[str, Source]:
    raw = yaml.safe_load(SOURCES_FILE.read_text())
    return {key: Source(id=key, **value) for key, value in raw.items()}


def data_dir() -> Path:
    """Root for downloads and build outputs: ``$DATA_DIR`` in production, ``api/data`` locally."""
    return Path(os.environ.get("DATA_DIR", API_ROOT / "data"))


def fetch(url: str, dest: Path, retries: int = 4, backoff_s: float = 5.0) -> Path:
    """Download ``url`` to ``dest`` unless it is already there. Writes atomically.

    Server errors (5xx) and network failures are retried with exponential backoff; client errors
    (4xx) fail at once.
    """
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    partial = dest.with_name(dest.name + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "mushma-grid/0.1"})
    for attempt in range(retries + 1):
        try:
            with (
                urllib.request.urlopen(request, timeout=300) as response,
                partial.open("wb") as out,
            ):
                shutil.copyfileobj(response, out, length=1 << 20)
            partial.replace(dest)
            return dest
        except urllib.error.HTTPError as error:
            if error.code < 500 or attempt == retries:
                raise
        except (urllib.error.URLError, TimeoutError):
            if url.startswith("file:") or attempt == retries:
                raise
        finally:
            partial.unlink(missing_ok=True)
        time.sleep(backoff_s * 2**attempt)
    raise AssertionError("unreachable")


def read_region_boundary(archive: Path, member: str, region_code: int, crs: str) -> BaseGeometry:
    """The dissolved boundary of one ISTAT region (``COD_REG``), reprojected to ``crs``."""
    regions = gpd.read_file(f"zip://{archive}!{member}")
    region = regions[regions["COD_REG"] == region_code]
    if region.empty:
        raise ValueError(f"region code {region_code} not found in {archive}!{member}")
    return region.to_crs(crs).union_all()


def extract_7z(archive: Path, dest: Path) -> Path:
    """Unpack a 7-Zip archive into ``dest`` once (the Regione Toscana downloads use 7z)."""
    import py7zr

    marker = dest / ".extracted"
    if marker.exists():
        return dest
    partial = dest.with_name(dest.name + ".part")
    shutil.rmtree(partial, ignore_errors=True)
    with py7zr.SevenZipFile(archive, "r") as zf:
        zf.extractall(partial)
    shutil.rmtree(dest, ignore_errors=True)
    partial.replace(dest)
    marker.touch()
    return dest


def copernicus_dem_tiles(bbox_wgs84: tuple[float, float, float, float]) -> list[tuple[str, str]]:
    """``(name, url)`` of the 1° Copernicus GLO-30 tiles covering a lon/lat bbox (AWS open data)."""
    lon_min, lat_min, lon_max, lat_max = bbox_wgs84
    tiles = []
    for lat in range(math.floor(lat_min), math.ceil(lat_max)):
        for lon in range(math.floor(lon_min), math.ceil(lon_max)):
            ns = f"{'N' if lat >= 0 else 'S'}{abs(lat):02d}"
            ew = f"{'E' if lon >= 0 else 'W'}{abs(lon):03d}"
            name = f"Copernicus_DSM_COG_10_{ns}_00_{ew}_00_DEM"
            tiles.append((name, f"https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"))
    return tiles


def soilgrids_url(prop: str, depth: str, bbox_wgs84: tuple[float, float, float, float]) -> str:
    """WCS request for the mean of a SoilGrids property at one depth over a lon/lat bbox."""
    lon_min, lat_min, lon_max, lat_max = bbox_wgs84
    wgs84 = "http://www.opengis.net/def/crs/EPSG/0/4326"
    return (
        f"https://maps.isric.org/mapserv?map=/map/{prop}.map&SERVICE=WCS&VERSION=2.0.1"
        f"&REQUEST=GetCoverage&COVERAGEID={prop}_{depth}_mean&FORMAT=image/tiff"
        f"&SUBSET=long({lon_min},{lon_max})&SUBSET=lat({lat_min},{lat_max})"
        f"&SUBSETTINGCRS={wgs84}&OUTPUTCRS={wgs84}"
    )


def fetch_arcgis_features(
    layer_url: str,
    bbox_wgs84: tuple[float, float, float, float],
    out_dir: Path,
    out_fields: str,
    out_crs: int = 3035,
    page_size: int = 2000,
) -> list[Path]:
    """Page through an ArcGIS REST layer's features in a bbox, caching each page as GeoJSON."""
    marker = out_dir / ".complete"
    if marker.exists():
        return sorted(out_dir.glob("page_*.geojson"))
    lon_min, lat_min, lon_max, lat_max = bbox_wgs84
    pages = []
    offset = 0
    while True:
        params = urllib.parse.urlencode(
            {
                "where": "1=1",
                "geometry": f"{lon_min},{lat_min},{lon_max},{lat_max}",
                "geometryType": "esriGeometryEnvelope",
                "inSR": 4326,
                "spatialRel": "esriSpatialRelIntersects",
                "outFields": out_fields,
                "returnGeometry": "true",
                "outSR": out_crs,
                "orderByFields": "objectid",
                "resultOffset": offset,
                "resultRecordCount": page_size,
                "f": "geojson",
            }
        )
        page = fetch(f"{layer_url}/query?{params}", out_dir / f"page_{len(pages):04d}.geojson")
        pages.append(page)
        data = json.loads(page.read_text())
        if "error" in data:
            page.unlink()
            raise OSError(f"ArcGIS query failed: {data['error']}")
        features = data.get("features", [])
        if not data.get("exceededTransferLimit", len(features) == page_size):
            break
        offset += page_size
    marker.touch()
    return pages
