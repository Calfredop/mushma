"""Reconstruct a "why this score" factor breakdown from a stored factors-tier row.

The factors Parquet tier (``api.model.store``) keeps each enabled factor's raw 0-1 ``value``, not
its ``contribution`` -- that's cheap to replay from ``value`` plus the rule config, exactly like
``api.model.engine.score_species`` computes it live: a gate's or stopper's contribution is its own
value; a driver's is ``value ** (weight / total_driver_weight)``. The product of every row's
contributions is the row's stored ``score``.
"""

from collections.abc import Mapping

from api.model.rules import Factor
from api.models import FactorBreakdown


def reconstruct_breakdown(
    enabled_factors: list[Factor], row: Mapping[str, float]
) -> list[FactorBreakdown]:
    """``enabled_factors`` in breakdown order (``SpeciesRules.enabled_factors``: gates, drivers,
    stoppers, file order). ``row`` maps each factor's ``id`` to its stored value; raises
    ``KeyError`` if a factor's value wasn't stored."""
    total_weight = sum(f.weight for f in enabled_factors if f.role == "driver")
    breakdown = []
    for f in enabled_factors:
        value = row[f.id]
        contribution = value ** (f.weight / total_weight) if f.role == "driver" else value
        breakdown.append(
            FactorBreakdown(key=f.id, i18n_key=f.i18n_key, value=value, contribution=contribution)
        )
    return breakdown
