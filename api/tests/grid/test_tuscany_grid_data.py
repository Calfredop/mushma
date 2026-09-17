"""Sanity checks on the built Tuscany grid (skipped until `python -m api.grid.build` has run).

Reference figures:
- INFC 2015 (tables released 2022): Tuscany "bosco" 1,035,448 ha, total wooded land
  1,189,722 ha, land area 2,299,018 ha.
- Regione Toscana, Rapporto sullo stato delle foreste 2019: 1,163,057 ha of forest incl. regrowth.
"""

import pandas as pd
import pytest
from pyproj import Transformer

from api.grid.sources import data_dir

GRID_DIR = data_dir() / "grid" / "tuscany"
pytestmark = pytest.mark.skipif(
    not (GRID_DIR / "cells.parquet").exists(), reason="Tuscany grid not built"
)

INFC_BOSCO_HA = 1_035_448
INFC_LAND_HA = 2_299_018
TO_LAEA = Transformer.from_crs(4326, 3035, always_xy=True)


@pytest.fixture(scope="module")
def cells() -> pd.DataFrame:
    return pd.read_parquet(GRID_DIR / "cells.parquet").set_index("cell_id")


@pytest.fixture(scope="module")
def habitats() -> pd.DataFrame:
    return pd.read_parquet(GRID_DIR / "cell_habitats.parquet")


def _cell_at(cells: pd.DataFrame, lon: float, lat: float) -> pd.Series:
    x, y = TO_LAEA.transform(lon, lat)
    return cells.loc[f"1kmE{int(x // 1000)}N{int(y // 1000)}"]


def test_cell_count_matches_the_region_area(cells: pd.DataFrame) -> None:
    assert len(cells) == 23_803
    assert cells["region_fraction"].sum() * 100 == pytest.approx(INFC_LAND_HA, rel=0.001)


def test_woodland_cells_are_about_twelve_thousand(cells: pd.DataFrame) -> None:
    assert 10_000 <= cells["woodland"].sum() <= 12_500


def test_forest_area_is_close_to_the_national_forest_inventory(cells: pd.DataFrame) -> None:
    forest_ha = (cells["forest_fraction"] * cells["region_fraction"]).sum() * 100

    assert forest_ha == pytest.approx(INFC_BOSCO_HA, rel=0.05)


def test_habitat_fractions_sum_to_one(habitats: pd.DataFrame) -> None:
    totals = habitats.groupby("cell_id")["fraction"].sum()

    assert totals.to_numpy() == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("place", "lon", "lat", "expected_habitats"),
    [
        (
            "Casentino, Camaldoli",
            11.815,
            43.805,
            {"beech", "fir_spruce", "mixed_broadleaf_conifer"},
        ),
        (
            "Casentino, Badia Prataglia",
            11.87,
            43.80,
            {"beech", "fir_spruce", "mixed_broadleaf_conifer"},
        ),
        ("Amiata, summit beech belt", 11.62, 42.885, {"beech"}),
        ("Amiata, chestnut belt above Castel del Piano", 11.58, 42.89, {"chestnut"}),
        ("Garfagnana, Orecchiella", 10.37, 44.20, {"beech", "mixed_broadleaf_conifer"}),
        ("Vallombrosa", 11.555, 43.73, {"fir_spruce", "beech", "mixed_broadleaf_conifer"}),
        ("San Rossore pine woods", 10.30, 43.72, {"mediterranean_pine"}),
        ("Maremma, Monti dell'Uccellina", 11.112, 42.625, {"evergreen_oak", "macchia"}),
    ],
)
def test_known_forests_are_woodland_of_the_right_kind(
    cells: pd.DataFrame, place: str, lon: float, lat: float, expected_habitats: set[str]
) -> None:
    cell = _cell_at(cells, lon, lat)

    assert cell["woodland"], place
    assert cell["dominant_habitat"] in expected_habitats, (place, cell["dominant_habitat"])


@pytest.mark.parametrize(
    ("place", "lon", "lat"), [("Pisa", 10.40, 43.716), ("Firenze", 11.255, 43.77)]
)
def test_cities_are_not_woodland(cells: pd.DataFrame, place: str, lon: float, lat: float) -> None:
    assert not _cell_at(cells, lon, lat)["woodland"], place


def test_monte_amiata_summit_height(cells: pd.DataFrame) -> None:
    cell = _cell_at(cells, 11.623, 42.885)

    assert cell["elevation_max_m"] == pytest.approx(1738, abs=40)
    assert cell["comune_name"] in {"Castel del Piano", "Abbadia San Salvatore", "Arcidosso"}
