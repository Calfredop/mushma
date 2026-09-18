from datetime import date

from api.fixtures.cells import CELLS
from api.fixtures.generator import WINDOW_OFFSETS, combined_score, score_and_factors
from api.fixtures.scoring import FACTOR_SPECS
from api.species import SPECIES


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


class TestCombinedScore:
    def test_combined_is_the_max_across_species(self) -> None:
        cell = CELLS[5]
        target = date(2026, 9, 17)
        for offset in WINDOW_OFFSETS:
            per_species = [score_and_factors(cell, sp, target, offset)[0] for sp in SPECIES]
            assert combined_score(cell, target, offset) == max(per_species)
