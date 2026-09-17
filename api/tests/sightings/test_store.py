from datetime import UTC, date, datetime
from pathlib import Path

import duckdb
import pandas as pd
from pyproj import Transformer

from api.sightings.store import SightingsStore, assign_cells

MORNING = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)
EVENING = datetime(2026, 9, 17, 17, 0, tzinfo=UTC)
CRS = "EPSG:3035"


def _lonlat(x: float, y: float) -> tuple[float, float]:
    lon, lat = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True).transform(x, y)
    return lon, lat


def _common_row(**overrides) -> dict:
    row = {
        "source": "gbif",
        "record_id": "1",
        "species": "porcini",
        "event_date": date(2026, 9, 1),
        "license": "CC0",
        "obscured": False,
        "fetched_at": MORNING,
    }
    row.update(overrides)
    return row


def _stored_row(**overrides) -> dict:
    row = {
        "species": "porcini",
        "cell_id": "1kmE4300N2400",
        "date": date(2026, 9, 1),
        "source": "gbif",
        "record_id": "1",
        "license": "CC0",
        "obscured": False,
        "fetched_at": MORNING,
    }
    row.update(overrides)
    return row


# --- assign_cells: the only place raw coordinates are read -------------------------------------


def test_assign_cells_keeps_a_point_inside_a_woodland_cell() -> None:
    lon, lat = _lonlat(4_300_500, 2_400_500)
    rows = pd.DataFrame([_common_row(lon=lon, lat=lat)])
    cells = pd.DataFrame({"cell_id": ["1kmE4300N2400"], "woodland": [True]})

    joined = assign_cells(rows, cells, crs=CRS, cell_size_m=1000)

    assert joined.iloc[0]["cell_id"] == "1kmE4300N2400"
    assert "lat" not in joined.columns and "lon" not in joined.columns


def test_assign_cells_drops_a_point_outside_any_woodland_cell() -> None:
    lon, lat = _lonlat(4_300_500, 2_400_500)
    rows = pd.DataFrame([_common_row(lon=lon, lat=lat)])
    cells = pd.DataFrame({"cell_id": ["1kmE4300N2400"], "woodland": [False]})

    joined = assign_cells(rows, cells, crs=CRS, cell_size_m=1000)

    assert joined.empty


def test_assign_cells_drops_a_point_off_the_grid_entirely() -> None:
    lon, lat = _lonlat(4_999_500, 2_999_500)
    rows = pd.DataFrame([_common_row(lon=lon, lat=lat)])
    cells = pd.DataFrame({"cell_id": ["1kmE4300N2400"], "woodland": [True]})

    joined = assign_cells(rows, cells, crs=CRS, cell_size_m=1000)

    assert joined.empty


def test_assign_cells_handles_no_rows() -> None:
    cells = pd.DataFrame({"cell_id": ["1kmE4300N2400"], "woodland": [True]})

    joined = assign_cells(pd.DataFrame(columns=["lon", "lat"]), cells, crs=CRS, cell_size_m=1000)

    assert joined.empty


# --- SightingsStore: upsert and count-only egress -----------------------------------------------


def _all(store: SightingsStore) -> list[tuple]:
    return duckdb.execute(
        f"SELECT species, cell_id, date, source, record_id, obscured FROM "
        f"read_parquet('{store.records_glob}', hive_partitioning=false) ORDER BY ALL"
    ).fetchall()


def test_upsert_writes_one_parquet_file_per_species_and_year(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)
    rows = pd.DataFrame(
        [
            _stored_row(species="porcini", record_id="1"),
            _stored_row(species="porcini", record_id="2", date=date(2025, 1, 1)),
            _stored_row(species="ovoli", record_id="3", cell_id="1kmE4301N2400"),
        ]
    )

    store.upsert(rows)

    files = sorted(p.relative_to(tmp_path / "records").as_posix() for p in store.record_files())
    assert files == [
        "species=ovoli/year=2026/data.parquet",
        "species=porcini/year=2025/data.parquet",
        "species=porcini/year=2026/data.parquet",
    ]
    assert len(_all(store)) == 3


def test_upserting_the_same_rows_again_changes_nothing(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)
    rows = pd.DataFrame([_stored_row()])

    store.upsert(rows)
    before = _all(store)
    store.upsert(rows)

    assert _all(store) == before


def test_a_newer_fetch_replaces_the_row_for_the_same_source_and_record(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)
    store.upsert(pd.DataFrame([_stored_row(obscured=False, fetched_at=MORNING)]))
    store.upsert(pd.DataFrame([_stored_row(obscured=True, fetched_at=EVENING)]))

    rows = _all(store)
    assert len(rows) == 1 and rows[0][5] is True


def test_upsert_keeps_rows_the_new_batch_does_not_mention(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)
    store.upsert(pd.DataFrame([_stored_row(record_id="1")]))
    store.upsert(pd.DataFrame([_stored_row(record_id="2")]))

    assert [r[4] for r in _all(store)] == ["1", "2"]


def test_counts_by_cell_aggregates_without_exposing_individual_records(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)
    store.upsert(
        pd.DataFrame(
            [
                _stored_row(record_id="1", species="porcini"),
                _stored_row(record_id="2", species="porcini"),
                _stored_row(record_id="3", species="ovoli"),
            ]
        )
    )

    con = duckdb.connect()
    counts = store.counts_by_cell(con).df()

    assert counts.columns.tolist() == ["species", "cell_id", "count"]
    assert counts.set_index(["species", "cell_id"]).loc[("porcini", "1kmE4300N2400"), "count"] == 2
