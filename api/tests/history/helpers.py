"""A small synthetic ``$DATA_DIR`` shaped like the real grid, weather, score and sightings stores,
for the history pipeline's end-to-end tests."""

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pandas as pd

from api.grid.cells import cell_id as make_cell_id
from api.model.store import ScoreStore
from api.sightings.store import SightingsStore
from api.weather.store import WeatherStore

REGION = "tuscany"
HISTORY_SOURCE = "era5_seamless"
FORECAST_SOURCE = "ecmwf_ifs"
FETCHED = datetime(2026, 1, 5, tzinfo=UTC)

# Two comuni: Alpha (two cells at 500 and 700 m) and Beta (one cell at 300 m); a fourth cell is
# not woodland.
CELLS = [
    {"x": 0, "y": 0, "comune": ("048001", "Alpha", "FI"), "elevation": 500.0, "woodland": True},
    {"x": 1000, "y": 0, "comune": ("048001", "Alpha", "FI"), "elevation": 700.0, "woodland": True},
    {
        "x": 9000,
        "y": 9000,
        "comune": ("053002", "Beta", "GR"),
        "elevation": 300.0,
        "woodland": True,
    },
    {"x": 0, "y": 9000, "comune": ("053002", "Beta", "GR"), "elevation": 10.0, "woodland": False},
]
CELL_IDS = [make_cell_id(c["x"], c["y"], 1000) for c in CELLS]
A1, A2, B1, B_TOWN = CELL_IDS
POINTS = {"P": 400.0, "Q": 600.0}  # model grid heights


def write_grid(root: Path) -> None:
    rows = []
    for spec, cid in zip(CELLS, CELL_IDS, strict=True):
        code, name, province = spec["comune"]
        rows.append(
            {
                "cell_id": cid,
                "x_min": spec["x"],
                "y_min": spec["y"],
                "lon": 11.0 + spec["x"] / 100_000,
                "lat": 43.0 + spec["y"] / 100_000,
                "woodland": spec["woodland"],
                "elevation_m": spec["elevation"],
                "comune_code": code,
                "comune_name": name,
                "province": province,
                "place_name": f"{name} place",
            }
        )
    path = root / "grid" / REGION / "cells.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(path, index=False)


def weather_store(root: Path) -> WeatherStore:
    return WeatherStore(root / "weather" / REGION)


def write_points(root: Path) -> None:
    store = weather_store(root)
    store.root.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            "point_id": list(POINTS),
            "lat": [43.0, 43.1],
            "lon": [11.0, 11.1],
            "land": True,
        }
    ).to_parquet(store.points_path, index=False)
    # A1 half P, half Q; A2 all Q; B1 all P. Both methods alike.
    weights = [
        (A1, "P", 1.0),
        (A1, "Q", 1.0),
        (A2, "Q", 1.0),
        (B1, "P", 1.0),
    ]
    pd.DataFrame(
        [
            {"method": method, "cell_id": c, "point_id": p, "weight": w}
            for method in ("bilinear", "nearest")
            for c, p, w in weights
        ]
    ).to_parquet(store.weights_path, index=False)
    store.upsert_point_cells(
        pd.DataFrame(
            [
                {
                    "source": source,
                    "point_id": point,
                    "model_lat": 43.0,
                    "model_lon": 11.0,
                    "elevation_m": height,
                    "fetched_at": FETCHED,
                }
                for source in (HISTORY_SOURCE, FORECAST_SOURCE)
                for point, height in POINTS.items()
            ]
        )
    )


def _days(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def write_weather(
    root: Path,
    start: date,
    end: date,
    *,
    rain: dict[str, float],
    temperature: dict[str, float],
    source: str = HISTORY_SOURCE,
) -> None:
    """Constant daily rain and mean temperature per point over ``start..end``."""
    rows = [
        {
            "source": source,
            "point_id": point,
            "date": day,
            "variable": variable,
            "value": values[point],
            "fetched_at": FETCHED,
        }
        for day in _days(start, end)
        for variable, values in (
            ("precipitation_sum", rain),
            ("temperature_2m_mean", temperature),
        )
        for point in POINTS
    ]
    weather_store(root).upsert_daily(pd.DataFrame(rows))


def write_scores(root: Path, key: str, start: date, end: date, score_of) -> None:
    """``score_of(cell_id, day)`` for every woodland cell and day."""
    rows = [
        {"cell_id": cid, "date": day, "score": float(score_of(cid, day)), "forecast": False}
        for day in _days(start, end)
        for cid in (A1, A2, B1)
    ]
    ScoreStore(root / "scores" / REGION).upsert(key, pd.DataFrame(rows))


def write_sightings(root: Path, records: list[tuple[str, str, date, bool]]) -> None:
    SightingsStore(root / "sightings" / REGION).upsert(
        pd.DataFrame(
            [
                {
                    "species": species,
                    "cell_id": cid,
                    "date": day,
                    "source": "gbif",
                    "record_id": str(i),
                    "license": "CC0",
                    "obscured": obscured,
                    "fetched_at": FETCHED,
                }
                for i, (species, cid, day, obscured) in enumerate(records)
            ]
        )
    )


def write_seasonal(root: Path, rows: list[dict]) -> None:
    path = root / "outlook" / REGION / "seasonal.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(path, index=False)
