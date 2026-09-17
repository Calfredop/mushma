import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from api.grid.habitats import load_vocabulary
from api.model.rules import SPECIES_DIR, RuleConfigError, load_rules

KEYS = {
    "porcini_edulis",
    "porcini_reticulatus",
    "porcini_aereus",
    "porcini_pinophilus",
    "ovoli_caesarea",
    "gallinacci_cibarius",
}


def test_the_shipped_rules_load_with_one_file_per_species_key() -> None:
    rules = load_rules()

    assert set(rules.species) == KEYS
    assert rules.groups == {
        "porcini": [
            "porcini_edulis",
            "porcini_reticulatus",
            "porcini_aereus",
            "porcini_pinophilus",
        ],
        "ovoli": ["ovoli_caesarea"],
        "gallinacci": ["gallinacci_cibarius"],
    }


def test_every_factor_cites_references_that_exist() -> None:
    rules = load_rules()

    for species in rules.species.values():
        for factor in species.factors:
            assert factor.source, f"{species.key}.{factor.id}"
            assert set(factor.source) <= set(rules.references), f"{species.key}.{factor.id}"
            assert factor.confidence in {"strong", "plausible", "folklore"}


def test_enabled_factors_are_listed_gates_then_drivers_then_stoppers() -> None:
    species = load_rules().species["porcini_edulis"]

    roles = [factor.role for factor in species.enabled_factors]
    assert roles == sorted(roles, key=["gate", "driver", "stopper"].index)
    assert [f.id for f in species.enabled_factors][:3] == ["season", "habitat", "altitude"]
    assert "soil_temperature" not in {f.id for f in species.enabled_factors}


def test_habitat_affinities_use_the_grid_vocabulary() -> None:
    habitats = set(load_vocabulary().habitats)

    for species in load_rules().species.values():
        for factor in species.factors:
            if factor.kind == "habitat":
                assert set(factor.input.affinity) <= habitats


# --- broken copies: the loader must refuse each one ---------------------------------------------


def _broken_copy(tmp_path: Path, key: str, mutate: Callable[[dict], None]) -> Path:
    folder = tmp_path / "species"
    shutil.copytree(SPECIES_DIR, folder)
    path = folder / f"{key}.yaml"
    doc = yaml.safe_load(path.read_text())
    mutate(doc)
    path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))
    return folder


def _factor(doc: dict, factor_id: str) -> dict:
    return next(f for f in doc["factors"] if f["id"] == factor_id)


def _set(factor_id: str, **fields) -> Callable[[dict], None]:
    return lambda doc: _factor(doc, factor_id).update(fields)


def _drop(factor_id: str, field: str) -> Callable[[dict], None]:
    return lambda doc: _factor(doc, factor_id).pop(field)


BROKEN = {
    "empty source": (_set("rain_trigger", source=[]), "source"),
    "missing source": (_drop("rain_30d", "source"), "source"),
    "unknown source id": (_set("frost", source=["nobody2031"]), "nobody2031"),
    "missing confidence": (_drop("frost", "confidence"), "confidence"),
    "unordered trapezoid": (
        _set("altitude", response={"trapezoid": [700, 200, 1600, 1900]}),
        "order",
    ),
    "half-open trapezoid pair": (
        _set("altitude", response={"trapezoid": [None, 700, 1600, 1900]}),
        "null",
    ),
    "driver without weight": (_drop("rain_30d", "weight"), "weight"),
    "gate with a weight": (_set("habitat", weight=1), "weight"),
    "unknown habitat": (
        lambda doc: _factor(doc, "habitat")["input"]["affinity"].update({"bamboo": 1.0}),
        "bamboo",
    ),
    "unknown variable": (
        _set(
            "rain_30d",
            input={"variable": "rainfall", "aggregate": "sum", "window_days": 30},
        ),
        "rainfall",
    ),
    "enabled rule on a variable the weather ingest lacks": (
        _set(
            "rain_30d",
            input={"variable": "wind_gusts_10m_max", "aggregate": "max", "window_days": 3},
        ),
        "wind_gusts_10m_max",
    ),
    "enabled rule on missing data": (_set("frost", data="missing"), "missing"),
    "derived rule without notes": (_drop("frost", "notes"), "notes"),
    "enabled climatology aggregate": (_set("soil_moisture", enabled=True), "climatology"),
    "bad date": (
        lambda doc: _factor(doc, "season")["input"]["windows"][0].update(
            {"dates": ["01-07", "31-09", "15-11", "20-12"]}
        ),
        "31-09",
    ),
    "duplicate factor id": (
        lambda doc: doc["factors"].append(dict(_factor(doc, "frost"))),
        "duplicate",
    ),
    "no enabled driver": (
        lambda doc: [f.update(enabled=False) for f in doc["factors"] if f["role"] == "driver"],
        "driver",
    ),
    "key not matching the file name": (lambda doc: doc.update(key="porcini_other"), "file name"),
    "unknown factor kind": (_set("frost", kind="moon_phase"), "moon_phase"),
    "unexpected field": (_set("frost", treshold=3), "treshold"),
    "group not matching the model config": (lambda doc: doc.update(group="ovoli"), "group"),
}


@pytest.mark.parametrize("case", list(BROKEN), ids=list(BROKEN))
def test_a_broken_rule_file_is_refused(tmp_path: Path, case: str) -> None:
    mutate, message = BROKEN[case]
    folder = _broken_copy(tmp_path, "porcini_edulis", mutate)

    with pytest.raises(RuleConfigError, match=message) as error:
        load_rules(folder)
    assert "porcini_edulis" in str(error.value)


def test_the_untouched_copy_loads(tmp_path: Path) -> None:
    folder = _broken_copy(tmp_path, "porcini_edulis", lambda doc: None)

    assert set(load_rules(folder).species) == KEYS


def test_a_species_file_missing_from_the_groups_is_refused(tmp_path: Path) -> None:
    folder = tmp_path / "species"
    shutil.copytree(SPECIES_DIR, folder)
    (folder / "ovoli_caesarea.yaml").unlink()

    with pytest.raises(RuleConfigError, match="ovoli_caesarea"):
        load_rules(folder)
