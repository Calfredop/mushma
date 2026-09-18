"""Fixture stand-in for M2 sightings ingest (GBIF + iNaturalist).

Only ever produces per-cell, per-source counts -- PRD -> Principles ->
Sightings privacy: coordinates never leave the sightings store, and this
fixture has none to leak in the first place.
"""

import hashlib
from dataclasses import dataclass

from api.fixtures.cells import CellSpec
from api.species import SPECIES, Species, SpeciesOrCombined

LICENSES: dict[str, str] = {
    "gbif": "CC-BY 4.0",
    "inaturalist": "CC-BY-NC 4.0",
}


@dataclass(frozen=True)
class SightingEvent:
    days_ago: int
    source: str


def _stable_int(*parts: str, modulo: int) -> int:
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return int(digest[:8], 16) % modulo


def sighting_events(cell: CellSpec, species: Species) -> list[SightingEvent]:
    if _stable_int(cell.id, species, "present", modulo=3) == 0:
        return []  # presence-only bias (PRD -> Known data traps): most cells have none
    count = 1 + _stable_int(cell.id, species, "count", modulo=4)
    events = []
    for i in range(count):
        days_ago = 3 + _stable_int(cell.id, species, f"days{i}", modulo=300)
        source = (
            "gbif" if _stable_int(cell.id, species, f"src{i}", modulo=2) == 0 else "inaturalist"
        )
        events.append(SightingEvent(days_ago=days_ago, source=source))
    return events


def counts_since(cell: CellSpec, species: Species, since_days_ago: int) -> dict[str, int]:
    """source -> count of events at least as recent as `since_days_ago` days back."""
    return counts_between(cell, species, since_days_ago, 0)


def counts_between(
    cell: CellSpec, species: Species, since_days_ago: int, until_days_ago: int
) -> dict[str, int]:
    """source -> count of events from `since_days_ago` to `until_days_ago` days back."""
    counts: dict[str, int] = {}
    for event in sighting_events(cell, species):
        if until_days_ago <= event.days_ago <= since_days_ago:
            counts[event.source] = counts.get(event.source, 0) + 1
    return counts


def recent_sightings_total(cell: CellSpec, species: SpeciesOrCombined, since_days_ago: int) -> int:
    species_list = SPECIES if species == "combined" else (species,)
    return sum(sum(counts_since(cell, sp, since_days_ago).values()) for sp in species_list)
