from pathlib import Path

import pytest

from api.grid.region import RegionConfig, load_region


def test_tuscany_region_uses_the_eea_1km_grid() -> None:
    region = load_region("tuscany")

    assert region.id == "tuscany"
    assert region.grid.crs == "EPSG:3035"
    assert region.grid.cell_size_m == 1000
    assert region.timezone == "Europe/Rome"


def test_tuscany_boundary_is_the_istat_region() -> None:
    region = load_region("tuscany")

    assert region.boundary.source == "istat_boundaries"
    assert region.boundary.region_code == 9


def test_tuscany_bbox_is_lon_lat_ordered_and_covers_the_region() -> None:
    lon_min, lat_min, lon_max, lat_max = load_region("tuscany").bbox_wgs84

    # Capraia/Gorgona in the west, Monte Argentario in the south, Apennine ridge in the north.
    assert lon_min < 9.69 and lon_max > 12.37
    assert lat_min < 42.24 and lat_max > 44.47


def test_a_region_is_swappable_by_pointing_at_another_file(tmp_path: Path) -> None:
    config = tmp_path / "umbria.yaml"
    config.write_text(
        """
id: umbria
name: {it: Umbria, en: Umbria}
timezone: Europe/Rome
bbox_wgs84: [11.8, 42.3, 13.3, 43.7]
grid: {crs: "EPSG:3035", cell_size_m: 1000}
boundary: {source: istat_boundaries, region_code: 10}
"""
    )

    region = load_region(config)

    assert isinstance(region, RegionConfig)
    assert region.id == "umbria"
    assert region.boundary.region_code == 10


def test_unknown_region_name_fails_loudly() -> None:
    with pytest.raises(FileNotFoundError, match="atlantis"):
        load_region("atlantis")


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("bbox_wgs84", "[12.0, 42.0, 11.0, 43.0]", "bbox"),
        ("grid", '{crs: "EPSG:3035", cell_size_m: 0}', "cell_size_m"),
        ("grid", '{crs: "EPSG:4326", cell_size_m: 1000}', "projected"),
    ],
)
def test_invalid_region_config_is_rejected(
    tmp_path: Path, field: str, value: str, message: str
) -> None:
    fields = {
        "id": "x",
        "name": "{it: X, en: X}",
        "timezone": "Europe/Rome",
        "bbox_wgs84": "[11.0, 42.0, 12.0, 43.0]",
        "grid": '{crs: "EPSG:3035", cell_size_m: 1000}',
        "boundary": "{source: istat_boundaries, region_code: 9}",
    }
    fields[field] = value
    config = tmp_path / "x.yaml"
    config.write_text("\n".join(f"{k}: {v}" for k, v in fields.items()))

    with pytest.raises(ValueError, match=message):
        load_region(config)
