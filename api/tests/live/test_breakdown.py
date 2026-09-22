"""api.live.breakdown replays api.model.engine.score_species's contribution formula from a
stored factors-tier row, since the row only keeps each factor's raw `value`."""

import numpy as np
import pandas as pd
import pytest
from pydantic import TypeAdapter

from api.live.breakdown import reconstruct_breakdown
from api.model.rules import (
    DERIVED_SERIES,
    GRID_ATTRIBUTES,
    SUN_SERIES,
    Factor,
    GrowthClock,
    load_rules,
)

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


def rain_event(id: str = "rain_trigger", weight: float = 2.0) -> Factor:
    return factor(
        id=id,
        role="driver",
        weight=weight,
        kind="rain_event",
        input={"variable": "precipitation_sum", "accumulation_days": 3},
        response={"amount_mm": [10, 30, None, None], "lag_days": [6, 10, 16, 24]},
    )


def window_aggregate(id: str, variable: str, **overrides) -> Factor:
    return factor(
        id=id,
        role="driver",
        weight=1.0,
        kind="window_aggregate",
        input={"variable": variable, "aggregate": "mean", "window_days": 20, "offset_days": 2},
        response={"trapezoid": [6, 10, 17, 22]},
        **overrides,
    )


def days_since(id: str = "last_rain") -> Factor:
    return factor(
        id=id,
        role="stopper",
        kind="days_since",
        input={
            "variable": "precipitation_sum",
            "op": "gte",
            "threshold": 5,
            "max_lookback_days": 30,
        },
        response={"trapezoid": [None, None, 10, 20]},
    )


class TestFactorMeasurements:
    """The measurement behind a value (stored as ``<factor>__input`` / ``__days_ago``) and what the
    rule wanted of it, so the "why this score" copy can say both."""

    def test_a_factor_reports_its_role_and_weight(self) -> None:
        factors = [gate(), driver("a", weight=2.0), stopper()]
        row = {"season_window": 1.0, "a": 0.5, "drying_wind": 1.0}
        breakdown = reconstruct_breakdown(factors, row)
        assert [(b.role, b.weight) for b in breakdown] == [
            ("gate", None),
            ("driver", 2.0),
            ("stopper", None),
        ]

    def test_a_rain_event_carries_the_amount_its_lag_and_the_rule_bands(self) -> None:
        row = {"rain_trigger": 0.7, "rain_trigger__input": 42.0, "rain_trigger__days_ago": 6}
        (b,) = reconstruct_breakdown([rain_event()], row)
        assert (b.input, b.unit, b.days_ago) == (42.0, "mm", 6)
        assert b.rule is not None
        assert (b.rule.kind, b.rule.variable, b.rule.variable_unit) == (
            "rain_event",
            "precipitation_sum",
            "mm",
        )
        assert b.rule.window_days == 3
        assert b.rule.trapezoid == [10, 30, None, None]
        assert b.rule.lag_days == [6, 10, 16, 24]

    def test_a_rain_event_on_a_growth_clock_reports_growth_days(self) -> None:
        clock = GrowthClock.model_validate(
            {
                "temperature": {
                    "variable": "soil_temperature_0_to_7cm_mean",
                    "cardinal_c": [0, 18, 30],
                    "reference_c": 15,
                },
                "max_lag_days": 40,
                "confidence": "folklore",
                "source": ["x"],
            }
        )
        row = {
            "rain_trigger": 0.7,
            "rain_trigger__input": 42.0,
            "rain_trigger__days_ago": 14,
            "rain_trigger__growth_days": np.float32(9.3),
        }

        (clocked,) = reconstruct_breakdown([rain_event()], row, growth=clock)
        (plain,) = reconstruct_breakdown([rain_event()], row)

        assert (clocked.days_ago, clocked.growth_days) == (14, 9.3)
        assert clocked.rule is not None and clocked.rule.lag_unit == "growth_days"
        assert plain.rule is not None and plain.rule.lag_unit == "days"

    def test_a_where_condition_is_described_with_its_unit(self) -> None:
        conditional = stopper(
            where={"attribute": "elevation_m", "trapezoid": [None, None, 900, 1100]}
        )

        (b,) = reconstruct_breakdown([conditional], {"drying_wind": 0.9})

        assert b.rule is not None and b.rule.where is not None
        assert (b.rule.where.variable, b.rule.where.variable_unit) == ("elevation_m", "m")
        assert b.rule.where.trapezoid == [None, None, 900, 1100]
        (plain,) = reconstruct_breakdown([stopper()], {"drying_wind": 0.9})
        assert plain.rule is not None and plain.rule.where is None

    def test_a_window_aggregate_takes_its_unit_from_the_weather_config(self) -> None:
        factors = [window_aggregate("air_temperature", "temperature_2m_mean")]
        row = {"air_temperature": 0.8, "air_temperature__input": 14.2}
        (b,) = reconstruct_breakdown(factors, row)
        assert (b.input, b.unit, b.days_ago) == (14.2, "°C", None)
        assert b.rule is not None
        assert (b.rule.aggregate, b.rule.window_days, b.rule.offset_days) == ("mean", 20, 2)
        assert b.rule.trapezoid == [6, 10, 17, 22]
        assert b.rule.lag_days is None

    def test_rain_as_a_share_of_its_normal_is_in_percent(self) -> None:
        factors = [
            factor(
                id="rain_30d",
                role="driver",
                weight=1.0,
                kind="window_aggregate",
                input={
                    "variable": "precipitation_sum",
                    "aggregate": "percent_of_normal",
                    "window_days": 30,
                },
                response={"trapezoid": [50, 125, None, None]},
            )
        ]
        row = {"rain_30d": 0.62, "rain_30d__input": 97.0}
        (b,) = reconstruct_breakdown(factors, row)
        assert (b.input, b.unit) == (97.0, "%")
        assert b.rule is not None
        assert (b.rule.aggregate, b.rule.variable_unit) == ("percent_of_normal", "mm")

    def test_a_derived_series_has_its_own_unit(self) -> None:
        factors = [
            window_aggregate("balance", "water_balance"),
            window_aggregate("spike", "temperature_2m_max_anomaly_30d"),
        ]
        row = {"balance": 1.0, "spike": 1.0}
        assert [b.rule.variable_unit for b in reconstruct_breakdown(factors, row)] == ["mm", "°C"]

    def test_a_count_of_days_is_in_days_and_keeps_the_threshold_it_counted(self) -> None:
        row = {"drying_wind": 0.5, "drying_wind__input": 2.0}
        (b,) = reconstruct_breakdown([stopper()], row)
        assert (b.input, b.unit) == (2.0, "days")
        assert b.rule is not None
        assert (b.rule.op, b.rule.threshold, b.rule.variable_unit) == ("gt", 10, "km/h")
        assert b.rule.window_days == 3
        assert b.rule.trapezoid == [0, 1, 2, 3]

    def test_days_since_is_in_days_and_reports_its_lookback(self) -> None:
        row = {"last_rain": 1.0, "last_rain__input": 12.0}
        (b,) = reconstruct_breakdown([days_since()], row)
        assert (b.input, b.unit) == (12.0, "days")
        assert b.rule is not None
        assert (b.rule.op, b.rule.threshold, b.rule.window_days) == ("gte", 5, 30)

    def test_a_static_band_reads_the_cell_attribute_in_its_unit(self) -> None:
        row = {"altitude": 1.0, "altitude__input": 640.0}
        (b,) = reconstruct_breakdown([driver("altitude", weight=1.0)], row)
        assert (b.input, b.unit) == (640.0, "m")
        assert b.rule is not None
        assert (b.rule.kind, b.rule.variable, b.rule.variable_unit) == (
            "static_band",
            "elevation_m",
            "m",
        )

    def test_season_and_habitat_have_a_rule_kind_and_nothing_measured(self) -> None:
        (b,) = reconstruct_breakdown([gate()], {"season_window": 0.6})
        assert (b.input, b.unit, b.days_ago) == (None, None, None)
        assert b.rule is not None
        assert (b.rule.kind, b.rule.variable, b.rule.trapezoid) == ("season_window", None, None)

    def test_columns_missing_from_the_row_degrade_to_none(self) -> None:
        """Days scored without the factors tier's measurement columns still explain themselves."""
        (b,) = reconstruct_breakdown([rain_event()], {"rain_trigger": 0.7})
        assert (b.input, b.days_ago) == (None, None)
        assert b.unit == "mm"
        assert b.rule is not None

    @pytest.mark.parametrize("empty", [np.nan, pd.NA, None])
    def test_an_empty_measurement_is_none(self, empty: object) -> None:
        row = {"rain_trigger": 0.0, "rain_trigger__input": empty, "rain_trigger__days_ago": empty}
        (b,) = reconstruct_breakdown([rain_event()], row)
        assert (b.input, b.days_ago) == (None, None)

    def test_a_stored_measurement_is_rounded_for_display(self) -> None:
        """The store keeps float32, whose 14.2 would reach the JSON as 14.199999809265137."""
        row = {"rain_trigger": 1.0, "rain_trigger__input": np.float32(14.2)}
        (b,) = reconstruct_breakdown([rain_event()], row)
        assert b.input == 14.2

    def test_a_pandas_nullable_lag_is_a_plain_int(self) -> None:
        stored = pd.DataFrame(
            {"rain_trigger": [1.0], "rain_trigger__days_ago": pd.array([6], "Int16")}
        )
        (b,) = reconstruct_breakdown([rain_event()], stored.iloc[0].to_dict())
        assert b.days_ago == 6
        assert isinstance(b.days_ago, int)

    def test_every_grid_attribute_and_derived_series_has_a_unit(self) -> None:
        from api.model.rules import ATTRIBUTE_UNITS, DERIVED_UNITS

        assert GRID_ATTRIBUTES <= set(ATTRIBUTE_UNITS)
        assert set(DERIVED_SERIES) | {SUN_SERIES} == set(DERIVED_UNITS)

    def test_every_shipped_factor_describes_itself(self) -> None:
        """A new rule on an unknown variable would fail here, not in front of a forager."""
        for key, species in load_rules().species.items():
            row = {f.id: 0.5 for f in species.enabled_factors}
            for b in reconstruct_breakdown(species.enabled_factors, row):
                assert b.rule is not None, (key, b.key)
                if b.rule.variable is not None:
                    assert b.rule.variable_unit is not None, (key, b.key)
                    assert b.unit is not None, (key, b.key)


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
