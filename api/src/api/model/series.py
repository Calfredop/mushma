"""Array helpers the factors are built from.

Every daily array is ``(cells, days)`` over consecutive days, float, with NaN for "no data". A
window that reaches before the first day, or holds a missing day, gives NaN: the engine never
scores on partial weather.
"""

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from api.model.rules import Trapezoid

# Cumulative days before each month in a non-leap year.
_MONTH_START = np.array([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])


def trapezoid(x: np.ndarray, t: Trapezoid) -> np.ndarray:
    """``[zero_below, full_from, full_to, zero_above]``: 0 outside, linear ramps, 1 on the plateau.

    A null pair leaves that side open. A zero-width ramp is a step that includes its edge
    (``[null, null, 0, 0]`` is 1 at 0 and 0 above).
    """
    a, b, c, d = t
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    with np.errstate(invalid="ignore"):
        if a is not None and b is not None:
            lower = np.clip((x - a) / (b - a), 0, 1) if b > a else (x >= b).astype(float)
            out = np.minimum(out, lower)
        if c is not None and d is not None:
            upper = np.clip((d - x) / (d - c), 0, 1) if d > c else (x <= c).astype(float)
            out = np.minimum(out, upper)
    out[np.isnan(x)] = np.nan
    return out


def with_floor(raw: np.ndarray, floor: float | None) -> np.ndarray:
    """Lift a 0-1 response so it never goes below ``floor``: ``floor + (1 - floor) * raw``."""
    if floor is None:
        return raw
    return floor + (1.0 - floor) * raw


def _window_sums(values: np.ndarray, window: int, offset: int) -> tuple[np.ndarray, np.ndarray]:
    """Sum of the window ending ``offset`` days before each day, and its count of missing days
    (the whole window counts as missing where it reaches before the first day)."""
    n, days = values.shape
    missing = np.isnan(values)
    zero_col = np.zeros((n, 1))
    total = np.concatenate([zero_col, np.cumsum(np.where(missing, 0.0, values), axis=1)], axis=1)
    gaps = np.concatenate([zero_col, np.cumsum(missing, axis=1, dtype=float)], axis=1)
    end = np.arange(days) - offset + 1  # exclusive end index into the cumulative arrays
    start = end - window
    ok = start >= 0
    sums = np.full((n, days), np.nan)
    gap_counts = np.full((n, days), float(window))
    sums[:, ok] = total[:, end[ok]] - total[:, start[ok]]
    gap_counts[:, ok] = gaps[:, end[ok]] - gaps[:, start[ok]]
    return sums, gap_counts


def rolling(values: np.ndarray, window: int, how: str, offset: int = 0) -> np.ndarray:
    """``how`` (sum, mean, min, max) over the ``window`` days ending ``offset`` days before each
    day, the day itself included when ``offset`` is 0."""
    if how in ("sum", "mean"):
        sums, gaps = _window_sums(values, window, offset)
        out = sums / window if how == "mean" else sums
        out[gaps > 0] = np.nan
        return out
    reducer = {"min": np.min, "max": np.max}[how]
    n, days = values.shape
    padded = np.concatenate([np.full((n, window + offset - 1), np.nan), values], axis=1)
    return reducer(sliding_window_view(padded, window, axis=1)[:, :days], axis=2)


_OPS = {"lt": np.less, "lte": np.less_equal, "gt": np.greater, "gte": np.greater_equal}


def _matches(values: np.ndarray, op: str, threshold: float) -> np.ndarray:
    with np.errstate(invalid="ignore"):
        return _OPS[op](values, threshold)


def count_days(
    values: np.ndarray, op: str, threshold: float, window: int, offset: int = 0
) -> np.ndarray:
    """Number of days in the window where ``values op threshold``."""
    flags = np.where(np.isnan(values), np.nan, _matches(values, op, threshold).astype(float))
    return rolling(flags, window, "sum", offset)


def days_since(values: np.ndarray, op: str, threshold: float, max_lookback: int) -> np.ndarray:
    """Days since the latest day (the day itself included) where ``values op threshold``, capped
    at ``max_lookback`` when no day within reach matches."""
    n, days = values.shape
    positions = np.broadcast_to(np.arange(days, dtype=float), (n, days))
    last = np.maximum.accumulate(
        np.where(_matches(values, op, threshold), positions, -np.inf), axis=1
    )
    out = np.minimum(positions - last, float(max_lookback))
    _, gaps = _window_sums(np.where(np.isnan(values), np.nan, 0.0), max_lookback + 1, 0)
    out[gaps > 0] = np.nan
    return out


def lagged_anomaly(values: np.ndarray, window: int) -> np.ndarray:
    """Each day minus the mean of the ``window`` days before it."""
    return values - rolling(values, window, "mean", offset=1)


def day_of_year(dates: np.ndarray) -> np.ndarray:
    """Day of a non-leap year (1-365) for ``datetime64[D]`` dates; 29 February counts as 28."""
    dates = np.asarray(dates, dtype="datetime64[D]")
    months = dates.astype("datetime64[M]")
    month = months.astype(int) % 12
    day = (dates - months).astype(int) + 1
    leap_day = (month == 1) & (day == 29)
    return _MONTH_START[month] + np.where(leap_day, 28, day)
