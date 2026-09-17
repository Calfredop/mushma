"""iNaturalist client: fetch the most recent observations for a taxon in a named place.

Used only for the days since the last GBIF fetch (``config/sightings.yaml`` ``recent_days``):
research-grade iNaturalist records are republished through GBIF with a days-to-weeks delay, so
this closes that gap. Rows are deduplicated against GBIF by observation id
(``api.sightings.filters.deduplicate``), matching ``gbif.INATURALIST_DATASET_KEY`` records'
``inaturalist_observation_id``.

The reported coordinate precision (``coordinate_uncertainty_m``) is always
``public_positional_accuracy``, not ``positional_accuracy``: iNaturalist can widen the public
coordinates of a record (geoprivacy, project rules, an auto-obscured taxon) well beyond what the
observer's own GPS reported, and the public value is what the returned ``location`` actually
means.
"""

import urllib.parse
from dataclasses import dataclass, replace
from datetime import date, datetime

import pandas as pd

OBSERVATION_COLUMNS = [
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


@dataclass(frozen=True)
class ObservationRequest:
    endpoint: str
    taxon_id: int
    place_id: int
    since: date
    quality_grades: list[str]
    page_size: int
    page: int = 1

    def url(self) -> str:
        params = {
            "taxon_id": self.taxon_id,
            "place_id": self.place_id,
            "d1": self.since.isoformat(),
            "quality_grade": ",".join(self.quality_grades),
            "geo": "true",
            "order_by": "observed_on",
            "order": "asc",
            "per_page": self.page_size,
            "page": self.page,
        }
        return f"{self.endpoint}?{urllib.parse.urlencode(params)}"

    def at_page(self, page: int) -> "ObservationRequest":
        return replace(self, page=page)


def is_last_page(payload: dict) -> bool:
    seen = payload.get("page", 1) * payload.get("per_page", 1)
    return seen >= payload.get("total_results", 0)


def parse_observations(pages: list[dict], taxon_id: int, fetched_at: datetime) -> pd.DataFrame:
    """Long rows, one per observation with coordinates, across every page of one taxon's search."""
    rows = []
    for page in pages:
        for record in page.get("results", []):
            location = record.get("location")
            if not location:
                continue
            lat, lon = (float(v) for v in location.split(","))
            rows.append(
                {
                    "source": "inaturalist",
                    "record_id": str(record["id"]),
                    "taxon_id": taxon_id,
                    "event_date": (
                        date.fromisoformat(record["observed_on"])
                        if record.get("observed_on")
                        else None
                    ),
                    "lat": lat,
                    "lon": lon,
                    "coordinate_uncertainty_m": (
                        float(record["public_positional_accuracy"])
                        if record.get("public_positional_accuracy") is not None
                        else None
                    ),
                    "license": record.get("license_code"),
                    "obscured": bool(record.get("obscured", False)),
                    "quality_grade": record.get("quality_grade"),
                    "fetched_at": fetched_at,
                }
            )
    return pd.DataFrame(rows, columns=OBSERVATION_COLUMNS)
