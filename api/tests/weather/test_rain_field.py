import numpy as np
import pandas as pd
import pytest

from api.weather.rain_field import (
    block_cv,
    fit_field,
    global_fit,
    pseudo_gauges,
    weighted_quantile,
)


def _gauges(x_km, z_m, ratio) -> pd.DataFrame:
    x = np.asarray(x_km, dtype=float) * 1000
    return pd.DataFrame(
        {
            "network": "test",
            "x": x,
            "y": np.zeros_like(x),
            "elevation_m": np.asarray(z_m, dtype=float),
            "ratio": np.asarray(ratio, dtype=float),
        }
    )


def test_global_fit_recovers_intercept_and_slope() -> None:
    z = np.array([100.0, 400, 800, 1200, 1600])
    gauges = _gauges(np.arange(5) * 10, z, 0.9 + 0.3 * z / 1000)

    a, b = global_fit(gauges)

    assert (a, b) == pytest.approx((0.9, 0.3))


def test_a_wide_kernel_is_the_national_fit_and_a_narrow_one_follows_the_local_gauges() -> None:
    # Two networks 400 km apart that disagree: 1.4 in the west, 0.9 in the east, flat with height.
    west = _gauges(np.linspace(0, 40, 6), np.linspace(100, 1100, 6), np.full(6, 1.4))
    east = _gauges(np.linspace(400, 440, 6), np.linspace(100, 1100, 6), np.full(6, 0.9))
    gauges = pd.concat([west, east], ignore_index=True)
    nodes = pd.DataFrame({"x": [20_000.0, 420_000.0], "y": [0.0, 0.0]})

    wide = fit_field(gauges, nodes, bandwidth_m=1e7, ridge=0.0)
    narrow = fit_field(gauges, nodes, bandwidth_m=30_000, ridge=0.0)

    assert wide["intercept"].tolist() == pytest.approx([1.15, 1.15], abs=1e-3)
    assert narrow["intercept"].tolist() == pytest.approx([1.4, 0.9], abs=1e-3)
    assert narrow["per_km"].tolist() == pytest.approx([0.0, 0.0], abs=1e-3)


def test_the_ridge_pulls_a_node_with_few_nearby_gauges_toward_the_prior() -> None:
    # One lone gauge: without a ridge the slope is undetermined; with one it stays at the prior.
    gauges = _gauges([0.0], [500.0], [1.5])
    nodes = pd.DataFrame({"x": [0.0], "y": [0.0]})

    field = fit_field(gauges, nodes, bandwidth_m=50_000, ridge=1.0, prior=(1.0, 0.0))

    a, b = field.loc[0, ["intercept", "per_km"]]
    assert a + b * 0.5 == pytest.approx(1.25, abs=0.05)  # halfway between gauge and prior
    assert 1.0 < a < 1.5


def test_z_max_is_the_kernel_weighted_high_quantile_of_gauge_heights() -> None:
    gauges = _gauges(np.zeros(100), np.arange(100) * 20.0, np.ones(100))
    nodes = pd.DataFrame({"x": [0.0], "y": [0.0]})

    field = fit_field(gauges, nodes, bandwidth_m=50_000, ridge=0.0)

    assert field.loc[0, "max_elevation_m"] == pytest.approx(1900, abs=25)


def test_weighted_quantile_matches_the_plain_one_with_equal_weights() -> None:
    values = np.arange(101.0)

    assert weighted_quantile(values, np.ones(101), 0.95) == pytest.approx(95, abs=1)
    assert weighted_quantile(values, np.r_[np.zeros(100), 1.0], 0.5) == 100


def test_block_cv_prefers_the_narrow_kernel_when_regions_really_differ() -> None:
    rng = np.random.default_rng(0)
    frames = []
    for centre, level in ((0, 1.4), (300, 0.9), (600, 1.2)):
        x = centre + rng.uniform(0, 60, 30)
        z = rng.uniform(100, 1500, 30)
        frames.append(_gauges(x, z, level + 0.2 * z / 1000 + rng.normal(0, 0.03, 30)))
    gauges = pd.concat(frames, ignore_index=True)

    scores = block_cv(gauges, bandwidths_m=[40_000, 1e7], block_m=20_000, ridge=0.1)

    best = scores.sort_values("rmse_log").iloc[0]
    assert best["bandwidth_m"] == 40_000
    assert set(scores.columns) >= {"bandwidth_m", "rmse_log", "bias_log", "gauges"}


def test_pseudo_gauges_carry_the_published_fit_at_sampled_cells() -> None:
    cells = pd.DataFrame(
        {"lon": [15.0, 15.1, 15.2, 15.3], "lat": [40.0] * 4, "elevation_m": [50, 400, 900, 2000]}
    )

    pseudo = pseudo_gauges(
        cells, network="yearbook", intercept=1.0, per_km=0.5, low_m=0, high_m=1000, count=3, seed=1
    )

    assert len(pseudo) == 3
    assert pseudo["elevation_m"].max() <= 1000
    assert pseudo["ratio"].tolist() == pytest.approx(1.0 + 0.5 * pseudo["elevation_m"] / 1000)
    assert (pseudo["network"] == "yearbook").all()


def test_season_totals_compare_matched_days_in_the_season_only() -> None:
    from datetime import date, timedelta

    from api.weather.checks import calendar_days
    from api.weather.rain_field import season_totals

    days = [date(2025, 3, 1) + timedelta(days=i) for i in range(300)]
    model = pd.Series(1.0, index=days)
    gauge = pd.Series(2.0, index=days).drop(days[100:110])  # ten missing days in the season

    totals = season_totals(model, gauge, calendar_days, year=2025, min_coverage=0.8)

    season = [d for d in days if 4 <= d.month <= 11]
    assert totals["days"] == len(season) - 10
    assert totals["ratio"] == pytest.approx(2.0)
    assert totals["gauge_mm"] == pytest.approx(2.0 * totals["days"])


def test_season_totals_skip_a_gauge_with_too_few_days() -> None:
    from datetime import date, timedelta

    from api.weather.checks import calendar_days
    from api.weather.rain_field import season_totals

    days = [date(2025, 4, 1) + timedelta(days=i) for i in range(100)]
    series = pd.Series(1.0, index=days)

    assert season_totals(series, series, calendar_days, year=2025, min_coverage=0.8) is None


def test_a_gauge_gets_the_bilinear_weights_a_cell_would_on_the_scoring_lattice() -> None:
    from api.weather.rain_field import lattice_corners, lattice_weights

    gauge = pd.DataFrame({"code": ["g"], "lat": [43.05], "lon": [11.15]})

    corners = lattice_corners(gauge)
    weights = lattice_weights(gauge, set(corners) - {(43.2, 11.2)})  # one corner at sea

    assert corners == [(43.0, 11.0), (43.0, 11.2), (43.2, 11.0), (43.2, 11.2)]
    by_node = dict(zip(weights["node"], weights["weight"], strict=True))
    assert set(by_node) == {(43.0, 11.0), (43.0, 11.2), (43.2, 11.0)}
    assert sum(by_node.values()) == pytest.approx(1.0)
    assert by_node[(43.0, 11.2)] > by_node[(43.0, 11.0)] > by_node[(43.2, 11.0)]
