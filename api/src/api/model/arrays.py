"""What the engine scores: cells with their static attributes, and their daily weather."""

from dataclasses import dataclass, field

import numpy as np

from api.model import series
from api.model.rules import DERIVED_SERIES

ANOMALY_WINDOW_DAYS = 30


@dataclass(frozen=True)
class Cells:
    ids: np.ndarray  # (cells,) cell ids
    attributes: dict[str, np.ndarray]  # attribute -> (cells,) float, NaN when unknown
    habitat_names: list[str]
    habitat_fractions: np.ndarray  # (cells, habitats); rows sum to 1 over the wooded area

    def __len__(self) -> int:
        return len(self.ids)

    def subset(self, index: np.ndarray) -> "Cells":
        return Cells(
            ids=self.ids[index],
            attributes={name: values[index] for name, values in self.attributes.items()},
            habitat_names=self.habitat_names,
            habitat_fractions=self.habitat_fractions[index],
        )


@dataclass(frozen=True)
class Weather:
    """Daily weather per cell over consecutive local days."""

    dates: np.ndarray  # (days,) datetime64[D]
    values: dict[str, np.ndarray]  # variable -> (cells, days) float, NaN when missing
    forecast: np.ndarray | None = None  # (cells, days) bool: the day leans on a forecast
    # variable -> (cells, days) the cell's normal for each day (``percent_of_normal``)
    normals: dict[str, np.ndarray] = field(default_factory=dict)
    _derived: dict[str, np.ndarray] = field(default_factory=dict, repr=False, compare=False)

    def series(self, name: str) -> np.ndarray:
        """A weather variable, or one of the series derived from them."""
        if name in self.values:
            return self.values[name]
        if name not in DERIVED_SERIES:
            raise KeyError(f"no weather variable {name!r}")
        if name not in self._derived:
            if name == "water_balance":
                rain = self.values["precipitation_sum"]
                derived = rain - self.values["et0_fao_evapotranspiration"]
            else:
                derived = series.lagged_anomaly(
                    self.values["temperature_2m_max"], ANOMALY_WINDOW_DAYS
                )
            self._derived[name] = derived
        return self._derived[name]

    def normal(self, name: str) -> np.ndarray:
        """The cell's daily normal of a weather variable."""
        if name not in self.normals:
            raise KeyError(f"no normals for {name!r}: build them with api.history.build normals")
        return self.normals[name]

    def index_of(self, day: np.datetime64) -> int:
        position = int((np.datetime64(day, "D") - self.dates[0]).astype(int))
        if not 0 <= position < len(self.dates):
            raise KeyError(f"{day} is outside the weather's dates")
        return position
