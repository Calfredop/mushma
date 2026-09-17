"""Model config (``config/model.yaml``): species groups and weather preparation."""

from pathlib import Path
from typing import Annotated

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict, Field

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
MODEL_FILE = CONFIG_DIR / "model.yaml"


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


class ModelConfig(_Strict):
    groups: dict[str, list[str]]
    precipitation_scale: PrecipitationScale

    @property
    def cited(self) -> dict[str, list[str]]:
        """Reference ids cited by each model-level rule."""
        return {"precipitation_scale": self.precipitation_scale.source}


def load_model_config(path: Path = MODEL_FILE) -> ModelConfig:
    return ModelConfig.model_validate(yaml.safe_load(path.read_text()))
