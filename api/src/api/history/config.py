"""Time-views config (``config/history.yaml``): good-day threshold, baseline years, normals and
the outlook's rain tilt. Cited like any rule: every ``source`` must resolve in
``species/references.yaml``."""

from pathlib import Path
from typing import Annotated

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from api.model.rules import REFERENCES_FILE, SPECIES_DIR, RuleSet

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
HISTORY_FILE = CONFIG_DIR / "history.yaml"


class HistoryConfigError(ValueError):
    pass


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Baseline(_Strict):
    start_year: int
    end_year: int

    @model_validator(mode="after")
    def _ordered(self) -> "Baseline":
        if self.end_year < self.start_year:
            raise ValueError(
                f"baseline ends ({self.end_year}) before it starts ({self.start_year})"
            )
        return self

    @property
    def years(self) -> list[int]:
        return list(range(self.start_year, self.end_year + 1))


class Normals(_Strict):
    window_days: Annotated[int, Field(ge=1)]
    variables: Annotated[list[str], Field(min_length=1)]

    @model_validator(mode="after")
    def _odd(self) -> "Normals":
        if self.window_days % 2 == 0:
            raise ValueError(f"normals.window_days must be odd, got {self.window_days}")
        return self


class RainTilt(_Strict):
    wetter_pct: Annotated[float, Field(gt=100)]
    drier_pct: Annotated[float, Field(gt=0, lt=100)]
    confidence: str
    source: Annotated[list[str], Field(min_length=1)]
    notes: str


class Outlook(_Strict):
    good_share: Annotated[float, Field(gt=0, le=1)]
    months_ahead: Annotated[int, Field(ge=0)]
    rain: RainTilt


class HistoryConfig(_Strict):
    good_score: Annotated[float, Field(gt=0, le=1)]
    baseline: Baseline
    normals: Normals
    outlook: Outlook


def load_history_config(path: Path = HISTORY_FILE) -> HistoryConfig:
    try:
        config = HistoryConfig.model_validate(yaml.safe_load(path.read_text()))
    except (OSError, yaml.YAMLError, ValidationError) as error:
        raise HistoryConfigError(f"{path.name}: {error}") from error
    references = yaml.safe_load((SPECIES_DIR / REFERENCES_FILE).read_text())["references"]
    unknown = [s for s in config.outlook.rain.source if s not in references]
    if unknown:
        raise HistoryConfigError(f"{path.name}: outlook.rain cites unknown sources {unknown}")
    return config


def rain_lead_days(rules: RuleSet, keys: list[str]) -> tuple[int, int]:
    """How many days rain leads fruiting for a group: the union of the full-response plateaus of
    its keys' enabled ``rain_event`` lags (``lag_days`` ``[zero_below, full_from, full_to,
    zero_above]``)."""
    lows, highs = [], []
    for key in keys:
        for factor in rules.species[key].enabled_factors:
            if factor.kind == "rain_event":
                _, full_from, full_to, _ = factor.response.lag_days
                lows.append(int(full_from))
                highs.append(int(full_to))
    if not lows:
        raise HistoryConfigError(f"no enabled rain_event rule among {keys}")
    return min(lows), max(highs)
