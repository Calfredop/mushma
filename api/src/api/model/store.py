"""The score table: Parquet files queried with DuckDB, one partition per tier, key and year.

Layout under ``$DATA_DIR/scores/<region>/``:

- ``daily/species=<key>/year=<yyyy>/data.parquet``: the scores. One row per woodland cell and day,
  keyed by ``(cell_id, date)``, for every species key (``porcini_edulis``), group (``porcini``) and
  ``combined``: ``score`` and ``forecast``, plus ``rules_version`` (species keys), ``source_key``
  (groups) or ``source_group`` and ``source_key`` (combined). Cell-days without weather are not
  stored. About 60 MB per year for every key.
- ``factors/species=<key>/year=<yyyy>/data.parquet``: the "why this score" columns of each species
  key: every enabled factor's value, its measured ``<factor>__input`` and, for rain events,
  ``<factor>__days_ago`` and, on a growth clock, ``<factor>__growth_days``. About 40 MB per key
  and year, so history is usually scored without it and the daily run keeps it for the days the
  app shows.
- ``meta.json``: the last scoring run (rules version, groups, period, credits).

Upserts replace the rows of the cell-days they carry and keep the rest, so re-scoring a period
(a fresh forecast, new reanalysis days, changed rules) is safe.
"""

from datetime import date
from pathlib import Path
from typing import Literal

import duckdb
import pandas as pd

Tier = Literal["daily", "factors"]


class ScoreStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.meta_path = root / "meta.json"

    def partition_path(self, key: str, year: int, tier: Tier = "daily") -> Path:
        return self.root / tier / f"species={key}" / f"year={year}" / "data.parquet"

    def keys(self, tier: Tier = "daily") -> list[str]:
        return sorted(
            path.name.split("=", 1)[1]
            for path in (self.root / tier).glob("species=*")
            if any(path.glob("year=*/data.parquet"))
        )

    def files(self, key: str, tier: Tier = "daily") -> list[Path]:
        return sorted((self.root / tier / f"species={key}").glob("year=*/data.parquet"))

    def upsert(self, key: str, rows: pd.DataFrame | list[Path], tier: Tier = "daily") -> None:
        """Merge ``rows`` (a frame, or Parquet files staged by a run) into the key's partitions."""
        con = duckdb.connect()
        if isinstance(rows, pd.DataFrame):
            if rows.empty:
                return
            con.register("incoming_rows", rows)
            source = "incoming_rows"
        else:
            if not rows:
                return
            source = f"read_parquet({[str(p) for p in rows]!r}, union_by_name = true)"
        con.execute(
            "CREATE TEMP VIEW incoming AS "
            f"SELECT * REPLACE (CAST(date AS DATE) AS date) FROM {source}"
        )
        years = [y for (y,) in con.execute("SELECT DISTINCT year(date) FROM incoming").fetchall()]
        for year in sorted(years):
            path = self.partition_path(key, int(year), tier)
            path.parent.mkdir(parents=True, exist_ok=True)
            new = f"SELECT * FROM incoming WHERE year(date) = {int(year)}"
            merged = new
            if path.exists():
                merged = f"""
                    SELECT old.* FROM read_parquet('{path}') AS old
                    ANTI JOIN ({new}) AS fresh USING (cell_id, date)
                    UNION ALL BY NAME {new}
                """
            partial = path.with_name("data.parquet.part")
            con.execute(
                f"""
                COPY (SELECT * FROM ({merged}) ORDER BY cell_id, date)
                TO '{partial}' (FORMAT parquet, COMPRESSION zstd)
                """
            )
            partial.replace(path)

    def read(
        self,
        con: duckdb.DuckDBPyConnection,
        key: str,
        start: date,
        end: date,
        cell_ids: list[str] | None = None,
        tier: Tier = "daily",
    ) -> duckdb.DuckDBPyRelation:
        """Rows for ``key`` between two dates (inclusive), optionally for some cells only."""
        files = [
            str(path)
            for path in self.files(key, tier)
            if start.year <= int(path.parent.name.split("=", 1)[1]) <= end.year
        ]
        if not files:
            return con.sql("SELECT NULL::VARCHAR AS cell_id, NULL::DATE AS date WHERE false")
        cells_filter = "AND cell_id IN (SELECT unnest(?))" if cell_ids is not None else ""
        return con.sql(
            f"""
            SELECT * FROM read_parquet({files!r}, union_by_name = true, hive_partitioning = false)
            WHERE date BETWEEN DATE '{start}' AND DATE '{end}' {cells_filter}
            ORDER BY date, cell_id
            """,
            params=[list(cell_ids)] if cell_ids is not None else None,
        )
