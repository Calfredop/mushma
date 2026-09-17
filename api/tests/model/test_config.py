from pathlib import Path

import numpy as np
import pytest
import yaml

from api.model.config import MODEL_FILE, load_model_config
from api.model.rules import RuleConfigError, load_rules


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
