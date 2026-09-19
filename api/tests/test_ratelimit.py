from unittest.mock import MagicMock

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from api.ratelimit import RateLimitMiddleware, client_ip


def _app(per_minute: int) -> Starlette:
    async def ok(request: Request) -> PlainTextResponse:
        return PlainTextResponse("ok")

    app = Starlette(routes=[Route("/thing", ok), Route("/health", ok)])
    app.add_middleware(RateLimitMiddleware, per_minute=per_minute)
    return app


def _request(headers: dict[str, str], client_host: str | None = "203.0.113.5") -> Request:
    request = MagicMock(spec=Request)
    request.headers = headers
    request.client = MagicMock(host=client_host) if client_host else None
    return request


def test_prefers_flys_own_header() -> None:
    request = _request({"fly-client-ip": "1.2.3.4", "x-forwarded-for": "5.6.7.8"})
    assert client_ip(request) == "1.2.3.4"


def test_falls_back_to_x_forwarded_for_first_hop() -> None:
    request = _request({"x-forwarded-for": "5.6.7.8, 9.9.9.9"})
    assert client_ip(request) == "5.6.7.8"


def test_falls_back_to_the_socket_address_with_no_proxy() -> None:
    request = _request({})
    assert client_ip(request) == "203.0.113.5"


def test_falls_back_to_unknown_with_nothing_at_all() -> None:
    request = _request({}, client_host=None)
    assert client_ip(request) == "unknown"


@pytest.fixture(autouse=True)
def _not_fixtures_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    # The middleware is disabled outright under MUSHMA_FIXTURES=1 (conftest.py sets it for the
    # rest of the suite) -- these tests exercise the real enforcement path, so they turn it back
    # off just for themselves.
    monkeypatch.delenv("MUSHMA_FIXTURES", raising=False)


def test_allows_requests_under_the_limit() -> None:
    client = TestClient(_app(per_minute=3))
    for _ in range(3):
        assert client.get("/thing").status_code == 200


def test_429s_once_the_limit_is_exceeded() -> None:
    client = TestClient(_app(per_minute=2))
    client.get("/thing")
    client.get("/thing")
    response = client.get("/thing")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["error"]


def test_health_is_exempt_even_over_the_limit() -> None:
    client = TestClient(_app(per_minute=1))
    client.get("/thing")
    client.get("/thing")  # over limit now
    assert client.get("/health").status_code == 200


def test_disabled_entirely_under_mushma_fixtures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MUSHMA_FIXTURES", "1")
    client = TestClient(_app(per_minute=1))
    for _ in range(5):
        assert client.get("/thing").status_code == 200
