"""GET /factors (analysis mode) in fixture mode: the route's rules and FixtureRepository's values.
The live repository's winner selection is in tests/live/test_factors.py; the shape every storage
must return is in tests/test_contract.py."""

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from api.cache import SHORT_LIVED
from api.fixtures.cells import CELLS
from api.fixtures.generator import score_and_factors
from api.fixtures.repository import FixtureRepository
from api.fixtures.scoring import FACTOR_SPECS
from api.main import app
from api.repository import DateOutOfRange
from api.timeutil import today_rome

client = TestClient(app)


class TestRoute:
    def test_defaults_to_today(self) -> None:
        response = client.get("/factors", params={"species": "porcini"})
        assert response.status_code == 200
        assert response.json()["date"] == str(today_rome())

    def test_rejects_the_combined_score(self) -> None:
        response = client.get("/factors", params={"species": "combined"})
        assert response.status_code == 422

    def test_a_day_without_factor_rows_404s_with_the_stored_range(self) -> None:
        response = client.get("/factors", params={"species": "ovoli", "date": "2000-01-01"})
        assert response.status_code == 404
        detail = response.json()["detail"]
        assert str(today_rome() - timedelta(days=6)) in detail
        assert str(today_rome() + timedelta(days=7)) in detail

    def test_cached_like_scores(self) -> None:
        response = client.get("/factors", params={"species": "gallinacci"})
        assert response.headers["cache-control"] == SHORT_LIVED


class TestFixtureRepository:
    @pytest.mark.parametrize("species", ["porcini", "ovoli", "gallinacci"])
    def test_chips_are_the_fixture_rule_file_in_breakdown_order(self, species: str) -> None:
        response = FixtureRepository().get_factors(species, today_rome())
        assert [(c.id, c.i18n_key, c.role) for c in response.factors] == [
            (spec.id, spec.i18n_key, spec.role) for spec in FACTOR_SPECS[species]
        ]

    def test_values_are_the_breakdowns_values_rounded(self) -> None:
        today = today_rome()
        response = FixtureRepository().get_factors("ovoli", today)
        assert [c.cell_id for c in response.cells] == [cell.id for cell in CELLS]
        cell = CELLS[3]
        _, breakdown = score_and_factors(cell, "ovoli", today, 0)
        row = next(c for c in response.cells if c.cell_id == cell.id)
        assert (row.lon, row.lat) == (cell.lon, cell.lat)
        assert row.values == [round(f.value, 3) for f in breakdown]

    def test_outside_the_window_raises(self) -> None:
        with pytest.raises(DateOutOfRange):
            FixtureRepository().get_factors("porcini", today_rome() + timedelta(days=8))
