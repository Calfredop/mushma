from pathlib import Path

import pytest
import yaml

from api.grid.sources import load_sources
from api.sightings.config import load_sightings_config


def test_species_carry_at_least_one_taxon_each() -> None:
    config = load_sightings_config()

    assert set(config.species) == {"porcini", "ovoli", "gallinacci"}
    for key, species in config.species.items():
        assert species.taxa, key
        for taxon in species.taxa:
            assert taxon.gbif_taxon_key > 0
            assert taxon.inaturalist_taxon_id > 0


def test_porcini_group_has_four_boletus_taxa() -> None:
    config = load_sightings_config()

    names = {taxon.scientific_name for taxon in config.species["porcini"].taxa}
    assert names == {
        "Boletus edulis",
        "Boletus aereus",
        "Boletus reticulatus",
        "Boletus pinophilus",
    }


def test_species_of_looks_up_by_gbif_or_inaturalist_taxon_id() -> None:
    config = load_sightings_config()

    assert config.species_of(5240269) == "ovoli"
    assert config.species_of(999999) is None
    assert config.species_of_inaturalist(47347) == "gallinacci"
    assert config.species_of_inaturalist(999999) is None


def test_gbif_taxon_keys_are_unique_across_species() -> None:
    config = load_sightings_config()

    keys = [taxon.gbif_taxon_key for species in config.species.values() for taxon in species.taxa]
    assert len(keys) == len(set(keys))


def test_quality_thresholds_are_positive() -> None:
    config = load_sightings_config()

    assert config.quality.max_coordinate_uncertainty_m > 0
    assert config.quality.town_centroid_distance_m > 0


def test_inaturalist_recency_window_is_days_not_months() -> None:
    config = load_sightings_config()

    assert 1 <= config.inaturalist.recent_days <= 60
    assert config.inaturalist.place_id > 0
    assert config.inaturalist.quality_grades


def test_every_credited_source_is_in_the_catalog() -> None:
    config = load_sightings_config()
    catalog = load_sources()

    assert config.credits
    for source_id in config.credits:
        assert catalog[source_id].attribution, source_id


def test_a_duplicate_gbif_taxon_key_is_rejected(tmp_path: Path) -> None:
    from api.sightings.config import SIGHTINGS_FILE

    raw = yaml.safe_load(SIGHTINGS_FILE.read_text())
    raw["species"]["ovoli"]["taxa"][0]["gbif_taxon_key"] = raw["species"]["porcini"]["taxa"][0][
        "gbif_taxon_key"
    ]
    path = tmp_path / "sightings.yaml"
    path.write_text(yaml.safe_dump(raw, allow_unicode=True))

    with pytest.raises(ValueError, match="gbif_taxon_key"):
        load_sightings_config(path)


def test_a_non_positive_quality_threshold_is_rejected(tmp_path: Path) -> None:
    from api.sightings.config import SIGHTINGS_FILE

    raw = yaml.safe_load(SIGHTINGS_FILE.read_text())
    raw["quality"]["max_coordinate_uncertainty_m"] = 0
    path = tmp_path / "sightings.yaml"
    path.write_text(yaml.safe_dump(raw, allow_unicode=True))

    with pytest.raises(ValueError, match="max_coordinate_uncertainty_m"):
        load_sightings_config(path)
