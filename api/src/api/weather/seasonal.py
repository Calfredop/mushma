"""Long-range forecast ingest for the seasonal outlook (M6): Open-Meteo's Seasonal Forecast API.

    uv run python -m api.weather.seasonal fetch      # daily, after the weather update

Open-Meteo's default seasonal model is ECMWF's seamless pair: EC46 for the first 46 days, SEAS5
after. Both are raw, coarse (about 36 km) model output, so mushma keeps only the **weekly** (EC46)
and **monthly** (SEAS5) ensemble means together with their anomalies against each model's own
hindcast climate, and maps them onto the weather store's variable names
(``config/weather.yaml`` -> ``seasonal``). The same weather points are asked for as the rest of the
weather, so the areas aggregate them with the same weights.

Rows: ``source, point_id, kind (week | month), start, end, variable, value, anomaly, fetched_at``.
``value - anomaly`` is the model's normal for the period. Each fetch replaces the previous one:
only the latest run is kept, in ``$DATA_DIR/outlook/<region>/seasonal.parquet``.
"""

import argparse
import calendar
import json
import time
import urllib.parse
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pandas as pd

from api.grid.region import load_region
from api.grid.sources import data_dir, load_sources
from api.weather.config import SeasonalVariable, WeatherConfig, load_weather_config
from api.weather.ingest import MAX_POINTS_PER_REQUEST, Point, region_paths, request_points_of
from api.weather.openmeteo import REFERENCE_DAYS, REFERENCE_VARIABLES, Client, RateBudget

# EC46 runs every day; a fetch younger than this is reused rather than asked for again.
SEASONAL_MAX_AGE_S = 12 * 3600
GRANULARITIES = ("weekly", "monthly")
KIND = {"weekly": "week", "monthly": "month"}
COLUMNS = [
    "source",
    "point_id",
    "kind",
    "start",
    "end",
    "variable",
    "value",
    "anomaly",
    "fetched_at",
]


@dataclass(frozen=True)
class SeasonalRequest:
    endpoint: str
    source: str
    points: list[Point]
    granularity: str  # weekly or monthly
    variables: dict[str, SeasonalVariable]  # weather-store name -> how the API names it
    timezone: str
    forecast_days: int

    @property
    def model(self) -> str:
        """The cache folder (``Client.cache_path``)."""
        return self.source

    @property
    def label(self) -> str:
        return f"{self.granularity}-{self.forecast_days}d"

    @property
    def api_variables(self) -> list[str]:
        return [name for v in self.variables.values() for name in (v.mean, v.anomaly)]

    def weight(self) -> float:
        """Counted like a daily request over the same horizon, per location: an estimate, as
        Open-Meteo does not publish the seasonal API's weights."""
        variables = len(self.api_variables) / REFERENCE_VARIABLES
        per_location = max(1.0, variables * self.forecast_days / REFERENCE_DAYS)
        return per_location * len(self.points)

    def url(self) -> str:
        params = {
            "latitude": ",".join(_coord(lat) for _, lat, _ in self.points),
            "longitude": ",".join(_coord(lon) for _, _, lon in self.points),
            self.granularity: ",".join(self.api_variables),
            "timezone": self.timezone,
            "forecast_days": str(self.forecast_days),
            "temperature_unit": "celsius",
            "precipitation_unit": "mm",
        }
        return f"{self.endpoint}?{urllib.parse.urlencode(params, safe=',/')}"


def _coord(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def seasonal_points(points: pd.DataFrame, stride: int) -> list[Point]:
    """Land weather points thinned by ``stride`` (1 = all; 3 ≈ 0.6° on a 0.2° lattice)."""
    land = request_points_of(points)
    stride = max(1, stride)
    return land[::stride]


def seasonal_requests(
    config: WeatherConfig, points: list[Point], timezone: str
) -> list[SeasonalRequest]:
    """The weekly requests, then the monthly ones, each batch of points under the weight cap."""
    spec = config.seasonal
    if spec is None:
        raise ValueError("weather.yaml has no seasonal section")
    requests = []
    for granularity in GRANULARITIES:
        if granularity not in spec.forecast_days:
            continue
        template = SeasonalRequest(
            endpoint=spec.endpoint,
            source=spec.source,
            points=points[:1],
            granularity=granularity,
            variables=spec.variables,
            timezone=timezone,
            forecast_days=spec.forecast_days[granularity],
        )
        size = max(
            1, min(MAX_POINTS_PER_REQUEST, int(config.max_request_weight // template.weight()))
        )
        requests += [
            replace(template, points=points[i : i + size]) for i in range(0, len(points), size)
        ]
    return requests


def _period_end(kind: str, start: date) -> date:
    if kind == "week":
        return start + timedelta(days=6)
    return start.replace(day=calendar.monthrange(start.year, start.month)[1])


def parse_seasonal(
    payload: list | dict, request: SeasonalRequest, fetched_at: datetime
) -> pd.DataFrame:
    """Long rows (see the module docstring); periods without a mean are dropped."""
    locations = payload if isinstance(payload, list) else [payload]
    if len(locations) != len(request.points):
        raise ValueError(
            f"expected {len(request.points)} locations, got {len(locations)} "
            f"from {request.source} {request.label}"
        )
    kind = KIND[request.granularity]
    frames = []
    for (point_id, _, _), location in zip(request.points, locations, strict=True):
        units = location.get(f"{request.granularity}_units", {})
        block = location[request.granularity]
        starts = pd.to_datetime(pd.Series(block["time"])).dt.date
        for variable, spec in request.variables.items():
            for name, expected in ((spec.mean, spec.unit), (spec.anomaly, spec.anomaly_unit)):
                if units.get(name) != expected:
                    raise ValueError(
                        f"{request.source} returned {name} in {units.get(name)!r}, "
                        f"expected {expected!r}"
                    )
            values = pd.Series(block[spec.mean], dtype="float64")
            anomalies = pd.Series(block[spec.anomaly], dtype="float64")
            present = values.notna()
            frames.append(
                pd.DataFrame(
                    {
                        "point_id": point_id,
                        "kind": kind,
                        "start": starts[present].to_numpy(),
                        "end": [_period_end(kind, s) for s in starts[present]],
                        "variable": variable,
                        "value": values[present].to_numpy(),
                        "anomaly": anomalies[present].to_numpy(),
                    }
                )
            )
    rows = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=COLUMNS)
    rows.insert(0, "source", request.source)
    rows["fetched_at"] = fetched_at
    return rows[COLUMNS]


def fetch_seasonal(
    client: Client,
    config: WeatherConfig,
    points: pd.DataFrame,
    timezone: str,
    max_age_s: float | None = SEASONAL_MAX_AGE_S,
) -> pd.DataFrame:
    """Every weekly and monthly value for the land points, from the cache when fresh."""
    frames = []
    stride = config.seasonal.point_stride if config.seasonal else 1
    for request in seasonal_requests(config, seasonal_points(points, stride), timezone):
        envelope = client.fetch_envelope(request, max_age_s)
        fetched_at = datetime.fromtimestamp(envelope["fetched_at"], UTC)
        frames.append(parse_seasonal(envelope["payload"], request, fetched_at))
    return pd.concat(frames, ignore_index=True)


def outlook_dir(region: str, root: Path | None = None) -> Path:
    return (root or data_dir()) / "outlook" / region


def write_seasonal(rows: pd.DataFrame, config: WeatherConfig, folder: Path) -> Path:
    """Replace the stored run with ``rows``, with a ``meta.json`` of when and whose it is."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "seasonal.parquet"
    partial = path.with_name(path.name + ".part")
    rows.to_parquet(partial, index=False)
    partial.replace(path)
    spec = config.seasonal
    catalog = load_sources()
    meta = {
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "fetched_at": rows["fetched_at"].max().isoformat() if not rows.empty else None,
        "endpoint": spec.endpoint if spec else None,
        "rows": len(rows),
        "sources": {
            source_id: {
                "name": catalog[source_id].name,
                "license": catalog[source_id].license,
                "attribution": catalog[source_id].attribution,
            }
            for source_id in (spec.credits if spec else [])
        },
    }
    (folder / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["fetch"])
    parser.add_argument("--region", default="tuscany")
    parser.add_argument("--per-day", type=float, help="override the daily call budget")
    args = parser.parse_args()

    config = load_weather_config()
    region = load_region(args.region)
    _, store, raw = region_paths(region.id)
    budget = RateBudget(
        per_minute=config.budget.per_minute,
        per_hour=config.budget.per_hour,
        per_day=args.per_day or config.budget.per_day,
        ledger=raw / "open_meteo" / "usage.json",
    )
    client = Client(cache_dir=raw / "open_meteo", budget=budget)
    started = time.monotonic()
    points = pd.read_parquet(store.points_path)
    rows = fetch_seasonal(client, config, points, region.timezone)
    path = write_seasonal(rows, config, outlook_dir(region.id))
    periods = rows.groupby("kind")["start"].agg(["min", "max", "nunique"]).to_dict("index")
    print(
        f"[{time.monotonic() - started:7.1f}s] seasonal: {len(rows)} rows -> {path} "
        f"({json.dumps(periods, default=str)}, calls today {client.budget.used_today:.0f})",
        flush=True,
    )


if __name__ == "__main__":
    main()
