"""Woodland per cell: how much of each cell is forest, and which kind.

Land-cover polygons are rasterized onto a fine raster aligned with the grid and counted per cell,
so a class's fraction is the share of the cell's area it covers.
"""

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio.features
from rasterio.transform import from_origin
from shapely.geometry import box

from api.grid.cells import cell_id, parse_cell_id


def class_fractions(
    polygons: gpd.GeoDataFrame,
    column: str,
    grid: gpd.GeoDataFrame,
    pixel_m: float = 20.0,
    chunk_cells: int = 50,
) -> pd.DataFrame:
    """Long table ``(cell_id, <column>, fraction)`` of each class's share of each grid cell.

    ``fraction`` is relative to the whole cell (not the part inside the region). Polygons must be
    in the grid's CRS and should not overlap each other. Cells not in ``grid`` are ignored.
    """
    _, _, cell_size_m = parse_cell_id(grid["cell_id"].iloc[0])
    per_cell = round(cell_size_m / pixel_m)
    if per_cell * pixel_m != cell_size_m:
        raise ValueError(f"pixel_m {pixel_m} must divide the cell size {cell_size_m}")

    classes = sorted(polygons[column].dropna().unique())
    codes = {name: i + 1 for i, name in enumerate(classes)}  # 0 = no class
    polygons = polygons[polygons[column].notna()].reset_index(drop=True)
    wanted = set(grid["cell_id"])
    ix = (grid["x_min"] // cell_size_m).to_numpy()
    iy = (grid["y_min"] // cell_size_m).to_numpy()

    frames = []
    for cx in range(ix.min(), ix.max() + 1, chunk_cells):
        for cy in range(iy.min(), iy.max() + 1, chunk_cells):
            if not (
                (ix >= cx) & (ix < cx + chunk_cells) & (iy >= cy) & (iy < cy + chunk_cells)
            ).any():
                continue
            x0, y0 = cx * cell_size_m, cy * cell_size_m
            x1, y1 = x0 + chunk_cells * cell_size_m, y0 + chunk_cells * cell_size_m
            hits = polygons.sindex.query(box(x0, y0, x1, y1), predicate="intersects")
            if len(hits) == 0:
                continue
            side = chunk_cells * per_cell
            raster = rasterio.features.rasterize(
                (
                    (geom, codes[name])
                    for geom, name in zip(
                        polygons.geometry.iloc[hits], polygons[column].iloc[hits], strict=True
                    )
                ),
                out_shape=(side, side),
                transform=from_origin(x0, y1, pixel_m, pixel_m),
                fill=0,
                dtype="uint16",
            )
            frames.append(_count_blocks(raster, per_cell, chunk_cells, x0, y1, cell_size_m))

    if not frames:
        return pd.DataFrame({"cell_id": [], column: [], "fraction": []})
    counts = pd.concat(frames, ignore_index=True)
    counts = counts[counts["cell_id"].isin(wanted)]
    names = np.array([None, *classes], dtype=object)
    return (
        pd.DataFrame(
            {
                "cell_id": counts["cell_id"].to_numpy(),
                column: names[counts["code"].to_numpy()],
                "fraction": counts["fraction"].to_numpy(),
            }
        )
        .sort_values(["cell_id", column])
        .reset_index(drop=True)
    )


def _count_blocks(
    raster: np.ndarray, per_cell: int, n_cells: int, x_left: int, y_top: int, cell_size_m: int
) -> pd.DataFrame:
    """Pixel counts per (cell, class code) for a square chunk of ``n_cells`` x ``n_cells``."""
    n_codes = int(raster.max()) + 1
    blocks = raster.reshape(n_cells, per_cell, n_cells, per_cell).swapaxes(1, 2)
    block_index = np.arange(n_cells * n_cells).reshape(n_cells, n_cells)[:, :, None, None]
    counts = np.bincount(
        (block_index * n_codes + blocks).ravel(), minlength=n_cells * n_cells * n_codes
    ).reshape(n_cells * n_cells, n_codes)
    block, code = np.nonzero(counts[:, 1:])
    code = code + 1
    row, col = np.divmod(block, n_cells)
    ids = [
        cell_id(int(x_left + c * cell_size_m), int(y_top - (r + 1) * cell_size_m), cell_size_m)
        for r, c in zip(row, col, strict=True)
    ]
    return pd.DataFrame(
        {"cell_id": ids, "code": code, "fraction": counts[block, code] / per_cell**2}
    )


WOODLAND_GROUPS = ("broadleaf", "conifer", "mixed")
# A cell is "mostly woodland" when forest covers at least this share of its area inside the region.
WOODLAND_THRESHOLD = 0.5
# ...and at least this much forest in absolute terms, so border slivers don't qualify.
MIN_FOREST_KM2 = 0.25
# Neighbourhood radii (in cells) searched for forest types when a cell has none of a group.
TYPE_SEARCH_RADII = (0, 2, 5)
WINDOW_SUM_TOLERANCE = 1e-9


def woodland_mask(
    grid: pd.DataFrame,
    groups: pd.DataFrame,
    woodland_groups: tuple[str, ...] = WOODLAND_GROUPS,
    threshold: float = WOODLAND_THRESHOLD,
    min_forest_km2: float = MIN_FOREST_KM2,
) -> pd.DataFrame:
    """Forest share and the "mostly woodland" flag for every grid cell.

    ``groups`` is a long table ``(cell_id, group, fraction)`` of broad land-cover groups, with
    fractions of the whole cell. Only ``woodland_groups`` count as forest; every group counts
    towards ``wooded_fraction``.
    """
    _, _, cell_size_m = parse_cell_id(grid["cell_id"].iloc[0])
    per_cell = groups.pivot_table(
        index="cell_id", columns="group", values="fraction", aggfunc="sum"
    )
    per_cell = per_cell.reindex(grid["cell_id"]).fillna(0.0)
    forest = per_cell[[g for g in woodland_groups if g in per_cell]].sum(axis=1).to_numpy()
    wooded = per_cell.sum(axis=1).to_numpy()
    inside = grid["region_fraction"].to_numpy()

    with np.errstate(invalid="ignore", divide="ignore"):
        forest_fraction = np.clip(np.nan_to_num(forest / inside), 0.0, 1.0)
        wooded_fraction = np.clip(np.nan_to_num(wooded / inside), 0.0, 1.0)
    forest_km2 = forest * (cell_size_m / 1000) ** 2
    return pd.DataFrame(
        {
            "cell_id": grid["cell_id"].to_numpy(),
            "forest_fraction": forest_fraction,
            "wooded_fraction": wooded_fraction,
            "woodland": (forest_fraction >= threshold - 1e-9) & (forest_km2 >= min_forest_km2),
        }
    )


def habitat_composition(
    grid: pd.DataFrame,
    groups: pd.DataFrame,
    types: pd.DataFrame,
    group_of: dict[str, str],
    fallback: dict[str, str] | None = None,
    radii: tuple[int, ...] = TYPE_SEARCH_RADII,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Habitat fractions per cell from broad groups (how much) and forest types (which kind).

    Each broad group's share of the cell is split among its habitats in proportion to the forest
    types mapped in the cell. When the cell has no type of that group, the types within ``radii``
    cells around it are used, then the group's ``fallback`` habitat (by default the group's last
    habitat in ``group_of``). Groups with a single habitat map straight to it.

    Returns ``(habitats, summary)``: the long table ``(cell_id, habitat, fraction)`` with fractions
    summing to 1 over the cell's wooded area, and per cell the ``dominant_habitat``, its
    ``dominant_fraction`` and ``borrowed_type_fraction`` (share typed from outside the cell).
    """
    _, _, cell_size_m = parse_cell_id(grid["cell_id"].iloc[0])
    order = list(group_of)
    members: dict[str, list[str]] = {}
    for habitat, group in group_of.items():
        members.setdefault(group, []).append(habitat)
    fallback = {g: hs[-1] for g, hs in members.items()} | (fallback or {})

    ids = grid["cell_id"].to_numpy()
    ix = (grid["x_min"].to_numpy() // cell_size_m).astype(np.int64)
    iy = (grid["y_min"].to_numpy() // cell_size_m).astype(np.int64)
    ix, iy = ix - ix.min(), iy - iy.min()
    shape = (ix.max() + 1, iy.max() + 1)

    group_table = groups[groups["fraction"] > 0].pivot_table(
        index="cell_id", columns="group", values="fraction", aggfunc="sum"
    )
    group_table = group_table.reindex(ids).fillna(0.0)
    type_table = types.pivot_table(
        index="cell_id", columns="habitat", values="fraction", aggfunc="sum"
    )
    type_table = type_table.reindex(index=ids, columns=order).fillna(0.0)

    area = {h: np.zeros(len(ids)) for h in order}
    borrowed = np.zeros(len(ids))
    for group in group_table.columns:
        share_of_cell = group_table[group].to_numpy()
        candidates = members[group]
        if len(candidates) == 1:
            area[candidates[0]] += share_of_cell
            continue
        pending = share_of_cell > 0
        type_grid = np.zeros((*shape, len(candidates)))
        type_grid[ix, iy] = type_table[candidates].to_numpy()
        for radius in radii:
            window = _window_sum(type_grid, radius)[ix, iy]
            total = window.sum(axis=1)
            found = pending & (total > 0)
            for k, habitat in enumerate(candidates):
                area[habitat][found] += share_of_cell[found] * window[found, k] / total[found]
            if radius > 0:
                borrowed[found] += share_of_cell[found]
            pending &= ~found
        area[fallback[group]][pending] += share_of_cell[pending]
        borrowed[pending] += share_of_cell[pending]

    wooded = group_table.sum(axis=1).to_numpy()
    has_wood = wooded > 0
    fractions = pd.DataFrame({h: area[h][has_wood] / wooded[has_wood] for h in order})
    fractions.insert(0, "cell_id", ids[has_wood])
    habitats = fractions.melt(id_vars="cell_id", var_name="habitat", value_name="fraction")
    habitats = habitats[habitats["fraction"] > 0]
    rank = {h: i for i, h in enumerate(order)}
    habitats = habitats.assign(_rank=habitats["habitat"].map(rank))
    habitats = habitats.sort_values(["cell_id", "fraction", "_rank"], ascending=[True, False, True])
    dominant = habitats.drop_duplicates("cell_id")
    summary = pd.DataFrame(
        {
            "cell_id": ids[has_wood],
            "borrowed_type_fraction": borrowed[has_wood] / wooded[has_wood],
        }
    ).merge(
        dominant.rename(columns={"habitat": "dominant_habitat", "fraction": "dominant_fraction"})[
            ["cell_id", "dominant_habitat", "dominant_fraction"]
        ],
        on="cell_id",
    )
    habitats = habitats.drop(columns="_rank").sort_values(["cell_id", "habitat"])
    return habitats.reset_index(drop=True), summary


def _window_sum(values: np.ndarray, radius: int) -> np.ndarray:
    """Sum of ``values[x, y, k]`` over the square window of ``radius`` cells around each cell."""
    if radius == 0:
        return values
    padded = np.pad(values, ((radius + 1, radius), (radius + 1, radius), (0, 0)))
    integral = padded.cumsum(axis=0).cumsum(axis=1)
    size = 2 * radius + 1
    sums = (
        integral[size:, size:]
        - integral[:-size, size:]
        - integral[size:, :-size]
        + integral[:-size, :-size]
    )
    # Differences of large running sums leave float residue where the window is empty. Real
    # fractions are whole pixels (at least 1/2500 of a cell), far above this tolerance.
    sums[sums < WINDOW_SUM_TOLERANCE] = 0.0
    return sums
