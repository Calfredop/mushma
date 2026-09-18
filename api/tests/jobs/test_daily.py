"""The scheduled daily job (M4-api.md): weather + sightings ingest, then score the served window."""

import json
from dataclasses import dataclass
from datetime import date

import pytest

from api.jobs import daily


@dataclass
class FakeResult:
    returncode: int = 0


def test_runs_weather_then_sightings_then_scores_the_served_window() -> None:
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        return FakeResult()

    daily.main(today=date(2026, 9, 18), runner=runner, alert=lambda message: None)

    assert calls == [
        [daily.sys.executable, "-m", "api.weather.ingest", "update"],
        [daily.sys.executable, "-m", "api.sightings.ingest", "fetch"],
        [
            daily.sys.executable,
            "-m",
            "api.model.pipeline",
            "score",
            "--start",
            "2026-09-12",
            "--end",
            "2026-09-25",
        ],
    ]


def test_score_window_is_six_days_back_to_seven_forward() -> None:
    assert daily.score_window(date(2026, 9, 18)) == (date(2026, 9, 12), date(2026, 9, 25))


def test_stops_and_alerts_on_the_first_failing_step() -> None:
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        return FakeResult(returncode=1 if "update" in args else 0)

    alerts: list[str] = []
    with pytest.raises(SystemExit):
        daily.main(today=date(2026, 9, 18), runner=runner, alert=alerts.append)

    assert len(calls) == 1, "the sightings fetch and the score step must not run after a failure"
    assert alerts and "update" in alerts[0]


def test_no_alert_on_success() -> None:
    alerts: list[str] = []
    daily.main(today=date(2026, 9, 18), runner=lambda args: FakeResult(), alert=alerts.append)
    assert alerts == []


def test_structured_logs_are_one_json_object_per_line(capsys: pytest.CaptureFixture[str]) -> None:
    daily.main(
        today=date(2026, 9, 18), runner=lambda args: FakeResult(), alert=lambda message: None
    )
    lines = [line for line in capsys.readouterr().out.splitlines() if line]
    events = [json.loads(line)["event"] for line in lines]
    assert events[0] == "job_start"
    assert events[-1] == "job_done"
    assert events.count("step_start") == 3
    assert events.count("step_done") == 3


def test_a_failed_step_is_logged_and_the_job_failure_is_logged_too(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def runner(args: list[str]) -> FakeResult:
        return FakeResult(returncode=1)

    with pytest.raises(SystemExit):
        daily.main(today=date(2026, 9, 18), runner=runner, alert=lambda message: None)

    events = [json.loads(line)["event"] for line in capsys.readouterr().out.splitlines() if line]
    assert events == ["job_start", "step_start", "step_failed", "job_failed"]
