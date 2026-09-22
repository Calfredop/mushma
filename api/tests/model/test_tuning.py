import pytest

from api.model.config import load_model_config
from api.model.rules import load_rules
from api.model.tuning import (
    RAIN_SEARCH,
    SEARCH,
    SEARCHES,
    Change,
    Choice,
    coordinate_descent,
    set_factor,
    set_precipitation_scale,
    shift_growth_temperature,
)


def test_set_factor_changes_one_factor_and_revalidates() -> None:
    rules = load_rules()

    changed = set_factor(
        rules, "ovoli_caesarea", "rain_trigger", {"response": {"lag_days": [10, 15, 24, 32]}}
    )

    factor = next(f for f in changed.species["ovoli_caesarea"].factors if f.id == "rain_trigger")
    assert factor.response.lag_days == (10, 15, 24, 32)
    assert factor.response.amount_mm == (10, 30, None, None)  # untouched
    original = next(f for f in rules.species["ovoli_caesarea"].factors if f.id == "rain_trigger")
    assert original.response.lag_days == (6, 10, 20, 28)


def test_set_factor_refuses_an_invalid_result() -> None:
    with pytest.raises(ValueError, match="order"):
        set_factor(
            load_rules(), "ovoli_caesarea", "rain_trigger", {"response": {"lag_days": [9, 1, 2, 3]}}
        )


def test_set_factor_refuses_to_touch_frozen_gates() -> None:
    with pytest.raises(ValueError, match="frozen"):
        set_factor(
            load_rules(),
            "porcini_edulis",
            "altitude",
            {"response": {"trapezoid": [0, 500, 1600, 1900]}},
            frozen_kinds=load_model_config().backtest.frozen_factor_kinds,
        )


def test_set_precipitation_scale_toggles_the_model_config() -> None:
    config = load_model_config()

    assert not set_precipitation_scale(config, False).precipitation_scale.enabled
    assert config.precipitation_scale.enabled


def _choice(name: str, group: str, *labels: str) -> Choice:
    return Choice(
        name=name,
        groups=[group],
        options=[
            Change(label, lambda rules, config, label=label: (rules, config)) for label in labels
        ],
    )


def test_coordinate_descent_keeps_a_change_only_when_it_clears_the_margin() -> None:
    search = [
        _choice("lag", "ovoli", "prior", "longer"),
        _choice("stopper", "ovoli", "prior", "off"),
    ]
    gains = {"longer": 0.05, "off": 0.01}  # only the first clears a 0.02 margin
    applied: list[str] = []

    def evaluate(rules, config, groups, trail):
        return {"ovoli": 0.6 + sum(gains.get(label, 0.0) for label in trail)}

    result = coordinate_descent(
        search, load_rules(), load_model_config(), evaluate, margin=0.02, log=applied.append
    )

    assert result.kept == {"lag": "longer", "stopper": "prior"}
    assert result.objective["ovoli"] == pytest.approx(0.65)
    assert [(row["choice"], row["option"]) for row in result.trials] == [
        ("lag", "prior"),
        ("lag", "longer"),
        ("stopper", "off"),
    ]


def test_shift_growth_temperature_moves_the_cardinal_curve_and_its_reference() -> None:
    rules = load_rules()

    shifted = shift_growth_temperature(rules, "ovoli_caesarea", -3)

    temperature = shifted.species["ovoli_caesarea"].growth.temperature
    assert temperature.cardinal_c == (2, 19, 31)
    assert temperature.reference_c == 15
    assert rules.species["ovoli_caesarea"].growth.temperature.reference_c == 18


def test_the_rain_search_is_its_own_pre_registered_search() -> None:
    assert SEARCHES == {"v1": SEARCH, "rain": RAIN_SEARCH}
    names = [choice.name for choice in RAIN_SEARCH]
    assert "porcini_rain_30d" in names and "gallinacci_sun_exposure" in names
    relative = next(
        o
        for c in RAIN_SEARCH
        if c.name == "porcini_rain_30d"
        for o in c.options
        if o.label == "relative"
    )
    rules, _ = relative.apply(load_rules(), load_model_config())
    rain = next(f for f in rules.species["porcini_edulis"].factors if f.id == "rain_30d")
    assert rain.input.aggregate == "percent_of_normal"


@pytest.mark.parametrize("search", ["v1", "rain"])
def test_every_pre_registered_choice_starts_from_the_prior_and_applies_cleanly(
    search: str,
) -> None:
    rules, config = load_rules(), load_model_config()
    frozen = set(config.backtest.frozen_factor_kinds)

    for choice in SEARCHES[search]:
        assert choice.options[0].label == "prior", choice.name
        for option in choice.options:
            new_rules, new_config = option.apply(rules, config)
            for key, spec in new_rules.species.items():
                for before, after in zip(rules.species[key].factors, spec.factors, strict=True):
                    if before.kind in frozen:
                        assert before == after, (
                            f"{choice.name}/{option.label} changed {key}.{before.id}"
                        )
