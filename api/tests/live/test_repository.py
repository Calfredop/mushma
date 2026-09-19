"""LiveRepository: the real ScoresRepository implementation, backed by the tiny synthetic on-disk
Parquet tree from tests/live/helpers.py (shaped exactly like the real M2/M3/M4 stores)."""

import math
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from api.live.repository import LiveRepository
from api.repository import CellNotFound, DateOutOfRange, ScoresUnavailable
from api.timeutil import today_rome
from tests.live.helpers import CELL_A, CELL_B, CELL_C, SCORES_DATE, build_dataset


@pytest.fixture
def repo(tmp_path: Path) -> LiveRepository:
    rules = build_dataset(tmp_path)
    return LiveRepository(tmp_path, rules=rules)


class TestGetScores:
    def test_returns_only_woodland_cells_with_lon_lat_and_score(self, repo: LiveRepository) -> None:
        response = repo.get_scores("porcini", SCORES_DATE)
        assert response.species == "porcini"
        assert response.date == SCORES_DATE
        assert {c.cell_id for c in response.cells} == {
            CELL_A["cell_id"],
            CELL_B["cell_id"],
            CELL_C["cell_id"],
        }
        by_id = {c.cell_id: c for c in response.cells}
        assert by_id[CELL_A["cell_id"]].score == pytest.approx(0.9)
        assert by_id[CELL_A["cell_id"]].lon == pytest.approx(CELL_A["lon"])

    def test_combined_reads_the_combined_tier_directly(self, repo: LiveRepository) -> None:
        response = repo.get_scores("combined", SCORES_DATE)
        assert {c.cell_id for c in response.cells} == {
            CELL_A["cell_id"],
            CELL_B["cell_id"],
            CELL_C["cell_id"],
        }

    def test_a_date_outside_the_stored_window_raises(self, repo: LiveRepository) -> None:
        with pytest.raises(DateOutOfRange):
            repo.get_scores("porcini", SCORES_DATE - timedelta(days=3000))


class TestGetHotspots:
    def test_adjacent_high_scoring_cells_cluster_and_carry_sightings(
        self, repo: LiveRepository
    ) -> None:
        response = repo.get_hotspots("porcini", SCORES_DATE, 10)
        assert response.species == "porcini"
        by_cells = {frozenset(h.cell_ids): h for h in response.hotspots}
        ab_cluster = by_cells[frozenset({CELL_A["cell_id"], CELL_B["cell_id"]})]
        assert ab_cluster.score == pytest.approx(0.9)
        assert ab_cluster.place.comune == "Alpha"
        assert ab_cluster.recent_sightings == 2  # one on A, one on B

        c_cluster = by_cells[frozenset({CELL_C["cell_id"]})]
        assert c_cluster.recent_sightings == 0

    def test_ranked_and_bounded_by_limit(self, repo: LiveRepository) -> None:
        response = repo.get_hotspots("porcini", SCORES_DATE, 1)
        assert len(response.hotspots) == 1
        assert response.hotspots[0].score == pytest.approx(0.9)

    def test_a_date_outside_the_stored_window_raises(self, repo: LiveRepository) -> None:
        with pytest.raises(DateOutOfRange):
            repo.get_hotspots("porcini", SCORES_DATE - timedelta(days=3000), 10)


class TestGetSightings:
    def test_counts_per_cell_source_and_license(self, repo: LiveRepository) -> None:
        response = repo.get_sightings("porcini", SCORES_DATE - timedelta(days=1))
        assert response.species == "porcini"
        by_cell = {c.cell_id: c for c in response.counts}
        assert by_cell[CELL_A["cell_id"]].source == "gbif"
        assert by_cell[CELL_A["cell_id"]].count == 1
        assert by_cell[CELL_B["cell_id"]].license == "CC-BY-NC-4.0"

    def test_since_in_the_future_returns_nothing(self, repo: LiveRepository) -> None:
        response = repo.get_sightings("porcini", SCORES_DATE + timedelta(days=1))
        assert response.counts == []


class TestGetCellDetailAndSpot:
    def test_cell_detail_covers_all_groups_for_the_8_day_outlook(
        self, repo: LiveRepository
    ) -> None:
        detail = repo.get_cell_detail(CELL_A["cell_id"])
        assert detail.cell_id == CELL_A["cell_id"]
        assert detail.place.comune == "Alpha"
        assert {f.species for f in detail.species} == {"porcini", "ovoli", "gallinacci"}
        for forecast in detail.species:
            assert len(forecast.days) == 8
            dates = [d.date for d in forecast.days]
            assert dates == sorted(dates)
            for day in forecast.days:
                assert len(day.factors) > 0
                product = math.prod(f.contribution for f in day.factors)
                assert product == pytest.approx(day.score, abs=1e-6)

    def test_the_breakdown_follows_the_winning_leaf_key_across_the_window(
        self, repo: LiveRepository
    ) -> None:
        detail = repo.get_cell_detail(CELL_A["cell_id"])
        porcini = next(f for f in detail.species if f.species == "porcini")
        assert porcini.days[0].factors[0].key == "rain_a"
        assert porcini.days[7].factors[0].key == "rain_b"

    def test_a_stored_measurement_reaches_the_breakdown_and_its_absence_reads_none(
        self, repo: LiveRepository
    ) -> None:
        def first_porcini_factor(cell_id: str):
            species = repo.get_cell_detail(cell_id).species
            return next(f for f in species if f.species == "porcini").days[0].factors[0]

        measured = first_porcini_factor(CELL_B["cell_id"])
        assert (measured.key, measured.input, measured.unit) == ("rain_a", 640.0, "m")
        unmeasured = first_porcini_factor(CELL_A["cell_id"])
        assert (unmeasured.key, unmeasured.input, unmeasured.unit) == ("rain_a", None, "m")

    def test_unknown_cell_id_raises(self, repo: LiveRepository) -> None:
        with pytest.raises(CellNotFound):
            repo.get_cell_detail("not-a-real-cell")

    def test_spot_resolves_to_the_nearest_woodland_cell(self, repo: LiveRepository) -> None:
        spot = repo.get_spot(lat=CELL_A["lat"] + 0.0001, lon=CELL_A["lon"] + 0.0001)
        assert spot.cell_id == CELL_A["cell_id"]


class TestGetStatus:
    def test_scored_through_is_the_latest_stored_combined_day(self, repo: LiveRepository) -> None:
        status = repo.get_status()
        assert status.scored_through >= today_rome() + timedelta(days=7)

    def test_no_meta_json_means_no_updated_at_or_rules_version(self, repo: LiveRepository) -> None:
        # tests/live/helpers.py writes score parquet files directly, the way the real pipeline's
        # rows look, without running api.model.pipeline.write_meta -- so there's no meta.json here.
        status = repo.get_status()
        assert status.updated_at is None
        assert status.rules_version is None

    def test_reads_meta_json_when_the_pipeline_has_written_one(self, tmp_path: Path) -> None:
        rules = build_dataset(tmp_path)
        repo = LiveRepository(tmp_path, rules=rules)
        repo.scores.meta_path.write_text(
            '{"written_at": "2026-09-18T05:30:00+00:00", "rules_version": "abc123"}'
        )
        status = repo.get_status()
        assert status.updated_at == datetime(2026, 9, 18, 5, 30, tzinfo=UTC)
        assert status.rules_version == "abc123"

    def test_raises_when_nothing_has_ever_been_scored(self, tmp_path: Path) -> None:
        from api.model.rules import RuleSet

        repo = LiveRepository(tmp_path, rules=RuleSet(groups={}, species={}, references={}))
        with pytest.raises(ScoresUnavailable):
            repo.get_status()


def test_a_replayed_days_hotspots_count_only_sightings_up_to_that_day(tmp_path: Path) -> None:
    from tests.live.helpers import sighting_record, write_sightings

    rules = build_dataset(tmp_path)
    write_sightings(
        tmp_path,
        [sighting_record("later", "porcini", CELL_A["cell_id"], SCORES_DATE + timedelta(days=5))],
    )
    repo = LiveRepository(tmp_path, rules=rules)

    response = repo.get_hotspots("porcini", SCORES_DATE, 10)

    by_cells = {frozenset(h.cell_ids): h for h in response.hotspots}
    assert by_cells[frozenset({CELL_A["cell_id"], CELL_B["cell_id"]})].recent_sightings == 2
