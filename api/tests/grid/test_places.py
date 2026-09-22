from pathlib import Path

import geopandas as gpd
import pandas as pd
import pytest
from pyproj import Transformer
from shapely.geometry import box

from api.grid.cells import generate_grid
from api.grid.places import assign_comuni, nearest_place, read_comuni, read_istat_localities

from .helpers import zip_shapefiles

X0, Y0 = 4_400_000, 2_300_000


def _comuni(*rows: tuple[str, str, str, object]) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {
            "comune_code": [r[0] for r in rows],
            "comune_name": [r[1] for r in rows],
            "province": [r[2] for r in rows],
        },
        geometry=[r[3] for r in rows],
        crs="EPSG:3035",
    )


def test_each_cell_takes_the_comune_covering_most_of_it() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 2000, Y0 + 1000), cell_size_m=1000)
    comuni = _comuni(
        ("051001", "West", "AR", box(X0, Y0, X0 + 1300, Y0 + 1000)),
        ("051002", "East", "AR", box(X0 + 1300, Y0, X0 + 2000, Y0 + 1000)),
    )

    labelled = assign_comuni(grid, comuni).set_index("cell_id")

    assert labelled.loc["1kmE4400N2300", "comune_name"] == "West"
    assert labelled.loc["1kmE4401N2300", "comune_name"] == "East"  # 70 % East, 30 % West
    assert labelled.loc["1kmE4401N2300", "comune_code"] == "051002"
    assert labelled.loc["1kmE4401N2300", "province"] == "AR"


def test_a_cell_outside_every_comune_has_no_comune() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 2000, Y0 + 1000), cell_size_m=1000)
    comuni = _comuni(("051001", "West", "AR", box(X0, Y0, X0 + 1000, Y0 + 1000)))

    labelled = assign_comuni(grid, comuni).set_index("cell_id")

    assert pd.isna(labelled.loc["1kmE4401N2300", "comune_name"])
    assert len(labelled) == 2


def test_read_comuni_keeps_the_region_and_joins_the_province_abbreviation(tmp_path: Path) -> None:
    comuni = gpd.GeoDataFrame(
        {
            "COD_REG": [9, 9, 10],
            "COD_UTS": [51, 53, 54],
            "PRO_COM_T": ["051002", "053011", "054001"],
            "COMUNE": ["Bibbiena", "Roccalbegna", "Assisi"],
        },
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(2, 0, 3, 1)],
        crs="EPSG:32632",
    )
    provinces = gpd.GeoDataFrame(
        {"COD_UTS": [51, 53, 54], "SIGLA": ["AR", "GR", "PG"]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(2, 0, 3, 1)],
        crs="EPSG:32632",
    )
    archive = zip_shapefiles(tmp_path / "limits.zip", {"Com": comuni, "Prov": provinces})

    result = read_comuni(archive, "Com/Com.shp", "Prov/Prov.shp", region_code=9, crs="EPSG:3035")

    assert result[["comune_code", "comune_name", "province"]].values.tolist() == [
        ["051002", "Bibbiena", "AR"],
        ["053011", "Roccalbegna", "GR"],
    ]
    assert result.crs == "EPSG:3035"


def _localities(
    tmp_path: Path, rows: list[tuple[str, int, float, float]], without_cpg: bool = False
) -> Path:
    """An ISTAT-like locality archive: (NOME, TIPO_LOC, lon, lat) points in UTM 32N."""
    points = gpd.GeoDataFrame(
        {"NOME": [r[0] for r in rows], "TIPO_LOC": [r[1] for r in rows]},
        geometry=gpd.points_from_xy([r[2] for r in rows], [r[3] for r in rows]),
        crs="EPSG:4326",
    ).to_crs("EPSG:32632")
    return zip_shapefiles(
        tmp_path / "LocalitaPuntuali_21.zip", {"Localita_2021_Point": points}, without_cpg
    )


def test_read_comuni_recovers_accented_names_from_a_cpg_less_archive(tmp_path: Path) -> None:
    comuni = gpd.GeoDataFrame(
        {
            "COD_REG": [9],
            "COD_UTS": [51],
            "PRO_COM_T": ["051011"],
            "COMUNE": ["Castel San Niccolò"],
        },
        geometry=[box(0, 0, 1, 1)],
        crs="EPSG:32632",
    )
    provinces = gpd.GeoDataFrame(
        {"COD_UTS": [51], "SIGLA": ["AR"]}, geometry=[box(0, 0, 1, 1)], crs="EPSG:32632"
    )
    archive = zip_shapefiles(
        tmp_path / "limits.zip", {"Com": comuni, "Prov": provinces}, without_cpg=True
    )

    result = read_comuni(archive, "Com/Com.shp", "Prov/Prov.shp", region_code=9, crs="EPSG:3035")

    assert result["comune_name"].tolist() == ["Castel San Niccolò"]


def test_read_localities_keeps_inhabited_places_inside_the_bbox(tmp_path: Path) -> None:
    archive = _localities(
        tmp_path,
        [
            ("Badia Prataglia", 1, 11.878, 43.794),  # centro abitato
            ("Camaldoli", 2, 11.820, 43.794),  # nucleo abitato
            ("Zona industriale", 3, 11.80, 43.70),  # località produttiva
            ("Case sparse", 4, 11.85, 43.75),  # scattered houses, not a place
            ("Roma", 1, 12.48, 41.89),  # outside the bbox
        ],
    )

    places = read_istat_localities(archive, bbox_wgs84=(9.68, 42.23, 12.38, 44.48), crs="EPSG:3035")

    assert places["place_name"].tolist() == ["Badia Prataglia", "Camaldoli"]
    assert places.crs == "EPSG:3035"


def test_read_localities_recovers_accented_names_from_a_cpg_less_archive(tmp_path: Path) -> None:
    archive = _localities(
        tmp_path, [("Campiglio di Sammommè", 1, 11.878, 43.794)], without_cpg=True
    )

    places = read_istat_localities(archive, bbox_wgs84=(9.68, 42.23, 12.38, 44.48), crs="EPSG:3035")

    assert places["place_name"].tolist() == ["Campiglio di Sammommè"]


def test_nearest_place_is_measured_from_the_cell_centre() -> None:
    grid = generate_grid(box(X0, Y0, X0 + 2000, Y0 + 1000), cell_size_m=1000)
    places = gpd.GeoDataFrame(
        {"place_name": ["Near west", "Far east"]},
        geometry=gpd.points_from_xy([X0 + 500, X0 + 5500], [Y0 + 3500, Y0 + 500]),
        crs="EPSG:3035",
    )

    labelled = nearest_place(grid, places).set_index("cell_id")

    assert labelled.loc["1kmE4400N2300", "place_name"] == "Near west"
    assert labelled.loc["1kmE4400N2300", "place_distance_km"] == pytest.approx(3.0)
    assert labelled.loc["1kmE4401N2300", "place_name"] == "Near west"  # 3.16 km vs 4.0 km
    assert labelled.loc["1kmE4401N2300", "place_distance_km"] == pytest.approx(3.162, abs=1e-3)


def test_localities_land_in_the_right_projected_cell(tmp_path: Path) -> None:
    archive = _localities(tmp_path, [("Camaldoli", 2, 11.82031, 43.79359)])
    x, y = Transformer.from_crs(4326, 3035, always_xy=True).transform(11.82031, 43.79359)
    cx, cy = int(x // 1000) * 1000, int(y // 1000) * 1000

    places = read_istat_localities(archive, bbox_wgs84=(9.68, 42.23, 12.38, 44.48), crs="EPSG:3035")
    grid = generate_grid(box(cx, cy, cx + 1000, cy + 1000), cell_size_m=1000)
    labelled = nearest_place(grid, places)

    assert labelled.iloc[0]["place_name"] == "Camaldoli"
    assert labelled.iloc[0]["place_distance_km"] < 0.75
