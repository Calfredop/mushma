"""Lazy per-region LiveRepository registry and the national ``/regions`` / ``/overview`` helpers."""

from __future__ import annotations

import os
from datetime import date
from functools import lru_cache
from pathlib import Path

from api.fixtures.repository import (
    FixtureRepository,
    fixture_overview,
    fixture_regions_response,
)
from api.grid.sources import data_dir
from api.history.config import load_history_config
from api.live.repository import LiveRepository
from api.models import OverviewResponse, RegionInfo, RegionOverview, RegionsResponse
from api.regions import (
    cached_region_config,
    history_start_date,
    list_served_region_ids,
    require_served,
    species_for_region,
)
from api.repository import ScoresRepository
from api.species import SpeciesOrCombined


def _fixtures_mode() -> bool:
    return os.environ.get("MUSHMA_FIXTURES") == "1"


@lru_cache
def _live_repository(region: str, root: str) -> LiveRepository:
    return LiveRepository(Path(root), region=region)


def repository_for(region: str, *, root: Path | None = None) -> ScoresRepository:
    fixtures = _fixtures_mode()
    require_served(region, root=root, fixtures=fixtures)
    if fixtures:
        return FixtureRepository(region)
    return _live_repository(region, str(root or data_dir()))


def clear_repository_cache() -> None:
    _live_repository.cache_clear()


def get_regions_response(*, root: Path | None = None) -> RegionsResponse:
    if _fixtures_mode():
        return fixture_regions_response()
    root = root or data_dir()
    start = history_start_date()
    regions = []
    for region_id in list_served_region_ids(root):
        config = cached_region_config(region_id)
        repo = _live_repository(region_id, str(root))
        regions.append(
            RegionInfo(
                id=region_id,
                name=dict(config.name),
                bbox_wgs84=list(config.bbox_wgs84),
                history_start=start,
                species=species_for_region(region_id),
                updated_at=repo.region_updated_at(),
            )
        )
    return RegionsResponse(regions=regions)


def get_overview_response(
    species: SpeciesOrCombined, target_date: date, *, root: Path | None = None
) -> OverviewResponse:
    if _fixtures_mode():
        return fixture_overview(species, target_date)
    root = root or data_dir()
    good_score = load_history_config().good_score
    rows = []
    for region_id in list_served_region_ids(root):
        repo = _live_repository(region_id, str(root))
        mean, good_share, updated_at = repo.overview_row(species, target_date, good_score)
        rows.append(
            RegionOverview(
                region=region_id,
                mean_score=round(mean, 3),
                good_share=round(good_share, 3),
                updated_at=updated_at,
            )
        )
    return OverviewResponse(species=species, date=target_date, good_score=good_score, regions=rows)
