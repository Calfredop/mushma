"""The seam routes.py depends on. `FixtureRepository` (fixtures/repository.py) serves
`MUSHMA_FIXTURES=1`; `LiveRepository` (live/repository.py) serves everything else, reading the
real M2/M3 Parquet stores under `$DATA_DIR`."""

from datetime import date
from typing import Protocol

from api.models import CellDetailResponse, HotspotsResponse, ScoresResponse, SightingsResponse
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

    def get_sightings(self, species: Species, since: date) -> SightingsResponse:
        """Never returns coordinates -- counts per cell only."""
