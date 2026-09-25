from pathlib import Path

import numpy as np
import pytest
import yaml

from api.model.config import MODEL_FILE, load_model_config
from api.model.rules import RuleConfigError, load_rules


def test_a_region_model_block_overrides_precipitation_scale(tmp_path: Path) -> None:
    raw = yaml.safe_load(MODEL_FILE.read_text())
    model_path = tmp_path / "model.yaml"
    model_path.write_text(yaml.safe_dump(raw))
    regions = tmp_path / "regions"
    regions.mkdir()
    (regions / "alpine.yaml").write_text(
        yaml.safe_dump(
            {
                "id": "alpine",
                "name": {"it": "Alpi", "en": "Alps"},
                "timezone": "Europe/Rome",
                "bbox_wgs84": [6.0, 45.0, 8.0, 47.0],
                "grid": {"crs": "EPSG:3035", "cell_size_m": 1000},
                "boundary": {"source": "istat_boundaries", "region_code": 1},
                "model": {
                    "precipitation_scale": {
                        "intercept": 1.0,
                        "per_km": 0.0,
                        "notes": "national rain is fine here; no Tuscan gauge fit.",
                    }
                },
            }
        )
    )

    scale = load_model_config(model_path, region="alpine", regions_dir=regions).precipitation_scale

    assert scale.intercept == 1.0 and scale.per_km == 0.0
    assert scale.factor(np.array([0.0, 1500.0])).tolist() == pytest.approx([1.0, 1.0])
    # National defaults unchanged without a region override.
    national = load_model_config(model_path, regions_dir=regions).precipitation_scale
    assert national.intercept == pytest.approx(1.28)


def test_groups_list_the_keys_in_tie_break_order() -> None:
    config = load_model_config()

    assert list(config.groups) == ["porcini", "ovoli", "gallinacci"]
    assert config.groups["porcini"][0] == "porcini_edulis"


def test_the_precipitation_scale_grows_with_elevation_and_stops_at_the_cap() -> None:
    scale = load_model_config().precipitation_scale

    factors = scale.factor(np.array([-50.0, 0.0, 1000.0, 1700.0, 2500.0, np.nan]))

    assert factors[:5] == pytest.approx([1.28, 1.28, 1.57, 1.773, 1.773])
    assert factors[5] == pytest.approx(1.28)  # no DEM height: treated as sea level
    assert scale.sources == ["era5_seamless"]


def test_the_precipitation_scale_cites_a_known_reference() -> None:
    scale = load_model_config().precipitation_scale

    assert scale.source and set(scale.source) <= set(load_rules().references)


def test_a_disabled_scale_leaves_rain_alone(tmp_path: Path) -> None:
    raw = yaml.safe_load(MODEL_FILE.read_text())
    raw["precipitation_scale"]["enabled"] = False
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(raw))

    scale = load_model_config(path).precipitation_scale

    assert scale.factor(np.array([0.0, 1500.0])).tolist() == [1.0, 1.0]


def test_a_model_config_citing_an_unknown_reference_is_refused(tmp_path: Path) -> None:
    raw = yaml.safe_load(MODEL_FILE.read_text())
    raw["precipitation_scale"]["source"] = ["somebody_else"]
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(raw))

    with pytest.raises(RuleConfigError, match="somebody_else"):
        load_rules(model_file=path)


def test_the_backtest_split_is_fixed_and_disjoint() -> None:
    split = load_model_config().backtest

    assert split.train_seasons == list(range(2016, 2024))
    assert split.holdout_seasons == [2024, 2025]
    assert split.live_seasons == [2026]
    assert split.role_of(2020) == "train" and split.role_of(2025) == "holdout"
    assert split.role_of(2030) is None


def test_a_season_in_two_roles_is_refused(tmp_path: Path) -> None:
    raw = yaml.safe_load(MODEL_FILE.read_text())
    raw["backtest"]["holdout_seasons"] = [2023, 2024]
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(raw))

    with pytest.raises(ValueError, match="2023"):
        load_model_config(path)


# --- terrain microclimate ------------------------------------------------------------------------


def test_the_microclimate_cites_known_references_and_has_a_diffuse_share_per_month() -> None:
    micro = load_model_config().microclimate

    assert micro.enabled
    assert micro.source and set(micro.source) <= set(load_rules().references)
    assert len(micro.diffuse_fraction) == 12
    assert all(0 < kd < 1 for kd in micro.diffuse_fraction)


def test_the_microclimate_warms_sunny_cells_cools_shady_ones_and_scales_drying() -> None:
    micro = load_model_config().microclimate
    k = micro.temperature_per_sun["temperature_2m_mean"]
    values = {
        "temperature_2m_mean": np.array([[10.0, 10.0], [10.0, 10.0]]),
        "temperature_2m_min": np.array([[2.0, 2.0], [2.0, 2.0]]),
        "et0_fao_evapotranspiration": np.array([[2.0, 2.0], [2.0, 2.0]]),
        "precipitation_sum": np.array([[5.0, 5.0], [5.0, 5.0]]),
    }
    sun = np.array([[1.2, 1.0], [0.7, np.nan]])

    adjusted = micro.apply(values, sun)

    assert adjusted["temperature_2m_mean"][0].tolist() == pytest.approx([10 + 0.2 * k, 10.0])
    assert adjusted["temperature_2m_mean"][1, 0] == pytest.approx(10 - 0.3 * k)
    assert np.isnan(adjusted["temperature_2m_mean"][1, 1])  # no sun ratio, no weather
    assert adjusted["et0_fao_evapotranspiration"][0].tolist() == pytest.approx(
        [2.0 * (1 + 0.2 * micro.et0_per_sun), 2.0]
    )
    assert adjusted["temperature_2m_min"] is values["temperature_2m_min"]  # nights: no sun
    assert adjusted["precipitation_sum"] is values["precipitation_sum"]
    assert values["temperature_2m_mean"][0, 0] == 10.0  # the input is left alone


def test_a_disabled_microclimate_leaves_the_weather_alone(tmp_path: Path) -> None:
    raw = yaml.safe_load(MODEL_FILE.read_text())
    raw["microclimate"]["enabled"] = False
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(raw))
    values = {"temperature_2m_mean": np.array([[10.0]])}

    adjusted = load_model_config(path).microclimate.apply(values, np.array([[1.5]]))

    assert adjusted["temperature_2m_mean"].tolist() == [[10.0]]


def test_a_microclimate_on_a_variable_the_ingest_lacks_is_refused(tmp_path: Path) -> None:
    raw = yaml.safe_load(MODEL_FILE.read_text())
    raw["microclimate"]["temperature_per_sun"]["dew_point_2m_mean"] = 1.0
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump(raw))

    with pytest.raises(RuleConfigError, match="dew_point_2m_mean"):
        load_rules(model_file=path)


def test_umbria_scales_its_cds_history_with_its_own_gauge_fit() -> None:
    scale = load_model_config(region="umbria").precipitation_scale

    assert scale.sources == ["era5_land_cds", "era5_seamless"]
    assert (scale.intercept, scale.per_km) == (0.89, 0.33)
    assert set(scale.source) <= set(load_rules("umbria").references)
