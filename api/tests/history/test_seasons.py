from datetime import date, timedelta

import duckdb
import numpy as np
import pandas as pd
import pytest
from pydantic import TypeAdapter

from api.history.areas import area_members
from api.history.seasons import (
    area_day_scores,
    area_good_days,
    area_sightings,
    assemble_seasons,
    cell_good_days,
    month_scores,
    season_scores,
    season_span,
    weather_summary,
    window_dates,
)
from api.model.rules import Factor
from tests.live.helpers import factor, ruleset, species_rules

REGION = "tuscany"


def _season_factor(
    *windows: tuple[str, str, str, str], id: str = "season", enabled: bool = True
) -> Factor:
    return TypeAdapter(Factor).validate_python(
        {
            "id": id,
            "role": "gate",
            "kind": "season_window",
            "i18n_key": "factor.season",
            "input": {
                "windows": [{"label": f"w{i}", "dates": list(w)} for i, w in enumerate(windows)]
            },
            "confidence": "plausible",
            "source": ["x"],
            "data": "available",
            "enabled": enabled,
            "notes": None if enabled else "off",
        }
    )


def _species(key: str, group: str, *season_factors: Factor):
    """A valid rule file needs a driver; only the season windows matter here."""
    return species_rules(key, group, [*season_factors, factor("rain", "driver", weight=1.0)])


# --- season_span -------------------------------------------------------------------------------


def test_the_span_runs_from_the_earliest_start_to_the_latest_end_of_the_groups_windows() -> None:
    rules = ruleset(
        {
            "a": _species("a", "porcini", _season_factor(("01-07", "01-09", "15-11", "20-12"))),
            "b": _species("b", "porcini", _season_factor(("01-05", "01-06", "30-09", "15-11"))),
        },
        groups={"porcini": ["a", "b"]},
    )

    start, end = season_span(rules, ["a", "b"])

    assert window_dates((start, end), 2025) == (date(2025, 5, 1), date(2025, 12, 20))


def test_a_window_that_wraps_into_january_runs_the_span_to_the_end_of_the_year() -> None:
    rules = ruleset(
        {"g": _species("g", "gallinacci", _season_factor(("15-04", "10-05", "15-12", "25-01")))},
        groups={"gallinacci": ["g"]},
    )

    span = season_span(rules, ["g"])

    assert window_dates(span, 2024) == (date(2024, 4, 15), date(2024, 12, 31))


def test_disabled_season_factors_do_not_widen_the_span() -> None:
    rules = ruleset(
        {
            "g": _species(
                "g",
                "gallinacci",
                _season_factor(("01-06", "01-07", "15-10", "15-11")),
                _season_factor(
                    ("01-02", "01-03", "01-04", "01-05"), id="season_two", enabled=False
                ),
            )
        },
        groups={"gallinacci": ["g"]},
    )

    assert window_dates(season_span(rules, ["g"]), 2025) == (date(2025, 6, 1), date(2025, 11, 15))


# --- area_day_scores / cell_good_days ----------------------------------------------------------


def _cells() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "cell_id": ["c1", "c2", "c3"],
            "woodland": True,
            "comune_code": ["A", "A", "B"],
        }
    )


def _scores(rows: list[tuple[str, date, float]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["cell_id", "date", "score"])


D1, D2 = date(2025, 10, 1), date(2025, 10, 2)


def test_area_days_count_scored_and_good_cells() -> None:
    scores = _scores(
        [("c1", D1, 0.7), ("c2", D1, 0.2), ("c3", D1, 0.6), ("c1", D2, 0.1), ("c2", D2, 0.3)]
    )

    days = area_day_scores(scores, area_members(_cells(), REGION), good_score=0.6)

    table = days.set_index(["area_code", "date"])
    assert table.loc[("A", D1), ["cells", "good_cells"]].tolist() == [2, 1]
    assert table.loc[("A", D1), "mean_score"] == pytest.approx(0.45)
    assert table.loc[("B", D1), ["cells", "good_cells"]].tolist() == [1, 1]  # 0.6 counts as good
    assert table.loc[(REGION, D1), ["cells", "good_cells"]].tolist() == [3, 2]
    assert table.loc[(REGION, D2), ["cells", "good_cells"]].tolist() == [2, 0]
    assert ("B", D2) not in table.index  # no score stored for c3 that day


def test_cell_good_days_count_each_cells_good_days() -> None:
    scores = _scores([("c1", D1, 0.7), ("c1", D2, 0.9), ("c2", D1, 0.2), ("c2", D2, 0.61)])

    good = cell_good_days(scores, good_score=0.6).set_index("cell_id")

    assert good["good_days"].to_dict() == {"c1": 2, "c2": 1}
    assert good["days"].to_dict() == {"c1": 2, "c2": 2}


def test_area_good_days_sum_each_days_share_of_good_cells() -> None:
    scores = _scores(
        [("c1", D1, 0.7), ("c2", D1, 0.2), ("c3", D1, 0.6), ("c1", D2, 0.1), ("c2", D2, 0.7)]
    )

    good = area_good_days(scores, area_members(_cells(), REGION), good_score=0.6)

    table = good.set_index("area_code")
    assert table["good_days"].to_dict() == pytest.approx({"A": 1.0, "B": 1.0, REGION: 7 / 6})
    assert table["days"].to_dict() == {"A": 2, "B": 1, REGION: 2}
    assert table.loc["A", "through"] == D2
    assert table.loc["B", "through"] == D1


# --- season_scores / month_scores --------------------------------------------------------------


def _area_days(
    area: str, species: str, start: date, goods: list[int], cells: int = 2
) -> list[dict]:
    return [
        {
            "area_code": area,
            "species": species,
            "date": start + timedelta(days=i),
            "cells": cells,
            "good_cells": good,
            "mean_score": 0.5,
        }
        for i, good in enumerate(goods)
    ]


def _full_year(year: int, good_on: dict[date, int], area: str = "A", cells: int = 2) -> list[dict]:
    days = (date(year + 1, 1, 1) - date(year, 1, 1)).days
    start = date(year, 1, 1)
    goods = [good_on.get(start + timedelta(days=i), 0) for i in range(days)]
    return _area_days(area, "porcini", start, goods, cells)


def test_good_days_are_the_mean_per_woodland_cell_over_the_year() -> None:
    rows = _full_year(2024, {date(2024, 10, 1): 2, date(2024, 10, 2): 1})

    seasons = season_scores(pd.DataFrame(rows), baseline_years=[2024])

    row = seasons.iloc[0]
    assert row["year"] == 2024
    assert row["good_days"] == pytest.approx(1.5)  # (2 + 1) good cell-days / 2 cells
    assert bool(row["complete"]) is True
    assert row["through"] == date(2024, 12, 31)
    assert row["days"] == 366


def test_days_with_cells_missing_count_by_their_share_of_good_cells() -> None:
    # Day 1 scored both cells, one good; day 2 scored only one cell, and it was good.
    rows = [
        *_area_days("A", "porcini", date(2025, 10, 1), [1], cells=2),
        *_area_days("A", "porcini", date(2025, 10, 2), [1], cells=1),
    ]

    row = season_scores(pd.DataFrame(rows), baseline_years=[]).iloc[0]

    assert row["good_days"] == pytest.approx(1.5)  # a typical cell: half a day, then a whole one


def test_the_peak_is_the_day_with_the_largest_share_of_good_cells() -> None:
    rows = _full_year(2025, {date(2025, 9, 20): 1, date(2025, 10, 3): 2, date(2025, 10, 4): 2})

    row = season_scores(pd.DataFrame(rows), baseline_years=[2025]).iloc[0]

    assert row["peak_date"] == date(2025, 10, 3)  # the first of the tied days
    assert row["peak_share"] == pytest.approx(1.0)


def test_a_season_without_good_days_has_no_peak() -> None:
    row = season_scores(pd.DataFrame(_full_year(2025, {})), baseline_years=[2025]).iloc[0]

    assert row["peak_date"] is None
    assert row["peak_share"] == 0
    assert row["good_days"] == 0


def test_typical_is_the_median_of_the_complete_baseline_seasons() -> None:
    rows = [
        *_full_year(2021, {date(2021, 10, 1): 2}),  # 1 good day per cell
        *_full_year(2022, {date(2022, 10, d): 2 for d in (1, 2, 3)}),  # 3
        *_full_year(2023, {date(2023, 10, d): 2 for d in range(1, 11)}),  # 10
        *_full_year(2024, {date(2024, 10, d): 2 for d in range(1, 21)}),  # 20, outside the baseline
    ]

    seasons = season_scores(pd.DataFrame(rows), baseline_years=[2021, 2022, 2023]).set_index("year")

    assert seasons["good_days"].to_dict() == {2021: 1, 2022: 3, 2023: 10, 2024: 20}
    assert set(seasons["good_days_typical"]) == {3}
    assert set(seasons["typical_years"]) == {3}


def test_a_season_in_progress_is_compared_with_past_seasons_to_the_same_day() -> None:
    rows = [
        # 2 good days per cell by 15 June, 10 more later in the year
        *_full_year(
            2023,
            {date(2023, 6, 1): 2, date(2023, 6, 15): 2}
            | {date(2023, 10, d): 2 for d in range(1, 11)},
        ),
        *_full_year(2024, {date(2024, 6, 16): 2}),  # nothing by 15 June
        # 2026 is scored to 15 June only, with one good day per cell
        *_area_days("A", "porcini", date(2026, 1, 1), [0] * 165 + [2]),
    ]

    seasons = season_scores(pd.DataFrame(rows), baseline_years=[2023, 2024]).set_index("year")

    current = seasons.loc[2026]
    assert bool(current["complete"]) is False
    assert current["through"] == date(2026, 6, 15)
    assert current["good_days"] == pytest.approx(1.0)
    assert current["good_days_typical"] == pytest.approx(1.0)  # median of 2 (2023) and 0 (2024)
    assert current["typical_years"] == 2


def test_areas_and_species_are_summarised_separately() -> None:
    rows = [
        *_area_days("A", "porcini", date(2025, 10, 1), [2]),
        *_area_days("B", "porcini", date(2025, 10, 1), [0], cells=1),
        *_area_days("A", "ovoli", date(2025, 10, 1), [1]),
    ]

    seasons = season_scores(pd.DataFrame(rows), baseline_years=[]).set_index(
        ["area_code", "species"]
    )

    assert seasons.loc[("A", "porcini"), "good_days"] == pytest.approx(1.0)
    assert seasons.loc[("B", "porcini"), "good_days"] == pytest.approx(0.0)
    assert seasons.loc[("A", "ovoli"), "good_days"] == pytest.approx(0.5)
    assert np.isnan(seasons.loc[("A", "ovoli"), "good_days_typical"])
    assert seasons.loc[("A", "ovoli"), "typical_years"] == 0


def test_months_carry_good_days_per_cell_and_the_share_of_good_cell_days() -> None:
    rows = [
        *_area_days("A", "porcini", date(2025, 9, 29), [2, 2, 1, 0]),  # 29, 30 Sep, 1, 2 Oct
    ]

    months = month_scores(pd.DataFrame(rows)).set_index("month")

    assert months.loc[9, "good_days"] == pytest.approx(2.0)
    assert months.loc[9, "good_share"] == pytest.approx(1.0)
    assert months.loc[10, "good_days"] == pytest.approx(0.5)
    assert months.loc[10, "good_share"] == pytest.approx(0.25)
    assert set(months["year"]) == {2025}


# --- weather_summary ---------------------------------------------------------------------------


def _weather(
    area: str, start: date, rain: list[float], forecast_from: int | None = None
) -> pd.DataFrame:
    n = len(rain)
    return pd.DataFrame(
        {
            "area_code": area,
            "date": [start + timedelta(days=i) for i in range(n)],
            "precipitation_sum": rain,
            "precipitation_normal": [2.0] * n,
            "temperature_2m_mean": [15.0] * n,
            "temperature_normal": [14.0] * n,
            "forecast": [forecast_from is not None and i >= forecast_from for i in range(n)],
        }
    )


def test_weather_summary_totals_rain_and_averages_temperature_over_the_window() -> None:
    weather = _weather("A", date(2025, 9, 1), [10.0, 0.0, 5.0, 1.0])

    summary = weather_summary(weather, date(2025, 9, 2), date(2025, 9, 3)).set_index("area_code")

    assert summary.loc["A", "rain_mm"] == pytest.approx(5.0)
    assert summary.loc["A", "rain_normal_mm"] == pytest.approx(4.0)
    assert summary.loc["A", "temp_c"] == pytest.approx(15.0)
    assert summary.loc["A", "temp_normal_c"] == pytest.approx(14.0)
    assert summary.loc["A", "through"] == date(2025, 9, 3)


def test_weather_summary_stops_at_the_last_observed_day() -> None:
    weather = _weather("A", date(2025, 9, 1), [1.0, 1.0, 50.0], forecast_from=2)

    summary = weather_summary(weather, date(2025, 9, 1), date(2025, 9, 30)).set_index("area_code")

    assert summary.loc["A", "rain_mm"] == pytest.approx(2.0)
    assert summary.loc["A", "rain_normal_mm"] == pytest.approx(4.0)
    assert summary.loc["A", "through"] == date(2025, 9, 2)


# --- area_sightings ----------------------------------------------------------------------------


def test_sightings_count_towards_their_comune_and_the_region() -> None:
    records = pd.DataFrame(
        [
            ("porcini", "c1", D1, False, 2),
            ("porcini", "c3", D1, False, 1),
            ("porcini", "c2", D2, True, 1),  # obscured: a town-centroid pin
        ],
        columns=["species", "cell_id", "date", "obscured", "count"],
    )

    counts = area_sightings(records, area_members(_cells(), REGION), REGION)

    totals = counts.groupby("area_code")["count"].sum().to_dict()
    assert totals == {"A": 2, "B": 1, REGION: 4}


# --- assemble_seasons --------------------------------------------------------------------------


def test_seasons_carry_the_windows_weather_and_the_years_sightings() -> None:
    area_days = pd.DataFrame(
        [
            *_full_year(2025, {date(2025, 10, 1): 2}),
            *[
                {**row, "species": "combined"}
                for row in _full_year(2025, {date(2025, 10, 1): 2, date(2025, 6, 1): 2})
            ],
        ]
    )
    # Rain 1 mm a day all year against a normal of 2; the window is May to December.
    weather = _weather("A", date(2025, 1, 1), [1.0] * 365)
    sightings = pd.DataFrame(
        [
            ("A", "porcini", date(2025, 10, 2), 2),
            ("A", "ovoli", date(2025, 8, 20), 1),
            ("A", "porcini", date(2024, 10, 2), 5),  # another season
        ],
        columns=["area_code", "species", "date", "count"],
    )
    windows = {"porcini": (121, 354), "combined": (1, 365)}  # 1 May-20 Dec; all year

    seasons, months = assemble_seasons(area_days, weather, sightings, windows, baseline_years=[])

    porcini = seasons[seasons["species"] == "porcini"].iloc[0]
    assert porcini["window_start"] == date(2025, 5, 1)
    assert porcini["window_end"] == date(2025, 12, 20)
    assert porcini["rain_mm"] == pytest.approx(234.0)  # 234 days from 1 May to 20 December
    assert porcini["rain_normal_mm"] == pytest.approx(468.0)
    assert porcini["temp_c"] == pytest.approx(15.0)
    assert porcini["sightings"] == 2
    combined = seasons[seasons["species"] == "combined"].iloc[0]
    assert combined["good_days"] == pytest.approx(2.0)
    assert combined["sightings"] == 3  # every species' sightings
    assert combined["rain_mm"] == pytest.approx(365.0)

    october = months[(months["species"] == "porcini") & (months["month"] == 10)].iloc[0]
    assert october["good_days"] == pytest.approx(1.0)
    assert october["rain_mm"] == pytest.approx(31.0)
    assert october["rain_normal_mm"] == pytest.approx(62.0)
    assert october["sightings"] == 2
    assert (
        months[(months["species"] == "porcini") & (months["month"] == 8)]["sightings"].iloc[0] == 0
    )


def test_a_season_without_weather_has_no_weather_stats() -> None:
    area_days = pd.DataFrame(_full_year(2025, {date(2025, 10, 1): 2}))
    empty_weather = _weather("A", date(2025, 1, 1), [])
    no_sightings = pd.DataFrame(columns=["area_code", "species", "date", "count"])

    seasons, months = assemble_seasons(
        area_days, empty_weather, no_sightings, {"porcini": (121, 354)}, baseline_years=[]
    )

    assert np.isnan(seasons.iloc[0]["rain_mm"])
    assert seasons.iloc[0]["sightings"] == 0
    assert months["rain_mm"].isna().all()


def test_a_partly_scored_season_takes_its_weather_only_to_its_last_scored_day() -> None:
    area_days = pd.DataFrame(_area_days("A", "porcini", date(2025, 5, 1), [0] * 31))  # May only
    weather = _weather("A", date(2025, 1, 1), [1.0] * 365)
    no_sightings = pd.DataFrame(columns=["area_code", "species", "date", "count"])

    seasons, _ = assemble_seasons(
        area_days, weather, no_sightings, {"porcini": (121, 354)}, baseline_years=[]
    )

    row = seasons.iloc[0]
    assert row["weather_through"] == date(2025, 5, 31)
    assert row["rain_mm"] == pytest.approx(31.0)


def test_the_tables_build_the_same_from_parquet_relations(tmp_path) -> None:
    """The build hands DuckDB relations over the stored partitions, never whole years in pandas:
    the answer must not depend on which it gets."""
    area_days = pd.DataFrame(
        [
            *_full_year(2024, {date(2024, 10, 1): 2}),
            *_full_year(2025, {date(2025, 10, d): 2 for d in (1, 2, 3)}),
        ]
    )
    weather = _weather("A", date(2025, 1, 1), [1.0] * 365)
    sightings = pd.DataFrame(
        [("A", "porcini", date(2025, 10, 2), 2)], columns=["area_code", "species", "date", "count"]
    )
    windows = {"porcini": (121, 354)}
    area_days.to_parquet(tmp_path / "days.parquet", index=False)
    weather.to_parquet(tmp_path / "weather.parquet", index=False)
    con = duckdb.connect()
    days_relation = con.sql(f"SELECT * FROM read_parquet('{tmp_path / 'days.parquet'}')")
    weather_relation = con.sql(f"SELECT * FROM read_parquet('{tmp_path / 'weather.parquet'}')")

    from_frames = assemble_seasons(area_days, weather, sightings, windows, baseline_years=[2024])
    from_relations = assemble_seasons(
        days_relation, weather_relation, sightings, windows, baseline_years=[2024], con=con
    )

    for frames, relations in zip(from_frames, from_relations, strict=True):
        pd.testing.assert_frame_equal(
            frames.reset_index(drop=True), relations.reset_index(drop=True), check_dtype=False
        )
