"""The time views (M6) served from the history tables ``api.history.build`` writes: comuni,
season comparison, the season map, the seasonal outlook and an area's plausible species.
``LiveRepository`` delegates here.
"""

from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from api.history.config import HistoryConfig, load_history_config
from api.history.outlook import (
    daily_signal,
    mean_temperature_anomaly,
    outlook_periods,
    period_starts,
    rain_share,
    rain_totals,
    tilt,
    typical_for_period,
)
from api.history.seasons import window_dates
from api.history.store import HistoryStore
from api.jobs.daily import WINDOW_FORWARD_DAYS
from api.models import (
    Area,
    Baseline,
    CellSeason,
    Comune,
    ComuneSeason,
    ComuniResponse,
    MonthStat,
    OutlookPeriod,
    OutlookResponse,
    PlausibleSpeciesResponse,
    RainLead,
    RainStat,
    RainTiltBands,
    SeasonMapResponse,
    SeasonsResponse,
    SeasonSummary,
    SeasonToDate,
    SeasonWindow,
    SpeciesProfile,
    SpeciesSeason,
    TaxonProfile,
    TemperatureStat,
)
from api.repository import AreaNotFound, HistoryUnavailable, SeasonNotFound
from api.species import SPECIES, Species, SpeciesOrCombined
from api.timeutil import ROME_TZ, today_rome
from api.weather.config import load_weather_config

# The served forecast's reach (the daily job scores to today +7): the outlook starts after it.
FORECAST_DAYS = WINDOW_FORWARD_DAYS


def _number(value: object) -> float | None:
    if value is None or (isinstance(value, float) and np.isnan(value)) or pd.isna(value):
        return None
    return float(value)


def _day(value: object) -> date | None:
    if value is None or pd.isna(value):
        return None
    return pd.Timestamp(value).date()


def _rain(total: object, normal: object) -> RainStat | None:
    total, normal = _number(total), _number(normal)
    if total is None or normal is None:
        return None
    return RainStat(total_mm=max(total, 0.0), normal_mm=max(normal, 0.0))


def _temperature(mean: object, normal: object) -> TemperatureStat | None:
    mean, normal = _number(mean), _number(normal)
    if mean is None or normal is None:
        return None
    return TemperatureStat(mean_c=mean, normal_c=normal)


class TimeViews:
    def __init__(
        self,
        root: Path,
        region: str,
        cells: pd.DataFrame,
        config: HistoryConfig | None = None,
        today=today_rome,
    ) -> None:
        self.store = HistoryStore(root / "history" / region)
        self.region = region
        self.cells = cells
        self.config = config or load_history_config()
        self.today = today
        seasonal = load_weather_config().seasonal
        # How far the long-range weeks reach (EC46); months take over after them.
        self.week_horizon_days = seasonal.forecast_days.get("weekly", 0) if seasonal else 0

    # --- shared ------------------------------------------------------------------------------

    def _require(self) -> None:
        if not self.store.areas_path.exists() or not self.store.seasons_path.exists():
            raise HistoryUnavailable(
                "history not built yet: run `python -m api.history.build update`"
            )

    def _areas(self) -> pd.DataFrame:
        self._require()
        return self.store.read_areas()

    def _area(self, comune: str | None) -> tuple[str, Area]:
        areas = self._areas().set_index("area_code")
        if comune is None:
            return self.region, Area(
                code=None, name=str(areas.loc[self.region, "name"]), kind="region"
            )
        if comune not in areas.index or areas.loc[comune, "kind"] != "comune":
            raise AreaNotFound(comune)
        return comune, Area(code=comune, name=str(areas.loc[comune, "name"]), kind="comune")

    def _baseline(self) -> Baseline:
        meta = self.store.read_meta()
        return Baseline(
            weather_years=list(meta.get("weather_years", [])),
            score_years=list(meta.get("score_years", [])),
        )

    def _good_score(self) -> float:
        return float(self.store.read_meta().get("good_score", self.config.good_score))

    # --- comuni ------------------------------------------------------------------------------

    def get_comuni(self) -> ComuniResponse:
        areas = self._areas()
        comuni = areas[areas["kind"] == "comune"].copy()
        comuni = comuni.iloc[comuni["name"].str.casefold().argsort(kind="stable")]
        return ComuniResponse(
            comuni=[
                Comune(
                    code=r.area_code,
                    name=r.name,
                    province=r.province or "",
                    lon=float(r.lon),
                    lat=float(r.lat),
                    cells=int(r.cells),
                )
                for r in comuni.itertuples()
            ]
        )

    # --- seasons -----------------------------------------------------------------------------

    def get_seasons(self, species: SpeciesOrCombined, comune: str | None) -> SeasonsResponse:
        code, area = self._area(comune)
        seasons = self.store.read_seasons()
        seasons = seasons[(seasons["area_code"] == code) & (seasons["species"] == species)]
        months = self.store.read_months()
        months = months[(months["area_code"] == code) & (months["species"] == species)]
        by_year = {int(year): rows for year, rows in months.groupby("year")}
        summaries = [
            self._summary(row, by_year.get(int(row.year), months.iloc[0:0]))
            for row in seasons.sort_values("year").itertuples()
        ]
        return SeasonsResponse(
            species=species,
            area=area,
            good_score=self._good_score(),
            baseline=self._baseline(),
            seasons=summaries,
        )

    def _summary(self, row, months: pd.DataFrame) -> SeasonSummary:
        return SeasonSummary(
            year=int(row.year),
            complete=bool(row.complete),
            through=_day(row.through),
            good_days=max(float(row.good_days), 0.0),
            good_days_typical=_number(row.good_days_typical),
            peak_date=_day(row.peak_date),
            peak_share=min(max(float(row.peak_share), 0.0), 1.0),
            window=SeasonWindow(start=_day(row.window_start), end=_day(row.window_end)),
            rain=_rain(row.rain_mm, row.rain_normal_mm),
            temperature=_temperature(row.temp_c, row.temp_normal_c),
            weather_through=_day(row.weather_through),
            sightings=int(row.sightings),
            months=[
                MonthStat(
                    month=int(m.month),
                    good_days=max(float(m.good_days), 0.0),
                    rain=_rain(m.rain_mm, m.rain_normal_mm),
                    temperature=_temperature(m.temp_c, m.temp_normal_c),
                    sightings=int(m.sightings),
                )
                for m in months.sort_values("month").itertuples()
            ],
        )

    def get_season_map(self, year: int, species: SpeciesOrCombined) -> SeasonMapResponse:
        self._require()
        available = self.store.years("cell_seasons")
        if year not in available:
            raise SeasonNotFound(year, available)
        good = self.store.read_cell_seasons(year, species)
        placed = good.merge(self.cells[["cell_id", "lon", "lat"]], on="cell_id", how="inner")
        seasons = self.store.read_seasons()
        seasons = seasons[(seasons["year"] == year) & (seasons["species"] == species)]
        region = seasons[seasons["area_code"] == self.region]
        if region.empty:
            raise SeasonNotFound(year, available)
        areas = self._areas()
        comuni = seasons.merge(
            areas[areas["kind"] == "comune"][["area_code", "name"]], on="area_code", how="inner"
        ).sort_values(["good_days", "name"], ascending=[False, True])
        head = region.iloc[0]
        return SeasonMapResponse(
            year=year,
            species=species,
            complete=bool(head["complete"]),
            through=_day(head["through"]),
            good_score=self._good_score(),
            cells=[
                CellSeason(
                    cell_id=r.cell_id,
                    lon=float(r.lon),
                    lat=float(r.lat),
                    good_days=int(r.good_days),
                )
                for r in placed.itertuples()
            ],
            comuni=[
                ComuneSeason(
                    code=r.area_code,
                    name=r.name,
                    good_days=max(float(r.good_days), 0.0),
                    good_days_typical=_number(r.good_days_typical),
                    rain=_rain(r.rain_mm, r.rain_normal_mm),
                    temperature=_temperature(r.temp_c, r.temp_normal_c),
                    sightings=int(r.sightings),
                )
                for r in comuni.itertuples()
            ],
        )

    # --- plausible species -------------------------------------------------------------------

    def get_species(self, comune: str | None) -> PlausibleSpeciesResponse:
        code, area = self._area(comune)
        meta = self.store.read_meta()
        groups, taxa = meta.get("groups"), meta.get("taxa")
        if not groups or not taxa or not self.store.area_fit_path.exists():
            raise HistoryUnavailable(
                "plausible species not built yet: run `python -m api.history.build update`"
            )
        fit = self.store.read_area_fit()
        fit = fit[fit["area_code"] == code].set_index("species")["fit_share"]
        seasons = self.store.read_seasons()
        seasons = seasons[seasons["area_code"] == code]
        taxon_seasons = self.store.read_taxon_seasons(code)

        def share(species: str) -> float:
            value = _number(fit.get(species))
            return min(max(value, 0.0), 1.0) if value is not None else 0.0

        def by_year(rows: pd.DataFrame) -> list[SpeciesSeason]:
            return [
                SpeciesSeason(year=int(r.year), good_days=max(float(r.good_days), 0.0))
                for r in rows.sort_values("year").itertuples()
            ]

        profiles = [
            SpeciesProfile(
                species=group,
                fit_share=share(group),
                seasons=by_year(seasons[seasons["species"] == group]),
                taxa=[
                    TaxonProfile(
                        key=key,
                        taxon=str(taxa[key]["taxon"]),
                        i18n_key=str(taxa[key]["i18n_key"]),
                        fit_share=share(key),
                        seasons=by_year(taxon_seasons[taxon_seasons["species"] == key]),
                    )
                    for key in groups[group]
                    if key in taxa
                ],
            )
            for group in groups
            if group in SPECIES
        ]
        return PlausibleSpeciesResponse(
            area=area,
            plausible_fit=float(meta.get("plausible_fit", self.config.plausible_fit)),
            good_score=self._good_score(),
            species=profiles,
        )

    # --- outlook -----------------------------------------------------------------------------

    def get_outlook(self, species: Species, comune: str | None) -> OutlookResponse:
        code, area = self._area(comune)
        today = self.today()
        meta = self.store.read_meta()
        span = meta.get("windows", {}).get(species)
        lead = meta.get("rain_lead", {}).get(species)
        if span is None or lead is None:
            raise HistoryUnavailable(f"no season window or rain lead for {species} in history meta")
        start, end = window_dates((int(span[0]), int(span[1])), today.year)
        window = SeasonWindow(start=start, end=end)
        lead_min, lead_max = int(lead[0]), int(lead[1])
        baseline = self._baseline()

        seasonal = self.store.read_area_seasonal()
        seasonal = seasonal[seasonal["area_code"] == code]
        months_ahead = self.config.outlook.months_ahead
        weeks, months = period_starts(today, self.week_horizon_days, months_ahead + 2)
        periods = outlook_periods(today, FORECAST_DAYS, weeks, months, (start, end), months_ahead)

        observed = self.store.read_area_weather(years=[today.year - 1, today.year], area_code=code)
        if observed.empty:
            observed = pd.DataFrame(
                columns=[
                    "date",
                    "precipitation_sum",
                    "precipitation_normal",
                    "temperature_2m_mean",
                    "temperature_normal",
                ]
            )
        signal = daily_signal(observed, seasonal)
        area_days = self.store.read_area_days(
            years=baseline.score_years or None, species=species, area_code=code
        )
        if area_days.empty:
            area_days = pd.DataFrame(columns=["date", "cells", "good_cells"])

        out = []
        for period in periods:
            typical = typical_for_period(
                area_days, period, baseline.score_years, self.config.outlook.good_share
            )
            totals = rain_totals(signal, period.start, period.end)
            lead_pct = rain_share(
                signal,
                period.start - timedelta(days=lead_max),
                period.end - timedelta(days=lead_min),
            )
            out.append(
                OutlookPeriod(
                    start=period.start,
                    end=period.end,
                    kind=period.kind,
                    past_good_years=typical.good_years,
                    past_years=typical.years,
                    rain=_rain(*totals) if totals else None,
                    temperature_anomaly_c=mean_temperature_anomaly(
                        signal, period.start, period.end
                    ),
                    lead_rain_pct=max(lead_pct, 0.0) if lead_pct is not None else None,
                    outlook=tilt(lead_pct, self.config.outlook.rain),
                )
            )

        issued = None
        if not seasonal.empty and "fetched_at" in seasonal:
            fetched = pd.Timestamp(seasonal["fetched_at"].max())
            if not pd.isna(fetched):
                stamp = fetched.tz_localize("UTC") if fetched.tzinfo is None else fetched
                issued = datetime.fromtimestamp(stamp.timestamp(), ROME_TZ).date()

        return OutlookResponse(
            species=species,
            area=area,
            issued=issued,
            good_share=self.config.outlook.good_share,
            rain_lead=RainLead(min_days=lead_min, max_days=lead_max),
            rain_tilt=RainTiltBands(
                wetter_pct=self.config.outlook.rain.wetter_pct,
                drier_pct=self.config.outlook.rain.drier_pct,
            ),
            baseline=baseline,
            window=window,
            season_to_date=self._season_to_date(code, species, today.year),
            periods=out,
        )

    def _season_to_date(self, code: str, species: str, year: int) -> SeasonToDate | None:
        seasons = self.store.read_seasons()
        rows = seasons[
            (seasons["area_code"] == code)
            & (seasons["species"] == species)
            & (seasons["year"] == year)
        ]
        if rows.empty:
            return None
        row = rows.iloc[0]
        return SeasonToDate(
            through=_day(row["through"]),
            good_days=max(float(row["good_days"]), 0.0),
            good_days_typical=_number(row["good_days_typical"]),
            rain=_rain(row["rain_mm"], row["rain_normal_mm"]),
            temperature=_temperature(row["temp_c"], row["temp_normal_c"]),
            weather_through=_day(row["weather_through"]),
            sightings=int(row["sightings"]),
        )
