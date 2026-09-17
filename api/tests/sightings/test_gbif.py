from datetime import UTC, datetime
from urllib.parse import parse_qs, urlparse

import pytest

from api.sightings.gbif import (
    OccurrenceRequest,
    is_last_page,
    match_url,
    parse_occurrences,
    parse_taxon_match,
)

BBOX = (9.68, 42.23, 12.38, 44.48)
FETCHED = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)


def _record(**overrides) -> dict:
    record = {
        "key": 6519759357,
        "taxonKey": 5954958,
        "datasetKey": "50c9509d-22c7-4a22-a47d-8c48425ef4a7",
        "basisOfRecord": "HUMAN_OBSERVATION",
        "eventDate": "2026-09-01T16:28:52",
        "decimalLatitude": 44.1219,
        "decimalLongitude": 10.606355,
        "coordinateUncertaintyInMeters": 4.0,
        "license": "http://creativecommons.org/publicdomain/zero/1.0/legalcode",
        "occurrenceID": "https://www.inaturalist.org/observations/396598350",
        "catalogNumber": "396598350",
    }
    record.update(overrides)
    return record


# --- taxon match -------------------------------------------------------------------------------


def test_match_url_asks_for_an_exact_species_match() -> None:
    url = match_url("https://api.gbif.org/v1/species/match", "Boletus edulis")

    query = parse_qs(urlparse(url).query)
    assert query["name"] == ["Boletus edulis"]
    assert query["rank"] == ["SPECIES"]


def test_parse_taxon_match_accepts_an_exact_accepted_match() -> None:
    payload = {
        "usageKey": 5954958,
        "canonicalName": "Boletus edulis",
        "matchType": "EXACT",
        "status": "ACCEPTED",
    }

    match = parse_taxon_match("Boletus edulis", payload)

    assert match.usage_key == 5954958
    assert match.is_exact


def test_parse_taxon_match_accepts_an_exact_synonym() -> None:
    # Boletus aestivalis resolves to the accepted usage key for B. reticulatus.
    payload = {
        "usageKey": 5954988,
        "acceptedUsageKey": 5954691,
        "canonicalName": "Boletus aestivalis",
        "matchType": "EXACT",
        "status": "SYNONYM",
    }

    match = parse_taxon_match("Boletus aestivalis", payload)

    assert match.is_exact
    assert match.accepted_usage_key == 5954691


def test_parse_taxon_match_rejects_a_fuzzy_or_higher_rank_match() -> None:
    payload = {
        "usageKey": 2568748,
        "canonicalName": "Xylaria",
        "matchType": "HIGHERRANK",
        "status": "ACCEPTED",
    }

    match = parse_taxon_match("Xylaria nonexistentia", payload)

    assert not match.is_exact


# --- occurrence requests -----------------------------------------------------------------------


def test_occurrence_request_scopes_to_the_bbox_and_excludes_bad_coordinates() -> None:
    request = OccurrenceRequest(
        endpoint="https://api.gbif.org/v1/occurrence/search",
        taxon_key=5954958,
        bbox_wgs84=BBOX,
        page_size=300,
        offset=0,
    )

    query = parse_qs(urlparse(request.url()).query)

    assert query["taxonKey"] == ["5954958"]
    assert query["decimalLongitude"] == ["9.68,12.38"]
    assert query["decimalLatitude"] == ["42.23,44.48"]
    assert query["hasCoordinate"] == ["true"]
    assert query["hasGeospatialIssue"] == ["false"]
    assert query["limit"] == ["300"]
    assert query["offset"] == ["0"]


def test_is_last_page_follows_gbifs_end_of_records_flag() -> None:
    assert is_last_page({"endOfRecords": True, "results": []})
    assert not is_last_page({"endOfRecords": False, "results": [1]})
    assert is_last_page({"results": []})  # no more results is also the end


# --- parsing -------------------------------------------------------------------------------------


def test_parse_occurrences_extracts_the_fields_the_store_needs() -> None:
    pages = [{"results": [_record()]}]

    rows = parse_occurrences(pages, taxon_key=5954958, fetched_at=FETCHED)

    assert list(rows.columns) == [
        "source",
        "record_id",
        "taxon_key",
        "event_date",
        "lat",
        "lon",
        "coordinate_uncertainty_m",
        "basis_of_record",
        "dataset_key",
        "license",
        "inaturalist_observation_id",
        "fetched_at",
    ]
    row = rows.iloc[0]
    assert row["source"] == "gbif"
    assert row["record_id"] == "6519759357"
    assert row["event_date"].isoformat() == "2026-09-01"
    assert row["lat"] == pytest.approx(44.1219)
    assert row["lon"] == pytest.approx(10.606355)
    assert row["inaturalist_observation_id"] == "396598350"
    assert row["fetched_at"] == FETCHED


def test_parse_occurrences_leaves_the_inaturalist_id_null_for_other_datasets() -> None:
    pages = [
        {
            "results": [
                _record(
                    datasetKey="2bc4c2db-1dfa-419c-93ce-6602c5ae8c99",
                    occurrenceID=None,
                    catalogNumber="123",
                )
            ]
        }
    ]

    rows = parse_occurrences(pages, taxon_key=5954958, fetched_at=FETCHED)

    assert rows.iloc[0]["inaturalist_observation_id"] is None


def test_parse_occurrences_tolerates_a_missing_event_date_or_uncertainty() -> None:
    pages = [{"results": [_record(eventDate=None, coordinateUncertaintyInMeters=None)]}]

    rows = parse_occurrences(pages, taxon_key=5954958, fetched_at=FETCHED)

    row = rows.iloc[0]
    assert row["event_date"] is None
    assert row["coordinate_uncertainty_m"] is None


def test_parse_occurrences_tolerates_a_century_range_event_date() -> None:
    # Some old specimen records give a date range instead of a single date.
    pages = [{"results": [_record(eventDate="1701/1783")]}]

    rows = parse_occurrences(pages, taxon_key=5954958, fetched_at=FETCHED)

    assert rows.iloc[0]["event_date"] is None


def test_parse_occurrences_takes_the_start_of_a_day_range_event_date() -> None:
    pages = [{"results": [_record(eventDate="2020-06-01/2020-06-03")]}]

    rows = parse_occurrences(pages, taxon_key=5954958, fetched_at=FETCHED)

    assert rows.iloc[0]["event_date"].isoformat() == "2020-06-01"


def test_parse_occurrences_concatenates_every_page() -> None:
    pages = [
        {"results": [_record(key=1), _record(key=2)]},
        {"results": [_record(key=3)]},
    ]

    rows = parse_occurrences(pages, taxon_key=5954958, fetched_at=FETCHED)

    assert list(rows["record_id"]) == ["1", "2", "3"]
