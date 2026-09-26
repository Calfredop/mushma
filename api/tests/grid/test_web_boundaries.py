import json
from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import MultiPolygon, Point, Polygon, box, shape

from api.grid.web_boundaries import region_slug, web_boundaries, write_web_boundaries
from tests.grid.helpers import zip_shapefiles

# ISTAT ships its "WGS84" regions in UTM 32N (metres).
UTM32 = "EPSG:32632"
X0, Y0 = 600_000, 4_800_000


def _jagged_west_edge(x: float, y0: float, y1: float, steps: int) -> list[tuple[float, float]]:
    """A border from north to south that zigzags by 20 m: detail the simplification removes."""
    return [(x + (20 if i % 2 else 0), y1 - (y1 - y0) * i / steps) for i in range(steps + 1)]


def _regions() -> gpd.GeoDataFrame:
    """Two neighbours sharing a jagged 40 km border, one with a big island and an islet."""
    border = _jagged_west_edge(X0 + 40_000, Y0, Y0 + 40_000, steps=400)
    west = Polygon([(X0, Y0 + 40_000), *border, (X0, Y0)])
    east = Polygon([*border, (X0 + 80_000, Y0), (X0 + 80_000, Y0 + 40_000)])
    island = box(X0 + 90_000, Y0, X0 + 92_000, Y0 + 2_000)  # 4 km²
    islet = box(X0 + 95_000, Y0, X0 + 95_500, Y0 + 500)  # 0.25 km²
    return gpd.GeoDataFrame(
        {
            "COD_REG": [9, 2],
            "DEN_REG": ["Toscana", "Valle d'Aosta/Vallée d'Aoste"],
        },
        geometry=[MultiPolygon([east, island, islet]), west],
        crs=UTM32,
    )


def _decimals(value: float) -> int:
    text = repr(value)
    return len(text.split(".")[1]) if "." in text else 0


def _coords(geometry: dict) -> list[list[float]]:
    polygons = geometry["coordinates"]
    if geometry["type"] == "Polygon":
        polygons = [polygons]
    return [point for polygon in polygons for ring in polygon for point in ring]


@pytest.mark.parametrize(
    ("name", "slug"),
    [
        ("Toscana", "toscana"),
        ("Emilia-Romagna", "emilia-romagna"),
        ("Valle d'Aosta/Vallée d'Aoste", "valle-d-aosta"),
        ("Trentino-Alto Adige/Südtirol", "trentino-alto-adige"),
        ("Friuli-Venezia Giulia", "friuli-venezia-giulia"),
    ],
)
def test_region_slug_matches_the_web_registry_paths(name: str, slug: str) -> None:
    assert region_slug(name) == slug


def test_features_carry_slug_code_and_italian_name_in_istat_order() -> None:
    collection = web_boundaries(_regions())

    assert collection["type"] == "FeatureCollection"
    assert [f["properties"]["slug"] for f in collection["features"]] == [
        "valle-d-aosta",
        "toscana",
    ]
    aosta, toscana = collection["features"]
    assert aosta["properties"]["code"] == 2
    assert aosta["properties"]["name"] == "Valle d'Aosta"
    assert toscana["properties"]["name"] == "Toscana"


def test_coordinates_are_wgs84_lon_lat_rounded_to_four_decimals() -> None:
    collection = web_boundaries(_regions())

    points = [p for f in collection["features"] for p in _coords(f["geometry"])]
    # UTM 32N 600-700 km east, 4800-4840 km north: central Italy.
    assert all(10 < lon < 12.5 and 43 < lat < 44 for lon, lat in points)
    assert max(_decimals(v) for point in points for v in point) <= 4


def test_islets_under_the_minimum_area_are_dropped() -> None:
    toscana = web_boundaries(_regions(), min_part_km2=1.0)["features"][1]

    assert toscana["geometry"]["type"] == "MultiPolygon"
    assert len(toscana["geometry"]["coordinates"]) == 2  # the mainland and the 4 km² island


def test_simplifying_keeps_neighbours_on_one_shared_border() -> None:
    source = _regions()
    aosta, toscana = web_boundaries(source, tolerance_m=500)["features"]
    west, east = shape(aosta["geometry"]), shape(toscana["geometry"])

    # The 20 m zigzag is gone...
    assert len(_coords(aosta["geometry"])) < 50
    # ...and both sides simplified it the same way: no overlap and no gap between them.
    assert west.intersection(east).area < 1e-9
    mainland = max(east.geoms, key=lambda part: part.area)
    union = west.union(mainland)
    assert isinstance(union, Polygon)
    assert len(union.interiors) == 0


def test_the_label_point_sits_inside_the_largest_part() -> None:
    for feature in web_boundaries(_regions())["features"]:
        geometry = shape(feature["geometry"])
        largest = max(getattr(geometry, "geoms", [geometry]), key=lambda part: part.area)
        lon, lat = feature["properties"]["label"]
        assert largest.contains(Point(lon, lat))
        assert max(_decimals(lon), _decimals(lat)) <= 4


def test_write_reads_the_istat_archive_and_writes_compact_geojson(tmp_path: Path) -> None:
    archive = zip_shapefiles(tmp_path / "limits.zip", {"Reg": _regions()}, without_cpg=True)
    out = tmp_path / "web" / "boundaries.json"

    write_web_boundaries(archive, "Reg/Reg.shp", out)

    text = out.read_text()
    assert "\n" not in text.strip()
    written = json.loads(text)
    assert [f["properties"]["slug"] for f in written["features"]] == [
        "valle-d-aosta",
        "toscana",
    ]
    assert written["attribution"] == "Confini amministrativi © ISTAT, CC BY 4.0"
