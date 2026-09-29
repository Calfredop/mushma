"""The 15-day trend: an area's (or a cell's) conditions index per day, ending today."""

from datetime import timedelta
from pathlib import Path

import pytest

from api.live.repository import LiveRepository
from api.repository import TREND_DAYS, AreaNotFound
from api.timeutil import today_rome
from tests.live.helpers import (
    CELL_A,
    CELL_B,
    CELL_D_NON_WOODLAND,
    build_dataset,
    write_daily,
)


def _past_days() -> list:
    """The trend window's days before today, oldest first."""
    today = today_rome()
    return [today - timedelta(days=offset) for offset in range(TREND_DAYS - 1, 0, -1)]


@pytest.fixture
def repo(tmp_path: Path) -> LiveRepository:
    """The synthetic dataset plus porcini scores for every past day of the window: A climbs
    0.10, 0.11, ...; B holds 0.30; the day before the window is scored too, and so is the
    non-woodland cell D, neither of which may reach a trend."""
    rules = build_dataset(tmp_path)
    today = today_rome()
    rows = []
    for i, day in enumerate(_past_days()):
        rows.append(
            {"cell_id": CELL_A["cell_id"], "date": day, "score": 0.1 + 0.01 * i, "source_key": "x"}
        )
        rows.append({"cell_id": CELL_B["cell_id"], "date": day, "score": 0.3, "source_key": "x"})
        rows.append(
            {
                "cell_id": CELL_D_NON_WOODLAND["cell_id"],
                "date": day,
                "score": 1.0,
                "source_key": "x",
            }
        )
    before = today - timedelta(days=TREND_DAYS)
    rows.append({"cell_id": CELL_A["cell_id"], "date": before, "score": 1.0, "source_key": "x"})
    write_daily(tmp_path, "porcini", rows)
    return LiveRepository(tmp_path, rules=rules)


class TestAreaTrend:
    def test_the_region_trend_is_the_woodland_mean_for_the_days_ending_today(
        self, repo: LiveRepository
    ) -> None:
        response = repo.get_trend("porcini", None)

        today = today_rome()
        assert response.species == "porcini"
        assert response.area.kind == "region"
        assert response.area.code is None
        assert [d.date for d in response.days] == [*_past_days(), today]
        # The oldest day: A 0.10 and B 0.30 (D is not woodland). Today: A 0.40 and B 0.35.
        assert response.days[0].score == pytest.approx(0.2)
        assert response.days[-1].score == pytest.approx(0.375)

    def test_a_comune_trend_averages_only_its_own_cells(self, repo: LiveRepository) -> None:
        response = repo.get_trend("porcini", "045001")

        assert response.area.code == "045001"
        assert response.area.kind == "comune"
        assert response.area.name == "Alpha"
        assert response.days[0].score == pytest.approx(0.1)
        assert response.days[TREND_DAYS - 2].score == pytest.approx(0.1 + 0.01 * (TREND_DAYS - 2))
        assert response.days[-1].score == pytest.approx(0.4)

    def test_days_with_no_stored_scores_are_left_out(self, tmp_path: Path) -> None:
        repo = LiveRepository(tmp_path, rules=build_dataset(tmp_path))

        response = repo.get_trend("ovoli", None)

        assert [d.date for d in response.days] == [today_rome()]

    def test_a_comune_without_scored_cells_has_an_empty_trend(self, repo: LiveRepository) -> None:
        # Gamma's only cell (C) is scored on none of the window's days.
        assert repo.get_trend("porcini", "045003").days == []

    def test_an_unknown_comune_raises(self, repo: LiveRepository) -> None:
        with pytest.raises(AreaNotFound):
            repo.get_trend("porcini", "999999")

    def test_a_key_never_scored_has_an_empty_trend(self, tmp_path: Path) -> None:
        repo = LiveRepository(tmp_path, rules=build_dataset(tmp_path))
        assert repo.region_trend("nothing_here") == []


class TestRegionTrend:
    def test_matches_the_region_wide_area_trend(self, repo: LiveRepository) -> None:
        assert repo.region_trend("porcini") == repo.get_trend("porcini", None).days


class TestCellPastDays:
    def test_each_species_carries_the_window_days_before_today(self, repo: LiveRepository) -> None:
        detail = repo.get_cell_detail(CELL_A["cell_id"])

        porcini = next(f for f in detail.species if f.species == "porcini")
        assert [d.date for d in porcini.past] == _past_days()
        assert porcini.past[0].score == pytest.approx(0.1)
        assert porcini.days[0].date == today_rome()

    def test_a_species_with_no_past_scores_has_no_past_days(self, repo: LiveRepository) -> None:
        detail = repo.get_cell_detail(CELL_A["cell_id"])

        ovoli = next(f for f in detail.species if f.species == "ovoli")
        assert ovoli.past == []

    def test_the_spot_carries_them_too(self, repo: LiveRepository) -> None:
        detail = repo.get_spot(CELL_B["lat"], CELL_B["lon"])

        porcini = next(f for f in detail.species if f.species == "porcini")
        assert [d.score for d in porcini.past] == pytest.approx([0.3] * (TREND_DAYS - 1))
