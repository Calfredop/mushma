"""Fixture scoring math: a compact stand-in for the M3 rule engine.

Mirrors the shape of the real per-species rule config in
`.gavin-root/docs/species-rules/` (factor id, role, i18n_key, weight, and the
[a, b, c, d] trapezoid response) closely enough that the fixture "why this
score" breakdown looks like what the real engine will eventually produce.
This module does not read those YAML files -- it is illustrative fixture
data, not the model.

score = product(gate values) * product(stopper values)
        * weighted_geometric_mean(driver values, driver weights)

Each factor's `contribution` is its own multiplicative share of that score
(a gate/stopper contributes its raw value; a driver contributes
value ** (weight / total_driver_weight)), so
`math.prod(contribution for all factors) == score`.
"""

from dataclasses import dataclass
from datetime import date
from typing import Literal

from api.species import Species

Trapezoid = tuple[float | None, float | None, float | None, float | None]
Role = Literal["gate", "driver", "stopper"]


def trapezoid(x: float, params: Trapezoid) -> float:
    """0 outside [a, d], linear ramps a->b and c->d, 1 on [b, c].

    A null (a, b) pair opens the shape to -inf (1 for every x <= c); a null
    (c, d) pair opens it to +inf (1 for every x >= b). Both null means "always 1".
    """
    a, b, c, d = params
    lower_open = a is None and b is None
    upper_open = c is None and d is None

    if not lower_open:
        assert a is not None and b is not None
        if x <= a:
            return 0.0
        if x < b:
            return (x - a) / (b - a)
    if not upper_open:
        assert c is not None and d is not None
        if x >= d:
            return 0.0
        if x > c:
            return (d - x) / (d - c)
    return 1.0


def _ddmm_to_day_of_year(ddmm: str) -> float:
    day, month = (int(part) for part in ddmm.split("-"))
    return date(2001, month, day).timetuple().tm_yday  # 2001: non-leap reference year


# Single-window approximation of the PRD's per-species ecology (Model table);
# the real per-key rules in species-rules/*.yaml use several sub-species
# windows combined by max. [zero_below, full_from, full_to, zero_above].
_SEASON_WINDOWS_DDMM: dict[Species, Trapezoid] = {
    "porcini": ("15-04", "15-05", "15-11", "20-12"),
    "ovoli": ("15-06", "15-07", "15-10", "15-11"),
    "gallinacci": ("15-05", "15-06", "31-10", "30-11"),
}
SEASON_WINDOWS: dict[Species, Trapezoid] = {
    species: tuple(  # type: ignore[misc]
        None if part is None else _ddmm_to_day_of_year(part) for part in ddmm_window
    )
    for species, ddmm_window in _SEASON_WINDOWS_DDMM.items()
}


def season_gate(species: Species, target: date) -> float:
    return trapezoid(target.timetuple().tm_yday, SEASON_WINDOWS[species])


# Elevation bands (metres), trimmed from the PRD ecology table and the drafted
# species-rules altitude factors.
ALTITUDE_TRAPEZOID: dict[Species, Trapezoid] = {
    "porcini": (200.0, 700.0, 1600.0, 1900.0),
    "ovoli": (0.0, 100.0, 700.0, 1000.0),
    "gallinacci": (0.0, 50.0, 1300.0, 1700.0),
}

# Habitat affinity, trimmed from species-rules/*.yaml's habitat factor tables.
HABITAT_AFFINITY: dict[Species, dict[str, float]] = {
    "porcini": {
        "beech": 1.0,
        "chestnut": 0.9,
        "fir_spruce": 0.9,
        "mixed_broadleaf_conifer": 0.8,
        "mountain_pine": 0.5,
        "deciduous_oak": 0.5,
        "mixed_broadleaf": 0.4,
        "other_conifer": 0.3,
        "evergreen_oak": 0.2,
        "mediterranean_pine": 0.2,
        "macchia": 0.1,
        "riparian": 0.1,
        "transitional_woodland_shrub": 0.3,
        "exotic_broadleaf": 0.05,
    },
    "ovoli": {
        "deciduous_oak": 1.0,
        "evergreen_oak": 0.9,
        "chestnut": 0.8,
        "mixed_broadleaf": 0.4,
        "mixed_broadleaf_conifer": 0.2,
        "transitional_woodland_shrub": 0.15,
        "macchia": 0.1,
    },
    "gallinacci": {
        "mixed_broadleaf_conifer": 1.0,
        "fir_spruce": 0.9,
        "chestnut": 0.8,
        "beech": 0.8,
        "mountain_pine": 0.7,
        "mixed_broadleaf": 0.6,
        "other_conifer": 0.6,
        "deciduous_oak": 0.4,
        "evergreen_oak": 0.3,
        "transitional_woodland_shrub": 0.3,
    },
}
HABITAT_AFFINITY_DEFAULT: dict[Species, float] = {
    "porcini": 0.0,
    "ovoli": 0.05,
    "gallinacci": 0.2,
}


@dataclass(frozen=True)
class FactorSpec:
    id: str
    role: Role
    i18n_key: str
    weight: float | None = None  # required iff role == "driver"

    def __post_init__(self) -> None:
        if self.role == "driver" and self.weight is None:
            raise ValueError(f"driver factor {self.id!r} needs a weight")
        if self.role != "driver" and self.weight is not None:
            raise ValueError(f"non-driver factor {self.id!r} must not have a weight")


@dataclass(frozen=True)
class FactorResult:
    key: str
    i18n_key: str
    value: float
    contribution: float


# Trimmed, illustrative subsets of the real per-species factor lists in
# species-rules/*.yaml (ids and i18n keys match; parameters are fixture-only).
FACTOR_SPECS: dict[Species, list[FactorSpec]] = {
    "porcini": [
        FactorSpec(id="season", role="gate", i18n_key="factor.season"),
        FactorSpec(id="habitat", role="gate", i18n_key="factor.habitat"),
        FactorSpec(id="altitude", role="gate", i18n_key="factor.altitude"),
        FactorSpec(id="rain_trigger", role="driver", i18n_key="factor.rain_trigger", weight=2.0),
        FactorSpec(id="rain_30d", role="driver", i18n_key="factor.rain_30d", weight=1.0),
        FactorSpec(
            id="air_temperature", role="driver", i18n_key="factor.air_temperature", weight=1.0
        ),
        FactorSpec(id="frost", role="stopper", i18n_key="factor.frost"),
        FactorSpec(id="drying", role="stopper", i18n_key="factor.drying"),
    ],
    "ovoli": [
        FactorSpec(id="season", role="gate", i18n_key="factor.season"),
        FactorSpec(id="habitat", role="gate", i18n_key="factor.habitat"),
        FactorSpec(id="altitude", role="gate", i18n_key="factor.altitude"),
        FactorSpec(id="rain_trigger", role="driver", i18n_key="factor.rain_trigger", weight=2.0),
        FactorSpec(id="rain_30d", role="driver", i18n_key="factor.rain_30d", weight=1.0),
        FactorSpec(
            id="air_temperature", role="driver", i18n_key="factor.air_temperature", weight=1.0
        ),
        FactorSpec(id="evaporative_demand", role="stopper", i18n_key="factor.drying"),
        FactorSpec(id="frost", role="stopper", i18n_key="factor.frost"),
    ],
    "gallinacci": [
        FactorSpec(id="season", role="gate", i18n_key="factor.season"),
        FactorSpec(id="habitat", role="gate", i18n_key="factor.habitat"),
        FactorSpec(id="altitude", role="gate", i18n_key="factor.altitude"),
        FactorSpec(id="rain_30d", role="driver", i18n_key="factor.rain_30d", weight=1.5),
        FactorSpec(id="rain_trigger", role="driver", i18n_key="factor.rain_trigger", weight=1.0),
        FactorSpec(
            id="air_temperature", role="driver", i18n_key="factor.air_temperature", weight=1.0
        ),
        FactorSpec(id="drought_14d", role="stopper", i18n_key="factor.drought"),
        FactorSpec(id="frost", role="stopper", i18n_key="factor.frost"),
    ],
}


def combine_factors(
    specs: list[FactorSpec], values: dict[str, float]
) -> tuple[float, list[FactorResult]]:
    driver_weight_total = sum(spec.weight or 0.0 for spec in specs if spec.role == "driver")
    score = 1.0
    results: list[FactorResult] = []
    for spec in specs:
        value = values[spec.id]
        if spec.role == "driver":
            assert spec.weight is not None
            contribution = value ** (spec.weight / driver_weight_total)
        else:
            contribution = value
        score *= contribution
        results.append(
            FactorResult(
                key=spec.id, i18n_key=spec.i18n_key, value=value, contribution=contribution
            )
        )
    return score, results
