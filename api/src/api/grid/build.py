"""Build the static woodland grid for a region.

    uv run python -m api.grid.build --region tuscany

Fetches every source into ``$DATA_DIR/raw/`` (once), computes the cell layers and writes
``$DATA_DIR/grid/<region>/`` (see ``api.grid.store``). Safe to re-run; delete a raw file to
re-download it. National downloads (ISTAT, DEM tiles, CLC pages by bbox) are shared across
regions under ``$DATA_DIR/raw/``.
"""

import argparse
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd

from api.grid import forest, terrain
from api.grid.cells import generate_grid
from api.grid.habitats import Vocabulary, load_vocabulary
from api.grid.infc import load_infc_bosco
from api.grid.places import assign_comuni, nearest_place, read_comuni, read_istat_localities
from api.grid.region import RegionConfig, load_region
from api.grid.soil import TOPSOIL_LAYERS, soil_ph_for_cells
from api.grid.sources import (
    Source,
    copernicus_dem_tiles,
    data_dir,
    fetch,
    load_sources,
    read_region_boundary,
    read_vector,
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


def forest_group_column(groups_config: dict) -> str:
    """Class column on the groups source: ``class_column``, or legacy ``year_column``."""
    if "class_column" in groups_config:
        return str(groups_config["class_column"])
    if "year_column" in groups_config:
        return str(groups_config["year_column"])
    raise KeyError("forest.groups needs class_column (or legacy year_column)")


def forest_classes(
    region: RegionConfig, vocabulary: Vocabulary
) -> tuple[dict[str, str], dict[str, str]]:
    """The region's land-cover code -> group and forest-type code -> habitat mappings, checked.

    When ``forest.groups`` is omitted, groups are derived from CLC IV prefixes (311x → broadleaf,
    …) and types default to ``CLC_IV_DEFAULT_TYPES`` unless ``forest.types.classes`` is set.
    """
    config = region.extra.get("forest") or {}
    types_config = config.get("types") or {}
    if "classes" in types_config:
        types = {str(k): v for k, v in types_config["classes"].items()}
    else:
        types = dict(forest.CLC_IV_DEFAULT_TYPES)

    if "groups" in config:
        groups = {str(k): v for k, v in config["groups"]["classes"].items()}
    else:
        groups = forest.clc_group_classes(types)

    for code, group in groups.items():
        if group not in vocabulary.groups:
            raise ValueError(f"land-cover class {code} maps to unknown group {group!r}")
    for code, habitat in types.items():
        if habitat not in vocabulary.group_of:
            raise ValueError(f"forest-type class {code} maps to unknown habitat {habitat!r}")
    return groups, types


@dataclass
class ForestCover:
    """Land-cover polygons tagged with a broad ``group`` and forest-type polygons with a
    ``habitat``, both in the grid's CRS, and the source ids they came from."""

    groups: gpd.GeoDataFrame
    types: gpd.GeoDataFrame
    sources: list[str]


def read_forest_cover(
    forest_config: dict,
    sources: dict[str, Source],
    raw: Path,
    *,
    region_id: str,
    bbox_wgs84: tuple[float, float, float, float],
    crs: str,
    group_classes: dict[str, str],
    type_classes: dict[str, str],
) -> ForestCover:
    """Read the region's forest sources once each and tag their polygons.

    - ``forest.groups`` set: groups from that land-cover source's ``class_column``, types from the
      ``forest.types`` source's ``field``. When both name the same source (a regional forest-type
      map that also carries the land-use code, e.g. Liguria), it is read once.
    - ``forest.groups`` omitted: groups and types both from the CLC IV code.
    """
    types_source_id = (forest_config.get("types") or {}).get("source", "ispra_clc18_iv")
    types_download = sources[types_source_id].download or {}
    type_field = types_download.get("field", "clc18")

    def tagged(frame: gpd.GeoDataFrame, column: str, name: str, classes: dict) -> gpd.GeoDataFrame:
        frame = frame.assign(**{name: frame[column].astype(str).map(classes)})
        return frame[frame[name].notna()].to_crs(crs)

    if "groups" not in forest_config:
        clc = read_vector(types_download, raw / types_source_id / region_id, bbox_wgs84=bbox_wgs84)
        return ForestCover(
            groups=tagged(clc, type_field, "group", group_classes),
            types=tagged(clc, type_field, "habitat", type_classes),
            sources=[types_source_id],
        )

    groups_config = forest_config["groups"]
    groups_source_id = groups_config["source"]
    class_col = forest_group_column(groups_config)
    one_map = groups_source_id == types_source_id
    listed = ", ".join(f"'{c}'" for c in group_classes)
    cover = read_vector(
        sources[groups_source_id].download or {},
        raw / groups_source_id,
        bbox_wgs84=bbox_wgs84,
        columns=[class_col, type_field] if one_map else [class_col],
        where=f"{class_col} IN ({listed})",
    )
    if one_map:
        type_cover = cover
    else:
        type_cover = read_vector(
            types_download, raw / types_source_id / region_id, bbox_wgs84=bbox_wgs84
        )
    return ForestCover(
        groups=tagged(cover, class_col, "group", group_classes),
        types=tagged(type_cover, type_field, "habitat", type_classes),
        sources=[groups_source_id] if one_map else [groups_source_id, types_source_id],
    )


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
    forest_config = region.extra.get("forest") or {}

    def step(message: str) -> None:
        print(f"[{time.monotonic() - started:6.1f}s] {message}", flush=True)

    step("boundary and grid")
    istat = sources["istat_boundaries"].download or {}
    limits = fetch(istat["url"], raw / "istat" / Path(istat["url"]).name)
    boundary = read_region_boundary(limits, istat["regions"], region.boundary.region_code, crs)
    grid = generate_grid(boundary, region.grid.cell_size_m, crs)

    group_classes, type_classes = forest_classes(region, vocabulary)
    step("forest groups and types")
    cover = read_forest_cover(
        forest_config,
        sources,
        raw,
        region_id=region.id,
        bbox_wgs84=bbox,
        crs=crs,
        group_classes=group_classes,
        type_classes=type_classes,
    )
    groups = forest.class_fractions(cover.groups, "group", grid)
    types = forest.class_fractions(cover.types, "habitat", grid)
    used_sources = cover.sources

    step("woodland mask and habitat composition")
    woodland_groups = tuple(g for g, spec in vocabulary.groups.items() if spec.woodland)
    mask = forest.woodland_mask(grid, groups, woodland_groups=woodland_groups)
    habitats, habitat_summary = forest.habitat_composition(
        grid, groups, types, vocabulary.group_of, fallback=vocabulary.fallback
    )

    forest_ha = forest.forest_area_ha(mask, grid)
    infc_ha = load_infc_bosco().get(region.id)
    if infc_ha is not None:
        delta, ok = forest.compare_infc_bosco(forest_ha, infc_ha)
        status = "ok" if ok else f"WARNING outside ±{forest.INFC_TOLERANCE:.0%}"
        step(
            f"INFC 2015 bosco: grid {forest_ha:,.0f} ha vs inventory {infc_ha:,} ha "
            f"({delta:+.1%}) — {status}"
        )
    else:
        step(f"forest area {forest_ha:,.0f} ha (no INFC row for {region.id})")

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
    used: list[str] = []
    for source_id in (
        "istat_boundaries",
        *used_sources,
        "copernicus_dem_glo30",
        "soilgrids",
        "istat_localities",
    ):
        if source_id not in used:
            used.append(source_id)
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
        "forest_area_ha": round(forest_ha, 1),
        "infc_bosco_ha": infc_ha,
        "sources": {
            s: {"license": sources[s].license, "attribution": sources[s].attribution} for s in used
        },
    }
    paths = write_grid(cells, habitats, out_dir, meta)
    paths["map"] = write_map_geojson(cells, MAP_PROPERTIES, out_dir / "cells_wgs84.geojson")
    step(f"done: {len(cells)} cells, {int(cells['woodland'].sum())} woodland -> {out_dir}")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--region", default="tuscany")
    args = parser.parse_args()
    paths = build(args.region)
    print(json.dumps({k: str(v) for k, v in paths.items()}, indent=2))


if __name__ == "__main__":
    main()
