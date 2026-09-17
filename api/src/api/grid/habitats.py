"""The habitat vocabulary shared by the woodland grid and the species rules."""

from dataclasses import dataclass
from pathlib import Path

import yaml

HABITATS_FILE = Path(__file__).resolve().parent.parent / "config" / "habitats.yaml"


@dataclass(frozen=True)
class GroupSpec:
    woodland: bool
    fallback: str


@dataclass(frozen=True)
class Vocabulary:
    habitats: list[str]  # in tie-break order
    group_of: dict[str, str]  # habitat -> broad group, in tie-break order
    groups: dict[str, GroupSpec]

    @property
    def fallback(self) -> dict[str, str]:
        return {name: spec.fallback for name, spec in self.groups.items()}


def load_vocabulary(path: Path = HABITATS_FILE) -> Vocabulary:
    raw = yaml.safe_load(path.read_text())
    groups = {name: GroupSpec(**spec) for name, spec in raw["groups"].items()}
    group_of = {name: spec["group"] for name, spec in raw["habitats"].items()}
    for habitat, group in group_of.items():
        if group not in groups:
            raise ValueError(f"habitat {habitat!r} has unknown group {group!r}")
    for group, spec in groups.items():
        if group_of.get(spec.fallback) != group:
            raise ValueError(f"fallback {spec.fallback!r} of group {group!r} is not in that group")
    return Vocabulary(habitats=list(group_of), group_of=group_of, groups=groups)
