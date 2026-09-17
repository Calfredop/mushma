import pandas as pd
import pytest

from api.weather.points import (
    candidate_points,
    footprint_elevation,
    interpolation_weights,
    point_id,
)


def _cells(*centres: tuple[str, float, float]) -> pd.DataFrame:
    return pd.DataFrame(centres, columns=["cell_id", "lat", "lon"])


def _points(*coords: tuple[float, float]) -> pd.DataFrame:
    return pd.DataFrame(
        [(point_id(lat, lon), lat, lon) for lat, lon in coords], columns=["point_id", "lat", "lon"]
    )


def _weights(frame: pd.DataFrame) -> dict[tuple[str, str], float]:
    return {(r.cell_id, r.point_id): r.weight for r in frame.itertuples()}


def test_point_id_names_the_node_by_its_coordinates() -> None:
    assert point_id(43.8, 11.8) == "N43.80E011.80"
    assert point_id(43.800003, 9.699997) == "N43.80E009.70"
    assert point_id(-0.2, -9.6) == "S00.20W009.60"


def test_candidate_points_are_the_lattice_nodes_around_each_cell_centre() -> None:
    cells = _cells(("a", 43.83, 11.77), ("b", 43.87, 11.79))

    points = candidate_points(cells, spacing_deg=0.1)

    assert list(points["point_id"]) == [
        "N43.80E011.70",
        "N43.80E011.80",
        "N43.90E011.70",
        "N43.90E011.80",
    ]
    assert points.loc[0, "lat"] == 43.8 and points.loc[3, "lon"] == 11.8


def test_candidate_points_follow_a_coarser_lattice() -> None:
    points = candidate_points(_cells(("a", 43.83, 11.77)), spacing_deg=0.2)

    assert set(points["point_id"]) == {
        "N43.80E011.60",
        "N43.80E011.80",
        "N44.00E011.60",
        "N44.00E011.80",
    }


def test_bilinear_weights_follow_the_cell_position_inside_the_lattice_square() -> None:
    cells = _cells(("a", 43.825, 11.75))
    points = _points((43.8, 11.7), (43.8, 11.8), (43.9, 11.7), (43.9, 11.8))

    weights = interpolation_weights(cells, points, spacing_deg=0.1, method="bilinear")

    assert _weights(weights) == pytest.approx(
        {
            ("a", "N43.80E011.70"): 0.375,
            ("a", "N43.80E011.80"): 0.375,
            ("a", "N43.90E011.70"): 0.125,
            ("a", "N43.90E011.80"): 0.125,
        }
    )


def test_a_cell_on_a_node_takes_all_its_weight_from_that_node() -> None:
    cells = _cells(("a", 43.8, 11.8))
    points = _points((43.8, 11.7), (43.8, 11.8), (43.9, 11.7), (43.9, 11.8))

    weights = interpolation_weights(cells, points, spacing_deg=0.1, method="bilinear")

    assert _weights(weights) == {("a", "N43.80E011.80"): pytest.approx(1.0)}


def test_bilinear_weights_skip_sea_nodes_and_renormalise() -> None:
    cells = _cells(("a", 43.825, 11.75))
    # (43.9, 11.8) is sea: not in the land point set.
    points = _points((43.8, 11.7), (43.8, 11.8), (43.9, 11.7))

    weights = interpolation_weights(cells, points, spacing_deg=0.1, method="bilinear")

    assert _weights(weights) == pytest.approx(
        {
            ("a", "N43.80E011.70"): 0.375 / 0.875,
            ("a", "N43.80E011.80"): 0.375 / 0.875,
            ("a", "N43.90E011.70"): 0.125 / 0.875,
        }
    )


def test_a_cell_with_only_sea_corners_uses_the_nearest_land_node_within_reach() -> None:
    # An island cell: its four corners are sea; the nearest land node is 0.2° to the east.
    cells = _cells(("island", 42.35, 10.95), ("far", 42.35, 9.25))
    points = _points((42.4, 11.2), (42.3, 11.3))

    weights = interpolation_weights(
        cells, points, spacing_deg=0.1, method="bilinear", max_distance_km=30
    )

    assert _weights(weights) == {("island", "N42.40E011.20"): pytest.approx(1.0)}


def test_nearest_weights_pick_one_node_per_cell() -> None:
    cells = _cells(("a", 43.825, 11.76), ("b", 43.89, 11.71))
    points = _points((43.8, 11.7), (43.8, 11.8), (43.9, 11.7), (43.9, 11.8))

    weights = interpolation_weights(cells, points, spacing_deg=0.1, method="nearest")

    assert _weights(weights) == {
        ("a", "N43.80E011.80"): pytest.approx(1.0),
        ("b", "N43.90E011.70"): pytest.approx(1.0),
    }


def test_nearest_weights_leave_out_cells_beyond_reach() -> None:
    cells = _cells(("near", 43.81, 11.79), ("far", 42.0, 9.0))
    points = _points((43.8, 11.8))

    weights = interpolation_weights(
        cells, points, spacing_deg=0.1, method="nearest", max_distance_km=30
    )

    assert list(weights["cell_id"]) == ["near"]


def test_unknown_interpolation_method_is_rejected() -> None:
    with pytest.raises(ValueError, match="kriging"):
        interpolation_weights(_cells(("a", 43.8, 11.8)), _points((43.8, 11.8)), 0.1, "kriging")


def test_footprint_elevation_averages_the_grid_cells_closest_to_each_node() -> None:
    cells = pd.DataFrame(
        {
            "cell_id": ["a", "b", "c", "d"],
            "lat": [43.79, 43.81, 43.84, 43.88],
            "lon": [11.79, 11.82, 11.77, 11.8],
            "elevation_m": [800.0, 900.0, 1000.0, None],
        }
    )
    points = _points((43.8, 11.8), (43.9, 11.8), (44.0, 11.8))

    elevation = footprint_elevation(cells, points, spacing_deg=0.1)

    assert list(elevation.index) == ["N43.80E011.80", "N43.90E011.80", "N44.00E011.80"]
    assert elevation["N43.80E011.80"] == pytest.approx(900.0)
    assert elevation[["N43.90E011.80", "N44.00E011.80"]].isna().all()
