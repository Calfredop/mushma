from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from api.weather.checks import compare_gauge, lapse_regression, leave_out_errors
from api.weather.points import point_id
from api.weather.sir import gauge_day_totals

DAYS = [date(2024, 10, 1) + timedelta(days=i) for i in range(3)]


def _nodes() -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(7)
    for i in range(11):
        for j in range(11):
            lat, lon = round(43.0 + i / 10, 6), round(11.0 + j / 10, 6)
            rows.append((point_id(lat, lon), lat, lon, float(rng.uniform(0, 1500))))
    return pd.DataFrame(rows, columns=["point_id", "lat", "lon", "z"])


def _field(nodes: pd.DataFrame, cooling_per_km: float) -> pd.DataFrame:
    """A temperature that is linear in lat/lon and cools with height; the day adds an offset."""
    rows = []
    for k, day in enumerate(DAYS):
        values = (
            20 + k - 2 * (nodes.lat - 43) + 0.5 * (nodes.lon - 11) - cooling_per_km * nodes.z / 1000
        )
        rows += [
            (pid, day, "temperature_2m_mean", v)
            for pid, v in zip(nodes.point_id, values, strict=True)
        ]
    return pd.DataFrame(rows, columns=["point_id", "date", "variable", "value"])


def test_lapse_regression_recovers_the_cooling_rate_across_nodes() -> None:
    nodes = _nodes()

    rates = lapse_regression(_field(nodes, cooling_per_km=4.5), nodes)

    assert set(rates["date"]) == set(DAYS)
    assert rates["cooling_per_km"].to_numpy() == pytest.approx(4.5)


def test_leave_out_is_exact_for_a_linear_field_with_the_right_lapse_rate() -> None:
    nodes = _nodes()
    daily = _field(nodes, cooling_per_km=4.5)

    right = leave_out_errors(daily, nodes, stride=2, lapse_rates={"temperature_2m_mean": 4.5})
    wrong = leave_out_errors(daily, nodes, stride=2, lapse_rates={"temperature_2m_mean": 0.0})

    assert right.loc["temperature_2m_mean", "rmse"] == pytest.approx(0.0, abs=1e-9)
    assert wrong.loc["temperature_2m_mean", "rmse"] > 0.1
    assert right.loc["temperature_2m_mean", "targets"] > 0


def test_compare_gauge_measures_bias_and_agreement_on_gauge_days() -> None:
    days = pd.date_range("2025-01-01", periods=120).date
    rng = np.random.default_rng(3)
    calendar = pd.Series(rng.gamma(0.4, 12, len(days)), index=days)
    gauge = gauge_day_totals(calendar)

    metrics = compare_gauge(0.8 * calendar, gauge)

    assert metrics["days"] == 119
    assert metrics["ratio"] == pytest.approx(0.8)
    assert metrics["daily_corr"] == pytest.approx(1.0)
    assert metrics["wet3_hit_rate"] <= 1.0
