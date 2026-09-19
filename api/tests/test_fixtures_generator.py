from datetime import date

import pytest

from api.fixtures.cells import CELLS
from api.fixtures.generator import WINDOW_OFFSETS, combined_score, score_and_factors
from api.fixtures.scoring import ALTITUDE_TRAPEZOID, FACTOR_SPECS, trapezoid
from api.species import SPECIES

TARGET = date(2026, 9, 17)


class TestScoreAndFactors:
    def test_score_is_bounded_and_matches_its_own_factor_breakdown(self) -> None:
        cell = CELLS[0]
        for species in SPECIES:
            for offset in WINDOW_OFFSETS:
                score, factors = score_and_factors(cell, species, date(2026, 9, 17), offset)
                assert 0.0 <= score <= 1.0
                assert [f.key for f in factors] == [spec.id for spec in FACTOR_SPECS[species]]
                for f in factors:
                    assert 0.0 <= f.value <= 1.0

    def test_deterministic_for_the_same_inputs(self) -> None:
        cell = CELLS[3]
        first = score_and_factors(cell, "porcini", date(2026, 9, 17), 2)
        second = score_and_factors(cell, "porcini", date(2026, 9, 17), 2)
        assert first == second

    def test_varies_across_cells_and_days(self) -> None:
        cell_a, cell_b = CELLS[0], CELLS[1]
        score_a, _ = score_and_factors(cell_a, "porcini", date(2026, 9, 17), 0)
        score_b, _ = score_and_factors(cell_b, "porcini", date(2026, 9, 17), 0)
        scores_over_time = {
            offset: score_and_factors(cell_a, "porcini", date(2026, 9, 17), offset)[0]
            for offset in WINDOW_OFFSETS
        }
        assert score_a != score_b
        assert len(set(scores_over_time.values())) > 1

    def test_out_of_season_zeroes_the_score(self) -> None:
        cell = CELLS[0]
        score, factors = score_and_factors(cell, "ovoli", date(2026, 2, 1), 0)
        assert score == 0.0
        assert next(f for f in factors if f.key == "season").value == 0.0


def every_factor():
    for cell in CELLS:
        for species in SPECIES:
            for offset in WINDOW_OFFSETS:
                _, factors = score_and_factors(cell, species, TARGET, offset)
                for factor in factors:
                    yield cell, species, factor


class TestMeasurements:
    """The fixture breakdown carries the same measurement fields as the live one, and they agree
    with the value and the rule beside them: a demo that shows "2 frosty nights" next to a value of
    0.9 would contradict its own rule."""

    def test_every_factor_names_its_role_weight_and_rule(self) -> None:
        for _, species, factor in every_factor():
            spec = next(s for s in FACTOR_SPECS[species] if s.id == factor.key)
            assert (factor.role, factor.weight) == (spec.role, spec.weight)
            assert factor.rule is not None

    def test_season_and_habitat_measure_nothing(self) -> None:
        for _, _, factor in every_factor():
            if factor.key in ("season", "habitat"):
                assert (factor.input, factor.unit, factor.days_ago) == (None, None, None)
            else:
                assert factor.input is not None
                assert factor.unit is not None

    def test_a_measurement_reproduces_the_value_it_explains(self) -> None:
        for _, _, factor in every_factor():
            if factor.input is not None:
                assert factor.rule is not None and factor.rule.trapezoid is not None
                assert trapezoid(factor.input, factor.rule.trapezoid) == pytest.approx(
                    factor.value, abs=0.02
                ), factor.key

    def test_altitude_reads_the_cells_own_elevation_and_its_species_band(self) -> None:
        for cell, species, factor in every_factor():
            if factor.key == "altitude":
                assert factor.input == cell.elevation_m
                assert factor.unit == "m"
                assert factor.rule is not None
                assert tuple(factor.rule.trapezoid) == ALTITUDE_TRAPEZOID[species]

    def test_a_rain_event_says_when_the_rain_ended_inside_its_lag_window(self) -> None:
        seen = 0
        for _, _, factor in every_factor():
            if factor.rule is not None and factor.rule.kind == "rain_event":
                assert factor.rule.lag_days is not None
                _, full_from, full_to, _ = factor.rule.lag_days
                assert factor.days_ago is not None
                assert full_from <= factor.days_ago <= full_to
                seen += 1
            else:
                assert factor.days_ago is None
        assert seen > 0

    def test_a_count_of_days_is_a_whole_number_of_days(self) -> None:
        seen = 0
        for _, _, factor in every_factor():
            if factor.rule is not None and factor.rule.kind in ("count_days", "days_since"):
                assert factor.unit == "days"
                assert factor.input == int(factor.input)
                seen += 1
        assert seen > 0


class TestCombinedScore:
    def test_combined_is_the_max_across_species(self) -> None:
        cell = CELLS[5]
        target = date(2026, 9, 17)
        for offset in WINDOW_OFFSETS:
            per_species = [score_and_factors(cell, sp, target, offset)[0] for sp in SPECIES]
            assert combined_score(cell, target, offset) == max(per_species)
