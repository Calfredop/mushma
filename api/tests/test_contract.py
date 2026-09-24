"""Contract tests every endpoint must pass (M4 plan, item 5). These parse responses with the same
Pydantic models the API declares, and don't assume any particular storage's cell set -- they
discover it from the responses themselves. So pointing MUSHMA_CONTRACT_BASE_URL at a deployed
api/ runs the identical assertions against real production data (M4-api.md item 9: verify a
deployment by running this suite against it)."""

import math

import httpx
import pytest

from api.grid.habitats import load_vocabulary
from api.models import (
    CellDetailResponse,
    ComuniResponse,
    FactorsResponse,
    ForestTypesResponse,
    HotspotsResponse,
    OutlookResponse,
    PlausibleSpeciesResponse,
    ScoresResponse,
    SeasonMapResponse,
    SeasonsResponse,
    SightingsResponse,
    StatusResponse,
)
from api.timeutil import today_rome


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


class TestFactors:
    @pytest.mark.parametrize("species", ["porcini", "ovoli", "gallinacci"])
    def test_every_scored_cell_has_a_value_per_chip(
        self, client: httpx.Client, species: str
    ) -> None:
        response = client.get("/factors", params={"species": species})
        assert response.status_code == 200
        body = FactorsResponse.model_validate(response.json())
        assert body.species == species
        assert body.factors, "no factor chips"
        ids = [chip.id for chip in body.factors]
        assert len(ids) == len(set(ids))
        roles = [chip.role for chip in body.factors]
        assert roles == sorted(roles, key=["gate", "driver", "stopper"].index)
        scores = client.get("/scores", params={"species": species, "date": str(body.date)})
        assert {cell.cell_id for cell in body.cells} == {
            cell["cell_id"] for cell in scores.json()["cells"]
        }
        for cell in body.cells:
            assert len(cell.values) == len(body.factors)
            assert any(value is not None for value in cell.values)

    def test_the_combined_score_has_no_factors(self, client: httpx.Client) -> None:
        response = client.get("/factors", params={"species": "combined"})
        assert response.status_code == 422

    def test_404s_outside_the_stored_factors(self, client: httpx.Client) -> None:
        response = client.get("/factors", params={"species": "porcini", "date": "2000-01-01"})
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
            # A woodland cell's forest types, largest first, sharing out its wooded area.
            fractions = [share.fraction for share in detail.habitats]
            assert fractions, "a woodland cell has at least one forest type"
            assert fractions == sorted(fractions, reverse=True)
            assert sum(fractions) == pytest.approx(1.0, abs=0.01)
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
                    for f in day.factors:
                        assert f.role is not None
                        assert f.rule is not None
                        if f.input is not None:
                            assert f.unit is not None

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

    def test_an_until_never_returns_more_than_no_until(self, client: httpx.Client) -> None:
        params = {"species": "porcini", "since": "2020-01-01"}
        bounded = client.get("/sightings", params={**params, "until": "2020-01-01"})
        open_ended = client.get("/sightings", params=params)
        assert bounded.status_code == 200
        bounded_total = sum(row["count"] for row in bounded.json()["counts"])
        open_total = sum(row["count"] for row in open_ended.json()["counts"])
        assert bounded_total <= open_total


class TestForestTypes:
    def test_covers_every_cell_scores_can_serve_today(
        self, client: httpx.Client, servable_cell_ids: set[str]
    ) -> None:
        # Static grid data: it can cover more than today's scored window (e.g. a cell that
        # hasn't been (re)scored yet still has a forest type), but never less.
        response = client.get("/forest-types")
        assert response.status_code == 200
        body = ForestTypesResponse.model_validate(response.json())
        assert servable_cell_ids <= {cell.cell_id for cell in body.cells}
        known = set(load_vocabulary().habitats)
        for cell in body.cells:
            assert cell.habitat in known

    def test_cell_ids_are_unique(self, client: httpx.Client) -> None:
        response = client.get("/forest-types")
        cell_ids = [cell["cell_id"] for cell in response.json()["cells"]]
        assert len(cell_ids) == len(set(cell_ids))


@pytest.fixture
def comuni(client: httpx.Client) -> ComuniResponse:
    response = client.get("/comuni")
    assert response.status_code == 200
    return ComuniResponse.model_validate(response.json())


class TestComuni:
    def test_lists_comuni_with_woodland_by_name(self, comuni: ComuniResponse) -> None:
        assert comuni.comuni, "no comuni"
        codes = [c.code for c in comuni.comuni]
        assert len(codes) == len(set(codes))
        names = [c.name for c in comuni.comuni]
        assert names == sorted(names, key=str.casefold)


def _check_season(season, year_days: int = 366) -> None:
    assert season.window.start <= season.window.end
    assert season.window.start.year == season.year == season.window.end.year
    assert season.through.year == season.year
    if season.weather_through is not None:
        assert season.weather_through <= season.through
    if season.rain is None:
        assert season.weather_through is None
    assert 0 <= season.good_days <= year_days
    if season.peak_date is not None:
        assert season.peak_date.year == season.year
        assert season.peak_share > 0
    months = [m.month for m in season.months]
    assert months == sorted(set(months))


class TestSeasons:
    def test_the_region_by_default(self, client: httpx.Client) -> None:
        response = client.get("/history/seasons")
        assert response.status_code == 200
        body = SeasonsResponse.model_validate(response.json())
        assert body.species == "combined"
        assert body.area.kind == "region"
        assert body.area.code is None
        years = [s.year for s in body.seasons]
        assert years, "no seasons"
        assert years == sorted(set(years))
        for season in body.seasons:
            _check_season(season)

    @pytest.mark.parametrize("species", ["porcini", "ovoli", "gallinacci", "combined"])
    def test_one_comune(self, client: httpx.Client, comuni: ComuniResponse, species: str) -> None:
        comune = comuni.comuni[0]
        response = client.get(
            "/history/seasons", params={"species": species, "comune": comune.code}
        )
        assert response.status_code == 200
        body = SeasonsResponse.model_validate(response.json())
        assert body.species == species
        assert (body.area.kind, body.area.code, body.area.name) == (
            "comune",
            comune.code,
            comune.name,
        )
        for season in body.seasons:
            _check_season(season)

    def test_an_unknown_comune_404s(self, client: httpx.Client) -> None:
        response = client.get("/history/seasons", params={"comune": "not-a-comune"})
        assert response.status_code == 404

    def test_rejects_an_unknown_species(self, client: httpx.Client) -> None:
        response = client.get("/history/seasons", params={"species": "amanita_phalloides"})
        assert response.status_code == 422


class TestSeasonMap:
    def test_a_stored_season(self, client: httpx.Client, comuni: ComuniResponse) -> None:
        seasons = SeasonsResponse.model_validate(client.get("/history/seasons").json()).seasons
        year = seasons[-1].year
        response = client.get(f"/history/season/{year}", params={"species": "porcini"})
        assert response.status_code == 200
        body = SeasonMapResponse.model_validate(response.json())
        assert (body.year, body.species) == (year, "porcini")
        assert body.cells, "no cells"
        assert len({c.cell_id for c in body.cells}) == len(body.cells)
        ranked = [c.good_days for c in body.comuni]
        assert ranked == sorted(ranked, reverse=True)
        assert {c.code for c in body.comuni} <= {c.code for c in comuni.comuni}

    def test_a_season_not_stored_404s(self, client: httpx.Client) -> None:
        response = client.get("/history/season/1900", params={"species": "porcini"})
        assert response.status_code == 404


class TestOutlook:
    @pytest.mark.parametrize("species", ["porcini", "ovoli", "gallinacci"])
    def test_periods_follow_each_other_inside_the_season(
        self, client: httpx.Client, species: str
    ) -> None:
        response = client.get("/outlook", params={"species": species})
        assert response.status_code == 200
        body = OutlookResponse.model_validate(response.json())
        assert body.species == species
        assert body.area.kind == "region"
        assert body.rain_lead.min_days <= body.rain_lead.max_days
        assert body.rain_tilt.drier_pct < 100 < body.rain_tilt.wetter_pct
        previous_end = None
        for period in body.periods:
            assert period.start <= period.end
            assert body.window.start <= period.start and period.end <= body.window.end
            if previous_end is not None:
                assert period.start > previous_end
            previous_end = period.end
            assert period.past_good_years <= period.past_years
            if period.lead_rain_pct is None:
                assert period.outlook == "unknown"

    def test_one_comune(self, client: httpx.Client, comuni: ComuniResponse) -> None:
        comune = comuni.comuni[0]
        response = client.get("/outlook", params={"species": "porcini", "comune": comune.code})
        assert response.status_code == 200
        body = OutlookResponse.model_validate(response.json())
        assert body.area.code == comune.code

    def test_the_combined_score_has_no_outlook(self, client: httpx.Client) -> None:
        response = client.get("/outlook", params={"species": "combined"})
        assert response.status_code == 422

    def test_an_unknown_comune_404s(self, client: httpx.Client) -> None:
        response = client.get("/outlook", params={"species": "porcini", "comune": "nope"})
        assert response.status_code == 404


class TestSpecies:
    def _check(self, body: PlausibleSpeciesResponse) -> None:
        assert [s.species for s in body.species] == ["porcini", "ovoli", "gallinacci"]
        for profile in body.species:
            assert profile.taxa, f"{profile.species} has no taxa"
            # A group is plausible wherever any of its taxa is.
            assert profile.fit_share >= max(t.fit_share for t in profile.taxa) - 1e-9
            years = [s.year for s in profile.seasons]
            assert years == sorted(set(years))
            for taxon in profile.taxa:
                assert taxon.key.startswith(f"{profile.species}_")
                assert [s.year for s in taxon.seasons] == sorted({s.year for s in taxon.seasons})

    def test_the_region_by_default(self, client: httpx.Client) -> None:
        response = client.get("/species")
        assert response.status_code == 200
        body = PlausibleSpeciesResponse.model_validate(response.json())
        assert body.area.kind == "region"
        self._check(body)

    def test_one_comune(self, client: httpx.Client, comuni: ComuniResponse) -> None:
        comune = comuni.comuni[0]
        response = client.get("/species", params={"comune": comune.code})
        assert response.status_code == 200
        body = PlausibleSpeciesResponse.model_validate(response.json())
        assert (body.area.code, body.area.name) == (comune.code, comune.name)
        self._check(body)

    def test_an_unknown_comune_404s(self, client: httpx.Client) -> None:
        response = client.get("/species", params={"comune": "nope"})
        assert response.status_code == 404


class TestStatus:
    def test_scored_through_covers_at_least_today(self, client: httpx.Client) -> None:
        response = client.get("/status")
        assert response.status_code == 200
        body = StatusResponse.model_validate(response.json())
        assert body.scored_through >= today_rome()


class TestOpenAPISurface:
    def test_every_planned_route_is_documented(self, client: httpx.Client) -> None:
        schema = client.get("/openapi.json").json()
        assert set(schema["paths"]) >= {
            "/scores",
            "/factors",
            "/spot",
            "/cells/{cell_id}",
            "/hotspots",
            "/sightings",
            "/status",
            "/comuni",
            "/history/seasons",
            "/history/season/{year}",
            "/outlook",
            "/species",
        }
