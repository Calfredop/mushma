from api.fixtures.cells import CELLS
from api.fixtures.sightings import LICENSES, counts_since, recent_sightings_total, sighting_events
from api.species import SPECIES


class TestSightingEvents:
    def test_deterministic(self) -> None:
        cell = CELLS[0]
        assert sighting_events(cell, "porcini") == sighting_events(cell, "porcini")

    def test_every_event_has_a_licensed_source(self) -> None:
        for cell in CELLS:
            for species in SPECIES:
                for event in sighting_events(cell, species):
                    assert event.source in LICENSES
                    assert event.days_ago >= 1

    def test_not_every_cell_has_sightings(self) -> None:
        # presence-only bias (PRD -> Model -> Known data traps): sparse, not uniform
        counts = [len(sighting_events(cell, "porcini")) for cell in CELLS]
        assert any(c == 0 for c in counts)
        assert any(c > 0 for c in counts)


class TestCountsSince:
    def test_a_narrower_window_never_counts_more_than_a_wider_one(self) -> None:
        cell = CELLS[0]
        for species in SPECIES:
            narrow = sum(counts_since(cell, species, since_days_ago=10).values())
            wide = sum(counts_since(cell, species, since_days_ago=365).values())
            assert narrow <= wide

    def test_never_exposes_anything_but_cell_id_and_count(self) -> None:
        # sightings privacy (PRD -> Principles): no coordinates ever leave this module
        cell = CELLS[0]
        counts = counts_since(cell, "porcini", since_days_ago=365)
        assert set(counts.keys()) <= set(LICENSES.keys())
        assert all(isinstance(v, int) for v in counts.values())


class TestRecentSightingsTotal:
    def test_combined_sums_all_three_species(self) -> None:
        cell = CELLS[0]
        per_species_total = sum(
            sum(counts_since(cell, species, since_days_ago=365).values()) for species in SPECIES
        )
        assert recent_sightings_total(cell, "combined", since_days_ago=365) == per_species_total
