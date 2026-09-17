import json
from pathlib import Path

import pytest

from api.grid.habitats import load_vocabulary

SPECIES_SCHEMA = (
    Path(__file__).resolve().parents[3] / ".gavin-root/docs/species-rules/species.schema.json"
)


def test_vocabulary_groups_every_habitat_and_falls_back_inside_the_group() -> None:
    vocabulary = load_vocabulary()

    assert vocabulary.habitats[0] == "beech"
    for group, spec in vocabulary.groups.items():
        assert vocabulary.group_of[spec.fallback] == group
    assert set(vocabulary.group_of.values()) == set(vocabulary.groups)
    assert vocabulary.groups["broadleaf"].woodland
    assert not vocabulary.groups["macchia"].woodland


@pytest.mark.skipif(not SPECIES_SCHEMA.exists(), reason="species rule schema not in the repo")
def test_vocabulary_matches_the_species_rule_schema() -> None:
    schema = json.loads(SPECIES_SCHEMA.read_text())

    assert set(load_vocabulary().habitats) == set(schema["$defs"]["habitat"]["enum"])
