from datetime import date

import pandas as pd
import pytest

from api.history.normals import complete_years, daily_normals


def _year(point: str, variable: str, year: int, value) -> pd.DataFrame:
    """Every day of ``year`` for one point and variable; ``value`` is a constant or a function of
    the date."""
    days = pd.date_range(date(year, 1, 1), date(year, 12, 31), freq="D").date
    values = [value(d) if callable(value) else value for d in days]
    return pd.DataFrame({"point_id": point, "date": days, "variable": variable, "value": values})


def _rows(*frames: pd.DataFrame) -> pd.DataFrame:
    return pd.concat(frames, ignore_index=True)


# --- complete_years ----------------------------------------------------------------------------


def test_a_year_counts_only_when_every_point_has_every_day_of_every_variable() -> None:
    rows = _rows(
        _year("A", "precipitation_sum", 2021, 1.0),
        _year("B", "precipitation_sum", 2021, 1.0),
        _year("A", "precipitation_sum", 2022, 1.0),
        _year("B", "precipitation_sum", 2022, 1.0).iloc[:-1],  # misses 31 December
    )

    assert complete_years(rows, points=["A", "B"], variables=["precipitation_sum"]) == [2021]


def test_a_missing_variable_makes_the_year_incomplete() -> None:
    rows = _rows(_year("A", "precipitation_sum", 2021, 1.0))

    years = complete_years(
        rows, points=["A"], variables=["precipitation_sum", "temperature_2m_mean"]
    )

    assert years == []


# --- daily_normals -----------------------------------------------------------------------------


def test_the_normal_is_the_mean_over_the_years_of_each_calendar_day() -> None:
    rows = _rows(
        _year("A", "temperature_2m_mean", 2021, 10.0),
        _year("A", "temperature_2m_mean", 2022, 14.0),
    )

    normals = daily_normals(rows, years=[2021, 2022], window_days=1)

    assert len(normals) == 365
    assert normals["normal"].tolist() == pytest.approx([12.0] * 365)
    assert set(normals["years"]) == {2}


def test_years_outside_the_baseline_are_ignored() -> None:
    rows = _rows(
        _year("A", "temperature_2m_mean", 2021, 10.0),
        _year("A", "temperature_2m_mean", 2026, 30.0),
    )

    normals = daily_normals(rows, years=[2021], window_days=1)

    assert normals["normal"].tolist() == pytest.approx([10.0] * 365)


def test_the_centred_window_smooths_across_the_new_year() -> None:
    # 1 January is wet (31 mm) and every other day dry: a 31-day centred window spreads it over
    # 15 days either side, wrapping into December.
    rows = _year("A", "precipitation_sum", 2021, lambda d: 31.0 if d == date(2021, 1, 1) else 0.0)

    normals = daily_normals(rows, years=[2021], window_days=31).set_index("doy")["normal"]

    assert normals[1] == pytest.approx(1.0)
    assert normals[16] == pytest.approx(1.0)  # 1 January is the window's first day
    assert normals[17] == pytest.approx(0.0)
    assert normals[351] == pytest.approx(1.0)  # 17 December reaches 1 January
    assert normals[350] == pytest.approx(0.0)
    # Smoothing never adds or loses rain over the year.
    assert normals.sum() == pytest.approx(31.0)


def test_29_february_counts_as_28_february() -> None:
    leap = _year("A", "temperature_2m_mean", 2024, lambda d: 20.0 if d.month == 2 else 0.0)

    normals = daily_normals(leap, years=[2024], window_days=1).set_index("doy")["normal"]

    assert len(normals) == 365
    assert normals[59] == pytest.approx(20.0)  # 28 Feb and 29 Feb, both 20
    assert normals[60] == pytest.approx(0.0)  # 1 March


def test_normals_are_kept_per_point_and_variable() -> None:
    rows = _rows(
        _year("A", "temperature_2m_mean", 2021, 10.0),
        _year("B", "temperature_2m_mean", 2021, 5.0),
        _year("A", "precipitation_sum", 2021, 2.0),
    )

    normals = daily_normals(rows, years=[2021], window_days=31)

    means = normals.groupby(["point_id", "variable"])["normal"].mean()
    assert means[("A", "temperature_2m_mean")] == pytest.approx(10.0)
    assert means[("B", "temperature_2m_mean")] == pytest.approx(5.0)
    assert means[("A", "precipitation_sum")] == pytest.approx(2.0)


def test_an_even_window_is_rejected() -> None:
    with pytest.raises(ValueError, match="odd"):
        daily_normals(_year("A", "precipitation_sum", 2021, 1.0), years=[2021], window_days=30)
