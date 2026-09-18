from datetime import date, timedelta

import pandas as pd
import pytest

from api.history.config import RainTilt
from api.history.outlook import (
    Period,
    daily_signal,
    mean_temperature_anomaly,
    outlook_periods,
    period_starts,
    rain_share,
    tilt,
    typical_for_period,
)

TODAY = date(2026, 9, 18)  # a Friday: the 7-day forecast runs to Friday 25
MONDAYS = [date(2026, 9, 14) + timedelta(weeks=i) for i in range(7)]  # 14 Sep .. 26 Oct
MONTHS = [date(2026, m, 1) for m in (9, 10, 11, 12)] + [date(2027, 1, 1)]
PORCINI = (date(2026, 5, 1), date(2026, 12, 20))


# --- outlook_periods ---------------------------------------------------------------------------


def test_weeks_start_after_the_7_day_forecast_then_months_follow() -> None:
    periods = outlook_periods(TODAY, 7, MONDAYS, MONTHS, PORCINI, months_ahead=3)

    assert periods[:2] == [
        Period(date(2026, 9, 28), date(2026, 10, 4), "week"),
        Period(date(2026, 10, 5), date(2026, 10, 11), "week"),
    ]
    weeks = [p for p in periods if p.kind == "week"]
    assert weeks[-1] == Period(date(2026, 10, 26), date(2026, 11, 1), "week")
    months = [p for p in periods if p.kind == "month"]
    # November starts the day after the last week; December stops at the end of the season.
    assert months == [
        Period(date(2026, 11, 2), date(2026, 11, 30), "month"),
        Period(date(2026, 12, 1), date(2026, 12, 20), "month"),
    ]


def test_months_stop_after_months_ahead() -> None:
    periods = outlook_periods(TODAY, 7, [], MONTHS, (date(2026, 1, 1), date(2026, 12, 31)), 1)

    assert periods == [Period(date(2026, 10, 1), date(2026, 10, 31), "month")]


def test_periods_outside_the_season_window_are_dropped_and_edges_clipped() -> None:
    ovoli = (date(2026, 6, 1), date(2026, 10, 10))

    periods = outlook_periods(TODAY, 7, MONDAYS, MONTHS, ovoli, months_ahead=3)

    assert periods == [
        Period(date(2026, 9, 28), date(2026, 10, 4), "week"),
        Period(date(2026, 10, 5), date(2026, 10, 10), "week"),
    ]


def test_out_of_season_there_are_no_periods() -> None:
    spring = (date(2026, 4, 15), date(2026, 7, 31))

    assert outlook_periods(TODAY, 7, MONDAYS, MONTHS, spring, months_ahead=3) == []


# --- typical_for_period ------------------------------------------------------------------------


def _days(year: int, good_by_day: dict[tuple[int, int], int], cells: int = 4) -> list[dict]:
    return [
        {"date": date(year, m, d), "cells": cells, "good_cells": good}
        for (m, d), good in good_by_day.items()
    ]


def test_past_seasons_tally_the_years_in_which_the_same_days_were_good() -> None:
    first_week = {(9, 28 + i) if i < 3 else (10, i - 2): 0 for i in range(7)}
    rows = [
        *_days(2023, {**first_week, (9, 28): 4, (9, 29): 4}),  # 8 of 28 cell-days: 0.29
        *_days(2024, first_week),  # none
        *_days(2025, {**first_week, (10, 1): 4, (10, 2): 4, (10, 3): 4}),  # 12 of 28: 0.43
    ]

    typical = typical_for_period(
        pd.DataFrame(rows),
        Period(date(2026, 9, 28), date(2026, 10, 4), "week"),
        years=[2023, 2024, 2025],
        good_share=0.25,
    )

    assert typical.good_years == 2
    assert typical.years == 3
    assert typical.share == pytest.approx(8 / 28)  # the median season


def test_years_without_scores_do_not_count() -> None:
    rows = _days(2025, {(10, 1): 4})

    typical = typical_for_period(
        pd.DataFrame(rows),
        Period(date(2026, 10, 1), date(2026, 10, 1), "week"),
        years=[2024, 2025],
        good_share=0.25,
    )

    assert (typical.good_years, typical.years) == (1, 1)


def test_no_past_seasons_give_an_empty_tally() -> None:
    typical = typical_for_period(
        pd.DataFrame(columns=["date", "cells", "good_cells"]),
        Period(date(2026, 10, 1), date(2026, 10, 7), "week"),
        years=[2024, 2025],
        good_share=0.25,
    )

    assert (typical.good_years, typical.years, typical.share) == (0, 0, None)


# --- daily_signal ------------------------------------------------------------------------------


def _observed(start: date, rain: list[float], normal: float = 2.0, temp_anomaly: float = 1.0):
    return pd.DataFrame(
        {
            "date": [start + timedelta(days=i) for i in range(len(rain))],
            "precipitation_sum": rain,
            "precipitation_normal": normal,
            "temperature_2m_mean": 15.0 + temp_anomaly,
            "temperature_normal": 15.0,
        }
    )


def _seasonal(*rows: tuple) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["kind", "start", "end", "variable", "value", "anomaly"])


def test_observed_days_come_first_then_weeks_then_months() -> None:
    observed = _observed(date(2026, 9, 20), [1.0] * 6)  # 20-25 September
    seasonal = _seasonal(
        ("week", date(2026, 9, 21), date(2026, 9, 27), "precipitation_sum", 14.0, 7.0),
        ("week", date(2026, 9, 21), date(2026, 9, 27), "temperature_2m_mean", 16.0, 2.0),
        ("month", date(2026, 9, 1), date(2026, 9, 30), "precipitation_sum", 90.0, 30.0),
        ("month", date(2026, 9, 1), date(2026, 9, 30), "temperature_2m_mean", 16.0, -1.0),
    )

    signal = daily_signal(observed, seasonal).set_index("date")

    assert signal.loc[date(2026, 9, 25), "source"] == "observed"
    assert signal.loc[date(2026, 9, 25), "rain"] == pytest.approx(1.0)
    # 26-27 September: the week's 14 mm spread over its 7 days; its normal is 14 - 7 = 7 mm.
    assert signal.loc[date(2026, 9, 26), "source"] == "week"
    assert signal.loc[date(2026, 9, 26), "rain"] == pytest.approx(2.0)
    assert signal.loc[date(2026, 9, 26), "rain_normal"] == pytest.approx(1.0)
    assert signal.loc[date(2026, 9, 26), "temp_anomaly"] == pytest.approx(2.0)
    # 28-30 September: only the month covers them.
    assert signal.loc[date(2026, 9, 28), "source"] == "month"
    assert signal.loc[date(2026, 9, 28), "rain"] == pytest.approx(3.0)
    assert signal.loc[date(2026, 9, 28), "rain_normal"] == pytest.approx(2.0)
    assert signal.loc[date(2026, 9, 28), "temp_anomaly"] == pytest.approx(-1.0)
    # The month does not reach back over observed days.
    assert signal.loc[date(2026, 9, 20), "source"] == "observed"


def test_a_signal_without_seasonal_data_is_the_observed_days() -> None:
    signal = daily_signal(_observed(date(2026, 9, 20), [1.0, 2.0]), _seasonal())

    assert signal["date"].tolist() == [date(2026, 9, 20), date(2026, 9, 21)]
    assert signal["temp_anomaly"].tolist() == pytest.approx([1.0, 1.0])


# --- rain_share / mean_temperature_anomaly -----------------------------------------------------


def test_rain_share_is_total_over_normal_in_percent() -> None:
    signal = daily_signal(_observed(date(2026, 9, 1), [4.0, 0.0, 2.0], normal=2.0), _seasonal())

    assert rain_share(signal, date(2026, 9, 1), date(2026, 9, 3)) == pytest.approx(100.0)
    assert rain_share(signal, date(2026, 9, 1), date(2026, 9, 1)) == pytest.approx(200.0)


def test_rain_share_needs_every_day_of_the_window() -> None:
    signal = daily_signal(_observed(date(2026, 9, 1), [4.0, 0.0]), _seasonal())

    assert rain_share(signal, date(2026, 9, 1), date(2026, 9, 3)) is None


def test_mean_temperature_anomaly_over_a_window() -> None:
    signal = daily_signal(_observed(date(2026, 9, 1), [0.0] * 3, temp_anomaly=1.5), _seasonal())

    assert mean_temperature_anomaly(signal, date(2026, 9, 1), date(2026, 9, 3)) == pytest.approx(
        1.5
    )
    assert mean_temperature_anomaly(signal, date(2026, 9, 1), date(2026, 9, 9)) is None


# --- tilt --------------------------------------------------------------------------------------

RAIN = RainTilt(wetter_pct=125, drier_pct=75, confidence="plausible", source=["x"], notes="n")


@pytest.mark.parametrize(
    ("share", "expected"),
    [(None, "unknown"), (50.0, "worse"), (75.0, "worse"), (100.0, "usual"), (125.0, "better")],
)
def test_the_tilt_follows_the_lead_windows_rain(share: float | None, expected: str) -> None:
    assert tilt(share, RAIN) == expected


# --- period_starts -----------------------------------------------------------------------------


def test_period_starts_come_from_the_calendar_not_from_the_data() -> None:
    weeks, months = period_starts(TODAY, week_horizon_days=46, months=5)

    assert weeks[0] == date(2026, 9, 14)  # this week's Monday
    assert all(w.weekday() == 0 for w in weeks)
    # Whole weeks inside the long-range reach only: 26 Oct-1 Nov ends before 3 Nov; 2-8 Nov doesn't.
    assert weeks[-1] == date(2026, 10, 26)
    assert months == [
        date(2026, 9, 1),
        date(2026, 10, 1),
        date(2026, 11, 1),
        date(2026, 12, 1),
        date(2027, 1, 1),
    ]
    assert weeks[: len(MONDAYS)] == MONDAYS
