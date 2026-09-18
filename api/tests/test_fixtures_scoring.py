import math
from datetime import date

import pytest

from api.fixtures.scoring import (
    FactorSpec,
    combine_factors,
    season_gate,
    trapezoid,
)


class TestTrapezoid:
    def test_full_trapezoid_shape(self) -> None:
        params = (10.0, 20.0, 30.0, 40.0)
        assert trapezoid(5.0, params) == 0.0
        assert trapezoid(10.0, params) == 0.0
        assert trapezoid(15.0, params) == pytest.approx(0.5)
        assert trapezoid(20.0, params) == 1.0
        assert trapezoid(25.0, params) == 1.0
        assert trapezoid(30.0, params) == 1.0
        assert trapezoid(35.0, params) == pytest.approx(0.5)
        assert trapezoid(40.0, params) == 0.0
        assert trapezoid(50.0, params) == 0.0

    def test_open_below_is_full_until_the_upper_ramp(self) -> None:
        # e.g. rain_event amount_mm response [10, 30, null, null]
        params = (10.0, 30.0, None, None)
        assert trapezoid(0.0, params) == 0.0
        assert trapezoid(20.0, params) == pytest.approx(0.5)
        assert trapezoid(100.0, params) == 1.0

    def test_open_above_is_full_from_the_lower_ramp(self) -> None:
        # e.g. a stopper response [null, null, 1, 3]
        params = (None, None, 1.0, 3.0)
        assert trapezoid(0.0, params) == 1.0
        assert trapezoid(1.0, params) == 1.0
        assert trapezoid(2.0, params) == pytest.approx(0.5)
        assert trapezoid(3.0, params) == 0.0

    def test_fully_open_is_always_one(self) -> None:
        assert trapezoid(-1000.0, (None, None, None, None)) == 1.0
        assert trapezoid(1000.0, (None, None, None, None)) == 1.0


class TestSeasonGate:
    def test_porcini_in_season_in_september(self) -> None:
        assert season_gate("porcini", date(2026, 9, 15)) == pytest.approx(1.0)

    def test_porcini_out_of_season_in_february(self) -> None:
        assert season_gate("porcini", date(2026, 2, 1)) == 0.0

    def test_ovoli_shorter_season_than_gallinacci(self) -> None:
        # ovoli (Jul-Oct) is out of season in late November while gallinacci (Jun-Nov) still is
        target = date(2026, 11, 25)
        assert season_gate("ovoli", target) == 0.0
        assert season_gate("gallinacci", target) > 0.0


class TestCombineFactors:
    def test_product_of_contributions_equals_the_score(self) -> None:
        specs = [
            FactorSpec(id="season", role="gate", i18n_key="factor.season"),
            FactorSpec(id="habitat", role="gate", i18n_key="factor.habitat"),
            FactorSpec(
                id="rain_trigger", role="driver", i18n_key="factor.rain_trigger", weight=2.0
            ),
            FactorSpec(
                id="air_temperature", role="driver", i18n_key="factor.air_temperature", weight=1.0
            ),
            FactorSpec(id="frost", role="stopper", i18n_key="factor.frost"),
        ]
        values = {
            "season": 1.0,
            "habitat": 0.8,
            "rain_trigger": 0.6,
            "air_temperature": 0.4,
            "frost": 0.9,
        }
        score, results = combine_factors(specs, values)
        assert score == pytest.approx(math.prod(r.contribution for r in results))
        assert 0.0 <= score <= 1.0

    def test_result_order_matches_spec_order(self) -> None:
        specs = [
            FactorSpec(id="a", role="gate", i18n_key="factor.a"),
            FactorSpec(id="b", role="driver", i18n_key="factor.b", weight=1.0),
            FactorSpec(id="c", role="stopper", i18n_key="factor.c"),
        ]
        values = {"a": 1.0, "b": 1.0, "c": 1.0}
        _, results = combine_factors(specs, values)
        assert [r.key for r in results] == ["a", "b", "c"]

    def test_a_zero_gate_zeroes_the_whole_score(self) -> None:
        specs = [
            FactorSpec(id="season", role="gate", i18n_key="factor.season"),
            FactorSpec(
                id="rain_trigger", role="driver", i18n_key="factor.rain_trigger", weight=1.0
            ),
        ]
        values = {"season": 0.0, "rain_trigger": 1.0}
        score, _ = combine_factors(specs, values)
        assert score == 0.0

    def test_single_driver_contribution_equals_its_own_value(self) -> None:
        specs = [FactorSpec(id="rain_30d", role="driver", i18n_key="factor.rain_30d", weight=1.0)]
        values = {"rain_30d": 0.42}
        score, results = combine_factors(specs, values)
        assert score == pytest.approx(0.42)
        assert results[0].contribution == pytest.approx(0.42)
