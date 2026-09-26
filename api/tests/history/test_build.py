"""The history pipeline end to end over a small synthetic $DATA_DIR (tests/history/helpers.py)."""

import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from api.history.build import build_normals, build_outlook_areas, update_history
from api.history.store import ClimatologyStore, HistoryStore
from api.model.config import load_model_config
from api.model.rules import load_rules
from api.weather.config import load_weather_config
from tests.history.helpers import (
    A1,
    A2,
    B1,
    REGION,
    write_grid,
    write_points,
    write_scores,
    write_seasonal,
    write_sightings,
    write_weather,
)

RAIN = {"P": 2.0, "Q": 4.0}
TEMPERATURE = {"P": 10.0, "Q": 12.0}


def _porcini(cell: str, day: date) -> float:
    if cell == A1 and date(2025, 10, 1) <= day <= date(2025, 10, 10):
        return 0.8
    if cell == B1 and date(2025, 9, 1) <= day <= date(2025, 9, 5):
        return 0.7
    return 0.1


@pytest.fixture
def root(tmp_path: Path) -> Path:
    write_grid(tmp_path)
    write_points(tmp_path)
    for year in (2024, 2025):
        write_weather(
            tmp_path, date(year, 1, 1), date(year, 12, 31), rain=RAIN, temperature=TEMPERATURE
        )
    write_scores(tmp_path, "porcini", date(2025, 1, 1), date(2025, 12, 31), _porcini)
    write_scores(tmp_path, "combined", date(2025, 1, 1), date(2025, 12, 31), _porcini)
    for key in ("ovoli", "gallinacci"):
        write_scores(tmp_path, key, date(2025, 1, 1), date(2025, 12, 31), lambda c, d: 0.2)
    write_sightings(
        tmp_path,
        [
            ("porcini", A1, date(2025, 10, 2), False),
            ("porcini", B1, date(2025, 10, 3), True),  # obscured: region only
        ],
    )
    return tmp_path


def _cell_rain(elevation: float, point_rain: float) -> float:
    return point_rain * float(load_model_config().precipitation_scale.factor([elevation])[0])


def _cell_temperature(point_temperature: float, point_height: float, elevation: float) -> float:
    lapse = load_weather_config().variables["temperature_2m_mean"].lapse_rate_c_per_km
    return point_temperature + lapse / 1000 * (point_height - elevation)


def test_normals_use_the_complete_reanalysis_years(root: Path) -> None:
    summary = build_normals(REGION, root)

    assert summary["years"] == [2024, 2025]
    normals = ClimatologyStore(root / "climatology" / REGION).read_normals()
    assert len(normals) == 2 * 2 * 365
    rain = normals[(normals["variable"] == "precipitation_sum") & (normals["point_id"] == "Q")]
    assert rain["normal"].tolist() == pytest.approx([4.0] * 365)


def test_update_writes_season_stats_per_area(root: Path) -> None:
    build_normals(REGION, root)

    update_history(REGION, [2025], root)

    store = HistoryStore(root / "history" / REGION)
    areas = store.read_areas().set_index("area_code")
    assert set(areas.index) == {REGION, "048001", "053002"}
    assert areas.loc["048001", "cells"] == 2

    seasons = store.read_seasons()
    porcini = seasons[(seasons["species"] == "porcini") & (seasons["year"] == 2025)].set_index(
        "area_code"
    )
    assert porcini.loc["048001", "good_days"] == pytest.approx(5.0)  # 10 days on 1 of 2 cells
    assert porcini.loc["053002", "good_days"] == pytest.approx(5.0)
    assert porcini.loc[REGION, "good_days"] == pytest.approx(15 / 3)
    assert porcini.loc["048001", "peak_date"] == date(2025, 10, 1)
    assert bool(porcini.loc["048001", "complete"]) is True

    # Rain over porcini's season window, through the same weights as the downscaling.
    window_days = (
        porcini.loc["048001", "window_end"] - porcini.loc["048001", "window_start"]
    ).days + 1
    alpha_daily = (_cell_rain(500.0, 3.0) + _cell_rain(700.0, 4.0)) / 2
    assert porcini.loc["048001", "rain_mm"] == pytest.approx(window_days * alpha_daily)
    assert porcini.loc["048001", "rain_normal_mm"] == pytest.approx(window_days * alpha_daily)
    alpha_temperature = (
        _cell_temperature(11.0, 500.0, 500.0) + _cell_temperature(12.0, 600.0, 700.0)
    ) / 2
    assert porcini.loc["048001", "temp_c"] == pytest.approx(alpha_temperature)
    assert porcini.loc["053002", "temp_c"] == pytest.approx(_cell_temperature(10.0, 400.0, 300.0))

    assert porcini.loc["048001", "sightings"] == 1
    assert porcini.loc["053002", "sightings"] == 0  # the obscured record stays out of its comune
    assert porcini.loc[REGION, "sightings"] == 2

    months = store.read_months()
    october = months[
        (months["species"] == "porcini")
        & (months["area_code"] == "048001")
        & (months["month"] == 10)
    ].iloc[0]
    assert october["good_days"] == pytest.approx(5.0)
    assert october["sightings"] == 1


def test_update_keeps_good_days_per_cell_for_the_season_map(root: Path) -> None:
    build_normals(REGION, root)
    update_history(REGION, [2025], root)

    cells = HistoryStore(root / "history" / REGION).read_cell_seasons(2025, "porcini")

    assert cells.set_index("cell_id")["good_days"].to_dict() == {A1: 10, A2: 0, B1: 5}


def test_update_writes_each_areas_plausible_species(root: Path) -> None:
    build_normals(REGION, root)
    update_history(REGION, [2025], root)

    fit = HistoryStore(root / "history" / REGION).read_area_fit()

    rules = load_rules()
    assert set(fit["species"]) == {*rules.species, *rules.groups}
    assert set(fit["area_code"]) == {REGION, "048001", "053002"}
    assert fit["fit_share"].between(0, 1).all()
    table = fit.set_index(["area_code", "species"])
    # Beta is Turkey oak at 300 m: the ovolo's lead host, in its altitude band.
    assert table.loc[("053002", "ovoli"), "fit_share"] == pytest.approx(1.0)
    assert table.loc[("053002", "ovoli_caesarea"), "fit_share"] == pytest.approx(1.0)
    assert table.loc[(REGION, "ovoli"), "cells"] == 3


def test_update_keeps_each_taxons_season_good_days(root: Path) -> None:
    write_scores(root, "porcini_edulis", date(2025, 1, 1), date(2025, 12, 31), _porcini)
    build_normals(REGION, root)
    update_history(REGION, [2025], root)

    store = HistoryStore(root / "history" / REGION)
    taxa = store.read_taxon_seasons("048001")

    assert taxa[["species", "year"]].values.tolist() == [["porcini_edulis", 2025]]
    assert taxa.iloc[0]["good_days"] == pytest.approx(5.0)  # 10 days on 1 of 2 cells
    assert taxa.iloc[0]["through"] == date(2025, 12, 31)
    meta = store.read_meta()
    assert meta["plausible_fit"] == pytest.approx(0.5)
    assert meta["groups"]["porcini"][0] in meta["taxa"]
    assert meta["taxa"]["porcini_edulis"]["taxon"] == "Boletus edulis"


def test_update_records_which_years_the_baselines_used(root: Path) -> None:
    build_normals(REGION, root)

    update_history(REGION, [2025], root)

    meta = json.loads((root / "history" / REGION / "meta.json").read_text())
    assert meta["weather_years"] == [2024, 2025]
    assert meta["score_years"] == [2025]
    assert meta["good_score"] > 0
    assert set(meta["windows"]) == {"porcini", "ovoli", "gallinacci", "combined"}
    # The outlook's rain lead per species, from the rule files' rain_event lags.
    assert set(meta["rain_lead"]) == {"porcini", "ovoli", "gallinacci"}
    assert all(low <= high for low, high in meta["rain_lead"].values())


def test_update_without_normals_builds_them_first(root: Path) -> None:
    update_history(REGION, [2025], root)

    assert ClimatologyStore(root / "climatology" / REGION).normals_path.exists()


def test_area_days_and_weather_are_kept_per_year(root: Path) -> None:
    update_history(REGION, [2025], root)
    store = HistoryStore(root / "history" / REGION)

    days = store.read_area_days(species="porcini", area_code="048001")
    weather = store.read_area_weather(years=[2025], area_code="053002")

    assert len(days) == 365
    assert set(days["good_cells"]) == {0, 1}
    assert len(weather) == 365
    assert weather["precipitation_normal"].iloc[0] == pytest.approx(_cell_rain(300.0, 2.0))
    assert not weather["forecast"].any()


def test_outlook_areas_average_the_long_range_forecast(root: Path) -> None:
    update_history(REGION, [2025], root)
    week = {"kind": "week", "start": date(2026, 9, 28), "end": date(2026, 10, 4)}
    write_seasonal(
        root,
        [
            {
                **week,
                "source": "ecmwf_seasonal",
                "point_id": "P",
                "variable": "precipitation_sum",
                "value": 10.0,
                "anomaly": -2.0,
                "fetched_at": pd.Timestamp("2026-09-18", tz="UTC"),
            },
            {
                **week,
                "source": "ecmwf_seasonal",
                "point_id": "Q",
                "variable": "precipitation_sum",
                "value": 20.0,
                "anomaly": 4.0,
                "fetched_at": pd.Timestamp("2026-09-18", tz="UTC"),
            },
        ],
    )

    build_outlook_areas(REGION, root)

    seasonal = HistoryStore(root / "history" / REGION).read_area_seasonal()
    alpha = seasonal[seasonal["area_code"] == "048001"].iloc[0]
    assert alpha["value"] == pytest.approx(0.25 * 10 + 0.75 * 20)
    assert alpha["anomaly"] == pytest.approx(0.25 * -2 + 0.75 * 4)
    assert alpha["start"] == date(2026, 9, 28)


def test_history_stops_at_yesterday_leaving_the_forecast_days_out(root: Path) -> None:
    update_history(REGION, [2025], root, today=date(2025, 10, 5))

    store = HistoryStore(root / "history" / REGION)
    days = store.read_area_days(species="porcini", area_code="048001")
    assert max(days["date"]) == date(2025, 10, 4)
    seasons = store.read_seasons()
    alpha = seasons[(seasons["species"] == "porcini") & (seasons["area_code"] == "048001")].iloc[0]
    assert alpha["good_days"] == pytest.approx(2.0)  # A1's 1-4 October, of its 1-10
    assert bool(alpha["complete"]) is False


def test_update_refreshes_the_normals_as_the_backfill_adds_years(root: Path) -> None:
    build_normals(REGION, root)  # 2024 and 2025
    # The backfill then reaches 2023.
    write_weather(root, date(2023, 1, 1), date(2023, 12, 31), rain=RAIN, temperature=TEMPERATURE)

    update_history(REGION, [2025], root)

    meta = ClimatologyStore(root / "climatology" / REGION).read_meta()
    assert meta["years"] == [2023, 2024, 2025]


def test_a_comune_whose_woodland_has_no_weather_is_not_listed(root: Path) -> None:
    cells_path = root / "grid" / REGION / "cells.parquet"
    cells = pd.read_parquet(cells_path)
    island = {
        **cells.iloc[0].to_dict(),
        "cell_id": "1kmE9000N9000",
        "x_min": 9_000_000,
        "y_min": 9_000_000,
        "comune_code": "053012",
        "comune_name": "Isola",
    }
    pd.concat([cells, pd.DataFrame([island])], ignore_index=True).to_parquet(
        cells_path, index=False
    )

    update_history(REGION, [2025], root)

    areas = HistoryStore(root / "history" / REGION).read_areas()
    assert "053012" not in set(areas["area_code"])


@pytest.fixture
def cds_root(tmp_path: Path) -> Path:
    """A region whose history is the CDS reanalysis only (every region after Tuscany)."""
    write_grid(tmp_path)
    write_points(tmp_path)
    cds = load_weather_config().cds.model
    for year in (2024, 2025):
        write_weather(
            tmp_path,
            date(year, 1, 1),
            date(year, 12, 31),
            rain=RAIN,
            temperature=TEMPERATURE,
            source=cds,
        )
    write_scores(tmp_path, "porcini", date(2025, 1, 1), date(2025, 12, 31), _porcini)
    write_scores(tmp_path, "combined", date(2025, 1, 1), date(2025, 12, 31), _porcini)
    for key in ("ovoli", "gallinacci"):
        write_scores(tmp_path, key, date(2025, 1, 1), date(2025, 12, 31), lambda c, d: 0.2)
    write_sightings(tmp_path, [])
    return tmp_path


def test_normals_come_from_the_cds_reanalysis_when_that_is_the_history(cds_root: Path) -> None:
    summary = build_normals(REGION, cds_root)

    assert summary["years"] == [2024, 2025]
    normals = ClimatologyStore(cds_root / "climatology" / REGION).read_normals()
    rain = normals[(normals["variable"] == "precipitation_sum") & (normals["point_id"] == "Q")]
    assert rain["normal"].tolist() == pytest.approx([4.0] * 365)


def test_cds_reanalysis_days_are_not_flagged_as_forecast(cds_root: Path) -> None:
    build_normals(REGION, cds_root)

    update_history(REGION, [2025], cds_root)

    weather = HistoryStore(cds_root / "history" / REGION).read_area_weather([2025])
    assert not weather["forecast"].any()
