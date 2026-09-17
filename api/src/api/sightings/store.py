"""The normalized sightings table: Parquet files queried with DuckDB, one row per kept record.

Layout under ``$DATA_DIR/sightings/<region>/``:

- ``records/species=<species>/year=<yyyy>/data.parquet``: one row per sighting that passed the
  quality filters, keyed by ``(source, record_id)``. Upserts are idempotent: re-running a fetch
  rewrites the same rows, and a newer fetch (by ``fetched_at``) replaces an older one (e.g. a
  record later reclassified as obscured).
- No row ever carries coordinates: :func:`assign_cells` is the one place raw lat/lon are read, and
  it replaces them with the woodland cell id they fall in. This is what PRD → Sightings privacy
  means by "never re-sharpen a record the source obscured" — the store cannot leak more precision
  than a 1 km cell even if asked to. :meth:`SightingsStore.counts_by_cell` is the one query this
  module offers back out; the API and any future consumer should read counts through it rather
  than the raw records.
"""

from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from pyproj import Transformer

from api.grid.cells import cell_id as make_cell_id

RECORD_COLUMNS = [
    "species",
    "cell_id",
    "date",
    "source",
    "record_id",
    "license",
    "obscured",
    "fetched_at",
]
_INCOMING_SQL = """
    SELECT CAST(species AS VARCHAR) AS species, CAST(cell_id AS VARCHAR) AS cell_id,
           CAST(date AS DATE) AS date, CAST(source AS VARCHAR) AS source,
           CAST(record_id AS VARCHAR) AS record_id, CAST(license AS VARCHAR) AS license,
           CAST(obscured AS BOOLEAN) AS obscured, CAST(fetched_at AS TIMESTAMPTZ) AS fetched_at,
           1 AS incoming
    FROM incoming
"""


def assign_cells(
    rows: pd.DataFrame, cells: pd.DataFrame, crs: str, cell_size_m: int
) -> pd.DataFrame:
    """Join each record's WGS84 coordinates to a woodland cell id, then drop the coordinates.

    Records outside every woodland cell (off the grid, or a non-woodland cell: sea, town, bare
    farmland) are dropped: the model only ever scores woodland cells, so a sighting elsewhere
    cannot validate anything.
    """
    if rows.empty:
        return rows.drop(columns=["lat", "lon"], errors="ignore").assign(
            cell_id=pd.Series(dtype=object)
        )
    to_projected = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    x, y = to_projected.transform(rows["lon"].to_numpy(), rows["lat"].to_numpy())
    x_min = np.floor(x / cell_size_m).astype(np.int64) * cell_size_m
    y_min = np.floor(y / cell_size_m).astype(np.int64) * cell_size_m
    ids = [make_cell_id(int(cx), int(cy), cell_size_m) for cx, cy in zip(x_min, y_min, strict=True)]

    joined = rows.drop(columns=["lat", "lon"]).assign(cell_id=ids)
    woodland_ids = set(cells.loc[cells["woodland"], "cell_id"])
    return joined[joined["cell_id"].isin(woodland_ids)].reset_index(drop=True)


class SightingsStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.records_dir = root / "records"

    @property
    def records_glob(self) -> str:
        return str(self.records_dir / "*" / "*" / "data.parquet")

    def record_files(self) -> list[Path]:
        return sorted(self.records_dir.glob("species=*/year=*/data.parquet"))

    def partition_path(self, species: str, year: int) -> Path:
        return self.records_dir / f"species={species}" / f"year={year}" / "data.parquet"

    def upsert(self, rows: pd.DataFrame) -> None:
        """Merge rows into their species/year partitions; the newest ``fetched_at`` wins per
        ``(source, record_id)``."""
        if rows.empty:
            return
        rows = rows[RECORD_COLUMNS].copy()
        years = pd.to_datetime(rows["date"]).dt.year
        con = duckdb.connect()
        for (species, year), part in rows.groupby([rows["species"], years]):
            path = self.partition_path(str(species), int(year))
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
                    SELECT {", ".join(RECORD_COLUMNS)} FROM ({merged})
                    QUALIFY row_number() OVER (
                        PARTITION BY source, record_id ORDER BY fetched_at DESC, incoming DESC
                    ) = 1
                    ORDER BY date, cell_id, source, record_id
                ) TO '{partial}' (FORMAT parquet, COMPRESSION zstd)
                """
            )
            con.unregister("incoming")
            partial.replace(path)

    def remove(self, source: str, record_ids: list[str]) -> int:
        """Delete ``(source, record_id)`` rows, e.g. records a tightened filter now rejects.
        Returns how many rows went."""
        if not record_ids or not self.record_files():
            return 0
        removed = 0
        con = duckdb.connect()
        for path in self.record_files():
            (hits,) = con.execute(
                f"SELECT count(*) FROM read_parquet('{path}') "
                "WHERE source = ? AND record_id IN (SELECT unnest(?))",
                [source, list(record_ids)],
            ).fetchone()
            if not hits:
                continue
            partial = path.with_name("data.parquet.part")
            con.execute(
                f"""
                COPY (
                    SELECT * FROM read_parquet('{path}')
                    WHERE NOT (source = $source AND record_id IN (SELECT unnest($ids)))
                    ORDER BY date, cell_id, source, record_id
                ) TO '{partial}' (FORMAT parquet, COMPRESSION zstd)
                """,
                {"source": source, "ids": list(record_ids)},
            )
            partial.replace(path)
            removed += hits
        return removed

    def counts_by_cell(self, con: duckdb.DuckDBPyConnection) -> duckdb.DuckDBPyRelation:
        """Sighting counts per species and cell: the only aggregate this module hands back out
        (PRD → Sightings privacy: counts per cell, never coordinates or individual records)."""
        if not self.record_files():
            return con.sql(
                "SELECT NULL::VARCHAR AS species, NULL::VARCHAR AS cell_id, "
                "NULL::BIGINT AS count WHERE false"
            )
        return con.sql(
            f"""
            SELECT species, cell_id, count(*) AS count
            FROM read_parquet('{self.records_glob}', hive_partitioning=false)
            GROUP BY species, cell_id
            ORDER BY species, cell_id
            """
        )
