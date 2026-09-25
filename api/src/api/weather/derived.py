"""FAO-56 / Open-Meteo derived weather: vapour-pressure deficit and reference ET0.

Open-Meteo exposes ``vapour_pressure_deficit`` and ``et0_fao_evapotranspiration`` as
daily fields; the Copernicus CDS does not. This module recomputes them from hourly
2 m temperature, dew point, 10 m wind and surface solar radiation the way Open-Meteo
documents (FAO-56 Penman–Monteith; saturation vapour pressure from Allen et al. 1998).
"""

from __future__ import annotations

import math

import numpy as np

# FAO-56 / Open-Meteo constants (Allen et al. 1998; Open-Meteo FaoEvapotranspiration.swift).
_BETA = 17.27
_LAMBDA = 237.3
_ES_A = 0.6108  # kPa
_STEFAN_BOLTZMANN = 4.903e-9  # MJ K^-4 m^-2 day^-1; hourly uses /24
_GSC = 0.0820  # MJ m^-2 min^-1, solar constant


def saturation_vapour_pressure_kpa(temperature_c: float | np.ndarray) -> float | np.ndarray:
    """e°(T) in kPa (FAO-56 eq. 11)."""
    t = np.asarray(temperature_c, dtype=float)
    return _ES_A * np.exp(_BETA * t / (t + _LAMBDA))


def vapour_pressure_deficit_kpa(
    temperature_c: float | np.ndarray, dewpoint_c: float | np.ndarray
) -> float | np.ndarray:
    """Hourly VPD = e°(T) − e°(Td) in kPa (Open-Meteo / FAO-56)."""
    return saturation_vapour_pressure_kpa(temperature_c) - saturation_vapour_pressure_kpa(
        dewpoint_c
    )


def wind_speed_2m_m_s(wind_10m_m_s: float | np.ndarray) -> float | np.ndarray:
    """Convert 10 m wind to 2 m (FAO-56 eq. 47, log profile over short grass)."""
    return np.asarray(wind_10m_m_s, dtype=float) * 4.87 / math.log(67.8 * 10.0 - 5.42)


def et0_hourly_mm(
    temperature_c: float,
    dewpoint_c: float,
    wind_10m_m_s: float,
    shortwave_mj_m2: float,
    elevation_m: float,
    latitude_deg: float,
    hour_utc: int,
    day_of_year: int,
) -> float:
    """One-hour FAO-56 Penman–Monteith ET₀ (mm), Open-Meteo hourly form.

    ``shortwave_mj_m2`` is the hour's surface solar radiation downwards (SSRD) in
    MJ m⁻². Returns 0 when inputs are non-finite.
    """
    if not all(
        math.isfinite(v)
        for v in (temperature_c, dewpoint_c, wind_10m_m_s, shortwave_mj_m2, elevation_m)
    ):
        return 0.0

    t_k = temperature_c + 273.16
    es = float(saturation_vapour_pressure_kpa(temperature_c))
    ea = float(saturation_vapour_pressure_kpa(dewpoint_c))
    vpd = max(0.0, es - ea)
    delta = 4098.0 * es / (temperature_c + _LAMBDA) ** 2
    p = 101.3 * ((293.0 - 0.0065 * elevation_m) / 293.0) ** 5.26
    gamma = 0.000665 * p
    u2 = float(wind_speed_2m_m_s(wind_10m_m_s))

    lat = math.radians(latitude_deg)
    dr = 1.0 + 0.033 * math.cos(2.0 * math.pi * day_of_year / 365.0)
    delta_s = 0.409 * math.sin(2.0 * math.pi * day_of_year / 365.0 - 1.39)
    gsc_hour = _GSC * 60.0  # MJ m⁻² h⁻¹
    sin_elev = math.sin(lat) * math.sin(delta_s) + math.cos(lat) * math.cos(delta_s) * math.cos(
        (hour_utc - 12) * math.pi / 12.0
    )
    ra = max(0.0, gsc_hour * dr * sin_elev) if sin_elev > 0 else 0.0

    rns = (1.0 - 0.23) * max(0.0, shortwave_mj_m2)
    rso = (0.75 + 2e-5 * elevation_m) * ra if ra > 0 else 0.0
    fcd = 1.35 * (shortwave_mj_m2 / rso) - 0.35 if rso > 0.05 else 0.05
    fcd = min(1.0, max(0.05, fcd))
    rnl = _STEFAN_BOLTZMANN / 24.0 * (t_k**4) * (0.34 - 0.14 * math.sqrt(max(0.0, ea))) * fcd
    rn = rns - rnl
    g = 0.1 * rn if shortwave_mj_m2 > 0.1 else 0.5 * rn

    denom = delta + gamma * (1.0 + 0.34 * u2)
    if denom <= 0:
        return 0.0
    radiation = 0.408 * (rn - g) * delta / denom
    aerodynamic = gamma * (37.0 / t_k) * u2 * vpd / denom
    return max(0.0, radiation + aerodynamic)


def daily_vpd_max_kpa(temperature_c: np.ndarray, dewpoint_c: np.ndarray) -> float:
    """Daily maximum of hourly VPD (kPa)."""
    vpd = vapour_pressure_deficit_kpa(temperature_c, dewpoint_c)
    finite = np.asarray(vpd, dtype=float)
    finite = finite[np.isfinite(finite)]
    return float(np.max(finite)) if len(finite) else float("nan")


def daily_et0_mm(
    temperature_c: np.ndarray,
    dewpoint_c: np.ndarray,
    wind_10m_m_s: np.ndarray,
    shortwave_mj_m2: np.ndarray,
    elevation_m: float,
    latitude_deg: float,
    hours_utc: np.ndarray,
    day_of_year: int,
) -> float:
    """Sum of hourly ET₀ over a local day (mm)."""
    total = 0.0
    for i in range(len(temperature_c)):
        total += et0_hourly_mm(
            float(temperature_c[i]),
            float(dewpoint_c[i]),
            float(wind_10m_m_s[i]),
            float(shortwave_mj_m2[i]),
            elevation_m,
            latitude_deg,
            int(hours_utc[i]),
            day_of_year,
        )
    return total
