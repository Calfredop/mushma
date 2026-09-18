"""The live time views over the synthetic history tables of tests/live/helpers.py."""

from datetime import timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.live.repository import LiveRepository
from api.main import app
from api.repository import AreaNotFound, HistoryUnavailable, SeasonNotFound
from api.routes import get_repository
from api.timeutil import today_rome
from tests.live.helpers import CELL_A, build_dataset, cell, write_cells


@pytest.fixture
def repo(tmp_path: Path) -> LiveRepository:
    return LiveRepository(tmp_path, rules=build_dataset(tmp_path))


def test_comuni_are_listed_by_name_with_their_woodland(repo: LiveRepository) -> None:
    comuni = repo.get_comuni().comuni

    assert [c.name for c in comuni] == ["Alpha", "Beta", "Gamma"]
    assert comuni[0].code == "045001"
    assert comuni[0].cells == 1


def test_a_comunes_seasons_carry_months_weather_and_the_typical(repo: LiveRepository) -> None:
    body = repo.get_seasons("porcini", "045001")

    years = [s.year for s in body.seasons]
    assert years == [today_rome().year - 2, today_rome().year - 1, today_rome().year]
    last_year = body.seasons[1]
    assert last_year.complete
    assert last_year.good_days_typical is not None
    assert last_year.rain is not None and last_year.rain.normal_mm > 0
    assert last_year.sightings == 2
    assert [m.month for m in last_year.months] == list(range(1, 13))
    assert body.baseline.score_years == years[:2]


def test_an_unknown_comune_is_not_found(repo: LiveRepository) -> None:
    with pytest.raises(AreaNotFound):
        repo.get_seasons("porcini", "999999")


def test_the_season_map_places_every_cell_and_ranks_the_comuni(repo: LiveRepository) -> None:
    year = today_rome().year - 1

    body = repo.get_season_map(year, "porcini")

    by_cell = {c.cell_id: c for c in body.cells}
    assert by_cell[CELL_A["cell_id"]].lon == pytest.approx(CELL_A["lon"])
    assert by_cell[CELL_A["cell_id"]].good_days == 20
    assert body.complete
    with pytest.raises(SeasonNotFound):
        repo.get_season_map(1900, "porcini")


def test_the_outlook_starts_after_the_7_day_forecast_and_reads_the_rain(
    repo: LiveRepository,
) -> None:
    body = repo.get_outlook("porcini", None)
    today = today_rome()

    if body.window.end <= today + timedelta(days=7):
        assert body.periods == []  # out of season: nothing to look ahead to
        return
    assert body.periods, "in season, the outlook has periods"
    first = body.periods[0]
    assert first.start > today + timedelta(days=7)
    assert first.past_years == 2
    assert body.rain_lead.min_days == 10
    assert body.issued == today
    assert body.season_to_date is not None
    assert body.season_to_date.good_days_typical is not None
    known = [p for p in body.periods if p.lead_rain_pct is not None]
    assert known, "the lead-window rain is known for at least the first periods"
    for period in known:
        assert period.outlook in ("better", "usual", "worse")


def test_without_history_the_time_views_are_unavailable(tmp_path: Path) -> None:
    write_cells(tmp_path, [cell(0, 0, lon=10.0, lat=43.0)])
    repo = LiveRepository(tmp_path, rules=None)
    app.dependency_overrides[get_repository] = lambda: repo
    try:
        with TestClient(app) as client:
            for path, params in (
                ("/comuni", {}),
                ("/history/seasons", {}),
                ("/history/season/2025", {"species": "porcini"}),
                ("/outlook", {"species": "porcini"}),
            ):
                assert client.get(path, params=params).status_code == 503, path
    finally:
        app.dependency_overrides.pop(get_repository, None)
    with pytest.raises(HistoryUnavailable):
        repo.get_comuni()


def test_without_long_range_data_the_outlook_still_lists_the_weeks_ahead(
    repo: LiveRepository,
) -> None:
    repo.time_views.store.area_seasonal_path.unlink()
    today = today_rome()

    body = repo.get_outlook("gallinacci", None)

    if body.window.end <= today + timedelta(days=7):
        return  # out of season
    assert body.periods, "the calendar still has weeks ahead in season"
    assert body.periods[-1].outlook == "unknown"  # nothing to read the rain from that far ahead
