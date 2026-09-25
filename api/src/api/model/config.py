"""Model config (``config/model.yaml``): species groups and weather preparation.

National defaults live in ``model.yaml``. A region may override parts (today:
``precipitation_scale``) via a ``model:`` block in ``config/regions/<id>.yaml``.
"""

from pathlib import Path
from typing import Annotated, Any, Literal

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

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
    """Multiply daily rain from ``sources`` by ``intercept + per_km x elevation_km``."""

    enabled: bool
    sources: list[str]
    intercept: Annotated[float, Field(gt=0)]
    per_km: float
    max_elevation_m: Annotated[float, Field(gt=0)]
    confidence: str
    source: Annotated[list[str], Field(min_length=1)]
    notes: str

    def factor(self, elevation_m: np.ndarray) -> np.ndarray:
        """The multiplier for cells at ``elevation_m`` (unknown heights count as sea level)."""
        elevation = np.clip(np.nan_to_num(np.asarray(elevation_m, dtype=float)), 0, None)
        if not self.enabled:
            return np.ones_like(elevation)
        return self.intercept + self.per_km * np.minimum(elevation, self.max_elevation_m) / 1000


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
