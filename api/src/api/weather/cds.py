"""Copernicus CDS ERA5-Land history: bulk hourly download → Europe/Rome daily Parquet.

Replaces Open-Meteo archive backfill for new regions. Forecast and seasonal stay on
Open-Meteo. See ``.gavin-root/docs/weather-history-cds.md``.

    uv run python -m api.weather.ingest backfill --source cds [--start …] [--end …]

Two ways to fetch the same hourly values (``cds.method`` in ``weather.yaml``):

- ``chunks``: the gridded dataset over the region's bbox, one request per ~week (CDS cost limit).
  About 630 requests for 2016 to today, and CDS runs one request per account at a time.
- ``timeseries``: the ERA5-Land time-series product, one request per weather node for the whole
  range (seconds each), plus snowfall, which that product lacks, from the gridded dataset half a
  year at a time. Measured 2026-09-25 against a week of chunks at one Umbrian node: identical to
  float32 precision, with precipitation and radiation already hourly increments.
"""

from __future__ import annotations

import json
import os
import time
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import ClassVar
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from api.weather.derived import daily_et0_mm, daily_vpd_max_kpa
from api.weather.store import WeatherStore

SOURCE_ID = "era5_land_cds"
CDS_DATASET = "reanalysis-era5-land"

CDS_VARS = {
    "2m_temperature": "t2m",
    "2m_dewpoint_temperature": "d2m",
    "total_precipitation": "tp",
    "snowfall": "sf",
    "volumetric_soil_water_layer_1": "swvl1",
    "volumetric_soil_water_layer_2": "swvl2",
    "soil_temperature_level_1": "stl1",
    "10m_u_component_of_wind": "u10",
    "10m_v_component_of_wind": "v10",
    "surface_solar_radiation_downwards": "ssrd",
}

TIMESERIES_DATASET = "reanalysis-era5-land-timeseries"
# The time-series product's names for CDS_VARS, minus snowfall (not offered there).
TIMESERIES_VARS = {
    "2m_temperature": "t2m",
    "2m_dewpoint_temperature": "d2m",
    "total_precipitation": "tp",
    "volumetric_soil_water_level_1": "swvl1",
    "volumetric_soil_water_level_2": "swvl2",
    "soil_temperature_level_1": "stl1",
    "10m_u_component_of_wind": "u10",
    "10m_v_component_of_wind": "v10",
    "surface_solar_radiation_downwards": "ssrd",
}
# Snowfall alone over a regional bbox: CDS costs 2 per hourly field and allows 12,000, so up to
# eight months of 31 days fit in one request; half a year keeps a margin.
SNOWFALL_MAX_MONTHS = 6
ACCUMULATED = ("tp", "sf", "ssrd")

Log = Callable[[str], None]


class CdsCredentialsError(RuntimeError):
    """No CDS API key in the environment or ``~/.cdsapirc``."""


def resolve_cds_key() -> str:
    """``CDSAPI_KEY`` (``uid:key``) or the ``key:`` line in ``~/.cdsapirc``."""
    env = os.environ.get("CDSAPI_KEY", "").strip()
    if env:
        return env
    rc = Path.home() / ".cdsapirc"
    if rc.is_file():
        for line in rc.read_text().splitlines():
            if line.strip().startswith("key:"):
                return line.split(":", 1)[1].strip()
    raise CdsCredentialsError(
        "CDS API key missing: set CDSAPI_KEY=uid:key in api/.env, or write ~/.cdsapirc "
        "(https://cds.climate.copernicus.eu/how-to-api)"
    )


def point_id(lat: float, lon: float) -> str:
    """Same id scheme as ``api.weather.points`` (N43.80E011.80)."""
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{ns}{abs(lat):05.2f}{ew}{abs(lon):06.2f}"


def _local_dates(times_utc: pd.Series, timezone: str) -> pd.Series:
    tz = ZoneInfo(timezone)
    aware = pd.to_datetime(times_utc, utc=True).dt.tz_convert(tz)
    return aware.dt.date


def _hourly_accumulation(cumulative: np.ndarray, hours_utc: np.ndarray | None = None) -> np.ndarray:
    """Turn an ERA5-Land cumulative-from-forecast-start series into per-hour increments.

    ERA5-Land accumulates from 00 UTC: the 01 UTC value is the first hour's own amount and the
    00 UTC step repeats the previous day's total. With ``hours_utc`` the 01 UTC step is always the
    reset, however large that first hour is against the day before; without it (or across a gap),
    a drop below half the previous value marks one. At the start of a series (chunk / missing prior
    hour) a 00 UTC value must not count as an increment: there is no previous step to difference.

    Tiny float32 decreases overnight (SSRD plateaus around 1e7 J m⁻²) are noise, not resets.
    """
    if len(cumulative) == 0:
        return cumulative
    diffs = np.empty_like(cumulative, dtype=float)
    first = float(cumulative[0])
    starts_fresh = hours_utc is not None and int(hours_utc[0]) == 1 and np.isfinite(first)
    diffs[0] = max(0.0, first) if starts_fresh else 0.0
    for i in range(1, len(cumulative)):
        cur = float(cumulative[i])
        prev = float(cumulative[i - 1])
        if not (np.isfinite(cur) and np.isfinite(prev)):
            diffs[i] = cur if np.isfinite(cur) else 0.0
            continue
        if hours_utc is not None and int(hours_utc[i]) == 1:
            diffs[i] = max(0.0, cur)  # accumulation restarted at 00 UTC
        elif prev > 0 and cur < 0.5 * prev:
            diffs[i] = max(0.0, cur)  # forecast reset
        else:
            diffs[i] = max(0.0, cur - prev)
    return diffs


def aggregate_hourly_frame(
    hourly: pd.DataFrame,
    timezone: str,
    elevations: dict[str, float] | None = None,
    accumulated: tuple[str, ...] = ACCUMULATED,
) -> pd.DataFrame:
    """Turn an hourly wide frame into the store's long daily rows for ``SOURCE_ID``.

    Required columns: ``time`` (UTC), ``lat``, ``lon``, plus CDS short names
    (``t2m``, ``d2m``, ``tp``, …). Temperatures in K, precip in m, SSRD in J m⁻²,
    wind in m s⁻¹.

    Accumulated fields (``accumulated``: ``tp``, ``sf``, ``ssrd`` from the gridded dataset) are
    deaccumulated per point on the full UTC series *before* grouping into Europe/Rome local days —
    ERA5-Land resets at 00 UTC, which falls mid local day. Pass the ones still cumulative; the
    time-series product already serves hourly increments.
    """
    if hourly.empty:
        return pd.DataFrame(
            columns=["source", "point_id", "date", "variable", "value", "fetched_at"]
        )
    df = hourly.copy()
    df["point_id"] = [point_id(lat, lon) for lat, lon in zip(df["lat"], df["lon"], strict=True)]
    df = df.sort_values(["point_id", "time"]).reset_index(drop=True)
    hours = pd.to_datetime(df["time"], utc=True).dt.hour.to_numpy()
    for col in accumulated:
        if col in df.columns:
            df[col] = df.groupby("point_id", sort=False)[col].transform(
                lambda s: _hourly_accumulation(s.to_numpy(dtype=float), hours[s.index])
            )
    df["local_date"] = _local_dates(df["time"], timezone)
    df["hour_utc"] = pd.to_datetime(df["time"], utc=True).dt.hour
    elevations = elevations or {}
    fetched_at = datetime.now(UTC)
    rows: list[dict] = []

    for (pid, local_day), group in df.groupby(["point_id", "local_date"], sort=True):
        g = group.sort_values("time")
        lat = float(g["lat"].iloc[0])
        elev = elevations.get(str(pid), 300.0)
        t_c = g["t2m"].to_numpy(dtype=float) - 273.15
        td_c = g["d2m"].to_numpy(dtype=float) - 273.15
        tp_m = g["tp"].to_numpy(dtype=float)
        sf_m = g["sf"].to_numpy(dtype=float)
        ssrd_mj = g["ssrd"].to_numpy(dtype=float) / 1e6
        wind_ms = np.hypot(g["u10"].to_numpy(dtype=float), g["v10"].to_numpy(dtype=float))
        day_of_year = date.fromisoformat(str(local_day)).timetuple().tm_yday

        values = {
            "temperature_2m_min": float(np.nanmin(t_c)),
            "temperature_2m_max": float(np.nanmax(t_c)),
            "temperature_2m_mean": float(np.nanmean(t_c)),
            "soil_temperature_0_to_7cm_mean": float(np.nanmean(g["stl1"].to_numpy() - 273.15)),
            "soil_moisture_0_to_7cm_mean": float(np.nanmean(g["swvl1"])),
            "soil_moisture_7_to_28cm_mean": float(np.nanmean(g["swvl2"])),
            "precipitation_sum": float(np.nansum(tp_m) * 1000.0),
            "snowfall_sum": float(np.nansum(sf_m) * 100.0),
            "wind_speed_10m_max": float(np.nanmax(wind_ms) * 3.6),
            "vapour_pressure_deficit_max": daily_vpd_max_kpa(t_c, td_c),
            "et0_fao_evapotranspiration": daily_et0_mm(
                t_c,
                td_c,
                wind_ms,
                ssrd_mj,
                elev,
                lat,
                g["hour_utc"].to_numpy(),
                day_of_year,
            ),
        }
        for variable, value in values.items():
            if value is None or (isinstance(value, float) and not np.isfinite(value)):
                continue
            rows.append(
                {
                    "source": SOURCE_ID,
                    "point_id": pid,
                    "date": local_day,
                    "variable": variable,
                    "value": float(value),
                    "fetched_at": fetched_at,
                }
            )
    return pd.DataFrame(rows)


@dataclass(frozen=True)
class CdsChunkRequest:
    """One CDS retrieve: region bbox, one contiguous day range within a month.

    A full month of hourly ERA5-Land for every variable exceeds CDS cost limits on a
    regional bbox; about a week of all variables fits (probed 2026-09-24).
    """

    north: float
    west: float
    south: float
    east: float
    year: int
    month: int  # 1..12
    days: tuple[int, ...]  # day-of-month numbers, contiguous
    dataset: ClassVar[str] = CDS_DATASET

    @property
    def label(self) -> str:
        first, last = self.days[0], self.days[-1]
        return (
            f"{self.year}{self.month:02d}{first:02d}-{last:02d}_"
            f"{self.south:.2f}_{self.west:.2f}_{self.north:.2f}_{self.east:.2f}"
        )

    def cds_request(self) -> dict:
        return {
            "product_type": "reanalysis",
            "variable": list(CDS_VARS),
            "year": [str(self.year)],
            "month": [f"{self.month:02d}"],
            "day": [f"{d:02d}" for d in self.days],
            "time": [f"{h:02d}:00" for h in range(24)],
            "area": [self.north, self.west, self.south, self.east],
            "data_format": "netcdf",
            "download_format": "zip",
        }


def month_day_chunks(year: int, month: int, chunk_days: int = 7) -> list[tuple[int, ...]]:
    """Split a calendar month into contiguous day tuples of at most ``chunk_days``."""
    import calendar

    last = calendar.monthrange(year, month)[1]
    chunks = []
    day = 1
    while day <= last:
        end = min(day + chunk_days - 1, last)
        chunks.append(tuple(range(day, end + 1)))
        day = end + 1
    return chunks


@dataclass(frozen=True)
class CdsPointRequest:
    """One weather node's hourly series, every variable but snowfall, from the time-series
    product. Coordinates are the node's own (on the 0.1° ERA5-Land grid)."""

    lat: float
    lon: float
    start: date
    end: date
    dataset: ClassVar[str] = TIMESERIES_DATASET

    @property
    def label(self) -> str:
        return f"ts_{point_id(self.lat, self.lon)}_{self.start:%Y%m%d}-{self.end:%Y%m%d}"

    def cds_request(self) -> dict:
        return {
            "variable": list(TIMESERIES_VARS),
            "location": {"longitude": self.lon, "latitude": self.lat},
            "date": [f"{self.start.isoformat()}/{self.end.isoformat()}"],
            "data_format": "netcdf",
        }


@dataclass(frozen=True)
class CdsSnowfallRequest:
    """Hourly snowfall over a bbox for whole months of one year, or for some days of one month
    (``days``), from the gridded dataset."""

    north: float
    west: float
    south: float
    east: float
    year: int
    months: tuple[int, ...]
    days: tuple[int, ...] | None = None
    dataset: ClassVar[str] = CDS_DATASET

    @property
    def label(self) -> str:
        span = f"{self.year}{self.months[0]:02d}-{self.months[-1]:02d}"
        if self.days is not None:
            span += f"_d{self.days[0]:02d}-{self.days[-1]:02d}"
        return f"sf_{span}_{self.south:.2f}_{self.west:.2f}_{self.north:.2f}_{self.east:.2f}"

    def cds_request(self) -> dict:
        days = self.days if self.days is not None else range(1, 32)
        return {
            "product_type": "reanalysis",
            "variable": ["snowfall"],
            "year": [str(self.year)],
            "month": [f"{m:02d}" for m in self.months],
            "day": [f"{d:02d}" for d in days],
            "time": [f"{h:02d}:00" for h in range(24)],
            "area": [self.north, self.west, self.south, self.east],
            "data_format": "netcdf",
            "download_format": "zip",
        }


CdsRequest = CdsChunkRequest | CdsPointRequest | CdsSnowfallRequest


def snowfall_requests(
    bbox: tuple[float, float, float, float],
    start: date,
    end: date,
    max_months: int = SNOWFALL_MAX_MONTHS,
) -> list[CdsSnowfallRequest]:
    """Snowfall requests covering ``start..end``: whole months grouped by year, at most
    ``max_months`` each; a month the range only partly covers goes alone with its days, so no
    request asks for a day before or after the range (CDS has no data yet past ~5 days ago)."""
    import calendar

    north, west, south, east = bbox
    requests: list[CdsSnowfallRequest] = []
    run: list[int] = []
    run_year = start.year

    def flush() -> None:
        if run:
            requests.append(CdsSnowfallRequest(north, west, south, east, run_year, tuple(run)))
            run.clear()

    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        last = calendar.monthrange(year, month)[1]
        first_day = start.day if (year, month) == (start.year, start.month) else 1
        last_day = end.day if (year, month) == (end.year, end.month) else last
        if first_day == 1 and last_day == last:
            if run and (year != run_year or len(run) == max_months):
                flush()
            run_year = year
            run.append(month)
        else:
            flush()
            requests.append(
                CdsSnowfallRequest(
                    north, west, south, east, year, (month,), tuple(range(first_day, last_day + 1))
                )
            )
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    flush()
    return requests


# CDS rejects a submission outright while the account's queue for a dataset is full; every
# region rail shares one account, so wait for room instead of failing the backfill.
QUEUE_FULL = "temporarily limited"


class CdsClient:
    """Cache under ``cache_dir``; retrieve via ``cdsapi`` when missing."""

    def __init__(
        self,
        cache_dir: Path,
        key: str | None = None,
        queue_wait_s: float = 120.0,
        queue_retries: int = 60,
    ) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._key = key
        self.queue_wait_s = queue_wait_s
        self.queue_retries = queue_retries

    def cache_path(self, request: CdsRequest) -> Path:
        return self.cache_dir / f"{request.label}.zip"

    def ensure(self, request: CdsRequest, log: Log = print) -> Path:
        path = self.cache_path(request)
        if path.exists() and path.stat().st_size > 0:
            return path
        key = self._key or resolve_cds_key()
        try:
            import cdsapi
        except ImportError as error:
            raise RuntimeError("cdsapi is not installed: uv sync --group cds") from error
        log(f"CDS retrieve {request.label} …")
        partial = path.with_suffix(".zip.part")
        client = cdsapi.Client(url="https://cds.climate.copernicus.eu/api", key=key)
        for attempt in range(self.queue_retries + 1):
            try:
                client.retrieve(request.dataset, request.cds_request(), str(partial))
                break
            except Exception as error:
                if QUEUE_FULL not in str(error) or attempt == self.queue_retries:
                    raise
                log(f"CDS queue full; retrying {request.label} in {self.queue_wait_s:.0f} s")
                time.sleep(self.queue_wait_s)
        partial.replace(path)
        return path


def bbox_of_points(
    points: pd.DataFrame, pad_deg: float = 0.15
) -> tuple[float, float, float, float]:
    """(north, west, south, east) covering land points."""
    land = points[points["land"]] if "land" in points.columns else points
    return (
        float(land["lat"].max() + pad_deg),
        float(land["lon"].min() - pad_deg),
        float(land["lat"].min() - pad_deg),
        float(land["lon"].max() + pad_deg),
    )


def read_hourly_netcdf_zip(path: Path) -> pd.DataFrame:
    """Load a CDS zip of NetCDF files into a wide hourly frame (requires xarray)."""
    try:
        import xarray as xr
    except ImportError as error:
        raise RuntimeError("xarray is required: uv sync --group cds") from error

    frames: list[pd.DataFrame] = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not name.endswith((".nc", ".nc4")):
                continue
            # Extract to a temp file: xarray needs a seekable path for some engines.
            target = path.parent / f".{path.stem}_{Path(name).name}"
            with zf.open(name) as src, target.open("wb") as dst:
                dst.write(src.read())
            try:
                ds = xr.open_dataset(target)
                frames.append(_dataset_to_frame(ds))
                ds.close()
            finally:
                target.unlink(missing_ok=True)
    if not frames:
        raise ValueError(f"no NetCDF members in {path}")
    out = frames[0]
    for frame in frames[1:]:
        out = out.merge(frame, on=["time", "lat", "lon"], how="outer")
    return out


def _dataset_to_frame(ds: object) -> pd.DataFrame:
    import xarray as xr

    assert isinstance(ds, xr.Dataset)
    rename = {}
    for candidate, target in (("latitude", "lat"), ("longitude", "lon"), ("valid_time", "time")):
        if candidate in ds.coords or candidate in ds.dims:
            rename[candidate] = target
    if rename:
        ds = ds.rename(rename)
    # Map long CDS names onto short ones when present.
    for long_name, short in CDS_VARS.items():
        if long_name in ds.data_vars and short not in ds.data_vars:
            ds = ds.rename({long_name: short})
    df = ds.to_dataframe().reset_index()
    keep = ["time", "lat", "lon", *CDS_VARS.values()]
    return df[[c for c in keep if c in df.columns]]


def subsample_to_points(hourly: pd.DataFrame, points: pd.DataFrame) -> pd.DataFrame:
    """Keep only the (lat, lon) nodes that appear in the region's land point set."""
    land = points[points["land"]] if "land" in points.columns else points
    wanted = {(round(float(r.lat), 2), round(float(r.lon), 2)) for r in land.itertuples()}
    mask = [
        (round(float(lat), 2), round(float(lon), 2)) in wanted
        for lat, lon in zip(hourly["lat"], hourly["lon"], strict=True)
    ]
    return hourly.loc[mask].reset_index(drop=True)


def point_elevations(points: pd.DataFrame) -> dict[str, float]:
    """Each node's height for ET0: the DEM mean under it, else the model's grid height."""
    elevations: dict[str, float] = {}
    for r in points.itertuples():
        elev = 300.0
        if "dem_elevation_m" in points.columns and pd.notna(getattr(r, "dem_elevation_m", None)):
            elev = float(r.dem_elevation_m)
        elif "grid_elevation_m" in points.columns and pd.notna(
            getattr(r, "grid_elevation_m", None)
        ):
            elev = float(r.grid_elevation_m)
        elevations[str(r.point_id)] = elev
    return elevations


def backfill_cds(
    client: CdsClient,
    store: WeatherStore,
    points: pd.DataFrame,
    timezone: str,
    start: date,
    end: date,
    log: Log = print,
) -> dict:
    """Fetch each ~week in ``start..end`` from CDS into the daily store.

    CDS cost limits reject a full month of hourly ERA5-Land for all variables on a
    regional bbox; ~7-day chunks fit (see weather-history-cds.md).
    """
    north, west, south, east = bbox_of_points(points)
    elevations = point_elevations(points)
    summary: dict = {"chunks": [], "rows": 0, "cached": 0, "fetched": 0}
    # Newest month first so a partial run still validates recent seasons.
    cursor = date(end.year, end.month, 1)
    first = date(start.year, start.month, 1)
    while cursor >= first:
        for days in reversed(month_day_chunks(cursor.year, cursor.month)):
            chunk_start = date(cursor.year, cursor.month, days[0])
            chunk_end = date(cursor.year, cursor.month, days[-1])
            window_start, window_end = max(start, chunk_start), min(end, chunk_end)
            if window_start > window_end:
                continue
            # Only request days that overlap the window.
            days_needed = tuple(
                d for d in days if window_start <= date(cursor.year, cursor.month, d) <= window_end
            )
            if not days_needed:
                continue
            request = CdsChunkRequest(
                north=north,
                west=west,
                south=south,
                east=east,
                year=cursor.year,
                month=cursor.month,
                days=days_needed,
            )
            cached = client.cache_path(request).exists()
            path = client.ensure(request, log=log)
            summary["cached" if cached else "fetched"] += 1
            hourly = subsample_to_points(read_hourly_netcdf_zip(path), points)
            daily = aggregate_hourly_frame(hourly, timezone, elevations)
            daily = daily[
                (pd.to_datetime(daily["date"]).dt.date >= window_start)
                & (pd.to_datetime(daily["date"]).dt.date <= window_end)
            ]
            store.upsert_daily(daily)
            summary["rows"] += len(daily)
            label = f"{cursor.year}-{cursor.month:02d}-{days_needed[0]:02d}..{days_needed[-1]:02d}"
            summary["chunks"].append(label)
            log(
                f"CDS {label}: {len(daily)} values -> "
                f"{store.partition_path(SOURCE_ID, cursor.year)}"
            )
        if cursor.month == 1:
            cursor = date(cursor.year - 1, 12, 1)
        else:
            cursor = date(cursor.year, cursor.month - 1, 1)
    (store.root / "cds_meta.json").write_text(
        json.dumps(
            {
                "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
                "source": SOURCE_ID,
                "dataset": CDS_DATASET,
                "start": str(start),
                "end": str(end),
                **summary,
            },
            indent=2,
        )
        + "\n"
    )
    return summary


def _on_grid(frame: pd.DataFrame) -> pd.DataFrame:
    """Round coordinates to the 0.1° grid (the time-series product's carry float noise) and make
    times naive UTC, so frames from the two products join."""
    out = frame.assign(lat=frame["lat"].round(2), lon=frame["lon"].round(2))
    times = pd.to_datetime(out["time"])
    if times.dt.tz is not None:
        times = times.dt.tz_convert("UTC").dt.tz_localize(None)
    return out.assign(time=times)


def read_snowfall_zip(path: Path, points: pd.DataFrame) -> pd.DataFrame:
    """Hourly snowfall (``time``, ``lat``, ``lon``, ``sf``) at the land nodes of ``points`` from a
    gridded CDS zip. Nodes are picked in xarray before any frame is built: an Italy-wide half-year
    is about 60 million grid-hours."""
    try:
        import xarray as xr
    except ImportError as error:
        raise RuntimeError("xarray is required: uv sync --group cds") from error

    land = points[points["land"]] if "land" in points.columns else points
    lats = xr.DataArray(land["lat"].round(2).to_numpy(), dims="node")
    lons = xr.DataArray(land["lon"].round(2).to_numpy(), dims="node")
    frames = []
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not name.endswith((".nc", ".nc4")):
                continue
            target = path.parent / f".{path.stem}_{Path(name).name}"
            with zf.open(name) as src, target.open("wb") as dst:
                dst.write(src.read())
            try:
                with xr.open_dataset(target) as ds:
                    if "sf" not in ds.data_vars:
                        continue
                    picked = ds["sf"].sel(
                        latitude=lats, longitude=lons, method="nearest", tolerance=0.01
                    )
                    frame = picked.to_dataframe().reset_index()
            finally:
                target.unlink(missing_ok=True)
            frame = frame.rename(columns={"valid_time": "time"})
            frames.append(
                frame.assign(
                    lat=land["lat"].round(2).to_numpy()[frame["node"].to_numpy()],
                    lon=land["lon"].round(2).to_numpy()[frame["node"].to_numpy()],
                )[["time", "lat", "lon", "sf"]]
            )
    if not frames:
        raise ValueError(f"no snowfall in {path}")
    return pd.concat(frames, ignore_index=True)


def backfill_cds_timeseries(
    client: CdsClient,
    store: WeatherStore,
    points: pd.DataFrame,
    timezone: str,
    start: date,
    end: date,
    log: Log = print,
    read: Callable[[Path], pd.DataFrame] = read_hourly_netcdf_zip,
    snowfall_area: tuple[float, float, float, float] | None = None,
    read_snowfall: Callable[[Path, pd.DataFrame], pd.DataFrame] = read_snowfall_zip,
) -> dict:
    """Fetch ``start..end`` node by node from the ERA5-Land time-series product, with snowfall
    from the gridded dataset, into the daily store under the same source id as ``backfill_cds``.

    The node series start a day early so each local day has its evening UTC hours. Snowfall is
    requested over ``snowfall_area`` (north, west, south, east), one area shared by every region
    so they all reuse one cache (CDS cost does not depend on area), else over the nodes' own bbox;
    it is deaccumulated per node over the whole range at once, so request edges lose nothing and
    only the range's very first hour counts as carry-over, as in a chunk.
    """
    land = points[points["land"]] if "land" in points.columns else points
    summary: dict = {"method": "timeseries", "rows": 0, "cached": 0, "fetched": 0}

    def fetch(request: CdsRequest) -> pd.DataFrame:
        cached = client.cache_path(request).exists()
        path = client.ensure(request, log=log)
        summary["cached" if cached else "fetched"] += 1
        return read(path)

    series = []
    for node in land.itertuples():
        request = CdsPointRequest(
            round(float(node.lat), 2), round(float(node.lon), 2), start - timedelta(days=1), end
        )
        series.append(_on_grid(fetch(request))[["time", "lat", "lon", *TIMESERIES_VARS.values()]])
        log(f"CDS time series {request.label}")
    hourly = pd.concat(series, ignore_index=True)

    snow = []
    area = snowfall_area or bbox_of_points(points)
    for request in snowfall_requests(area, start, end):
        cached = client.cache_path(request).exists()
        path = client.ensure(request, log=log)
        summary["cached" if cached else "fetched"] += 1
        snow.append(_on_grid(read_snowfall(path, points))[["time", "lat", "lon", "sf"]])
        log(f"CDS snowfall {request.label}")
    snowfall = (
        pd.concat(snow, ignore_index=True)
        .drop_duplicates(["time", "lat", "lon"])
        .sort_values(["lat", "lon", "time"])
    )
    snowfall = snowfall.reset_index(drop=True)
    snow_hours = pd.to_datetime(snowfall["time"]).dt.hour.to_numpy()
    snowfall["sf"] = snowfall.groupby(["lat", "lon"], sort=False)["sf"].transform(
        lambda s: _hourly_accumulation(s.to_numpy(dtype=float), snow_hours[s.index])
    )
    hourly = hourly.merge(snowfall, on=["time", "lat", "lon"], how="left")

    elevations = point_elevations(points)
    years = []
    for year in range(start.year, end.year + 1):
        first, last = max(start, date(year, 1, 1)), min(end, date(year, 12, 31))
        window = hourly[
            (hourly["time"] >= pd.Timestamp(first - timedelta(days=1)))
            & (hourly["time"] < pd.Timestamp(last + timedelta(days=1)))
        ]
        daily = aggregate_hourly_frame(window, timezone, elevations, accumulated=())
        dates = pd.to_datetime(daily["date"]).dt.date
        daily = daily[(dates >= first) & (dates <= last)]
        store.upsert_daily(daily)
        summary["rows"] += len(daily)
        years.append(year)
        log(f"CDS {year}: {len(daily)} values -> {store.partition_path(SOURCE_ID, year)}")
    (store.root / "cds_meta.json").write_text(
        json.dumps(
            {
                "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
                "source": SOURCE_ID,
                "dataset": f"{TIMESERIES_DATASET} + {CDS_DATASET} (snowfall)",
                "start": str(start),
                "end": str(end),
                "years": years,
                **summary,
            },
            indent=2,
        )
        + "\n"
    )
    return summary
