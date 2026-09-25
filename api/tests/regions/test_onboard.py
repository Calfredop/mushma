"""Region onboarding command: step selection, resumption, summary."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import pytest

from api.regions import onboard


@dataclass
class FakeResult:
    returncode: int = 0


def test_select_steps_default_is_the_full_chain() -> None:
    assert onboard.select_steps() == list(onboard.STEP_NAMES)


def test_select_steps_from_and_only() -> None:
    assert onboard.select_steps(from_step="sightings") == [
        "sightings",
        "score",
        "history",
        "backtest",
        "sanity",
    ]
    assert onboard.select_steps(only_step="cds") == ["cds"]
    with pytest.raises(ValueError, match="unknown step"):
        onboard.select_steps(only_step="nope")


def test_parse_years_defaults_and_ranges() -> None:
    today = date(2026, 9, 24)
    assert onboard.parse_years(None, today) == onboard.YearsRange(2016, 2026)
    assert onboard.parse_years("2018-2022", today).as_flag() == "2018-2022"
    assert onboard.parse_years("2020,2022,2021", today) == onboard.YearsRange(2020, 2022)


def test_resumption_skips_steps_whose_outputs_exist(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    region = "tuscany"
    root = tmp_path / "data"
    monkeypatch.setenv("DATA_DIR", str(root))

    # Grid + points present → those steps skip; cds not ready → runs (and needs a fake key).
    grid = root / "grid" / region
    grid.mkdir(parents=True)
    cells = pd.DataFrame(
        {
            "cell_id": ["1kmE1N1"],
            "woodland": [True],
            "forest_fraction": [0.8],
            "region_fraction": [1.0],
        }
    )
    cells.to_parquet(grid / "cells.parquet", index=False)
    (grid / "meta.json").write_text(
        json.dumps({"cell_count": 1, "woodland_cell_count": 1, "forest_area_ha": 80.0}) + "\n"
    )
    weather = root / "weather" / region
    weather.mkdir(parents=True)
    pd.DataFrame({"point_id": ["N1"], "land": [True], "lat": [43.0], "lon": [11.0]}).to_parquet(
        weather / "points.parquet", index=False
    )

    monkeypatch.setenv("CDSAPI_KEY", "uid:test-key")
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        return FakeResult()

    docs = tmp_path / "docs"
    onboard.run_onboard(
        region,
        years=onboard.YearsRange(2024, 2024),
        only_step=None,
        from_step="grid",
        today=date(2026, 9, 18),
        runner=runner,
        root=root,
        docs_dir=docs,
        write_doc=True,
    )

    # grid and points skipped; first real call is cds backfill
    assert calls, "cds (and later steps) should run"
    assert any("api.weather.ingest" in c and "cds" in c for c in calls)
    assert not any("api.grid.build" in c for c in calls)
    assert not any(c[2:] == ["api.weather.ingest", "points", "--region", region] for c in calls)


def test_cds_fails_clearly_without_a_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CDSAPI_KEY", raising=False)
    monkeypatch.setattr(onboard, "resolve_cds_key", onboard.resolve_cds_key)
    # Ensure ~/.cdsapirc is not used: stub resolve to raise.
    from api.weather.cds import CdsCredentialsError

    def missing() -> str:
        raise CdsCredentialsError("CDS API key missing: set CDSAPI_KEY=uid:key")

    monkeypatch.setattr(onboard, "resolve_cds_key", missing)
    with pytest.raises(SystemExit, match="CDS API key missing"):
        onboard.ensure_cds_credentials()


def test_summary_from_stores(tmp_path: Path) -> None:
    region = "tuscany"
    root = tmp_path
    grid = root / "grid" / region
    grid.mkdir(parents=True)
    pd.DataFrame(
        {
            "cell_id": ["a", "b"],
            "woodland": [True, False],
            "forest_fraction": [0.9, 0.1],
            "region_fraction": [1.0, 1.0],
        }
    ).to_parquet(grid / "cells.parquet", index=False)
    (grid / "meta.json").write_text(
        json.dumps(
            {
                "cell_count": 2,
                "woodland_cell_count": 1,
                "forest_area_ha": 1058106.9,
                "infc_bosco_ha": 1035448,
            }
        )
        + "\n"
    )
    weather = root / "weather" / region / "daily" / "source=era5_seamless" / "year=2024"
    weather.mkdir(parents=True)
    (weather / "data.parquet").write_bytes(b"")  # path name only; years_present globs it
    points = root / "weather" / region
    pd.DataFrame({"point_id": ["p"], "land": [True]}).to_parquet(
        points / "points.parquet", index=False
    )

    bt = root / "backtest" / region / "onboard"
    bt.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "group": "porcini",
                "role": "holdout",
                "season": "all",
                "variant": "model",
                "metric": "auc_local",
                "value": 0.477,
            },
            {
                "group": "ovoli",
                "role": "holdout",
                "season": "all",
                "variant": "model",
                "metric": "auc_local",
                "value": 0.531,
            },
        ]
    ).to_csv(bt / "summary.csv", index=False)
    pd.DataFrame({"id": ["a", "b"], "holds": [True, False]}).to_csv(
        bt / "sanity_porcini.csv", index=False
    )

    summary = onboard.collect_summary(region, root)
    assert summary.cells == 2
    assert summary.woodland_cells == 1
    assert summary.infc_ok is True
    assert summary.nodes == 1
    assert summary.years_stored == [2024]
    assert summary.backtest_aucs["porcini"] == pytest.approx(0.477)
    assert summary.sanity_passed == 1 and summary.sanity_total == 2

    doc = onboard.write_region_doc(region, summary, docs_dir=tmp_path / "docs")
    text = doc.read_text()
    assert "## Data" in text
    assert "woodland cells: 1" in text


def test_only_backtest_invokes_holdout_label(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    region = "tuscany"
    root = tmp_path / "data"
    monkeypatch.setenv("DATA_DIR", str(root))
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        # Pretend the backtest wrote its summary so collect_summary has something.
        out = root / "backtest" / region / onboard.BACKTEST_LABEL
        out.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(
            [
                {
                    "group": "porcini",
                    "role": "holdout",
                    "season": "all",
                    "variant": "model",
                    "metric": "auc_local",
                    "value": 0.476912,
                },
                {
                    "group": "ovoli",
                    "role": "holdout",
                    "season": "all",
                    "variant": "model",
                    "metric": "auc_local",
                    "value": 0.531,
                },
                {
                    "group": "gallinacci",
                    "role": "holdout",
                    "season": "all",
                    "variant": "model",
                    "metric": "auc_local",
                    "value": 0.550005,
                },
            ]
        ).to_csv(out / "summary.csv", index=False)
        return FakeResult()

    summary = onboard.run_onboard(
        region,
        only_step="backtest",
        today=date(2026, 9, 18),
        runner=runner,
        root=root,
        docs_dir=tmp_path / "docs",
        write_doc=False,
    )
    assert len(calls) == 1
    assert calls[0][2:] == [
        "api.model.backtest",
        "run",
        "--region",
        "tuscany",
        "--seasons",
        "holdout",
        "--label",
        "onboard",
        "--allow-holdout",
    ]
    # Numbers match the current tuned-holdout report (model, all, auc_local).
    assert summary.backtest_aucs["porcini"] == pytest.approx(0.476912, abs=1e-5)
    assert summary.backtest_aucs["gallinacci"] == pytest.approx(0.550005, abs=1e-5)


def test_tuscany_summary_matches_tuned_holdout_report() -> None:
    """``--only backtest`` report numbers: auc_local from the shipped hold-out summary."""
    root = Path(__file__).resolve().parents[2] / "data"
    summary_csv = root / "backtest" / "tuscany" / "tuned-holdout" / "summary.csv"
    if not summary_csv.is_file():
        pytest.skip("no local tuned-holdout report")
    expected = onboard._read_backtest_aucs(root, "tuscany", label="tuned-holdout")
    # Current report (model-v1-validation.md hold-out, model / all / auc_local).
    assert expected["porcini"] == pytest.approx(0.476912, abs=1e-4)
    assert expected["gallinacci"] == pytest.approx(0.550005, abs=1e-4)
    assert "ovoli" in expected


def test_tuscany_dry_run_skips_everything_when_data_is_present(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Against the real local DATA_DIR, a full onboard should skip every step."""
    root = Path(__file__).resolve().parents[2] / "data"
    if not (root / "grid" / "tuscany" / "cells.parquet").is_file():
        pytest.skip("no local Tuscany stores")
    monkeypatch.setenv("DATA_DIR", str(root))
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        return FakeResult()

    # score_ready needs last_run.end covering the window for today; use a fixed "today" that the
    # local meta can satisfy, or accept that update/score may still run.
    meta = json.loads((root / "scores" / "tuscany" / "meta.json").read_text())
    last_end = date.fromisoformat(meta["last_run"]["end"])
    today = last_end - __import__("datetime").timedelta(days=7)

    summary = onboard.run_onboard(
        "tuscany",
        years=onboard.YearsRange(2016, 2026),
        today=today,
        runner=runner,
        root=root,
        write_doc=False,
    )
    assert summary.woodland_cells and summary.woodland_cells > 10_000
    assert summary.nodes == 103
    assert 2016 in summary.years_stored
    # Prefer skip; update/score may still fire if the window moved — not grid/cds.
    modules = [c[2] for c in calls]
    assert "api.grid.build" not in modules
    assert not any("cds" in c for c in calls)


def test_cds_step_stops_where_the_reanalysis_has_settled(tmp_path: Path) -> None:
    """ERA5-Land runs days behind: the CDS step ends where the ingest's own default does, and the
    Open-Meteo update step fills the days after."""
    from api.weather.ingest import SETTLE_DAYS

    today = date(2026, 9, 25)
    specs = onboard.step_specs("tuscany", onboard.YearsRange(2016, 2026), today, tmp_path)

    args = specs["cds"].args_lists[0]
    end = date.fromisoformat(args[args.index("--end") + 1])
    assert end == today - timedelta(days=SETTLE_DAYS + 1)
    assert args[args.index("--start") + 1] == "2016-01-01"


def test_cds_step_keeps_a_past_years_end() -> None:
    today = date(2026, 9, 25)
    specs = onboard.step_specs("tuscany", onboard.YearsRange(2016, 2024), today, Path("/nowhere"))

    args = specs["cds"].args_lists[0]
    assert args[args.index("--end") + 1] == "2024-12-31"
