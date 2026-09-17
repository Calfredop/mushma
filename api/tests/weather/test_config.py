from pathlib import Path

import pytest
import yaml

from api.grid.sources import load_sources
from api.weather.config import load_weather_config

SPECIES_RULES = Path(__file__).resolve().parents[2] / "src/api/config/species"
DERIVED_SERIES = {"water_balance", "temperature_2m_max_anomaly_30d"}


def test_history_comes_from_era5_and_the_forecast_from_ecmwf_ifs() -> None:
    config = load_weather_config()

    assert config.history.model == "era5_seamless"
    assert config.history.endpoint == "https://archive-api.open-meteo.com/v1/archive"
    assert config.forecast.model == "ecmwf_ifs"
    assert config.forecast.endpoint == "https://api.open-meteo.com/v1/forecast"
    assert config.forecast.forecast_days == 8  # today + 7 days
    assert config.source_order == ["era5_seamless", "ecmwf_ifs"]


def test_points_follow_the_era5_land_grid() -> None:
    config = load_weather_config()

    assert config.points.native_spacing_deg == 0.1
    assert config.points.spacing_deg == pytest.approx(0.1 * config.points.stride)


def test_temperatures_are_lapse_rate_corrected_and_the_rest_is_not() -> None:
    variables = load_weather_config().variables

    assert variables["temperature_2m_min"].unit == "°C"
    for name in ("temperature_2m_min", "temperature_2m_max", "temperature_2m_mean"):
        assert 4.0 <= variables[name].lapse_rate_c_per_km <= 7.0, name
    for name in ("precipitation_sum", "soil_moisture_0_to_7cm_mean", "et0_fao_evapotranspiration"):
        assert variables[name].lapse_rate_c_per_km is None, name
    assert {v.downscale for v in variables.values()} <= {"bilinear", "nearest"}


def test_every_weather_variable_the_species_rules_use_is_ingested() -> None:
    used = set()
    for path in SPECIES_RULES.glob("*_*.yaml"):
        for factor in yaml.safe_load(path.read_text()).get("factors", []):
            variable = (factor.get("input") or {}).get("variable")
            if variable:
                used.add(variable)

    assert used - DERIVED_SERIES <= set(load_weather_config().variables)


def test_every_credited_source_is_in_the_catalog() -> None:
    config = load_weather_config()
    catalog = load_sources()

    assert config.credits
    for source_id in config.credits:
        assert catalog[source_id].attribution, source_id


def test_an_unknown_downscaling_method_is_rejected(tmp_path: Path) -> None:
    raw = yaml.safe_load(
        (Path(__file__).resolve().parents[2] / "src/api/config/weather.yaml").read_text()
    )
    raw["variables"]["precipitation_sum"]["downscale"] = "kriging"
    path = tmp_path / "weather.yaml"
    path.write_text(yaml.safe_dump(raw, allow_unicode=True))

    with pytest.raises(ValueError, match="kriging"):
        load_weather_config(path)
