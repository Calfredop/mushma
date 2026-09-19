"""Small builders for model tests: factors from plain dicts, cells and weather from lists."""

from datetime import date, timedelta

import numpy as np
from pydantic import TypeAdapter

from api.model.arrays import Cells, Weather
from api.model.rules import Factor

START = date(2024, 9, 1)
_FACTOR = TypeAdapter(Factor)
COMMON = {
    "i18n_key": "factor.test",
    "confidence": "plausible",
    "source": ["x"],
    "data": "available",
}


def factor(**fields) -> Factor:
    return _FACTOR.validate_python({**COMMON, "id": fields.get("kind", "f"), **fields})


def cells(
    n: int = 1,
    elevation_m: list[float] | None = None,
    habitats: dict[str, list[float]] | None = None,
    slope_deg: list[float] | None = None,
) -> Cells:
    habitats = habitats or {"beech": [1.0] * n}
    return Cells(
        ids=np.array([f"c{i}" for i in range(n)]),
        attributes={
            "elevation_m": np.array(elevation_m or [800.0] * n, dtype=float),
            "slope_deg": np.array(slope_deg or [10.0] * n, dtype=float),
        },
        habitat_names=list(habitats),
        habitat_fractions=np.array(list(habitats.values()), dtype=float).T,
    )


def weather(start: date = START, days: int | None = None, **series: list) -> Weather:
    """Daily series for one cell (a flat list) or several (a list of lists); a scalar value
    fills ``days`` days."""
    arrays = {}
    for name, values in series.items():
        if np.isscalar(values):
            values = [values] * days
        array = np.array(values, dtype=float)
        arrays[name] = array[np.newaxis, :] if array.ndim == 1 else array
    length = next(iter(arrays.values())).shape[1] if arrays else days
    dates = np.array([start + timedelta(days=i) for i in range(length)], dtype="datetime64[D]")
    return Weather(dates=dates, values=arrays)


def day_index(weather: Weather, day: date) -> int:
    return int(np.where(weather.dates == np.datetime64(day))[0][0])
