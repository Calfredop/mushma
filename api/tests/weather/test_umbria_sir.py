from datetime import date
from io import StringIO

import pandas as pd
import pytest

from api.weather.umbria_sir import gauges_covering, parse_daily

HEADER = (
    '"ID_SENSORE_DETTAGLIO","ID_TIPOLOGIA_SENSORE","STRUMENTO","TIPO_STRUMENTO","UNITA_MISURA",'
    '"ID_STAZIONE","NOME_STAZIONE","COMUNE","LATITUDINE","LONGITUDINE","ANNO","MESE","GIORNO",'
    '"CUMDAY"\n'
)


def csv(*rows: str) -> StringIO:
    return StringIO(HEADER + "".join(row + "\n" for row in rows))


def test_parse_daily_reads_one_rain_value_per_station_and_day() -> None:
    daily = parse_daily(
        csv(
            '12883,"20204","Pluviometro","Pluviometro","mm",25300,"Ponticelli",'
            '"CITTA\' DELLA PIEVE",42.93166667,11.96888889,2026,1,1,7.4',
            '12883,"20204","Pluviometro","Pluviometro","mm",25300,"Ponticelli",'
            '"CITTA\' DELLA PIEVE",42.93166667,11.96888889,2026,1,2,0',
        )
    )

    assert list(daily.columns) == ["code", "name", "comune", "lat", "lon", "date", "mm"]
    assert daily["code"].tolist() == ["25300", "25300"]
    assert daily["date"].tolist() == [date(2026, 1, 1), date(2026, 1, 2)]
    assert daily["mm"].tolist() == [7.4, 0.0]
    assert daily["lat"].iloc[0] == pytest.approx(42.93166667)


def test_parse_daily_drops_missing_values_and_other_units() -> None:
    daily = parse_daily(
        csv(
            '1,"20204","Pluviometro","Pluviometro","mm",100,"A","X",43.0,12.0,2024,5,1,',
            '2,"20204","Pluviometro","Pluviometro","cm",200,"B","Y",43.0,12.0,2024,5,1,3',
            '3,"20204","Pluviometro","Pluviometro","mm",300,"C","Z",43.0,12.0,2024,5,1,-1',
            '4,"20204","Pluviometro","Pluviometro","mm",400,"D","W",43.0,12.0,2024,5,1,2.5',
        )
    )

    assert daily["code"].tolist() == ["400"]


def test_parse_daily_keeps_one_value_when_a_station_has_two_rain_sensors() -> None:
    daily = parse_daily(
        csv(
            '1,"20204","Pluviometro","Pluviometro","mm",100,"A","X",43.0,12.0,2024,5,1,2.0',
            '2,"20204","Pluviometro","Pluviometro","mm",100,"A","X",43.0,12.0,2024,5,1,2.4',
        )
    )

    assert len(daily) == 1
    assert daily["mm"].iloc[0] == pytest.approx(2.2)


def test_gauges_covering_keeps_stations_with_most_days_in_the_window() -> None:
    days = pd.date_range("2024-01-01", "2024-01-10").date
    daily = pd.DataFrame(
        {
            "code": ["full"] * 10 + ["sparse"] * 5,
            "name": ["F"] * 10 + ["S"] * 5,
            "comune": ["X"] * 15,
            "lat": [43.0] * 15,
            "lon": [12.0] * 15,
            "date": list(days) + list(days[:5]),
            "mm": [1.0] * 15,
        }
    )

    gauges = gauges_covering(daily, date(2024, 1, 1), date(2024, 1, 10), min_coverage=0.8)

    assert gauges["code"].tolist() == ["full"]
    assert set(gauges.columns) >= {"code", "name", "comune", "lat", "lon"}


def test_parse_daily_drops_implausible_daily_totals() -> None:
    daily = parse_daily(
        csv(
            '1,"20207","Pluviometro","Pluviometro","mm",100,"Moiano","X",43.0,12.0,2017,10,17,7062.8',
            '1,"20207","Pluviometro","Pluviometro","mm",100,"Moiano","X",43.0,12.0,2017,10,18,246.4',
        )
    )

    assert daily["mm"].tolist() == [246.4]
