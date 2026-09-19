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


def test_every_species_has_a_cited_growth_clock_long_enough_for_its_rain_lags() -> None:
    rules = load_rules()

    for species in rules.species.values():
        clock = species.clock
        assert clock is not None, species.key
        assert set(clock.source) <= set(rules.references), species.key
        assert clock.temperature.variable == "soil_temperature_0_to_7cm_mean"
        low, optimum, high = clock.temperature.cardinal_c
        assert low < clock.temperature.reference_c <= optimum < high, species.key
        for factor in species.enabled_factors:
            if factor.kind == "rain_event":
                assert clock.max_lag_days >= factor.response.lag_days[3], species.key


def test_every_species_scores_sun_exposure_and_slope_as_soft_stoppers() -> None:
    for species in load_rules().species.values():
        by_id = {f.id: f for f in species.enabled_factors}
        sun, slope = by_id["sun_exposure"], by_id["slope"]
        assert sun.role == slope.role == "stopper"
        assert sun.input.variable == "sun_exposure_pct"
        assert slope.input.attribute == "slope_deg"
        assert sun.floor >= 0.8 and slope.floor >= 0.8, species.key
        assert "aspect" not in {gap.id for gap in species.known_gaps}, species.key


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


def _growth(**fields) -> Callable[[dict], None]:
    return lambda doc: doc["growth"].update(fields)


def _growth_temperature(**fields) -> Callable[[dict], None]:
    return lambda doc: doc["growth"]["temperature"].update(fields)


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
    "growth without a source": (_growth(source=[]), "source"),
    "growth citing an unknown source": (_growth(source=["nobody2031"]), "nobody2031"),
    "growth derived without notes": (lambda doc: doc["growth"].pop("notes"), "notes"),
    "growth cardinal temperatures out of order": (
        _growth_temperature(cardinal_c=[18, 0, 30]),
        "cardinal_c",
    ),
    "growth reference outside the cardinal range": (
        _growth_temperature(reference_c=35),
        "reference_c",
    ),
    "growth on a variable the weather ingest lacks": (
        _growth_temperature(variable="soil_temperature_7_to_28cm_mean"),
        "soil_temperature_7_to_28cm_mean",
    ),
    "growth lookback shorter than the rain lag window": (_growth(max_lag_days=20), "max_lag_days"),
    "where on a driver": (
        _set("rain_30d", where={"attribute": "elevation_m", "trapezoid": [None, None, 900, 1100]}),
        "where",
    ),
    "where on an attribute the grid lacks": (
        _set("sun_exposure", where={"attribute": "stand_age", "trapezoid": [None, None, 10, 20]}),
        "stand_age",
    ),
    "unordered where trapezoid": (
        _set(
            "sun_exposure", where={"attribute": "elevation_m", "trapezoid": [None, None, 900, 100]}
        ),
        "order",
    ),
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
