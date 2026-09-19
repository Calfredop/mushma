"""The seam routes.py depends on. `FixtureRepository` (fixtures/repository.py) serves
`MUSHMA_FIXTURES=1`; `LiveRepository` (live/repository.py) serves everything else, reading the
real M2/M3 Parquet stores under `$DATA_DIR`."""

from datetime import date
from typing import Protocol

from api.models import (
    CellDetailResponse,
    ComuniResponse,
    HotspotsResponse,
    OutlookResponse,
    PlausibleSpeciesResponse,
    ScoresResponse,
    SeasonMapResponse,
    SeasonsResponse,
    SightingsResponse,
    StatusResponse,
)
from api.species import Species, SpeciesOrCombined


class DateOutOfRange(Exception):
    def __init__(self, requested: date, available_from: date, available_to: date) -> None:
        self.requested = requested
        self.available_from = available_from
        self.available_to = available_to
        super().__init__(
            f"no data for {requested}; available range is {available_from} to {available_to}"
        )


class CellNotFound(Exception):
    def __init__(self, cell_id: str) -> None:
        self.cell_id = cell_id
        super().__init__(f"cell {cell_id!r} not found")


class AreaNotFound(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"no comune {code!r} with woodland")


class SeasonNotFound(Exception):
    def __init__(self, year: int, available: list[int]) -> None:
        self.year = year
        self.available = available
        super().__init__(f"no season {year}; available seasons are {available}")


class HistoryUnavailable(Exception):
    """The time views' tables have not been built yet (``api.history.build``)."""


class ScoresUnavailable(Exception):
    """No scores have been generated yet (``api.jobs.daily`` / ``api.model.pipeline``)."""


class ScoresRepository(Protocol):
    def get_scores(self, species: SpeciesOrCombined, target_date: date) -> ScoresResponse:
        """Raises DateOutOfRange if target_date isn't in the served window."""

    def get_cell_detail(self, cell_id: str) -> CellDetailResponse:
        """Raises CellNotFound if cell_id doesn't exist."""

    def get_spot(self, lat: float, lon: float) -> CellDetailResponse:
        """Resolves to the nearest cell; always succeeds."""

    def get_hotspots(
        self, species: SpeciesOrCombined, target_date: date, limit: int
    ) -> HotspotsResponse:
        """Raises DateOutOfRange if target_date isn't in the served window."""

    def get_sightings(
        self, species: Species, since: date, until: date | None = None
    ) -> SightingsResponse:
        """Never returns coordinates -- counts per cell only."""

    def get_comuni(self) -> ComuniResponse:
        """Comuni with woodland, by name."""

    def get_seasons(self, species: SpeciesOrCombined, comune: str | None) -> SeasonsResponse:
        """Every stored season for Tuscany (``comune`` None) or one comune. Raises AreaNotFound."""

    def get_season_map(self, year: int, species: SpeciesOrCombined) -> SeasonMapResponse:
        """Good days per woodland cell and per comune for one season. Raises SeasonNotFound."""

    def get_outlook(self, species: Species, comune: str | None) -> OutlookResponse:
        """The season so far and the periods after the 7-day forecast. Raises AreaNotFound."""

    def get_species(self, comune: str | None) -> PlausibleSpeciesResponse:
        """Which species the woodland of Tuscany or one comune plausibly holds, and each one's
        good days per season. Raises AreaNotFound."""

    def get_status(self) -> StatusResponse:
        """Data freshness. Raises ScoresUnavailable if the pipeline has never scored anything."""
