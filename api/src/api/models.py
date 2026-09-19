"""API response contract. See PRD -> Principles (Honest uncertainty, Sightings
privacy) and AGENTS.md -> Conventions (Score wording, Rules are data)."""

from datetime import date, datetime
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


class StatusResponse(BaseModel):
    """Data freshness, for the frontend's "last updated" and stale-data warning (M7)."""

    scored_through: date = Field(description="the latest day the pipeline has scored")
    updated_at: datetime | None = Field(
        description="when the scores were last (re)generated; null before the first pipeline run"
    )
    rules_version: str | None = Field(
        description="the species rule config's version stamp; null before the first pipeline run"
    )


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


# --- Time views (M6): history and seasonal outlook ---------------------------------------------
# A "good day" is a cell-day whose conditions score reaches `good_score`; area values are a typical
# woodland cell's (see .gavin-root/docs/time-views.md). Counts of past years, never chances.


class Area(BaseModel):
    code: str | None = Field(description="ISTAT comune code; null for the whole region")
    name: str
    kind: Literal["region", "comune"]


class Comune(BaseModel):
    code: str
    name: str
    province: str
    lon: float
    lat: float
    cells: int = Field(ge=1, description="woodland cells in the comune")


class ComuniResponse(BaseModel):
    comuni: list[Comune]


class RainStat(BaseModel):
    total_mm: float = Field(ge=0)
    normal_mm: float = Field(ge=0)


class TemperatureStat(BaseModel):
    mean_c: float
    normal_c: float


class SeasonWindow(BaseModel):
    """The span of the species' season windows in its rule files, for one year."""

    start: date
    end: date


class Baseline(BaseModel):
    weather_years: list[int] = Field(description="years behind the weather normals")
    score_years: list[int] = Field(description="seasons behind the typical good days")


class MonthStat(BaseModel):
    month: int = Field(ge=1, le=12)
    good_days: float = Field(ge=0, description="a typical woodland cell's good days")
    rain: RainStat | None
    temperature: TemperatureStat | None
    sightings: int = Field(ge=0)


class SeasonSummary(BaseModel):
    year: int
    complete: bool = Field(description="every day of the year is scored")
    through: date = Field(description="the last day scored")
    good_days: float = Field(ge=0, description="a typical woodland cell's good days")
    good_days_typical: float | None = Field(
        description="median over the baseline seasons, to the same day of the year"
    )
    peak_date: date | None
    peak_share: float = Field(ge=0, le=1, description="share of woodland cells good that day")
    window: SeasonWindow
    rain: RainStat | None = Field(description="over the observed days of the window")
    temperature: TemperatureStat | None
    weather_through: date | None = Field(description="the last observed day behind the weather")
    sightings: int = Field(ge=0)
    months: list[MonthStat]


class SeasonsResponse(BaseModel):
    species: SpeciesOrCombined
    area: Area
    good_score: float = Field(gt=0, le=1)
    baseline: Baseline
    seasons: list[SeasonSummary]


class CellSeason(BaseModel):
    cell_id: str
    lon: float
    lat: float
    good_days: int = Field(ge=0)


class ComuneSeason(BaseModel):
    code: str
    name: str
    good_days: float = Field(ge=0)
    good_days_typical: float | None
    rain: RainStat | None
    temperature: TemperatureStat | None
    sightings: int = Field(ge=0)


class SeasonMapResponse(BaseModel):
    """One season on the map: good days per woodland cell, and the comuni ranked by them."""

    year: int
    species: SpeciesOrCombined
    complete: bool
    through: date
    good_score: float = Field(gt=0, le=1)
    cells: list[CellSeason]
    comuni: list[ComuneSeason]


class SeasonToDate(BaseModel):
    through: date
    good_days: float = Field(ge=0)
    good_days_typical: float | None
    rain: RainStat | None
    temperature: TemperatureStat | None
    weather_through: date | None
    sightings: int = Field(ge=0)


class OutlookPeriod(BaseModel):
    """A week (EC46) or month (SEAS5) after the 7-day forecast. An outlook, not a forecast."""

    start: date
    end: date
    kind: Literal["week", "month"]
    past_good_years: int = Field(ge=0, description="past seasons in which these days were good")
    past_years: int = Field(ge=0, description="past seasons with scores for these days")
    rain: RainStat | None = Field(description="long-range forecast total and its own normal")
    temperature_anomaly_c: float | None
    lead_rain_pct: float | None = Field(
        ge=0, description="rain over the lead window, as a percentage of normal"
    )
    outlook: Literal["better", "usual", "worse", "unknown"]


class RainLead(BaseModel):
    min_days: int = Field(ge=0)
    max_days: int = Field(ge=0)


class RainTiltBands(BaseModel):
    """Lead-window rain at or above ``wetter_pct`` of normal tilts a period better; at or below
    ``drier_pct``, worse (``config/history.yaml``)."""

    wetter_pct: float = Field(gt=100)
    drier_pct: float = Field(gt=0, lt=100)


class OutlookResponse(BaseModel):
    species: Species
    area: Area
    issued: date | None = Field(description="when the long-range forecast was fetched")
    good_share: float = Field(gt=0, le=1)
    rain_lead: RainLead
    rain_tilt: RainTiltBands
    baseline: Baseline
    window: SeasonWindow
    season_to_date: SeasonToDate | None
    periods: list[OutlookPeriod]
