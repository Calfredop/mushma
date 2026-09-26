"""Simplified ISTAT region boundaries for the web app's hub map.

    uv run python -m api.grid.web_boundaries

Reads the ISTAT generalised regions (``istat_boundaries`` in ``config/sources.yaml``, fetched once
into ``$DATA_DIR/raw/istat/``) and writes ``web/src/regions/boundaries.json``: one feature per
region in WGS84 ``[lon, lat]``, keyed by the web registry's slug (``toscana``,
``emilia-romagna``). The regions are simplified as one coverage, so neighbours keep a single shared
border with no slivers between them, and islets are dropped. Re-run it when ISTAT publishes new
boundaries; the output is small enough to commit with the web app.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

import geopandas as gpd
import numpy as np
import shapely
from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import polylabel

from api.grid.sources import API_ROOT, data_dir, fetch, load_sources

WEB_BOUNDARIES = API_ROOT.parent / "web" / "src" / "regions" / "boundaries.json"

# An equal-area CRS in metres (the grid's), for areas and the simplification tolerance.
METRIC_CRS = "EPSG:3035"
# ~500 m of detail: under a pixel at the hub's national zooms, and a few KB per region.
TOLERANCE_M = 500.0
# Islets smaller than this are dropped; Tuscany's smallest kept island, Gorgona, is 2.2 km².
MIN_PART_KM2 = 1.0
# 4 decimals of a degree: about 10 m.
DECIMALS = 4


def region_slug(name: str) -> str:
    """The web path segment for an ISTAT region name: its Italian part, ASCII, hyphenated."""
    italian = name.split("/")[0]
    ascii_name = unicodedata.normalize("NFKD", italian).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def _parts(geometry: shapely.Geometry) -> list[Polygon]:
    return list(getattr(geometry, "geoms", [geometry]))


def _without_islets(geometry: shapely.Geometry, min_area_m2: float) -> MultiPolygon:
    parts = _parts(geometry)
    kept = [part for part in parts if part.area >= min_area_m2]
    # A region is never only islets, but keep its largest part if it were.
    return MultiPolygon(kept or [max(parts, key=lambda part: part.area)])


def _rounded(geometry: shapely.Geometry, decimals: int) -> shapely.Geometry:
    """Snapped to the grid (valid, shared vertices stay shared), then printed short."""
    snapped = shapely.set_precision(geometry, 10**-decimals)
    return shapely.transform(snapped, lambda coords: np.round(coords, decimals))


def _single_if_one(geometry: shapely.Geometry) -> shapely.Geometry:
    parts = _parts(geometry)
    return parts[0] if len(parts) == 1 else geometry


def web_boundaries(
    regions: gpd.GeoDataFrame,
    tolerance_m: float = TOLERANCE_M,
    min_part_km2: float = MIN_PART_KM2,
    decimals: int = DECIMALS,
) -> dict:
    """ISTAT regions (``COD_REG``, ``DEN_REG``) as a compact GeoJSON FeatureCollection."""
    ordered = regions.sort_values("COD_REG").to_crs(METRIC_CRS)
    kept = [_without_islets(g, min_part_km2 * 1e6) for g in ordered.geometry]
    simplified = gpd.GeoSeries(
        shapely.coverage_simplify(kept, tolerance_m), crs=METRIC_CRS, index=ordered.index
    )
    labels = gpd.GeoSeries(
        [polylabel(max(_parts(g), key=lambda part: part.area), 100.0) for g in simplified],
        crs=METRIC_CRS,
        index=ordered.index,
    ).to_crs("EPSG:4326")
    geometries = simplified.to_crs("EPSG:4326")

    features = []
    for index, row in ordered.iterrows():
        label = labels[index]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "slug": region_slug(str(row["DEN_REG"])),
                    "code": int(row["COD_REG"]),
                    "name": str(row["DEN_REG"]).split("/")[0],
                    "label": [round(label.x, decimals), round(label.y, decimals)],
                },
                "geometry": mapping(_single_if_one(_rounded(geometries[index], decimals))),
            }
        )
    return {"type": "FeatureCollection", "features": features}


def write_web_boundaries(archive: Path, member: str, out: Path) -> Path:
    """Read the regions layer of the ISTAT archive and write the web's boundaries file."""
    regions = gpd.read_file(f"zip://{archive}!{member}", encoding="utf-8")
    collection = {
        **web_boundaries(regions),
        "attribution": load_sources()["istat_boundaries"].attribution,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(collection, ensure_ascii=False, separators=(",", ":")) + "\n")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=WEB_BOUNDARIES)
    args = parser.parse_args()

    istat = load_sources()["istat_boundaries"].download or {}
    archive = fetch(istat["url"], data_dir() / "raw" / "istat" / Path(istat["url"]).name)
    out = write_web_boundaries(archive, istat["regions"], args.out)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
