import json
from datetime import date, timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pytest

from api.model.pipeline import rules_version, run_scoring
from api.model.store import ScoreStore

from ..weather.test_downscale import _store
from .test_inputs import write_grid

CELL_HIGH, CELL_LOW = "1kmE4400N2300", "1kmE4401N2300"
SPECIES_KEYS = [
    "porcini_edulis",
    "porcini_reticulatus",
    "porcini_aereus",
    "porcini_pinophilus",
    "ovoli_caesarea",
    "gallinacci_cibarius",
]


def _data_root(tmp_path: Path, first: date, days: int) -> Path:
    """A grid of two woodland cells fed by one weather point with a wet, mild autumn."""
    root = tmp_path / "data"
    write_grid(root / "grid" / "tuscany")
    rows = []
    for i in range(days):
        day = first + timedelta(days=i)
        source = "era5_seamless" if i < days - 4 else "ecmwf_ifs"
        daily = {
            "precipitation_sum": 12.0 if i % 9 == 0 else 1.0,
            "snowfall_sum": 0.0,
            "temperature_2m_min": 9.0,
            "temperature_2m_max": 19.0,
            "temperature_2m_mean": 14.0,
            "soil_temperature_0_to_7cm_mean": 15.0,
            "et0_fao_evapotranspiration": 1.5,
        }
        rows += [(source, "A", day, name, value) for name, value in daily.items()]
    store = _store(
        root / "weather" / "tuscany",
        rows,
        {("era5_seamless", "A"): 600.0, ("ecmwf_ifs", "A"): 600.0},
    )
    weights = []
    for cell in (CELL_HIGH, CELL_LOW):
        weights += [("bilinear", cell, "A", 1.0), ("nearest", cell, "A", 1.0)]
    pd.DataFrame(weights, columns=["method", "cell_id", "point_id", "weight"]).to_parquet(
        store.weights_path
    )
    return root


FIRST = date(2024, 8, 1)
START, END = date(2024, 10, 20), date(2024, 10, 24)


@pytest.fixture
def scored(tmp_path: Path) -> tuple[ScoreStore, Path]:
    root = _data_root(tmp_path, FIRST, 86)  # to 25 October, the last 4 days forecast
    run_scoring("tuscany", START, END, data_root=root)
    return ScoreStore(root / "scores" / "tuscany"), root


def _read(store: ScoreStore, key: str) -> pd.DataFrame:
    return store.read(duckdb.connect(), key, START, END).df()


def _factors(store: ScoreStore, key: str) -> pd.DataFrame:
    return store.read(duckdb.connect(), key, START, END, tier="factors").df()


def _keys(store: ScoreStore, tier: str) -> list[str]:
    return store.keys(tier=tier)


def test_scoring_stores_every_species_key_group_and_the_combined_score(scored) -> None:
    store, _ = scored

    assert sorted(store.keys()) == sorted(
        [*SPECIES_KEYS, "porcini", "ovoli", "gallinacci", "combined"]
    )
    for key in store.keys():
        rows = _read(store, key)
        assert len(rows) == 2 * 5, key
        assert rows["score"].between(0, 1).all(), key


def test_species_rows_carry_the_score_forecast_flag_and_rule_version(scored) -> None:
    store, _ = scored

    rows = _read(store, "porcini_edulis")

    assert set(rows.columns) == {"cell_id", "date", "score", "forecast", "rules_version"}
    assert set(rows["rules_version"]) == {rules_version()}
    assert rows["forecast"].tolist().count(True) == 2 * 3


def test_the_factor_tier_carries_each_enabled_factor_with_its_input(scored) -> None:
    store, _ = scored

    rows = _factors(store, "porcini_edulis")

    assert len(rows) == 2 * 5
    for column in ("season", "habitat", "altitude", "rain_trigger", "rain_trigger__input"):
        assert column in rows, column
    assert "rain_trigger__days_ago" in rows
    assert "soil_temperature" not in rows  # disabled
    assert "porcini" not in _keys(store, "factors")  # groups have no factors of their own


def test_history_can_be_scored_without_the_factor_tier(tmp_path: Path) -> None:
    root = _data_root(tmp_path, FIRST, 86)

    run_scoring("tuscany", START, END, data_root=root, factors=False)

    store = ScoreStore(root / "scores" / "tuscany")
    assert len(store.keys()) == 10
    assert store.keys(tier="factors") == []


def test_scoring_in_small_chunks_gives_the_same_rows(tmp_path: Path, scored) -> None:
    store, _ = scored
    root = _data_root(tmp_path / "chunked", FIRST, 86)

    run_scoring("tuscany", START, END, data_root=root, cell_days_per_chunk=5)

    chunked = ScoreStore(root / "scores" / "tuscany")
    for key in ("gallinacci_cibarius", "porcini", "combined"):
        pd.testing.assert_frame_equal(_read(chunked, key), _read(store, key))
    pd.testing.assert_frame_equal(
        _factors(chunked, "ovoli_caesarea"), _factors(store, "ovoli_caesarea")
    )


def test_the_factor_values_multiply_back_to_the_score(scored) -> None:
    store, _ = scored
    from api.model.rules import load_rules

    rules = load_rules().species["ovoli_caesarea"]
    rows = _factors(store, "ovoli_caesarea").merge(_read(store, "ovoli_caesarea"))
    drivers = [f for f in rules.enabled_factors if f.role == "driver"]
    total = sum(f.weight for f in drivers)
    product = np.ones(len(rows))
    for factor in rules.enabled_factors:
        exponent = factor.weight / total if factor.role == "driver" else 1.0
        product *= rows[factor.id].to_numpy() ** exponent

    assert product == pytest.approx(rows["score"].to_numpy(), abs=1e-6)


def test_group_scores_are_the_max_of_their_keys_and_name_the_winner(scored) -> None:
    store, _ = scored
    porcini = _read(store, "porcini").set_index(["cell_id", "date"])
    keys = pd.concat(
        {
            key: _read(store, key).set_index(["cell_id", "date"])["score"]
            for key in SPECIES_KEYS[:4]
        },
        axis=1,
    )

    assert porcini["score"].to_numpy() == pytest.approx(keys.max(axis=1).to_numpy(), abs=1e-6)
    winners = porcini["source_key"]
    for (cell, day), winner in winners.items():
        assert keys.loc[(cell, day), winner] == pytest.approx(porcini.loc[(cell, day), "score"])


def test_combined_names_the_winning_group_and_key(scored) -> None:
    store, _ = scored
    combined = _read(store, "combined")
    groups = {
        g: _read(store, g).set_index(["cell_id", "date"])
        for g in ("porcini", "ovoli", "gallinacci")
    }

    for row in combined.itertuples():
        if row.source_group is None or pd.isna(row.source_group):
            assert row.score == 0
            continue
        group = groups[row.source_group].loc[(row.cell_id, row.date)]
        assert row.score == pytest.approx(group["score"])
        assert row.source_key == group["source_key"]


def test_rescoring_replaces_rows_and_records_the_run(scored) -> None:
    store, root = scored

    run_scoring("tuscany", END, END + timedelta(days=1), data_root=root)

    rows = store.read(duckdb.connect(), "ovoli", START, END + timedelta(days=1)).df()
    assert len(rows) == 2 * 6
    meta = json.loads((store.root / "meta.json").read_text())
    assert meta["rules_version"] == rules_version()
    assert meta["groups"]["porcini"] == SPECIES_KEYS[:4]
    assert "open_meteo" in meta["sources"]


def test_a_period_without_enough_lookback_weather_is_refused(tmp_path: Path) -> None:
    root = _data_root(tmp_path, FIRST, 90)

    with pytest.raises(ValueError, match="lookback"):
        run_scoring("tuscany", date(2024, 8, 10), date(2024, 8, 12), data_root=root)
