"""The scheduled daily job (M4-api.md): keep the served window fresh.

Runs the same commands the README documents for a human to run by hand, in order: top up
weather (new reanalysis days + the forecast), fetch recent sightings, then score today -6 to +7
(the window the app serves) with the factor breakdown kept. Then the time views (M6): rebuild this
season's per-area history, fetch the long-range forecast and average it over the areas.

There's no separate "downscale to cells" step: scoring reads the point-level weather store and
downscales on the fly (``api.model.inputs.load_weather``) -- the ingest CLI's own ``downscale``
command only writes a standalone export nothing else reads, so running it here would just be unused
disk churn on the Fly volume. Fly runs this as the scheduled machine's command (see ``fly.toml``);
it must finish well before 07:00 Europe/Rome.

Each step is a child process, so one step's crash can't take the others down with a shared
in-process state; failure still stops the job (a partial pipeline run is safe to resume tomorrow,
but scoring on top of half-updated weather is not worth risking). Every step logs one JSON line on
start and on completion, so Fly's log viewer can be grepped for ``"event": "step_failed"``. On
failure, an optional webhook (``ALERT_WEBHOOK_URL``) gets a one-line summary; unset, it's a no-op --
Fly's own machine-exit-code alerting still fires either way.

    uv run python -m api.jobs.daily
"""

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import date, timedelta
from typing import Protocol

from api.timeutil import today_rome

WINDOW_BACK_DAYS = 6
WINDOW_FORWARD_DAYS = 7
ALERT_WEBHOOK_ENV = "ALERT_WEBHOOK_URL"
ALERT_TIMEOUT_S = 10


class StepResult(Protocol):
    returncode: int


Runner = Callable[[list[str]], StepResult]
Alert = Callable[[str], None]


def score_window(today: date) -> tuple[date, date]:
    return today - timedelta(days=WINDOW_BACK_DAYS), today + timedelta(days=WINDOW_FORWARD_DAYS)


def _steps(today: date) -> list[list[str]]:
    start, end = score_window(today)
    return [
        [sys.executable, "-m", "api.weather.ingest", "update"],
        [sys.executable, "-m", "api.sightings.ingest", "fetch"],
        [
            sys.executable,
            "-m",
            "api.model.pipeline",
            "score",
            "--start",
            start.isoformat(),
            "--end",
            end.isoformat(),
        ],
        # Time views (M6): this season's per-area stats, then the long-range forecast. The
        # forecast comes last so an outage of the seasonal API never holds back today's scores.
        [
            sys.executable,
            "-m",
            "api.history.build",
            "update",
            "--years",
            f"{start.year}-{today.year}",
        ],
        [sys.executable, "-m", "api.weather.seasonal", "fetch"],
        [sys.executable, "-m", "api.history.build", "outlook"],
    ]


def _log(**fields: object) -> None:
    print(json.dumps({"ts": time.time(), **fields}, default=str), flush=True)


def send_alert(message: str) -> None:
    url = os.environ.get(ALERT_WEBHOOK_ENV)
    if not url:
        return
    request = urllib.request.Request(
        url,
        data=json.dumps({"text": message}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(request, timeout=ALERT_TIMEOUT_S)
    except (urllib.error.URLError, OSError) as error:
        _log(event="alert_failed", error=str(error))


def _run_step(args: list[str], runner: Runner) -> None:
    step = " ".join(args[2:])  # drop the interpreter and "-m"
    _log(event="step_start", step=step)
    started = time.monotonic()
    result = runner(args)
    elapsed = round(time.monotonic() - started, 1)
    if result.returncode != 0:
        _log(event="step_failed", step=step, elapsed_s=elapsed, returncode=result.returncode)
        raise SystemExit(result.returncode)
    _log(event="step_done", step=step, elapsed_s=elapsed)


def main(
    *,
    today: date | None = None,
    runner: Runner = subprocess.run,
    alert: Alert = send_alert,
) -> None:
    today = today or today_rome()
    started = time.monotonic()
    _log(event="job_start", job="daily", date=today)
    current = "startup"
    try:
        for args in _steps(today):
            current = " ".join(args[2:])
            _run_step(args, runner)
    except SystemExit:
        _log(event="job_failed", job="daily", elapsed_s=round(time.monotonic() - started, 1))
        alert(f"mushma daily job failed at step {current!r} -- see Fly logs")
        raise
    _log(event="job_done", job="daily", elapsed_s=round(time.monotonic() - started, 1))


if __name__ == "__main__":
    main()
