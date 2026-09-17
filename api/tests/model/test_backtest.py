from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from api.model.arrays import Cells
from api.model.backtest import (
    AUC_METRICS,
    BacktestInputs,
    SeasonScores,
    evaluate_season,
    load_presences,
    run,
    score_season,
    summarise,
)
from api.model.config import load_model_config
from api.model.rules import RuleSet, SpeciesRules
from api.sightings.store import SightingsStore

from .helpers import cells, weather

FETCHED = datetime(2026, 9, 17, tzinfo=UTC)
A, B, C = "1kmE4400N2300", "1kmE4405N2300", "1kmE4460N2300"  # C is 60 km from A


# --- presences ---------------------------------------------------------------------------------


def _sighting(record_id: str, species: str, cell_id: str, day: date, **extra) -> dict:
    return {
        "species": species,
        "cell_id": cell_id,
        "date": day,
        "source": "gbif",
        "record_id": record_id,
        "license": "CC0",
        "obscured": False,
        "fetched_at": FETCHED,
        **extra,
    }


def test_presences_are_unique_unobscured_cell_days_on_scored_cells_in_the_seasons(
    tmp_path: Path,
) -> None:
    store = SightingsStore(tmp_path)
    day = date(2020, 10, 5)
    store.upsert(
        pd.DataFrame(
            [
                _sighting("1", "porcini", A, day),
                _sighting("2", "porcini", A, day),  # same outing
                _sighting("3", "ovoli", A, day),  # another group, same cell-day
                _sighting("4", "porcini", B, day, obscured=True),  # a village-square pin
                _sighting("5", "porcini", "1kmE9999N9999", day),  # not a scored cell
                _sighting("6", "porcini", B, date(2012, 10, 5)),  # outside the seasons
            ]
        )
    )

    presences = load_presences(store, np.array([A, B]), seasons=[2019, 2020])

    assert presences[["group", "cell_id", "date", "season"]].values.tolist() == [
        ["ovoli", A, day, 2020],
        ["porcini", A, day, 2020],
    ]


# --- scoring a season --------------------------------------------------------------------------


def _toy_rules() -> RuleSet:
    common = {"confidence": "plausible", "source": ["x"], "data": "available"}
    all_year = {"label": "all_year", "dates": ["01-01", "01-01", "31-12", "31-12"]}

    def species(key: str, group: str, affinity: float, altitude: list) -> SpeciesRules:
        return SpeciesRules.model_validate(
            {
                "schema_version": 1,
                "key": key,
                "group": group,
                "taxon": "T",
                "status": "draft",
                "i18n_key": f"species.{key}",
                "records": {"gbif_taxon_keys": [1], "inat_taxon_ids": [1]},
                "factors": [
                    {
                        **common,
                        "id": "season",
                        "role": "gate",
                        "i18n_key": "factor.season",
                        "kind": "season_window",
                        "input": {"windows": [all_year]},
                    },
                    {
                        **common,
                        "id": "habitat",
                        "role": "gate",
                        "i18n_key": "factor.habitat",
                        "kind": "habitat",
                        "input": {"affinity": {"beech": affinity}},
                    },
                    {
                        **common,
                        "id": "altitude",
                        "role": "gate",
                        "i18n_key": "factor.altitude",
                        "kind": "static_band",
                        "input": {"attribute": "elevation_m"},
                        "response": {"trapezoid": altitude},
                    },
                    {
                        **common,
                        "id": "rain",
                        "role": "driver",
                        "weight": 1,
                        "i18n_key": "factor.rain",
                        "kind": "window_aggregate",
                        "input": {
                            "variable": "precipitation_sum",
                            "aggregate": "sum",
                            "window_days": 1,
                        },
                        "response": {"trapezoid": [0, 10, None, None]},
                    },
                ],
            }
        )

    keys = {
        "porcini_a": species("porcini_a", "porcini", 0.5, [0, 1000, None, None]),
        "porcini_b": species("porcini_b", "porcini", 0.8, [None, None, 400, 600]),
        "ovoli_a": species("ovoli_a", "ovoli", 1.0, [None, None, 2000, 3000]),
    }
    return RuleSet(
        species=keys,
        groups={"porcini": ["porcini_a", "porcini_b"], "ovoli": ["ovoli_a"]},
        references={},
    )


def test_score_season_keeps_the_model_and_three_baselines_per_group() -> None:
    here = cells(2, elevation_m=[500, 1000])
    days = 366  # 2020 is a leap year; the toy rules need no lookback

    def load(chunk, start, end):
        assert start == date(2020, 1, 1) and end == date(2020, 12, 31)
        rain = np.full((len(chunk), days), 5.0)
        return weather(start=start, precipitation_sum=rain)

    result = score_season(_toy_rules(), here, load, 2020, cell_days_per_chunk=1)

    assert result.dates[0] == np.datetime64("2020-01-01") and len(result.dates) == 366
    porcini = {
        v: result.scores[v, "porcini"][:, 0] for v in ("habitat", "static", "calendar", "model")
    }
    # gates at 500 m: key a 0.5 x 0.5, key b 0.8 x 0.5; at 1000 m: a 0.5 x 1, b 0. Rain gives 0.5.
    assert porcini["habitat"].tolist() == pytest.approx([0.8, 0.8])
    assert porcini["static"].tolist() == pytest.approx([0.4, 0.5])
    assert porcini["calendar"].tolist() == pytest.approx([0.4, 0.5])
    assert porcini["model"].tolist() == pytest.approx([0.2, 0.25])
    assert result.scores["model", "ovoli"][:, 0].tolist() == pytest.approx([0.5, 0.5])


# --- evaluation --------------------------------------------------------------------------------


def _season_scores(model: np.ndarray, habitat: np.ndarray, ids: list[str]) -> SeasonScores:
    first = np.datetime64("2020-09-01")
    dates = first + np.arange(model.shape[1])
    return SeasonScores(
        season=2020,
        cell_ids=np.array(ids),
        dates=dates,
        scores={("model", "porcini"): model, ("habitat", "porcini"): habitat},
        winners={},
    )


def test_each_sighting_is_ranked_against_every_background() -> None:
    days = 61
    model = np.full((3, days), 0.2)
    model[0, 30] = 0.9  # the sighting's cell-day stands out in time and space
    model[1, 30] = 0.5
    model[2, 30] = 0.95  # a better cell, but 60 km away
    model[0, 10] = 1.0  # one earlier day in the same cell scored higher
    habitat = np.full((3, days), 0.6)
    scores = _season_scores(model, habitat, [A, B, C])
    presences = pd.DataFrame(
        {"group": ["porcini"], "cell_id": [A], "date": [date(2020, 10, 1)], "season": [2020]}
    )
    effort = pd.Series(
        {date(2020, 9, 1) + timedelta(days=i): 0 for i in range(days)}, dtype="int64"
    )
    effort[date(2020, 9, 11)] = 9  # the one higher-scoring day was a busy day

    rows = evaluate_season(scores, presences, effort, radius_km=20, window_days=30)

    model_row = rows[rows.variant == "model"].iloc[0]
    assert model_row["score"] == pytest.approx(0.9)
    assert model_row["auc_day"] == pytest.approx(1 / 2)  # beats B, loses to C
    assert model_row["auc_local"] == 1.0  # only B is within 20 km
    assert model_row["auc_time"] == pytest.approx(59 / 60)
    # the higher day carries weight 9 + 1 against 1 for each of the other 59
    assert model_row["auc_time_effort"] == pytest.approx(59 / 69)
    habitat_row = rows[rows.variant == "habitat"].iloc[0]
    assert habitat_row["auc_local"] == 0.5 and habitat_row["auc_time"] == 0.5


def test_summarise_pools_sightings_per_group_role_and_season() -> None:
    per_presence = pd.DataFrame(
        {
            "group": ["porcini"] * 3,
            "season": [2020, 2022, 2024],
            "cell_id": [A, A, A],
            "date": [date(2020, 10, 1), date(2022, 10, 1), date(2024, 10, 1)],
            "variant": ["model"] * 3,
            "score": [0.9, 0.8, 0.7],
            "auc_region": [0.9, 0.7, 0.8],
            "auc_day": [0.95, 0.5, 0.92],
            "auc_local": [1.0, 0.6, 0.8],
            "auc_time": [0.9, 0.9, 0.3],
            "auc_time_effort": [0.8, 0.9, 0.3],
        }
    )

    summary = summarise(per_presence, load_model_config().backtest)

    def value(role: str, season: str, metric: str) -> pd.Series:
        rows = summary[
            (summary.role == role) & (summary.season == season) & (summary.metric == metric)
        ]
        assert len(rows) == 1
        return rows.iloc[0]

    train = value("train", "all", "auc_local")
    assert train["value"] == pytest.approx(0.8) and train["n"] == 2
    assert value("train", "2022", "auc_local")["value"] == pytest.approx(0.6)
    assert value("holdout", "all", "auc_day")["n"] == 1
    assert value("train", "all", "lift10_day")["value"] == pytest.approx((1 / 2) / 0.1)


def test_sightings_at_random_cell_days_score_no_better_than_chance() -> None:
    rng = np.random.default_rng(3)
    ids = [f"1kmE{4400 + x}N{2300 + y}" for x in range(20) for y in range(20)]
    days = 120
    model = rng.random((len(ids), days)).round(2)  # rounded: plenty of ties
    scores = _season_scores(model, np.full(model.shape, 0.5), ids)
    picks = rng.integers(0, [len(ids), days], size=(400, 2))
    presences = pd.DataFrame(
        {
            "group": "porcini",
            "cell_id": [ids[i] for i, _ in picks],
            "date": [date(2020, 9, 1) + timedelta(days=int(j)) for _, j in picks],
            "season": 2020,
        }
    )
    effort = pd.Series(
        {date(2020, 9, 1) + timedelta(days=i): int(rng.integers(0, 20)) for i in range(days)}
    )

    rows = evaluate_season(scores, presences, effort, radius_km=5, window_days=30)

    means = rows[rows.variant == "model"][list(AUC_METRICS)].mean()
    assert means.to_numpy() == pytest.approx(np.full(5, 0.5), abs=0.04)


def test_run_scores_each_season_with_sightings_and_summarises(tmp_path: Path) -> None:
    here = cells(2, elevation_m=[500, 1000])
    here = Cells(
        ids=np.array([A, B]),
        attributes=here.attributes,
        habitat_names=here.habitat_names,
        habitat_fractions=here.habitat_fractions,
    )
    store = SightingsStore(tmp_path)
    store.upsert(pd.DataFrame([_sighting("1", "porcini", B, date(2020, 10, 5))]))

    def load(chunk, start, end):
        days = (end - start).days + 1
        return weather(start=start, precipitation_sum=np.full((len(chunk), days), 5.0))

    inputs = BacktestInputs(
        cells=here,
        load=load,
        sightings=store,
        effort=pd.Series(dtype="int64"),
        split=load_model_config().backtest,
    )

    per_presence, summary, winners = run(inputs, _toy_rules(), [2019, 2020])

    assert set(per_presence["variant"]) == {"model", "calendar", "static", "habitat"}
    assert per_presence["season"].unique().tolist() == [2020]
    assert list(winners) == [2020]
    assert set(summary["role"]) == {"train"}
