"""How much sun a cell's slope gets, compared with flat ground: the input of the terrain
microclimate (``config/model.yaml``) and of the per-species ``sun_exposure`` rules.

The **sun ratio** of a cell on a day is its daily clear-sky sunlight divided by flat ground's at the
same latitude:

    ratio = (1 - Kd) x beam_ratio + Kd x (1 + cos slope) / 2

- ``beam_ratio``: the day's direct sun on the cell's mean surface over flat ground's, integrated
  over the hours the sun is up (Duffie & Beckman's incidence angle on a tilted plane; Swift 1976
  and Allen et al. 2006 do the same in closed form). Direct light on a plane is linear in its
  normal, so the cell's mean surface stands for the average of its pixels as long as few of them
  are turned away from the sun.
- the second term is the isotropic diffuse sky a slope sees (Liu & Jordan 1963), with ``Kd`` the
  month's diffuse share of global radiation (PVGIS, Tuscany).

The **mean surface** of a cell tilts by ``atan(c x tan slope)`` towards its dominant bearing, where
``c`` (0-1) is how consistently its pixels face that way: a valley whose two sides cancel out is
almost flat as the sun sees it, however steep each side is. The woodland grid keeps ``northness``
(the mean of cos aspect) and the mean bearing, from which ``c = northness / cos(bearing)``.

Known limits: no shade cast by neighbouring ridges, no ground-reflected light (under 1 % at the
cells' slopes), no afternoon-heat asymmetry (east and west slopes get the same ratio).
"""

import numpy as np

from api.model import series

# Hour-angle samples per day for the numerical integration (midpoint rule).
SAMPLES_PER_DAY = 96


def declination(day_of_year: np.ndarray) -> np.ndarray:
    """Solar declination in radians for days of a 365-day year (Cooper 1969)."""
    doy = np.asarray(day_of_year, dtype=float)
    return np.radians(23.45) * np.sin(2 * np.pi * (284 + doy) / 365)


def aspect_consistency(northness: np.ndarray, aspect_deg: np.ndarray) -> np.ndarray:
    """How consistently a cell's pixels face its mean bearing, 0-1; 0 without a dominant facing."""
    bearing = np.radians(np.asarray(aspect_deg, dtype=float))
    with np.errstate(invalid="ignore", divide="ignore"):
        c = np.asarray(northness, dtype=float) / np.cos(bearing)
    c = np.where(np.isfinite(c), c, 0.0)
    return np.clip(c, 0.0, 1.0)


def mean_surface(
    slope_deg: np.ndarray, aspect_deg: np.ndarray, consistency: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Tilt (degrees) and compass bearing (degrees) of the cell's mean surface."""
    slope = np.radians(np.nan_to_num(np.asarray(slope_deg, dtype=float)))
    c = np.where(np.isnan(aspect_deg), 0.0, consistency)
    tilt = np.degrees(np.arctan2(c * np.sin(slope), np.cos(slope)))
    return tilt, np.nan_to_num(np.asarray(aspect_deg, dtype=float), nan=180.0)


def beam_ratio(
    lat_deg: np.ndarray,
    tilt_deg: np.ndarray,
    azimuth_deg: np.ndarray,
    declinations: np.ndarray,
    samples: int = SAMPLES_PER_DAY,
) -> np.ndarray:
    """Daily direct sun on a plane over flat ground's, ``(cells, days)``, one day per declination.

    ``azimuth_deg`` is the compass bearing the plane faces (0 north, 90 east).
    """
    phi = np.radians(np.asarray(lat_deg, dtype=float))[:, np.newaxis]
    beta = np.radians(np.asarray(tilt_deg, dtype=float))[:, np.newaxis]
    # Duffie & Beckman measure the surface azimuth from south, west positive.
    gamma = np.radians(np.asarray(azimuth_deg, dtype=float) - 180.0)[:, np.newaxis]
    sin_phi, cos_phi = np.sin(phi), np.cos(phi)
    sin_beta, cos_beta = np.sin(beta), np.cos(beta)
    fraction = (np.arange(samples) + 0.5) / samples  # midpoints across the day

    out = np.empty((phi.shape[0], len(declinations)))
    for j, delta in enumerate(np.asarray(declinations, dtype=float)):
        sin_d, cos_d = np.sin(delta), np.cos(delta)
        sunset = np.arccos(np.clip(-np.tan(phi) * np.tan(delta), -1.0, 1.0))
        omega = -sunset + 2 * sunset * fraction  # (cells, samples)
        cos_omega, sin_omega = np.cos(omega), np.sin(omega)
        flat = sin_d * sin_phi + cos_d * cos_phi * cos_omega
        tilted = (
            sin_d * (sin_phi * cos_beta - cos_phi * sin_beta * np.cos(gamma))
            + cos_d * cos_omega * (cos_phi * cos_beta + sin_phi * sin_beta * np.cos(gamma))
            + cos_d * sin_beta * np.sin(gamma) * sin_omega
        )
        daylight = flat > 0
        on_flat = np.where(daylight, flat, 0.0).sum(axis=1)
        on_plane = np.where(daylight, np.maximum(tilted, 0.0), 0.0).sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[:, j] = np.where(on_flat > 0, on_plane / on_flat, 1.0)
    return out


def sun_ratio(
    lat_deg: np.ndarray,
    slope_deg: np.ndarray,
    aspect_deg: np.ndarray,
    northness: np.ndarray,
    dates: np.ndarray,
    diffuse_fraction: list[float],
) -> np.ndarray:
    """Each cell's daily sun over flat ground's, ``(cells, days)``; ``diffuse_fraction`` holds
    the diffuse share of global radiation for each month, January first."""
    consistency = aspect_consistency(northness, aspect_deg)
    tilt, azimuth = mean_surface(slope_deg, aspect_deg, consistency)
    doy = series.day_of_year(dates)
    unique, index = np.unique(doy, return_inverse=True)
    beam = beam_ratio(lat_deg, tilt, azimuth, declination(unique))[:, index]
    months = np.asarray(dates, dtype="datetime64[M]").astype(int) % 12
    kd = np.asarray(diffuse_fraction, dtype=float)[months][np.newaxis, :]
    sky = ((1 + np.cos(np.radians(np.nan_to_num(slope_deg)))) / 2)[:, np.newaxis]
    return (1 - kd) * beam + kd * sky
