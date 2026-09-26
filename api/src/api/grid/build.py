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


@dataclass(frozen=True)
class GroupLayer:
    """One land-cover layer of ``forest.groups``: which codes of which column are which group.

    ``where`` (an OGR SQL filter) keeps the layer to some features, e.g. a regional forest map's
    forest land uses, when the class column alone cannot tell them apart.
    """

    source: str
    class_column: str
    classes: dict[str, str]
    where: str | None = None


def forest_group_column(groups_config: dict) -> str:
    """Class column on the groups source: ``class_column``, or legacy ``year_column``."""
    if "class_column" in groups_config:
        return str(groups_config["class_column"])
    if "year_column" in groups_config:
        return str(groups_config["year_column"])
    raise KeyError("forest.groups needs class_column (or legacy year_column)")


def forest_type_column(types_config: dict, download: dict) -> str:
    """Class column on the types source: the region's ``class_column``, else the source's field."""
    return str(types_config.get("class_column") or download.get("field", "clc18"))


def class_filter(class_column: str, codes: list[str], where: str | None = None) -> str:
    """OGR SQL keeping ``codes`` of ``class_column``, inside the layer's own ``where`` if any."""
    listed = ", ".join(f"'{c}'" for c in codes)
    wanted = f"{class_column} IN ({listed})"
    return f"({where}) AND {wanted}" if where else wanted


def forest_group_layers(region: RegionConfig, vocabulary: Vocabulary) -> list[GroupLayer] | None:
    """The region's ``forest.groups`` as layers (one mapping or a list), or None when omitted."""
    config = (region.extra.get("forest") or {}).get("groups")
    if config is None:
        return None
    layers = []
    for layer in config if isinstance(config, list) else [config]:
        classes = {str(k): v for k, v in layer["classes"].items()}
        for code, group in classes.items():
            if group not in vocabulary.groups:
                raise ValueError(f"land-cover class {code} maps to unknown group {group!r}")
        layers.append(
            GroupLayer(
                source=str(layer["source"]),
                class_column=forest_group_column(layer),
                classes=classes,
                where=layer.get("where"),
            )
        )
    return layers


def forest_classes(
    region: RegionConfig, vocabulary: Vocabulary
) -> tuple[dict[str, str], dict[str, str]]:
    """The region's land-cover code -> group and forest-type code -> habitat mappings, checked.

    When ``forest.groups`` is omitted, groups are derived from CLC IV prefixes (311x → broadleaf,
    …) and types default to ``CLC_IV_DEFAULT_TYPES`` unless ``forest.types.classes`` is set. With
    several group layers the group mapping is their union (the build maps each layer on its own).
    """
    config = region.extra.get("forest") or {}
    types_config = config.get("types") or {}
    if "classes" in types_config:
        types = {str(k): v for k, v in types_config["classes"].items()}
    else:
        types = dict(forest.CLC_IV_DEFAULT_TYPES)

    layers = forest_group_layers(region, vocabulary)
    if layers is not None:
        groups = {code: group for layer in layers for code, group in layer.classes.items()}
    else:
        groups = forest.clc_group_classes(types)

    for code, group in groups.items():
        if group not in vocabulary.groups:
            raise ValueError(f"land-cover class {code} maps to unknown group {group!r}")
    for code, habitat in types.items():
        if habitat not in vocabulary.group_of:
            raise ValueError(f"forest-type class {code} maps to unknown habitat {habitat!r}")
    return groups, types


def _needs_bbox(download: dict) -> bool:
    return "arcgis_layer" in download or "wfs" in download


def source_cache_dir(raw: Path, source_id: str, download: dict, region_id: str) -> Path:
    """Where a source's download is cached: per region for bbox queries, shared otherwise."""
    folder = raw / source_id
    return folder / region_id if _needs_bbox(download) else folder


def read_group_cover(
    layers: list[GroupLayer],
    sources: dict[str, Source],
    raw: Path,
    crs: str,
    *,
    bbox_wgs84: tuple[float, float, float, float] | None = None,
) -> gpd.GeoDataFrame:
    """Every layer's features mapped to their group (``group``, ``geometry``) in ``crs``.

    ``bbox_wgs84`` goes to the layers whose source is queried by bbox (WFS, ArcGIS).
    """
    frames = []
    for layer in layers:
        download = sources[layer.source].download or {}
        cover = read_vector(
            download,
            raw / layer.source,
            bbox_wgs84=bbox_wgs84 if _needs_bbox(download) else None,
            # OGR skips unread columns in a filter, so read them all when the layer filters.
            columns=None if layer.where else [layer.class_column],
            where=class_filter(layer.class_column, list(layer.classes), layer.where),
        )
        cover["group"] = cover[layer.class_column].astype(str).map(layer.classes)
        frames.append(cover.loc[cover["group"].notna(), ["group", "geometry"]].to_crs(crs))
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=crs)


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

    - ``forest.groups`` omitted: groups and types both from the CLC IV code.
    - ``forest.groups`` a single layer on the ``forest.types`` source, with no filters: one
      regional forest-type map that also carries the land-use code (e.g. Liguria), read once.
    - otherwise: groups from each ``forest.groups`` layer (``read_group_cover``), types from the
      ``forest.types`` source's class column, filtered by its ``where`` if set.
    """
    types_config = forest_config.get("types") or {}
    types_source_id = types_config.get("source", "ispra_clc18_iv")
    types_download = sources[types_source_id].download or {}
    type_field = forest_type_column(types_config, types_download)
    types_cache = source_cache_dir(raw, types_source_id, types_download, region_id)

    def tagged(frame: gpd.GeoDataFrame, column: str, name: str, classes: dict) -> gpd.GeoDataFrame:
        frame = frame.assign(**{name: frame[column].astype(str).map(classes)})
        return frame[frame[name].notna()].to_crs(crs)

    groups_config = forest_config.get("groups")
    if groups_config is None:
        clc = read_vector(types_download, types_cache, bbox_wgs84=bbox_wgs84)
        return ForestCover(
            groups=tagged(clc, type_field, "group", group_classes),
            types=tagged(clc, type_field, "habitat", type_classes),
            sources=[types_source_id],
        )

    layers = groups_config if isinstance(groups_config, list) else [groups_config]
    one_map = (
        len(layers) == 1
        and layers[0]["source"] == types_source_id
        and not layers[0].get("where")
        and not types_config.get("where")
    )
    if one_map:
        class_col = forest_group_column(layers[0])
        cover = read_vector(
            types_download,
            raw / types_source_id,
            bbox_wgs84=bbox_wgs84,
            columns=[class_col, type_field],
            where=class_filter(class_col, list(group_classes)),
        )
        return ForestCover(
            groups=tagged(cover, class_col, "group", group_classes),
            types=tagged(cover, type_field, "habitat", type_classes),
            sources=[types_source_id],
        )

    group_layers = [
        GroupLayer(
            source=str(layer["source"]),
            class_column=forest_group_column(layer),
            classes={str(k): v for k, v in layer["classes"].items()},
            where=layer.get("where"),
        )
        for layer in layers
    ]
    types = read_vector(
        types_download, types_cache, bbox_wgs84=bbox_wgs84, where=types_config.get("where")
    )
    return ForestCover(
        groups=read_group_cover(group_layers, sources, raw, crs, bbox_wgs84=bbox_wgs84),
        types=tagged(types, type_field, "habitat", type_classes),
        sources=[*dict.fromkeys(layer.source for layer in group_layers), types_source_id],
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
