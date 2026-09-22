"""Backtest: do sightings fall on cell-days the rules score highly?

    uv run python -m api.model.backtest run --seasons train --label priors
    uv run python -m api.model.backtest run --seasons holdout --label v1 --allow-holdout

For every season it scores every woodland cell and day (model, and three baselines built from the
same gates), then ranks each sighting's score against backgrounds that correct for how sightings
are collected (see ``.gavin-root/docs/model-v1-validation.md``):

- ``auc_region``: every woodland cell-day of the season. Naive: season and habitat alone win it.
- ``auc_day``: every other woodland cell on the sighting's day. Removes when people went out.
- ``auc_local``: other woodland cells within ``radius_km`` on that day. Also removes where people
  live and walk: a sighting is only compared with places its finder could as easily have visited.
- ``auc_time``: the sighting's own cell on the other days within ``window_days``. Removes where,
  so it tests timing alone.
- ``auc_time_effort``: the same, each day weighted by how many fungi of any kind people recorded in
  the region that day (plus one), so busy weekends and October do not flatter the model.

Baselines per group (max over its keys, like the model): ``habitat`` (habitat affinity alone,
required by the PRD), ``static`` (habitat x altitude and any other cell attribute), ``calendar``
(every gate, season included: the rules with the weather taken out). The model has to beat
``calendar`` to show the weather adds anything.

Sightings are unique (group, cell, day) records not flagged obscured; the hold-out seasons are only
scored with ``--allow-holdout``, once tuning is frozen.
"""

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from api.grid.sources import data_dir
from api.model import metrics
from api.model.arrays import Cells, Weather
from api.model.config import BacktestSplit, ModelConfig, load_model_config
from api.model.effort import daily_effort
from api.model.engine import (
    SpeciesScores,
    combine_groups,
    group_scores,
    required_lookback,
    score_species,
)
from api.model.inputs import load_cells, load_normals, load_weather
from api.model.pipeline import rules_version
from api.model.rules import RuleSet, load_rules
from api.sightings.config import load_sightings_config
from api.sightings.http import JsonClient
from api.sightings.store import SightingsStore
from api.weather.config import load_weather_config
from api.weather.ingest import region_paths

VARIANTS = ("model", "calendar", "static", "habitat")
AUC_METRICS = ("auc_region", "auc_day", "auc_local", "auc_time", "auc_time_effort")
RADIUS_KM = 20
WINDOW_DAYS = 30
CELL_DAYS_PER_CHUNK = 400_000

WeatherLoader = Callable[[Cells, date, date], Weather]
Log = Callable[[str], None]


# --- sightings -----------------------------------------------------------------------------------


def load_presences(store: SightingsStore, cell_ids: np.ndarray, seasons: list[int]) -> pd.DataFrame:
    """Unique, unobscured ``(group, cell_id, date)`` sightings on scored cells in ``seasons``."""
    columns = ["group", "cell_id", "date", "season"]
    if not store.record_files():
        return pd.DataFrame(columns=columns)
    rows = duckdb.execute(
        f"""
        SELECT DISTINCT species AS "group", cell_id, date, year(date) AS season
        FROM read_parquet('{store.records_glob}', hive_partitioning = false)
        WHERE NOT obscured AND year(date) IN (SELECT unnest(?)) AND cell_id IN (SELECT unnest(?))
        ORDER BY date, "group", cell_id
        """,
        [list(seasons), [str(c) for c in cell_ids]],
    ).df()
    rows["date"] = pd.to_datetime(rows["date"]).dt.date
    return rows[columns].reset_index(drop=True)


# --- scoring a season ----------------------------------------------------------------------------


@dataclass(frozen=True)
class SeasonScores:
    season: int
    cell_ids: np.ndarray  # (cells,)
    dates: np.ndarray  # (days,) datetime64[D], the whole calendar year
    scores: dict[tuple[str, str], np.ndarray]  # (variant, group) -> (cells, days) float32
    winners: dict[str, int]  # group -> cell-days where it won a positive combined score


def _gate_product(scores: SpeciesScores, kinds: set[str]) -> np.ndarray:
    product = np.ones_like(scores.score)
    for factor in scores.factors:
        if factor.factor.role == "gate" and factor.factor.kind in kinds:
            product = product * factor.value
    return product


_BASELINE_KINDS = {
    "habitat": {"habitat"},
    "static": {"habitat", "static_band"},
    "calendar": {"habitat", "static_band", "season_window"},
}


def score_season(
    rules: RuleSet,
    cells: Cells,
    load: WeatherLoader,
    season: int,
    cell_days_per_chunk: int = CELL_DAYS_PER_CHUNK,
) -> SeasonScores:
    """Model and baseline scores per group for every cell and day of ``season``."""
    start, end = date(season, 1, 1), date(season, 12, 31)
    days = (end - start).days + 1
    lookback = max(required_lookback(spec) for spec in rules.species.values())
    chunk_size = max(1, cell_days_per_chunk // (days + lookback))
    parts: dict[tuple[str, str], list[np.ndarray]] = {}
    winners = {group: 0 for group in rules.groups}
    for first in range(0, len(cells), chunk_size):
        chunk = cells.subset(np.arange(first, min(first + chunk_size, len(cells))))
        weather = load(chunk, start - timedelta(days=lookback), end)
        species = {
            key: score_species(spec, chunk, weather, start, end)
            for key, spec in rules.species.items()
        }
        groups = []
        for group, keys in rules.groups.items():
            members = [species[key] for key in keys]
            model = group_scores(group, members)
            groups.append(model)
            parts.setdefault(("model", group), []).append(model.score.astype(np.float32))
            for variant, kinds in _BASELINE_KINDS.items():
                baseline = np.max([_gate_product(m, kinds) for m in members], axis=0)
                parts.setdefault((variant, group), []).append(baseline.astype(np.float32))
        combined = combine_groups(groups)
        positive = np.nan_to_num(combined.score) > 0
        for index, group in enumerate(rules.groups):
            winners[group] += int(((combined.winner_index == index) & positive).sum())
    return SeasonScores(
        season=season,
        cell_ids=cells.ids,
        dates=np.arange(np.datetime64(start), np.datetime64(end) + np.timedelta64(1, "D")),
        scores={key: np.concatenate(arrays, axis=0) for key, arrays in parts.items()},
        winners=winners,
    )


# --- evaluation ----------------------------------------------------------------------------------


def evaluate_season(
    scores: SeasonScores,
    presences: pd.DataFrame,
    effort: pd.Series | None,
    radius_km: float = RADIUS_KM,
    window_days: int = WINDOW_DAYS,
) -> pd.DataFrame:
    """One row per sighting and variant, with the sighting's score and its AUC against each
    background."""
    cell_index = {cell: i for i, cell in enumerate(scores.cell_ids)}
    centres = metrics.cell_centres_m(scores.cell_ids)
    first_day = scores.dates[0].astype(object)
    effort_weights = np.ones(len(scores.dates))
    if effort is not None:
        days = [first_day + timedelta(days=int(k)) for k in range(len(scores.dates))]
        effort_weights = effort.reindex(days).fillna(0).to_numpy(dtype=float) + 1.0
    sorted_cache: dict[tuple[str, str], np.ndarray] = {}
    rows = []
    for sighting in presences.itertuples(index=False):
        i = cell_index.get(sighting.cell_id)
        j = (sighting.date - first_day).days
        if i is None or not 0 <= j < len(scores.dates):
            continue
        near = metrics.cells_within(sighting.cell_id, scores.cell_ids, radius_km, centres)
        others = np.ones(len(scores.cell_ids), dtype=bool)
        others[i] = False
        low, high = max(0, j - window_days), min(len(scores.dates), j + window_days + 1)
        window = np.arange(low, high)
        window = window[window != j]
        for variant in VARIANTS:
            grid = scores.scores.get((variant, sighting.group))
            if grid is None:
                continue
            score = float(grid[i, j])
            key = (variant, sighting.group)
            if key not in sorted_cache:
                flat = grid.ravel()
                sorted_cache[key] = np.sort(flat[~np.isnan(flat)])
            rows.append(
                {
                    "group": sighting.group,
                    "season": scores.season,
                    "cell_id": sighting.cell_id,
                    "date": sighting.date,
                    "variant": variant,
                    "score": score,
                    "auc_region": _sorted_auc(score, sorted_cache[key]),
                    "auc_day": metrics.presence_auc(score, grid[others, j]),
                    "auc_local": metrics.presence_auc(score, grid[near, j]),
                    "auc_time": metrics.presence_auc(score, grid[i, window]),
                    "auc_time_effort": metrics.presence_auc(
                        score, grid[i, window], effort_weights[window]
                    ),
                }
            )
    return pd.DataFrame(rows)


def _sorted_auc(score: float, background: np.ndarray) -> float:
    if np.isnan(score) or not len(background):
        return float("nan")
    below = np.searchsorted(background, score, side="left")
    tied = np.searchsorted(background, score, side="right") - below
    return float((below + 0.5 * tied) / len(background))


def summarise(per_presence: pd.DataFrame, split: BacktestSplit) -> pd.DataFrame:
    """Mean per-sighting metrics with 90 % bootstrap intervals, per group, role, season (and
    ``all`` seasons of the role) and variant; lifts from the same-day and local percentiles."""
    rows = []
    if per_presence.empty:
        return pd.DataFrame(
            columns=["group", "role", "season", "variant", "metric", "value", "low", "high", "n"]
        )
    frame = per_presence.assign(role=per_presence["season"].map(split.role_of))
    for (group, role, variant), part in frame.groupby(["group", "role", "variant"]):
        seasons = [("all", part)] + [
            (str(season), rows_) for season, rows_ in part.groupby("season")
        ]
        for season, rows_ in seasons:
            for metric in AUC_METRICS:
                values = rows_[metric].to_numpy(dtype=float)
                valid = values[~np.isnan(values)]
                low, high = metrics.bootstrap_interval(valid)
                rows.append(
                    {
                        "group": group,
                        "role": role,
                        "season": season,
                        "variant": variant,
                        "metric": metric,
                        "value": float(valid.mean()) if len(valid) else float("nan"),
                        "low": low,
                        "high": high,
                        "n": int(len(valid)),
                    }
                )
            for name, column, top in (
                ("lift10_day", "auc_day", 0.1),
                ("lift20_day", "auc_day", 0.2),
                ("lift10_local", "auc_local", 0.1),
            ):
                values = rows_[column].to_numpy(dtype=float)
                rows.append(
                    {
                        "group": group,
                        "role": role,
                        "season": season,
                        "variant": variant,
                        "metric": name,
                        "value": metrics.lift(values, top),
                        "low": float("nan"),
                        "high": float("nan"),
                        "n": int((~np.isnan(values)).sum()),
                    }
                )
    return pd.DataFrame(rows)


def objective(summary: pd.DataFrame, group: str, role: str = "train") -> float:
    """What tuning maximises: the mean of the model's pooled local and effort-weighted time AUCs,
    the two metrics that correct for where and when people look."""
    rows = summary[
        (summary.group == group)
        & (summary.role == role)
        & (summary.season == "all")
        & (summary.variant == "model")
        & summary.metric.isin(["auc_local", "auc_time_effort"])
    ]
    return float(rows["value"].mean()) if len(rows) == 2 else float("nan")


# --- running it ----------------------------------------------------------------------------------


@dataclass
class BacktestInputs:
    cells: Cells
    load: WeatherLoader
    sightings: SightingsStore
    effort: pd.Series
    split: BacktestSplit


def prepare(
    region: str,
    seasons: list[int],
    data_root: Path | None = None,
    model_config: ModelConfig | None = None,
) -> BacktestInputs:
    root = data_root or data_dir()
    grid_dir, weather_store, raw_dir = region_paths(region, root)
    model_config = model_config or load_model_config()
    weather_config = load_weather_config()
    cells = load_cells(grid_dir)
    weights = pd.read_parquet(weather_store.weights_path)
    normals = load_normals(root, region)
    con = duckdb.connect()

    def load(chunk: Cells, start: date, end: date) -> Weather:
        return load_weather(
            con, weather_store, chunk, weights, start, end, weather_config, model_config, normals
        )

    place_id = load_sightings_config().inaturalist.place_id
    effort = daily_effort(
        JsonClient(), place_id, sorted(seasons), raw_dir / "inaturalist" / "effort"
    )
    return BacktestInputs(
        cells=cells,
        load=load,
        sightings=SightingsStore(root / "sightings" / region),
        effort=effort,
        split=model_config.backtest,
    )


def run(
    inputs: BacktestInputs,
    rules: RuleSet,
    seasons: list[int],
    log: Log = lambda message: None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[int, dict[str, int]]]:
    """Per-sighting rows, the summary and the combined-score winners per season."""
    presences = load_presences(inputs.sightings, inputs.cells.ids, seasons)
    per_presence, winners = [], {}
    for season in seasons:
        in_season = presences[presences["season"] == season]
        if in_season.empty:
            log(f"{season}: no sightings, skipped")
            continue
        scored = score_season(rules, inputs.cells, inputs.load, season)
        winners[season] = scored.winners
        per_presence.append(evaluate_season(scored, in_season, inputs.effort))
        log(f"{season}: {len(in_season)} sightings evaluated")
    rows = pd.concat(per_presence, ignore_index=True) if per_presence else pd.DataFrame()
    return rows, summarise(rows, inputs.split), winners


def _seasons(argument: str, split: BacktestSplit) -> list[int]:
    named = {"train": split.train_seasons, "holdout": split.holdout_seasons}
    if argument in named:
        return list(named[argument])
    return [int(part) for part in argument.split(",")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("run", help="score seasons and rank their sightings")
    command.add_argument("--seasons", default="train", help="train, holdout, or 2020,2022")
    command.add_argument("--label", required=True, help="output folder name")
    command.add_argument("--region", default="tuscany")
    command.add_argument("--allow-holdout", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()

    def log(message: str) -> None:
        print(f"[{time.monotonic() - started:7.1f}s] {message}", flush=True)

    split = load_model_config().backtest
    seasons = _seasons(args.seasons, split)
    touched = sorted(set(seasons) & set(split.holdout_seasons + split.live_seasons))
    if touched and not args.allow_holdout:
        parser.error(f"seasons {touched} are held out: pass --allow-holdout once tuning is frozen")
    inputs = prepare(args.region, seasons)
    rules = load_rules()
    per_presence, summary, winners = run(inputs, rules, seasons, log)
    out = data_dir() / "backtest" / args.region / args.label
    out.mkdir(parents=True, exist_ok=True)
    per_presence.to_csv(out / "per_sighting.csv", index=False)
    summary.to_csv(out / "summary.csv", index=False)
    (out / "run.json").write_text(
        json.dumps(
            {
                "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
                "rules_version": rules_version(),
                "seasons": seasons,
                "radius_km": RADIUS_KM,
                "window_days": WINDOW_DAYS,
                "combined_winners": winners,
                "objective": {g: objective(summary, g) for g in rules.groups},
            },
            indent=2,
        )
        + "\n"
    )
    log(f"wrote {out}")


if __name__ == "__main__":
    main()
