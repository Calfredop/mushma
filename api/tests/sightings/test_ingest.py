from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd
import pytest

from api.sightings.config import load_sightings_config
from api.sightings.ingest import (
    fetch_gbif,
    fetch_inaturalist,
    normalize_gbif,
    normalize_inaturalist,
    profile_stats,
    resolve_taxa,
    stale_gbif_record_ids,
    write_meta,
)
from api.sightings.store import SightingsStore

FETCHED = datetime(2026, 9, 17, 5, 0, tzinfo=UTC)
CONFIG = load_sightings_config()


class FakeClient:
    def __init__(self, responses: dict[str, dict]) -> None:
        self.responses = responses
        self.urls: list[str] = []

    def get(self, url: str) -> dict:
        self.urls.append(url)
        for key, payload in self.responses.items():
            if key in url:
                return payload
        raise AssertionError(f"no fake response for {url}")


# --- normalize -----------------------------------------------------------------------------


def test_normalize_gbif_maps_taxon_key_to_species() -> None:
    rows = pd.DataFrame(
        [
            {
                "source": "gbif",
                "record_id": "1",
                "taxon_key": 5240269,  # Amanita caesarea -> ovoli
                "event_date": date(2026, 9, 1),
                "lat": 43.8,
                "lon": 11.2,
                "coordinate_uncertainty_m": 20.0,
                "basis_of_record": "HUMAN_OBSERVATION",
                "dataset_key": "50c9509d-22c7-4a22-a47d-8c48425ef4a7",
                "license": "CC0",
                "inaturalist_observation_id": "900",
                "species_key": 5240269,
                "fetched_at": FETCHED,
            }
        ]
    )

    normalized = normalize_gbif(rows, CONFIG)

    assert normalized.iloc[0]["species"] == "ovoli"
    assert not normalized.iloc[0]["obscured"]
    assert normalized.iloc[0]["inaturalist_observation_id"] == "900"


def test_normalize_inaturalist_maps_taxon_id_to_species() -> None:
    rows = pd.DataFrame(
        [
            {
                "source": "inaturalist",
                "record_id": "42",
                "taxon_id": 47348,  # Cantharellus (genus) -> gallinacci
                "event_date": date(2026, 9, 1),
                "lat": 43.8,
                "lon": 11.2,
                "coordinate_uncertainty_m": 20.0,
                "license": "cc-by-nc",
                "obscured": False,
                "quality_grade": "research",
                "fetched_at": FETCHED,
            }
        ]
    )

    normalized = normalize_inaturalist(rows, CONFIG)

    assert normalized.iloc[0]["species"] == "gallinacci"


def _gbif_row(record_id: str, taxon_key: int, species_key: int) -> dict:
    return {
        "source": "gbif",
        "record_id": record_id,
        "taxon_key": taxon_key,
        "event_date": date(2026, 9, 1),
        "lat": 43.8,
        "lon": 11.2,
        "coordinate_uncertainty_m": 20.0,
        "basis_of_record": "HUMAN_OBSERVATION",
        "dataset_key": "x",
        "license": "CC0",
        "inaturalist_observation_id": None,
        "species_key": species_key,
        "fetched_at": FETCHED,
    }


def test_normalize_gbif_drops_species_excluded_from_a_genus_taxon() -> None:
    rows = pd.DataFrame(
        [
            _gbif_row("1", 9623860, 5249504),  # Cantharellus cibarius: kept
            _gbif_row("2", 9623860, 9226626),  # Cantharellus cinereus: excluded
            _gbif_row("3", 9623860, 9623860),  # identified to genus only: kept
        ]
    )

    normalized = normalize_gbif(rows, CONFIG)

    assert normalized["record_id"].tolist() == ["1", "3"]
    assert set(normalized["species"]) == {"gallinacci"}
    assert "basis_of_record" in normalized


def test_stale_gbif_records_are_the_fetched_ones_no_longer_kept() -> None:
    fetched = pd.DataFrame({"record_id": ["1", "2", "3"]})
    stored = pd.DataFrame({"record_id": ["1"]})

    assert stale_gbif_record_ids(fetched, stored) == ["2", "3"]


# --- resolve-taxa ----------------------------------------------------------------------------


def test_resolve_taxa_confirms_every_pinned_key(capsys: pytest.CaptureFixture) -> None:
    client = FakeClient(
        {
            "Boletus+edulis": {
                "usageKey": 5954958,
                "canonicalName": "Boletus edulis",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            },
            "Boletus+aereus": {
                "usageKey": 8733688,
                "canonicalName": "Boletus aereus",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            },
            "Boletus+reticulatus": {
                "usageKey": 5954691,
                "canonicalName": "Boletus reticulatus",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            },
            "Boletus+pinophilus": {
                "usageKey": 5954949,
                "canonicalName": "Boletus pinophilus",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            },
            "Amanita+caesarea": {
                "usageKey": 5240269,
                "canonicalName": "Amanita caesarea",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            },
            "name=Cantharellus&rank=GENUS": {
                "usageKey": 9623860,
                "canonicalName": "Cantharellus",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            },
        }
    )
    messages = []

    matches = resolve_taxa(client, CONFIG, log=messages.append)

    assert len(matches) == 6
    assert all(m.is_exact for m in matches.values())
    assert not any("WARNING" in message for message in messages)


def test_resolve_taxa_warns_when_a_key_would_change() -> None:
    client = FakeClient(
        {
            "Boletus+edulis": {
                "usageKey": 999,
                "canonicalName": "Boletus edulis",
                "matchType": "EXACT",
                "status": "ACCEPTED",
            }
        }
    )
    # Only test the one taxon in isolation by using a tiny config.
    from api.sightings.config import (
        SightingsConfig,
        Species,
        Taxon,
    )

    tiny = SightingsConfig(
        species={
            "porcini": Species(
                common_name={"en": "Porcini"}, taxa=[Taxon("Boletus edulis", 5954958, 48701)]
            )
        },
        gbif=CONFIG.gbif,
        inaturalist=CONFIG.inaturalist,
        quality=CONFIG.quality,
        credits=CONFIG.credits,
    )
    messages = []

    resolve_taxa(client, tiny, log=messages.append)

    assert any("WARNING" in message and "999" in message for message in messages)


# --- fetch orchestration -----------------------------------------------------------------------


def test_fetch_gbif_pages_every_taxon_and_caches_under_its_own_key(tmp_path: Path) -> None:
    client = FakeClient(
        {
            f"taxonKey={taxon.gbif_taxon_key}": {
                "results": [
                    {
                        "key": taxon.gbif_taxon_key * 10,
                        "taxonKey": taxon.gbif_taxon_key,
                        "datasetKey": "x",
                        "basisOfRecord": "HUMAN_OBSERVATION",
                        "eventDate": "2026-09-01",
                        "decimalLatitude": 43.8,
                        "decimalLongitude": 11.2,
                        "coordinateUncertaintyInMeters": 10.0,
                        "license": "CC0",
                    }
                ],
                "endOfRecords": True,
            }
            for species in CONFIG.species.values()
            for taxon in species.taxa
        }
    )

    rows = fetch_gbif(
        client,
        CONFIG,
        bbox=(9.68, 42.23, 12.38, 44.48),
        cache_root=tmp_path,
        fetched_at=FETCHED,
        cache_scope="tuscany",
    )

    total_taxa = sum(len(s.taxa) for s in CONFIG.species.values())
    assert len(rows) == total_taxa
    assert (tmp_path / "gbif" / "tuscany" / "5954958" / ".complete").exists()


def test_fetch_gbif_never_reuses_another_regions_pages(tmp_path: Path) -> None:
    """The cache is per region: a second region's bbox is fetched, not read from the first's."""
    payload = {"results": [], "endOfRecords": True}
    client = FakeClient({"taxonKey=": payload})

    fetch_gbif(
        client,
        CONFIG,
        bbox=(9.68, 42.23, 12.38, 44.48),
        cache_root=tmp_path,
        fetched_at=FETCHED,
        cache_scope="tuscany",
    )
    first = len(client.urls)
    fetch_gbif(
        client,
        CONFIG,
        bbox=(11.89, 42.36, 13.27, 43.62),
        cache_root=tmp_path,
        fetched_at=FETCHED,
        cache_scope="umbria",
    )

    assert len(client.urls) == 2 * first
    assert all("11.89" in url for url in client.urls[first:])


def test_fetch_inaturalist_pages_every_taxon(tmp_path: Path) -> None:
    client = FakeClient(
        {
            f"taxon_id={taxon.inaturalist_taxon_id}": {
                "total_results": 1,
                "page": 1,
                "per_page": CONFIG.inaturalist.page_size,
                "results": [
                    {
                        "id": taxon.inaturalist_taxon_id * 10,
                        "observed_on": "2026-09-01",
                        "location": "43.8,11.2",
                        "public_positional_accuracy": 20,
                        "license_code": "cc-by-nc",
                        "obscured": False,
                        "quality_grade": "research",
                    }
                ],
            }
            for species in CONFIG.species.values()
            for taxon in species.taxa
        }
    )

    rows = fetch_inaturalist(
        client,
        CONFIG,
        since=date(2026, 9, 1),
        cache_root=tmp_path,
        fetched_at=FETCHED,
        place_id=10875,
        cache_scope="umbria",
    )

    total_taxa = sum(len(s.taxa) for s in CONFIG.species.values())
    assert len(rows) == total_taxa
    assert all("place_id=10875" in url for url in client.urls)
    assert (tmp_path / "inaturalist" / "umbria" / "48701" / "2026-09-01" / ".complete").exists()


# --- profile ------------------------------------------------------------------------------------


def test_profile_stats_summarizes_counts_and_town_proximity(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)
    store.upsert(
        pd.DataFrame(
            [
                {
                    "species": "porcini",
                    "cell_id": "1kmE4300N2400",
                    "date": date(2025, 10, 5),
                    "source": "gbif",
                    "record_id": "1",
                    "license": "CC0",
                    "obscured": False,
                    "fetched_at": FETCHED,
                },
                {
                    "species": "porcini",
                    "cell_id": "1kmE4301N2400",
                    "date": date(2026, 9, 1),
                    "source": "inaturalist",
                    "record_id": "2",
                    "license": "cc-by-nc",
                    "obscured": False,
                    "fetched_at": FETCHED,
                },
            ]
        )
    )
    cells = pd.DataFrame(
        {
            "cell_id": ["1kmE4300N2400", "1kmE4301N2400", "1kmE4302N2400"],
            "woodland": [True, True, True],
            "place_distance_km": [0.2, 3.0, 6.0],
        }
    )

    stats = profile_stats(store, cells)

    assert stats.total == 2
    assert stats.by_species == {"porcini": 2}
    assert stats.by_year == {2025: 1, 2026: 1}
    assert stats.by_license == {"CC0": 1, "cc-by-nc": 1}
    assert stats.mean_place_distance_km_sightings < stats.mean_place_distance_km_all_cells


# --- meta ----------------------------------------------------------------------------------


def test_write_meta_credits_every_configured_source(tmp_path: Path) -> None:
    store = SightingsStore(tmp_path)

    path = write_meta(CONFIG, store, "tuscany")

    import json

    meta = json.loads(path.read_text())
    assert meta["region"] == "tuscany"
    assert set(meta["sources"]) == set(CONFIG.credits)
    for source in meta["sources"].values():
        assert source["attribution"]
    assert meta["species"]["porcini"]["taxa"][0]["scientific_name"] == "Boletus edulis"
    assert (
        meta["quality"]["max_coordinate_uncertainty_m"]
        == CONFIG.quality.max_coordinate_uncertainty_m
    )
