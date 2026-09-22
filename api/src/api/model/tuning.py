"""Tune the rules on the train seasons: one pass of coordinate descent over pre-registered choices.

    uv run python -m api.model.tuning --label tuned

Every choice lists its alternatives with the prior first: the comparison pairs the species research
handed over (rain vs water balance, air vs soil temperature, the ovoli lag), the folklore stoppers
on or off, shifts of the rain trigger's amount and lag, driver weights, and the rain scale. Choices
are tried in order; an alternative is kept only if it raises the train objective of the choice's
groups (``api.model.backtest.objective``) by at least ``MARGIN``, because with a few dozen
sightings per group smaller gains are noise. Season windows, altitude bands and habitat affinities
are frozen (``config/model.yaml``). The search was fixed before any train season was scored.
"""

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from pydantic import TypeAdapter

from api.grid.sources import data_dir
from api.model.backtest import objective, prepare, run
from api.model.config import ModelConfig, load_model_config
from api.model.rules import Factor, RuleSet, SpeciesRules, load_rules

MARGIN = 0.02
_FACTOR = TypeAdapter(Factor)

Apply = Callable[[RuleSet, ModelConfig], tuple[RuleSet, ModelConfig]]
Evaluate = Callable[[RuleSet, ModelConfig, list[str], list[str]], dict[str, float]]


@dataclass(frozen=True)
class Change:
    label: str
    apply: Apply


@dataclass(frozen=True)
class Choice:
    name: str
    groups: list[str]
    options: list[Change]  # the prior first


def _merge(base: dict, update: dict) -> dict:
    merged = dict(base)
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def set_factor(
    rules: RuleSet,
    key: str,
    factor_id: str,
    update: dict,
    frozen_kinds: list[str] | tuple[str, ...] = (),
) -> RuleSet:
    """A copy of ``rules`` with one factor's fields deep-merged with ``update`` and revalidated."""
    species = rules.species[key]
    factors = []
    for factor in species.factors:
        if factor.id == factor_id:
            if factor.kind in frozen_kinds:
                raise ValueError(f"{key}.{factor_id} is a {factor.kind}, which is frozen")
            factor = _FACTOR.validate_python(_merge(factor.model_dump(), update))
        factors.append(factor)
    rebuilt = SpeciesRules.model_validate(
        {**species.model_dump(), "factors": [f.model_dump() for f in factors]}
    )
    return RuleSet(
        species={**rules.species, key: rebuilt},
        groups=rules.groups,
        references=rules.references,
    )


def shift_growth_temperature(rules: RuleSet, key: str, delta_c: float) -> RuleSet:
    """A copy of ``rules`` with one key's growth-clock temperatures (cardinal curve and reference)
    moved by ``delta_c``: the same curve, warmer or cooler."""
    species = rules.species[key]
    temperature = species.growth.temperature
    growth = species.growth.model_dump()
    growth["temperature"] = {
        **temperature.model_dump(),
        "cardinal_c": [t + delta_c for t in temperature.cardinal_c],
        "reference_c": temperature.reference_c + delta_c,
    }
    rebuilt = SpeciesRules.model_validate({**species.model_dump(), "growth": growth})
    return RuleSet(
        species={**rules.species, key: rebuilt},
        groups=rules.groups,
        references=rules.references,
    )


def set_precipitation_scale(config: ModelConfig, enabled: bool) -> ModelConfig:
    scale = config.precipitation_scale.model_copy(update={"enabled": enabled})
    return config.model_copy(update={"precipitation_scale": scale})


def _factors(keys: list[str], updates: dict[str, dict]) -> Apply:
    """Apply ``{factor_id: update}`` to every key that has the factor."""

    def apply(rules: RuleSet, config: ModelConfig) -> tuple[RuleSet, ModelConfig]:
        frozen = config.backtest.frozen_factor_kinds
        for key in keys:
            present = {f.id for f in rules.species[key].factors}
            for factor_id, update in updates.items():
                if factor_id in present:
                    rules = set_factor(rules, key, factor_id, update, frozen)
        return rules, config

    return apply


def _clock(keys: list[str], delta_c: float) -> Apply:
    """Shift every key's growth-clock temperatures by ``delta_c``."""

    def apply(rules: RuleSet, config: ModelConfig) -> tuple[RuleSet, ModelConfig]:
        for key in keys:
            rules = shift_growth_temperature(rules, key, delta_c)
        return rules, config

    return apply


def _prior(rules: RuleSet, config: ModelConfig) -> tuple[RuleSet, ModelConfig]:
    return rules, config


PORCINI = ["porcini_edulis", "porcini_reticulatus", "porcini_aereus", "porcini_pinophilus"]
OVOLI = ["ovoli_caesarea"]
GALLINACCI = ["gallinacci_cibarius"]
ON, OFF = {"enabled": True}, {"enabled": False}

SEARCH: list[Choice] = [
    Choice(
        "rain_scale",
        ["porcini", "ovoli", "gallinacci"],
        [
            Change("prior", _prior),
            Change("raw", lambda r, c: (r, set_precipitation_scale(c, False))),
        ],
    ),
    # --- porcini (the four keys share the rain logic) ---
    Choice(
        "porcini_rain_amount",
        ["porcini"],
        [
            Change("prior", _prior),
            Change(
                "lower",
                _factors(
                    PORCINI, {"rain_trigger": {"response": {"amount_mm": [5, 20, None, None]}}}
                ),
            ),
            Change(
                "higher",
                _factors(
                    PORCINI, {"rain_trigger": {"response": {"amount_mm": [15, 45, None, None]}}}
                ),
            ),
        ],
    ),
    Choice(
        "porcini_lag",
        ["porcini"],
        [
            Change("prior", _prior),
            Change(
                "earlier",
                _factors(PORCINI, {"rain_trigger": {"response": {"lag_days": [4, 7, 13, 20]}}}),
            ),
            Change(
                "later",
                _factors(PORCINI, {"rain_trigger": {"response": {"lag_days": [8, 12, 20, 28]}}}),
            ),
        ],
    ),
    Choice(
        "porcini_water_balance",
        ["porcini"],
        [
            Change("prior", _prior),
            Change("water_balance", _factors(PORCINI, {"rain_30d": OFF, "water_balance_30d": ON})),
        ],
    ),
    Choice(
        "porcini_trigger_weight",
        ["porcini"],
        [
            Change("prior", _prior),
            Change("equal", _factors(PORCINI, {"rain_trigger": {"weight": 1}})),
        ],
    ),
    Choice(
        "porcini_soil_temperature",
        ["porcini"],
        [
            Change("prior", _prior),
            Change(
                "soil",
                _factors(["porcini_edulis"], {"air_temperature": OFF, "soil_temperature": ON}),
            ),
        ],
    ),
    Choice(
        "porcini_drying",
        ["porcini"],
        [Change("prior", _prior), Change("off", _factors(PORCINI, {"drying": OFF}))],
    ),
    Choice(
        "porcini_frost",
        ["porcini"],
        [
            Change("prior", _prior),
            Change("off", _factors(PORCINI, {"frost": OFF, "cold_nights": OFF})),
        ],
    ),
    Choice(
        "porcini_heat_spike",
        ["porcini"],
        [Change("prior", _prior), Change("off", _factors(PORCINI, {"heat_spike": OFF}))],
    ),
    # --- ovoli ---
    Choice(
        "ovoli_lag",
        ["ovoli"],
        [
            Change("prior", _prior),
            Change(
                "later",
                _factors(OVOLI, {"rain_trigger": {"response": {"lag_days": [10, 15, 24, 32]}}}),
            ),
        ],
    ),
    Choice(
        "ovoli_temperature",
        ["ovoli"],
        [
            Change("prior", _prior),
            Change("air", _factors(OVOLI, {"soil_temperature": OFF, "air_temperature": ON})),
        ],
    ),
    Choice(
        "ovoli_trigger_weight",
        ["ovoli"],
        [
            Change("prior", _prior),
            Change("double", _factors(OVOLI, {"rain_trigger": {"weight": 2}})),
        ],
    ),
    Choice(
        "ovoli_evaporative_demand",
        ["ovoli"],
        [Change("prior", _prior), Change("off", _factors(OVOLI, {"evaporative_demand": OFF}))],
    ),
    Choice(
        "ovoli_cold_nights",
        ["ovoli"],
        [Change("prior", _prior), Change("off", _factors(OVOLI, {"cold_nights": OFF}))],
    ),
    Choice(
        "ovoli_frost",
        ["ovoli"],
        [Change("prior", _prior), Change("off", _factors(OVOLI, {"frost": OFF}))],
    ),
    # --- gallinacci ---
    Choice(
        "gallinacci_temperature",
        ["gallinacci"],
        [
            Change("prior", _prior),
            Change("air", _factors(GALLINACCI, {"soil_temperature": OFF, "air_temperature": ON})),
        ],
    ),
    Choice(
        "gallinacci_lag",
        ["gallinacci"],
        [
            Change("prior", _prior),
            Change(
                "shorter",
                _factors(GALLINACCI, {"rain_trigger": {"response": {"lag_days": [4, 8, 20, 35]}}}),
            ),
        ],
    ),
    Choice(
        "gallinacci_water_balance_60d",
        ["gallinacci"],
        [Change("prior", _prior), Change("off", _factors(GALLINACCI, {"water_balance_60d": OFF}))],
    ),
    Choice(
        "gallinacci_drought_14d",
        ["gallinacci"],
        [Change("prior", _prior), Change("off", _factors(GALLINACCI, {"drought_14d": OFF}))],
    ),
    Choice(
        "gallinacci_heat",
        ["gallinacci"],
        [
            Change("prior", _prior),
            Change("vpd", _factors(GALLINACCI, {"heat": OFF, "heat_vpd": ON})),
            Change("off", _factors(GALLINACCI, {"heat": OFF})),
        ],
    ),
    Choice(
        "gallinacci_cold",
        ["gallinacci"],
        [
            Change("prior", _prior),
            Change("off", _factors(GALLINACCI, {"frost": OFF, "hard_frost": OFF, "snow": OFF})),
        ],
    ),
    Choice(
        "gallinacci_drying",
        ["gallinacci"],
        [Change("prior", _prior), Change("off", _factors(GALLINACCI, {"drying": OFF}))],
    ),
]


# --- the rain drivers (card tune-rain-drivers-saturate) ------------------------------------------
#
# Fixed before the train seasons were scored with the rules of 2026-09-22. Both rain drivers reach
# full credit in an ordinary September (model-v1-validation.md), so each group tries its trigger
# ramp and its 30-day ramp raised by half and doubled, and a 30-day driver relative to the cell's
# own normal (0 at 50 %, full from 125 %, the outlook's "wetter"), which an ordinary month cannot
# fill. Then the growth clock's temperatures 3 °C cooler and warmer, and gallinacci's shade line
# (GAL-07) off, which the engine applies all year though its source limits it to June-September.
# Run once with the rain scale as configured and once without (``--rain-scale off``): the scale
# lowers the raw rain a threshold needs by 22 % at sea level to 43 % at 1.7 km.


def _relative_30d() -> dict:
    return {
        "input": {"aggregate": "percent_of_normal"},
        "response": {"trapezoid": [50, 125, None, None]},
    }


def _rain_choices(group: str, keys: list[str], trigger: list, rain_30d: list) -> list[Choice]:
    """Trigger and 30-day ramps as ``[prior, x1.5, x2]`` lower and full edges."""

    def amount(edges: tuple[float, float]) -> dict:
        return {"rain_trigger": {"response": {"amount_mm": [*edges, None, None]}}}

    def month(edges: tuple[float, float]) -> dict:
        return {"rain_30d": {"response": {"trapezoid": [*edges, None, None]}}}

    return [
        Choice(
            f"{group}_trigger_amount",
            [group],
            [
                Change("prior", _prior),
                Change("higher", _factors(keys, amount(trigger[1]))),
                Change("much_higher", _factors(keys, amount(trigger[2]))),
            ],
        ),
        Choice(
            f"{group}_rain_30d",
            [group],
            [
                Change("prior", _prior),
                Change("higher", _factors(keys, month(rain_30d[1]))),
                Change("much_higher", _factors(keys, month(rain_30d[2]))),
                Change("relative", _factors(keys, {"rain_30d": _relative_30d()})),
            ],
        ),
        Choice(
            f"{group}_clock_temperature",
            [group],
            [
                Change("prior", _prior),
                Change("cooler", _clock(keys, -3)),
                Change("warmer", _clock(keys, 3)),
            ],
        ),
    ]


RAIN_SEARCH: list[Choice] = [
    *_rain_choices(
        "porcini", PORCINI, [(10, 30), (15, 45), (20, 60)], [(20, 80), (30, 120), (40, 160)]
    ),
    *_rain_choices(
        "ovoli", OVOLI, [(10, 30), (15, 45), (20, 60)], [(25, 75), (40, 110), (50, 150)]
    ),
    *_rain_choices(
        "gallinacci", GALLINACCI, [(10, 20), (15, 30), (20, 40)], [(15, 70), (25, 105), (30, 140)]
    ),
    Choice(
        "gallinacci_sun_exposure",
        ["gallinacci"],
        [Change("prior", _prior), Change("off", _factors(GALLINACCI, {"sun_exposure": OFF}))],
    ),
]

SEARCHES = {"v1": SEARCH, "rain": RAIN_SEARCH}


@dataclass
class TuningResult:
    rules: RuleSet
    config: ModelConfig
    kept: dict[str, str]
    objective: dict[str, float]
    trials: list[dict] = field(default_factory=list)


def _mean(scores: dict[str, float], groups: list[str]) -> float:
    values = [scores[g] for g in groups if g in scores]
    return sum(values) / len(values) if values else float("nan")


def coordinate_descent(
    search: list[Choice],
    rules: RuleSet,
    config: ModelConfig,
    evaluate: Evaluate,
    margin: float = MARGIN,
    log: Callable[[str], None] = lambda message: None,
) -> TuningResult:
    """One pass over ``search``: keep an alternative only if it beats the current state by
    ``margin`` on the mean objective of the choice's groups."""
    every_group = sorted({g for choice in search for g in choice.groups})
    trail: list[str] = []
    current = evaluate(rules, config, every_group, trail)
    result = TuningResult(rules=rules, config=config, kept={}, objective=dict(current))
    if search:
        result.trials.append({"choice": search[0].name, "option": "prior", **current})
    log(f"start: {current}")
    for choice in search:
        result.kept[choice.name] = "prior"
        best, best_state = _mean(result.objective, choice.groups), None
        for option in choice.options[1:]:
            candidate_rules, candidate_config = option.apply(result.rules, result.config)
            scores = evaluate(
                candidate_rules, candidate_config, choice.groups, [*trail, option.label]
            )
            result.trials.append({"choice": choice.name, "option": option.label, **scores})
            gain = _mean(scores, choice.groups) - _mean(result.objective, choice.groups)
            log(f"{choice.name}={option.label}: {scores} (gain {gain:+.3f})")
            if gain >= margin and _mean(scores, choice.groups) > best:
                best = _mean(scores, choice.groups)
                best_state = (option, candidate_rules, candidate_config, scores)
        if best_state is not None:
            option, result.rules, result.config, scores = best_state
            result.kept[choice.name] = option.label
            result.objective.update(scores)
            trail.append(option.label)
            log(f"kept {choice.name}={option.label}")
    return result


def backtest_evaluator(region: str, seasons: list[int], data_root: Path | None = None) -> Evaluate:
    """Score the train seasons for a rule variant and return each group's objective."""
    prepared: dict[bool, object] = {}

    def evaluate(rules: RuleSet, config: ModelConfig, groups: list[str], trail: list[str]):
        enabled = config.precipitation_scale.enabled
        if enabled not in prepared:
            prepared[enabled] = prepare(region, seasons, data_root, config)
        subset = RuleSet(
            species={k: v for k, v in rules.species.items() if v.group in groups},
            groups={g: keys for g, keys in rules.groups.items() if g in groups},
            references=rules.references,
        )
        _, summary, _ = run(prepared[enabled], subset, seasons)
        return {group: objective(summary, group) for group in groups}

    return evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--label", required=True)
    parser.add_argument("--region", default="tuscany")
    parser.add_argument("--search", choices=sorted(SEARCHES), default="v1")
    parser.add_argument(
        "--rain-scale",
        choices=["config", "off"],
        default="config",
        help="start from the rain scale as configured, or with it off",
    )
    args = parser.parse_args()
    started = time.monotonic()

    def log(message: str) -> None:
        print(f"[{time.monotonic() - started:7.1f}s] {message}", flush=True)

    config = load_model_config()
    if args.rain_scale == "off":
        config = set_precipitation_scale(config, False)
    seasons = config.backtest.train_seasons
    result = coordinate_descent(
        SEARCHES[args.search],
        load_rules(),
        config,
        backtest_evaluator(args.region, seasons),
        log=log,
    )
    out = data_dir() / "backtest" / args.region / args.label
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(result.trials).to_csv(out / "trials.csv", index=False)
    (out / "tuning.json").write_text(
        json.dumps(
            {
                "margin": MARGIN,
                "search": args.search,
                "rain_scale": config.precipitation_scale.enabled,
                "seasons": seasons,
                "kept": result.kept,
                "objective": result.objective,
            },
            indent=2,
        )
        + "\n"
    )
    log(f"kept: {result.kept}")


if __name__ == "__main__":
    main()
