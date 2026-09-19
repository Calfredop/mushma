"""The scheduled daily job (M4-api.md): weather + sightings ingest, then score the served window."""

import json
from dataclasses import dataclass
from datetime import date

import pytest

from api.jobs import daily


@dataclass
class FakeResult:
    returncode: int = 0


def test_runs_ingest_scoring_then_the_time_views_steps() -> None:
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
        [daily.sys.executable, "-m", "api.history.build", "update", "--years", "2026-2026"],
        [daily.sys.executable, "-m", "api.weather.seasonal", "fetch"],
        [daily.sys.executable, "-m", "api.history.build", "outlook"],
    ]


def test_early_january_updates_last_years_history_too() -> None:
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        return FakeResult()

    daily.main(today=date(2027, 1, 3), runner=runner, alert=lambda message: None)

    history = next(args for args in calls if "api.history.build" in args and "update" in args)
    assert history[-1] == "2026-2027"


def test_a_long_range_forecast_outage_comes_after_the_days_scores() -> None:
    calls: list[list[str]] = []

    def runner(args: list[str]) -> FakeResult:
        calls.append(args)
        return FakeResult(returncode=1 if "api.weather.seasonal" in args else 0)

    with pytest.raises(SystemExit):
        daily.main(today=date(2026, 9, 18), runner=runner, alert=lambda message: None)

    modules = [args[2] for args in calls]
    assert modules.index("api.model.pipeline") < modules.index("api.weather.seasonal")
    assert modules.index("api.history.build") < modules.index("api.weather.seasonal")


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
    assert events.count("step_start") == 6
    assert events.count("step_done") == 6


def test_a_failed_step_is_logged_and_the_job_failure_is_logged_too(
    capsys: pytest.CaptureFixture[str],
) -> None:
    def runner(args: list[str]) -> FakeResult:
        return FakeResult(returncode=1)

    with pytest.raises(SystemExit):
        daily.main(today=date(2026, 9, 18), runner=runner, alert=lambda message: None)

    events = [json.loads(line)["event"] for line in capsys.readouterr().out.splitlines() if line]
    assert events == ["job_start", "step_start", "step_failed", "job_failed"]


def test_heartbeat_fires_once_the_job_succeeds() -> None:
    heartbeats: list[None] = []
    daily.main(
        today=date(2026, 9, 18),
        runner=lambda args: FakeResult(),
        alert=lambda message: None,
        heartbeat=lambda: heartbeats.append(None),
    )
    assert len(heartbeats) == 1


def test_no_heartbeat_on_failure() -> None:
    heartbeats: list[None] = []

    def runner(args: list[str]) -> FakeResult:
        return FakeResult(returncode=1)

    with pytest.raises(SystemExit):
        daily.main(
            today=date(2026, 9, 18),
            runner=runner,
            alert=lambda message: None,
            heartbeat=lambda: heartbeats.append(None),
        )
    assert heartbeats == []


def test_send_heartbeat_is_a_no_op_without_a_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(daily.HEARTBEAT_ENV, raising=False)
    daily.send_heartbeat()  # must not raise / must not attempt a request


def test_send_heartbeat_pings_the_configured_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(daily.HEARTBEAT_ENV, "https://hc-ping.com/some-id")
    requested: list[str] = []
    monkeypatch.setattr(
        daily.urllib.request,
        "urlopen",
        lambda request, timeout: requested.append(request.full_url),
    )
    daily.send_heartbeat()
    assert requested == ["https://hc-ping.com/some-id"]
