from datetime import UTC, date, datetime
from urllib.parse import parse_qs, urlparse

import pytest

from api.sightings.inaturalist import (
    ObservationRequest,
    is_last_page,
    parse_observations,
)

FETCHED = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)


def _observation(**overrides) -> dict:
    observation = {
        "id": 4251438,
        "observed_on": "2016-10-01",
        "location": "43.8039337412,11.7917633057",
        "positional_accuracy": 61,
        "public_positional_accuracy": 61,
        "obscured": False,
        "geoprivacy": None,
        "license_code": "cc-by-sa",
        "quality_grade": "research",
    }
    observation.update(overrides)
    return observation


# --- requests --------------------------------------------------------------------------------


def test_observation_request_scopes_to_the_taxon_place_and_window() -> None:
    request = ObservationRequest(
        endpoint="https://api.inaturalist.org/v1/observations",
        taxon_id=48701,
        place_id=13073,
        since=date(2026, 9, 1),
        quality_grades=["research", "needs_id"],
        page_size=200,
        page=1,
    )

    query = parse_qs(urlparse(request.url()).query)

    assert query["taxon_id"] == ["48701"]
    assert query["place_id"] == ["13073"]
    assert query["d1"] == ["2026-09-01"]
    assert query["quality_grade"] == ["research,needs_id"]
    assert query["geo"] == ["true"]
    assert query["per_page"] == ["200"]
    assert query["page"] == ["1"]


def test_is_last_page_follows_page_arithmetic() -> None:
    assert is_last_page({"total_results": 5, "page": 1, "per_page": 5})
    assert not is_last_page({"total_results": 6, "page": 1, "per_page": 5})
    assert is_last_page({"total_results": 0, "page": 1, "per_page": 5})


# --- parsing -----------------------------------------------------------------------------------


def test_parse_observations_extracts_the_fields_the_store_needs() -> None:
    pages = [{"results": [_observation()]}]

    rows = parse_observations(pages, taxon_id=48701, fetched_at=FETCHED)

    assert list(rows.columns) == [
        "source",
        "record_id",
        "taxon_id",
        "event_date",
        "lat",
        "lon",
        "coordinate_uncertainty_m",
        "license",
        "obscured",
        "quality_grade",
        "fetched_at",
    ]
    row = rows.iloc[0]
    assert row["source"] == "inaturalist"
    assert row["record_id"] == "4251438"
    assert row["event_date"] == date(2016, 10, 1)
    assert row["lat"] == pytest.approx(43.8039337412)
    assert row["lon"] == pytest.approx(11.7917633057)
    assert row["coordinate_uncertainty_m"] == 61
    assert not row["obscured"]


def test_parse_observations_uses_the_public_positional_accuracy_not_the_private_one() -> None:
    # A record can carry a tight private accuracy but a far coarser public one.
    pages = [{"results": [_observation(positional_accuracy=132, public_positional_accuracy=27380)]}]

    rows = parse_observations(pages, taxon_id=48701, fetched_at=FETCHED)

    assert rows.iloc[0]["coordinate_uncertainty_m"] == 27380


def test_parse_observations_flags_obscured_geoprivacy() -> None:
    pages = [{"results": [_observation(obscured=True, geoprivacy="obscured")]}]

    rows = parse_observations(pages, taxon_id=48701, fetched_at=FETCHED)

    assert rows.iloc[0]["obscured"]


def test_parse_observations_drops_records_without_a_location() -> None:
    pages = [{"results": [_observation(location=None), _observation(id=2)]}]

    rows = parse_observations(pages, taxon_id=48701, fetched_at=FETCHED)

    assert len(rows) == 1
    assert rows.iloc[0]["record_id"] == "2"


def test_parse_observations_tolerates_a_missing_observed_on() -> None:
    pages = [{"results": [_observation(observed_on=None)]}]

    rows = parse_observations(pages, taxon_id=48701, fetched_at=FETCHED)

    assert rows.iloc[0]["event_date"] is None
