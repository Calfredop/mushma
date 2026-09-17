import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from api.sightings.http import JsonClient, fetch_pages


class FakeApi(BaseHTTPRequestHandler):
    responses: list[tuple[int, dict]] = []
    hits: list[str] = []

    def do_GET(self) -> None:  # noqa: N802
        type(self).hits.append(self.path)
        queue = type(self).responses
        status, body = queue.pop(0) if len(queue) > 1 else queue[0]
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def server():
    FakeApi.responses = []
    FakeApi.hits = []
    httpd = HTTPServer(("127.0.0.1", 0), FakeApi)
    threading.Thread(target=httpd.serve_forever, args=(0.01,), daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()


class FakeClock:
    def __init__(self) -> None:
        self.sleeps: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.sleeps.append(seconds)


# --- JsonClient: retries and errors -----------------------------------------------------------


def test_client_retries_server_errors_with_backoff(server: str) -> None:
    FakeApi.responses = [(502, {}), (503, {}), (200, {"ok": True})]
    clock = FakeClock()

    payload = JsonClient(sleep=clock, backoff_s=1).get(server)

    assert payload == {"ok": True}
    assert clock.sleeps == [1, 2]


def test_client_retries_429_with_backoff(server: str) -> None:
    FakeApi.responses = [(429, {}), (200, {"ok": True})]
    clock = FakeClock()

    payload = JsonClient(sleep=clock, backoff_s=1).get(server)

    assert payload == {"ok": True}
    assert clock.sleeps == [1]


def test_client_fails_fast_on_a_client_error(server: str) -> None:
    FakeApi.responses = [(400, {"reason": "bad request"})]
    clock = FakeClock()

    with pytest.raises(ValueError, match="400"):
        JsonClient(sleep=clock).get(server)

    assert len(FakeApi.hits) == 1


def test_client_gives_up_after_its_retry_budget(server: str) -> None:
    FakeApi.responses = [(503, {})] * 10
    clock = FakeClock()

    with pytest.raises(ValueError, match="503"):
        JsonClient(sleep=clock, retries=2, backoff_s=1).get(server)

    assert len(FakeApi.hits) == 3  # first try + 2 retries


# --- fetch_pages: caching and resumability ------------------------------------------------------


def test_fetch_pages_stops_at_the_last_page_and_caches_each_one(tmp_path: Path) -> None:
    cache_dir = tmp_path / "gbif" / "123"
    served = {
        0: {"results": [1, 2], "endOfRecords": False},
        2: {"results": [3], "endOfRecords": True},
    }
    urls_fetched = []

    client = JsonClient()
    client.get = lambda url: urls_fetched.append(url) or served[int(url.split("=")[1])]  # type: ignore[method-assign]

    pages = fetch_pages(
        client,
        lambda offset: f"http://example.invalid/?offset={offset}",
        cache_dir,
        page_size=2,
        is_last_page=lambda payload: bool(payload.get("endOfRecords")),
    )

    assert [p["results"] for p in pages] == [[1, 2], [3]]
    assert len(urls_fetched) == 2
    assert sorted(p.name for p in cache_dir.glob("page_*.json")) == [
        "page_0000000.json",
        "page_0000002.json",
    ]
    assert (cache_dir / ".complete").exists()


def test_fetch_pages_resumes_from_cached_pages_without_refetching(tmp_path: Path) -> None:
    cache_dir = tmp_path / "gbif" / "123"
    cache_dir.mkdir(parents=True)
    (cache_dir / "page_0000000.json").write_text(json.dumps({"results": [1], "endOfRecords": True}))

    client = JsonClient()
    calls: list[str] = []

    def failing_get(url: str) -> dict:
        calls.append(url)
        raise AssertionError("should not fetch: page already cached")

    client.get = failing_get  # type: ignore[method-assign]

    pages = fetch_pages(
        client,
        lambda offset: f"http://example.invalid/?offset={offset}",
        cache_dir,
        page_size=1,
        is_last_page=lambda payload: bool(payload.get("endOfRecords")),
    )

    assert [p["results"] for p in pages] == [[1]]
    assert calls == []


def test_fetch_pages_short_circuits_once_marked_complete(tmp_path: Path) -> None:
    cache_dir = tmp_path / "gbif" / "123"
    cache_dir.mkdir(parents=True)
    (cache_dir / "page_0000000.json").write_text(json.dumps({"results": [1], "endOfRecords": True}))
    (cache_dir / ".complete").touch()

    client = JsonClient()
    client.get = lambda url: (_ for _ in ()).throw(AssertionError("no calls expected"))  # type: ignore[method-assign]

    pages = fetch_pages(
        client,
        lambda offset: f"http://example.invalid/?offset={offset}",
        cache_dir,
        page_size=1,
        is_last_page=lambda payload: True,
    )

    assert [p["results"] for p in pages] == [[1]]
