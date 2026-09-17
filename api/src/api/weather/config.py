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
class WeatherConfig:
    points: PointsSpec
    history: HistorySpec
    forecast: ForecastSpec
    max_request_weight: float
    budget: Budget
    variables: dict[str, Variable]
    credits: list[str]

    @property
    def source_order(self) -> list[str]:
        """Source ids, most trusted first: reanalysis wins over forecast for the same day."""
        return [self.history.model, self.forecast.model]


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
    )
