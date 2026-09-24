"""The scheduled daily job (M4-api.md): keep the served window fresh.

Runs the same commands the README documents for a human to run by hand, in order: top up
weather (new reanalysis days + the forecast), fetch recent sightings, then score today -6 to +7
(the window the app serves) with the factor breakdown kept. Then the time views (M6): rebuild this
season's per-area history, fetch the long-range forecast and average it over the areas.

There's no separate "downscale to cells" step: scoring reads the point-level weather store and
downscales on the fly (``api.model.inputs.load_weather``) -- the ingest CLI's own ``downscale``
command only writes a standalone export nothing else reads, so running it here would just be unused
disk churn on the server. deploy/mushma-daily.timer runs this every morning as a one-off container
of the API image; it must finish well before 07:00 Europe/Rome.

Each step is a child process, so one step's crash can't take the others down with a shared
in-process state. Every step runs for every served region in turn; one region's failure is logged
and alerted but does not stop the others. Every step logs one JSON line on start and on completion,
so ``journalctl -u mushma-daily`` can be grepped for ``"event": "step_failed"``. On failure, an
optional webhook (``ALERT_WEBHOOK_URL``) gets a one-line summary; unset, it's a no-op -- the failed
systemd unit still records it either way. The job also logs the weighted Open-Meteo calls spent
today (shared ledger under ``$DATA_DIR/raw/open_meteo/usage.json``). One heartbeat as before.

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
from pathlib import Path
from typing import Protocol

from api.grid.sources import data_dir
from api.regions import list_served_region_ids
from api.timeutil import today_rome
from api.weather.openmeteo import RateBudget

WINDOW_BACK_DAYS = 6
WINDOW_FORWARD_DAYS = 7
ALERT_WEBHOOK_ENV = "ALERT_WEBHOOK_URL"
ALERT_TIMEOUT_S = 10
HEARTBEAT_ENV = "HEARTBEAT_URL"
HEARTBEAT_TIMEOUT_S = 10


class StepResult(Protocol):
    returncode: int


Runner = Callable[[list[str]], StepResult]
Alert = Callable[[str], None]
Heartbeat = Callable[[], None]


def score_window(today: date) -> tuple[date, date]:
    return today - timedelta(days=WINDOW_BACK_DAYS), today + timedelta(days=WINDOW_FORWARD_DAYS)


def _steps(today: date, region: str) -> list[list[str]]:
    start, end = score_window(today)
    return [
        [sys.executable, "-m", "api.weather.ingest", "update", "--region", region],
        [sys.executable, "-m", "api.sightings.ingest", "fetch", "--region", region],
        [
            sys.executable,
            "-m",
            "api.model.pipeline",
            "score",
            "--region",
            region,
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
            "--region",
            region,
            "--years",
            f"{start.year}-{today.year}",
        ],
        [sys.executable, "-m", "api.weather.seasonal", "fetch", "--region", region],
        [sys.executable, "-m", "api.history.build", "outlook", "--region", region],
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


def send_heartbeat() -> None:
    """A dead-man's-switch ping (healthchecks.io-style: a plain GET) for a run that finished --
    `send_alert` only fires if the job runs and fails, not if the scheduler never runs it at all."""
    url = os.environ.get(HEARTBEAT_ENV)
    if not url:
        return
    try:
        urllib.request.urlopen(urllib.request.Request(url), timeout=HEARTBEAT_TIMEOUT_S)
    except (urllib.error.URLError, OSError) as error:
        _log(event="heartbeat_failed", error=str(error))


def open_meteo_calls_today(root: Path | None = None) -> float:
    """Weighted Open-Meteo calls spent today from the shared ledger (0 if none yet)."""
    ledger = (root or data_dir()) / "raw" / "open_meteo" / "usage.json"
    path = ledger if ledger.exists() else None
    budget = RateBudget(per_minute=1, per_hour=1, per_day=1, ledger=path)
    return budget.used_today


def _run_step(args: list[str], runner: Runner, *, region: str) -> None:
    step = " ".join(args[2:])  # drop the interpreter and "-m"
    _log(event="step_start", region=region, step=step)
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


def main(
    *,
    today: date | None = None,
    runner: Runner = subprocess.run,
    alert: Alert = send_alert,
    heartbeat: Heartbeat = send_heartbeat,
    regions: list[str] | None = None,
    root: Path | None = None,
) -> None:
    today = today or today_rome()
    served = regions if regions is not None else list_served_region_ids(root)
    if not served:
        served = ["tuscany"]
    started = time.monotonic()
    _log(event="job_start", job="daily", date=today, regions=served)
    failed_regions: list[str] = []
    for region in served:
        current = "startup"
        region_started = time.monotonic()
        try:
            for args in _steps(today, region):
                current = " ".join(args[2:])
                _run_step(args, runner, region=region)
        except SystemExit:
            _log(
                event="region_failed",
                region=region,
                step=current,
                elapsed_s=round(time.monotonic() - region_started, 1),
            )
            alert(
                f"mushma daily job failed for region {region!r} at step {current!r} "
                "-- see journalctl -u mushma-daily"
            )
            failed_regions.append(region)
            continue
        _log(
            event="region_done",
            region=region,
            elapsed_s=round(time.monotonic() - region_started, 1),
        )
    calls = open_meteo_calls_today(root)
    _log(event="open_meteo_calls", weighted_calls_today=round(calls, 1))
    if failed_regions:
        _log(
            event="job_failed",
            job="daily",
            failed_regions=failed_regions,
            elapsed_s=round(time.monotonic() - started, 1),
        )
        raise SystemExit(1)
    _log(event="job_done", job="daily", elapsed_s=round(time.monotonic() - started, 1))
    heartbeat()


if __name__ == "__main__":
    main()
