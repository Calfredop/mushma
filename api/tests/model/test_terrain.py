import math

import numpy as np
import pytest

from api.model.terrain import (
    aspect_consistency,
    beam_ratio,
    declination,
    mean_surface,
    sun_ratio,
)

LAT = 43.5


def _beam(tilt: float, azimuth: float, dec: float = 0.0, lat: float = LAT) -> float:
    return float(
        beam_ratio(np.array([lat]), np.array([tilt]), np.array([azimuth]), np.array([dec]))[0, 0]
    )


# --- declination ---------------------------------------------------------------------------------


def test_declination_is_zero_near_the_equinoxes_and_extreme_at_the_solstices() -> None:
    dec = np.degrees(declination(np.array([81, 172, 264, 355])))

    assert dec[0] == pytest.approx(0, abs=0.5)
    assert dec[1] == pytest.approx(23.45, abs=0.1)
    assert dec[2] == pytest.approx(0, abs=0.5)
    assert dec[3] == pytest.approx(-23.45, abs=0.1)


# --- beam ratio: exact cases on the equinox ------------------------------------------------------


def test_flat_ground_has_ratio_one() -> None:
    assert _beam(0, 180) == pytest.approx(1)
    assert _beam(0, 0, dec=math.radians(-20)) == pytest.approx(1)


def test_a_south_slope_as_steep_as_the_latitude_faces_the_equinox_sun() -> None:
    # On the equinox a south slope of tilt beta sees the sun as flat ground at latitude
    # (lat - beta) does: the daily ratio is cos(lat - beta) / cos(lat).
    assert _beam(LAT, 180) == pytest.approx(1 / math.cos(math.radians(LAT)), rel=1e-3)
    assert _beam(20, 180) == pytest.approx(
        math.cos(math.radians(LAT - 20)) / math.cos(math.radians(LAT)), rel=1e-3
    )


def test_a_north_slope_on_the_equinox_gets_cos_lat_plus_tilt() -> None:
    assert _beam(20, 0) == pytest.approx(
        math.cos(math.radians(LAT + 20)) / math.cos(math.radians(LAT)), rel=1e-3
    )


def test_east_and_west_facing_slopes_get_the_same_daily_sun() -> None:
    for dec in (-20.0, 0.0, 15.0):
        east, west = _beam(25, 90, math.radians(dec)), _beam(25, 270, math.radians(dec))
        assert east == pytest.approx(west, rel=1e-6)
        assert _beam(25, 0, math.radians(dec)) < east < _beam(25, 180, math.radians(dec))


def test_the_incidence_matches_a_sun_vector_integration() -> None:
    # Independent check: the sun's direction in (east, north, up) through the day, dotted with the
    # plane's normal. Values from 20,000 samples: 25° E slope in winter (1.0415, the low sun
    # rakes it), 30° S and N slopes in October (1.6534, 0.1293), 40° SE slope (1.7191).
    cases = [(25, 90, -20, 1.0415), (30, 180, -10, 1.6534), (30, 0, -10, 0.1293)]
    for tilt, azimuth, dec, expected in [*cases, (40, 135, -15, 1.7191)]:
        assert _beam(tilt, azimuth, math.radians(dec)) == pytest.approx(expected, abs=2e-4)


def test_the_north_south_contrast_grows_as_the_sun_gets_lower() -> None:
    summer, autumn = math.radians(20), math.radians(-10)

    assert _beam(30, 180, autumn) - _beam(30, 0, autumn) > _beam(30, 180, summer) - _beam(
        30, 0, summer
    )


def test_a_steep_north_slope_in_winter_gets_no_direct_sun() -> None:
    assert _beam(60, 0, math.radians(-23.45)) == 0


# --- the cell's mean surface ---------------------------------------------------------------------


def test_aspect_consistency_is_recovered_from_northness_and_the_mean_bearing() -> None:
    c = aspect_consistency(
        northness=np.array([0.45, -0.3, 0.2 * math.cos(math.radians(80)), 0.0]),
        aspect_deg=np.array([0.0, 180.0, 80.0, np.nan]),
    )

    assert c.tolist() == pytest.approx([0.45, 0.3, 0.2, 0.0])


def test_aspect_consistency_is_zero_where_it_cannot_be_recovered() -> None:
    c = aspect_consistency(northness=np.array([0.0, 0.5]), aspect_deg=np.array([90.0, 0.0]))

    assert c.tolist() == [0.0, 0.5]


def test_mean_surface_tilt_is_the_slope_when_every_pixel_faces_the_same_way() -> None:
    tilt, azimuth = mean_surface(
        slope_deg=np.array([30.0, 30.0, 30.0]),
        aspect_deg=np.array([200.0, 200.0, np.nan]),
        consistency=np.array([1.0, 0.5, 0.0]),
    )

    assert tilt[0] == pytest.approx(30)
    assert tilt[1] == pytest.approx(math.degrees(math.atan(0.5 * math.tan(math.radians(30)))))
    assert tilt[2] == 0
    assert azimuth[:2].tolist() == [200.0, 200.0]


# --- sun ratio per cell and day ------------------------------------------------------------------


def test_sun_ratio_mixes_beam_and_isotropic_diffuse_light() -> None:
    days = np.array(["2024-03-20", "2024-10-15"], dtype="datetime64[D]")
    diffuse = [0.5] * 12
    cells = dict(
        lat_deg=np.array([LAT, LAT]),
        slope_deg=np.array([30.0, 0.0]),
        aspect_deg=np.array([180.0, np.nan]),
        northness=np.array([-1.0, 0.0]),
    )

    ratio = sun_ratio(**cells, dates=days, diffuse_fraction=diffuse)

    beam = _beam(30, 180, float(declination(np.array([79]))[0]))  # 20 March: day 79
    sky = (1 + math.cos(math.radians(30))) / 2
    assert ratio[0, 0] == pytest.approx(0.5 * beam + 0.5 * sky, rel=1e-3)
    assert ratio[1].tolist() == pytest.approx([1.0, 1.0])
    assert ratio[0, 1] > ratio[0, 0]  # a lower autumn sun favours the south slope more


def test_sun_ratio_reads_the_diffuse_share_of_each_month() -> None:
    days = np.array(["2024-01-15", "2024-07-15"], dtype="datetime64[D]")
    cells = dict(
        lat_deg=np.array([LAT]),
        slope_deg=np.array([30.0]),
        aspect_deg=np.array([0.0]),
        northness=np.array([1.0]),
    )
    all_diffuse = [1.0] * 12
    sky = (1 + math.cos(math.radians(30))) / 2

    ratio = sun_ratio(**cells, dates=days, diffuse_fraction=all_diffuse)

    assert ratio[0].tolist() == pytest.approx([sky, sky])
