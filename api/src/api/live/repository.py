"""ScoresRepository backed by the real M2/M3 Parquet stores (api.grid.store, api.model.store,
api.sightings.store) via DuckDB. Replaces fixture mode once the daily pipeline (api.jobs.daily) is
producing data. See api.repository.ScoresRepository for the contract each method implements.

Tuscany is the only region in v1 (PRD -> Current focus), so it's hardcoded rather than plumbed
through as a parameter nothing yet varies.
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb
import pandas as pd

from api.live.breakdown import reconstruct_breakdown
from api.live.hotspots import cluster_hotspots
from api.model.rules import RuleSet, load_rules
from api.model.store import ScoreStore
from api.models import (
    CellDetailResponse,
    DayScore,
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
from api.sightings.store import SightingsStore
from api.species import SPECIES, Species, SpeciesOrCombined
from api.timeutil import today_rome

REGION = "tuscany"
FORECAST_OFFSETS = range(0, 8)  # today + 7-day outlook, PRD -> Features 2
HOTSPOT_SIGHTINGS_WINDOW_DAYS = 90
CELL_COLUMNS = ["cell_id", "lon", "lat", "woodland", "comune_name", "place_name", "x_min", "y_min"]


class LiveRepository:
    def __init__(self, root: Path, rules: RuleSet | None = None) -> None:
        self.root = root
        self.scores = ScoreStore(root / "scores" / REGION)
        self.sightings = SightingsStore(root / "sightings" / REGION)
        self.rules = rules or load_rules()
        self._cells: pd.DataFrame | None = None

    @property
    def cells(self) -> pd.DataFrame:
        """Woodland cells only -- the model never scores anything else, so nothing else is ever
        servable through this repository."""
        if self._cells is None:
            grid_path = self.root / "grid" / REGION / "cells.parquet"
            all_cells = pd.read_parquet(grid_path, columns=CELL_COLUMNS)
            self._cells = all_cells[all_cells["woodland"]].reset_index(drop=True)
        return self._cells

    def _cell_row(self, cell_id: str) -> pd.Series:
        matches = self.cells[self.cells["cell_id"] == cell_id]
        if matches.empty:
            raise CellNotFound(cell_id)
        return matches.iloc[0]

    def _nearest_cell(self, lat: float, lon: float) -> pd.Series:
        cells = self.cells
        distance_sq = (cells["lat"] - lat) ** 2 + (cells["lon"] - lon) ** 2
        return cells.loc[distance_sq.idxmin()]

    def _date_bounds(
        self, con: duckdb.DuckDBPyConnection, key: str, tier: str = "daily"
    ) -> tuple[date, date] | None:
        files = [str(path) for path in self.scores.files(key, tier)]
        if not files:
            return None
        lo, hi = con.sql(f"SELECT min(date), max(date) FROM read_parquet({files!r})").fetchone()
        return None if lo is None else (lo, hi)

    def _scores_for_date(
        self, con: duckdb.DuckDBPyConnection, key: str, target_date: date
    ) -> pd.DataFrame:
        rows = self.scores.read(con, key, target_date, target_date).df()
        if rows.empty:
            bounds = self._date_bounds(con, key)
            lo, hi = bounds or (target_date, target_date)
            raise DateOutOfRange(target_date, lo, hi)
        rows["date"] = pd.to_datetime(rows["date"]).dt.date
        return rows

    def get_scores(self, species: SpeciesOrCombined, target_date: date) -> ScoresResponse:
        con = duckdb.connect()
        rows = self._scores_for_date(con, species, target_date)
        merged = rows.merge(self.cells[["cell_id", "lon", "lat"]], on="cell_id", how="inner")
        cells = [
            GridCellScore(
                cell_id=r.cell_id, lon=float(r.lon), lat=float(r.lat), score=float(r.score)
            )
            for r in merged.itertuples()
        ]
        return ScoresResponse(species=species, date=target_date, cells=cells)

    def _forecast(self, cell_row: pd.Series) -> CellDetailResponse:
        cell_id = cell_row["cell_id"]
        today = today_rome()
        start, end = today, today + timedelta(days=FORECAST_OFFSETS.stop - 1)
        con = duckdb.connect()

        species_forecasts = []
        for group in SPECIES:
            daily = self.scores.read(con, group, start, end, cell_ids=[cell_id]).df()
            if len(daily) != len(FORECAST_OFFSETS):
                raise RuntimeError(
                    f"incomplete {group} outlook for {cell_id}: "
                    f"{len(daily)}/{len(FORECAST_OFFSETS)} days stored"
                )
            daily["date"] = pd.to_datetime(daily["date"]).dt.date
            daily = daily.sort_values("date")

            factor_frames: dict[str, pd.DataFrame] = {}
            for leaf_key in sorted(daily["source_key"].dropna().unique().tolist()):
                factors = self.scores.read(
                    con, leaf_key, start, end, cell_ids=[cell_id], tier="factors"
                ).df()
                factors["date"] = pd.to_datetime(factors["date"]).dt.date
                factor_frames[leaf_key] = factors.set_index("date")

            days = []
            for row in daily.itertuples():
                factor_row = factor_frames[row.source_key].loc[row.date].to_dict()
                breakdown = reconstruct_breakdown(
                    self.rules.species[row.source_key].enabled_factors, factor_row
                )
                days.append(DayScore(date=row.date, score=float(row.score), factors=breakdown))
            species_forecasts.append(SpeciesForecast(species=group, days=days))

        return CellDetailResponse(
            cell_id=cell_id,
            lon=float(cell_row["lon"]),
            lat=float(cell_row["lat"]),
            place=Place(comune=cell_row["comune_name"], nearest_place=cell_row["place_name"]),
            species=species_forecasts,
        )

    def get_cell_detail(self, cell_id: str) -> CellDetailResponse:
        return self._forecast(self._cell_row(cell_id))

    def get_spot(self, lat: float, lon: float) -> CellDetailResponse:
        return self._forecast(self._nearest_cell(lat, lon))

    def get_hotspots(
        self, species: SpeciesOrCombined, target_date: date, limit: int
    ) -> HotspotsResponse:
        con = duckdb.connect()
        rows = self._scores_for_date(con, species, target_date)
        merged = rows.merge(
            self.cells[["cell_id", "x_min", "y_min", "lon", "lat", "comune_name", "place_name"]],
            on="cell_id",
            how="inner",
        )
        clusters = cluster_hotspots(merged, limit=limit)

        since = target_date - timedelta(days=HOTSPOT_SIGHTINGS_WINDOW_DAYS)
        species_list = SPECIES if species == "combined" else (species,)
        sightings_by_cell: dict[str, int] = {}
        for sp in species_list:
            for r in self.sightings.counts_since(con, sp, since).df().itertuples():
                sightings_by_cell[r.cell_id] = sightings_by_cell.get(r.cell_id, 0) + r.count

        hotspots = [
            Hotspot(
                id=f"hotspot-{i + 1}",
                place=Place(comune=cluster.comune, nearest_place=cluster.nearest_place),
                lon=cluster.lon,
                lat=cluster.lat,
                score=cluster.score,
                cell_ids=cluster.cell_ids,
                recent_sightings=sum(sightings_by_cell.get(cid, 0) for cid in cluster.cell_ids),
            )
            for i, cluster in enumerate(clusters)
        ]
        return HotspotsResponse(species=species, date=target_date, hotspots=hotspots)

    def get_sightings(self, species: Species, since: date) -> SightingsResponse:
        con = duckdb.connect()
        counts = self.sightings.counts_since(con, species, since).df()
        rows = [
            SightingCount(cell_id=r.cell_id, source=r.source, license=r.license, count=int(r.count))
            for r in counts.itertuples()
        ]
        return SightingsResponse(species=species, since=since, counts=rows)
