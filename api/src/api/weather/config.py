"""Weather config: sources, variables and downscaling rules, from ``config/weather.yaml``."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from api.weather.points import METHODS

WEATHER_FILE = Path(__file__).resolve().parent.parent / "config" / "weather.yaml"


@dataclass(frozen=True)
class LandProbe:
    model: str
    date: date
    variables: list[str]


@dataclass(frozen=True)
class PointsSpec:
    native_spacing_deg: float
    stride: int
    max_distance_km: float
    land_probe: LandProbe

    @property
    def spacing_deg(self) -> float:
        return round(self.native_spacing_deg * self.stride, 6)


@dataclass(frozen=True)
class CdsSpec:
    """Bulk ERA5-Land history from the Copernicus CDS (source id ``era5_land_cds``)."""

    dataset: str
    model: str
    start_date: date
    # How the hourly values are fetched: "chunks" (gridded, ~weekly bbox requests) or
    # "timeseries" (one request per node, snowfall from the gridded dataset); api.weather.cds.
    method: str = "chunks"
    # Snowfall area for the timeseries method, (north, west, south, east): one area for every
    # region so they share one snowfall cache. None = each region's own node bbox.
    snowfall_area: tuple[float, float, float, float] | None = None


CDS_METHODS = ("chunks", "timeseries")


@dataclass(frozen=True)
class HistorySpec:
    endpoint: str
    model: str
    start_date: date
    recent_days: int


@dataclass(frozen=True)
class ForecastSpec:
    endpoint: str
    model: str
    past_days: int
    forecast_days: int


@dataclass(frozen=True)
class Budget:
    per_minute: float
    per_hour: float
    per_day: float


@dataclass(frozen=True)
class Variable:
    name: str
    unit: str
    downscale: str
    lapse_rate_c_per_km: float | None = None


@dataclass(frozen=True)
class SeasonalVariable:
    """How one weather-store variable is read from the long-range forecast: its ensemble mean and
    its anomaly against the model's own climate, with the units each must come back in."""

    mean: str
    anomaly: str
    unit: str
    anomaly_unit: str


@dataclass(frozen=True)
class SeasonalSpec:
    endpoint: str
    source: str
    forecast_days: dict[str, int]  # granularity (weekly, monthly) -> horizon asked for
    variables: dict[str, SeasonalVariable]
    credits: list[str]
    point_stride: int = 1


@dataclass(frozen=True)
class WeatherConfig:
    points: PointsSpec
    history: HistorySpec
    forecast: ForecastSpec
    max_request_weight: float
    budget: Budget
    variables: dict[str, Variable]
    credits: list[str]
    seasonal: SeasonalSpec | None = None
    cds: CdsSpec | None = None

    @property
    def source_order(self) -> list[str]:
        """Source ids, most trusted first: CDS, then Open-Meteo archive, then forecast."""
        order = []
        if self.cds is not None:
            order.append(self.cds.model)
        order.append(self.history.model)
        order.append(self.forecast.model)
        return order

    @property
    def reanalysis_order(self) -> list[str]:
        """Reanalysis source ids, most trusted first: the source order without the forecast. A
        region's history is whichever of these it stores (CDS for every region after Tuscany)."""
        return [source for source in self.source_order if source != self.forecast.model]


def load_weather_config(path: Path = WEATHER_FILE) -> WeatherConfig:
    raw = yaml.safe_load(path.read_text())
    points = raw["points"]
    probe = points["land_probe"]
    variables = {
        name: Variable(
            name=name,
            unit=str(spec["unit"]),
            downscale=str(spec["downscale"]),
            lapse_rate_c_per_km=spec.get("lapse_rate_c_per_km"),
        )
        for name, spec in raw["variables"].items()
    }
    for variable in variables.values():
        if variable.downscale not in METHODS:
            raise ValueError(
                f"variable {variable.name!r} has unknown downscale method {variable.downscale!r}"
            )
    stride = int(points["stride"])
    if stride < 1:
        raise ValueError(f"points.stride must be at least 1, got {stride}")
    return WeatherConfig(
        points=PointsSpec(
            native_spacing_deg=float(points["native_spacing_deg"]),
            stride=stride,
            max_distance_km=float(points["max_distance_km"]),
            land_probe=LandProbe(
                model=str(probe["model"]),
                date=date.fromisoformat(str(probe["date"])),
                variables=list(probe["variables"]),
            ),
        ),
        history=HistorySpec(
            endpoint=raw["history"]["endpoint"],
            model=raw["history"]["model"],
            start_date=date.fromisoformat(str(raw["history"]["start_date"])),
            recent_days=int(raw["history"]["recent_days"]),
        ),
        forecast=ForecastSpec(**raw["forecast"]),
        max_request_weight=float(raw["requests"]["max_weight"]),
        budget=Budget(**raw["requests"]["budget"]),
        variables=variables,
        credits=list(raw.get("credits") or []),
        seasonal=_seasonal(raw.get("seasonal"), variables),
        cds=_cds(raw.get("cds")),
    )


def _cds(raw: dict | None) -> CdsSpec | None:
    if raw is None:
        return None
    method = str(raw.get("method", "chunks"))
    if method not in CDS_METHODS:
        raise ValueError(f"cds.method must be one of {CDS_METHODS}, got {method!r}")
    return CdsSpec(
        dataset=str(raw["dataset"]),
        model=str(raw["model"]),
        start_date=date.fromisoformat(str(raw["start_date"])),
        method=method,
        snowfall_area=(
            tuple(float(v) for v in raw["snowfall_area"]) if raw.get("snowfall_area") else None
        ),
    )


def _seasonal(raw: dict | None, variables: dict[str, Variable]) -> SeasonalSpec | None:
    if raw is None:
        return None
    mapped = {name: SeasonalVariable(**spec) for name, spec in raw["variables"].items()}
    unknown = sorted(set(mapped) - set(variables))
    if unknown:
        raise ValueError(f"seasonal maps variables the weather store does not have: {unknown}")
    granularities = {str(k): int(v) for k, v in raw["forecast_days"].items()}
    if not set(granularities) <= {"weekly", "monthly"}:
        raise ValueError(f"seasonal.forecast_days: unknown granularity in {sorted(granularities)}")
    return SeasonalSpec(
        endpoint=str(raw["endpoint"]),
        source=str(raw["source"]),
        forecast_days=granularities,
        variables=mapped,
        credits=list(raw.get("credits") or []),
        point_stride=max(1, int(raw.get("point_stride") or 1)),
    )
