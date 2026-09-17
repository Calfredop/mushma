from datetime import date

import pandas as pd
import pytest

from api.model.sanity import (
    AREAS,
    CONTRASTS,
    Area,
    Contrast,
    Window,
    area_cells,
    evaluate_contrasts,
    fix_mojibake,
)

CELLS = pd.DataFrame(
    {
        "cell_id": ["a", "b", "c", "d"],
        "comune_name": ["Poppi", "Castel San NiccolÃ²", "Arezzo", "Pontremoli"],
        "province": ["AR", "AR", "AR", "MS"],
        "woodland": [True, True, True, True],
    }
)


def test_fix_mojibake_recovers_utf8_read_as_latin1_and_leaves_clean_names() -> None:
    assert fix_mojibake("Castel San NiccolÃ²") == "Castel San Niccolò"
    assert fix_mojibake("Poppi") == "Poppi"
    assert fix_mojibake("Città") == "Città"


def test_area_cells_by_comune_or_by_province_minus_comuni() -> None:
    casentino = Area(comuni=["Poppi", "Castel San Niccolò"])
    rest = Area(provinces=["AR"], excluding=["Poppi", "Castel San Niccolò"])

    assert area_cells(CELLS, casentino) == {"a", "b"}
    assert area_cells(CELLS, rest) == {"c"}
    assert area_cells(CELLS, Area(provinces=["*"])) == {"a", "b", "c", "d"}


def _scores(rows: list[tuple[str, date, float]]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["cell_id", "date", "score"])


def test_a_contrast_holds_when_the_higher_window_scores_higher() -> None:
    areas = {
        "casentino": Area(comuni=["Poppi"]),
        "rest": Area(provinces=["AR"], excluding=["Poppi"]),
    }
    contrast = Contrast(
        id="t",
        claim="Casentino beat the rest of Arezzo",
        source="https://example.org",
        higher=Window("casentino", [2023], "09-15", "10-31"),
        lower=Window("rest", [2023], "09-15", "10-31"),
    )
    scores = _scores(
        [
            ("a", date(2023, 9, 20), 0.8),
            ("a", date(2023, 11, 20), 0.0),  # outside the window
            ("c", date(2023, 9, 20), 0.3),
            ("b", date(2023, 9, 20), 0.1),
        ]
    )

    (row,) = evaluate_contrasts([contrast], scores, CELLS, areas).to_dict("records")

    assert row["higher_mean"] == pytest.approx(0.8)
    assert row["lower_mean"] == pytest.approx(0.2)  # cells b and c
    assert row["holds"]


def test_a_window_over_several_seasons_averages_them_as_a_normal() -> None:
    areas = {"casentino": Area(comuni=["Poppi"])}
    contrast = Contrast(
        id="t",
        claim="2024 above normal",
        source="x",
        higher=Window("casentino", [2024], "09-01", "09-30"),
        lower=Window("casentino", [2022, 2023, 2024], "09-01", "09-30"),
    )
    scores = _scores(
        [
            ("a", date(2022, 9, 5), 0.2),
            ("a", date(2023, 9, 5), 0.2),
            ("a", date(2024, 9, 5), 0.5),
        ]
    )

    (row,) = evaluate_contrasts([contrast], scores, CELLS, areas).to_dict("records")

    assert row["lower_mean"] == pytest.approx(0.3) and row["holds"]


def test_the_pre_registered_contrasts_name_known_areas_and_cite_a_source() -> None:
    assert len(CONTRASTS) >= 8
    for contrast in CONTRASTS:
        assert contrast.higher.area in AREAS and contrast.lower.area in AREAS
        assert contrast.source.startswith("http")
