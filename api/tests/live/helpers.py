"""Builders for a tiny synthetic on-disk $DATA_DIR tree, shaped exactly like the real M2/M3/M4
stores (api.grid.store, api.model.store, api.sightings.store) but small enough for fast tests."""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from pydantic import TypeAdapter

from api.grid.cells import cell_id as make_cell_id
from api.model.rules import Factor, Group, Records, RuleSet, SpeciesRules
from api.sightings.store import SightingsStore
from api.timeutil import today_rome

REGION = "tuscany"

_FACTOR = TypeAdapter(Factor)
_FACTOR_COMMON = {
    "confidence": "plausible",
    "source": ["x"],
    "data": "available",
}
_RECORDS = Records(gbif_taxon_keys=[1], inat_taxon_ids=[1])


def factor(id: str, role: str, **overrides) -> Factor:
    fields = {
        **_FACTOR_COMMON,
        "id": id,
        "role": role,
        "i18n_key": f"factor.{id}",
        "kind": "static_band",
        "input": {"attribute": "elevation_m"},
        "response": {"trapezoid": [0, 1, 2, 3]},
    }
    fields.update(overrides)
    return _FACTOR.validate_python(fields)


def species_rules(key: str, group: Group, factors: list[Factor]) -> SpeciesRules:
    return SpeciesRules(
        schema_version=1,
        key=key,
        group=group,
        taxon=f"Testus {key}",
        status="draft",
        i18n_key=f"species.{key}",
        records=_RECORDS,
        factors=factors,
    )


def ruleset(species: dict[str, SpeciesRules], groups: dict[str, list[str]]) -> RuleSet:
    return RuleSet(species=species, groups=groups, references={})


def write_cells(root: Path, cells: list[dict]) -> None:
    """``cells``: dicts of cell_id/x_min/y_min/lon/lat/woodland/comune_name/place_name."""
    path = root / "grid" / REGION / "cells.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(cells).to_parquet(path, index=False)


def cell(x: int, y: int, lon: float, lat: float, *, woodland: bool = True, **overrides) -> dict:
    row = {
        "cell_id": make_cell_id(x, y, 1000),
        "x_min": x,
        "y_min": y,
        "lon": lon,
        "lat": lat,
        "woodland": woodland,
        "comune_name": "Comune",
        "place_name": "Place",
    }
    row.update(overrides)
    return row


def _write_partitioned(root: Path, tier: str, key: str, rows: list[dict]) -> None:
    frame = pd.DataFrame(rows)
    for year, part in frame.groupby(pd.to_datetime(frame["date"]).dt.year):
        path = root / "scores" / REGION / tier / f"species={key}" / f"year={year}" / "data.parquet"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            part = pd.concat([pd.read_parquet(path), part], ignore_index=True)
        part.to_parquet(path, index=False)


def write_daily(root: Path, key: str, rows: list[dict]) -> None:
    """``rows``: dicts of cell_id/date/score, plus source_key (groups) or source_group+source_key
    (combined) as the real pipeline writes them (api.model.pipeline.group_frame/combined_frame).
    Merges into any existing partition for the same key/year, like the real store's upsert."""
    _write_partitioned(root, "daily", key, rows)


def write_factors(root: Path, key: str, rows: list[dict]) -> None:
    """``rows``: dicts of cell_id/date plus one column per enabled factor id. Merges like
    :func:`write_daily`."""
    _write_partitioned(root, "factors", key, rows)


def write_sightings(root: Path, records: list[dict]) -> None:
    SightingsStore(root / "sightings" / REGION).upsert(pd.DataFrame(records))


SCORES_DATE = today_rome() - timedelta(days=200)  # any date well away from the "today" window

CELL_A = cell(0, 0, lon=10.000, lat=43.000, comune_name="Alpha", place_name="APlace")
CELL_B = cell(1000, 0, lon=10.010, lat=43.000, comune_name="Beta", place_name="BPlace")
CELL_C = cell(50_000, 50_000, lon=10.5, lat=43.5, comune_name="Gamma", place_name="CPlace")
CELL_D_NON_WOODLAND = cell(0, 50_000, lon=10.0, lat=43.5, woodland=False)


def dataset_ruleset() -> RuleSet:
    return ruleset(
        {
            "porcini_a": species_rules(
                "porcini_a", "porcini", [factor("rain_a", "driver", weight=1.0)]
            ),
            "porcini_b": species_rules(
                "porcini_b", "porcini", [factor("rain_b", "driver", weight=1.0)]
            ),
            "ovoli_a": species_rules("ovoli_a", "ovoli", [factor("warmth", "driver", weight=1.0)]),
            "gallinacci_a": species_rules(
                "gallinacci_a", "gallinacci", [factor("moisture", "driver", weight=1.0)]
            ),
        },
        groups={
            "porcini": ["porcini_a", "porcini_b"],
            "ovoli": ["ovoli_a"],
            "gallinacci": ["gallinacci_a"],
        },
    )


def build_dataset(root: Path) -> RuleSet:
    """A small but complete synthetic $DATA_DIR: enough for every ScoresRepository method (and
    the API contract tests) to exercise real code paths, not just fixture-mode stand-ins.

    - cells A and B are edge-adjacent (a hotspot cluster); C is isolated; D isn't woodland.
    - one arbitrary day (SCORES_DATE, unrelated to "today") has combined + all 3 groups scored
      for A/B/C, for get_scores / get_hotspots / cross-species cell-set consistency.
    - the 8-day "today..+7" outlook is scored (with factors) for all 3 groups plus combined, on
      cells A and B, for get_spot / get_cell_detail and for the contract tests (which query with
      no explicit date, defaulting to "today"). Porcini switches its winning member halfway
      through the window at cell A, to exercise the per-day daily-tier -> factors-tier join.
    - a couple of sightings, for get_sightings and hotspot sighting counts.
    """
    write_cells(root, [CELL_A, CELL_B, CELL_C, CELL_D_NON_WOODLAND])

    for group, leaf, scores in [
        ("porcini", "porcini_a", [(CELL_A, 0.9), (CELL_B, 0.85), (CELL_C, 0.6)]),
        ("ovoli", "ovoli_a", [(CELL_A, 0.5), (CELL_B, 0.45), (CELL_C, 0.4)]),
        ("gallinacci", "gallinacci_a", [(CELL_A, 0.3), (CELL_B, 0.25), (CELL_C, 0.2)]),
    ]:
        write_daily(
            root,
            group,
            [
                {"cell_id": c["cell_id"], "date": SCORES_DATE, "score": score, "source_key": leaf}
                for c, score in scores
            ],
        )
    write_daily(
        root,
        "combined",
        [
            {
                "cell_id": c["cell_id"],
                "date": SCORES_DATE,
                "score": 0.9,
                "source_group": "porcini",
                "source_key": "porcini_a",
            }
            for c in (CELL_A, CELL_B, CELL_C)
        ],
    )

    # The 8-day "today..+7" outlook, for get_spot / get_cell_detail (and the contract tests, which
    # query with no explicit date and so default to "today"). Cells A and B both get the full
    # window for every group, so every group/combined agrees on the same served cell set. Porcini
    # switches its winning member halfway through the window at cell A, to exercise the per-day
    # daily-tier -> factors-tier join; cell B keeps one winner throughout, simpler.
    days = [today_rome() + timedelta(days=i) for i in range(8)]
    porcini_daily, porcini_a_factors, porcini_b_factors = [], [], []
    for i, day in enumerate(days):
        winner, score = ("porcini_a", 0.4 + 0.01 * i) if i < 4 else ("porcini_b", 0.5 + 0.01 * i)
        porcini_daily.append(
            {"cell_id": CELL_A["cell_id"], "date": day, "score": score, "source_key": winner}
        )
        # Both members are scored (and their factors kept) every day, whether or not they win.
        porcini_a_factors.append(
            {"cell_id": CELL_A["cell_id"], "date": day, "rain_a": 0.4 + 0.01 * i}
        )
        porcini_b_factors.append(
            {"cell_id": CELL_A["cell_id"], "date": day, "rain_b": 0.5 + 0.01 * i}
        )

        b_score = 0.35 + 0.01 * i
        porcini_daily.append(
            {"cell_id": CELL_B["cell_id"], "date": day, "score": b_score, "source_key": "porcini_a"}
        )
        # Cell B's rows carry the stored measurement (its rule reads the cell's elevation); cell A's
        # do not, like days scored before the pipeline kept measurements.
        porcini_a_factors.append(
            {"cell_id": CELL_B["cell_id"], "date": day, "rain_a": b_score, "rain_a__input": 640.0}
        )
    write_daily(root, "porcini", porcini_daily)
    write_factors(root, "porcini_a", porcini_a_factors)
    write_factors(root, "porcini_b", porcini_b_factors)

    for group, leaf, factor_id in [
        ("ovoli", "ovoli_a", "warmth"),
        ("gallinacci", "gallinacci_a", "moisture"),
    ]:
        daily_rows, factor_rows = [], []
        for cell_row, base in [(CELL_A, 0.3), (CELL_B, 0.2)]:
            for i, day in enumerate(days):
                score = base + 0.01 * i
                daily_rows.append(
                    {
                        "cell_id": cell_row["cell_id"],
                        "date": day,
                        "score": score,
                        "source_key": leaf,
                    }
                )
                factor_rows.append({"cell_id": cell_row["cell_id"], "date": day, factor_id: score})
        write_daily(root, group, daily_rows)
        write_factors(root, leaf, factor_rows)

    # Combined: porcini scores highest at both cells throughout, so it's always the winner.
    write_daily(
        root,
        "combined",
        [
            {
                "cell_id": row["cell_id"],
                "date": row["date"],
                "score": row["score"],
                "source_group": "porcini",
                "source_key": row["source_key"],
            }
            for row in porcini_daily
        ],
    )

    write_sightings(
        root,
        [
            sighting_record(
                "1", "porcini", CELL_A["cell_id"], SCORES_DATE, source="gbif", license="CC0"
            ),
            sighting_record(
                "2",
                "porcini",
                CELL_B["cell_id"],
                SCORES_DATE,
                source="inaturalist",
                license="CC-BY-NC-4.0",
            ),
        ],
    )

    write_history(root)

    return dataset_ruleset()


def sighting_record(
    record_id: str,
    species: str,
    cell_id: str,
    on: date,
    *,
    source: str = "gbif",
    license: str = "CC0",
    fetched_at=None,
) -> dict:
    from datetime import UTC, datetime

    return {
        "species": species,
        "cell_id": cell_id,
        "date": on,
        "source": source,
        "record_id": record_id,
        "license": license,
        "obscured": False,
        "fetched_at": fetched_at or datetime(2026, 1, 1, tzinfo=UTC),
    }


# --- Time views (M6): history tables shaped like api.history.build's -----------------------------

HISTORY_AREAS = [
    # area_code, kind, name, province, cells (lon/lat from the cells below)
    ("tuscany", "region", "Toscana", None, [CELL_A, CELL_B, CELL_C]),
    ("045001", "comune", "Alpha", "MS", [CELL_A]),
    ("045002", "comune", "Beta", "MS", [CELL_B]),
    ("045003", "comune", "Gamma", "SI", [CELL_C]),
]
HISTORY_WINDOWS = {
    "porcini": (121, 354),
    "ovoli": (152, 334),
    "gallinacci": (105, 365),
    "combined": (105, 365),
}
HISTORY_RAIN_LEAD = {"porcini": [10, 16], "ovoli": [10, 20], "gallinacci": [10, 30]}
HISTORY_GROUPS = {
    "porcini": ["porcini_a", "porcini_b"],
    "ovoli": ["ovoli_a"],
    "gallinacci": ["gallinacci_a"],
}
HISTORY_TAXA = {
    key: {"taxon": f"Testus {key}", "i18n_key": f"species.{key}"}
    for keys in HISTORY_GROUPS.values()
    for key in keys
}
HISTORY_FIT = {
    ("045001", "porcini"): 1.0,
    ("045001", "porcini_a"): 1.0,
    ("045001", "porcini_b"): 0.25,
    ("045001", "gallinacci"): 0.5,
    ("045001", "gallinacci_a"): 0.5,
    ("tuscany", "porcini"): 0.4,
    ("tuscany", "porcini_a"): 1 / 3,
}
HISTORY_TAXON_GOOD_DAYS = {"porcini_a": 12.0, "porcini_b": 4.5, "gallinacci_a": 7.0}


def _history_days(first: date, last: date) -> list[date]:
    return [first + timedelta(days=i) for i in range((last - first).days + 1)]


def write_history(root: Path) -> None:
    """Two complete past seasons and this one to yesterday, for every area and species; weather
    with normals through today + 6 (the last days forecast); a long-range forecast of weeks from
    this Monday and five months; good days per cell for every season."""
    from api.history.seasons import assemble_seasons
    from api.history.store import HistoryStore

    store = HistoryStore(root / "history" / REGION)
    today = today_rome()
    years = [today.year - 2, today.year - 1, today.year]
    store.write(
        store.areas_path,
        pd.DataFrame(
            [
                {
                    "area_code": code,
                    "kind": kind,
                    "name": name,
                    "province": province,
                    "cells": len(cells),
                    "lon": sum(c["lon"] for c in cells) / len(cells),
                    "lat": sum(c["lat"] for c in cells) / len(cells),
                }
                for code, kind, name, province, cells in HISTORY_AREAS
            ]
        ),
    )

    all_days, all_weather = [], []
    for year in years:
        last = date(year, 12, 31) if year < today.year else today - timedelta(days=1)
        days = _history_days(date(year, 1, 1), last)
        rows = []
        for code, _, _, _, cells in HISTORY_AREAS:
            for species in ("porcini", "ovoli", "gallinacci", "combined"):
                for day in days:
                    autumn = 9 <= day.month <= 10
                    good = len(cells) if autumn and (day.day + year) % 3 == 0 else 0
                    rows.append(
                        {
                            "area_code": code,
                            "species": species,
                            "date": day,
                            "cells": len(cells),
                            "good_cells": good,
                            "mean_score": 0.3 + 0.5 * bool(good),
                        }
                    )
        frame = pd.DataFrame(rows)
        store.write_partition("area_days", year, frame)
        all_days.append(frame)

        weather_last = min(date(year, 12, 31), today + timedelta(days=6))
        weather = pd.DataFrame(
            [
                {
                    "area_code": code,
                    "date": day,
                    "precipitation_sum": 2.0 + (day.day % 5),
                    "temperature_2m_mean": 15.0,
                    "precipitation_normal": 3.5,
                    "temperature_normal": 14.0,
                    "forecast": day >= today,
                }
                for code, *_ in HISTORY_AREAS
                for day in _history_days(date(year, 1, 1), weather_last)
            ]
        )
        store.write_partition("area_weather", year, weather)
        all_weather.append(weather)

        store.write_partition(
            "cell_seasons",
            year,
            pd.DataFrame(
                [
                    {"species": species, "cell_id": c["cell_id"], "days": 365, "good_days": 20 + i}
                    for species in ("porcini", "ovoli", "gallinacci", "combined")
                    for i, c in enumerate([CELL_A, CELL_B, CELL_C])
                ]
            ),
        )

    sightings = pd.DataFrame(
        [
            ("045001", "porcini", date(years[1], 10, 2), 2),
            ("tuscany", "porcini", date(years[1], 10, 2), 2),
        ],
        columns=["area_code", "species", "date", "count"],
    )
    store.write(store.area_sightings_path, sightings)
    seasons, months = assemble_seasons(
        pd.concat(all_days), pd.concat(all_weather), sightings, HISTORY_WINDOWS, years[:2]
    )
    store.write(store.seasons_path, seasons)
    store.write(store.months_path, months)

    monday = today - timedelta(days=today.weekday())
    month_starts = []
    first = today.replace(day=1)
    for _ in range(5):
        month_starts.append(first)
        first = (first + timedelta(days=32)).replace(day=1)
    periods = [
        ("week", monday + timedelta(weeks=i), monday + timedelta(weeks=i, days=6)) for i in range(7)
    ]
    for start in month_starts:
        end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        periods.append(("month", start, end))
    store.write(
        store.area_seasonal_path,
        pd.DataFrame(
            [
                {
                    "area_code": code,
                    "kind": kind,
                    "start": start,
                    "end": end,
                    "variable": variable,
                    "value": value,
                    "anomaly": anomaly,
                    "fetched_at": pd.Timestamp(today, tz="UTC"),
                }
                for code, *_ in HISTORY_AREAS
                for kind, start, end in periods
                for variable, value, anomaly in (
                    ("precipitation_sum", 30.0, 5.0),
                    ("temperature_2m_mean", 14.0, 1.2),
                )
            ]
        ),
    )
    # Plausible species: Alpha is porcini_a country, Beta and Gamma are not; porcini_b and the
    # other groups' taxa have their own good days only in the last complete season.
    store.write(
        store.area_fit_path,
        pd.DataFrame(
            [
                {
                    "area_code": code,
                    "species": species,
                    "cells": len(cells),
                    "fit_share": HISTORY_FIT.get((code, species), 0.0),
                }
                for code, _, _, _, cells in HISTORY_AREAS
                for species in (*HISTORY_GROUPS, *HISTORY_TAXA)
            ]
        ),
    )
    for year in years:
        store.write_partition(
            "taxon_seasons",
            year,
            pd.DataFrame(
                [
                    {
                        "area_code": code,
                        "species": key,
                        "year": year,
                        "days": 365,
                        "through": date(year, 12, 31),
                        "good_days": HISTORY_TAXON_GOOD_DAYS.get(key, 0.0)
                        if year == years[1]
                        else 0.0,
                    }
                    for code, *_ in HISTORY_AREAS
                    for key in HISTORY_TAXA
                ]
            ),
        )
    store.write_meta(
        {
            "good_score": 0.6,
            "plausible_fit": 0.5,
            "groups": HISTORY_GROUPS,
            "taxa": HISTORY_TAXA,
            "weather_years": years[:2],
            "score_years": years[:2],
            "windows": {k: list(v) for k, v in HISTORY_WINDOWS.items()},
            "rain_lead": HISTORY_RAIN_LEAD,
        }
    )
