"""Evaluate one factor for every cell and target day.

Each kind returns its 0-1 ``value`` (after the ``floor``), and where the factor reads a
measurable input, that ``input`` (the aggregate, the count of days, the attribute) so the "why this
score" copy can quote it. A rain event also returns ``days_ago``: when the rain it scored fell,
and with the species' growth clock on, ``growth_days``: the growth since then, which its lag is
scored on. A factor with a ``where`` condition fades towards 1 outside the cells it applies to.
"""

import math
from dataclasses import dataclass, replace

import numpy as np

from api.model import series
from api.model.arrays import ANOMALY_WINDOW_DAYS, Cells, Weather
from api.model.rules import (
    CountDaysFactor,
    DaysSinceFactor,
    Factor,
    GrowthClock,
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
    growth_days: np.ndarray | None = None  # (cells, targets) rain events on a growth clock


def cardinal_rate(temperature: np.ndarray, cardinal: tuple[float, float, float]) -> np.ndarray:
    """Yan & Hunt's (1999, eq. 4A) development rate: 0 at ``t_min`` and ``t_max``, 1 at ``t_opt``,
    ``((t_max - T) / (t_max - t_opt)) x ((T - t_min) / (t_opt - t_min)) ^ ((t_opt - t_min) /
    (t_max - t_opt))`` in between."""
    low, optimum, high = cardinal
    t = np.asarray(temperature, dtype=float)
    exponent = (optimum - low) / (high - optimum)
    with np.errstate(invalid="ignore"):
        rise = np.clip((t - low) / (optimum - low), 0.0, None) ** exponent
        rate = np.where((t > low) & (t < high), (high - t) / (high - optimum) * rise, 0.0)
    rate[np.isnan(t)] = np.nan
    return rate


def growth_pace(growth: GrowthClock, weather: Weather) -> np.ndarray:
    """The species' daily development pace, ``(cells, days)``: 1 at the reference temperature in
    humid air, above 1 towards the optimum, slower in the cold or in dry air. NaN where an input is
    missing."""
    temperature = growth.temperature
    pace = cardinal_rate(weather.series(temperature.variable), temperature.cardinal_c) / float(
        cardinal_rate(np.array([temperature.reference_c]), temperature.cardinal_c)[0]
    )
    humidity = growth.humidity
    if humidity is not None:
        dryness = series.trapezoid(weather.series(humidity.variable), humidity.trapezoid)
        pace = pace * series.with_floor(dryness, humidity.floor)
    return pace


def _lags(factor: RainEventFactor, growth: GrowthClock | None = None) -> list[int]:
    """Whole-day lags that can score: those the lag response gives any weight to, or on a growth
    clock every calendar day up to its ``max_lag_days``."""
    if growth is not None:
        return list(range(growth.max_lag_days + 1))
    a, _, _, d = factor.response.lag_days
    candidates = np.arange(max(0, math.floor(a)), math.ceil(d) + 1, dtype=float)
    weights = series.trapezoid(candidates, factor.response.lag_days)
    return [int(lag) for lag, w in zip(candidates, weights, strict=True) if w > 0]


def _variable_lookback(variable: str) -> int:
    return ANOMALY_WINDOW_DAYS if variable == "temperature_2m_max_anomaly_30d" else 0


def lookback_days(factor: Factor, growth: GrowthClock | None = None) -> int:
    """How many days before a target day the factor reads (``growth``: the species' clock)."""
    match factor:
        case RainEventFactor():
            return max(_lags(factor, growth)) + factor.input.accumulation_days - 1
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
    blended = np.zeros((len(cells), doy.shape[1]))
    for window in factor.input.windows:
        t = doy
        if window.altitude_shift is not None:
            shift = window.altitude_shift
            t = doy - shift.days_per_100m * (elevation - shift.reference_m) / 100.0
        edges = _unwrapped(window.dates)
        inside = np.maximum.reduce([series.trapezoid(t + k * YEAR_DAYS, edges) for k in (-1, 0, 1)])
        if window.elevation_weight is not None:
            blended = blended + inside * series.trapezoid(elevation, window.elevation_weight)
        else:
            best = np.maximum(best, inside)
    return Evaluated(value=np.maximum(best, blended))


def _habitat(factor: HabitatFactor, cells: Cells, weather: Weather, targets: slice):
    affinity = np.array(
        [factor.input.affinity.get(h, factor.input.default) for h in cells.habitat_names]
    )
    share = cells.habitat_fractions @ affinity
    if factor.response is not None:
        share = series.trapezoid(share, factor.response.trapezoid)
    return Evaluated(value=_static(share, targets, weather))


def _static_band(factor: StaticBandFactor, cells: Cells, weather: Weather, targets: slice):
    attribute = cells.attributes[factor.input.attribute]
    value = series.trapezoid(attribute, factor.response.trapezoid)
    return Evaluated(
        value=_static(series.with_floor(value, factor.floor), targets, weather),
        input=_static(attribute, targets, weather),
    )


def _cumulative(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Running totals of ``values`` and of its missing days, each with a leading 0 column, so the
    days ``(a, b]`` sum to ``total[:, b + 1] - total[:, a + 1]``."""
    zero = np.zeros((values.shape[0], 1))
    missing = np.isnan(values)
    total = np.concatenate([zero, np.cumsum(np.where(missing, 0.0, values), axis=1)], axis=1)
    gaps = np.concatenate([zero, np.cumsum(missing, axis=1, dtype=float)], axis=1)
    return total, gaps


def _rain_event(
    factor: RainEventFactor,
    cells: Cells,
    weather: Weather,
    targets: slice,
    growth: GrowthClock | None = None,
):
    rain = weather.series(factor.input.variable)
    totals = series.rolling(rain, factor.input.accumulation_days, "sum")
    n, days = rain.shape
    index = np.arange(days)[targets]
    shape = (n, len(index))
    if growth is not None:
        grown_total, grown_gaps = _cumulative(growth_pace(growth, weather))
    best = np.full(shape, -1.0)
    best_amount = np.full(shape, -1.0)
    best_lag = np.zeros(shape)
    best_grown = np.full(shape, np.nan)
    # The rain to quote when nothing scores: the wettest inside the lag window, else (on a growth
    # clock, when no rain has grown into the window yet) the wettest within reach.
    wettest = {window: np.full(shape, -1.0) for window in (True, False)}
    wettest_lag = {window: np.zeros(shape) for window in (True, False)}
    wettest_grown = {window: np.full(shape, np.nan) for window in (True, False)}
    missing = np.zeros(shape, dtype=bool)
    # Longest lag first, so a tie goes to the window that ends where the rain ended.
    for lag in sorted(_lags(factor, growth), reverse=True):
        source = index - lag
        amount = np.full(shape, np.nan)
        reachable = source >= 0
        amount[:, reachable] = totals[:, source[reachable]]
        missing |= np.isnan(amount)
        if growth is None:
            grown = np.full(shape, float(lag))
        else:
            # Growth over the days after the rain ended, up to the scored day: (source, index].
            end, start = index[reachable] + 1, source[reachable] + 1
            grown = np.full(shape, np.nan)
            grown[:, reachable] = grown_total[:, end] - grown_total[:, start]
            gap = np.zeros(shape, dtype=bool)
            gap[:, reachable] = grown_gaps[:, end] - grown_gaps[:, start] > 0
            grown[gap] = np.nan
            missing |= np.isnan(grown)
        lag_weight = series.trapezoid(grown, factor.response.lag_days)
        candidate = series.trapezoid(amount, factor.response.amount_mm) * lag_weight
        better = np.nan_to_num(candidate, nan=-1.0) > best
        best = np.where(better, candidate, best)
        best_amount = np.where(better, amount, best_amount)
        best_lag = np.where(better, lag, best_lag)
        best_grown = np.where(better, grown, best_grown)
        in_window = np.nan_to_num(lag_weight) > 0
        for window in (True, False):
            wetter = np.nan_to_num(amount, nan=-1.0) > wettest[window]
            if window:
                wetter &= in_window
            wettest[window] = np.where(wetter, amount, wettest[window])
            wettest_lag[window] = np.where(wetter, lag, wettest_lag[window])
            wettest_grown[window] = np.where(wetter, grown, wettest_grown[window])
    inside = wettest[True] >= 0
    quoted, quoted_lag, quoted_grown = (
        np.where(inside, pick[True], pick[False]) for pick in (wettest, wettest_lag, wettest_grown)
    )
    dry = best <= 0
    value = series.with_floor(np.maximum(best, 0.0), factor.floor)
    reported = np.where(dry, quoted, best_amount)
    lag = np.where(dry, quoted_lag, best_lag)
    grown = np.where(dry, quoted_grown, best_grown)
    value[missing], reported[missing], lag[missing], grown[missing] = (np.nan,) * 4
    return Evaluated(
        value=value, input=reported, days_ago=lag, growth_days=None if growth is None else grown
    )


def _window_aggregate(factor: WindowAggregateFactor, cells: Cells, weather: Weather, targets):
    inp = factor.input
    if inp.aggregate == "percent_of_normal":
        aggregate = series.percent_of_normal(
            weather.series(inp.variable),
            weather.normal(inp.variable),
            inp.window_days,
            inp.offset_days,
        )[:, targets]
    else:
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


def _applied_where(factor: Factor, cells: Cells, result: Evaluated) -> Evaluated:
    """Fade the value towards 1 outside the cells the factor's ``where`` condition covers."""
    if factor.where is None:
        return result
    share = series.trapezoid(cells.attributes[factor.where.attribute], factor.where.trapezoid)
    value = 1.0 - share[:, np.newaxis] * (1.0 - result.value)
    return replace(result, value=value)


def evaluate(
    factor: Factor,
    cells: Cells,
    weather: Weather,
    targets: slice,
    growth: GrowthClock | None = None,
) -> Evaluated:
    """The factor for every cell on the target days ``weather.dates[targets]``; ``growth`` is the
    species' clock, which rain events count their lag in."""
    if getattr(factor.input, "aggregate", None) == "percentile_of_normal":
        raise NotImplementedError(f"{factor.id}: {factor.input.aggregate} needs a climatology")
    if factor.kind == "rain_event":
        result = _rain_event(factor, cells, weather, targets, growth)
    else:
        result = _KINDS[factor.kind](factor, cells, weather, targets)
    return _applied_where(factor, cells, result)
