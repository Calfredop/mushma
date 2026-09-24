"""CLC-only forest groups and the INFC 2015 bosco check."""

import pytest

from api.grid.build import forest_classes, forest_group_column
from api.grid.forest import (
    CLC_IV_DEFAULT_TYPES,
    clc_group_for_code,
    compare_infc_bosco,
    forest_area_ha,
)
from api.grid.habitats import load_vocabulary
from api.grid.infc import load_infc_bosco
from api.grid.region import load_region


def test_clc_group_for_code_follows_the_documented_prefixes() -> None:
    assert clc_group_for_code("3114") == "broadleaf"
    assert clc_group_for_code("3123") == "conifer"
    assert clc_group_for_code("3131") == "mixed"
    assert clc_group_for_code("3231") == "macchia"
    assert clc_group_for_code("3232") == "macchia"
    assert clc_group_for_code("324") == "transitional"
    assert clc_group_for_code("3241") == "transitional"
    assert clc_group_for_code("211") is None


def test_clc_iv_default_types_cover_every_tuscany_class() -> None:
    vocabulary = load_vocabulary()
    tuscany_types = forest_classes(load_region("tuscany"), vocabulary)[1]

    assert CLC_IV_DEFAULT_TYPES == tuscany_types
    assert set(CLC_IV_DEFAULT_TYPES.values()) <= set(vocabulary.habitats)


def test_forest_classes_derive_groups_from_clc_when_groups_are_omitted() -> None:
    vocabulary = load_vocabulary()
    region = load_region("umbria")

    assert "groups" not in region.extra["forest"]
    group_classes, type_classes = forest_classes(region, vocabulary)

    assert group_classes["3114"] == "broadleaf"
    assert group_classes["3121"] == "conifer"
    assert group_classes["3132"] == "mixed"
    assert group_classes["3231"] == "macchia"
    assert group_classes["324"] == "transitional"
    assert type_classes == CLC_IV_DEFAULT_TYPES


def test_forest_group_column_accepts_class_column_and_year_column() -> None:
    assert forest_group_column({"class_column": "codice", "year_column": "ucs19"}) == "codice"
    assert forest_group_column({"year_column": "ucs19"}) == "ucs19"
    with pytest.raises(KeyError, match="class_column"):
        forest_group_column({})


def test_infc_bosco_table_has_every_italian_region() -> None:
    table = load_infc_bosco()

    assert table["tuscany"] == 1_035_448
    assert table["umbria"] == 390_305
    assert len(table) == 20
    assert sum(table.values()) == pytest.approx(9_085_188, abs=2)


def test_compare_infc_bosco_warns_beyond_ten_percent() -> None:
    delta, ok = compare_infc_bosco(1_058_107, 1_035_448)
    assert ok
    assert delta == pytest.approx(0.0219, abs=1e-3)

    delta, ok = compare_infc_bosco(1_200_000, 1_035_448)
    assert not ok
    assert delta > 0.10


def test_forest_area_ha_sums_forest_share_of_region_area() -> None:
    import pandas as pd

    grid = pd.DataFrame({"cell_id": ["a", "b"], "region_fraction": [1.0, 0.5]})
    mask = pd.DataFrame({"cell_id": ["a", "b"], "forest_fraction": [0.8, 1.0]})

    # 0.8 * 1.0 * 100 + 1.0 * 0.5 * 100 = 130 ha
    assert forest_area_ha(mask, grid) == pytest.approx(130.0)
