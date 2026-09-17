"""Quality filters over the common sighting schema (``api.sightings.ingest.normalize_*``).

PRD → Model (Known data traps) and Sightings privacy: a record is only as good as its coordinate
precision, and a record the source itself obscured must never be pretended into a single 1 km
cell.
"""

from dataclasses import dataclass

import geopandas as gpd
import numpy as np
import pandas as pd


def deduplicate_inaturalist(gbif: pd.DataFrame, inaturalist: pd.DataFrame) -> pd.DataFrame:
    """iNaturalist rows whose observation isn't already present via GBIF.

    Research-grade iNaturalist observations are republished through GBIF (with a delay); GBIF
    rows carry the iNaturalist observation id in ``inaturalist_observation_id`` when they came
    from that dataset (``api.sightings.gbif.INATURALIST_DATASET_KEY``).
    """
    seen = set(gbif.get("inaturalist_observation_id", pd.Series(dtype=object)).dropna())
    if not seen:
        return inaturalist
    return inaturalist[~inaturalist["record_id"].isin(seen)].reset_index(drop=True)


@dataclass(frozen=True)
class FilterCounts:
    input: int
    missing_date: int
    missing_coordinates: int
    too_imprecise: int
    unknown_uncertainty: int
    kept: int


def drop_low_quality(
    rows: pd.DataFrame, max_uncertainty_m: float
) -> tuple[pd.DataFrame, FilterCounts]:
    """Drop records with no date, no coordinates, or a precision too coarse to trust to one cell.

    A record the source itself flagged as obscured is dropped outright, whatever its reported
    ``coordinate_uncertainty_m`` says: geoprivacy obscuring is often expressed as a shifted point
    with a deceptively small stated radius (api.sightings.inaturalist docstring), and PRD →
    Sightings privacy forbids re-sharpening it. A *missing* uncertainty is not treated as coarse
    (some precise records legitimately omit it), but is counted so it shows up in the profile.
    """
    uncertainty = rows["coordinate_uncertainty_m"]
    missing_date = rows["event_date"].isna()
    missing_coordinates = rows["lat"].isna() | rows["lon"].isna()
    obscured = rows["obscured"].fillna(False).astype(bool)
    too_imprecise = (uncertainty.notna() & (uncertainty > max_uncertainty_m)) | obscured
    unknown_uncertainty = uncertainty.isna() & ~missing_coordinates

    drop = missing_date | missing_coordinates | too_imprecise
    kept = rows[~drop].reset_index(drop=True)
    counts = FilterCounts(
        input=len(rows),
        missing_date=int(missing_date.sum()),
        missing_coordinates=int(missing_coordinates.sum()),
        too_imprecise=int(too_imprecise.sum()),
        unknown_uncertainty=int(unknown_uncertainty.sum()),
        kept=len(kept),
    )
    return kept, counts


def flag_near_localities(
    rows: pd.DataFrame, localities: gpd.GeoDataFrame, distance_m: float
) -> pd.Series:
    """True where a record's coordinates sit within ``distance_m`` of an ISTAT inhabited-locality
    point (``api.grid.places.read_istat_localities``): the common pattern of pinning an
    observation to a village square rather than the actual find."""
    if rows.empty:
        return pd.Series([], dtype=bool, index=rows.index)
    points = gpd.GeoSeries(gpd.points_from_xy(rows["lon"], rows["lat"]), crs="EPSG:4326").to_crs(
        localities.crs
    )
    (query_idx, _), distance = localities.sindex.nearest(
        points, return_all=False, return_distance=True
    )
    order = np.argsort(query_idx)
    near = np.zeros(len(rows), dtype=bool)
    near[query_idx[order]] = distance[order] <= distance_m
    return pd.Series(near, index=rows.index)
