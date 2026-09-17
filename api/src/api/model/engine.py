"""Score species keys, roll them up into groups, and combine the groups.

For one cell, species key and day (see ``config/species/README.md``)::

    score = Π gates  ×  Π stoppers  ×  exp( Σ_d w_d · ln f_d  /  Σ_d w_d )

Each factor's ``contribution`` is its own multiplicative share of the score: a gate's or
stopper's value, a driver's ``value ** (w / Σ w)``. Their product is the score, so the "why this
score" UI can split the shortfall between factors without knowing the formula.

A **group** (the UI species) scores the max over its keys, with the winning key's breakdown; on a
tie the key listed first wins. The **combined** score is the max over the groups in season, with
the winning group's breakdown; no group in season means 0 and no breakdown.
"""

from dataclasses import dataclass
from datetime import date

import numpy as np

from api.model.arrays import Cells, Weather
from api.model.factors import evaluate, lookback_days
from api.model.rules import Factor, SpeciesRules

COMBINED = "combined"


@dataclass(frozen=True)
class FactorContribution:
    """One line of the "why this score" breakdown."""

    key: str
    i18n_key: str
    role: str
    value: float
    contribution: float
    weight: float | None = None
    input: float | None = None
    days_ago: int | None = None


@dataclass(frozen=True)
class FactorScores:
    factor: Factor
    value: np.ndarray  # (cells, days)
    contribution: np.ndarray  # (cells, days)
    input: np.ndarray | None = None
    days_ago: np.ndarray | None = None

    def at(self, i: int, j: int) -> FactorContribution:
        def scalar(array: np.ndarray | None) -> float | None:
            if array is None or np.isnan(array[i, j]):
                return None
            return float(array[i, j])

        days_ago = scalar(self.days_ago)
        return FactorContribution(
            key=self.factor.id,
            i18n_key=self.factor.i18n_key,
            role=self.factor.role,
            value=float(self.value[i, j]),
            contribution=float(self.contribution[i, j]),
            weight=self.factor.weight,
            input=scalar(self.input),
            days_ago=None if days_ago is None else int(days_ago),
        )


@dataclass(frozen=True)
class SpeciesScores:
    key: str
    group: str
    cell_ids: np.ndarray  # (cells,)
    dates: np.ndarray  # (days,) datetime64[D]
    score: np.ndarray  # (cells, days), NaN where the weather is missing
    factors: list[FactorScores]  # breakdown order: gates, drivers, stoppers
    in_season: np.ndarray  # (cells, days) bool: every season gate is open
    forecast: np.ndarray | None = None  # (cells, days) bool

    def breakdown(self, i: int, j: int) -> list[FactorContribution]:
        return [f.at(i, j) for f in self.factors]

    def factor(self, factor_id: str) -> FactorScores:
        return next(f for f in self.factors if f.factor.id == factor_id)


def required_lookback(rules: SpeciesRules) -> int:
    """Days of weather needed before the first target day."""
    return max(lookback_days(f) for f in rules.enabled_factors)


def score_species(
    rules: SpeciesRules, cells: Cells, weather: Weather, start: date, end: date | None = None
) -> SpeciesScores:
    """Score every cell for every day from ``start`` to ``end`` (inclusive, default ``start``)."""
    end = end or start
    first, last = weather.index_of(np.datetime64(start)), weather.index_of(np.datetime64(end))
    needed = required_lookback(rules)
    if first < needed:
        raise ValueError(
            f"{rules.key}: scoring {start} needs {needed} days of lookback weather, "
            f"but the weather starts {first} days before"
        )
    targets = slice(first, last + 1)
    enabled = rules.enabled_factors
    total_weight = sum(f.weight for f in enabled if f.role == "driver")

    shape = (len(cells), last + 1 - first)
    score = np.ones(shape)
    in_season = np.ones(shape, dtype=bool)
    factors = []
    for factor in enabled:
        result = evaluate(factor, cells, weather, targets)
        value = result.value
        if factor.role == "driver":
            contribution = np.power(value, factor.weight / total_weight)
        else:
            contribution = value
        score = score * contribution
        if factor.kind == "season_window":
            in_season &= np.nan_to_num(value) > 0
        factors.append(FactorScores(factor, value, contribution, result.input, result.days_ago))

    return SpeciesScores(
        key=rules.key,
        group=rules.group,
        cell_ids=cells.ids,
        dates=weather.dates[targets],
        score=score,
        factors=factors,
        in_season=in_season,
        forecast=None if weather.forecast is None else weather.forecast[:, targets],
    )


@dataclass(frozen=True)
class GroupScores:
    key: str
    members: list[SpeciesScores]  # tie-break order
    score: np.ndarray  # (cells, days)
    winner_index: np.ndarray  # (cells, days) index into members
    in_season: np.ndarray  # (cells, days): any member in season

    @property
    def cell_ids(self) -> np.ndarray:
        return self.members[0].cell_ids

    @property
    def dates(self) -> np.ndarray:
        return self.members[0].dates

    def winner(self, i: int, j: int) -> SpeciesScores:
        return self.members[int(self.winner_index[i, j])]

    def breakdown(self, i: int, j: int) -> list[FactorContribution]:
        return self.winner(i, j).breakdown(i, j)


def group_scores(key: str, members: list[SpeciesScores]) -> GroupScores:
    """Max over the members, which must cover the same cells and days."""
    stacked = np.stack([m.score for m in members])
    winner = np.argmax(np.nan_to_num(stacked, nan=-1.0), axis=0)
    score = np.take_along_axis(stacked, winner[np.newaxis], axis=0)[0]
    return GroupScores(
        key=key,
        members=members,
        score=score,
        winner_index=winner,
        in_season=np.logical_or.reduce([m.in_season for m in members]),
    )


@dataclass(frozen=True)
class CombinedScores:
    groups: list[GroupScores]  # tie-break order
    score: np.ndarray  # (cells, days)
    winner_index: np.ndarray  # (cells, days) index into groups, -1 when none is in season
    key: str = COMBINED

    @property
    def cell_ids(self) -> np.ndarray:
        return self.groups[0].cell_ids

    @property
    def dates(self) -> np.ndarray:
        return self.groups[0].dates

    def winning_group(self, i: int, j: int) -> str | None:
        index = int(self.winner_index[i, j])
        return None if index < 0 else self.groups[index].key

    def breakdown(self, i: int, j: int) -> list[FactorContribution]:
        index = int(self.winner_index[i, j])
        return [] if index < 0 else self.groups[index].breakdown(i, j)


def combine_groups(groups: list[GroupScores]) -> CombinedScores:
    """Max over the groups in season; 0 with no winner where none is."""
    scores = np.stack([g.score for g in groups])
    in_season = np.stack([g.in_season for g in groups])
    candidates = np.where(in_season & ~np.isnan(scores), scores, -1.0)
    winner = np.argmax(candidates, axis=0)
    best = np.take_along_axis(candidates, winner[np.newaxis], axis=0)[0]
    none_in_season = best < 0
    score = np.where(none_in_season, 0.0, best)
    score[np.isnan(scores).all(axis=0)] = np.nan
    return CombinedScores(
        groups=groups, score=score, winner_index=np.where(none_in_season, -1, winner)
    )
