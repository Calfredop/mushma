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


def read_vector(
    download: dict,
    cache_dir: Path,
    *,
    bbox_wgs84: tuple[float, float, float, float] | None = None,
    columns: list[str] | None = None,
    where: str | None = None,
) -> gpd.GeoDataFrame:
    """Load a vector layer from a ``sources.yaml`` download block into a GeoDataFrame.

    Supported shapes:
    - ``shapefile`` (+ ``url`` zip): shapefile inside a zip (nested ``.7z`` unpacked once)
    - ``geopackage`` / ``.gpkg`` url (+ optional ``layer``): GeoPackage file
    - ``member`` + ``layer`` (+ ``url`` zip): named layer inside a file member of a zip
    - ``arcgis_layer`` (+ ``field``, needs ``bbox_wgs84``): ArcGIS REST FeatureServer/MapServer
    - ``wfs`` (+ ``type_name``, needs ``bbox_wgs84``): OGC WFS GetFeature; with ``page_size``
      (+ ``sort_by``) it pages a server that caps the feature count
    - ``parts``: a list of the url shapes above (e.g. one zip per province), read and concatenated

    A url shape may set ``file``, the name the download is saved under, when the url's last
    segment does not name it (e.g. ``.../@@download/file``).
    """
    import pandas as pd
    import pyogrio

    cache_dir.mkdir(parents=True, exist_ok=True)

    if "parts" in download:
        frames = [
            read_vector(part, cache_dir, bbox_wgs84=bbox_wgs84, columns=columns, where=where)
            for part in download["parts"]
        ]
        crs = frames[0].crs if frames else None
        return gpd.GeoDataFrame(
            pd.concat([frame.to_crs(crs) for frame in frames], ignore_index=True), crs=crs
        )

    if "arcgis_layer" in download:
        if bbox_wgs84 is None:
            raise ValueError("arcgis_layer downloads need bbox_wgs84")
        pages = fetch_arcgis_features(
            download["arcgis_layer"],
            bbox_wgs84,
            cache_dir,
            out_fields=download.get("field", "*"),
        )
        frame = pd.concat([gpd.read_file(p) for p in pages], ignore_index=True)
        if len(pages):
            # Pages are written in the requested outSR (EPSG:3035 by default).
            frame = frame.set_crs(3035, allow_override=True)
        return frame

    if "wfs" in download:
        if bbox_wgs84 is None:
            raise ValueError("wfs downloads need bbox_wgs84")
        return _read_wfs(download, cache_dir, bbox_wgs84)

    if "url" not in download:
        raise ValueError(
            f"unsupported download shape (need url, parts, arcgis_layer or wfs): {download}"
        )

    if not (
        download.get("geopackage")
        or download.get("shapefile")
        or ("member" in download and "layer" in download)
        or Path(urllib.parse.urlparse(download["url"]).path).suffix.lower() == ".gpkg"
    ):
        raise ValueError(
            "unsupported download shape: need shapefile, geopackage, member+layer, "
            f"arcgis_layer or wfs, got {sorted(download)}"
        )

    url = download["url"]
    name = download.get("file") or Path(urllib.parse.urlparse(url).path).name
    local = fetch(url, cache_dir / name)

    if download.get("geopackage") or local.suffix.lower() == ".gpkg":
        kwargs: dict = {}
        if download.get("layer"):
            kwargs["layer"] = download["layer"]
        if columns:
            kwargs["columns"] = columns
        if where:
            kwargs["where"] = where
        return pyogrio.read_dataframe(local, **kwargs)

    if "member" in download and "layer" in download:
        return pyogrio.read_dataframe(
            f"zip://{local}!{download['member']}",
            layer=download["layer"],
            columns=columns,
            where=where,
        )

    return _read_zip_shapefile(local, cache_dir, download["shapefile"], columns, where)


def _read_wfs(
    download: dict, cache_dir: Path, bbox_wgs84: tuple[float, float, float, float]
) -> gpd.GeoDataFrame:
    lon_min, lat_min, lon_max, lat_max = bbox_wgs84
    params = {
        "SERVICE": "WFS",
        "REQUEST": "GetFeature",
        "VERSION": download.get("version", "2.0.0"),
        "TYPENAME": download["type_name"],
        "OUTPUTFORMAT": download.get("output_format", "application/json"),
        "SRSNAME": download.get("srs", "EPSG:4326"),
        "BBOX": f"{lon_min},{lat_min},{lon_max},{lat_max},EPSG:4326",
    }
    base = download["wfs"].rstrip("?")
    sep = "&" if "?" in base else "?"
    # Bbox is part of the cache key so overlapping regions do not share a stale clip.
    stem = f"wfs_{lon_min}_{lat_min}_{lon_max}_{lat_max}".replace(".", "p")
    page_size = download.get("page_size")
    if not page_size:
        dest = cache_dir / f"{stem}.json"
        fetch(f"{base}{sep}{urllib.parse.urlencode(params)}", dest)
        return gpd.read_file(dest)

    import pandas as pd

    # Servers cap GetFeature (GeoServer's maxFeatures); page with WFS 2.0 COUNT/STARTINDEX,
    # sorted on a stable key so pages neither overlap nor skip, until a short page.
    if download.get("sort_by"):
        params["SORTBY"] = download["sort_by"]
    frames = []
    start = 0
    while True:
        page = {**params, "COUNT": str(page_size), "STARTINDEX": str(start)}
        dest = cache_dir / f"{stem}_page{start // page_size:04d}.json"
        frame = gpd.read_file(fetch(f"{base}{sep}{urllib.parse.urlencode(page)}", dest))
        frames.append(frame)
        if len(frame) < page_size:
            break
        start += page_size
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=frames[0].crs)


def _read_zip_shapefile(
    archive: Path,
    cache_dir: Path,
    shapefile_name: str,
    columns: list[str] | None,
    where: str | None,
) -> gpd.GeoDataFrame:
    import zipfile

    import pyogrio

    # Regione Toscana UCS ships a zip that holds a 7z of the shapefile; unpack once.
    with zipfile.ZipFile(archive) as zf:
        seven = next((n for n in zf.namelist() if n.endswith(".7z")), None)
    if seven is not None:
        unpacked = cache_dir / "unpacked"
        if not (unpacked / ".extracted").exists():
            with zipfile.ZipFile(archive) as zf:
                seven_zip = Path(zf.extract(seven, cache_dir))
            extract_7z(seven_zip, unpacked)
            seven_zip.unlink(missing_ok=True)
        shapefile = next(unpacked.rglob(shapefile_name))
        return pyogrio.read_dataframe(shapefile, columns=columns, where=where)

    # Plain zip of a shapefile (ISTAT-style path or a single .shp with sidecars).
    with zipfile.ZipFile(archive) as zf:
        member = next(
            (
                name
                for name in zf.namelist()
                if name.endswith(shapefile_name) or name.endswith("/" + shapefile_name)
            ),
            None,
        )
    if member is None:
        raise FileNotFoundError(f"{shapefile_name} not found in {archive}")
    return pyogrio.read_dataframe(f"zip://{archive}!{member}", columns=columns, where=where)
