"""The seasonal outlook: the weeks and months after the 7-day forecast, what past seasons did in
them, and which way the rain leading into them tilts (``.gavin-root/docs/time-views.md``).

It is an outlook, not a forecast: each period says how often the same days were good in past
seasons ("good in 7 of 10 years", never a chance) and whether the rain before it is running wetter
or drier than normal. Observed days and the 7-day forecast come from the weather store against the
reanalysis normals; days beyond come from the long-range forecast against its own climate.
"""

import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Literal

import numpy as np
import pandas as pd

from api.history.config import RainTilt

PeriodKind = Literal["week", "month"]
Tilt = Literal["better", "usual", "worse", "unknown"]


@dataclass(frozen=True)
class Period:
    start: date
    end: date
    kind: PeriodKind


@dataclass(frozen=True)
class Typical:
    share: float | None  # median share of good woodland cell-days over the seasons with scores
    good_years: int  # seasons in which the share reached good_share
    years: int  # seasons with scores for these days


def _clip(start: date, end: date, window: tuple[date, date]) -> tuple[date, date] | None:
    start, end = max(start, window[0]), min(end, window[1])
    return (start, end) if start <= end else None


def outlook_periods(
    today: date,
    forecast_days: int,
    week_starts: list[date],
    month_starts: list[date],
    window: tuple[date, date],
    months_ahead: int,
) -> list[Period]:
    """Weeks starting after the ``forecast_days`` forecast, then up to ``months_ahead`` months
    from the day after the last week, all clipped to the season ``window``. A month already mostly
    behind that day is skipped."""
    boundary = today + timedelta(days=forecast_days)
    periods: list[Period] = []
    for start in sorted(week_starts):
        end = start + timedelta(days=6)
        if start <= boundary:
            continue
        boundary = end
        clipped = _clip(start, end, window)
        if clipped:
            periods.append(Period(*clipped, "week"))

    months = 0
    for first in sorted(month_starts):
        if months >= months_ahead:
            break
        last = first.replace(day=calendar.monthrange(first.year, first.month)[1])
        start = max(first, boundary + timedelta(days=1))
        if (last - start).days + 1 < ((last - first).days + 1) / 2:
            continue
        months += 1
        clipped = _clip(start, last, window)
        if clipped:
            periods.append(Period(*clipped, "month"))
    return periods


def period_starts(
    today: date, week_horizon_days: int, months: int
) -> tuple[list[date], list[date]]:
    """The calendar the outlook is cut from: the Mondays from this week's whose whole week ends
    within ``week_horizon_days`` (the long-range weeks' reach), and the first days of this month and the ``months - 1``
    after it. From the calendar, not from the stored long-range rows, so a missing or partial
    fetch shows as periods without a tendency rather than as no periods at all."""
    monday = today - timedelta(days=today.weekday())
    horizon = today + timedelta(days=week_horizon_days)
    weeks = []
    while monday + timedelta(days=6) <= horizon:
        weeks.append(monday)
        monday += timedelta(days=7)
    firsts, first = [], today.replace(day=1)
    for _ in range(months):
        firsts.append(first)
        first = (first + timedelta(days=32)).replace(day=1)
    return weeks, firsts


def _same_days(day: date, year: int) -> date:
    return day.replace(year=year, day=min(day.day, calendar.monthrange(year, day.month)[1]))


def typical_for_period(
    area_days: pd.DataFrame, period: Period, years: list[int], good_share: float
) -> Typical:
    """How the same calendar days went in each of ``years``: the share of scored woodland
    cell-days that were good, from ``area_days`` (``date, cells, good_cells``) for one area and
    species."""
    frame = area_days.assign(date=pd.to_datetime(area_days["date"]).dt.date)
    shares = []
    for year in years:
        start, end = _same_days(period.start, year), _same_days(period.end, year)
        rows = frame[(frame["date"] >= start) & (frame["date"] <= end)]
        cells = rows["cells"].sum()
        if cells > 0:
            shares.append(rows["good_cells"].sum() / cells)
    if not shares:
        return Typical(share=None, good_years=0, years=0)
    return Typical(
        share=float(np.median(shares)),
        good_years=sum(share >= good_share for share in shares),
        years=len(shares),
    )


def _spread(seasonal: pd.DataFrame, kind: str, after: date | None) -> pd.DataFrame:
    """One row per day of each ``kind`` period: rain and its normal spread evenly over the
    period's days, the temperature anomaly as it is."""
    rows = []
    for (start, end), group in seasonal[seasonal["kind"] == kind].groupby(["start", "end"]):
        start, end = pd.Timestamp(start).date(), pd.Timestamp(end).date()
        days = (end - start).days + 1
        by_variable = group.set_index("variable")
        rain = (
            by_variable.loc["precipitation_sum"]
            if "precipitation_sum" in by_variable.index
            else None
        )
        temperature = (
            by_variable.loc["temperature_2m_mean"]
            if "temperature_2m_mean" in by_variable.index
            else None
        )
        for offset in range(days):
            day = start + timedelta(days=offset)
            if after is not None and day <= after:
                continue
            rows.append(
                {
                    "date": day,
                    "rain": rain["value"] / days if rain is not None else np.nan,
                    "rain_normal": (rain["value"] - rain["anomaly"]) / days
                    if rain is not None
                    else np.nan,
                    "temp_anomaly": temperature["anomaly"] if temperature is not None else np.nan,
                    "source": kind,
                }
            )
    return pd.DataFrame(rows, columns=["date", "rain", "rain_normal", "temp_anomaly", "source"])


def daily_signal(observed: pd.DataFrame, seasonal: pd.DataFrame) -> pd.DataFrame:
    """``date, rain, rain_normal, temp_anomaly, source`` per day: the observed (and 7-day forecast)
    days of one area (``date, precipitation_sum, precipitation_normal, temperature_2m_mean,
    temperature_normal``), then the long-range weeks, then its months, each only where nothing
    more trusted covers the day. ``seasonal`` holds ``kind, start, end, variable, value, anomaly``
    for the same area."""
    frame = observed.assign(date=pd.to_datetime(observed["date"]).dt.date)
    known = pd.DataFrame(
        {
            "date": frame["date"],
            "rain": frame["precipitation_sum"],
            "rain_normal": frame["precipitation_normal"],
            "temp_anomaly": frame["temperature_2m_mean"] - frame["temperature_normal"],
            "source": "observed",
        }
    )
    last = max(known["date"]) if not known.empty else None
    parts = [known]
    for kind in ("week", "month"):
        spread = _spread(seasonal, kind, last)
        covered = set().union(*(set(part["date"]) for part in parts))
        parts.append(spread[~spread["date"].isin(covered)])
    parts = [part for part in parts if not part.empty]
    if not parts:
        return known
    return pd.concat(parts, ignore_index=True).sort_values("date").reset_index(drop=True)


def _window(signal: pd.DataFrame, start: date, end: date) -> pd.DataFrame | None:
    rows = signal[(signal["date"] >= start) & (signal["date"] <= end)]
    return rows if len(rows) == (end - start).days + 1 else None


def rain_share(signal: pd.DataFrame, start: date, end: date) -> float | None:
    """Rain from ``start`` to ``end`` as a percentage of normal, or None unless every day is
    covered."""
    rows = _window(signal, start, end)
    if rows is None or rows["rain"].isna().any() or rows["rain_normal"].isna().any():
        return None
    normal = rows["rain_normal"].sum()
    return float(rows["rain"].sum() / normal * 100) if normal > 0 else None


def rain_totals(signal: pd.DataFrame, start: date, end: date) -> tuple[float, float] | None:
    """Rain and normal rain (mm) from ``start`` to ``end``, or None unless every day is covered."""
    rows = _window(signal, start, end)
    if rows is None or rows["rain"].isna().any() or rows["rain_normal"].isna().any():
        return None
    return float(rows["rain"].sum()), float(rows["rain_normal"].sum())


def mean_temperature_anomaly(signal: pd.DataFrame, start: date, end: date) -> float | None:
    rows = _window(signal, start, end)
    if rows is None or rows["temp_anomaly"].isna().any():
        return None
    return float(rows["temp_anomaly"].mean())


def tilt(share: float | None, rain: RainTilt) -> Tilt:
    if share is None:
        return "unknown"
    if share >= rain.wetter_pct:
        return "better"
    if share <= rain.drier_pct:
        return "worse"
    return "usual"
