"""Weather ingest: point set, history backfill, daily update and cell export.

    uv run python -m api.weather.ingest points              # once, after the grid is built
    uv run python -m api.weather.ingest backfill [--wait]   # resumable; newest year first
    uv run python -m api.weather.ingest update              # daily: recent reanalysis + forecast
    uv run python -m api.weather.ingest downscale --start 2024-10-01 --end 2024-10-31

Raw responses are cached under ``$DATA_DIR/raw/open_meteo/``; the normalized table lives in
``$DATA_DIR/weather/<region>/`` (see ``api.weather.store``). Every command is safe to re-run.
"""

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import duckdb
import pandas as pd

from api.grid.region import load_region
from api.grid.sources import data_dir, load_sources
from api.weather.config import WeatherConfig, load_weather_config
from api.weather.downscale import cell_weather
from api.weather.openmeteo import (
    HOUR_MARGIN_S,
    BudgetExhausted,
    Client,
    DailyRequest,
    RateBudget,
    RateLimited,
    parse_daily,
    seconds_until_next_window,
    sleep_until,
)
from api.weather.points import candidate_points, footprint_elevation, interpolation_weights
from api.weather.store import WeatherStore

# A history chunk ending this many days ago is past the reanalysis delay: cache it for good.
SETTLE_DAYS = 10
# Responses that may still change (recent reanalysis days, forecasts) are re-fetched when older.
PROVISIONAL_MAX_AGE_S = 6 * 3600
FORECAST_MAX_AGE_S = 3 * 3600
# Open-Meteo takes up to 1,000 locations per call; smaller batches keep URLs short.
MAX_POINTS_PER_REQUEST = 100

Log = Callable[[str], None]
Point = tuple[str, float, float]


def _batches(points: list[Point], per_point_weight: float, max_weight: float) -> list[list[Point]]:
    size = max(1, min(MAX_POINTS_PER_REQUEST, int(max_weight // per_point_weight)))
    return [points[i : i + size] for i in range(0, len(points), size)]


def request_points_of(points: pd.DataFrame) -> list[Point]:
    land = points[points["land"]] if "land" in points else points
    land = land.sort_values("point_id")
    return list(zip(land["point_id"], land["lat"], land["lon"], strict=True))


def _units(config: WeatherConfig, names: list[str] | None = None) -> dict[str, str]:
    names = names or list(config.variables)
    return {name: config.variables[name].unit for name in names}


def history_requests(
    config: WeatherConfig, points: list[Point], timezone: str, start: date, end: date
) -> list[DailyRequest]:
    """Archive requests for ``start..end``: one calendar year at a time, newest first, each
    batch of points kept under the configured weight."""
    requests = []
    for year in range(end.year, start.year - 1, -1):
        first, last = max(start, date(year, 1, 1)), min(end, date(year, 12, 31))
        template = DailyRequest(
            endpoint=config.history.endpoint,
            model=config.history.model,
            points=points[:1],
            units=_units(config),
            timezone=timezone,
            start_date=first,
            end_date=last,
        )
        for batch in _batches(points, template.weight(), config.max_request_weight):
            requests.append(replace(template, points=batch))
    return requests


def forecast_requests(
    config: WeatherConfig, points: list[Point], timezone: str
) -> list[DailyRequest]:
    template = DailyRequest(
        endpoint=config.forecast.endpoint,
        model=config.forecast.model,
        points=points[:1],
        units=_units(config),
        timezone=timezone,
        past_days=config.forecast.past_days,
        forecast_days=config.forecast.forecast_days,
    )
    return [
        replace(template, points=batch)
        for batch in _batches(points, template.weight(), config.max_request_weight)
    ]


def load_request(
    client: Client, store: WeatherStore, request: DailyRequest, max_age_s: float | None
) -> pd.DataFrame:
    envelope = client.fetch_envelope(request, max_age_s)
    fetched_at = datetime.fromtimestamp(envelope["fetched_at"], UTC)
    rows, cells = parse_daily(envelope["payload"], request, fetched_at)
    store.upsert_daily(rows)
    store.upsert_point_cells(cells)
    return rows


def build_points(
    client: Client,
    config: WeatherConfig,
    timezone: str,
    cells: pd.DataFrame,
    store: WeatherStore,
    log: Log = print,
) -> pd.DataFrame:
    """Find the land nodes around woodland cells and store them with the cell weights."""
    spacing = config.points.spacing_deg
    woodland = cells[cells["woodland"]]
    candidates = candidate_points(woodland, spacing)
    probe = config.points.land_probe
    request_points = request_points_of(candidates)
    template = DailyRequest(
        endpoint=config.history.endpoint,
        model=probe.model,
        points=request_points[:1],
        units=_units(config, probe.variables),
        timezone=timezone,
        start_date=probe.date,
        end_date=probe.date,
    )
    frames, model_cells = [], []
    for batch in _batches(request_points, template.weight(), config.max_request_weight):
        request = replace(template, points=batch)
        envelope = client.fetch_envelope(request)
        fetched_at = datetime.fromtimestamp(envelope["fetched_at"], UTC)
        rows, found = parse_daily(envelope["payload"], request, fetched_at)
        frames.append(rows)
        model_cells.append(found)
    rows = pd.concat(frames, ignore_index=True)
    found = pd.concat(model_cells, ignore_index=True)
    store.upsert_point_cells(found)

    complete = rows.groupby("point_id")["variable"].nunique() == len(probe.variables)
    points = candidates.assign(land=candidates["point_id"].map(complete).fillna(False).astype(bool))
    points = points.merge(
        found[["point_id", "elevation_m"]].rename(columns={"elevation_m": "grid_elevation_m"}),
        on="point_id",
        how="left",
    )
    points["dem_elevation_m"] = footprint_elevation(cells, points, spacing).to_numpy()
    land = points[points["land"]]
    weights = pd.concat(
        [
            interpolation_weights(
                woodland, land, spacing, method, config.points.max_distance_km
            ).assign(method=method)
            for method in ("bilinear", "nearest")
        ],
        ignore_index=True,
    )[["method", "cell_id", "point_id", "weight"]]
    used = weights[weights["method"] == "bilinear"].groupby("point_id")["cell_id"].nunique()
    points["woodland_cells"] = points["point_id"].map(used).fillna(0).astype(int)

    store.root.mkdir(parents=True, exist_ok=True)
    points.to_parquet(store.points_path, index=False)
    weights.to_parquet(store.weights_path, index=False)
    unserved = sorted(set(woodland["cell_id"]) - set(weights["cell_id"]))
    log(
        f"points: {len(points)} candidates at {spacing}°, {int(points['land'].sum())} on land; "
        f"{weights['cell_id'].nunique()} woodland cells weighted, {len(unserved)} out of reach"
    )
    return points


@dataclass
class BackfillStatus:
    fetched: int = 0
    skipped: int = 0
    weight: float = 0.0
    incomplete: list[str] = field(default_factory=list)
    paused: str | None = None
    remaining: int = 0

    @property
    def done(self) -> bool:
        return self.paused is None and not self.incomplete


def backfill(
    client: Client,
    config: WeatherConfig,
    store: WeatherStore,
    points: pd.DataFrame,
    timezone: str,
    end: date,
    today: date,
    start: date | None = None,
    log: Log = print,
) -> BackfillStatus:
    """Fetch every history chunk the store does not have yet, newest first, until the budget
    runs out. Re-run to resume: chunks already in the store are skipped without a call."""
    start = start or config.history.start_date
    request_points = request_points_of(points)
    requests = history_requests(config, request_points, timezone, start, end)
    variables = list(config.variables)
    status = BackfillStatus()
    for index, request in enumerate(requests):
        ids = [pid for pid, _, _ in request.points]
        if store.has_complete(request.model, ids, request.start_date, request.end_date, variables):
            status.skipped += 1
            continue
        settled = request.end_date < today - timedelta(days=SETTLE_DAYS)
        max_age_s = None if settled else PROVISIONAL_MAX_AGE_S
        try:
            cached = client.cached(request, max_age_s) is not None
            rows = load_request(client, store, request, max_age_s)
        except (BudgetExhausted, RateLimited) as error:
            status.paused = str(error)
            status.remaining = len(requests) - index
            log(f"paused with {status.remaining} requests left: {error}")
            break
        if not cached:
            status.fetched += 1
            status.weight += request.weight()
        expected = len(ids) * request.days * len(variables)
        if settled and len(rows) < expected:
            # Past the reanalysis delay a gap is unexpected: keep what came, re-ask next run.
            status.incomplete.append(request.label)
            client.forget(request)
        log(
            f"history {request.label} x{len(ids)} points: {len(rows)}/{expected} values"
            f"{'' if cached else f', {request.weight():.0f} calls'}"
            f" (today {client.budget.used_today:.0f})"
        )
    return status


# How long ``run_until_done`` waits after a network failure, and after a chunk came back with gaps.
NETWORK_RETRY_S = 600
INCOMPLETE_RETRY_S = 3600
MAX_INCOMPLETE_ROUNDS = 3


def run_until_done(
    run: Callable[[], BackfillStatus],
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.time,
    log: Log = print,
) -> BackfillStatus:
    """Repeat a backfill until it is done: sleep past a server-side daily limit (to just after
    00:00 UTC), retry network failures, and give up on chunks still incomplete after a few
    rounds."""
    incomplete_rounds = 0
    while True:
        try:
            status = run()
        except OSError as error:
            log(f"network error, retrying in {NETWORK_RETRY_S}s: {error}")
            sleep(NETWORK_RETRY_S)
            continue
        if status.done:
            return status
        if status.paused:
            now = clock()
            wait = seconds_until_next_window(now, 86400) + HOUR_MARGIN_S
            log(f"paused ({status.paused}); sleeping {wait / 3600:.1f} h until the next UTC day")
            sleep_until(now + wait, clock, sleep)
            continue
        incomplete_rounds += 1
        if incomplete_rounds >= MAX_INCOMPLETE_ROUNDS:
            log(
                f"giving up: still incomplete after {incomplete_rounds} rounds: {status.incomplete}"
            )
            return status
        log(f"incomplete {status.incomplete}; retrying in {INCOMPLETE_RETRY_S}s")
        sleep(INCOMPLETE_RETRY_S)


def update(
    client: Client,
    config: WeatherConfig,
    store: WeatherStore,
    points: pd.DataFrame,
    timezone: str,
    today: date,
    log: Log = print,
) -> dict:
    """Daily refresh: reanalysis days published since the last run, then the forecast."""
    request_points = request_points_of(points)
    ids = [pid for pid, _, _ in request_points]
    start = today - timedelta(days=config.history.recent_days)
    last = store.last_complete_date(config.history.model, ids)
    if last is not None:
        start = min(start, last + timedelta(days=1))
    start = max(start, config.history.start_date)
    end = today - timedelta(days=1)
    summary = {"history_values": 0, "forecast_values": 0, "history_start": str(start)}
    for request in history_requests(config, request_points, timezone, start, end):
        summary["history_values"] += len(
            load_request(client, store, request, PROVISIONAL_MAX_AGE_S)
        )
    for request in forecast_requests(config, request_points, timezone):
        summary["forecast_values"] += len(load_request(client, store, request, FORECAST_MAX_AGE_S))
    summary["history_last_complete"] = str(store.last_complete_date(config.history.model, ids))
    log(f"update: {json.dumps(summary)} (calls today {client.budget.used_today:.0f})")
    return summary


def write_meta(config: WeatherConfig, store: WeatherStore, region: str) -> Path:
    """``meta.json`` next to the weather table: sources and credits, points and downscaling."""
    sources = load_sources()
    meta = {
        "region": region,
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "history": {
            "model": config.history.model,
            "endpoint": config.history.endpoint,
            "start_date": str(config.history.start_date),
        },
        "forecast": {
            "model": config.forecast.model,
            "endpoint": config.forecast.endpoint,
            "past_days": config.forecast.past_days,
            "forecast_days": config.forecast.forecast_days,
        },
        "source_order": config.source_order,
        "points": {
            "spacing_deg": config.points.spacing_deg,
            "stride": config.points.stride,
            "max_distance_km": config.points.max_distance_km,
        },
        "variables": {
            name: {
                "unit": v.unit,
                "downscale": v.downscale,
                "lapse_rate_c_per_km": v.lapse_rate_c_per_km,
            }
            for name, v in config.variables.items()
        },
        "sources": {
            source_id: {
                "name": sources[source_id].name,
                "homepage": sources[source_id].homepage,
                "license": sources[source_id].license,
                "attribution": sources[source_id].attribution,
            }
            for source_id in config.credits
        },
    }
    store.root.mkdir(parents=True, exist_ok=True)
    path = store.root / "meta.json"
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    return path


def region_paths(region_id: str, root: Path | None = None) -> tuple[Path, WeatherStore, Path]:
    root = root or data_dir()
    return root / "grid" / region_id, WeatherStore(root / "weather" / region_id), root / "raw"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["points", "backfill", "update", "downscale"])
    parser.add_argument("--region", default="tuscany")
    parser.add_argument("--start", type=date.fromisoformat)
    parser.add_argument("--end", type=date.fromisoformat)
    parser.add_argument(
        "--wait", action="store_true", help="backfill: keep going through daily limits until done"
    )
    parser.add_argument("--per-day", type=float, help="override the daily call budget")
    args = parser.parse_args()

    config = load_weather_config()
    region = load_region(args.region)
    grid_dir, store, raw = region_paths(region.id)
    budget = RateBudget(
        per_minute=config.budget.per_minute,
        per_hour=config.budget.per_hour,
        per_day=args.per_day or config.budget.per_day,
        wait_for_day=args.wait,
        ledger=raw / "open_meteo" / "usage.json",
    )
    client = Client(cache_dir=raw / "open_meteo", budget=budget)
    today = datetime.now(ZoneInfo(region.timezone)).date()
    started = time.monotonic()

    def log(message: str) -> None:
        print(f"[{time.monotonic() - started:7.1f}s] {message}", flush=True)

    write_meta(config, store, region.id)
    if args.command == "points":
        cells = pd.read_parquet(
            grid_dir / "cells.parquet", columns=["cell_id", "lon", "lat", "elevation_m", "woodland"]
        )
        build_points(client, config, region.timezone, cells, store, log)
        return

    points = pd.read_parquet(store.points_path)
    if args.command == "backfill":
        # Newer days are still arriving in the archive: the daily update fetches those.
        end = args.end or today - timedelta(days=SETTLE_DAYS + 1)

        def run() -> BackfillStatus:
            now = datetime.now(ZoneInfo(region.timezone)).date()
            return backfill(
                client, config, store, points, region.timezone, end, now, args.start, log
            )

        status = run_until_done(run, log=log) if args.wait else run()
        log(f"backfill: {json.dumps(status.__dict__ | {'done': status.done})}")
    elif args.command == "update":
        update(client, config, store, points, region.timezone, today, log)
    else:
        start = args.start or today - timedelta(days=7)
        end = args.end or today + timedelta(days=config.forecast.forecast_days - 1)
        cells = pd.read_parquet(grid_dir / "cells.parquet", columns=["cell_id", "elevation_m"])
        weights = pd.read_parquet(store.weights_path)
        cells = cells[cells["cell_id"].isin(weights["cell_id"])]
        out = store.root / "cells" / f"{start:%Y%m%d}-{end:%Y%m%d}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        con = duckdb.connect()
        relation = cell_weather(
            con, store, cells, weights, start, end, config.variables, config.source_order
        )
        relation.write_parquet(str(out), compression="zstd")
        (count,) = con.execute(f"SELECT count(*) FROM read_parquet('{out}')").fetchone()
        log(f"downscale: {count} values -> {out}")


if __name__ == "__main__":
    main()
