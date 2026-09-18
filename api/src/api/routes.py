import os
from datetime import date as Date
from datetime import timedelta
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from api.cache import SHORT_LIVED, cache_control_for_date
from api.grid.sources import data_dir
from api.models import CellDetailResponse, HotspotsResponse, ScoresResponse, SightingsResponse
from api.repository import CellNotFound, DateOutOfRange, ScoresRepository
from api.species import Species, SpeciesOrCombined
from api.timeutil import today_rome

SIGHTINGS_DEFAULT_LOOKBACK_DAYS = 365


@lru_cache
def _live_repository() -> ScoresRepository:
    # Cached: loading the rule config (YAML + validation) and the grid on every request would be
    # wasted work -- both are read-only for the process's lifetime.
    from api.live.repository import LiveRepository

    return LiveRepository(data_dir())


def get_repository() -> ScoresRepository:
    if os.environ.get("MUSHMA_FIXTURES") == "1":
        from api.fixtures.repository import FixtureRepository

        return FixtureRepository()
    return _live_repository()


Repository = Annotated[ScoresRepository, Depends(get_repository)]

router = APIRouter()


@router.get(
    "/scores",
    response_model=ScoresResponse,
    summary="Whole-region grid of conditions scores for one species (or combined)",
    responses={404: {"description": "date outside the served window"}},
)
def get_scores(
    repository: Repository,
    response: Response,
    species: Annotated[SpeciesOrCombined, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
) -> ScoresResponse:
    target_date = date or today_rome()
    try:
        result = repository.get_scores(species, target_date)
    except DateOutOfRange as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    response.headers["Cache-Control"] = cache_control_for_date(target_date)
    return result


@router.get(
    "/spot",
    response_model=CellDetailResponse,
    summary="Score, 7-day outlook and factor breakdown for every species at a point",
)
def get_spot(
    repository: Repository,
    response: Response,
    lat: Annotated[float, Query(ge=-90, le=90)],
    lon: Annotated[float, Query(ge=-180, le=180)],
) -> CellDetailResponse:
    result = repository.get_spot(lat, lon)
    response.headers["Cache-Control"] = SHORT_LIVED  # always today + forecast, never a past date
    return result


@router.get(
    "/cells/{cell_id}",
    response_model=CellDetailResponse,
    summary="Score, 7-day outlook and factor breakdown for every species in one cell",
    responses={404: {"description": "unknown cell id"}},
)
def get_cell(repository: Repository, response: Response, cell_id: str) -> CellDetailResponse:
    try:
        result = repository.get_cell_detail(cell_id)
    except CellNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    response.headers["Cache-Control"] = SHORT_LIVED  # always today + forecast, never a past date
    return result


@router.get(
    "/hotspots",
    response_model=HotspotsResponse,
    summary="Ranked clusters of high-scoring cells, with nearby recent sightings",
    responses={404: {"description": "date outside the served window"}},
)
def get_hotspots(
    repository: Repository,
    response: Response,
    species: Annotated[SpeciesOrCombined, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> HotspotsResponse:
    target_date = date or today_rome()
    try:
        result = repository.get_hotspots(species, target_date, limit)
    except DateOutOfRange as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    response.headers["Cache-Control"] = cache_control_for_date(target_date)
    return result


@router.get(
    "/sightings",
    response_model=SightingsResponse,
    summary="Public sighting counts per cell (never coordinates)",
)
def get_sightings(
    repository: Repository,
    response: Response,
    species: Annotated[Species, Query()],
    since: Annotated[Date | None, Query(description="defaults to one year ago")] = None,
) -> SightingsResponse:
    since_date = since or (today_rome() - timedelta(days=SIGHTINGS_DEFAULT_LOOKBACK_DAYS))
    result = repository.get_sightings(species, since_date)
    response.headers["Cache-Control"] = SHORT_LIVED  # counts grow as new sightings are ingested
    return result
