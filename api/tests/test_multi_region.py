"""Multi-region API contract: ``region`` query param, ``/regions``, ``/overview``."""

from datetime import date

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.models import OverviewResponse, RegionsResponse, ScoresResponse

client = TestClient(app)

DATA_ROUTES = (
    ("/scores", {"species": "combined"}),
    ("/factors", {"species": "porcini"}),
    ("/forest-types", {}),
    ("/spot", {"lat": 43.85, "lon": 11.73}),
    ("/hotspots", {"species": "combined"}),
    ("/sightings", {"species": "porcini"}),
    ("/status", {}),
    ("/comuni", {}),
    ("/history/seasons", {}),
    ("/outlook", {"species": "porcini"}),
    ("/species", {}),
)


class TestRegionParameter:
    @pytest.mark.parametrize(("path", "params"), DATA_ROUTES)
    def test_defaults_to_tuscany(self, path: str, params: dict[str, object]) -> None:
        bare = client.get(path, params=params)
        with_default = client.get(path, params={**params, "region": "tuscany"})
        assert bare.status_code == 200
        assert with_default.status_code == 200
        assert bare.json() == with_default.json()

    @pytest.mark.parametrize(("path", "params"), DATA_ROUTES)
    def test_unknown_region_is_a_problem_404(self, path: str, params: dict[str, object]) -> None:
        response = client.get(path, params={**params, "region": "not_a_region"})
        assert response.status_code == 404
        assert response.headers["content-type"].startswith("application/problem+json")
        body = response.json()
        assert body["status"] == 404
        assert body["title"]
        assert "not_a_region" in body["detail"]

    def test_cell_detail_takes_region(self) -> None:
        cell_id = client.get("/scores", params={"species": "combined"}).json()["cells"][0][
            "cell_id"
        ]
        ok = client.get(f"/cells/{cell_id}", params={"region": "tuscany"})
        bad = client.get(f"/cells/{cell_id}", params={"region": "atlantis"})
        assert ok.status_code == 200
        assert bad.status_code == 404
        assert bad.headers["content-type"].startswith("application/problem+json")

    def test_season_map_takes_region(self) -> None:
        year = date.today().year
        ok = client.get(
            f"/history/season/{year}", params={"species": "porcini", "region": "tuscany"}
        )
        bad = client.get(
            f"/history/season/{year}", params={"species": "porcini", "region": "atlantis"}
        )
        assert ok.status_code == 200
        assert bad.status_code == 404


class TestRegionsEndpoint:
    def test_lists_served_fixture_regions(self) -> None:
        response = client.get("/regions")
        assert response.status_code == 200
        body = RegionsResponse.model_validate(response.json())
        ids = [region.id for region in body.regions]
        assert ids == ["tuscany", "umbria"]
        by_id = {region.id: region for region in body.regions}
        assert by_id["tuscany"].name == {"it": "Toscana", "en": "Tuscany"}
        assert by_id["umbria"].name == {"it": "Umbria", "en": "Umbria"}
        assert by_id["tuscany"].bbox_wgs84 == [9.68, 42.23, 12.38, 44.48]
        assert by_id["umbria"].bbox_wgs84 == [11.89, 42.36, 13.27, 43.62]
        assert by_id["tuscany"].history_start == date(2016, 1, 1)
        assert by_id["umbria"].history_start == date(2016, 1, 1)
        for region in body.regions:
            assert set(region.species) == {"porcini", "ovoli", "gallinacci"}
            assert region.updated_at is not None


class TestOverviewEndpoint:
    def test_aggregates_every_served_region(self) -> None:
        response = client.get("/overview", params={"species": "porcini"})
        assert response.status_code == 200
        body = OverviewResponse.model_validate(response.json())
        assert body.species == "porcini"
        assert body.good_score == pytest.approx(0.6)
        assert [row.region for row in body.regions] == ["tuscany", "umbria"]
        for row in body.regions:
            assert 0.0 <= row.mean_score <= 1.0
            assert 0.0 <= row.good_share <= 1.0
            assert row.updated_at is not None

    def test_defaults_species_date_and_caches_like_scores(self) -> None:
        overview = client.get("/overview", params={"species": "combined"})
        scores = client.get("/scores", params={"species": "combined"})
        assert overview.status_code == 200
        assert overview.headers["cache-control"] == scores.headers["cache-control"]

    def test_unknown_region_is_not_a_query_here(self) -> None:
        # /overview is national: no region filter; an unknown species still 422s.
        response = client.get("/overview", params={"species": "amanita_phalloides"})
        assert response.status_code == 422


class TestFixtureRouting:
    def test_scores_differ_between_fixture_regions(self) -> None:
        tuscany = ScoresResponse.model_validate(
            client.get("/scores", params={"species": "combined", "region": "tuscany"}).json()
        )
        umbria = ScoresResponse.model_validate(
            client.get("/scores", params={"species": "combined", "region": "umbria"}).json()
        )
        assert {cell.cell_id for cell in tuscany.cells} != {cell.cell_id for cell in umbria.cells}
        assert all(cell.cell_id.startswith("1kmN") for cell in umbria.cells)
