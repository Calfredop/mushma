from datetime import date

import numpy as np
import pytest

from api.model.series import (
    count_days,
    day_of_year,
    days_since,
    lagged_anomaly,
    percent_of_normal,
    rolling,
    trapezoid,
    with_floor,
)

nan = np.nan


def _row(*values: float) -> np.ndarray:
    return np.array([values], dtype=float)


# --- trapezoid ---------------------------------------------------------------------------------


def test_trapezoid_is_zero_outside_linear_on_the_ramps_and_one_on_the_plateau() -> None:
    x = np.array([0.0, 10.0, 15.0, 20.0, 30.0, 40.0, 45.0, 50.0, 60.0])

    assert trapezoid(x, (10, 20, 40, 50)).tolist() == [0, 0, 0.5, 1, 1, 1, 0.5, 0, 0]


def test_a_null_lower_pair_opens_the_trapezoid_downwards() -> None:
    x = np.array([-100.0, 800.0, 1025.0, 1250.0])

    assert trapezoid(x, (None, None, 800, 1250)).tolist() == [1, 1, 0.5, 0]


def test_a_null_upper_pair_opens_the_trapezoid_upwards() -> None:
    x = np.array([5.0, 20.0, 1000.0])

    assert trapezoid(x, (10, 30, None, None)).tolist() == [0, 0.5, 1]


def test_a_zero_width_ramp_is_a_step_that_includes_its_edge() -> None:
    counts = np.array([0.0, 1.0, 2.0])

    assert trapezoid(counts, (None, None, 0, 0)).tolist() == [1, 0, 0]
    assert trapezoid(counts, (1, 1, None, None)).tolist() == [0, 1, 1]


def test_trapezoid_keeps_missing_values_missing() -> None:
    assert np.isnan(trapezoid(np.array([nan]), (0, 1, 2, 3))).all()


def test_a_floor_lifts_the_response_linearly() -> None:
    raw = np.array([0.0, 1 / 3, 1.0, nan])

    lifted = with_floor(raw, 0.3)

    assert lifted[:3] == pytest.approx([0.3, 0.3 + 0.7 / 3, 1.0])
    assert np.isnan(lifted[3])
    assert with_floor(raw, None) is raw


# --- rolling windows ---------------------------------------------------------------------------


def test_rolling_sum_includes_the_day_itself() -> None:
    rain = _row(1, 2, 3, 4, 5)

    assert rolling(rain, window=3, how="sum")[0, 2:].tolist() == [6, 9, 12]


def test_rolling_window_is_missing_until_it_is_complete() -> None:
    out = rolling(_row(1, 2, 3, 4, 5), window=3, how="mean")

    assert np.isnan(out[0, :2]).all()
    assert out[0, 2:].tolist() == [2, 3, 4]


def test_rolling_offset_ends_the_window_before_the_day() -> None:
    out = rolling(_row(1, 2, 3, 4, 5), window=2, how="sum", offset=1)

    assert np.isnan(out[0, :2]).all()
    assert out[0, 2:].tolist() == [3, 5, 7]


@pytest.mark.parametrize(("how", "expected"), [("min", [1, 1, 0]), ("max", [5, 3, 3])])
def test_rolling_min_and_max(how: str, expected: list[float]) -> None:
    out = rolling(_row(5, 1, 2, 3, 0), window=3, how=how)

    assert out[0, 2:].tolist() == expected


def test_a_missing_day_makes_every_window_holding_it_missing() -> None:
    out = rolling(_row(1, nan, 3, 4, 5, 6), window=2, how="sum")

    assert np.isnan(out[0, :3]).all()
    assert out[0, 3:].tolist() == [7, 9, 11]


def test_rolling_works_across_cells_independently() -> None:
    values = np.array([[1.0, 1.0, 1.0], [2.0, 4.0, 6.0]])

    assert rolling(values, window=2, how="sum")[:, 2].tolist() == [2, 10]


# --- day counts ----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("op", "expected"), [("lt", 1), ("lte", 3), ("gt", 2), ("gte", 4)]
)  # window holds [-1, 0, 0, 2, 5]
def test_count_days_counts_matching_days_in_the_window(op: str, expected: int) -> None:
    tmin = _row(9, -1, 0, 0, 2, 5)

    assert count_days(tmin, op, 0, window=5)[0, 5] == expected


def test_count_days_is_missing_when_the_window_is_incomplete_or_has_gaps() -> None:
    out = count_days(_row(0, 0, nan, 0, 0, 0), "lte", 0, window=3)

    assert np.isnan(out[0, :5]).all()
    assert out[0, 5] == 3


def test_days_since_is_zero_on_a_matching_day_and_counts_up_after() -> None:
    rain = _row(0, 0, 0, 25, 0, 0, 0)

    out = days_since(rain, "gte", 20, max_lookback=3)

    assert out[0, 3:].tolist() == [0, 1, 2, 3]


def test_days_since_is_capped_when_nothing_matches_within_the_lookback() -> None:
    out = days_since(_row(25, 0, 0, 0, 0, 0), "gte", 20, max_lookback=3)

    assert out[0, 3] == 3  # the match 3 days back is still in reach
    assert out[0, 4:].tolist() == [3, 3]


def test_days_since_is_missing_without_a_full_lookback_or_with_gaps() -> None:
    out = days_since(_row(0, 0, 0, nan, 0, 0, 0, 0), "gte", 20, max_lookback=2)

    assert np.isnan(out[0, :2]).all()
    assert np.isnan(out[0, 3:6]).all()
    assert out[0, 2] == 2 and out[0, 6] == 2


# --- derived series and calendar ---------------------------------------------------------------


def test_lagged_anomaly_compares_a_day_with_the_mean_of_the_days_before() -> None:
    tmax = _row(20, 20, 22, 30)

    out = lagged_anomaly(tmax, window=2)

    assert np.isnan(out[0, :2]).all()
    assert out[0, 2:].tolist() == [2, 9]


def test_day_of_year_uses_a_non_leap_calendar() -> None:
    dates = np.array(["2024-01-01", "2024-02-28", "2024-02-29", "2024-03-01", "2024-12-31"])

    assert day_of_year(dates.astype("datetime64[D]")).tolist() == [1, 59, 59, 60, 365]
    assert day_of_year(np.array([date(2025, 3, 1)], dtype="datetime64[D]")).tolist() == [60]


# --- percent of normal -------------------------------------------------------------------------


def test_percent_of_normal_compares_the_window_sum_with_the_normal_sum() -> None:
    rain = _row(0.0, 4.0, 2.0, 6.0)
    normal = _row(2.0, 2.0, 2.0, 2.0)

    out = percent_of_normal(rain, normal, 2)

    assert out[0].tolist() == pytest.approx([nan, 100.0, 150.0, 200.0], nan_ok=True)


def test_percent_of_normal_is_missing_on_gaps_and_where_the_normal_is_dry() -> None:
    rain = _row(1.0, nan, 1.0, 1.0)
    normal = _row(1.0, 1.0, 0.0, 0.0)

    out = percent_of_normal(rain, normal, 2)

    assert np.isnan(out[0]).tolist() == [True, True, True, True]
