"""The species rule config: one YAML file per species key per region, a shared bibliography, and
the group roll-up in ``config/model.yaml``.

Rules are data (AGENTS.md): every factor carries a ``source`` that resolves to
``species/references.yaml`` and a ``confidence``. :func:`load_rules` validates the files and
refuses anything the engine could not score faithfully: a rule without a source, an unordered
trapezoid, an enabled rule on data v1 does not have, an unknown habitat or weather variable. See
``config/species/README.md`` for the scoring semantics.

Layout: ``config/species/<region>/<key>.yaml``; ``references.yaml`` stays shared under
``config/species/``. A region may omit a group that ``model.yaml`` lists (no ovoli in the Alps);
the region's files say which keys exist.
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Annotated, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from api.grid.habitats import load_vocabulary
from api.model.config import CONFIG_DIR, MODEL_FILE, load_model_config
from api.weather.config import load_weather_config

SPECIES_DIR = CONFIG_DIR / "species"
REFERENCES_FILE = "references.yaml"
# Meta files that live beside species keys in a region folder; not scored.
NON_SPECIES_FILES = frozenset({"sanity.yaml"})
DEFAULT_REGION = "tuscany"

Role = Literal["gate", "driver", "stopper"]
ROLE_ORDER: tuple[Role, ...] = ("gate", "driver", "stopper")
Confidence = Literal["strong", "plausible", "folklore"]
Group = Literal["porcini", "ovoli", "gallinacci"]

# Daily Open-Meteo variables a rule may name (checked against both APIs by the species research),
# plus the series the engine derives. Only the ones the weather ingest fetches can be enabled.
DailyVariable = Literal[
    "precipitation_sum",
    "rain_sum",
    "snowfall_sum",
    "precipitation_hours",
    "temperature_2m_min",
    "temperature_2m_max",
    "temperature_2m_mean",
    "soil_temperature_0_to_7cm_mean",
    "soil_temperature_7_to_28cm_mean",
    "soil_moisture_0_to_7cm_mean",
    "soil_moisture_7_to_28cm_mean",
    "wind_speed_10m_max",
    "wind_speed_10m_mean",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "et0_fao_evapotranspiration",
    "vapour_pressure_deficit_max",
    "relative_humidity_2m_mean",
    "relative_humidity_2m_min",
    "shortwave_radiation_sum",
    "water_balance",
    "temperature_2m_max_anomaly_30d",
    "sun_exposure_pct",
]
# The cell-day's sun over flat ground's, x 100 (api.model.terrain), added with the weather.
SUN_SERIES = "sun_exposure_pct"
DERIVED_SERIES = {
    # precipitation_sum - et0_fao_evapotranspiration (mm)
    "water_balance": ("precipitation_sum", "et0_fao_evapotranspiration"),
    # temperature_2m_max minus the mean temperature_2m_max of the 30 days before (°C)
    "temperature_2m_max_anomaly_30d": ("temperature_2m_max",),
}
# Cell attributes in the woodland grid (cells.parquet) and ones v1 does not have.
StaticAttribute = Literal[
    "elevation_m",
    "slope_deg",
    "aspect_deg",
    "northness",
    "soil_ph",
    "soil_texture",
    "lithology_calcareous",
    "stand_age",
    "canopy_cover",
    "litter_depth",
]
GRID_ATTRIBUTES = {"elevation_m", "slope_deg", "aspect_deg", "northness", "soil_ph"}
# Display units for the "why this score" measurements. Weather variables carry theirs in
# config/weather.yaml; these two cover what that file lacks. A unitless attribute has "".
ATTRIBUTE_UNITS = {
    "elevation_m": "m",
    "slope_deg": "°",
    "aspect_deg": "°",
    "northness": "",
    "soil_ph": "",
}
DERIVED_UNITS = {
    "water_balance": "mm",
    "temperature_2m_max_anomaly_30d": "°C",
    SUN_SERIES: "%",
}
# Aggregates that compare a window with the cell's own climatology. ``percent_of_normal`` reads
# the daily rain normals (api.history.normals, downscaled like the rain); a percentage only makes
# sense for rain. ``percentile_of_normal`` needs a distribution per cell, which is not computed.
PERCENT_OF_NORMAL_VARIABLES = {"precipitation_sum"}
UNSUPPORTED_AGGREGATES = {"percentile_of_normal"}

Trapezoid = tuple[float | None, float | None, float | None, float | None]


class RuleConfigError(ValueError):
    """A rule file the engine refuses to load."""


def check_trapezoid(t: Trapezoid) -> Trapezoid:
    """``[zero_below, full_from, full_to, zero_above]``: nulls only in pairs, numbers in order."""
    a, b, c, d = t
    if (a is None) != (b is None) or (c is None) != (d is None):
        raise ValueError(f"trapezoid {list(t)}: a null edge must come as a (zero, full) pair")
    known = [v for v in t if v is not None]
    if known != sorted(known):
        raise ValueError(f"trapezoid {list(t)}: edges out of order")
    return t


def ddmm_day_of_year(ddmm: str) -> int:
    """``DD-MM`` as a day of a non-leap year (1-365)."""
    day, month = (int(part) for part in ddmm.split("-"))
    return date(2001, month, day).timetuple().tm_yday


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Where(_Strict):
    """Where a gate or stopper applies: its effect fades out as the cell attribute leaves the
    trapezoid, ``value' = 1 - m x (1 - value)`` with ``m`` the trapezoid of the attribute."""

    attribute: StaticAttribute
    trapezoid: Trapezoid

    @field_validator("trapezoid")
    @classmethod
    def _ordered(cls, t: Trapezoid) -> Trapezoid:
        return check_trapezoid(t)


class _Factor(_Strict):
    id: Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]*$")]
    role: Role
    i18n_key: Annotated[str, Field(pattern=r"^factor\.[a-z0-9_.]+$")]
    weight: Annotated[float, Field(gt=0)] | None = None
    floor: Annotated[float, Field(ge=0, le=1)] | None = None
    confidence: Confidence
    source: Annotated[list[Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]], Field(min_length=1)]
    derived: bool = False
    data: Literal["available", "derived", "missing"]
    enabled: bool = True
    notes: str | None = None
    where: Where | None = None

    @model_validator(mode="after")
    def _common_rules(self) -> "_Factor":
        if self.role == "driver" and self.where is not None:
            raise ValueError(
                f"driver {self.id!r} must not have a where condition (gates, stoppers)"
            )
        if self.role == "driver" and self.weight is None:
            raise ValueError(f"driver {self.id!r} needs a weight")
        if self.role != "driver" and self.weight is not None:
            raise ValueError(f"{self.role} {self.id!r} must not have a weight (drivers only)")
        if self.data == "missing" and self.enabled:
            raise ValueError(f"{self.id!r} uses missing data and must be enabled: false")
        if self.derived and not self.notes:
            raise ValueError(f"{self.id!r} is derived: its notes must say how")
        if not self.enabled and self.data != "missing" and not self.notes:
            raise ValueError(f"{self.id!r} is disabled: its notes must say why")
        return self

    @property
    def uses(self) -> str | None:
        """The weather variable or cell attribute the factor reads, if any."""
        return getattr(self.input, "variable", None) or getattr(self.input, "attribute", None)


class _TrapezoidResponse(_Strict):
    trapezoid: Trapezoid

    _check = field_validator("trapezoid")(check_trapezoid)


class AltitudeShift(_Strict):
    reference_m: float
    days_per_100m: float


class SeasonWindow(_Strict):
    label: str
    dates: tuple[str, str, str, str]
    altitude_shift: AltitudeShift | None = None
    elevation_weight: Trapezoid | None = None

    @field_validator("dates")
    @classmethod
    def _real_dates(cls, dates: tuple[str, str, str, str]) -> tuple[str, str, str, str]:
        for ddmm in dates:
            try:
                day, month = ddmm.split("-")
                if len(day) != 2 or len(month) != 2:
                    raise ValueError
                ddmm_day_of_year(ddmm)
            except ValueError:
                raise ValueError(f"{ddmm!r} is not a DD-MM date") from None
        return dates

    @field_validator("elevation_weight")
    @classmethod
    def _ordered(cls, t: Trapezoid | None) -> Trapezoid | None:
        return None if t is None else check_trapezoid(t)


def _trapezoid_value(t: Trapezoid, x: float) -> float:
    """A single point's value of :func:`api.model.series.trapezoid`, reimplemented here (rather
    than imported) because that module imports ``Trapezoid`` from this one."""
    a, b, c, d = t
    value = 1.0
    if a is not None and b is not None:
        lower = (x - a) / (b - a) if b > a else float(x >= b)
        value = min(value, max(0.0, min(1.0, lower)))
    if c is not None and d is not None:
        upper = (d - x) / (d - c) if d > c else float(x <= c)
        value = min(value, max(0.0, min(1.0, upper)))
    return value


class SeasonInput(_Strict):
    windows: Annotated[list[SeasonWindow], Field(min_length=1)]

    @model_validator(mode="after")
    def _elevation_weights_sum_to_one(self) -> "SeasonInput":
        """``_season`` (api.model.factors) sums the elevation-weighted windows together, so once
        two or more windows carry a weight, they must partition the elevation range: sum to 1
        everywhere. A single weighted window is just a soft elevation gate on it and needs no
        partner."""
        weighted = [w.elevation_weight for w in self.windows if w.elevation_weight is not None]
        if len(weighted) < 2:
            return self
        breakpoints = sorted({v for t in weighted for v in t if v is not None})
        if not breakpoints:
            return self
        probes = [breakpoints[0] - 1.0, *breakpoints, breakpoints[-1] + 1.0]
        for x in probes:
            total = sum(_trapezoid_value(t, x) for t in weighted)
            if abs(total - 1.0) > 1e-9:
                raise ValueError(
                    f"elevation_weight windows must sum to 1 at every elevation; got {total:g} "
                    f"at {x:g} m"
                )
        return self


class SeasonWindowFactor(_Factor):
    """Sum over the windows that carry an elevation weight of (day-of-year trapezoid x elevation
    weight), maxed with any windows that carry none."""

    kind: Literal["season_window"]
    input: SeasonInput


class HabitatInput(_Strict):
    affinity: dict[str, Annotated[float, Field(ge=0, le=1)]]
    default: Annotated[float, Field(ge=0, le=1)] = 0.0


class HabitatFactor(_Factor):
    """Sum over the cell's habitat fractions of fraction x affinity (the host-weighted share),
    optionally saturated by a trapezoid so a high enough share reaches full credit."""

    kind: Literal["habitat"]
    input: HabitatInput
    response: _TrapezoidResponse | None = None


class StaticBandInput(_Strict):
    attribute: StaticAttribute


class StaticBandFactor(_Factor):
    """Trapezoid of a cell attribute."""

    kind: Literal["static_band"]
    input: StaticBandInput
    response: _TrapezoidResponse


class RainEventInput(_Strict):
    variable: Literal["precipitation_sum", "rain_sum"]
    accumulation_days: Annotated[int, Field(ge=1, le=10)]


class RainEventResponse(_Strict):
    amount_mm: Trapezoid
    lag_days: Trapezoid

    _check = field_validator("amount_mm", "lag_days")(check_trapezoid)

    @field_validator("lag_days")
    @classmethod
    def _bounded_lag(cls, t: Trapezoid) -> Trapezoid:
        if t[0] is None or t[3] is None or t[0] < 0:
            raise ValueError(f"lag_days {list(t)} must be a closed window of days >= 0")
        return t


class RainEventFactor(_Factor):
    """Max over lags d of amount(rain over the accumulation days ending d days ago) x lag(d)."""

    kind: Literal["rain_event"]
    input: RainEventInput
    response: RainEventResponse


class WindowAggregateInput(_Strict):
    variable: DailyVariable
    aggregate: Literal["sum", "mean", "min", "max", "percent_of_normal", "percentile_of_normal"]
    window_days: Annotated[int, Field(ge=1, le=180)]
    offset_days: Annotated[int, Field(ge=0)] = 0


class WindowAggregateFactor(_Factor):
    """Trapezoid of an aggregate over the window ending ``offset_days`` before the day."""

    kind: Literal["window_aggregate"]
    input: WindowAggregateInput
    response: _TrapezoidResponse


Op = Literal["lt", "lte", "gt", "gte"]


class CountDaysInput(_Strict):
    variable: DailyVariable
    op: Op
    threshold: float
    window_days: Annotated[int, Field(ge=1, le=60)]
    offset_days: Annotated[int, Field(ge=0)] = 0


class CountDaysFactor(_Factor):
    """Trapezoid of the number of days in the window where ``variable op threshold``."""

    kind: Literal["count_days"]
    input: CountDaysInput
    response: _TrapezoidResponse


class DaysSinceInput(_Strict):
    variable: DailyVariable
    op: Op
    threshold: float
    max_lookback_days: Annotated[int, Field(ge=1, le=180)]


class DaysSinceFactor(_Factor):
    """Trapezoid of the days since the latest day where ``variable op threshold``."""

    kind: Literal["days_since"]
    input: DaysSinceInput
    response: _TrapezoidResponse


Factor = Annotated[
    SeasonWindowFactor
    | HabitatFactor
    | StaticBandFactor
    | RainEventFactor
    | WindowAggregateFactor
    | CountDaysFactor
    | DaysSinceFactor,
    Field(discriminator="kind"),
]


class GrowthTemperature(_Strict):
    """Temperature pace: Yan & Hunt's cardinal curve over ``[t_min, t_opt, t_max]``, divided by
    its value at ``reference_c``, so the pace is 1 at the reference and highest at ``t_opt``."""

    variable: DailyVariable
    cardinal_c: tuple[float, float, float]
    reference_c: float

    @model_validator(mode="after")
    def _ordered(self) -> "GrowthTemperature":
        low, optimum, high = self.cardinal_c
        if not low < optimum < high:
            raise ValueError(f"cardinal_c {list(self.cardinal_c)}: need t_min < t_opt < t_max")
        if not low < self.reference_c < high:
            raise ValueError(
                f"reference_c {self.reference_c} must lie inside cardinal_c {list(self.cardinal_c)}"
            )
        return self


class GrowthHumidity(_Strict):
    """Humidity pace: ``floor + (1 - floor) x trapezoid(variable)``; it only ever slows growth."""

    variable: DailyVariable
    trapezoid: Trapezoid
    floor: Annotated[float, Field(ge=0, le=1)] = 0.0

    _check = field_validator("trapezoid")(check_trapezoid)


class GrowthClock(_Strict):
    """How fast the species develops from a rain to fruit bodies, day by day: pace = temperature
    pace x humidity pace. With it, a ``rain_event`` counts its lag in growth days (the sum of the
    paces since the rain ended) instead of calendar days, looking back at most ``max_lag_days``."""

    enabled: bool = True
    temperature: GrowthTemperature
    humidity: GrowthHumidity | None = None
    max_lag_days: Annotated[int, Field(ge=1, le=120)]
    confidence: Confidence
    source: Annotated[list[Annotated[str, Field(pattern=r"^[a-z0-9_]+$")]], Field(min_length=1)]
    derived: bool = False
    notes: str | None = None

    @model_validator(mode="after")
    def _explained(self) -> "GrowthClock":
        if self.derived and not self.notes:
            raise ValueError("growth is derived: its notes must say how")
        return self

    @property
    def variables(self) -> list[str]:
        """The weather variables the pace reads."""
        found = [self.temperature.variable]
        return found + ([self.humidity.variable] if self.humidity else [])


class Records(_Strict):
    gbif_taxon_keys: Annotated[list[int], Field(min_length=1)]
    inat_taxon_ids: Annotated[list[int], Field(min_length=1)]
    exclude_basis_of_record: list[
        Literal[
            "MATERIAL_SAMPLE",
            "PRESERVED_SPECIMEN",
            "FOSSIL_SPECIMEN",
            "LIVING_SPECIMEN",
            "MACHINE_OBSERVATION",
        ]
    ] = []
    exclude_gbif_taxon_keys: list[int] = []
    exclude_inat_taxon_ids: list[int] = []
    notes: str | None = None


class KnownGap(_Strict):
    id: Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]*$")]
    description: str
    needs: Annotated[list[str], Field(min_length=1)]
    confidence: Confidence
    source: Annotated[list[str], Field(min_length=1)]


class SpeciesRules(_Strict):
    schema_version: Literal[1]
    key: Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]*$")]
    group: Group
    taxon: str
    synonyms: list[str] = []
    status: Literal["draft", "reviewed", "tuned"]
    i18n_key: Annotated[str, Field(pattern=r"^species\.[a-z0-9_]+$")]
    records: Records
    notes: str | None = None
    growth: GrowthClock | None = None
    factors: Annotated[list[Factor], Field(min_length=1)]
    known_gaps: list[KnownGap] = []

    @property
    def clock(self) -> GrowthClock | None:
        """The growth clock the rain events count in, if one is on."""
        return self.growth if self.growth is not None and self.growth.enabled else None

    @model_validator(mode="after")
    def _factor_set(self) -> "SpeciesRules":
        ids = [f.id for f in self.factors]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            raise ValueError(f"duplicate factor ids: {duplicates}")
        if not any(f.enabled and f.role == "driver" for f in self.factors):
            raise ValueError("no enabled driver factor: nothing would move the score day to day")
        if self.clock is not None:
            for f in self.factors:
                if f.enabled and f.kind == "rain_event":
                    window_end = f.response.lag_days[3]
                    if self.clock.max_lag_days < window_end:
                        raise ValueError(
                            f"growth max_lag_days {self.clock.max_lag_days} is shorter than "
                            f"{f.id!r}'s lag window, which ends at {window_end} days"
                        )
        return self

    @property
    def enabled_factors(self) -> list[Factor]:
        """Enabled factors in scoring and breakdown order: gates, drivers, stoppers, each in
        file order."""
        enabled = [f for f in self.factors if f.enabled]
        return sorted(enabled, key=lambda f: ROLE_ORDER.index(f.role))


class Reference(_Strict):
    citation: Annotated[str, Field(min_length=10)]
    doi: Annotated[str, Field(pattern=r"^10\.\S+/\S+$")] | None = None
    url: str | None = None
    kind: Literal[
        "peer_reviewed",
        "preprint",
        "thesis",
        "institutional",
        "society",
        "monograph",
        "dataset",
        "analysis",
        "web",
    ]
    region: str | None = None
    verified: Literal["verified", "snippet-only"]
    supports: str
    cited_as: list[str] = []

    @model_validator(mode="after")
    def _locatable(self) -> "Reference":
        if not self.doi and not self.url:
            raise ValueError("a reference needs a doi or a url")
        return self


class _References(_Strict):
    schema_version: Literal[1]
    references: dict[Annotated[str, Field(pattern=r"^[a-z0-9_]+$")], Reference]


@dataclass(frozen=True)
class RuleSet:
    species: dict[str, SpeciesRules]  # by key, in group order
    groups: dict[str, list[str]]  # group -> keys, in tie-break order
    references: dict[str, Reference]

    def group_of(self, key: str) -> str:
        return self.species[key].group


def _read_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text())
    except (OSError, yaml.YAMLError) as error:
        raise RuleConfigError(f"{path.name}: {error}") from error


def _validate(model: type[BaseModel], doc: dict, name: str) -> BaseModel:
    try:
        return model.model_validate(doc)
    except ValidationError as error:
        raise RuleConfigError(f"{name}: {error}") from error


def _check_species(
    rules: SpeciesRules,
    stem: str,
    references: dict[str, Reference],
    habitats: set[str],
    ingested: set[str],
) -> list[str]:
    errors = []
    if rules.key != stem:
        errors.append(f"key {rules.key!r} does not match the file name")
    if rules.growth is not None:
        unknown = [s for s in rules.growth.source if s not in references]
        if unknown:
            errors.append(f"growth: unknown source ids {unknown} (not in {REFERENCES_FILE})")
        if rules.growth.enabled:
            lacking = [v for v in rules.growth.variables if v not in ingested]
            if lacking:
                errors.append(f"growth: enabled but the weather ingest lacks {lacking}")
    for factor in rules.factors:
        where = f"factor {factor.id!r}"
        unknown = [s for s in factor.source if s not in references]
        if unknown:
            errors.append(f"{where}: unknown source ids {unknown} (not in {REFERENCES_FILE})")
        if factor.kind == "habitat":
            strangers = sorted(set(factor.input.affinity) - habitats)
            if strangers:
                errors.append(f"{where}: unknown habitats {strangers}")
        if not factor.enabled:
            continue
        if factor.where is not None and factor.where.attribute not in GRID_ATTRIBUTES:
            errors.append(f"{where}: enabled but the grid has no {factor.where.attribute!r}")
        uses = factor.uses
        if factor.kind == "static_band" and uses not in GRID_ATTRIBUTES:
            errors.append(f"{where}: enabled but the grid has no {uses!r}")
        elif factor.kind != "static_band" and uses is not None and uses != SUN_SERIES:
            inputs = DERIVED_SERIES.get(uses, (uses,))
            missing = [v for v in inputs if v not in ingested]
            if missing:
                errors.append(f"{where}: enabled but the weather ingest lacks {missing}")
        aggregate = getattr(factor.input, "aggregate", None)
        if aggregate in UNSUPPORTED_AGGREGATES:
            errors.append(
                f"{where}: {aggregate} needs a per-cell climatology, which the engine does not "
                "compute"
            )
        elif aggregate == "percent_of_normal" and uses not in PERCENT_OF_NORMAL_VARIABLES:
            errors.append(
                f"{where}: percent_of_normal only reads {sorted(PERCENT_OF_NORMAL_VARIABLES)}, "
                f"not {uses!r}"
            )
    return errors


def list_rule_regions(species_dir: Path = SPECIES_DIR) -> list[str]:
    """Region ids that have a species rule directory under ``species_dir``."""
    return sorted(
        path.name for path in species_dir.iterdir() if path.is_dir() and any(path.glob("*.yaml"))
    )


def region_rules_dir(region: str, species_dir: Path = SPECIES_DIR) -> Path:
    """``species_dir/<region>/``; raises if the folder is missing."""
    path = species_dir / region
    if not path.is_dir():
        raise RuleConfigError(f"no species rules for region {region!r} at {path}")
    return path


def load_rules(
    region: str = DEFAULT_REGION,
    *,
    species_dir: Path = SPECIES_DIR,
    model_file: Path = MODEL_FILE,
) -> RuleSet:
    """Load and validate every species file for ``region``; raise :class:`RuleConfigError`
    naming the file and the rule on the first file that fails.

    ``model.yaml`` lists the keys each group may use; the region's files say which exist, so a
    region may omit a whole group. ``references.yaml`` is shared at ``species_dir``.
    """
    region_dir = region_rules_dir(region, species_dir)
    refs = _validate(_References, _read_yaml(species_dir / REFERENCES_FILE), REFERENCES_FILE)
    try:
        model = load_model_config(model_file, region=region)
    except (OSError, yaml.YAMLError, ValidationError) as error:
        raise RuleConfigError(f"{model_file.name}: {error}") from error
    for rule, cited in model.cited.items():
        unknown = [s for s in cited if s not in refs.references]
        if unknown:
            raise RuleConfigError(f"{model_file.name}: {rule} cites unknown sources {unknown}")
    catalog = model.groups
    habitats = set(load_vocabulary().habitats)
    ingested = set(load_weather_config().variables)
    unknown = [v for v in model.microclimate.variables if v not in ingested]
    if unknown:
        raise RuleConfigError(
            f"{model_file.name}: microclimate adjusts {unknown}, which the weather ingest lacks"
        )

    loaded: dict[str, SpeciesRules] = {}
    for path in sorted(region_dir.glob("*.yaml")):
        if path.name in NON_SPECIES_FILES:
            continue
        rules = _validate(SpeciesRules, _read_yaml(path), path.stem)
        errors = _check_species(rules, path.stem, refs.references, habitats, ingested)
        listed = [group for group, keys in catalog.items() if rules.key in keys]
        if listed != [rules.group]:
            errors.append(
                f"group {rules.group!r} does not match model.yaml, which lists it under {listed}"
            )
        if errors:
            raise RuleConfigError(f"{path.stem}: " + "; ".join(errors))
        loaded[rules.key] = rules

    if not loaded:
        raise RuleConfigError(f"{region}: no species rule files in {region_dir}")

    groups = {
        group: [key for key in keys if key in loaded]
        for group, keys in catalog.items()
        if any(key in loaded for key in keys)
    }
    ordered = {key: loaded[key] for keys in groups.values() for key in keys}
    return RuleSet(species=ordered, groups=groups, references=refs.references)
