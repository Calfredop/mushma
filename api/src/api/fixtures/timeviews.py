"""Fixture stand-in for the time views (M6): comuni, seasons, the season map, the outlook and the
plausible species.

Deterministic, plausible-looking numbers hashed from the fixture cells, so the frontend has
something shaped exactly like the real history to draw. No real weather or scores behind them.
"""

import calendar
import hashlib
from datetime import date, timedelta

from api.fixtures.cells import CELLS, CellSpec
from api.history.config import load_history_config
from api.history.outlook import outlook_periods, period_starts, tilt
from api.jobs.daily import WINDOW_FORWARD_DAYS
from api.model.rules import load_rules
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
from api.repository import AreaNotFound, SeasonNotFound
from api.species import Species, SpeciesOrCombined
from api.timeutil import today_rome
from api.weather.config import load_weather_config

FIRST_YEAR = 2016
GOOD_SCORE = 0.6
PLAUSIBLE_FIT = 0.5
REGION_NAME = "Toscana"
# (month, day) spans, like the real rule files' season windows.
WINDOWS: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {
    "porcini": ((5, 1), (12, 20)),
    "ovoli": ((6, 1), (11, 30)),
    "gallinacci": ((4, 15), (12, 31)),
    "combined": ((4, 15), (12, 31)),
}
RAIN_LEAD = {"porcini": (10, 16), "ovoli": (10, 20), "gallinacci": (10, 30)}
PROVINCES = {
    "Abetone Cutigliano": "PT",
    "Arcidosso": "GR",
    "Bibbiena": "AR",
    "Camporgiano": "LU",
    "Capoliveri": "LI",
    "Careggine": "LU",
    "Castel del Piano": "GR",
    "Castellina in Chianti": "SI",
    "Castiglione della Pescaia": "GR",
    "Chiusi della Verna": "AR",
    "Fivizzano": "MS",
    "Follonica": "GR",
    "Gaiole in Chianti": "SI",
    "Marradi": "FI",
    "Massa Marittima": "GR",
    "Montalcino": "SI",
    "Palazzuolo sul Senio": "FI",
    "Piancastagnaio": "SI",
    "Poppi": "AR",
    "Portoferraio": "LI",
    "Pratovecchio Stia": "AR",
    "Radda in Chianti": "SI",
    "Radicofani": "SI",
    "Reggello": "FI",
    "San Godenzo": "FI",
    "San Marcello Piteglio": "PT",
    "Santa Fiora": "GR",
    "Sarteano": "SI",
    "Sassetta": "LI",
    "Seggiano": "GR",
    "Sillano Giuncugnano": "LU",
}


def _unit(*parts: object) -> float:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _code(name: str) -> str:
    return name.lower().replace(" ", "-").replace("'", "")


def _comuni() -> dict[str, list[CellSpec]]:
    by_name: dict[str, list[CellSpec]] = {}
    for cell in CELLS:
        by_name.setdefault(cell.comune, []).append(cell)
    return dict(sorted(by_name.items(), key=lambda item: item[0].casefold()))


def _window(species: str, year: int) -> SeasonWindow:
    (m1, d1), (m2, d2) = WINDOWS[species]
    return SeasonWindow(start=date(year, m1, d1), end=date(year, m2, d2))


def _years(today: date) -> list[int]:
    return list(range(FIRST_YEAR, today.year + 1))


def _area(comune: str | None) -> tuple[str, Area]:
    if comune is None:
        return "tuscany", Area(code=None, name=REGION_NAME, kind="region")
    for name in _comuni():
        if _code(name) == comune:
            return name, Area(code=comune, name=name, kind="comune")
    raise AreaNotFound(comune)


def _month_goods(area: str, species: str, year: int, through: date) -> dict[int, float]:
    """Good days per month: a bell over the season window, scaled by a per-year strength."""
    window = _window(species, year)
    strength = 0.4 + 0.9 * _unit(area, species, year, "strength")
    peak = window.start.month + (window.end.month - window.start.month) * 0.7
    goods = {}
    for month in range(window.start.month, window.end.month + 1):
        if date(year, month, 1) > through:
            break
        days = calendar.monthrange(year, month)[1]
        if month == through.month and through.year == year:
            days = through.day
        shape = max(0.0, 1 - abs(month - peak) / 3.5)
        goods[month] = round(min(days, days * 0.6 * shape * strength), 1)
    return goods


def _rain(area: str, key: object, normal: float) -> RainStat:
    return RainStat(
        total_mm=round(normal * (0.55 + 0.9 * _unit(area, key, "rain")), 1), normal_mm=normal
    )


def _temperature(area: str, key: object, normal: float) -> TemperatureStat:
    return TemperatureStat(
        mean_c=round(normal - 1.5 + 3 * _unit(area, key, "temp"), 1), normal_c=normal
    )


def _season(area: str, species: str, year: int, today: date) -> SeasonSummary:
    complete = year < today.year
    through = date(year, 12, 31) if complete else max(today - timedelta(days=1), date(year, 1, 1))
    goods = _month_goods(area, species, year, through)
    typical_goods = [
        sum(
            _month_goods(
                area,
                species,
                y,
                date(y, through.month, min(through.day, calendar.monthrange(y, through.month)[1])),
            ).values()
        )
        for y in range(FIRST_YEAR, today.year)
    ]
    typical_goods.sort()
    window = _window(species, year)
    observed_end = min(window.end, through)
    window_days = max(0, (observed_end - window.start).days + 1)
    peak_month = max(goods, key=goods.get) if goods and max(goods.values()) > 0 else None
    months = [
        MonthStat(
            month=month,
            good_days=good,
            rain=_rain(area, (year, month), 95.0),
            temperature=_temperature(area, (year, month), 12.0 + 8 * (month in (6, 7, 8))),
            sightings=int(4 * _unit(area, species, year, month) ** 3),
        )
        for month, good in goods.items()
    ]
    return SeasonSummary(
        year=year,
        complete=complete,
        through=through,
        good_days=round(sum(goods.values()), 1),
        good_days_typical=typical_goods[len(typical_goods) // 2] if typical_goods else None,
        peak_date=min(date(year, peak_month, 12), through) if peak_month else None,
        peak_share=round(0.3 + 0.6 * _unit(area, species, year, "peak"), 2) if peak_month else 0.0,
        window=window,
        rain=_rain(area, (year, "season"), round(3.2 * window_days, 1)) if window_days else None,
        temperature=_temperature(area, (year, "season"), 15.0) if window_days else None,
        weather_through=observed_end if window_days else None,
        sightings=sum(m.sightings for m in months),
        months=months,
    )


def _baseline(today: date) -> Baseline:
    years = list(range(FIRST_YEAR, today.year))
    return Baseline(weather_years=years, score_years=years)


class FixtureTimeViews:
    def get_comuni(self) -> ComuniResponse:
        return ComuniResponse(
            comuni=[
                Comune(
                    code=_code(name),
                    name=name,
                    province=PROVINCES.get(name, ""),
                    lon=round(sum(c.lon for c in cells) / len(cells), 4),
                    lat=round(sum(c.lat for c in cells) / len(cells), 4),
                    cells=len(cells),
                )
                for name, cells in _comuni().items()
            ]
        )

    def get_seasons(self, species: SpeciesOrCombined, comune: str | None) -> SeasonsResponse:
        today = today_rome()
        key, area = _area(comune)
        return SeasonsResponse(
            species=species,
            area=area,
            good_score=GOOD_SCORE,
            baseline=_baseline(today),
            seasons=[_season(key, species, year, today) for year in _years(today)],
        )

    def get_season_map(self, year: int, species: SpeciesOrCombined) -> SeasonMapResponse:
        today = today_rome()
        years = _years(today)
        if year not in years:
            raise SeasonNotFound(year, years)
        region = _season("tuscany", species, year, today)
        cells = [
            CellSeason(
                cell_id=cell.id,
                lon=cell.lon,
                lat=cell.lat,
                good_days=int(region.good_days * (0.3 + 1.4 * _unit(cell.id, species, year))),
            )
            for cell in CELLS
        ]
        comuni = []
        for name in _comuni():
            season = _season(name, species, year, today)
            comuni.append(
                ComuneSeason(
                    code=_code(name),
                    name=name,
                    good_days=season.good_days,
                    good_days_typical=season.good_days_typical,
                    rain=season.rain,
                    temperature=season.temperature,
                    sightings=season.sightings,
                )
            )
        comuni.sort(key=lambda c: (-c.good_days, c.name))
        return SeasonMapResponse(
            year=year,
            species=species,
            complete=region.complete,
            through=region.through,
            good_score=GOOD_SCORE,
            cells=cells,
            comuni=comuni,
        )

    def get_outlook(self, species: Species, comune: str | None) -> OutlookResponse:
        today = today_rome()
        key, area = _area(comune)
        config = load_history_config()
        window = _window(species, today.year)
        seasonal = load_weather_config().seasonal
        week_reach = seasonal.forecast_days.get("weekly", 0) if seasonal else 0
        weeks, months = period_starts(today, week_reach, config.outlook.months_ahead + 2)
        periods = outlook_periods(
            today,
            WINDOW_FORWARD_DAYS,
            weeks,
            months,
            (window.start, window.end),
            config.outlook.months_ahead,
        )
        past_years = today.year - FIRST_YEAR
        out = []
        for period in periods:
            share = 40 + 120 * _unit(key, species, period.start, "lead")
            normal = round(3.0 * ((period.end - period.start).days + 1), 1)
            out.append(
                OutlookPeriod(
                    start=period.start,
                    end=period.end,
                    kind=period.kind,
                    past_good_years=int(past_years * _unit(key, species, period.start.isoformat())),
                    past_years=past_years,
                    rain=_rain(key, period.start, normal),
                    temperature_anomaly_c=round(-1 + 3 * _unit(key, period.start, "t"), 1),
                    lead_rain_pct=round(share, 1),
                    outlook=tilt(share, config.outlook.rain),
                )
            )
        season = _season(key, species, today.year, today)
        lead_min, lead_max = RAIN_LEAD[species]
        return OutlookResponse(
            species=species,
            area=area,
            issued=today,
            good_share=config.outlook.good_share,
            rain_lead=RainLead(min_days=lead_min, max_days=lead_max),
            rain_tilt=RainTiltBands(
                wetter_pct=config.outlook.rain.wetter_pct,
                drier_pct=config.outlook.rain.drier_pct,
            ),
            baseline=_baseline(today),
            window=window,
            season_to_date=SeasonToDate(
                through=season.through,
                good_days=season.good_days,
                good_days_typical=season.good_days_typical,
                rain=season.rain,
                temperature=season.temperature,
                weather_through=season.weather_through,
                sightings=season.sightings,
            ),
            periods=out,
        )

    def get_species(self, comune: str | None) -> PlausibleSpeciesResponse:
        today = today_rome()
        key, area = _area(comune)
        rules = load_rules()
        profiles = []
        for group, keys in rules.groups.items():
            group_days = {
                year: _season(key, group, year, today).good_days for year in _years(today)
            }
            taxa = [
                TaxonProfile(
                    key=taxon,
                    taxon=rules.species[taxon].taxon,
                    i18n_key=rules.species[taxon].i18n_key,
                    # Squared: most taxa suit a little of an area's woodland, a few most of it.
                    fit_share=round(_unit(key, taxon, "fit") ** 2, 2),
                    seasons=[
                        SpeciesSeason(
                            year=year,
                            good_days=round(days * (0.2 + 0.8 * _unit(key, taxon, year)), 1),
                        )
                        for year, days in group_days.items()
                    ],
                )
                for taxon in keys
            ]
            best = max(t.fit_share for t in taxa)
            profiles.append(
                SpeciesProfile(
                    species=group,
                    fit_share=round(min(1.0, best + 0.15 * _unit(key, group, "fit")), 2),
                    seasons=[
                        SpeciesSeason(year=year, good_days=days)
                        for year, days in group_days.items()
                    ],
                    taxa=taxa,
                )
            )
        return PlausibleSpeciesResponse(
            area=area, plausible_fit=PLAUSIBLE_FIT, good_score=GOOD_SCORE, species=profiles
        )
