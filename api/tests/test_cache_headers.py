from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from api.cache import DAILY, SHORT_LIVED, cache_control_for_date
from api.main import app
from api.timeutil import today_rome

client = TestClient(app)


class TestScoresCacheHeaders:
    def test_a_past_day_the_daily_job_still_rescores_is_short_lived(self) -> None:
        # The job scores today -6 to +7 every morning: yesterday changes as reanalysis arrives.
        past = today_rome() - timedelta(days=1)
        response = client.get("/scores", params={"species": "porcini", "date": str(past)})
        assert response.headers["cache-control"] == SHORT_LIVED

    def test_an_older_day_is_kept_for_a_day_as_history_can_be_rescored(self) -> None:
        assert cache_control_for_date(today_rome() - timedelta(days=30)) == DAILY
        assert cache_control_for_date(today_rome() - timedelta(days=6)) == SHORT_LIVED
        assert cache_control_for_date(today_rome() - timedelta(days=7)) == DAILY

    def test_today_is_short_lived(self) -> None:
        response = client.get("/scores", params={"species": "porcini"})
        assert response.headers["cache-control"] == SHORT_LIVED

    def test_a_forecast_date_is_short_lived(self) -> None:
        forecast = today_rome() + timedelta(days=3)
        response = client.get("/scores", params={"species": "porcini", "date": str(forecast)})
        assert response.headers["cache-control"] == SHORT_LIVED


class TestHotspotsCacheHeaders:
    def test_a_past_day_in_the_rescored_window_is_short_lived(self) -> None:
        past = today_rome() - timedelta(days=1)
        response = client.get("/hotspots", params={"species": "combined", "date": str(past)})
        assert response.headers["cache-control"] == SHORT_LIVED

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


class TestTimeViewsCacheHeaders:
    def test_the_comuni_list_is_kept_for_a_day(self) -> None:
        assert client.get("/comuni").headers["cache-control"] == DAILY

    def test_seasons_and_the_outlook_are_short_lived(self) -> None:
        for path, params in (
            ("/history/seasons", {}),
            ("/outlook", {"species": "porcini"}),
            (f"/history/season/{today_rome().year}", {"species": "porcini"}),
        ):
            assert client.get(path, params=params).headers["cache-control"] == SHORT_LIVED

    def test_a_past_season_is_kept_for_a_day_not_forever(self) -> None:
        past = today_rome().year - 1
        response = client.get(f"/history/season/{past}", params={"species": "porcini"})
        assert response.headers["cache-control"] == DAILY
