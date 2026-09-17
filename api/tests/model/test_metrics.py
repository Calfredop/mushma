import numpy as np
import pytest

from api.model.metrics import (
    bootstrap_interval,
    cells_within,
    lift,
    presence_auc,
)


def test_presence_auc_is_the_share_of_background_scoring_below_with_ties_counting_half() -> None:
    background = np.array([0.1, 0.2, 0.5, 0.5, 0.9])

    assert presence_auc(0.5, background) == pytest.approx((2 + 0.5 * 2) / 5)
    assert presence_auc(1.0, background) == 1.0
    assert presence_auc(0.0, background) == 0.0


def test_presence_auc_weights_the_background() -> None:
    background = np.array([0.1, 0.9])

    assert presence_auc(0.5, background, weights=np.array([3.0, 1.0])) == pytest.approx(0.75)


def test_presence_auc_ignores_missing_background_and_is_missing_without_any() -> None:
    assert presence_auc(0.5, np.array([np.nan, 0.1])) == 1.0
    assert np.isnan(presence_auc(0.5, np.array([np.nan])))
    assert np.isnan(presence_auc(np.nan, np.array([0.1])))


def test_a_constant_score_is_no_better_than_chance() -> None:
    assert presence_auc(0.3, np.full(10, 0.3)) == 0.5


def test_lift_is_the_share_of_presences_in_the_top_fraction_over_that_fraction() -> None:
    percentiles = np.array([0.95, 0.91, 0.5, 0.2, np.nan])

    assert lift(percentiles, top=0.1) == pytest.approx((2 / 4) / 0.1)
    assert lift(percentiles, top=0.5) == pytest.approx((3 / 4) / 0.5)


def test_bootstrap_interval_brackets_the_mean_and_is_reproducible() -> None:
    values = np.array([0.4, 0.6, 0.7, 0.8, 0.9, 0.5])

    low, high = bootstrap_interval(values, seed=1)

    assert low < values.mean() < high
    assert (low, high) == bootstrap_interval(values, seed=1)
    assert bootstrap_interval(np.array([0.7]), seed=1) == (0.7, 0.7)
    assert all(np.isnan(bootstrap_interval(np.array([]), seed=1)))


def test_cells_within_uses_the_grid_distance_between_cell_centres() -> None:
    ids = np.array(["1kmE4400N2300", "1kmE4410N2300", "1kmE4400N2321", "1kmE4414N2314"])

    near = cells_within("1kmE4400N2300", ids, radius_km=20)

    assert near.tolist() == [False, True, False, True]  # itself excluded; 21 km too far
