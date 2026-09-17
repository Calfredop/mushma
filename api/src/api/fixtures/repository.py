from datetime import date, timedelta

from api.fixtures.cells import CELLS, CellSpec
from api.fixtures.generator import WINDOW_OFFSETS, combined_score, score_and_factors
from api.fixtures.hotspots import build_hotspots
from api.fixtures.scoring import FactorResult
from api.fixtures.sightings import LICENSES, counts_since, recent_sightings_total
from api.models import (
    CellDetailResponse,
    DayScore,
    FactorBreakdown,
    GridCellScore,
    Hotspot,
    HotspotsResponse,
    Place,
    ScoresResponse,
    SightingCount,
    SightingsResponse,
    SpeciesForecast,
)
from api.repository import CellNotFound, DateOutOfRange
from api.species import SPECIES, Species, SpeciesOrCombined
from api.timeutil import today_rome

WINDOW_START = WINDOW_OFFSETS.start  # -6
WINDOW_END = WINDOW_OFFSETS.stop - 1  # 7
FORECAST_OFFSETS = range(0, 8)  # today + 7-day outlook (PRD -> Features 2)
HOTSPOT_SIGHTINGS_WINDOW_DAYS = 90


def _cell_by_id(cell_id: str) -> CellSpec:
    for cell in CELLS:
        if cell.id == cell_id:
            return cell
    raise CellNotFound(cell_id)


def _nearest_cell(lat: float, lon: float) -> CellSpec:
    return min(CELLS, key=lambda cell: (cell.lat - lat) ** 2 + (cell.lon - lon) ** 2)


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
        FactorBreakdown(key=f.key, i18n_key=f.i18n_key, value=f.value, contribution=f.contribution)
        for f in factors
    ]


class FixtureRepository:
    def get_scores(self, species: SpeciesOrCombined, target_date: date) -> ScoresResponse:
        offset = _offset_for(target_date)
        cells = [
            GridCellScore(
                cell_id=cell.id,
                lon=cell.lon,
                lat=cell.lat,
                score=_score_for(cell, species, target_date, offset),
            )
            for cell in CELLS
        ]
        return ScoresResponse(species=species, date=target_date, cells=cells)

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
            species=species_forecasts,
        )

    def get_cell_detail(self, cell_id: str) -> CellDetailResponse:
        return self._forecast(_cell_by_id(cell_id))

    def get_spot(self, lat: float, lon: float) -> CellDetailResponse:
        return self._forecast(_nearest_cell(lat, lon))

    def get_hotspots(
        self, species: SpeciesOrCombined, target_date: date, limit: int
    ) -> HotspotsResponse:
        offset = _offset_for(target_date)
        cell_scores = [(cell, _score_for(cell, species, target_date, offset)) for cell in CELLS]
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
                        _cell_by_id(cell_id), species, HOTSPOT_SIGHTINGS_WINDOW_DAYS
                    )
                    for cell_id in cluster.cell_ids
                ),
            )
            for cluster in clusters
        ]
        return HotspotsResponse(species=species, date=target_date, hotspots=hotspots)

    def get_sightings(self, species: Species, since: date) -> SightingsResponse:
        since_days_ago = max((today_rome() - since).days, 0)
        counts = [
            SightingCount(cell_id=cell.id, source=source, license=LICENSES[source], count=count)
            for cell in CELLS
            for source, count in counts_since(cell, species, since_days_ago).items()
        ]
        return SightingsResponse(species=species, since=since, counts=counts)
