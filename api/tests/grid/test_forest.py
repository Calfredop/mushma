import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import box

from api.grid.cells import generate_grid
from api.grid.forest import class_fractions, habitat_composition, woodland_mask

X0, Y0 = 4_400_000, 2_300_000


def _polygons(*rows: tuple[str, object]) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"habitat": [r[0] for r in rows]}, geometry=[r[1] for r in rows], crs="EPSG:3035"
    )


def _as_dict(fractions: pd.DataFrame) -> dict[tuple[str, str], float]:
    return {(row.cell_id, row.habitat): row.fraction for row in fractions.itertuples(index=False)}


def test_class_fractions_measure_each_class_share_of_the_cell() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 1000, Y0 + 1000), cell_size_m=1000)
    polygons = _polygons(
        ("beech", box(X0, Y0, X0 + 500, Y0 + 1000)),
        ("chestnut", box(X0 + 500, Y0, X0 + 1000, Y0 + 400)),
    )

    fractions = class_fractions(polygons, "habitat", grid, pixel_m=20.0)

    assert _as_dict(fractions) == pytest.approx(
        {("1kmE4400N2300", "beech"): 0.5, ("1kmE4400N2300", "chestnut"): 0.2}
    )


def test_class_fractions_split_a_polygon_across_cells() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 2000, Y0 + 1000), cell_size_m=1000)
    polygons = _polygons(("fir_spruce", box(X0 + 600, Y0, X0 + 1200, Y0 + 1000)))

    fractions = class_fractions(polygons, "habitat", grid, pixel_m=20.0)

    assert _as_dict(fractions) == pytest.approx(
        {("1kmE4400N2300", "fir_spruce"): 0.4, ("1kmE4401N2300", "fir_spruce"): 0.2}
    )


def test_class_fractions_skip_cells_without_any_class() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 3000, Y0 + 1000), cell_size_m=1000)
    polygons = _polygons(("beech", box(X0, Y0, X0 + 1000, Y0 + 1000)))

    fractions = class_fractions(polygons, "habitat", grid, pixel_m=20.0)

    assert fractions["cell_id"].tolist() == ["1kmE4400N2300"]


def test_class_fractions_ignore_cells_not_in_the_grid() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 1000, Y0 + 1000), cell_size_m=1000)
    polygons = _polygons(("beech", box(X0 - 1000, Y0, X0 + 1000, Y0 + 1000)))

    fractions = class_fractions(polygons, "habitat", grid, pixel_m=20.0)

    assert fractions["cell_id"].tolist() == ["1kmE4400N2300"]


def test_class_fractions_do_not_depend_on_chunking() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 5000, Y0 + 4000), cell_size_m=1000)
    polygons = _polygons(
        ("beech", box(X0 + 300, Y0 + 700, X0 + 4100, Y0 + 3300)),
        ("macchia", box(X0 + 2000, Y0, X0 + 5000, Y0 + 900)),
    )

    whole = class_fractions(polygons, "habitat", grid, pixel_m=20.0, chunk_cells=50)
    chunked = class_fractions(polygons, "habitat", grid, pixel_m=20.0, chunk_cells=2)

    assert _as_dict(chunked) == pytest.approx(_as_dict(whole))
    assert sum(whole.loc[whole["habitat"] == "beech", "fraction"]) == pytest.approx(3.8 * 2.6)


# --- woodland mask -------------------------------------------------------------------------------

GROUP_OF = {
    "beech": "broadleaf",
    "chestnut": "broadleaf",
    "deciduous_oak": "broadleaf",
    "mixed_broadleaf": "broadleaf",
    "fir_spruce": "conifer",
    "other_conifer": "conifer",
    "mixed_broadleaf_conifer": "mixed",
    "macchia": "macchia",
    "transitional_woodland_shrub": "transitional",
}


def _grid(n_cells: int = 1, region_fraction: float = 1.0) -> pd.DataFrame:
    grid = generate_grid(box(X0, Y0, X0 + n_cells * 1000, Y0 + 1000), cell_size_m=1000)
    grid["region_fraction"] = region_fraction
    return grid


def _groups(*rows: tuple[str, str, float]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["cell_id", "group", "fraction"])


def _mask_row(mask: pd.DataFrame, cell: str = "1kmE4400N2300") -> pd.Series:
    return mask.set_index("cell_id").loc[cell]


def test_forest_fraction_is_relative_to_the_cell_area_inside_the_region() -> None:
    mask = woodland_mask(_grid(region_fraction=0.5), _groups(("1kmE4400N2300", "broadleaf", 0.3)))

    row = _mask_row(mask)
    assert row["forest_fraction"] == pytest.approx(0.6)
    assert row["woodland"]


@pytest.mark.parametrize(("forest", "expected"), [(0.49, False), (0.5, True)])
def test_mostly_woodland_means_at_least_half_forest(forest: float, expected: bool) -> None:
    mask = woodland_mask(_grid(), _groups(("1kmE4400N2300", "conifer", forest)))

    assert bool(_mask_row(mask)["woodland"]) is expected


def test_macchia_and_regrowth_do_not_count_as_forest() -> None:
    mask = woodland_mask(
        _grid(),
        _groups(
            ("1kmE4400N2300", "broadleaf", 0.3),
            ("1kmE4400N2300", "macchia", 0.3),
            ("1kmE4400N2300", "transitional", 0.1),
        ),
    )

    row = _mask_row(mask)
    assert row["forest_fraction"] == pytest.approx(0.3)
    assert row["wooded_fraction"] == pytest.approx(0.7)
    assert not row["woodland"]


def test_a_sliver_of_forest_on_the_border_is_not_a_woodland_cell() -> None:
    mask = woodland_mask(_grid(region_fraction=0.2), _groups(("1kmE4400N2300", "mixed", 0.2)))

    row = _mask_row(mask)
    assert row["forest_fraction"] == pytest.approx(1.0)
    assert not row["woodland"]  # only 20 ha of forest


def test_forest_fraction_is_capped_where_boundaries_disagree() -> None:
    mask = woodland_mask(_grid(region_fraction=0.3), _groups(("1kmE4400N2300", "broadleaf", 0.36)))

    assert _mask_row(mask)["forest_fraction"] == 1.0


def test_every_grid_cell_gets_a_mask_row() -> None:
    mask = woodland_mask(_grid(n_cells=2), _groups(("1kmE4400N2300", "broadleaf", 0.9)))

    row = _mask_row(mask, "1kmE4401N2300")
    assert (row["forest_fraction"], row["wooded_fraction"], row["woodland"]) == (0.0, 0.0, False)


# --- habitat composition -------------------------------------------------------------------------


def _types(*rows: tuple[str, str, float]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["cell_id", "habitat", "fraction"])


def _composition(habitats: pd.DataFrame, cell: str = "1kmE4400N2300") -> dict[str, float]:
    rows = habitats[habitats["cell_id"] == cell]
    return dict(zip(rows["habitat"], rows["fraction"], strict=True))


def test_broad_groups_are_split_by_the_forest_types_found_in_the_cell() -> None:
    habitats, _ = habitat_composition(
        _grid(),
        _groups(("1kmE4400N2300", "broadleaf", 0.6), ("1kmE4400N2300", "conifer", 0.2)),
        _types(
            ("1kmE4400N2300", "chestnut", 0.3),
            ("1kmE4400N2300", "beech", 0.1),
            ("1kmE4400N2300", "fir_spruce", 0.4),
        ),
        GROUP_OF,
    )

    assert _composition(habitats) == pytest.approx(
        {"chestnut": 0.5625, "beech": 0.1875, "fir_spruce": 0.25}
    )


def test_single_habitat_groups_map_directly() -> None:
    habitats, _ = habitat_composition(
        _grid(),
        _groups(("1kmE4400N2300", "mixed", 0.2), ("1kmE4400N2300", "macchia", 0.2)),
        _types(("1kmE4400N2300", "beech", 0.4)),
        GROUP_OF,
    )

    assert _composition(habitats) == pytest.approx({"mixed_broadleaf_conifer": 0.5, "macchia": 0.5})


def test_types_are_borrowed_from_neighbouring_cells_when_the_cell_has_none() -> None:
    habitats, summary = habitat_composition(
        _grid(n_cells=2),
        _groups(("1kmE4400N2300", "broadleaf", 0.8), ("1kmE4401N2300", "broadleaf", 0.1)),
        _types(("1kmE4401N2300", "deciduous_oak", 0.9)),
        GROUP_OF,
    )

    assert _composition(habitats) == {"deciduous_oak": 1.0}
    assert summary.set_index("cell_id").loc["1kmE4400N2300", "borrowed_type_fraction"] == 1.0
    assert summary.set_index("cell_id").loc["1kmE4401N2300", "borrowed_type_fraction"] == 0.0


def test_groups_fall_back_to_their_generic_habitat_when_no_type_is_in_reach() -> None:
    habitats, summary = habitat_composition(
        _grid(),
        _groups(("1kmE4400N2300", "broadleaf", 0.5), ("1kmE4400N2300", "conifer", 0.5)),
        _types(),
        GROUP_OF,
        fallback={"broadleaf": "mixed_broadleaf", "conifer": "other_conifer"},
    )

    assert _composition(habitats) == {"mixed_broadleaf": 0.5, "other_conifer": 0.5}
    assert summary.iloc[0]["borrowed_type_fraction"] == 1.0


def test_summary_names_the_dominant_habitat_with_ties_in_vocabulary_order() -> None:
    _, summary = habitat_composition(
        _grid(),
        _groups(("1kmE4400N2300", "broadleaf", 0.6)),
        _types(("1kmE4400N2300", "chestnut", 0.2), ("1kmE4400N2300", "beech", 0.2)),
        GROUP_OF,
    )

    row = summary.iloc[0]
    assert (row["dominant_habitat"], row["dominant_fraction"]) == ("beech", 0.5)


def test_cells_without_woodland_have_no_habitats() -> None:
    habitats, summary = habitat_composition(
        _grid(n_cells=2), _groups(("1kmE4400N2300", "conifer", 0.4)), _types(), GROUP_OF
    )

    assert set(habitats["cell_id"]) == {"1kmE4400N2300"}
    assert summary["cell_id"].tolist() == ["1kmE4400N2300"]


def test_habitat_fractions_sum_to_one_per_cell() -> None:
    habitats, _ = habitat_composition(
        _grid(n_cells=2),
        _groups(
            ("1kmE4400N2300", "broadleaf", 0.37),
            ("1kmE4400N2300", "transitional", 0.11),
            ("1kmE4401N2300", "conifer", 0.52),
            ("1kmE4401N2300", "mixed", 0.03),
        ),
        _types(
            ("1kmE4400N2300", "chestnut", 0.13),
            ("1kmE4400N2300", "deciduous_oak", 0.29),
            ("1kmE4401N2300", "fir_spruce", 0.05),
            ("1kmE4401N2300", "other_conifer", 0.61),
        ),
        GROUP_OF,
    )

    assert habitats.groupby("cell_id")["fraction"].sum().tolist() == pytest.approx([1.0, 1.0])


def test_empty_neighbourhoods_stay_empty_on_a_large_grid() -> None:
    # Window sums over a big grid must not leave float residue that looks like a forest type.
    rng = np.random.default_rng(1)
    grid = generate_grid(box(X0, Y0, X0 + 30_000, Y0 + 30_000), cell_size_m=1000)
    far_corner = (grid["x_min"] >= X0 + 16_000) & (grid["y_min"] >= Y0 + 16_000)
    types = pd.DataFrame(
        [
            (cell, habitat, round(rng.random(), 4))
            for cell in grid.loc[~far_corner, "cell_id"]
            for habitat in ("beech", "chestnut", "deciduous_oak")
        ],
        columns=["cell_id", "habitat", "fraction"],
    )

    habitats, _ = habitat_composition(
        grid, _groups(("1kmE4422N2322", "broadleaf", 0.9)), types, GROUP_OF
    )

    assert _composition(habitats, "1kmE4422N2322") == {"mixed_broadleaf": 1.0}
