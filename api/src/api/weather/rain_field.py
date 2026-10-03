"""One rain calibration for all of Italy, fitted on every region's open gauges at once.

    uv run python -m api.weather.rain_field collect [--network tuscany ...]
    uv run python -m api.weather.rain_field cds [--region sicilia ...]
    uv run python -m api.weather.rain_field fit

The reanalysis rain is too dry or too wet by an amount that depends on place and height. Each region
used to fit its own ``intercept + per_km x elevation_km`` on its own gauges, and the fits disagree:
the same raw rain was scaled x1.41 on the Tuscan side of the Umbrian border and x0.99 twelve
kilometres away. This fits a field instead. At every node of a lattice over Italy, a local
``a + b x z`` is fitted by weighted least squares on gauge/reanalysis ratios, the weights a Gaussian
in distance with a ridge pull toward the national fit; its height clamp is the kernel-weighted 95th
percentile of the gauge heights around it. The kernel width is chosen by spatial-block
cross-validation (a very wide kernel is one national fit; a narrow one follows each network).

``collect`` compares each gauge's season totals (April to November, when the scores matter and
before snow undercatch) with CDS ERA5-Land rain downscaled to the gauge as the model downscales it
to a cell (bilinear on the 0.2° lattice of land nodes), read from the weather stores; a corner node
no store holds is fetched from CDS first. CDS is what every region but Tuscany scores. Tuscany's
history and every region's last few days are Open-Meteo ``era5_seamless``, which is coarse ERA5:
``cds`` measures the two at every weather node and ``fit`` writes CDS / ``era5_seamless`` for
``model.yaml``'s ``source_ratios`` as well. Networks whose gauges have no
parser here join as pseudo-gauges carrying their published fit (``pseudo`` in
``config/rain_field.yaml``). ``fit`` writes ``config/rain_scale_field.csv``,
``config/rain_cds_per_seamless.csv`` and a cross-validation report. Intermediate files live in
``$DATA_DIR/weather/rain_field/``. See ``.gavin-root/docs/rain-scale-field.md``.
"""

import argparse
import json
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from api.model.config import CONFIG_DIR

CONFIG_FILE = CONFIG_DIR / "rain_field.yaml"
FIELD_FILE = CONFIG_DIR / "rain_scale_field.csv"
SOURCE_RATIO_FILE = CONFIG_DIR / "rain_cds_per_seamless.csv"
LATTICE_DEG = 0.25
# Italy and its islands, (west, south, east, north).
LATTICE_BBOX = (6.5, 35.5, 18.75, 47.25)
SEASON_MONTHS = range(4, 12)
Z_QUANTILE = 0.95


def season_totals(
    model_calendar: pd.Series,
    gauge: pd.Series,
    day_totals: Callable[[pd.Series], pd.Series],
    *,
    year: int,
    min_coverage: float,
) -> dict | None:
    """Season (April-November of ``year``) totals over the days both report, the model's local
    calendar days re-cut into the gauge's days by ``day_totals``; ``ratio`` is gauge over model.
    ``None`` when the gauge reports under ``min_coverage`` of the season's days."""
    first, last = date(year, SEASON_MONTHS[0], 1), date(year, SEASON_MONTHS[-1] + 1, 1)
    season_days = (last - first).days
    model = day_totals(model_calendar)
    days = model.index.intersection(gauge.dropna().index)
    days = days[(days >= first) & (days < last)]
    if len(days) < min_coverage * season_days:
        return None
    gauge_mm, model_mm = float(gauge[days].sum()), float(model[days].sum())
    return {
        "days": len(days),
        "gauge_mm": gauge_mm,
        "model_mm": model_mm,
        "ratio": gauge_mm / model_mm if model_mm > 0 else float("nan"),
    }


def global_fit(gauges: pd.DataFrame) -> tuple[float, float]:
    """``(a, b)`` of ``ratio ~ a + b x elevation_km`` over every gauge, equally weighted."""
    z = gauges["elevation_m"].to_numpy(dtype=float) / 1000
    design = np.column_stack([np.ones_like(z), z])
    (a, b), *_ = np.linalg.lstsq(design, gauges["ratio"].to_numpy(dtype=float), rcond=None)
    return float(a), float(b)


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    """The ``q`` quantile of ``values`` under ``weights`` (midpoint rule, interpolated)."""
    keep = weights > 0
    values, weights = values[keep], weights[keep]
    order = np.argsort(values)
    values, weights = values[order], weights[order]
    cumulative = (np.cumsum(weights) - 0.5 * weights) / weights.sum()
    return float(np.interp(q, cumulative, values))


def fit_field(
    gauges: pd.DataFrame,
    nodes: pd.DataFrame,
    bandwidth_m: float,
    ridge: float,
    prior: tuple[float, float] | None = None,
) -> pd.DataFrame:
    """``nodes`` (projected ``x``, ``y`` in metres) with ``intercept``, ``per_km`` and
    ``max_elevation_m`` fitted on ``gauges`` (``x``, ``y``, ``elevation_m``, ``ratio``).

    Each node minimises ``sum w (ratio - a - b z)^2 + ridge ((a - a0)^2 + (b - b0)^2)`` with
    ``w = exp(-d^2 / 2 bandwidth^2)``, so ``ridge`` is counted in gauges at distance zero and
    ``(a0, b0)`` is ``prior`` (the national fit by default)."""
    a0, b0 = prior if prior is not None else global_fit(gauges)
    gx, gy = gauges["x"].to_numpy(dtype=float), gauges["y"].to_numpy(dtype=float)
    z = gauges["elevation_m"].to_numpy(dtype=float) / 1000
    y = gauges["ratio"].to_numpy(dtype=float)
    nx, ny = nodes["x"].to_numpy(dtype=float), nodes["y"].to_numpy(dtype=float)
    d2 = (nx[:, None] - gx[None, :]) ** 2 + (ny[:, None] - gy[None, :]) ** 2
    w = np.exp(-d2 / (2 * bandwidth_m**2))
    s0, s1, s2 = w.sum(1) + ridge, w @ z, w @ z**2 + ridge
    t0, t1 = w @ y + ridge * a0, w @ (z * y) + ridge * b0
    det = s0 * s2 - s1**2
    out = nodes.copy()
    out["intercept"] = (s2 * t0 - s1 * t1) / det
    out["per_km"] = (s0 * t1 - s1 * t0) / det
    heights = gauges["elevation_m"].to_numpy(dtype=float)
    out["max_elevation_m"] = [weighted_quantile(heights, row, Z_QUANTILE) for row in w]
    return out


def predict(field: pd.DataFrame, elevation_m: np.ndarray) -> np.ndarray:
    """The factor at nodes of ``field`` for heights ``elevation_m`` (one per node)."""
    z = np.minimum(np.clip(elevation_m, 0, None), field["max_elevation_m"].to_numpy()) / 1000
    return field["intercept"].to_numpy() + field["per_km"].to_numpy() * z


def block_cv(
    gauges: pd.DataFrame,
    bandwidths_m: list[float],
    block_m: float,
    ridge: float,
) -> pd.DataFrame:
    """For each kernel width, predict every gauge from the gauges outside its ``block_m`` square
    and score ``log(predicted / ratio)``: its root mean square and mean, one row per width."""
    blocks = (
        np.floor(gauges["x"] / block_m).astype(int).astype(str)
        + ":"
        + np.floor(gauges["y"] / block_m).astype(int).astype(str)
    )
    rows = []
    for bandwidth in bandwidths_m:
        errors = np.empty(len(gauges))
        for block in blocks.unique():
            held = (blocks == block).to_numpy()
            train, test = gauges[~held], gauges[held]
            field = fit_field(train, test[["x", "y"]], bandwidth, ridge)
            errors[held] = np.log(predict(field, test["elevation_m"].to_numpy()) / test["ratio"])
        rows.append(
            {
                "bandwidth_m": bandwidth,
                "rmse_log": float(np.sqrt(np.mean(errors**2))),
                "bias_log": float(np.mean(errors)),
                "gauges": len(gauges),
            }
        )
    return pd.DataFrame(rows)


def pseudo_gauges(
    cells: pd.DataFrame,
    *,
    network: str,
    intercept: float,
    per_km: float,
    low_m: float,
    high_m: float,
    count: int,
    seed: int = 0,
) -> pd.DataFrame:
    """``count`` gauges at cells (``lon``, ``lat``, ``elevation_m``) between ``low_m`` and
    ``high_m``, each carrying the published fit's ratio at its height."""
    eligible = cells[cells["elevation_m"].between(low_m, high_m)]
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(eligible), size=count, replace=count > len(eligible))
    chosen = eligible.iloc[pick].reset_index(drop=True)
    return pd.DataFrame(
        {
            "network": network,
            "code": [f"pseudo{i}" for i in range(count)],
            "lon": chosen["lon"].to_numpy(dtype=float),
            "lat": chosen["lat"].to_numpy(dtype=float),
            "elevation_m": chosen["elevation_m"].to_numpy(dtype=float),
            "ratio": intercept + per_km * chosen["elevation_m"].to_numpy(dtype=float) / 1000,
        }
    )


def node_season_totals(cds: pd.DataFrame, seamless: pd.DataFrame, *, year: int) -> pd.DataFrame:
    """Per weather node (``point_id``), the April-November ``year`` rain totals of CDS ERA5-Land
    (``cds``) and ``era5_seamless`` (``seamless``), both ``point_id, date, value``, over the days
    both report."""
    first, last = date(year, SEASON_MONTHS[0], 1), date(year, SEASON_MONTHS[-1] + 1, 1)
    both = cds.merge(seamless, on=["point_id", "date"], suffixes=("_cds", "_seamless")).dropna(
        subset=["value_cds", "value_seamless"]
    )
    both = both[(both["date"] >= first) & (both["date"] < last)]
    totals = both.groupby("point_id", as_index=False).agg(
        days=("date", "size"),
        cds_mm=("value_cds", "sum"),
        seamless_mm=("value_seamless", "sum"),
    )
    return totals.assign(year=year)


def ratio_field(
    nodes: pd.DataFrame, at: pd.DataFrame, bandwidth_m: float, ridge: float
) -> pd.Series:
    """At ``at`` (projected ``x``, ``y``), the Gaussian-weighted mean of the nodes' ``ratio``,
    pulled toward 1 (no correction) by ``ridge``, counted in nodes at distance zero."""
    d2 = (at["x"].to_numpy(dtype=float)[:, None] - nodes["x"].to_numpy(dtype=float)[None, :]) ** 2
    d2 += (at["y"].to_numpy(dtype=float)[:, None] - nodes["y"].to_numpy(dtype=float)[None, :]) ** 2
    w = np.exp(-d2 / (2 * bandwidth_m**2))
    ratio = (w @ nodes["ratio"].to_numpy(dtype=float) + ridge) / (w.sum(1) + ridge)
    return pd.Series(ratio, index=at.index)


def load_config(path: Path = CONFIG_FILE) -> dict:
    return yaml.safe_load(path.read_text())


def _out_dir() -> Path:
    from api.grid.sources import data_dir

    return data_dir() / "weather" / "rain_field"


def _dem_heights(gauges: pd.DataFrame, raw: Path) -> np.ndarray:
    """Copernicus GLO-30 height at each gauge, for networks that publish none (Umbria)."""
    import rasterio

    from api.grid.sources import copernicus_dem_tiles, fetch_dem_tiles

    bbox = (gauges["lon"].min(), gauges["lat"].min(), gauges["lon"].max(), gauges["lat"].max())
    heights = np.full(len(gauges), np.nan)
    for path in fetch_dem_tiles(copernicus_dem_tiles(bbox), raw / "copernicus_dem"):
        with rasterio.open(path) as dem:
            b = dem.bounds
            inside = (
                gauges["lon"].between(b.left, b.right) & gauges["lat"].between(b.bottom, b.top)
            ).to_numpy()
            if inside.any():
                xy = zip(gauges["lon"][inside], gauges["lat"][inside], strict=True)
                heights[inside] = [v[0] for v in dem.sample(xy)]
    return heights


def _reanalysis(client, nodes: list[tuple[float, float]], year: int) -> dict[tuple, pd.Series]:
    """Reanalysis daily rain (Europe/Rome days) at ``nodes`` over ``year``'s season and the day
    before, from the Open-Meteo archive, cached."""
    from datetime import UTC, datetime

    from api.weather.config import load_weather_config
    from api.weather.openmeteo import DailyRequest, parse_daily

    endpoint = load_weather_config().history.endpoint
    start = date(year, SEASON_MONTHS[0], 1) - timedelta(days=1)
    end = date(year, SEASON_MONTHS[-1] + 1, 1) - timedelta(days=1)
    series = {}
    for i in range(0, len(nodes), 100):
        batch = nodes[i : i + 100]
        request = DailyRequest(
            endpoint=endpoint,
            model="era5_seamless",
            points=[(f"{lat:.1f}_{lon:.1f}", lat, lon) for lat, lon in batch],
            units={"precipitation_sum": "mm"},
            timezone="Europe/Rome",
            start_date=start,
            end_date=end,
        )
        rows, _ = parse_daily(client.fetch(request), request, datetime.now(UTC))
        by_point = dict(list(rows.groupby("point_id")))
        for pid, lat, lon in request.points:
            if pid in by_point:  # sea nodes have no ERA5-Land values
                series[(lat, lon)] = by_point[pid].set_index("date")["value"]
    return series


def _scoring_lattice() -> tuple[float, float]:
    """The scoring lattice's spacing (degrees) and its farthest-node distance (km)."""
    from api.weather.config import load_weather_config

    config = load_weather_config().points
    return round(config.native_spacing_deg * config.stride, 6), config.max_distance_km


def lattice_weights(gauges: pd.DataFrame, land: set[tuple[float, float]]) -> pd.DataFrame:
    """``(code, node, weight)``: each gauge's bilinear weights on the scoring lattice's ``land``
    nodes, exactly as a cell's (``api.weather.points.interpolation_weights``)."""
    from api.weather.points import interpolation_weights, point_id

    spacing, max_distance_km = _scoring_lattice()
    node_of_id = {point_id(lat, lon): (lat, lon) for lat, lon in land}
    points = pd.DataFrame(
        {
            "point_id": list(node_of_id),
            "lat": [lat for lat, _ in node_of_id.values()],
            "lon": [lon for _, lon in node_of_id.values()],
        }
    )
    weights = interpolation_weights(
        gauges.rename(columns={"code": "cell_id"})[["cell_id", "lat", "lon"]],
        points,
        spacing,
        "bilinear",
        max_distance_km,
    )
    return pd.DataFrame(
        {
            "code": weights["cell_id"],
            "node": weights["point_id"].map(node_of_id),
            "weight": weights["weight"],
        }
    )


def lattice_corners(gauges: pd.DataFrame) -> list[tuple[float, float]]:
    """The scoring lattice's nodes around each gauge (``api.weather.points.candidate_points``)."""
    from api.weather.points import candidate_points

    spacing, _ = _scoring_lattice()
    corners = candidate_points(gauges[["lat", "lon"]], spacing)
    return sorted(
        (round(lat, 1), round(lon, 1))
        for lat, lon in zip(corners["lat"], corners["lon"], strict=True)
    )


def collect_network(
    network: str, years: list[int], config: dict, folder: Path, log=print
) -> pd.DataFrame:
    """One row per gauge and season year: its totals against CDS ERA5-Land rain downscaled to it
    as to a cell (bilinear on the scoring lattice), read from the weather stores; corner nodes no
    store holds are fetched from CDS first (``_fetch_cds_nodes``)."""
    from api.grid.sources import data_dir
    from api.weather.checks import GAUGE_NETWORKS, _client
    from api.weather.points import point_id

    raw = data_dir() / "raw"
    net = GAUGE_NETWORKS[network](raw, date(min(years), 1, 1), date(max(years), 12, 31))
    gauges = net.gauges.dropna(subset=["lon", "lat"]).reset_index(drop=True)
    if "elevation_m" not in gauges.columns or gauges["elevation_m"].isna().all():
        gauges["elevation_m"] = _dem_heights(gauges, raw)
    gauges = gauges.dropna(subset=["elevation_m"]).reset_index(drop=True)
    gauges["code"] = gauges["code"].astype(str)
    client = _client(raw)
    nodes = lattice_corners(gauges)
    corners = pd.DataFrame(
        {
            "point_id": [point_id(lat, lon) for lat, lon in nodes],
            "lat": [lat for lat, _ in nodes],
            "lon": [lon for _, lon in nodes],
        }
    )
    missing = corners[~corners["point_id"].isin(_held_nodes(folder))]
    if len(missing):
        _fetch_cds_nodes(f"gauges_{network}", missing, client, years, folder, log)
    rows = []
    for year in years:
        model = cds_rain(_store_roots(folder), nodes, year)
        weights = lattice_weights(gauges, set(model))
        for gauge in gauges.itertuples():
            mine = weights[weights["code"] == gauge.code]
            if mine.empty:
                continue
            downscaled = sum(
                w * model[node] for node, w in zip(mine["node"], mine["weight"], strict=True)
            )
            try:
                series = net.series(gauge)
            except Exception as error:  # a station without data for the window
                log(f"{network} {gauge.code}: {error!r}")
                continue
            totals = season_totals(
                downscaled.dropna(),
                series,
                net.day_totals,
                year=year,
                min_coverage=config.get("min_coverage_by_network", {}).get(
                    network, config["min_coverage"]
                ),
            )
            if totals is not None:
                rows.append(
                    {
                        "network": network,
                        "code": str(gauge.code),
                        "name": gauge.name,
                        "lon": float(gauge.lon),
                        "lat": float(gauge.lat),
                        "elevation_m": float(gauge.elevation_m),
                        "year": year,
                        **totals,
                    }
                )
    frame = pd.DataFrame(rows)
    log(f"{network}: {frame['code'].nunique() if len(frame) else 0} gauges, {len(frame)} seasons")
    return frame


def cds_rain(
    roots: list[Path], nodes: list[tuple[float, float]], year: int
) -> dict[tuple, pd.Series]:
    """CDS ERA5-Land daily rain (Europe/Rome days) in ``year`` at those ``nodes`` some weather
    store under ``roots`` holds (``<root>/<store>/daily/...``), the first store's where several
    do (a border node is in both regions' stores, with the same values)."""
    import duckdb

    from api.weather.cds import SOURCE_ID
    from api.weather.points import point_id

    files = [
        path
        for root in roots
        for path in sorted(root.glob(f"*/daily/source={SOURCE_ID}/year={year}/data.parquet"))
    ]
    if not files:
        return {}
    wanted = {point_id(lat, lon): (lat, lon) for lat, lon in nodes}
    rows = duckdb.sql(
        f"SELECT point_id, date, value FROM read_parquet({[str(f) for f in files]!r}) "
        f"WHERE variable = 'precipitation_sum' AND list_contains({list(wanted)!r}, point_id)"
    ).df()
    rows["date"] = pd.to_datetime(rows["date"]).dt.date
    rows = rows.drop_duplicates(["point_id", "date"])
    return {
        wanted[pid]: group.set_index("date")["value"].sort_index()
        for pid, group in rows.groupby("point_id")
    }


def _store_roots(folder: Path) -> list[Path]:
    """Where weather stores live: the regions' own, and those ``cds`` fetched into ``folder``."""
    from api.grid.sources import data_dir

    return [data_dir() / "weather", folder / "cds_store"]


def _held_nodes(folder: Path) -> set[str]:
    """Every node a weather store under ``_store_roots`` lists."""
    return {
        pid
        for root in _store_roots(folder)
        for path in root.glob("*/points.parquet")
        for pid in pd.read_parquet(path, columns=["point_id"])["point_id"]
    }


def cds_regions() -> list[str]:
    """Regions whose local weather store holds CDS ERA5-Land history."""
    from api.grid.sources import data_dir
    from api.weather.cds import SOURCE_ID

    root = data_dir() / "weather"
    return sorted(p.parent.parent.name for p in root.glob(f"*/daily/source={SOURCE_ID}"))


def region_nodes(region: str) -> pd.DataFrame:
    """The scoring lattice's nodes whose lattice square around them touches ``region``: every node
    a cell of the region can read, and some at sea (``point_id``, ``lat``, ``lon``)."""
    from shapely.geometry import box

    from api.weather.points import point_id

    spacing, _ = _scoring_lattice()
    shape = _region_shapes([region]).to_crs(4326).geometry.iloc[0]
    west, south, east, north = shape.bounds
    lats = np.arange(np.floor(south / spacing) - 1, np.ceil(north / spacing) + 2) * spacing
    lons = np.arange(np.floor(west / spacing) - 1, np.ceil(east / spacing) + 2) * spacing
    nodes = [
        (round(lat, 1), round(lon, 1))
        for lat in lats
        for lon in lons
        if shape.intersects(box(lon - spacing, lat - spacing, lon + spacing, lat + spacing))
    ]
    return pd.DataFrame(
        {
            "point_id": [point_id(lat, lon) for lat, lon in nodes],
            "lat": [lat for lat, _ in nodes],
            "lon": [lon for _, lon in nodes],
        }
    )


def _seamless_rain(client, nodes: list[tuple[float, float]], year: int) -> pd.DataFrame:
    """``point_id, date, value``: ``era5_seamless`` rain at the land ``nodes`` (``_reanalysis``)."""
    from api.weather.points import point_id

    frame = pd.concat(
        [
            pd.DataFrame(
                {"point_id": point_id(lat, lon), "date": list(series.index), "value": series}
            )
            for (lat, lon), series in _reanalysis(client, nodes, year).items()
        ],
        ignore_index=True,
    )
    return frame.assign(date=pd.to_datetime(frame["date"]).dt.date)


def _land_nodes(client, nodes: pd.DataFrame) -> set[str]:
    """The ``point_id`` of the ``nodes`` that are land, by the weather points' own probe: one day
    of ERA5-Land, which has no values over the sea (``era5_seamless`` fills the sea from ERA5)."""
    from datetime import UTC, datetime

    from api.weather.config import load_weather_config
    from api.weather.openmeteo import DailyRequest, parse_daily

    config = load_weather_config()
    probe = config.points.land_probe
    units = {name: config.variables[name].unit for name in probe.variables}
    land = set()
    for i in range(0, len(nodes), 100):
        batch = nodes.iloc[i : i + 100]
        request = DailyRequest(
            endpoint=config.history.endpoint,
            model=probe.model,
            points=list(zip(batch["point_id"], batch["lat"], batch["lon"], strict=True)),
            units=units,
            timezone="Europe/Rome",
            start_date=probe.date,
            end_date=probe.date,
        )
        rows, _ = parse_daily(client.fetch(request), request, datetime.now(UTC))
        complete = rows.dropna(subset=["value"]).groupby("point_id")["variable"].nunique()
        land |= set(complete[complete == len(probe.variables)].index)
    return land


def _fetch_cds_nodes(
    name: str, nodes: pd.DataFrame, client, years: list[int], folder: Path, log=print
):
    """A scratch store ``folder/cds_store/<name>`` of CDS ERA5-Land history over ``years`` at the
    ``nodes`` (``point_id``, ``lat``, ``lon``) that are land (``_land_nodes``), from the CDS
    time-series product as a region's backfill fetches them."""
    from api.grid.sources import data_dir
    from api.weather.cds import CdsClient, backfill_cds_timeseries
    from api.weather.store import WeatherStore

    land = nodes[nodes["point_id"].isin(_land_nodes(client, nodes))].assign(
        land=True, grid_elevation_m=np.nan
    )
    store = WeatherStore(folder / "cds_store" / name)
    store.root.mkdir(parents=True, exist_ok=True)
    land.to_parquet(store.points_path, index=False)
    log(f"{name}: {len(land)} land nodes of {len(nodes)}, fetching CDS time series")
    if len(land):
        backfill_cds_timeseries(
            CdsClient(cache_dir=data_dir() / "raw" / "cds"),
            store,
            land,
            "Europe/Rome",
            date(min(years), 1, 1),
            date(max(years), 12, 31),
            log=log,
            snowfall=False,
        )
    return store


def _fetched_cds_store(region: str, client, years: list[int], folder: Path, log=print):
    """A scratch CDS store for a region whose own store is not on this machine: the nodes
    ``region_nodes`` finds that no local region store holds (``_fetch_cds_nodes``)."""
    from api.weather.ingest import region_paths

    held = set()  # nodes a local store already measures (a neighbour's border nodes)
    for other in cds_regions():
        held |= set(pd.read_parquet(region_paths(other)[1].points_path)["point_id"])
    nodes = region_nodes(region)
    nodes = nodes[~nodes["point_id"].isin(held)].reset_index(drop=True)
    return _fetch_cds_nodes(region, nodes, client, years, folder, log)


def collect_cds(region: str, years: list[int], folder: Path, log=print) -> pd.DataFrame:
    """One row per land weather node of ``region`` and season year: its CDS ERA5-Land rain and its
    ``era5_seamless`` rain (Open-Meteo archive) over the same days. The CDS side is the region's
    own store, or, where that is not on this machine, one fetched here (``_fetched_cds_store``)."""
    import duckdb

    from api.weather.cds import SOURCE_ID
    from api.weather.checks import _client
    from api.weather.ingest import region_paths

    _, store, raw = region_paths(region)
    client = _client(raw)
    if not (store.daily_dir / f"source={SOURCE_ID}").exists():
        store = _fetched_cds_store(region, client, years, folder, log)
    points = pd.read_parquet(store.points_path)
    points = points[points["land"]] if "land" in points else points
    nodes = sorted(zip(points["lat"].round(1), points["lon"].round(1), strict=True))
    rows = []
    for year in years:
        path = store.partition_path(SOURCE_ID, year)
        if not path.exists():
            log(f"{region} {year}: no CDS partition")
            continue
        cds = duckdb.sql(
            f"SELECT point_id, date, value FROM read_parquet('{path}') "
            "WHERE variable = 'precipitation_sum'"
        ).df()
        cds["date"] = pd.to_datetime(cds["date"]).dt.date
        rows.append(node_season_totals(cds, _seamless_rain(client, nodes, year), year=year))
    frame = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    if len(frame):
        frame = frame.merge(points[["point_id", "lat", "lon"]], on="point_id").assign(region=region)
        pooled = frame["seamless_mm"].sum() / frame["cds_mm"].sum()
        log(f"{region}: {frame['point_id'].nunique()} nodes, seamless / CDS {pooled:.3f}")
    return frame


def gauge_table(config: dict, folder: Path) -> pd.DataFrame:
    """Every collected gauge, seasons pooled, plausible ratios only, plus the pseudo-gauges."""
    from api.grid.sources import data_dir

    files = [folder / f"gauges_{network}.csv" for network in config["networks"]]
    seasons = pd.concat(
        # A network with no usable gauge writes an empty file.
        [pd.read_csv(f, dtype={"code": str}) for f in files if f.exists() and f.stat().st_size > 1],
        ignore_index=True,
    )
    pooled = seasons.groupby(["network", "code"], as_index=False).agg(
        lon=("lon", "first"),
        lat=("lat", "first"),
        elevation_m=("elevation_m", "first"),
        gauge_mm=("gauge_mm", "sum"),
        model_mm=("model_mm", "sum"),
    )
    pooled["ratio"] = pooled["gauge_mm"] / pooled["model_mm"]
    low, high = config["ratio_range"]
    pooled = pooled[pooled["ratio"].between(low, high)]
    pseudo = []
    for region, fit in config["pseudo"].items():
        cells = pd.read_parquet(
            data_dir() / "grid" / region / "cells.parquet",
            columns=["lon", "lat", "elevation_m", "woodland"],
        )
        pseudo.append(
            pseudo_gauges(
                cells[cells["woodland"]],
                network=region,
                intercept=fit["intercept"],
                per_km=fit["per_km"],
                low_m=fit["low_m"],
                high_m=fit["high_m"],
                count=fit["count"],
            ).assign(pseudo=True)
        )
    gauges = pd.concat([pooled.assign(pseudo=False), *pseudo], ignore_index=True)
    return project(gauges)


def project(frame: pd.DataFrame) -> pd.DataFrame:
    from pyproj import Transformer

    to_laea = Transformer.from_crs(4326, 3035, always_xy=True)
    x, y = to_laea.transform(frame["lon"].to_numpy(), frame["lat"].to_numpy())
    return frame.assign(x=x, y=y)


def lattice(spacing: float = LATTICE_DEG) -> pd.DataFrame:
    """The nodes at multiples of ``spacing`` degrees over Italy (``LATTICE_BBOX``)."""
    west, south, east, north = LATTICE_BBOX
    lats = np.round(np.arange(np.ceil(south / spacing - 1e-9), north / spacing + 1e-9) * spacing, 3)
    lons = np.round(np.arange(np.ceil(west / spacing - 1e-9), east / spacing + 1e-9) * spacing, 3)
    grid_lat, grid_lon = np.meshgrid(lats, lons, indexing="ij")
    return project(pd.DataFrame({"lat": grid_lat.ravel(), "lon": grid_lon.ravel()}))


def cds_nodes(folder: Path) -> pd.DataFrame:
    """Every node ``cds`` measured, its seasons pooled: ``ratio`` is CDS over era5_seamless rain."""
    seasons = pd.concat(
        [pd.read_csv(f) for f in sorted(folder.glob("cds_*.csv")) if f.stat().st_size > 1],
        ignore_index=True,
    ).drop_duplicates(["point_id", "year"])  # a border node is in two regions' stores
    nodes = seasons.groupby("point_id", as_index=False).agg(
        lat=("lat", "first"),
        lon=("lon", "first"),
        years=("year", "nunique"),
        seamless_mm=("seamless_mm", "sum"),
        cds_mm=("cds_mm", "sum"),
    )
    return project(nodes.assign(ratio=nodes["cds_mm"] / nodes["seamless_mm"]))


def fit_source_ratio(config: dict, folder: Path, log=print) -> pd.DataFrame:
    """Write ``SOURCE_RATIO_FILE``: CDS / era5_seamless rain on the scoring lattice, each node's
    own pooled ratio lightly smoothed, and 1 (no correction) away from every measured node.
    era5_seamless rain is coarse ERA5 (neighbouring nodes share 0.25° blocks), so a node's ratio
    carries those blocks and multiplying era5_seamless by it takes them out again."""
    nodes = cds_nodes(folder)
    spacing, _ = _scoring_lattice()
    ratios = lattice(spacing)
    bandwidth, ridge = config["cds_bandwidth_km"] * 1000.0, config["cds_ridge"]
    ratios["ratio"] = ratio_field(nodes, ratios, bandwidth, ridge)
    ratios[["lat", "lon", "ratio"]].round({"ratio": 4}).to_csv(SOURCE_RATIO_FILE, index=False)
    nodes["smoothed"] = ratio_field(nodes, nodes, bandwidth, ridge)
    nodes.to_csv(folder / "cds_nodes.csv", index=False)
    pooled = nodes["cds_mm"].sum() / nodes["seamless_mm"].sum()
    low, high = nodes["ratio"].min(), nodes["ratio"].max()
    log(f"CDS / seamless: {len(nodes)} nodes, pooled {pooled:.3f}, nodes {low:.2f}-{high:.2f}")
    return nodes


def run_fit(config: dict, folder: Path, log=print) -> dict:
    nodes = fit_source_ratio(config, folder, log)
    gauges = gauge_table(config, folder)
    ridge = config["ridge"]
    bandwidths = [km * 1000.0 for km in config["bandwidths_km"]]
    scores = block_cv(gauges, bandwidths, config["block_km"] * 1000.0, ridge)
    log(scores.to_string(index=False))
    best = float(scores.sort_values("rmse_log").iloc[0]["bandwidth_m"])
    # How well each network is told by the others alone (not used to choose, only reported).
    held_out = []
    for network in sorted(gauges["network"].unique()):
        own = (gauges["network"] == network).to_numpy()
        field = fit_field(gauges[~own], gauges.loc[own, ["x", "y"]], best, ridge)
        error = np.log(
            predict(field, gauges.loc[own, "elevation_m"].to_numpy()) / gauges.loc[own, "ratio"]
        )
        held_out.append(
            {
                "network": network,
                "gauges": int(own.sum()),
                "bias_log": float(error.mean()),
                "rmse_log": float(np.sqrt((error**2).mean())),
            }
        )
    held_out = pd.DataFrame(held_out)
    log(held_out.round(3).to_string(index=False))
    field = fit_field(gauges, lattice(), best, ridge)
    field[["lat", "lon", "intercept", "per_km", "max_elevation_m"]].round(
        {"intercept": 4, "per_km": 4, "max_elevation_m": 0}
    ).to_csv(FIELD_FILE, index=False)
    at_gauges = fit_field(gauges, gauges[["x", "y"]], best, ridge)
    gauges["fitted"] = predict(at_gauges, gauges["elevation_m"].to_numpy())
    gauges.to_csv(folder / "gauges_fitted.csv", index=False)
    scores.to_csv(folder / "block_cv.csv", index=False)
    held_out.to_csv(folder / "network_held_out.csv", index=False)
    summary = {
        "gauges": int((~gauges["pseudo"]).sum()),
        "pseudo_gauges": int(gauges["pseudo"].sum()),
        "networks": sorted(gauges["network"].unique()),
        "national_fit": global_fit(gauges),
        "bandwidth_km": best / 1000,
        "ridge": ridge,
        "block_km": config["block_km"],
        "cds_nodes": len(nodes),
        "cds_per_seamless": float(nodes["cds_mm"].sum() / nodes["seamless_mm"].sum()),
    }
    (folder / "fit.json").write_text(json.dumps(summary, indent=2))
    log(json.dumps(summary, indent=2))
    return summary


def old_fits(rev: str) -> dict:
    """Each region's ``precipitation_scale`` as the config stood at git revision ``rev``, its field
    and source ratios too (a refit changes them under an unchanged ``model.yaml``)."""
    import subprocess
    import tempfile

    from api.model.config import REGIONS_DIR, load_model_config

    def show(path: Path) -> str:
        relative = path.resolve().relative_to(CONFIG_DIR.parents[3])
        return subprocess.run(
            ["git", "show", f"{rev}:{relative}"], capture_output=True, text=True, check=True
        ).stdout

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "regions").mkdir()
        (root / "model.yaml").write_text(show(CONFIG_DIR / "model.yaml"))
        regions = sorted(p.stem for p in REGIONS_DIR.glob("*.yaml"))
        for region in regions:
            (root / "regions" / f"{region}.yaml").write_text(show(REGIONS_DIR / f"{region}.yaml"))
        scales = {
            region: load_model_config(
                root / "model.yaml", region=region, regions_dir=root / "regions"
            ).precipitation_scale
            for region in regions
        }

    def at_rev(name: str) -> str:
        """``name`` (a lattice under ``config/``) as it stood at ``rev``, copied out of the tree."""
        copy = _out_dir() / "at_rev" / rev / name
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_text(show(CONFIG_DIR / name))
        return str(copy)

    return {
        region: scale.model_copy(
            update={
                "field": at_rev(scale.field) if scale.field else None,
                "source_ratios": {k: at_rev(v) for k, v in scale.source_ratios.items()},
            }
        )
        for region, scale in scales.items()
    }


def _region_shapes(regions: list[str]):
    """The ISTAT outlines of ``regions`` in EPSG:3035, one row per ISTAT region code."""
    import geopandas as gpd

    from api.grid.region import load_region
    from api.grid.sources import data_dir, fetch, load_sources

    codes = [load_region(r).boundary.region_code for r in regions]
    istat = load_sources()["istat_boundaries"].download or {}
    archive = fetch(istat["url"], data_dir() / "raw" / "istat" / Path(istat["url"]).name)
    shapes = gpd.read_file(f"zip://{archive}!{istat['regions']}").to_crs(3035)
    return shapes[shapes["COD_REG"].isin(codes)].dissolve("COD_REG")


def run_borders(rev: str, folder: Path, spacing_m: float = 5000, log=print) -> pd.DataFrame:
    """At points every ``spacing_m`` along each land border between two regions, the rain factor
    each side applied at ``rev`` and the one the field applies now, at the point's DEM height."""
    import geopandas as gpd

    from api.grid.region import load_region
    from api.grid.sources import data_dir
    from api.model.config import load_model_config
    from api.weather.cds import SOURCE_ID

    before = old_fits(rev)
    now = load_model_config().precipitation_scale
    codes = {load_region(r).boundary.region_code: r for r in before}
    raw = data_dir() / "raw"
    shapes = _region_shapes(list(before))
    rows = []
    ids = list(shapes.index)
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            line = shapes.geometry[a].boundary.intersection(shapes.geometry[b].boundary)
            if line.is_empty or line.length < 2 * spacing_m:
                continue
            steps = np.arange(spacing_m / 2, line.length, spacing_m)
            points = gpd.GeoSeries([line.interpolate(d) for d in steps], crs=3035).to_crs(4326)
            frame = pd.DataFrame({"lon": points.x, "lat": points.y})
            frame["elevation_m"] = _dem_heights(frame, raw)
            z = frame["elevation_m"].to_numpy()
            lon, lat = frame["lon"].to_numpy(), frame["lat"].to_numpy()
            ra, rb = codes[a], codes[b]
            rows.append(
                frame.assign(
                    region_a=ra,
                    region_b=rb,
                    before_a=before[ra].factor(z, frame["lon"], frame["lat"]),
                    before_b=before[rb].factor(z, frame["lon"], frame["lat"]),
                    after=now.factor(z, frame["lon"].to_numpy(), frame["lat"].to_numpy()),
                    # What CDS rows (most regions' history) get, before and now.
                    before_cds=before[ra].factor(z, lon, lat, SOURCE_ID),
                    after_cds=now.factor(z, lon, lat, SOURCE_ID),
                )
            )
    points = pd.concat(rows, ignore_index=True)
    points.to_csv(folder / "borders_points.csv", index=False)
    points["step_before"] = np.abs(np.log(points["before_a"] / points["before_b"]))
    summary = points.groupby(["region_a", "region_b"], as_index=False).agg(
        points=("lon", "size"),
        median_elevation_m=("elevation_m", "median"),
        before_a=("before_a", "median"),
        before_b=("before_b", "median"),
        after=("after", "median"),
        after_min=("after", "min"),
        after_max=("after", "max"),
        before_cds=("before_cds", "median"),
        after_cds=("after_cds", "median"),
        median_step_before=("step_before", "median"),
    )
    summary["median_step_before"] = np.expm1(summary["median_step_before"])
    summary.to_csv(folder / "borders.csv", index=False)
    log(summary.round(2).to_string(index=False))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["collect", "cds", "fit", "borders"])
    parser.add_argument("--before", default="HEAD", help="borders: git revision of the old fits")
    parser.add_argument("--network", action="append", help="collect: only these networks")
    parser.add_argument("--region", action="append", help="cds: only these regions' stores")
    args = parser.parse_args()
    config = load_config()
    folder = _out_dir()
    folder.mkdir(parents=True, exist_ok=True)
    if args.command == "collect":
        for network, years in config["networks"].items():
            if args.network and network not in args.network:
                continue
            collect_network(network, years, config, folder).to_csv(
                folder / f"gauges_{network}.csv", index=False
            )
    elif args.command == "cds":
        for region in args.region or [*cds_regions(), *config["cds_fetch"]]:
            collect_cds(region, config["cds_years"], folder).to_csv(
                folder / f"cds_{region}.csv", index=False
            )
    elif args.command == "fit":
        run_fit(config, folder)
    else:
        run_borders(args.before, folder)


if __name__ == "__main__":
    main()
