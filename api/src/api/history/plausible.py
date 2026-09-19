"""Which species an area's woodland can plausibly hold, weather aside.

A cell's **fit** for a taxon is the product of its rule set's static gates, habitat affinity and
the attribute bands such as altitude: the backtest's ``static`` baseline (``api.model.backtest``).
A group's fit is its best taxon's, as the model's group score is. An area's **fit share** is the
share of its woodland cells whose fit reaches ``plausible_fit`` (``config/history.yaml``).
"""

import numpy as np
import pandas as pd

from api.model.arrays import Cells, Weather
from api.model.factors import evaluate
from api.model.rules import RuleSet

STATIC_KINDS = {"habitat", "static_band"}
# Static gates read no weather, but the evaluator shapes its output by the weather's days: one
# empty day stands in for them.
_NO_WEATHER = Weather(dates=np.array(["2001-01-01"], dtype="datetime64[D]"), values={})
# The habitat mix is a weighted sum of fractions, so an exact threshold can land a hair below it.
_TOLERANCE = 1e-9


def static_fit(rules: RuleSet, cells: Cells) -> pd.DataFrame:
    """``cell_id, species, fit``: for every cell, each taxon key's static gates multiplied, and
    each group's best key."""
    by_key: dict[str, np.ndarray] = {}
    for key, spec in rules.species.items():
        fit = np.ones(len(cells))
        for factor in spec.enabled_factors:
            if factor.role == "gate" and factor.kind in STATIC_KINDS:
                fit = fit * evaluate(factor, cells, _NO_WEATHER, slice(0, 1)).value[:, 0]
        by_key[key] = fit
    by_group = {
        group: np.fmax.reduce([by_key[key] for key in keys]) for group, keys in rules.groups.items()
    }
    return pd.concat(
        [
            pd.DataFrame({"cell_id": cells.ids, "species": species, "fit": fit})
            for species, fit in {**by_key, **by_group}.items()
        ],
        ignore_index=True,
    )


def area_fit(fits: pd.DataFrame, members: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """``area_code, species, cells, fit_share`` from :func:`static_fit` and the area members
    (``area_code, cell_id``). A cell without a fit (an attribute unknown) is not plausible."""
    joined = members[["area_code", "cell_id"]].merge(fits, on="cell_id", how="inner")
    joined = joined.assign(plausible=(joined["fit"] >= threshold - _TOLERANCE).astype(float))
    out = joined.groupby(["area_code", "species"], as_index=False).agg(
        cells=("cell_id", "count"), fit_share=("plausible", "mean")
    )
    return out.astype({"cells": int}).sort_values(["area_code", "species"], ignore_index=True)
