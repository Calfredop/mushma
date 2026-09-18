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
        porcini_a_factors.append({"cell_id": CELL_B["cell_id"], "date": day, "rain_a": b_score})
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
