from datetime import UTC, date, datetime

import geopandas as gpd
import pandas as pd
from pyproj import Transformer

from api.sightings.filters import deduplicate_inaturalist, drop_low_quality, flag_near_localities

FETCHED = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)


def _row(**overrides) -> dict:
    row = {
        "source": "gbif",
        "record_id": "1",
        "species": "porcini",
        "event_date": date(2026, 9, 1),
        "lat": 43.8,
        "lon": 11.2,
        "coordinate_uncertainty_m": 50.0,
        "license": "CC0",
        "obscured": False,
        "fetched_at": FETCHED,
    }
    row.update(overrides)
    return row


# --- dedup against GBIF --------------------------------------------------------------------


def test_deduplicate_drops_inaturalist_rows_already_seen_via_gbif() -> None:
    gbif = pd.DataFrame(
        [_row(record_id="1", inaturalist_observation_id="900"), _row(record_id="2")]
    )
    inaturalist = pd.DataFrame(
        [
            _row(source="inaturalist", record_id="900"),  # already in gbif
            _row(source="inaturalist", record_id="901"),  # not yet in gbif
        ]
    )

    kept = deduplicate_inaturalist(gbif, inaturalist)

    assert list(kept["record_id"]) == ["901"]


def test_deduplicate_keeps_everything_when_gbif_has_no_inaturalist_ids() -> None:
    gbif = pd.DataFrame([_row(record_id="1")])
    inaturalist = pd.DataFrame([_row(source="inaturalist", record_id="901")])

    kept = deduplicate_inaturalist(gbif, inaturalist)

    assert list(kept["record_id"]) == ["901"]


# --- quality filters -------------------------------------------------------------------------


def test_drop_low_quality_keeps_a_precise_recent_record() -> None:
    rows = pd.DataFrame([_row()])

    kept, counts = drop_low_quality(rows, max_uncertainty_m=1000)

    assert len(kept) == 1 and counts.kept == 1
    assert counts.input == 1
    assert counts.missing_date == counts.missing_coordinates == counts.too_imprecise == 0


def test_drop_low_quality_drops_a_missing_date() -> None:
    rows = pd.DataFrame([_row(event_date=None), _row(record_id="2")])

    kept, counts = drop_low_quality(rows, max_uncertainty_m=1000)

    assert list(kept["record_id"]) == ["2"]
    assert counts.missing_date == 1


def test_drop_low_quality_drops_missing_coordinates() -> None:
    rows = pd.DataFrame([_row(lat=None), _row(record_id="2", lon=None), _row(record_id="3")])

    kept, counts = drop_low_quality(rows, max_uncertainty_m=1000)

    assert list(kept["record_id"]) == ["3"]
    assert counts.missing_coordinates == 2


def test_drop_low_quality_drops_coordinates_coarser_than_the_cell() -> None:
    rows = pd.DataFrame(
        [_row(coordinate_uncertainty_m=1500), _row(record_id="2", coordinate_uncertainty_m=999)]
    )

    kept, counts = drop_low_quality(rows, max_uncertainty_m=1000)

    assert list(kept["record_id"]) == ["2"]
    assert counts.too_imprecise == 1


def test_drop_low_quality_never_trusts_a_cell_for_an_obscured_record() -> None:
    # Small reported uncertainty, but the source itself says the location is obscured.
    rows = pd.DataFrame([_row(coordinate_uncertainty_m=10, obscured=True)])

    kept, counts = drop_low_quality(rows, max_uncertainty_m=1000)

    assert kept.empty
    assert counts.too_imprecise == 1


def test_drop_low_quality_keeps_a_null_uncertainty_but_counts_it() -> None:
    # Missing precision metadata isn't the same as known-coarse; some precise GBIF records
    # legitimately lack coordinateUncertaintyInMeters (api.sightings.gbif docstring).
    rows = pd.DataFrame([_row(coordinate_uncertainty_m=None)])

    kept, counts = drop_low_quality(rows, max_uncertainty_m=1000)

    assert len(kept) == 1
    assert counts.unknown_uncertainty == 1


# --- town-centroid flag ------------------------------------------------------------------------


def _wgs84(x: float, y: float) -> tuple[float, float]:
    lon, lat = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True).transform(x, y)
    return lon, lat


def test_flag_near_localities_flags_points_pinned_to_a_village_square() -> None:
    x0, y0 = 4_300_000, 2_400_000
    locality = gpd.GeoDataFrame(
        {"place_name": ["Village"]}, geometry=gpd.points_from_xy([x0], [y0]), crs="EPSG:3035"
    )
    near_lon, near_lat = _wgs84(x0 + 20, y0 + 20)  # ~28 m away
    far_lon, far_lat = _wgs84(x0 + 5000, y0)  # 5 km away
    rows = pd.DataFrame(
        [
            _row(record_id="near", lon=near_lon, lat=near_lat),
            _row(record_id="far", lon=far_lon, lat=far_lat),
        ]
    )

    flags = flag_near_localities(rows, locality, distance_m=75)

    assert flags.loc[rows.index[rows["record_id"] == "near"]].iloc[0]
    assert not flags.loc[rows.index[rows["record_id"] == "far"]].iloc[0]


def test_flag_near_localities_handles_no_rows() -> None:
    locality = gpd.GeoDataFrame(
        {"place_name": ["Village"]}, geometry=gpd.points_from_xy([0], [0]), crs="EPSG:3035"
    )

    flags = flag_near_localities(pd.DataFrame(columns=["lon", "lat"]), locality, distance_m=75)

    assert flags.empty


def test_drop_low_quality_drops_excluded_kinds_of_record_and_counts_them() -> None:
    rows = pd.DataFrame(
        [
            _row(record_id="1", basis_of_record="HUMAN_OBSERVATION"),
            _row(record_id="2", basis_of_record="MATERIAL_SAMPLE"),
            _row(record_id="3", basis_of_record=None),
        ]
    )

    kept, counts = drop_low_quality(rows, 1000, exclude_basis_of_record=["MATERIAL_SAMPLE"])

    assert kept["record_id"].tolist() == ["1", "3"]
    assert counts.excluded_basis == 1
