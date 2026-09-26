"""Which regions the API serves: config YAMLs filtered by stores on disk.

API ids are Italian slugs with underscores (``emilia_romagna``); Tuscany keeps ``tuscany``
(PRD → Architecture → Multi-region API). Fixture mode always serves Tuscany plus Umbria so the
web card can route between two without any Parquet on disk.
"""

from __future__ import annotations

from datetime import date
from functools import lru_cache
from pathlib import Path

from api.grid.region import REGIONS_DIR, RegionConfig, load_region
from api.grid.sources import data_dir
from api.model.rules import DEFAULT_REGION, list_rule_regions, load_rules
from api.species import SPECIES, Species
from api.weather.config import load_weather_config

FIXTURE_REGIONS: tuple[str, ...] = (DEFAULT_REGION, "umbria")


class RegionNotServed(Exception):
    """Raised when a ``region`` query names an unknown or unserved id."""

    def __init__(self, region: str) -> None:
        self.region = region
        super().__init__(f"unknown or unserved region {region!r}")


def list_configured_regions(regions_dir: Path = REGIONS_DIR) -> list[str]:
    return sorted(path.stem for path in regions_dir.glob("*.yaml"))


def region_store_ready(root: Path, region_id: str) -> bool:
    """A region is served when its grid and score meta are on disk (onboarding finished a score)."""
    grid = root / "grid" / region_id / "cells.parquet"
    scores_meta = root / "scores" / region_id / "meta.json"
    return grid.is_file() and scores_meta.is_file()


def list_served_region_ids(root: Path | None = None, *, fixtures: bool = False) -> list[str]:
    if fixtures:
        return list(FIXTURE_REGIONS)
    root = root or data_dir()
    # Rules too: a region's config can reach main before its species rules, and its stores the
    # server before either; serving it then would make /regions and /overview raise.
    with_rules = set(list_rule_regions())
    return [
        region_id
        for region_id in list_configured_regions()
        if region_id in with_rules and region_store_ready(root, region_id)
    ]


def require_served(region_id: str, *, root: Path | None = None, fixtures: bool = False) -> str:
    if region_id not in list_served_region_ids(root, fixtures=fixtures):
        raise RegionNotServed(region_id)
    return region_id


def history_start_date() -> date:
    """National weather history start (CDS / archive); every region backfills from here."""
    weather = load_weather_config()
    if weather.cds is not None:
        return weather.cds.start_date
    return weather.history.start_date


def species_for_region(region_id: str, *, fixtures: bool = False) -> list[Species]:
    if fixtures:
        return list(SPECIES)
    if region_id not in list_rule_regions():
        return []
    return [group for group in load_rules(region_id).groups if group in SPECIES]  # type: ignore[return-value]


@lru_cache
def cached_region_config(region_id: str) -> RegionConfig:
    return load_region(region_id)


def region_display_name(region_id: str, locale: str = "it") -> str:
    """Names come from ``config/regions/<id>.yaml``, never a hard-coded map."""
    names = cached_region_config(region_id).name
    return names.get(locale) or names.get("it") or region_id
