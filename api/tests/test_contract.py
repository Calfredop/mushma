"""Contract tests every endpoint must pass (M4 plan, item 5). These parse responses with the same
Pydantic models the API declares, and don't assume any particular storage's cell set -- they
discover it from the responses themselves. So pointing MUSHMA_CONTRACT_BASE_URL at a deployed
api/ runs the identical assertions against real production data (M4-api.md item 9: verify a
deployment by running this suite against it)."""

import math

import httpx
import pytest

from api.models import CellDetailResponse, HotspotsResponse, ScoresResponse, SightingsResponse


@pytest.fixture
def servable_cell_ids(client: httpx.Client) -> set[str]:
    response = client.get("/scores", params={"species": "combined"})
    assert response.status_code == 200
    return {cell["cell_id"] for cell in response.json()["cells"]}


@pytest.fixture
def a_known_cell(client: httpx.Client) -> tuple[str, dict[str, float]]:
    """A real cell id and point, taken from a live ``/scores`` response rather than assumed in
    advance -- this suite doesn't know or care which storage is behind ``client``."""
    response = client.get("/scores", params={"species": "combined"})
    assert response.status_code == 200
    cells = response.json()["cells"]
    assert cells, "no scored cells -- is the served window empty?"
    first = cells[0]
    return first["cell_id"], {"lat": first["lat"], "lon": first["lon"]}


class TestScores:
    @pytest.mark.parametrize("species", ["porcini", "ovoli", "gallinacci", "combined"])
    def test_every_species_scores_the_same_set_of_cells(
        self, client: httpx.Client, species: str, servable_cell_ids: set[str]
    ) -> None:
        response = client.get("/scores", params={"species": species})
        assert response.status_code == 200
        body = ScoresResponse.model_validate(response.json())
        assert body.species == species
        assert {cell.cell_id for cell in body.cells} == servable_cell_ids
        for cell in body.cells:
            assert 0.0 <= cell.score <= 1.0

    def test_rejects_an_unknown_species(self, client: httpx.Client) -> None:
        response = client.get("/scores", params={"species": "amanita_phalloides"})
        assert response.status_code == 422

    def test_404s_outside_the_served_window(self, client: httpx.Client) -> None:
        response = client.get("/scores", params={"species": "porcini", "date": "2000-01-01"})
        assert response.status_code == 404


class TestSpotAndCells:
    def test_spot_and_cell_detail_share_a_shape(
        self, client: httpx.Client, a_known_cell: tuple[str, dict[str, float]]
    ) -> None:
        cell_id, point = a_known_cell
        spot_response = client.get("/spot", params=point)
        cell_response = client.get(f"/cells/{cell_id}")
        assert spot_response.status_code == 200
        assert cell_response.status_code == 200

        spot = CellDetailResponse.model_validate(spot_response.json())
        cell = CellDetailResponse.model_validate(cell_response.json())
        assert spot.cell_id == cell_id
        assert cell.cell_id == cell_id

        for detail in (spot, cell):
            assert {forecast.species for forecast in detail.species} == {
                "porcini",
                "ovoli",
                "gallinacci",
            }
            for forecast in detail.species:
                assert len(forecast.days) == 8  # today + 7-day outlook
                dates = [day.date for day in forecast.days]
                assert dates == sorted(dates)
                for day in forecast.days:
                    assert 0.0 <= day.score <= 1.0
                    assert len(day.factors) > 0
                    contributions = math.prod(f.contribution for f in day.factors)
                    assert contributions == pytest.approx(day.score, abs=1e-6)

    def test_unknown_cell_id_404s(self, client: httpx.Client) -> None:
        response = client.get("/cells/not-a-real-cell")
        assert response.status_code == 404


class TestHotspots:
    def test_ranked_and_bounded_by_limit(
        self, client: httpx.Client, servable_cell_ids: set[str]
    ) -> None:
        response = client.get("/hotspots", params={"species": "combined", "limit": 3})
        assert response.status_code == 200
        body = HotspotsResponse.model_validate(response.json())
        assert len(body.hotspots) <= 3
        scores = [h.score for h in body.hotspots]
        assert scores == sorted(scores, reverse=True)
        for hotspot in body.hotspots:
            assert set(hotspot.cell_ids) <= servable_cell_ids
            assert hotspot.recent_sightings >= 0

    def test_404s_outside_the_served_window(self, client: httpx.Client) -> None:
        response = client.get("/hotspots", params={"species": "porcini", "date": "2000-01-01"})
        assert response.status_code == 404


class TestSightings:
    def test_never_exposes_coordinates(
        self, client: httpx.Client, servable_cell_ids: set[str]
    ) -> None:
        response = client.get("/sightings", params={"species": "porcini"})
        assert response.status_code == 200
        raw = response.json()
        for row in raw["counts"]:
            assert set(row.keys()) == {"cell_id", "source", "license", "count"}

        body = SightingsResponse.model_validate(raw)
        for count in body.counts:
            assert count.cell_id in servable_cell_ids
            assert count.count >= 1

    def test_a_narrower_since_never_returns_more_than_a_wider_one(
        self, client: httpx.Client
    ) -> None:
        narrow = client.get("/sightings", params={"species": "porcini", "since": "2026-09-01"})
        wide = client.get("/sightings", params={"species": "porcini", "since": "2020-01-01"})
        narrow_total = sum(row["count"] for row in narrow.json()["counts"])
        wide_total = sum(row["count"] for row in wide.json()["counts"])
        assert narrow_total <= wide_total


class TestOpenAPISurface:
    def test_every_planned_route_is_documented(self, client: httpx.Client) -> None:
        schema = client.get("/openapi.json").json()
        assert set(schema["paths"]) >= {
            "/scores",
            "/spot",
            "/cells/{cell_id}",
            "/hotspots",
            "/sightings",
        }
