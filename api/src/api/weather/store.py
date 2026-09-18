"""The normalized daily weather table: Parquet files queried with DuckDB.

Layout under ``$DATA_DIR/weather/<region>/``:

- ``daily/source=<model>/year=<yyyy>/data.parquet``: long rows
  ``(source, point_id, date, variable, value, fetched_at)``, one per point, local day and variable.
  The key is ``(source, point_id, date, variable)``. Upserts are idempotent: re-running a fetch
  rewrites the same rows, and a newer fetch replaces older values (forecasts, fresh reanalysis
  days). Null values are never stored, so a missing row means "no data".
- ``point_cells.parquet``: the model grid cell each point was served from, per source, with its
  mean height (the reference height for lapse-rate corrections).
- ``points.parquet`` and ``weights.parquet``: the point set and the cell -> point interpolation
  weights (see ``api.weather.points``).
"""

from datetime import date
from pathlib import Path

import duckdb
import pandas as pd

DAILY_COLUMNS = ["source", "point_id", "date", "variable", "value", "fetched_at"]
POINT_CELL_COLUMNS = ["source", "point_id", "model_lat", "model_lon", "elevation_m", "fetched_at"]
# The registered pandas frame ``incoming``, with the column types the Parquet files use.
_INCOMING_SQL = """
    SELECT CAST(source AS VARCHAR) AS source, CAST(point_id AS VARCHAR) AS point_id,
           CAST(date AS DATE) AS date, CAST(variable AS VARCHAR) AS variable,
           CAST(value AS DOUBLE) AS value, CAST(fetched_at AS TIMESTAMPTZ) AS fetched_at,
           1 AS incoming
    FROM incoming
"""


class WeatherStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.daily_dir = root / "daily"
        self.points_path = root / "points.parquet"
        self.weights_path = root / "weights.parquet"
        self.point_cells_path = root / "point_cells.parquet"

    @property
    def daily_glob(self) -> str:
        return str(self.daily_dir / "*" / "*" / "data.parquet")

    def daily_files(self) -> list[Path]:
        return sorted(self.daily_dir.glob("source=*/year=*/data.parquet"))

    def partition_path(self, source: str, year: int) -> Path:
        return self.daily_dir / f"source={source}" / f"year={year}" / "data.parquet"

    def upsert_daily(self, rows: pd.DataFrame) -> None:
        """Merge rows into their source/year partitions; the newest ``fetched_at`` wins per key."""
        if rows.empty:
            return
        rows = rows[DAILY_COLUMNS].copy()
        years = pd.to_datetime(rows["date"]).dt.year
        con = duckdb.connect()
        for (source, year), part in rows.groupby([rows["source"], years]):
            path = self.partition_path(str(source), int(year))
            path.parent.mkdir(parents=True, exist_ok=True)
            con.register("incoming", part)
            merged = _INCOMING_SQL
            if path.exists():
                existing = f"SELECT *, 0 AS incoming FROM read_parquet('{path}')"
                merged = f"{existing} UNION ALL BY NAME {merged}"
            partial = path.with_name("data.parquet.part")
            con.execute(
                f"""
                COPY (
                    SELECT {", ".join(DAILY_COLUMNS)} FROM ({merged})
                    QUALIFY row_number() OVER (
                        PARTITION BY point_id, date, variable
                        ORDER BY fetched_at DESC, incoming DESC
                    ) = 1
                    ORDER BY date, point_id, variable
                ) TO '{partial}' (FORMAT parquet, COMPRESSION zstd)
                """
            )
            con.unregister("incoming")
            partial.replace(path)

    def _daily_sql(self) -> str:
        return f"read_parquet('{self.daily_glob}', hive_partitioning=false)"

    def best_daily(
        self,
        con: duckdb.DuckDBPyConnection,
        start: date,
        end: date,
        source_order: list[str],
        variables: list[str] | None = None,
    ) -> duckdb.DuckDBPyRelation:
        """One row per point, day and variable, taken from the first source in ``source_order``;
        only ``variables`` when given."""
        order = repr(list(source_order))
        only = f"AND list_contains({list(variables)!r}, variable)" if variables else ""
        return con.sql(
            f"""
            SELECT point_id, date, variable, value, source
            FROM {self._daily_sql()}
            WHERE date BETWEEN DATE '{start}' AND DATE '{end}'
              AND list_contains({order}, source) {only}
            QUALIFY row_number() OVER (
                PARTITION BY point_id, date, variable ORDER BY list_position({order}, source)
            ) = 1
            ORDER BY date, point_id, variable
            """
        )

    def last_complete_date(self, source: str, point_ids: list[str]) -> date | None:
        """The latest day for which every one of ``point_ids`` has data from ``source``."""
        if not self.daily_files() or not point_ids:
            return None
        latest = duckdb.execute(
            f"""
            SELECT point_id, max(date) FROM {self._daily_sql()}
            WHERE source = ? AND point_id IN (SELECT unnest(?))
            GROUP BY point_id
            """,
            [source, point_ids],
        ).fetchall()
        if len(latest) < len(set(point_ids)):
            return None
        return min(day for _, day in latest)

    def has_complete(
        self, source: str, point_ids: list[str], start: date, end: date, variables: list[str]
    ) -> bool:
        """Whether ``source`` has a value for every point, day and variable in the span."""
        if not self.daily_files() or not point_ids:
            return False
        expected = len(set(point_ids)) * ((end - start).days + 1) * len(set(variables))
        (found,) = duckdb.execute(
            f"""
            SELECT count(*) FROM {self._daily_sql()}
            WHERE source = ? AND date BETWEEN ? AND ?
              AND point_id IN (SELECT unnest(?)) AND variable IN (SELECT unnest(?))
            """,
            [source, start, end, list(set(point_ids)), list(set(variables))],
        ).fetchone()
        return found == expected

    def upsert_point_cells(self, cells: pd.DataFrame) -> None:
        merged = pd.concat([self.read_point_cells(), cells[POINT_CELL_COLUMNS]], ignore_index=True)
        merged = merged.sort_values("fetched_at", kind="stable").drop_duplicates(
            ["source", "point_id"], keep="last"
        )
        self.root.mkdir(parents=True, exist_ok=True)
        merged.sort_values(["source", "point_id"]).to_parquet(self.point_cells_path, index=False)

    def read_point_cells(self) -> pd.DataFrame:
        if not self.point_cells_path.exists():
            return pd.DataFrame(columns=POINT_CELL_COLUMNS)
        return pd.read_parquet(self.point_cells_path).reset_index(drop=True)
