"""Model config (``config/model.yaml``): species groups and weather preparation.

National defaults live in ``model.yaml``. A region may override parts via a ``model:`` block in
``config/regions/<id>.yaml`` (none does for ``precipitation_scale`` since the national field).
"""

from pathlib import Path
from typing import Annotated, Any, Literal

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from api.model.rain_field import load_rain_field

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
MODEL_FILE = CONFIG_DIR / "model.yaml"
REGIONS_DIR = CONFIG_DIR / "regions"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Copy ``base`` with ``override`` applied; nested dicts merge, other values replace."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class PrecipitationScale(_Strict):
    """Multiply daily rain from ``sources`` by a factor that grows with the cell's height.

    With ``field`` (a CSV under ``config/``, ``api.model.rain_field``) the factor's intercept,
    slope and height clamp are read at the cell's position; without it they are the constant
    ``intercept + per_km x elevation_km`` up to ``max_elevation_m``. The fit is against one
    source's rain; ``source_ratios`` names, per other source, a lattice of that source's rain level
    relative to it (column ``ratio``), which multiplies the factor for that source's rows.
    """

    enabled: bool
    sources: list[str]
    field: str | None = None
    intercept: Annotated[float, Field(gt=0)] | None = None
    per_km: float | None = None
    max_elevation_m: Annotated[float, Field(gt=0)] | None = None
    source_ratios: dict[str, str] = {}
    confidence: str
    source: Annotated[list[str], Field(min_length=1)]
    notes: str

    @model_validator(mode="after")
    def _one_shape(self) -> "PrecipitationScale":
        constant = (self.intercept, self.per_km, self.max_elevation_m)
        if self.field is None and any(value is None for value in constant):
            raise ValueError(
                "precipitation_scale needs a field or intercept, per_km and max_elevation_m"
            )
        if self.field is not None and any(value is not None for value in constant):
            raise ValueError("precipitation_scale takes a field or a constant fit, not both")
        for name in self.source_ratios:
            if name not in self.sources:
                raise ValueError(
                    f"precipitation_scale source_ratios: {name} is not a scaled source"
                )
        return self

    def factor(
        self,
        elevation_m: np.ndarray,
        lon: np.ndarray | None = None,
        lat: np.ndarray | None = None,
        source: str | None = None,
    ) -> np.ndarray:
        """The multiplier for cells at ``elevation_m`` (unknown heights count as sea level) and,
        for a field or a ``source`` with a ratio, at ``lon``/``lat``."""
        elevation = np.clip(np.nan_to_num(np.asarray(elevation_m, dtype=float)), 0, None)
        if not self.enabled:
            return np.ones_like(elevation)
        ratio = self.source_ratios.get(source) if source is not None else None
        if (self.field is not None or ratio is not None) and (lon is None or lat is None):
            raise ValueError("a precipitation_scale field needs each cell's lon and lat")
        if self.field is not None:
            factor = load_rain_field(CONFIG_DIR / self.field).factor(elevation, lon, lat)
        else:
            height = np.minimum(elevation, self.max_elevation_m)
            factor = self.intercept + self.per_km * height / 1000
        if ratio is not None:
            factor = factor * load_rain_field(CONFIG_DIR / ratio).value("ratio", lon, lat)
        return factor


class Microclimate(_Strict):
    """Shift each cell's weather by how much sun its slope gets (``api.model.terrain``).

    With ``sun`` the cell-day's sun ratio (1 = flat ground), each variable in
    ``temperature_per_sun`` gains ``k x (sun - 1)`` °C and ET0 is multiplied by
    ``1 + et0_per_sun x (sun - 1)``. Everything else, night-time minimum temperature included, is
    left as the weather model gave it.
    """

    enabled: bool
    diffuse_fraction: Annotated[
        list[Annotated[float, Field(ge=0, le=1)]], Field(min_length=12, max_length=12)
    ]
    temperature_per_sun: dict[str, float]
    et0_per_sun: Annotated[float, Field(ge=0)]
    confidence: str
    source: Annotated[list[str], Field(min_length=1)]
    notes: str

    @property
    def variables(self) -> list[str]:
        """The weather variables it adjusts."""
        return [*self.temperature_per_sun, "et0_fao_evapotranspiration"]

    def apply(self, values: dict[str, np.ndarray], sun: np.ndarray) -> dict[str, np.ndarray]:
        """``values`` with the adjusted variables replaced (new arrays; the input is left alone)."""
        if not self.enabled:
            return values
        excess = sun - 1.0
        adjusted = dict(values)
        for variable, per_sun in self.temperature_per_sun.items():
            if variable in adjusted:
                adjusted[variable] = adjusted[variable] + per_sun * excess
        et0 = "et0_fao_evapotranspiration"
        if et0 in adjusted:
            adjusted[et0] = np.maximum(adjusted[et0] * (1.0 + self.et0_per_sun * excess), 0.0)
        return adjusted


SeasonRole = Literal["train", "holdout", "live"]


class BacktestSplit(_Strict):
    """Which seasons (calendar years) tune the rules, which judge them, and which are still open."""

    train_seasons: list[int]
    holdout_seasons: list[int]
    live_seasons: list[int]
    frozen_factor_kinds: list[str]

    @model_validator(mode="after")
    def _disjoint(self) -> "BacktestSplit":
        roles = [*self.train_seasons, *self.holdout_seasons, *self.live_seasons]
        repeated = sorted({season for season in roles if roles.count(season) > 1})
        if repeated:
            raise ValueError(f"seasons in more than one role: {repeated}")
        return self

    def role_of(self, season: int) -> SeasonRole | None:
        for role, seasons in (
            ("train", self.train_seasons),
            ("holdout", self.holdout_seasons),
            ("live", self.live_seasons),
        ):
            if season in seasons:
                return role  # type: ignore[return-value]
        return None


class ModelConfig(_Strict):
    groups: dict[str, list[str]]
    precipitation_scale: PrecipitationScale
    microclimate: Microclimate
    backtest: BacktestSplit

    @property
    def cited(self) -> dict[str, list[str]]:
        """Reference ids cited by each model-level rule."""
        return {
            "precipitation_scale": self.precipitation_scale.source,
            "microclimate": self.microclimate.source,
        }


def load_model_config(
    path: Path = MODEL_FILE,
    *,
    region: str | None = None,
    regions_dir: Path = REGIONS_DIR,
) -> ModelConfig:
    """Load national model config, optionally merging a region's ``model:`` overrides.

    Missing region files (or no ``model:`` block) leave the national values unchanged.
    """
    raw = yaml.safe_load(path.read_text())
    if region is not None:
        region_path = regions_dir / f"{region}.yaml"
        if region_path.is_file():
            override = (yaml.safe_load(region_path.read_text()) or {}).get("model") or {}
            if override:
                raw = _deep_merge(raw, override)
    return ModelConfig.model_validate(raw)
