"""Turns a fixture cell into a deterministic score + factor breakdown.

Gates (season, habitat, altitude) come from the cell's static attributes and
the tables in `scoring.py`. Drivers and stoppers stand in for weather with a
deterministic smooth wave (hashed per cell/species/factor, so it never
changes between requests) rather than real rain and temperature history --
there is no pipeline yet (M2/M3). It just needs to look, and stay, plausible.
"""

import hashlib
import math
from dataclasses import replace
from datetime import date

from api.fixtures.cells import CellSpec
from api.fixtures.scoring import (
    ALTITUDE_TRAPEZOID,
    FACTOR_SPECS,
    HABITAT_AFFINITY,
    HABITAT_AFFINITY_DEFAULT,
    FactorResult,
    FactorSpec,
    combine_factors,
    measure,
    rule_for,
    season_gate,
    trapezoid,
)
from api.species import SPECIES, Species

# 6 days back, today, 7 days ahead -- PRD Feature 1 (date control) and Feature 2
# (spot forecast: today + 7-day outlook).
WINDOW_OFFSETS: range = range(-6, 8)


def _unit_hash(*parts: str) -> float:
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF  # deterministic value in [0, 1)


def _smooth_wave(
    cell_id: str,
    species: Species,
    factor_id: str,
    day_offset: int,
    *,
    base: float,
    amplitude: float,
    period: float,
) -> float:
    phase = _unit_hash(cell_id, species, factor_id) * period
    raw = base + amplitude * math.sin(2 * math.pi * (day_offset + phase) / period)
    return min(1.0, max(0.0, raw))


def _factor_value(
    spec: FactorSpec, cell: CellSpec, species: Species, target_date: date, day_offset: int
) -> float:
    if spec.id == "season":
        return season_gate(species, target_date)
    if spec.id == "habitat":
        return HABITAT_AFFINITY[species].get(cell.habitat, HABITAT_AFFINITY_DEFAULT[species])
    if spec.id == "altitude":
        return trapezoid(cell.elevation_m, ALTITUDE_TRAPEZOID[species])
    if spec.role == "stopper":
        return _smooth_wave(
            cell.id, species, spec.id, day_offset, base=0.6, amplitude=0.4, period=9.0
        )
    return _smooth_wave(cell.id, species, spec.id, day_offset, base=0.5, amplitude=0.4, period=13.0)


def score_and_factors(
    cell: CellSpec, species: Species, target_date: date, day_offset: int
) -> tuple[float, list[FactorResult]]:
    specs = FACTOR_SPECS[species]
    values, measured = {}, {}
    for spec in specs:
        rule = rule_for(species, spec.id)
        value, input_, days_ago = measure(
            rule, _factor_value(spec, cell, species, target_date, day_offset), cell.elevation_m
        )
        values[spec.id] = value
        measured[spec.id] = (rule, input_, days_ago)
    score, results = combine_factors(specs, values)
    return score, [
        replace(
            result,
            rule=measured[result.key][0],
            input=measured[result.key][1],
            unit=measured[result.key][0].input_unit,
            days_ago=measured[result.key][2],
        )
        for result in results
    ]


def combined_score(cell: CellSpec, target_date: date, day_offset: int) -> float:
    """PRD -> Model: the combined score is the max across species (v1 default)."""
    return max(score_and_factors(cell, species, target_date, day_offset)[0] for species in SPECIES)
