from pathlib import Path

import numpy as np
import pytest
import yaml

from api.model.config import MODEL_FILE, REGIONS_DIR, load_model_config
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
                        "field": None,
                        "intercept": 1.0,
                        "per_km": 0.0,
                        "max_elevation_m": 2000,
                        "notes": "national rain is fine here; no gauge field.",
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
    assert national.field == "rain_scale_field.csv"


def test_groups_list_the_keys_in_tie_break_order() -> None:
    config = load_model_config()

    assert list(config.groups) == ["porcini", "ovoli", "gallinacci"]
    assert config.groups["porcini"][0] == "porcini_edulis"


def test_the_precipitation_scale_is_one_national_field_on_every_reanalysis_source() -> None:
    scale = load_model_config().precipitation_scale

    assert scale.field == "rain_scale_field.csv"
    assert scale.sources == ["era5_land_cds", "era5_seamless"]
    for region in sorted(p.stem for p in REGIONS_DIR.glob("*.yaml")):
        assert load_model_config(region=region).precipitation_scale == scale, region


def test_the_rain_field_grows_with_elevation_and_stops_at_its_cap() -> None:
    scale = load_model_config().precipitation_scale
    # Near Cortona, on the Tuscan-Umbrian border.
    lon, lat = np.full(5, 12.0), np.full(5, 43.3)

    factors = scale.factor(np.array([-50.0, 0.0, 800.0, 5000.0, np.nan]), lon, lat)

    assert factors[0] == factors[1] == factors[4]  # below sea level or no DEM height: sea level
    assert factors[3] >= factors[2] >= factors[1]
    assert 0.5 < factors[1] < 2.0 and factors[3] < 2.5


def test_the_rain_field_has_no_step_at_a_region_border() -> None:
    scale = load_model_config().precipitation_scale
    # Cortona (Tuscany) and Lisciano Niccone (Umbria), 12 km apart, at the same height.
    lon, lat = np.array([11.99, 12.14]), np.array([43.28, 43.25])

    tuscan, umbrian = scale.factor(np.array([400.0, 400.0]), lon, lat)

    assert tuscan / umbrian == pytest.approx(1.0, abs=0.05)


def test_a_scale_takes_a_field_or_a_constant_fit_not_both() -> None:
    from api.model.config import PrecipitationScale

    common = {"enabled": True, "sources": ["x"], "confidence": "c", "source": ["s"], "notes": ""}
    with pytest.raises(ValueError, match="not both"):
        PrecipitationScale(**common, field="f.csv", intercept=1.0, per_km=0.0, max_elevation_m=1)
    with pytest.raises(ValueError, match="needs a field"):
        PrecipitationScale(**common, intercept=1.0)


def _ratio_lattice(path: Path, ratio: float) -> Path:
    import pandas as pd

    pd.DataFrame(
        {"lat": [43.0, 43.0, 43.2, 43.2], "lon": [11.0, 11.2, 11.0, 11.2], "ratio": ratio}
    ).to_csv(path, index=False)
    return path


def test_a_source_ratio_multiplies_only_that_sources_factor(tmp_path: Path) -> None:
    from api.model.config import PrecipitationScale

    scale = PrecipitationScale(
        enabled=True,
        sources=["cds", "seamless"],
        intercept=1.2,
        per_km=0.0,
        max_elevation_m=1000,
        source_ratios={"cds": str(_ratio_lattice(tmp_path / "r.csv", 0.9))},
        confidence="c",
        source=["s"],
        notes="",
    )
    z, lon, lat = np.array([500.0]), np.array([11.1]), np.array([43.1])

    assert scale.factor(z, lon, lat, source="cds").tolist() == pytest.approx([1.2 * 0.9])
    assert scale.factor(z, lon, lat, source="seamless").tolist() == pytest.approx([1.2])
    assert scale.factor(z, lon, lat).tolist() == pytest.approx([1.2])


def test_a_source_ratio_must_name_a_scaled_source() -> None:
    from api.model.config import PrecipitationScale

    with pytest.raises(ValueError, match="other.*not a scaled source"):
        PrecipitationScale(
            enabled=True,
            sources=["cds"],
            field="f.csv",
            source_ratios={"other": "r.csv"},
            confidence="c",
            source=["s"],
            notes="",
        )


def test_era5_seamless_rain_is_brought_to_the_cds_level_the_field_was_fitted_on() -> None:
    scale = load_model_config().precipitation_scale
    # Inland Sicily, where era5_seamless rain runs about 10 % below CDS ERA5-Land.
    z, lon, lat = np.array([500.0]), np.array([14.2]), np.array([37.6])

    cds = scale.factor(z, lon, lat, source="era5_land_cds")
    seamless = scale.factor(z, lon, lat, source="era5_seamless")

    assert 1.03 < (seamless / cds)[0] < 1.35


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
