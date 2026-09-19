"""Where the time views' tables live. Parquet, read with pandas or DuckDB like the other stores.

``$DATA_DIR/climatology/<region>/``:

- ``normals.parquet``: ``point_id, variable, doy, normal, years`` (``api.history.normals``).
- ``meta.json``: the source, variables, smoothing window and the years the normals used.

``$DATA_DIR/history/<region>/``:

- ``areas.parquet``: the region and each comune with woodland (``api.history.areas.area_table``).
- ``area_normals.parquet``: ``area_code, doy, precipitation_normal, temperature_normal``.
- ``area_weather/year=<yyyy>/data.parquet``: ``area_code, date, precipitation_sum,
  temperature_2m_mean, precipitation_normal, temperature_normal, forecast``.
- ``area_days/year=<yyyy>/data.parquet``: ``area_code, species, date, cells, good_cells,
  mean_score``.
- ``cell_seasons/year=<yyyy>/data.parquet``: ``species, cell_id, days, good_days`` (the season map).
- ``taxon_seasons/year=<yyyy>/data.parquet``: ``area_code, species, year, days, through,
  good_days`` for each taxon key (``porcini_edulis``): its own good days, where ``seasons.parquet``
  has the groups'.
- ``area_fit.parquet``: ``area_code, species, cells, fit_share``: the share of each area's woodland
  where a taxon key or group is plausible (``api.history.plausible``).
- ``area_sightings.parquet``: ``area_code, species, date, count`` (counts only).
- ``seasons.parquet`` and ``months.parquet``: ``api.history.seasons.assemble_seasons``.
- ``area_seasonal.parquet``: the latest long-range forecast per area: ``area_code, kind, start,
  end, variable, value, anomaly, fetched_at``.
- ``meta.json``: good-day and plausible-fit thresholds, season windows, the years behind each
  baseline, and the groups with their taxa.
"""

import json
from pathlib import Path

import duckdb
import pandas as pd

YEARLY = ("area_weather", "area_days", "cell_seasons", "taxon_seasons")


def _write(frame: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".part")
    frame.to_parquet(partial, index=False)
    partial.replace(path)
    return path


def _dates(frame: pd.DataFrame, *columns: str) -> pd.DataFrame:
    for column in columns:
        if column in frame:
            frame[column] = pd.to_datetime(frame[column]).dt.date
    return frame


class ClimatologyStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.normals_path = root / "normals.parquet"
        self.meta_path = root / "meta.json"

    def write_normals(self, normals: pd.DataFrame, meta: dict) -> None:
        _write(normals, self.normals_path)
        self.meta_path.write_text(json.dumps(meta, indent=2, default=str) + "\n")

    def read_normals(self) -> pd.DataFrame:
        return pd.read_parquet(self.normals_path)

    def read_meta(self) -> dict:
        return json.loads(self.meta_path.read_text()) if self.meta_path.exists() else {}


class HistoryStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.areas_path = root / "areas.parquet"
        self.area_normals_path = root / "area_normals.parquet"
        self.area_sightings_path = root / "area_sightings.parquet"
        self.seasons_path = root / "seasons.parquet"
        self.months_path = root / "months.parquet"
        self.area_seasonal_path = root / "area_seasonal.parquet"
        self.area_fit_path = root / "area_fit.parquet"
        self.meta_path = root / "meta.json"

    def partition_path(self, table: str, year: int) -> Path:
        if table not in YEARLY:
            raise ValueError(f"{table!r} is not a yearly table")
        return self.root / table / f"year={year}" / "data.parquet"

    def years(self, table: str) -> list[int]:
        return sorted(
            int(path.parent.name.split("=", 1)[1])
            for path in (self.root / table).glob("year=*/data.parquet")
        )

    def relation(
        self, con: duckdb.DuckDBPyConnection, table: str
    ) -> duckdb.DuckDBPyRelation | None:
        """Every stored year of a yearly table as a DuckDB relation (nothing loaded), or None
        when no year is stored."""
        files = [str(self.partition_path(table, year)) for year in self.years(table)]
        if not files:
            return None
        return con.sql(f"SELECT * FROM read_parquet({files!r}, hive_partitioning = false)")

    def write_partition(self, table: str, year: int, frame: pd.DataFrame) -> Path:
        return _write(frame, self.partition_path(table, year))

    def write(self, path: Path, frame: pd.DataFrame) -> Path:
        return _write(frame, path)

    def _read_yearly(
        self, table: str, years: list[int] | None, filters: list[tuple] | None = None
    ) -> pd.DataFrame:
        wanted = (
            self.years(table) if years is None else [y for y in years if y in self.years(table)]
        )
        frames = [
            pd.read_parquet(self.partition_path(table, year), filters=filters or None)
            for year in wanted
        ]
        frames = [f for f in frames if not f.empty]
        if not frames:
            return pd.DataFrame()
        return _dates(pd.concat(frames, ignore_index=True), "date")

    def read_area_days(
        self,
        years: list[int] | None = None,
        species: str | None = None,
        area_code: str | None = None,
    ) -> pd.DataFrame:
        filters = []
        if species is not None:
            filters.append(("species", "==", species))
        if area_code is not None:
            filters.append(("area_code", "==", area_code))
        return self._read_yearly("area_days", years, filters)

    def read_area_weather(
        self, years: list[int] | None = None, area_code: str | None = None
    ) -> pd.DataFrame:
        filters = [("area_code", "==", area_code)] if area_code is not None else None
        return self._read_yearly("area_weather", years, filters)

    def read_cell_seasons(self, year: int, species: str) -> pd.DataFrame:
        path = self.partition_path("cell_seasons", year)
        if not path.exists():
            return pd.DataFrame(columns=["species", "cell_id", "days", "good_days"])
        return pd.read_parquet(path, filters=[("species", "==", species)])

    def read_taxon_seasons(self, area_code: str) -> pd.DataFrame:
        frame = self._read_yearly("taxon_seasons", None, [("area_code", "==", area_code)])
        if frame.empty:
            return pd.DataFrame(
                columns=["area_code", "species", "year", "days", "through", "good_days"]
            )
        return _dates(frame, "through").sort_values(["species", "year"], ignore_index=True)

    def read_area_fit(self) -> pd.DataFrame:
        if not self.area_fit_path.exists():
            return pd.DataFrame(columns=["area_code", "species", "cells", "fit_share"])
        return pd.read_parquet(self.area_fit_path)

    def read_areas(self) -> pd.DataFrame:
        return pd.read_parquet(self.areas_path)

    def read_seasons(self) -> pd.DataFrame:
        frame = pd.read_parquet(self.seasons_path)
        return _dates(frame, "through", "window_start", "window_end", "weather_through")

    def read_months(self) -> pd.DataFrame:
        return pd.read_parquet(self.months_path)

    def read_area_sightings(self) -> pd.DataFrame:
        if not self.area_sightings_path.exists():
            return pd.DataFrame(columns=["area_code", "species", "date", "count"])
        return _dates(pd.read_parquet(self.area_sightings_path), "date")

    def read_area_normals(self) -> pd.DataFrame:
        return pd.read_parquet(self.area_normals_path)

    def read_area_seasonal(self) -> pd.DataFrame:
        if not self.area_seasonal_path.exists():
            return pd.DataFrame(
                columns=["area_code", "kind", "start", "end", "variable", "value", "anomaly"]
            )
        return _dates(pd.read_parquet(self.area_seasonal_path), "start", "end")

    def write_meta(self, meta: dict) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.meta_path.write_text(
            json.dumps(meta, indent=2, ensure_ascii=False, default=str) + "\n"
        )

    def read_meta(self) -> dict:
        return json.loads(self.meta_path.read_text()) if self.meta_path.exists() else {}
