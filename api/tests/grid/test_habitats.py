from api.grid.habitats import load_vocabulary
from api.model.rules import load_rules


def test_vocabulary_groups_every_habitat_and_falls_back_inside_the_group() -> None:
    vocabulary = load_vocabulary()

    assert vocabulary.habitats[0] == "beech"
    for group, spec in vocabulary.groups.items():
        assert vocabulary.group_of[spec.fallback] == group
    assert set(vocabulary.group_of.values()) == set(vocabulary.groups)
    assert vocabulary.groups["broadleaf"].woodland
    assert not vocabulary.groups["macchia"].woodland


def test_every_species_rule_scores_every_habitat_in_the_vocabulary() -> None:
    habitats = set(load_vocabulary().habitats)

    for species in load_rules().species.values():
        (habitat,) = [f for f in species.factors if f.kind == "habitat"]
        assert set(habitat.input.affinity) == habitats, species.key
