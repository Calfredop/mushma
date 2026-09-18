"""API response contract. See PRD -> Principles (Honest uncertainty, Sightings
privacy) and AGENTS.md -> Conventions (Score wording, Rules are data)."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

from api.species import Species, SpeciesOrCombined


class Place(BaseModel):
    comune: str
    nearest_place: str


class FactorBreakdown(BaseModel):
    """One rule's contribution to a score, in evaluation order (gates, then
    drivers, then stoppers) -- the "why this score" breakdown never re-sorts
    by magnitude, so the same species always reads in the same order.

    `contribution` is this factor's own multiplicative share of the day's
    score: the product of every factor's `contribution` equals `score`.
    """

    key: str
    i18n_key: str
    value: float = Field(ge=0, le=1)
    contribution: float = Field(ge=0, le=1)


class DayScore(BaseModel):
    date: date
    score: float = Field(ge=0, le=1, description="0-1 conditions index, never a probability")
    factors: list[FactorBreakdown]


class SpeciesForecast(BaseModel):
    species: Species
    days: list[DayScore]


class GridCellScore(BaseModel):
    cell_id: str
    lon: float
    lat: float
    score: float = Field(ge=0, le=1)


class ScoresResponse(BaseModel):
    species: SpeciesOrCombined
    date: date
    cells: list[GridCellScore]


class CellDetailResponse(BaseModel):
    """Shared shape for `GET /spot` and `GET /cells/{id}`: today plus a
    7-day outlook, per species, with the full factor breakdown."""

    cell_id: str
    lon: float
    lat: float
    place: Place
    species: list[SpeciesForecast]


class Hotspot(BaseModel):
    id: str
    place: Place
    lon: float
    lat: float
    score: float = Field(ge=0, le=1)
    cell_ids: list[str]
    recent_sightings: int = Field(ge=0)


class HotspotsResponse(BaseModel):
    species: SpeciesOrCombined
    date: date
    hotspots: list[Hotspot]


class SightingCount(BaseModel):
    """Never coordinates (PRD -> Principles -> Sightings privacy): a count per
    cell, source and license."""

    cell_id: str
    source: Literal["gbif", "inaturalist"]
    license: str
    count: int = Field(ge=1)


class SightingsResponse(BaseModel):
    species: Species
    since: date
    counts: list[SightingCount]
