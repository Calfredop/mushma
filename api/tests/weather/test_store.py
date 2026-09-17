from datetime import UTC, date, datetime
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from api.weather.store import WeatherStore

MORNING = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)
EVENING = datetime(2026, 9, 17, 17, 0, tzinfo=UTC)


def _rows(*rows: tuple, fetched_at: datetime = MORNING) -> pd.DataFrame:
    frame = pd.DataFrame(rows, columns=["source", "point_id", "date", "variable", "value"])
    frame["fetched_at"] = fetched_at
    return frame


def _all(store: WeatherStore) -> list[tuple]:
    return duckdb.execute(
        f"SELECT source, point_id, date, variable, value FROM read_parquet('{store.daily_glob}', "
        "hive_partitioning=false) ORDER BY ALL"
    ).fetchall()


def test_upsert_writes_one_parquet_file_per_source_and_year(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    store.upsert_daily(
        _rows(
            ("era5_seamless", "N43.80E011.80", date(2023, 12, 31), "precipitation_sum", 4.2),
            ("era5_seamless", "N43.80E011.80", date(2024, 1, 1), "precipitation_sum", 0.0),
            ("ecmwf_ifs", "N43.80E011.80", date(2024, 1, 1), "precipitation_sum", 0.3),
        )
    )

    files = sorted(p.relative_to(tmp_path / "daily").as_posix() for p in store.daily_files())
    assert files == [
        "source=ecmwf_ifs/year=2024/data.parquet",
        "source=era5_seamless/year=2023/data.parquet",
        "source=era5_seamless/year=2024/data.parquet",
    ]
    assert len(_all(store)) == 3


def test_upserting_the_same_rows_again_changes_nothing(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    rows = _rows(
        ("era5_seamless", "N43.80E011.80", date(2024, 10, 1), "precipitation_sum", 0.8),
        ("era5_seamless", "N43.80E011.80", date(2024, 10, 1), "temperature_2m_min", 8.4),
    )

    store.upsert_daily(rows)
    before = _all(store)
    store.upsert_daily(rows)

    assert _all(store) == before


def test_a_newer_fetch_replaces_the_value_for_the_same_day(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    key = ("ecmwf_ifs", "N43.80E011.80", date(2026, 9, 18), "precipitation_sum")
    store.upsert_daily(_rows((*key, 12.0), fetched_at=MORNING))
    store.upsert_daily(_rows((*key, 3.5), fetched_at=EVENING))
    store.upsert_daily(_rows((*key, 99.0), fetched_at=MORNING))  # a stale re-run loses

    assert _all(store) == [(*key[:3], "precipitation_sum", 3.5)]


def test_upsert_keeps_rows_the_new_batch_does_not_mention(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    store.upsert_daily(
        _rows(("era5_seamless", "N43.80E011.80", date(2024, 10, 1), "precipitation_sum", 0.8))
    )
    store.upsert_daily(
        _rows(("era5_seamless", "N43.90E011.80", date(2024, 10, 1), "precipitation_sum", 1.0))
    )

    assert [r[1] for r in _all(store)] == ["N43.80E011.80", "N43.90E011.80"]


def test_best_daily_prefers_the_reanalysis_and_falls_back_to_the_forecast(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    store.upsert_daily(
        _rows(
            ("era5_seamless", "N43.80E011.80", date(2026, 9, 10), "precipitation_sum", 25.5),
            ("ecmwf_ifs", "N43.80E011.80", date(2026, 9, 10), "precipitation_sum", 39.0),
            ("ecmwf_ifs", "N43.80E011.80", date(2026, 9, 17), "precipitation_sum", 10.7),
            ("ecmwf_ifs", "N43.80E011.80", date(2026, 9, 30), "precipitation_sum", 1.0),
        )
    )

    best = store.best_daily(
        duckdb.connect(), date(2026, 9, 1), date(2026, 9, 20), ["era5_seamless", "ecmwf_ifs"]
    ).df()

    assert best[["date", "value", "source"]].values.tolist() == [
        [pd.Timestamp(2026, 9, 10), 25.5, "era5_seamless"],
        [pd.Timestamp(2026, 9, 17), 10.7, "ecmwf_ifs"],
    ]


def test_last_complete_date_is_the_latest_day_every_point_has(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    store.upsert_daily(
        _rows(
            ("era5_seamless", "A", date(2026, 9, 10), "precipitation_sum", 1.0),
            ("era5_seamless", "A", date(2026, 9, 11), "precipitation_sum", 1.0),
            ("era5_seamless", "B", date(2026, 9, 10), "precipitation_sum", 1.0),
            ("ecmwf_ifs", "A", date(2026, 9, 20), "precipitation_sum", 1.0),
        )
    )

    assert store.last_complete_date("era5_seamless", ["A", "B"]) == date(2026, 9, 10)
    assert store.last_complete_date("era5_seamless", ["C"]) is None
    assert WeatherStore(tmp_path / "empty").last_complete_date("era5_seamless", ["A"]) is None


def test_point_cells_keep_the_latest_model_cell_per_source_and_point(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    cell = {"source": "ecmwf_ifs", "point_id": "N43.80E011.80", "model_lat": 43.76}
    store.upsert_point_cells(
        pd.DataFrame([{**cell, "model_lon": 11.83, "elevation_m": 838.0, "fetched_at": MORNING}])
    )
    store.upsert_point_cells(
        pd.DataFrame([{**cell, "model_lon": 11.83, "elevation_m": 840.0, "fetched_at": EVENING}])
    )

    cells = store.read_point_cells()
    assert len(cells) == 1
    assert cells.loc[0, "elevation_m"] == pytest.approx(840.0)


def test_has_complete_checks_every_point_day_and_variable(tmp_path: Path) -> None:
    store = WeatherStore(tmp_path)
    store.upsert_daily(
        _rows(
            *[
                ("era5_seamless", pid, date(2024, 1, day), variable, 1.0)
                for pid in ("A", "B")
                for day in (1, 2)
                for variable in ("precipitation_sum", "temperature_2m_min")
            ]
        )
    )
    variables = ["precipitation_sum", "temperature_2m_min"]
    span = (date(2024, 1, 1), date(2024, 1, 2))

    assert store.has_complete("era5_seamless", ["A", "B"], *span, variables)
    assert not store.has_complete(
        "era5_seamless", ["A", "B"], date(2024, 1, 1), date(2024, 1, 3), variables
    )
    assert not store.has_complete("era5_seamless", ["A", "C"], *span, variables)
    assert not store.has_complete("era5_seamless", ["A"], *span, [*variables, "snowfall_sum"])
    assert not store.has_complete("ecmwf_ifs", ["A"], *span, variables)
    assert not WeatherStore(tmp_path / "empty").has_complete(
        "era5_seamless", ["A"], *span, variables
    )
