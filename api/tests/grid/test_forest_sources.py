"""CLC-only forest groups, one-map regional sources and the INFC 2015 bosco check."""

from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import box

from api.grid import build
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
from api.grid.sources import Source


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


def _source(source_id: str, download: dict) -> Source:
    return Source(
        id=source_id, name=source_id, homepage="", license="", attribution="", download=download
    )


def test_one_regional_map_gives_groups_and_types_from_a_single_read(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Liguria's forest-type map carries both the land-use code and the forest category."""
    layer = gpd.GeoDataFrame(
        {"cod_uso": ["3115", "312", "223"], "cod_catfor": ["CA", "PC", "NA"]},
        geometry=[
            box(500_000 + i * 100, 4_900_000, 500_100 + i * 100, 4_900_100) for i in range(3)
        ],
        crs="EPSG:25832",
    )
    calls: list[dict] = []

    def fake_read_vector(download: dict, cache_dir: Path, **kwargs: object) -> gpd.GeoDataFrame:
        calls.append(kwargs)
        return layer.copy()

    monkeypatch.setattr(build, "read_vector", fake_read_vector)
    forest_config = {
        "groups": {"source": "rl_forest", "class_column": "cod_uso", "classes": {}},
        "types": {"source": "rl_forest"},
    }
    sources = {"rl_forest": _source("rl_forest", {"wfs": "x", "field": "cod_catfor"})}

    cover = build.read_forest_cover(
        forest_config,
        sources,
        tmp_path,
        region_id="liguria",
        bbox_wgs84=(7.4, 43.7, 10.1, 44.7),
        crs="EPSG:3035",
        group_classes={"3115": "broadleaf", "312": "conifer"},
        type_classes={"CA": "chestnut", "PC": "mediterranean_pine"},
    )

    assert len(calls) == 1
    assert calls[0]["bbox_wgs84"] == (7.4, 43.7, 10.1, 44.7)
    assert list(cover.groups["group"]) == ["broadleaf", "conifer"]
    assert list(cover.types["habitat"]) == ["chestnut", "mediterranean_pine"]
    assert cover.groups.crs == cover.types.crs == "EPSG:3035"
    assert cover.sources == ["rl_forest"]
