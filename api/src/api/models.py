"""API response contract. See PRD -> Principles (Honest uncertainty, Sightings
privacy) and AGENTS.md -> Conventions (Score wording, Rules are data)."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from api.species import Species, SpeciesOrCombined


class Place(BaseModel):
    comune: str
    nearest_place: str


class FactorRule(BaseModel):
    """What a rule asked of the measurement (`config/species/*.yaml`), so the copy can say what it
    wanted. Which fields are set follows `kind`: a season window or habitat has none of them.
    """

    kind: Literal[
        "season_window",
        "habitat",
        "static_band",
        "rain_event",
        "window_aggregate",
        "count_days",
        "days_since",
    ]
    variable: str | None = Field(
        default=None, description="the weather variable or cell attribute the factor reads"
    )
    variable_unit: str | None = Field(
        default=None, description="the unit of `variable` (and of `threshold`); '' when unitless"
    )
    aggregate: Literal["sum", "mean", "min", "max"] | None = Field(
        default=None, description="how a window aggregate combines the days"
    )
    window_days: int | None = Field(
        default=None,
        description="days of rain a rain event adds up, the days an aggregate or count spans, or "
        "how far back days_since looks",
    )
    offset_days: int | None = Field(
        default=None, description="the window ends this many days before the scored day"
    )
    op: Literal["lt", "lte", "gt", "gte"] | None = Field(
        default=None, description="what counts as a matching day, against `threshold`"
    )
    threshold: float | None = None
    # Lists, not tuples: openapi-fetch turns a generated tuple type into an array, so the client's
    # response type would no longer match the schema's.
    trapezoid: list[float | None] | None = Field(
        default=None,
        min_length=4,
        max_length=4,
        description="[zero_below, full_from, full_to, zero_above] over the measurement (`input`, "
        "in `unit`); a null pair leaves that side open",
    )
    lag_days: list[float | None] | None = Field(
        default=None,
        min_length=4,
        max_length=4,
        description="rain events: the same shape over `days_ago`, the lag the rain may have",
    )

    @property
    def input_unit(self) -> str | None:
        """The unit of the measurement the rule reads: days for a count, else the variable's own."""
        if self.kind in ("count_days", "days_since"):
            return "days"
        if self.kind in ("season_window", "habitat"):
            return None
        return self.variable_unit


class FactorBreakdown(BaseModel):
    """One rule's contribution to a score, in evaluation order (gates, then
    drivers, then stoppers) -- the "why this score" breakdown never re-sorts
    by magnitude, so the same species always reads in the same order.

    `contribution` is this factor's own multiplicative share of the day's
    score: the product of every factor's `contribution` equals `score`.

    `input`, `unit` and `days_ago` are the measurement this factor read; they
    are null for a factor that measures nothing (season, habitat) and for days
    scored without the measurement columns. `rule` says what the rule wanted.
    """

    key: str
    i18n_key: str
    value: float = Field(ge=0, le=1)
    contribution: float = Field(ge=0, le=1)
    role: Literal["gate", "driver", "stopper"] | None = None
    weight: float | None = Field(default=None, description="drivers only")
    input: float | None = Field(
        default=None,
        description="what the factor measured: mm of rain, a temperature, a count of days, metres",
    )
    unit: str | None = Field(default=None, description="the unit of `input`")
    days_ago: int | None = Field(
        default=None, description="rain events: when the rain it scored ended"
    )
    rule: FactorRule | None = None


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


class SpeciesSeason(BaseModel):
    year: int
    good_days: float = Field(ge=0, description="a typical woodland cell's good days")


class TaxonProfile(BaseModel):
    key: str = Field(description="the taxon's rule set, e.g. porcini_edulis")
    taxon: str = Field(description="scientific name, as the rule set gives it")
    i18n_key: str
    fit_share: float = Field(
        ge=0,
        le=1,
        description="share of the area's woodland whose habitat and altitude plausibly suit it",
    )
    seasons: list[SpeciesSeason] = Field(description="its own good days per season, oldest first")


class SpeciesProfile(BaseModel):
    species: Species
    fit_share: float = Field(
        ge=0, le=1, description="share of the area's woodland plausible for any of its taxa"
    )
    seasons: list[SpeciesSeason] = Field(description="good days per season, oldest first")
    taxa: list[TaxonProfile]


class PlausibleSpeciesResponse(BaseModel):
    """Which species an area's woodland plausibly holds, from habitat and altitude alone (weather
    and season aside), and how each species and taxon fared in every stored season."""

    area: Area
    plausible_fit: float = Field(
        gt=0, le=1, description="the habitat x altitude fit a cell needs for a taxon to count"
    )
    good_score: float = Field(gt=0, le=1)
    species: list[SpeciesProfile]
