"""`client` runs the contract tests in fixture mode against the in-process app
by default. Point MUSHMA_CONTRACT_BASE_URL at a deployed api/ (M4-api.md) to
run the exact same contract tests against real storage instead."""

import os
from collections.abc import Iterator

import httpx
import pytest

os.environ.setdefault("MUSHMA_FIXTURES", "1")


@pytest.fixture
def client() -> Iterator[httpx.Client]:
    base_url = os.environ.get("MUSHMA_CONTRACT_BASE_URL")
    if base_url:
        with httpx.Client(base_url=base_url) as real_client:
            yield real_client
        return

    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as test_client:
        yield test_client
