import pytest
from shapely.geometry import box

from api.grid.cells import cell_id, generate_grid, parse_cell_id

X0, Y0 = 4_000_000, 2_000_000


@pytest.mark.parametrize(
    ("x", "y", "size", "expected"),
    [
        (4_321_000, 2_345_000, 1000, "1kmE4321N2345"),
        (4_320_000, 2_340_000, 10_000, "10kmE432N234"),
        (4_321_100, 2_345_600, 100, "100mE43211N23456"),
    ],
)
def test_cell_id_follows_eea_reference_grid_naming(
    x: int, y: int, size: int, expected: str
) -> None:
    assert cell_id(x, y, size) == expected


def test_cell_id_round_trips_to_the_lower_left_corner() -> None:
    assert parse_cell_id("1kmE4321N2345") == (4_321_000, 2_345_000, 1000)
    assert parse_cell_id("100mE43211N23456") == (4_321_100, 2_345_600, 100)


def test_cell_id_rejects_a_corner_off_the_grid() -> None:
    with pytest.raises(ValueError, match="multiple"):
        cell_id(4_321_500, 2_345_000, 1000)


def test_parse_cell_id_rejects_garbage() -> None:
    with pytest.raises(ValueError):
        parse_cell_id("E4321N2345")


def test_grid_keeps_cells_overlapping_the_boundary_with_their_inside_fraction() -> None:
    # 2.5 km wide, 1.5 km tall, anchored on a grid corner.
    boundary = box(X0, Y0, X0 + 2500, Y0 + 1500)

    grid = generate_grid(boundary, cell_size_m=1000)

    fractions = dict(zip(grid["cell_id"], grid["region_fraction"], strict=True))
    assert fractions == pytest.approx(
        {
            "1kmE4000N2000": 1.0,
            "1kmE4001N2000": 1.0,
            "1kmE4002N2000": 0.5,
            "1kmE4000N2001": 0.5,
            "1kmE4001N2001": 0.5,
            "1kmE4002N2001": 0.25,
        }
    )


def test_grid_cells_are_full_squares_with_their_corner_coordinates() -> None:
    grid = generate_grid(box(X0 + 200, Y0 + 200, X0 + 800, Y0 + 800), cell_size_m=1000)

    assert len(grid) == 1
    row = grid.iloc[0]
    assert (row["x_min"], row["y_min"]) == (X0, Y0)
    assert row.geometry.equals(box(X0, Y0, X0 + 1000, Y0 + 1000))
    assert row["region_fraction"] == pytest.approx(0.36)


def test_grid_skips_cells_that_only_touch_the_boundary_edge() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 1000, Y0 + 1000), cell_size_m=1000)

    assert grid["cell_id"].tolist() == ["1kmE4000N2000"]


def test_grid_ids_are_stable_whatever_the_boundary_extent() -> None:
    small = generate_grid(box(X0 + 1500, Y0 + 1500, X0 + 1600, Y0 + 1600), cell_size_m=1000)
    large = generate_grid(box(X0 - 5000, Y0 - 5000, X0 + 5000, Y0 + 5000), cell_size_m=1000)

    assert set(small["cell_id"]) <= set(large["cell_id"])
    assert small["cell_id"].tolist() == ["1kmE4001N2001"]


def test_grid_is_sorted_by_cell_id_and_unique() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 3000, Y0 + 3000), cell_size_m=1000)

    assert grid["cell_id"].is_unique
    assert grid["cell_id"].tolist() == sorted(grid["cell_id"])
