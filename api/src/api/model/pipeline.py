"""Score every woodland cell for a date range and store the results.

    uv run python -m api.model.pipeline score --start 2025-06-01 --end 2025-12-31
    uv run python -m api.model.pipeline rules      # validate the rule config and summarise it

Reads the woodland grid and the downscaled weather (M2), scores every species key, rolls the keys
up into groups and the combined score, and upserts all of them into ``$DATA_DIR/scores/<region>/``
(see ``api.model.store``). Safe to re-run: a period scored again replaces its rows.
"""

import argparse
import hashlib
import json
import shutil
import tempfile
import time
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from api.grid.sources import data_dir, load_sources
from api.model.arrays import Cells, Weather
from api.model.config import MODEL_FILE, load_model_config
from api.model.engine import (
    COMBINED,
    CombinedScores,
    GroupScores,
    SpeciesScores,
    combine_groups,
    group_scores,
    required_lookback,
    score_species,
)
from api.model.inputs import load_cells, load_normals, load_weather
from api.model.rules import SPECIES_DIR, RuleSet, load_rules
from api.model.store import ScoreStore, Tier
from api.weather.config import load_weather_config
from api.weather.ingest import region_paths

Log = Callable[[str], None]
# Cell-days (targets plus lookback) scored per pass: keeps a run near 1 GB of memory.
CELL_DAYS_PER_CHUNK = 400_000


def rules_version(species_dir: Path = SPECIES_DIR, model_file: Path = MODEL_FILE) -> str:
    """A short hash of the rule files and the model config: which rules produced a score."""
    digest = hashlib.sha256()
    for path in [*sorted(species_dir.glob("*.yaml")), model_file]:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def _grid(scores: SpeciesScores | GroupScores | CombinedScores) -> tuple[np.ndarray, np.ndarray]:
    cells, days = scores.score.shape
    return np.repeat(scores.cell_ids, days), np.tile(scores.dates, cells)


def _keep(scores: SpeciesScores | GroupScores | CombinedScores) -> np.ndarray:
    return ~np.isnan(scores.score.ravel())


def _forecast(scores: SpeciesScores, size: int) -> np.ndarray:
    return scores.forecast.ravel() if scores.forecast is not None else np.zeros(size, dtype=bool)


def species_frames(scores: SpeciesScores, version: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The key's rows for the score tier and for the factor tier."""
    cell_ids, dates = _grid(scores)
    keep = _keep(scores)
    daily = pd.DataFrame(
        {
            "cell_id": cell_ids,
            "date": dates,
            "score": scores.score.ravel().astype(np.float32),
            "forecast": _forecast(scores, len(cell_ids)),
            "rules_version": version,
        }
    )
    columns: dict[str, object] = {"cell_id": cell_ids, "date": dates, "rules_version": version}
    for factor in scores.factors:
        name = factor.factor.id
        columns[name] = np.asarray(factor.value, dtype=np.float32).ravel()
        if factor.input is not None:
            # Inputs are for display ("32 mm, 12 days ago"): two decimals compress far better.
            columns[f"{name}__input"] = np.round(factor.input, 2).astype(np.float32).ravel()
        if factor.days_ago is not None:
            columns[f"{name}__days_ago"] = pd.array(factor.days_ago.ravel(), dtype="Int16")
        if factor.growth_days is not None:
            columns[f"{name}__growth_days"] = (
                np.round(factor.growth_days, 1).astype(np.float32).ravel()
            )
    factors = pd.DataFrame(columns)
    return daily[keep].reset_index(drop=True), factors[keep].reset_index(drop=True)


def group_frame(group: GroupScores) -> pd.DataFrame:
    cell_ids, dates = _grid(group)
    keys = np.array([m.key for m in group.members], dtype=object)
    frame = pd.DataFrame(
        {
            "cell_id": cell_ids,
            "date": dates,
            "score": group.score.ravel().astype(np.float32),
            "source_key": pd.array(keys[group.winner_index.ravel()], dtype="string"),
            "forecast": _forecast(group.members[0], len(cell_ids)),
        }
    )
    return frame[_keep(group)].reset_index(drop=True)


def combined_frame(combined: CombinedScores) -> pd.DataFrame:
    cell_ids, dates = _grid(combined)
    winner = combined.winner_index.ravel()
    group_keys = np.array([g.key for g in combined.groups] + [None], dtype=object)
    member_keys = np.full(winner.shape, None, dtype=object)
    for g, group in enumerate(combined.groups):
        keys = np.array([m.key for m in group.members], dtype=object)
        chosen = winner == g
        member_keys[chosen] = keys[group.winner_index.ravel()[chosen]]
    frame = pd.DataFrame(
        {
            "cell_id": cell_ids,
            "date": dates,
            "score": combined.score.ravel().astype(np.float32),
            # -1 (no group in season) picks the trailing None
            "source_group": pd.array(group_keys[winner], dtype="string"),
            "source_key": pd.array(member_keys, dtype="string"),
            "forecast": _forecast(combined.groups[0].members[0], len(cell_ids)),
        }
    )
    return frame[_keep(combined)].reset_index(drop=True)


def score_frames(
    rules: RuleSet,
    cells: Cells,
    weather: Weather,
    start: date,
    end: date,
    version: str,
    factors: bool = True,
) -> dict[tuple[Tier, str], pd.DataFrame]:
    """Rows per (tier, key) for every species key, group and the combined score."""
    species = {
        key: score_species(spec, cells, weather, start, end) for key, spec in rules.species.items()
    }
    frames: dict[tuple[Tier, str], pd.DataFrame] = {}
    for key, scores in species.items():
        daily, breakdown = species_frames(scores, version)
        frames["daily", key] = daily
        if factors:
            frames["factors", key] = breakdown
    groups = [
        group_scores(group, [species[key] for key in keys]) for group, keys in rules.groups.items()
    ]
    for group in groups:
        frames["daily", group.key] = group_frame(group)
    frames["daily", COMBINED] = combined_frame(combine_groups(groups))
    return frames


def _years(start: date, end: date) -> list[tuple[date, date]]:
    return [
        (max(start, date(year, 1, 1)), min(end, date(year, 12, 31)))
        for year in range(start.year, end.year + 1)
    ]


def _first_weather_day(con: duckdb.DuckDBPyConnection, weather_root: Path) -> date | None:
    files = sorted(weather_root.glob("daily/source=*/year=*/data.parquet"))
    if not files:
        return None
    (first,) = con.execute(
        f"SELECT min(date) FROM read_parquet({[str(f) for f in files]!r})"
    ).fetchone()
    return first


def run_scoring(
    region: str,
    start: date,
    end: date,
    data_root: Path | None = None,
    factors: bool = True,
    cell_days_per_chunk: int = CELL_DAYS_PER_CHUNK,
    log: Log = lambda message: None,
) -> dict:
    """Score ``start..end`` for every woodland cell of ``region`` and upsert the results.

    ``factors=False`` skips the factor tier (the breakdown columns), for long history runs."""
    if end < start:
        raise ValueError(f"end {end} is before start {start}")
    root = data_root or data_dir()
    grid_dir, weather_store, _ = region_paths(region, root)
    rules = load_rules()
    model_config = load_model_config()
    weather_config = load_weather_config()
    version = rules_version()
    lookback = max(required_lookback(spec) for spec in rules.species.values())
    con = duckdb.connect()

    first_needed = start - timedelta(days=lookback)
    first_available = _first_weather_day(con, weather_store.root)
    if first_available is None or first_available > first_needed:
        raise ValueError(
            f"scoring from {start} needs {lookback} days of lookback weather from {first_needed}, "
            f"but the weather store starts {first_available}"
        )

    cells = load_cells(grid_dir)
    weights = pd.read_parquet(weather_store.weights_path)
    normals = load_normals(root, region)
    store = ScoreStore(root / "scores" / region)
    rows_written: dict[str, int] = {}
    missing_cell_days = 0
    for period_start, period_end in _years(start, end):
        days = (period_end - period_start).days + 1
        chunk_size = max(1, cell_days_per_chunk // (days + lookback))
        staging = Path(tempfile.mkdtemp(prefix="staging-", dir=_ensure(store.root)))
        try:
            staged: dict[tuple[Tier, str], list[Path]] = {}
            for n, first in enumerate(range(0, len(cells), chunk_size)):
                chunk = cells.subset(np.arange(first, min(first + chunk_size, len(cells))))
                weather = load_weather(
                    con,
                    weather_store,
                    chunk,
                    weights,
                    period_start - timedelta(days=lookback),
                    period_end,
                    weather_config,
                    model_config,
                    normals,
                )
                frames = score_frames(
                    rules, chunk, weather, period_start, period_end, version, factors
                )
                missing_cell_days += len(chunk) * days - len(frames["daily", COMBINED])
                for (tier, key), frame in frames.items():
                    path = staging / tier / key / f"chunk_{n:05d}.parquet"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    frame.to_parquet(path, index=False)
                    staged.setdefault((tier, key), []).append(path)
                    if tier == "daily":
                        rows_written[key] = rows_written.get(key, 0) + len(frame)
                log(f"{period_start}..{period_end}: scored cells {first + 1}-{first + len(chunk)}")
            for (tier, key), paths in staged.items():
                store.upsert(key, paths, tier=tier)
            log(f"{period_start}..{period_end}: stored {len(staged)} tables")
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    summary = {
        "region": region,
        "start": str(start),
        "end": str(end),
        "rules_version": version,
        "factors": factors,
        "cells": len(cells),
        "rows": rows_written,
        "cell_days_without_weather": missing_cell_days,
    }
    write_meta(store, rules, model_config, weather_config.credits, grid_dir, summary)
    return summary


def _ensure(folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def write_meta(store, rules, model_config, credits, grid_dir: Path, run: dict) -> Path:
    catalog = load_sources()
    source_ids = list(credits)
    grid_meta = grid_dir / "meta.json"
    grid_sources = (
        json.loads(grid_meta.read_text()).get("sources", {}) if grid_meta.exists() else {}
    )
    meta = {
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "rules_version": run["rules_version"],
        "last_run": run,
        "groups": rules.groups,
        "combined": {
            "key": COMBINED,
            "rule": "max over the groups in season; ties go to the group listed first",
        },
        "precipitation_scale": model_config.precipitation_scale.model_dump(),
        "score": "0-1 conditions index, not a probability",
        "sources": {
            **{
                source_id: {
                    "name": catalog[source_id].name,
                    "license": catalog[source_id].license,
                    "attribution": catalog[source_id].attribution,
                }
                for source_id in source_ids
            },
            **grid_sources,
        },
    }
    store.root.mkdir(parents=True, exist_ok=True)
    store.meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False, default=str) + "\n")
    return store.meta_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    score = sub.add_parser("score", help="score a date range and store it")
    score.add_argument("--start", type=date.fromisoformat, required=True)
    score.add_argument("--end", type=date.fromisoformat, required=True)
    score.add_argument("--region", default="tuscany")
    score.add_argument(
        "--no-factors",
        dest="factors",
        action="store_false",
        help="skip the factor tier (breakdown columns): for long history runs",
    )
    sub.add_parser("rules", help="validate the rule config and print a summary")
    args = parser.parse_args()
    started = time.monotonic()

    def log(message: str) -> None:
        print(f"[{time.monotonic() - started:7.1f}s] {message}", flush=True)

    if args.command == "rules":
        rules = load_rules()
        for group, keys in rules.groups.items():
            for key in keys:
                spec = rules.species[key]
                enabled = spec.enabled_factors
                confidence = {
                    c: sum(f.confidence == c for f in enabled)
                    for c in ("strong", "plausible", "folklore")
                }
                print(
                    f"{group:10} {key:22} {len(enabled):2} of {len(spec.factors):2} factors on, "
                    f"lookback {required_lookback(spec):2} d, {confidence}"
                )
        print(f"{len(rules.references)} references, rules version {rules_version()}")
        return
    summary = run_scoring(args.region, args.start, args.end, factors=args.factors, log=log)
    log(json.dumps(summary))


if __name__ == "__main__":
    main()
