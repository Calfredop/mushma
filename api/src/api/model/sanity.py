"""Sanity check: do the stored scores agree with seasons foragers and local news remembered?

    uv run python -m api.model.sanity --label v1

Each contrast pairs two windows of the porcini group score (an area, one or more seasons, a date
range) and states which one local sources say was better. A window's value is its mean score over
its woodland cell-days; a list of several seasons is that area's normal for the window. Contrasts
and areas live in ``config/species/<region>/sanity.yaml``, written down from the sources cited
before any area score was looked at. A contrast holding is a sanity check, not validation: the
sources are news and forager blogs, often about a single valley, and several describe a record
season in Coldiretti's recycled wording.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Annotated

import duckdb
import pandas as pd
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from api.grid.sources import data_dir
from api.model.rules import DEFAULT_REGION, SPECIES_DIR, region_rules_dir
from api.model.store import ScoreStore


def fix_mojibake(name: str) -> str:
    """Undo UTF-8 text read as Latin-1 (``Castel San NiccolÃ²``), which the grid's ISTAT names
    carry until the grid reader is fixed; clean names pass through."""
    if "Ã" not in name and "Â" not in name:
        return name
    try:
        return name.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


@dataclass(frozen=True)
class Area:
    comuni: list[str] = field(default_factory=list)
    provinces: list[str] = field(default_factory=list)  # "*" for the whole region
    excluding: list[str] = field(default_factory=list)  # comuni left out of the provinces


def area_cells(cells: pd.DataFrame, area: Area) -> set[str]:
    woodland = cells[cells["woodland"]]
    names = woodland["comune_name"].fillna("").map(fix_mojibake)
    chosen = names.isin(area.comuni)
    if area.provinces:
        in_provinces = (
            pd.Series(True, index=woodland.index)
            if "*" in area.provinces
            else woodland["province"].isin(area.provinces)
        )
        chosen |= in_provinces & ~names.isin(area.excluding)
    return set(woodland.loc[chosen, "cell_id"])


@dataclass(frozen=True)
class Window:
    area: str
    seasons: list[int]
    start: str  # MM-DD
    end: str  # MM-DD, same year

    def bounds(self, season: int) -> tuple[date, date]:
        return date.fromisoformat(f"{season}-{self.start}"), date.fromisoformat(
            f"{season}-{self.end}"
        )


@dataclass(frozen=True)
class Contrast:
    id: str
    claim: str
    source: str
    higher: Window
    lower: Window


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class _AreaDoc(_Strict):
    comuni: list[str] = []
    provinces: list[str] = []
    excluding: list[str] = []

    @model_validator(mode="after")
    def _named(self) -> _AreaDoc:
        if not self.comuni and not self.provinces:
            raise ValueError("an area needs comuni or provinces")
        return self


class _WindowDoc(_Strict):
    area: str
    seasons: list[int] | Annotated[str, Field(pattern=r"^normal$")]
    start: Annotated[str, Field(pattern=r"^\d{2}-\d{2}$")]
    end: Annotated[str, Field(pattern=r"^\d{2}-\d{2}$")]


class _ContrastDoc(_Strict):
    id: str
    claim: Annotated[str, Field(min_length=1)]
    source: Annotated[str, Field(min_length=1)]
    higher: _WindowDoc
    lower: _WindowDoc


class _SanityDoc(_Strict):
    areas: dict[str, _AreaDoc]
    normal_seasons: list[int]
    contrasts: Annotated[list[_ContrastDoc], Field(min_length=1)]


class SanityConfigError(ValueError):
    pass


@dataclass(frozen=True)
class SanityCheck:
    areas: dict[str, Area]
    contrasts: list[Contrast]
    normal_seasons: list[int]


def _window(doc: _WindowDoc, normal: list[int]) -> Window:
    seasons = normal if doc.seasons == "normal" else list(doc.seasons)
    if not seasons:
        raise SanityConfigError("a window needs at least one season")
    return Window(area=doc.area, seasons=seasons, start=doc.start, end=doc.end)


def load_sanity(
    region: str = DEFAULT_REGION,
    *,
    species_dir: Path = SPECIES_DIR,
) -> SanityCheck:
    """Load ``species/<region>/sanity.yaml``; raise SanityConfigError on the first fault."""
    path = region_rules_dir(region, species_dir) / "sanity.yaml"
    try:
        raw = yaml.safe_load(path.read_text())
        doc = _SanityDoc.model_validate(raw)
    except (OSError, yaml.YAMLError, ValidationError) as error:
        raise SanityConfigError(f"{path.name}: {error}") from error

    areas = {
        name: Area(comuni=a.comuni, provinces=a.provinces, excluding=a.excluding)
        for name, a in doc.areas.items()
    }
    contrasts: list[Contrast] = []
    for item in doc.contrasts:
        higher = _window(item.higher, doc.normal_seasons)
        lower = _window(item.lower, doc.normal_seasons)
        for window in (higher, lower):
            if window.area not in areas:
                raise SanityConfigError(f"{item.id}: unknown area {window.area!r}")
        if not item.source.startswith("http"):
            raise SanityConfigError(f"{item.id}: source must be a URL")
        contrasts.append(
            Contrast(
                id=item.id,
                claim=item.claim,
                source=item.source,
                higher=higher,
                lower=lower,
            )
        )
    return SanityCheck(areas=areas, contrasts=contrasts, normal_seasons=list(doc.normal_seasons))


def _window_mean(scores: pd.DataFrame, cells: set[str], window: Window) -> tuple[float, int]:
    days = pd.to_datetime(scores["date"]).dt.date
    in_window = pd.Series(False, index=scores.index)
    for season in window.seasons:
        start, end = window.bounds(season)
        in_window |= (days >= start) & (days <= end)
    rows = scores.loc[in_window & scores["cell_id"].isin(cells), "score"]
    return (float(rows.mean()) if len(rows) else float("nan")), int(len(rows))


def evaluate_contrasts(
    contrasts: list[Contrast],
    scores: pd.DataFrame,
    cells: pd.DataFrame,
    areas: dict[str, Area],
) -> pd.DataFrame:
    """One row per contrast: both windows' mean scores and whether the higher one is higher."""
    resolved = {name: area_cells(cells, area) for name, area in areas.items()}
    rows = []
    for contrast in contrasts:
        high, high_n = _window_mean(scores, resolved[contrast.higher.area], contrast.higher)
        low, low_n = _window_mean(scores, resolved[contrast.lower.area], contrast.lower)
        rows.append(
            {
                "id": contrast.id,
                "claim": contrast.claim,
                "higher_mean": high,
                "lower_mean": low,
                "higher_cell_days": high_n,
                "lower_cell_days": low_n,
                "holds": bool(high > low),
                "source": contrast.source,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--label", required=True)
    parser.add_argument("--region", default=DEFAULT_REGION)
    parser.add_argument("--group", default="porcini")
    args = parser.parse_args()
    started = time.monotonic()
    sanity = load_sanity(args.region)
    root = data_dir()
    cells = pd.read_parquet(
        root / "grid" / args.region / "cells.parquet",
        columns=["cell_id", "comune_name", "province", "woodland"],
    )
    seasons = sorted({s for c in sanity.contrasts for w in (c.higher, c.lower) for s in w.seasons})
    store = ScoreStore(root / "scores" / args.region)
    scores = store.read(
        duckdb.connect(), args.group, date(min(seasons), 1, 1), date(max(seasons), 12, 31)
    ).df()
    result = evaluate_contrasts(sanity.contrasts, scores, cells, sanity.areas)
    out = root / "backtest" / args.region / args.label
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / f"sanity_{args.group}.csv", index=False)
    print(result[["id", "higher_mean", "lower_mean", "holds"]].to_string(index=False))
    print(f"[{time.monotonic() - started:.1f}s] {int(result['holds'].sum())}/{len(result)} hold")


if __name__ == "__main__":
    main()
