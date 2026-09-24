"""Reconstruct a "why this score" factor breakdown from a stored factors-tier row.

The factors Parquet tier (``api.model.store``) keeps each enabled factor's raw 0-1 ``value``, not
its ``contribution`` -- that's cheap to replay from ``value`` plus the rule config, exactly like
``api.model.engine.score_species`` computes it live: a gate's or stopper's contribution is its own
value; a driver's is ``value ** (weight / total_driver_weight)``. The product of every row's
contributions is the row's stored ``score``.

The row also keeps, per factor, the measurement behind the value (``<factor>__input``, and for rain
events ``<factor>__days_ago`` and, on a growth clock, ``<factor>__growth_days``). Those columns are
absent for days scored without them, so they read as ``None`` rather than raising. What the rule
wanted of the measurement comes from the rule config.
"""

from collections.abc import Mapping
from functools import cache

import pandas as pd

from api.grid.habitats import load_vocabulary
from api.model.rules import (
    ATTRIBUTE_UNITS,
    DERIVED_UNITS,
    CountDaysFactor,
    DaysSinceFactor,
    Factor,
    GrowthClock,
    HabitatFactor,
    RainEventFactor,
    StaticBandFactor,
    WindowAggregateFactor,
)
from api.models import FactorBreakdown, FactorRule, FactorWhere
from api.weather.config import load_weather_config


@cache
def _weather_units() -> dict[str, str]:
    return {name: v.unit for name, v in load_weather_config().variables.items()}


@cache
def _habitats() -> list[str]:
    return load_vocabulary().habitats


def _variable_unit(variable: str) -> str:
    if variable in ATTRIBUTE_UNITS:
        return ATTRIBUTE_UNITS[variable]
    if variable in DERIVED_UNITS:
        return DERIVED_UNITS[variable]
    return _weather_units()[variable]


def _describe(factor: Factor, growth: GrowthClock | None = None) -> FactorRule:
    """What the rule wants of the measurement it reads, and where it applies."""
    rule = _describe_measurement(factor, growth)
    if factor.where is None:
        return rule
    where = FactorWhere(
        variable=factor.where.attribute,
        variable_unit=_variable_unit(factor.where.attribute),
        trapezoid=list(factor.where.trapezoid),
    )
    return rule.model_copy(update={"where": where})


def _describe_measurement(factor: Factor, growth: GrowthClock | None) -> FactorRule:
    match factor:
        case StaticBandFactor():
            return FactorRule(
                kind=factor.kind,
                variable=factor.input.attribute,
                variable_unit=_variable_unit(factor.input.attribute),
                trapezoid=factor.response.trapezoid,
            )
        case RainEventFactor():
            return FactorRule(
                kind=factor.kind,
                variable=factor.input.variable,
                variable_unit=_variable_unit(factor.input.variable),
                window_days=factor.input.accumulation_days,
                trapezoid=factor.response.amount_mm,
                lag_days=factor.response.lag_days,
                lag_unit="days" if growth is None else "growth_days",
            )
        case WindowAggregateFactor():
            return FactorRule(
                kind=factor.kind,
                variable=factor.input.variable,
                variable_unit=_variable_unit(factor.input.variable),
                aggregate=factor.input.aggregate,
                window_days=factor.input.window_days,
                offset_days=factor.input.offset_days,
                trapezoid=factor.response.trapezoid,
            )
        case CountDaysFactor():
            return FactorRule(
                kind=factor.kind,
                variable=factor.input.variable,
                variable_unit=_variable_unit(factor.input.variable),
                window_days=factor.input.window_days,
                offset_days=factor.input.offset_days,
                op=factor.input.op,
                threshold=factor.input.threshold,
                trapezoid=factor.response.trapezoid,
            )
        case DaysSinceFactor():
            return FactorRule(
                kind=factor.kind,
                variable=factor.input.variable,
                variable_unit=_variable_unit(factor.input.variable),
                window_days=factor.input.max_lookback_days,
                op=factor.input.op,
                threshold=factor.input.threshold,
                trapezoid=factor.response.trapezoid,
            )
        case HabitatFactor():
            fit = factor.input.affinity
            return FactorRule(
                kind=factor.kind,
                affinity={h: fit.get(h, factor.input.default) for h in _habitats()},
            )
        case _:
            return FactorRule(kind=factor.kind)


def _measured(row: Mapping[str, object], column: str) -> float | None:
    value = row.get(column)
    return None if value is None or pd.isna(value) else float(value)


def reconstruct_breakdown(
    enabled_factors: list[Factor],
    row: Mapping[str, object],
    growth: GrowthClock | None = None,
) -> list[FactorBreakdown]:
    """``enabled_factors`` in breakdown order (``SpeciesRules.enabled_factors``: gates, drivers,
    stoppers, file order). ``row`` maps each factor's ``id`` to its stored value, and may carry the
    ``<id>__input``, ``<id>__days_ago`` and ``<id>__growth_days`` measurements; ``growth`` is the
    species' clock (``SpeciesRules.clock``). Raises ``KeyError`` if a factor's value wasn't
    stored."""
    total_weight = sum(f.weight for f in enabled_factors if f.role == "driver")
    breakdown = []
    for f in enabled_factors:
        value = float(row[f.id])
        contribution = value ** (f.weight / total_weight) if f.role == "driver" else value
        rule = _describe(f, growth)
        measured = _measured(row, f"{f.id}__input")
        days_ago = _measured(row, f"{f.id}__days_ago")
        grown = _measured(row, f"{f.id}__growth_days")
        breakdown.append(
            FactorBreakdown(
                key=f.id,
                i18n_key=f.i18n_key,
                value=value,
                contribution=contribution,
                role=f.role,
                weight=f.weight,
                # Stored as float32: two decimals is all the pipeline kept on purpose.
                input=None if measured is None else round(measured, 2),
                unit=rule.input_unit,
                days_ago=None if days_ago is None else int(days_ago),
                growth_days=None if grown is None else round(grown, 1),
                rule=rule,
            )
        )
    return breakdown
