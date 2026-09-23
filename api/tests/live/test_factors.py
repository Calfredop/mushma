"""LiveRepository.get_factors (analysis mode): every factor's 0-1 value per woodland cell, from the
rule file that wins the cell that day -- the one "why this score" explains."""

from datetime import timedelta
from pathlib import Path

import pytest

from api.live.repository import LiveRepository
from api.model.rules import RuleSet
from api.repository import DateOutOfRange
from api.timeutil import today_rome
from tests.live.helpers import (
    CELL_A,
    CELL_B,
    CELL_C,
    CELL_D_NON_WOODLAND,
    factor,
    ruleset,
    species_rules,
    write_cells,
    write_daily,
    write_factors,
)

DAY = today_rome()
NEXT_DAY = DAY + timedelta(days=1)
UNFACTORED_DAY = DAY - timedelta(days=200)  # scored, like history, without the factors tier

A, B, C, D = (c["cell_id"] for c in (CELL_A, CELL_B, CELL_C, CELL_D_NON_WOODLAND))


def _rules() -> RuleSet:
    return ruleset(
        {
            # File order puts the driver first; the breakdown (and the chips) put gates first.
            "porcini_a": species_rules(
                "porcini_a",
                "porcini",
                [
                    factor("rain_a", "driver", weight=1.0),
                    factor("season", "gate"),
                    factor("frost", "stopper"),
                    factor("retired", "stopper", enabled=False, notes="switched off"),
                ],
            ),
            "porcini_b": species_rules(
                "porcini_b",
                "porcini",
                [
                    factor("season", "gate"),
                    factor("rain_b", "driver", weight=1.0),
                    factor("cold", "stopper", i18n_key="factor.frost"),
                    factor("frost", "stopper"),
                ],
            ),
            "ovoli_a": species_rules("ovoli_a", "ovoli", [factor("warmth", "driver", weight=1.0)]),
        },
        groups={"porcini": ["porcini_a", "porcini_b"], "ovoli": ["ovoli_a"]},
    )


def _build(root: Path) -> RuleSet:
    write_cells(root, [CELL_A, CELL_B, CELL_C, CELL_D_NON_WOODLAND])
    # A is won by porcini_a, B by porcini_b; C has no weather that day (no row); D isn't woodland.
    write_daily(
        root,
        "porcini",
        [
            {"cell_id": A, "date": DAY, "score": 0.5, "source_key": "porcini_a"},
            {"cell_id": B, "date": DAY, "score": 0.6, "source_key": "porcini_b"},
            {"cell_id": D, "date": DAY, "score": 0.4, "source_key": "porcini_a"},
            {"cell_id": A, "date": NEXT_DAY, "score": 0.7, "source_key": "porcini_b"},
            {"cell_id": A, "date": UNFACTORED_DAY, "score": 0.3, "source_key": "porcini_a"},
        ],
    )
    # Both members are scored everywhere, winner or not; only the winner's values may show.
    write_factors(
        root,
        "porcini_a",
        [
            {
                "cell_id": A,
                "date": DAY,
                "season": 1.0,
                "rain_a": 0.123456,
                "frost": 0.9,
                "rain_a__input": 31.5,
            },
            {"cell_id": B, "date": DAY, "season": 1.0, "rain_a": 0.2, "frost": 0.3},
            {"cell_id": D, "date": DAY, "season": 1.0, "rain_a": 0.4, "frost": 1.0},
            {"cell_id": A, "date": NEXT_DAY, "season": 1.0, "rain_a": 0.1, "frost": 1.0},
        ],
    )
    write_factors(
        root,
        "porcini_b",
        [
            {"cell_id": A, "date": DAY, "season": 0.8, "rain_b": 0.7, "cold": 0.1, "frost": 0.6},
            {"cell_id": B, "date": DAY, "season": 1.0, "rain_b": 0.6, "cold": 0.4, "frost": 0.95},
            {
                "cell_id": A,
                "date": NEXT_DAY,
                "season": 1.0,
                "rain_b": 0.75,
                "cold": 1.0,
                "frost": 0.5,
            },
        ],
    )
    return _rules()


@pytest.fixture
def repo(tmp_path: Path) -> LiveRepository:
    return LiveRepository(tmp_path, rules=_build(tmp_path))


def _values(response) -> dict[str, dict[str, float | None]]:
    ids = [chip.id for chip in response.factors]
    return {cell.cell_id: dict(zip(ids, cell.values, strict=True)) for cell in response.cells}


class TestChips:
    def test_the_union_of_the_groups_enabled_factors_in_breakdown_order(
        self, repo: LiveRepository
    ) -> None:
        response = repo.get_factors("porcini", DAY)
        assert [chip.id for chip in response.factors] == [
            "season",
            "rain_a",
            "rain_b",
            "frost",
            "cold",
        ]
        roles = {chip.id: chip.role for chip in response.factors}
        assert roles == {
            "season": "gate",
            "rain_a": "driver",
            "rain_b": "driver",
            "frost": "stopper",
            "cold": "stopper",
        }

    def test_chips_carry_the_i18n_key_the_breakdown_names_them_by(
        self, repo: LiveRepository
    ) -> None:
        chips = {chip.id: chip.i18n_key for chip in repo.get_factors("porcini", DAY).factors}
        assert chips["cold"] == "factor.frost"
        assert chips["rain_a"] == "factor.rain_a"

    def test_a_group_of_one_rule_file_lists_its_own_factors(
        self, tmp_path: Path, repo: LiveRepository
    ) -> None:
        write_daily(
            tmp_path, "ovoli", [{"cell_id": A, "date": DAY, "score": 0.2, "source_key": "ovoli_a"}]
        )
        write_factors(tmp_path, "ovoli_a", [{"cell_id": A, "date": DAY, "warmth": 0.2}])
        response = repo.get_factors("ovoli", DAY)
        assert [chip.id for chip in response.factors] == ["warmth"]
        assert _values(response) == {A: {"warmth": pytest.approx(0.2)}}


class TestCellValues:
    def test_each_cell_takes_its_values_from_the_rule_file_that_wins_it(
        self, repo: LiveRepository
    ) -> None:
        values = _values(repo.get_factors("porcini", DAY))
        assert values[A]["rain_a"] == pytest.approx(0.123)
        assert values[A]["frost"] == pytest.approx(0.9)  # porcini_a's, not porcini_b's 0.6
        assert values[B]["season"] == pytest.approx(1.0)
        assert values[B]["rain_b"] == pytest.approx(0.6)
        assert values[B]["frost"] == pytest.approx(0.95)  # porcini_b's, not porcini_a's 0.3
        assert values[B]["cold"] == pytest.approx(0.4)

    def test_a_factor_the_winner_lacks_is_null(self, repo: LiveRepository) -> None:
        values = _values(repo.get_factors("porcini", DAY))
        assert values[A]["rain_b"] is None
        assert values[A]["cold"] is None
        assert values[B]["rain_a"] is None

    def test_the_winner_is_that_days_winner(self, repo: LiveRepository) -> None:
        values = _values(repo.get_factors("porcini", NEXT_DAY))
        assert values == {
            A: {"season": 1.0, "rain_a": None, "rain_b": 0.75, "frost": 0.5, "cold": 1.0}
        }

    def test_only_woodland_cells_scored_that_day_with_their_centre(
        self, repo: LiveRepository
    ) -> None:
        response = repo.get_factors("porcini", DAY)
        assert response.species == "porcini"
        assert response.date == DAY
        assert {cell.cell_id for cell in response.cells} == {A, B}
        by_id = {cell.cell_id: cell for cell in response.cells}
        assert (by_id[A].lon, by_id[A].lat) == (pytest.approx(10.0), pytest.approx(43.0))

    def test_values_are_rounded_to_three_decimals(self, repo: LiveRepository) -> None:
        cell = next(c for c in repo.get_factors("porcini", DAY).cells if c.cell_id == A)
        assert 0.123 in cell.values


class TestNoFactorRows:
    def test_a_day_scored_without_factors_raises_with_the_stored_range(
        self, repo: LiveRepository
    ) -> None:
        with pytest.raises(DateOutOfRange) as caught:
            repo.get_factors("porcini", UNFACTORED_DAY)
        assert (caught.value.available_from, caught.value.available_to) == (DAY, NEXT_DAY)

    def test_a_day_never_scored_raises_too(self, repo: LiveRepository) -> None:
        with pytest.raises(DateOutOfRange):
            repo.get_factors("porcini", DAY + timedelta(days=30))

    def test_a_group_with_nothing_stored_raises(self, repo: LiveRepository) -> None:
        with pytest.raises(DateOutOfRange):
            repo.get_factors("ovoli", DAY)
