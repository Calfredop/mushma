"""Weather normals: the mean of each calendar day over a baseline of complete years, per weather
point and variable, smoothed with a centred window so ten years give a stable curve.

Days of the year run 1-365; 29 February counts as 28 February (``api.model.series.day_of_year``),
so a leap year gives that day two values. The window wraps around the new year: the normal for
1 January also looks at late December.
"""

from collections.abc import Iterable
from datetime import date

import numpy as np
import pandas as pd

from api.model.series import day_of_year

DAYS = 365


def _days_in_year(year: int) -> int:
    return (date(year + 1, 1, 1) - date(year, 1, 1)).days


def complete_years(
    rows: pd.DataFrame, points: Iterable[str], variables: Iterable[str]
) -> list[int]:
    """Years in which every one of ``points`` has a value for every day and ``variables``.

    ``rows`` holds ``point_id, date, variable, value`` (nulls already dropped, as the weather store
    keeps them)."""
    points, variables = set(points), set(variables)
    if rows.empty or not points or not variables:
        return []
    kept = rows[rows["point_id"].isin(points) & rows["variable"].isin(variables)]
    years = pd.to_datetime(kept["date"]).dt.year
    counts = kept.assign(year=years).groupby("year").size()
    return sorted(
        int(year)
        for year, count in counts.items()
        if count == _days_in_year(int(year)) * len(points) * len(variables)
    )


def _circular_mean(values: np.ndarray, window_days: int) -> np.ndarray:
    """Centred moving mean over ``window_days`` of a 365-day cycle, wrapping at the ends."""
    half = window_days // 2
    padded = np.concatenate([values[-half:], values, values[:half]]) if half else values
    kernel = np.ones(window_days) / window_days
    return np.convolve(padded, kernel, mode="valid")


def daily_normals(rows: pd.DataFrame, years: list[int], window_days: int = 31) -> pd.DataFrame:
    """``point_id, variable, doy, normal, years`` for every point and variable in ``rows``.

    ``rows`` holds ``point_id, date, variable, value`` from one source. Only ``years`` count; a
    calendar day's normal is the mean of its values over them, then smoothed with a centred
    ``window_days`` window (odd, so it has a centre). ``years`` is how many years contributed."""
    if window_days < 1 or window_days % 2 == 0:
        raise ValueError(f"window_days must be odd and positive, got {window_days}")
    dates = pd.to_datetime(rows["date"])
    kept = rows[dates.dt.year.isin(years)].copy()
    kept["year"] = dates[kept.index].dt.year
    kept["doy"] = day_of_year(dates[kept.index].to_numpy().astype("datetime64[D]"))

    frames = []
    for (point_id, variable), group in kept.groupby(["point_id", "variable"], sort=True):
        by_day = group.groupby("doy")["value"].mean().reindex(np.arange(1, DAYS + 1))
        frames.append(
            pd.DataFrame(
                {
                    "point_id": point_id,
                    "variable": variable,
                    "doy": np.arange(1, DAYS + 1),
                    "normal": _circular_mean(by_day.to_numpy(dtype=float), window_days),
                    "years": int(group["year"].nunique()),
                }
            )
        )
    if not frames:
        return pd.DataFrame(columns=["point_id", "variable", "doy", "normal", "years"])
    return pd.concat(frames, ignore_index=True)
