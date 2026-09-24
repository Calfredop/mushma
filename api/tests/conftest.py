"""`client` runs the contract tests (tests/test_contract.py) twice: once against fixture mode,
once against a real `LiveRepository` over a tiny synthetic on-disk dataset (tests/live/helpers.py)
-- so "the contract tests pass against real data" (M4-api.md) is actually exercised, not just
plausible. Point MUSHMA_CONTRACT_BASE_URL at a deployed api/ to run the exact same tests against a
live deployment instead (e.g. `https://api.mappafunghi.app` after a deploy); that replaces both
modes with a single run against the given URL."""

import os
from collections.abc import Iterator

import httpx
import pytest

os.environ.setdefault("MUSHMA_FIXTURES", "1")

_DEPLOYED_BASE_URL = os.environ.get("MUSHMA_CONTRACT_BASE_URL")
_CLIENT_MODES = ["deployed"] if _DEPLOYED_BASE_URL else ["fixtures", "real"]


@pytest.fixture(params=_CLIENT_MODES)
def client(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Iterator[httpx.Client]:
    if _DEPLOYED_BASE_URL:
        with httpx.Client(base_url=_DEPLOYED_BASE_URL) as real_client:
            yield real_client
        return

    from fastapi.testclient import TestClient

    from api.main import app
    from api.routes import get_repository

    if request.param == "real":
        from api.live.repository import LiveRepository
        from tests.live.helpers import build_dataset

        root = tmp_path_factory.mktemp("live_contract")
        rules = build_dataset(root)
        app.dependency_overrides[get_repository] = lambda: LiveRepository(
            root, region="tuscany", rules=rules
        )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_repository, None)
