"""api.live.breakdown replays api.model.engine.score_species's contribution formula from a
stored factors-tier row, since the row only keeps each factor's raw `value`."""

import pytest
from pydantic import TypeAdapter

from api.live.breakdown import reconstruct_breakdown
from api.model.rules import Factor

_FACTOR = TypeAdapter(Factor)
COMMON = {
    "i18n_key": "factor.test",
    "confidence": "plausible",
    "source": ["x"],
    "data": "available",
}


def factor(**fields):
    return _FACTOR.validate_python({**COMMON, "id": fields.get("kind", "f"), **fields})


def gate(id: str = "season_window", **overrides) -> Factor:
    return factor(
        id=id,
        role="gate",
        kind="season_window",
        input={"windows": [{"label": "main", "dates": ["01-06", "15-06", "01-09", "15-09"]}]},
        **overrides,
    )


def driver(id: str, weight: float, **overrides) -> Factor:
    return factor(
        id=id,
        role="driver",
        weight=weight,
        kind="static_band",
        input={"attribute": "elevation_m"},
        response={"trapezoid": [0, 1, 2, 3]},
        **overrides,
    )


def stopper(id: str = "drying_wind", **overrides) -> Factor:
    return factor(
        id=id,
        role="stopper",
        kind="count_days",
        input={
            "variable": "wind_speed_10m_max",
            "window_days": 3,
            "offset_days": 0,
            "op": "gt",
            "threshold": 10,
        },
        response={"trapezoid": [0, 1, 2, 3]},
        **overrides,
    )


class TestReconstructBreakdown:
    def test_a_single_driver_keeps_its_own_value_as_contribution(self) -> None:
        factors = [driver("rain_trigger", weight=1.0)]
        row = {"rain_trigger": 0.8}
        breakdown = reconstruct_breakdown(factors, row)
        assert len(breakdown) == 1
        assert breakdown[0].key == "rain_trigger"
        assert breakdown[0].value == pytest.approx(0.8)
        assert breakdown[0].contribution == pytest.approx(0.8)

    def test_gates_and_stoppers_pass_their_value_through_unweighted(self) -> None:
        factors = [gate(), stopper()]
        row = {"season_window": 1.0, "drying_wind": 0.5}
        breakdown = reconstruct_breakdown(factors, row)
        by_key = {b.key: b for b in breakdown}
        assert by_key["season_window"].contribution == pytest.approx(1.0)
        assert by_key["drying_wind"].contribution == pytest.approx(0.5)

    def test_drivers_split_the_score_by_weight_share(self) -> None:
        factors = [driver("a", weight=1.0), driver("b", weight=3.0)]
        row = {"a": 0.5, "b": 0.5}
        breakdown = reconstruct_breakdown(factors, row)
        by_key = {b.key: b for b in breakdown}
        assert by_key["a"].contribution == pytest.approx(0.5 ** (1 / 4))
        assert by_key["b"].contribution == pytest.approx(0.5 ** (3 / 4))

    def test_product_of_contributions_equals_the_score_the_engine_would_give(self) -> None:
        factors = [gate(), driver("a", weight=1.0), driver("b", weight=1.0), stopper()]
        row = {"season_window": 1.0, "a": 0.9, "b": 0.4, "drying_wind": 0.7}
        breakdown = reconstruct_breakdown(factors, row)
        score = 1.0
        for b in breakdown:
            score *= b.contribution
        expected = 1.0 * (0.9**0.5) * (0.4**0.5) * 0.7
        assert score == pytest.approx(expected)

    def test_breakdown_order_matches_enabled_factors_order(self) -> None:
        factors = [gate(), driver("a", weight=1.0), stopper()]
        row = {"season_window": 1.0, "a": 0.6, "drying_wind": 1.0}
        breakdown = reconstruct_breakdown(factors, row)
        assert [b.key for b in breakdown] == ["season_window", "a", "drying_wind"]

    def test_a_missing_value_raises(self) -> None:
        factors = [driver("rain_trigger", weight=1.0)]
        with pytest.raises(KeyError):
            reconstruct_breakdown(factors, {})
