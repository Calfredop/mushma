from datetime import date

import numpy as np
import pytest

from api.model.factors import evaluate, lookback_days

from .helpers import cells, day_index, factor, weather

nan = np.nan


def _all_days(w) -> slice:
    return slice(0, len(w.dates))


# --- season_window -----------------------------------------------------------------------------


def _season(*windows: dict) -> object:
    return factor(kind="season_window", role="gate", input={"windows": list(windows)})


def test_season_window_ramps_in_is_full_on_the_plateau_and_ramps_out() -> None:
    rule = _season({"label": "autumn", "dates": ["01-07", "01-09", "15-11", "20-12"]})
    w = weather(start=date(2024, 6, 1), days=214, rain=0.0)  # to 31 Dec

    value = evaluate(rule, cells(), w, _all_days(w)).value[0]

    assert value[day_index(w, date(2024, 6, 15))] == 0
    assert value[day_index(w, date(2024, 8, 1))] == pytest.approx(31 / 62)
    assert value[day_index(w, date(2024, 10, 1))] == 1
    assert value[day_index(w, date(2024, 12, 20))] == 0


def test_season_window_can_wrap_the_year_end() -> None:
    rule = _season({"label": "winter", "dates": ["15-11", "15-12", "10-01", "25-01"]})
    w = weather(start=date(2024, 11, 1), days=100, rain=0.0)

    value = evaluate(rule, cells(), w, _all_days(w)).value[0]

    assert value[day_index(w, date(2024, 12, 31))] == 1
    assert value[day_index(w, date(2025, 1, 5))] == 1
    assert value[day_index(w, date(2025, 1, 20))] == pytest.approx(1 / 3)
    assert value[day_index(w, date(2025, 2, 1))] == 0
    assert value[day_index(w, date(2024, 11, 30))] == pytest.approx(0.5)


def test_elevation_weights_hand_over_between_windows() -> None:
    rule = _season(
        {
            "label": "lowland",
            "dates": ["01-01", "02-01", "30-12", "31-12"],
            "elevation_weight": [None, None, 400, 600],
        },
        {
            "label": "upland",
            "dates": ["01-07", "01-08", "30-09", "31-10"],
            "elevation_weight": [400, 600, None, None],
        },
    )
    w = weather(start=date(2024, 3, 1), days=200, rain=0.0)
    here = cells(3, elevation_m=[300, 500, 900])

    value = evaluate(rule, here, w, _all_days(w)).value
    march, august = day_index(w, date(2024, 3, 15)), day_index(w, date(2024, 8, 15))

    assert value[:, march].tolist() == [1, 0.5, 0]
    assert value[:, august].tolist() == [1, 0.5, 1]


def test_altitude_shift_delays_the_window_higher_up() -> None:
    rule = _season(
        {
            "label": "autumn",
            "dates": ["01-09", "11-09", "30-09", "10-10"],
            "altitude_shift": {"reference_m": 500, "days_per_100m": -2},
        }
    )
    w = weather(start=date(2024, 8, 20), days=40, rain=0.0)
    here = cells(2, elevation_m=[500, 1000])  # the second opens 10 days earlier

    value = evaluate(rule, here, w, _all_days(w)).value

    assert value[:, day_index(w, date(2024, 9, 1))].tolist() == [0, 1]


# --- static factors ----------------------------------------------------------------------------


def test_habitat_is_the_fraction_weighted_affinity() -> None:
    rule = factor(
        kind="habitat",
        role="gate",
        input={"affinity": {"beech": 1.0, "chestnut": 0.5}, "default": 0.1},
    )
    here = cells(
        2,
        habitats={"beech": [0.5, 0.0], "chestnut": [0.5, 0.2], "macchia": [0.0, 0.8]},
    )
    w = weather(days=3, rain=0.0)

    result = evaluate(rule, here, w, slice(1, 3))

    assert result.value.shape == (2, 2)
    assert result.value[:, 0] == pytest.approx([0.75, 0.18])


def test_static_band_scores_a_cell_attribute_and_reports_it() -> None:
    rule = factor(
        kind="static_band",
        role="gate",
        input={"attribute": "elevation_m"},
        response={"trapezoid": [None, None, 800, 1250]},
    )
    w = weather(days=2, rain=0.0)

    result = evaluate(rule, cells(2, elevation_m=[300, 1025]), w, slice(0, 2))

    assert result.value[:, 1].tolist() == [1, 0.5]
    assert result.input[:, 1].tolist() == [300, 1025]


# --- rain_event --------------------------------------------------------------------------------


def _rain_trigger() -> object:
    return factor(
        kind="rain_event",
        role="driver",
        weight=2,
        input={"variable": "precipitation_sum", "accumulation_days": 3},
        response={"amount_mm": [10, 30, None, None], "lag_days": [6, 10, 16, 24]},
    )


def _rain_on(total_days: int, falls: dict[int, float]) -> list[float]:
    rain = [0.0] * total_days
    for day, mm in falls.items():
        rain[day] = mm
    return rain


def test_rain_event_finds_the_rain_and_how_many_days_ago_it_fell() -> None:
    w = weather(precipitation_sum=_rain_on(40, {20: 12.0, 21: 18.0}))  # 30 mm ending day 21

    result = evaluate(_rain_trigger(), cells(), w, slice(33, 34))

    assert result.value[0, 0] == 1
    assert result.days_ago[0, 0] == 12
    assert result.input[0, 0] == 30


def test_rain_event_multiplies_amount_by_the_lag_response() -> None:
    w = weather(precipitation_sum=_rain_on(40, {30: 20.0}))  # 20 mm, 8 days before day 38

    result = evaluate(_rain_trigger(), cells(), w, slice(38, 39))

    assert result.value[0, 0] == pytest.approx(0.5 * 0.5)
    assert result.days_ago[0, 0] == 8


def test_rain_event_keeps_the_best_of_several_rains() -> None:
    rain = _rain_on(50, {25: 30.0, 38: 30.0})  # at day 48: 23 and 10 days ago

    result = evaluate(_rain_trigger(), cells(), weather(precipitation_sum=rain), slice(48, 49))

    assert result.value[0, 0] == 1
    assert result.days_ago[0, 0] == 10


def test_rain_event_without_enough_rain_reports_the_biggest_rain_in_the_lag_window() -> None:
    rain = _rain_on(40, {25: 4.0, 30: 9.0})

    result = evaluate(_rain_trigger(), cells(), weather(precipitation_sum=rain), slice(39, 40))

    assert result.value[0, 0] == 0
    assert result.input[0, 0] == 9
    assert result.days_ago[0, 0] == 9


def test_rain_event_needs_the_whole_lag_window() -> None:
    assert lookback_days(_rain_trigger()) == 25  # lags up to 23 days, over 3 days
    w = weather(precipitation_sum=[0.0] * 30)

    assert np.isnan(evaluate(_rain_trigger(), cells(), w, slice(24, 26)).value[0, 0])
    assert not np.isnan(evaluate(_rain_trigger(), cells(), w, slice(24, 26)).value[0, 1])


# --- daily windows -----------------------------------------------------------------------------


def test_window_aggregate_scores_the_aggregate_and_reports_it() -> None:
    rule = factor(
        kind="window_aggregate",
        role="driver",
        weight=1,
        input={"variable": "precipitation_sum", "aggregate": "sum", "window_days": 30},
        response={"trapezoid": [20, 40, None, None]},
    )
    w = weather(precipitation_sum=[1.0] * 40)

    result = evaluate(rule, cells(), w, slice(29, 31))

    assert result.value[0].tolist() == [0.5, 0.5]
    assert result.input[0].tolist() == [30, 30]
    assert lookback_days(rule) == 29


def test_count_days_applies_the_floor() -> None:
    rule = factor(
        kind="count_days",
        role="stopper",
        input={"variable": "temperature_2m_min", "op": "lte", "threshold": 0, "window_days": 7},
        response={"trapezoid": [None, None, 1, 2]},
        floor=0.2,
    )
    tmin = [5.0] * 5 + [-1.0, -2.0, 3.0]

    result = evaluate(rule, cells(), weather(temperature_2m_min=tmin), slice(6, 8))

    assert result.value[0].tolist() == pytest.approx([0.2, 0.2])
    assert result.input[0].tolist() == [2, 2]


def test_days_since_scores_the_days_since_a_matching_day() -> None:
    rule = factor(
        kind="days_since",
        role="driver",
        weight=1,
        input={
            "variable": "precipitation_sum",
            "op": "gte",
            "threshold": 20,
            "max_lookback_days": 30,
        },
        response={"trapezoid": [None, None, 10, 20]},
    )
    rain = _rain_on(50, {30: 25.0})

    result = evaluate(rule, cells(), weather(precipitation_sum=rain), slice(45, 46))

    assert result.input[0, 0] == 15
    assert result.value[0, 0] == 0.5


def test_water_balance_is_rain_minus_evapotranspiration() -> None:
    rule = factor(
        kind="window_aggregate",
        role="stopper",
        input={"variable": "water_balance", "aggregate": "sum", "window_days": 2},
        response={"trapezoid": [-10, 0, None, None]},
    )
    w = weather(precipitation_sum=[1.0, 1.0, 1.0], et0_fao_evapotranspiration=[3.0, 4.0, 4.0])

    result = evaluate(rule, cells(), w, slice(2, 3))

    assert result.input[0, 0] == -6
    assert result.value[0, 0] == pytest.approx(0.4)


def test_heat_spike_uses_the_tmax_anomaly_against_the_previous_30_days() -> None:
    rule = factor(
        kind="count_days",
        role="stopper",
        input={
            "variable": "temperature_2m_max_anomaly_30d",
            "op": "gte",
            "threshold": 8,
            "window_days": 14,
        },
        response={"trapezoid": [None, None, 0, 1]},
        floor=0.5,
    )
    tmax = [20.0] * 40 + [29.0] + [20.0] * 5

    result = evaluate(rule, cells(), weather(temperature_2m_max=tmax), slice(43, 46))

    assert lookback_days(rule) == 43
    assert result.value[0].tolist() == [0.5, 0.5, 0.5]
    assert result.input[0].tolist() == [1, 1, 1]


def test_missing_weather_leaves_the_factor_missing() -> None:
    rule = factor(
        kind="window_aggregate",
        role="driver",
        weight=1,
        input={"variable": "temperature_2m_mean", "aggregate": "mean", "window_days": 3},
        response={"trapezoid": [6, 10, 17, 22]},
    )
    w = weather(temperature_2m_mean=[[12.0, 12.0, 12.0, 12.0], [12.0, nan, 12.0, 12.0]])

    result = evaluate(rule, cells(2), w, slice(3, 4))

    assert result.value[:, 0].tolist()[0] == 1
    assert np.isnan(result.value[1, 0])
