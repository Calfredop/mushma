"""One resumable command for a region's whole data chain.

    uv run python -m api.regions.onboard <region> [--from STEP] [--only STEP] [--years 2016-2026]

Runs grid → weather points → CDS history → Open-Meteo update → sightings → score (history +
served window) → history (update + seasonal + outlook) → backtest → sanity. Each step is a child
process (same pattern as ``api.jobs.daily``). Skips a step when its outputs already exist; safe to
re-run. Honours ``DATA_DIR``. Prints a summary and writes it under a ``## Data`` heading in
``.gavin-root/docs/regions/<region>.md``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Protocol

import pandas as pd

from api.grid.forest import INFC_TOLERANCE, compare_infc_bosco, forest_area_ha
from api.grid.infc import load_infc_bosco
from api.grid.sources import data_dir
from api.jobs.daily import score_window
from api.model.engine import required_lookback
from api.model.rules import load_rules
from api.regions import history_start_date, list_configured_regions
from api.timeutil import today_rome
from api.weather.cds import CdsCredentialsError, resolve_cds_key
from api.weather.ingest import SETTLE_DAYS

STEP_NAMES = (
    "grid",
    "points",
    "cds",
    "update",
    "sightings",
    "score",
    "history",
    "backtest",
    "sanity",
)

BACKTEST_LABEL = "onboard"
DOCS_REGIONS = Path(__file__).resolve().parents[4] / ".gavin-root" / "docs" / "regions"


class StepResult(Protocol):
    returncode: int


Runner = Callable[[list[str]], StepResult]


@dataclass
class YearsRange:
    start: int
    end: int

    def as_flag(self) -> str:
        return f"{self.start}-{self.end}"

    def dates(self, today: date) -> tuple[date, date]:
        start = date(self.start, 1, 1)
        end = date(self.end, 12, 31)
        if self.end == today.year:
            end = min(end, today)
        return start, end


@dataclass
class StepSpec:
    name: str
    args_lists: list[list[str]]
    ready: Callable[[], bool]


@dataclass
class OnboardSummary:
    region: str
    cells: int | None = None
    woodland_cells: int | None = None
    forest_area_ha: float | None = None
    infc_bosco_ha: int | None = None
    infc_deviation: float | None = None
    infc_ok: bool | None = None
    nodes: int | None = None
    years_stored: list[int] = field(default_factory=list)
    sightings_kept: int | None = None
    backtest_aucs: dict[str, float] = field(default_factory=dict)
    sanity_passed: int | None = None
    sanity_total: int | None = None

    def as_dict(self) -> dict:
        return {
            "region": self.region,
            "cells": self.cells,
            "woodland_cells": self.woodland_cells,
            "forest_area_ha": self.forest_area_ha,
            "infc_bosco_ha": self.infc_bosco_ha,
            "infc_deviation": self.infc_deviation,
            "infc_ok": self.infc_ok,
            "nodes": self.nodes,
            "years_stored": self.years_stored,
            "sightings_kept": self.sightings_kept,
            "backtest_aucs": self.backtest_aucs,
            "sanity_passed": self.sanity_passed,
            "sanity_total": self.sanity_total,
        }


def parse_years(text: str | None, today: date | None = None) -> YearsRange:
    today = today or today_rome()
    if not text:
        return YearsRange(history_start_date().year, today.year)
    if "-" in text and "," not in text:
        first, last = text.split("-", 1)
        return YearsRange(int(first), int(last))
    years = sorted(int(part) for part in text.split(","))
    return YearsRange(years[0], years[-1])


def select_steps(*, from_step: str | None = None, only_step: str | None = None) -> list[str]:
    if only_step is not None:
        if only_step not in STEP_NAMES:
            raise ValueError(f"unknown step {only_step!r}; choose from {', '.join(STEP_NAMES)}")
        return [only_step]
    if from_step is not None:
        if from_step not in STEP_NAMES:
            raise ValueError(f"unknown step {from_step!r}; choose from {', '.join(STEP_NAMES)}")
        start = STEP_NAMES.index(from_step)
        return list(STEP_NAMES[start:])
    return list(STEP_NAMES)


def _exe(*module_and_args: str) -> list[str]:
    return [sys.executable, "-m", *module_and_args]


def weather_years_present(root: Path, region: str) -> list[int]:
    daily = root / "weather" / region / "daily"
    if not daily.is_dir():
        return []
    years: set[int] = set()
    for path in daily.glob("source=*/year=*/data.parquet"):
        years.add(int(path.parent.name.removeprefix("year=")))
    return sorted(years)


def cds_years_ready(root: Path, region: str, years: YearsRange) -> bool:
    """True when every year in the range already has daily weather (any source, or CDS meta)."""
    present = set(weather_years_present(root, region))
    needed = set(range(years.start, years.end + 1))
    if needed <= present:
        return True
    meta = root / "weather" / region / "cds_meta.json"
    if not meta.is_file():
        return False
    written = json.loads(meta.read_text())
    covered = set(written.get("years") or [])
    return needed <= covered


def grid_ready(root: Path, region: str) -> bool:
    return (root / "grid" / region / "cells.parquet").is_file()


def points_ready(root: Path, region: str) -> bool:
    return (root / "weather" / region / "points.parquet").is_file()


def update_ready(root: Path, region: str, today: date) -> bool:
    """Forecast partition covering today is present (Open-Meteo update already ran recently)."""
    store = root / "weather" / region / "daily"
    if not store.is_dir():
        return False
    # Skip when this year's daily partition exists; the daily job still refreshes.
    year_dirs = list(store.glob(f"source=*/year={today.year}/data.parquet"))
    return bool(year_dirs)


def sightings_ready(root: Path, region: str) -> bool:
    records = root / "sightings" / region / "records"
    return records.is_dir() and any(records.rglob("data.parquet"))


def score_ready(root: Path, region: str, years: YearsRange, today: date) -> bool:
    """Scores exist and cover at least ``today`` (the daily job keeps the +7 window fresh)."""
    del years  # history-year completeness is checked by the region card, not onboard skip
    meta_path = root / "scores" / region / "meta.json"
    daily = root / "scores" / region / "daily"
    if not meta_path.is_file() or not daily.is_dir() or not any(daily.rglob("*.parquet")):
        return False
    info = json.loads(meta_path.read_text())
    last_end = info.get("last_run", {}).get("end")
    if not last_end:
        return False
    return date.fromisoformat(last_end) >= today


def history_score_range(region: str, years: YearsRange, today: date) -> tuple[date, date]:
    """First scorable day (after weather lookback) through the end of the year range."""
    hist_start, hist_end = years.dates(today)
    rules = load_rules(region)
    lookback = max(required_lookback(spec) for spec in rules.species.values())
    return hist_start + timedelta(days=lookback), hist_end


def history_ready(root: Path, region: str) -> bool:
    return (root / "history" / region).is_dir() and (root / "outlook" / region).is_dir()


def backtest_ready(root: Path, region: str) -> bool:
    folder = root / "backtest" / region
    if (folder / BACKTEST_LABEL / "summary.csv").is_file():
        return True
    # Prior hold-out report (e.g. Tuscany) is enough to skip on a re-onboard.
    return (folder / "tuned-holdout" / "summary.csv").is_file()


def sanity_ready(root: Path, region: str) -> bool:
    folder = root / "backtest" / region
    return any(folder.glob("*/sanity_*.csv"))


def step_specs(
    region: str,
    years: YearsRange,
    today: date,
    root: Path,
) -> dict[str, StepSpec]:
    cds_start, cds_end = years.dates(today)
    # ERA5-Land runs days behind: stop where the ingest's own default does; `update` fills after.
    cds_end = min(cds_end, today - timedelta(days=SETTLE_DAYS + 1))
    hist_score_start, hist_score_end = history_score_range(region, years, today)
    window_start, window_end = score_window(today)
    return {
        "grid": StepSpec(
            "grid",
            [_exe("api.grid.build", "--region", region)],
            lambda: grid_ready(root, region),
        ),
        "points": StepSpec(
            "points",
            [_exe("api.weather.ingest", "points", "--region", region)],
            lambda: points_ready(root, region),
        ),
        "cds": StepSpec(
            "cds",
            [
                _exe(
                    "api.weather.ingest",
                    "backfill",
                    "--source",
                    "cds",
                    "--region",
                    region,
                    "--start",
                    cds_start.isoformat(),
                    "--end",
                    cds_end.isoformat(),
                )
            ],
            lambda: cds_years_ready(root, region, years),
        ),
        "update": StepSpec(
            "update",
            [_exe("api.weather.ingest", "update", "--region", region)],
            lambda: update_ready(root, region, today),
        ),
        "sightings": StepSpec(
            "sightings",
            [_exe("api.sightings.ingest", "fetch", "--region", region)],
            lambda: sightings_ready(root, region),
        ),
        "score": StepSpec(
            "score",
            [
                _exe("api.history.build", "normals", "--region", region),
                _exe(
                    "api.model.pipeline",
                    "score",
                    "--region",
                    region,
                    "--start",
                    hist_score_start.isoformat(),
                    "--end",
                    hist_score_end.isoformat(),
                    "--no-factors",
                ),
                _exe(
                    "api.model.pipeline",
                    "score",
                    "--region",
                    region,
                    "--start",
                    window_start.isoformat(),
                    "--end",
                    window_end.isoformat(),
                ),
            ],
            lambda: score_ready(root, region, years, today),
        ),
        "history": StepSpec(
            "history",
            [
                _exe(
                    "api.history.build",
                    "update",
                    "--region",
                    region,
                    "--years",
                    years.as_flag(),
                ),
                _exe("api.weather.seasonal", "fetch", "--region", region),
                _exe("api.history.build", "outlook", "--region", region),
            ],
            lambda: history_ready(root, region),
        ),
        "backtest": StepSpec(
            "backtest",
            [
                _exe(
                    "api.model.backtest",
                    "run",
                    "--region",
                    region,
                    "--seasons",
                    "holdout",
                    "--label",
                    BACKTEST_LABEL,
                    "--allow-holdout",
                )
            ],
            lambda: backtest_ready(root, region),
        ),
        "sanity": StepSpec(
            "sanity",
            [
                _exe(
                    "api.model.sanity",
                    "--region",
                    region,
                    "--label",
                    BACKTEST_LABEL,
                )
            ],
            lambda: sanity_ready(root, region),
        ),
    }


def _log(**fields: object) -> None:
    print(json.dumps({"ts": time.time(), **fields}, default=str), flush=True)


def _run_child(args: list[str], runner: Runner, *, region: str, step: str) -> None:
    _log(event="step_start", region=region, step=step, cmd=" ".join(args[2:]))
    started = time.monotonic()
    result = runner(args)
    elapsed = round(time.monotonic() - started, 1)
    if result.returncode != 0:
        _log(
            event="step_failed",
            region=region,
            step=step,
            elapsed_s=elapsed,
            returncode=result.returncode,
        )
        raise SystemExit(result.returncode)
    _log(event="step_done", region=region, step=step, elapsed_s=elapsed)


def ensure_cds_credentials() -> None:
    """Fail clearly before spawning the CDS child when the key is missing."""
    try:
        resolve_cds_key()
    except CdsCredentialsError as error:
        raise SystemExit(str(error)) from error


def collect_summary(region: str, root: Path | None = None) -> OnboardSummary:
    root = root or data_dir()
    summary = OnboardSummary(region=region)

    meta_path = root / "grid" / region / "meta.json"
    cells_path = root / "grid" / region / "cells.parquet"
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text())
        summary.cells = meta.get("cell_count")
        summary.woodland_cells = meta.get("woodland_cell_count")
        summary.forest_area_ha = meta.get("forest_area_ha")
        summary.infc_bosco_ha = meta.get("infc_bosco_ha")
    if cells_path.is_file() and summary.forest_area_ha is None:
        cells = pd.read_parquet(
            cells_path, columns=["cell_id", "woodland", "forest_fraction", "region_fraction"]
        )
        summary.cells = summary.cells if summary.cells is not None else int(len(cells))
        summary.woodland_cells = (
            summary.woodland_cells
            if summary.woodland_cells is not None
            else int(cells["woodland"].sum())
        )
        mask = cells[["cell_id", "forest_fraction"]].copy()
        summary.forest_area_ha = round(forest_area_ha(mask, cells), 1)
    if summary.infc_bosco_ha is None:
        summary.infc_bosco_ha = load_infc_bosco().get(region)
    if summary.forest_area_ha is not None and summary.infc_bosco_ha:
        delta, ok = compare_infc_bosco(summary.forest_area_ha, float(summary.infc_bosco_ha))
        summary.infc_deviation = round(delta, 4)
        summary.infc_ok = ok

    points_path = root / "weather" / region / "points.parquet"
    if points_path.is_file():
        points = pd.read_parquet(points_path)
        summary.nodes = int(points["land"].sum()) if "land" in points.columns else int(len(points))
    summary.years_stored = weather_years_present(root, region)

    sightings = root / "sightings" / region / "records"
    if sightings.is_dir() and any(sightings.rglob("data.parquet")):
        import duckdb

        glob = str(sightings / "**" / "data.parquet")
        summary.sightings_kept = int(
            duckdb.execute(f"SELECT count(*) FROM read_parquet('{glob}')").fetchone()[0]
        )

    summary.backtest_aucs = _read_backtest_aucs(root, region)
    sanity_files = sorted((root / "backtest" / region).glob("*/sanity_*.csv"))
    if sanity_files:
        frame = pd.read_csv(sanity_files[0])
        summary.sanity_total = int(len(frame))
        summary.sanity_passed = int(frame["holds"].sum()) if "holds" in frame.columns else None

    return summary


def _read_backtest_aucs(root: Path, region: str, label: str = BACKTEST_LABEL) -> dict[str, float]:
    path = root / "backtest" / region / label / "summary.csv"
    if not path.is_file():
        # Fall back to the shipped hold-out report for Tuscany dry-runs.
        alt = root / "backtest" / region / "tuned-holdout" / "summary.csv"
        path = alt if alt.is_file() else path
    if not path.is_file():
        return {}
    frame = pd.read_csv(path)
    rows = frame[
        (frame["variant"] == "model")
        & (frame["season"].astype(str) == "all")
        & (frame["metric"] == "auc_local")
    ]
    return {str(row.group): float(row.value) for row in rows.itertuples()}


def format_summary(summary: OnboardSummary) -> str:
    lines = [
        f"- cells: {summary.cells}",
        f"- woodland cells: {summary.woodland_cells}",
    ]
    if summary.infc_deviation is not None:
        status = "within ±10 %" if summary.infc_ok else f"outside ±{INFC_TOLERANCE:.0%}"
        lines.append(
            f"- INFC deviation: {summary.infc_deviation:+.1%} "
            f"(grid {summary.forest_area_ha:,.0f} ha vs {summary.infc_bosco_ha:,} ha) — {status}"
        )
    lines.append(f"- weather nodes: {summary.nodes}")
    lines.append(
        f"- years stored: {summary.years_stored[0]}–{summary.years_stored[-1]} "
        f"({len(summary.years_stored)} years)"
        if summary.years_stored
        else "- years stored: none"
    )
    lines.append(f"- sightings kept: {summary.sightings_kept}")
    if summary.backtest_aucs:
        aucs = ", ".join(f"{g} {v:.3f}" for g, v in sorted(summary.backtest_aucs.items()))
        lines.append(f"- backtest AUC (auc_local, model, all): {aucs}")
    if summary.sanity_total is not None:
        lines.append(f"- sanity contrasts: {summary.sanity_passed}/{summary.sanity_total} passed")
    return "\n".join(lines) + "\n"


def write_region_doc(region: str, summary: OnboardSummary, docs_dir: Path = DOCS_REGIONS) -> Path:
    docs_dir.mkdir(parents=True, exist_ok=True)
    path = docs_dir / f"{region}.md"
    body = format_summary(summary)
    section = f"## Data\n\n{body}"
    if path.is_file():
        text = path.read_text()
        if re.search(r"^## Data\b", text, re.MULTILINE):
            text = re.sub(
                r"^## Data\b.*?(?=^## |\Z)",
                section + "\n",
                text,
                count=1,
                flags=re.MULTILINE | re.DOTALL,
            )
        else:
            text = text.rstrip() + "\n\n" + section + "\n"
        path.write_text(text)
    else:
        path.write_text(f"# {region}\n\n{section}\n")
    return path


def run_onboard(
    region: str,
    *,
    years: YearsRange | None = None,
    from_step: str | None = None,
    only_step: str | None = None,
    today: date | None = None,
    runner: Runner = subprocess.run,
    root: Path | None = None,
    docs_dir: Path = DOCS_REGIONS,
    write_doc: bool = True,
) -> OnboardSummary:
    today = today or today_rome()
    root = root or data_dir()
    years = years or parse_years(None, today)
    if region not in list_configured_regions():
        raise SystemExit(f"unknown region {region!r}: add config/regions/{region}.yaml first")

    names = select_steps(from_step=from_step, only_step=only_step)
    specs = step_specs(region, years, today, root)
    started = time.monotonic()
    _log(
        event="job_start",
        job="onboard",
        region=region,
        years=years.as_flag(),
        steps=names,
        data_dir=str(root),
    )

    for name in names:
        spec = specs[name]
        if spec.ready():
            _log(event="step_skipped", region=region, step=name, reason="outputs_exist")
            continue
        if name == "cds":
            ensure_cds_credentials()
        for args in spec.args_lists:
            _run_child(args, runner, region=region, step=name)

    summary = collect_summary(region, root)
    _log(event="summary", **summary.as_dict())
    printed = format_summary(summary)
    print(printed, flush=True)
    if write_doc:
        doc = write_region_doc(region, summary, docs_dir=docs_dir)
        _log(event="doc_written", path=str(doc))
    _log(
        event="job_done",
        job="onboard",
        region=region,
        elapsed_s=round(time.monotonic() - started, 1),
    )
    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("region", help="API region id (e.g. tuscany, emilia_romagna)")
    parser.add_argument(
        "--from", dest="from_step", choices=STEP_NAMES, help="resume from this step"
    )
    parser.add_argument("--only", dest="only_step", choices=STEP_NAMES, help="run only this step")
    parser.add_argument(
        "--years",
        default=None,
        help="history year range for CDS, score and history (default: CDS start–this year)",
    )
    args = parser.parse_args(argv)
    if args.from_step and args.only_step:
        parser.error("use --from or --only, not both")
    today = today_rome()
    years = parse_years(args.years, today)
    run_onboard(
        args.region,
        years=years,
        from_step=args.from_step,
        only_step=args.only_step,
        today=today,
    )


if __name__ == "__main__":
    main()
