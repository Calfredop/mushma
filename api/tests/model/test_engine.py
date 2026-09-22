import math
from datetime import date

import numpy as np
import pytest

from api.model.engine import (
    COMBINED,
    combine_groups,
    group_scores,
    required_lookback,
    score_species,
)
from api.model.factors import lookback_days
from api.model.rules import SpeciesRules, load_rules

from .helpers import cells, weather

nan = np.nan


def _rules(*factors: dict, key: str = "porcini_test", group: str = "porcini") -> SpeciesRules:
    common = {"confidence": "plausible", "source": ["x"], "data": "available"}
    return SpeciesRules.model_validate(
        {
            "schema_version": 1,
            "key": key,
            "group": group,
            "taxon": "Boletus testus",
            "status": "draft",
            "i18n_key": f"species.{key}",
            "records": {"gbif_taxon_keys": [1], "inat_taxon_ids": [1]},
            "factors": [{**common, **f} for f in factors],
        }
    )


def _band(id: str, role: str, attribute_trapezoid: list, **extra) -> dict:
    return {
        "id": id,
        "role": role,
        "i18n_key": f"factor.{id}",
        "kind": "static_band",
        "input": {"attribute": "elevation_m"},
        "response": {"trapezoid": attribute_trapezoid},
        **extra,
    }


def _mean(id: str, role: str, variable: str, trapezoid: list, **extra) -> dict:
    return {
        "id": id,
        "role": role,
        "i18n_key": f"factor.{id}",
        "kind": "window_aggregate",
        "input": {"variable": variable, "aggregate": "mean", "window_days": 1},
        "response": {"trapezoid": trapezoid},
        **extra,
    }


# One gate at 0.5, drivers at 0.25 (weight 2) and 1.0 (weight 1), a stopper at 0.8.
TOY = _rules(
    _mean("frost", "stopper", "temperature_2m_min", [None, None, 0, 5]),
    _band("altitude", "gate", [0, 1000, None, None]),
    _mean("rain", "driver", "precipitation_sum", [0, 40, None, None], weight=2),
    _mean("warmth", "driver", "temperature_2m_mean", [0, 10, None, None], weight=1),
    _mean(
        "unused",
        "driver",
        "temperature_2m_max",
        [0, 10, None, None],
        weight=5,
        enabled=False,
        notes="an alternative the engine must skip",
    ),
)


def _toy_weather(**overrides):
    series = {
        "precipitation_sum": [10.0, 10.0],
        "temperature_2m_mean": [12.0, 12.0],
        "temperature_2m_min": [1.0, 1.0],
        "temperature_2m_max": [nan, nan],
    }
    series.update(overrides)
    return weather(start=date(2024, 10, 1), **series)


def test_score_is_gates_times_stoppers_times_the_weighted_geometric_mean_of_drivers() -> None:
    result = score_species(TOY, cells(elevation_m=[500]), _toy_weather(), date(2024, 10, 2))

    expected = 0.5 * 0.8 * math.exp((2 * math.log(0.25) + 1 * math.log(1.0)) / 3)
    assert result.score[0, 0] == pytest.approx(expected)


def test_the_breakdown_lists_gates_drivers_stoppers_and_multiplies_back_to_the_score() -> None:
    result = score_species(TOY, cells(elevation_m=[500]), _toy_weather(), date(2024, 10, 2))

    breakdown = result.breakdown(0, 0)

    assert [f.key for f in breakdown] == ["altitude", "rain", "warmth", "frost"]
    assert [f.role for f in breakdown] == ["gate", "driver", "driver", "stopper"]
    assert [f.i18n_key for f in breakdown] == [
        "factor.altitude",
        "factor.rain",
        "factor.warmth",
        "factor.frost",
    ]
    by_key = {f.key: f for f in breakdown}
    assert by_key["rain"].value == pytest.approx(0.25)
    assert by_key["rain"].contribution == pytest.approx(0.25 ** (2 / 3))
    assert by_key["frost"].contribution == pytest.approx(0.8)
    assert by_key["rain"].input == pytest.approx(10)
    assert math.prod(f.contribution for f in breakdown) == pytest.approx(result.score[0, 0])


def test_a_driver_at_zero_zeroes_the_score_whatever_the_others_say() -> None:
    dry = _toy_weather(precipitation_sum=[0.0, 0.0])

    result = score_species(TOY, cells(elevation_m=[1500]), dry, date(2024, 10, 2))

    assert result.score[0, 0] == 0
    assert {f.key: f.contribution for f in result.breakdown(0, 0)}["rain"] == 0


def test_missing_weather_leaves_the_score_missing() -> None:
    gap = _toy_weather(temperature_2m_mean=[12.0, nan])

    result = score_species(TOY, cells(elevation_m=[500]), gap, date(2024, 10, 1), date(2024, 10, 2))

    assert not np.isnan(result.score[0, 0])
    assert np.isnan(result.score[0, 1])


def test_weather_must_reach_back_far_enough_for_every_enabled_factor() -> None:
    rules = load_rules().species["porcini_edulis"]
    days = required_lookback(rules)
    assert days == 43  # the heat spike: 14-day count over a 30-day Tmax anomaly

    short = weather(start=date(2024, 9, 1), days=days, precipitation_sum=0.0)
    with pytest.raises(ValueError, match="lookback"):
        score_species(rules, cells(), short, date(2024, 10, 13))


def test_scores_cover_the_requested_days_and_cells() -> None:
    w = _toy_weather(
        precipitation_sum=[[40.0, 40.0], [0.0, 20.0]],
        temperature_2m_mean=[[12.0, 12.0], [12.0, 12.0]],
        temperature_2m_min=[[-1.0, -1.0], [-1.0, -1.0]],
        temperature_2m_max=[[nan, nan], [nan, nan]],
    )

    result = score_species(
        TOY, cells(2, elevation_m=[1000, 1000]), w, date(2024, 10, 1), date(2024, 10, 2)
    )

    assert result.score.shape == (2, 2)
    assert result.dates.tolist() == [date(2024, 10, 1), date(2024, 10, 2)]
    assert result.cell_ids.tolist() == ["c0", "c1"]
    assert result.score[0].tolist() == [1, 1]
    assert result.score[1, 0] == 0
    assert result.score[1, 1] == pytest.approx(0.5 ** (2 / 3))


# --- the real rules on made-up weather ---------------------------------------------------------


def _autumn(rain_days_ago: int | None, tmean: float = 13.0, tmin: float = 8.0, vpd: float = 0.6):
    days = 90
    rain = [2.0] * days
    if rain_days_ago is not None:
        for d in range(3):
            rain[days - 1 - rain_days_ago - d] = 15.0
    autumn = weather(
        start=date(2024, 8, 1),
        precipitation_sum=rain,
        temperature_2m_mean=[tmean] * days,
        temperature_2m_min=[tmin] * days,
        temperature_2m_max=[tmean + 6] * days,
        soil_temperature_0_to_7cm_mean=[tmean] * days,
        snowfall_sum=[0.0] * days,
        et0_fao_evapotranspiration=[1.5] * days,
        vapour_pressure_deficit_max=[vpd] * days,
        sun_exposure_pct=[100.0] * days,
    )
    autumn.normals["precipitation_sum"] = np.full((1, days), 2.0)  # the drizzle is normal
    return autumn


def test_porcini_score_high_twelve_days_after_a_good_rain_in_a_beech_wood() -> None:
    edulis = load_rules().species["porcini_edulis"]
    beech = cells(elevation_m=[1100], habitats={"beech": [1.0]})
    last_day = date(2024, 10, 29)

    wet = score_species(edulis, beech, _autumn(rain_days_ago=12), last_day).score[0, 0]
    no_trigger = score_species(edulis, beech, _autumn(rain_days_ago=None), last_day).score[0, 0]
    frosty = score_species(edulis, beech, _autumn(12, tmin=-2.0), last_day).score[0, 0]

    assert wet > 0.9
    assert no_trigger == 0
    assert frosty == pytest.approx(0.2 * wet)


def test_a_cold_or_dry_spell_after_the_rain_holds_the_porcini_flush_back() -> None:
    edulis = load_rules().species["porcini_edulis"]
    beech = cells(elevation_m=[1100], habitats={"beech": [1.0]})
    last_day = date(2024, 10, 29)

    def trigger(weather) -> tuple[float, float]:
        """The rain line's value, and its pace: growth days per calendar day since the rain."""
        line = score_species(edulis, beech, weather, last_day).factor("rain_trigger")
        return line.value[0, 0], line.growth_days[0, 0] / line.days_ago[0, 0]

    mild = trigger(_autumn(rain_days_ago=10, tmean=15.0))
    cold = trigger(_autumn(rain_days_ago=10, tmean=6.0))
    dry = trigger(_autumn(rain_days_ago=10, tmean=15.0, vpd=2.5))

    assert mild == (1.0, pytest.approx(1.0))  # the reference pace: growth days = days
    assert cold[1] < 0.5 and dry[1] == pytest.approx(0.5)  # ten days are under six growth days
    assert cold[0] == dry[0] == 0  # so the same rain has not fruited yet


def test_the_breakdown_reports_growth_days_on_the_rain_line() -> None:
    edulis = load_rules().species["porcini_edulis"]
    beech = cells(elevation_m=[1100], habitats={"beech": [1.0]})

    result = score_species(edulis, beech, _autumn(rain_days_ago=12, tmean=15.0), date(2024, 10, 29))

    lines = {line.key: line for line in result.breakdown(0, 0)}
    assert lines["rain_trigger"].days_ago in (12, 13)  # a tie goes to the longest lag
    assert lines["rain_trigger"].growth_days == pytest.approx(lines["rain_trigger"].days_ago)
    assert lines["rain_30d"].growth_days is None
    trigger = next(f for f in edulis.enabled_factors if f.id == "rain_trigger")
    assert lookback_days(trigger, edulis.clock) == 42  # 40 calendar days of lag, over 3 of rain


# --- groups and the combined score -------------------------------------------------------------


def _const(key: str, group: str, season: list, value_mm: float) -> SpeciesRules:
    """A species in season all year where the elevation trapezoid ``season`` allows, whose only
    driver is rain reaching full at ``value_mm``."""
    all_year = {"label": "all_year", "dates": ["01-01", "01-01", "31-12", "31-12"]}
    return _rules(
        {
            "id": "season",
            "role": "gate",
            "i18n_key": "factor.season",
            "kind": "season_window",
            "input": {"windows": [{**all_year, "elevation_weight": season}]},
        },
        _mean("rain", "driver", "precipitation_sum", [0, value_mm, None, None], weight=1),
        key=key,
        group=group,
    )


def _two_days():
    return weather(start=date(2024, 10, 1), precipitation_sum=[[10.0, 10.0], [10.0, 10.0]])


def test_a_group_takes_the_max_over_its_keys_and_names_the_winner() -> None:
    here, w = cells(2, elevation_m=[500, 500]), _two_days()
    edulis = score_species(
        _const("a", "porcini", [0, 1, None, None], 20), here, w, date(2024, 10, 2)
    )
    aereus = score_species(
        _const("b", "porcini", [0, 1, None, None], 40), here, w, date(2024, 10, 2)
    )

    porcini = group_scores("porcini", [aereus, edulis])

    assert porcini.score[:, 0].tolist() == [0.5, 0.5]
    assert porcini.winner(0, 0).key == "a"


def test_a_tie_goes_to_the_key_listed_first() -> None:
    here, w = (
        cells(1, elevation_m=[500]),
        weather(start=date(2024, 10, 1), precipitation_sum=[10.0]),
    )
    first = score_species(
        _const("first", "porcini", [0, 1, None, None], 10), here, w, date(2024, 10, 1)
    )
    second = score_species(
        _const("second", "porcini", [0, 1, None, None], 10), here, w, date(2024, 10, 1)
    )

    assert group_scores("porcini", [first, second]).winner(0, 0).key == "first"


def test_combined_is_the_best_group_in_season() -> None:
    here = cells(3, elevation_m=[500, 1500, 3000])
    w = weather(start=date(2024, 10, 1), precipitation_sum=[[10.0], [10.0], [10.0]])
    day = date(2024, 10, 1)
    # porcini in season below 1000 m, ovoli below 2000 m, gallinacci never
    porcini = group_scores(
        "porcini",
        [score_species(_const("p", "porcini", [None, None, 999, 1000], 40), here, w, day)],
    )
    ovoli = group_scores(
        "ovoli", [score_species(_const("o", "ovoli", [None, None, 1999, 2000], 20), here, w, day)]
    )
    gallinacci = group_scores(
        "gallinacci",
        [score_species(_const("g", "gallinacci", [None, None, -1, 0], 10), here, w, day)],
    )

    combined = combine_groups([porcini, ovoli, gallinacci])

    assert combined.key == COMBINED
    assert combined.score[:, 0].tolist() == [0.5, 0.5, 0]
    assert combined.winning_group(0, 0) == "ovoli"
    assert combined.winning_group(1, 0) == "ovoli"
    assert combined.winning_group(2, 0) is None  # nothing in season
    assert combined.breakdown(0, 0) == ovoli.breakdown(0, 0)
    assert combined.breakdown(2, 0) == []


def test_combined_prefers_an_in_season_group_at_zero_over_one_out_of_season() -> None:
    here = cells(1, elevation_m=[500])
    w = weather(start=date(2024, 10, 1), precipitation_sum=[0.0])
    day = date(2024, 10, 1)
    porcini = group_scores(
        "porcini", [score_species(_const("p", "porcini", [None, None, -1, 0], 40), here, w, day)]
    )
    ovoli = group_scores(
        "ovoli", [score_species(_const("o", "ovoli", [None, None, 999, 1000], 20), here, w, day)]
    )

    combined = combine_groups([porcini, ovoli])

    assert combined.score[0, 0] == 0
    assert combined.winning_group(0, 0) == "ovoli"
