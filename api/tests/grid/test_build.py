import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import box

from api.grid.build import CELL_COLUMNS, assemble_cells, forest_classes
from api.grid.cells import generate_grid
from api.grid.habitats import load_vocabulary
from api.grid.region import load_region

X0, Y0 = 4_453_000, 2_199_000


def test_tuscany_forest_classes_use_the_habitat_vocabulary() -> None:
    vocabulary = load_vocabulary()

    group_classes, type_classes = forest_classes(load_region("tuscany"), vocabulary)

    assert set(group_classes.values()) == set(vocabulary.groups)
    assert set(type_classes.values()) <= set(vocabulary.habitats)
    for group in ("broadleaf", "conifer"):
        members = {h for h, g in vocabulary.group_of.items() if g == group}
        assert members <= set(type_classes.values()), group


def test_forest_classes_reject_a_habitat_outside_the_vocabulary() -> None:
    region = load_region("tuscany")
    region.extra["forest"]["types"]["classes"]["3115"] = "beech_forest"

    with pytest.raises(ValueError, match="beech_forest"):
        forest_classes(region, load_vocabulary())


def test_assemble_cells_joins_every_layer_onto_the_grid() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 2000, Y0 + 1000), cell_size_m=1000)
    ids = grid["cell_id"].tolist()
    mask = pd.DataFrame(
        {
            "cell_id": ids,
            "forest_fraction": [0.9, 0.1],
            "wooded_fraction": [0.95, 0.2],
            "woodland": [True, False],
        }
    )
    summary = pd.DataFrame(
        {
            "cell_id": ids,
            "dominant_habitat": ["beech", "macchia"],
            "dominant_fraction": [0.8, 1.0],
            "borrowed_type_fraction": [0.0, 0.0],
        }
    )
    terrain = pd.DataFrame(
        {"cell_id": [ids[0]], "elevation_m": [1549.0], "slope_deg": [17.6], "valid_fraction": [1.0]}
    )
    soil = pd.DataFrame({"cell_id": ids, "soil_ph": [5.9, 6.4]})
    comuni = pd.DataFrame(
        {"cell_id": ids, "comune_code": ["053004"] * 2, "comune_name": ["Castel del Piano"] * 2}
    )
    places = pd.DataFrame(
        {
            "cell_id": ids,
            "place_name": ["Prato delle Macinaie"] * 2,
            "place_distance_km": [1.1, 1.9],
        }
    )

    cells = assemble_cells(grid, mask, summary, terrain, soil, comuni, places)

    assert isinstance(cells, gpd.GeoDataFrame)
    assert cells["cell_id"].tolist() == ids
    assert list(cells.columns) == [c for c in CELL_COLUMNS if c in cells.columns]
    second = cells.set_index("cell_id").loc[ids[1]]
    assert np.isnan(second["elevation_m"])  # no terrain row for that cell
    assert second["soil_ph"] == 6.4
    assert cells["woodland"].dtype == bool
