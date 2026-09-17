"""Evaluate one factor for every cell and target day.

Each kind returns its 0-1 ``value`` (after the ``floor``), and where the factor reads a
measurable input, that ``input`` (the aggregate, the count of days, the attribute) so the "why this
score" copy can quote it. A rain event also returns ``days_ago``: when the rain it scored fell.
"""

import math
from dataclasses import dataclass

import numpy as np

from api.model import series
from api.model.arrays import ANOMALY_WINDOW_DAYS, Cells, Weather
from api.model.rules import (
    CountDaysFactor,
    DaysSinceFactor,
    Factor,
    HabitatFactor,
    RainEventFactor,
    SeasonWindowFactor,
    StaticBandFactor,
    WindowAggregateFactor,
    ddmm_day_of_year,
)

YEAR_DAYS = 365


@dataclass(frozen=True)
class Evaluated:
    value: np.ndarray  # (cells, targets) 0-1, NaN when the inputs are missing
    input: np.ndarray | None = None  # (cells, targets) the measured input, in its own unit
    days_ago: np.ndarray | None = None  # (cells, targets) rain events: lag of the scored rain


def _lags(factor: RainEventFactor) -> list[int]:
    """Whole-day lags the lag response gives any weight to."""
    a, _, _, d = factor.response.lag_days
    candidates = np.arange(max(0, math.floor(a)), math.ceil(d) + 1, dtype=float)
    weights = series.trapezoid(candidates, factor.response.lag_days)
    return [int(lag) for lag, w in zip(candidates, weights, strict=True) if w > 0]


def _variable_lookback(variable: str) -> int:
    return ANOMALY_WINDOW_DAYS if variable == "temperature_2m_max_anomaly_30d" else 0


def lookback_days(factor: Factor) -> int:
    """How many days before a target day the factor reads."""
    match factor:
        case RainEventFactor():
            return max(_lags(factor)) + factor.input.accumulation_days - 1
        case WindowAggregateFactor() | CountDaysFactor():
            inp = factor.input
            return inp.window_days + inp.offset_days - 1 + _variable_lookback(inp.variable)
        case DaysSinceFactor():
            inp = factor.input
            return inp.max_lookback_days + _variable_lookback(inp.variable)
        case _:
            return 0


def _static(values: np.ndarray, targets: slice, weather: Weather) -> np.ndarray:
    days = len(range(*targets.indices(len(weather.dates))))
    return np.broadcast_to(values[:, np.newaxis], (len(values), days))


def _unwrapped(dates: tuple[str, str, str, str]) -> tuple[float, float, float, float]:
    """Window dates as days of year, made non-decreasing across the year end."""
    days = [float(ddmm_day_of_year(d)) for d in dates]
    for i in range(1, 4):
        while days[i] < days[i - 1]:
            days[i] += YEAR_DAYS
    return tuple(days)  # type: ignore[return-value]


def _season(factor: SeasonWindowFactor, cells: Cells, weather: Weather, targets: slice):
    doy = series.day_of_year(weather.dates[targets]).astype(float)[np.newaxis, :]
    elevation = cells.attributes["elevation_m"][:, np.newaxis]
    best = np.zeros((len(cells), doy.shape[1]))
    for window in factor.input.windows:
        t = doy
        if window.altitude_shift is not None:
            shift = window.altitude_shift
            t = doy - shift.days_per_100m * (elevation - shift.reference_m) / 100.0
        edges = _unwrapped(window.dates)
        inside = np.maximum.reduce([series.trapezoid(t + k * YEAR_DAYS, edges) for k in (-1, 0, 1)])
        if window.elevation_weight is not None:
            inside = inside * series.trapezoid(elevation, window.elevation_weight)
        best = np.maximum(best, inside)
    return Evaluated(value=best)


def _habitat(factor: HabitatFactor, cells: Cells, weather: Weather, targets: slice):
    affinity = np.array(
        [factor.input.affinity.get(h, factor.input.default) for h in cells.habitat_names]
    )
    return Evaluated(value=_static(cells.habitat_fractions @ affinity, targets, weather))


def _static_band(factor: StaticBandFactor, cells: Cells, weather: Weather, targets: slice):
    attribute = cells.attributes[factor.input.attribute]
    value = series.trapezoid(attribute, factor.response.trapezoid)
    return Evaluated(
        value=_static(series.with_floor(value, factor.floor), targets, weather),
        input=_static(attribute, targets, weather),
    )


def _rain_event(factor: RainEventFactor, cells: Cells, weather: Weather, targets: slice):
    rain = weather.series(factor.input.variable)
    totals = series.rolling(rain, factor.input.accumulation_days, "sum")
    n, days = rain.shape
    index = np.arange(days)[targets]
    best = np.full((n, len(index)), -1.0)
    best_amount = np.full((n, len(index)), -1.0)
    best_lag = np.zeros((n, len(index)))
    wettest = np.full((n, len(index)), -1.0)
    wettest_lag = np.zeros((n, len(index)))
    missing = np.zeros((n, len(index)), dtype=bool)
    # Longest lag first, so a tie goes to the window that ends where the rain ended.
    for lag in sorted(_lags(factor), reverse=True):
        source = index - lag
        amount = np.full((n, len(index)), np.nan)
        reachable = source >= 0
        amount[:, reachable] = totals[:, source[reachable]]
        missing |= np.isnan(amount)
        lag_weight = series.trapezoid(np.array([float(lag)]), factor.response.lag_days)[0]
        candidate = series.trapezoid(amount, factor.response.amount_mm) * lag_weight
        better = np.nan_to_num(candidate, nan=-1.0) > best
        best = np.where(better, candidate, best)
        best_amount = np.where(better, amount, best_amount)
        best_lag = np.where(better, lag, best_lag)
        wetter = np.nan_to_num(amount, nan=-1.0) > wettest
        wettest = np.where(wetter, amount, wettest)
        wettest_lag = np.where(wetter, lag, wettest_lag)
    dry = best <= 0
    value = series.with_floor(np.maximum(best, 0.0), factor.floor)
    reported = np.where(dry, wettest, best_amount)
    lag = np.where(dry, wettest_lag, best_lag)
    value[missing], reported[missing], lag[missing] = np.nan, np.nan, np.nan
    return Evaluated(value=value, input=reported, days_ago=lag)


def _window_aggregate(factor: WindowAggregateFactor, cells: Cells, weather: Weather, targets):
    inp = factor.input
    aggregate = series.rolling(
        weather.series(inp.variable), inp.window_days, inp.aggregate, inp.offset_days
    )[:, targets]
    value = series.trapezoid(aggregate, factor.response.trapezoid)
    return Evaluated(value=series.with_floor(value, factor.floor), input=aggregate)


def _count_days(factor: CountDaysFactor, cells: Cells, weather: Weather, targets: slice):
    inp = factor.input
    counts = series.count_days(
        weather.series(inp.variable), inp.op, inp.threshold, inp.window_days, inp.offset_days
    )[:, targets]
    value = series.trapezoid(counts, factor.response.trapezoid)
    return Evaluated(value=series.with_floor(value, factor.floor), input=counts)


def _days_since(factor: DaysSinceFactor, cells: Cells, weather: Weather, targets: slice):
    inp = factor.input
    days = series.days_since(
        weather.series(inp.variable), inp.op, inp.threshold, inp.max_lookback_days
    )[:, targets]
    value = series.trapezoid(days, factor.response.trapezoid)
    return Evaluated(value=series.with_floor(value, factor.floor), input=days)


_KINDS = {
    "season_window": _season,
    "habitat": _habitat,
    "static_band": _static_band,
    "rain_event": _rain_event,
    "window_aggregate": _window_aggregate,
    "count_days": _count_days,
    "days_since": _days_since,
}


def evaluate(factor: Factor, cells: Cells, weather: Weather, targets: slice) -> Evaluated:
    """The factor for every cell on the target days ``weather.dates[targets]``."""
    if getattr(factor.input, "aggregate", None) in ("percent_of_normal", "percentile_of_normal"):
        raise NotImplementedError(f"{factor.id}: {factor.input.aggregate} needs a climatology")
    return _KINDS[factor.kind](factor, cells, weather, targets)
