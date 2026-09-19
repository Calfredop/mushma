"""Season statistics per area and species: good days, their peak, how they compare with past
seasons, and the weather and sightings behind them (``.gavin-root/docs/time-views.md``).

A season is a calendar year. A **good day** is a cell-day scoring at least ``good_score``; an
area's good days are a typical woodland cell's, so comuni of any size compare fairly. Everything
over area-days runs in DuckDB: eleven seasons are four million rows, and the daily job has 1 GB.
"""

from datetime import date, timedelta

import duckdb
import pandas as pd

from api.model.rules import RuleSet, ddmm_day_of_year

YEAR_DAYS = 365
_REFERENCE_YEAR = 2001  # non-leap: day-of-year numbering matches api.model.series.day_of_year

Span = tuple[int, int]  # first and last day of a non-leap year
Scores = pd.DataFrame | duckdb.DuckDBPyRelation


def season_span(rules: RuleSet, keys: list[str]) -> Span:
    """The calendar span of the season windows of ``keys``: from the earliest window's
    ``zero_below`` to the latest ``zero_above``, both as days of a non-leap year. A window that
    wraps into the next year runs the span to 31 December."""
    starts, ends, wraps = [], [], False
    for key in keys:
        for factor in rules.species[key].enabled_factors:
            if factor.kind != "season_window":
                continue
            for window in factor.input.windows:
                start = ddmm_day_of_year(window.dates[0])
                end = ddmm_day_of_year(window.dates[3])
                starts.append(start)
                ends.append(end)
                wraps |= end < start
    if not starts:
        return 1, YEAR_DAYS
    return min(starts), YEAR_DAYS if wraps else max(ends)


def window_dates(span: Span, year: int) -> tuple[date, date]:
    """The span as dates of ``year`` (day numbers are non-leap, so 1 March stays 1 March)."""

    def to_date(doy: int) -> date:
        reference = date(_REFERENCE_YEAR, 1, 1) + timedelta(days=doy - 1)
        return reference.replace(year=year)

    return to_date(span[0]), to_date(span[1])


def _dates(values: pd.Series) -> pd.Series:
    return pd.to_datetime(values).dt.date


def _scores_view(con: duckdb.DuckDBPyConnection, scores: Scores) -> str:
    if isinstance(scores, pd.DataFrame):
        con.register("history_scores", scores)
    else:
        scores.create_view("history_scores", replace=True)
    return "history_scores"


def area_day_scores(
    scores: Scores,
    members: pd.DataFrame,
    good_score: float,
    con: duckdb.DuckDBPyConnection | None = None,
) -> pd.DataFrame:
    """``area_code, date, cells, good_cells, mean_score`` from cell scores ``cell_id, date,
    score`` (a frame, or a relation on ``con``): per area and day, how many of its woodland cells
    were scored and how many were good. Runs in DuckDB: a year of one key is millions of rows."""
    con = con or duckdb.connect()
    source = _scores_view(con, scores)
    con.register("history_members", members[["area_code", "cell_id"]])
    out = con.sql(
        f"""
        SELECT m.area_code, s.date, count(*)::INTEGER AS cells,
               sum(CASE WHEN s.score >= {float(good_score)} THEN 1 ELSE 0 END)::INTEGER
                   AS good_cells,
               avg(s.score) AS mean_score
        FROM {source} AS s JOIN history_members AS m USING (cell_id)
        GROUP BY m.area_code, s.date
        ORDER BY m.area_code, s.date
        """
    ).df()
    out["date"] = _dates(out["date"])
    return out


def area_good_days(
    scores: Scores,
    members: pd.DataFrame,
    good_score: float,
    con: duckdb.DuckDBPyConnection | None = None,
) -> pd.DataFrame:
    """``area_code, days, through, good_days``: per area, the days scored, the last of them, and
    a typical woodland cell's good days (the sum of each day's share of good cells, as
    :func:`season_scores` counts them). The taxon keys' seasons: their good days alone."""
    con = con or duckdb.connect()
    source = _scores_view(con, scores)
    con.register("history_members", members[["area_code", "cell_id"]])
    out = con.sql(
        f"""
        WITH days AS (
            SELECT m.area_code, s.date, count(*) AS cells,
                   sum(CASE WHEN s.score >= {float(good_score)} THEN 1 ELSE 0 END) AS good_cells
            FROM {source} AS s JOIN history_members AS m USING (cell_id)
            GROUP BY m.area_code, s.date
        )
        SELECT area_code, count(*)::INTEGER AS days, max(date) AS through,
               sum(good_cells::DOUBLE / cells) AS good_days
        FROM days GROUP BY area_code ORDER BY area_code
        """
    ).df()
    out["through"] = _dates(out["through"])
    return out


def cell_good_days(
    scores: Scores, good_score: float, con: duckdb.DuckDBPyConnection | None = None
) -> pd.DataFrame:
    """``cell_id, days, good_days``: per cell, the days scored and the good ones among them."""
    con = con or duckdb.connect()
    source = _scores_view(con, scores)
    return con.sql(
        f"""
        SELECT cell_id, count(*)::INTEGER AS days,
               sum(CASE WHEN score >= {float(good_score)} THEN 1 ELSE 0 END)::INTEGER AS good_days
        FROM {source} GROUP BY cell_id ORDER BY cell_id
        """
    ).df()


Frame = pd.DataFrame | duckdb.DuckDBPyRelation

# Day of a non-leap year (29 February counts as the 28th), as api.model.series.day_of_year.
_LEAP = "((year({d}) % 4 = 0 AND year({d}) % 100 <> 0) OR year({d}) % 400 = 0)"
_DOY = (
    "CASE WHEN month({d}) = 2 AND day({d}) = 29 THEN 59 "
    "WHEN month({d}) > 2 AND " + _LEAP + " THEN dayofyear({d}) - 1 "
    "ELSE dayofyear({d}) END"
)


def _doy(column: str) -> str:
    return _DOY.format(d=column)


def _view(con: duckdb.DuckDBPyConnection, name: str, source: Frame) -> str:
    """``source`` (a frame, or a relation on ``con``) as a view called ``name``."""
    if isinstance(source, pd.DataFrame):
        con.register(f"{name}_frame", source)
        con.execute(f"CREATE OR REPLACE TEMP VIEW {name} AS SELECT * FROM {name}_frame")
    else:
        source.create_view(name, replace=True)
    return name


def _days_view(con: duckdb.DuckDBPyConnection, area_days: Frame) -> str:
    """The area-day tallies with each day's share of good cells and its calendar."""
    raw = _view(con, "history_days_raw", area_days)
    con.execute(
        f"""
        CREATE OR REPLACE TEMP VIEW history_days AS
        SELECT area_code, species, CAST(date AS DATE) AS date, cells, good_cells,
               good_cells::DOUBLE / cells AS share,
               year(CAST(date AS DATE)) AS year, month(CAST(date AS DATE)) AS month,
               {_doy("CAST(date AS DATE)")} AS doy
        FROM {raw}
        """
    )
    return "history_days"


def _to_dates(frame: pd.DataFrame, *columns: str) -> pd.DataFrame:
    for column in columns:
        if column in frame:
            values = pd.to_datetime(frame[column])
            frame[column] = values.dt.date.astype(object).where(values.notna(), None)
    return frame


SEASON_KEYS = ["area_code", "species", "year"]


def season_scores(
    area_days: Frame, baseline_years: list[int], con: duckdb.DuckDBPyConnection | None = None
) -> pd.DataFrame:
    """One row per area, species and year from ``area_days`` (``area_code, species, date, cells,
    good_cells``): ``through`` (last day scored), ``days``, ``complete`` (every day of the year
    scored), ``cells`` (the most scored on a day), ``good_days`` (the sum of each day's share of
    good cells: a typical cell's good days, unbiased by a day that missed some cells),
    ``peak_date`` and ``peak_share`` (the first day with the largest share of good cells; none
    without a good day), and ``good_days_typical``: the median over the complete baseline seasons
    of their good days up to the same day of the year (the whole year for a complete season), with
    ``typical_years`` how many seasons that took.

    Runs in DuckDB over a frame or a relation: every stored year is millions of rows."""
    con = con or duckdb.connect()
    days = _days_view(con, area_days)
    con.execute(
        f"""
        CREATE OR REPLACE TEMP VIEW history_season_base AS
        SELECT area_code, species, year, max(date) AS through,
               count(DISTINCT date)::INTEGER AS days, max(cells)::INTEGER AS cells,
               sum(share) AS good_days,
               count(DISTINCT date) = CASE WHEN {_LEAP.format(d="max(date)")} THEN 366 ELSE 365 END
                   AS complete
        FROM {days} GROUP BY area_code, species, year
        """
    )
    # Hash aggregates only, no window sorts: they stay inside a small memory cap however many
    # seasons are stored.
    seasons = con.sql(
        f"""
        WITH peak_shares AS (
            SELECT area_code, species, year, max(share) AS peak_share
            FROM {days} GROUP BY area_code, species, year
        ),
        peaks AS (
            SELECT d.area_code, d.species, d.year, min(d.date) AS peak_date,
                   any_value(p.peak_share) AS peak_share
            FROM {days} AS d JOIN peak_shares AS p
              ON p.area_code = d.area_code AND p.species = d.species AND p.year = d.year
             AND d.share = p.peak_share
            GROUP BY d.area_code, d.species, d.year
        ),
        baseline AS (
            SELECT area_code, species, year AS baseline_year, good_days
            FROM history_season_base
            WHERE complete AND list_contains($years, year)
        ),
        targets AS (
            SELECT area_code, species, year, complete, {_doy("through")} AS doy_limit
            FROM history_season_base
        ),
        -- A complete season compares with whole baseline seasons; one under way with the
        -- baseline seasons up to its own last day of the year.
        limits AS (
            SELECT DISTINCT area_code, species, doy_limit FROM targets WHERE NOT complete
        ),
        partial AS (
            SELECT d.area_code, d.species, d.year AS baseline_year, l.doy_limit,
                   sum(d.share) AS good_days
            FROM {days} AS d
            JOIN baseline AS b
              ON b.area_code = d.area_code AND b.species = d.species AND b.baseline_year = d.year
            JOIN limits AS l ON l.area_code = d.area_code AND l.species = d.species
            WHERE d.doy <= l.doy_limit
            GROUP BY d.area_code, d.species, d.year, l.doy_limit
        ),
        typical AS (
            SELECT t.area_code, t.species, t.year,
                   median(b.good_days) AS good_days_typical,
                   count(DISTINCT b.baseline_year)::INTEGER AS typical_years
            FROM targets AS t JOIN baseline AS b
              ON b.area_code = t.area_code AND b.species = t.species
            WHERE t.complete
            GROUP BY t.area_code, t.species, t.year
            UNION ALL
            SELECT t.area_code, t.species, t.year,
                   median(pt.good_days) AS good_days_typical,
                   count(DISTINCT pt.baseline_year)::INTEGER AS typical_years
            FROM targets AS t JOIN partial AS pt
              ON pt.area_code = t.area_code AND pt.species = t.species
             AND pt.doy_limit = t.doy_limit
            WHERE NOT t.complete
            GROUP BY t.area_code, t.species, t.year
        )
        SELECT b.area_code, b.species, b.year, b.through, b.days, b.complete, b.cells,
               b.good_days, t.good_days_typical, coalesce(t.typical_years, 0) AS typical_years,
               CASE WHEN p.peak_share > 0 THEN p.peak_date END AS peak_date,
               CASE WHEN p.peak_share > 0 THEN p.peak_share ELSE 0.0 END AS peak_share
        FROM history_season_base AS b
        LEFT JOIN peaks AS p USING (area_code, species, year)
        LEFT JOIN typical AS t USING (area_code, species, year)
        ORDER BY b.area_code, b.species, b.year
        """,
        params={"years": [int(y) for y in baseline_years]},
    ).df()
    seasons["complete"] = seasons["complete"].astype(bool)
    return _to_dates(seasons, "through", "peak_date")


def month_scores(area_days: Frame, con: duckdb.DuckDBPyConnection | None = None) -> pd.DataFrame:
    """``area_code, species, year, month, days, good_days, good_share``: per month, a typical
    woodland cell's good days and the share of scored cell-days that were good."""
    con = con or duckdb.connect()
    days = _days_view(con, area_days)
    return con.sql(
        f"""
        SELECT area_code, species, year, month, count(DISTINCT date)::INTEGER AS days,
               sum(share) AS good_days, sum(good_cells)::DOUBLE / sum(cells) AS good_share
        FROM {days} GROUP BY area_code, species, year, month
        ORDER BY area_code, species, year, month
        """
    ).df()


def _weather_view(con: duckdb.DuckDBPyConnection, area_weather: Frame) -> str:
    """The observed (not forecast) area-days of weather."""
    raw = _view(con, "history_weather_raw", area_weather)
    con.execute(
        f"""
        CREATE OR REPLACE TEMP VIEW history_weather AS
        SELECT area_code, CAST(date AS DATE) AS date, precipitation_sum, precipitation_normal,
               temperature_2m_mean, temperature_normal
        FROM {raw} WHERE NOT forecast
        """
    )
    return "history_weather"


_WEATHER_TOTALS = """
    sum(w.precipitation_sum) AS rain_mm, sum(w.precipitation_normal) AS rain_normal_mm,
    avg(w.temperature_2m_mean) AS temp_c, avg(w.temperature_normal) AS temp_normal_c
"""


def weather_summary(
    area_weather: Frame, start: date, end: date, con: duckdb.DuckDBPyConnection | None = None
) -> pd.DataFrame:
    """Per area, over the observed (not forecast) days from ``start`` to ``end``: ``rain_mm`` and
    ``rain_normal_mm`` (totals), ``temp_c`` and ``temp_normal_c`` (means), ``through`` and
    ``days``. ``area_weather`` holds ``area_code, date, precipitation_sum, precipitation_normal,
    temperature_2m_mean, temperature_normal, forecast``."""
    con = con or duckdb.connect()
    weather = _weather_view(con, area_weather)
    out = con.sql(
        f"""
        SELECT w.area_code, {_WEATHER_TOTALS}, max(w.date) AS through,
               count(DISTINCT w.date)::INTEGER AS days
        FROM {weather} AS w WHERE w.date BETWEEN $start AND $end
        GROUP BY w.area_code ORDER BY w.area_code
        """,
        params={"start": start, "end": end},
    ).df()
    return _to_dates(out, "through")


def area_sightings(records: pd.DataFrame, members: pd.DataFrame, region_id: str) -> pd.DataFrame:
    """``area_code, species, date, count`` from per-cell counts ``species, cell_id, date,
    obscured, count``. An obscured record's cell is a town-centroid pin that may lie in another
    comune, so it counts towards the region only."""
    joined = records.merge(members, on="cell_id", how="inner")
    kept = joined[(joined["area_code"] == region_id) | ~joined["obscured"].astype(bool)]
    return kept.groupby(["area_code", "species", "date"], as_index=False)["count"].sum()


SPECIES_ALL = "combined"
WEATHER_COLUMNS = ["rain_mm", "rain_normal_mm", "temp_c", "temp_normal_c"]


def _sightings_by(sightings: pd.DataFrame, species: list[str], keys: list[str]) -> pd.DataFrame:
    """Counts per ``keys`` for each of ``species``; the combined score counts every species'."""
    counts = sightings.assign(date=pd.to_datetime(sightings["date"]))
    counts = counts.assign(year=counts["date"].dt.year, month=counts["date"].dt.month)
    frames = []
    for sp in species:
        chosen = counts if sp == SPECIES_ALL else counts[counts["species"] == sp]
        by = [k for k in keys if k != "species"]
        frames.append(chosen.groupby(by, as_index=False)["count"].sum().assign(species=sp))
    frames = [f for f in frames if not f.empty]
    if not frames:
        return pd.DataFrame(columns=[*keys, "sightings"])
    joined = pd.concat(frames, ignore_index=True).rename(columns={"count": "sightings"})
    return joined.astype({"year": int})[[*keys, "sightings"]]


def assemble_seasons(
    area_days: Frame,
    area_weather: Frame,
    sightings: pd.DataFrame,
    windows: dict[str, Span],
    baseline_years: list[int],
    con: duckdb.DuckDBPyConnection | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The stored season and month tables.

    Seasons: :func:`season_scores` plus the species' season window (``window_start``,
    ``window_end``), the rain and temperature over the observed days of that window against normal
    (never past the season's last scored day) and the calendar year's sightings. Months:
    :func:`month_scores` plus each month's observed rain and temperature and its sightings.
    ``sightings`` holds ``area_code, species, date, count`` (small: counts only).

    ``area_days`` and ``area_weather`` may be frames or relations on ``con``: the build passes
    relations over the stored partitions, so no year is ever loaded whole into memory."""
    con = con or duckdb.connect()
    seasons = season_scores(area_days, baseline_years, con)
    months = month_scores(area_days, con)
    weather = _weather_view(con, area_weather)

    spans = seasons.groupby(["species", "year"], as_index=False)["through"].max()
    rows = []
    for row in spans.itertuples():
        start, end = window_dates(windows[row.species], int(row.year))
        rows.append(
            {
                "species": row.species,
                "year": int(row.year),
                "window_start": start,
                "window_end": end,
                # A season scored in part keeps its weather in step with its scores.
                "weather_end": min(end, row.through),
            }
        )
    spans = pd.DataFrame(
        rows, columns=["species", "year", "window_start", "window_end", "weather_end"]
    )
    seasons = seasons.merge(spans[["species", "year", "window_start", "window_end"]], how="left")

    con.register("history_spans", spans)
    season_weather = con.sql(
        f"""
        SELECT s.species, s.year, w.area_code, {_WEATHER_TOTALS}, max(w.date) AS weather_through
        FROM history_spans AS s
        JOIN {weather} AS w ON w.date BETWEEN CAST(s.window_start AS DATE)
                                          AND CAST(s.weather_end AS DATE)
        GROUP BY s.species, s.year, w.area_code
        """
    ).df()
    seasons = seasons.merge(season_weather, on=SEASON_KEYS, how="left")
    seasons = _to_dates(seasons, "window_start", "window_end", "weather_through")
    species = sorted(seasons["species"].unique())
    seasons = seasons.merge(_sightings_by(sightings, species, SEASON_KEYS), how="left")
    seasons["sightings"] = seasons["sightings"].fillna(0).astype(int)

    month_weather = con.sql(
        f"""
        SELECT w.area_code, year(w.date) AS year, month(w.date) AS month, {_WEATHER_TOTALS}
        FROM {weather} AS w GROUP BY ALL
        """
    ).df()
    months = months.merge(month_weather, on=["area_code", "year", "month"], how="left")
    months = months.merge(
        _sightings_by(sightings, species, [*SEASON_KEYS, "month"]),
        on=[*SEASON_KEYS, "month"],
        how="left",
    )
    months["sightings"] = months["sightings"].fillna(0).astype(int)
    return seasons, months
