"""Route-level: a response cache hit skips the repository after the first call."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.models import GridCellScore, ScoresResponse, StatusResponse
from api.response_cache import MemoryBackend, bump_region, reset_cache_for_tests
from api.routes import get_repository
from api.timeutil import today_rome


@pytest.fixture(autouse=True)
def _memory_cache() -> None:
    reset_cache_for_tests(MemoryBackend())


@pytest.fixture
def scores_repo() -> MagicMock:
    repo = MagicMock()
    repo.region = "tuscany"
    today = today_rome()
    repo.get_scores.return_value = ScoresResponse(
        species="porcini",
        date=today,
        cells=[GridCellScore(cell_id="c1", lon=11.0, lat=43.0, score=0.5)],
    )
    repo.get_status.return_value = StatusResponse(
        scored_through=today,
        updated_at=datetime(2026, 9, 28, 5, 0, tzinfo=UTC),
        rules_version="abc",
    )
    return repo


def test_second_scores_request_is_served_from_cache(scores_repo: MagicMock) -> None:
    app.dependency_overrides[get_repository] = lambda: scores_repo
    try:
        client = TestClient(app)
        first = client.get("/scores", params={"species": "porcini"})
        second = client.get("/scores", params={"species": "porcini"})
    finally:
        app.dependency_overrides.pop(get_repository, None)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert scores_repo.get_scores.call_count == 1


def test_bump_makes_the_next_scores_request_recompute(scores_repo: MagicMock) -> None:
    app.dependency_overrides[get_repository] = lambda: scores_repo
    try:
        client = TestClient(app)
        client.get("/scores", params={"species": "porcini"})
        bump_region("tuscany")
        client.get("/scores", params={"species": "porcini"})
    finally:
        app.dependency_overrides.pop(get_repository, None)

    assert scores_repo.get_scores.call_count == 2


def test_status_is_not_cached(scores_repo: MagicMock) -> None:
    app.dependency_overrides[get_repository] = lambda: scores_repo
    try:
        client = TestClient(app)
        client.get("/status")
        client.get("/status")
    finally:
        app.dependency_overrides.pop(get_repository, None)

    assert scores_repo.get_status.call_count == 2
