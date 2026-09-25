"""CLC-only forest groups and the INFC 2015 bosco check."""

import pytest

from api.grid.build import (
    GroupLayer,
    class_filter,
    forest_classes,
    forest_group_column,
    forest_group_layers,
    forest_type_column,
    read_group_cover,
)
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


def test_forest_group_layers_read_a_single_mapping_as_one_layer() -> None:
    layers = forest_group_layers(load_region("tuscany"), load_vocabulary())

    assert layers is not None
    assert len(layers) == 1
    assert layers[0].source == "rt_ucs"
    assert layers[0].class_column == "ucs19"
    assert layers[0].classes["324"] == "transitional"
    assert layers[0].where is None


def test_forest_group_layers_are_none_when_groups_are_omitted() -> None:
    assert forest_group_layers(load_region("umbria"), load_vocabulary()) is None


def test_forest_group_layers_take_a_list_with_filters() -> None:
    region = load_region("tuscany")
    region.extra["forest"]["groups"] = [
        {
            "source": "cf",
            "class_column": "COD_CAT",
            "where": "STC_RER IN ('11', '26')",
            "classes": {"08": "broadleaf", "55": "conifer"},
        },
        {"source": "cf", "class_column": "STC_RER", "classes": {"210": "transitional"}},
    ]

    layers = forest_group_layers(region, load_vocabulary())

    assert [layer.class_column for layer in layers] == ["COD_CAT", "STC_RER"]
    assert layers[0].where == "STC_RER IN ('11', '26')"
    assert layers[1].classes == {"210": "transitional"}
    groups, _ = forest_classes(region, load_vocabulary())
    assert groups == {"08": "broadleaf", "55": "conifer", "210": "transitional"}


def test_forest_group_layers_reject_an_unknown_group() -> None:
    region = load_region("tuscany")
    region.extra["forest"]["groups"] = [
        {"source": "cf", "class_column": "STC_RER", "classes": {"210": "shrubland"}}
    ]

    with pytest.raises(ValueError, match="shrubland"):
        forest_group_layers(region, load_vocabulary())


def test_class_filter_combines_the_layer_filter_with_its_codes() -> None:
    assert class_filter("ucs19", ["311", "312"]) == "ucs19 IN ('311', '312')"
    assert (
        class_filter("COD_CAT", ["08"], "STC_RER IN ('11')")
        == "(STC_RER IN ('11')) AND COD_CAT IN ('08')"
    )


def test_forest_type_column_prefers_the_region_config_over_the_source_field() -> None:
    assert forest_type_column({}, {"field": "clc18"}) == "clc18"
    assert forest_type_column({}, {}) == "clc18"
    assert forest_type_column({"class_column": "COD_CAT"}, {"field": "clc18"}) == "COD_CAT"


def test_read_group_cover_maps_each_layer_and_drops_filtered_features(tmp_path) -> None:
    import geopandas as gpd
    from shapely.geometry import box

    from api.grid.sources import Source

    x0, y0 = 4_400_000, 2_300_000
    layer = gpd.GeoDataFrame(
        {
            "STC_RER": ["11", "11", "210", "22p"],
            "COD_CAT": ["08", "55", "221", "181"],
        },
        geometry=[box(x0 + 100 * i, y0, x0 + 100 * (i + 1), y0 + 100) for i in range(4)],
        crs="EPSG:3035",
    )
    folder = tmp_path / "shp"
    folder.mkdir()
    layer.to_file(folder / "cf.shp")
    archive = tmp_path / "cf.zip"
    import zipfile

    with zipfile.ZipFile(archive, "w") as zf:
        for part in folder.iterdir():
            zf.write(part, part.name)
    sources = {
        "cf": Source(
            id="cf",
            name="cf",
            homepage="",
            license="CC BY 4.0",
            attribution="cf",
            download={"url": archive.as_uri(), "shapefile": "cf.shp"},
        )
    }
    layers = [
        GroupLayer(
            source="cf",
            class_column="COD_CAT",
            classes={"08": "broadleaf", "55": "conifer", "181": "broadleaf"},
            where="STC_RER IN ('11')",
        ),
        GroupLayer(source="cf", class_column="STC_RER", classes={"210": "transitional"}),
    ]

    cover = read_group_cover(layers, sources, tmp_path / "raw", "EPSG:3035")

    assert sorted(cover["group"]) == ["broadleaf", "conifer", "transitional"]
    assert list(cover.columns) == ["group", "geometry"]
    assert cover.crs.to_epsg() == 3035
