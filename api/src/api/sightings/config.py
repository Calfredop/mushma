"""Sightings config: species taxa, quality thresholds and the iNaturalist recency window, from
``config/sightings.yaml``."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from api.grid.region import RegionConfig
from api.model.rules import DEFAULT_REGION

SIGHTINGS_FILE = Path(__file__).resolve().parent.parent / "config" / "sightings.yaml"


@dataclass(frozen=True)
class Taxon:
    scientific_name: str
    gbif_taxon_key: int
    inaturalist_taxon_id: int
    # GBIF rank the name is matched at: a genus pulls every species under it...
    rank: str = "SPECIES"
    # ...except these species keys, which GBIF files under the genus but are not the target.
    exclude_gbif_taxon_keys: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class Species:
    common_name: dict[str, str]
    taxa: list[Taxon]

    @property
    def gbif_taxon_keys(self) -> list[int]:
        return [taxon.gbif_taxon_key for taxon in self.taxa]


@dataclass(frozen=True)
class GbifSpec:
    endpoint: str
    match_endpoint: str
    page_size: int


@dataclass(frozen=True)
class INaturalistSpec:
    endpoint: str
    place_id: int
    page_size: int
    recent_days: int
    quality_grades: list[str]


@dataclass(frozen=True)
class QualitySpec:
    max_coordinate_uncertainty_m: float
    town_centroid_distance_m: float
    # GBIF basisOfRecord values that are not a fruiting body someone saw (e.g. soil DNA).
    exclude_basis_of_record: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SightingsConfig:
    species: dict[str, Species]
    gbif: GbifSpec
    inaturalist: INaturalistSpec
    quality: QualitySpec
    credits: list[str]

    def species_of(self, gbif_taxon_key: int) -> str | None:
        """The species key whose taxa include this GBIF taxon key, if any."""
        for key, species in self.species.items():
            if gbif_taxon_key in species.gbif_taxon_keys:
                return key
        return None

    def excluded_gbif_species(self, gbif_taxon_key: int) -> list[int]:
        """Species keys to drop from the records fetched for this configured taxon key."""
        for species in self.species.values():
            for taxon in species.taxa:
                if taxon.gbif_taxon_key == gbif_taxon_key:
                    return taxon.exclude_gbif_taxon_keys
        return []

    def species_of_inaturalist(self, inaturalist_taxon_id: int) -> str | None:
        """The species key whose taxa include this iNaturalist taxon id, if any."""
        for key, species in self.species.items():
            if inaturalist_taxon_id in (t.inaturalist_taxon_id for t in species.taxa):
                return key
        return None


def load_sightings_config(path: Path = SIGHTINGS_FILE) -> SightingsConfig:
    raw = yaml.safe_load(path.read_text())
    species = {
        key: Species(
            common_name=dict(spec["common_name"]),
            taxa=[Taxon(**taxon) for taxon in spec["taxa"]],
        )
        for key, spec in raw["species"].items()
    }
    keys = [taxon.gbif_taxon_key for s in species.values() for taxon in s.taxa]
    if len(keys) != len(set(keys)):
        raise ValueError(f"gbif_taxon_key must be unique across species, got {keys}")

    quality = QualitySpec(**raw["quality"])
    if quality.max_coordinate_uncertainty_m <= 0:
        raise ValueError(
            "quality.max_coordinate_uncertainty_m must be positive, got "
            f"{quality.max_coordinate_uncertainty_m}"
        )
    if quality.town_centroid_distance_m <= 0:
        raise ValueError(
            f"quality.town_centroid_distance_m must be positive, got "
            f"{quality.town_centroid_distance_m}"
        )

    return SightingsConfig(
        species=species,
        gbif=GbifSpec(**raw["gbif"]),
        inaturalist=INaturalistSpec(**raw["inaturalist"]),
        quality=quality,
        credits=list(raw.get("credits") or []),
    )


def inaturalist_place_id(region: RegionConfig, config: SightingsConfig) -> int:
    """The iNaturalist place a region's recent observations are filtered to.

    ``sightings.inaturalist_place_id`` in the region YAML, resolved once by the place's name. The
    default region keeps the place in ``sightings.yaml``; any other region must name its own, or
    its fetch would silently pull the default region's observations.
    """
    place = (region.extra.get("sightings") or {}).get("inaturalist_place_id")
    if place is not None:
        return int(place)
    if region.id == DEFAULT_REGION:
        return config.inaturalist.place_id
    raise ValueError(
        f"region {region.id!r} has no sightings.inaturalist_place_id in its config: resolve the "
        "region's place by name (api.inaturalist.org/v1/places/autocomplete) and add it"
    )
