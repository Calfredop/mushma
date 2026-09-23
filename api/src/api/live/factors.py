"""Analysis mode (``GET /factors``): every factor behind a group's score, per cell, for one day.

A cell's values come from the rule file that wins it that day (the group row's ``source_key``),
the same one "why this score" explains, so a factor that file lacks is null rather than borrowed
from a losing taxon.
"""

import pandas as pd

from api.model.rules import ROLE_ORDER, RuleSet
from api.models import FactorChip

VALUE_DECIMALS = 3  # a map opacity needs far less; keeps the whole region near 0.25 MB gzipped


def factor_chips(rules: RuleSet, group: str) -> list[FactorChip]:
    """The union of the enabled factors over the group's rule files, in breakdown order: gates,
    drivers, stoppers, each in the order the files first list them (tie-break order)."""
    chips: dict[str, FactorChip] = {}
    for key in rules.groups[group]:
        for f in rules.species[key].enabled_factors:
            chips.setdefault(f.id, FactorChip(id=f.id, i18n_key=f.i18n_key, role=f.role))
    return sorted(chips.values(), key=lambda chip: ROLE_ORDER.index(chip.role))


def winner_values(
    winners: pd.DataFrame, factor_rows: dict[str, pd.DataFrame], chips: list[FactorChip]
) -> pd.DataFrame:
    """``winners``: one row per cell with its ``source_key``. ``factor_rows``: each rule file's
    factor rows for the day (``cell_id`` plus a column per factor it has). Returns ``winners`` with
    a column per chip, holding the winner's value or NaN where the winner lacks it."""
    ids = [chip.id for chip in chips]
    frames = []
    for key, rows in factor_rows.items():
        frame = rows.reindex(columns=["cell_id", *ids])
        frame["source_key"] = key
        frames.append(frame)
    if not frames:
        return winners.reindex(columns=[*winners.columns, *ids])
    values = pd.concat(frames, ignore_index=True)
    values[ids] = values[ids].astype(float).round(VALUE_DECIMALS)
    return winners.merge(values, on=["cell_id", "source_key"], how="left")
