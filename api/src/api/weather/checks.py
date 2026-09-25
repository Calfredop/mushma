"""Checks behind the weather config, reproducible from cached data.

    uv run python -m api.weather.checks lattice   # lapse rates and the 0.2° lattice leave-out test
    uv run python -m api.weather.checks gauges --start 2025-01-01 --end 2026-09-06
    uv run python -m api.weather.checks cds_vs_seamless --region tuscany --year 2024

``lattice`` re-fetches (from the cache, when present) three 14-day windows of 2024 for every 0.1°
ERA5-Land land node, estimates the cooling rate with height across nodes, and predicts the nodes a
coarser lattice skips from the ones it keeps. ``gauges`` compares downscaled rain in woodland cells
with the regional network's gauges inside them (SIR Toscana for Tuscany, ARPA Liguria for Liguria,
the Servizio Idrografico for Umbria, ARPA Piemonte for Piemonte: ``GAUGE_NETWORKS``). Results land
in ``$DATA_DIR/weather/<region>/checks/``.
"""

import argparse
import json
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import date, timedelta
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from pyproj import Transformer

from api.grid.region import load_region
from api.grid.sources import fetch
from api.weather import arpa_piemonte, arpal, umbria_sir
from api.weather.config import load_weather_config
from api.weather.downscale import cell_weather
from api.weather.ingest import (
    build_points,
    history_requests,
    load_request,
    region_paths,
    request_points_of,
)
from api.weather.openmeteo import Client, RateBudget
from api.weather.points import interpolation_weights
from api.weather.sir import STATIONS_URL, gauge_day_totals, parse_series, parse_stations
from api.weather.store import WeatherStore

VALIDATION_WINDOWS = [
    (date(2024, 1, 8), date(2024, 1, 21)),
    (date(2024, 7, 8), date(2024, 7, 21)),
    (date(2024, 10, 14), date(2024, 10, 27)),
]
WET_MM = 10.0
ELEVATION_BANDS = [0, 400, 800, 3000]


def lapse_regression(
    daily: pd.DataFrame, nodes: pd.DataFrame, min_elevation_m: float | None = None
) -> pd.DataFrame:
    """Per variable and day, the cooling per km of height across nodes (OLS on height, lat, lon)."""
    data = daily.merge(nodes[["point_id", "lat", "lon", "z"]], on="point_id")
    if min_elevation_m is not None:
        data = data[data["z"] >= min_elevation_m]
    rows = []
    for (variable, day), group in data.groupby(["variable", "date"]):
        design = np.column_stack(
            [np.ones(len(group)), group["z"] / 1000, group["lat"], group["lon"]]
        )
        coef, *_ = np.linalg.lstsq(design, group["value"].to_numpy(), rcond=None)
        rows.append((variable, day, -coef[1]))
    return pd.DataFrame(rows, columns=["variable", "date", "cooling_per_km"])


def leave_out_errors(
    daily: pd.DataFrame,
    nodes: pd.DataFrame,
    stride: int,
    lapse_rates: dict[str, float],
    native_spacing_deg: float = 0.1,
) -> pd.DataFrame:
    """Predict the nodes a ``stride`` lattice skips from the ones it keeps; errors per variable."""
    index = np.round(nodes[["lat", "lon"]].to_numpy() / native_spacing_deg).astype(int)
    kept = (index % stride == 0).all(axis=1)
    lattice, targets = nodes[kept], nodes[~kept]
    weights = interpolation_weights(
        targets.rename(columns={"point_id": "cell_id"}),
        lattice,
        round(native_spacing_deg * stride, 6),
        "bilinear",
    )
    z = nodes.set_index("point_id")["z"]
    weights["z"] = weights["point_id"].map(z)
    reference = weights.assign(wz=weights["weight"] * weights["z"]).groupby("cell_id")["wz"].sum()
    target_z = z.reindex(reference.index)
    rows = {}
    for variable, group in daily.groupby("variable"):
        wide = group.pivot(index="date", columns="point_id", values="value")
        matrix = weights.pivot_table(
            index="cell_id", columns="point_id", values="weight", fill_value=0
        ).reindex(columns=wide.columns, fill_value=0)
        predicted = wide.fillna(0).to_numpy() @ matrix.to_numpy().T
        predicted = pd.DataFrame(predicted, index=wide.index, columns=matrix.index)
        rate = lapse_rates.get(variable, 0.0) / 1000
        predicted += rate * (reference - target_z).reindex(matrix.index).to_numpy()
        errors = (predicted - wide[matrix.index]).stack()
        rows[variable] = {
            "rmse": float(np.sqrt((errors**2).mean())),
            "mae": float(errors.abs().mean()),
            "bias": float(errors.mean()),
            "targets": int(len(matrix.index)),
            "n": int(errors.size),
        }
    return pd.DataFrame.from_dict(rows, orient="index")


def compare_gauge(
    model_calendar: pd.Series,
    gauge: pd.Series,
    day_totals: Callable[[pd.Series], pd.Series] = gauge_day_totals,
) -> dict:
    """Downscaled calendar-day rain against a gauge's days, re-cut by ``day_totals`` (SIR
    Toscana's 09:00-09:00 days by default)."""
    model = day_totals(model_calendar)
    days = model.index.intersection(gauge.index)
    model, gauge = model[days], gauge[days]
    full = pd.Index(
        [days.min() + timedelta(days=i) for i in range((days.max() - days.min()).days + 1)]
    )
    model3 = model.reindex(full).rolling(3).sum()
    gauge3 = gauge.reindex(full).rolling(3).sum()
    valid = model3.notna() & gauge3.notna()
    wet = valid & (gauge3 >= WET_MM)
    dry = valid & (gauge3 < WET_MM)
    return {
        "days": int(len(days)),
        "gauge_mm": float(gauge.sum()),
        "model_mm": float(model.sum()),
        "ratio": float(model.sum() / gauge.sum()) if gauge.sum() > 0 else float("nan"),
        "daily_corr": float(model.corr(gauge)),
        "wet3_windows": int(wet.sum()),
        "wet3_hit_rate": float((model3[wet] >= WET_MM).mean()) if wet.any() else float("nan"),
        "wet3_false_alarm": float((model3[dry] >= WET_MM).mean()) if dry.any() else float("nan"),
        "wet3_mae": float((model3[wet] - gauge3[wet]).abs().mean()) if wet.any() else float("nan"),
    }


def _client(raw: Path) -> Client:
    config = load_weather_config()
    budget = RateBudget(
        per_minute=config.budget.per_minute,
        per_hour=config.budget.per_hour,
        per_day=config.budget.per_day,
        ledger=raw / "open_meteo" / "usage.json",
    )
    return Client(cache_dir=raw / "open_meteo", budget=budget)


def run_lattice(region_id: str) -> None:
    region = load_region(region_id)
    grid_dir, store, raw = region_paths(region.id)
    out = store.root / "checks"
    config = load_weather_config()
    native = replace(config, points=replace(config.points, stride=1))
    check_store = WeatherStore(out / "lattice")
    client = _client(raw)
    cells = pd.read_parquet(
        grid_dir / "cells.parquet", columns=["cell_id", "lon", "lat", "elevation_m", "woodland"]
    )
    points = build_points(client, native, region.timezone, cells, check_store, print)
    for start, end in VALIDATION_WINDOWS:
        for request in history_requests(
            native, request_points_of(points), region.timezone, start, end
        ):
            load_request(client, check_store, request, None)
    heights = check_store.read_point_cells().query("source == @config.history.model")
    nodes = points[points["land"]].merge(
        heights[["point_id", "elevation_m"]].rename(columns={"elevation_m": "z"}), on="point_id"
    )
    daily = duckdb.sql(
        f"SELECT point_id, date, variable, value FROM read_parquet('{check_store.daily_glob}')"
    ).df()
    daily["date"] = pd.to_datetime(daily["date"]).dt.date

    rates = lapse_regression(daily, nodes)
    rates["month"] = pd.to_datetime(rates["date"]).dt.month
    summary = rates.pivot_table(
        index="variable", columns="month", values="cooling_per_km", aggfunc="median"
    )
    summary["all"] = rates.groupby("variable")["cooling_per_km"].median()
    print("cooling per km of height across nodes (median of daily fits):")
    print(summary.round(2).to_string())

    regional = {
        name: v.lapse_rate_c_per_km
        for name, v in config.variables.items()
        if v.lapse_rate_c_per_km is not None
    }
    tables = []
    for stride in (2, 3):
        for label, rates_used in (
            ("none", {}),
            ("6.5", dict.fromkeys(regional, 6.5)),
            ("config", regional),
        ):
            table = leave_out_errors(daily, nodes, stride, rates_used)
            tables.append(table.assign(stride=stride, lapse=label))
    errors = pd.concat(tables).rename_axis("variable").reset_index()
    print(f"\nleave-out errors vs the full 0.1° field ({len(nodes)} land nodes):")
    print(errors.round(3).to_string(index=False))
    out.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out / "lapse_rates.csv")
    errors.to_csv(out / "lattice_errors.csv", index=False)


@dataclass(frozen=True)
class GaugeNetwork:
    """A region's rain gauges: one row per gauge (``code``, ``name``, ``elevation_m``, ``lon``,
    ``lat``), each gauge's daily rain, and how the network cuts its days."""

    gauges: pd.DataFrame
    series: Callable[[object], pd.Series]
    day_totals: Callable[[pd.Series], pd.Series]


def sir_toscana(raw: Path, start: date, end: date) -> GaugeNetwork:
    """SIR Toscana: open JSON per station, 09:00-09:00 days."""
    sir = raw / "sir_toscana"
    stations = json.loads(fetch(STATIONS_URL, sir / "stations.json").read_text())
    years = {str(y) for y in range(start.year, end.year + 1)}

    def series(gauge: object) -> pd.Series:
        path = fetch(gauge.url, sir / f"{gauge.code}.json")
        return parse_series(json.loads(path.read_text()))

    return GaugeNetwork(parse_stations(stations, years), series, gauge_day_totals)


def arpa_liguria(raw: Path, start: date, end: date) -> GaugeNetwork:
    """ARPA Liguria (OMIRL): a regional CSV per year, UTC days (api.weather.arpal)."""
    cache = raw / "arpal"
    report = pd.concat(
        [
            arpal.parse_daily_report(arpal.fetch_daily_report(year, cache).read_text())
            for year in range(start.year, end.year + 1)
        ],
        ignore_index=True,
    )
    stations = arpal.parse_station_list(arpal.fetch_station_list(cache).read_text())
    omirl_path = fetch(arpal.OMIRL_STATIONS_URL, cache / "omirl_pluvio.json")
    omirl = arpal.parse_omirl_stations(json.loads(omirl_path.read_text()))
    by_name = {
        name: rows.set_index("date")["rain_mm"] for name, rows in report.groupby("station_name")
    }
    return GaugeNetwork(
        arpal.gauge_stations(report, stations, omirl),
        lambda gauge: by_name[gauge.name],
        arpal.utc_day_totals,
    )


def calendar_days(calendar: pd.Series) -> pd.Series:
    """Gauge days that are the model's own local calendar days."""
    return calendar


def umbria_sir_network(raw: Path, start: date, end: date) -> GaugeNetwork:
    """Regione Umbria Servizio Idrografico: open daily CSVs (history zip + current year), no
    station heights (run_gauges takes the gauge cell's), calendar days (api.weather.umbria_sir)."""
    folder = raw / "umbria_sir"
    frames = [
        umbria_sir.parse_daily(fetch(umbria_sir.HISTORY_URL, folder / "storico_giornalieri.zip"))
    ]
    if end.year >= date.today().year:
        current = fetch(umbria_sir.CURRENT_YEAR_URL, folder / "anno_corrente_giornalieri.csv")
        frames.append(umbria_sir.parse_daily(current))
    daily = pd.concat(frames, ignore_index=True).drop_duplicates(["code", "date"], keep="last")
    return GaugeNetwork(
        umbria_sir.gauges_covering(daily, start, end),
        lambda gauge: umbria_sir.series_of(daily, gauge.code),
        calendar_days,
    )


def arpa_piemonte_network(raw: Path, start: date, end: date) -> GaugeNetwork:
    """ARPA Piemonte: open REST API, stations with heights, one series per measuring point
    fetched only for the gauges in woodland cells, UTC days (api.weather.arpa_piemonte)."""
    folder = raw / "arpa_piemonte"
    stations = json.loads(fetch(arpa_piemonte.STATIONS_URL, folder / "stations.json").read_text())

    def series(gauge: object) -> pd.Series:
        return arpa_piemonte.parse_daily(arpa_piemonte.fetch_daily(gauge.code, start, end, folder))

    return GaugeNetwork(arpa_piemonte.parse_stations(stations), series, arpal.utc_day_totals)


GAUGE_NETWORKS: dict[str, Callable[[Path, date, date], GaugeNetwork]] = {
    "tuscany": sir_toscana,
    "liguria": arpa_liguria,
    "umbria": umbria_sir_network,
    "piemonte": arpa_piemonte_network,
}


def run_gauges(region_id: str, start: date, end: date) -> None:
    region = load_region(region_id)
    if region.id not in GAUGE_NETWORKS:
        raise SystemExit(f"no rain gauge network wired for {region.id!r} (GAUGE_NETWORKS)")
    grid_dir, store, raw = region_paths(region.id)
    config = load_weather_config()
    network = GAUGE_NETWORKS[region.id](raw, start, end)
    gauges = network.gauges.copy()
    to_laea = Transformer.from_crs(4326, region.grid.crs, always_xy=True)
    x, y = to_laea.transform(gauges["lon"].to_numpy(), gauges["lat"].to_numpy())
    size = region.grid.cell_size_m
    gauges["cell_id"] = [
        f"1kmE{int(a // size)}N{int(b // size)}" for a, b in zip(x, y, strict=True)
    ]
    cells = pd.read_parquet(grid_dir / "cells.parquet", columns=["cell_id", "elevation_m"])
    if "elevation_m" not in gauges.columns:
        # A network without station heights (Umbria): band each gauge by its cell's DEM height.
        gauges = gauges.merge(cells, on="cell_id", how="left")
    weights = pd.read_parquet(store.weights_path)
    gauges = gauges[gauges["cell_id"].isin(weights["cell_id"])]
    # The reanalysis the model scores with: CDS where stored, else the Open-Meteo archive.
    reanalysis = [s for s in config.source_order if s != config.forecast.model]
    con = duckdb.connect()
    model = cell_weather(
        con,
        store,
        cells[cells["cell_id"].isin(gauges["cell_id"])],
        weights,
        start - timedelta(days=1),
        end + timedelta(days=1),
        {"precipitation_sum": config.variables["precipitation_sum"]},
        reanalysis,
    ).df()
    model["date"] = pd.to_datetime(model["date"]).dt.date
    rows = []
    for gauge in gauges.itertuples():
        series = network.series(gauge)
        series = series[(series.index >= start) & (series.index <= end)]
        cell = model[model["cell_id"] == gauge.cell_id].set_index("date")["value"]
        if cell.empty or len(series) < 0.8 * ((end - start).days + 1):
            continue
        rows.append(
            {
                "code": gauge.code,
                "name": gauge.name,
                "elevation_m": gauge.elevation_m,
                "cell_id": gauge.cell_id,
                **compare_gauge(cell, series, network.day_totals),
            }
        )
    results = pd.DataFrame(rows)
    results["band"] = pd.cut(results["elevation_m"], ELEVATION_BANDS, right=False)
    by_band = results.groupby("band", observed=True).agg(
        gauges=("code", "size"),
        pooled_ratio=("model_mm", "sum"),
        gauge_mm=("gauge_mm", "sum"),
        median_ratio=("ratio", "median"),
        median_daily_corr=("daily_corr", "median"),
        wet3_hit_rate=("wet3_hit_rate", "median"),
        wet3_false_alarm=("wet3_false_alarm", "median"),
        wet3_mae=("wet3_mae", "median"),
    )
    by_band["pooled_ratio"] = by_band["pooled_ratio"] / by_band.pop("gauge_mm")
    overall = compare_overall(results)
    print(f"{len(results)} woodland gauges, {start} to {end}")
    print(by_band.round(3).to_string())
    print(json.dumps(overall, indent=2))
    out = store.root / "checks"
    out.mkdir(parents=True, exist_ok=True)
    results.to_csv(out / f"gauges_{start:%Y%m%d}_{end:%Y%m%d}.csv", index=False)


def compare_overall(results: pd.DataFrame) -> dict:
    return {
        "gauges": int(len(results)),
        "pooled_ratio": round(float(results["model_mm"].sum() / results["gauge_mm"].sum()), 3),
        "median_ratio": round(float(results["ratio"].median()), 3),
        "median_daily_corr": round(float(results["daily_corr"].median()), 3),
        "median_wet3_hit_rate": round(float(results["wet3_hit_rate"].median()), 3),
        "median_wet3_false_alarm": round(float(results["wet3_false_alarm"].median()), 3),
        "median_wet3_mae_mm": round(float(results["wet3_mae"].median()), 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("check", choices=["lattice", "gauges", "cds_vs_seamless"])
    parser.add_argument("--region", default="tuscany")
    parser.add_argument("--start", type=date.fromisoformat, default=date(2025, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date(2025, 12, 31))
    parser.add_argument("--year", type=int, default=2024)
    args = parser.parse_args()
    if args.check == "lattice":
        run_lattice(args.region)
    elif args.check == "gauges":
        run_gauges(args.region, args.start, args.end)
    else:
        from api.weather.cds_compare import main_compare

        main_compare(args.region, args.year)


if __name__ == "__main__":
    main()
