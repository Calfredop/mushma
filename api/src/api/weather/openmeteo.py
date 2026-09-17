"""Open-Meteo client: daily weather for many points, cached, batched and within the rate limits.

- :class:`DailyRequest` is one API call: a batch of points, a list of daily variables with the units
  they must come back in, and either a date range (archive) or past/forecast days (forecast). It
  always asks for local days (``timezone``), raw model grid cells (``elevation=nan``,
  ``cell_selection=nearest``) and pinned units.
- :func:`parse_daily` turns a response into long rows ``(source, point_id, date, variable, value)``
  and the model grid cell each point was served from, with that cell's mean height.
- :class:`RateBudget` keeps the weighted call count under Open-Meteo's per-minute, per-hour and
  per-day limits. The server counts in fixed UTC windows, so the budget does too.
- :class:`Client` fetches with a gzip JSON cache, retries server errors with backoff and waits out
  minute and hour rate limits. A daily limit stops the run: resume it later.
"""

import fcntl
import gzip
import hashlib
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import pandas as pd

USER_AGENT = "mushma-weather/0.1"
# Open-Meteo's weight reference: 10 variables over 14 days count as one call per location.
REFERENCE_VARIABLES = 10
REFERENCE_DAYS = 14
# Seconds past a window boundary before trying again: the server resets its hour and day counters
# from a once-a-minute timer.
MINUTE_MARGIN_S = 2
HOUR_MARGIN_S = 65


class RateLimited(RuntimeError):
    """The server refused the request for the rest of the day."""


class BudgetExhausted(RuntimeError):
    """The local daily budget is spent; resume after the next UTC midnight."""


@dataclass(frozen=True)
class DailyRequest:
    endpoint: str
    model: str
    points: list[tuple[str, float, float]]  # (point_id, lat, lon)
    units: dict[str, str]  # daily variable -> expected unit, in request order
    timezone: str
    start_date: date | None = None
    end_date: date | None = None
    past_days: int | None = None
    forecast_days: int | None = None

    @property
    def variables(self) -> list[str]:
        return list(self.units)

    @property
    def days(self) -> int:
        if self.start_date is not None and self.end_date is not None:
            return (self.end_date - self.start_date).days + 1
        return (self.past_days or 0) + (self.forecast_days or 0)

    @property
    def label(self) -> str:
        if self.start_date is not None:
            return f"{self.start_date:%Y%m%d}-{self.end_date:%Y%m%d}"
        return f"past{self.past_days}-next{self.forecast_days}"

    def weight(self) -> float:
        """Calls this request counts as: per location max(1, vars/10 x max(1, days/14))."""
        variables = len(self.units) / REFERENCE_VARIABLES
        per_location = max(1.0, variables, variables * self.days / REFERENCE_DAYS)
        return per_location * len(self.points)

    def url(self) -> str:
        params = {
            "latitude": ",".join(_coord(lat) for _, lat, _ in self.points),
            "longitude": ",".join(_coord(lon) for _, _, lon in self.points),
            "elevation": ",".join("nan" for _ in self.points),
            "cell_selection": "nearest",
            "daily": ",".join(self.units),
            "timezone": self.timezone,
            "models": self.model,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
        }
        if self.start_date is not None:
            params["start_date"] = self.start_date.isoformat()
            params["end_date"] = (self.end_date or self.start_date).isoformat()
        else:
            params["past_days"] = str(self.past_days or 0)
            params["forecast_days"] = str(self.forecast_days or 1)
        return f"{self.endpoint}?{urllib.parse.urlencode(params, safe=',/')}"


def _coord(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def parse_daily(
    payload: list | dict, request: DailyRequest, fetched_at: datetime
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Long daily rows (nulls dropped) and the model grid cell behind each point."""
    locations = payload if isinstance(payload, list) else [payload]
    if len(locations) != len(request.points):
        raise ValueError(
            f"expected {len(request.points)} locations, got {len(locations)} "
            f"from {request.model} {request.label}"
        )
    frames, cells = [], []
    for (pid, _, _), location in zip(request.points, locations, strict=True):
        units = location.get("daily_units", {})
        for variable, expected in request.units.items():
            if units.get(variable) != expected:
                raise ValueError(
                    f"{request.model} returned {variable} in {units.get(variable)!r}, "
                    f"expected {expected!r}"
                )
        daily = location["daily"]
        dates = pd.to_datetime(pd.Series(daily["time"])).dt.date
        for variable in request.units:
            values = pd.Series(daily[variable], dtype="float64")
            present = values.notna()
            frames.append(
                pd.DataFrame(
                    {
                        "point_id": pid,
                        "date": dates[present].to_numpy(),
                        "variable": variable,
                        "value": values[present].to_numpy(),
                    }
                )
            )
        cells.append(
            {
                "source": request.model,
                "point_id": pid,
                "model_lat": float(location["latitude"]),
                "model_lon": float(location["longitude"]),
                "elevation_m": float(location["elevation"]),
                "fetched_at": fetched_at,
            }
        )
    rows = pd.concat(frames, ignore_index=True)
    rows.insert(0, "source", request.model)
    rows["fetched_at"] = fetched_at
    return rows, pd.DataFrame(cells)


@dataclass
class RateBudget:
    """Weighted calls spent in the current UTC minute, hour and day, with waits to stay under.

    The server counts per IP, so separate runs on one machine should share a ``ledger`` file.
    """

    per_minute: float
    per_hour: float
    per_day: float
    clock: Callable[[], float] = time.time
    sleep: Callable[[float], None] = time.sleep
    wait_for_day: bool = False
    ledger: Path | None = None
    _used: dict[int, tuple[int, float]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._load()

    def _load(self) -> None:
        if self.ledger is not None and self.ledger.exists():
            raw = json.loads(self.ledger.read_text())
            self._used = {int(k): (int(w), float(u)) for k, (w, u) in raw.items()}

    def _save(self) -> None:
        if self.ledger is None:
            return
        partial = self.ledger.with_name(self.ledger.name + ".part")
        partial.write_text(json.dumps({str(k): list(v) for k, v in self._used.items()}))
        partial.replace(self.ledger)

    @contextmanager
    def _shared(self) -> Iterator[None]:
        """Hold the ledger lock and work on its latest tally, so parallel runs add up."""
        if self.ledger is None:
            yield
            return
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger.with_name(self.ledger.name + ".lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                self._load()
                yield
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    @property
    def used_today(self) -> float:
        self._load()
        return self._spent(86400, self.clock())

    def _spent(self, window_s: int, now: float) -> float:
        window, used = self._used.get(window_s, (-1, 0.0))
        return used if window == int(now // window_s) else 0.0

    def acquire(self, weight: float) -> None:
        """Block until ``weight`` fits in every window, then record it."""
        limits = ((86400, self.per_day, HOUR_MARGIN_S), (3600, self.per_hour, HOUR_MARGIN_S))
        limits += ((60, self.per_minute, MINUTE_MARGIN_S),)
        while True:
            with self._shared():
                now = self.clock()
                blocked = next(
                    (
                        (window_s, margin, self._spent(window_s, now))
                        for window_s, limit, margin in limits
                        if 0 < self._spent(window_s, now)
                        and self._spent(window_s, now) + weight > limit
                    ),
                    None,
                )
                if blocked is None:
                    for window_s, _, _ in limits:
                        spent = self._spent(window_s, now) + weight
                        self._used[window_s] = (int(now // window_s), spent)
                    self._save()
                    return
            window_s, margin, spent = blocked
            if window_s == 86400 and not self.wait_for_day:
                raise BudgetExhausted(
                    f"daily budget of {self.per_day:.0f} calls spent ({spent:.0f} used); "
                    "resume after 00:00 UTC"
                )
            self.sleep(seconds_until_next_window(now, window_s) + margin)

    def exhaust(self, window_s: int) -> None:
        """Mark a window as spent, e.g. after the server said so."""
        limit = {60: self.per_minute, 3600: self.per_hour, 86400: self.per_day}[window_s]
        with self._shared():
            now = self.clock()
            self._used[window_s] = (int(now // window_s), max(limit, self._spent(window_s, now)))
            self._save()


def seconds_until_next_window(now: float, window_s: int) -> float:
    return math.floor(now / window_s + 1) * window_s - now


@dataclass
class Client:
    cache_dir: Path
    budget: RateBudget
    sleep: Callable[[float], None] = time.sleep
    now: Callable[[], float] = time.time
    retries: int = 4
    backoff_s: float = 5.0
    timeout_s: float = 180.0
    max_rate_limit_waits: int = 30
    calls: int = 0

    def cache_path(self, request: DailyRequest) -> Path:
        digest = hashlib.sha1(request.url().encode()).hexdigest()[:16]
        return self.cache_dir / request.model / f"{request.label}-{digest}.json.gz"

    def cached(self, request: DailyRequest, max_age_s: float | None = None) -> dict | None:
        """The cached envelope ``{fetched_at, url, payload}`` if present and fresh enough."""
        path = self.cache_path(request)
        if not path.exists():
            return None
        envelope = json.loads(gzip.decompress(path.read_bytes()))
        if max_age_s is not None and self.now() - envelope["fetched_at"] > max_age_s:
            return None
        return envelope

    def forget(self, request: DailyRequest) -> None:
        self.cache_path(request).unlink(missing_ok=True)

    def fetch(self, request: DailyRequest, max_age_s: float | None = None) -> list | dict:
        """The response payload, from the cache when fresh (``max_age_s=None``: any age)."""
        return self.fetch_envelope(request, max_age_s)["payload"]

    def fetch_envelope(self, request: DailyRequest, max_age_s: float | None = None) -> dict:
        envelope = self.cached(request, max_age_s)
        if envelope is not None:
            return envelope
        self.budget.acquire(request.weight())
        payload = self._get(request.url())
        self.calls += 1
        envelope = {"fetched_at": self.now(), "url": request.url(), "payload": payload}
        path = self.cache_path(request)
        path.parent.mkdir(parents=True, exist_ok=True)
        partial = path.with_name(path.name + ".part")
        partial.write_bytes(gzip.compress(json.dumps(envelope).encode()))
        partial.replace(path)
        return envelope

    def _get(self, url: str) -> list | dict:
        http = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        failures = 0
        waits = 0
        while True:
            try:
                with urllib.request.urlopen(http, timeout=self.timeout_s) as response:
                    return json.loads(response.read())
            except urllib.error.HTTPError as error:
                reason = _reason(error)
                if error.code == 429:
                    waits += 1
                    if waits > self.max_rate_limit_waits:
                        raise RateLimited(
                            f"still rate limited after {waits - 1} waits: {reason}"
                        ) from error
                    self._wait_out(reason)
                    continue
                if error.code < 500:
                    raise ValueError(
                        f"Open-Meteo rejected the request ({error.code}): {reason}"
                    ) from error
                failure = error
            except (urllib.error.URLError, TimeoutError) as error:
                failure = error
            if failures >= self.retries:
                raise failure
            self.sleep(self.backoff_s * 2**failures)
            failures += 1

    def _wait_out(self, reason: str) -> None:
        now = self.budget.clock()
        text = reason.lower()
        if text.startswith("daily"):
            self.budget.exhaust(86400)
            raise RateLimited(reason)
        if text.startswith("hourly"):
            self.budget.exhaust(3600)
            self.sleep(seconds_until_next_window(now, 3600) + HOUR_MARGIN_S)
        elif text.startswith("minutely"):
            self.budget.exhaust(60)
            self.sleep(seconds_until_next_window(now, 60) + MINUTE_MARGIN_S)
        else:  # too many concurrent requests, or unknown
            self.sleep(self.backoff_s)


def _reason(error: urllib.error.HTTPError) -> str:
    try:
        body = json.loads(error.read())
        return str(body.get("reason", body))
    except (ValueError, OSError):
        return error.reason if isinstance(error.reason, str) else str(error)
