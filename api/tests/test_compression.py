"""Large responses (the whole-region grids) go out gzipped: PRD -> Constraints -> Mobile
performance counts the payload budget compressed."""

from fastapi.testclient import TestClient

from api.main import app
from api.timeutil import today_rome

client = TestClient(app)


def test_a_grid_is_gzipped_when_the_client_accepts_it() -> None:
    response = client.get(
        f"/history/season/{today_rome().year - 1}",
        params={"species": "porcini"},
        headers={"Accept-Encoding": "gzip"},
    )

    assert response.status_code == 200
    assert response.headers.get("content-encoding") == "gzip"


def test_a_tiny_response_is_left_alone() -> None:
    response = client.get("/health", headers={"Accept-Encoding": "gzip"})

    assert "content-encoding" not in response.headers
