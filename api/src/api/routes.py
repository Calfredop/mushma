import os
from datetime import date as Date
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from api.models import CellDetailResponse, HotspotsResponse, ScoresResponse, SightingsResponse
from api.repository import CellNotFound, DateOutOfRange, ScoresRepository
from api.species import Species, SpeciesOrCombined
from api.timeutil import today_rome

SIGHTINGS_DEFAULT_LOOKBACK_DAYS = 365


def get_repository() -> ScoresRepository:
    if os.environ.get("MUSHMA_FIXTURES") == "1":
        from api.fixtures.repository import FixtureRepository

        return FixtureRepository()
    raise HTTPException(
        status_code=503,
        detail=(
            "Real storage isn't wired up yet (M4-api.md). "
            "Set MUSHMA_FIXTURES=1 to run against fixture data."
        ),
    )


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
    species: Annotated[SpeciesOrCombined, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
) -> ScoresResponse:
    try:
        return repository.get_scores(species, date or today_rome())
    except DateOutOfRange as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/spot",
    response_model=CellDetailResponse,
    summary="Score, 7-day outlook and factor breakdown for every species at a point",
)
def get_spot(
    repository: Repository,
    lat: Annotated[float, Query(ge=-90, le=90)],
    lon: Annotated[float, Query(ge=-180, le=180)],
) -> CellDetailResponse:
    return repository.get_spot(lat, lon)


@router.get(
    "/cells/{cell_id}",
    response_model=CellDetailResponse,
    summary="Score, 7-day outlook and factor breakdown for every species in one cell",
    responses={404: {"description": "unknown cell id"}},
)
def get_cell(repository: Repository, cell_id: str) -> CellDetailResponse:
    try:
        return repository.get_cell_detail(cell_id)
    except CellNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/hotspots",
    response_model=HotspotsResponse,
    summary="Ranked clusters of high-scoring cells, with nearby recent sightings",
    responses={404: {"description": "date outside the served window"}},
)
def get_hotspots(
    repository: Repository,
    species: Annotated[SpeciesOrCombined, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> HotspotsResponse:
    try:
        return repository.get_hotspots(species, date or today_rome(), limit)
    except DateOutOfRange as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/sightings",
    response_model=SightingsResponse,
    summary="Public sighting counts per cell (never coordinates)",
)
def get_sightings(
    repository: Repository,
    species: Annotated[Species, Query()],
    since: Annotated[Date | None, Query(description="defaults to one year ago")] = None,
) -> SightingsResponse:
    since_date = since or (today_rome() - timedelta(days=SIGHTINGS_DEFAULT_LOOKBACK_DAYS))
    return repository.get_sightings(species, since_date)
