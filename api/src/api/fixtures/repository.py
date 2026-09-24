from datetime import UTC, date, datetime, timedelta

from api.fixtures.cells import CELLS, CellSpec
from api.fixtures.generator import WINDOW_OFFSETS, combined_score, score_and_factors
from api.fixtures.hotspots import build_hotspots
from api.fixtures.scoring import FACTOR_SPECS, FactorResult
from api.fixtures.sightings import LICENSES, counts_between, recent_sightings_total
from api.fixtures.timeviews import FixtureTimeViews
from api.fixtures.umbria_cells import UMBRIA_CELLS
from api.history.config import load_history_config
from api.model.rules import DEFAULT_REGION
from api.models import (
    CellDetailResponse,
    CellFactors,
    CellForestType,
    ComuniResponse,
    DayScore,
    FactorBreakdown,
    FactorChip,
    FactorsResponse,
    ForestTypesResponse,
    GridCellScore,
    HabitatShare,
    Hotspot,
    HotspotsResponse,
    OutlookResponse,
    OverviewResponse,
    Place,
    PlausibleSpeciesResponse,
    RegionInfo,
    RegionOverview,
    RegionsResponse,
    ScoresResponse,
    SeasonMapResponse,
    SeasonsResponse,
    SightingCount,
    SightingsResponse,
    SpeciesForecast,
    StatusResponse,
)
from api.regions import (
    FIXTURE_REGIONS,
    cached_region_config,
    history_start_date,
    species_for_region,
)
from api.repository import CellNotFound, DateOutOfRange
from api.species import SPECIES, Species, SpeciesOrCombined
from api.timeutil import today_rome

WINDOW_START = WINDOW_OFFSETS.start  # -6
WINDOW_END = WINDOW_OFFSETS.stop - 1  # 7
FORECAST_OFFSETS = range(0, 8)  # today + 7-day outlook (PRD -> Features 2)
HOTSPOT_SIGHTINGS_WINDOW_DAYS = 90
# Stable across requests so ``/status`` without ``region`` matches ``?region=tuscany``.
FIXTURE_UPDATED_AT = datetime(2026, 9, 18, 6, 0, 0, tzinfo=UTC)

CELLS_BY_REGION: dict[str, tuple[CellSpec, ...]] = {
    DEFAULT_REGION: CELLS,
    "umbria": UMBRIA_CELLS,
}


def cells_for_region(region: str) -> tuple[CellSpec, ...]:
    try:
        return CELLS_BY_REGION[region]
    except KeyError as exc:
        raise CellNotFound(region) from exc


def _cell_by_id(cells: tuple[CellSpec, ...], cell_id: str) -> CellSpec:
    for cell in cells:
        if cell.id == cell_id:
            return cell
    raise CellNotFound(cell_id)


def _nearest_cell(cells: tuple[CellSpec, ...], lat: float, lon: float) -> CellSpec:
    return min(cells, key=lambda cell: (cell.lat - lat) ** 2 + (cell.lon - lon) ** 2)


def _offset_for(target_date: date) -> int:
    today = today_rome()
    offset = (target_date - today).days
    if offset < WINDOW_START or offset > WINDOW_END:
        raise DateOutOfRange(
            target_date, today + timedelta(days=WINDOW_START), today + timedelta(days=WINDOW_END)
        )
    return offset


def _score_for(cell: CellSpec, species: SpeciesOrCombined, target_date: date, offset: int) -> float:
    if species == "combined":
        return combined_score(cell, target_date, offset)
    return score_and_factors(cell, species, target_date, offset)[0]


def _to_breakdown(factors: list[FactorResult]) -> list[FactorBreakdown]:
    return [
        FactorBreakdown(
            key=f.key,
            i18n_key=f.i18n_key,
            value=f.value,
            contribution=f.contribution,
            role=f.role,
            weight=f.weight,
            input=f.input,
            unit=f.unit,
            days_ago=f.days_ago,
            rule=f.rule,
        )
        for f in factors
    ]


class FixtureRepository:
    def __init__(self, region: str = DEFAULT_REGION) -> None:
        self.region = region
        self.cells = cells_for_region(region)
        self._time_views = FixtureTimeViews(region_id=region, cells=self.cells)

    def get_scores(self, species: SpeciesOrCombined, target_date: date) -> ScoresResponse:
        offset = _offset_for(target_date)
        cells = [
            GridCellScore(
                cell_id=cell.id,
                lon=cell.lon,
                lat=cell.lat,
                score=_score_for(cell, species, target_date, offset),
            )
            for cell in self.cells
        ]
        return ScoresResponse(species=species, date=target_date, cells=cells)

    def get_factors(self, species: Species, target_date: date) -> FactorsResponse:
        # One stand-in rule file per species, so every cell is won by it.
        offset = _offset_for(target_date)
        chips = [
            FactorChip(id=spec.id, i18n_key=spec.i18n_key, role=spec.role)
            for spec in FACTOR_SPECS[species]
        ]
        cells = [
            CellFactors(
                cell_id=cell.id,
                lon=cell.lon,
                lat=cell.lat,
                values=[
                    round(f.value, 3)
                    for f in score_and_factors(cell, species, target_date, offset)[1]
                ],
            )
            for cell in self.cells
        ]
        return FactorsResponse(species=species, date=target_date, factors=chips, cells=cells)

    def _forecast(self, cell: CellSpec) -> CellDetailResponse:
        today = today_rome()
        species_forecasts = []
        for species in SPECIES:
            days = []
            for offset in FORECAST_OFFSETS:
                target_date = today + timedelta(days=offset)
                score, factors = score_and_factors(cell, species, target_date, offset)
                days.append(DayScore(date=target_date, score=score, factors=_to_breakdown(factors)))
            species_forecasts.append(SpeciesForecast(species=species, days=days))
        return CellDetailResponse(
            cell_id=cell.id,
            lon=cell.lon,
            lat=cell.lat,
            place=Place(comune=cell.comune, nearest_place=cell.nearest_place),
            habitats=[HabitatShare(habitat=cell.habitat, fraction=1.0)],
            species=species_forecasts,
        )

    def get_cell_detail(self, cell_id: str) -> CellDetailResponse:
        return self._forecast(_cell_by_id(self.cells, cell_id))

    def get_spot(self, lat: float, lon: float) -> CellDetailResponse:
        return self._forecast(_nearest_cell(self.cells, lat, lon))

    def get_hotspots(
        self, species: SpeciesOrCombined, target_date: date, limit: int
    ) -> HotspotsResponse:
        offset = _offset_for(target_date)
        cell_scores = [
            (cell, _score_for(cell, species, target_date, offset)) for cell in self.cells
        ]
        clusters = build_hotspots(cell_scores, limit=limit)
        hotspots = [
            Hotspot(
                id=cluster.id,
                place=Place(comune=cluster.comune, nearest_place=cluster.nearest_place),
                lon=cluster.lon,
                lat=cluster.lat,
                score=cluster.score,
                cell_ids=cluster.cell_ids,
                recent_sightings=sum(
                    recent_sightings_total(
                        _cell_by_id(self.cells, cell_id), species, HOTSPOT_SIGHTINGS_WINDOW_DAYS
                    )
                    for cell_id in cluster.cell_ids
                ),
            )
            for cluster in clusters
        ]
        return HotspotsResponse(species=species, date=target_date, hotspots=hotspots)

    def get_sightings(
        self, species: Species, since: date, until: date | None = None
    ) -> SightingsResponse:
        today = today_rome()
        since_days_ago = max((today - since).days, 0)
        until_days_ago = max((today - until).days, 0) if until is not None else 0
        counts = [
            SightingCount(cell_id=cell.id, source=source, license=LICENSES[source], count=count)
            for cell in self.cells
            for source, count in counts_between(
                cell, species, since_days_ago, until_days_ago
            ).items()
        ]
        return SightingsResponse(species=species, since=since, counts=counts)

    def get_status(self) -> StatusResponse:
        # Fixtures are computed on the fly (api.fixtures.generator), so they're always "fresh".
        return StatusResponse(
            scored_through=today_rome() + timedelta(days=WINDOW_END),
            updated_at=FIXTURE_UPDATED_AT,
            rules_version="fixtures",
        )

    def get_comuni(self) -> ComuniResponse:
        return self._time_views.get_comuni()

    def get_forest_types(self) -> ForestTypesResponse:
        return ForestTypesResponse(
            cells=[CellForestType(cell_id=cell.id, habitat=cell.habitat) for cell in self.cells]
        )

    def get_seasons(self, species: SpeciesOrCombined, comune: str | None) -> SeasonsResponse:
        return self._time_views.get_seasons(species, comune)

    def get_season_map(self, year: int, species: SpeciesOrCombined) -> SeasonMapResponse:
        return self._time_views.get_season_map(year, species)

    def get_outlook(self, species: Species, comune: str | None) -> OutlookResponse:
        return self._time_views.get_outlook(species, comune)

    def get_species(self, comune: str | None) -> PlausibleSpeciesResponse:
        return self._time_views.get_species(comune)

    def overview_row(self, species: SpeciesOrCombined, target_date: date) -> RegionOverview:
        scores = self.get_scores(species, target_date)
        values = [cell.score for cell in scores.cells]
        good_score = load_history_config().good_score
        mean = sum(values) / len(values) if values else 0.0
        good_share = (
            sum(1 for value in values if value >= good_score) / len(values) if values else 0.0
        )
        return RegionOverview(
            region=self.region,
            mean_score=round(mean, 4),
            good_share=round(good_share, 4),
            updated_at=FIXTURE_UPDATED_AT,
        )


def fixture_regions_response() -> RegionsResponse:
    start = history_start_date()
    regions = []
    for region_id in FIXTURE_REGIONS:
        config = cached_region_config(region_id)
        regions.append(
            RegionInfo(
                id=region_id,
                name=dict(config.name),
                bbox_wgs84=list(config.bbox_wgs84),
                history_start=start,
                species=species_for_region(region_id, fixtures=True),
                updated_at=FIXTURE_UPDATED_AT,
            )
        )
    return RegionsResponse(regions=regions)


def fixture_overview(species: SpeciesOrCombined, target_date: date) -> OverviewResponse:
    good_score = load_history_config().good_score
    return OverviewResponse(
        species=species,
        date=target_date,
        good_score=good_score,
        regions=[
            FixtureRepository(region_id).overview_row(species, target_date)
            for region_id in FIXTURE_REGIONS
        ],
    )
