from datetime import date as Date
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse

from api.cache import DAILY, SHORT_LIVED, cache_control_for_date
from api.model.rules import DEFAULT_REGION
from api.models import (
    CellDetailResponse,
    ComuniResponse,
    FactorsResponse,
    ForestTypesResponse,
    HotspotsResponse,
    OutlookResponse,
    OverviewResponse,
    PlausibleSpeciesResponse,
    RegionsResponse,
    ScoresResponse,
    SeasonMapResponse,
    SeasonsResponse,
    SightingsResponse,
    StatusResponse,
)
from api.regions import RegionNotServed
from api.registry import get_overview_response, get_regions_response, repository_for
from api.repository import (
    AreaNotFound,
    CellNotFound,
    DateOutOfRange,
    HistoryUnavailable,
    ScoresRepository,
    ScoresUnavailable,
    SeasonNotFound,
)
from api.response_cache import NATIONAL_REGION, cached_model
from api.species import Species, SpeciesOrCombined
from api.timeutil import today_rome

SIGHTINGS_DEFAULT_LOOKBACK_DAYS = 365

RegionQuery = Annotated[
    str,
    Query(
        description="Italian region slug with underscores (e.g. emilia_romagna); "
        "defaults to tuscany so installed PWAs keep working"
    ),
]


def get_repository(
    region: RegionQuery = DEFAULT_REGION,
) -> ScoresRepository:
    return repository_for(region)


Repository = Annotated[ScoresRepository, Depends(get_repository)]

router = APIRouter()


def problem_response(status: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"type": "about:blank", "title": title, "status": status, "detail": detail},
        media_type="application/problem+json",
    )


def region_problem(exc: RegionNotServed) -> JSONResponse:
    return problem_response(404, "Region not found", str(exc))


async def region_not_served_handler(_request: Request, exc: RegionNotServed) -> JSONResponse:
    return region_problem(exc)


@router.get(
    "/regions",
    response_model=RegionsResponse,
    summary="Served regions (id, names, bbox, history start, species, freshness)",
)
def get_regions(response: Response) -> RegionsResponse:
    result = cached_model(NATIONAL_REGION, "regions", RegionsResponse, get_regions_response)
    response.headers["Cache-Control"] = SHORT_LIVED
    return result


@router.get(
    "/overview",
    response_model=OverviewResponse,
    summary="Per served region: mean score and share of woodland at or above good_score",
)
def get_overview(
    response: Response,
    species: Annotated[SpeciesOrCombined, Query()] = "combined",
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
) -> OverviewResponse:
    target_date = date or today_rome()

    def compute() -> OverviewResponse:
        try:
            return get_overview_response(species, target_date)
        except DateOutOfRange as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    result = cached_model(
        NATIONAL_REGION,
        "overview",
        OverviewResponse,
        compute,
        species=species,
        date=target_date,
    )
    response.headers["Cache-Control"] = cache_control_for_date(target_date)
    return result


@router.get(
    "/scores",
    response_model=ScoresResponse,
    summary="Whole-region grid of conditions scores for one species (or combined)",
    responses={404: {"description": "date outside the served window, or unknown region"}},
)
def get_scores(
    repository: Repository,
    response: Response,
    species: Annotated[SpeciesOrCombined, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
) -> ScoresResponse:
    target_date = date or today_rome()

    def compute() -> ScoresResponse:
        try:
            return repository.get_scores(species, target_date)
        except DateOutOfRange as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    result = cached_model(
        repository.region,
        "scores",
        ScoresResponse,
        compute,
        species=species,
        date=target_date,
    )
    response.headers["Cache-Control"] = cache_control_for_date(target_date)
    return result


@router.get(
    "/factors",
    response_model=FactorsResponse,
    summary="Analysis mode: every factor behind one species' conditions score, per woodland cell",
    responses={404: {"description": "no factors stored for that day, or unknown region"}},
)
def get_factors(
    repository: Repository,
    response: Response,
    species: Annotated[Species, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
) -> FactorsResponse:
    target_date = date or today_rome()

    def compute() -> FactorsResponse:
        try:
            return repository.get_factors(species, target_date)
        except DateOutOfRange as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    result = cached_model(
        repository.region,
        "factors",
        FactorsResponse,
        compute,
        species=species,
        date=target_date,
    )
    response.headers["Cache-Control"] = cache_control_for_date(target_date)
    return result


@router.get(
    "/forest-types",
    response_model=ForestTypesResponse,
    summary="Analysis mode's Bosco layer: every woodland cell's dominant forest type",
)
def get_forest_types(repository: Repository, response: Response) -> ForestTypesResponse:
    result = cached_model(
        repository.region, "forest-types", ForestTypesResponse, repository.get_forest_types
    )
    response.headers["Cache-Control"] = DAILY
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
    result = cached_model(
        repository.region,
        "spot",
        CellDetailResponse,
        lambda: repository.get_spot(lat, lon),
        lat=lat,
        lon=lon,
    )
    response.headers["Cache-Control"] = SHORT_LIVED  # always today + forecast, never a past date
    return result


@router.get(
    "/cells/{cell_id}",
    response_model=CellDetailResponse,
    summary="Score, 7-day outlook and factor breakdown for every species in one cell",
    responses={404: {"description": "unknown cell id or region"}},
)
def get_cell(repository: Repository, response: Response, cell_id: str) -> CellDetailResponse:
    def compute() -> CellDetailResponse:
        try:
            return repository.get_cell_detail(cell_id)
        except CellNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    result = cached_model(repository.region, "cell", CellDetailResponse, compute, cell_id=cell_id)
    response.headers["Cache-Control"] = SHORT_LIVED  # always today + forecast, never a past date
    return result


@router.get(
    "/hotspots",
    response_model=HotspotsResponse,
    summary="Ranked clusters of high-scoring cells, with nearby recent sightings",
    responses={404: {"description": "date outside the served window, or unknown region"}},
)
def get_hotspots(
    repository: Repository,
    response: Response,
    species: Annotated[SpeciesOrCombined, Query()],
    date: Annotated[Date | None, Query(description="defaults to today, Europe/Rome")] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
) -> HotspotsResponse:
    target_date = date or today_rome()

    def compute() -> HotspotsResponse:
        try:
            return repository.get_hotspots(species, target_date, limit)
        except DateOutOfRange as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    result = cached_model(
        repository.region,
        "hotspots",
        HotspotsResponse,
        compute,
        species=species,
        date=target_date,
        limit=limit,
    )
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
    until: Annotated[
        Date | None, Query(description="last day included; defaults to no limit")
    ] = None,
) -> SightingsResponse:
    since_date = since or (today_rome() - timedelta(days=SIGHTINGS_DEFAULT_LOOKBACK_DAYS))
    result = cached_model(
        repository.region,
        "sightings",
        SightingsResponse,
        lambda: repository.get_sightings(species, since_date, until),
        species=species,
        since=since_date,
        until=until,
    )
    response.headers["Cache-Control"] = SHORT_LIVED  # counts grow as new sightings are ingested
    return result


@router.get(
    "/status",
    response_model=StatusResponse,
    summary="Data freshness: the latest scored day, when it was generated, and the rules version",
    responses={
        503: {"description": "the pipeline has never scored anything yet"},
        404: {"description": "unknown or unserved region"},
    },
)
def get_status(repository: Repository, response: Response) -> StatusResponse:
    # Uncached on purpose: this is how the app learns the pipeline has finished.
    try:
        result = repository.get_status()
    except ScoresUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    response.headers["Cache-Control"] = SHORT_LIVED
    return result


# --- Time views (M6) ---------------------------------------------------------------------------
# Tables built by api.history.build; until they exist the routes answer 503.

Comune = Annotated[
    str | None, Query(description="ISTAT comune code (see /comuni); omit for the whole region")
]
_HISTORY_ERRORS = {503: {"description": "history not built yet"}}


@router.get(
    "/comuni",
    response_model=ComuniResponse,
    summary="Comuni with woodland, for the season and outlook views",
    responses=_HISTORY_ERRORS,
)
def get_comuni(repository: Repository, response: Response) -> ComuniResponse:
    def compute() -> ComuniResponse:
        try:
            return repository.get_comuni()
        except HistoryUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    result = cached_model(repository.region, "comuni", ComuniResponse, compute)
    response.headers["Cache-Control"] = DAILY
    return result


@router.get(
    "/history/seasons",
    response_model=SeasonsResponse,
    summary="Every stored season for the region or a comune: good days, weather vs normal, "
    "sightings",
    responses={404: {"description": "unknown comune or region"}, **_HISTORY_ERRORS},
)
def get_seasons(
    repository: Repository,
    response: Response,
    comune: Comune = None,
    species: Annotated[SpeciesOrCombined, Query()] = "combined",
) -> SeasonsResponse:
    def compute() -> SeasonsResponse:
        try:
            return repository.get_seasons(species, comune)
        except AreaNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except HistoryUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    result = cached_model(
        repository.region,
        "seasons",
        SeasonsResponse,
        compute,
        species=species,
        comune=comune,
    )
    response.headers["Cache-Control"] = SHORT_LIVED  # this season grows every day
    return result


@router.get(
    "/history/season/{year}",
    response_model=SeasonMapResponse,
    summary="One season on the map: good days per woodland cell, comuni ranked by them",
    responses={404: {"description": "season not stored, or unknown region"}, **_HISTORY_ERRORS},
)
def get_season_map(
    repository: Repository,
    response: Response,
    year: int,
    species: Annotated[SpeciesOrCombined, Query()],
) -> SeasonMapResponse:
    def compute() -> SeasonMapResponse:
        try:
            return repository.get_season_map(year, species)
        except SeasonNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except HistoryUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    result = cached_model(
        repository.region,
        "season-map",
        SeasonMapResponse,
        compute,
        year=year,
        species=species,
    )
    # A past season only changes when history is re-scored, which is rare but real (a finished
    # backfill, new rules): a day, not forever.
    response.headers["Cache-Control"] = DAILY if year < today_rome().year else SHORT_LIVED
    return result


@router.get(
    "/outlook",
    response_model=OutlookResponse,
    summary="The season so far and an outlook (not a forecast) for the weeks and months ahead",
    responses={404: {"description": "unknown comune or region"}, **_HISTORY_ERRORS},
)
def get_outlook(
    repository: Repository,
    response: Response,
    species: Annotated[Species, Query()],
    comune: Comune = None,
) -> OutlookResponse:
    def compute() -> OutlookResponse:
        try:
            return repository.get_outlook(species, comune)
        except AreaNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except HistoryUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    result = cached_model(
        repository.region,
        "outlook",
        OutlookResponse,
        compute,
        species=species,
        comune=comune,
    )
    response.headers["Cache-Control"] = SHORT_LIVED
    return result


@router.get(
    "/species",
    response_model=PlausibleSpeciesResponse,
    summary="Plausible species for the region or a comune: habitat fit and good days per season, "
    "per species and taxon",
    responses={404: {"description": "unknown comune or region"}, **_HISTORY_ERRORS},
)
def get_species(
    repository: Repository, response: Response, comune: Comune = None
) -> PlausibleSpeciesResponse:
    def compute() -> PlausibleSpeciesResponse:
        try:
            return repository.get_species(comune)
        except AreaNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except HistoryUnavailable as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    result = cached_model(
        repository.region, "species", PlausibleSpeciesResponse, compute, comune=comune
    )
    response.headers["Cache-Control"] = SHORT_LIVED  # this season grows every day
    return result
