"""Which species an area's woodland plausibly holds: the rules' static gates per cell, and the
share of each area's woodland where they reach the plausible fit."""

import numpy as np
import pandas as pd
import pytest
from pydantic import TypeAdapter

from api.history.plausible import area_fit, static_fit
from api.model.arrays import Cells
from api.model.rules import Factor
from tests.live.helpers import factor, ruleset, species_rules

HABITATS = ["beech", "chestnut", "deciduous_oak"]


def _cells(elevations: list[float], fractions: list[list[float]]) -> Cells:
    return Cells(
        ids=np.array([f"c{i}" for i in range(len(elevations))], dtype=object),
        attributes={"elevation_m": np.array(elevations, dtype=float)},
        habitat_names=HABITATS,
        habitat_fractions=np.array(fractions, dtype=float),
    )


def _habitat(affinity: dict[str, float]) -> Factor:
    return TypeAdapter(Factor).validate_python(
        {
            "id": "habitat",
            "role": "gate",
            "i18n_key": "factor.habitat",
            "kind": "habitat",
            "input": {"affinity": affinity, "default": 0.0},
            "confidence": "plausible",
            "source": ["x"],
            "data": "available",
        }
    )


def _altitude(trapezoid: list[float | None]):
    return factor("altitude", "gate", response={"trapezoid": trapezoid})


def _rain() -> Factor:
    """A weather driver: every rule set needs one, and it never enters the fit."""
    return factor(
        "rain",
        "driver",
        weight=1.0,
        kind="window_aggregate",
        input={"variable": "precipitation_sum", "aggregate": "sum", "window_days": 10},
        response={"trapezoid": [100, 200, None, None]},
    )


def _rules():
    return ruleset(
        {
            "porcini_a": species_rules(
                "porcini_a",
                "porcini",
                [
                    _habitat({"beech": 1.0, "chestnut": 0.5}),
                    _altitude([500, 1000, 2000, 2500]),
                    _rain(),
                ],
            ),
            "porcini_b": species_rules(
                "porcini_b",
                "porcini",
                [_habitat({"chestnut": 1.0, "deciduous_oak": 0.8}), _rain()],
            ),
            "ovoli_a": species_rules(
                "ovoli_a",
                "ovoli",
                [
                    _habitat({"deciduous_oak": 1.0}),
                    # A floored band never drops below its floor.
                    factor(
                        "altitude",
                        "gate",
                        response={"trapezoid": [None, None, 400, 800]},
                        floor=0.5,
                    ),
                    _rain(),
                ],
            ),
        },
        {"porcini": ["porcini_a", "porcini_b"], "ovoli": ["ovoli_a"]},
    )


def test_the_fit_multiplies_the_static_gates_of_each_taxon() -> None:
    cells = _cells(
        [1000.0, 750.0, 900.0],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    )

    fits = static_fit(_rules(), cells).set_index(["cell_id", "species"])["fit"]

    assert fits["c0", "porcini_a"] == pytest.approx(1.0)
    assert fits["c1", "porcini_a"] == pytest.approx(0.5 * 0.5)  # chestnut 0.5, half-way up
    assert fits["c2", "porcini_a"] == pytest.approx(0.0)
    assert fits["c2", "porcini_b"] == pytest.approx(0.8)
    assert fits["c2", "ovoli_a"] == pytest.approx(0.5)  # above the band: its floor


def test_a_groups_fit_is_its_best_taxon_like_the_model() -> None:
    cells = _cells([1000.0, 750.0], [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

    fits = static_fit(_rules(), cells).set_index(["cell_id", "species"])["fit"]

    assert fits["c0", "porcini"] == pytest.approx(1.0)  # porcini_a
    assert fits["c1", "porcini"] == pytest.approx(1.0)  # porcini_b on chestnut
    assert set(fits.index.get_level_values("species")) == {
        "porcini_a",
        "porcini_b",
        "ovoli_a",
        "porcini",
        "ovoli",
    }


def test_mixed_woodland_weighs_the_affinity_by_habitat_share() -> None:
    cells = _cells([1500.0], [[0.5, 0.5, 0.0]])

    fits = static_fit(_rules(), cells).set_index(["cell_id", "species"])["fit"]

    assert fits["c0", "porcini_a"] == pytest.approx(0.75)


def test_the_share_counts_the_area_woodland_reaching_the_threshold() -> None:
    fits = pd.DataFrame(
        {
            "cell_id": ["c0", "c1", "c2", "c0", "c1", "c2"],
            "species": ["porcini"] * 3 + ["ovoli"] * 3,
            "fit": [0.9, 0.5, 0.2, 0.0, 0.1, 0.49999999999],
        }
    )
    members = pd.DataFrame(
        {"area_code": ["tuscany"] * 3 + ["A"] * 2, "cell_id": ["c0", "c1", "c2", "c0", "c1"]}
    )

    shares = area_fit(fits, members, 0.5).set_index(["area_code", "species"])

    assert shares.loc[("tuscany", "porcini"), "fit_share"] == pytest.approx(2 / 3)
    assert shares.loc[("A", "porcini"), "fit_share"] == pytest.approx(1.0)
    # Exactly the threshold counts, float noise included.
    assert shares.loc[("tuscany", "ovoli"), "fit_share"] == pytest.approx(1 / 3)
    assert shares.loc[("A", "ovoli"), "fit_share"] == pytest.approx(0.0)
    assert shares.loc[("A", "ovoli"), "cells"] == 2


def test_a_cell_without_a_fit_counts_as_not_plausible() -> None:
    fits = pd.DataFrame(
        {"cell_id": ["c0", "c1"], "species": ["porcini", "porcini"], "fit": [0.9, np.nan]}
    )
    members = pd.DataFrame({"area_code": ["A", "A"], "cell_id": ["c0", "c1"]})

    shares = area_fit(fits, members, 0.5)

    assert shares["fit_share"].tolist() == pytest.approx([0.5])
