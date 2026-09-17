"""Build the static woodland grid for a region.

    uv run python -m api.grid.build --region tuscany

Fetches every source into ``$DATA_DIR/raw/`` (once), computes the cell layers and writes
``$DATA_DIR/grid/<region>/`` (see ``api.grid.store``). Safe to re-run; delete a raw file to
re-download it.
"""

import argparse
import json
import time
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pyogrio

from api.grid import forest, terrain
from api.grid.cells import generate_grid
from api.grid.habitats import Vocabulary, load_vocabulary
from api.grid.places import assign_comuni, nearest_place, read_comuni, read_istat_localities
from api.grid.region import RegionConfig, load_region
from api.grid.soil import TOPSOIL_LAYERS, soil_ph_for_cells
from api.grid.sources import (
    copernicus_dem_tiles,
    data_dir,
    extract_7z,
    fetch,
    fetch_arcgis_features,
    load_sources,
    read_region_boundary,
    soilgrids_url,
)
from api.grid.store import write_grid, write_map_geojson

CELL_COLUMNS = [
    "cell_id",
    "x_min",
    "y_min",
    "region_fraction",
    "woodland",
    "forest_fraction",
    "wooded_fraction",
    "dominant_habitat",
    "dominant_fraction",
    "borrowed_type_fraction",
    "elevation_m",
    "elevation_min_m",
    "elevation_max_m",
    "slope_deg",
    "aspect_deg",
    "northness",
    "soil_ph",
    "comune_code",
    "comune_name",
    "province",
    "place_name",
    "place_distance_km",
    "geometry",
]
MAP_PROPERTIES = ["dominant_habitat", "elevation_m"]
# Places just outside the region can still be the nearest to a border cell.
PLACE_SEARCH_MARGIN_DEG = 0.1


def forest_classes(
    region: RegionConfig, vocabulary: Vocabulary
) -> tuple[dict[str, str], dict[str, str]]:
    """The region's land-cover code -> group and forest-type code -> habitat mappings, checked."""
    config = region.extra["forest"]
    groups = {str(k): v for k, v in config["groups"]["classes"].items()}
    types = {str(k): v for k, v in config["types"]["classes"].items()}
    for code, group in groups.items():
        if group not in vocabulary.groups:
            raise ValueError(f"land-cover class {code} maps to unknown group {group!r}")
    for code, habitat in types.items():
        if habitat not in vocabulary.group_of:
            raise ValueError(f"forest-type class {code} maps to unknown habitat {habitat!r}")
    return groups, types


def assemble_cells(
    grid: gpd.GeoDataFrame,
    mask: pd.DataFrame,
    habitat_summary: pd.DataFrame,
    terrain_stats: pd.DataFrame,
    soil: pd.DataFrame,
    comuni: pd.DataFrame,
    places: pd.DataFrame,
) -> gpd.GeoDataFrame:
    """One row per grid cell with every layer joined on ``cell_id``."""
    cells = grid.drop(columns="geometry")
    for layer in (mask, habitat_summary, terrain_stats, soil, comuni, places):
        cells = cells.merge(layer, on="cell_id", how="left")
    cells["woodland"] = cells["woodland"].fillna(False).astype(bool)
    columns = [c for c in CELL_COLUMNS if c in cells.columns or c == "geometry"]
    cells = gpd.GeoDataFrame(cells, geometry=grid.geometry.to_numpy(), crs=grid.crs)
    return cells[columns]


def build(region_name: str = "tuscany", root: Path | None = None) -> dict[str, Path]:
    started = time.monotonic()
    root = root or data_dir()
    raw = root / "raw"
    region = load_region(region_name)
    vocabulary = load_vocabulary()
    sources = load_sources()
    crs = region.grid.crs
    bbox = region.bbox_wgs84

    def step(message: str) -> None:
        print(f"[{time.monotonic() - started:6.1f}s] {message}", flush=True)

    step("boundary and grid")
    istat = sources["istat_boundaries"].download or {}
    limits = fetch(istat["url"], raw / "istat" / Path(istat["url"]).name)
    boundary = read_region_boundary(limits, istat["regions"], region.boundary.region_code, crs)
    grid = generate_grid(boundary, region.grid.cell_size_m, crs)

    step("forest groups (land cover)")
    group_classes, type_classes = forest_classes(region, vocabulary)
    groups_config = region.extra["forest"]["groups"]
    ucs = _read_rt_ucs(
        sources["rt_ucs"].download or {},
        raw / "rt_ucs",
        groups_config["year_column"],
        codes=list(group_classes),
    )
    ucs["group"] = ucs[groups_config["year_column"]].map(group_classes)
    ucs = ucs[ucs["group"].notna()].to_crs(crs)
    groups = forest.class_fractions(ucs, "group", grid)

    step("forest types (CLC IV level)")
    clc_download = sources["ispra_clc18_iv"].download or {}
    pages = fetch_arcgis_features(
        clc_download["arcgis_layer"],
        bbox,
        raw / "ispra_clc18_iv" / region.id,
        out_fields=clc_download["field"],
    )
    clc = pd.concat([gpd.read_file(p) for p in pages], ignore_index=True).set_crs(
        crs, allow_override=True
    )
    clc["habitat"] = clc[clc_download["field"]].astype(str).map(type_classes)
    types = forest.class_fractions(clc[clc["habitat"].notna()], "habitat", grid)

    step("woodland mask and habitat composition")
    woodland_groups = tuple(g for g, spec in vocabulary.groups.items() if spec.woodland)
    mask = forest.woodland_mask(grid, groups, woodland_groups=woodland_groups)
    habitats, habitat_summary = forest.habitat_composition(
        grid, groups, types, vocabulary.group_of, fallback=vocabulary.fallback
    )

    step("terrain (Copernicus DEM GLO-30)")
    tiles = [
        fetch(url, raw / "copernicus_dem" / f"{name}.tif")
        for name, url in copernicus_dem_tiles(bbox)
    ]
    terrain_stats = terrain.terrain_for_cells(tiles, grid, boundary)

    step("soil pH (SoilGrids)")
    padded = (bbox[0] - 0.05, bbox[1] - 0.05, bbox[2] + 0.05, bbox[3] + 0.05)
    layers = {
        depth: fetch(
            soilgrids_url("phh2o", depth, padded),
            raw / "soilgrids" / region.id / f"phh2o_{depth}_mean.tif",
        )
        for depth in TOPSOIL_LAYERS
    }
    soil = soil_ph_for_cells(layers, grid, boundary)

    step("places (ISTAT comuni and localities)")
    comuni = read_comuni(
        limits, istat["comuni"], istat["provinces"], region.boundary.region_code, crs
    )
    localities = sources["istat_localities"].download or {}
    margin = PLACE_SEARCH_MARGIN_DEG
    places = read_istat_localities(
        fetch(localities["url"], raw / "istat" / Path(localities["url"]).name),
        (bbox[0] - margin, bbox[1] - margin, bbox[2] + margin, bbox[3] + margin),
        crs,
    )
    comune_labels = assign_comuni(grid, comuni)
    place_labels = nearest_place(grid, places)

    step("write")
    cells = assemble_cells(
        grid, mask, habitat_summary, terrain_stats, soil, comune_labels, place_labels
    )
    out_dir = root / "grid" / region.id
    used = [
        "istat_boundaries",
        "rt_ucs",
        "ispra_clc18_iv",
        "copernicus_dem_glo30",
        "soilgrids",
        "istat_localities",
    ]
    meta = {
        "region": region.id,
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "crs": crs,
        "cell_size_m": region.grid.cell_size_m,
        "woodland_rule": {
            "forest_groups": list(woodland_groups),
            "min_forest_fraction": forest.WOODLAND_THRESHOLD,
            "min_forest_km2": forest.MIN_FOREST_KM2,
        },
        "type_search_radii_cells": list(forest.TYPE_SEARCH_RADII),
        "sources": {
            s: {"license": sources[s].license, "attribution": sources[s].attribution} for s in used
        },
    }
    paths = write_grid(cells, habitats, out_dir, meta)
    paths["map"] = write_map_geojson(cells, MAP_PROPERTIES, out_dir / "cells_wgs84.geojson")
    step(f"done: {len(cells)} cells, {int(cells['woodland'].sum())} woodland -> {out_dir}")
    return paths


def _read_rt_ucs(
    download: dict, folder: Path, year_column: str, codes: list[str]
) -> gpd.GeoDataFrame:
    archive = fetch(download["url"], folder / Path(download["url"]).name)
    unpacked = folder / "unpacked"
    if not (unpacked / ".extracted").exists():
        with zipfile.ZipFile(archive) as zf:
            inner = next(n for n in zf.namelist() if n.endswith(".7z"))
            seven_zip = Path(zf.extract(inner, folder))
        extract_7z(seven_zip, unpacked)
        seven_zip.unlink()
    shapefile = next(unpacked.rglob(download["shapefile"]))
    listed = ", ".join(f"'{c}'" for c in codes)
    return pyogrio.read_dataframe(
        shapefile, columns=[year_column], where=f"{year_column} IN ({listed})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--region", default="tuscany")
    args = parser.parse_args()
    paths = build(args.region)
    print(json.dumps({k: str(v) for k, v in paths.items()}, indent=2))


if __name__ == "__main__":
    main()
