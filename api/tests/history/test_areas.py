from datetime import date

import numpy as np
import pandas as pd
import pytest

from api.history.areas import (
    aggregate_to_areas,
    area_members,
    area_point_weights,
    area_table,
    lapse_offsets,
)

REGION = "tuscany"


def _cells() -> pd.DataFrame:
    return pd.DataFrame(
        [
            # cell, woodland, comune, name, province, lon, lat, elevation
            ("c1", True, "048001", "Alpha", "FI", 11.0, 43.0, 500.0),
            ("c2", True, "048001", "Alpha", "FI", 11.2, 43.2, 700.0),
            ("c3", True, "053002", "Beta", "GR", 11.5, 42.8, 300.0),
            ("c4", False, "053002", "Beta", "GR", 11.6, 42.9, 10.0),  # not woodland
        ],
        columns=[
            "cell_id",
            "woodland",
            "comune_code",
            "comune_name",
            "province",
            "lon",
            "lat",
            "elevation_m",
        ],
    )


def _weights() -> pd.DataFrame:
    # c1 sits between points P and Q; c2 and c3 each use one point. Weights are not normalised
    # (the downscaling divides by their sum), so c1's 2:2 means half and half.
    return pd.DataFrame(
        [
            ("bilinear", "c1", "P", 2.0),
            ("bilinear", "c1", "Q", 2.0),
            ("bilinear", "c2", "Q", 1.0),
            ("bilinear", "c3", "R", 0.5),
            ("nearest", "c1", "P", 1.0),
        ],
        columns=["method", "cell_id", "point_id", "weight"],
    )


# --- area_members / area_table -----------------------------------------------------------------


def test_every_woodland_cell_belongs_to_its_comune_and_to_the_region() -> None:
    members = area_members(_cells(), REGION)

    by_area = members.groupby("area_code")["cell_id"].apply(sorted).to_dict()
    assert by_area == {"048001": ["c1", "c2"], "053002": ["c3"], REGION: ["c1", "c2", "c3"]}


def test_the_area_table_names_each_area_and_counts_its_woodland_cells() -> None:
    table = area_table(_cells(), REGION, "Toscana").set_index("area_code")

    assert table.loc[REGION, "kind"] == "region"
    assert table.loc[REGION, "name"] == "Toscana"
    assert table.loc[REGION, "cells"] == 3
    assert table.loc["048001", "kind"] == "comune"
    assert table.loc["048001", "name"] == "Alpha"
    assert table.loc["048001", "province"] == "FI"
    assert table.loc["048001", "cells"] == 2
    assert table.loc["048001", "lon"] == pytest.approx(11.1)
    assert table.loc["048001", "lat"] == pytest.approx(43.1)


# --- area_point_weights ------------------------------------------------------------------------


def test_area_weights_average_the_normalised_cell_weights() -> None:
    members = area_members(_cells(), REGION)

    weights = area_point_weights(members, _weights(), "bilinear")

    table = weights.pivot_table(index="area_code", columns="point_id", values="weight").fillna(0)
    # Alpha: c1 is half P, half Q; c2 is all Q -> P 0.25, Q 0.75.
    assert table.loc["048001"].to_dict() == pytest.approx({"P": 0.25, "Q": 0.75, "R": 0.0})
    assert table.loc["053002"].to_dict() == pytest.approx({"P": 0.0, "Q": 0.0, "R": 1.0})
    assert table.loc[REGION].to_dict() == pytest.approx({"P": 1 / 6, "Q": 1 / 2, "R": 1 / 3})


def test_a_per_cell_factor_scales_that_cells_share() -> None:
    members = area_members(_cells(), REGION)
    factor = pd.Series({"c1": 1.0, "c2": 2.0, "c3": 1.0})

    weights = area_point_weights(members, _weights(), "bilinear", cell_factor=factor)

    alpha = weights[weights["area_code"] == "048001"].set_index("point_id")["weight"]
    # (c1 0.5 P + 0.5 Q, c2 2 x Q) / 2 cells
    assert alpha.to_dict() == pytest.approx({"P": 0.25, "Q": 1.25})


def test_cells_without_weather_weights_are_left_out_of_the_area() -> None:
    cells = pd.concat(
        [_cells(), pd.DataFrame([{**_cells().iloc[0].to_dict(), "cell_id": "c5"}])],
        ignore_index=True,
    )
    members = area_members(cells, REGION)

    weights = area_point_weights(members, _weights(), "bilinear")

    alpha = weights[weights["area_code"] == "048001"].set_index("point_id")["weight"]
    assert alpha.sum() == pytest.approx(1.0)


# --- aggregate_to_areas ------------------------------------------------------------------------


def _values(*rows: tuple) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=["point_id", "date", "value"])


D1, D2 = date(2025, 10, 1), date(2025, 10, 2)


def test_an_area_value_is_the_weighted_mean_of_its_points() -> None:
    members = area_members(_cells(), REGION)
    weights = area_point_weights(members, _weights(), "bilinear")
    values = _values(("P", D1, 4.0), ("Q", D1, 8.0), ("R", D1, 1.0))

    out = aggregate_to_areas(values, weights).set_index(["area_code", "date"])["value"]

    assert out[("048001", D1)] == pytest.approx(0.25 * 4 + 0.75 * 8)
    assert out[("053002", D1)] == pytest.approx(1.0)
    # The region's value is the mean of its cells' downscaled values: c1 6, c2 8, c3 1.
    assert out[(REGION, D1)] == pytest.approx((6 + 8 + 1) / 3)


def test_a_missing_point_drops_out_and_the_rest_renormalise() -> None:
    members = area_members(_cells(), REGION)
    weights = area_point_weights(members, _weights(), "bilinear")
    values = _values(("P", D1, 4.0), ("Q", D1, 8.0), ("P", D2, 4.0), ("R", D2, 1.0))

    out = aggregate_to_areas(values, weights).set_index(["area_code", "date"])["value"]

    assert out[("048001", D2)] == pytest.approx(4.0)  # only P reported
    assert np.isnan(out[("053002", D1)])  # R did not report on D1


def test_scaled_rows_use_the_scaled_weights() -> None:
    members = area_members(_cells(), REGION)
    plain = area_point_weights(members, _weights(), "bilinear")
    doubled = area_point_weights(
        members, _weights(), "bilinear", cell_factor=pd.Series({"c1": 2.0, "c2": 2.0, "c3": 2.0})
    )
    values = _values(("R", D1, 1.0), ("R", D2, 1.0)).assign(scaled=[True, False])

    out = aggregate_to_areas(values, plain, scaled_weights=doubled)
    beta = out[out["area_code"] == "053002"].set_index("date")["value"]

    assert beta[D1] == pytest.approx(2.0)  # reanalysis rain, scaled by height
    assert beta[D2] == pytest.approx(1.0)  # forecast rain, left as it is


def test_an_offset_is_added_per_area() -> None:
    members = area_members(_cells(), REGION)
    weights = area_point_weights(members, _weights(), "bilinear")
    values = _values(("R", D1, 10.0))

    out = aggregate_to_areas(values, weights, offset=pd.Series({"053002": -1.5}))

    beta = out[out["area_code"] == "053002"]["value"].iloc[0]
    assert beta == pytest.approx(8.5)


# --- lapse_offsets -----------------------------------------------------------------------------


def test_the_lapse_offset_is_the_mean_cell_correction() -> None:
    members = area_members(_cells(), REGION)
    heights = pd.Series({"P": 400.0, "Q": 800.0, "R": 300.0})

    offsets = lapse_offsets(members, _weights(), "bilinear", _cells(), heights, lapse_c_per_km=5.0)

    # c1: points at 600 m mean, cell at 500 m -> +0.5 °C; c2: 800 vs 700 -> +0.5; c3: 300 vs 300.
    assert offsets["048001"] == pytest.approx(0.5)
    assert offsets["053002"] == pytest.approx(0.0)
    assert offsets[REGION] == pytest.approx(1 / 3)
