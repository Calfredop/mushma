"""GBIF client: resolve a scientific name to a taxon key, and fetch occurrence records for a
region's bounding box.

``occurrence/search`` is scoped to a lon/lat bbox rather than the region's exact polygon; joining
the parsed rows to the woodland grid (``api.sightings.store``) drops anything outside Tuscany or
off the grid, so the bbox is deliberately a superset. ``hasCoordinate=true`` and
``hasGeospatialIssue=false`` keep out records GBIF already flagged as ungeoreferenced or
contradictory; the remaining quality checks (coordinate precision, missing dates) are
``api.sightings.filters``.
"""

import urllib.parse
from dataclasses import dataclass, replace
from datetime import date, datetime

import pandas as pd

# GBIF's iNaturalist Research-Grade Observations dataset: records from here also flow directly
# through the iNaturalist API, so they need deduplicating (api.sightings.filters.deduplicate).
INATURALIST_DATASET_KEY = "50c9509d-22c7-4a22-a47d-8c48425ef4a7"

OCCURRENCE_COLUMNS = [
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
    "species_key",
    "fetched_at",
]


@dataclass(frozen=True)
class TaxonMatch:
    query: str
    usage_key: int
    canonical_name: str
    match_type: str
    status: str
    accepted_usage_key: int | None = None

    @property
    def is_exact(self) -> bool:
        return self.match_type == "EXACT" and self.status in {"ACCEPTED", "SYNONYM"}

    @property
    def resolved_key(self) -> int:
        """The key to use for occurrence search: a synonym resolves to its accepted usage."""
        return self.accepted_usage_key or self.usage_key


def match_url(endpoint: str, name: str, rank: str = "SPECIES") -> str:
    params = {"name": name, "rank": rank, "strict": "true"}
    return f"{endpoint}?{urllib.parse.urlencode(params)}"


def parse_taxon_match(query: str, payload: dict) -> TaxonMatch:
    return TaxonMatch(
        query=query,
        usage_key=int(payload["usageKey"]),
        accepted_usage_key=(
            int(payload["acceptedUsageKey"]) if payload.get("acceptedUsageKey") else None
        ),
        canonical_name=str(payload.get("canonicalName", "")),
        match_type=str(payload.get("matchType", "NONE")),
        status=str(payload.get("status", "")),
    )


@dataclass(frozen=True)
class OccurrenceRequest:
    endpoint: str
    taxon_key: int
    bbox_wgs84: tuple[float, float, float, float]  # lon_min, lat_min, lon_max, lat_max
    page_size: int
    offset: int = 0

    def url(self) -> str:
        lon_min, lat_min, lon_max, lat_max = self.bbox_wgs84
        params = {
            "taxonKey": self.taxon_key,
            "decimalLongitude": f"{lon_min},{lon_max}",
            "decimalLatitude": f"{lat_min},{lat_max}",
            "hasCoordinate": "true",
            "hasGeospatialIssue": "false",
            "limit": self.page_size,
            "offset": self.offset,
        }
        return f"{self.endpoint}?{urllib.parse.urlencode(params)}"

    def at_offset(self, offset: int) -> "OccurrenceRequest":
        return replace(self, offset=offset)


def is_last_page(payload: dict) -> bool:
    return bool(payload.get("endOfRecords", True)) or not payload.get("results")


def _event_date(value: str | None) -> date | None:
    """A GBIF ``eventDate`` as a plain date, or ``None`` if it can't be read as one.

    Most records are a single ISO date or datetime. A few historical specimens give a date
    *range* instead (``"1701/1783"``, precision to the century); this takes the range's start and
    falls back to ``None`` when even that isn't a full calendar date (a bare year, say), letting
    the quality filters drop it as a missing date rather than crashing the ingest.
    """
    if not value:
        return None
    try:
        return date.fromisoformat(value.split("/", 1)[0][:10])
    except ValueError:
        return None


def _inaturalist_observation_id(record: dict) -> str | None:
    if record.get("datasetKey") != INATURALIST_DATASET_KEY:
        return None
    catalog_number = record.get("catalogNumber")
    if catalog_number:
        return str(catalog_number)
    occurrence_id = record.get("occurrenceID") or ""
    return occurrence_id.rstrip("/").rsplit("/", 1)[-1] or None


def parse_occurrences(pages: list[dict], taxon_key: int, fetched_at: datetime) -> pd.DataFrame:
    """Long rows, one per occurrence record across every page of one taxon's search."""
    rows = [
        {
            "source": "gbif",
            "record_id": str(record["key"]),
            "taxon_key": taxon_key,
            "event_date": _event_date(record.get("eventDate")),
            "lat": float(record["decimalLatitude"]),
            "lon": float(record["decimalLongitude"]),
            "coordinate_uncertainty_m": (
                float(record["coordinateUncertaintyInMeters"])
                if record.get("coordinateUncertaintyInMeters") is not None
                else None
            ),
            "basis_of_record": record.get("basisOfRecord"),
            "dataset_key": record.get("datasetKey"),
            "license": record.get("license"),
            "inaturalist_observation_id": _inaturalist_observation_id(record),
            # The record's own species (the searched key can be a genus); taxonKey when the
            # record is only identified to a higher rank.
            "species_key": int(record.get("speciesKey") or record["taxonKey"]),
            "fetched_at": fetched_at,
        }
        for page in pages
        for record in page.get("results", [])
    ]
    return pd.DataFrame(rows, columns=OCCURRENCE_COLUMNS)
