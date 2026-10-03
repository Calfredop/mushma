from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from api.model.rain_field import load_rain_field


def _write_field(path: Path) -> Path:
    # A 2 x 2 lattice: intercept rises eastward, slope northward.
    pd.DataFrame(
        {
            "lat": [43.0, 43.0, 43.5, 43.5],
            "lon": [11.0, 11.5, 11.0, 11.5],
            "intercept": [1.0, 2.0, 1.0, 2.0],
            "per_km": [0.0, 0.0, 1.0, 1.0],
            "max_elevation_m": [1000, 1000, 1000, 1000],
        }
    ).to_csv(path, index=False)
    return path


def test_the_field_is_exact_on_its_nodes(tmp_path: Path) -> None:
    field = load_rain_field(_write_field(tmp_path / "f.csv"))

    factor = field.factor(np.array([500.0, 500.0]), np.array([11.0, 11.5]), np.array([43.5, 43.0]))

    assert factor.tolist() == pytest.approx([1.5, 2.0])


def test_the_field_interpolates_between_nodes_and_clamps_height(tmp_path: Path) -> None:
    field = load_rain_field(_write_field(tmp_path / "f.csv"))

    # Centre of the square: intercept 1.5, per_km 0.5; 3000 m is clamped to 1000 m.
    factor = field.factor(np.array([0.0, 3000.0]), np.array([11.25, 11.25]), np.array([43.25] * 2))

    assert factor.tolist() == pytest.approx([1.5, 2.0])


def test_points_off_the_lattice_take_the_nearest_edge(tmp_path: Path) -> None:
    field = load_rain_field(_write_field(tmp_path / "f.csv"))

    factor = field.factor(np.array([np.nan]), np.array([20.0]), np.array([40.0]))

    assert factor.tolist() == pytest.approx([2.0])  # south-east corner, unknown height = 0 m


def test_a_lattice_of_any_named_value_reads_bilinearly(tmp_path: Path) -> None:
    path = tmp_path / "r.csv"
    pd.DataFrame(
        {
            "lat": [43.0, 43.0, 43.2, 43.2],
            "lon": [11.0, 11.2, 11.0, 11.2],
            "ratio": [1.0, 1.0, 0.8, 0.8],
        }
    ).to_csv(path, index=False)

    ratio = load_rain_field(path).value("ratio", np.array([11.1, 11.0]), np.array([43.1, 43.2]))

    assert ratio.tolist() == pytest.approx([0.9, 0.8])


def test_the_rules_version_changes_when_the_rain_field_is_refitted(tmp_path: Path) -> None:
    import shutil

    from api.model.config import CONFIG_DIR, MODEL_FILE
    from api.model.pipeline import rules_version

    config = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, config)
    model_file = config / MODEL_FILE.name
    species = config / "species"
    before = rules_version("tuscany", species_dir=species, model_file=model_file)

    field = config / "rain_scale_field.csv"
    field.write_text(field.read_text().replace("0.95", "0.96", 1))

    assert rules_version("tuscany", species_dir=species, model_file=model_file) != before


def test_the_rules_version_changes_when_a_source_ratio_is_refitted(tmp_path: Path) -> None:
    import shutil

    from api.model.config import CONFIG_DIR, MODEL_FILE
    from api.model.pipeline import rules_version

    config = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, config)
    model_file = config / MODEL_FILE.name
    species = config / "species"
    before = rules_version("tuscany", species_dir=species, model_file=model_file)

    ratios = config / "rain_cds_per_seamless.csv"
    ratios.write_text(ratios.read_text() + "\n")

    assert rules_version("tuscany", species_dir=species, model_file=model_file) != before
