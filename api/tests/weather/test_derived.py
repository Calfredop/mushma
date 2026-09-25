"""Unit tests for FAO-56 / Open-Meteo derived VPD and ET0."""

import numpy as np
import pytest

from api.weather.derived import (
    daily_et0_mm,
    daily_vpd_max_kpa,
    saturation_vapour_pressure_kpa,
    vapour_pressure_deficit_kpa,
)


def test_saturation_vapour_pressure_at_20c_matches_fao56_table() -> None:
    # FAO-56 Table 2.3: e°(20 °C) = 2.3388 kPa.
    assert float(saturation_vapour_pressure_kpa(20.0)) == pytest.approx(2.3388, abs=0.001)


def test_vpd_is_zero_when_air_is_saturated() -> None:
    assert float(vapour_pressure_deficit_kpa(15.0, 15.0)) == pytest.approx(0.0, abs=1e-9)


def test_vpd_grows_when_dewpoint_drops() -> None:
    humid = float(vapour_pressure_deficit_kpa(25.0, 20.0))
    dry = float(vapour_pressure_deficit_kpa(25.0, 5.0))
    assert dry > humid > 0.0


def test_daily_vpd_max_picks_the_driest_hour() -> None:
    t = np.array([10.0, 20.0, 30.0])
    td = np.array([10.0, 10.0, 10.0])
    assert daily_vpd_max_kpa(t, td) == pytest.approx(float(vapour_pressure_deficit_kpa(30.0, 10.0)))


def test_daily_et0_is_positive_on_a_sunny_day_and_near_zero_at_night() -> None:
    hours = np.arange(24)
    t = np.full(24, 20.0)
    td = np.full(24, 12.0)
    wind = np.full(24, 2.0)  # m/s at 10 m
    night = np.zeros(24)
    day = np.where((hours >= 8) & (hours <= 16), 1.5, 0.0)  # MJ m^-2 per hour
    sunny = daily_et0_mm(t, td, wind, day, 300.0, 43.5, hours, day_of_year=200)
    dark = daily_et0_mm(t, td, wind, night, 300.0, 43.5, hours, day_of_year=200)
    assert sunny > 2.0
    assert sunny > dark * 1.5  # radiation term dominates on a sunny day
