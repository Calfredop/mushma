"""Build the time views' tables: weather normals, per-area history and the outlook's areas.

    uv run python -m api.history.build normals                 # after the backfill, then yearly
    uv run python -m api.history.build update --years 2016-2026
    uv run python -m api.history.build update                  # this year (the daily job)
    uv run python -m api.history.build outlook                 # after api.weather.seasonal fetch

Reads the grid, the weather store, the score store and the sightings store; writes
``$DATA_DIR/climatology/<region>/`` and ``$DATA_DIR/history/<region>/`` (``api.history.store``).
Every command is safe to re-run: a year is rebuilt whole, and the season and month tables are
rebuilt from every stored year. See ``.gavin-root/docs/time-views.md``.
"""

import argparse
import json
import time
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import duckdb
import pandas as pd

from api.grid.sources import data_dir, load_sources
from api.history.areas import (
    aggregate_to_areas,
    area_members,
    area_point_weights,
    area_table,
    lapse_offsets,
)
from api.history.config import HistoryConfig, load_history_config, rain_lead_days
from api.history.normals import complete_years, daily_normals
from api.history.plausible import area_fit, static_fit
from api.history.seasons import (
    SPECIES_ALL,
    area_day_scores,
    area_good_days,
    area_sightings,
    assemble_seasons,
    cell_good_days,
    season_span,
)
from api.history.store import ClimatologyStore, HistoryStore
from api.model.config import ModelConfig, load_model_config
from api.model.inputs import load_cells
from api.model.rules import load_rules
from api.model.series import day_of_year
from api.model.store import ScoreStore
from api.regions import region_display_name
from api.sightings.store import SightingsStore
from api.timeutil import today_rome
from api.weather.config import WeatherConfig, load_weather_config
from api.weather.ingest import region_paths
from api.weather.seasonal import outlook_dir

Log = Callable[[str], None]
RAIN = "precipitation_sum"
TEMPERATURE = "temperature_2m_mean"
MEMORY_LIMIT = "256MB"
CELL_COLUMNS = [
    "cell_id",
    "woodland",
    "comune_code",
    "comune_name",
    "province",
    "lon",
    "lat",
    "elevation_m",
]


def history_connection(root: Path) -> duckdb.DuckDBPyConnection:
    """A DuckDB connection capped at MEMORY_LIMIT, spilling to ``$DATA_DIR/tmp/duckdb`` beyond
    it: every stored season is millions of area-days and the daily job has a 1 GB machine."""
    temp = root / "tmp" / "duckdb"
    temp.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(
        config={
            "memory_limit": MEMORY_LIMIT,
            "temp_directory": str(temp),
            # Output order is set by the queries' ORDER BY; not keeping scan order saves memory.
            "preserve_insertion_order": False,
            "threads": 2,
        }
    )


def _stores(region: str, root: Path) -> tuple[ClimatologyStore, HistoryStore]:
    return (
        ClimatologyStore(root / "climatology" / region),
        HistoryStore(root / "history" / region),
    )


def build_normals(
    region: str,
    root: Path | None = None,
    config: HistoryConfig | None = None,
    weather_config: WeatherConfig | None = None,
    log: Log = lambda message: None,
    con: duckdb.DuckDBPyConnection | None = None,
) -> dict:
    """Daily normals per weather point over the complete reanalysis years of the baseline."""
    root = root or data_dir()
    con = con or history_connection(root)
    config = config or load_history_config()
    weather_config = weather_config or load_weather_config()
    _, weather, _ = region_paths(region, root)
    climatology, _ = _stores(region, root)
    points = pd.read_parquet(weather.points_path)
    points = points[points["land"]] if "land" in points else points
    point_ids = sorted(points["point_id"])
    variables = list(config.normals.variables)
    source = weather_config.history.model
    first, last = config.baseline.start_year, config.baseline.end_year

    rows = pd.DataFrame(columns=["point_id", "date", "variable", "value"])
    files = [str(p) for p in weather.daily_files() if f"source={source}" in str(p)]
    if files:
        rows = con.execute(
            f"""
            SELECT point_id, date, variable, value
            FROM read_parquet({files!r}, hive_partitioning=false)
            WHERE source = ? AND variable IN (SELECT unnest(?))
              AND year(date) BETWEEN ? AND ?
            """,
            [source, variables, first, last],
        ).df()
    years = complete_years(rows, point_ids, variables)
    normals = daily_normals(rows, years, config.normals.window_days)
    meta = {
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source": source,
        "variables": variables,
        "window_days": config.normals.window_days,
        "baseline": [first, last],
        "years": years,
        "points": len(point_ids),
    }
    climatology.write_normals(normals, meta)
    log(f"normals: {len(point_ids)} points x {variables} over {years}")
    return meta


class _AreaWeather:
    """How weather points roll up into each area, for rain and mean temperature."""

    def __init__(
        self,
        cells: pd.DataFrame,
        members: pd.DataFrame,
        weights: pd.DataFrame,
        point_cells: pd.DataFrame,
        weather_config: WeatherConfig,
        model_config: ModelConfig,
    ) -> None:
        rain_var = weather_config.variables[RAIN]
        temperature_var = weather_config.variables[TEMPERATURE]
        scale = model_config.precipitation_scale
        factor = pd.Series(
            scale.factor(cells["elevation_m"].to_numpy(dtype=float)), index=cells["cell_id"]
        )
        self.rain = area_point_weights(members, weights, rain_var.downscale)
        self.rain_scaled = area_point_weights(
            members, weights, rain_var.downscale, cell_factor=factor
        )
        self.scaled_sources = set(scale.sources) if scale.enabled else set()
        self.temperature = area_point_weights(members, weights, temperature_var.downscale)
        history = weather_config.history.model
        heights = point_cells[point_cells["source"] == history].set_index("point_id")["elevation_m"]
        self.offset = (
            lapse_offsets(
                members,
                weights,
                temperature_var.downscale,
                cells,
                heights,
                temperature_var.lapse_rate_c_per_km,
            )
            if temperature_var.lapse_rate_c_per_km is not None
            else None
        )
        self.history_source = history

    def rain_values(self, rows: pd.DataFrame) -> pd.DataFrame:
        values = rows.assign(scaled=rows["source"].isin(self.scaled_sources))
        return aggregate_to_areas(values, self.rain, scaled_weights=self.rain_scaled)

    def temperature_values(self, rows: pd.DataFrame) -> pd.DataFrame:
        return aggregate_to_areas(rows, self.temperature, offset=self.offset)

    def normals(self, point_normals: pd.DataFrame) -> pd.DataFrame:
        """Per area and day of year: normals come from the reanalysis, so rain is scaled."""
        by_variable = {}
        for variable in (RAIN, TEMPERATURE):
            rows = point_normals[point_normals["variable"] == variable].rename(
                columns={"doy": "date", "normal": "value"}
            )
            if variable == RAIN:
                out = self.rain_values(rows.assign(source=self.history_source))
            else:
                out = self.temperature_values(rows)
            by_variable[variable] = out.rename(columns={"date": "doy", "value": variable})
        merged = by_variable[RAIN].merge(by_variable[TEMPERATURE], on=["area_code", "doy"])
        return merged.rename(
            columns={RAIN: "precipitation_normal", TEMPERATURE: "temperature_normal"}
        )


def _area_weather_year(
    con: duckdb.DuckDBPyConnection,
    root: Path,
    region: str,
    year: int,
    rollup: _AreaWeather,
    area_normals: pd.DataFrame,
    weather_config: WeatherConfig,
) -> pd.DataFrame:
    _, weather, _ = region_paths(region, root)
    order = weather_config.source_order
    if not weather.daily_files():
        return pd.DataFrame()
    best = weather.best_daily(
        con, date(year, 1, 1), date(year, 12, 31), order, [RAIN, TEMPERATURE]
    ).df()
    if best.empty:
        return pd.DataFrame()
    best["date"] = pd.to_datetime(best["date"]).dt.date
    rain = rollup.rain_values(best[best["variable"] == RAIN])
    temperature = rollup.temperature_values(best[best["variable"] == TEMPERATURE])
    frame = rain.rename(columns={"value": RAIN}).merge(
        temperature.rename(columns={"value": TEMPERATURE}), on=["area_code", "date"], how="outer"
    )
    # A day leans on the forecast when any point's value came from it.
    forecast_days = set(best.loc[best["source"] != weather_config.history.model, "date"])
    frame["forecast"] = frame["date"].isin(forecast_days)
    frame["doy"] = day_of_year(pd.to_datetime(frame["date"]).to_numpy().astype("datetime64[D]"))
    frame = frame.merge(area_normals, on=["area_code", "doy"], how="left").drop(columns="doy")
    return frame.sort_values(["area_code", "date"]).reset_index(drop=True)


def _score_years(seasons: pd.DataFrame, region: str, baseline: list[int]) -> list[int]:
    """Seasons inside the baseline scored on every day for the whole region and every species.
    (Each area's "typical" uses its own complete seasons.)"""
    if seasons.empty:
        return []
    complete = seasons[seasons["area_code"] == region].groupby("year")["complete"].all()
    return sorted(int(y) for y, ok in complete.items() if ok and y in baseline)


def _taxon_seasons(
    con: duckdb.DuckDBPyConnection,
    scores: ScoreStore,
    keys: list[str],
    members: pd.DataFrame,
    year: int,
    last_day: date,
    config: HistoryConfig,
) -> pd.DataFrame:
    """Each taxon key's good days per area in ``year``, up to ``last_day``."""
    end = min(date(year, 12, 31), last_day)
    frames = []
    for key in keys:
        path = scores.partition_path(key, year)
        if not path.exists():
            continue
        relation = con.sql(
            f"SELECT cell_id, date, score FROM read_parquet('{path}') WHERE date <= DATE '{end}'"
        )
        frames.append(
            area_good_days(relation, members, config.good_score, con).assign(species=key, year=year)
        )
    frames = [f for f in frames if not f.empty]
    if not frames:
        return pd.DataFrame()
    columns = ["area_code", "species", "year", "days", "through", "good_days"]
    return pd.concat(frames, ignore_index=True)[columns]


def update_history(
    region: str,
    years: list[int],
    root: Path | None = None,
    log: Log = lambda message: None,
    today: date | None = None,
) -> dict:
    """Rebuild the weather normals, the per-area tables of ``years``, and the season and month
    tables from every stored year.

    History stops at yesterday: the days from today on are forecast scores, which the map shows
    but a season's record should not count."""
    root = root or data_dir()
    last_day = (today or today_rome()) - timedelta(days=1)
    config = load_history_config()
    weather_config = load_weather_config()
    model_config = load_model_config(region=region)
    rules = load_rules(region)
    climatology, store = _stores(region, root)
    con = history_connection(root)
    # About a second: rebuilt every time, so the normals follow the backfill as it adds years.
    build_normals(region, root, config, weather_config, log, con)

    grid_dir, weather, _ = region_paths(region, root)
    cells = pd.read_parquet(grid_dir / "cells.parquet", columns=CELL_COLUMNS)
    woodland = cells[cells["woodland"]].reset_index(drop=True)
    members = area_members(cells, region)
    weights = pd.read_parquet(weather.weights_path)
    # Only areas with weather can have seasons: a comune whose woodland no weather point reaches
    # (Isola del Giglio) would list with nothing behind it.
    served = cells[cells["cell_id"].isin(set(weights["cell_id"]))]
    store.write(store.areas_path, area_table(served, region, region_display_name(region)))
    fits = static_fit(rules, load_cells(grid_dir))
    store.write(store.area_fit_path, area_fit(fits, members, config.plausible_fit))

    rollup = _AreaWeather(
        woodland,
        members,
        weights,
        weather.read_point_cells(),
        weather_config,
        model_config,
    )
    area_normals = rollup.normals(climatology.read_normals())
    store.write(store.area_normals_path, area_normals)

    keys = [*rules.groups, SPECIES_ALL]
    scores = ScoreStore(root / "scores" / region)
    for year in [y for y in years if y <= last_day.year]:
        area_weather = _area_weather_year(
            con, root, region, year, rollup, area_normals, weather_config
        )
        if not area_weather.empty:
            store.write_partition("area_weather", year, area_weather)
        day_frames, cell_frames = [], []
        for key in keys:
            path = scores.partition_path(key, year)
            if not path.exists():
                continue
            end = min(date(year, 12, 31), last_day)
            relation = con.sql(
                f"SELECT cell_id, date, score FROM read_parquet('{path}') "
                f"WHERE date <= DATE '{end}'"
            )
            day_frames.append(
                area_day_scores(relation, members, config.good_score, con).assign(species=key)
            )
            cell_frames.append(cell_good_days(relation, config.good_score, con).assign(species=key))
        days = pd.concat([f for f in day_frames if not f.empty] or [pd.DataFrame()])
        if not days.empty:
            store.write_partition("area_days", year, days)
            store.write_partition(
                "cell_seasons", year, pd.concat([f for f in cell_frames if not f.empty])
            )
        taxa = _taxon_seasons(con, scores, list(rules.species), members, year, last_day, config)
        if not taxa.empty:
            store.write_partition("taxon_seasons", year, taxa)
        log(f"history {year}: {len(area_weather)} area-days of weather, {len(days)} of scores")

    records = SightingsStore(root / "sightings" / region).daily_counts_by_cell(con).df()
    records["date"] = pd.to_datetime(records["date"]).dt.date
    sightings = area_sightings(records, members, region)
    store.write(store.area_sightings_path, sightings)

    windows = {group: season_span(rules, keys_) for group, keys_ in rules.groups.items()}
    windows[SPECIES_ALL] = season_span(rules, list(rules.species))
    days = store.relation(con, "area_days")
    if days is None:
        log("history: no scored seasons yet")
        seasons = months = pd.DataFrame()
    else:
        weather = store.relation(con, "area_weather")
        if weather is None:
            weather = con.sql(
                f"""
            SELECT NULL::VARCHAR AS area_code, NULL::DATE AS date, NULL::DOUBLE AS {RAIN},
                   NULL::DOUBLE AS precipitation_normal, NULL::DOUBLE AS {TEMPERATURE},
                   NULL::DOUBLE AS temperature_normal, NULL::BOOLEAN AS forecast
            WHERE false
            """
            )
        seasons, months = assemble_seasons(
            days, weather, sightings, windows, config.baseline.years, con
        )
        store.write(store.seasons_path, seasons)
        store.write(store.months_path, months)

    catalog = load_sources()
    credits = [*weather_config.credits, "gbif", "inaturalist"]
    meta = {
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "region": region,
        "good_score": config.good_score,
        "plausible_fit": config.plausible_fit,
        "groups": {group: list(keys_) for group, keys_ in rules.groups.items()},
        "taxa": {
            key: {"taxon": spec.taxon, "i18n_key": spec.i18n_key}
            for key, spec in rules.species.items()
        },
        "baseline": [config.baseline.start_year, config.baseline.end_year],
        "weather_years": climatology.read_meta().get("years", []),
        "score_years": _score_years(seasons, region, config.baseline.years),
        "years": store.years("area_days"),
        "windows": {species: [int(start), int(end)] for species, (start, end) in windows.items()},
        "rain_lead": {
            group: list(rain_lead_days(rules, keys_)) for group, keys_ in rules.groups.items()
        },
        "sources": {
            source_id: {
                "name": catalog[source_id].name,
                "license": catalog[source_id].license,
                "attribution": catalog[source_id].attribution,
            }
            for source_id in credits
            if source_id in catalog
        },
    }
    store.write_meta(meta)
    return meta


def build_outlook_areas(region: str, root: Path | None = None, log: Log = print) -> int:
    """Average the latest long-range forecast (``api.weather.seasonal``) over each area, with the
    plain downscaling weights: it is compared with its own climate, so no height scaling."""
    root = root or data_dir()
    _, store = _stores(region, root)
    path = outlook_dir(region, root) / "seasonal.parquet"
    if not path.exists():
        log("outlook: no long-range forecast fetched yet")
        return 0
    rows = pd.read_parquet(path)
    rows["start"] = pd.to_datetime(rows["start"]).dt.date
    rows["end"] = pd.to_datetime(rows["end"]).dt.date
    grid_dir, weather, _ = region_paths(region, root)
    cells = pd.read_parquet(grid_dir / "cells.parquet", columns=CELL_COLUMNS)
    members = area_members(cells, region)
    weather_config = load_weather_config()
    weights_table = pd.read_parquet(weather.weights_path)
    frames = []
    for variable, group in rows.groupby("variable"):
        weights = area_point_weights(
            members, weights_table, weather_config.variables[str(variable)].downscale
        )
        for (kind, start, end), period in group.groupby(["kind", "start", "end"]):
            parts = {}
            for column in ("value", "anomaly"):
                values = period[["point_id", column]].rename(columns={column: "value"})
                parts[column] = aggregate_to_areas(values.assign(date=start), weights)
            merged = parts["value"].merge(
                parts["anomaly"].rename(columns={"value": "anomaly"}), on=["area_code", "date"]
            )
            frames.append(
                merged.drop(columns="date").assign(
                    kind=kind,
                    start=start,
                    end=end,
                    variable=variable,
                    fetched_at=period["fetched_at"].max(),
                )
            )
    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    store.write(store.area_seasonal_path, out)
    log(f"outlook: {len(out)} area periods")
    return len(out)


def _years(text: str) -> list[int]:
    if "-" in text:
        first, last = (int(part) for part in text.split("-", 1))
        return list(range(first, last + 1))
    return [int(part) for part in text.split(",")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["normals", "update", "outlook"])
    parser.add_argument("--region", default="tuscany")
    parser.add_argument(
        "--years", type=_years, help="update: 2016-2026 or 2024,2025 (default: this year)"
    )
    args = parser.parse_args()
    started = time.monotonic()

    def log(message: str) -> None:
        print(f"[{time.monotonic() - started:7.1f}s] {message}", flush=True)

    if args.command == "normals":
        log(json.dumps(build_normals(args.region, log=log)))
    elif args.command == "update":
        years = args.years or [today_rome().year]
        meta = update_history(args.region, years, log=log)
        log(json.dumps({k: meta[k] for k in ("years", "weather_years", "score_years")}))
    else:
        build_outlook_areas(args.region, log=log)


if __name__ == "__main__":
    main()
