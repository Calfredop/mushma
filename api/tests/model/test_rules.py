import shutil
from collections.abc import Callable
from datetime import date
from pathlib import Path

import numpy as np
import pytest
import yaml

from api.grid.habitats import load_vocabulary
from api.model.engine import score_species
from api.model.rules import (
    DEFAULT_REGION,
    SPECIES_DIR,
    RuleConfigError,
    list_rule_regions,
    load_rules,
)
from api.weather.config import load_weather_config

from .helpers import cells, weather

KEYS = {
    "porcini_edulis",
    "porcini_reticulatus",
    "porcini_aereus",
    "porcini_pinophilus",
    "ovoli_caesarea",
    "gallinacci_cibarius",
}

# Frozen before the per-region move: porcini_edulis on a beech cell, 12 days after a 45 mm rain.
TUSCANY_WET_SCORE = 1.0
TUSCANY_SPECIES_SHA = "61d40acba3382dd552f5f3fe675399737ac46f7ee0defe657496d4619670ee03"


def test_regions_are_discovered_under_species() -> None:
    assert DEFAULT_REGION in list_rule_regions()
    assert (SPECIES_DIR / DEFAULT_REGION).is_dir()
    assert (SPECIES_DIR / "references.yaml").is_file()


@pytest.mark.parametrize("region", list_rule_regions())
def test_every_region_loads_with_valid_files_variables_and_references(region: str) -> None:
    rules = load_rules(region)
    ingested = set(load_weather_config().variables)
    habitats = set(load_vocabulary().habitats)

    assert rules.species
    assert set(rules.groups) <= {"porcini", "ovoli", "gallinacci"}
    for species in rules.species.values():
        for factor in species.factors:
            assert factor.source and set(factor.source) <= set(rules.references)
            assert factor.confidence in {"strong", "plausible", "folklore"}
            if factor.kind == "habitat":
                assert set(factor.input.affinity) <= habitats
            if not factor.enabled:
                continue
            uses = factor.uses
            if factor.kind != "static_band" and uses is not None and uses != "sun_exposure_pct":
                from api.model.rules import DERIVED_SERIES

                for variable in DERIVED_SERIES.get(uses, (uses,)):
                    assert variable in ingested, f"{species.key}.{factor.id}: {variable}"


def test_the_shipped_tuscany_rules_load_with_one_file_per_species_key() -> None:
    rules = load_rules("tuscany")

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


def test_a_tuscany_score_for_the_test_window_is_unchanged_after_the_move() -> None:
    import hashlib
    import json

    rules = load_rules("tuscany")
    blob = json.dumps(
        {k: s.model_dump(mode="json") for k, s in rules.species.items()},
        sort_keys=True,
    ).encode()
    assert hashlib.sha256(blob).hexdigest() == TUSCANY_SPECIES_SHA

    edulis = rules.species["porcini_edulis"]
    beech = cells(elevation_m=[1100], habitats={"beech": [1.0]})
    days = 90
    rain = [2.0] * days
    for d in range(3):
        rain[days - 1 - 12 - d] = 15.0
    autumn = weather(
        start=date(2024, 8, 1),
        precipitation_sum=rain,
        temperature_2m_mean=[13.0] * days,
        temperature_2m_min=[8.0] * days,
        temperature_2m_max=[19.0] * days,
        soil_temperature_0_to_7cm_mean=[13.0] * days,
        snowfall_sum=[0.0] * days,
        et0_fao_evapotranspiration=[1.5] * days,
        vapour_pressure_deficit_max=[0.6] * days,
        sun_exposure_pct=[100.0] * days,
    )
    autumn.normals["precipitation_sum"] = np.full((1, days), 2.0)

    wet = score_species(edulis, beech, autumn, date(2024, 10, 29)).score[0, 0]
    assert float(wet) == pytest.approx(TUSCANY_WET_SCORE)


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


def test_a_region_may_omit_a_group(tmp_path: Path) -> None:
    root = _region_tree(tmp_path, "alpine")
    for path in (root / "alpine").glob("*.yaml"):
        if path.stem.startswith("ovoli") or path.stem.startswith("gallinacci"):
            path.unlink()

    rules = load_rules("alpine", species_dir=root)

    assert set(rules.groups) == {"porcini"}
    assert "ovoli_caesarea" not in rules.species


# --- broken copies: the loader must refuse each one ---------------------------------------------


def _region_tree(tmp_path: Path, region: str = "tuscany") -> Path:
    """A species root with shared references and one region's files (no sanity.yaml)."""
    root = tmp_path / "species"
    (root / region).mkdir(parents=True)
    shutil.copy(SPECIES_DIR / "references.yaml", root / "references.yaml")
    for path in (SPECIES_DIR / DEFAULT_REGION).glob("*.yaml"):
        if path.name == "sanity.yaml":
            continue
        shutil.copy(path, root / region / path.name)
    return root


def _broken_copy(tmp_path: Path, key: str, mutate: Callable[[dict], None]) -> Path:
    root = _region_tree(tmp_path)
    path = root / "tuscany" / f"{key}.yaml"
    doc = yaml.safe_load(path.read_text())
    mutate(doc)
    path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))
    return root


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
    "percent of normal on a variable without normals": (
        _set(
            "air_temperature",
            input={
                "variable": "temperature_2m_mean",
                "aggregate": "percent_of_normal",
                "window_days": 20,
            },
        ),
        "percent_of_normal",
    ),
    "bad date": (
        lambda doc: _factor(doc, "season")["input"]["windows"][0].update(
            {"dates": ["01-07", "31-09", "15-11", "20-12"]}
        ),
        "31-09",
    ),
    "elevation weights that do not sum to 1": (
        lambda doc: _factor(doc, "season")["input"].update(
            {
                "windows": [
                    dict(_factor(doc, "season")["input"]["windows"][0], elevation_weight=w)
                    for w in ([None, None, 600, 1000], [None, None, 600, 1000])
                ]
            }
        ),
        "sum to 1",
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
    root = _broken_copy(tmp_path, "porcini_edulis", mutate)

    with pytest.raises(RuleConfigError, match=message) as error:
        load_rules("tuscany", species_dir=root)
    assert "porcini_edulis" in str(error.value)


def test_an_enabled_percent_of_normal_rain_rule_loads(tmp_path: Path) -> None:
    root = _broken_copy(tmp_path, "porcini_edulis", _set("early_season_wetness", enabled=True))

    factors = load_rules("tuscany", species_dir=root).species["porcini_edulis"].factors
    rule = next(f for f in factors if f.id == "early_season_wetness")

    assert rule.enabled and rule.input.aggregate == "percent_of_normal"


def test_the_untouched_copy_loads(tmp_path: Path) -> None:
    root = _broken_copy(tmp_path, "porcini_edulis", lambda doc: None)

    assert set(load_rules("tuscany", species_dir=root).species) == KEYS


def test_a_key_not_listed_in_model_yaml_is_refused(tmp_path: Path) -> None:
    root = _region_tree(tmp_path)
    stray = root / "tuscany" / "porcini_mystery.yaml"
    doc = yaml.safe_load((root / "tuscany" / "porcini_edulis.yaml").read_text())
    doc["key"] = "porcini_mystery"
    stray.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))

    with pytest.raises(RuleConfigError, match="group"):
        load_rules("tuscany", species_dir=root)
