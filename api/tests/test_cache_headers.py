from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from api.cache import IMMUTABLE, SHORT_LIVED
from api.main import app
from api.timeutil import today_rome

client = TestClient(app)


class TestScoresCacheHeaders:
    def test_a_past_date_is_immutable(self) -> None:
        past = today_rome() - timedelta(days=1)
        response = client.get("/scores", params={"species": "porcini", "date": str(past)})
        assert response.headers["cache-control"] == IMMUTABLE

    def test_today_is_short_lived(self) -> None:
        response = client.get("/scores", params={"species": "porcini"})
        assert response.headers["cache-control"] == SHORT_LIVED

    def test_a_forecast_date_is_short_lived(self) -> None:
        forecast = today_rome() + timedelta(days=3)
        response = client.get("/scores", params={"species": "porcini", "date": str(forecast)})
        assert response.headers["cache-control"] == SHORT_LIVED


class TestHotspotsCacheHeaders:
    def test_a_past_date_is_immutable(self) -> None:
        past = today_rome() - timedelta(days=1)
        response = client.get("/hotspots", params={"species": "combined", "date": str(past)})
        assert response.headers["cache-control"] == IMMUTABLE

    def test_today_is_short_lived(self) -> None:
        response = client.get("/hotspots", params={"species": "combined"})
        assert response.headers["cache-control"] == SHORT_LIVED


@pytest.mark.parametrize(
    ("path", "params"),
    [
        ("/spot", {"lat": 43.7, "lon": 11.2}),
        ("/sightings", {"species": "porcini"}),
    ],
)
def test_always_current_endpoints_are_short_lived(path: str, params: dict) -> None:
    response = client.get(path, params=params)
    assert response.headers["cache-control"] == SHORT_LIVED


def test_cell_detail_is_short_lived() -> None:
    scores = client.get("/scores", params={"species": "combined"}).json()
    cell_id = scores["cells"][0]["cell_id"]
    response = client.get(f"/cells/{cell_id}")
    assert response.headers["cache-control"] == SHORT_LIVED
