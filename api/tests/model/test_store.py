from datetime import date
from pathlib import Path

import duckdb
import pandas as pd

from api.model.store import ScoreStore


def _frame(days: list[date], score: float, **extra) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "cell_id": ["c1"] * len(days),
            "date": days,
            "score": [score] * len(days),
            **{k: [v] * len(days) for k, v in extra.items()},
        }
    )


def test_upsert_writes_one_partition_per_key_and_year(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path)

    store.upsert("ovoli", _frame([date(2024, 12, 31), date(2025, 1, 1)], 0.5))

    assert store.partition_path("ovoli", 2024).exists()
    assert store.partition_path("ovoli", 2025).exists()
    assert store.keys() == ["ovoli"]


def test_upsert_replaces_the_same_cell_days_and_keeps_the_rest(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path)
    store.upsert("ovoli", _frame([date(2024, 10, 1), date(2024, 10, 2)], 0.2))

    store.upsert("ovoli", _frame([date(2024, 10, 2), date(2024, 10, 3)], 0.9))

    rows = store.read(duckdb.connect(), "ovoli", date(2024, 1, 1), date(2024, 12, 31)).df()
    assert rows["date"].dt.date.tolist() == [date(2024, 10, d) for d in (1, 2, 3)]
    assert rows["score"].tolist() == [0.2, 0.9, 0.9]


def test_new_columns_can_appear_between_runs(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path)
    store.upsert("ovoli", _frame([date(2024, 10, 1)], 0.2, frost=1.0))

    store.upsert("ovoli", _frame([date(2024, 10, 2)], 0.3, frost=0.5, snow=1.0))

    rows = store.read(duckdb.connect(), "ovoli", date(2024, 10, 1), date(2024, 10, 2)).df()
    assert rows["frost"].tolist() == [1.0, 0.5]
    assert pd.isna(rows["snow"].iloc[0])


def test_read_filters_by_date_and_cells(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path)
    frame = pd.concat(
        [_frame([date(2024, 10, 1), date(2024, 10, 2)], 0.1), _frame([date(2024, 10, 1)], 0.4)]
    )
    frame.iloc[2, 0] = "c2"
    store.upsert("combined", frame)

    rows = store.read(
        duckdb.connect(), "combined", date(2024, 10, 1), date(2024, 10, 1), cell_ids=["c2"]
    ).df()

    assert rows[["cell_id", "score"]].values.tolist() == [["c2", 0.4]]


def test_the_factor_tier_is_separate_from_the_scores(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path)
    store.upsert("ovoli", _frame([date(2024, 10, 1)], 0.2))
    store.upsert(
        "ovoli", _frame([date(2024, 10, 1)], 0.2, frost=1.0).drop(columns="score"), tier="factors"
    )

    scores = store.read(duckdb.connect(), "ovoli", date(2024, 10, 1), date(2024, 10, 1)).df()
    factors = store.read(
        duckdb.connect(), "ovoli", date(2024, 10, 1), date(2024, 10, 1), tier="factors"
    ).df()

    assert "frost" not in scores and "score" in scores
    assert factors["frost"].tolist() == [1.0]
    assert store.partition_path("ovoli", 2024, tier="factors").exists()


def test_upsert_takes_staged_parquet_files(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path / "scores")
    staged = []
    for i, day in enumerate([date(2024, 12, 31), date(2025, 1, 1)]):
        path = tmp_path / f"chunk_{i}.parquet"
        _frame([day], 0.1 * (i + 1)).to_parquet(path)
        staged.append(path)

    store.upsert("combined", staged)

    rows = store.read(duckdb.connect(), "combined", date(2024, 1, 1), date(2025, 12, 31)).df()
    assert rows["score"].tolist() == [0.1, 0.2]
